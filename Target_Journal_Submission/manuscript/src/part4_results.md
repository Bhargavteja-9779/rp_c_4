# 4. Results and discussion

## 4.1. Point accuracy after transfer

Calibration transfer was necessary, but it was not equally beneficial everywhere (Table 2).
- **Corn:** applying the master models directly to mp5/mp6 spectra gave RMSEP values {{corn_none_vs_pds}} times larger than after PDS with *m* = 20 standards.
- **Tablets:** PDS reduced the assay RMSEP from {{tab_assay_rmsep_m10}} mg (*m* = 10) to {{tab_assay_rmsep_m50}} mg (*m* = 50). The weight and hardness predictions were insensitive to the transfer.
- **Mango:** SBC did not improve on the uncorrected source model (RMSEP {{mango_sbc_rmsep}} vs {{mango_none_rmsep}} %), consistent with reports that models built over several seasons are already fairly robust [@anderson2020].

All interval methods share the same point predictor within a pipeline, so the comparisons below isolate the interval construction.

{{table_rmsep}}

## 4.2. Conventional intervals after transfer (RQ1)

Source-calibrated intervals under-covered whenever the transfer added error that the source calibration had not seen (Fig. 3; Table 3).
- **Corn:** the mean coverage of nominal 90% intervals was {{src_cov_range_corn}} for ASTM-PI, SCP-S and WCP-S, which were flagged as under-covering in {{src_under_corn}} scenario × method cells.
- **Mango:** coverage was {{src_cov_range_mango}} ({{src_under_mango}} cells under-covering).
- **Tablets:** the picture was mixed ({{src_cov_range_tablets}}; {{src_under_tablets}} cells under-covering). Under-coverage occurred mainly for the assay with few standards, where a poorly determined PDS inflated the error, while weight and hardness were unaffected by the transfer.

Weighting the source residuals for covariate shift (WCP-S) did not repair coverage, and it produced unbounded intervals in {{wcp_inf_pct}} of corn repetitions. When the domains are almost perfectly separable, the estimated likelihood ratios degenerate. More fundamentally, an instrument change alters the conditional relation between spectrum and property, which violates the covariate-shift assumption. The transport baseline, which maps source-calibration spectra into the secondary-instrument space with a master→secondary PDS, recovered part of the coverage on corn ({{transport_cov_corn}}). It still under-covered in {{transport_under_corn}} of 24 scenarios, because the transported residuals inherit the source error distribution and only approximate the transfer error.

{{table_main}}

## 4.3. Validity and efficiency of the transfer jackknife+ (RQ2)

TJ+N was not flagged as under-covering in any of the {{n_scen_main}} primary scenarios. Its mean coverage was {{tjn_cov_main}} at α = 0.10, and the same held at α = 0.05 and 0.20 ({{tjn_under_all_alpha}} under-covering scenarios over all three levels; Table 4). Coverage exceeded the nominal level most clearly for *m* = 10–15. This is expected from the discrete rank $\lceil (1-\alpha)(m+1)\rceil$: with *m* = 10 the upper bound is the largest of the ten leave-one-out bounds.

**Against the valid split-standards baseline.** Halving the standards made SCP-T-split unbounded in every repetition for *m* ≤ 15 at α = 0.10 ({{split_inf_text}}). Where both methods gave bounded intervals, TJ+N had a lower interval score in {{tjn_vs_split_better}} of {{tjn_vs_split_n}} scenarios (paired Wilcoxon, Holm-adjusted *p* < 0.05), with a median rank-biserial correlation of {{tjn_vs_split_rb}}. Reusing every standard for both transfer and calibration is therefore the main practical gain.

**Against Gaussian leave-one-standard-out intervals.** The simple Gauss-LOO interval was a strong competitor at α = 0.10.
- It was never flagged as under-covering at this level.
- It had the best mean rank of interval score in the Friedman analysis (Fig. S2; χ² = {{friedman_chi2}}, *p* = {{friedman_p}}; mean ranks Gauss-LOO {{rank_gauss}}, TJ+N {{rank_tjn}}, TJ+ {{rank_tj}}).
- It did not differ significantly from TJ+N after Holm correction (*p* = {{p_tjn_gauss}}).
- Per scenario, Gauss-LOO had the lower score more often on corn ({{gauss_better_corn}} of 24 scenarios), while TJ+N was better more often on tablets and mango ({{tjn_better_gauss_other}} of 16).

Its validity, however, depends on approximately Gaussian errors. At α = 0.05 it under-covered in {{gauss_under_005}} of 40 scenarios, and at α = 0.20 in {{gauss_under_020}}, whereas TJ+N and TJ+ never did. The price of distribution-free validity at α = 0.05 is that TJ+N needs *m* ≥ 19 standards. With fewer standards it returns unbounded intervals rather than over-confident ones.

## 4.4. Ablation (RQ3)

Table 5 and Fig. 5 isolate the components.
- **Leave-one-out re-fitting is essential.** With residuals from the transfer fitted on all standards (TJ-insample-N), the intervals under-covered in {{insample_under}} of {{n_scen_main}} scenarios. The effect was largest for SBC on mango (coverage {{insample_cov_mango}}), because a slope and bias fitted to the same standards absorb part of their own residuals.
- **The "+" construction.** Centring the interval on the full-fit prediction (TJ-naive-N) was valid on average here, but it carries no guarantee and gave lower coverage than TJ+N.
- **K-fold CV+.** Five-fold CV+ (TCV+N) needs only five refits but was more conservative, with a higher interval score than TJ+N in {{tcv_worse}} of {{n_scen_main}} scenarios.
- **Difficulty normalisation helped only partly.**
  - TJ+N had a lower interval score than unnormalised TJ+ in {{tjn_vs_tj_better}} scenarios and a higher one in {{tjn_vs_tj_worse}}.
  - Unnormalised intervals under-covered the most difficult third of test samples (coverage in the highest-σ tertile {{tj_cov_sig3}}) and over-covered the easiest third ({{tj_cov_sig1}}).
  - TJ+N moved coverage towards the difficult samples ({{tjn_cov_sig1}} and {{tjn_cov_sig3}}; Fig. 7). On corn it over-corrected, mainly through the Q term.
  - A T²-only difficulty function gave the most balanced conditional coverage on corn. Because this variant was identified after the results were seen, we report it as exploratory and keep the pre-registered TJ+N as the primary method.

{{table_ablation}}

## 4.5. Robustness (RQ4)

{{robust_text}}

{{table_robust}}

## 4.6. Generalisation across pipelines, directions and model classes (RQ5)

{{general_text}}

{{table_general}}

## 4.7. Label-free variant (exploratory)

The label-free LF-conv interval uses only paired, unlabelled standards. It was not reliable: it under-covered in {{lf_under_010}} of {{lf_n}} paired scenarios at α = 0.10. Its independence assumption between source error and transfer discrepancy is evidently too strong. Reference values for at least a random subset of standards remain necessary for valid intervals.

## 4.8. Sensitivity to transfer and model settings

{{sens_text}}

## 4.9. Computational cost (RQ6)

{{timing_text}}

## 4.10. Error analysis

Misses were concentrated in spectra that the source model reconstructed poorly after transfer. For the classical parametric interval, the miss rate rose with the Q-residual quintile of the test spectrum (Fig. 8; {{astm_miss_q1}} in the lowest vs {{astm_miss_q5}} in the highest quintile, corn). TJ+N kept the miss rate closer to nominal across quintiles ({{tjn_miss_q1}}–{{tjn_miss_q5}}). Large Q is therefore a useful warning flag for a transferred calibration, and it is the rationale for including Q in σ(x).

Coverage is a property of the procedure, not of one realised set of standards. Across repetitions, the 5th percentile of per-repetition coverage of TJ+N at *m* = 20 was {{tjn_p05_m20}} (Fig. 10). An unlucky draw of 20 standards can therefore give a markedly lower realised coverage on a given test batch. This variability, intrinsic to marginal guarantees with small calibration sets, shrinks as *m* grows ({{tjn_p05_m50}} at *m* = 50 for tablets and mango).

## 4.11. Practical recommendations

1. Do not reuse source-domain interval formulas after transfer without checking them on target data.
2. Draw at least part of the transfer standards at random from the routine target population, and obtain their reference values.
3. Use TJ+ intervals: re-fit the transfer with each standard left out. This needs *m* ≥ 9 for 90% and *m* ≥ 19 for 95% intervals.
4. Report the leave-one-standard-out RMSE as well. Gaussian intervals built from it are a reasonable approximation at 90% but can under-cover at 95%.
5. Flag predictions with large Q residuals after transfer.
