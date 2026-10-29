
# 4. Results and discussion

## 4.1. The old uncertainty statement does not survive the move

Transfer was clearly needed. Applied directly to the mp5 and mp6 spectra, the corn master models had prediction errors {{corn_none_vs_pds}} times larger than after PDS with 20 standards (Supplementary Table S1). The uncertainty statements of the original calibrations fared worse than their predictions. On corn, nominal 90% intervals from the ASTM formula, from source split conformal prediction and from the covariate-shift-weighted version contained far fewer reference values than intended (coverage {{src_cov_range_corn}}). All {{src_under_corn}} scenario-method combinations were too narrow. On mango the coverage was {{src_cov_range_mango}} ({{src_under_mango}} too narrow). On tablets the picture was mixed ({{src_cov_range_tablets}}; {{src_under_tablets}} too narrow): the assay suffered with ten standards, while hardness, which hardly changed between instruments, was unaffected (Table 2, Fig. 3).

The reason is simple. The original calibration error does not include the error added by the transfer itself, which is estimated from only a few standards. Out-of-fold source residuals did not help (SCP-S under-covered almost as badly as ASTM-PI). Neither did reweighting them for the change in spectral distribution: WCP-S returned unbounded intervals in {{wcp_inf_pct}} of corn repetitions and was too narrow elsewhere, because an instrument change alters the relation between spectrum and property, not only the spectra. Mapping source samples into the new instrument's space (Transport) recovered part of the coverage ({{transport_cov_corn}}) but remained too narrow in {{transport_under_corn}} of {{n_scen_corn}} corn scenarios. The independent instrument shift on mango told the same story: after PDS, the source-based intervals covered only {{e8_src_cov_pds}} of the fruit (Supplementary Table S6).

The practical message is plain. An uncertainty range validated on the original instrument says little about the transferred method and has to be re-established on the new one.

{{table_main}}

![**Fig. 3.** Coverage of nominal 90% intervals versus the number of standards *m* when the standards are drawn at random (main pipelines; 500 repetitions for corn and tablets, 300 for mango). Markers: mean over scenarios; lines: range over scenarios; hollow markers: unbounded in more than half of the repetitions. Dashed line: nominal level.](figures/fig3_coverage_vs_m.png){width=16.5cm}

## 4.2. With randomly chosen standards, the standards are enough

When the standards were a random sample of the target samples, TJ+N held its level everywhere we looked. It was never too narrow in the {{n_scen_main}} main scenarios, at any of the three confidence levels (90% shown in Table 2, 95% and 80% in Supplementary Table S2). Its mean coverage was {{tjn_cov_mean}} at 90%. The same held across all four transfer pipelines ({{allpipe_tjn_under}} combinations too narrow), for ridge and 1D-CNN models ({{gen_tjn_under}} of {{gen_tjn_n}}; Supplementary Table S4), for the reverse transfer direction, and for the independent transfer between handheld fruit spectrometers ({{e8_tjn_under_allalpha}} scenario-level combinations too narrow).

This is what Proposition 1 predicts, and it should be read as a confirmation that the transfer step is the right thing to re-fit rather than as a discovery. It is still worth seeing how close the coverage stays to nominal. The lower end of the 95% confidence interval of coverage was within 0.02 of the nominal level in {{r_ni_tjn}} scenario-level cases, so the intervals were not only "not detectably too narrow" but demonstrably close to target. Leaving the standard out matters. Computing the errors from a transfer that had seen all standards (the obvious shortcut) produced intervals that were too narrow in {{allcells_insample_under}} cases, because a slope and bias fitted on the same standards absorb part of their own errors (Supplementary Table S3).

The alternative that is equally valid, splitting the standards in half, wastes them. With 15 or fewer standards, the half left for calibration was too small for a bounded 90% interval in any repetition ({{split_inf_text}}). Where both methods gave bounded intervals, TJ+N was narrower in {{tjn_vs_split_better}} of {{tjn_vs_split_n}} scenarios.
