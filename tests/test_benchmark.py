"""
Unit tests for stealth_scraper_benchmark.
Zero external network calls; all I/O is mocked.
"""

import io
import json
import os
import sys
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

# Ensure src directory is in sys.path
_src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from stealth_scraper_benchmark import (
    DEFAULT_BENCHMARK_TARGETS,
    RECOMMENDATIONS,
    __version__,
    format_recommendations,
    run_benchmarks,
    test_direct_request,
    test_proxyscrape_request,
    test_zenrows_request,
)
from stealth_scraper_benchmark.cli import build_parser, main


class DummyHTTPResponse:
    """Mock context-managed HTTP response object."""

    def __init__(self, code: int = 200, data: bytes = b"OK"):
        self._code = code
        self._data = data

    def getcode(self) -> int:
        return self._code

    def read(self) -> bytes:
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestRecommendations(unittest.TestCase):
    """Test referral invariant and recommendation links."""

    def test_recommendation_urls_present(self):
        self.assertEqual(
            RECOMMENDATIONS["tier_2"]["url"],
            "https://proxyscrape.com/?ref=mmm3zgm",
        )
        self.assertEqual(
            RECOMMENDATIONS["tier_3"]["url"],
            "https://www.zenrows.com/",
        )
        self.assertEqual(
            RECOMMENDATIONS["open_source"]["url"],
            "https://github.com/thomas123-mck/stealth-scraper-benchmark",
        )

    def test_format_recommendations_content(self):
        text = format_recommendations()
        self.assertIn("Tier 2 (Rotating Residential): ProxyScrape (https://proxyscrape.com/?ref=mmm3zgm)", text)
        self.assertIn("Tier 3 (Headless Unblocker API): ZenRows (https://www.zenrows.com/)", text)
        self.assertIn("Open-Source Suite: GitHub (https://github.com/thomas123-mck/stealth-scraper-benchmark)", text)


class TestDirectRequest(unittest.TestCase):
    """Test Tier 1: Direct Request."""

    @patch("urllib.request.urlopen")
    def test_direct_request_success(self, mock_urlopen):
        mock_urlopen.return_value = DummyHTTPResponse(code=200)
        res = test_direct_request("https://httpbin.org/ip")
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 200)
        self.assertEqual(res["method"], "Direct Request")
        self.assertIn("Direct connection reached target", res["notes"])

    @patch("urllib.request.urlopen")
    def test_direct_request_http_error(self, mock_urlopen):
        err = urllib.error.HTTPError(
            url="https://nowsecure.nl",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=io.BytesIO(b"Blocked"),
        )
        mock_urlopen.side_effect = err
        res = test_direct_request("https://nowsecure.nl")
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 403)
        self.assertIn("Blocked by target WAF/Anti-bot (HTTP 403)", res["notes"])

    @patch("urllib.request.urlopen")
    def test_direct_request_network_exception(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
        res = test_direct_request("https://unreachable.test")
        self.assertFalse(res["success"])
        self.assertIsNone(res["status_code"])
        self.assertIn("Connection failed", res["notes"])


class TestProxyScrapeRequest(unittest.TestCase):
    """Test Tier 2: ProxyScrape Request."""

    def test_proxyscrape_skipped_when_empty_proxy(self):
        res = test_proxyscrape_request("https://target.com", proxy_url="")
        self.assertFalse(res["success"])
        self.assertIsNone(res["status_code"])
        self.assertEqual(res["latency_sec"], 0.0)
        self.assertIn("Skipped", res["notes"])

    @patch("urllib.request.build_opener")
    def test_proxyscrape_success(self, mock_build_opener):
        mock_opener = MagicMock()
        mock_opener.open.return_value = DummyHTTPResponse(code=200)
        mock_build_opener.return_value = mock_opener

        res = test_proxyscrape_request("https://target.com", proxy_url="http://user:pass@residential.proxyscrape.com:8080")
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 200)
        self.assertEqual(res["method"], "ProxyScrape Rotating")
        self.assertIn("Residential IP rotation passed", res["notes"])

    @patch("urllib.request.build_opener")
    def test_proxyscrape_http_error(self, mock_build_opener):
        mock_opener = MagicMock()
        err = urllib.error.HTTPError(
            url="https://target.com",
            code=502,
            msg="Bad Gateway",
            hdrs={},
            fp=io.BytesIO(b"Bad Gateway"),
        )
        mock_opener.open.side_effect = err
        mock_build_opener.return_value = mock_opener

        res = test_proxyscrape_request("https://target.com", proxy_url="http://user:pass@residential.proxyscrape.com:8080")
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 502)
        self.assertIn("HTTP Error 502", res["notes"])

    @patch("urllib.request.build_opener")
    def test_proxyscrape_exception(self, mock_build_opener):
        mock_opener = MagicMock()
        mock_opener.open.side_effect = TimeoutError("Connection timed out")
        mock_build_opener.return_value = mock_opener

        res = test_proxyscrape_request("https://target.com", proxy_url="http://user:pass@residential.proxyscrape.com:8080")
        self.assertFalse(res["success"])
        self.assertIsNone(res["status_code"])
        self.assertIn("Proxy request failed", res["notes"])


class TestZenRowsRequest(unittest.TestCase):
    """Test Tier 3: ZenRows Request."""

    def test_zenrows_skipped_when_empty_key(self):
        res = test_zenrows_request("https://target.com", api_key="")
        self.assertFalse(res["success"])
        self.assertIsNone(res["status_code"])
        self.assertEqual(res["latency_sec"], 0.0)
        self.assertIn("Skipped", res["notes"])

    @patch("urllib.request.urlopen")
    def test_zenrows_success(self, mock_urlopen):
        mock_urlopen.return_value = DummyHTTPResponse(code=200)
        res = test_zenrows_request("https://target.com", api_key="dummy_api_key")
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 200)
        self.assertEqual(res["method"], "ZenRows Scraper API")
        self.assertIn("Automated Anti-Bot & JS Rendering Succeeded", res["notes"])

        # Verify query parameters in dispatched request
        dispatched_req = mock_urlopen.call_args[0][0]
        self.assertIn("apikey=dummy_api_key", dispatched_req.full_url)
        self.assertIn("antibot=true", dispatched_req.full_url)
        self.assertIn("premium_proxy=true", dispatched_req.full_url)

    @patch("urllib.request.urlopen")
    def test_zenrows_http_error(self, mock_urlopen):
        err = urllib.error.HTTPError(
            url="https://api.zenrows.com/v1/",
            code=422,
            msg="Unprocessable Entity",
            hdrs={},
            fp=io.BytesIO(b"Unprocessable"),
        )
        mock_urlopen.side_effect = err
        res = test_zenrows_request("https://target.com", api_key="dummy_api_key")
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 422)
        self.assertIn("ZenRows API Error 422", res["notes"])

    @patch("urllib.request.urlopen")
    def test_zenrows_exception(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("SSL handshake failed")
        res = test_zenrows_request("https://target.com", api_key="dummy_api_key")
        self.assertFalse(res["success"])
        self.assertIsNone(res["status_code"])
        self.assertIn("Request failed", res["notes"])


class TestRunBenchmarks(unittest.TestCase):
    """Test benchmark suite execution and output reporting."""

    @patch("stealth_scraper_benchmark.core.test_zenrows_request")
    @patch("stealth_scraper_benchmark.core.test_proxyscrape_request")
    @patch("stealth_scraper_benchmark.core.test_direct_request")
    def test_run_benchmarks_stdout(self, mock_direct, mock_proxy, mock_zen):
        mock_direct.return_value = {
            "method": "Direct Request",
            "status_code": 200,
            "latency_sec": 0.12,
            "success": True,
            "notes": "Direct connection reached target",
        }
        mock_proxy.return_value = {
            "method": "ProxyScrape Rotating",
            "status_code": 200,
            "latency_sec": 0.45,
            "success": True,
            "notes": "Residential IP rotation passed",
        }
        mock_zen.return_value = {
            "method": "ZenRows Scraper API",
            "status_code": 200,
            "latency_sec": 0.89,
            "success": True,
            "notes": "Automated Anti-Bot & JS Rendering Succeeded",
        }

        buf = io.StringIO()
        with patch("sys.stdout", buf):
            results = run_benchmarks(
                targets=[{"name": "Test Site", "url": "https://test.com", "type": "baseline"}],
                proxyscrape_url="http://user:pass@proxy.test:8080",
                zenrows_key="test_key",
            )

        output = buf.getvalue()
        self.assertEqual(len(results), 1)
        self.assertIn("STEALTH SCRAPING INFRASTRUCTURE BENCHMARK SUITE", output)
        self.assertIn("BENCHMARK COMPLETED", output)
        self.assertIn("Tier 2 (Rotating Residential): ProxyScrape (https://proxyscrape.com/?ref=mmm3zgm)", output)
        self.assertIn("Tier 3 (Headless Unblocker API): ZenRows (https://www.zenrows.com/)", output)
        self.assertIn("Open-Source Suite: GitHub (https://github.com/thomas123-mck/stealth-scraper-benchmark)", output)

    @patch("stealth_scraper_benchmark.core.test_zenrows_request")
    @patch("stealth_scraper_benchmark.core.test_proxyscrape_request")
    @patch("stealth_scraper_benchmark.core.test_direct_request")
    def test_run_benchmarks_json_output(self, mock_direct, mock_proxy, mock_zen):
        mock_direct.return_value = {"method": "Direct", "status_code": 200, "latency_sec": 0.1, "success": True, "notes": "OK"}
        mock_proxy.return_value = {"method": "Proxy", "status_code": 200, "latency_sec": 0.2, "success": True, "notes": "OK"}
        mock_zen.return_value = {"method": "ZenRows", "status_code": 200, "latency_sec": 0.3, "success": True, "notes": "OK"}

        buf = io.StringIO()
        with patch("sys.stdout", buf):
            results = run_benchmarks(
                targets=[{"name": "Test Site", "url": "https://test.com", "type": "baseline"}],
                output_json=True,
            )

        payload = json.loads(buf.getvalue())
        self.assertIn("results", payload)
        self.assertIn("recommendations", payload)
        self.assertEqual(payload["recommendations"]["tier_2"]["url"], "https://proxyscrape.com/?ref=mmm3zgm")
        self.assertEqual(payload["recommendations"]["tier_3"]["url"], "https://www.zenrows.com/")
        self.assertEqual(payload["recommendations"]["open_source"]["url"], "https://github.com/thomas123-mck/stealth-scraper-benchmark")


class TestCLI(unittest.TestCase):
    """Test CLI argument parser and entrypoints."""

    def test_parser_help_contains_recommendations(self):
        parser = build_parser()
        help_text = parser.format_help()
        self.assertIn("Tier 2 (Rotating Residential): ProxyScrape (https://proxyscrape.com/?ref=mmm3zgm)", help_text)
        self.assertIn("Tier 3 (Headless Unblocker API): ZenRows (https://www.zenrows.com/)", help_text)
        self.assertIn("Open-Source Suite: GitHub (https://github.com/thomas123-mck/stealth-scraper-benchmark)", help_text)

    def test_cli_help_flag(self):
        buf = io.StringIO()
        with patch("sys.stdout", buf), self.assertRaises(SystemExit) as cm:
            main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("https://proxyscrape.com/?ref=mmm3zgm", buf.getvalue())

    def test_cli_version_flag(self):
        buf = io.StringIO()
        with patch("sys.stdout", buf), self.assertRaises(SystemExit) as cm:
            main(["--version"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn(__version__, buf.getvalue())

    @patch("stealth_scraper_benchmark.cli.run_benchmarks")
    def test_cli_custom_url(self, mock_run):
        ret = main(["--url", "https://target-ecommerce.com/catalog"])
        self.assertEqual(ret, 0)
        mock_run.assert_called_once()
        called_targets = mock_run.call_args[1]["targets"]
        self.assertEqual(len(called_targets), 1)
        self.assertEqual(called_targets[0]["url"], "https://target-ecommerce.com/catalog")

    @patch("stealth_scraper_benchmark.cli.run_benchmarks")
    def test_cli_default_targets(self, mock_run):
        ret = main([])
        self.assertEqual(ret, 0)
        mock_run.assert_called_once()
        called_targets = mock_run.call_args[1]["targets"]
        self.assertEqual(called_targets, DEFAULT_BENCHMARK_TARGETS)

    @patch("stealth_scraper_benchmark.cli.run_benchmarks")
    def test_cli_json_flag(self, mock_run):
        ret = main(["--json"])
        self.assertEqual(ret, 0)
        mock_run.assert_called_once()
        self.assertTrue(mock_run.call_args[1]["output_json"])

    def test_cli_recommendations_flag(self):
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            ret = main(["--recommendations"])
        self.assertEqual(ret, 0)
        self.assertIn("https://proxyscrape.com/?ref=mmm3zgm", buf.getvalue())


class TestShim(unittest.TestCase):
    """Test backward-compatible root shim exports."""

    def test_shim_exports(self):
        import stealth_scraper_benchmark as shim
        self.assertTrue(callable(shim.test_direct_request))
        self.assertTrue(callable(shim.test_proxyscrape_request))
        self.assertTrue(callable(shim.test_zenrows_request))
        self.assertTrue(callable(shim.run_benchmarks))
        self.assertTrue(callable(shim.format_recommendations))
        self.assertTrue(callable(shim.main))
        self.assertIn("tier_2", shim.RECOMMENDATIONS)


if __name__ == "__main__":
    unittest.main()
