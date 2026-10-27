"""
Stealth Web Scraping & Anti-Bot Benchmark Toolkit
Author: Data Engineering & Web Scraping Intelligence
Purpose: Benchmark scraping success rate against Cloudflare/Akamai using
         Direct Requests vs ProxyScrape Residential Proxies vs ZenRows Scraper API.
"""

import os
import sys
import time
import argparse
from typing import Dict, Any, List
import urllib.request
import urllib.error
import json
import ssl

# Target URLs for anti-bot benchmarks
DEFAULT_BENCHMARK_TARGETS = [
    {"name": "HTTPBin IP Probe", "url": "https://httpbin.org/ip", "type": "baseline"},
    {"name": "Cloudflare Test Site", "url": "https://nowsecure.nl", "type": "cloudflare_challenge"},
    {"name": "E-Commerce Target", "url": "https://shopee.vn", "type": "waf_protected"}
]


def test_direct_request(url: str, timeout: int = 10) -> Dict[str, Any]:
    """Tier 1: Standard direct HTTP request with common User-Agent."""
    start_time = time.time()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=context) as response:
            latency = round(time.time() - start_time, 2)
            return {
                "method": "Direct Request",
                "status_code": response.getcode(),
                "latency_sec": latency,
                "success": response.getcode() == 200,
                "notes": "Direct connection reached target"
            }
    except urllib.error.HTTPError as e:
        latency = round(time.time() - start_time, 2)
        return {
            "method": "Direct Request",
            "status_code": e.code,
            "latency_sec": latency,
            "success": False,
            "notes": f"Blocked by target WAF/Anti-bot (HTTP {e.code})"
        }
    except Exception as e:
        latency = round(time.time() - start_time, 2)
        return {
            "method": "Direct Request",
            "status_code": None,
            "latency_sec": latency,
            "success": False,
            "notes": f"Connection failed: {str(e)[:60]}"
        }


def test_proxyscrape_request(url: str, proxy_url: str, timeout: int = 15) -> Dict[str, Any]:
    """
    Tier 2: ProxyScrape Rotating Residential / Datacenter Proxy.
    proxy_url format: http://user:pass@residential.proxyscrape.com:8080
    """
    if not proxy_url:
        return {
            "method": "ProxyScrape Rotating",
            "status_code": None,
            "latency_sec": 0.0,
            "success": False,
            "notes": "Skipped (PROXYSCRAPE_PROXY_URL not configured)"
        }

    start_time = time.time()
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }
        )
        with opener.open(req, timeout=timeout) as response:
            latency = round(time.time() - start_time, 2)
            return {
                "method": "ProxyScrape Rotating",
                "status_code": response.getcode(),
                "latency_sec": latency,
                "success": response.getcode() == 200,
                "notes": "Residential IP rotation passed"
            }
    except urllib.error.HTTPError as e:
        latency = round(time.time() - start_time, 2)
        return {
            "method": "ProxyScrape Rotating",
            "status_code": e.code,
            "latency_sec": latency,
            "success": False,
            "notes": f"HTTP Error {e.code}"
        }
    except Exception as e:
        latency = round(time.time() - start_time, 2)
        return {
            "method": "ProxyScrape Rotating",
            "status_code": None,
            "latency_sec": latency,
            "success": False,
            "notes": f"Proxy request failed: {str(e)[:60]}"
        }


def test_zenrows_request(url: str, api_key: str, js_render: bool = True, timeout: int = 25) -> Dict[str, Any]:
    """
    Tier 3: ZenRows Scraper API (Auto Anti-Bot & JS Rendering Bypass).
    ZenRows handles headless browser simulation, cookie solving, and CAPTCHA bypass.
    """
    if not api_key:
        return {
            "method": "ZenRows Scraper API",
            "status_code": None,
            "latency_sec": 0.0,
            "success": False,
            "notes": "Skipped (ZENROWS_API_KEY not configured)"
        }

    start_time = time.time()
    params = urllib.parse.urlencode({
        "apikey": api_key,
        "url": url,
        "js_render": "true" if js_render else "false",
        "antibot": "true",
        "premium_proxy": "true"
    })
    zenrows_endpoint = f"https://api.zenrows.com/v1/?{params}"

    try:
        req = urllib.request.Request(zenrows_endpoint)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = round(time.time() - start_time, 2)
            return {
                "method": "ZenRows Scraper API",
                "status_code": response.getcode(),
                "latency_sec": latency,
                "success": response.getcode() == 200,
                "notes": "Automated Anti-Bot & JS Rendering Succeeded"
            }
    except urllib.error.HTTPError as e:
        latency = round(time.time() - start_time, 2)
        return {
            "method": "ZenRows Scraper API",
            "status_code": e.code,
            "latency_sec": latency,
            "success": False,
            "notes": f"ZenRows API Error {e.code}"
        }
    except Exception as e:
        latency = round(time.time() - start_time, 2)
        return {
            "method": "ZenRows Scraper API",
            "status_code": None,
            "latency_sec": latency,
            "success": False,
            "notes": f"Request failed: {str(e)[:60]}"
        }


def run_benchmarks(targets: List[Dict[str, str]]):
    proxyscrape_url = os.environ.get("PROXYSCRAPE_PROXY_URL", "")
    zenrows_key = os.environ.get("ZENROWS_API_KEY", "")

    print("=" * 80)
    print(" STEALTH SCRAPING INFRASTRUCTURE BENCHMARK SUITE")
    print("=" * 80)
    print(f"ProxyScrape configured: {'[YES]' if proxyscrape_url else '[NO] (Set PROXYSCRAPE_PROXY_URL)'}")
    print(f"ZenRows API configured: {'[YES]' if zenrows_key else '[NO] (Set ZENROWS_API_KEY)'}")
    print("-" * 80)

    for item in targets:
        name = item["name"]
        url = item["url"]
        target_type = item["type"]
        print(f"\nTarget: {name} ({target_type})")
        print(f"URL: {url}")
        print("." * 60)

        # 1. Direct
        res_direct = test_direct_request(url)
        status_direct = "[PASS]" if res_direct["success"] else "[BLOCKED]"
        print(f"  - Direct:     {status_direct:<10} HTTP {res_direct['status_code']} | Latency: {res_direct['latency_sec']}s | {res_direct['notes']}")

        # 2. ProxyScrape
        res_proxy = test_proxyscrape_request(url, proxyscrape_url)
        status_proxy = "[PASS]" if res_proxy["success"] else ("[BLOCKED]" if res_proxy["status_code"] else "[SKIPPED]")
        print(f"  - ProxyScrape:{status_proxy:<10} HTTP {res_proxy['status_code']} | Latency: {res_proxy['latency_sec']}s | {res_proxy['notes']}")

        # 3. ZenRows
        res_zenrows = test_zenrows_request(url, zenrows_key)
        status_zen = "[PASS]" if res_zenrows["success"] else ("[BLOCKED]" if res_zenrows["status_code"] else "[SKIPPED]")
        print(f"  - ZenRows:    {status_zen:<10} HTTP {res_zenrows['status_code']} | Latency: {res_zenrows['latency_sec']}s | {res_zenrows['notes']}")

    print("\n" + "=" * 80)
    print(" BENCHMARK COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Scraping Anti-Bot Benchmark")
    parser.add_argument("--url", type=str, help="Single target URL to test")
    args = parser.parse_args()

    if args.url:
        targets = [{"name": "Custom Target", "url": args.url, "type": "custom"}]
    else:
        targets = DEFAULT_BENCHMARK_TARGETS

    run_benchmarks(targets)
