# 5. Limitations

1. **Reference values for the standards.**
   - TJ+ needs the reference values of the transfer standards.
   - SBC needs them anyway, and PDS/DS standards are usually calibration samples with known values.
   - When reference values are unavailable, only the exploratory label-free variant applies, and it carries no guarantee and under-covered in our tests (§4.7).
2. **How the standards are selected.**
   - The guarantee assumes the standards are a random sample of the target population, exchangeable with future samples.
   - Kennard–Stone and other representative designs violate this assumption. Kennard–Stone selection made TJ+N conservative in our tests (§4.5), but it is not covered by Proposition 1.
   - In practice, a random subset of standards can be reserved for interval calibration.
3. **Marginal, not conditional, guarantee.**
   - Coverage holds on average over the draw of standards and future samples.
   - With small *m*, the realised coverage for one particular set of standards varies (Fig. 9). Conditional coverage across difficulty strata is only approximately balanced (Fig. 6).
   - The worst-case bound is 1−2α, although the observed coverage was close to or above 1−α.
4. **Scope of the evidence.**
   - Three public NIR data sets were used, one of them small (corn, *n* = 80). They cover two instrument pairs for corn, one for tablets, one season shift and three handheld-instrument pairs for mango.
   - Coverage refers to the samples in these data sets. Test samples recur across repetitions, so the results characterise the procedure on these populations, not on all possible samples.
   - The noise, wavelength-shift and source-size perturbations are simulated.
   - Other techniques (Raman, MIR), non-linear or deep domain-adaptation transfers, and process data streams with drift were not tested.
5. **A simple competitor.** Gaussian intervals built from leave-one-standard-out residuals (Gauss-LOO) were often as efficient as TJ+N, and in some scenarios more so (§4.3). The advantage of TJ+N is its distribution-free guarantee and its behaviour under heavy-tailed or heteroscedastic errors, not uniformly narrower intervals.
6. **Difficulty normalisation.** The pre-registered σ(x), built from T² and Q, improved efficiency and conditional coverage in most scenarios, but not uniformly. On corn it over-covered difficult samples, and a T²-only variant was more balanced there. That variant was identified *post hoc* and needs confirmation on independent data.
7. **Drift after standardisation.** A shift of the routine spectra after the transfer has been fitted (simulated as a one-channel wavelength shift) invalidated all intervals, including TJ+N (§4.5). The guarantee presupposes a stable target instrument between standardisation and use.

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

**Data availability.** All data sets are public: corn and IDRC Shootout 2002 tablets from Eigenvector Research [@eigenvector_data], and mango DMC from Mendeley Data (CC BY 4.0). Record version 1 (doi:10.17632/46htwnp833.1) was used for the season shift [@mango_data], and record version 6 (doi:10.17632/46htwnp833.6) for the instrument shift [@mango_data_v6]. All code, configuration, raw per-repetition results and the scripts regenerating every table and figure are available at [repository URL / archived DOI to be inserted on acceptance].

**Acknowledgements.** We thank the providers of the public data sets: Cargill and Eigenvector Research (corn), the International Diffuse Reflectance Conference (Shootout 2002), and N. Anderson, K. Walsh, P. Subedi and J. Walsh (mango).
