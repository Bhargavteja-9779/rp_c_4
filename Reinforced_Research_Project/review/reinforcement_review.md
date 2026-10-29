# Reinforcement review (Phase 8): what the new experiments established

All numbers below come from `results/statistics_reinforcement.json`, `results/summary/*.csv` and `manuscript/build/values.json`. They are generated from the raw results by `code/run_reinforcement.py --skip-experiments` and `manuscript/build/values_reinforced.py`.

## Hypotheses: supported or rejected

| Hypothesis (protocol) | Result | Verdict |
|---|---|---|
| H10a: with standards from 2 consignments, sample-level TJ+N under-covers new-batch samples in most cells (α = 0.10) | Too narrow in 6 of 8 cells, coverage 0.67–0.91. Gauss-LOO 8/8, split 8/8, ANOVA-PI 8/8, ASTM-PI 8/8, SCP-S 8/8. Damage largest for SBC (0.67–0.77). | **Supported** |
| H10b: TJ+G, TJ+G-N, TJ+H, TJ+H-N never too narrow where bounded (random designs) | TJ+H-N 0 of 58 bounded cells; TJ+G, TJ+G-N and TJ+H each 0 of 58 (statistics JSON). Coverage 0.90–0.98 at 90%. | **Supported** |
| H10c: one standard per consignment makes sample-level TJ+N valid | 0 of 42 cells over three α levels (15 × 1, 20 × 1) | **Supported** |
| H10d: deficit increases with the ICC of target errors | Spearman 0.52, p = 0.18 (n = 8 cells). ICC was high everywhere (0.46–0.63 in random designs), so it did not discriminate between cells. Coverage was governed by K. | **Not supported** (inconclusive; reported as such, figure moved to the supplement) |
| H10e: chronological design (exploratory) | TJ+N too narrow in 3/8, Gauss-LOO 7/8, ANOVA-PI 5/8, ASTM-PI 8/8. TJ+B unbounded at 90% (K = 5); at 80% it covered 0.89–1.00. | Reported descriptively |
| H11a: OLS-PI valid at 90% in most SBC scenarios, failing at 95% | Too narrow in 2 of 52 at 90% and 16 of 52 at 95%. Where both were valid at 90%, OLS-PI was narrower (lower interval score) in 33 of 50, TJ+N in 7. | **Supported**; OLS-PI is the more efficient choice for SBC at 90% |
| H11b: Boot-T under-covers at small m | 52 of 100 at 90% (19 of 29 with m = 10), and also at larger m | **Supported** (stronger than expected) |
| H11c: TJ+N never too narrow in E11 | 0 of 300 | **Supported** (as theory predicts) |
| H12: Gaussian deficit associated with LOO-scale optimism and kurtosis | Gauss-LOO: skewness ρ = 0.35 and RMSEP/RMSE_LOO ρ = 0.35 (both p < 0.001), excess kurtosis ρ = 0.17 (p = 0.08). OLS-PI: skewness ρ = 0.54, kurtosis ρ = 0.41. | **Partly supported** (skewness rather than kurtosis dominates for Gauss-LOO) |
| E13: positive evidence of near-nominal coverage | TJ+N non-inferior (CI lower ≥ nominal − 0.02) in 192 of 192 scenario × α cells. Per-set reliability: median share of standard sets with realised coverage ≥ 0.85 = 0.88 (minimum 0.74); Gauss-LOO 0.82. | Confirms validity; quantifies the training-conditional limitation |
| E14 (application) | Point rule passed 45% of immature fruit, ASTM-PI 21%. TJ+N passed 8.4% with 2 × 10 standards and 3.8% with 10 × 2; TJ+B passed 1.3% with 10 × 2. Referral rates were 56–67% for TJ+N and 67–100% for TJ+B, depending on the design. | Translates E10 into decision terms; shows the price (referrals) honestly |

## Which changes materially improved the contribution

1. **E10 changes what the paper is about.** The paper's headline used to be a validity result that theory guarantees. It is now a practically decisive, previously untested finding on real batch structure: the unit of exchangeability of transfer standards. The design rule (spread the standards over many batches) costs nothing to apply. It is supported by theory (Appendix B) and by data from 4 settings with 8 pipeline combinations.
2. **E11 sharpened the efficiency message instead of weakening the paper.** The paper now says plainly that:
   - for SBC at 90%, the textbook OLS interval is usually narrower;
   - Gaussian intervals are acceptable at 90%;
   - the bootstrap is not acceptable.
   Its value lies at 95% and in the guarantee, not in narrower intervals.
3. **E14 provides the application perspective that ACA readers and editors look for.**

## Additions with no measurable benefit

- **The ICC mechanism (H10d).** It did not explain differences between cells and was moved to the supplement.
- **The max-score variant TJ+G.** It gave practically the same results as the hierarchical TJ+B. It was kept only in Appendix B, as a simple, self-contained proof.

## Original claims that had to be weakened

- **"TJ+N is the proposed method that is valid where others fail."** This is now presented as a confirmation of known theory under random standards. Validity under realistic batch sampling *fails* for sample-level TJ+N (H10a).
- **Normalisation as a contribution.** It is now explicitly a refinement with modest effect.
- **Novelty.** No new conformal methodology is claimed. The batch-level construction is credited to Lee, Barber & Willett (2026).
- **"Valid whenever its assumptions held."** This is kept, but the paper now spells out that random sampling of *batches*, not of samples, is the assumption that matters in practice.

## New limitations that emerged

1. The batch evidence comes from one product (mango).
2. Interval rules refer a large share of fruit for re-measurement near the decision threshold. This is a property of the measurement precision, not of the method, and the paper reports it plainly.
3. TJ+B needs at least nine batches for 90% statements, which may be more than some laboratories can collect.
