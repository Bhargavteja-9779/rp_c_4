# 3. Experimental

## 3.1. Data sets

Three public NIR data sets with documented domain shifts were used (Table 1; Fig. 2). No data were collected for this study.

**Corn** [@eigenvector_data]. Eighty corn samples were measured on three NIR spectrometers: m5 (master), mp5 and mp6. The range is 1100–2498 nm at 2 nm intervals (700 channels). Moisture, oil, protein and starch were determined by reference methods. Instrument shift: m5→mp5 and m5→mp6, plus mp5→m5 as a reverse-direction check.

**Pharmaceutical tablets (IDRC Shootout 2002)** [@eigenvector_data]. 655 tablets were measured on two spectrometers (600–1898 nm, 650 channels), with reference weight, hardness and active-ingredient assay. The distributed calibrate (155), validate (40) and test (460) partition was retained; the target pool is therefore the organisers' test set. Instrument 1 is the master.

**Mango dry matter** [@anderson2020; @mango_data]. The data comprise 11,691 NIR spectra (684–990 nm used, 103 channels) of intact mango fruit from four harvest seasons, with dry-matter content (DMC) as reference. As recommended by the data providers, replicate scans of the same fruit (2–6 scans; one subset scanned at three temperatures) must never be split between training and test sets. Replicates were therefore averaged per fruit (fruit identified by season, region, harvest date, maturity type, cultivar, population and DM value), giving {{n_fruit}} fruit (file version 1 of the data record). For the additional instrument-shift test (§4.6), the providers' extended file (record version 6) was used. Spectra flagged as outliers by the providers were excluded, and replicates were averaged per fruit and instrument. Season shift: seasons 1–3 (source) → season 4 (target, the providers' external validation season).

{{table1}}

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
