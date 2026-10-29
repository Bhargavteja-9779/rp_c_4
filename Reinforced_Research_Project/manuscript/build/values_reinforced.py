"""Every number of the revised manuscript, computed from machine-generated result files -> values.json.

Sources:
  ../../../Target_Journal_Submission/manuscript/build/values.json  numbers of the original study (E1-E9), regenerated
                                                                    from the committed raw results by compute_values.py
                                                                    (verified 175/175 identical in the integrity audit)
  ../../results/summary/E10_summary.csv, E11_summary.csv, E14 raw, statistics/*.csv, statistics_reinforcement.json
"""
import glob, json, os
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "results")
ORIG = os.path.abspath(os.path.join(ROOT, "..", "Target_Journal_Submission", "manuscript", "build", "values.json"))

def rng(x, nd=2):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    lo, hi = np.round(x.min(), nd), np.round(x.max(), nd)
    return f"{lo:.{nd}f}" if lo == hi else f"{lo:.{nd}f}–{hi:.{nd}f}"

def frac(flags):
    flags = np.asarray(flags, bool)
    return f"{int(flags.sum())} of {len(flags)}"

def e10_values(V):
    s = pd.read_csv(os.path.join(RES, "summary", "E10_summary.csv"))
    a = s[s["alpha"] == 0.1]; rnd = a[a["design"] == "random"]
    def cell(K, meth, col="under"):
        return rnd[(rnd["K"] == K) & (rnd["method"] == meth)]
    V["r_k2_tjn_under"] = frac(cell(2, "TJ+N")["under"])
    V["r_k2_tjn_cov"] = rng(cell(2, "TJ+N")["coverage_mean"])
    V["r_k2_tjn_same_cov"] = rng(cell(2, "TJ+N")["same_coverage"])
    V["r_k2_gauss_under"] = frac(cell(2, "Gauss-LOO")["under"])
    V["r_k2_split_under"] = frac(cell(2, "SCP-T-split-N")["under"])
    V["r_k2_anova_under"] = frac(cell(2, "ANOVA-PI")["under"])
    for K in (5, 10, 15, 20):
        V[f"r_tjn_under_K{K}"] = frac(cell(K, "TJ+N")["under"])
    V["r_tjn_cov_K15"] = rng(cell(15, "TJ+N")["coverage_mean"])
    V["r_k2_lgo_under"] = frac(cell(2, "LGO-CV+N")["under"])
    for K in (2, 5, 10):
        V[f"r_anova_under_K{K}"] = frac(cell(K, "ANOVA-PI")["under"])
    ng1 = s[(s["design"] == "random") & (s["n_g"] == 1) & (s["method"] == "TJ+N")]
    V["r_tjn_under_ng1"] = frac(ng1["under"]) + " combinations over the three confidence levels"
    for al, key in ((0.1, "a01"), (0.2, "a02"), (0.05, "a005")):
        tb = s[(s["design"] == "random") & (s["method"] == "TJ+H-N") & (s["alpha"] == al) & (s["new_frac_inf"] < 0.5)]
        V[f"r_tjb_under_{key}"] = frac(tb["under"])
    tb = rnd[(rnd["method"] == "TJ+H-N") & (rnd["new_frac_inf"] < 0.5)]
    V["r_tjb_cov"] = rng(tb["coverage_mean"])
    V["r_tjb_under_bounded"] = frac(s[(s["design"] == "random") & (s["method"] == "TJ+H-N") & (s["new_frac_inf"] < 0.5)]["under"])
    V["r_gausslgo_under_a01"] = frac(rnd[rnd["method"] == "Gauss-LGO"]["under"])
    t = rnd[rnd["method"] == "TJ+N"]
    V["r_icc_range"] = rng(t.groupby(["setting", "kind"])["icc_new"].mean())
    import json as _j
    st = _j.load(open(os.path.join(RES, "statistics_reinforcement.json")))["E10"]
    V["r_h10d_rho"] = f"{st['h10d_spearman_icc_deficit']:.2f}, p = {st['h10d_p']:.2f}"
    p = a.pivot_table(index=["setting", "kind", "design", "K"], columns="method", values="new_median_width")
    r10 = (p["TJ+H-N"] / p["TJ+N"]).xs(("random", 10), level=("design", "K"))
    V["r_tjb_width_10"] = f"{np.median(r10):.2f}"
    r2 = (p["Gauss-LGO"] / p["TJ+N"]).xs(("random", 2), level=("design", "K"))
    V["r_gausslgo_width_2"] = f"{np.median(r2):.1f}"
    for K in (5, 10):
        r = (p["Gauss-LGO"] / p["TJ+N"]).xs(("random", K), level=("design", "K"))
        V[f"r_gausslgo_ratio_{K}"] = f"{r.min():.2f}–{r.max():.2f}"
        r = (p["ANOVA-PI"] / p["TJ+N"]).xs(("random", K), level=("design", "K"))
        V[f"r_anova_ratio_{K}"] = f"{r.min():.2f}–{r.max():.2f}"
    ch = a[a["design"] == "chrono"]
    V["r_chrono_n"] = int((ch["method"] == "TJ+N").sum())
    for meth, key in (("TJ+N", "tjn"), ("Gauss-LOO", "gauss"), ("ANOVA-PI", "anova"), ("ASTM-PI", "astm"), ("Gauss-LGO", "gausslgo")):
        V[f"r_chrono_{key}_under"] = frac(ch[ch["method"] == meth]["under"])
    c2 = s[(s["design"] == "chrono") & (s["alpha"] == 0.2) & (s["method"] == "TJ+H-N")]
    V["r_chrono_tjb_020"] = rng(c2["coverage_mean"])
    # Table 4 (batch designs)
    meths = [("TJ+N", "TJ+N"), ("Gauss-LOO", "Gauss-LOO"), ("SCP-T-split-N", "Split"), ("ASTM-PI", "ASTM-PI"),
             ("TJ+H-N", "TJ+B"), ("LGO-CV+N", "LGO-CV+N"), ("Gauss-LGO", "Gauss-LGO"), ("ANOVA-PI", "ANOVA-PI")]
    a2 = a.copy()
    a2["lab"] = a2.apply(lambda r: ("chronological " if r["design"] == "chrono" else "") + f"{int(r['K'])} × {int(r['n_g'])}", axis=1)
    order = ["2 × 10", "5 × 4", "10 × 2", "15 × 1", "20 × 1", "chronological 5 × 4"]
    lines = ["| Consignments × fruit | " + " | ".join(m[1] for m in meths) + " |", "|:--|" + "--:|" * len(meths)]
    for lab in order:
        g = a2[a2["lab"] == lab]
        cells = []
        for m, _ in meths:
            x = g[g["method"] == m]
            if x["new_frac_inf"].mean() > 0.5:
                cells.append("unbounded")
            else:
                cells.append(f"{x['coverage_mean'].mean():.2f} ({int(x['under'].sum())}/{len(x)})")
        lines.append(f"| {lab} | " + " | ".join(cells) + " |")
    V["table_batch"] = "\n".join(lines) + (
        "\n\nTable: Coverage of nominal 90% intervals for fruit from consignments that supplied no standards, by how the "
        "standards were spread over consignments (mean over the setting-pipeline combinations, 300 repetitions each; "
        "in parentheses: combinations flagged as too narrow / combinations). The instrument settings alone have the "
        "20 × 1 design. TJ+B: leave-one-consignment-out (hierarchical) jackknife+; Split: half the standards for "
        "transfer, half for calibration; LGO-CV+N: CV+ with consignments as folds but fruit as units; Gauss-LGO and ANOVA-PI: Gaussian and random-effects intervals from leave-one-consignment-out errors. The first four methods treat samples as the unit, the last four consignments.\n")

def e13_values(V):
    p = os.path.join(RES, "statistics", "E13_noninferiority_trainingconditional.csv")
    s = pd.read_csv(p)
    t = s[s["method"] == "TJ+N"]
    V["r_ni_tjn"] = f"{int(t['noninferior'].sum())} of {len(t)}"
    x = s[(s["alpha"] == 0.1)]
    V["r_tc_tjn_median"] = f"{x[x['method'] == 'TJ+N']['tc_share'].median():.2f}"
    V["r_tc_tjn_min"] = f"{x[x['method'] == 'TJ+N']['tc_share'].min():.2f}"
    V["r_tc_gauss_median"] = f"{x[x['method'] == 'Gauss-LOO']['tc_share'].median():.2f}"

def data_values(V):
    """Batch structure of the mango data (computed from the data files)."""
    import sys
    sys.path.insert(0, os.path.join(ROOT, "code", "src"))
    from tjplus.data.loaders import load_mango, load_mango_instruments
    from tjplus.data.meta import load_mango_meta, load_mango_inst_meta
    raw = os.path.join(ROOT, "code", "data", "raw")
    d = load_mango(raw); m = load_mango_meta(raw)
    c = pd.Series(m["pop"][d.season == 4]).value_counts()
    V["r_n_pops_s4"] = int(len(c)); V["r_pop_size_s4"] = f"{c.min()}–{c.max()}"
    di = load_mango_instruments(raw); mi = load_mango_inst_meta(raw)
    n = [int(pd.Series(mi["pop"][di.present[15006] & di.present[t]]).nunique()) for t in (15016, 15014, 15029)]
    V["r_n_pops_inst"] = f"{n[0]}, {n[1]} and {n[2]}"

def main():
    V = json.load(open(ORIG))
    data_values(V)
    e10_values(V)
    e13_values(V)
    extra = os.path.join(HERE, "values_reinforced_e11_e14.py")
    if os.path.exists(extra):
        ns = {}
        exec(open(extra).read(), ns)
        ns["fill"](V, RES)
        ns["fill_text"](V)
    json.dump(V, open(os.path.join(HERE, "values.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{len(V)} values written")

if __name__ == "__main__":
    main()
