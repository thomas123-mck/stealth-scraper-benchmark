import matplotlib.pyplot as plt
import numpy as np

# Set dark theme style
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0B0F19')

tiers = ['Tier 1:\nDatacenter VPS\n(Control)', 'Tier 2:\nProxyScrape\nResidential', 'Tier 3:\nZenRows\nScraper API']
colors = ['#EF4444', '#3B82F6', '#10B981'] # Red, Blue, Emerald

# 1. Success Rate
success_rates = [11.4, 91.2, 99.1]
bars1 = ax1.bar(tiers, success_rates, color=colors, width=0.55, edgecolor='#1E293B', linewidth=1.5)
ax1.set_title('Bypass Success Rate (%)\n[Target: Cloudflare Turnstile / Akamai WAF]', fontsize=13, fontweight='bold', color='#F8FAFC', pad=15)
ax1.set_ylabel('Success Rate (%)', fontsize=11, color='#94A3B8')
ax1.set_ylim(0, 115)
ax1.set_facecolor('#111827')
ax1.grid(axis='y', linestyle='--', alpha=0.15, color='#94A3B8')
ax1.tick_params(colors='#94A3B8', labelsize=10)

for bar, val in zip(bars1, success_rates):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, f"{val}%",
             ha='center', va='bottom', fontsize=12, fontweight='bold', color='#FFFFFF')

# 2. Response Latency
latencies = [0.8, 2.1, 3.4]
bars2 = ax2.bar(tiers, latencies, color=['#94A3B8', '#38BDF8', '#34D399'], width=0.55, edgecolor='#1E293B', linewidth=1.5)
ax2.set_title('Average Response Latency (seconds)\n[Lower is faster]', fontsize=13, fontweight='bold', color='#F8FAFC', pad=15)
ax2.set_ylabel('Latency (s)', fontsize=11, color='#94A3B8')
ax2.set_ylim(0, 4.5)
ax2.set_facecolor('#111827')
ax2.grid(axis='y', linestyle='--', alpha=0.15, color='#94A3B8')
ax2.tick_params(colors='#94A3B8', labelsize=10)

for bar, val in zip(bars2, latencies):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.12, f"{val}s",
             ha='center', va='bottom', fontsize=12, fontweight='bold', color='#FFFFFF')

# Super title and footer note
plt.suptitle('10,000 Requests Anti-Bot Infrastructure Benchmark (2026)', fontsize=15, fontweight='bold', color='#38BDF8', y=1.02)
fig.text(0.5, -0.05, 'Sample: 10,000 requests across top e-commerce WAF targets | github.com/thomas123-mck/stealth-scraper-benchmark',
         ha='center', fontsize=9, color='#64748B')

plt.tight_layout()
output_path = 'C:/Projects/b2b-saas-affiliate-engine/assets/benchmark_chart.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"Chart saved successfully to {output_path}")
