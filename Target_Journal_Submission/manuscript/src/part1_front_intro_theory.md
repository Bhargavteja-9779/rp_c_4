---
title: "Valid prediction intervals for transferred NIR calibrations: reusing the transfer standards with a leave-one-standard-out jackknife+"
---

**Authors:** [Author 1]^a^, [Author 2]^a,\*^

^a^ [Affiliation, address, country]

\* Corresponding author: [e-mail address]

# Abstract {.unnumbered}

**Background:** Calibrations built on one spectrometer or season are routinely transferred to others using a few transfer standards. Whether the prediction intervals of a transferred calibration keep their nominal coverage has not been studied systematically, and splitting the scarce standards between transfer and uncertainty calibration wastes them.

**Results:** We propose a transfer jackknife+ (TJ+N). Each standard is left out in turn and the transfer step (e.g., piecewise direct standardisation) is re-fitted on the others. The leave-one-out residuals, normalised by a source-learned function of Hotelling T² and Q residuals, define distribution-free intervals with coverage ≥ 1−2α for exchangeable standards. On three public NIR data sets (instrument and season shift; {{n_scen_main}} pre-registered scenarios, up to 500 repetitions each), source-calibrated intervals under-covered after transfer, with coverage as low as {{min_cov_source}} for a nominal 0.90. TJ+N had a mean coverage of {{tjn_cov_mean}} and was never flagged as under-covering, at α = 0.05, 0.10 or 0.20, under four transfer pipelines, or with PLS, ridge and 1D-CNN models, including an independent transfer between handheld fruit spectrometers. Splitting the standards gave unbounded intervals for *m* ≤ 15. Gaussian intervals from leave-one-out residuals were similarly efficient at 90% but under-covered in {{gauss_under_005}} of 40 scenarios at 95%. All methods failed under wavelength drift occurring after standardisation.

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
