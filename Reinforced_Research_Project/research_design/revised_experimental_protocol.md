# Revised experimental protocol: reinforcement experiments E10–E13

**Status.** This protocol was written and committed to version control *before* any full-scale result of E10–E13 was computed. A two-repetition smoke test (`run_reinforcement.py --mode quick`) was run beforehand to check that the pipeline executes. Its numbers are not results; they are not reported, and no design element was changed after it. Seeds depend only on the repetition index (`BASE_SEED = 20261013`). Configuration: `code/config/reinforcement.json`.

The original pre-registered study (E1–E9; `Target_Journal_Submission/research_design/preregistration.md`) is unchanged, and its raw results are reused as they are.

---

## E10 — Batch-structured standards and routine samples from new batches (primary reinforcement)

**Question.** Transfer standards are rarely a simple random sample of individual routine samples. In practice they come from a few production lots or harvest consignments, while routine samples come from later or other lots. Does sample-level TJ+N stay valid for samples from **new batches** when the standards come from K batches? Does the batch-level jackknife+ TJ+G (Proposition 2) restore validity?

**Data (real batch structure; nothing simulated).** A *batch* is a mango population, i.e. a consignment of about 40 fruit of one cultivar, region, maturity stage and harvest date, as defined by the data providers.

- `season`: season shift. The source model is identical to E1 (fruit seasons 1–3, fixed seed). The target is the 725 season-4 fruit in 18 batches. Pipelines: SBC (primary) and no transfer (secondary).
- `inst_15016`, `inst_15014`, `inst_15029`: instrument shift. The source model is identical to E8 (instrument 15006, fruit not measured on the target instrument). The target pools are the fruit measured on both instruments: 49, 38 and 29 batches. Pipelines: PDS and SBC.

**Designs (K batches × n_g standards per batch).**

| Design | Settings | Rule |
|---|---|---|
| random (2, 10), (5, 4), (10, 2), (15, 1) | all | K batches drawn at random among batches with ≥ n_g fruit; n_g standards drawn at random within each |
| random (20, 1) | instrument settings only | as above (needs > 20 batches) |
| chrono (5, 4) | all | batches ordered by first harvest date (ties by label); standards from the 5 earliest; new-batch test set = batches harvested strictly after the latest standard batch |

- **New-batch test set:** all fruit of the batches that are not standard batches.
- **Same-batch test set:** the remaining fruit of the standard batches.

**Methods.**

- *Sample level*: TJ+N, TJ+, Gauss-LOO, SCP-T-split-N, ASTM-PI, SCP-S.
- *Batch level*:
  - TJ+G and TJ+G-N: leave-one-batch-out re-fitting of the transfer step, batch score = largest normalised member residual, jackknife+ ranks over the K batches;
  - LGO-CV+N: CV+ with batches as folds and pooled member scores;
  - Gauss-LGO: t with K−1 degrees of freedom × leave-batch-out RMSE.

**Levels and repetitions.** α ∈ {0.05, 0.10, 0.20}; α = 0.10 is primary. 300 repetitions.

**Outcomes.**

- *Primary:* **batch-weighted coverage** on the new-batch test set, i.e. the mean over new batches of the within-batch coverage. This is the probability addressed by Proposition 2.
- *Secondary:*
  - fruit-weighted coverage;
  - same-batch coverage;
  - median width;
  - fraction of unbounded intervals;
  - interval score;
  - intra-batch correlation (ICC) of the deployed predictor's errors on the new-batch test set;
  - ICC of the leave-one-out residuals of the standards.

**Statistics.**

- Mean coverage over repetitions, with a 95% percentile-bootstrap CI over repetitions (2000 resamples).
- *Under-covering*: CI upper limit < 1 − α, as before.
- *Non-inferiority* (new criterion; see E13): CI lower limit ≥ 1 − α − 0.02.

**Hypotheses (directional, stated in advance).**

- **H10a.** With standards from few batches (K = 2), sample-level TJ+N under-covers new-batch samples in the majority of setting × pipeline cells at α = 0.10.
- **H10b.** TJ+G and TJ+G-N are not flagged as under-covering in any random-design cell in which they are bounded (K ≥ 9 at α = 0.10; K ≥ 19 at α = 0.05; K ≥ 4 at α = 0.20).
- **H10c.** With one standard per batch (n_g = 1), sample-level TJ+N is not flagged in random designs; by Proposition 2 it is then a batch-level jackknife+.
- **H10d (mechanism).** Across cells, the coverage deficit of sample-level TJ+N in the K = 2 design increases with the ICC of the target errors.
- **H10e (exploratory, no guarantee).** Under the chronological design, all methods may under-cover; this cell is reported descriptively.

**Interpretation if false.**

- If H10a fails, batch effects after transfer are small in these data, and sample-level TJ+N is robust to the batch structure here. This would be reported as a positive robustness finding, with the ICC values that explain it.
- If H10b fails in a random design, there is an implementation error or a violated assumption, and it must be investigated before anything else is reported.

---

## E11 — Classical and bootstrap competitors (simpler-method challenge)

**Question.** Do textbook procedures that a chemometrician would use already solve the problem?

**Methods added.**

- **ASTM-T.** The ASTM E1655-type interval re-estimated on the target standards: μ(x) ± t_{m−1}·RMSE_LOO·√(1+h(x)).
- **OLS-PI.** For SBC only. SBC is an OLS regression of y on the source prediction f, so the exact Gaussian regression prediction interval is ŷ ± t_{m−2}·s·√(1 + 1/m + (f−f̄)²/S_ff).
- **Boot-T.** A bootstrap prediction interval:
  - B = 200 pairs-bootstrap refits of the transfer step;
  - centred in-sample residuals, scaled by √(m/(m−p)) with p = 2 for SBC and 0 otherwise;
  - interval from the quantiles of μ*_b(x) − μ(x) − e_j over all b and j (Davison & Hinkley 1997, Alg. 6.4, pairs version).

**Reference methods.** These are re-run on identical splits: TJ+N, TJ+, Gauss-LOO, Gauss-LOO-N, SCP-T-split-N.

**Scenarios.** Corn (PDS, SBC; 24 scenarios each), tablets (PDS, SBC; 12 each), mango season (SBC; 4), mango instruments (PDS, SBC; 12 each). The seeds equal those of E1/E9, so repetition r uses the same standards and test samples as E1 repetition r. 200 repetitions; α ∈ {0.05, 0.10, 0.20}.

**Outcomes and statistics.** As in E1: coverage, the under-coverage flag, interval score, and within-scenario Wilcoxon tests with Holm correction against TJ+N for methods that are not under-covering.

**Hypotheses.**

- **H11a.** OLS-PI is valid at α = 0.10 in most SBC scenarios, but under-covers at α = 0.05 where the target errors are heavy-tailed or heteroscedastic.
- **H11b.** Boot-T under-covers for small m, because bootstrap distributions are too narrow for small samples.
- **H11c.** TJ+N is not flagged in any E11 scenario.

**Interpretation if false.** If OLS-PI or Boot-T is valid everywhere *and* narrower, TJ+N's practical advantage reduces to the guarantee alone, and the manuscript must say so.

## E12 — Mechanism: why do Gaussian intervals fail where they fail?

In every E11 repetition, the following are recorded for the deployed predictor's errors on the test samples:

- skewness;
- excess kurtosis;
- standardised bias;
- the ratio RMSEP / RMSE_LOO, i.e. how well the leave-one-out RMSE estimates the actual error;
- the Spearman correlation of |e| with σ(x).

**Analysis.** A scenario-level regression of the coverage deficit (1 − α − coverage) of Gauss-LOO and OLS-PI at α = 0.05, on the scenario medians of these statistics. Spearman correlations are reported; the analysis is descriptive.

**Hypothesis H12.** The deficit is associated with RMSEP/RMSE_LOO > 1 (an over-optimistic LOO scale for small m) and with excess kurtosis.

## E13 — Statistical re-analysis (no new data)

On E1, E8, E9, E10 and E11 the following are computed:

1. **Non-inferiority of coverage.** The proportion of scenarios whose bootstrap CI lower limit is ≥ 1 − α − 0.02, i.e. *positive* evidence of near-nominal coverage rather than absence of a detected deficit.
2. **Training-conditional reliability.** The share of repetitions (one draw of standards each) whose realised test-set coverage is ≥ 1 − α − 0.05, compared between methods on identical draws.
3. **A scenario-clustered summary.** For each data set, the coverage deficit is averaged over scenarios, with a bootstrap CI that resamples *repetitions jointly across scenarios*, which respects the dependence between scenarios.

## Leakage and correctness checks (Experiment 7 of the brief)

The following unit tests are in `code/tests/test_reinforcement.py`:

- the new-batch test set contains no fruit of a standard batch;
- standards, new-batch and same-batch sets are disjoint;
- the chronological test set is harvested strictly later;
- TJ+G equals TJ+ when every standard is its own batch;
- TJ+G is unbounded when K < ⌈(1−α)(K+1)⌉;
- OLS-PI has exact coverage under Gaussian errors;
- in a Monte Carlo simulation with batch effects, sample-level TJ+ fails while TJ+G holds.

The source models, σ and the source residual pools are unchanged from E1/E8. They use no target data (`source_model.py`; checked in the integrity audit).
