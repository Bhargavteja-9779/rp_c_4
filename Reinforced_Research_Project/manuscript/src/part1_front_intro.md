---
title: "Trustworthy prediction intervals after moving an NIR calibration to a new instrument or season: how many reference samples, and from how many batches?"
---

**Authors:** [Author 1]^a^, [Author 2]^a,\*^

^a^ [Affiliation, address, country]

\* Corresponding author: [e-mail address]

# Abstract {.unnumbered}

**Background:** When a near-infrared (NIR) calibration is moved to a new instrument or harvest season, a few reference samples are measured to adapt it. Results are then reported, and products accepted or rejected, with an uncertainty range. Whether that range still holds after the move, and what the reference samples must look like for it to hold, is rarely checked.

**Results:** On three public data sets (corn, tablets, mango), ranges taken from the original calibration lost most of their coverage after transfer (as low as {{min_cov_source}} for nominal 90%). Re-fitting the transfer with each reference sample left out in turn gave valid intervals in all {{n_scen_main}} planned scenarios with randomly chosen samples, at no extra cost. How the samples were collected mattered more than how many. With 20 reference fruit from only two consignments, intervals were too narrow for fruit from other consignments in {{r_k2_tjn_under}} instrument and season settings (coverage {{r_k2_tjn_cov}}), and the usual Gaussian, split-sample and random-effects intervals failed likewise. Spreading the samples over 15 or more consignments, or leaving out whole consignments when re-fitting, restored coverage. {{r_abstract_app}}

**Significance:** Reliable uncertainty for a transferred NIR method can be obtained from the reference samples the transfer already needs, provided they come from many batches.

**Keywords:** calibration transfer; prediction interval; near-infrared spectroscopy; measurement uncertainty; conformal prediction; fruit dry matter

# 1. Introduction

NIR spectroscopy is used every day to measure moisture in grain, active ingredient in tablets and dry matter in fruit [@pasquini2018]. Each of these measurements relies on a calibration model built on one instrument, for one population of samples. Sooner or later the model has to be moved. A packhouse replaces a handheld unit, a pharmaceutical site adds a second spectrometer, a new harvest season brings fruit grown under different conditions. Calibration transfer handles the move. A small set of reference samples is measured on the new instrument, or in the new season, and used to correct either the spectra or the predictions: direct and piecewise direct standardisation (DS, PDS), or slope/bias correction (SBC) [@wang1991; @bouveresse1996; @feudale2002; @workman2018]. Newer approaches adapt the model with few or no reference values [@nikzad2018; @mishra2020dipls; @fonseca2022; @xie2024; @fan2025; @huang2026].

Transfer methods are almost always judged by their prediction error (RMSEP or bias). In practice, though, a laboratory does not report a bare number. It reports a value with an uncertainty range and takes decisions with it: a tablet batch is released if its assay lies within specification, and a mango block is harvested if the fruit reach a minimum dry matter. For mango, a minimum of 14% dry matter at harvest has long been recommended in Australia [@ainsworth2016]. The usual uncertainty statements for multivariate calibrations are error-propagation formulas and ASTM E1655-type intervals [@faber1997; @olivieri2006; @allegrini2016; @astm_e1655]. They are built from the error of the *original* calibration. After a move to a new instrument or season, that error no longer describes the model in use. A recent review of calibration transfer for portable optical instruments names the lack of uncertainty-aware validation as one of the open problems of the field [@haggam2026].

This paper asks a practical question. After a calibration has been transferred with *m* reference samples, can those same samples be used to give each new prediction an uncertainty range that can be trusted? And if so, which samples are needed?

Trusted here has a precise meaning. A 90% prediction interval should contain the reference value of about 90% of future samples. In method-validation language, this is a β-expectation tolerance interval, the quantity behind accuracy profiles [@hubert2004; @mee1984]. Conformal prediction gives intervals with this property under one assumption: the calibration samples and the future samples must be exchangeable, for example drawn at random from the same population [@vovk2005; @lei2018; @angelopoulos2023]. Conformal intervals have recently been used for NIR and MIR regression on a single instrument [@jovic2025; @duma2026], and for spectral classification under laboratory-to-field shift [@khairbek2026]. Transfer creates two difficulties. First, the reference samples are needed to fit the transfer itself, and setting half of them aside to calibrate an interval leaves too few for either job. Second, the samples are rarely a random draw from future production. They usually come from one or two lots, collected on the day the instrument was set up.

The first difficulty has a clean solution. The jackknife+ [@barber2021] re-fits a model with each calibration sample left out in turn and uses the left-out errors to build the interval, so no sample is wasted. We apply it to the transfer step only: the original calibration stays as it is, and only the standardisation or bias correction is re-fitted. We call the result the transfer jackknife+ (TJ+). The coverage guarantee then follows from the existing theory; we do not claim new statistics. The second difficulty is the one that decides whether the method is useful in practice. When samples come in batches (harvest consignments, production lots), the theory says that the batch, not the individual sample, has to be the random unit [@lee2026; @dunn2023]. Whether this matters after calibration transfer, and how much, has to be measured. The mango data used here record which consignment every fruit came from, which allowed us to measure it.

We therefore organised the study around four questions a laboratory would ask:

1. Can the uncertainty statement of the original calibration be kept after transfer?
2. If not, can valid intervals be obtained from the reference samples alone, and how do they compare with the simpler options a laboratory might use (Gaussian intervals, the regression prediction interval of slope/bias correction, bootstrap)?
3. Does it matter whether the reference samples come from a few batches or from many?
4. What does this mean for a real accept/reject decision, here harvest-maturity screening of mango?

The study uses public data only and was planned in advance. The complete code reproduces every number in the paper.
