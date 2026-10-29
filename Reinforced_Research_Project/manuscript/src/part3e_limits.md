
## 4.5. What the intervals cannot do

Two further situations break the exchangeability on which every method here relies, and they are worth knowing before the intervals are used.

**Selecting standards by design.** Kennard–Stone selection picks standards that span the target population, so they are not a random sample. In our tests it made TJ+N conservative (coverage {{rob_ks_cov}}), because extreme standards produce larger left-out errors than typical samples. This is reassuring for a common practice, but it is an observation, not a guarantee.

**Drift after standardisation.** A shift of the routine spectra by one wavelength channel *after* the transfer had been fitted simulates an instrument that drifts between set-up and use. Under this shift no interval method remained valid (Fig. 6; Supplementary Table S5). On tablets, TJ+N covered only {{rob_shift_tjn_tablets}} of the samples. On corn and mango the $Q$ residual in the difficulty scaling caught much of the damage (TJ+N {{rob_shift_tjn_corn}} and {{rob_shift_tjn_mango}}, against {{rob_shift_gauss_corn}} and {{rob_shift_gauss_mango}} for Gaussian intervals). Even a quarter-channel shift left TJ+N too narrow in {{e4b_tjn_under}} combinations (Supplementary Table S8). Spectral drift must therefore be monitored, for example through the $Q$ residual or periodic check samples, and the transfer repeated when it appears; an interval computed at set-up time cannot absorb it.

Added spectral noise and halving the source data did not cause under-coverage ({{rob_tjn_under_nonshift}} of {{rob_n_nonshift}} robustness scenarios without drift). Neither did changing the PDS window or the number of PLS components ({{sens_tjn_under}} of {{sens_n}}; Supplementary Table S9), although these settings changed the prediction error considerably. Poorer transfer settings simply produced wider intervals.

![**Fig. 6.** Coverage of nominal 90% intervals under Kennard–Stone selection of the standards, added spectral noise, a ±1-channel wavelength shift of the routine spectra after standardisation, and halved source data. Results for a ±0.25-channel shift are in Supplementary Table S8.](figures/fig6_robustness.png){width=16.5cm}

## 4.6. Cost and use in routine work

TJ+N needs *m* extra fits of the transfer step, carried out once, when the instrument is set up. A PDS fit with prediction took {{time_one_corn}} ms for corn and {{time_one_tablets}} ms for tablets on one CPU core. The complete interval computation took {{time_tj_corn}} s, {{time_tj_tablets}} s and {{time_tj_mango}} s for corn, tablets and mango (Supplementary Table S10). In routine use, each new spectrum is passed through the *m* stored transfers, which is negligible for any laboratory computer. The leave-one-batch-out version needs only *K* fits and is cheaper still.
