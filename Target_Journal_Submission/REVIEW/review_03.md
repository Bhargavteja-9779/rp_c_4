# Review round 3 — Reviewer #3 (statistical validity and experimental fairness)

**Recommendation:** Minor-to-major revision. The design is pre-registered and the unit of analysis is mostly appropriate, but several inferential statements need qualification. My concerns do not overlap with Reviewers #1–2.

## MAJOR
| # | Issue | Evidence / reasoning | Required fix |
|---|---|---|---|
| S1 | **Power of the validity criterion is not reported.** "Not flagged" is used as evidence of validity, but a method slightly below nominal (e.g. 0.895) will not be flagged if the CI is wide. Readers need the precision of the coverage estimates. | Corn has 10–20 test samples per repetition; tablets ≈410–450; mango ≈675–715. CI widths therefore differ between data sets. | Report the half-width of the 95% CI of mean coverage (TJ+N, per data set), and state that "not flagged" means "not significantly below nominal at this precision". |
| S2 | **Dependence between scenarios in the Friedman test.** The 40 scenarios are not independent: corn properties share the same samples and splits, and *m* levels share data. The Friedman *p*-value (3.6 × 10⁻²⁸) therefore overstates the evidence. | Scenarios with the same data set, target instrument and repetition seeds are correlated. | Present the Friedman ranks as descriptive. State the dependence explicitly, and base inferential statements on the within-scenario paired tests, where the repetition is the unit and the pairs are genuinely matched. |
| S3 | **Fairness of the classical baseline.** ASTM-PI uses the in-sample SEC; a cross-validated error (SECV) would give wider intervals. | The comparison could be seen as using a deliberately optimistic classical interval. | Point out that SCP-S, which uses out-of-fold (cross-validated) source residuals, is the cross-validated analogue and also under-covered severely (corn 0.05–0.68). The source-domain error model, not the SEC/SECV choice, is what fails. |

## MODERATE
| # | Issue | Fix |
|---|---|---|
| s1 | The bootstrap CI over repetitions is conditional on the fixed data sets (repetitions reuse the same samples). This is stated in §3.2 but should be recalled where population-level statements are made (Conclusions). | Add "for these data sets" qualifiers where needed. |
| s2 | Ties in the leave-one-out residuals (possible with SBC on duplicated reference values) could affect the strict inequality in Appendix A. | Note that ties have probability zero for continuous scores, and that ties only make the jackknife+ more conservative. |
| s3 | The median IS differences with bootstrap CIs are computed (paired_tests.csv) but not reported. | Point to Supplementary Table S5 and the CSV file. |
| s4 | The "valid" criterion is applied per scenario without multiplicity control. For the *baselines* this favours flagging (more false positives), whereas for TJ+N it is conservative. | State this asymmetry; it does not favour the proposed method. |

## MINOR
- Seeds: confirm in the text that the same repetition seed gives identical standards for all methods (paired design). *(Confirmed in code: the splits depend only on the repetition and m.)*
- Hyperparameters: confirm that no setting was tuned on target data. *(Confirmed: PDS window/tolerance fixed a priori; LVs/preprocessing by source CV.)*
- Leakage: confirmed none in the code audit. Mango fruit-level averaging, disjoint standards/test samples and source-only σ fitting were all checked. For E8, source fruit are disjoint from the target pool by construction.

## Verified as adequate
- A paired design (identical splits across methods) with Wilcoxon signed-rank tests, Holm correction and effect sizes is appropriate.
- Multiple predefined seeds and no seed selection.
- The pre-registered validity criterion was applied mechanically.
