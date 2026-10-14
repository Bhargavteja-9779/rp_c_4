# 4. Results and discussion

## 4.1. Point accuracy after transfer

Calibration transfer was necessary, but it was not equally beneficial everywhere (Table 2).
- **Corn:** applying the master models directly to mp5/mp6 spectra gave RMSEP values {{corn_none_vs_pds}} times larger than after PDS with *m* = 20 standards.
- **Tablets:** PDS reduced the assay RMSEP from {{tab_assay_rmsep_m10}} mg (*m* = 10) to {{tab_assay_rmsep_m50}} mg (*m* = 50). The weight and hardness predictions were insensitive to the transfer.
- **Mango:** SBC did not improve on the uncorrected source model (RMSEP {{mango_sbc_rmsep}} vs {{mango_none_rmsep}} % DM), consistent with reports that models built over several seasons are already fairly robust [@anderson2020].

The transfer settings (PDS window 5, SBC slope and bias, LV numbers) were fixed in advance and were not tuned on target data. They are therefore not the most accurate possible: on corn, SBC gave lower RMSEP than the pre-registered PDS for all four properties, and a 3-channel PDS window was more accurate than the 5-channel one (§4.8). This does not affect the comparison of interval methods. All interval methods share the same point predictor within a pipeline, so the comparisons isolate the interval construction, and interval validity is reported for every pipeline (§4.3).

{{table_rmsep}}

## 4.2. Conventional intervals after transfer (RQ1)

Source-calibrated intervals under-covered when the transfer added substantial error that the source calibration had not seen (Fig. 3; Table 3; compare Table 2).
- **Corn:** the mean coverage of nominal 90% intervals was {{src_cov_range_corn}} for ASTM-PI, SCP-S and WCP-S, which were flagged as under-covering in {{src_under_corn}} scenario × method cells.
- **Mango:** coverage was {{src_cov_range_mango}} ({{src_under_mango}} cells under-covering).
- **Tablets:** the picture was mixed ({{src_cov_range_tablets}}; {{src_under_tablets}} cells under-covering). Severe under-coverage occurred for the assay with *m* = 10 (all three methods, {{tab_assay_m10_src}}), where PDS fitted on ten standards inflated the error. For weight, SCP-S and WCP-S under-covered slightly but systematically at every *m* ({{tab_weight_scps}}), while hardness intervals were valid.

The failure is not an artefact of the in-sample calibration error used by ASTM-PI: SCP-S, which uses cross-validated (out-of-fold) source residuals, under-covered almost as severely. Weighting the source residuals for covariate shift (WCP-S) did not repair coverage either, and it produced unbounded intervals in {{wcp_inf_pct}} of corn repetitions. When the domains are almost perfectly separable, the estimated likelihood ratios degenerate. More fundamentally, an instrument change alters the conditional relation between spectrum and property, which violates the covariate-shift assumption. The transport baseline, which maps source-calibration spectra into the secondary-instrument space with a master→secondary PDS, recovered part of the coverage on corn ({{transport_cov_corn}}). It still under-covered in {{transport_under_corn}} of 24 scenarios, because the transported residuals inherit the source error distribution and only approximate the transfer error.

{{table_main}}

![**Fig. 3.** Mean empirical coverage of nominal 90% intervals versus the number of transfer standards *m* (primary pipelines; 500 repetitions for corn and tablets, 300 for mango). Markers show the mean over scenarios (properties and target instruments); vertical lines show the range over scenarios. Hollow markers: the method returned unbounded intervals in more than half of the repetitions (coverage trivially 1). Horizontal line: nominal level.](figures/fig3_coverage_vs_m.png){width=16.5cm}


## 4.3. Validity and efficiency of the transfer jackknife+ (RQ2)

TJ+N was not flagged as under-covering in any of the {{n_scen_main}} primary scenarios. Given the precision of the coverage estimates (median half-width of the 95% CI: {{ci_hw_text}}), this means that no scenario was significantly below nominal at that resolution. Its mean coverage was {{tjn_cov_main}} at α = 0.10, and the same held at α = 0.05 and 0.20 ({{tjn_under_all_alpha}} under-covering scenarios over all three levels; Table 4). Coverage exceeded the nominal level most clearly for *m* = 10–15. This is expected from the discrete rank $\lceil (1-\alpha)(m+1)\rceil$: with *m* = 10 the upper bound is the largest of the ten leave-one-out bounds. In practice, this conservativeness means somewhat wider intervals than necessary when few standards are available; it decreases as *m* grows (Fig. 3).

**Against the valid split-standards baseline.** Halving the standards made SCP-T-split unbounded in every repetition for *m* ≤ 15 at α = 0.10 ({{split_inf_text}}). Where both methods gave bounded intervals, TJ+N had a lower interval score in {{tjn_vs_split_better}} of {{tjn_vs_split_n}} scenarios (paired Wilcoxon, Holm-adjusted *p* < 0.05), with a median rank-biserial correlation of {{tjn_vs_split_rb}}. Reusing every standard for both transfer and calibration is therefore the main practical gain.

Interval widths relative to the RMSEP of the deployed predictor are shown in Fig. 4.

![**Fig. 4.** Median interval width relative to the RMSEP of the deployed predictor for the methods that were not under-covering (unbounded settings omitted).](figures/fig4_width_vs_m.png){width=16.5cm}

**Against Gaussian leave-one-standard-out intervals.** The simple Gauss-LOO interval was a strong competitor at α = 0.10.
- It was never flagged as under-covering at this level.
- It had the best mean rank of interval score across scenarios (Fig. S2; mean ranks Gauss-LOO {{rank_gauss}}, TJ+N {{rank_tjn}}, TJ+ {{rank_tj}}; Friedman χ² = {{friedman_chi2}}, nominal *p* = {{friedman_p}}, which overstates the evidence because scenarios are dependent).
- Across scenarios, it did not differ significantly from TJ+N after Holm correction (*p* = {{p_tjn_gauss}}).
- Per scenario (Holm-adjusted *p* < 0.05), Gauss-LOO had the lower interval score in {{gauss_better_corn}} of 24 corn scenarios. On tablets and mango, TJ+N was better in {{tjn_better_gauss_other}} and Gauss-LOO in {{gauss_better_other}} of 16 scenarios.

Its validity, however, depends on approximately Gaussian errors. At α = 0.05 it under-covered in {{gauss_under_005}} of 40 scenarios, and at α = 0.20 in {{gauss_under_020}}, whereas TJ+N and TJ+ never did. The price of distribution-free validity at α = 0.05 is that TJ+N needs *m* ≥ 19 standards. With fewer standards it returns unbounded intervals rather than over-confident ones.

**Normalised Gaussian competitor (E9).** One might expect a heteroscedastic Gaussian interval using the same difficulty function to combine the efficiency of Gauss-LOO with the adaptivity of TJ+N: μ(x) ± t₁₋α/₂,ₘ₋₁ · RMS(Rᵢ) · σ(x), with Rᵢ from Eq. (3) (Gauss-LOO-N). We tested this in an additional experiment specified during review (200 repetitions; all primary pipelines and the instrument shift of E8; three α levels; Table S8).
- Under-covering scenarios over all α levels: TJ+N {{e9_tjn_under}}, Gauss-LOO {{e9_gauss_under}}, Gauss-LOO-N {{e9_gaussn_under}}.
- At α = 0.05: {{e9_tjn_under_005}}, {{e9_gauss_under_005}} and {{e9_gaussn_under_005}}, respectively.
- At α = 0.10, Gauss-LOO-N had a lower median interval score than TJ+N in {{e9_gaussn_better}} of {{e9_n_scen}} scenarios (median score ratio {{e9_gaussn_rel_is}}).

The normalised Gaussian interval was therefore slightly more efficient, by about 3% in interval score, but it under-covered in several scenarios, mostly at 95%. TJ+N trades this small loss of efficiency for validity without distributional assumptions. Where a few percent of interval width matter more than a coverage guarantee, Gauss-LOO-N is a defensible pragmatic choice, provided its coverage is checked.
 Over all four transfer pipelines (PDS, DS, SBC and no transfer) and the three data sets, TJ+N under-covered in {{allpipe_tjn_under}} pipeline × scenario combinations at α = 0.10. The corresponding numbers were {{allpipe_gauss_under}} for Gauss-LOO, {{allpipe_astm_under}} for ASTM-PI and {{allpipe_scps_under}} for SCP-S (Table S2).

{{table_alpha}}

## 4.4. Ablation (RQ3)

Table 5 and Fig. 5 isolate the components.
- **Leave-one-out re-fitting is essential.** With residuals from the transfer fitted on all standards (TJ-insample-N), the intervals under-covered in {{insample_under}} of {{n_scen_main}} scenarios. The effect was largest for SBC on mango (coverage {{insample_cov_mango}}), because a slope and bias fitted to the same standards absorb part of their own residuals.
- **K-fold CV+.** Five-fold CV+ (TCV+N) needs only five refits but was more conservative, with a higher interval score than TJ+N in {{tcv_worse}} of {{n_scen_main}} scenarios.
- **The "+" construction.** Centring the interval on the full-fit prediction (TJ-naive-N) gave equal or slightly lower coverage than TJ+N. It is a reasonable practical alternative, but it carries no finite-sample guarantee.
- **Over all pipelines and α levels (E1 and E8 together):**
  - TJ-naive-N under-covered in {{allcells_naive_under}} scenario cells, against {{allcells_tjn_under}} for TJ+N and {{allcells_tcv_under}} for TCV+N.
  - Residuals without leave-one-out re-fitting (TJ-insample-N) under-covered in {{allcells_insample_under}}.
  - Gauss-LOO under-covered in {{allcells_gauss_under}}.
- **Difficulty normalisation.** Normalisation improved efficiency in most scenarios.
  - TJ+N had a significantly lower interval score than unnormalised TJ+ in {{tjn_vs_tj_better}} of {{n_scen_main}} scenarios, and a higher one in {{tjn_vs_tj_worse}}.
  - It also rebalanced conditional coverage. Unnormalised intervals under-covered the most difficult third of test samples (coverage in the highest-σ tertile {{tj_cov_sig3}}) and over-covered the easiest third ({{tj_cov_sig1}}). With TJ+N these became {{tjn_cov_sig3}} and {{tjn_cov_sig1}} (Fig. 6).
  - On corn, the Q term over-corrected slightly: the highest-σ tertile was over-covered. A T²-only difficulty function was more balanced there. Because this variant was identified after the results were seen, we report it as exploratory and keep the pre-registered TJ+N as the primary method.
  - The Q term was most valuable when the test spectra drifted after standardisation (§4.5).

{{table_ablation}}

![**Fig. 5.** Ablation of TJ+N. Left: mean coverage. Right: median interval score relative to TJ+N (finite intervals only).](figures/fig5_ablation.png){width=16.5cm}

![**Fig. 6.** Conditional coverage within tertiles of the difficulty σ(x) of the test spectra (primary pipelines, α = 0.10).](figures/fig7_conditional_coverage.png){width=16.5cm}


## 4.5. Robustness (RQ4)

Apart from post-standardisation drift, TJ+N was not flagged as under-covering in any of the {{rob_n_nonshift}} robustness scenarios (Fig. 7; Supplementary Table S9). These were Kennard–Stone selection of the standards, added noise at SNR 1000–100, and halving the source data.

**Kennard–Stone standards.** Selecting the standards by Kennard–Stone, which is outside the scope of Proposition 1, made TJ+N conservative (coverage {{rob_ks_cov}}). The selected standards span the extremes of the target population, so their leave-one-out residuals are, if anything, larger than those of typical samples. This empirical result is reassuring, but it is not a guarantee. Other non-random selection schemes, for example standards concentrated in a narrow concentration range, could bias coverage in either direction.

**Post-standardisation wavelength drift.** The decisive failure mode was a one-channel wavelength shift of the test spectra after the transfer had been fitted. This simulates instrument drift between standardisation and routine use, and it breaks exchangeability between standards and test samples. No method remained valid.
- Tablets: TJ+N coverage was {{rob_shift_tjn_tablets}}; Gauss-LOO {{rob_shift_gauss_tablets}}.
- Corn: TJ+N {{rob_shift_tjn_corn}}, against {{rob_shift_tj_corn}} for unnormalised TJ+ and {{rob_shift_gauss_corn}} for Gauss-LOO.
- Mango: TJ+N {{rob_shift_tjn_mango}}, against {{rob_shift_tj_mango}} for TJ+ and {{rob_shift_gauss_mango}} for Gauss-LOO.

On corn and mango, the Q residual of the shifted spectra inflated σ(x) and recovered a large part of the coverage. On tablets, where the assay information is concentrated in a few sharp bands, it did not. Drift after standardisation must therefore be detected (for example by monitoring Q) and corrected by re-standardisation. No interval method compensates for it reliably.


![**Fig. 7.** Robustness of interval coverage (α = 0.10): Kennard–Stone selection of standards, spectral noise added to all target spectra, a ±1-channel wavelength shift of the test spectra after standardisation, and halved source training data.](figures/fig6_robustness.png){width=16.5cm}



## 4.6. Generalisation across pipelines, directions, model classes and instruments (RQ5)

The conclusions did not depend on the primary pipeline, the transfer direction or the model class (Table 6).
- **Transfer pipelines.** With DS, SBC or no transfer instead of PDS, TJ+N and TJ+ were never flagged as under-covering (§4.3).
- **Reverse direction.** Transferring from mp5 to m5 gave the same picture: no under-coverage for TJ+N, and under-coverage of the source-calibrated intervals.
- **Ridge regression.** With ridge source models, TJ+N was valid on all three data sets.
- **1D-CNN on mango.** The CNN ({{cnn_params}} parameters, early stopping after {{cnn_epochs}} epochs, {{cnn_train_s}} s on a CPU) reached RMSEP {{cnn_rmsep}} % DM after SBC. On top of it:
  - TJ+N gave coverage {{cnn_tjn_cov}} with the lowest interval score ({{cnn_tjn_is}}).
  - Gauss-LOO under-covered in {{cnn_gauss_under}} scenarios (coverage {{cnn_gauss_cov}}; score {{cnn_gauss_is}}).
  - MC-dropout intervals [@gal2016], a common deep-learning uncertainty estimate for spectra [@maxime2025], under-covered in {{cnn_mc_under}} scenarios (coverage {{cnn_mc_cov}}), presumably because dropout variance captures model uncertainty but not the systematic error introduced by the season shift.

Over all generalisation settings, TJ+N under-covered in {{gen_tjn_under}} of {{gen_tjn_n}} scenarios.

**Independent instrument shift (mango, E8).** Prompted by the review process, we added a test that was not part of the pre-registered design: transfer between handheld spectrometers on intact fruit, using the data providers' extended data set with paired spectra of the same fruit on several instruments [@mango_data_v6]. The design was fixed before any result was computed:
- source instrument 15006;
- the three target instruments with most shared fruit;
- PDS and SBC pipelines;
- *m* = 10–50 standards, 200 repetitions.

The results reproduced the main findings (Table 7).
- ASTM-PI and SCP-S under-covered in every scenario: coverage {{e8_fin_cov_pds}} after PDS ({{e8_fin_under_pds}} scenarios) and {{e8_fin_cov_sbc}} after SBC ({{e8_fin_under_sbc}}). WCP-S under-covered after PDS ({{e8_wcp_cov_pds}}). After SBC it returned unbounded intervals in {{e8_wcp_inf_sbc}} of repetitions: valid, but uninformative.
- TJ+N was valid: mean coverage {{e8_tjn_cov_pds}} (PDS) and {{e8_tjn_cov_sbc}} (SBC). It was never flagged at any α ({{e8_tjn_under_allalpha}} under-covering scenarios), whereas Gauss-LOO was flagged in {{e8_gauss_under_allalpha}}.
- PDS proved a poor transfer for these instruments (RMSEP {{e8_rmsep_pds}} % DM, against {{e8_rmsep_sbc}} % with SBC). TJ+N made this visible through wide intervals (median width {{e8_width_pds}} vs {{e8_width_sbc}} % DM), whereas the source-calibrated intervals remained narrow and missed most samples. Valid intervals are thus also a diagnostic of transfer quality.



{{table_general}}

{{table_e8}}

## 4.7. Label-free variant (exploratory)

The label-free LF-conv interval uses only paired, unlabelled standards. It was not reliable: it under-covered in {{lf_under_010}} of {{lf_n}} paired scenarios at α = 0.10. Its independence assumption between source error and transfer discrepancy is evidently too strong. Reference values for at least a random subset of standards remain necessary for valid intervals.

## 4.8. Sensitivity to transfer and model settings

Changing the PDS window (3, 7 or 11 channels instead of the pre-registered 5) or the number of latent variables (±2) changed point accuracy considerably. For example, the mean corn RMSEP with *m* = 15 was {{sens_corn_rmsep_w5}} with the pre-registered 5-channel window and {{sens_corn_rmsep_hw}} with the other windows. The pre-registered window was thus not the most accurate choice for corn; it was nevertheless kept, since it was fixed before any target data were analysed. Interval validity was unaffected: TJ+N under-covered in {{sens_tjn_under}} of {{sens_n}} sensitivity scenarios (coverage {{sens_tjn_cov}}; Table S3). The source-calibrated intervals under-covered in {{sens_src_under}} cases. Their validity also depended on the setting. For example, with an 11-channel PDS window the tablet-assay coverage of ASTM-PI and SCP-S fell to {{sens_tab_hw5_astm}} and {{sens_tab_hw5_scps}}. Because TJ+ calibrates on the deployed pipeline itself, poorer transfer settings are reflected in wider, but still valid, intervals.

## 4.9. Error analysis

Misses of the conventional intervals were associated with spectra that the source model reconstructed poorly after transfer (Fig. 8). On corn, the miss rate of ASTM-PI was {{astm_miss_q1}} in the lowest and {{astm_miss_q5}} in the highest Q-residual quintile of the test spectra. Gauss-LOO, which uses one width for all samples, was valid on average but missed more often in the highest Q quintile: {{miss_q5_gauss_corn}} (corn), {{miss_q5_gauss_tablets}} (tablets) and {{miss_q5_gauss_mango}} (mango), against {{miss_q5_tjn_corn}}, {{miss_q5_tjn_tablets}} and {{miss_q5_tjn_mango}} for TJ+N, for a nominal 0.10. The difficulty normalisation thus moves coverage to where it is needed. A large Q residual after transfer is in any case a useful warning flag for an individual prediction.

Coverage is a property of the procedure, not of one realised set of standards. Across repetitions, the 5th percentile of per-repetition coverage of TJ+N at *m* = 20 was {{tjn_p05_m20}} (Fig. 9). An unlucky draw of 20 standards can therefore give a markedly lower realised coverage on a given test batch. This variability, intrinsic to marginal guarantees with small calibration sets, shrinks as *m* grows ({{tjn_p05_m50}} at *m* = 50 for tablets and mango).

![**Fig. 8.** Miss rate (1 − coverage) by Q-residual quintile of the test spectra (first 100 repetitions; corn m = 15, tablets assay and mango m = 20). Horizontal line: nominal miss rate 0.10.](figures/fig8_error_analysis.png){width=16.5cm}

![**Fig. 9.** Distribution over repetitions of the realised test-set coverage for one scenario per data set (violins; dots = mean). The guarantee concerns the mean; individual draws of standards vary.](figures/fig10_coverage_distribution.png){width=16.5cm}

## 4.10. Computational cost (RQ6)

TJ+N requires *m* leave-one-out refits of the transfer step (plus five refits for the optional CV+ comparison included in our timing). On a single CPU core, one transfer fit with prediction took {{time_one_corn}} ms (corn, *m* = 20), {{time_one_tablets}} ms (tablets, *m* = 50, 410 test spectra) and {{time_one_mango}} ms (mango SBC). The complete TJ+N interval computation took {{time_tj_corn}} s, {{time_tj_tablets}} s and {{time_tj_mango}} s, respectively, with peak memory below {{time_mem_max}} MB (Fig. S3). The source model is never re-fitted. Measured over *m* = 10–50, the cost of TJ+N grew approximately linearly with the number of standards ({{scaling_text}}; Supplementary Table S7). These timings include the five CV+ refits and are thus upper bounds.

**Deployment.**
- The *m* leave-one-out transfers are fitted once, when the instrument is standardised.
- For each routine spectrum, TJ+N then requires *m* applications of a stored transfer map and *m* predictions of the source model. For PDS, each map is a *p* × 5 coefficient array (about 28 kB for 700 channels); for SBC, it is two numbers.
- Energy use is negligible at these scales.
- For computationally expensive adaptation methods, for example domain-adaptive PLS with hyperparameter search or neural domain adaptation, the five-fold CV+ variant reduces the cost to five refits. It remained valid in all scenarios, at the price of somewhat wider intervals (§4.4).

The added cost is therefore negligible for routine laboratory use.



## 4.11. Relation to analytical measurement uncertainty

A TJ+ interval is a *prediction* interval for the reference value of an individual routine sample. Its target is the value that the reference method would return. Its width therefore reflects, jointly, the error of the reference method, spectral noise, model error and the error introduced by the transfer. All of these enter the leave-one-standard-out residuals.

It is not a GUM-type uncertainty budget, in which components are estimated separately and propagated. Nor is it conditional on the particular sample: the 1−2α (empirically ≈1−α) statement concerns samples drawn from the routine population. Error-propagation approaches to multivariate prediction uncertainty [@faber1997; @olivieri2006; @allegrini2016] give sample-specific uncertainties, but they rest on a calibration error model that, as shown in §4.2, no longer holds after transfer.

TJ+N is complementary. It provides an empirically calibrated coverage statement for the transferred method, it can be used to check whether a parametric uncertainty statement still holds after transfer, and, through σ(x), it retains sample-specific widths. Where the reference-method repeatability is known, comparing it with the TJ+N interval width shows how much of the uncertainty after transfer stems from the NIR method itself.

## 4.12. Practical recommendations

1. Do not reuse source-domain interval formulas after transfer without checking them on target data.
2. Draw at least part of the transfer standards at random from the routine target population, and obtain their reference values.
3. Use TJ+ intervals: re-fit the transfer with each standard left out. This needs *m* ≥ 9 for 90% and *m* ≥ 19 for 95% intervals.
4. Report the leave-one-standard-out RMSE as well. Gaussian intervals built from it are a reasonable approximation at 90% but can under-cover at 95%.
5. Flag predictions with large Q residuals after transfer.
