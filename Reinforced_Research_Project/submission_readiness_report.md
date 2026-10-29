# Submission readiness report (Parts XII–XIII)

**Manuscript:** *Trustworthy prediction intervals after moving an NIR calibration to a new instrument or season: how many reference samples, and from how many batches?*
**Target:** *Analytica Chimica Acta* (Elsevier), retained after reinforcement.

## 1. Original weaknesses identified

The project was inspected component by component (`audit/project_integrity_report.md`). It was technically sound:

- 64/64 raw-file hashes matched;
- 175/175 manuscript values regenerated identically;
- the tests passed;
- no data leakage was found.

The weaknesses were scientific (`audit/rejection_risk_register.md`, `audit/novelty_reassessment.md`):

1. **Critical.** The headline result ("TJ+N never under-covers") was guaranteed by existing theory, because standards and test samples were drawn at random from the same pool.
2. **Critical.** The realistic case was never tested: standards from a few lots, routine samples from new lots. The data even contained the lot information.
3. **Major.** Classical competitors that an analytical chemist would use first were missing: the OLS interval for slope/bias correction, a bootstrap, the re-estimated ASTM interval, and random-effects intervals for new batches.
4. **Major.** The closest statistical prior art, the hierarchical jackknife+ of Lee, Barber & Willett (2026), was not cited.
5. **Moderate.** Validity was supported only by absence of evidence. There was no non-inferiority or per-set reliability analysis.
6. **Moderate.** The manuscript was framed as a method paper, was long (≈9,100 words), and was not written in the language of analytical method validation.

## 2. Scientific changes made

- **Reformulation.** The paper now asks a laboratory question: can uncertainty statements survive calibration transfer, and how must the reference samples be collected? The jackknife+ is presented as the reference construction, and no new statistics is claimed. The batch-level version is credited to Lee et al.
- **Application framing**, at the corresponding author's request:
  - a mango harvest-maturity case study at the published 14% dry-matter minimum;
  - a plain-language title and procedure;
  - a four-step overview figure;
  - prose rewritten to remove formulaic phrasing.
- **New experiments**, specified in a protocol committed before the full runs (`research_design/revised_experimental_protocol.md`, deviations R1–R3):

| Experiment | Content | Size |
|---|---|---|
| E10 | Standards from K consignments × n_g fruit; test on new consignments; plus a chronological design | 4 settings, 8 setting-pipeline combinations, 300 repetitions |
| E11 | Simpler formulas on identical standards | 100 scenario-pipeline combinations, 200 repetitions |
| E12 | Error-shape mechanism | — |
| E13 | Non-inferiority, per-set reliability, clustered CIs | — |
| E14 | Harvest-maturity case study | 200 repetitions |

## 3. Actual results obtained

These are the headline results. Every value is generated from `results/`.

- **Source intervals fail after transfer.** Intervals carried over from the original calibration fell to coverage as low as 0.03 for a nominal 0.90. The exception was Transport on the handheld pairs, which stayed valid but was more than twice as wide.
- **TJ+N holds with random standards, as theory says.**
  - It was never too narrow in the 40 main scenarios.
  - It was non-inferior (within 0.02 of nominal) in 192/192 scenario × α cells.
  - It was unbounded at 95% when m < 19 (20/40 main scenarios; 45/100 in E11).
- **Simpler formulas are nearly as good at 90% and slightly worse at 95%.**
  - OLS-PI was narrower than TJ+N in 33/50 slope/bias scenarios.
  - At 95% with m ≥ 20, Gauss-LOO was too narrow in 16/55 combinations and TJ+N in 0/55. The shortfalls were 1–2 percentage points (Gauss-LOO non-inferior in 77/100).
  - The bootstrap, as implemented, was too narrow in 52/100.
- **Batch sampling decides validity for new batches** (main new finding).
  - With 2 × 10 standards, sample-level TJ+N was too narrow for new consignments in 6/8 combinations (coverage 0.67–0.91).
  - Gauss-LOO and split intervals were too narrow in 8/8.
  - With 20 × 1 standards, TJ+N was too narrow in 0/6.
  - Leaving out whole consignments worked whatever the formula:
    - TJ+B was too narrow in 0/22 (90%), 0/30 (80%) and 0/6 (95%) of its bounded cells.
    - Gauss-LGO was too narrow in 0/38.
    - The corrected ANOVA-PI was too narrow in 2/8 at K = 2 and 0/8 from K = 5.
  - The chronological design (one configuration per setting) defeated most methods.
  - Hypothesis H10d (the ICC drives the deficit) was **not** supported.
- **Application (slope/bias correction).**
  - Passing fruit on the predicted value alone accepted 36% of immature fruit.
  - 90% intervals from fruit of ten consignments cut this to 3.2%, against 9.8% with fruit from two consignments.
  - TJ+N and the Gaussian interval behaved identically here.
  - About half of the fruit had to be referred for re-measurement.

## 4. Changes to the central contribution

| Before | After |
|---|---|
| "A new method that gives valid intervals after transfer" | "Uncertainty statements do not survive transfer. The transfer standards can restore them, but they hold for new batches only if the standards span many batches. Leave-one-batch-out error estimation, with the jackknife+ or even a *t*-interval, does this. A cost-free sampling rule follows, and its effect on a real accept/reject decision is shown." |

## 5. Rejection risks reduced, and those remaining

| Risk | Status |
|---|---|
| Headline is theory-guaranteed | Reduced: reframed, with a new headline finding |
| Unrealistic sampling | Reduced (E10) |
| Missing classical baselines | Reduced (E11; ANOVA-PI corrected after the second review) |
| Uncited prior art | Resolved |
| Absence-of-evidence statistics | Reduced (E13) |
| Unfair 95% comparison (found in the second review) | Resolved |
| Overclaimed application | Resolved: SBC only; TJ+N = Gauss-LOO stated |
| **Novelty** | **Remains the main risk.** No new statistics; simple formulas are close at 90%; the batch rule follows random-effects reasoning |
| **Generality** | **Remains.** Batch evidence comes from one product (mango); the 8 combinations are closer to 2 independent settings |
| Bootstrap implementation | Remains (labelled as implementation-specific) |
| **72-day acceptance target** | **Not controllable** |

## 6. Journal suitability and the 72-day constraint

ACA remains the best match among journals whose timelines can be measured: high scope fit, median submission-to-acceptance 59 days, 67.8% (95% CI 63.6–72.0%) of accepted research papers accepted within 72 days, n = 500, PubMed history dates 2025-10 to 2026-10. **The 72-day constraint is verified only as a historical distribution, not for this manuscript.** About one accepted paper in three takes longer, and a second review round would very likely exceed 72 days (90th percentile 103 days).

Other journals:

- *Talanta*: 57.5% within 72 days; the documented fallback.
- *J. Chemometrics*: median 124 days; rejected under the constraint.
- *CILS*, RSC and SAGE journals: timelines not verifiable, so not eligible.

JIF and quartile could not be verified against JCR from this environment. See `audit/journal_fit_assessment.md`.

## 7. Author actions required before submission

1. Complete the author names, affiliations, corresponding-author details, CRediT roles, funding statement and suggested reviewers.
2. Deposit the code and results in a public archive (e.g. Zenodo) and insert the URL/DOI in the data-availability statement and the cover letter.
3. Check the current ACA guide for authors (the page returned HTTP 403 here) and the JIF/quartile in JCR.
4. Decide on the title. The current title follows the request for a plain, student-friendly wording. The independent reviewer suggested a more technical alternative: "Valid prediction intervals for transferred NIR calibrations: leave-one-out re-fitting of the transfer step and sampling standards across batches".
5. Review the generative-AI declaration.

## 8. Final decision (Part XIII)

*(completed after the verification pass; see below)*
