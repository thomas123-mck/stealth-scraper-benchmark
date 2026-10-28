"""
Stealth Web Scraping & Anti-Bot Benchmark Toolkit - CLI Entrypoint
"""

import argparse
import sys
from typing import List, Optional

from stealth_scraper_benchmark import __version__
from stealth_scraper_benchmark.core import (
    DEFAULT_BENCHMARK_TARGETS,
    format_recommendations,
    run_benchmarks,
)


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser with recommendation epilog."""
    parser = argparse.ArgumentParser(
        prog="stealth-benchmark",
        description="Stealth Web Scraping & Anti-Bot Infrastructure Benchmark Toolkit",
        epilog=format_recommendations(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--url",
        type=str,
        help="Single target URL to benchmark (e.g. https://target.com/catalog)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output benchmark results as structured JSON",
    )
    parser.add_argument(
        "--recommendations",
        action="store_true",
        help="Display recommended proxy and anti-bot infrastructure providers",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI main entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.recommendations:
        print(format_recommendations())
        return 0

    if args.url:
        targets = [{"name": "Custom Target", "url": args.url, "type": "custom"}]
    else:
        targets = DEFAULT_BENCHMARK_TARGETS

    run_benchmarks(targets=targets, output_json=args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
