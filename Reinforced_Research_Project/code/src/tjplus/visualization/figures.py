"""Publication figures, generated exclusively from machine-readable results (<out>/summary, raw, ...).
Palette: validated categorical order (dataviz reference palette, light mode); colour follows the
method entity; markers give secondary (non-colour) encoding."""
import glob, json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

SLOT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
METHOD_STYLE = {  # colour follows the entity; never re-assigned by rank
    "TJ+N": (SLOT[0], "o"), "SCP-T-split-N": (SLOT[1], "s"), "Gauss-LOO": (SLOT[2], "^"), "ASTM-PI": (SLOT[3], "D"),
    "SCP-S": (SLOT[4], "v"), "WCP-S": (SLOT[5], "P"), "Transport": (SLOT[6], "X"), "LF-conv": (SLOT[7], "*"),
}
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
DS_LABEL = {"corn": "Corn (m5→mp5/mp6, PDS)", "tablets": "Tablets (inst. 1→2, PDS)", "mango": "Mango (seasons 1–3→4, SBC)"}

def _style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
                         "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7, "axes.edgecolor": INK2,
                         "axes.linewidth": 0.6, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
                         "grid.linestyle": "-", "axes.spines.top": False, "axes.spines.right": False,
                         "axes.facecolor": SURF, "figure.facecolor": "white", "lines.linewidth": 1.6,
                         "lines.markersize": 5.5, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "savefig.dpi": 600})

def _save(fig, figdir, name):
    os.makedirs(figdir, exist_ok=True)
    fig.savefig(os.path.join(figdir, name + ".png"), bbox_inches="tight")
    fig.savefig(os.path.join(figdir, name + ".pdf"), bbox_inches="tight")
    plt.close(fig)

def _primary(summary, cfg, alpha=0.1):
    pk = cfg["primary_kind"]
    s = summary[summary["experiment"].str.startswith("E1_main") & (summary["alpha"] == alpha)]
    return s[s.apply(lambda r: r["kind"] == pk[r["dataset"]], axis=1)]

# ------------------------------------------------------------------ Fig 1: workflow schematic (not data)
def fig_workflow(figdir):
    fig, ax = plt.subplots(figsize=(7.2, 3.0)); ax.set_axis_off(); ax.set_xlim(0, 104); ax.set_ylim(-4, 44)
    def box(x, y, w, h, text, fc="#eef4fc", ec=SLOT[0]):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.2", fc=fc, ec=ec, lw=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=6.6, color=INK, linespacing=1.35)
    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=8, lw=0.8, color=INK2))
    box(0.5, 27, 22, 14, "Source domain\n(master / past seasons)\nmodel f; difficulty σ(x)\nfrom T², Q (source only)", "#f4f4f2", INK2)
    box(0.5, 3, 22, 16, "Target domain\nm transfer standards\n(x$^T_i$, [x$^S_i$], y$_i$),\nrandom sample of target", "#f4f4f2", INK2)
    box(28, 14, 21, 15, "For i = 1, …, m:\nre-fit transfer g on the\nm−1 other standards\nμ$_{-i}$ = post ∘ f ∘ g$_{-i}$")
    box(54.5, 14, 21, 15, "Leave-one-standard-out\nnormalised residuals\nR$_i$ = |y$_i$ − μ$_{-i}$(x$_i$)|\n/ σ$_{-i}$(x$_i$)")
    box(81, 14, 22.5, 15, "Jackknife+ interval\nq$^-${μ$_{-i}$(x) − σ$_{-i}$(x)R$_i$},\nq$^+${μ$_{-i}$(x) + σ$_{-i}$(x)R$_i$}\ncoverage ≥ 1 − 2α", "#fdf0ea", SLOT[1])
    arrow(23, 33, 28, 25); arrow(23, 11, 28, 18); arrow(49.5, 21.5, 54.5, 21.5); arrow(76, 21.5, 81, 21.5)
    ax.text(52, -2.5, "Transfer g ∈ {PDS, DS, SBC, none}: the same m standards fit the transfer and calibrate the interval",
            ha="center", fontsize=6.8, color=INK2, style="italic")
    _save(fig, figdir, "fig1_workflow")

# ------------------------------------------------------------------ Fig 2: data overview
def fig_data(raw_dir, figdir):
    import sys
    from ..data.loaders import load_corn, load_tablets, load_mango
    c, t, m = load_corn(raw_dir), load_tablets(raw_dir), load_mango(raw_dir)
    fig, axs = plt.subplots(2, 3, figsize=(7.2, 4.2), gridspec_kw=dict(height_ratios=[1.3, 1]))
    for k, (lab, X) in enumerate([("m5 (master)", c.spectra["m5"]), ("mp5", c.spectra["mp5"]), ("mp6", c.spectra["mp6"])]):
        axs[0, 0].plot(c.wavelengths, X.mean(0), color=SLOT[k], lw=1.2, label=lab)
    for k, (lab, X) in enumerate([("instrument 1 (master)", t.spectra["1"]), ("instrument 2", t.spectra["2"])]):
        axs[0, 1].plot(t.wavelengths, X.mean(0), color=SLOT[k], lw=1.2, label=lab)
    for k, (lab, X) in enumerate([("seasons 1–3 (source)", m.X[m.season <= 3]), ("season 4 (target)", m.X[m.season == 4])]):
        axs[0, 2].plot(m.wavelengths, X.mean(0), color=SLOT[k], lw=1.2, label=lab)
    for a, ttl in zip(axs[0], ["Corn: mean NIR spectra", "Tablets: mean NIR spectra", "Mango: mean NIR spectra (fruit means)"]):
        a.set_title(ttl, loc="left"); a.set_xlabel("Wavelength (nm)"); a.legend(frameon=False)
    axs[0, 0].set_ylabel("Absorbance (a.u.)")
    for k, p in enumerate(c.properties):
        axs[1, 0].boxplot(c.Y[:, k] - c.Y[:, k].mean(), positions=[k], widths=0.5, showfliers=True,
                          medianprops=dict(color=SLOT[0]), boxprops=dict(color=INK2, lw=0.7), whiskerprops=dict(color=INK2, lw=0.7),
                          capprops=dict(color=INK2, lw=0.7), flierprops=dict(markersize=3, markeredgecolor=INK2))
    axs[1, 0].set_xticks(range(4)); axs[1, 0].set_xticklabels(c.properties); axs[1, 0].set_ylabel("Centred value (%)")
    axs[1, 0].set_title("Corn properties (n = 80)", loc="left")
    pool = t.split == "test"
    axs[1, 1].hist(t.Y[~pool, 2], bins=25, color=SLOT[0], alpha=0.85, label="calibrate+validate (source)")
    axs[1, 1].hist(t.Y[pool, 2], bins=25, color=SLOT[1], alpha=0.6, label="test (target pool)")
    axs[1, 1].set_xlabel("Assay (mg)"); axs[1, 1].set_ylabel("Tablets"); axs[1, 1].legend(frameon=False)
    axs[1, 1].set_title("Tablet assay distribution", loc="left")
    axs[1, 2].hist(m.y[m.season <= 3], bins=30, color=SLOT[0], alpha=0.85, density=True, label="seasons 1–3")
    axs[1, 2].hist(m.y[m.season == 4], bins=30, color=SLOT[1], alpha=0.6, density=True, label="season 4")
    axs[1, 2].set_xlabel("Dry matter (%)"); axs[1, 2].set_ylabel("Density"); axs[1, 2].legend(frameon=False)
    axs[1, 2].set_title("Mango dry matter distribution", loc="left")
    fig.tight_layout(); _save(fig, figdir, "fig2_datasets")

# ------------------------------------------------------------------ Fig 3/4: coverage and efficiency vs m
def fig_coverage_vs_m(summary, cfg, figdir, alpha=0.1):
    s = _primary(summary, cfg, alpha)
    meths = ["TJ+N", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "Transport", "LF-conv"]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.9), sharey=True)
    for ax, ds in zip(axs, ["corn", "tablets", "mango"]):
        d = s[s["dataset"] == ds]
        ms = sorted(d["m"].unique())
        for j, meth in enumerate(meths):
            g = d[d["method"] == meth].groupby("m")["coverage_mean"]
            if g.ngroups == 0:
                continue
            mean, lo, hi = g.mean(), g.min(), g.max()
            x = np.array(mean.index) + (j - 3.5) * 0.18 * (ms[-1] - ms[0]) / 20
            col, mk = METHOD_STYLE[meth]
            inf = d[d["method"] == meth].groupby("m")["frac_reps_any_inf"].mean()
            fill = [col if inf.get(mm, 0) < 0.5 else "white" for mm in mean.index]
            ax.vlines(x, lo, hi, color=col, lw=0.8)
            ax.plot(x, mean.values, color=col, lw=1.0, alpha=0.8)
            ax.scatter(x, mean.values, marker=mk, s=22, facecolors=fill, edgecolors=col, linewidths=0.9, zorder=3,
                       label=meth)
        ax.axhline(1 - alpha, color=INK, lw=0.8)
        ax.text(1.0, 1 - alpha, f" {1 - alpha:.2f}", transform=ax.get_yaxis_transform(), fontsize=6.5, color=INK2, va="center", ha="left", clip_on=False)
        ax.set_title(DS_LABEL[ds], loc="left"); ax.set_xlabel("Number of transfer standards m"); ax.set_xticks(ms)
    axs[0].set_ylabel("Empirical coverage (mean over repetitions)")
    axs[0].set_ylim(0, 1.02)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=8, frameon=False, bbox_to_anchor=(0.5, -0.06), handletextpad=0.2, columnspacing=0.9)
    fig.tight_layout(); _save(fig, figdir, "fig3_coverage_vs_m")

def fig_efficiency_vs_m(summary, cfg, figdir, alpha=0.1):
    s = _primary(summary, cfg, alpha)
    meths = ["TJ+N", "SCP-T-split-N", "Gauss-LOO", "LF-conv"]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6))
    for ax, ds in zip(axs, ["corn", "tablets", "mango"]):
        d = s[s["dataset"] == ds].copy()
        d["rel_width"] = d["width_median"] / d["rmsep_mean"]
        for meth in meths:
            g = d[d["method"] == meth]
            if g.empty:
                continue
            gg = g.groupby("m")["rel_width"].median()
            fin = g.groupby("m")["frac_reps_any_inf"].mean() < 0.5
            col, mk = METHOD_STYLE[meth]
            ax.plot(gg.index[fin.values], gg.values[fin.values], color=col, marker=mk, ms=4.5, lw=1.4, label=meth)
        ax.set_title(DS_LABEL[ds], loc="left"); ax.set_xlabel("m"); ax.set_xticks(sorted(d["m"].unique()))
    axs[0].set_ylabel("Median interval width / RMSEP")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.07))
    fig.tight_layout(); _save(fig, figdir, "fig4_width_vs_m")

# ------------------------------------------------------------------ Fig 5: ablation
def fig_ablation(summary, cfg, figdir, alpha=0.1):
    s = _primary(summary, cfg, alpha)
    abl = ["TJ+N", "TJ+", "TCV+N", "TJ-naive-N", "TJ-insample-N", "TJ+N[T2]", "TJ+N[Q]", "SCP-T-split-N"]
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.8))
    for k, ds in enumerate(["corn", "tablets", "mango"]):
        d = s[(s["dataset"] == ds) & s["method"].isin(abl)]
        cov = d.groupby("method")["coverage_mean"].mean().reindex(abl)
        # relative interval score vs TJ+N within scenario
        piv = d.pivot_table(index=["property", "target", "m"], columns="method", values="IS_median")
        rel = (piv.div(piv["TJ+N"], axis=0)).replace([np.inf, -np.inf], np.nan).median().reindex(abl)
        y = np.arange(len(abl)) + (k - 1) * 0.22
        axs[0].scatter(cov.values, y, color=SLOT[k], marker="osD"[k], s=20, label=ds, zorder=3)
        axs[1].scatter(rel.values, y, color=SLOT[k], marker="osD"[k], s=20, label=ds, zorder=3)
    for ax in axs:
        ax.set_yticks(range(len(abl))); ax.set_yticklabels(abl); ax.invert_yaxis()
    axs[1].set_yticklabels([])
    axs[0].axvline(1 - alpha, color=INK, lw=0.8); axs[0].set_xlabel("Mean coverage (nominal 0.90)")
    axs[1].axvline(1.0, color=INK, lw=0.8); axs[1].set_xlabel("Median interval score relative to TJ+N (finite only)")
    axs[0].legend(frameon=False, loc="lower left")
    fig.tight_layout(); _save(fig, figdir, "fig5_ablation")

# ------------------------------------------------------------------ Fig 6: robustness
def fig_robustness(summary, figdir, alpha=0.1):
    s = summary[summary["experiment"].str.startswith("E4_") & (summary["alpha"] == alpha)].copy()
    if s.empty:
        return
    s["variant"] = s["experiment"].str.split("__").str[1]
    order = ["ks", "noise_1000", "noise_300", "noise_100", "shift_1", "shift_-1", "half_source"]
    labels = {"ks": "Kennard–Stone standards", "noise_1000": "noise SNR 1000", "noise_300": "noise SNR 300",
              "noise_100": "noise SNR 100", "shift_1": "λ-shift +1 ch (test)", "shift_-1": "λ-shift −1 ch (test)",
              "half_source": "half source data"}
    meths = ["TJ+N", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S"]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.0), sharey=True)
    for ax, ds in zip(axs, ["corn", "tablets", "mango"]):
        d = s[s["dataset"] == ds]
        for j, meth in enumerate(meths):
            g = d[d["method"] == meth].groupby("variant")["coverage_mean"].mean().reindex(order)
            col, mk = METHOD_STYLE[meth]
            ax.scatter(g.values, np.arange(len(order)) + (j - 2.5) * 0.11, color=col, marker=mk, s=16, label=meth, zorder=3)
        ax.axvline(1 - alpha, color=INK, lw=0.8); ax.set_title(ds.capitalize(), loc="left"); ax.set_xlabel("Mean coverage")
        ax.set_xlim(0, 1.02)
    axs[0].set_yticks(range(len(order))); axs[0].set_yticklabels([labels[o] for o in order]); axs[0].invert_yaxis()
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=6, frameon=False, bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout(); _save(fig, figdir, "fig6_robustness")

# ------------------------------------------------------------------ Fig 7: conditional coverage
def fig_conditional(summary, cfg, figdir, alpha=0.1):
    s = _primary(summary, cfg, alpha)
    meths = ["TJ+N", "SCP-T-split-N", "Gauss-LOO"]
    extra = {"TJ+": ("#7a7974", "o")}
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.5), sharey=True)
    for ax, ds in zip(axs, ["corn", "tablets", "mango"]):
        d = s[(s["dataset"] == ds) & (s["frac_reps_any_inf"] < 0.5)]
        for meth in meths + ["TJ+"]:
            g = d[d["method"] == meth][["cov_sig1", "cov_sig2", "cov_sig3"]].mean()
            col, mk = METHOD_STYLE.get(meth, extra.get(meth))
            ax.plot([1, 2, 3], g.values, color=col, marker=mk, ms=4.5, lw=1.4 if meth != "TJ+" else 1.0,
                    ls="-" if meth != "TJ+" else (0, (3, 2)), label=meth)
        ax.axhline(1 - alpha, color=INK, lw=0.8); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(["low σ", "mid σ", "high σ"])
        ax.set_title(ds.capitalize(), loc="left")
    axs[0].set_ylabel("Coverage within σ(x) tertile")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout(); _save(fig, figdir, "fig7_conditional_coverage")

# ------------------------------------------------------------------ Fig 8: error analysis
def fig_errors(out, figdir):
    fs = {ds: sorted(glob.glob(os.path.join(out, "raw", f"E1_main_{ds}*_samples.csv.gz"))) for ds in ("corn", "tablets", "mango")}
    fs = {k: v for k, v in fs.items() if v}
    if not fs:
        return
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.5), sharey=True)
    for ax, (ds_, fl) in zip(axs, fs.items()):
        d = pd.concat([pd.read_csv(f) for f in fl], ignore_index=True)
        ds = d["dataset"].iloc[0]
        d = d[d["m"] == d["m"].median() if d["m"].median() in d["m"].values else d["m"] == sorted(d["m"].unique())[1]]
        for meth in ["TJ+N", "Gauss-LOO", "ASTM-PI"]:
            g = d[d["method"] == meth].copy()
            g["miss"] = ~((g["y"] >= g["lo"]) & (g["y"] <= g["hi"]))
            g["bin"] = pd.qcut(g["q"].rank(method="first"), 5, labels=False)
            r = g.groupby("bin")["miss"].mean()
            col, mk = METHOD_STYLE[meth]
            ax.plot(r.index + 1, r.values, color=col, marker=mk, ms=4.5, label=meth)
        ax.axhline(0.1, color=INK, lw=0.8)
        ax.set_title(f"{ds.capitalize()} (m = {int(d['m'].iloc[0])})", loc="left"); ax.set_xlabel("Q-residual quintile of test spectrum")
    axs[0].set_ylabel("Miss rate")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout(); _save(fig, figdir, "fig8_error_analysis")

# ------------------------------------------------------------------ Fig 9: timing
def fig_timing(out, figdir):
    f = os.path.join(out, "raw", "E6_timing.csv")
    if not os.path.exists(f):
        return
    d = pd.read_csv(f)
    steps = list(d["step"].unique())
    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    for k, ds in enumerate(["corn", "tablets", "mango"]):
        g = d[d["dataset"] == ds].set_index("step").reindex(steps)
        ax.barh(np.arange(len(steps)) + (k - 1) * 0.26, g["median_s"] * 1000, height=0.24, color=SLOT[k], label=f"{ds} (m={int(g['m'].iloc[0])})")
    ax.set_xscale("log"); ax.set_yticks(range(len(steps))); ax.set_yticklabels([s.replace(" (", "\n(") for s in steps])
    ax.set_xlabel("Median wall-clock time per test batch (ms, log scale)"); ax.legend(frameon=False, fontsize=6.5)
    ax.invert_yaxis(); fig.tight_layout(); _save(fig, figdir, "fig9_timing")

# ------------------------------------------------------------------ Fig 10: coverage distribution over repetitions
def fig_cov_distribution(out, cfg, figdir, alpha=0.1):
    fs = {ds: [f for f in sorted(glob.glob(os.path.join(out, "raw", f"E1_main_{ds}*.csv.gz"))) if "samples" not in f]
          for ds in ("corn", "tablets", "mango")}
    fs = {k: v for k, v in fs.items() if v}
    if not fs:
        return
    meths = ["TJ+N", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S"]
    sel = {"corn": ("protein", "mp5", 15), "tablets": ("assay", "2", 20), "mango": ("dry_matter", "S4", 20)}
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    for ax, ds in zip(axs, ["corn", "tablets", "mango"]):
        if ds not in fs:
            continue
        d = pd.concat([pd.read_csv(f) for f in fs[ds]], ignore_index=True); prop, tgt, m = sel[ds]
        d = d[(d["alpha"] == alpha) & (d["kind"] == cfg["primary_kind"][ds]) & (d["property"] == prop)
              & (d["target"].astype(str) == tgt) & (d["m"] == m)]
        data = [d[d["method"] == mm]["coverage"].to_numpy() for mm in meths]
        parts = ax.violinplot(data, showextrema=False, widths=0.8)
        for b, mm in zip(parts["bodies"], meths):
            b.set_facecolor(METHOD_STYLE[mm][0]); b.set_alpha(0.55); b.set_edgecolor("none")
        ax.scatter(range(1, len(meths) + 1), [np.mean(x) for x in data], color=INK, s=10, zorder=3)
        ax.axhline(1 - alpha, color=INK, lw=0.8)
        ax.set_xticks(range(1, len(meths) + 1)); ax.set_xticklabels(meths, rotation=35, ha="right")
        ax.set_title(f"{ds.capitalize()}: {prop}, m = {m}", loc="left")
    axs[0].set_ylabel("Per-repetition test coverage")
    fig.tight_layout(); _save(fig, figdir, "fig10_coverage_distribution")

def fig_cnn_history(out, figdir):
    f = os.path.join(out, "raw", "E5_cnn_training_history.csv")
    if not os.path.exists(f):
        return
    h = pd.read_csv(f)
    fig, ax = plt.subplots(figsize=(3.5, 2.3))
    ax.plot(h["epoch"], h["train_mse_std"], color=SLOT[0], lw=1.4, label="training")
    ax.plot(h["epoch"], h["val_mse_std"], color=SLOT[1], lw=1.4, label="validation (source)")
    ax.set_xlabel("Epoch"); ax.set_ylabel("MSE (standardised y)"); ax.legend(frameon=False)
    ax.set_title("1D-CNN training (mango, seasons 1–3)", loc="left")
    fig.tight_layout(); _save(fig, figdir, "figS1_cnn_training")

def fig_friedman(out, figdir):
    f = os.path.join(out, "statistics", "friedman.json")
    if not os.path.exists(f):
        return
    fr = json.load(open(f))["median_interval_score"]
    r = pd.Series(fr["mean_ranks"]).sort_values()
    fig, ax = plt.subplots(figsize=(3.5, 2.3))
    ax.hlines(range(len(r)), 1, r.values, color=GRID, lw=1)
    ax.scatter(r.values, range(len(r)), color=[METHOD_STYLE.get(m, ("#7a7974", "o"))[0] for m in r.index], s=24, zorder=3)
    ax.set_yticks(range(len(r))); ax.set_yticklabels(r.index); ax.invert_yaxis()
    ax.set_xlabel("Mean rank of median interval score (1 = best)")
    ax.set_title(f"Friedman χ² = {fr['friedman_chi2']:.1f}, p = {fr['p_value']:.1e} ({fr['n_scenarios']} scenarios)", loc="left", fontsize=7)
    fig.tight_layout(); _save(fig, figdir, "figS2_friedman_ranks")


def fig_graphical_abstract(summary, cfg, figdir, alpha=0.1):
    """Graphical abstract (Elsevier: >= 1328 x 531 px, ~5:2): pipeline + key evidence (mean coverage)."""
    s = _primary(summary, cfg, alpha)
    meths = ["ASTM-PI", "SCP-S", "WCP-S", "Gauss-LOO", "TJ+N"]
    fig = plt.figure(figsize=(8.0, 3.2))
    ax0 = fig.add_axes([0.0, 0.0, 0.42, 1.0]); ax0.set_axis_off(); ax0.set_xlim(0, 10); ax0.set_ylim(0, 10)
    def b(x, y, w, h, t, ec):
        ax0.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.3", fc="white", ec=ec, lw=1.0))
        ax0.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=7.5, color=INK, linespacing=1.3)
    b(0.3, 6.6, 4.2, 2.6, "Master instrument /\npast seasons\nPLS model", INK2)
    b(5.5, 6.6, 4.2, 2.6, "New instrument /\nnew season\nm transfer standards", INK2)
    b(1.2, 2.0, 7.6, 3.0, "Transfer jackknife+:\nre-fit the transfer m times,\nleave-one-standard-out residuals\n→ valid intervals (≥ 1 − 2α)", SLOT[0])
    ax0.add_patch(FancyArrowPatch((2.4, 6.5), (4.0, 4.9), arrowstyle="-|>", mutation_scale=9, lw=0.9, color=INK2))
    ax0.add_patch(FancyArrowPatch((7.6, 6.5), (6.0, 4.9), arrowstyle="-|>", mutation_scale=9, lw=0.9, color=INK2))
    ax = fig.add_axes([0.52, 0.2, 0.46, 0.68])
    dss = ["corn", "tablets", "mango"]
    for j, meth in enumerate(meths):
        vals = [s[(s["dataset"] == ds) & (s["method"] == meth)]["coverage_mean"].mean() for ds in dss]
        col, mk = METHOD_STYLE[meth]
        ax.bar(np.arange(3) + (j - 2) * 0.16, vals, width=0.15, color=col, label=meth, edgecolor=SURF, linewidth=1.0)
    ax.axhline(1 - alpha, color=INK, lw=0.9); ax.text(2.55, 1 - alpha + 0.01, "nominal 0.90", fontsize=6.5, color=INK2, ha="right")
    ax.set_xticks(range(3)); ax.set_xticklabels(["Corn", "Tablets", "Mango"]); ax.set_ylim(0, 1.05)
    ax.set_ylabel("Mean coverage after transfer"); ax.legend(frameon=False, fontsize=6.3, ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.2))
    fig.savefig(os.path.join(figdir, "graphical_abstract.png"), dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(figdir, "graphical_abstract.pdf"), bbox_inches="tight")
    plt.close(fig)

def make_all_figures(out, cfg, log=None):
    _style()
    from ..statistics.analysis import output_dir
    figdir = output_dir(out, "figures")
    summary = pd.read_csv(os.path.join(out, "summary", "summary_all.csv"))
    summary["source"] = summary["source"].astype(str); summary["target"] = summary["target"].astype(str)
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "raw")
    fig_workflow(figdir); fig_data(raw_dir, figdir)
    fig_coverage_vs_m(summary, cfg, figdir); fig_efficiency_vs_m(summary, cfg, figdir)
    fig_ablation(summary, cfg, figdir); fig_robustness(summary, figdir); fig_conditional(summary, cfg, figdir)
    fig_errors(out, figdir); fig_timing(out, figdir); fig_cov_distribution(out, cfg, figdir)
    fig_cnn_history(out, figdir); fig_friedman(out, figdir); fig_graphical_abstract(summary, cfg, figdir)
    if log: log.info(f"figures written to {os.path.abspath(figdir)}")
