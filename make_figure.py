"""Figure: privacy-relevant instances, claimed level vs. the three cost models."""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def v(i, m):
    return json.load(open(f"results/{i}__{m}.json"))["min_rop_log2"]

# (label, instance id, claimed value or None)
ROWS = [
    ("EVOLVE", "evolve_hide", 119),
    ("EVOLVED ($k$=1)", "evolved_hide_k1", 172.2),
    ("Epoque IBE, n=300, $\\sigma$=3.2", "epoque_ibe_n300_s3.2", 128),
    ("Epoque IBE, n=300, $\\sigma$=1", "epoque_ibe_n300_s1.0", 128),
    ("Aranha et al. 2021 (hiding)", "abgst21_com_hide", 100),
    ("Farzaliyev et al. 2021 (RLWE)", "fwk21_rlwe", 180),
    ("Aranha et al. 2023 (BGV)", "abgs_bgv", 168),
    ("Hough et al. (RLWE)", "hough_rlwe", 128),
    ("Hough et al. (NTRU)", "hough_ntru", 128),
    ("Farzaliyev et al. 2025 (BGV)", "farz_bgv", 192),
    ("PQKryvos (MLWE)", "pqk_hide", 150),
    ("Boyen et al. 2020 (LWE)", "bhm_lwe", 240),
    ("Bootle et al. (MLWE)", "blm_mlwe", 128),
    ("Bootle et al. (MLWR)", "blm_mlwr", 128),
]
MODELS = [("core265", "0.265$\\beta$", "#2a78d6", "o"),
          ("core292", "0.292$\\beta$", "#eb6834", "s"),
          ("matzov", "MATZOV", "#1baf7a", "^")]

plt.rcParams.update({"font.size": 7, "font.family": "serif"})
fig, ax = plt.subplots(figsize=(3.45, 3.5))
ys = list(range(len(ROWS)))[::-1]
for y, (lab, i, cl) in zip(ys, ROWS):
    vals = [v(i, m) for m, *_ in MODELS]
    ax.plot([min(vals), max(vals)], [y, y], color="#b0b0aa", lw=1.2, zorder=1)
    for (m, name, c, mk), x in zip(MODELS, vals):
        ax.scatter(x, y, s=16, color=c, marker=mk, zorder=3, edgecolor="white", linewidth=0.5)
    ax.scatter(cl, y, s=34, marker="|", color="black", zorder=4, linewidth=1.2)
ax.axvline(128, color="#888", lw=0.6, ls=":", zorder=0)
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in ROWS])
ax.set_xlabel("log$_2$ cost of the best attack")
ax.set_xlim(30, 280)
ax.grid(axis="x", color="#e6e6e3", lw=0.5); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
handles = [plt.Line2D([], [], ls="", marker=mk, color=c, label=name, markersize=4) for _, name, c, mk in MODELS]
handles.append(plt.Line2D([], [], ls="", marker="|", color="black", label="claimed", markersize=6))
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.4, 1.0), ncol=4, frameon=False, fontsize=6, handletextpad=0.1, columnspacing=0.8)
fig.tight_layout()
fig.savefig("fig_models.pdf"); fig.savefig("fig_models.png", dpi=200)
print("ok")
