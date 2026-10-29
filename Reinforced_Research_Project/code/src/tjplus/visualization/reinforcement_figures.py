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
              ("Batch-level intervals", ["TJ+H-N", "Gauss-LGO", "LGO-CV+N", "ANOVA-PI"])]
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
            ax.plot([], [], mk, color=col, label={"TJ+H-N": "TJ+B"}.get(meth, meth))
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
    fig_application(out, figdir)

# ------------------------------------------------------------------ schematic figures (not data)
def fig_overview(figdir, name="fig1_overview", size=(7.2, 2.15)):
    """Fig. 1: the practical workflow, in plain words."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    _style()
    fig, ax = plt.subplots(figsize=size); ax.set_axis_off(); ax.set_xlim(-1.5, 105.5); ax.set_ylim(-3, 27)
    def box(x, y, w, h, title, body, ec, fc):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.2", fc=fc, ec=ec, lw=0.9))
        ax.text(x + w / 2, y + h - 2.6, title, ha="center", va="top", fontsize=6.9, color=INK, weight="bold")
        ax.text(x + w / 2, y + h - 7.6, body, ha="center", va="top", fontsize=6.2, color=INK, linespacing=1.35)
    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=8, lw=0.8, color=INK2))
    box(0.5, 5, 22, 20, "1. Collect standards", "m reference samples,\nmeasured on the new\ninstrument or season,\nfrom many batches", INK2, "#f4f4f2")
    box(27.5, 5, 22, 20, "2. Transfer as usual", "fit PDS, DS or slope/\nbias correction on all\nm standards; the old\nmodel stays unchanged", INK2, "#f4f4f2")
    box(54.5, 5, 22, 20, "3. Leave one out", "re-fit the transfer m\ntimes, each time without\none standard (or batch);\nkeep the left-out error", SLOT[0], "#eef4fc")
    box(81.5, 5, 22, 20, "4. Report an interval", "combine the m left-out\npredictions and errors\ninto a 90% interval for\neach new sample (Eq. 3)", SLOT[1], "#fdf0ea")
    for x in (23, 50, 77):
        arrow(x, 15, x + 4.5, 15)
    ax.text(52, -2, "No extra reference analyses are needed: the same standards fit the transfer and set the interval.",
            ha="center", fontsize=6.8, color=INK2, style="italic")
    _save(fig, figdir, name)

def graphical_abstract(out, figdir):
    """Graphical abstract: the batch finding in one panel, plus the recipe."""
    s = pd.read_csv(os.path.join(out, "summary", "E10_summary.csv"))
    s = s[(s["alpha"] == 0.1) & (s["design"] == "random")]
    _style()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw={"width_ratios": [1.15, 1]})
    order = _design_order(s); xs = np.arange(len(order))
    for meth, lab in (("TJ+N", "leave one standard out"), ("TJ+H-N", "leave one batch out"), ("Gauss-LOO", "Gaussian ± t·RMSE")):
        col, mk = STYLE[meth]
        ys, hol = [], []
        for K, ng in order:
            g = s[(s["K"] == K) & (s["n_g"] == ng) & (s["method"] == meth)]
            ys.append(g["coverage_mean"].mean()); hol.append(g["new_frac_inf"].mean() > 0.5)
        a1.plot(xs, ys, "-", color=col, lw=1.0, alpha=0.7)
        for x, y, h in zip(xs, ys, hol):
            a1.plot(x, y, mk, color=col, mfc="white" if h else col, ms=5)
        a1.plot([], [], mk + "-", color=col, label=lab)
    a1.axhline(0.9, color=INK, ls="--", lw=0.8)
    a1.set_xticks(xs, [f"{K}×{ng}" for K, ng in order]); a1.set_xlabel("20 standards: batches × samples per batch")
    a1.set_ylabel("Coverage, new batches"); a1.set_title("Mango fruit, new consignments", loc="left")
    a1.legend(frameon=False, fontsize=6.3, loc="lower right", title="hollow = no finite interval", title_fontsize=6)
    a2.set_axis_off()
    a2.text(0.0, 0.95, "After moving an NIR calibration:", fontsize=8, weight="bold", va="top", color=INK)
    tips = ["1  Do not reuse the old uncertainty formula", "2  Take standards from many batches",
            "3  Re-fit the transfer leaving one out", "4  Report the resulting 90% interval",
            "5  Watch for drift (Q residual)"]
    for i, t in enumerate(tips):
        a2.text(0.0, 0.78 - i * 0.15, t, fontsize=7.3, va="top", color=INK)
    _save(fig, figdir, "graphical_abstract_revised")

def fig_application(out, figdir):
    p = os.path.join(out, "summary", "E14_summary.csv")
    if not os.path.exists(p):
        return
    s = pd.read_csv(p)
    s = s[s["kind"] == "sbc"]
    meths = [("Point", "point\nrule"), ("ASTM-PI", "ASTM-\nPI"), ("Gauss-LOO", "Gauss-\nLOO"), ("TJ+N", "TJ+N"), ("TJ+H-N", "TJ+B")]
    designs = sorted({(int(k), int(n)) for k, n in zip(s["K"], s["n_g"])})
    cols = {2: SLOT[3], 10: SLOT[0], 20: SLOT[2]}
    _style()
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    w = 0.8 / len(designs); xs = np.arange(len(meths))
    for j, (K, ng) in enumerate(designs):
        g = s[(s["K"] == K) & (s["n_g"] == ng)]
        for ax, col in zip(axes, ["immature_passed", "referred"]):
            vals = [100 * g[g["method"] == m][col].mean() for m, _ in meths]
            lo = [100 * g[g["method"] == m][col].min() for m, _ in meths]
            hi = [100 * g[g["method"] == m][col].max() for m, _ in meths]
            pos = xs + (j - (len(designs) - 1) / 2) * w
            ax.bar(pos, vals, width=w * 0.92, color=cols.get(K, INK2),
                   label=f"{K}×{ng}" + (" (instruments only)" if K == 20 else ""))
            ax.vlines(pos, lo, hi, color=INK, lw=0.7)
    axes[0].set_ylabel("Immature fruit passed as mature (%)")
    axes[1].set_ylabel("Fruit referred for re-measurement (%)")
    axes[0].set_title("(a) Consumer risk", loc="left"); axes[1].set_title("(b) Price: fruit to re-check", loc="left")
    for ax in axes:
        ax.set_xticks(xs, [lab for _, lab in meths], rotation=0)
        ax.grid(axis="x", visible=False)
    axes[0].legend(title="consignments × fruit", frameon=False, fontsize=6.5, title_fontsize=6.5)
    _save(fig, figdir, "fig_application")
