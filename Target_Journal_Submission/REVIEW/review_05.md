# Review round 5 — Reviewer #5 (dataset validity, generalisation, domain shift, external validity, deployment)

I tried to invalidate the central claim ("TJ+N stays valid after transfer where conventional intervals fail") on data the authors had not designed for. My concerns are new relative to Reviewers #1–4.

## MAJOR
| # | Issue | Attempt to invalidate / evidence | Required fix |
|---|---|---|---|
| D1 | **Only one season shift and essentially one family of instrument shifts.** Corn (80 samples) and tablets are classic, much-studied benchmarks. Instrument transfer on a second matrix is missing. Intact fruit, where light scattering and sample presentation differ, is exactly where instrument transfer is hardest. | The data providers' extended mango file (Mendeley record v6, `MangoDMC_NIR_Data_v4.csv`) contains spectra of the same fruit on several handheld spectrometers (7,100 reference samples measured on ≥ 2 instruments). This allows an independent, paired instrument-transfer test that the authors did not pre-register. | **Run it (E8).** Source instrument 15006; the three instruments sharing the most fruit (15016, 15014, 15029); PDS and SBC; m = 10–50; 200 repetitions; specified before results. *(Done; see results below.)* |
| D2 | **The mango season split relies on the providers' grouping of replicate scans.** The fruit key (season, region, date, type, cultivar, population, DM) could merge two distinct fruit with identical DM on the same day. | 4,677 groups were found, with sizes 1–6. 404 single-scan groups and a few groups of 3–5 scans show that the key is not a perfect fruit identifier. | Report the group-size distribution. Note that rare merges of two fruit with identical metadata would only average their spectra, without creating train/test leakage, because a merged group is always on one side of the split. |
| D3 | **Target pools are finite and reused across repetitions.** Every corn test sample appears in many repetitions. "Coverage" therefore refers to these 80 samples, not to the population of corn. | Inherent in public benchmarks. | Already stated as conditional inference. Repeat it in the Limitations with this concrete consequence. |
| D4 | **Deployment realism.** In routine use, intervals are needed sample by sample over months; standards are measured once. Drift after standardisation (E4) invalidated all methods. | A real risk. | Already reported. Strengthen the recommendation to monitor Q and to re-standardise. Point out that TJ+N, unlike source intervals, makes a failed transfer visible through wide intervals (E8 PDS). |

## E8 results (independent instrument shift; generated after this review)
- With PDS, all source-calibrated intervals under-covered (coverage 0.15–0.51; 36/36 method × scenario cells). With SBC, ASTM-PI and SCP-S under-covered in all 24 cells (0.73–0.81), while WCP-S returned unbounded intervals in almost every repetition (valid but uninformative).
- TJ+N was valid with both pipelines: PDS 0.931 (0/12 under-covering); SBC 0.906 (0/12). At all α levels: 0/72.
- PDS was a poor transfer for these handheld fruit spectrometers (RMSEP 2.03–7.40 % DM vs 1.06–1.22 % with SBC). TJ+N reflected this in wide intervals (median width 11.1 vs 4.0 % DM), whereas the source-calibrated intervals stayed narrow and missed most samples.
- Conclusion: the central claim survives an independent test that was not part of the original design.

## MODERATE
- State the mango record version used for each analysis (v1 for E1–E7, v6 for E8). *(Done: deviation log #8; data availability.)*
- The tablets target pool comes from the organisers' test set, which may differ systematically from calibrate/validate (it was designed as a test set). This is acceptable but should be mentioned.
