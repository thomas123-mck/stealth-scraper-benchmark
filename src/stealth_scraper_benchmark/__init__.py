"""
Stealth Web Scraping & Anti-Bot Benchmark Toolkit.
Author: Data Engineering & Web Scraping Intelligence
"""

__version__ = "0.1.0"

from stealth_scraper_benchmark.core import (
    DEFAULT_BENCHMARK_TARGETS,
    RECOMMENDATIONS,
    format_recommendations,
    run_benchmarks,
    test_direct_request,
    test_proxyscrape_request,
    test_zenrows_request,
)
from stealth_scraper_benchmark.cli import main

__all__ = [
    "DEFAULT_BENCHMARK_TARGETS",
    "RECOMMENDATIONS",
    "test_direct_request",
    "test_proxyscrape_request",
    "test_zenrows_request",
    "run_benchmarks",
    "format_recommendations",
    "main",
    "__version__",
]
