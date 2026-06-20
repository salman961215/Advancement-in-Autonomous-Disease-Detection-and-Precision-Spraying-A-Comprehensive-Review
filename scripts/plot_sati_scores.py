#!/usr/bin/env python3
"""
Reproduce the SATI (Sensor--Actuation Tightness Index) stacked-bar figure
from tables/sati_scores.csv.

SATI = 0.30*T_lat + 0.25*S_align + 0.25*A_sem + 0.20*F_close
Theoretical maximum = 0.80 (achieved only with full feedback closure F_close=1).
Empirical ceiling among surveyed systems = 0.54.
"""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tables" / "sati_scores.csv"
OUT = ROOT / "figures" / "fig_sati_scores.png"

WEIGHTS = {"T_lat": 0.30, "S_align": 0.25, "A_sem": 0.25, "F_close": 0.20}
CEILING = 0.54

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 10,
})

rows = list(csv.DictReader(open(SRC)))
# sort descending by SATI so the strongest coupling is on top
rows.sort(key=lambda r: float(r["SATI"]), reverse=True)

labels = [r["reference"] for r in rows]
T = np.array([float(r["T_lat"]) * WEIGHTS["T_lat"] for r in rows])
S = np.array([float(r["S_align"]) * WEIGHTS["S_align"] for r in rows])
A = np.array([float(r["A_sem"]) * WEIGHTS["A_sem"] for r in rows])
F = np.array([float(r["F_close"]) * WEIGHTS["F_close"] for r in rows])
sati = np.array([float(r["SATI"]) for r in rows])

y = np.arange(len(rows))[::-1]

c_T, c_S, c_A, c_F = "#1F4E5F", "#3E8DA3", "#E8B14B", "#C0392B"
c_empty = "#ECECEC"

fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.barh(y, T, color=c_T, label="$T_{lat}$ (temporal latency, w=0.30)")
ax.barh(y, S, left=T, color=c_S, label="$S_{align}$ (spatial alignment, w=0.25)")
ax.barh(y, A, left=T+S, color=c_A, label="$A_{sem}$ (semantic alignment, w=0.25)")
ax.barh(y, F, left=T+S+A, color=c_F, label="$F_{close}$ (feedback closure, w=0.20)")
# faint "missing feedback" extension to the theoretical max where F_close == 0
for yi, (sc, fc) in zip(y, zip(sati, F)):
    if fc == 0:
        ax.barh(yi, 0.80 - sc, left=sc, color=c_empty, edgecolor="none", zorder=0)

ax.axvline(CEILING, color="#C0392B", linestyle="--", linewidth=1.1)
ax.text(CEILING, len(rows)-0.3, f"Empirical\nceiling = {CEILING}",
        color="#C0392B", fontsize=8.5, style="italic", ha="center", va="bottom")

for yi, sc in zip(y, sati):
    ax.text(0.82, yi, f"{sc:.2f}", va="center", ha="left", fontweight="bold", fontsize=9)

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlim(0, 0.9)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
ax.set_xlabel("SATI (composite score, 0--0.8 theoretical maximum)")
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8, frameon=False)

fig.tight_layout()
fig.savefig(OUT, dpi=200, bbox_inches="tight")
print("saved", OUT)
print("mean SATI:", round(sati.mean(), 3), "| range:", sati.min(), "-", sati.max())
