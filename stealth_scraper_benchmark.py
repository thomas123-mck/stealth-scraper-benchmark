"""
Stealth Web Scraping & Anti-Bot Benchmark Toolkit (Compatibility Shim).
Redirects execution to src/stealth_scraper_benchmark.
"""

import os
import sys

# Ensure src directory is on sys.path and package path is set for submodule resolution
_src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
_pkg_dir = os.path.join(_src_dir, "stealth_scraper_benchmark")
__path__ = [_pkg_dir]

if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from stealth_scraper_benchmark.cli import main
from stealth_scraper_benchmark.core import (
    DEFAULT_BENCHMARK_TARGETS,
    RECOMMENDATIONS,
    format_recommendations,
    run_benchmarks,
    test_direct_request,
    test_proxyscrape_request,
    test_zenrows_request,
)

__all__ = [
    "DEFAULT_BENCHMARK_TARGETS",
    "RECOMMENDATIONS",
    "test_direct_request",
    "test_proxyscrape_request",
    "test_zenrows_request",
    "run_benchmarks",
    "format_recommendations",
    "main",
]

if __name__ == "__main__":
    sys.exit(main())
