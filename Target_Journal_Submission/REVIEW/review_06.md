# Review round 6 — Reviewer #6 (computational complexity, latency, memory, scalability, deployment)

Question asked: *is the improvement worth its computational cost?* My points are new relative to Reviewers #1–5.

## MAJOR
| # | Issue | Fix |
|---|---|---|
| C1 | **Scaling with *m* is asserted ("linear in *m*") but shown at only one *m* per data set.** | Measure wall-clock time of a single transfer fit and of TJ+N for m = 10, 20, 30, 50 (single core). *(Added: experiment E6b; Supplementary Table S7.)* |
| C2 | **Deployment cost for routine (online) use is not discussed.** For every new spectrum, TJ+ must apply all *m* leave-one-out transfer maps and models, and the *m* maps must be stored. | Quantify the storage (PDS: a p × w coefficient array per map; SBC: two numbers) and the per-sample prediction cost (*m* map applications + *m* source-model predictions). State that the maps are computed once at standardisation time. |
| C3 | **Expensive transfers.** For costly adaptation methods (e.g. di-PLS with hyperparameter search, or neural domain adaptation), *m* refits may be prohibitive. | Recommend CV+ (K refits; TCV+N was valid in all scenarios but more conservative, §4.4) as the cheaper alternative, and state the trade-off. |

## MODERATE
- The timing for TJ+N also includes the five CV+ refits. Report it as an upper bound.
- Energy consumption is not meaningful at these scales (sub-second to seconds on one CPU core); say so briefly instead of omitting it.
- Peak memory (≤ 15 MB) is reported; keep it.

## Verdict on cost-benefit
The cost is negligible for laboratory use. The benefit, validity where all source-calibrated intervals failed, clearly outweighs it. The concerns are about presentation and guidance, not about feasibility.
