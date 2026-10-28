"""Analysis of the reinforcement experiments E10-E13 (research_design/revised_experimental_protocol.md).

Outputs under <out>/:
  summary/E10_summary.csv, summary/E11_summary.csv
  statistics/E11_paired_tests.csv, statistics/E12_mechanism.csv, statistics/E13_*.csv
  statistics_reinforcement.json   key numbers (machine-readable; used by the manuscript builder)
  tables/E10_*.md, tables/E11_*.md, tables/E13_*.md
"""
import glob, json, os
import numpy as np, pandas as pd
from scipy import stats
from .analysis import _boot_mean_ci, paired_tests, holm

NI_MARGIN = 0.02
TC_MARGIN = 0.05

def _load(raw_dir, pattern, usecols=None):
    frames = []
    for f in sorted(glob.glob(os.path.join(raw_dir, pattern))):
        if f.endswith("_samples.csv.gz"):
            continue
        d = pd.read_csv(f, usecols=usecols)
        d["experiment"] = os.path.basename(f).replace(".csv.gz", "").split("@")[0]
        frames.append(d)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def _cov_summary(df, keys, cov_col, rng):
    rows = []
    for key, g in df.groupby(keys, sort=False):
        c = g[cov_col].to_numpy(float)
        c = c[np.isfinite(c)]
        if not len(c):
            continue
        lo, hi = _boot_mean_ci(c, rng)
        alpha = dict(zip(keys, key))["alpha"]
        rows.append(dict(zip(keys, key), n_reps=len(c), coverage_mean=c.mean(), ci_lo=lo, ci_hi=hi,
                         under=bool(hi < 1 - alpha), noninferior=bool(lo >= 1 - alpha - NI_MARGIN),
                         tc_share=float(np.mean(c >= 1 - alpha - TC_MARGIN))))
    return pd.DataFrame(rows)

# ----------------------------------------------------------------------------- E10
E10_KEYS = ["setting", "kind", "design", "K", "n_g", "m", "alpha", "method"]

def analyse_e10(raw_dir, out, log=None):
    d = _load(raw_dir, "E10_batch*.csv.gz")
    if d.empty:
        return {}
    dup = d.duplicated(E10_KEYS + ["rep"]).sum()
    if dup:
        raise RuntimeError(f"E10: {dup} duplicated rows")
    rng = np.random.default_rng(20261021)
    s = _cov_summary(d, E10_KEYS, "new_coverage", rng)
    extra = d.groupby(E10_KEYS, sort=False).agg(
        same_coverage=("same_coverage", "mean"), new_coverage_fruit=("new_coverage_fruit", "mean"),
        new_median_width=("new_median_width", "median"), new_frac_inf=("new_frac_inf", "mean"),
        new_IS_median=("new_interval_score", "median"), icc_new=("icc_new", "mean"),
        icc_std_loo=("icc_std_loo", "mean"), rmsep_new=("rmsep_new", "mean"),
        new_n_batches=("new_n_batches", "mean")).reset_index()
    s = s.merge(extra, on=E10_KEYS)
    os.makedirs(os.path.join(out, "summary"), exist_ok=True)
    s.to_csv(os.path.join(out, "summary", "E10_summary.csv"), index=False, float_format="%.6g")
    a = s[s["alpha"] == 0.1]
    rnd = a[a["design"] == "random"]
    res = {}
    # H10a: sample-level TJ+N with K = 2
    k2 = rnd[(rnd["K"] == 2) & (rnd["method"] == "TJ+N")]
    res["h10a_tjn_under_K2"] = f"{int(k2['under'].sum())}/{len(k2)}"
    res["h10a_tjn_cov_K2"] = f"{k2['coverage_mean'].min():.2f}–{k2['coverage_mean'].max():.2f}"
    for meth in ("TJ+", "Gauss-LOO", "SCP-T-split-N", "ASTM-PI", "SCP-S", "LGO-CV+N", "Gauss-LGO", "ANOVA-PI"):
        x = rnd[(rnd["K"] == 2) & (rnd["method"] == meth)]
        res[f"K2_under_{meth}"] = f"{int(x['under'].sum())}/{len(x)}"
    # under-coverage of TJ+N by K (random designs)
    for K in sorted(rnd["K"].unique()):
        x = rnd[(rnd["K"] == K) & (rnd["method"] == "TJ+N")]
        res[f"tjn_under_K{K}"] = f"{int(x['under'].sum())}/{len(x)}"
        res[f"tjn_cov_K{K}"] = f"{x['coverage_mean'].min():.2f}–{x['coverage_mean'].max():.2f}"
    # H10b: TJ+G(-N) where bounded (all alphas)
    gb = s[(s["design"] == "random") & s["method"].isin(["TJ+G", "TJ+G-N", "TJ+H", "TJ+H-N"]) & (s["new_frac_inf"] < 0.5)]
    for meth in ("TJ+G", "TJ+G-N", "TJ+H", "TJ+H-N", "ANOVA-PI"):
        x = s[(s["design"] == "random") & (s["method"] == meth) & (s["new_frac_inf"] < 0.5)]
        res[f"bounded_under_{meth}"] = f"{int(x['under'].sum())}/{len(x)}"
    res["h10b_tjg_under_bounded"] = f"{int(gb['under'].sum())}/{len(gb)}"
    res["h10b_tjg_cov_bounded_a01"] = (lambda x: f"{x.min():.2f}–{x.max():.2f}")(
        gb[gb["alpha"] == 0.1]["coverage_mean"])
    # H10c: n_g = 1, sample-level TJ+N
    ng1 = s[(s["design"] == "random") & (s["n_g"] == 1) & (s["method"] == "TJ+N")]
    res["h10c_tjn_under_ng1_allalpha"] = f"{int(ng1['under'].sum())}/{len(ng1)}"
    # H10d: mechanism (K = 2 cells, alpha = 0.1)
    if len(k2) >= 4:
        deficit = 0.9 - k2["coverage_mean"]
        rho, p = stats.spearmanr(k2["icc_new"], deficit)
        res["h10d_spearman_icc_deficit"] = float(rho); res["h10d_p"] = float(p)
        res["icc_range"] = f"{s['icc_new'].min():.2f}–{s['icc_new'].max():.2f}"
    # chronological design
    ch = a[a["design"] == "chrono"]
    for meth in ("TJ+N", "TJ+H-N", "TJ+G-N", "Gauss-LOO", "Gauss-LGO", "ANOVA-PI", "ASTM-PI"):
        x = ch[ch["method"] == meth]
        res[f"chrono_under_{meth}"] = f"{int(x['under'].sum())}/{len(x)}"
        res[f"chrono_cov_{meth}"] = f"{x['coverage_mean'].min():.2f}–{x['coverage_mean'].max():.2f}"
    # same-batch coverage of TJ+N (K=2): standards are exchangeable with same-batch samples
    res["K2_tjn_same_cov"] = f"{k2['same_coverage'].min():.2f}–{k2['same_coverage'].max():.2f}"
    _table_e10(s, out)
    if log: log.info(f"E10 analysed: {len(d)} rows")
    return res

def _table_e10(s, out):
    os.makedirs(os.path.join(out, "tables"), exist_ok=True)
    a = s[(s["alpha"] == 0.1)].copy()
    a["design_lab"] = a.apply(lambda r: f"{'chronological' if r['design'] == 'chrono' else 'random'} {int(r['K'])}×{int(r['n_g'])}", axis=1)
    meths = ["TJ+N", "TJ+H-N", "TJ+G-N", "LGO-CV+N", "Gauss-LOO", "Gauss-LGO", "ANOVA-PI", "ASTM-PI"]
    lines = ["| Design (K × n_g) | Cells | " + " | ".join(meths) + " |", "|:--|--:|" + "--:|" * len(meths)]
    order = sorted(a["design_lab"].unique(), key=lambda x: (x.startswith("chrono"), -int(x.split()[1].split("×")[1]), int(x.split()[1].split("×")[0])))
    for lab in order:
        g = a[a["design_lab"] == lab]
        cells = []
        for mth in meths:
            x = g[g["method"] == mth]
            if x.empty:
                cells.append("–"); continue
            inf = x["new_frac_inf"].mean()
            if inf > 0.5:
                cells.append(f"unbounded ({inf:.0%})")
            else:
                cells.append(f"{x['coverage_mean'].mean():.3f} ({int(x['under'].sum())}/{len(x)})")
        n = len(g[g["method"] == "TJ+N"])
        lines.append(f"| {lab} | {n} | " + " | ".join(cells) + " |")
    open(os.path.join(out, "tables", "E10_batch_alpha010.md"), "w").write("\n".join(lines) + "\n")
    s.to_csv(os.path.join(out, "tables", "E10_batch_summary.csv"), index=False, float_format="%.4g")

# ----------------------------------------------------------------------------- E11 / E12
E11_KEYS = ["experiment", "dataset", "property", "source", "target", "kind", "m", "alpha", "method"]

def analyse_e11(raw_dir, out, log=None):
    d = _load(raw_dir, "E11_classical_*.csv.gz")
    if d.empty:
        return {}
    d["source"] = d["source"].astype(str); d["target"] = d["target"].astype(str)
    dup = d.duplicated(E11_KEYS + ["rep"]).sum()
    if dup:
        raise RuntimeError(f"E11: {dup} duplicated rows")
    rng = np.random.default_rng(20261022)
    s = _cov_summary(d, E11_KEYS, "coverage", rng)
    med = d.groupby(E11_KEYS, sort=False).agg(IS_median=("interval_score", "median"), width_median=("width", "median"),
                                              frac_inf=("frac_inf", "mean")).reset_index()
    s = s.merge(med, on=E11_KEYS)
    s.to_csv(os.path.join(out, "summary", "E11_summary.csv"), index=False, float_format="%.6g")
    res = {}
    rows = []
    for (ds, kind), g in s.groupby(["dataset", "kind"]):
        for meth, gm in g.groupby("method"):
            r = dict(dataset=ds, kind=kind, method=meth)
            for al in (0.05, 0.1, 0.2):
                x = gm[gm["alpha"] == al]
                r[f"under_{al}"] = f"{int(x['under'].sum())}/{len(x)}"
            ref = g[(g["method"] == "TJ+N") & (g["alpha"] == 0.1)].set_index(["property", "target", "m"])["IS_median"]
            x = gm[gm["alpha"] == 0.1].set_index(["property", "target", "m"])["IS_median"]
            rel = (x / ref.reindex(x.index)).replace([np.inf, -np.inf], np.nan)
            r["rel_IS_median_a01"] = float(rel.median()) if rel.notna().any() else np.nan
            rows.append(r)
    t = pd.DataFrame(rows)
    os.makedirs(os.path.join(out, "statistics"), exist_ok=True)
    t.to_csv(os.path.join(out, "statistics", "E11_validity_by_dataset.csv"), index=False)
    # overall counts per method and alpha
    for meth in s["method"].unique():
        for al in (0.05, 0.1, 0.2):
            x = s[(s["method"] == meth) & (s["alpha"] == al)]
            res[f"E11_under_{meth}_{al}"] = f"{int(x['under'].sum())}/{len(x)}"
    sb = s[s["kind"] == "sbc"]
    for meth in ("OLS-PI", "TJ+N", "Gauss-LOO", "Boot-T"):
        for al in (0.05, 0.1, 0.2):
            x = sb[(sb["method"] == meth) & (sb["alpha"] == al)]
            res[f"E11_sbc_under_{meth}_{al}"] = f"{int(x['under'].sum())}/{len(x)}"
    # small-m Boot-T
    bt = s[(s["method"] == "Boot-T") & (s["alpha"] == 0.1)]
    res["E11_boot_under_m10"] = f"{int(bt[bt['m'] == 10]['under'].sum())}/{int((bt['m'] == 10).sum())}"
    res["E11_boot_cov_range"] = f"{bt['coverage_mean'].min():.2f}–{bt['coverage_mean'].max():.2f}"
    # paired interval-score tests vs TJ+N at alpha = 0.1, among non-under-covering methods
    pt = paired_tests(d.assign(experiment=d["experiment"]), ref="TJ+N", alpha_level=0.1)
    pt.to_csv(os.path.join(out, "statistics", "E11_paired_tests.csv"), index=False, float_format="%.6g")
    s01 = s[s["alpha"] == 0.1].set_index(["experiment", "property", "target", "kind", "m", "method"])["under"]
    def ok(r, meth):
        k = (r["experiment"], r["property"], r["target"], r["kind"], r["m"], meth)
        return k in s01.index and not s01[k]
    for meth in ("OLS-PI", "Boot-T", "ASTM-T", "Gauss-LOO", "Gauss-LOO-N"):
        x = pt[pt["other"] == meth]
        x = x[[ok(r, meth) and ok(r, "TJ+N") for _, r in x.iterrows()]]
        better_tjn = int(((x["p_holm"] < 0.05) & (x["rank_biserial"] < 0)).sum())
        better_oth = int(((x["p_holm"] < 0.05) & (x["rank_biserial"] > 0)).sum())
        res[f"E11_IS_{meth}"] = dict(n_both_valid=len(x), tjn_better=better_tjn, other_better=better_oth)
    _table_e11(t, out)
    res.update(analyse_e12(d, s, out))
    if log: log.info(f"E11 analysed: {len(d)} rows")
    return res

def _table_e11(t, out):
    meths = ["TJ+N", "TJ+", "Gauss-LOO", "Gauss-LOO-N", "ASTM-T", "OLS-PI", "Boot-T", "SCP-T-split-N"]
    labs = {"corn": "Corn", "tablets": "Tablets", "mango": "Mango (season)", "mango_inst": "Mango (instruments)"}
    lines = ["| Data set | Pipeline | " + " | ".join(meths) + " |", "|:--|:--|" + "--:|" * len(meths)]
    for ds in ("corn", "tablets", "mango", "mango_inst"):
        for kind in ("pds", "sbc"):
            g = t[(t["dataset"] == ds) & (t["kind"] == kind)]
            if g.empty:
                continue
            cells = []
            for mth in meths:
                x = g[g["method"] == mth]
                cells.append("–" if x.empty else f"{x['under_0.05'].iloc[0]} · {x['under_0.1'].iloc[0]} · {x['under_0.2'].iloc[0]}")
            lines.append(f"| {labs[ds]} | {kind.upper()} | " + " | ".join(cells) + " |")
    open(os.path.join(out, "tables", "E11_classical_validity.md"), "w").write("\n".join(lines) + "\n")

def analyse_e12(d, s, out):
    """Scenario-level association between error shape and the deficit of Gaussian-type intervals (alpha = 0.05)."""
    keys = ["experiment", "dataset", "property", "target", "kind", "m"]
    st = d[(d["method"] == "TJ+N") & (d["alpha"] == 0.1)].groupby(keys).agg(
        skew=("err_skew", "median"), exkurt=("err_exkurt", "median"), ratio=("rmsep_over_rmseloo", "median"),
        bias=("err_bias_rel", "median"), rho_sigma=("spearman_abs_err_sigma", "median")).reset_index()
    res = {}
    rows = []
    for meth in ("Gauss-LOO", "OLS-PI", "Boot-T", "TJ+N"):
        x = s[(s["method"] == meth) & (s["alpha"] == 0.05)][keys + ["coverage_mean", "under"]]
        m = st.merge(x, on=keys)
        if len(m) < 5:
            continue
        m["deficit"] = 0.95 - m["coverage_mean"]
        for feat in ("ratio", "exkurt", "skew", "bias", "rho_sigma"):
            rho, p = stats.spearmanr(m[feat], m["deficit"], nan_policy="omit")
            rows.append(dict(method=meth, feature=feat, spearman=float(rho), p=float(p), n=len(m)))
            res[f"E12_{meth}_{feat}"] = round(float(rho), 2)
        # flagged vs not flagged comparison of the LOO-scale ratio
        res[f"E12_{meth}_ratio_flagged"] = float(m[m["under"]]["ratio"].median()) if m["under"].any() else np.nan
        res[f"E12_{meth}_ratio_ok"] = float(m[~m["under"]]["ratio"].median()) if (~m["under"]).any() else np.nan
    pd.DataFrame(rows).to_csv(os.path.join(out, "statistics", "E12_mechanism.csv"), index=False, float_format="%.4g")
    st.to_csv(os.path.join(out, "statistics", "E12_error_shape_by_scenario.csv"), index=False, float_format="%.4g")
    return res

# ----------------------------------------------------------------------------- E13 (re-analysis of the original study)
PRIMARY = {"corn": "pds", "tablets": "pds", "mango": "sbc"}

def analyse_e13(orig_dir, out, log=None):
    cols = ["dataset", "property", "source", "target", "kind", "m", "alpha", "method", "rep", "coverage"]
    d = pd.concat([_load(os.path.join(orig_dir, "raw"), p, cols) for p in ("E1_main_*.csv.gz", "E8_*.csv.gz")],
                  ignore_index=True)
    prim = d[((d["dataset"].map(PRIMARY) == d["kind"])) | (d["dataset"] == "mango_inst")]
    rng = np.random.default_rng(20261023)
    keys = ["experiment", "dataset", "property", "source", "target", "kind", "m", "alpha", "method"]
    s = _cov_summary(prim, keys, "coverage", rng)
    s.to_csv(os.path.join(out, "statistics", "E13_noninferiority_trainingconditional.csv"), index=False, float_format="%.6g")
    res = {}
    for meth in ("TJ+N", "TJ+", "Gauss-LOO", "SCP-T-split-N", "ASTM-PI"):
        for al in (0.05, 0.1, 0.2):
            x = s[(s["method"] == meth) & (s["alpha"] == al)]
            res[f"E13_NI_{meth}_{al}"] = f"{int(x['noninferior'].sum())}/{len(x)}"
        x = s[(s["method"] == meth) & (s["alpha"] == 0.1)]
        res[f"E13_tc_{meth}_median"] = round(float(x["tc_share"].median()), 3)
        res[f"E13_tc_{meth}_min"] = round(float(x["tc_share"].min()), 3)
    # scenario-clustered CI: resample repetitions jointly across all scenarios of a data set
    rows = []
    for (ds, al, meth), g in prim.groupby(["dataset", "alpha", "method"]):
        piv = g.pivot_table(index="rep", columns=["property", "target", "kind", "m"], values="coverage", aggfunc="first")
        rep_mean = piv.mean(1).to_numpy()
        lo, hi = _boot_mean_ci(rep_mean, rng)
        rows.append(dict(dataset=ds, alpha=al, method=meth, n_scen=piv.shape[1], n_reps=piv.shape[0],
                         coverage=float(rep_mean.mean()), ci_lo=lo, ci_hi=hi))
    cl = pd.DataFrame(rows)
    cl.to_csv(os.path.join(out, "statistics", "E13_clustered_coverage.csv"), index=False, float_format="%.6g")
    x = cl[(cl["method"] == "TJ+N") & (cl["alpha"] == 0.1)]
    res["E13_clustered_TJN_a01"] = "; ".join(f"{r.dataset} {r.coverage:.3f} ({r.ci_lo:.3f}–{r.ci_hi:.3f})" for r in x.itertuples())
    # NI / TC table
    meths = ["TJ+N", "TJ+", "Gauss-LOO", "SCP-T-split-N", "ASTM-PI"]
    lines = ["| Method | Non-inferior α=0.05 | α=0.10 | α=0.20 | Training-conditional share, median (min), α=0.10 |",
             "|:--|--:|--:|--:|--:|"]
    for mth in meths:
        lines.append(f"| {mth} | {res[f'E13_NI_{mth}_0.05']} | {res[f'E13_NI_{mth}_0.1']} | {res[f'E13_NI_{mth}_0.2']} | "
                     f"{res[f'E13_tc_{mth}_median']:.2f} ({res[f'E13_tc_{mth}_min']:.2f}) |")
    open(os.path.join(out, "tables", "E13_noninferiority.md"), "w").write("\n".join(lines) + "\n")
    if log: log.info("E13 analysed")
    return res

def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    return o

def analyse_reinforcement(out, orig_dir, cfg, log=None):
    raw = os.path.join(out, "raw")
    for sub in ("summary", "statistics", "tables"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    res = {}
    res["E10"] = analyse_e10(raw, out, log)
    res["E11_E12"] = analyse_e11(raw, out, log)
    if os.path.isdir(os.path.join(orig_dir, "raw")):
        res["E13"] = analyse_e13(orig_dir, out, log)
    res["E14"] = analyse_e14(raw, out, log)
    json.dump(_clean(res), open(os.path.join(out, "statistics_reinforcement.json"), "w"), indent=1)
    return res

# ----------------------------------------------------------------------------- E14 application case study
APP_METHODS = ["Point", "ASTM-PI", "Gauss-LOO", "TJ+N", "TJ+H-N"]

def analyse_e14(raw_dir, out, log=None):
    d = _load(raw_dir, "E14_application*.csv.gz")
    if d.empty:
        return {}
    keys = ["setting", "kind", "design", "K", "n_g", "method"]
    if d.duplicated(keys + ["rep"]).sum():
        raise RuntimeError("E14: duplicated rows")
    rng = np.random.default_rng(20261028)
    rows = []
    for key, g in d.groupby(keys, sort=False):
        # pooled rates over repetitions, CI by resampling repetitions
        num, den = g["immature_passed"].to_numpy(float), g["n_immature"].to_numpy(float)
        idx = rng.integers(0, len(g), (2000, len(g)))
        boot = num[idx].sum(1) / np.maximum(den[idx].sum(1), 1)
        rows.append(dict(zip(keys, key), n_reps=len(g), immature_frac=den.sum() / g["n"].sum(),
                         immature_passed=num.sum() / max(den.sum(), 1),
                         ci_lo=float(np.quantile(boot, .025)), ci_hi=float(np.quantile(boot, .975)),
                         passed=g["n_passed"].sum() / g["n"].sum(), referred=g["n_referred"].sum() / g["n"].sum(),
                         mature_failed=g["mature_failed"].sum() / max((g["n"] - g["n_immature"]).sum(), 1)))
    s = pd.DataFrame(rows)
    s.to_csv(os.path.join(out, "summary", "E14_summary.csv"), index=False, float_format="%.6g")
    # detail table (supplement)
    t = s.copy()
    t["design"] = t.apply(lambda r: f"{int(r.K)}×{int(r.n_g)}", axis=1)
    t["method"] = t["method"].replace({"TJ+H-N": "TJ+B"})
    t["Immature passed, % [95% CI]"] = t.apply(lambda r: f"{100 * r.immature_passed:.1f} [{100 * r.ci_lo:.1f}, {100 * r.ci_hi:.1f}]", axis=1)
    t["Passed, %"] = (100 * t["passed"]).round(1); t["Referred, %"] = (100 * t["referred"]).round(1)
    t["Mature failed, %"] = (100 * t["mature_failed"]).round(1); t["Immature, %"] = (100 * t["immature_frac"]).round(1)
    t = t[["setting", "kind", "design", "method", "Immature, %", "Immature passed, % [95% CI]", "Passed, %", "Referred, %", "Mature failed, %"]]
    t.columns = ["Setting", "Pipeline", "Design", "Rule"] + list(t.columns[4:])
    lines = ["| " + " | ".join(t.columns) + " |", "|" + "|".join([":--"] * 4 + ["--:"] * 5) + "|"]
    lines += ["| " + " | ".join(str(v) for v in r) + " |" for r in t.itertuples(index=False)]
    lines.append("\nTable: **Table S14.** Harvest-maturity screening at 14% dry matter with 90% intervals, for fruit from consignments without standards (200 repetitions). Immature passed: share of truly immature fruit (DM < 14%) declared mature; Referred: share of fruit whose interval contains 14%.\n")
    open(os.path.join(out, "tables", "E14_application_detail.md"), "w").write("\n".join(lines) + "\n")
    if log: log.info("E14 analysed")
    return {"n_rows": len(d)}
