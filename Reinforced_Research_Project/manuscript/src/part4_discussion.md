
## 4.7. A procedure for the laboratory

For someone who transfers an NIR calibration and must report results with an uncertainty range, the results suggest the following procedure:

1. Do not reuse the uncertainty formula of the original calibration after a change of instrument or season. Re-establish it on the new instrument.
2. Collect the reference samples for the transfer from as many different batches as practical, ideally one or two per batch. A distribution-free 90% statement for future batches (TJ+B) needs at least nine batches; the Gaussian and random-effects batch formulas worked from five batches in our data. In our data, twenty samples from twenty consignments served far better than twenty from two, at the same cost in reference analyses.
3. Fit the transfer as usual. Then re-fit it with each standard left out, or each batch left out if several standards share a batch, and build the interval of Eq. (3) from the left-out errors. A *t*-interval or a random-effects interval from the leave-one-batch-out errors are simpler alternatives that worked as well in our data, although without a distribution-free guarantee.
4. For 90% statements with standards from many batches, a Gaussian interval from the leave-one-out RMSE (or, for slope/bias correction, the regression prediction interval) is a reasonable shortcut. For 95% statements these formulas fell one or two points short in some scenarios, and TJ+N needs at least 19 standards.
5. Monitor the instrument after set-up, as described in Section 4.5.

## 4.8. Relation to measurement uncertainty

The intervals studied here are prediction intervals for the reference value of an individual routine sample. In method-validation terms they are β-expectation tolerance intervals [@hubert2004; @mee1984]. Their width therefore contains everything that separates the NIR result from the reference method: reference-method error, spectral noise, model error and the error added by the transfer. They are not a GUM-type uncertainty budget, in which components are estimated separately and propagated. Instead, they provide an empirical check that the transferred method meets a stated coverage. Error-propagation methods for multivariate calibration [@faber1997; @olivieri2006; @allegrini2016] give sample-specific uncertainties, but they rest on the original calibration's error model, which Section 4.1 shows no longer applies after transfer.

The guarantee is an average over possible sets of standards. For a single transfer, the realised coverage on the following samples varies. Across the main scenarios (m = 10–50 random standards; test sets of 10–700 samples), a median of {{r_tc_tjn_median}} of the standard sets gave a realised coverage of at least 0.85 on their test samples. In the least favourable scenario the share was {{r_tc_tjn_min}} (Supplementary Table S13). The Gaussian intervals reached {{r_tc_gauss_median}}. Statements about one particular set of standards (β-content intervals in validation terms) cannot be guaranteed by the jackknife+ in general [@bian2023], unless the fitting procedure is stable in a quantifiable sense [@liang2025]. A laboratory that needs them should use more standards, or a lower α, and re-check coverage on fresh samples.

## 4.9. Limitations

The evidence comes from three public data sets. The batch results, which carry the main practical finding, come from one product (mango), in one season shift and on three handheld-instrument pairs. These eight combinations share a product, a master instrument, consignments and standards, and are closer to two independent settings than to eight. We found no other public NIR transfer data set that records lots. Whether the findings carry over to pharmaceutical production lots or grain deliveries is therefore a conjecture to be tested.

The batches used as standards were drawn at random from the available consignments, which is more favourable than many real set-ups, and the bootstrap intervals are conditional on those consignments. The chronological design is a single configuration per setting. The 15 × 1 design used 15 rather than 20 standards, because the season shift has only 18 consignments.

The noise, wavelength-drift and Kennard–Stone experiments are simulations on real spectra. Only PLS, ridge and a small CNN were tested as models, and PDS, DS and SBC as transfer methods. The bootstrap competitor used in-sample residuals; other bootstrap schemes were not tested. Domain-adaptation methods that use no reference values cannot be covered by this approach, because it needs reference values for the standards. An exploratory label-free variant under-covered in {{lf_under_010}} of {{lf_n}} scenarios (Table 2). The harvest case study was designed after the batch results were known. Finally, every guarantee here is marginal and assumes a stable instrument between set-up and use.

# 5. Conclusions

Moving an NIR calibration to a new instrument or season breaks its old uncertainty statement. In our data, nominal 90% intervals carried over from the original calibration covered as few as {{min_cov_source}} of the reference values. The reference samples used for the transfer are enough to restore a valid statement, without measuring anything extra, if the transfer is re-fitted with each of them left out in turn and the left-out errors are used to set the interval. This takes seconds. With randomly chosen standards, simple Gaussian and regression intervals built from the same left-out errors were nearly as good at 90%, so the main benefit of the jackknife+ is its guarantee and its behaviour at 95%.

How the reference samples are collected turned out to matter more than the formula. Intervals built from samples of a few consignments were accurate for those consignments but too narrow for new ones, whichever sample-level formula was used. Spreading the same number of reference samples over many consignments, or leaving out whole consignments when estimating the errors, gave intervals that held for new consignments. {{r_conclusion_app}}

For laboratories this leads to a rule that costs nothing: collect transfer standards from as many batches as possible, and estimate the interval from errors obtained by leaving them out one at a time, or one batch at a time.

# Declarations {.unnumbered}

**CRediT authorship contribution statement.** [Author 1]: Conceptualization, Methodology, Software, Formal analysis, Writing – original draft. [Author 2]: Supervision, Validation, Writing – review & editing. *(To be completed by the authors.)*

**Declaration of competing interest.** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the authors used an AI assistant (Claude, Anthropic) for literature search support, code development, data analysis and drafting of the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

**Funding.** [To be completed by the authors.]

**Data availability.** All data sets are public: corn and IDRC Shootout 2002 tablets from Eigenvector Research [@eigenvector_data], and mango dry matter from Mendeley Data (record version 1, doi:10.17632/46htwnp833.1 [@mango_data]; record version 6, doi:10.17632/46htwnp833.6 [@mango_data_v6]). All code, configuration files, raw per-repetition results and the scripts that regenerate every table and figure are available at [repository URL / archived DOI to be inserted].

**Acknowledgements.** We thank the providers of the public data sets: Cargill and Eigenvector Research (corn), the International Diffuse Reflectance Conference (Shootout 2002), and N. Anderson, K. Walsh, P. Subedi and J. Walsh (mango).
