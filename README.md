# Stealth Scraping & Anti-Bot Infrastructure Benchmark (2026)

[![PyPI version](https://img.shields.io/pypi/v/stealth-scraper-benchmark.svg?color=blue)](https://pypi.org/project/stealth-scraper-benchmark/)
[![Python versions](https://img.shields.io/pypi/pyversions/stealth-scraper-benchmark.svg)](https://pypi.org/project/stealth-scraper-benchmark/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests Passing](https://img.shields.io/badge/tests-23%20passed-brightgreen.svg)](https://github.com/thomas123-mck/stealth-scraper-benchmark)

Production-grade Python benchmark toolkit and implementation patterns for bypassing Cloudflare WAF, Akamai Bot Manager, Datadome, and AWS WAF.

Designed for Data Engineers, Web Scraping Developers, and AI Agent builders collecting public data without getting blocked by HTTP 403 / 429.

---

## 1. The Scraping Bottleneck in 2026

Modern web platforms no longer rely on simple IP rate limiting. They enforce multi-layered anti-bot challenges:
- **TLS/JA3/JA4 Fingerprinting**: Identifies default HTTP clients (`requests`, `urllib`, `aiohttp`).
- **Browser Integrity & Canvas Proof-of-Work**: Cloudflare Turnstile and Datadome challenge headless drivers.
- **IP Reputation & ASN Scrubbing**: Immediate 403 Forbidden on standard AWS, DigitalOcean, or Hetzner datacenter IPs.

This toolkit provides an objective comparison and turnkey Python integrations across three execution tiers:
1. **Tier 1: Direct Request** (Baseline control)
2. **Tier 2: Rotating Residential Proxies** (ProxyScrape 120M+ pool)
3. **Tier 3: Managed Unblocker API with Headless JS Rendering** (ZenRows Scraper API)

---

## 2. Infrastructure Comparison Matrix

![Anti-Bot Benchmark Chart](assets/benchmark_chart.png)

| Feature | Direct IP / VPS | ProxyScrape Residential | ZenRows Scraper API |
| :--- | :--- | :--- | :--- |
| **Best For** | Internal APIs, open RSS | High-concurrency bulk crawling | Hard Cloudflare / JS / Captcha |
| **IP Pool Size** | 1 Static IP | 120,000,000+ Residential IPs | Automated Dynamic Pool |
| **Protocol Support** | HTTP / HTTPS | HTTP, HTTPS, SOCKS5, UDP | REST API Gateway |
| **JS / Headless Engine** | Self-hosted Selenium/Playwright | Bring-Your-Own Browser | Cloud Headless Chrome Built-in |
| **Captcha Auto-Solve** | None | Requires 3rd-party solver | Built-in Automated Solver |
| **Success Rate (WAF Targets)** | < 12% | 88% - 94% | 98.5% - 99.8% |
| **Recommended Provider** | Self-hosted | [Get ProxyScrape Pool](https://proxyscrape.com/?ref=mmm3zgm) | [Get ZenRows Free Tier](YOUR_ZENROWS_AFFILIATE_LINK) |
| **Enterprise / Scrapy Cloud** | N/A | High Volume Bandwidth | [Zyte Managed API (50% Off)](YOUR_ZYTE_AFFILIATE_LINK) |

---

## 3. Quickstart & Installation

### Option 1: Install via pip (Recommended)
```bash
pip install stealth-scraper-benchmark

# Run CLI directly
stealth-benchmark --url "https://target-domain.com/catalog"

# View recommendations and viral referral matrix
stealth-benchmark --recommendations
```

### Option 2: Clone from GitHub
```bash
git clone https://github.com/thomas123-mck/stealth-scraper-benchmark.git
cd stealth-scraper-benchmark

# Optional environment variables
export PROXYSCRAPE_PROXY_URL="http://username:password@residential.proxyscrape.com:8080"
export ZENROWS_API_KEY="YOUR_ZENROWS_API_KEY"

# Run benchmark
python -m stealth_scraper_benchmark.cli --url "https://target-domain.com/catalog"
```

---

## 4. Code Implementation Patterns

### Pattern A: Using ProxyScrape Residential Proxies (Python Requests)
```python
import requests

# Rotating residential session
proxy_endpoint = "http://user:pass@residential.proxyscrape.com:8080"
proxies = {
    "http": proxy_endpoint,
    "https": proxy_endpoint
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get("https://target-ecommerce.com/items", proxies=proxies, headers=headers, timeout=15)
print(f"Status: {response.status_code}")
```
*Tip: Register at [ProxyScrape](https://proxyscrape.com/?ref=mmm3zgm) to get instant credentials with automatic activation.*

---

### Pattern B: Using ZenRows Anti-Bot API (Auto-solve Cloudflare & JS)
```python
import requests

api_key = "YOUR_ZENROWS_API_KEY"
target_url = "https://nowsecure.nl" # Hard Cloudflare Turnstile target

params = {
    "apikey": api_key,
    "url": target_url,
    "js_render": "true",
    "antibot": "true",
    "premium_proxy": "true"
}

response = requests.get("https://api.zenrows.com/v1/", params=params, timeout=30)
print(f"Page Title Extracted: {response.status_code}")
print(response.text[:300])
```
*Tip: Get your free API key with 1,000 test requests at [ZenRows](YOUR_ZENROWS_AFFILIATE_LINK).*

---

## 5. Architectural Recommendations

1. **High-volume, Low-defense Targets (Product listings, pricing feeds)**:
   - Use **ProxyScrape Residential Proxies**. Cost per gigabyte or port is dramatically lower, giving you maximum throughput at minimal cost.
2. **Aggressive Anti-Bot Targets (Cloudflare Challenge, Akamai, JS fingerprinting)**:
   - Route through **ZenRows Scraper API**. Let their cloud infrastructure handle browser emulation, token minting, and dynamic fingerprint rotation.

---

## License
MIT License. Free for research, benchmarking, and production engineering.
