"""Statistical analysis exactly as pre-registered (research_design/preregistration.md).

Outputs (under <out>/):
  summary/summary_all.csv           per-configuration aggregates over repetitions
  statistics/paired_tests.csv       TJ+N vs each method, paired Wilcoxon on per-repetition interval score
  statistics/friedman.json          across-scenario Friedman test + Holm-corrected pairwise Wilcoxon
  statistics.json, metrics.json     machine-readable key numbers used in the manuscript
  tables/*.csv|md                   manuscript tables (generated, never typed by hand)
"""
import glob, json, os
import numpy as np, pandas as pd
from scipy import stats

GROUP = ["experiment", "dataset", "property", "source", "target", "kind", "m", "alpha", "method"]
DEPLOYABLE = ["TJ+N", "TJ+", "SCP-T-split-N", "SCP-T-split", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S"]
B = 2000

def load_raw(out):
    frames = []
    for f in sorted(glob.glob(os.path.join(out, "raw", "E*.csv.gz"))):
        if f.endswith("_samples.csv.gz"):
            continue
        d = pd.read_csv(f)
        d["experiment"] = os.path.basename(f).replace(".csv.gz", "").split("@")[0]
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    dup = df.duplicated(["experiment", "dataset", "property", "source", "target", "kind", "m", "alpha", "method", "rep"]).sum()
    if dup:
        raise RuntimeError(f"{dup} duplicated rows across result chunks")
    df["source"] = df["source"].astype(str); df["target"] = df["target"].astype(str)
    return df

def _boot_mean_ci(x, rng):
    x = np.asarray(x, float)
    idx = rng.integers(0, len(x), (B, len(x)))
    bm = x[idx].mean(1)
    return float(np.quantile(bm, 0.025)), float(np.quantile(bm, 0.975))

def summarise(df):
    rng = np.random.default_rng(20261013)
    rows = []
    for key, g in df.groupby(GROUP, sort=False):
        cov = g["coverage"].to_numpy()
        lo, hi = _boot_mean_ci(cov, rng)
        IS = g["interval_score"].to_numpy()
        fin = np.isfinite(IS)
        alpha = key[GROUP.index("alpha")]
        r = dict(zip(GROUP, key))
        r.update(n_reps=len(g), coverage_mean=cov.mean(), coverage_ci_lo=lo, coverage_ci_hi=hi,
                 coverage_p05=float(np.quantile(cov, 0.05)), coverage_sd=float(cov.std(ddof=1)) if len(g) > 1 else np.nan,
                 width_median=float(np.nanmedian(g["width"])) if g["width"].notna().any() else np.nan,
                 width_mean=float(np.nanmean(g["width"])) if g["width"].notna().any() else np.nan,
                 frac_inf_mean=float(g["frac_inf"].mean()), frac_reps_any_inf=float((~fin).mean()),
                 IS_median=float(np.median(IS)), IS_mean_finite=float(IS[fin].mean()) if fin.any() else np.nan,
                 rmsep_mean=float(g["rmsep"].mean()), miss_lo=float(g["miss_lo"].mean()), miss_hi=float(g["miss_hi"].mean()),
                 under_covering=bool(hi < 1 - alpha))
        for c in ("cov_sig1", "cov_sig2", "cov_sig3", "cov_y1", "cov_y2", "cov_y3"):
            if c in g:
                r[c] = float(g[c].mean())
        rows.append(r)
    return pd.DataFrame(rows)

def _finite_for_ranks(a, b):
    """Replace +inf interval scores by a value larger than every finite score (ranks preserved)."""
    allv = np.r_[a, b]; fin = allv[np.isfinite(allv)]
    big = (fin.max() if fin.size else 1.0) * 10 + 1
    return np.where(np.isfinite(a), a, big), np.where(np.isfinite(b), b, big)

def holm(p):
    p = np.asarray(p, float); n = len(p); order = np.argsort(p)
    adj = np.empty(n); run = 0.0
    for k, i in enumerate(order):
        run = max(run, (n - k) * p[i]); adj[i] = min(1.0, run)
    return adj

def paired_tests(df, ref="TJ+N", alpha_level=0.1):
    d = df[(df["alpha"] == alpha_level)]
    rows = []
    scen_cols = ["experiment", "dataset", "property", "source", "target", "kind", "m"]
    rng = np.random.default_rng(1)
    for key, g in d.groupby(scen_cols, sort=False):
        piv = g.pivot_table(index="rep", columns="method", values="interval_score", aggfunc="first")
        if ref not in piv:
            continue
        block = []
        for meth in piv.columns:
            if meth == ref:
                continue
            a, b = piv[ref].to_numpy(), piv[meth].to_numpy()
            ok = ~(np.isnan(a) | np.isnan(b))
            a, b = _finite_for_ranks(a[ok], b[ok])
            diff = a - b
            if np.allclose(diff, 0):
                p, W, r_rb = 1.0, np.nan, 0.0
            else:
                res = stats.wilcoxon(a, b, zero_method="wilcox", alternative="two-sided")
                p, W = float(res.pvalue), float(res.statistic)
                nz = diff[diff != 0]; rk = stats.rankdata(np.abs(nz))
                r_rb = float((rk[nz > 0].sum() - rk[nz < 0].sum()) / rk.sum())
            raw = (piv[ref] - piv[meth]).to_numpy()
            raw = raw[np.isfinite(raw)]
            med = float(np.median(raw)) if raw.size else np.nan
            if raw.size > 1:
                bm = np.median(raw[rng.integers(0, raw.size, (B, raw.size))], 1)
                ci = (float(np.quantile(bm, .025)), float(np.quantile(bm, .975)))
            else:
                ci = (np.nan, np.nan)
            block.append(dict(zip(scen_cols, key), comparison=f"{ref} vs {meth}", other=meth, n_pairs=int(ok.sum()),
                              wilcoxon_W=W, p_value=p, rank_biserial=r_rb, median_IS_diff=med,
                              median_IS_diff_ci_lo=ci[0], median_IS_diff_ci_hi=ci[1],
                              n_finite_pairs=int(raw.size)))
        if block:
            adj = holm([x["p_value"] for x in block])
            for x, pa in zip(block, adj):
                x["p_holm"] = float(pa)
            rows += block
    return pd.DataFrame(rows)

def friedman(summary, primary_kind, alpha_level=0.1, methods=DEPLOYABLE, ref="TJ+N"):
    s = summary[(summary["experiment"].str.startswith("E1_main")) & (summary["alpha"] == alpha_level)]
    s = s[s.apply(lambda r: r["kind"] == primary_kind[r["dataset"]], axis=1)]
    s = s[s["method"].isin(methods)]
    scen = ["dataset", "property", "target", "m"]
    out = {}
    for metric, col in (("median_interval_score", "IS_median"), ("coverage_shortfall", None)):
        if col is None:
            s = s.assign(shortfall=np.maximum(0, (1 - alpha_level) - s["coverage_mean"]))
            col = "shortfall"
        piv = s.pivot_table(index=scen, columns="method", values=col, aggfunc="first").dropna()
        M = piv.to_numpy()
        M = np.where(np.isfinite(M), M, np.nanmax(M[np.isfinite(M)]) * 10 + 1)
        chi, p = stats.friedmanchisquare(*[M[:, j] for j in range(M.shape[1])])
        ranks = pd.DataFrame(np.apply_along_axis(stats.rankdata, 1, M), columns=piv.columns).mean().sort_values()
        pw = []
        for j, meth in enumerate(piv.columns):
            if meth == ref:
                continue
            a, b = M[:, list(piv.columns).index(ref)], M[:, j]
            if np.allclose(a, b):
                pw.append((meth, 1.0, 0.0)); continue
            res = stats.wilcoxon(a, b)
            nz = (a - b)[a != b]; rk = stats.rankdata(np.abs(nz))
            pw.append((meth, float(res.pvalue), float((rk[nz > 0].sum() - rk[nz < 0].sum()) / rk.sum())))
        adj = holm([x[1] for x in pw])
        out[metric] = dict(n_scenarios=int(M.shape[0]), methods=list(piv.columns), friedman_chi2=float(chi), p_value=float(p),
                           mean_ranks=ranks.to_dict(),
                           pairwise_vs_ref=[dict(method=m_, p=p_, p_holm=float(pa), rank_biserial=r_)
                                            for (m_, p_, r_), pa in zip(pw, adj)])
    return out

def _fmt_cov(r):
    return f"{r.coverage_mean:.3f} [{r.coverage_ci_lo:.3f}, {r.coverage_ci_hi:.3f}]"

def output_dir(out, kind):
    """Full mode (<root>/results) writes tables/figures next to results; quick mode keeps them inside."""
    base = os.path.join(out, "..") if os.path.basename(os.path.normpath(out)) == "results" else out
    d = os.path.join(base, kind); os.makedirs(d, exist_ok=True); return d

def _write_table(df, out, name, caption):
    path = os.path.join(output_dir(out, "tables"), name)
    df.to_csv(path + ".csv", index=False)
    with open(path + ".md", "w") as f:
        f.write(f"**{caption}**\n\n" + df.to_markdown(index=False) + "\n")

def make_tables(summary, tests, fr, cfg, out):
    pk = cfg["primary_kind"]; a = cfg["primary_alpha"]
    s = summary[(summary["alpha"] == a)]
    main = s[s["experiment"].str.startswith("E1_main") & s.apply(lambda r: r["kind"] == pk[r["dataset"]], axis=1)]
    order = ["TJ+N", "TJ+", "SCP-T-split-N", "SCP-T-split", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "Transport", "LF-conv"]
    # Table 2: main results pooled over properties/targets per dataset and m (mean of scenario means)
    t = main[main["method"].isin(order)].groupby(["dataset", "m", "method"]).agg(
        coverage=("coverage_mean", "mean"), coverage_min=("coverage_mean", "min"), p05=("coverage_p05", "mean"),
        width_median=("width_median", "median"), IS_median=("IS_median", "median"), frac_inf=("frac_reps_any_inf", "mean"),
        n_under=("under_covering", "sum"), n_scen=("under_covering", "size")).reset_index()
    t["method"] = pd.Categorical(t["method"], order); t = t.sort_values(["dataset", "m", "method"])
    _write_table(t.round(4), out, "table2_main_results",
                 f"Main results (alpha={a}, primary transfer pipeline). Coverage = mean over scenarios of mean per-repetition coverage; n_under = scenarios flagged under-covering (95% CI upper bound < 1-alpha).")
    # Per-scenario detail
    det = main[main["method"].isin(order)].copy()
    det["coverage [95% CI]"] = det.apply(_fmt_cov, axis=1)
    det = det[["dataset", "property", "source", "target", "m", "method", "coverage [95% CI]", "coverage_p05", "width_median",
               "IS_median", "frac_reps_any_inf", "rmsep_mean", "under_covering"]]
    _write_table(det.round(4), out, "tableS1_main_results_by_scenario", "Main results per scenario (alpha=0.1, primary pipeline).")
    # Table 3: ablation
    abl = ["TJ+N", "TJ+", "TCV+N", "TJ-naive-N", "TJ-insample-N", "TJ+N[T2]", "TJ+N[Q]", "SCP-T-split-N"]
    t3 = main[main["method"].isin(abl)].groupby(["dataset", "method"]).agg(
        coverage=("coverage_mean", "mean"), coverage_min=("coverage_mean", "min"), IS_median=("IS_median", "median"),
        width_median=("width_median", "median"), n_under=("under_covering", "sum"), n_scen=("under_covering", "size"),
        cov_sig1=("cov_sig1", "mean"), cov_sig3=("cov_sig3", "mean")).reset_index()
    t3["method"] = pd.Categorical(t3["method"], abl); t3 = t3.sort_values(["dataset", "method"])
    _write_table(t3.round(4), out, "table3_ablation", "Ablation of TJ+N components (alpha=0.1, primary pipeline, pooled over m/properties/targets).")
    # Table 4: robustness
    rob = s[s["experiment"].str.startswith("E4_")].copy()
    rob["variant"] = rob["experiment"].str.split("__").str[1]
    t4 = rob.groupby(["dataset", "variant", "method"]).agg(coverage=("coverage_mean", "mean"), coverage_min=("coverage_mean", "min"),
                                                           IS_median=("IS_median", "median"), n_under=("under_covering", "sum"),
                                                           n_scen=("under_covering", "size")).reset_index()
    _write_table(t4.round(4), out, "table4_robustness", "Robustness (E4), alpha=0.1.")
    # Table 5: generalisation (reverse direction, ridge, CNN) + other transfer pipelines from E1
    gen = s[s["experiment"].str.startswith("E5_")]
    t5 = gen.groupby(["experiment", "dataset", "method"]).agg(coverage=("coverage_mean", "mean"), coverage_min=("coverage_mean", "min"),
                                                             IS_median=("IS_median", "median"), width_median=("width_median", "median"),
                                                             rmsep=("rmsep_mean", "mean"), n_under=("under_covering", "sum"),
                                                             n_scen=("under_covering", "size")).reset_index()
    _write_table(t5.round(4), out, "table5_generalisation", "Generalisation (E5): reverse transfer direction, ridge and 1D-CNN source models, alpha=0.1.")
    other = s[s["experiment"].str.startswith("E1_main") & s["method"].isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S"])]
    t5b = other.groupby(["dataset", "kind", "method"]).agg(coverage=("coverage_mean", "mean"), coverage_min=("coverage_mean", "min"),
                                                          IS_median=("IS_median", "median"), rmsep=("rmsep_mean", "mean"),
                                                          n_under=("under_covering", "sum"), n_scen=("under_covering", "size")).reset_index()
    _write_table(t5b.round(4), out, "table5b_transfer_pipelines", "All transfer pipelines (E1), alpha=0.1.")
    # Table 7: sensitivity (alpha, window, LV)
    sa = summary[summary["experiment"].str.startswith("E1_main") & summary.apply(lambda r: r["kind"] == pk[r["dataset"]], axis=1)
                 & summary["method"].isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S"])]
    t7a = sa.groupby(["dataset", "alpha", "method"]).agg(nominal=("alpha", lambda x: 1 - x.iloc[0]), coverage=("coverage_mean", "mean"),
                                                        coverage_min=("coverage_mean", "min"), frac_inf=("frac_reps_any_inf", "mean"),
                                                        n_under=("under_covering", "sum"), n_scen=("under_covering", "size")).reset_index()
    _write_table(t7a.round(4), out, "table7a_alpha_sensitivity", "Sensitivity to the miscoverage level alpha (primary pipelines).")
    sw = s[s["experiment"].str.startswith("E7_")].copy(); sw["setting"] = sw["experiment"].str.split("__").str[1]
    t7b = sw.groupby(["dataset", "setting", "method"]).agg(coverage=("coverage_mean", "mean"), coverage_min=("coverage_mean", "min"),
                                                          IS_median=("IS_median", "median"), rmsep=("rmsep_mean", "mean"),
                                                          n_under=("under_covering", "sum"), n_scen=("under_covering", "size")).reset_index()
    _write_table(t7b.round(4), out, "table7b_window_lv_sensitivity", "Sensitivity to PDS half-window (hw) and number of latent variables (lv offset).")
    # Table 8: paired tests (primary pipeline, alpha=0.1)
    if len(tests):
        tt = tests[tests["experiment"].str.startswith("E1_main") & tests.apply(lambda r: r["kind"] == pk[r["dataset"]], axis=1)]
        t8 = tt.groupby(["dataset", "other"]).agg(n_scen=("p_holm", "size"), n_sig_TJ_better=("p_holm", lambda x: 0),
                                                  median_rank_biserial=("rank_biserial", "median")).reset_index()
        better = tt[(tt["p_holm"] < 0.05) & (tt["median_IS_diff"] < 0)].groupby(["dataset", "other"]).size()
        worse = tt[(tt["p_holm"] < 0.05) & (tt["median_IS_diff"] > 0)].groupby(["dataset", "other"]).size()
        t8["n_sig_TJ_better"] = [int(better.get((d, o), 0)) for d, o in zip(t8["dataset"], t8["other"])]
        t8["n_sig_TJ_worse"] = [int(worse.get((d, o), 0)) for d, o in zip(t8["dataset"], t8["other"])]
        _write_table(t8.round(4), out, "table8_paired_tests",
                     "Paired Wilcoxon signed-rank tests of per-repetition interval score, TJ+N vs each method (Holm-corrected within scenario; alpha=0.1; primary pipeline). Negative rank-biserial = TJ+N lower (better) score.")

def analyse_all(out, cfg, log=None):
    df = load_raw(out)
    os.makedirs(os.path.join(out, "summary"), exist_ok=True); os.makedirs(os.path.join(out, "statistics"), exist_ok=True)
    summary = summarise(df)
    summary.to_csv(os.path.join(out, "summary", "summary_all.csv"), index=False)
    tests = paired_tests(df)
    tests.to_csv(os.path.join(out, "statistics", "paired_tests.csv"), index=False)
    fr = friedman(summary, cfg["primary_kind"])
    json.dump(fr, open(os.path.join(out, "statistics", "friedman.json"), "w"), indent=2)
    make_tables(summary, tests, fr, cfg, out)
    # key numbers for the manuscript
    pk = cfg["primary_kind"]
    main = summary[summary["experiment"].str.startswith("E1_main") & (summary["alpha"] == cfg["primary_alpha"])
                   & summary.apply(lambda r: r["kind"] == pk[r["dataset"]], axis=1)]
    metrics = {}
    for meth, g in main.groupby("method"):
        metrics[meth] = dict(n_scenarios=int(len(g)), mean_coverage=float(g["coverage_mean"].mean()),
                             min_coverage=float(g["coverage_mean"].min()), n_under_covering=int(g["under_covering"].sum()),
                             median_IS=float(g["IS_median"].median()), frac_reps_infinite=float(g["frac_reps_any_inf"].mean()))
    json.dump(dict(primary_alpha=cfg["primary_alpha"], by_method=metrics), open(os.path.join(out, "metrics.json"), "w"), indent=2)
    json.dump(dict(friedman=fr, n_paired_tests=int(len(tests)),
                   description="Paired Wilcoxon tests in statistics/paired_tests.csv; Friedman across E1 scenarios"),
              open(os.path.join(out, "statistics.json"), "w"), indent=2)
    if log: log.info(f"analysis done: {len(summary)} summary rows, {len(tests)} paired tests")
    return summary, tests, fr
