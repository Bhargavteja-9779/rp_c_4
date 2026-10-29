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
    a = pd.read_csv(p)
    def agg(meth, K, col):
        x = a[(a["method"] == meth) & (a["K"] == K)][col] * 100
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
    V["r_app_immature_share"] = f"{100 * a[a['method'] == 'Point']['immature_frac'].mean():.0f}%"
    V["r_app_ncomb"] = int(a[(a["method"] == "Point") & (a["K"] == 2)].shape[0])
    rows = []
    lab = {"Point": "Point rule (ŷ ≥ 14%)", "ASTM-PI": "ASTM-PI (original calibration)", "Gauss-LOO": "Gauss-LOO",
           "TJ+N": "TJ+N", "TJ+H-N": "TJ+B (leave one consignment out)"}
    designs = sorted({(int(k), int(n)) for k, n in zip(a["K"], a["n_g"])})
    hdr = "| Rule | " + " | ".join(f"{K} × {n}: immature passed | {K} × {n}: referred" for K, n in designs) + " |"
    lines = [hdr, "|:--|" + "--:|" * (2 * len(designs))]
    for meth in ("Point", "ASTM-PI", "Gauss-LOO", "TJ+N", "TJ+H-N"):
        cells = []
        for K, n in designs:
            g = a[(a["method"] == meth) & (a["K"] == K)]
            if g.empty:
                cells += ["–", "–"]; continue
            cells += [f"{100 * g['immature_passed'].mean():.1f} ({100 * g['immature_passed'].min():.1f}–{100 * g['immature_passed'].max():.1f})",
                      f"{100 * g['referred'].mean():.0f}"]
        lines.append(f"| {lab[meth]} | " + " | ".join(cells) + " |")
    V["table_application"] = "\n".join(lines) + (
        "\n\nTable: Harvest-maturity screening of mango at 14% dry matter with 90% intervals, for fruit from consignments "
        "that supplied no standards. Immature passed: percentage of truly immature fruit (DM < 14%) declared mature, "
        "mean (range) over the setting-pipeline combinations; referred: percentage of all fruit whose interval contains "
        "14% and which would be re-measured. Designs: consignments × fruit per consignment (the 20 × 1 design for the "
        "instrument settings only). 200 repetitions. Details: Supplementary Table S14.\n")

def fill_text(V):
    """Sentences for abstract, cover letter and conclusions (numbers only from values above)."""
    if "r_app_point_imm_K10" not in V:
        return
    V["r_abstract_app"] = (f"In a mango harvest-maturity check at 14% dry matter, the point prediction passed "
                           f"{V['r_app_point_imm_K10']} of immature fruit; intervals from samples spread over ten consignments "
                           f"cut this to {V['r_app_tjn_imm_K10']} ({V['r_app_tjn_imm_K2']} with two consignments).")
    V["r_cover_app"] = (f"In a harvest-maturity check of mango at the industry minimum of 14% dry matter, the usual point rule "
                        f"passed {V['r_app_point_imm_K10']} of immature fruit; valid intervals from well-spread standards "
                        f"reduced this to {V['r_app_tjn_imm_K10']} and showed which fruit needed a second look.")
    V["r_conclusion_app"] = (f"In a harvest-maturity check of mango, these intervals reduced the share of immature fruit passed "
                             f"as mature from {V['r_app_point_imm_K10']} with the point prediction to {V['r_app_tjn_imm_K10']}, "
                             f"and identified the fruit close to the threshold that should be re-measured.")
