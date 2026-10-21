# Research reinforcement plan (Phase 6)

**Prioritisation.** Changes are ranked by scientific impact × feasibility × risk reduction. The first step was to work out what the scientific argument lacks (see `audit/novelty_reassessment.md`); additions were chosen only where they address an identified weakness. No model component was added to the method itself.

| Rank | Change | Addresses | Impact | Feasibility | Cost |
|---|---|---|---|---|---|
| 1 | E10: real-lot standards → new-lot samples; sample- vs batch-level constructions | R01, R02, R03, R09 | Very high: turns a theorem check into a practically decisive finding | High: lot labels exist in the mango data | ≈30 CPU-min × 4 cores |
| 2 | E11: classical/bootstrap competitors on identical splits | R04 | High | High | ≈2 h on 4 cores (bootstrap B = 200) |
| 3 | E13: non-inferiority, training-conditional and clustered re-analysis | R05, R06, R07 | Medium | Very high (no new data) | Minutes |
| 4 | E12: mechanism of Gaussian failure | R11 | Medium | High (recorded within E11) | Negligible |
| 5 | Reframing: analytical-validation vocabulary, contribution list, length | R01, R08, R12, R16 | High (editorial) | High | Writing |

## Specification of each change

### 1. E10 — unit of exchangeability of transfer standards

1. **Deficiency.** Every validity result assumes standards drawn at random from the same pool as the routine samples.
2. **Evidence it matters.** Errors of a transferred model plausibly share a lot-specific bias (cultivar, maturity, harvest date). The mango season-4 lots differ in mean DM from 13.2% to 19.4%. A unit-test simulation shows that sample-level TJ+ coverage falls below 0.75 when lots carry a bias and the standards come from 2 lots.
3. **Proposed improvement.** Test sample-level intervals (TJ+N, Gauss-LOO, split, ASTM-PI, SCP-S) against batch-level ones under real lot designs and a chronological design. The batch-level constructions are:
   - TJ+H(-N): hierarchical jackknife+ of Lee et al., instantiated for the transfer step;
   - TJ+G(-N): max-score variant;
   - LGO-CV+N;
   - Gauss-LGO;
   - ANOVA-PI.
4. **Hypotheses.** H10a–H10e (protocol).
5. **Implementation.** `intervals/group.py`, `experiments/batch.py`, `data/meta.py`; tests in `tests/test_reinforcement.py`.
6. **Experiment.** Four real settings (one season shift, three instrument shifts) × 5–6 designs × 2 pipelines × 3 α levels, with 300 repetitions.
7. **Expected result if true.** Sample-level intervals under-cover new lots when K is small. Batch-level constructions are valid where bounded and need K ≥ 9 lots at 90%. With one standard per lot, ordinary TJ+ is valid.
8. **If false.** If lot effects after transfer are small, sample-level TJ+ is robust here. This is reported with the ICC values that explain it, and the design rule becomes a precaution rather than a necessity.
9. **Cost.** About 30 min wall time on 4 cores.
10. **Effect on the main contribution.** It changes the paper from "a method that works where theory says it works" into "when an uncertainty statement for a transferred calibration holds, and what that requires of the standards".
11. **Verification criterion.** Executed as pre-registered (plus deviation R1 before any result). Unit tests pass. Under-coverage and non-inferiority statistics are reported for every cell.
12. **Objection addressed.** "In practice standards are not random" and "the guarantee is borrowed".

### 2. E11 — simpler-method challenge

1. **Deficiency.** The textbook procedures that a chemometrician would use first were not compared.
2. **Evidence it matters.** SBC is OLS on m points, so its exact Gaussian prediction interval exists. Bootstrap uncertainty is standard practice in ACA (Chiappini et al. 2025).
3. **Improvement.** Add OLS-PI (SBC), Boot-T (B = 200) and ASTM-T on identical splits.
4. **Hypotheses.** H11a–c.
5. **Implementation.** `intervals/classical.py`, dispatch in `experiments/core.py`.
6. **Experiment.** 200 repetitions over all data sets and pipelines, at the three α levels.
7. **Expected result if true.** OLS-PI is valid at 90% but fails at 95% in heavy-tailed scenarios. Boot-T under-covers at small m.
8. **If false.** If OLS-PI or Boot-T is valid everywhere and narrower, TJ+N's value reduces to the guarantee, and this is stated plainly.
9. **Cost.** About 2 h.
10. **Effect.** Turns the efficiency discussion into a decision rule for practitioners.
11. **Verification criterion.** All methods are reported with flags and paired tests.
12. **Objection addressed.** "Why not the textbook interval / the bootstrap?"

### 3. E13 — positive statistical evidence

1. **Deficiency.** Validity is supported only by the absence of a detected deficit; dependence between scenarios is handled descriptively; per-standard-set reliability is not quantified.
2. **Improvement.**
   - Non-inferiority (margin 0.02).
   - Share of standard draws with realised coverage ≥ 1−α−0.05. This is the β-content analogue: training-conditional reliability.
   - Clustered bootstrap over repetitions across all scenarios of a data set.
3. **Hypothesis.** TJ+N is non-inferior in all primary cells. Its training-conditional share is similar to that of other valid methods; no method offers a per-set guarantee at small m.
4. **If false.** Report which cells fail non-inferiority, and weaken the claims accordingly.
5. **Cost.** Minutes.
6. **Objection addressed.** Statistician R05–R07.

### 4. E12 — mechanism

1. **Deficiency.** Gaussian failures at 95% are documented but unexplained.
2. **Improvement.** Per-repetition error-shape statistics (skewness, excess kurtosis, RMSEP/RMSE_LOO, bias, heteroscedasticity), associated with the coverage deficit at the scenario level.
3. **If false.** If no association is found, report that the mechanism remains open.
4. **Objection addressed.** The competing-group explanation (R11).

### 5. Manuscript reconstruction

1. **Deficiency.** The current framing claims a method.
2. **Improvement.** The framing becomes a validity question:
   - the evidence and conditions are in the foreground;
   - analytical-validation vocabulary is used (β-expectation / β-content tolerance intervals);
   - normalisation is demoted to a secondary component (R12);
   - the main text is shortened (R16).

## Explicitly rejected additions

- **New interval architectures, learned difficulty functions, deep models.** These do not address any identified weakness, and they would add complexity (prompt: "do not add layers").
- **Additional data sets without lot labels.** They cannot test the critical external-validity question. No public NIR transfer data set with lot labels was identified besides mango.
- **Training-conditional (PAC) variant of TJ+.** Theory shows that no general guarantee exists for jackknife+ (Bian & Barber 2023), and a stability-based route (Liang & Barber 2025) would require constants that cannot be computed for PDS. It is left as future work; empirical reliability is reported instead (E13).
