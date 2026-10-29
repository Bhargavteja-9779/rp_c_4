---
title: "Trustworthy prediction intervals after moving an NIR calibration to a new instrument or season: how many reference samples, and from how many batches?"
---

**Authors:** [Author 1]^a^, [Author 2]^a,\*^

^a^ [Affiliation, address, country]

\* Corresponding author: [e-mail address]

# Abstract {.unnumbered}

**Background:** When a near-infrared (NIR) calibration is moved to a new instrument or harvest season, a few reference samples are measured to adapt it. Results are then reported, and products accepted or rejected, with an uncertainty range. Whether that range still holds after the move, and what the reference samples must look like for it to hold, is rarely checked.

**Results:** On three public data sets (corn, tablets, mango), ranges taken from the original calibration lost most of their coverage after transfer (as low as 0.03 for nominal 90%). Re-fitting the transfer with each reference sample left out in turn gave valid intervals in all 40 planned scenarios with randomly chosen samples, at no extra cost. How the samples were collected mattered more than how many. With 20 reference fruit from only two consignments, intervals were too narrow for fruit from other consignments in 6 of 8 instrument and season settings (coverage 0.67–0.91), and the usual Gaussian, split-sample and random-effects intervals failed likewise. Spreading the samples over 15 or more consignments, or leaving out whole consignments when re-fitting, restored coverage. In a mango harvest-maturity check at 14% dry matter, the point prediction passed 45% of immature fruit; intervals from samples spread over ten consignments cut this to 3.8% (8.4% with two consignments).

**Significance:** Reliable uncertainty for a transferred NIR method can be obtained from the reference samples the transfer already needs, provided they come from many batches.

**Keywords:** calibration transfer; prediction interval; near-infrared spectroscopy; measurement uncertainty; conformal prediction; fruit dry matter

# 1. Introduction

NIR spectroscopy is used every day to measure moisture in grain, active ingredient in tablets and dry matter in fruit [@pasquini2018]. Each of these measurements relies on a calibration model built on one instrument, for one population of samples. Sooner or later the model has to be moved. A packhouse replaces a handheld unit, a pharmaceutical site adds a second spectrometer, a new harvest season brings fruit grown under different conditions. Calibration transfer handles the move. A small set of reference samples is measured on the new instrument, or in the new season, and used to correct either the spectra or the predictions: direct and piecewise direct standardisation (DS, PDS), or slope/bias correction (SBC) [@wang1991; @bouveresse1996; @feudale2002; @workman2018]. Newer approaches adapt the model with few or no reference values [@nikzad2018; @mishra2020dipls; @fonseca2022; @xie2024; @fan2025; @huang2026].

Transfer methods are almost always judged by their prediction error (RMSEP or bias). In practice, though, a laboratory does not report a bare number. It reports a value with an uncertainty range and takes decisions with it: a tablet batch is released if its assay lies within specification, and a mango block is harvested if the fruit reach a minimum dry matter. For mango, a minimum of 14% dry matter at harvest has long been recommended in Australia [@ainsworth2016]. The usual uncertainty statements for multivariate calibrations are error-propagation formulas and ASTM E1655-type intervals [@faber1997; @olivieri2006; @allegrini2016; @astm_e1655]. They are built from the error of the *original* calibration. After a move to a new instrument or season, that error no longer describes the model in use. A recent review of calibration transfer for portable optical instruments names the lack of uncertainty-aware validation as one of the open problems of the field [@haggam2026].

This paper asks a practical question. After a calibration has been transferred with *m* reference samples, can those same samples be used to give each new prediction an uncertainty range that can be trusted? And if so, which samples are needed?

Trusted here has a precise meaning. A 90% prediction interval should contain the reference value of about 90% of future samples. In method-validation language, this is a β-expectation tolerance interval, the quantity behind accuracy profiles [@hubert2004; @mee1984]. Conformal prediction gives intervals with this property under one assumption: the calibration samples and the future samples must be exchangeable, for example drawn at random from the same population [@vovk2005; @lei2018; @angelopoulos2023]. Conformal intervals have recently been used for NIR and MIR regression on a single instrument [@jovic2025; @duma2026], and for spectral classification under laboratory-to-field shift [@khairbek2026]. Corrections for a change in the spectral distribution exist [@tibshirani2019; @prinster2022], but they assume that the relation between spectrum and property stays the same, which an instrument change violates. Transfer creates two difficulties. First, the reference samples are needed to fit the transfer itself, and setting half of them aside to calibrate an interval leaves too few for either job. Second, the samples are rarely a random draw from future production. They usually come from one or two lots, collected on the day the instrument was set up.

The first difficulty has a clean solution. The jackknife+ [@barber2021] re-fits a model with each calibration sample left out in turn and uses the left-out errors to build the interval, so no sample is wasted. We apply it to the transfer step only: the original calibration stays as it is, and only the standardisation or bias correction is re-fitted. We call the result the transfer jackknife+ (TJ+). The coverage guarantee then follows from the existing theory; we do not claim new statistics. The second difficulty is the one that decides whether the method is useful in practice. When samples come in batches (harvest consignments, production lots), the theory says that the batch, not the individual sample, has to be the random unit [@lee2026; @dunn2023]. Whether this matters after calibration transfer, and how much, has to be measured. The mango data used here record which consignment every fruit came from, which allowed us to measure it.

We therefore organised the study around four questions a laboratory would ask:

1. Can the uncertainty statement of the original calibration be kept after transfer?

2. If not, can valid intervals be obtained from the reference samples alone, and how do they compare with the simpler options a laboratory might use (Gaussian intervals, the regression prediction interval of slope/bias correction, bootstrap)?

3. Does it matter whether the reference samples come from a few batches or from many?

4. What does this mean for a real accept/reject decision, here harvest-maturity screening of mango?

The study uses public data only and was planned in advance. The complete code reproduces every number in the paper.



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

This is the jackknife+ theorem applied to the transfer step, which is a symmetric fitting algorithm; Appendix A writes out the argument for this setting. In practice the coverage is usually close to $1-\alpha$ [@barber2021]. A bounded interval needs $m\ge9$ standards at $\alpha=0.10$ and $m\ge19$ at $\alpha=0.05$. With fewer, the method honestly returns an unbounded interval rather than an over-confident one.

## 2.3. Making the width follow the sample

PLS calibrations come with two standard warning signals: Hotelling $T^2$, for samples far from the calibration set, and the residual $Q$, for spectral features the model cannot explain. We use them to let the interval widen for difficult samples. The difficulty is

$$\sigma(\mathbf{x}) = \max\left\{\varepsilon,\; c_0 + c_1\sqrt{T^2(\mathbf{x})} + c_2\sqrt{Q(\mathbf{x})}\right\}, \qquad (4)$$

with $c_j\ge0$ fitted on the source cross-validation residuals only. Such normalised scores are standard in conformal regression [@papadopoulos2011; @jovic2025]. Inside TJ+N it is evaluated on the spectrum after each fold's transfer, so a spectrum that the transfer maps poorly gets a large $Q$ and a wider interval. This scaling is a refinement, not the core of the method. Its effect on efficiency was modest (Section 4.2), and the guarantee holds without it.

## 2.4. When the standards come in batches

Fruit arrive in consignments, tablets in production lots, grain in deliveries. Errors of a transferred calibration are often shared within a batch: a consignment of slightly riper fruit is predicted slightly too low, all together. If the $m$ standards come from only $K$ batches, their left-out errors reflect those $K$ batches. A sample from a new batch can then fall outside the interval more often than the nominal rate. Proposition 1 does not cover this case, because a sample from a new batch is not exchangeable with standards from the old ones.

The remedy is to treat the batch as the unit. In the batch-level version (TJ+B), all standards of batch $k$ are left out together, the transfer is re-fitted on the other batches, and each left-out error is given the weight $1/((K+1)n_k)$, so that every batch counts equally. This is the hierarchical jackknife+ of Lee, Barber and Willett [@lee2026]. It guarantees coverage $\ge1-2\alpha$ for a sample from a new batch, provided the batches behind the standards are a random draw of batches. Two consequences are useful in practice (Appendix B).

First, a bounded interval needs at least nine *batches* at $\alpha=0.10$, however many samples are taken from each.

Second, if every standard comes from a different, randomly chosen batch, the ordinary TJ+ already is the batch-level method, so nothing else is needed.

Appendix B also gives a simpler variant (TJ+G, the largest error per batch) with a short proof.

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

- ANOVA-PI: the random-effects (one-way ANOVA) prediction interval for a new batch, the classical counterpart of TJ+B [@mee1984];

- Gauss-LGO: a Gaussian interval from leave-batch-out errors, with $K-1$ degrees of freedom.

An exploratory label-free variant and the ablations of TJ+N (no leave-one-out, no "+", five-fold CV+, single-diagnostic scaling) are reported in the Supplementary Material.

# 3. Experimental

## 3.1. Data

Three public NIR data sets with documented shifts were used (Table 1, Fig. 2).

**Corn** [@eigenvector_data]. 80 samples measured on three spectrometers (m5 as master, mp5 and mp6) at 1100–2498 nm, with moisture, oil, protein and starch.

**Pharmaceutical tablets** (IDRC Shootout 2002) [@eigenvector_data]. 655 tablets on two spectrometers (600–1898 nm), with weight, hardness and assay. The organisers' calibrate, validate and test sets were kept.

**Mango dry matter** [@anderson2020; @mango_data]. Spectra of intact fruit (684–990 nm) from four seasons. Replicate scans were averaged per fruit, giving 4,677 fruit. Seasons 1–3 were the source and season 4 the target. Season 4 contains 18 consignments of 33–54 fruit each; the data providers call them populations, and each is one cultivar from one orchard, at one maturity stage and harvest date. For an instrument shift, the providers' extended data set [@mango_data_v6] was used: fruit measured on handheld unit 15006 and on one of three other units (15016, 15014, 15029). These pairs share 49, 38 and 29 consignments, respectively.

| Data set | Size | Shift | Range (channels) | Responses | Source train / source cal. / target pool | m |
|:--|--:|--:|--:|--:|--:|--:|
| Corn | 80 samples | m5 → mp5, mp6 (and mp5 → m5) | 1100–2498 nm (700) | moisture, oil, protein, starch (%) | 40 / 10 / 30 (random each repetition) | 10, 15, 20 |
| Tablets | 655 tablets | 1 → 2 | 600–1898 nm (650) | assay (mg), weight (mg), hardness | 155 / 40 / 460 (fixed) | 10, 20, 30, 50 |
| Mango | 4,677 fruit (3,952 source, 725 target) | seasons 1–3 → 4 | 684–990 nm (103) | dry matter (%) | 3,162 / 790 / 725 | 10, 20, 30, 50 |

Table: **Table 1.** Data sets and splitting protocol.


![**Fig. 2.** The three data sets. Top: mean spectra per instrument (corn, tablets) or per season group (mango). Bottom: distributions of the reference values.](figures/fig2_datasets.png){width=16.5cm}

## 3.2. How the study was run

All settings, seeds and criteria were fixed before target results were computed and are listed, together with a log of deviations, in the repository.

**Original calibrations.** Preprocessing (none, SNV, first or second Savitzky–Golay derivative) and the number of PLS components were chosen by 10-fold cross-validation on source data only [@barnes1989; @savitzky1964; @wold2001]. Ridge regression and a small 1D-CNN were used as alternative model types.

**Transfer.** PDS (window 5) [@wang1991], DS, SBC and no transfer. The planned main pipelines were PDS for corn and tablets and SBC for mango.

**Random standards.** In each repetition, $m$ standards were drawn at random from the target pool, and the remaining target samples served as test samples:

- corn: $m$ = 10, 15, 20;

- tablets and mango: $m$ = 10, 20, 30, 50.

This gives 40 main scenarios, with 500 repetitions for corn and tablets and 300 for mango. A further 200 repetitions per scenario compared the simpler interval formulas (Gauss-LOO-N, ASTM-T, OLS-PI, Boot-T) on identical standards.

**Standards from batches.** For the four mango settings (season shift with SBC; three instrument shifts with PDS and SBC), $K$ consignments were drawn at random and $n_g$ fruit taken from each, always with 20 standards or fewer:

- 2 × 10;

- 5 × 4;

- 10 × 2;

- 15 × 1;

- 20 × 1, for the instrument data only.

A chronological design took 4 fruit from each of the five earliest-harvested consignments. Coverage was measured on the fruit of the consignments that supplied no standards, averaging first within and then across consignments. Each design was repeated 300 times. This part of the study was specified after the first submission draft and before any of its results were computed.

**Application.** For the harvest-maturity case study, each test fruit was classified with its 90% interval:

- *pass* (mature) if the lower limit was at least 14% dry matter [@ainsworth2016];

- *fail* if the upper limit was below 14%;

- *refer* for a re-measurement otherwise.

The usual point rule (pass if the prediction is at least 14%) served as reference. We recorded how many immature fruit were passed, and how many fruit had to be referred (200 repetitions).

**Robustness and sensitivity.** These checks covered:

- Kennard–Stone selection of the standards [@kennard1969];

- added spectral noise;

- a wavelength shift of the routine spectra after standardisation (±1 and ±0.25 channel);

- half the source data;

- the PDS window and the number of PLS components;

- other model types (ridge, 1D-CNN);

- the reverse transfer direction.

**Evaluation.** For each repetition we recorded the share of test samples inside their interval (coverage), the interval width, and the interval score, which rewards narrow intervals and penalises misses [@gneiting2007]. Mean coverage over repetitions is given with a 95% bootstrap confidence interval. A method was flagged as *too narrow* in a scenario when the upper end of this interval was below the nominal level. As a positive check, we also report how often the lower end stayed within 0.02 of nominal. Interval scores were compared within scenarios with paired Wilcoxon tests and Holm correction [@holm1979]. Because realised coverage varies from one set of standards to the next, we also report the share of standard sets whose coverage on the test samples reached at least 0.85, which is what a laboratory validating a single transfer experiences. Computations used Python (NumPy, SciPy, scikit-learn, PyTorch) on 4 CPU cores.



# 4. Results and discussion

## 4.1. The old uncertainty statement does not survive the move

Transfer was clearly needed. Applied directly to the mp5 and mp6 spectra, the corn master models had prediction errors 2.6–5.2 times larger than after PDS with 20 standards (Supplementary Table S1). The uncertainty statements of the original calibrations fared worse than their predictions. On corn, nominal 90% intervals from the ASTM formula, from source split conformal prediction and from the covariate-shift-weighted version contained far fewer reference values than intended (coverage 0.03–0.74). All 72 of 72 scenario-method combinations were too narrow. On mango the coverage was 0.71–0.76 (12 of 12 too narrow). On tablets the picture was mixed (0.81–0.95; 11 of 36 too narrow): the assay suffered with ten standards, while hardness, which hardly changed between instruments, was unaffected (Table 2, Fig. 3).

The reason is simple. The original calibration error does not include the error added by the transfer itself, which is estimated from only a few standards. Out-of-fold source residuals did not help (SCP-S under-covered almost as badly as ASTM-PI). Neither did reweighting them for the change in spectral distribution: WCP-S returned unbounded intervals in 59% of corn repetitions and was too narrow elsewhere, because an instrument change alters the relation between spectrum and property, not only the spectra. Mapping source samples into the new instrument's space (Transport) recovered part of the coverage (mean coverage 0.75, range 0.29–0.92) but remained too narrow in 14 of 24 corn scenarios. The independent instrument shift on mango told the same story: after PDS, the source-based intervals covered only 0.15–0.51 of the fruit (Supplementary Table S6).

The practical message is plain. An uncertainty range validated on the original instrument says little about the transferred method and has to be re-established on the new one.

| Method | Corn coverage | Corn under | Tablets coverage | Tablets under | Mango coverage | Mango under | Unbounded (% reps) | Friedman rank (IS) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| TJ+N | 0.931 (0.91–0.96) | 0/24 | 0.910 (0.90–0.95) | 0/12 | 0.904 (0.90–0.91) | 0/4 | 0 | 2.52 |
| TJ+ | 0.933 (0.91–0.96) | 0/24 | 0.911 (0.90–0.95) | 0/12 | 0.904 (0.90–0.91) | 0/4 | 0 | 3.12 |
| SCP-T-split-N | 0.970 (0.90–1.00) | 0/24 | 0.942 (0.91–1.00) | 0/12 | 0.942 (0.90–1.00) | 0/4 | 50 | 6.03 |
| SCP-T-split | 0.969 (0.89–1.00) | 0/24 | 0.943 (0.91–1.00) | 0/12 | 0.941 (0.91–1.00) | 0/4 | 50 | 6.60 |
| Gauss-LOO | 0.904 (0.89–0.91) | 0/24 | 0.908 (0.89–0.93) | 0/12 | 0.904 (0.90–0.91) | 0/4 | 0 | 2.17 |
| ASTM-PI | 0.233 (0.03–0.43) | 24/24 | 0.925 (0.85–0.95) | 1/12 | 0.748 (0.73–0.76) | 4/4 | 0 | 5.03 |
| SCP-S | 0.453 (0.05–0.68) | 24/24 | 0.910 (0.81–0.94) | 5/12 | 0.729 (0.71–0.74) | 4/4 | 0 | 4.26 |
| WCP-S | 0.567 (0.19–0.74) | 24/24 | 0.917 (0.85–0.95) | 5/12 | 0.736 (0.72–0.75) | 4/4 | 49 | 6.26 |
| Transport | 0.753 (0.29–0.92) | 14/24 | 0.926 (0.88–0.97) | 4/12 | – | – | 0 | – |
| LF-conv | 0.883 (0.85–0.91) | 16/24 | 0.920 (0.88–0.96) | 4/12 | – | – | 0 | – |

Table: **Table 2.** Coverage of nominal 90% intervals (α = 0.10) for the primary transfer pipelines (corn and tablets: PDS; mango: SBC). Coverage: mean over scenarios of the mean per-repetition coverage, with the range over scenarios in parentheses. Under: scenarios flagged as under-covering (upper limit of the 95% bootstrap CI < 0.90) / number of scenarios. Friedman rank: mean rank of the scenario median interval score over the 40 scenarios (1 = best; only methods available in all scenarios).


![**Fig. 3.** Coverage of nominal 90% intervals versus the number of standards *m* when the standards are drawn at random (main pipelines; 500 repetitions for corn and tablets, 300 for mango). Markers: mean over scenarios; lines: range over scenarios; hollow markers: unbounded in more than half of the repetitions. Dashed line: nominal level.](figures/fig3_coverage_vs_m.png){width=16.5cm}

## 4.2. With randomly chosen standards, the standards are enough

When the standards were a random sample of the target samples, TJ+N held its level everywhere we looked. It was never too narrow in the 40 main scenarios, at any of the three confidence levels (90% shown in Table 2, 95% and 80% in Supplementary Table S2). Its mean coverage was 0.922 at 90%. The same held across all four transfer pipelines (0 of 152 combinations too narrow), for ridge and 1D-CNN models (0 of 22; Supplementary Table S4), for the reverse transfer direction, and for the independent transfer between handheld fruit spectrometers (0/72 scenario-level combinations too narrow).

This is what Proposition 1 predicts, and it should be read as a confirmation that the transfer step is the right thing to re-fit rather than as a discovery. It is still worth seeing how close the coverage stays to nominal. The lower end of the 95% confidence interval of coverage was within 0.02 of the nominal level in 192 of 192 scenario-level cases, so the intervals were not only "not detectably too narrow" but demonstrably close to target. Leaving the standard out matters. Computing the errors from a transfer that had seen all standards (the obvious shortcut) produced intervals that were too narrow in 199 of 528 cases, because a slope and bias fitted on the same standards absorb part of their own errors (Supplementary Table S3).

The alternative that is equally valid, splitting the standards in half, wastes them. With 15 or fewer standards, the half left for calibration was too small for a bounded 90% interval in any repetition (20 of 40 scenarios, all with m ≤ 15). Where both methods gave bounded intervals, TJ+N was narrower in 20 of 20 scenarios.



**Is a simpler formula enough?** A laboratory that has the left-out errors of its standards will naturally try something simpler first. We therefore compared TJ+N, on identical standards, with five formulas that need no new theory (Table 3; 100 scenario-pipeline combinations, 200 repetitions each):

- a *t*-interval from the leave-one-out RMSE (Gauss-LOO), and its version scaled by σ(x);

- the ASTM formula with the standard error re-estimated on the standards (ASTM-T);

- for slope/bias correction, the textbook prediction interval of the regression (OLS-PI);

- a bootstrap interval (Boot-T).

At 90%, most of them did reasonably well. Gauss-LOO was too narrow in 2 of 100 combinations, ASTM-T in 1 of 100 and OLS-PI in 2 of 52 of the slope/bias cases. They were often also narrower than TJ+N:

- the textbook OLS-PI had the lower interval score in 33 of 50 SBC scenarios where both were valid, TJ+N in 7;

- Gauss-LOO-N had the lower score in 81 of 97 (see also Supplementary Table S7).

For routine 90% statements with randomly chosen standards, these formulas are a defensible shortcut, and for slope/bias correction the textbook regression interval is hard to beat.

The picture changed at 95%. Gauss-LOO was then too narrow in 31 of 100, Gauss-LOO-N in 23 of 100, ASTM-T in 16 of 100 and OLS-PI in 16 of 52 combinations. TJ+N was never too narrow at any level (0 of 300). The bootstrap was the weakest option: it was too narrow in 52 of 100 combinations at 90%, and in 19 of 29 scenarios with ten standards. A bootstrap of 10–20 standards does not see enough variety to reproduce the error of a new sample.

Why do the formulas fail at 95%? Across scenarios, the coverage shortfall of Gauss-LOO grew with the skewness of the prediction errors (Spearman ρ = 0.35, p < 0.001) and with how much the leave-one-out RMSE underestimated the actual error (ρ = 0.35, p < 0.001). The shortfall of OLS-PI grew with skewness (ρ = 0.54, p < 0.001) and with heavy tails (excess kurtosis, ρ = 0.41, p = 0.002). This is what one would expect. A Gaussian interval sets its 95% limits from the spread of the errors and assumes symmetric tails. After transfer the errors are often skewed, for example when the transferred predictor is biased for part of the population, so one tail is longer than the formula assumes. TJ+N reads its limits from the left-out errors themselves and makes no such assumption, which is exactly what costs it some width at 90% and saves it at 95%.

| Data set | Pipeline | TJ+N | Gauss-LOO | Gauss-LOO-N | ASTM-T | OLS-PI | Boot-T | Split |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| Corn | PDS (24) | 0 / 0 | 6 / 0 | 0 / 0 | 0 / 0 | – | 7 / 3 | 0 / 0 |
| Corn | SBC (24) | 0 / 0 | 8 / 1 | 7 / 1 | 0 / 0 | 5 / 1 | 24 / 19 | 0 / 0 |
| Tablets | PDS (12) | 0 / 0 | 5 / 0 | 2 / 1 | 4 / 0 | – | 8 / 7 | 0 / 0 |
| Tablets | SBC (12) | 0 / 0 | 8 / 1 | 8 / 1 | 8 / 1 | 8 / 1 | 10 / 8 | 0 / 0 |
| Mango, season | SBC (4) | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 4 / 4 | 0 / 0 |
| Mango, instruments | PDS (12) | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | – | 0 / 0 | 0 / 0 |
| Mango, instruments | SBC (12) | 0 / 0 | 4 / 0 | 6 / 0 | 4 / 0 | 3 / 0 | 12 / 11 | 0 / 0 |

Table: **Table 3.** Simpler interval formulas on identical, randomly chosen standards (200 repetitions per scenario). Each cell gives the number of scenarios in which the method was too narrow at 95% / at 90% (number of scenarios in parentheses after the pipeline). OLS-PI applies to slope/bias correction only; Split: half of the standards fit the transfer, half calibrate the interval. Results at 80% and interval scores: Supplementary Table S12.




## 4.3. Where the standards come from matters more than how many there are

The results so far assume that the standards are a random sample of everything the instrument will measure later. In a packhouse this is rarely true. The fruit used to adapt a new handheld unit are typically picked from one or two consignments on the day of installation, and the unit is then used on consignments that arrive weeks later. We reproduced this on the mango data, where each fruit's consignment is recorded. The errors of the transferred predictors were clearly shared within consignments: the intra-consignment correlation of the errors was 0.46–0.63 across the eight setting-pipeline combinations.

Table 4, Fig. 4 and Supplementary Table S11 show what happens to fruit from consignments that supplied no standards. With 20 standards taken from only two consignments, TJ+N was too narrow in 6 of 8 combinations, with coverage of 0.67–0.91 for a nominal 0.90. The simple alternatives were worse:

- Gaussian intervals from the same left-out errors were too narrow in 8 of 8;

- the split-standards interval was too narrow in 8 of 8;

- the classical random-effects interval for a new batch (ANOVA-PI), which is designed for exactly this situation but has to estimate the between-batch variance from two batches, was too narrow in 8 of 8;

- the intervals carried over from the source calibration were too narrow everywhere.

The damage was largest for slope/bias correction. A slope and an offset fitted on two consignments learn the particular bias of those two consignments, and the left-out errors within them cannot reveal how different the next consignment will be. The same intervals were fine for the remaining fruit of the two sampled consignments (TJ+N coverage 0.91–0.93). The intervals were therefore accurate for the batches that had been sampled, but not for new ones.

Spreading the same number of standards over more consignments removed the problem step by step. TJ+N was too narrow in 4 of 8 combinations with 5 × 4 standards and 3 of 8 with 10 × 2. With one fruit from each of 15 or 20 consignments, no combination was too narrow at any confidence level (0 of 42 combinations over the three confidence levels), as Appendix B predicts.

The batch-level version TJ+B was never too narrow wherever it gave a bounded interval (0 of 58 combinations over all random designs and confidence levels; coverage 0.90–0.98 at 90%). With fewer than nine consignments it gives no finite interval at 90%, which is the honest answer: two consignments cannot certify what a third will look like. Where both were bounded, its intervals were wider than those of TJ+N with 10 × 2 standards (median width ratio 1.38) and identical with one fruit per consignment. A Gaussian interval with leave-one-consignment-out errors and K − 1 degrees of freedom was not too narrow either, but with two consignments its *t* factor made it 5.3 times wider than TJ+N, too wide to be useful.

The chronological design, with standards from the five earliest consignments and tests on everything harvested later, is the most realistic and the least favourable case: the later consignments were harvested weeks or seasons later, partly from other regions and cultivars. TJ+N was too narrow in 3 of 8 combinations, Gaussian intervals in 7 of 8, ANOVA-PI in 5 of 8, and the source-based ASTM interval in all 8. With five consignments, TJ+B could not give a bounded 90% interval; at the 80% level, where five consignments are enough, it covered 0.89–1.00 of the later fruit. No guarantee covers this design, and these numbers show why: early-season standards cannot speak for the late season.

For a laboratory, the lesson is cheap to apply. The cost of a transfer is the number of reference analyses, and that cost is the same whether 20 fruit come from 2 consignments or from 20. Taking one or two samples from each of many batches gives intervals that remain valid for future batches; taking many samples from a few batches does not.

| Consignments × fruit | TJ+N | TJ+B | Gauss-LOO | Split | ANOVA-PI | Gauss-LGO | ASTM-PI |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 2 × 10 | 0.80 (6/8) | unbounded | 0.74 (8/8) | 0.80 (8/8) | 0.81 (8/8) | 0.99 (0/8) | 0.55 (8/8) |
| 5 × 4 | 0.87 (4/8) | unbounded | 0.85 (7/8) | 0.87 (4/8) | 0.89 (3/8) | 0.94 (0/8) | 0.58 (8/8) |
| 10 × 2 | 0.90 (3/8) | 0.96 (0/8) | 0.89 (5/8) | 0.90 (1/8) | 0.91 (0/8) | 0.92 (0/8) | 0.59 (8/8) |
| 15 × 1 | 0.95 (0/8) | 0.95 (0/8) | 0.91 (0/8) | unbounded | 0.92 (0/8) | 0.91 (0/8) | 0.59 (8/8) |
| 20 × 1 | 0.92 (0/6) | 0.92 (0/6) | 0.91 (0/6) | 0.91 (0/6) | 0.92 (0/6) | 0.91 (0/6) | 0.57 (6/6) |
| chronological 5 × 4 | 0.87 (3/8) | unbounded | 0.81 (7/8) | 0.87 (3/8) | 0.84 (5/8) | 0.92 (1/8) | 0.55 (8/8) |

Table: **Table 4.** Coverage of nominal 90% intervals for fruit from consignments that supplied no standards, by how the standards were spread over consignments (mean over the setting-pipeline combinations, 300 repetitions each; in parentheses: combinations flagged as too narrow / combinations). The instrument settings alone have the 20 × 1 design. TJ+B: leave-one-consignment-out (hierarchical) jackknife+; Split: half the standards for transfer, half for calibration.


![**Fig. 4.** Coverage of nominal 90% intervals for mango fruit from consignments that supplied no standards, as a function of how 20 (or 15) standards were spread over consignments. Markers: mean over the eight setting-pipeline combinations (season shift; three handheld-instrument pairs; SBC, PDS or no transfer); lines: range. Hollow markers: unbounded intervals. Left: methods that treat samples as the unit; right: methods that treat consignments as the unit. Dashed line: nominal level.](figures/fig_batch_coverage.png){width=16.5cm}



## 4.4. What this means for a harvest decision

To see what interval validity means in practice, we used the mango data for the task the handheld instruments are bought for: deciding whether fruit have reached the 14% dry matter recommended at harvest [@ainsworth2016]. About 23% of the test fruit were below this threshold. Every test fruit came from a consignment that had supplied no standards, as it would in practice. A fruit was passed as mature if the lower limit of its 90% interval was at least 14%, and referred for re-measurement if the interval contained 14%. The usual practice, passing every fruit whose predicted value is at least 14%, served as reference (Table 5, Fig. 5).

The point rule passed 45% of the immature fruit after a season or instrument change (range over settings 31%–75%). A single NIR value close to the threshold carries little information about which side of it the fruit is really on. Intervals carried over from the original calibration halved this (21%) but were still far too optimistic. With intervals rebuilt from the standards the rate dropped to a few per cent, and here the sampling of the standards mattered as much as the formula. With standards from two consignments, TJ+N still passed 8.4% of the immature fruit and Gaussian intervals 11%. With the same number of standards spread over ten consignments, the rates were 3.8% and 3.7%. The batch-level TJ+B was the most cautious (1.3% with ten consignments). With only two consignments it referred every fruit, which is the honest outcome when the standards cannot say anything about new consignments.

The price of safety is the number of fruit that need a second look. With well-spread standards, TJ+N referred 63% of the fruit, and TJ+B 72%. This is not a weakness of the intervals. It reflects how close much of the fruit was to the threshold relative to the accuracy of a transferred handheld calibration (RMSEP 1.1–5.4% dry matter). An interval cannot make a measurement more precise. What it can do is tell the user which results can be acted on and which cannot, and it does so correctly only if it is valid for the consignments being tested.

| Rule | 2 × 10: immature passed | 2 × 10: referred | 10 × 2: immature passed | 10 × 2: referred | 20 × 1: immature passed | 20 × 1: referred |
|:--|--:|--:|--:|--:|--:|--:|
| Point rule (ŷ ≥ 14%) | 45.8 (31.5–69.3) | 0 | 45.1 (31.2–75.0) | 0 | 46.1 (27.6–74.2) | 0 |
| ASTM-PI (original calibration) | 22.6 (8.2–52.8) | 29 | 21.0 (4.3–53.8) | 31 | 23.4 (5.0–51.3) | 33 |
| Gauss-LOO | 11.5 (7.8–19.9) | 49 | 3.7 (0.9–6.0) | 62 | 3.3 (1.6–5.2) | 68 |
| TJ+N | 8.4 (2.3–12.0) | 56 | 3.8 (1.1–7.9) | 63 | 3.8 (1.3–6.8) | 67 |
| TJ+B (leave one consignment out) | 0.0 (0.0–0.0) | 100 | 1.3 (0.3–2.4) | 72 | 3.8 (1.3–6.8) | 67 |

Table: **Table 5.** Harvest-maturity screening of mango at 14% dry matter with 90% intervals, for fruit from consignments that supplied no standards. Immature passed: percentage of truly immature fruit (DM < 14%) declared mature, mean (range) over the setting-pipeline combinations; referred: percentage of all fruit whose interval contains 14% and which would be re-measured. Designs: consignments × fruit per consignment (the 20 × 1 design for the instrument settings only). 200 repetitions. Details: Supplementary Table S14.


![**Fig. 5.** Harvest-maturity screening at 14% dry matter, for fruit from consignments without standards. Left: share of immature fruit passed as mature; right: share of fruit referred for re-measurement because the 90% interval contains 14%. Bars: mean over setting-pipeline combinations; lines: range. Colours: how 20 standards were spread over consignments.](figures/fig_application.png){width=16.5cm}



## 4.5. What the intervals cannot do

Two further situations break the exchangeability on which every method here relies, and they are worth knowing before the intervals are used.

**Selecting standards by design.** Kennard–Stone selection picks standards that span the target population, so they are not a random sample. In our tests it made TJ+N conservative (coverage 0.93–0.96), because extreme standards produce larger left-out errors than typical samples. This is reassuring for a common practice, but it is an observation, not a guarantee.

**Drift after standardisation.** A shift of the routine spectra by one wavelength channel *after* the transfer had been fitted simulates an instrument that drifts between set-up and use. Under this shift no interval method remained valid (Fig. 6; Supplementary Table S5). On tablets, TJ+N covered only 0.04–0.07 of the samples. On corn and mango the $Q$ residual in the difficulty scaling caught much of the damage (TJ+N 0.60–0.94 and 0.73–0.97, against 0.02–0.29 and 0.07–0.21 for Gaussian intervals). Even a quarter-channel shift left TJ+N too narrow in 4/12 combinations (Supplementary Table S8). Spectral drift must therefore be monitored, for example with the $Q$ residual or with periodic check samples, and the transfer repeated when it appears. No interval computed at set-up time can absorb it.

Added spectral noise and halving the source data did not cause under-coverage (0 of 30 robustness scenarios without drift). Neither did changing the PDS window or the number of PLS components (0 of 27; Supplementary Table S9), although these settings changed the prediction error considerably. Poorer transfer settings simply produced wider intervals.

![**Fig. 6.** Coverage of nominal 90% intervals under Kennard–Stone selection of the standards, added spectral noise, a ±1-channel wavelength shift of the routine spectra after standardisation, and halved source data.](figures/fig6_robustness.png){width=16.5cm}

## 4.6. Cost and use in routine work

TJ+N needs *m* extra fits of the transfer step, carried out once, when the instrument is set up. A PDS fit with prediction took 4.6 ms for corn and 24.3 ms for tablets on one CPU core. The complete interval computation took 0.15 s, 2.79 s and 0.06 s for corn, tablets and mango (Supplementary Table S10). In routine use, each new spectrum is passed through the *m* stored transfers, which is negligible for any laboratory computer. The leave-one-batch-out version needs only *K* fits and is cheaper still.



## 4.7. A recipe for the laboratory

The results can be condensed into a short procedure for anyone who transfers an NIR calibration and must report results with an uncertainty range:

1. Do not reuse the uncertainty formula of the original calibration after a change of instrument or season.

2. Collect the reference samples for the transfer from as many different batches as practical, ideally one or two per batch, and at least nine batches for 90% statements about future batches. Twenty samples from twenty lots are worth far more than twenty samples from two lots, and cost the same in reference analyses.

3. Fit the transfer as usual. Then re-fit it with each standard left out (or, if several standards share a batch, each batch left out) and build the interval of Eq. (3) from the left-out errors. The code that accompanies this paper does this in a few lines.

4. Report the leave-one-out RMSE as well. Gaussian intervals built from it are acceptable at 90% when the standards are spread over many batches, but should not be used for 95% statements.

5. Watch for spectral drift after set-up (rising $Q$ residuals) and check a few fresh reference samples now and then. No interval computed at set-up time protects against drift.

## 4.8. Relation to measurement uncertainty

The intervals studied here are prediction intervals for the reference value of an individual routine sample. In method-validation terms they are β-expectation tolerance intervals [@hubert2004; @mee1984]. Their width therefore contains everything that separates the NIR result from the reference method: reference-method error, spectral noise, model error and the error added by the transfer. They are not a GUM-type uncertainty budget, in which components are estimated separately and propagated. They are a direct, empirical check that the transferred method meets a stated coverage. Error-propagation methods for multivariate calibration [@faber1997; @olivieri2006; @allegrini2016] give sample-specific uncertainties, but they rest on the original calibration's error model, which Section 4.1 shows no longer applies after transfer.

The guarantee is an average over possible sets of standards. For a single transfer, the realised coverage on the next few hundred samples varies. Across the main scenarios (m = 10–50 random standards), a median of 0.88 of the standard sets gave a realised coverage of at least 0.85 on the test samples; in the least favourable scenario the share was 0.74 (Supplementary Table S13). The Gaussian intervals did no better (0.82). Such statements about one particular set of standards (β-content intervals in validation terms) cannot be guaranteed by the jackknife+ in general [@bian2023], unless the fitting procedure is stable in a quantifiable sense [@liang2025]. A laboratory that needs them should use more standards, or a lower α, and re-check coverage on fresh samples.

## 4.9. Limitations

The evidence comes from three public data sets. The data on batches, which carry the central practical finding, come from one product (mango), measured in one season shift and on three handheld-instrument pairs. We found no other public NIR transfer data set that records lots, so the batch results should be confirmed on other products, such as pharmaceutical production lots or grain deliveries. The batch structure itself is real, but the batches used for standards were drawn at random from those available, which is more favourable than many real set-ups. The chronological design shows what happens otherwise.

The noise, wavelength-drift and Kennard–Stone experiments are simulations on real spectra. Only PLS, ridge and a small CNN were tested as models, and PDS, DS and SBC as transfer methods. Domain-adaptation methods that use no reference values cannot be covered by this approach, because it needs reference values for the standards. An exploratory label-free variant under-covered in 20 of 36 scenarios (Table 2).

Finally, every guarantee here is marginal and assumes a stable instrument between set-up and use.

# 5. Conclusions

Moving an NIR calibration to a new instrument or season breaks its old uncertainty statement. In our data, nominal 90% intervals carried over from the original calibration covered as few as 0.03 of the reference values. The reference samples used for the transfer are enough to restore a valid statement, without measuring anything extra, if the transfer is re-fitted with each of them left out in turn and the left-out errors are used to set the interval. This takes seconds.

What the reference samples must represent is the more important lesson. Intervals built from samples of a few batches were accurate for those batches but too narrow for the next ones, and none of the common alternatives avoided this without becoming too wide to be useful. Spreading the same number of reference samples over many batches, or leaving out whole batches when re-fitting, gave intervals that held for new batches. In a harvest-maturity check of mango, these intervals reduced the share of immature fruit passed as mature from 45% with the point prediction to 3.8%, and identified the fruit close to the threshold that should be re-measured.

For laboratories this turns into a rule that costs nothing: collect transfer standards from as many batches as possible, and report intervals obtained by leaving them out one (or one batch) at a time.

# Declarations {.unnumbered}

**CRediT authorship contribution statement.** [Author 1]: Conceptualization, Methodology, Software, Formal analysis, Writing – original draft. [Author 2]: Supervision, Validation, Writing – review & editing. *(To be completed by the authors.)*

**Declaration of competing interest.** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the authors used an AI assistant (Claude, Anthropic) for literature search support, code development, data analysis and drafting of the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

**Funding.** [To be completed by the authors.]

**Data availability.** All data sets are public: corn and IDRC Shootout 2002 tablets from Eigenvector Research [@eigenvector_data], and mango dry matter from Mendeley Data (record version 1, doi:10.17632/46htwnp833.1 [@mango_data]; record version 6, doi:10.17632/46htwnp833.6 [@mango_data_v6]). All code, configuration files, raw per-repetition results and the scripts that regenerate every table and figure are available at [repository URL / archived DOI to be inserted].

**Acknowledgements.** We thank the providers of the public data sets: Cargill and Eigenvector Research (corn), the International Diffuse Reflectance Conference (Shootout 2002), and N. Anderson, K. Walsh, P. Subedi and J. Walsh (mango).


# Appendix A. Proof of Proposition 1 {.unnumbered}

**Setting.** Let $Z_1,\dots,Z_m$ be the transfer standards and $Z_{m+1}=(\mathbf{x}^T_{m+1},\mathbf{x}^S_{m+1},y_{m+1})$ the future sample. Its master spectrum $\mathbf{x}^S_{m+1}$ is never used by the procedure; it enters only the argument, as the spectrum the sample *would* give on the master instrument. For any index set $S\subseteq\{1,\dots,m+1\}$, let $\mu_S$ and $\sigma_S$ be the deployed predictor (Eq. (1)) and the difficulty function obtained by applying the transfer algorithm $\mathcal{T}$ to $\{Z_k:k\in S\}$. The source model $f$ and the function $\sigma$ of Eq. (4) are fixed beforehand from source data. $\mathcal{T}$ is *symmetric*, i.e. invariant to the order of its inputs; this holds for PDS, DS and SBC, which are least-squares fits on the set of standards. Because $\sigma\ge\varepsilon>0$, all normalised scores are well defined.

**Step 1 (scores).** For $i\neq j$, write $-ij$ for the set $\{1,\dots,m+1\}\backslash \{i,j\}$ and define
$$R_{ij}=\frac{|y_i-\mu_{-ij}(\mathbf{x}^T_i)|}{\sigma_{-ij}(\mathbf{x}^T_i)}.$$
The fit that excludes $i$ and $m+1$ is exactly the leave-one-out fit $\mu_{-i}$ of Eq. (2), computed from the $m$ standards without standard $i$. Hence $R_i=R_{i,m+1}$, and for the future sample $|y_{m+1}-\mu_{-i}(\mathbf{x}^T_{m+1})|/\sigma_{-i}(\mathbf{x}^T_{m+1})=R_{m+1,i}$.

**Step 2 (miscoverage implies many lost comparisons).** Let $U_i=\mu_{-i}(\mathbf{x})+\sigma_{-i}(\mathbf{x})R_i$ and $L_i=\mu_{-i}(\mathbf{x})-\sigma_{-i}(\mathbf{x})R_i$ with $\mathbf{x}=\mathbf{x}^T_{m+1}$.

- *Upper tail.* If $y_{m+1}$ exceeds the upper bound in Eq. (3), the $\lceil(1-\alpha)(m+1)\rceil$-th smallest $U_i$, then $y_{m+1}>U_i$ for at least $(1-\alpha)(m+1)$ indices $i$.

- *Lower tail.* If $y_{m+1}$ is below the lower bound, the $k$-th smallest $L_i$ with $k=\lfloor\alpha(m+1)\rfloor$, then $y_{m+1}<L_i$ for at least $m-k+1\ge(1-\alpha)(m+1)$ indices.

In both cases $|y_{m+1}-\mu_{-i}(\mathbf{x})|/\sigma_{-i}(\mathbf{x})>R_i$, i.e. $R_{m+1,i}>R_{i,m+1}$, for at least $(1-\alpha)(m+1)$ indices. Therefore
$$\{y_{m+1}\notin\hat C(\mathbf{x}^T_{m+1})\}\subseteq\Big\{\textstyle\sum_{i\le m}\mathbf{1}\lbrack R_{m+1,i}>R_{i,m+1}\rbrack \ge(1-\alpha)(m+1)\Big\}.$$

**Step 3 (tournament bound).** Call a point $j\in\{1,\dots,m+1\}$ *strange* if $\sum_{i\neq j}\mathbf{1}\lbrack R_{ji}>R_{ij}\rbrack \ge(1-\alpha)(m+1)$. By the counting lemma in the proof of Theorem 1 of Barber et al. [@barber2021], at most $2\alpha(m+1)$ points can be strange, for any realisation of the scores.

**Step 4 (exchangeability).** The $Z_k$ are exchangeable and $\mathcal{T}$ is symmetric. Hence the joint law of the matrix $(R_{ij})$ is invariant under a simultaneous permutation of rows and columns, and every point is equally likely to be strange. Thus $\Pr\{Z_{m+1}\text{ strange}\}=\mathbb{E}\lbrack N_{\text{strange}}\rbrack /(m+1)\le 2\alpha$. Combining with Step 2 gives $\Pr\{y_{m+1}\notin\hat C\}\le 2\alpha$. $\square$

**Remarks.**

- The normalisation enters only through the definition of the scores. Steps 2–4 hold for any score of the form $|y_i-\mu_{-ij}(\mathbf{x}_i)|/\sigma_{-ij}(\mathbf{x}_i)$ with $\sigma>0$, provided the pair $(\mu,\sigma)$ is produced by a symmetric algorithm.

- Fitting the transfer on all $m$ standards and reusing it to compute residuals (TJ-insample) breaks Step 1: the residual of standard $i$ is then computed with a fit that has seen $i$, and the exchangeability with the future sample's residual is lost. The resulting under-coverage is observed in Section 4.2.

- Ties between scores have probability zero for continuous data; with ties, the strict inequalities in Step 2 make the interval only more conservative.

- If the standards are chosen by a data-dependent design such as Kennard–Stone, they are no longer exchangeable with a random future sample, and Step 4 does not apply.



# Appendix B. Batch-level validity (Proposition 2) {.unnumbered}

**Setting.** The target population consists of batches (production lots, harvest consignments). Let $B_1,\dots,B_{K+1}$ be batches drawn so that they are exchangeable, for example at random from the population of batches. Within batch $k$, let $Z_{k1},\dots,Z_{kn_g}$ be drawn so that, conditionally on the batch, they are exchangeable, for example at random from the batch. The standards are the $Kn_g$ samples of batches $1,\dots,K$. The future routine sample is $Z_{K+1,1}$. The other members of batch $K+1$ are hypothetical and are used only in the argument.

The transfer algorithm $\mathcal{T}$ is symmetric in its input samples. For index sets of batches $S$, write $\mu_S,\sigma_S$ for the deployed predictor and difficulty function fitted on the standards of the batches in $S$. For $k\neq l$, let $-kl$ denote all batches except $k$ and $l$.

**Proposition 2 (TJ+G).** Define the batch scores
$$S_{kl}=\max_{j\le n_g}\frac{|y_{kj}-\mu_{-kl}(\mathbf{x}^T_{kj})|}{\sigma_{-kl}(\mathbf{x}^T_{kj})},\qquad S_k=S_{k,K+1},$$
and the interval
$$\hat C_G(\mathbf{x})=\lbrack \hat q^-_\alpha\{\mu_{-k}(\mathbf{x})-\sigma_{-k}(\mathbf{x})S_k\},\ \hat q^{\text{+}}_\alpha\{\mu_{-k}(\mathbf{x})+\sigma_{-k}(\mathbf{x})S_k\}\rbrack ,$$
where the quantiles are taken over the $K$ batches with the ranks of Eq. (3) ($m$ replaced by $K$). Then $\Pr\{y_{K+1,1}\in\hat C_G(\mathbf{x}^T_{K+1,1})\}\ge1-2\alpha$.

*Proof.* Let $\mathbf{x}=\mathbf{x}^T_{K+1,1}$.

- **Step 1 (miscoverage implies lost comparisons).** If $y_{K+1,1}\notin\hat C_G(\mathbf{x})$, the argument of Appendix A, Step 2 gives
  $$|y_{K+1,1}-\mu_{-k}(\mathbf{x})|/\sigma_{-k}(\mathbf{x})>S_{k,K+1}$$
  for at least $(1-\alpha)(K+1)$ batches $k$.

- **Step 2 (bound by the batch score).** Since $\mu_{-k}=\mu_{-(K+1),k}$ is fitted without batches $k$ and $K+1$, the left-hand side is one of the terms of the maximum defining $S_{K+1,k}$. Hence $S_{K+1,k}>S_{k,K+1}$ for at least $(1-\alpha)(K+1)$ indices, i.e. batch $K+1$ is *strange* in the sense of Appendix A, Step 3.

- **Step 3 (exchangeability).** $S_{kl}$ is a symmetric function of the members of batch $k$. The batches are exchangeable and $\mathcal{T}$ is symmetric, so the law of the matrix $(S_{kl})$ is invariant under simultaneous permutations of the batch indices.

- **Step 4 (counting).** The tournament lemma of Barber et al. [@barber2021] bounds the expected number of strange batches by $2\alpha(K+1)$. Therefore $\Pr\{\text{batch }K+1\text{ strange}\}\le2\alpha$. $\square$

**Remarks.**

1. **One standard per batch.** With $n_g=1$, TJ+G coincides with TJ+. Ordinary TJ+ is therefore valid for samples from *new* batches when every standard comes from a different, randomly drawn batch.

2. **The hierarchical jackknife+.** The hierarchical jackknife+ of Lee, Barber & Willett [@lee2026] uses the same leave-one-batch-out fits. It weights each member score by $1/((K+1)n_k)$ and places a mass $1/(K+1)$ at $\pm\infty$, with the same $1-2\alpha$ guarantee. TJ+H is its instantiation for the transfer step. It is less conservative than the maximum score of TJ+G when $n_g>1$. We use TJ+H as the primary batch-level construction and claim no new conformal methodology.

3. **Number of batches.** Both constructions give finite bounds only if $\lceil(1-\alpha)(K+1)\rceil\le K$, i.e. $K\ge9$ batches at $\alpha=0.10$, $K\ge19$ at $\alpha=0.05$ and $K\ge4$ at $\alpha=0.20$, whatever the number of standards per batch. The number of distinct batches, not the number of standards, determines whether a valid statement for new batches can be made.

4. **Samples from batches that supplied standards.** For routine samples from such batches, neither construction is tailored. Prediction sets for a new observation from an already observed group have been studied for hierarchical models [@dunn2023] and are not pursued here.
