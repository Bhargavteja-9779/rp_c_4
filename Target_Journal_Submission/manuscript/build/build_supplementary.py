"""Build the Supplementary Material (DOCX + PDF) from result files only."""
import json, os, subprocess
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "results"); TAB = os.path.join(ROOT, "tables")
CFG = json.load(open(os.path.join(ROOT, "code", "config", "experiments.json")))

def md(df, cap):
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join([":--"] + ["--:"] * (len(cols) - 1)) + "|"]
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(out) + f"\n\nTable: {cap}\n\n"

def main():
    S = pd.read_csv(os.path.join(RES, "summary", "summary_all.csv"))
    pk = CFG["primary_kind"]
    parts = ["---\ntitle: \"Supplementary Material\"\nsubtitle: \"Valid prediction intervals for transferred NIR calibrations: reusing the transfer standards with a leave-one-standard-out jackknife+\"\n---\n",
             "All tables and figures in this document were generated automatically from the machine-readable result files of the study (`results/`).\n"]
    # S1: per-scenario main results
    m = S[S.experiment.str.startswith("E1_main") & (S.alpha == 0.1) & S.apply(lambda r: r["kind"] == pk[r["dataset"]], axis=1)]
    m = m[m.method.isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "Transport"])]
    t = m.assign(cov=m.apply(lambda r: f"{r.coverage_mean:.3f} [{r.coverage_ci_lo:.3f}, {r.coverage_ci_hi:.3f}]", axis=1),
                 IS=m["IS_median"].map(lambda x: "∞" if x == float("inf") else f"{x:.3g}"))
    t = t[["dataset", "property", "target", "m", "method", "cov", "IS", "under_covering"]]
    t.columns = ["Data", "Response", "Target", "m", "Method", "Coverage [95% CI]", "Median IS", "Under-covering"]
    parts.append("# Table S1. Main results for every scenario\n\n" + md(t, "**Table S1.** Coverage of nominal 90% intervals and median interval score for every primary scenario (α = 0.10). CI: percentile bootstrap over repetitions."))
    # S2: transfer pipelines
    p = pd.read_csv(os.path.join(TAB, "table5b_transfer_pipelines.csv")).round(3)
    parts.append("# Table S2. All transfer pipelines\n\n" + md(p, "**Table S2.** Coverage (mean and minimum over scenarios), median interval score, RMSEP and under-covering scenarios for every transfer pipeline (α = 0.10)."))
    # S3: sensitivity
    q = pd.read_csv(os.path.join(TAB, "table7b_window_lv_sensitivity.csv")).round(3)
    q = q[q.method.isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S"])]
    parts.append("# Table S3. Sensitivity to transfer and model settings\n\n" + md(q, "**Table S3.** Sensitivity to the PDS half-window (hw1 = 3 channels, hw3 = 7, hw5 = 11; the primary analysis used 5 channels) and to the number of latent variables (lv ±2)."))
    # S4: timing
    tm = pd.read_csv(os.path.join(RES, "raw", "E6_timing.csv")).round(4)
    parts.append("# Table S4. Computational cost\n\n" + md(tm, "**Table S4.** Wall-clock time and peak memory (single CPU core, median of 20 runs)."))
    # S5: paired tests summary
    pt = pd.read_csv(os.path.join(TAB, "table8_paired_tests.csv")).round(3)
    parts.append("# Table S5. Paired tests\n\n" + md(pt, "**Table S5.** Paired Wilcoxon signed-rank tests of per-repetition interval score, TJ+N against each method: number of scenarios with a significantly lower (better) or higher (worse) score for TJ+N (Holm-adjusted p < 0.05 within scenario) and median matched-pairs rank-biserial correlation (negative = TJ+N better)."))
    # S6: E8 (if available)
    e8 = S[S.experiment.str.startswith("E8_") & (S.alpha == 0.1)]
    if len(e8):
        e = e8[e8.method.isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S", "Transport", "LF-conv"])]
        e = e.assign(cov=e.apply(lambda r: f"{r.coverage_mean:.3f} [{r.coverage_ci_lo:.3f}, {r.coverage_ci_hi:.3f}]", axis=1),
                     IS=e["IS_median"].map(lambda x: "∞" if x == float("inf") else f"{x:.3g}"))
        e = e[["kind", "target", "m", "method", "cov", "IS", "rmsep_mean", "under_covering"]].round(3)
        e.columns = ["Pipeline", "Target instrument", "m", "Method", "Coverage [95% CI]", "Median IS", "RMSEP", "Under-covering"]
        parts.append("# Table S6. Independent instrument shift (mango, E8)\n\n" + md(e, "**Table S6.** Mango instrument transfer (source instrument 15006; α = 0.10; 200 repetitions)."))
    scp = os.path.join(RES, "raw", "E6b_timing_scaling.csv")
    if os.path.exists(scp):
        z = pd.read_csv(scp).round(4)
        parts.append("# Table S7. Scaling of computational cost with m\n\n" + md(z, "**Table S7.** Wall-clock time of a single transfer fit with prediction and of TJ+N (including five CV+ refits) versus the number of standards m (single CPU core, median of 10 runs)."))
    parts.append("# Fig. S1. CNN training\n\n![**Fig. S1.** Training and validation loss of the 1D-CNN (mango, seasons 1–3).](figures/figS1_cnn_training.png){width=12cm}\n\n")
    parts.append("# Fig. S2. Friedman ranks\n\n![**Fig. S2.** Mean Friedman ranks of the scenario median interval score over the 40 primary scenarios (1 = best).](figures/figS2_friedman_ranks.png){width=12cm}\n")
    mdp = os.path.join(HERE, "supplementary_filled.md"); open(mdp, "w").write("\n".join(parts))
    out = os.path.join(ROOT, "supplementary", "Supplementary_Material.docx"); os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["pandoc", mdp, "-o", out, "--reference-doc", os.path.join(HERE, "reference.docx"), "--resource-path", ROOT], check=True, cwd=ROOT)
    from postprocess_docx import postprocess
    postprocess(out)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(out), out], check=True, capture_output=True)
    print("built", out)

if __name__ == "__main__":
    main()
