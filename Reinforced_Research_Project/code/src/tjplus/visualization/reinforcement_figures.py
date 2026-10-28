"""Figures of the reinforcement experiments, generated only from <out>/summary and <out>/statistics files.
Same palette and style as the original figures (validated categorical order; colour follows the method)."""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .figures import _style, _save, SLOT, INK, INK2, GRID

STYLE = {  # sample level: filled markers; batch level: different hues
    "TJ+N": (SLOT[0], "o"), "Gauss-LOO": (SLOT[2], "^"), "SCP-T-split-N": (SLOT[1], "s"), "ASTM-PI": (SLOT[3], "D"),
    "TJ+H-N": (SLOT[6], "o"), "TJ+G-N": (SLOT[4], "v"), "LGO-CV+N": (SLOT[5], "P"), "ANOVA-PI": (SLOT[7], "X"),
    "Gauss-LGO": ("#8a8984", "^"),
}
SETTING_LABEL = {"season": "season shift", "inst_15016": "15006→15016", "inst_15014": "15006→15014",
                 "inst_15029": "15006→15029"}

def _design_order(df):
    d = df[df["design"] == "random"][["K", "n_g"]].drop_duplicates().sort_values("K")
    return [(int(r.K), int(r.n_g)) for r in d.itertuples()]

def fig_batch_coverage(out, figdir, alpha=0.1):
    s = pd.read_csv(os.path.join(out, "summary", "E10_summary.csv"))
    s = s[(s["alpha"] == alpha) & (s["design"] == "random")]
    order = _design_order(s)
    _style()
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    panels = [("Sample-level intervals", ["TJ+N", "Gauss-LOO", "SCP-T-split-N", "ASTM-PI"]),
              ("Batch-level intervals", ["TJ+H-N", "TJ+G-N", "LGO-CV+N", "ANOVA-PI"])]
    xs = np.arange(len(order))
    for ax, (title, meths) in zip(axes, panels):
        for j, meth in enumerate(meths):
            col, mk = STYLE[meth]
            off = (j - (len(meths) - 1) / 2) * 0.12
            ys, lo, hi, hollow = [], [], [], []
            for (K, ng) in order:
                g = s[(s["K"] == K) & (s["n_g"] == ng) & (s["method"] == meth)]
                ys.append(g["coverage_mean"].mean()); lo.append(g["coverage_mean"].min()); hi.append(g["coverage_mean"].max())
                hollow.append(g["new_frac_inf"].mean() > 0.5)
            ys, lo, hi = map(np.array, (ys, lo, hi))
            ax.vlines(xs + off, lo, hi, color=col, lw=1.0, alpha=0.8)
            ax.plot(xs + off, ys, color=col, lw=1.0, alpha=0.6)
            for x, y, h in zip(xs + off, ys, hollow):
                ax.plot(x, y, mk, color=col, mfc="white" if h else col, mec=col, ms=5)
            ax.plot([], [], mk, color=col, label=meth)
        ax.axhline(1 - alpha, color=INK, lw=0.8, ls="--")
        ax.set_xticks(xs, [f"{K}×{ng}" for K, ng in order])
        ax.set_xlabel("Standards: batches K × standards per batch")
        ax.set_title(title, loc="left", color=INK)
        ax.legend(frameon=False, loc="lower right", ncol=2, handletextpad=0.3, columnspacing=0.8)
    axes[0].set_ylabel("Coverage of samples from new batches")
    axes[0].set_ylim(max(0.0, s["coverage_mean"].min() - 0.05), 1.01)
    _save(fig, figdir, "fig_batch_coverage")

def fig_batch_mechanism(out, figdir, alpha=0.1):
    s = pd.read_csv(os.path.join(out, "summary", "E10_summary.csv"))
    s = s[(s["alpha"] == alpha) & (s["design"] == "random") & (s["method"] == "TJ+N")]
    _style()
    fig, ax = plt.subplots(figsize=(3.5, 2.9))
    cols = {2: SLOT[3], 5: SLOT[1], 10: SLOT[0], 15: SLOT[2], 20: SLOT[6]}
    for K, g in s.groupby("K"):
        ng = int(g["n_g"].iloc[0])
        ax.plot(g["icc_new"], g["coverage_mean"], "o", color=cols.get(int(K), INK2), ms=4.5, label=f"{int(K)}×{ng}")
    ax.axhline(1 - alpha, color=INK, lw=0.8, ls="--")
    ax.set_xlabel("Intra-batch correlation of target errors (ICC)")
    ax.set_ylabel("TJ+N coverage, new batches")
    ax.legend(title="K × n$_g$", frameon=False, fontsize=6.5, title_fontsize=6.5, loc="lower left")
    _save(fig, figdir, "fig_batch_mechanism")

def fig_training_conditional(out, figdir, alpha=0.1):
    p = os.path.join(out, "statistics", "E13_noninferiority_trainingconditional.csv")
    if not os.path.exists(p):
        return
    s = pd.read_csv(p)
    s = s[(s["alpha"] == alpha) & s["method"].isin(["TJ+N", "TJ+", "Gauss-LOO", "SCP-T-split-N"])]
    _style()
    fig, ax = plt.subplots(figsize=(3.5, 2.9))
    meths = ["TJ+N", "TJ+", "Gauss-LOO", "SCP-T-split-N"]
    ms = sorted(s["m"].unique())
    for j, meth in enumerate(meths):
        col, mk = STYLE.get(meth, (SLOT[4], "v"))
        g = s[s["method"] == meth].groupby("m")["tc_share"]
        ax.plot(np.array(ms) + (j - 1.5) * 0.6, g.median().reindex(ms), mk + "-", color=col, ms=4.5, lw=1.0, label=meth)
    ax.set_xlabel("Number of standards m")
    ax.set_ylabel(f"Share of standard sets with\nrealised coverage ≥ {1 - alpha - 0.05:.2f}")
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=6.5, loc="lower right")
    _save(fig, figdir, "fig_training_conditional")

def make_reinforcement_figures(out, figdir):
    fig_batch_coverage(out, figdir)
    fig_batch_mechanism(out, figdir)
    fig_training_conditional(out, figdir)
