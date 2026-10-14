---
title: "Valid prediction intervals for transferred NIR calibrations: reusing the transfer standards with a leave-one-standard-out jackknife+"
---

**Authors:** [Author 1]^a^, [Author 2]^a,\*^

^a^ [Affiliation, address, country]

\* Corresponding author: [e-mail address]

# Abstract {.unnumbered}

**Background:** Calibrations built on one spectrometer or season are routinely transferred to others using a few transfer standards. Whether the prediction intervals of a transferred calibration keep their nominal coverage has not been studied systematically, and splitting the scarce standards between transfer and uncertainty calibration wastes them.

**Results:** We propose a transfer jackknife+ (TJ+N). Each standard is left out in turn and the transfer step (e.g., piecewise direct standardisation) is re-fitted on the others. The leave-one-out residuals, normalised by a source-learned function of Hotelling T² and Q residuals, define distribution-free intervals with coverage ≥ 1−2α for exchangeable standards. On three public NIR data sets (instrument and season shift; 40 pre-registered scenarios, up to 500 repetitions each), source-calibrated intervals under-covered after transfer, with coverage as low as 0.03 for a nominal 0.90. TJ+N had a mean coverage of 0.922 and was never flagged as under-covering, at α = 0.05, 0.10 or 0.20, under four transfer pipelines, or with PLS, ridge and 1D-CNN models, including an independent transfer between handheld fruit spectrometers. Splitting the standards gave unbounded intervals for *m* ≤ 15. Gaussian intervals from leave-one-out residuals were similarly efficient at 90% but under-covered in 14 of 40 scenarios at 95%. Wavelength drift after standardisation, even by a quarter channel, compromised all methods.

**Significance:** TJ+N gives finite-sample-valid uncertainty for transferred NIR calibrations from the standards that calibration transfer already requires, at the cost of *m* refits of the transfer step (seconds or less).

**Keywords:** calibration transfer; prediction interval; conformal prediction; jackknife+; near-infrared spectroscopy; measurement uncertainty

# 1. Introduction

Near-infrared (NIR) spectroscopy with multivariate calibration is a mature analytical technique [@pasquini2018]. Its calibrations, however, are tied to the instrument, measurement conditions and sample population on which they were built. When a model developed on a master instrument is moved to a secondary instrument, or applied to a new harvest season, its predictions degrade unless the model or the spectra are corrected [@feudale2002; @workman2018; @anderson2020]. Calibration transfer addresses this. Direct and piecewise direct standardisation (DS, PDS) map secondary-instrument spectra onto the master space using transfer standards measured on both instruments [@wang1991; @bouveresse1996]. Slope/bias correction (SBC) adjusts the predictions using standards with reference values [@feudale2002]. Domain-adaptation methods such as di-PLS and standard-free approaches remain an active topic, including in this journal [@nikzad2018; @mishra2020dipls; @fonseca2022; @xie2024; @fan2025; @huang2026].

Calibration-transfer studies are almost always judged by point-prediction accuracy (RMSEP, bias). Analytical results, however, must be accompanied by a statement of uncertainty, and multivariate calibration has a long tradition of uncertainty estimation and figures of merit [@faber1997; @olivieri2006; @allegrini2016]. In routine practice, approximate prediction intervals are derived from the calibration error and the leverage of the new sample, as in ASTM E1655-type procedures [@astm_e1655]. These intervals use the *source* calibration error model. After an instrument or season change, that error model no longer describes the deployed predictor. The transfer step adds its own error, and the standardisation is estimated from only a few standards.

Conformal prediction provides intervals with finite-sample, distribution-free coverage guarantees under exchangeability [@vovk2005; @lei2018; @angelopoulos2023; @fontana2023]. In chemometrics it has been used mainly for classification [@gu2019; @redd2024; @qian2024; @booksh2025] and for in-distribution regression. Examples are normalised conformal regression of mid-infrared spectra [@jovic2025], conformal-inspired intervals for PLS and PCR [@duma2025], and QSAR applicability domains [@norinder2014]. Coverage guarantees break when calibration and deployment data are not exchangeable, which is exactly the calibration-transfer situation. Weighted conformal prediction [@tibshirani2019] and its jackknife+ counterpart JAWS [@prinster2022] correct for covariate shift using labelled source data. An instrument change, however, alters the relation between spectrum and property, not only the spectral distribution, which violates the covariate-shift assumption. Outside spectroscopy, the growth of uncertainty after calibration transfer has been characterised empirically for networks of low-cost air-quality sensors [@zhivkov2026], without finite-sample guarantees. Transporting calibration data between paired domains has very recently been proposed for classification [@doula2026]. In searches of Crossref, arXiv and the web (2015–2026; terms combining conformal prediction, jackknife+, prediction intervals and uncertainty with calibration transfer, model transfer, standardisation, near-infrared and spectroscopy), we found no study of interval validity for transferred spectroscopic calibrations.

A practical constraint shapes the problem. The only target-domain data with reference values are typically the *m* transfer standards, often 10–30 samples, and they are already needed to fit the transfer. A valid but naïve solution splits them: half fit the transfer and half calibrate a split-conformal interval. With *m* < 18 at α = 0.1, the calibration half is too small to give finite intervals. The jackknife+ [@barber2021] avoids sample splitting through leave-one-out refits, with a coverage guarantee of 1−2α. We use this to construct intervals for *transferred* calibrations by re-fitting the transfer step, not the source model, inside the leave-one-out loop. All standards are therefore reused for both purposes.

**What is and is not new.** The inference engine is the jackknife+ [@barber2021], and normalised nonconformity scores are established [@papadopoulos2011; @jovic2025]; we claim no new conformal theory. What we contribute is the instantiation of the method for calibration transfer, together with the evidence that it is needed:

- **Which step to re-fit.** Only the transfer step is placed inside the leave-one-out loop. The source model is kept fixed, and in practice it often cannot be re-fitted because it belongs to another instrument or season.

- **Why the obvious alternatives fall short.** The two natural practices are residuals of the fitted transfer and Gaussian intervals from the leave-one-standard-out RMSE. Neither carries a guarantee, and both are shown to fail in identifiable conditions.

- **Practical consequences** for analytical laboratories: the minimum number of standards, the requirement on how standards are selected, and the failure under drift after standardisation.

The contributions of this work are:

1. A transfer jackknife+ (TJ+) for transferred multivariate calibrations, with a finite-sample coverage statement under explicit conditions on how the standards are selected (Appendix A).

2. A chemometric normalisation (TJ+N). A source-learned difficulty function of Hotelling T² and Q residuals is evaluated on the *transferred* spectrum within each leave-one-out fit, so that interval width adapts to the sample and to spectra that the transfer maps poorly.

3. A pre-registered benchmark on three public NIR data sets covering instrument and season shift. It compares classical, source-calibrated, shift-weighted, transport-based, split-standards and Gaussian intervals, and includes ablation, robustness, model-class (PLS, ridge, 1D-CNN), sensitivity, computational and error analyses.

4. An exploratory label-free variant for the case in which the transfer standards have no reference values.

The study addresses the following research questions:

- **RQ1.** Do conventional intervals remain valid after transfer?

- **RQ2.** Is TJ+N valid and efficient for realistic numbers of standards?

- **RQ3.** Which components of TJ+N matter?

- **RQ4.** How robust is it to standard selection, noise, drift and reduced source data?

- **RQ5.** Does it generalise across transfer pipelines, directions, model classes and instruments?

- **RQ6.** What does it cost?

All code and the complete reproduction pipeline are publicly available.

# 2. Theory

## 2.1. Problem formulation

Let $f:\mathbb{R}^p\to\mathbb{R}$ be a calibration model (PLS unless stated otherwise) fitted on source-domain data $\mathcal{D}_S$: master-instrument spectra or earlier seasons. In the target domain, $m$ transfer standards $Z_i=(\mathbf{x}^T_i,\mathbf{x}^S_i,y_i)$, $i=1,\dots,m$, are available. Here $\mathbf{x}^T_i$ is the target spectrum, $\mathbf{x}^S_i$ the master spectrum of the same sample (needed only for spectral standardisation) and $y_i$ the reference value. A transfer algorithm $\mathcal{T}$ maps a set of standards $\mathcal{D}$ to a *deployed predictor*

$$\mu_{\mathcal{D}}(\mathbf{x}) = a_{\mathcal{D}} + b_{\mathcal{D}}\, f\!\left(g_{\mathcal{D}}(\mathbf{x})\right), \qquad (1)$$

where $g_{\mathcal{D}}$ is a spectral standardisation and $(a_{\mathcal{D}},b_{\mathcal{D}})$ an output correction.

- PDS or DS: $g$ is fitted from the pairs $(\mathbf{x}^T_i,\mathbf{x}^S_i)$ and $(a,b)=(0,1)$.

- SBC: $g$ is the identity and $(a,b)$ come from the least-squares regression of $y_i$ on $f(\mathbf{x}^T_i)$.

- No transfer: $\mu=f$.

For a new target sample $(\mathbf{x}^T_{m+1},y_{m+1})$ we seek an interval $\hat C(\mathbf{x}^T_{m+1})$ with $\Pr\{y_{m+1}\in\hat C(\mathbf{x}^T_{m+1})\}\ge 1-\alpha$, as narrow as possible.

## 2.2. Difficulty function

A heteroscedastic, sample-specific scale is obtained from PLS diagnostics. For a (transferred) spectrum, let $T^2(\mathbf{x})=\sum_{a=1}^{A} t_a^2/s_{t_a}^2$ (Hotelling T² in the $A$-dimensional score space) and $Q(\mathbf{x})=\lVert \mathbf{x}_c-\mathbf{t}\mathbf{P}^{\mathsf T}\rVert^2$ (the squared spectral residual), both computed in the preprocessed, mean-centred spectral space of the source model. We set

$$\sigma(\mathbf{x}) = \max\left\{\varepsilon,\; c_0 + c_1\sqrt{T^2(\mathbf{x})} + c_2\sqrt{Q(\mathbf{x})}\right\}, \qquad (2)$$

with $c_j\ge 0$ fitted by non-negative least squares to the absolute out-of-fold residuals of the source cross-validation, and $\varepsilon$ equal to 5% of their median. $\sigma$ is fixed **before** any target datum is used. Within TJ+N, $\sigma$ is evaluated on the spectrum after the fold-specific transfer, $\sigma_{\mathcal{D}}(\mathbf{x})=\sigma(g_{\mathcal{D}}(\mathbf{x}))$. Spectra that are poorly reconstructed by the source model after transfer (large $Q$), or that extrapolate in score space (large $T^2$), therefore receive wider intervals.

## 2.3. Transfer jackknife+ (TJ+)

For each $i$, the transfer is re-fitted without standard $i$, giving $\mu_{-i}=\mu_{\mathcal{D}\setminus\{i\}}$ and $\sigma_{-i}=\sigma_{\mathcal{D}\setminus\{i\}}$. The leave-one-standard-out normalised residuals are

$$R_i = \frac{\lvert y_i - \mu_{-i}(\mathbf{x}^T_i)\rvert}{\sigma_{-i}(\mathbf{x}^T_i)}, \qquad i=1,\dots,m. \qquad (3)$$

The TJ+N interval for a new target spectrum $\mathbf{x}$ is

$$\hat C(\mathbf{x}) = \left[\, \hat q^{-}_{\alpha}\{\mu_{-i}(\mathbf{x}) - \sigma_{-i}(\mathbf{x})R_i\},\;\; \hat q^{+}_{\alpha}\{\mu_{-i}(\mathbf{x}) + \sigma_{-i}(\mathbf{x})R_i\}\,\right], \qquad (4)$$

where $\hat q^{+}_{\alpha}\{v_i\}$ is the $\lceil(1-\alpha)(m+1)\rceil$-th smallest of $v_1,\dots,v_m$ (and $+\infty$ if this rank exceeds $m$), and $\hat q^{-}_{\alpha}\{v_i\}$ is the $\lfloor\alpha(m+1)\rfloor$-th smallest (and $-\infty$ if this rank is below 1). The unnormalised variant TJ+ uses $\sigma\equiv 1$. The source model $f$ is **never** re-fitted; only the transfer step is (Fig. 1).

**Proposition 1.** *Suppose that $Z_1,\dots,Z_{m+1}$ are exchangeable. This holds, for example, when the standards and the future sample are drawn at random from the same target population. Suppose also that $\mathcal{T}$ treats its input standards symmetrically, and that $f$ and $\sigma$ do not depend on the target data. Then $\Pr\{y_{m+1}\in\hat C(\mathbf{x}^T_{m+1})\}\ge 1-2\alpha$.*

*Proof sketch.* Fix the source model and $\sigma$, and view $\mathcal{A}:\mathcal{D}\mapsto(\mu_{\mathcal{D}},\sigma_{\mathcal{D}})$ as a symmetric regression algorithm acting on the augmented standards. Define, for $i\neq j$, the score of point $i$ under the fit without $\{i,j\}$, $R_{ij}=\lvert y_i-\mu_{-ij}(\mathbf{x}_i)\rvert/\sigma_{-ij}(\mathbf{x}_i)$. If $y_{m+1}\notin\hat C$, then $R_{m+1,i}>R_{i,m+1}$ for at least $(1-\alpha)(m+1)$ indices $i$. Because the matrix $(R_{ij})$ is exchangeable under permutations of the $m+1$ points, the counting argument of Barber et al. [@barber2021, Thm. 1] bounds the probability of this event by $2\alpha$. A step-by-step proof, including the role of $\varepsilon>0$ and of the paired master spectrum, is given in Appendix A. $\square$

Three remarks clarify the scope of the guarantee.

- **No transfer step.** When there is no transfer ($\mu_{-i}=f$), TJ+ reduces to split conformal prediction that uses *all* $m$ standards for calibration, with exact $1-\alpha$ coverage.

- **Minimum number of standards.** Finite upper bounds require $\lceil(1-\alpha)(m+1)\rceil\le m$, i.e. $m\ge 9$ for α = 0.1 and $m\ge 19$ for α = 0.05. Splitting the standards in half (SCP-T-split, §2.4) needs twice as many.

- **Conditions are not automatic.** Exchangeability is a property of how the standards are chosen. Representative-design selection, such as Kennard–Stone [@kennard1969], is not covered by Proposition 1 and is examined empirically (§4.5). The bound is also marginal: it holds on average over the draw of standards and the test sample, not conditionally on a particular set of standards.


![**Fig. 1.** Transfer jackknife+ (TJ+N). Only the transfer step is re-fitted in the leave-one-standard-out loop; the source model and the difficulty function σ are fixed beforehand from source data.](figures/fig1_workflow.png){width=16.5cm}

## 2.4. Comparison methods

All methods share the same deployed point predictor $\mu_{\mathcal{D}}$ fitted on all $m$ standards. They differ only in the interval.

- **ASTM-PI** (classical parametric): $\mu(\mathbf{x})\pm t_{1-\alpha/2,\,n-A-1}\,\mathrm{SEC}\sqrt{1+h(\mathbf{x})}$, with the source standard error of calibration and the leverage $h$ of the transferred spectrum [@astm_e1655]. For ridge models, the leverage and degrees of freedom of the companion PLS model are used (an approximation).

- **SCP-S:** split conformal prediction with the pooled source residuals (out-of-fold residuals of the source training set plus source-calibration residuals), assuming no shift [@lei2018].

- **WCP-S:** weighted conformal prediction for covariate shift [@tibshirani2019]. Likelihood ratios come from a logistic domain classifier on the PLS scores of source spectra versus transferred, unlabelled target spectra; the test spectra themselves are included (transductive use).

- **Transport:** a regression analogue of transported conformal calibration [@doula2026]. Source-calibration spectra are mapped into the target space by a master→secondary PDS fitted on the standards, passed through the deployed pipeline, and their residuals calibrate a split-conformal quantile. It applies to paired transfers only. This baseline implements only the transport idea of [@doula2026]; the mismatch correction (TCC-KS) and weighting proposed there for classification were not adapted to regression here.

- **Gauss-LOO:** $\mu(\mathbf{x})\pm t_{1-\alpha/2,\,m-1}\,\mathrm{RMSE}_{\text{LOO}}$, using the leave-one-standard-out residuals. This mimics the common practice of validating a transfer by its prediction error on check samples.

- **SCP-T-split(-N):** the standards are split at random into halves. The first half fits the transfer and the second half calibrates (normalised) split conformal prediction. This is valid, at the cost of halving both sets.

- **MC-dropout** (CNN only): Gaussian intervals from 100 stochastic forward passes plus the source residual variance [@gal2016], followed by SBC.

**Ablations:**

- TJ-naive-N: full-fit centre with leave-one-out residual quantile, i.e. a jackknife without "+".

- TJ-insample-N: residuals from the transfer fitted on all standards, without leave-one-out.

- TCV+N: five-fold CV+.

- TJ+N[T²] and TJ+N[Q]: σ from a single diagnostic.

**Label-free variant (exploratory, LF-conv).** If the paired standards have no reference values, the target error decomposes as $y-\mu(\mathbf{x}^T)=e^S-d$. Here $e^S=y-f(\mathbf{x}^S)$ is the source error, estimated by the pooled source residuals $e_j$. The term $d=\mu(\mathbf{x}^T)-f(\mathbf{x}^S)$ is the transfer discrepancy, estimated from leave-one-out fits on the standards as $d_i=\mu_{-i}(\mathbf{x}^T_i)-f(\mathbf{x}^S_i)$. The interval is $\mu(\mathbf{x})+[\,Q_{\alpha/2},Q_{1-\alpha/2}\,]$ of $\{e_j-d_i\}_{j,i}$. It assumes independence of $e^S$ and $d$ and has no finite-sample guarantee.


# 3. Experimental

## 3.1. Data sets

Three public NIR data sets with documented domain shifts were used (Table 1; Fig. 2). No data were collected for this study.

**Corn** [@eigenvector_data]. Eighty corn samples were measured on three NIR spectrometers: m5 (master), mp5 and mp6. The range is 1100–2498 nm at 2 nm intervals (700 channels). Moisture, oil, protein and starch were determined by reference methods. Instrument shift: m5→mp5 and m5→mp6, plus mp5→m5 as a reverse-direction check.

**Pharmaceutical tablets (IDRC Shootout 2002)** [@eigenvector_data]. 655 tablets were measured on two spectrometers (600–1898 nm, 650 channels), with reference weight, hardness and active-ingredient assay. The distributed calibrate (155), validate (40) and test (460) partition was retained; the target pool is therefore the organisers' test set. Instrument 1 is the master.

**Mango dry matter** [@anderson2020; @mango_data]. The data comprise 11,691 NIR spectra (684–990 nm used, 103 channels) of intact mango fruit from four harvest seasons, with dry-matter content (DMC) as reference. As recommended by the data providers, replicate scans of the same fruit (2–6 scans; one subset scanned at three temperatures) must never be split between training and test sets. Replicates were therefore averaged per fruit (fruit identified by season, region, harvest date, maturity type, cultivar, population and DM value), giving 4,677 fruit (file version 1 of the data record). For the additional instrument-shift test (§4.6), the providers' extended file (record version 6) was used. Spectra flagged as outliers by the providers were excluded, and replicates were averaged per fruit and instrument. Season shift: seasons 1–3 (source) → season 4 (target, the providers' external validation season).

| Data set | Size | Shift | Range (channels) | Responses | Source train / source cal. / target pool | m |
|:--|--:|--:|--:|--:|--:|--:|
| Corn | 80 samples | m5 → mp5, mp6 (and mp5 → m5) | 1100–2498 nm (700) | moisture, oil, protein, starch (%) | 40 / 10 / 30 (random each repetition) | 10, 15, 20 |
| Tablets | 655 tablets | 1 → 2 | 600–1898 nm (650) | assay (mg), weight (mg), hardness | 155 / 40 / 460 (fixed) | 10, 20, 30, 50 |
| Mango | 4,677 fruit (3,952 source, 725 target) | seasons 1–3 → 4 | 684–990 nm (103) | dry matter (%) | 3,162 / 790 / 725 | 10, 20, 30, 50 |

Table: **Table 1.** Data sets and splitting protocol.


![**Fig. 2.** Data sets. Top: mean NIR spectra per instrument (corn, tablets) or per season group (mango). Bottom: reference-value distributions.](figures/fig2_datasets.png){width=16.5cm}


## 3.2. Protocol

The design, including all hyperparameters, seeds, metrics, tests and the validity criterion, was fixed before any target-domain result was computed. It is documented with a deviation log in the repository.

**Source models.** Preprocessing was chosen among none, SNV [@barnes1989], Savitzky–Golay [@savitzky1964] first derivative (window 11, order 2) and second derivative (window 13, order 2). The number of PLS latent variables [@wold2001] (≤15 for corn and tablets, ≤25 for mango) was chosen by 10-fold cross-validation (one-standard-error rule) on the source training data only. The out-of-fold residuals of this cross-validation were used to fit σ (Eq. (2)). For model-class generalisation, ridge regression (penalty by 10-fold CV, same preprocessing) and a small 1D-CNN were used. The CNN (mango only) takes SNV-corrected, channel-standardised spectra. It has two 1D convolutional layers (16 and 32 filters, kernel 7, the second with stride 2), a dense layer of 64 units, ReLU activations and dropout 0.2. It was trained once on seasons 1–3 (Adam, learning rate 10⁻³, weight decay 10⁻⁵, batch 128, at most 150 epochs, early stopping with patience 20 on a 10% split of the source training data).

**Splits.**

- *Corn:* in every repetition, 40 random samples were the source training set (master spectra), 10 the source calibration set and 30 the target pool. From the pool, *m* ∈ {10, 15, 20} random standards were drawn; the remaining 30−*m* samples were test samples.

- *Tablets:* the source training set was the instrument-1 calibrate set and the source calibration set the instrument-1 validate set. The target pool was the instrument-2 test set, with *m* ∈ {10, 20, 30, 50} standards and the remaining 460−*m* tablets as test samples.

- *Mango:* source fruit were split once (80/20, fixed seed) into source training and source calibration sets. The target pool was the 725 season-4 fruit, with *m* ∈ {10, 20, 30, 50}.

Standards were never used to train the source model, and test samples were never standards. Repetitions: 500 (corn, tablets) and 300 (mango) for the main experiment, 200 for the secondary experiments, with seeds fixed in advance.

**Transfer.** PDS (window 5, truncated pseudo-inverse with relative tolerance 0.01, with intercept; windows truncated at the spectral edges) [@wang1991; @bouveresse1996], DS, SBC and no transfer were applied. Spectral preprocessing was applied after spectral standardisation. The pre-registered primary pipelines were PDS for corn and tablets and SBC for mango; the other pipelines are reported as secondary results.

**Metrics.** For each repetition and method we recorded:

- empirical coverage on the test samples;

- mean and median interval width;

- the fraction of unbounded intervals;

- the Winkler interval score $\mathrm{IS}_\alpha=(u-l)+\tfrac{2}{\alpha}(l-y)_+ + \tfrac{2}{\alpha}(y-u)_+$, a proper scoring rule for central intervals [@gneiting2007];

- RMSEP of the point prediction;

- coverage within tertiles of σ(x) and of y (conditional coverage).

The primary miscoverage level was α = 0.10; α = 0.05 and 0.20 were sensitivity analyses.

**Statistics.** Mean coverage over repetitions is reported with a 95% percentile-bootstrap confidence interval (2000 resamples of repetitions). A method was pre-registered as *under-covering* in a scenario when the upper limit of this interval was below 1−α. Interval scores were compared only between methods that were not under-covering. Within each scenario, TJ+N was compared with every other method by a two-sided Wilcoxon signed-rank test on the per-repetition interval score, paired by repetition (identical splits). Holm's correction [@holm1979] was applied within the scenario, and the matched-pairs rank-biserial correlation was used as effect size. Unbounded intervals were assigned the worst rank. Across scenarios, methods were compared with a Friedman test on the scenario-level median interval score, followed by Holm-corrected pairwise Wilcoxon tests against TJ+N [@demsar2006]. Repetitions are independent random draws of the splits from fixed data sets, so inferences are conditional on the data sets. Every method is evaluated on identical standards and test samples in each repetition (paired design). Scenarios that share a data set are not independent (corn properties share samples; the *m* levels share splits). The Friedman ranks are therefore interpreted descriptively, and inferential statements rest on the within-scenario paired tests. Because the under-coverage flag is applied per scenario without multiplicity correction, it errs towards flagging, which works against the proposed method rather than in its favour.

**Robustness and sensitivity.** Robustness conditions were:

- Kennard–Stone selection of the standards from a random half of the target pool (non-exchangeable);

- Gaussian noise added to all target spectra (SNR 1000, 300, 100);

- a ±1-channel wavelength shift of the test spectra after the transfer was fitted (post-standardisation drift);

- halving the source training set.

Sensitivity analyses covered the PDS half-window (1, 2, 3, 5), the number of latent variables (±2) and α.

**Software and hardware.** All methods were implemented in Python (NumPy, SciPy, scikit-learn, PyTorch). Our PLS implementation agrees with scikit-learn to within 10⁻¹⁴. Unit tests include a Monte Carlo coverage check of TJ+. Computations ran on 4 CPU cores without a GPU. The full study is reproduced by a single command (`python run_all.py --mode full`).


# 4. Results and discussion

## 4.1. Point accuracy after transfer

Calibration transfer was necessary, but it was not equally beneficial everywhere (Table 2).

- **Corn:** applying the master models directly to mp5/mp6 spectra gave RMSEP values 2.6–5.2 times larger than after PDS with *m* = 20 standards.

- **Tablets:** PDS reduced the assay RMSEP from 6.43 mg (*m* = 10) to 4.65 mg (*m* = 50). The weight and hardness predictions were insensitive to the transfer.

- **Mango:** SBC did not improve on the uncorrected source model (RMSEP 1.06–1.15 vs 1.05 % DM), consistent with reports that models built over several seasons are already fairly robust [@anderson2020].

The transfer settings (PDS window 5, SBC slope and bias, LV numbers) were fixed in advance and were not tuned on target data. They are therefore not the most accurate possible: on corn, SBC gave lower RMSEP than the pre-registered PDS for all four properties, and a 3-channel PDS window was more accurate than the 5-channel one (§4.8). This does not affect the comparison of interval methods. All interval methods share the same point predictor within a pipeline, so the comparisons isolate the interval construction, and interval validity is reported for every pipeline (§4.3).

| Data set | Response | DS (m=10) | DS (m=20) | NONE (m=10) | NONE (m=20) | PDS (m=10) | PDS (m=20) | SBC (m=10) | SBC (m=20) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Corn | moisture | 0.308 | 0.238 | 1.598 | 1.592 | 0.349 | 0.304 | 0.251 | 0.229 |
| Corn | oil | 0.187 | 0.145 | 0.287 | 0.286 | 0.142 | 0.109 | 0.091 | 0.084 |
| Corn | protein | 0.439 | 0.316 | 0.794 | 0.794 | 0.233 | 0.194 | 0.168 | 0.158 |
| Corn | starch | 0.885 | 0.669 | 1.901 | 1.897 | 0.568 | 0.466 | 0.406 | 0.377 |
| Mango | dry matter | – | – | 1.052 | 1.052 | – | – | 1.155 | 1.095 |
| Tablets | assay | 9.216 | 5.998 | 7.351 | 7.347 | 6.434 | 5.101 | 7.797 | 7.298 |
| Tablets | hardness | 1.011 | 1.014 | 1.055 | 1.054 | 1.021 | 1.022 | 1.074 | 0.998 |
| Tablets | weight | 4.138 | 4.165 | 4.456 | 4.456 | 4.194 | 4.201 | 4.212 | 3.926 |

Table: **Table 2.** Point accuracy (mean RMSEP over repetitions; corn averaged over mp5 and mp6) of the deployed predictor for each transfer pipeline and number of standards m. NONE = source model applied without transfer.


## 4.2. Conventional intervals after transfer (RQ1)

Source-calibrated intervals under-covered when the transfer added substantial error that the source calibration had not seen (Fig. 3; Table 3; compare Table 2).

- **Corn:** the mean coverage of nominal 90% intervals was 0.03–0.74 for ASTM-PI, SCP-S and WCP-S, which were flagged as under-covering in 72 of 72 scenario × method cells.

- **Mango:** coverage was 0.71–0.76 (12 of 12 cells under-covering).

- **Tablets:** the picture was mixed (0.81–0.95; 11 of 36 cells under-covering). Severe under-coverage occurred for the assay with *m* = 10 (all three methods, coverage 0.81–0.85), where PDS fitted on ten standards inflated the error. For weight, SCP-S and WCP-S under-covered slightly but systematically at every *m* (0.894–0.895), while hardness intervals were valid.

The failure is not an artefact of the in-sample calibration error used by ASTM-PI: SCP-S, which uses cross-validated (out-of-fold) source residuals, under-covered almost as severely. Weighting the source residuals for covariate shift (WCP-S) did not repair coverage either, and it produced unbounded intervals in 59% of corn repetitions. When the domains are almost perfectly separable, the estimated likelihood ratios degenerate. More fundamentally, an instrument change alters the conditional relation between spectrum and property, which violates the covariate-shift assumption. The transport baseline, which maps source-calibration spectra into the secondary-instrument space with a master→secondary PDS, recovered part of the coverage on corn (mean coverage 0.75, range 0.29–0.92). It still under-covered in 14 of 24 scenarios, because the transported residuals inherit the source error distribution and only approximate the transfer error.

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

Table: **Table 3.** Coverage of nominal 90% intervals (α = 0.10) for the primary transfer pipelines (corn and tablets: PDS; mango: SBC). Coverage: mean over scenarios of the mean per-repetition coverage, with the range over scenarios in parentheses. Under: scenarios flagged as under-covering (upper limit of the 95% bootstrap CI < 0.90) / number of scenarios. Friedman rank: mean rank of the scenario median interval score over the 40 scenarios (1 = best; only methods available in all scenarios).


![**Fig. 3.** Mean empirical coverage of nominal 90% intervals versus the number of transfer standards *m* (primary pipelines; 500 repetitions for corn and tablets, 300 for mango). Markers show the mean over scenarios (properties and target instruments); vertical lines show the range over scenarios. Hollow markers: the method returned unbounded intervals in more than half of the repetitions (coverage trivially 1). Horizontal line: nominal level.](figures/fig3_coverage_vs_m.png){width=16.5cm}


## 4.3. Validity and efficiency of the transfer jackknife+ (RQ2)

TJ+N was not flagged as under-covering in any of the 40 primary scenarios. Given the precision of the coverage estimates (median half-width of the 95% CI: corn ±0.008, mango ±0.007, tablets ±0.005), this means that no scenario was significantly below nominal at that resolution. Its mean coverage was 0.922 (range over scenarios 0.898–0.959) at α = 0.10, and the same held at α = 0.05 and 0.20 (0 under-covering scenarios over all three levels; Table 4). Coverage exceeded the nominal level most clearly for *m* = 10–15. This is expected from the discrete rank $\lceil (1-\alpha)(m+1)\rceil$: with *m* = 10 the upper bound is the largest of the ten leave-one-out bounds. In practice, this conservativeness means somewhat wider intervals than necessary when few standards are available; it decreases as *m* grows (Fig. 3).

**Against the valid split-standards baseline.** Halving the standards made SCP-T-split unbounded in every repetition for *m* ≤ 15 at α = 0.10 (20 of 40 scenarios, all with m ≤ 15). Where both methods gave bounded intervals, TJ+N had a lower interval score in 20 of 20 scenarios (paired Wilcoxon, Holm-adjusted *p* < 0.05), with a median rank-biserial correlation of -0.52. Reusing every standard for both transfer and calibration is therefore the main practical gain.

Interval widths relative to the RMSEP of the deployed predictor are shown in Fig. 4.

![**Fig. 4.** Median interval width relative to the RMSEP of the deployed predictor for the methods that were not under-covering (unbounded settings omitted).](figures/fig4_width_vs_m.png){width=16.5cm}

**Against Gaussian leave-one-standard-out intervals.** The simple Gauss-LOO interval was a strong competitor at α = 0.10.

- It was never flagged as under-covering at this level.

- It had the best mean rank of interval score across scenarios (Fig. S2; mean ranks Gauss-LOO 2.17, TJ+N 2.52, TJ+ 3.12; Friedman χ² = 145.5, nominal *p* = 3.6×10^−^28, which overstates the evidence because scenarios are dependent).

- Across scenarios, it did not differ significantly from TJ+N after Holm correction (*p* = 0.11).

- Per scenario (Holm-adjusted *p* < 0.05), Gauss-LOO had the lower interval score in 14 of 24 corn scenarios. On tablets and mango, TJ+N was better in 9 and Gauss-LOO in 5 of 16 scenarios.

Its validity, however, depends on approximately Gaussian errors. At α = 0.05 it under-covered in 14 of 40 scenarios, and at α = 0.20 in 2, whereas TJ+N and TJ+ never did. The price of distribution-free validity at α = 0.05 is that TJ+N needs *m* ≥ 19 standards. With fewer standards it returns unbounded intervals rather than over-confident ones.

**Normalised Gaussian competitor (E9).** One might expect a heteroscedastic Gaussian interval using the same difficulty function to combine the efficiency of Gauss-LOO with the adaptivity of TJ+N: μ(x) ± t₁₋α/₂,ₘ₋₁ · RMS(Rᵢ) · σ(x), with Rᵢ from Eq. (3) (Gauss-LOO-N). We tested this in an additional experiment specified during review (200 repetitions; all primary pipelines and the instrument shift of E8; three α levels; Table S8).

- Under-covering scenarios over all α levels: TJ+N 0/192, Gauss-LOO 18/192, Gauss-LOO-N 14/192.

- At α = 0.05: 0/64, 16/64 and 8/64, respectively.

- At α = 0.10, Gauss-LOO-N had a lower median interval score than TJ+N in 59 of 64 scenarios (median score ratio 0.970).

The normalised Gaussian interval was therefore slightly more efficient, by about 3% in interval score, but it under-covered in several scenarios, mostly at 95%. TJ+N trades this small loss of efficiency for validity without distributional assumptions. Where a few percent of interval width matter more than a coverage guarantee, Gauss-LOO-N is a defensible pragmatic choice, provided its coverage is checked.
 Over all four transfer pipelines (PDS, DS, SBC and no transfer) and the three data sets, TJ+N under-covered in 0 of 152 pipeline × scenario combinations at α = 0.10. The corresponding numbers were 12 of 152 for Gauss-LOO, 120 of 152 for ASTM-PI and 129 of 152 for SCP-S (Table S2).

| Method | α = 0.05 (nominal 0.95) | α = 0.1 (nominal 0.90) | α = 0.2 (nominal 0.80) |
|:--|--:|--:|--:|
| TJ+N | 0/40 (50%) | 0/40 (0%) | 0/40 (0%) |
| TJ+ | 0/40 (50%) | 0/40 (0%) | 0/40 (0%) |
| SCP-T-split-N | 0/40 (90%) | 0/40 (50%) | 0/40 (0%) |
| Gauss-LOO | 14/40 (0%) | 0/40 (0%) | 2/40 (0%) |
| ASTM-PI | 29/40 (0%) | 29/40 (0%) | 29/40 (0%) |
| SCP-S | 29/40 (0%) | 33/40 (0%) | 34/40 (0%) |
| WCP-S | 29/40 (69%) | 33/40 (49%) | 33/40 (30%) |
| LF-conv | 25/36 (0%) | 20/36 (0%) | 13/36 (0%) |

Table: **Table 4.** Validity across miscoverage levels: number of under-covering scenarios / scenarios, with the mean percentage of repetitions returning unbounded intervals in parentheses (primary pipelines).


## 4.4. Ablation (RQ3)

Table 5 and Fig. 5 isolate the components.

- **Leave-one-out re-fitting is essential.** With residuals from the transfer fitted on all standards (TJ-insample-N), the intervals under-covered in 14 of 40 scenarios. The effect was largest for SBC on mango (coverage 0.83–0.89), because a slope and bias fitted to the same standards absorb part of their own residuals.

- **K-fold CV+.** Five-fold CV+ (TCV+N) needs only five refits but was more conservative, with a higher interval score than TJ+N in 32 of 40 scenarios.

- **The "+" construction.** Centring the interval on the full-fit prediction (TJ-naive-N) gave equal or slightly lower coverage than TJ+N. It is a reasonable practical alternative, but it carries no finite-sample guarantee.

- **Over all pipelines and α levels (E1 and E8 together):**

  - TJ-naive-N under-covered in 3 of 528 scenario cells, against 0 of 528 for TJ+N and 0 of 528 for TCV+N.

  - Residuals without leave-one-out re-fitting (TJ-insample-N) under-covered in 199 of 528.

  - Gauss-LOO under-covered in 77 of 528.

- **Difficulty normalisation.** Normalisation improved efficiency in most scenarios.

  - TJ+N had a significantly lower interval score than unnormalised TJ+ in 24 of 40 scenarios, and a higher one in 5.

  - It also rebalanced conditional coverage. Unnormalised intervals under-covered the most difficult third of test samples (coverage in the highest-σ tertile 0.878) and over-covered the easiest third (0.957). With TJ+N these became 0.933 and 0.904 (Fig. 6).

  - On corn, the Q term over-corrected slightly: the highest-σ tertile was over-covered. A T²-only difficulty function was more balanced there. Because this variant was identified after the results were seen, we report it as exploratory and keep the pre-registered TJ+N as the primary method.

  - The Q term was most valuable when the test spectra drifted after standardisation (§4.5).

| Variant | Corn cov. | Corn under | Corn rel. IS | Tablets cov. | Tablets under | Tablets rel. IS | Mango cov. | Mango under | Mango rel. IS | Cov. low/high σ tertile |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| TJ+N | 0.931 | 0/24 | 1.000 | 0.910 | 0/12 | 1.000 | 0.904 | 0/4 | 1.000 | 0.904 / 0.933 |
| TJ+ | 0.933 | 0/24 | 1.019 | 0.911 | 0/12 | 1.062 | 0.904 | 0/4 | 1.016 | 0.957 / 0.878 |
| TCV+N | 0.942 | 0/24 | 1.066 | 0.917 | 0/12 | 1.000 | 0.908 | 0/4 | 1.009 | 0.916 / 0.941 |
| TJ-naive-N | 0.919 | 0/24 | 0.961 | 0.905 | 0/12 | 0.999 | 0.903 | 0/4 | 0.996 | 0.894 / 0.924 |
| TJ-insample-N | 0.897 | 10/24 | 0.935 | 0.912 | 0/12 | 1.000 | 0.863 | 4/4 | 0.992 | 0.878 / 0.909 |
| TJ+N[T2] | 0.931 | 0/24 | 0.976 | 0.911 | 0/12 | 0.999 | 0.904 | 0/4 | 1.005 | 0.922 / 0.916 |
| TJ+N[Q] | 0.931 | 0/24 | 1.020 | 0.911 | 0/12 | 1.011 | 0.904 | 0/4 | 1.006 | 0.914 / 0.924 |

Table: **Table 5.** Ablation of TJ+N (α = 0.10, primary pipelines). Rel. IS: median over scenarios of the scenario median interval score relative to TJ+N (< 1 = narrower/better). Cov. low/high σ tertile: mean coverage in the lowest and highest tertile of σ(x) over all scenarios.


![**Fig. 5.** Ablation of TJ+N. Left: mean coverage. Right: median interval score relative to TJ+N (finite intervals only).](figures/fig5_ablation.png){width=16.5cm}

![**Fig. 6.** Conditional coverage within tertiles of the difficulty σ(x) of the test spectra (primary pipelines, α = 0.10).](figures/fig7_conditional_coverage.png){width=16.5cm}


## 4.5. Robustness (RQ4)

Apart from post-standardisation drift, TJ+N was not flagged as under-covering in any of the 30 robustness scenarios (Fig. 7; Supplementary Table S9). These were Kennard–Stone selection of the standards, added noise at SNR 1000–100, and halving the source data.

**Kennard–Stone standards.** Selecting the standards by Kennard–Stone, which is outside the scope of Proposition 1, made TJ+N conservative (coverage 0.93–0.96). The selected standards span the extremes of the target population, so their leave-one-out residuals are, if anything, larger than those of typical samples. This empirical result is reassuring, but it is not a guarantee. Other non-random selection schemes, for example standards concentrated in a narrow concentration range, could bias coverage in either direction.

**Post-standardisation wavelength drift.** The decisive failure mode was a one-channel wavelength shift of the test spectra after the transfer had been fitted. This simulates instrument drift between standardisation and routine use, and it breaks exchangeability between standards and test samples. No method remained valid.

- Tablets: TJ+N coverage was 0.04–0.07; Gauss-LOO 0.02–0.04.

- Corn: TJ+N 0.60–0.94, against 0.05–0.45 for unnormalised TJ+ and 0.02–0.29 for Gauss-LOO.

- Mango: TJ+N 0.73–0.97, against 0.08–0.22 for TJ+ and 0.07–0.21 for Gauss-LOO.

On corn and mango, the Q residual of the shifted spectra inflated σ(x) and recovered a large part of the coverage. On tablets, where the assay information is concentrated in a few sharp bands, it did not. A one-channel shift is a large drift. In an additional test with a sub-channel shift of ±0.25 channel (linear interpolation; specified during review; Supplementary Table S10), coverage was:

- TJ+N: corn 0.84–0.96, tablets 0.59–0.62, mango 0.86–0.96 (4/12 scenarios under-covering);

- Gauss-LOO: corn 0.62–0.71, tablets 0.66–0.66, mango 0.78–0.83 (12/12);

- ASTM-PI: corn 0.02–0.31, tablets 0.66–0.66, mango 0.62–0.68.

TJ+N degraded least on corn and mango, but even this small drift invalidated all methods for the tablet assay. Drift after standardisation must therefore be detected (for example by monitoring Q) and corrected by re-standardisation. No interval method compensates for it reliably.


![**Fig. 7.** Robustness of interval coverage (α = 0.10): Kennard–Stone selection of standards, spectral noise added to all target spectra, a ±1-channel wavelength shift of the test spectra after standardisation, and halved source training data.](figures/fig6_robustness.png){width=16.5cm}



## 4.6. Generalisation across pipelines, directions, model classes and instruments (RQ5)

The conclusions did not depend on the primary pipeline, the transfer direction or the model class (Table 6).

- **Transfer pipelines.** With DS, SBC or no transfer instead of PDS, TJ+N and TJ+ were never flagged as under-covering (§4.3).

- **Reverse direction.** Transferring from mp5 to m5 gave the same picture: no under-coverage for TJ+N, and under-coverage of the source-calibrated intervals.

- **Ridge regression.** With ridge source models, TJ+N was valid on all three data sets.

- **1D-CNN on mango.** The CNN (110,369 parameters, early stopping after 101 epochs, 36 s on a CPU) reached RMSEP 1.22 % DM after SBC. On top of it:

  - TJ+N gave coverage 0.910 with the lowest interval score (5.24).

  - Gauss-LOO under-covered in 2/4 scenarios (coverage 0.894; score 5.42).

  - MC-dropout intervals [@gal2016], a common deep-learning uncertainty estimate for spectra [@maxime2025], under-covered in 4/4 scenarios (coverage 0.807), presumably because dropout variance captures model uncertainty but not the systematic error introduced by the season shift.

Over all generalisation settings, TJ+N under-covered in 0 of 22 scenarios.

**Independent instrument shift (mango, E8).** Prompted by the review process, we added a test that was not part of the pre-registered design: transfer between handheld spectrometers on intact fruit, using the data providers' extended data set with paired spectra of the same fruit on several instruments [@mango_data_v6]. The design was fixed before any result was computed:

- source instrument 15006;

- the three target instruments with most shared fruit;

- PDS and SBC pipelines;

- *m* = 10–50 standards, 200 repetitions.

The results reproduced the main findings (Table 7).

- ASTM-PI and SCP-S under-covered in every scenario: coverage 0.20–0.51 after PDS (24/24 scenarios) and 0.73–0.81 after SBC (24/24). WCP-S under-covered after PDS (0.15–0.47). After SBC it returned unbounded intervals in 100% of repetitions: valid, but uninformative.

- TJ+N was valid: mean coverage 0.931 (PDS) and 0.906 (SBC). It was never flagged at any α (0/72 under-covering scenarios), whereas Gauss-LOO was flagged in 4/72.

- PDS proved a poor transfer for these instruments (RMSEP 2.03–7.40 % DM, against 1.06–1.22 % with SBC). TJ+N made this visible through wide intervals (median width 11.1 vs 4.0 % DM), whereas the source-calibrated intervals remained narrow and missed most samples. Valid intervals are thus also a diagnostic of transfer quality.



| Setting | TJ+N | TJ+ | Gauss-LOO | SCP-T-split-N | ASTM-PI | SCP-S | WCP-S | MC-dropout |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Corn mp5→m5, PLS, PDS | 0.931 (0/12); 1.11 | 0.932 (0/12); 1.21 | 0.905 (0/12); 1.17 | 0.971 (0/12); inf | 0.657 (12/12); 1.34 | 0.757 (12/12); 1.25 | 0.800 (12/12); 1.53 | – |
| Corn m5→mp5, ridge, PDS | 0.943 (0/4); 1.21 | 0.953 (0/4); 1.17 | 0.904 (0/4); 1.06 | 1.000 (0/4); inf | 0.057 (4/4); 3.6 | 0.416 (4/4); 1.98 | 0.518 (4/4); inf | – |
| Tablets assay, ridge, PDS | 0.916 (0/1); 21.8 | 0.915 (0/1); 21.9 | 0.914 (0/1); 22 | 0.918 (0/1); 26.4 | 0.905 (0/1); 20.7 | 0.874 (1/1); 20.9 | 0.888 (1/1); 21.8 | – |
| Mango, ridge, SBC | 0.898 (0/1); 4.5 | 0.899 (0/1); 4.57 | 0.899 (0/1); 4.52 | 0.902 (0/1); 4.97 | 0.729 (1/1); 5.1 | 0.716 (1/1); 5.2 | 0.742 (1/1); inf | – |
| Mango, 1D-CNN, SBC | 0.910 (0/4); 5.24 | 0.909 (0/4); 5.51 | 0.894 (2/4); 5.42 | 0.945 (0/4); 5.59 | 0.714 (4/4); 6.48 | 0.693 (4/4); 6.71 | 0.780 (4/4); inf | 0.807 (4/4); 5.66 |

Table: **Table 6.** Generalisation (E5; α = 0.10). Each cell: mean coverage (under-covering / scenarios); median interval score (lower is better).


| Pipeline | Method | Coverage (range) | Under | Unbounded (% reps) | Median width (% DM) | RMSEP (% DM) |
|:--|--:|--:|--:|--:|--:|--:|
| PDS | TJ+N | 0.931 (0.91–0.97) | 0/12 | 0 | 11.05 | 4.03 |
| PDS | TJ+ | 0.929 (0.90–0.97) | 0/12 | 0 | 12.79 | 4.03 |
| PDS | SCP-T-split-N | 0.943 (0.91–1.00) | 0/12 | 25 | 11.15 | 4.03 |
| PDS | Gauss-LOO | 0.916 (0.90–0.93) | 0/12 | 0 | 12.13 | 4.03 |
| PDS | ASTM-PI | 0.355 (0.22–0.51) | 12/12 | 0 | 2.71 | 4.03 |
| PDS | SCP-S | 0.342 (0.20–0.50) | 12/12 | 0 | 2.60 | 4.03 |
| PDS | WCP-S | 0.292 (0.15–0.47) | 12/12 | 25 | 2.24 | 4.03 |
| PDS | Transport | 0.978 (0.95–0.99) | 0/12 | 0 | 24.63 | 4.03 |
| PDS | LF-conv | 0.887 (0.86–0.91) | 6/12 | 0 | 11.83 | 4.03 |
| SBC | TJ+N | 0.906 (0.90–0.92) | 0/12 | 0 | 4.00 | 1.14 |
| SBC | TJ+ | 0.906 (0.90–0.92) | 0/12 | 0 | 3.87 | 1.14 |
| SBC | SCP-T-split-N | 0.941 (0.90–1.00) | 0/12 | 25 | 4.56 | 1.14 |
| SBC | Gauss-LOO | 0.900 (0.89–0.91) | 0/12 | 0 | 3.85 | 1.14 |
| SBC | ASTM-PI | 0.781 (0.74–0.81) | 12/12 | 0 | 2.66 | 1.14 |
| SBC | SCP-S | 0.762 (0.73–0.80) | 12/12 | 0 | 2.60 | 1.14 |
| SBC | WCP-S | 1.000 (1.00–1.00) | 0/12 | 100 | 4.54 | 1.14 |

Table: **Table 7.** Independent instrument shift (E8): mango dry matter, source instrument 15006, three target instruments × four values of m (12 scenarios per pipeline; α = 0.10; 200 repetitions).


## 4.7. Label-free variant (exploratory)

The label-free LF-conv interval uses only paired, unlabelled standards. It was not reliable: it under-covered in 20 of 36 paired scenarios at α = 0.10. Its independence assumption between source error and transfer discrepancy is evidently too strong. Reference values for at least a random subset of standards remain necessary for valid intervals.

## 4.8. Sensitivity to transfer and model settings

Changing the PDS window (3, 7 or 11 channels instead of the pre-registered 5) or the number of latent variables (±2) changed point accuracy considerably. For example, the mean corn RMSEP with *m* = 15 was 0.281 with the pre-registered 5-channel window and 0.237 (3 channels), 0.348 (7 channels), 0.503 (11 channels) with the other windows. The pre-registered window was thus not the most accurate choice for corn; it was nevertheless kept, since it was fixed before any target data were analysed. Interval validity was unaffected: TJ+N under-covered in 0 of 27 sensitivity scenarios (coverage 0.898–0.972; Table S3). The source-calibrated intervals under-covered in 48 of 54 cases. Their validity also depended on the setting. For example, with an 11-channel PDS window the tablet-assay coverage of ASTM-PI and SCP-S fell to 0.87 and 0.84. Because TJ+ calibrates on the deployed pipeline itself, poorer transfer settings are reflected in wider, but still valid, intervals.

## 4.9. Error analysis

Misses of the conventional intervals were associated with spectra that the source model reconstructed poorly after transfer (Fig. 8). On corn, the miss rate of ASTM-PI was 0.76 in the lowest and 0.86 in the highest Q-residual quintile of the test spectra. Gauss-LOO, which uses one width for all samples, was valid on average but missed more often in the highest Q quintile: 0.12 (corn), 0.17 (tablets) and 0.13 (mango), against 0.04, 0.10 and 0.10 for TJ+N, for a nominal 0.10. The difficulty normalisation thus moves coverage to where it is needed. A large Q residual after transfer is in any case a useful warning flag for an individual prediction.

Coverage is a property of the procedure, not of one realised set of standards. Across repetitions, the 5th percentile of per-repetition coverage of TJ+N at *m* = 20 was 0.70–0.81 (Fig. 9). An unlucky draw of 20 standards can therefore give a markedly lower realised coverage on a given test batch. This variability, intrinsic to marginal guarantees with small calibration sets, shrinks as *m* grows (0.82–0.84 at *m* = 50 for tablets and mango). Put differently, the share of repetitions whose realised coverage on the test set fell below 0.80 was corn m = 20: 8%; tablets m = 20: 6%; tablets m = 50: 2%; mango m = 20: 10%; mango m = 50: 2%. Users who need a guarantee for their particular set of standards (training-conditional coverage) should use more standards or a more conservative α.

![**Fig. 8.** Miss rate (1 − coverage) by Q-residual quintile of the test spectra (first 100 repetitions; corn m = 15, tablets assay and mango m = 20). Horizontal line: nominal miss rate 0.10.](figures/fig8_error_analysis.png){width=16.5cm}

![**Fig. 9.** Distribution over repetitions of the realised test-set coverage for one scenario per data set (violins; dots = mean). The guarantee concerns the mean; individual draws of standards vary.](figures/fig10_coverage_distribution.png){width=16.5cm}

## 4.10. Computational cost (RQ6)

TJ+N requires *m* leave-one-out refits of the transfer step (plus five refits for the optional CV+ comparison included in our timing). On a single CPU core, one transfer fit with prediction took 4.6 ms (corn, *m* = 20), 24.3 ms (tablets, *m* = 50, 410 test spectra) and 0.4 ms (mango SBC). The complete TJ+N interval computation took 0.15 s, 2.79 s and 0.06 s, respectively, with peak memory below 15 MB (Fig. S3). The source model is never re-fitted. Measured over *m* = 10–50, the cost of TJ+N grew approximately linearly with the number of standards (corn: 0.10 s at m = 10 to 0.15 s at m = 20; tablets: 0.80 s at m = 10 to 2.56 s at m = 50; mango: 0.02 s at m = 10 to 0.06 s at m = 50; Supplementary Table S7). These timings include the five CV+ refits and are thus upper bounds.

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

5. Flag predictions with large Q residuals after transfer. Re-check coverage periodically on a few fresh reference samples, because drift after standardisation invalidates any interval calibrated at standardisation time.


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

   - Probabilistic alternatives that model the transfer jointly (for example Gaussian-process or Bayesian PLS models) were not compared; their intervals depend on model assumptions that would themselves need validation after transfer.

   - Very high confidence levels are expensive: at α = 0.01, a bounded TJ+ interval requires *m* ≥ 99 standards.

5. **A simple competitor.** Gaussian intervals built from leave-one-standard-out residuals (Gauss-LOO) were often as efficient as TJ+N, and in some scenarios more so (§4.3). The advantage of TJ+N is its distribution-free guarantee and its behaviour under heavy-tailed or heteroscedastic errors, not uniformly narrower intervals.

6. **Difficulty normalisation.** The pre-registered σ(x), built from T² and Q, improved efficiency and conditional coverage in most scenarios, but not uniformly. On corn it over-covered difficult samples, and a T²-only variant was more balanced there. That variant was identified *post hoc* and needs confirmation on independent data.

7. **Drift after standardisation.** A wavelength shift of the routine spectra after the transfer had been fitted invalidated the intervals of all methods, including TJ+N. This happened for a one-channel shift and, for some responses, already for a quarter-channel shift (§4.5). The guarantee presupposes a stable target instrument between standardisation and use.

# 6. Conclusions

Prediction intervals for calibrations moved to a new instrument or season should not be calibrated on source-domain data. In our benchmark, the classical parametric interval, source split conformal prediction and covariate-shift-weighted conformal prediction all under-covered after transfer, sometimes severely.

The transfer jackknife+ re-fits only the transfer step in a leave-one-standard-out loop. It thereby reuses the transfer standards that calibration transfer already requires, and gives distribution-free intervals with a finite-sample guarantee. Its intervals were valid across instruments, properties, shift types and model classes whenever its assumptions held. They were bounded with far fewer standards than the valid alternative that splits the standards. The extra cost is *m* refits of the transfer step, which took seconds or less in all cases studied. No interval method, TJ+N included, protects against drift that occurs after standardisation; it must be monitored.

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


# Appendix A. Proof of Proposition 1 {.unnumbered}

**Setting.** Let $Z_1,\dots,Z_m$ be the transfer standards and $Z_{m+1}=(\mathbf{x}^T_{m+1},\mathbf{x}^S_{m+1},y_{m+1})$ the future sample. Its master spectrum $\mathbf{x}^S_{m+1}$ is never used by the procedure; it enters only the argument, as the spectrum the sample *would* give on the master instrument. For any index set $S\subseteq\{1,\dots,m+1\}$, let $\mu_S$ and $\sigma_S$ be the deployed predictor (Eq. (1)) and the difficulty function obtained by applying the transfer algorithm $\mathcal{T}$ to $\{Z_k:k\in S\}$. The source model $f$ and the function $\sigma$ of Eq. (2) are fixed beforehand from source data. $\mathcal{T}$ is *symmetric*, i.e. invariant to the order of its inputs; this holds for PDS, DS and SBC, which are least-squares fits on the set of standards. Because $\sigma\ge\varepsilon>0$, all normalised scores are well defined.

**Step 1 (scores).** For $i\neq j$, write $-ij$ for the set $\{1,\dots,m+1\}\setminus\{i,j\}$ and define
$$R_{ij}=\frac{\lvert y_i-\mu_{-ij}(\mathbf{x}^T_i)\rvert}{\sigma_{-ij}(\mathbf{x}^T_i)}.$$
The fit that excludes $i$ and $m+1$ is exactly the leave-one-out fit $\mu_{-i}$ of Eq. (3), computed from the $m$ standards without standard $i$. Hence $R_i=R_{i,m+1}$, and for the future sample $\lvert y_{m+1}-\mu_{-i}(\mathbf{x}^T_{m+1})\rvert/\sigma_{-i}(\mathbf{x}^T_{m+1})=R_{m+1,i}$.

**Step 2 (miscoverage implies many lost comparisons).** Let $U_i=\mu_{-i}(\mathbf{x})+\sigma_{-i}(\mathbf{x})R_i$ and $L_i=\mu_{-i}(\mathbf{x})-\sigma_{-i}(\mathbf{x})R_i$ with $\mathbf{x}=\mathbf{x}^T_{m+1}$.

- *Upper tail.* If $y_{m+1}$ exceeds the upper bound in Eq. (4), the $\lceil(1-\alpha)(m+1)\rceil$-th smallest $U_i$, then $y_{m+1}>U_i$ for at least $(1-\alpha)(m+1)$ indices $i$.

- *Lower tail.* If $y_{m+1}$ is below the lower bound, the $k$-th smallest $L_i$ with $k=\lfloor\alpha(m+1)\rfloor$, then $y_{m+1}<L_i$ for at least $m-k+1\ge(1-\alpha)(m+1)$ indices.

In both cases $\lvert y_{m+1}-\mu_{-i}(\mathbf{x})\rvert/\sigma_{-i}(\mathbf{x})>R_i$, i.e. $R_{m+1,i}>R_{i,m+1}$, for at least $(1-\alpha)(m+1)$ indices. Therefore
$$\{y_{m+1}\notin\hat C(\mathbf{x}^T_{m+1})\}\subseteq\Big\{\textstyle\sum_{i\le m}\mathbf{1}[R_{m+1,i}>R_{i,m+1}]\ge(1-\alpha)(m+1)\Big\}.$$

**Step 3 (tournament bound).** Call a point $j\in\{1,\dots,m+1\}$ *strange* if $\sum_{i\neq j}\mathbf{1}[R_{ji}>R_{ij}]\ge(1-\alpha)(m+1)$. By the counting lemma in the proof of Theorem 1 of Barber et al. [@barber2021], at most $2\alpha(m+1)$ points can be strange, for any realisation of the scores.

**Step 4 (exchangeability).** The $Z_k$ are exchangeable and $\mathcal{T}$ is symmetric. Hence the joint law of the matrix $(R_{ij})$ is invariant under a simultaneous permutation of rows and columns, and every point is equally likely to be strange. Thus $\Pr\{Z_{m+1}\text{ strange}\}=\mathbb{E}[\#\text{strange}]/(m+1)\le 2\alpha$. Combining with Step 2 gives $\Pr\{y_{m+1}\notin\hat C\}\le 2\alpha$. $\square$

**Remarks.**

- The normalisation enters only through the definition of the scores. Steps 2–4 hold for any score of the form $\lvert y_i-\mu_{-ij}(\mathbf{x}_i)\rvert/\sigma_{-ij}(\mathbf{x}_i)$ with $\sigma>0$, provided the pair $(\mu,\sigma)$ is produced by a symmetric algorithm.

- Fitting the transfer on all $m$ standards and reusing it to compute residuals (TJ-insample) breaks Step 1: the residual of standard $i$ is then computed with a fit that has seen $i$, and the exchangeability with the future sample's residual is lost. The resulting under-coverage is observed in §4.4.

- Ties between scores have probability zero for continuous data; with ties, the strict inequalities in Step 2 make the interval only more conservative.

- If the standards are chosen by a data-dependent design such as Kennard–Stone, they are no longer exchangeable with a random future sample, and Step 4 does not apply.
