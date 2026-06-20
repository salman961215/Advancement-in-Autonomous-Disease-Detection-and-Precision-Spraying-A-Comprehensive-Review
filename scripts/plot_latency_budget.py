"""
Latency budget figure for:
"Advancement in Autonomous Disease Detection and Precision Spraying: A Comprehensive Review"

Horizontal bar chart comparing inference / actuation latency of five approaches
against the ~144 ms spray-window budget of a 5 km/h ground sprayer (20 cm footprint).
Log x-axis. Styled to match the paper's existing matplotlib figures (Figs. 2, 5).

Numbers sourced from the manuscript:
  - Edge YOLO (Jetson):        15-35 ms   (Sec. 5.5 A3, Sec. 7.2)
  - Spray-window budget:       ~144 ms    (Sec. 5.4, 7.2)
  - PWM nozzle settling:       180 ms     (Vijayakumar et al. 2026, 0.18 s; Sec. 5.5 A3)
  - Cloud VLM (low):           500 ms     (Sec. 5.5 A3, 7.2)
  - Cloud VLM / MLLM (high):   1500 ms    (Sec. 5.5 A3, 7.2)
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

# ---- global style to match the paper's figures ----
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Nimbus Roman"],
    "font.size": 10,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#333333",
    "savefig.dpi": 300,
})

BUDGET = 144.0  # ms

# Each entry: label, low, high (single-value items have low == high)
items = [
    ("Edge YOLO\n(NVIDIA Jetson)",        15,   35),
    ("Spray-window budget\n(5 km/h, 20 cm)", 144, 144),
    ("PWM nozzle settling\n(Vijayakumar et al., 2026)", 180, 180),
    ("Cloud VLM\n(low estimate)",          500,  500),
    ("Cloud VLM / MLLM\n(high estimate)",  1500, 1500),
]

# Colours: green = within budget, grey = the budget itself, red ramp = over budget
def colour_for(low, high):
    if abs(low - BUDGET) < 1e-6 and abs(high - BUDGET) < 1e-6:
        return "#7F7E78"   # neutral grey: the budget bar itself
    if high <= BUDGET:
        return "#2C8C6E"   # teal-green: fits
    return "#B0492A"       # coral-red: exceeds

labels = [it[0] for it in items]
lows   = np.array([it[1] for it in items], dtype=float)
highs  = np.array([it[2] for it in items], dtype=float)
colours = [colour_for(l, h) for l, h in zip(lows, highs)]

y = np.arange(len(items))[::-1]  # top-to-bottom in listed order

fig, ax = plt.subplots(figsize=(7.0, 3.6))

# Bars: for ranges, draw from low->high; for singletons, draw a thin bar from a small floor.
FLOOR = 8  # ms visual floor on log axis so single-value bars are visible
for yi, (lab, lo, hi, col) in zip(y, [(l, a, b, c) for (l, a, b), c in zip(items, colours)]):
    if hi > lo:  # range
        ax.barh(yi, hi - lo, left=lo, height=0.55, color=col,
                edgecolor="#222222", linewidth=0.6, zorder=3)
        txt = f"{int(lo)}\u2013{int(hi)} ms"
        ax.text(hi * 1.08, yi, txt, va="center", ha="left", fontsize=9, color="#222222")
    else:        # single value
        ax.barh(yi, lo - FLOOR, left=FLOOR, height=0.55, color=col,
                edgecolor="#222222", linewidth=0.6, zorder=3)
        txt = f"{int(lo)} ms"
        ax.text(lo * 1.08, yi, txt, va="center", ha="left", fontsize=9, color="#222222")

# Budget threshold line
ax.axvline(BUDGET, color="#B0492A", linestyle="--", linewidth=1.1, zorder=2)
ax.annotate("144 ms budget", xy=(BUDGET, len(items) - 0.4),
            xytext=(BUDGET, len(items) - 0.18),
            ha="center", va="bottom", fontsize=8.5, color="#B0492A",
            annotation_clip=False)

# Log x-axis
ax.set_xscale("log")
ax.set_xlim(FLOOR, 3200)
ax.set_xticks([10, 30, 100, 144, 300, 1000, 2000])
ax.set_xticklabels(["10", "30", "100", "144", "300", "1000", "2000"])
ax.set_xlabel("Latency from sensing to actuation (ms, log scale)")

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.set_ylim(-0.6, len(items) - 0.4)

# Shade the "exceeds budget" region lightly
ax.axvspan(BUDGET, 3200, color="#B0492A", alpha=0.05, zorder=0)

ax.grid(axis="x", which="major", color="#DDDDDD", linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

legend_handles = [
    Patch(facecolor="#2C8C6E", edgecolor="#222222", linewidth=0.6, label="Fits spray window"),
    Patch(facecolor="#7F7E78", edgecolor="#222222", linewidth=0.6, label="Budget threshold"),
    Patch(facecolor="#B0492A", edgecolor="#222222", linewidth=0.6, label="Exceeds spray window"),
]
ax.legend(handles=legend_handles, loc="center right", bbox_to_anchor=(1.0, 0.62),
          fontsize=8.5, frameon=True, edgecolor="#CCCCCC", framealpha=0.95)

fig.tight_layout()
fig.savefig("/home/claude/latency_budget.pdf", bbox_inches="tight")
fig.savefig("/home/claude/latency_budget.png", bbox_inches="tight", dpi=200)
print("saved pdf and png")
