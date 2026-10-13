# 5. Limitations

1. **Reference values for the standards.**
   - TJ+ needs the reference values of the transfer standards.
   - SBC needs them anyway, and PDS/DS standards are usually calibration samples with known values.
   - When reference values are unavailable, only the exploratory label-free variant applies, and it carries no guarantee (§4.5).
2. **How the standards are selected.**
   - The guarantee assumes the standards are a random sample of the target population, exchangeable with future samples.
   - Kennard–Stone and other representative designs violate this assumption. Their empirical effect is reported in §4.4, but they are not covered by Proposition 1.
   - In practice, a random subset of standards can be reserved for interval calibration.
3. **Marginal, not conditional, guarantee.**
   - Coverage holds on average over the draw of standards and future samples.
   - With small *m*, the realised coverage for one particular set of standards varies (Fig. 10). Conditional coverage across difficulty strata is only approximately balanced (Fig. 7).
   - The worst-case bound is 1−2α, although the observed coverage was close to or above 1−α.
4. **Scope of the evidence.**
   - Three public NIR data sets were used, one of them small (corn, *n* = 80), with two instrument pairs and one season shift.
   - The noise, wavelength-shift and source-size perturbations are simulated.
   - Other techniques (Raman, MIR), non-linear or deep domain-adaptation transfers, and process data streams with drift were not tested.
5. **A simple competitor.** Gaussian intervals built from leave-one-standard-out residuals (Gauss-LOO) were often as efficient as TJ+N, and in some scenarios more so (§4.2). The advantage of TJ+N is its distribution-free guarantee and its behaviour under heavy-tailed or heteroscedastic errors, not uniformly narrower intervals.
6. **Difficulty normalisation.** The pre-registered σ(x) built from both T² and Q did not uniformly improve efficiency over unnormalised TJ+. A T²-only variant performed better in several scenarios, but this was observed *post hoc* and needs confirmation on independent data.

# 6. Conclusions

Prediction intervals for calibrations moved to a new instrument or season should not be calibrated on source-domain data. In our benchmark, the classical parametric interval, source split conformal prediction and covariate-shift-weighted conformal prediction all under-covered after transfer, sometimes severely.

The transfer jackknife+ re-fits only the transfer step in a leave-one-standard-out loop. It thereby reuses the transfer standards that calibration transfer already requires, and gives distribution-free intervals with a finite-sample guarantee. Its intervals were valid across instruments, properties, shift types and model classes whenever its assumptions held. They were bounded with far fewer standards than the valid alternative that splits the standards. The extra cost is *m* refits of the transfer step, which took seconds or less in all cases studied.

We recommend:
1. drawing at least a random subset of transfer standards from the target population;
2. using *m* ≥ 9 (α = 0.10) or *m* ≥ 19 (α = 0.05);
3. reporting TJ+-type intervals, or at least Gaussian leave-one-standard-out intervals, alongside RMSEP whenever a calibration is transferred.

# Declarations {.unnumbered}

**CRediT authorship contribution statement.** [Author 1]: Conceptualization, Methodology, Software, Formal analysis, Writing – original draft. [Author 2]: Supervision, Validation, Writing – review & editing. *(To be completed by the authors.)*

**Declaration of competing interest.** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the authors used an AI assistant (Claude, Anthropic) for literature search support, code development, data analysis and drafting of the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

**Funding.** [To be completed by the authors; e.g. "This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."]

**Data availability.** All data sets are public: corn and IDRC Shootout 2002 tablets from Eigenvector Research [@eigenvector_data], and mango DMC from Mendeley Data (doi:10.17632/46htwnp833, CC BY 4.0) [@mango_data]. All code, configuration, raw per-repetition results and the scripts regenerating every table and figure are available at [repository URL / archived DOI to be inserted on acceptance].

**Acknowledgements.** We thank the providers of the public data sets: Cargill and Eigenvector Research (corn), the International Diffuse Reflectance Conference (Shootout 2002), and N. Anderson, K. Walsh, P. Subedi and J. Walsh (mango).
