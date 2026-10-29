
## 4.7. A recipe for the laboratory

The results can be condensed into a short procedure for anyone who transfers an NIR calibration and must report results with an uncertainty range:

1. Do not reuse the uncertainty formula of the original calibration after a change of instrument or season.
2. Collect the reference samples for the transfer from as many different batches as practical, ideally one or two per batch, and at least nine batches for 90% statements about future batches. Twenty samples from twenty lots are worth far more than twenty samples from two lots, and cost the same in reference analyses.
3. Fit the transfer as usual. Then re-fit it with each standard left out (or, if several standards share a batch, each batch left out) and build the interval of Eq. (3) from the left-out errors. The code that accompanies this paper does this in a few lines.
4. Report the leave-one-out RMSE as well. Gaussian intervals built from it are acceptable at 90% when the standards are spread over many batches, but should not be used for 95% statements.
5. Watch for spectral drift after set-up (rising $Q$ residuals) and check a few fresh reference samples now and then. No interval computed at set-up time protects against drift.

## 4.8. Relation to measurement uncertainty

The intervals studied here are prediction intervals for the reference value of an individual routine sample. In method-validation terms they are β-expectation tolerance intervals [@hubert2004; @mee1984]. Their width therefore contains everything that separates the NIR result from the reference method: reference-method error, spectral noise, model error and the error added by the transfer. They are not a GUM-type uncertainty budget, in which components are estimated separately and propagated. They are a direct, empirical check that the transferred method meets a stated coverage. Error-propagation methods for multivariate calibration [@faber1997; @olivieri2006; @allegrini2016] give sample-specific uncertainties, but they rest on the original calibration's error model, which Section 4.1 shows no longer applies after transfer.

The guarantee is an average over possible sets of standards. For a single transfer, the realised coverage on the next few hundred samples varies. Across the main scenarios (m = 10–50 random standards), a median of {{r_tc_tjn_median}} of the standard sets gave a realised coverage of at least 0.85 on the test samples; in the least favourable scenario the share was {{r_tc_tjn_min}} (Supplementary Table S13). The Gaussian intervals did no better ({{r_tc_gauss_median}}). Such statements about one particular set of standards (β-content intervals in validation terms) cannot be guaranteed by the jackknife+ in general [@bian2023], unless the fitting procedure is stable in a quantifiable sense [@liang2025]. A laboratory that needs them should use more standards, or a lower α, and re-check coverage on fresh samples.

## 4.9. Limitations

The evidence comes from three public data sets. The data on batches, which carry the central practical finding, come from one product (mango), measured in one season shift and on three handheld-instrument pairs. We found no other public NIR transfer data set that records lots, so the batch results should be confirmed on other products, such as pharmaceutical production lots or grain deliveries. The batch structure itself is real, but the batches used for standards were drawn at random from those available, which is more favourable than many real set-ups. The chronological design shows what happens otherwise.

The noise, wavelength-drift and Kennard–Stone experiments are simulations on real spectra. Only PLS, ridge and a small CNN were tested as models, and PDS, DS and SBC as transfer methods. Domain-adaptation methods that use no reference values cannot be covered by this approach, because it needs reference values for the standards. An exploratory label-free variant under-covered in {{lf_under_010}} of {{lf_n}} scenarios (Table 2).

Finally, every guarantee here is marginal and assumes a stable instrument between set-up and use.

# 5. Conclusions

Moving an NIR calibration to a new instrument or season breaks its old uncertainty statement. In our data, nominal 90% intervals carried over from the original calibration covered as few as {{min_cov_source}} of the reference values. The reference samples used for the transfer are enough to restore a valid statement, without measuring anything extra, if the transfer is re-fitted with each of them left out in turn and the left-out errors are used to set the interval. This takes seconds.

What the reference samples must represent is the more important lesson. Intervals built from samples of a few batches were accurate for those batches but too narrow for the next ones, and none of the common alternatives avoided this without becoming too wide to be useful. Spreading the same number of reference samples over many batches, or leaving out whole batches when re-fitting, gave intervals that held for new batches. {{r_conclusion_app}}

For laboratories this turns into a rule that costs nothing: collect transfer standards from as many batches as possible, and report intervals obtained by leaving them out one (or one batch) at a time.

# Declarations {.unnumbered}

**CRediT authorship contribution statement.** [Author 1]: Conceptualization, Methodology, Software, Formal analysis, Writing – original draft. [Author 2]: Supervision, Validation, Writing – review & editing. *(To be completed by the authors.)*

**Declaration of competing interest.** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the authors used an AI assistant (Claude, Anthropic) for literature search support, code development, data analysis and drafting of the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

**Funding.** [To be completed by the authors.]

**Data availability.** All data sets are public: corn and IDRC Shootout 2002 tablets from Eigenvector Research [@eigenvector_data], and mango dry matter from Mendeley Data (record version 1, doi:10.17632/46htwnp833.1 [@mango_data]; record version 6, doi:10.17632/46htwnp833.6 [@mango_data_v6]). All code, configuration files, raw per-repetition results and the scripts that regenerate every table and figure are available at [repository URL / archived DOI to be inserted].

**Acknowledgements.** We thank the providers of the public data sets: Cargill and Eigenvector Research (corn), the International Diffuse Reflectance Conference (Shootout 2002), and N. Anderson, K. Walsh, P. Subedi and J. Walsh (mango).
