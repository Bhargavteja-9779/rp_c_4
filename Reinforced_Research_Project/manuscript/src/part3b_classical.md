
**Is a simpler formula enough?** A laboratory that has the left-out errors of its standards will naturally try something simpler first. We therefore compared TJ+N, on identical standards, with five formulas that need no new theory (Table 3; {{r_e11_n}} scenario-pipeline combinations, 200 repetitions each):

- a *t*-interval from the leave-one-out RMSE (Gauss-LOO), and its version scaled by σ(x);
- the ASTM formula with the standard error re-estimated on the standards (ASTM-T);
- for slope/bias correction, the textbook prediction interval of the regression (OLS-PI);
- a bootstrap interval (Boot-T).

At 90%, most of them did reasonably well. Gauss-LOO was too narrow in {{r_gauss_under_010}} combinations, ASTM-T in {{r_astmt_under_010}} and OLS-PI in {{r_ols_under_010}} of the slope/bias cases. They were often also narrower than TJ+N:

- the textbook OLS-PI had the lower interval score in {{r_ols_better}} SBC scenarios where both were valid, TJ+N in {{r_ols_worse}};
- Gauss-LOO-N had the lower score in {{r_gaussn_better}} (see also Supplementary Table S7).

For routine 90% statements with randomly chosen standards, these formulas are a defensible shortcut, and for slope/bias correction the textbook regression interval is hard to beat.

The picture changed at 95%. Gauss-LOO was then too narrow in {{r_gauss_under_005}}, Gauss-LOO-N in {{r_gaussn_under_005}}, ASTM-T in {{r_astmt_under_005}} and OLS-PI in {{r_ols_under_005}} combinations. TJ+N was never too narrow at any level ({{r_e11_tjn_under}}). The bootstrap was the weakest option: it was too narrow in {{r_boot_under_010}} combinations at 90%, and in {{r_boot_under_m10}} with ten standards. A bootstrap of 10–20 standards does not see enough variety to reproduce the error of a new sample.

Why do the formulas fail at 95%? Across scenarios, the coverage shortfall of Gauss-LOO grew with the skewness of the prediction errors (Spearman ρ = {{r_e12_gauss_skew}}) and with how much the leave-one-out RMSE underestimated the actual error (ρ = {{r_e12_gauss_ratio}}). The shortfall of OLS-PI grew with skewness (ρ = {{r_e12_ols_skew}}) and with heavy tails (excess kurtosis, ρ = {{r_e12_ols_kurt}}). This is what one would expect. A Gaussian interval sets its 95% limits from the spread of the errors and assumes symmetric tails. After transfer the errors are often skewed, for example when the transferred predictor is biased for part of the population, so one tail is longer than the formula assumes. TJ+N reads its limits from the left-out errors themselves and makes no such assumption, which is exactly what costs it some width at 90% and saves it at 95%.

{{table_classical}}
