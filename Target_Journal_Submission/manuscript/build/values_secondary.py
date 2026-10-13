"""Values for robustness (E4), generalisation (E5), sensitivity (E7), timing (E6) and the error analysis.
Called by compute_values.py; every returned number is computed from result files."""
import glob, json, os
import numpy as np, pandas as pd

VAR = {"ks": "Kennard–Stone standards", "noise_1000": "Noise SNR 1000", "noise_300": "Noise SNR 300", "noise_100": "Noise SNR 100",
       "shift_1": "λ-shift +1 channel (test)", "shift_-1": "λ-shift −1 channel (test)", "half_source": "Half source data"}

def values(S, T, RES, CFG, md_table, primary):
    V = {}
    a = CFG["primary_alpha"]
    s = S[S["alpha"] == a].copy()
    # ------------------------------------------------------------ robustness
    r = s[s["experiment"].str.startswith("E4_")].copy(); r["variant"] = r["experiment"].str.split("__").str[1]
    meths = ["TJ+N", "TJ+", "Gauss-LOO", "SCP-T-split-N", "ASTM-PI", "SCP-S"]
    rows = []
    for v in VAR:
        for ds in ("corn", "tablets", "mango"):
            d = r[(r.variant == v) & (r.dataset == ds)]
            row = [VAR[v], ds.capitalize()]
            for mth in meths:
                x = d[d.method == mth]
                row.append(f"{x['coverage_mean'].mean():.2f} ({int(x['under_covering'].sum())}/{len(x)})")
            rows.append(row)
    V["table_robust"] = md_table(pd.DataFrame(rows, columns=["Condition", "Data"] + meths),
                                 "Robustness (E4; α = 0.10; corn m = 15, tablets assay and mango m = 20; 200 repetitions). Mean coverage with under-covering scenarios / scenarios in parentheses.")
    nonshift = r[~r.variant.str.startswith("shift")]
    V["rob_tjn_under_nonshift"] = int(nonshift[nonshift.method == "TJ+N"]["under_covering"].sum())
    V["rob_n_nonshift"] = int((nonshift.method == "TJ+N").sum())
    ks = r[(r.variant == "ks") & (r.method == "TJ+N")]
    V["rob_ks_cov"] = f"{ks['coverage_mean'].min():.2f}–{ks['coverage_mean'].max():.2f}"
    sh = r[r.variant.str.startswith("shift")]
    def rng(meth, ds):
        x = sh[(sh.method == meth) & (sh.dataset == ds)]["coverage_mean"]
        return f"{x.min():.2f}–{x.max():.2f}"
    for ds in ("corn", "tablets", "mango"):
        V[f"rob_shift_tjn_{ds}"] = rng("TJ+N", ds); V[f"rob_shift_tj_{ds}"] = rng("TJ+", ds); V[f"rob_shift_gauss_{ds}"] = rng("Gauss-LOO", ds)
    # ------------------------------------------------------------ generalisation
    g = s[s["experiment"].str.startswith("E5_")]
    def cell(exp, mth):
        x = g[(g.experiment == exp) & (g.method == mth)]
        if x.empty: return "–"
        return f"{x['coverage_mean'].mean():.3f} ({int(x['under_covering'].sum())}/{len(x)}); {x['IS_median'].median():.3g}"
    gm = ["TJ+N", "TJ+", "Gauss-LOO", "SCP-T-split-N", "ASTM-PI", "SCP-S", "WCP-S", "MC-dropout"]
    exps = [("E5_reverse_corn", "Corn mp5→m5, PLS, PDS"), ("E5_ridge_corn", "Corn m5→mp5, ridge, PDS"),
            ("E5_ridge_tablets", "Tablets assay, ridge, PDS"), ("E5_ridge_mango", "Mango, ridge, SBC"), ("E5_cnn_mango", "Mango, 1D-CNN, SBC")]
    rows = [[lab] + [cell(e, mth) for mth in gm] for e, lab in exps]
    V["table_general"] = md_table(pd.DataFrame(rows, columns=["Setting"] + gm),
                                  "Generalisation (E5; α = 0.10). Each cell: mean coverage (under-covering / scenarios); median interval score (lower is better).")
    def cov(exp, mth):
        x = g[(g.experiment == exp) & (g.method == mth)]; return x
    c = cov("E5_cnn_mango", "TJ+N"); V["cnn_tjn_cov"] = f"{c['coverage_mean'].mean():.3f}"; V["cnn_tjn_is"] = f"{c['IS_median'].median():.2f}"
    for mth, k in (("Gauss-LOO", "gauss"), ("MC-dropout", "mc"), ("SCP-T-split-N", "split")):
        x = cov("E5_cnn_mango", mth)
        V[f"cnn_{k}_cov"] = f"{x['coverage_mean'].mean():.3f}"; V[f"cnn_{k}_under"] = f"{int(x['under_covering'].sum())}/{len(x)}"
        V[f"cnn_{k}_is"] = f"{x['IS_median'].median():.2f}"
    info = json.load(open(os.path.join(RES, "raw", "E5_cnn_info.json")))
    V["cnn_params"] = f"{int(info['n_params']):,}"; V["cnn_epochs"] = int(info["epochs_run"]); V["cnn_train_s"] = f"{info['train_seconds']:.0f}"
    V["cnn_rmsep"] = f"{cov('E5_cnn_mango', 'TJ+N')['rmsep_mean'].mean():.2f}"
    gen_tjn = g[g.method == "TJ+N"]
    V["gen_tjn_under"] = int(gen_tjn["under_covering"].sum()); V["gen_tjn_n"] = len(gen_tjn)
    # all transfer pipelines in E1
    e1 = s[s["experiment"].str.startswith("E1_main")]
    for mth, k in (("TJ+N", "tjn"), ("TJ+", "tj"), ("Gauss-LOO", "gauss"), ("ASTM-PI", "astm"), ("SCP-S", "scps")):
        x = e1[e1.method == mth]
        V[f"allpipe_{k}_under"] = f"{int(x['under_covering'].sum())} of {len(x)}"
    # ------------------------------------------------------------ E8 independent instrument shift (mango)
    e8 = s[s["experiment"].str.startswith("E8_")]
    if len(e8):
        meths8 = ["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "Transport", "LF-conv"]
        rows = []
        for kind in ("pds", "sbc"):
            for mth in meths8:
                x = e8[(e8.kind == kind) & (e8.method == mth)]
                if x.empty: continue
                rows.append([kind.upper(), mth, f"{x['coverage_mean'].mean():.3f} ({x['coverage_mean'].min():.2f}–{x['coverage_mean'].max():.2f})",
                             f"{int(x['under_covering'].sum())}/{len(x)}", f"{100 * x['frac_reps_any_inf'].mean():.0f}",
                             f"{x['width_median'].median():.2f}", f"{x['rmsep_mean'].mean():.2f}"])
        V["table_e8"] = md_table(pd.DataFrame(rows, columns=["Pipeline", "Method", "Coverage (range)", "Under", "Unbounded (% reps)", "Median width (% DM)", "RMSEP (% DM)"]),
                                 "Independent instrument shift (E8): mango dry matter, source instrument 15006, three target instruments × four values of m (12 scenarios per pipeline; α = 0.10; 200 repetitions).")
        for kind in ("pds", "sbc"):
            t8 = e8[(e8.kind == kind) & (e8.method == "TJ+N")]
            V[f"e8_tjn_cov_{kind}"] = f"{t8['coverage_mean'].mean():.3f}"; V[f"e8_tjn_under_{kind}"] = f"{int(t8['under_covering'].sum())}/{len(t8)}"
            V[f"e8_rmsep_{kind}"] = f"{t8['rmsep_mean'].min():.2f}–{t8['rmsep_mean'].max():.2f}"
            V[f"e8_width_{kind}"] = f"{t8['width_median'].median():.1f}"
            src8 = e8[(e8.kind == kind) & e8.method.isin(["ASTM-PI", "SCP-S", "WCP-S"])]
            V[f"e8_src_cov_{kind}"] = f"{src8['coverage_mean'].min():.2f}–{src8['coverage_mean'].max():.2f}"
            V[f"e8_src_under_{kind}"] = f"{int(src8['under_covering'].sum())}/{len(src8)}"
            g8 = e8[(e8.kind == kind) & (e8.method == "Gauss-LOO")]
            V[f"e8_gauss_under_{kind}"] = f"{int(g8['under_covering'].sum())}/{len(g8)}"
        fin = e8[e8.method.isin(["ASTM-PI", "SCP-S"])]
        for kind in ("pds", "sbc"):
            x = fin[fin.kind == kind]
            V[f"e8_fin_cov_{kind}"] = f"{x['coverage_mean'].min():.2f}–{x['coverage_mean'].max():.2f}"
            V[f"e8_fin_under_{kind}"] = f"{int(x['under_covering'].sum())}/{len(x)}"
        w = e8[(e8.method == "WCP-S")]
        V["e8_wcp_inf_sbc"] = f"{100 * w[w.kind == 'sbc']['frac_reps_any_inf'].mean():.0f}%"
        V["e8_wcp_cov_pds"] = f"{w[w.kind == 'pds']['coverage_mean'].min():.2f}–{w[w.kind == 'pds']['coverage_mean'].max():.2f}"
        allA8 = S[S["experiment"].str.startswith("E8_") & (S.method == "TJ+N")]
        V["e8_tjn_under_allalpha"] = f"{int(allA8['under_covering'].sum())}/{len(allA8)}"
        g8a = S[S["experiment"].str.startswith("E8_") & (S.method == "Gauss-LOO")]
        V["e8_gauss_under_allalpha"] = f"{int(g8a['under_covering'].sum())}/{len(g8a)}"
    # ------------------------------------------------------------ sensitivity
    e7 = s[s["experiment"].str.startswith("E7_")].copy(); e7["setting"] = e7["experiment"].str.split("__").str[1]
    t = e7[e7.method == "TJ+N"]
    V["sens_tjn_under"] = int(t["under_covering"].sum()); V["sens_n"] = len(t)
    V["sens_tjn_cov"] = f"{t['coverage_mean'].min():.3f}–{t['coverage_mean'].max():.3f}"
    w = e7[(e7.dataset == "corn") & e7.setting.str.startswith("hw") & (e7.method == "TJ+N")].groupby("setting")["rmsep_mean"].mean()
    V["sens_corn_rmsep_hw"] = ", ".join(f"{v:.3f} ({int(k[2:]) * 2 + 1} channels)" for k, v in w.items())
    e1c = s[s["experiment"].str.startswith("E1_main_corn") & (s.kind == "pds") & (s.m == 15) & (s.method == "TJ+N") & (s.target == "mp5")]
    V["sens_corn_rmsep_w5"] = f"{e1c['rmsep_mean'].mean():.3f}"
    tb = s[s["experiment"].str.startswith("E1_main_tablets") & (s.kind == "pds")]
    a10 = tb[(tb.property == "assay") & (tb.m == 10) & tb.method.isin(["ASTM-PI", "SCP-S", "WCP-S"])]
    V["tab_assay_m10_src"] = f"coverage {a10['coverage_mean'].min():.2f}–{a10['coverage_mean'].max():.2f}"
    wt = tb[(tb.property == "weight") & tb.method.isin(["SCP-S", "WCP-S"])]
    V["tab_weight_scps"] = f"{wt['coverage_mean'].min():.3f}–{wt['coverage_mean'].max():.3f}"
    src = e7[e7.method.isin(["ASTM-PI", "SCP-S"])]
    V["sens_src_under"] = f"{int(src['under_covering'].sum())} of {len(src)}"
    hw5 = e7[(e7.dataset == "tablets") & (e7.setting == "hw5")]
    V["sens_tab_hw5_astm"] = f"{hw5[hw5.method == 'ASTM-PI']['coverage_mean'].mean():.2f}"
    V["sens_tab_hw5_scps"] = f"{hw5[hw5.method == 'SCP-S']['coverage_mean'].mean():.2f}"
    # ------------------------------------------------------------ timing
    tm = pd.read_csv(os.path.join(RES, "raw", "E6_timing.csv"))
    def tsec(ds, step_prefix):
        x = tm[(tm.dataset == ds) & tm.step.str.startswith(step_prefix)]["median_s"].iloc[0]; return x
    for ds in ("corn", "tablets", "mango"):
        V[f"time_tj_{ds}"] = f"{tsec(ds, 'TJ+N'):.2f}"; V[f"time_one_{ds}"] = f"{1000 * tsec(ds, 'point'):.1f}"
    V["time_mem_max"] = f"{tm['peak_mem_MB'].max():.0f}"
    V["table_timing"] = md_table(tm.assign(**{"median time (s)": tm["median_s"].map(lambda x: f"{x:.4f}"), "peak memory (MB)": tm["peak_mem_MB"].map(lambda x: f"{x:.1f}")})
                                 [["dataset", "kind", "m", "n_test", "n_channels", "step", "median time (s)", "peak memory (MB)"]],
                                 "Computational cost (single CPU core, median of 20 runs).")
    sc = os.path.join(RES, "raw", "E6b_timing_scaling.csv")
    if os.path.exists(sc):
        z = pd.read_csv(sc); zt = z[z.step.str.startswith("TJ+N")]
        parts = []
        for ds in ("corn", "tablets", "mango"):
            x = zt[zt.dataset == ds].sort_values("m")
            if len(x) >= 2:
                parts.append(f"{ds}: {x['median_s'].iloc[0]:.2f} s at m = {int(x['m'].iloc[0])} to {x['median_s'].iloc[-1]:.2f} s at m = {int(x['m'].iloc[-1])}")
        V["scaling_text"] = "; ".join(parts)
        V["table_scaling"] = md_table(z.assign(median_s=z["median_s"].map(lambda v: f"{v:.4f}")), "Wall-clock time versus number of standards (single core, median of 10 runs).")
    # ------------------------------------------------------------ error analysis (Gauss at high Q)
    fs = sorted(glob.glob(os.path.join(RES, "raw", "E1_main_*_samples.csv.gz")))
    keep = {"corn": 15, "tablets": 20, "mango": 20}
    out = {}
    for f in fs:
        d = pd.read_csv(f); ds = d["dataset"].iloc[0]; d = d[d["m"] == keep[ds]]
        for mth in ("Gauss-LOO", "TJ+N"):
            gg = d[d.method == mth].copy()
            gg["miss"] = ~((gg["y"] >= gg["lo"]) & (gg["y"] <= gg["hi"]))
            gg["bin"] = pd.qcut(gg["q"].rank(method="first"), 5, labels=False)
            out.setdefault((ds, mth), []).append(gg.groupby("bin")["miss"].agg(["sum", "count"]))
    for (ds, mth), parts in out.items():
        p = sum(parts); rate = p["sum"] / p["count"]
        V[f"miss_q5_{'gauss' if mth == 'Gauss-LOO' else 'tjn'}_{ds}"] = f"{rate.iloc[-1]:.2f}"
    return V
