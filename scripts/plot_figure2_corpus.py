"""
Figure 2 (corrected) for:
"Advancement in Autonomous Disease Detection and Precision Spraying: A Comprehensive Review"

Annual distribution of the reviewed corpus (2020-2026), organised by the THREE
core review sections, with table-verified counts:
  - Detection (Sec 4) = 69  (47 visual + 22 spectral)
  - Spraying  (Sec 5) = 21
  - Closed-loop (Sec 6) = 41
Grand total 130 unique papers (Baltazar et al. 2021 spans spraying + closed-loop,
counted once in the total; per-section bars therefore sum to 131).

Per-year counts derived from the publication year of every cite key in
Tables 1-2 (detection), 4/6/7 unique (spraying), and 8/9/10 unique (closed-loop).
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Nimbus Roman"],
    "font.size": 10,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#333333",
    "savefig.dpi": 300,
})

years = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]

detection  = [2, 3, 8, 18, 23, 14, 1]   # total 69 (47 visual + 22 spectral)
spraying   = [1, 2, 3, 6, 4, 3, 2]      # total 21
closedloop = [2, 4, 6, 7, 5, 15, 2]     # total 41

assert sum(detection) == 69
assert sum(spraying) == 21
assert sum(closedloop) == 41

x = np.arange(len(years))
w = 0.26

c_det = "#2C8C6E"   # teal-green
c_spr = "#C77F2A"   # amber
c_clo = "#3266AD"   # blue

fig, ax = plt.subplots(figsize=(7.6, 4.1))

# Acceleration band 2023-2025 (indices 3..5), drawn behind bars
ax.axvspan(2.5, 5.5, color="#888780", alpha=0.07, zorder=0)
ax.text(4.0, 24.2, "2023\u20132025 acceleration", ha="center", va="bottom",
        fontsize=8.5, color="#5F5E5A", style="italic")

b1 = ax.bar(x - w, detection,  w, label=f"Detection (n = 69)",
            color=c_det, edgecolor="#1f6650", linewidth=0.5, zorder=3)
b2 = ax.bar(x,      spraying,   w, label=f"Spraying (n = 21)",
            color=c_spr, edgecolor="#8a560f", linewidth=0.5, zorder=3)
b3 = ax.bar(x + w,  closedloop, w, label=f"Closed-loop (n = 41)",
            color=c_clo, edgecolor="#22497d", linewidth=0.5, zorder=3)

# Value labels on each non-zero bar
for bars in (b1, b2, b3):
    for rect in bars:
        h = rect.get_height()
        if h > 0:
            ax.text(rect.get_x() + rect.get_width()/2, h + 0.35, str(int(h)),
                    ha="center", va="bottom", fontsize=8, color="#333333")

ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_xlabel("Year")
ax.set_ylabel("Number of studies")
ax.set_ylim(0, 26)
ax.set_xlim(-0.6, len(years) - 0.4)

ax.grid(axis="y", color="#DDDDDD", linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ax.legend(loc="upper left", fontsize=9, frameon=True,
          edgecolor="#CCCCCC", framealpha=0.95)

fig.tight_layout()
fig.savefig("/home/claude/figure2_corpus.pdf", bbox_inches="tight")
fig.savefig("/home/claude/figure2_corpus.png", bbox_inches="tight", dpi=200)
print("saved; section totals:", sum(detection), sum(spraying), sum(closedloop),
      "| per-section sum:", sum(detection)+sum(spraying)+sum(closedloop))
