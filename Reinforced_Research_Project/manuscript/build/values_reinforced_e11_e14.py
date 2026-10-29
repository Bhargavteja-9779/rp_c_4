"""Values from the simpler-formula comparison (E11), its mechanism analysis (E12) and the application case study (E14)."""
import os
import numpy as np, pandas as pd

def _frac(x):
    x = np.asarray(x, bool)
    return f"{int(x.sum())} of {len(x)}"

def fill(V, RES):
    s = pd.read_csv(os.path.join(RES, "summary", "E11_summary.csv"))
    def under(meth, al, kind=None):
        x = s[(s["method"] == meth) & (s["alpha"] == al)]
        if kind: x = x[x["kind"] == kind]
        return _frac(x["under"])
    V["r_e11_n"] = int(((s["method"] == "TJ+N") & (s["alpha"] == 0.1)).sum())
    t = s[s["method"] == "TJ+N"]; V["r_e11_tjn_under"] = _frac(t["under"])
    for meth, key in (("Gauss-LOO", "gauss"), ("Gauss-LOO-N", "gaussn"), ("ASTM-T", "astmt"), ("OLS-PI", "ols"), ("Boot-T", "boot")):
        V[f"r_{key}_under_010"] = under(meth, 0.1); V[f"r_{key}_under_005"] = under(meth, 0.05)
    a05 = s[s["alpha"] == 0.05]
    V["r_e11_tjn_unb_005"] = _frac(a05[a05["method"] == "TJ+N"]["frac_inf"] > 0.5)
    for meth, key in (("TJ+N", "tjn"), ("Gauss-LOO", "gauss"), ("ASTM-T", "astmt"), ("OLS-PI", "ols"), ("Gauss-LOO-N", "gaussn")):
        x = a05[(a05["method"] == meth)]
        V[f"r_{key}_under_005_m20"] = _frac(x[x["m"] >= 20]["under"])
        V[f"r_ni_{key}_005"] = _frac(x["noninferior"])
    g = a05[(a05["method"] == "Gauss-LOO") & a05["under"]]["coverage_mean"]
    V["r_gauss_flag_cov_005"] = f"{g.min():.2f}–{g.max():.2f} (median {g.median():.2f})"
    S = pd.read_csv(os.path.join(RES, "..", "..", "Target_Journal_Submission", "results", "summary", "summary_all.csv"))
    pk = {"corn": "pds", "tablets": "pds", "mango": "sbc"}
    e1 = S[S["experiment"].str.startswith("E1_main") & (S["alpha"] == 0.05) & (S["method"] == "TJ+N")]
    e1 = e1[e1.apply(lambda r: r["kind"] == pk[r["dataset"]], axis=1)]
    V["r_e1_tjn_unb_005"] = _frac(e1["frac_inf_mean"] > 0.5)
    e8 = S[S["experiment"].str.startswith("E8") & (S["alpha"] == 0.1)]
    tr = e8[(e8["method"] == "Transport")]
    V["r_e8_transport_cov"] = f"{tr['coverage_mean'].min():.2f}–{tr['coverage_mean'].max():.2f}"
    V["r_e8_transport_width"] = f"{tr['width_median'].median():.1f}"
    V["r_e8_tjn_width_pds"] = f"{e8[(e8['method'] == 'TJ+N') & (e8['kind'] == 'pds')]['width_median'].median():.1f}"
    bt = s[(s["method"] == "Boot-T") & (s["alpha"] == 0.1) & (s["m"] == 10)]
    V["r_boot_under_m10"] = _frac(bt["under"]) + " scenarios"
    # paired interval-score comparisons (alpha = 0.10, both methods not too narrow)
    pt = pd.read_csv(os.path.join(RES, "statistics", "E11_paired_tests.csv"))
    s01 = s[s["alpha"] == 0.1].set_index(["experiment", "property", "target", "kind", "m", "method"])["under"]
    pt["target"] = pt["target"].astype(str)
    s01.index = s01.index.set_levels(s01.index.levels[2].astype(str), level=2)
    def ok(r, meth):
        k = (r["experiment"], r["property"], str(r["target"]), r["kind"], r["m"], meth)
        return k in s01.index and not s01[k]
    for meth, key in (("OLS-PI", "ols"), ("Gauss-LOO-N", "gaussn"), ("Gauss-LOO", "gauss"), ("ASTM-T", "astmt")):
        x = pt[pt["other"] == meth]
        x = x[[ok(r, meth) and ok(r, "TJ+N") for _, r in x.iterrows()]]
        n = len(x)
        V[f"r_{key}_better"] = f"{int(((x['p_holm'] < 0.05) & (x['rank_biserial'] > 0)).sum())} of {n}"
        V[f"r_{key}_worse"] = f"{int(((x['p_holm'] < 0.05) & (x['rank_biserial'] < 0)).sum())}"
    m = pd.read_csv(os.path.join(RES, "statistics", "E12_mechanism.csv")).set_index(["method", "feature"])
    def rho(meth, feat):
        r = m.loc[(meth, feat)]
        p = r["p"]; ps = "p < 0.001" if p < 0.001 else f"p = {p:.3f}"
        return f"{r['spearman']:.2f}, {ps}"
    V["r_e12_gauss_skew"] = rho("Gauss-LOO", "skew"); V["r_e12_gauss_ratio"] = rho("Gauss-LOO", "ratio")
    V["r_e12_ols_skew"] = rho("OLS-PI", "skew"); V["r_e12_ols_kurt"] = rho("OLS-PI", "exkurt")
    # Table 3
    tv = pd.read_csv(os.path.join(RES, "statistics", "E11_validity_by_dataset.csv"))
    meths = [("TJ+N", "TJ+N"), ("Gauss-LOO", "Gauss-LOO"), ("Gauss-LOO-N", "Gauss-LOO-N"), ("ASTM-T", "ASTM-T"),
             ("OLS-PI", "OLS-PI"), ("Boot-T", "Boot-T"), ("SCP-T-split-N", "Split")]
    labs = {"corn": "Corn", "tablets": "Tablets", "mango": "Mango, season", "mango_inst": "Mango, instruments"}
    lines = ["| Data set | Pipeline | " + " | ".join(l for _, l in meths) + " |", "|:--|:--|" + "--:|" * len(meths)]
    for ds in ("corn", "tablets", "mango", "mango_inst"):
        for kind in ("pds", "sbc"):
            g = tv[(tv["dataset"] == ds) & (tv["kind"] == kind)]
            if g.empty:
                continue
            cells = []
            for mth, _ in meths:
                x = g[g["method"] == mth]
                if x.empty:
                    cells.append("–"); continue
                a, b = x["under_0.05"].iloc[0], x["under_0.1"].iloc[0]
                cells.append(f"{a.split('/')[0]} / {b.split('/')[0]}")
            n = g[g["method"] == "TJ+N"]["under_0.1"].iloc[0].split("/")[1]
            lines.append(f"| {labs[ds]} | {kind.upper()} ({n}) | " + " | ".join(cells) + " |")
    V["table_classical"] = "\n".join(lines) + (
        "\n\nTable: Simpler interval formulas on identical, randomly chosen standards (200 repetitions per scenario). "
        "Each cell gives the number of scenarios in which the method was too narrow at 95% / at 90% (number of "
        "scenarios in parentheses after the pipeline). OLS-PI applies to slope/bias correction only; Split: half of "
        "the standards fit the transfer, half calibrate the interval. Results at 80% and interval scores: "
        "Supplementary Table S12.\n")
    # ----------------------------------------------------------------- E14 (application)
    p = os.path.join(RES, "summary", "E14_summary.csv")
    if not os.path.exists(p):
        return
    a_all = pd.read_csv(p)
    a = a_all[a_all["kind"] == "sbc"]          # headline: slope/bias correction (PDS between handheld units was unusable)
    e10 = pd.read_csv(os.path.join(RES, "summary", "E10_summary.csv"))
    rr = e10[(e10["method"] == "TJ+N") & (e10["alpha"] == 0.1) & (e10["design"] == "random") & (e10["K"] == 10)]
    V["r_app_rmsep_sbc"] = f"{rr[rr['kind'] == 'sbc']['rmsep_new'].min():.1f}–{rr[rr['kind'] == 'sbc']['rmsep_new'].max():.1f}"
    V["r_app_rmsep_pds"] = f"{rr[rr['kind'] == 'pds']['rmsep_new'].min():.1f}–{rr[rr['kind'] == 'pds']['rmsep_new'].max():.1f}"
    def agg(meth, K, col, d=a):
        x = d[(d["method"] == meth) & (d["K"] == K)][col] * 100
        return x.mean(), x.min(), x.max()
    def pct(v):
        return f"{v:.0f}%" if v >= 10 else f"{v:.1f}%"
    for meth, key in (("Point", "point"), ("ASTM-PI", "astm"), ("Gauss-LOO", "gauss"), ("TJ+N", "tjn"), ("TJ+H-N", "tjb")):
        for K in sorted(a["K"].unique()):
            mi, lo, hi = agg(meth, K, "immature_passed")
            V[f"r_app_{key}_imm_K{K}"] = pct(mi)
            V[f"r_app_{key}_imm_K{K}_range"] = f"{pct(lo)}–{pct(hi)}"
            V[f"r_app_{key}_ref_K{K}"] = pct(agg(meth, K, "referred")[0])
            V[f"r_app_{key}_pass_K{K}"] = pct(agg(meth, K, "passed")[0])
        V[f"r_app_pds_{key}_imm_K10"] = pct(agg(meth, 10, "immature_passed", a_all[a_all["kind"] == "pds"])[0])
    V["r_app_ratio_tjn"] = f"{agg('TJ+N', 2, 'immature_passed')[0] / agg('TJ+N', 10, 'immature_passed')[0]:.1f}"
    V["r_app_immature_share"] = f"{100 * a[a['method'] == 'Point']['immature_frac'].mean():.0f}%"
    V["r_app_ncomb"] = int(a[(a["method"] == "Point") & (a["K"] == 2)].shape[0])
    lab = {"Point": "Point rule (ŷ ≥ 14%)", "ASTM-PI": "ASTM-PI (original calibration)", "Gauss-LOO": "Gauss-LOO",
           "TJ+N": "TJ+N", "TJ+H-N": "TJ+B (leave one consignment out)"}
    designs = sorted({(int(k), int(n)) for k, n in zip(a["K"], a["n_g"])})
    hdr = "| Rule | " + " | ".join(f"{K} × {n}: immature passed | {K} × {n}: referred" for K, n in designs) + " |"
    lines = [hdr, "|:--|" + "--:|" * (2 * len(designs))]
    for meth in ("Point", "ASTM-PI", "Gauss-LOO", "TJ+N", "TJ+H-N"):
        cells = []
        for K, n in designs:
            g = a[(a["method"] == meth) & (a["K"] == K)]
            cells += [f"{100 * g['immature_passed'].mean():.1f} ({100 * g['immature_passed'].min():.1f}–{100 * g['immature_passed'].max():.1f})",
                      f"{100 * g['referred'].mean():.0f}"]
        lines.append(f"| {lab[meth]} | " + " | ".join(cells) + " |")
    V["table_application"] = "\n".join(lines) + (
        "\n\nTable: Harvest-maturity screening of mango at 14% dry matter with 90% intervals, slope/bias correction, for fruit "
        "from consignments that supplied no standards. Immature passed: percentage of truly immature fruit (DM < 14%) "
        "declared mature, mean (range) over the season shift and the three handheld-instrument pairs; referred: "
        "percentage of all fruit whose interval contains 14%. Designs: consignments × fruit per consignment (20 × 1: "
        "instrument pairs only). 200 repetitions. PDS results: Supplementary Table S14.\n")

def fill_text(V):
    """Sentences for abstract, cover letter and conclusions (numbers only from values above)."""
    if "r_app_point_imm_K10" not in V:
        return
    V["r_abstract_app"] = (f"In a mango harvest-maturity check at 14% dry matter, passing fruit on the predicted value alone "
                           f"accepted {V['r_app_point_imm_K10']} of immature fruit; 90% intervals cut this to "
                           f"{V['r_app_tjn_imm_K10']} with reference fruit from ten consignments and {V['r_app_tjn_imm_K2']} "
                           f"with fruit from two.")
    V["r_cover_app"] = (f"In a harvest-maturity check of mango at the recommended minimum of 14% dry matter, deciding on the "
                        f"predicted value alone passed {V['r_app_point_imm_K10']} of immature fruit; intervals from well-spread "
                        f"reference fruit reduced this to {V['r_app_tjn_imm_K10']}, against {V['r_app_tjn_imm_K2']} with "
                        f"fruit from two consignments, and flagged the fruit that needed a second measurement.")
    V["r_conclusion_app"] = (f"In a harvest-maturity check of mango, intervals from well-spread reference fruit reduced the share of "
                             f"immature fruit passed as mature from {V['r_app_point_imm_K10']} (predicted value alone) to "
                             f"{V['r_app_tjn_imm_K10']}, at the cost of referring about half of the fruit for a second "
                             f"measurement.")
