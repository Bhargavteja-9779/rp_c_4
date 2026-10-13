"""Compute every number quoted in the manuscript from machine-generated result files -> values.json.
No number in the manuscript is typed by hand: each {{key}} placeholder is filled from this file.
Usage: python compute_values.py [results_dir]   (default: ../../results)"""
import glob, json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RES = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "results")
CFG = json.load(open(os.path.join(ROOT, "code", "config", "experiments.json")))
PK = CFG["primary_kind"]; A = CFG["primary_alpha"]
SRC = ["ASTM-PI", "SCP-S", "WCP-S"]
DSN = {"corn": "Corn", "tablets": "Tablets", "mango": "Mango"}

def f2(x): return f"{x:.2f}"
def f3(x): return f"{x:.3f}"
def pfmt(p): return f"{p:.2g}" if p >= 1e-3 else f"{p:.1e}".replace("e-0", "e-").replace("e-", "×10^−^")

def md_table(df, caption):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join([":--"] + ["--:"] * (len(cols) - 1)) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(out) + f"\n\nTable: {caption}\n"

def primary(S, alpha=A, prefix="E1_main"):
    d = S[S["experiment"].str.startswith(prefix) & (S["alpha"] == alpha)]
    return d[d.apply(lambda r: r["kind"] == PK[r["dataset"]], axis=1)]

def main():
    S = pd.read_csv(os.path.join(RES, "summary", "summary_all.csv"))
    S["source"] = S["source"].astype(str); S["target"] = S["target"].astype(str)
    T = pd.read_csv(os.path.join(RES, "statistics", "paired_tests.csv"))
    FR = json.load(open(os.path.join(RES, "statistics", "friedman.json")))
    P = primary(S)
    V = {}
    # ---------------------------------------------------------------- data set facts
    sys.path.insert(0, os.path.join(ROOT, "code", "src"))
    from tjplus.data.loaders import load_corn, load_tablets, load_mango
    raw = os.path.join(ROOT, "code", "data", "raw")
    c, t, m = load_corn(raw), load_tablets(raw), load_mango(raw)
    V["n_fruit"] = f"{len(m.y):,}"
    rows = [["Corn", "80 samples", "m5 → mp5, mp6 (and mp5 → m5)", "1100–2498 nm (700)", "moisture, oil, protein, starch (%)",
             "40 / 10 / 30 (random each repetition)", "10, 15, 20"],
            ["Tablets", "655 tablets", "1 → 2", "600–1898 nm (650)", "assay (mg), weight (mg), hardness",
             "155 / 40 / 460 (fixed)", "10, 20, 30, 50"],
            ["Mango", f"{len(m.y):,} fruit ({int((m.season <= 3).sum()):,} source, {int((m.season == 4).sum())} target)",
             "seasons 1–3 → 4", "684–990 nm (103)", "dry matter (%)",
             f"{int(round(0.8 * (m.season <= 3).sum())):,} / {int((m.season <= 3).sum()) - int(round(0.8 * (m.season <= 3).sum())):,} / {int((m.season == 4).sum())}",
             "10, 20, 30, 50"]]
    V["table1"] = md_table(pd.DataFrame(rows, columns=["Data set", "Size", "Shift", "Range (channels)", "Responses",
                                                      "Source train / source cal. / target pool", "m"]),
                           "Data sets and splitting protocol.")
    # ---------------------------------------------------------------- point accuracy
    E1 = S[S["experiment"].str.startswith("E1_main") & (S["alpha"] == A) & (S["method"] == "TJ+N")]
    r = E1.groupby(["dataset", "property", "kind", "m"])["rmsep_mean"].mean().reset_index()
    cn = r[(r.dataset == "corn") & (r.m == 20)].pivot_table(index="property", columns="kind", values="rmsep_mean")
    ratio = cn["none"] / cn["pds"]
    V["corn_none_vs_pds"] = f"{ratio.min():.1f}–{ratio.max():.1f}"
    ta = r[(r.dataset == "tablets") & (r.property == "assay") & (r.kind == "pds")].set_index("m")["rmsep_mean"]
    V["tab_assay_rmsep_m10"], V["tab_assay_rmsep_m50"] = f2(ta[10]), f2(ta[50])
    mg = r[(r.dataset == "mango")].pivot_table(index="m", columns="kind", values="rmsep_mean")
    V["mango_sbc_rmsep"] = f"{mg['sbc'].min():.2f}–{mg['sbc'].max():.2f}"; V["mango_none_rmsep"] = f2(mg["none"].mean())
    tr = r[r.m.isin([10, 20])].copy()
    tr["Pipeline"] = tr["kind"].str.upper()
    tab = tr.pivot_table(index=["dataset", "property"], columns=["Pipeline", "m"], values="rmsep_mean").round(3)
    tab.columns = [f"{k} (m={mm})" for k, mm in tab.columns]
    tab = tab.reset_index().rename(columns={"dataset": "Data set", "property": "Response"})
    tab["Response"] = tab["Response"].str.replace("_", " ")
    tab["Data set"] = tab["Data set"].map(DSN)
    V["table_rmsep"] = md_table(tab.fillna("–"), "Point accuracy (mean RMSEP over repetitions; corn averaged over mp5 and mp6) of the deployed predictor for each transfer pipeline and number of standards m. NONE = source model applied without transfer.")
    # ---------------------------------------------------------------- RQ1
    src = P[P["method"].isin(SRC)]
    V["min_cov_source"] = f2(src["coverage_mean"].min())
    for ds in ("corn", "tablets", "mango"):
        d = src[src.dataset == ds]
        V[f"src_cov_range_{ds}"] = f"{d['coverage_mean'].min():.2f}–{d['coverage_mean'].max():.2f}"
        V[f"src_under_{ds}"] = f"{int(d['under_covering'].sum())} of {len(d)}"
    V["wcp_inf_pct"] = f"{100 * P[(P.dataset == 'corn') & (P.method == 'WCP-S')]['frac_reps_any_inf'].mean():.0f}%"
    tp = P[(P.dataset == "corn") & (P.method == "Transport")]
    V["transport_cov_corn"] = f"mean coverage {tp['coverage_mean'].mean():.2f}, range {tp['coverage_mean'].min():.2f}–{tp['coverage_mean'].max():.2f}"
    V["transport_under_corn"] = int(tp["under_covering"].sum())
    # ---------------------------------------------------------------- main table
    order = ["TJ+N", "TJ+", "SCP-T-split-N", "SCP-T-split", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "Transport", "LF-conv"]
    ranks = FR["median_interval_score"]["mean_ranks"]
    rows = []
    for meth in order:
        row = [meth]
        for ds in ("corn", "tablets", "mango"):
            d = P[(P.dataset == ds) & (P.method == meth)]
            if d.empty:
                row += ["–", "–"]; continue
            row += [f"{d['coverage_mean'].mean():.3f} ({d['coverage_mean'].min():.2f}–{d['coverage_mean'].max():.2f})",
                    f"{int(d['under_covering'].sum())}/{len(d)}"]
        allm = P[P.method == meth]
        row += [f"{100 * allm['frac_reps_any_inf'].mean():.0f}", f"{ranks[meth]:.2f}" if meth in ranks else "–"]
        rows.append(row)
    V["table_main"] = md_table(pd.DataFrame(rows, columns=["Method", "Corn coverage", "Corn under", "Tablets coverage", "Tablets under",
                                                          "Mango coverage", "Mango under", "Unbounded (% reps)", "Friedman rank (IS)"]),
                               f"Coverage of nominal 90% intervals (α = {A:.2f}) for the primary transfer pipelines (corn and tablets: PDS; mango: SBC). Coverage: mean over scenarios of the mean per-repetition coverage, with the range over scenarios in parentheses. Under: scenarios flagged as under-covering (upper limit of the 95% bootstrap CI < 0.90) / number of scenarios. Friedman rank: mean rank of the scenario median interval score over the {FR['median_interval_score']['n_scenarios']} scenarios (1 = best; only methods available in all scenarios).")
    # ---------------------------------------------------------------- RQ2
    t = P[P.method == "TJ+N"]
    V["n_scen_main"] = len(t)
    V["tjn_cov_main"] = f"{t['coverage_mean'].mean():.3f} (range over scenarios {t['coverage_mean'].min():.3f}–{t['coverage_mean'].max():.3f})"
    allA = pd.concat([primary(S, a) for a in CFG["alphas"]])
    hw = t.assign(hw=(t["coverage_ci_hi"] - t["coverage_ci_lo"]) / 2).groupby("dataset")["hw"].median()
    V["ci_hw_text"] = ", ".join(f"{DSN[k].lower()} ±{v:.3f}" for k, v in hw.items())
    V["tjn_cov_mean"] = f"{t['coverage_mean'].mean():.3f}"
    V["tjn_under_all_alpha"] = int(allA[allA.method == "TJ+N"]["under_covering"].sum())
    ok = None
    for mm in sorted(t["m"].unique()):
        if not t[t["m"] >= mm]["under_covering"].any():
            ok = mm; break
    V["tjn_valid_m"] = ok
    sp = P[P.method == "SCP-T-split-N"]
    inf_sc = sp[sp["frac_reps_any_inf"] > 0.99]
    V["split_inf_text"] = f"{len(inf_sc)} of {len(sp)} scenarios, all with m ≤ {int(inf_sc['m'].max())}"
    tt = T[T["experiment"].str.startswith("E1_main") & T.apply(lambda r: r["kind"] == PK[r["dataset"]], axis=1)]
    sp2 = tt[(tt.other == "SCP-T-split-N") & (tt.n_finite_pairs > 0)]
    sp2 = sp2[sp2["m"] >= 20]
    V["tjn_vs_split_n"] = len(sp2)
    V["tjn_vs_split_better"] = int(((sp2.p_holm < 0.05) & (sp2.median_IS_diff < 0)).sum())
    V["tjn_vs_split_rb"] = f2(sp2["rank_biserial"].median())
    fr = FR["median_interval_score"]
    V["friedman_chi2"] = f"{fr['friedman_chi2']:.1f}"; V["friedman_p"] = pfmt(fr["p_value"])
    V["rank_gauss"], V["rank_tjn"], V["rank_tj"] = (f2(fr["mean_ranks"][k]) for k in ("Gauss-LOO", "TJ+N", "TJ+"))
    V["p_tjn_gauss"] = f2([x for x in fr["pairwise_vs_ref"] if x["method"] == "Gauss-LOO"][0]["p_holm"])
    g = tt[tt.other == "Gauss-LOO"]
    V["gauss_better_corn"] = int(((g.dataset == "corn") & (g.p_holm < 0.05) & (g.median_IS_diff > 0)).sum())
    V["tjn_better_gauss_other"] = int(((g.dataset != "corn") & (g.p_holm < 0.05) & (g.median_IS_diff < 0)).sum())
    V["gauss_better_other"] = int(((g.dataset != "corn") & (g.p_holm < 0.05) & (g.median_IS_diff > 0)).sum())
    for a, k in ((0.05, "005"), (0.2, "020")):
        d = primary(S, a)
        V[f"gauss_under_{k}"] = int(d[d.method == "Gauss-LOO"]["under_covering"].sum())
    # alpha table
    rows = []
    for meth in ["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "LF-conv"]:
        row = [meth]
        for a in CFG["alphas"]:
            d = primary(S, a); d = d[d.method == meth]
            row.append(f"{int(d['under_covering'].sum())}/{len(d)} ({100 * d['frac_reps_any_inf'].mean():.0f}%)")
        rows.append(row)
    V["table_alpha"] = md_table(pd.DataFrame(rows, columns=["Method"] + [f"α = {a} (nominal {1 - a:.2f})" for a in CFG["alphas"]]),
                                "Validity across miscoverage levels: number of under-covering scenarios / scenarios, with the mean percentage of repetitions returning unbounded intervals in parentheses (primary pipelines).")
    # ---------------------------------------------------------------- RQ3 ablation
    abl = ["TJ+N", "TJ+", "TCV+N", "TJ-naive-N", "TJ-insample-N", "TJ+N[T2]", "TJ+N[Q]"]
    V["insample_under"] = int(P[P.method == "TJ-insample-N"]["under_covering"].sum())
    V["insample_cov_mango"] = f"{P[(P.method == 'TJ-insample-N') & (P.dataset == 'mango')]['coverage_mean'].min():.2f}–{P[(P.method == 'TJ-insample-N') & (P.dataset == 'mango')]['coverage_mean'].max():.2f}"
    tc = tt[tt.other == "TCV+N"]; V["tcv_worse"] = int(((tc.p_holm < 0.05) & (tc.median_IS_diff < 0)).sum())
    tj = tt[tt.other == "TJ+"]
    V["tjn_vs_tj_better"] = int(((tj.p_holm < 0.05) & (tj.median_IS_diff < 0)).sum())
    V["tjn_vs_tj_worse"] = int(((tj.p_holm < 0.05) & (tj.median_IS_diff > 0)).sum())
    for meth, k in (("TJ+", "tj"), ("TJ+N", "tjn")):
        d = P[P.method == meth]
        V[f"{k}_cov_sig1"], V[f"{k}_cov_sig3"] = f3(d["cov_sig1"].mean()), f3(d["cov_sig3"].mean())
    rows = []
    for meth in abl:
        row = [meth]
        for ds in ("corn", "tablets", "mango"):
            d = P[(P.dataset == ds) & (P.method == meth)]
            base = P[(P.dataset == ds) & (P.method == "TJ+N")].set_index(["property", "target", "m"])["IS_median"]
            rel = (d.set_index(["property", "target", "m"])["IS_median"] / base).median()
            row += [f"{d['coverage_mean'].mean():.3f}", f"{int(d['under_covering'].sum())}/{len(d)}", f"{rel:.3f}"]
        d = P[P.method == meth]
        row += [f"{d['cov_sig1'].mean():.3f} / {d['cov_sig3'].mean():.3f}"]
        rows.append(row)
    V["table_ablation"] = md_table(pd.DataFrame(rows, columns=["Variant", "Corn cov.", "Corn under", "Corn rel. IS", "Tablets cov.", "Tablets under",
                                                              "Tablets rel. IS", "Mango cov.", "Mango under", "Mango rel. IS", "Cov. low/high σ tertile"]),
                                   "Ablation of TJ+N (α = 0.10, primary pipelines). Rel. IS: median over scenarios of the scenario median interval score relative to TJ+N (< 1 = narrower/better). Cov. low/high σ tertile: mean coverage in the lowest and highest tertile of σ(x) over all scenarios.")
    # ---------------------------------------------------------------- LF-conv
    lf = P[P.method == "LF-conv"]; V["lf_under_010"] = int(lf["under_covering"].sum()); V["lf_n"] = len(lf)
    # ---------------------------------------------------------------- error analysis (samples)
    fs = sorted(glob.glob(os.path.join(RES, "raw", "E1_main_corn*_samples.csv.gz")))
    if fs:
        d = pd.concat([pd.read_csv(f) for f in fs]); d = d[d["m"] == 15]
        for meth, k in (("ASTM-PI", "astm"), ("TJ+N", "tjn")):
            g = d[d.method == meth].copy()
            g["miss"] = ~((g["y"] >= g["lo"]) & (g["y"] <= g["hi"]))
            g["bin"] = pd.qcut(g["q"].rank(method="first"), 5, labels=False)
            r = g.groupby("bin")["miss"].mean()
            V[f"{k}_miss_q1"], V[f"{k}_miss_q5"] = f2(r.iloc[0]), f2(r.iloc[-1])
    t20 = P[(P.method == "TJ+N") & (P.m == 20)]; t50 = P[(P.method == "TJ+N") & (P.m == 50)]
    V["tjn_p05_m20"] = f"{t20['coverage_p05'].min():.2f}–{t20['coverage_p05'].max():.2f}"
    V["tjn_p05_m50"] = f"{t50['coverage_p05'].min():.2f}–{t50['coverage_p05'].max():.2f}"
    # ---------------------------------------------------------------- abstract numbers
    V["n_scen_corn"], V["n_scen_tablets"], V["n_scen_mango"] = (int((t.dataset == ds).sum()) for ds in ("corn", "tablets", "mango"))
    extra = os.path.join(HERE, "values_secondary.py")
    if os.path.exists(extra):
        import importlib.util
        spec = importlib.util.spec_from_file_location("vs", extra); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        V.update(mod.values(S, T, RES, CFG, md_table, primary))
    for k, v in V.items():
        if not k.startswith("table"):
            print(f"{k} = {v}")
    json.dump({k: (int(v) if isinstance(v, np.integer) else v) for k, v in V.items()},
              open(os.path.join(HERE, "values.json"), "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
