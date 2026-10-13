# Pre-registered research design (written before any target-domain result was computed)

Date fixed: 2026-10-13. Any deviation made after results were seen is logged in `deviations.md`, with its reason.

## Working title
Distribution-free prediction intervals for transferred multivariate calibrations: reusing transfer standards through leave-one-standard-out jackknife+

## Problem
A calibration model *f* (e.g. PLS) is built on a **source** domain (master instrument / past seasons) and deployed on a **target** domain (secondary instrument / new season) after calibration transfer or model updating. The transfer uses a small set of *m* **transfer standards** measured in the target domain: for PDS/DS also on the master; for slope/bias correction (SBC), with reference values. Analysts need prediction intervals with a stated coverage for target predictions. Reference-analysed target samples are expensive.

## Hypotheses
* **H1.** Interval methods calibrated in the source domain (parametric PLS intervals, source split conformal, covariate-shift weighted conformal) under-cover after instrument or season shift, even after calibration transfer.
* **H2.** The proposed transfer jackknife+ (**TJ+**) attains at least nominal coverage (theoretical floor 1−2α; empirically ≈1−α) when the standards are a random sample of the target population. It does so with the same *m* standards used to fit the transfer, and gives narrower intervals than the valid alternative that splits the standards (**SCP-T-split**).
* **H3.** Normalising the TJ+ scores with a source-learned chemometric difficulty function σ(x) (built from Hotelling T² and Q residual) reduces the mean interval score and improves coverage balance across difficulty strata, compared with unnormalised TJ+.

## Research questions → experiments
| RQ | Question | Experiment |
|---|---|---|
| RQ1 | Are conventional intervals valid after transfer/update? | E1 main evaluation, E2 baseline comparison |
| RQ2 | Is TJ+ valid and efficient for realistic standard budgets *m*? | E1, E2, E7 (sensitivity to *m*, α) |
| RQ3 | Does each TJ+ component matter (leave-one-out re-fitting, "+" construction, σ normalisation)? | E3 ablation |
| RQ4 | How robust is validity to non-random (Kennard–Stone) standards, spectral noise, residual wavelength misalignment, and reduced source data? | E4 robustness |
| RQ5 | Does the behaviour generalise across instruments, properties, shift types (instrument vs season) and model classes (PLS, ridge, 1D-CNN)? | E5 generalisation |
| RQ6 | What does TJ+ cost computationally? | E6 efficiency |
| RQ7 (exploratory) | Can a label-free variant using unlabelled paired standards approximate validity? | E1 secondary |
| — | Where and why do intervals fail? | E8 error analysis |

## Datasets (public)
1. **Corn** (Eigenvector Research; Cargill): 80 samples, NIR 1100–2498 nm (700 channels), instruments m5 (master), mp5, mp6; moisture, oil, protein, starch.
2. **IDRC Shootout 2002 pharmaceutical tablets** (Eigenvector): 655 tablets on instruments 1 and 2, 600–1898 nm (650 channels); calibrate (155) / validate (40) / test (460); assay (API, mg), weight, hardness.
3. **Mango DMC** (Anderson et al. 2020; Mendeley 10.17632/46htwnp833, file `NAnderson2020MendeleyMangoNIRData.csv`, SHA-256 86159e2d…f153f): 11,691 spectra, ~4,677 fruit, seasons 1–4. Season 4 (designated external set) is the target domain. Region 684–990 nm.

## Protocol (fixed)
* **Repetitions.** Corn R = 500 per scenario. Tablets R = 500. Mango R = 300. Seeds: `base_seed = 20261013`; repetition *r* uses `base_seed + r`. Seeds are fixed in advance and never selected on results.
* **Corn split per repetition.** Random 40 samples for source training (m5 spectra) and 10 for source calibration (m5). The remaining 30 form the target pool on the slave. From the pool, *m* random standards; the rest (30−*m*) are test. *m* ∈ {10, 15, 20}. Scenarios: m5→mp5 and m5→mp6, × 4 properties.
* **Tablets.** Source training = calibrate set on instrument 1 (155), plus source calibration = validate set on instrument 1 (40); both are fixed. Target pool = test set on instrument 2 (460); for PDS/DS, the paired instrument-1 spectra of the standards are used. *m* ∈ {10, 20, 30, 50}. Properties: assay (primary), weight, hardness.
* **Mango.** Spectra are averaged per fruit. Source = seasons 1–3, split by fruit (seed-fixed, once) into 80% training and 20% calibration. Target = season 4 fruit (725), *m* ∈ {10, 20, 30, 50}, with the remaining fruit as test.
* **Preprocessing and model selection, source only.** The preprocessing is chosen from {none, SNV, SG 1st derivative (w = 11, p = 2), SG 2nd derivative (w = 13, p = 2)} by 10-fold CV RMSE on source training data. The number of PLS latent variables is chosen by 10-fold CV on source training (maximum 15 for corn/tablets, 25 for mango), using the 1-SE rule. Target data are never used for these choices.
* **Transfer methods.** None; SBC (slope/bias correction fitted on the standards' predictions and reference values); DS (pseudo-inverse); PDS (window 5, i.e. half-width 2, least squares via truncated pseudo-inverse with relative tolerance 1e-2, plus intercept). Preprocessing is applied after spectral transfer. Mango (same instrument) uses None and SBC only. **Primary pipeline:** PDS for corn and tablets, SBC for mango.
* **α.** 0.10 is primary; 0.05 and 0.20 are sensitivity analyses.

## Interval methods
Notation: ŷ(x) is the deployed point prediction (after transfer).
* **ASTM-PI (classical):** ŷ ± t_{1−α/2, n−A−1} · SEC · √(1 + h(x)), where h is the leverage in the source PLS score space.
* **SCP-S:** split conformal using |residuals| on the source calibration set (in-domain source spectra).
* **WCP-S:** weighted split conformal (Tibshirani et al. 2019). Likelihood ratios come from a logistic-regression domain classifier on the PLS scores of source-calibration versus target-pool spectra (transferred, unlabelled; transductive use of test spectra is allowed).
* **Gauss-LOO:** ŷ ± t_{1−α/2, m−1} · RMSE_LOO, where RMSE_LOO comes from leave-one-standard-out residuals.
* **SCP-T-split:** split the standards in half; the first half fits the transfer and the second half calibrates split conformal (exactly valid).
* **Transport (regression analogue of Doula 2026):** fit a master→slave mapping on the standards, map the source-calibration spectra into slave space, pass them through the deployed pipeline, and take the conformal quantile of their residuals. Paired-spectra transfers only.
* **MC-dropout (CNN only, mango):** predictive interval from 100 dropout samples, assuming Gaussian errors.
* **Proposed TJ+:** for each standard *i*, re-fit the transfer on the remaining *m*−1 standards to obtain μ₋ᵢ, and compute Rᵢ = |yᵢ − μ₋ᵢ(xᵢ)| / σ(xᵢ). The interval is C(x) = [ q⁻_α{μ₋ᵢ(x) − σ(x)Rᵢ}, q⁺_α{μ₋ᵢ(x) + σ(x)Rᵢ} ].
  * **TJ+N** (primary): σ(x) = max(ε, a + b√T²(x) + c√Q(x)). It is fitted by non-negative least squares to the absolute out-of-fold source-training residuals, and is fixed before any target data are seen.
  * **TJ+** (σ ≡ 1).
* **Ablations:**
  * TJ-naive: jackknife without "+", i.e. ŷ_full ± q⁺(Rᵢ).
  * TJ-insample: residuals from the transfer fitted on all *m* standards, with no leave-one-out.
  * TCV+: 5-fold CV+.
  * TJ+N with σ from T² only and from Q only.
* **Label-free (exploratory) LF-conv:** dᵢ = f(g₋ᵢ(xᵢᵀ)) − f(xᵢˢ) (LOO transfer discrepancy on paired, unlabelled standards); eⱼ = source-calibration residuals. The interval is ŷ + quantiles_{α/2, 1−α/2} of {eⱼ − dᵢ}. It has no finite-sample guarantee.

**Source residual pool (fairness, fixed before results).** All source-calibrated baselines (SCP-S, WCP-S, Transport, LF-conv residuals eⱼ) use the union of (i) source-calibration residuals and (ii) out-of-fold residuals from the 10-fold CV on source training at the selected settings. This maximises their calibration sample size (corn: 50 instead of 10). OOF residuals are slightly pessimistic, which, if anything, favours the baselines' coverage.

## Metrics
* Per repetition: empirical coverage on test samples; mean width (finite intervals only); fraction of infinite intervals; Winkler interval score IS = width + (2/α)·exceedance; RMSEP of the point prediction.
* Aggregated over repetitions: mean coverage with 95% percentile-bootstrap CI (2,000 resamples of repetitions); 5th percentile of per-repetition coverage; median width; mean IS (repetitions with infinite intervals are reported separately).
* Conditional coverage: by tertiles of σ(x) and of the reference value y.
* **Validity criterion (pre-registered):** a method is flagged *under-covering* when the upper bound of the 95% CI of mean coverage is < 1−α.

## Statistical analysis
* **Within each scenario:** TJ+N against each baseline, on the paired per-repetition interval score (same splits). Two-sided Wilcoxon signed-rank test; effect size as matched-pairs rank-biserial correlation and median difference with bootstrap CI. Holm correction within each scenario. Repetitions are independent random draws of splits, so inference is conditional on the dataset (stated as such).
* **Across scenarios:** Friedman test on each method's mean IS ranks over scenarios (dataset × property × instrument pair × *m*), with Holm-corrected pairwise Wilcoxon tests against TJ+N (Demšar 2006 style).
* Any method's interval score is compared only among methods that are not under-covering; "narrower but invalid" is never reported as a win.

## Robustness (E4)
Conditions, each on the primary pipelines:
* Kennard–Stone standard selection.
* Gaussian noise added to target spectra (SNR 1000, 300, 100 relative to spectral SD).
* Residual wavelength shift of target spectra by ±1 channel after transfer is fitted (applied to test spectra only, simulating drift after standardisation).
* Source training size halved.

## Generalisation (E5)
* Corn: mp5 and mp6, plus the reverse direction mp5→m5.
* Tablets: all three properties.
* Mango: season shift.
* Model classes: PLS (primary), ridge regression (all datasets), 1D-CNN (mango only; trained once on source data).

## Efficiency (E6)
Wall-clock time per interval method (fit + predict) and number of model/transfer refits.

## Error analysis (E8)
* Miss rates against T², Q and y-extremity.
* Upper vs lower misses.
* Repetitions with lowest coverage: inspect standard composition (range of y covered).

## Leakage audit (Phase 8)
* Duplicates: each corn/tablet sample appears once per instrument. Test samples are never standards, and never source training/calibration samples, in the same repetition.
* Mango replicate scans (2–6 per fruit) are averaged per fruit before splitting, which eliminates replicate leakage. Seasons 1–3 versus season 4 is a temporal split.
* Preprocessing parameters with fitted state (mean centring) come from source training only; SNV/SG are per-spectrum operations. The PDS/SBC transfer is refitted inside each leave-one-out fold.
* The σ(x) model and LV selection use only source data.
* Hyperparameters that influence target results (PDS window, α, *m*) are fixed here, or examined only as declared sensitivity analyses.
