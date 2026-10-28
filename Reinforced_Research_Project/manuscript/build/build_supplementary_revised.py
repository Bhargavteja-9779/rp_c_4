"""Supplementary Material of the revised manuscript, built only from result files and values.json."""
import json, os, re, subprocess
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ORIG = os.path.abspath(os.path.join(ROOT, "..", "Target_Journal_Submission"))
RES = os.path.join(ROOT, "results")

def md(df, cap):
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join([":--"] + ["--:"] * (len(cols) - 1)) + "|"]
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(out) + f"\n\nTable: {cap}\n\n"

def from_value(v, cap):
    """Re-caption a generated Markdown table from values.json."""
    body = re.split(r"\n\s*Table: ", v)[0].strip()
    return body + f"\n\nTable: {cap}\n\n"

def main():
    V = json.load(open(os.path.join(HERE, "values.json")))
    P = ["---\ntitle: \"Supplementary Material\"\nsubtitle: \"Trustworthy prediction intervals after moving an NIR calibration to a new instrument or season\"\n---\n",
         "Every table and figure in this document was generated automatically from the result files of the study. Method names: TJ+N, transfer jackknife+ with T²/Q scaling; TJ+, without scaling; TJ+B, leave-one-batch-out version; Split, half of the standards for transfer and half for calibration (SCP-T-split); Gauss-LOO, t-interval from leave-one-out errors.\n"]
    P.append("# Table S1. Prediction error after transfer\n\n" + from_value(V["table_rmsep"], "**Table S1.** Mean RMSEP of the transferred predictor for each pipeline and number of standards m (corn averaged over mp5 and mp6). NONE: original calibration applied without transfer."))
    P.append("# Table S2. Three confidence levels\n\n" + from_value(V["table_alpha"], "**Table S2.** Number of scenarios flagged as too narrow / scenarios, with the mean percentage of repetitions that returned unbounded intervals in parentheses (main pipelines, random standards)."))
    P.append("# Table S3. Components of TJ+N\n\n" + from_value(V["table_ablation"], "**Table S3.** Ablation of TJ+N (α = 0.10, main pipelines). TCV+N: five-fold CV+; TJ-naive-N: full-fit centre with leave-one-out quantile; TJ-insample-N: residuals of the transfer fitted on all standards; TJ+N[T2], TJ+N[Q]: scaling with one diagnostic. Rel. IS: median interval score relative to TJ+N. Last column: coverage in the lowest/highest third of σ(x)."))
    P.append("# Table S4. Pipelines, directions and model types\n\n" + from_value(V["table_general"], "**Table S4.** Reverse direction, ridge regression and a 1D-CNN (α = 0.10). Each cell: mean coverage (scenarios too narrow / scenarios); median interval score."))
    rb = pd.read_csv(os.path.join(ORIG, "tables", "table4_robustness.csv")).round(3)
    rb = rb[rb.method.isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S"])]
    P.append("# Table S5. Robustness\n\n" + md(rb, "**Table S5.** Robustness (α = 0.10; corn m = 15, tablets assay and mango m = 20; 200 repetitions): mean and minimum coverage over scenarios, median interval score and scenarios flagged as too narrow."))
    P.append("# Table S6. Transfer between handheld fruit spectrometers\n\n" + from_value(V["table_e8"], "**Table S6.** Mango instrument transfer, source unit 15006 to three target units, four values of m (12 scenarios per pipeline; α = 0.10; 200 repetitions; standards drawn at random)."))
    P.append("# Table S7. Gaussian intervals with difficulty scaling\n\n" + from_value(V["table_e9"], "**Table S7.** TJ+N compared with Gaussian leave-one-out intervals without (Gauss-LOO) and with (Gauss-LOO-N) σ(x) scaling (200 repetitions)."))
    S = pd.read_csv(os.path.join(ORIG, "results", "summary", "summary_all.csv"))
    e4b = S[S.experiment.str.startswith("E4b_")].copy()
    e4b["shift"] = e4b.experiment.str.split("__").str[1]
    z = e4b[e4b.method.isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S"])].groupby(["dataset", "shift", "method"]).agg(
        coverage=("coverage_mean", "mean"), coverage_min=("coverage_mean", "min"), too_narrow=("under_covering", "sum"), n=("under_covering", "size")).reset_index().round(3)
    P.append("# Table S8. Quarter-channel drift\n\n" + md(z, "**Table S8.** Coverage under a ±0.25-channel wavelength shift of the routine spectra after standardisation (α = 0.10; 200 repetitions)."))
    q = pd.read_csv(os.path.join(ORIG, "tables", "table7b_window_lv_sensitivity.csv")).round(3)
    q = q[q.method.isin(["TJ+N", "TJ+", "SCP-T-split-N", "Gauss-LOO", "ASTM-PI", "SCP-S", "WCP-S"])]
    P.append("# Table S9. Transfer and model settings\n\n" + md(q, "**Table S9.** Sensitivity to the PDS window (hw1 = 3 channels, hw3 = 7, hw5 = 11; main analysis 5) and to the number of PLS components (±2)."))
    tm = pd.read_csv(os.path.join(ORIG, "results", "raw", "E6_timing.csv")).round(4)
    P.append("# Table S10. Computing time\n\n" + md(tm, "**Table S10.** Wall-clock time and peak memory (one CPU core, median of 20 runs)."))
    e10 = pd.read_csv(os.path.join(RES, "summary", "E10_summary.csv"))
    e10 = e10[(e10.alpha == 0.1) & e10.method.isin(["TJ+N", "TJ+H-N", "Gauss-LOO", "SCP-T-split-N", "ANOVA-PI", "Gauss-LGO", "LGO-CV+N", "ASTM-PI"])]
    e10 = e10.assign(method=e10.method.replace({"TJ+H-N": "TJ+B", "SCP-T-split-N": "Split"}),
                     cov=e10.apply(lambda r: "unbounded" if r.new_frac_inf > 0.5 else f"{r.coverage_mean:.3f} [{r.ci_lo:.3f}, {r.ci_hi:.3f}]", axis=1),
                     same=e10.same_coverage.round(3), icc=e10.icc_new.round(2))
    e10 = e10[["setting", "kind", "design", "K", "n_g", "method", "cov", "under", "same", "icc"]]
    e10.columns = ["Setting", "Pipeline", "Design", "K", "n_g", "Method", "Coverage, new batches [95% CI]", "Too narrow", "Coverage, same batches", "ICC"]
    P.append("# Table S11. Batch designs, every combination\n\n" + md(e10, "**Table S11.** Standards from K consignments × n_g fruit (α = 0.10; 300 repetitions). Coverage for fruit from consignments without standards (consignment-weighted) and for the remaining fruit of the sampled consignments; ICC: intra-consignment correlation of the errors of the transferred predictor."))
    p11 = os.path.join(RES, "statistics", "E11_validity_by_dataset.csv")
    if os.path.exists(p11):
        t = pd.read_csv(p11).round(3)
        t.columns = ["Data set", "Pipeline", "Method", "Too narrow α=0.05", "Too narrow α=0.10", "Too narrow α=0.20", "Median IS relative to TJ+N (α=0.10)"]
        P.append("# Table S12. Simpler interval formulas\n\n" + md(t, "**Table S12.** Simpler interval formulas on identical standards (200 repetitions; standards drawn at random)."))
    p13 = os.path.join(RES, "tables", "E13_noninferiority.md")
    P.append("# Table S13. Closeness to nominal and per-set reliability\n\n" + open(p13).read().strip() +
             "\n\nTable: **Table S13.** Main scenarios with random standards (corn, tablets, mango season shift and mango instruments; 64 scenario-pipeline combinations). Non-inferior: lower limit of the 95% CI of coverage ≥ nominal − 0.02. Last column: share of standard sets (repetitions) with realised coverage ≥ 0.85 on the test samples, median (minimum) over scenarios. Unbounded intervals count as covering.\n\n")
    p14 = os.path.join(RES, "tables", "E14_application_detail.md")
    if os.path.exists(p14):
        P.append("# Table S14. Harvest-maturity case study, all settings\n\n" + open(p14).read())
    figs = [("fig5_ablation", "Ablation of TJ+N: mean coverage (left) and median interval score relative to TJ+N (right)."),
            ("fig7_conditional_coverage", "Coverage within thirds of the difficulty σ(x) of the test spectra (main pipelines, α = 0.10)."),
            ("fig8_error_analysis", "Miss rate by Q-residual quintile of the test spectra (first 100 repetitions)."),
            ("fig10_coverage_distribution", "Distribution over repetitions of the realised coverage for one scenario per data set; the guarantee concerns the mean."),
            ("fig_training_conditional", "Share of standard sets whose realised coverage reached 0.85, by number of standards (median over scenarios)."),
            ("fig_batch_mechanism", "TJ+N coverage for new consignments against the intra-consignment correlation of the errors, by design. Within the narrow ICC range observed, the design (number of consignments) rather than the ICC determined coverage."),
            ("fig4_width_vs_m", "Median interval width relative to RMSEP for methods that were not too narrow."),
            ("figS1_cnn_training", "Training and validation loss of the 1D-CNN (mango, seasons 1–3)."),
            ("figS2_friedman_ranks", "Mean Friedman ranks of the scenario median interval score over the 40 main scenarios (descriptive)."),
            ("fig9_timing", "Wall-clock time per test batch (one CPU core, median of 20 runs).")]
    for i, (f, cap) in enumerate(figs, 1):
        P.append(f"# Fig. S{i}\n\n![**Fig. S{i}.** {cap}](figures/{f}.png){{width=13cm}}\n\n")
    mdp = os.path.join(HERE, "supplementary_filled.md"); open(mdp, "w").write("\n".join(P))
    out = os.path.join(ROOT, "supplementary", "Supplementary_Material.docx"); os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["pandoc", mdp, "-o", out, "--reference-doc", os.path.join(HERE, "reference.docx"), "--resource-path", ROOT], check=True, cwd=ROOT)
    from postprocess_docx import postprocess
    postprocess(out)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(out), out], check=True, capture_output=True)
    print("built", out)

if __name__ == "__main__":
    import sys; sys.path.insert(0, HERE)
    main()
