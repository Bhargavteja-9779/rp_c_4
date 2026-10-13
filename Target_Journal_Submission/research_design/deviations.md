# Deviations from the pre-registered design

| # | Deviation | When / why | Effect on conclusions |
|---|---|---|---|
| 1 | Source-calibrated baselines use the union of out-of-fold source-training residuals and source-calibration residuals. | Decided **before any result was computed** (fairness: corn has only 10 calibration samples); added to the pre-registration text before the first run. | Favours the baselines (larger calibration pool). |
| 2 | 1D-CNN (mango, E5): σ(x) and the source residual pool use source-calibration residuals instead of 10-fold OOF residuals; the CNN is trained once with early stopping on a 10% split of source training. | Implementation stage, for compute reasons (no 10-fold CNN retraining). Decided before any CNN result. | None on validity (σ is still fixed before target data are seen). |
| 3 | The PDS solver uses an eigen-decomposition of the window Gram matrices instead of an SVD pseudo-inverse. | Implementation stage, for speed. Numerically identical (max coefficient difference 5e-12, tested). | None. |
| 4 | A CNN prediction cache keyed by array memory address returned stale predictions during a smoke test. It was removed before any reported CNN run. | Bug found in the 3-repetition smoke test. | None on reported results (bug fixed before the full run). |
