
# 2. Theory

## 2.1. Setting

Let $f$ be the original calibration (PLS unless stated otherwise), built on source data: the master instrument, or earlier seasons. After the move, $m$ reference samples (transfer standards) $Z_i=(\mathbf{x}^T_i,\mathbf{x}^S_i,y_i)$ are available. $\mathbf{x}^T_i$ is the spectrum on the new instrument or in the new season, $\mathbf{x}^S_i$ the spectrum of the same sample on the master instrument (needed only for spectral standardisation), and $y_i$ the reference value. The transfer method $\mathcal{T}$ turns a set of standards $\mathcal{D}$ into the predictor that is actually used,

$$\mu_{\mathcal{D}}(\mathbf{x}) = a_{\mathcal{D}} + b_{\mathcal{D}}\, f\!\left(g_{\mathcal{D}}(\mathbf{x})\right), \qquad (1)$$

where $g_{\mathcal{D}}$ is a spectral standardisation and $(a_{\mathcal{D}},b_{\mathcal{D}})$ an output correction. For PDS and DS, $g$ is fitted on the spectrum pairs and $(a,b)=(0,1)$. For SBC, $g$ is the identity and $(a,b)$ come from regressing $y_i$ on $f(\mathbf{x}^T_i)$. Without transfer, $\mu=f$. For a new routine sample we want an interval $\hat C(\mathbf{x})$ that contains its reference value with probability at least $1-\alpha$ and is as narrow as possible.

## 2.2. Re-fitting the transfer with one standard left out (TJ+)

For each $i$ the transfer is re-fitted without standard $i$, giving $\mu_{-i}$. The left-out error of standard $i$ is scaled by a difficulty value $\sigma_{-i}(\mathbf{x}^T_i)$ (Section 2.3):

$$R_i = \frac{|y_i - \mu_{-i}(\mathbf{x}^T_i)|}{\sigma_{-i}(\mathbf{x}^T_i)}, \qquad i=1,\dots,m. \qquad (2)$$

The interval for a new spectrum $\mathbf{x}$ collects the $m$ left-out predictions, each widened by its own scaled error:

$$\hat C(\mathbf{x}) = \lbrack \hat q^{-}_{\alpha}\{\mu_{-i}(\mathbf{x}) - \sigma_{-i}(\mathbf{x})R_i\},\;\; \hat q^{\text{+}}_{\alpha}\{\mu_{-i}(\mathbf{x}) + \sigma_{-i}(\mathbf{x})R_i\}\rbrack. \qquad (3)$$

Here $\hat q^{\text{+}}_{\alpha}$ is the $\lceil(1-\alpha)(m+1)\rceil$-th smallest value ($+\infty$ if this rank exceeds $m$), and $\hat q^{-}_{\alpha}$ is the $\lfloor\alpha(m+1)\rfloor$-th smallest ($-\infty$ if the rank is below 1). The original calibration $f$ is never re-fitted; often it could not be, because its data belong to another instrument or season. We write TJ+N for the scaled version used throughout, and TJ+ when $\sigma\equiv1$. For PDS each re-fit takes milliseconds, and the whole interval takes seconds at most. Fig. 1 summarises the procedure.

![**Fig. 1.** The procedure in four steps. Only the transfer step is re-fitted; the original calibration and the difficulty scaling are fixed beforehand from source data.](figures/fig1_overview.png){width=16.5cm}

**Proposition 1** [@barber2021]. *If the $m$ standards and the future sample are exchangeable (for instance, all drawn at random from the routine population), and $f$ and $\sigma$ do not use the standards, then $\Pr\{y\in\hat C(\mathbf{x})\}\ge 1-2\alpha$.*

This is the jackknife+ theorem applied to the transfer step, which is a symmetric fitting algorithm; Appendix A writes out the argument for this setting. In practice the coverage is usually close to $1-\alpha$ [@barber2021]. A bounded interval needs $m\ge9$ standards at $\alpha=0.10$ and $m\ge19$ at $\alpha=0.05$. With fewer standards the method returns an unbounded interval rather than an over-confident one.

## 2.3. Making the width follow the sample

PLS calibrations come with two standard warning signals: Hotelling $T^2$, for samples far from the calibration set, and the residual $Q$, for spectral features the model cannot explain. We use them to let the interval widen for difficult samples. The difficulty is

$$\sigma(\mathbf{x}) = \max\left\{\varepsilon,\; c_0 + c_1\sqrt{T^2(\mathbf{x})} + c_2\sqrt{Q(\mathbf{x})}\right\}, \qquad (4)$$

with $c_j\ge0$ fitted on the source cross-validation residuals only. Such normalised scores are standard in conformal regression [@papadopoulos2011; @jovic2025]. Inside TJ+N it is evaluated on the spectrum after each fold's transfer, so a spectrum that the transfer maps poorly gets a large $Q$ and a wider interval. This scaling is a refinement, not the core of the method. Its effect on efficiency was modest (Supplementary Table S3), and the guarantee holds without it.

## 2.4. When the standards come in batches

Fruit arrive in consignments, tablets in production lots, grain in deliveries. Errors of a transferred calibration are often shared within a batch: a consignment of slightly riper fruit is predicted slightly too low, all together. If the $m$ standards come from only $K$ batches, their left-out errors reflect those $K$ batches. A sample from a new batch can then fall outside the interval more often than the nominal rate. Proposition 1 does not cover this case, because a sample from a new batch is not exchangeable with standards from the old ones.

The remedy is to treat the batch as the unit. In the batch-level version (TJ+B), all standards of batch $k$ are left out together, the transfer is re-fitted on the other batches, and each left-out error is given the weight $1/((K+1)n_k)$, so that every batch counts equally. This is the hierarchical jackknife+ of Lee, Barber and Willett [@lee2026]. It guarantees coverage $\ge1-2\alpha$ for a sample from a new batch, provided the batches behind the standards are a random draw of batches. Two consequences are useful in practice (Appendix B).

First, a bounded interval needs at least nine *batches* at $\alpha=0.10$, however many samples are taken from each.

Second, if every standard comes from a different, randomly chosen batch, the ordinary TJ+ already is the batch-level method, so nothing else is needed.

We use this construction with the σ(x) scaling and call it TJ+B. Appendix B also gives a variant that keeps only the largest error per batch (TJ+G), with a short self-contained proof. At 90% and 95% both gave identical intervals in the designs studied here, because both then reduce to the largest left-out error; at 80% TJ+B was slightly less conservative. The guarantee of TJ+B rests on the theorem of Lee et al. [@lee2026], that of TJ+G on Appendix B.

## 2.5. Methods compared

All methods use the same transferred predictor and differ only in the interval. They fall into four groups.

*Intervals carried over from the original calibration:*

- ASTM-PI: the ASTM E1655-type interval $\mu(\mathbf{x})\pm t\,\mathrm{SEC}\sqrt{1+h(\mathbf{x})}$, with the source standard error of calibration [@astm_e1655];
- SCP-S: split conformal prediction with source residuals [@lei2018];
- WCP-S: a version reweighted for covariate shift [@tibshirani2019];
- Transport: a regression version of transported conformal calibration [@doula2026].

*Intervals built from the standards with simple formulas:*

- Gauss-LOO: $\mu(\mathbf{x})\pm t_{m-1}\mathrm{RMSE_{LOO}}$, from the same left-out errors as TJ+;
- Gauss-LOO-N: the same, scaled by $\sigma(\mathbf{x})$;
- ASTM-T: the ASTM formula with the standard error re-estimated from the left-out errors;
- OLS-PI: for SBC only, the textbook prediction interval of the regression of $y$ on $f$;
- Boot-T: a bootstrap prediction interval with 200 resamples of the standards [@davison1997], in the resampling tradition of chemometric uncertainty estimation [@chiappini2025].

*Valid alternatives that cost standards:*

- SCP-T-split: half the standards fit the transfer and half calibrate a split-conformal interval.

*Batch-aware alternatives:*

- Gauss-LGO: a Gaussian interval from leave-one-batch-out errors, with $K-1$ degrees of freedom;
- ANOVA-PI: the random-effects (one-way ANOVA) prediction interval for a new batch [@mee1984], computed from the same signed leave-one-batch-out errors, with moment estimates of the between- and within-batch variances (the former truncated at zero), Satterthwaite degrees of freedom, and a centre shifted by the mean left-out error;
- LGO-CV+N: CV+ with batches as folds but with every sample counted as a separate unit, a natural shortcut without a guarantee for new batches.

An exploratory label-free variant and the ablations of TJ+N (no leave-one-out, no "+", five-fold CV+, single-diagnostic scaling) are reported in the Supplementary Material.

# 3. Experimental

## 3.1. Data

Three public NIR data sets with documented shifts were used (Table 1, Fig. 2).

**Corn** [@eigenvector_data]. 80 samples measured on three spectrometers (m5 as master, mp5 and mp6) at 1100–2498 nm, with moisture, oil, protein and starch.

**Pharmaceutical tablets** (IDRC Shootout 2002) [@eigenvector_data]. 655 tablets on two spectrometers (600–1898 nm), with weight, hardness and assay. The organisers' calibrate, validate and test sets were kept.

**Mango dry matter** [@anderson2020; @mango_data]. Spectra of intact fruit (684–990 nm) from four seasons. Replicate scans were averaged per fruit, giving {{n_fruit}} fruit. Seasons 1–3 were the source and season 4 the target. Season 4 contains {{r_n_pops_s4}} consignments of {{r_pop_size_s4}} fruit each; the data providers call them populations, and each is one cultivar from one orchard, at one maturity stage and harvest date. For an instrument shift, the providers' extended data set [@mango_data_v6] was used: fruit measured on handheld unit 15006 and on one of three other units (15016, 15014, 15029). These pairs share {{r_n_pops_inst}} consignments, respectively.

{{table1}}

![**Fig. 2.** The three data sets. Top: mean spectra per instrument (corn, tablets) or per season group (mango). Bottom: distributions of the reference values.](figures/fig2_datasets.png){width=16.5cm}

## 3.2. How the study was run

For the main experiments with random standards, all settings, seeds and criteria were fixed before target results were computed. The batch study and the harvest case study were specified later, before their own results were computed, and one baseline was corrected after an internal review; all changes are recorded in a dated deviation log in the repository.

**Original calibrations.** Preprocessing (none, SNV, first or second Savitzky–Golay derivative) and the number of PLS components were chosen by 10-fold cross-validation on source data only [@barnes1989; @savitzky1964; @wold2001]. Ridge regression and a small 1D-CNN were used as alternative model types.

**Transfer.** PDS (window 5) [@wang1991], DS, SBC and no transfer. The planned main pipelines were PDS for corn and tablets and SBC for mango.

**Random standards.** In each repetition, $m$ standards were drawn at random from the target pool, and the remaining target samples served as test samples:

- corn: $m$ = 10, 15, 20;
- tablets and mango: $m$ = 10, 20, 30, 50.

This gives {{n_scen_main}} main scenarios, with 500 repetitions for corn and tablets and 300 for mango. A further 200 repetitions per scenario compared the simpler interval formulas (Gauss-LOO-N, ASTM-T, OLS-PI, Boot-T) on identical standards.

**Standards from batches.** For the four mango settings, giving eight setting-pipeline combinations (season shift with SBC and without transfer; three instrument shifts with PDS and SBC), $K$ consignments were drawn at random and $n_g$ fruit taken from each, always with 20 standards or fewer:

- 2 × 10;
- 5 × 4;
- 10 × 2;
- 15 × 1;
- 20 × 1, for the instrument data only.

A chronological design took 4 fruit from each of the five earliest-harvested consignments. Coverage was measured on the fruit of the consignments that supplied no standards, averaging first within and then across consignments. Each design was repeated 300 times. This part of the study was specified after the first manuscript draft and before any of its results were computed. One baseline (ANOVA-PI) was corrected after an internal review and the experiment re-run (deviation R3).

**Application.** For the harvest-maturity case study, each test fruit was classified with its 90% interval:

- *pass* (mature) if the lower limit was at least 14% dry matter [@ainsworth2016];
- *fail* if the upper limit was below 14%;
- *refer* for a re-measurement otherwise.

The usual point rule (pass if the prediction is at least 14%) served as reference. We recorded how many immature fruit were passed, and how many fruit had to be referred (200 repetitions). This case study was added after the batch results were known.

**Robustness and sensitivity.** These checks covered:

- Kennard–Stone selection of the standards [@kennard1969];
- added spectral noise;
- a wavelength shift of the routine spectra after standardisation (±1 and ±0.25 channel);
- half the source data;
- the PDS window and the number of PLS components;
- other model types (ridge, 1D-CNN);
- the reverse transfer direction.

**Evaluation.** For each repetition we recorded the share of test samples inside their interval (coverage), the interval width, and the interval score, which rewards narrow intervals and penalises misses [@gneiting2007]. Mean coverage over repetitions is given with a 95% bootstrap confidence interval. A method was flagged as *too narrow* in a scenario when the upper end of this interval was below the nominal level. As a positive check, we also report how often the lower end stayed within 0.02 of nominal. Interval scores were compared within scenarios with paired Wilcoxon tests and Holm correction [@holm1979]. Because realised coverage varies from one set of standards to the next, we also report the share of standard sets whose coverage on their test samples reached at least 0.85. For small test sets (corn: 10–20 samples) this share also reflects the randomness of the test set itself. Bootstrap intervals resample repetitions and are therefore conditional on the data sets and, for the batch study, on the available consignments. Computations used Python (NumPy, SciPy, scikit-learn, PyTorch) on 4 CPU cores.
