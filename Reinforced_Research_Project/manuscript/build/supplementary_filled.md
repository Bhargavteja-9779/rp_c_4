---
title: "Supplementary Material"
subtitle: "Trustworthy prediction intervals after moving an NIR calibration to a new instrument or season"
---

Every table and figure in this document was generated automatically from the result files of the study. Method names: TJ+N, transfer jackknife+ with T²/Q scaling; TJ+, without scaling; TJ+B, leave-one-batch-out version; Split, half of the standards for transfer and half for calibration (SCP-T-split); Gauss-LOO, t-interval from leave-one-out errors.

# Table S1. Prediction error after transfer

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

Table: **Table S1.** Mean RMSEP of the transferred predictor for each pipeline and number of standards m (corn averaged over mp5 and mp6). NONE: original calibration applied without transfer.


# Table S2. Three confidence levels

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

Table: **Table S2.** Number of scenarios flagged as too narrow / scenarios, with the mean percentage of repetitions that returned unbounded intervals in parentheses (main pipelines, random standards).


# Table S3. Components of TJ+N

| Variant | Corn cov. | Corn under | Corn rel. IS | Tablets cov. | Tablets under | Tablets rel. IS | Mango cov. | Mango under | Mango rel. IS | Cov. low/high σ tertile |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| TJ+N | 0.931 | 0/24 | 1.000 | 0.910 | 0/12 | 1.000 | 0.904 | 0/4 | 1.000 | 0.904 / 0.933 |
| TJ+ | 0.933 | 0/24 | 1.019 | 0.911 | 0/12 | 1.062 | 0.904 | 0/4 | 1.016 | 0.957 / 0.878 |
| TCV+N | 0.942 | 0/24 | 1.066 | 0.917 | 0/12 | 1.000 | 0.908 | 0/4 | 1.009 | 0.916 / 0.941 |
| TJ-naive-N | 0.919 | 0/24 | 0.961 | 0.905 | 0/12 | 0.999 | 0.903 | 0/4 | 0.996 | 0.894 / 0.924 |
| TJ-insample-N | 0.897 | 10/24 | 0.935 | 0.912 | 0/12 | 1.000 | 0.863 | 4/4 | 0.992 | 0.878 / 0.909 |
| TJ+N[T2] | 0.931 | 0/24 | 0.976 | 0.911 | 0/12 | 0.999 | 0.904 | 0/4 | 1.005 | 0.922 / 0.916 |
| TJ+N[Q] | 0.931 | 0/24 | 1.020 | 0.911 | 0/12 | 1.011 | 0.904 | 0/4 | 1.006 | 0.914 / 0.924 |

Table: **Table S3.** Ablation of TJ+N (α = 0.10, main pipelines). TCV+N: five-fold CV+; TJ-naive-N: full-fit centre with leave-one-out quantile; TJ-insample-N: residuals of the transfer fitted on all standards; TJ+N[T2], TJ+N[Q]: scaling with one diagnostic. Rel. IS: median interval score relative to TJ+N. Last column: coverage in the lowest/highest third of σ(x).


# Table S4. Pipelines, directions and model types

| Setting | TJ+N | TJ+ | Gauss-LOO | SCP-T-split-N | ASTM-PI | SCP-S | WCP-S | MC-dropout |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Corn mp5→m5, PLS, PDS | 0.931 (0/12); 1.11 | 0.932 (0/12); 1.21 | 0.905 (0/12); 1.17 | 0.971 (0/12); inf | 0.657 (12/12); 1.34 | 0.757 (12/12); 1.25 | 0.800 (12/12); 1.53 | – |
| Corn m5→mp5, ridge, PDS | 0.943 (0/4); 1.21 | 0.953 (0/4); 1.17 | 0.904 (0/4); 1.06 | 1.000 (0/4); inf | 0.057 (4/4); 3.6 | 0.416 (4/4); 1.98 | 0.518 (4/4); inf | – |
| Tablets assay, ridge, PDS | 0.916 (0/1); 21.8 | 0.915 (0/1); 21.9 | 0.914 (0/1); 22 | 0.918 (0/1); 26.4 | 0.905 (0/1); 20.7 | 0.874 (1/1); 20.9 | 0.888 (1/1); 21.8 | – |
| Mango, ridge, SBC | 0.898 (0/1); 4.5 | 0.899 (0/1); 4.57 | 0.899 (0/1); 4.52 | 0.902 (0/1); 4.97 | 0.729 (1/1); 5.1 | 0.716 (1/1); 5.2 | 0.742 (1/1); inf | – |
| Mango, 1D-CNN, SBC | 0.910 (0/4); 5.24 | 0.909 (0/4); 5.51 | 0.894 (2/4); 5.42 | 0.945 (0/4); 5.59 | 0.714 (4/4); 6.48 | 0.693 (4/4); 6.71 | 0.780 (4/4); inf | 0.807 (4/4); 5.66 |

Table: **Table S4.** Reverse direction, ridge regression and a 1D-CNN (α = 0.10). Each cell: mean coverage (scenarios too narrow / scenarios); median interval score.


# Table S5. Robustness

| dataset | variant | method | coverage | coverage_min | IS_median | n_under | n_scen |
|:--|--:|--:|--:|--:|--:|--:|--:|
| corn | half_source | ASTM-PI | 0.335 | 0.071 | 2.841 | 4 | 4 |
| corn | half_source | Gauss-LOO | 0.908 | 0.898 | 1.092 | 0 | 4 |
| corn | half_source | SCP-S | 0.608 | 0.157 | 1.627 | 4 | 4 |
| corn | half_source | SCP-T-split-N | 1.0 | 1.0 | inf | 0 | 4 |
| corn | half_source | TJ+ | 0.947 | 0.941 | 1.183 | 0 | 4 |
| corn | half_source | TJ+N | 0.948 | 0.932 | 1.2 | 0 | 4 |
| corn | half_source | WCP-S | 0.7 | 0.355 | inf | 4 | 4 |
| corn | ks | ASTM-PI | 0.232 | 0.033 | 2.929 | 4 | 4 |
| corn | ks | Gauss-LOO | 0.913 | 0.9 | 1.048 | 0 | 4 |
| corn | ks | SCP-S | 0.452 | 0.067 | 1.813 | 4 | 4 |
| corn | ks | SCP-T-split-N | 1.0 | 1.0 | inf | 0 | 4 |
| corn | ks | TJ+ | 0.955 | 0.946 | 1.191 | 0 | 4 |
| corn | ks | TJ+N | 0.947 | 0.934 | 1.185 | 0 | 4 |
| corn | ks | WCP-S | 0.554 | 0.221 | inf | 4 | 4 |
| corn | noise_100 | ASTM-PI | 0.181 | 0.033 | 3.558 | 4 | 4 |
| corn | noise_100 | Gauss-LOO | 0.908 | 0.893 | 1.167 | 0 | 4 |
| corn | noise_100 | SCP-S | 0.327 | 0.058 | 3.197 | 4 | 4 |
| corn | noise_100 | SCP-T-split-N | 1.0 | 1.0 | inf | 0 | 4 |
| corn | noise_100 | TJ+ | 0.956 | 0.946 | 1.306 | 0 | 4 |
| corn | noise_100 | TJ+N | 0.956 | 0.939 | 1.261 | 0 | 4 |
| corn | noise_100 | WCP-S | 0.473 | 0.238 | inf | 4 | 4 |
| corn | noise_1000 | ASTM-PI | 0.234 | 0.037 | 2.983 | 4 | 4 |
| corn | noise_1000 | Gauss-LOO | 0.905 | 0.892 | 1.044 | 0 | 4 |
| corn | noise_1000 | SCP-S | 0.456 | 0.066 | 1.794 | 4 | 4 |
| corn | noise_1000 | SCP-T-split-N | 1.0 | 1.0 | inf | 0 | 4 |
| corn | noise_1000 | TJ+ | 0.951 | 0.943 | 1.17 | 0 | 4 |
| corn | noise_1000 | TJ+N | 0.946 | 0.934 | 1.175 | 0 | 4 |
| corn | noise_1000 | WCP-S | 0.554 | 0.221 | inf | 4 | 4 |
| corn | noise_300 | ASTM-PI | 0.23 | 0.036 | 3.006 | 4 | 4 |
| corn | noise_300 | Gauss-LOO | 0.906 | 0.895 | 1.054 | 0 | 4 |
| corn | noise_300 | SCP-S | 0.446 | 0.065 | 1.97 | 4 | 4 |
| corn | noise_300 | SCP-T-split-N | 1.0 | 1.0 | inf | 0 | 4 |
| corn | noise_300 | TJ+ | 0.952 | 0.944 | 1.175 | 0 | 4 |
| corn | noise_300 | TJ+N | 0.945 | 0.931 | 1.168 | 0 | 4 |
| corn | noise_300 | WCP-S | 0.548 | 0.22 | inf | 4 | 4 |
| corn | shift_-1 | ASTM-PI | 0.086 | 0.0 | 18.75 | 4 | 4 |
| corn | shift_-1 | Gauss-LOO | 0.17 | 0.025 | 13.629 | 4 | 4 |
| corn | shift_-1 | SCP-S | 0.074 | 0.0 | 19.4 | 4 | 4 |
| corn | shift_-1 | SCP-T-split-N | 1.0 | 1.0 | inf | 0 | 4 |
| corn | shift_-1 | TJ+ | 0.286 | 0.058 | 9.399 | 4 | 4 |
| corn | shift_-1 | TJ+N | 0.843 | 0.679 | 5.656 | 2 | 4 |
| corn | shift_-1 | WCP-S | 0.416 | 0.361 | 30.404 | 4 | 4 |
| corn | shift_1 | ASTM-PI | 0.079 | 0.0 | 19.718 | 4 | 4 |
| corn | shift_1 | Gauss-LOO | 0.151 | 0.02 | 14.643 | 4 | 4 |
| corn | shift_1 | SCP-S | 0.067 | 0.0 | 20.582 | 4 | 4 |
| corn | shift_1 | SCP-T-split-N | 1.0 | 1.0 | inf | 0 | 4 |
| corn | shift_1 | TJ+ | 0.262 | 0.05 | 10.341 | 4 | 4 |
| corn | shift_1 | TJ+N | 0.823 | 0.605 | 5.795 | 2 | 4 |
| corn | shift_1 | WCP-S | 0.497 | 0.416 | inf | 4 | 4 |
| mango | half_source | ASTM-PI | 0.755 | 0.755 | 4.864 | 1 | 1 |
| mango | half_source | Gauss-LOO | 0.899 | 0.899 | 4.46 | 0 | 1 |
| mango | half_source | SCP-S | 0.752 | 0.752 | 4.887 | 1 | 1 |
| mango | half_source | SCP-T-split-N | 0.905 | 0.905 | 4.857 | 0 | 1 |
| mango | half_source | TJ+ | 0.9 | 0.9 | 4.51 | 0 | 1 |
| mango | half_source | TJ+N | 0.899 | 0.899 | 4.479 | 0 | 1 |
| mango | half_source | WCP-S | 0.785 | 0.785 | inf | 1 | 1 |
| mango | ks | ASTM-PI | 0.752 | 0.752 | 4.888 | 1 | 1 |
| mango | ks | Gauss-LOO | 0.968 | 0.968 | 4.994 | 0 | 1 |
| mango | ks | SCP-S | 0.733 | 0.733 | 5.028 | 1 | 1 |
| mango | ks | SCP-T-split-N | 0.956 | 0.956 | 5.337 | 0 | 1 |
| mango | ks | TJ+ | 0.968 | 0.968 | 5.005 | 0 | 1 |
| mango | ks | TJ+N | 0.964 | 0.964 | 4.958 | 0 | 1 |
| mango | ks | WCP-S | 0.739 | 0.739 | inf | 1 | 1 |
| mango | noise_100 | ASTM-PI | 0.508 | 0.508 | 13.075 | 1 | 1 |
| mango | noise_100 | Gauss-LOO | 0.895 | 0.895 | 7.863 | 0 | 1 |
| mango | noise_100 | SCP-S | 0.49 | 0.49 | 13.545 | 1 | 1 |
| mango | noise_100 | SCP-T-split-N | 0.91 | 0.91 | 8.261 | 0 | 1 |
| mango | noise_100 | TJ+ | 0.9 | 0.9 | 7.968 | 0 | 1 |
| mango | noise_100 | TJ+N | 0.901 | 0.901 | 7.627 | 0 | 1 |
| mango | noise_100 | WCP-S | 0.507 | 0.507 | inf | 1 | 1 |
| mango | noise_1000 | ASTM-PI | 0.744 | 0.744 | 5.038 | 1 | 1 |
| mango | noise_1000 | Gauss-LOO | 0.9 | 0.9 | 4.554 | 0 | 1 |
| mango | noise_1000 | SCP-S | 0.726 | 0.726 | 5.186 | 1 | 1 |
| mango | noise_1000 | SCP-T-split-N | 0.908 | 0.908 | 4.957 | 0 | 1 |
| mango | noise_1000 | TJ+ | 0.902 | 0.902 | 4.63 | 0 | 1 |
| mango | noise_1000 | TJ+N | 0.902 | 0.902 | 4.54 | 0 | 1 |
| mango | noise_1000 | WCP-S | 0.733 | 0.733 | inf | 1 | 1 |
| mango | noise_300 | ASTM-PI | 0.693 | 0.693 | 6.271 | 1 | 1 |
| mango | noise_300 | Gauss-LOO | 0.9 | 0.9 | 5.235 | 0 | 1 |
| mango | noise_300 | SCP-S | 0.675 | 0.675 | 6.478 | 1 | 1 |
| mango | noise_300 | SCP-T-split-N | 0.91 | 0.91 | 5.722 | 0 | 1 |
| mango | noise_300 | TJ+ | 0.907 | 0.907 | 5.328 | 0 | 1 |
| mango | noise_300 | TJ+N | 0.908 | 0.908 | 5.149 | 0 | 1 |
| mango | noise_300 | WCP-S | 0.685 | 0.685 | inf | 1 | 1 |
| mango | shift_-1 | ASTM-PI | 0.023 | 0.023 | 50.584 | 1 | 1 |
| mango | shift_-1 | Gauss-LOO | 0.07 | 0.07 | 42.187 | 1 | 1 |
| mango | shift_-1 | SCP-S | 0.018 | 0.018 | 52.878 | 1 | 1 |
| mango | shift_-1 | SCP-T-split-N | 0.789 | 0.789 | 13.758 | 1 | 1 |
| mango | shift_-1 | TJ+ | 0.081 | 0.081 | 41.036 | 1 | 1 |
| mango | shift_-1 | TJ+N | 0.732 | 0.732 | 13.493 | 1 | 1 |
| mango | shift_-1 | WCP-S | 0.305 | 0.305 | inf | 1 | 1 |
| mango | shift_1 | ASTM-PI | 0.109 | 0.109 | 30.41 | 1 | 1 |
| mango | shift_1 | Gauss-LOO | 0.206 | 0.206 | 25.282 | 1 | 1 |
| mango | shift_1 | SCP-S | 0.069 | 0.069 | 34.439 | 1 | 1 |
| mango | shift_1 | SCP-T-split-N | 0.97 | 0.97 | 15.736 | 0 | 1 |
| mango | shift_1 | TJ+ | 0.216 | 0.216 | 24.705 | 1 | 1 |
| mango | shift_1 | TJ+N | 0.974 | 0.974 | 14.14 | 0 | 1 |
| mango | shift_1 | WCP-S | 0.207 | 0.207 | inf | 1 | 1 |
| tablets | half_source | ASTM-PI | 0.971 | 0.971 | 21.998 | 0 | 1 |
| tablets | half_source | Gauss-LOO | 0.916 | 0.916 | 20.21 | 0 | 1 |
| tablets | half_source | SCP-S | 0.957 | 0.957 | 20.65 | 0 | 1 |
| tablets | half_source | SCP-T-split-N | 0.913 | 0.913 | 22.635 | 0 | 1 |
| tablets | half_source | TJ+ | 0.908 | 0.908 | 20.01 | 0 | 1 |
| tablets | half_source | TJ+N | 0.907 | 0.907 | 19.729 | 0 | 1 |
| tablets | half_source | WCP-S | 0.964 | 0.964 | 21.402 | 0 | 1 |
| tablets | ks | ASTM-PI | 0.94 | 0.94 | 21.237 | 0 | 1 |
| tablets | ks | Gauss-LOO | 0.954 | 0.954 | 23.123 | 0 | 1 |
| tablets | ks | SCP-S | 0.922 | 0.922 | 21.252 | 0 | 1 |
| tablets | ks | SCP-T-split-N | 0.92 | 0.92 | 25.461 | 0 | 1 |
| tablets | ks | TJ+ | 0.956 | 0.956 | 23.808 | 0 | 1 |
| tablets | ks | TJ+N | 0.93 | 0.93 | 20.831 | 0 | 1 |
| tablets | ks | WCP-S | 0.928 | 0.928 | 21.95 | 0 | 1 |
| tablets | noise_100 | ASTM-PI | 0.927 | 0.927 | 21.563 | 0 | 1 |
| tablets | noise_100 | Gauss-LOO | 0.91 | 0.91 | 23.167 | 0 | 1 |
| tablets | noise_100 | SCP-S | 0.91 | 0.91 | 21.729 | 0 | 1 |
| tablets | noise_100 | SCP-T-split-N | 0.913 | 0.913 | 28.094 | 0 | 1 |
| tablets | noise_100 | TJ+ | 0.913 | 0.913 | 23.109 | 0 | 1 |
| tablets | noise_100 | TJ+N | 0.914 | 0.914 | 22.03 | 0 | 1 |
| tablets | noise_100 | WCP-S | 0.926 | 0.926 | 23.533 | 0 | 1 |
| tablets | noise_1000 | ASTM-PI | 0.928 | 0.928 | 21.591 | 0 | 1 |
| tablets | noise_1000 | Gauss-LOO | 0.91 | 0.91 | 23.064 | 0 | 1 |
| tablets | noise_1000 | SCP-S | 0.91 | 0.91 | 21.695 | 0 | 1 |
| tablets | noise_1000 | SCP-T-split-N | 0.916 | 0.916 | 27.687 | 0 | 1 |
| tablets | noise_1000 | TJ+ | 0.913 | 0.913 | 23.01 | 0 | 1 |
| tablets | noise_1000 | TJ+N | 0.916 | 0.916 | 22.036 | 0 | 1 |
| tablets | noise_1000 | WCP-S | 0.927 | 0.927 | 23.478 | 0 | 1 |
| tablets | noise_300 | ASTM-PI | 0.927 | 0.927 | 21.568 | 0 | 1 |
| tablets | noise_300 | Gauss-LOO | 0.91 | 0.91 | 23.077 | 0 | 1 |
| tablets | noise_300 | SCP-S | 0.91 | 0.91 | 21.718 | 0 | 1 |
| tablets | noise_300 | SCP-T-split-N | 0.916 | 0.916 | 27.932 | 0 | 1 |
| tablets | noise_300 | TJ+ | 0.912 | 0.912 | 23.032 | 0 | 1 |
| tablets | noise_300 | TJ+N | 0.915 | 0.915 | 22.011 | 0 | 1 |
| tablets | noise_300 | WCP-S | 0.926 | 0.926 | 23.397 | 0 | 1 |
| tablets | shift_-1 | ASTM-PI | 0.02 | 0.02 | 304.33 | 1 | 1 |
| tablets | shift_-1 | Gauss-LOO | 0.035 | 0.035 | 300.236 | 1 | 1 |
| tablets | shift_-1 | SCP-S | 0.015 | 0.015 | 314.736 | 1 | 1 |
| tablets | shift_-1 | SCP-T-split-N | 0.253 | 0.253 | 226.108 | 1 | 1 |
| tablets | shift_-1 | TJ+ | 0.034 | 0.034 | 286.928 | 1 | 1 |
| tablets | shift_-1 | TJ+N | 0.069 | 0.069 | 259.707 | 1 | 1 |
| tablets | shift_-1 | WCP-S | 0.022 | 0.022 | 340.682 | 1 | 1 |
| tablets | shift_1 | ASTM-PI | 0.008 | 0.008 | 350.126 | 1 | 1 |
| tablets | shift_1 | Gauss-LOO | 0.018 | 0.018 | 347.84 | 1 | 1 |
| tablets | shift_1 | SCP-S | 0.007 | 0.007 | 360.886 | 1 | 1 |
| tablets | shift_1 | SCP-T-split-N | 0.22 | 0.22 | 245.495 | 1 | 1 |
| tablets | shift_1 | TJ+ | 0.014 | 0.014 | 341.348 | 1 | 1 |
| tablets | shift_1 | TJ+N | 0.04 | 0.04 | 299.11 | 1 | 1 |
| tablets | shift_1 | WCP-S | 0.015 | 0.015 | 444.978 | 1 | 1 |

Table: **Table S5.** Robustness (α = 0.10; corn m = 15, tablets assay and mango m = 20; 200 repetitions): mean and minimum coverage over scenarios, median interval score and scenarios flagged as too narrow.


# Table S6. Transfer between handheld fruit spectrometers

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

Table: **Table S6.** Mango instrument transfer, source unit 15006 to three target units, four values of m (12 scenarios per pipeline; α = 0.10; 200 repetitions; standards drawn at random).


# Table S7. Gaussian intervals with difficulty scaling

| Data/pipeline set | Method | α = 0.05 | α = 0.10 | α = 0.20 |
|:--|--:|--:|--:|--:|
| corn | TJ+N | 0.986 (0/24) | 0.932 (0/24) | 0.835 (0/24) |
| corn | Gauss-LOO | 0.945 (6/24) | 0.903 (0/24) | 0.818 (0/24) |
| corn | Gauss-LOO-N | 0.951 (0/24) | 0.905 (0/24) | 0.811 (0/24) |
| mango | TJ+N | 0.968 (0/4) | 0.902 (0/4) | 0.803 (0/4) |
| mango | Gauss-LOO | 0.955 (0/4) | 0.902 (0/4) | 0.792 (1/4) |
| mango | Gauss-LOO-N | 0.956 (0/4) | 0.902 (0/4) | 0.790 (2/4) |
| mango_inst | TJ+N | 0.974 (0/24) | 0.919 (0/24) | 0.827 (0/24) |
| mango_inst | Gauss-LOO | 0.950 (4/24) | 0.908 (0/24) | 0.820 (0/24) |
| mango_inst | Gauss-LOO-N | 0.958 (6/24) | 0.915 (0/24) | 0.810 (3/24) |
| tablets | TJ+N | 0.971 (0/12) | 0.912 (0/12) | 0.820 (0/12) |
| tablets | Gauss-LOO | 0.949 (6/12) | 0.910 (0/12) | 0.825 (1/12) |
| tablets | Gauss-LOO-N | 0.948 (2/12) | 0.907 (1/12) | 0.819 (0/12) |

Table: **Table S7.** TJ+N compared with Gaussian leave-one-out intervals without (Gauss-LOO) and with (Gauss-LOO-N) σ(x) scaling (200 repetitions).


# Table S8. Quarter-channel drift

| dataset | shift | method | coverage | coverage_min | too_narrow | n |
|:--|--:|--:|--:|--:|--:|--:|
| corn | shift_-0.25 | ASTM-PI | 0.152 | 0.017 | 4 | 4 |
| corn | shift_-0.25 | Gauss-LOO | 0.692 | 0.672 | 4 | 4 |
| corn | shift_-0.25 | SCP-S | 0.259 | 0.025 | 4 | 4 |
| corn | shift_-0.25 | SCP-T-split-N | 1.0 | 1.0 | 0 | 4 |
| corn | shift_-0.25 | TJ+ | 0.807 | 0.781 | 4 | 4 |
| corn | shift_-0.25 | TJ+N | 0.928 | 0.879 | 0 | 4 |
| corn | shift_-0.25 | WCP-S | 0.459 | 0.281 | 4 | 4 |
| corn | shift_0.25 | ASTM-PI | 0.152 | 0.021 | 4 | 4 |
| corn | shift_0.25 | Gauss-LOO | 0.665 | 0.616 | 4 | 4 |
| corn | shift_0.25 | SCP-S | 0.251 | 0.03 | 4 | 4 |
| corn | shift_0.25 | SCP-T-split-N | 1.0 | 1.0 | 0 | 4 |
| corn | shift_0.25 | TJ+ | 0.781 | 0.746 | 4 | 4 |
| corn | shift_0.25 | TJ+N | 0.919 | 0.839 | 1 | 4 |
| corn | shift_0.25 | WCP-S | 0.501 | 0.392 | 4 | 4 |
| mango | shift_-0.25 | ASTM-PI | 0.624 | 0.624 | 1 | 1 |
| mango | shift_-0.25 | Gauss-LOO | 0.781 | 0.781 | 1 | 1 |
| mango | shift_-0.25 | SCP-S | 0.605 | 0.605 | 1 | 1 |
| mango | shift_-0.25 | SCP-T-split-N | 0.885 | 0.885 | 0 | 1 |
| mango | shift_-0.25 | TJ+ | 0.786 | 0.786 | 1 | 1 |
| mango | shift_-0.25 | TJ+N | 0.861 | 0.861 | 1 | 1 |
| mango | shift_-0.25 | WCP-S | 0.619 | 0.619 | 1 | 1 |
| mango | shift_0.25 | ASTM-PI | 0.682 | 0.682 | 1 | 1 |
| mango | shift_0.25 | Gauss-LOO | 0.833 | 0.833 | 1 | 1 |
| mango | shift_0.25 | SCP-S | 0.659 | 0.659 | 1 | 1 |
| mango | shift_0.25 | SCP-T-split-N | 0.958 | 0.958 | 0 | 1 |
| mango | shift_0.25 | TJ+ | 0.832 | 0.832 | 1 | 1 |
| mango | shift_0.25 | TJ+N | 0.961 | 0.961 | 0 | 1 |
| mango | shift_0.25 | WCP-S | 0.682 | 0.682 | 1 | 1 |
| tablets | shift_-0.25 | ASTM-PI | 0.663 | 0.663 | 1 | 1 |
| tablets | shift_-0.25 | Gauss-LOO | 0.659 | 0.659 | 1 | 1 |
| tablets | shift_-0.25 | SCP-S | 0.613 | 0.613 | 1 | 1 |
| tablets | shift_-0.25 | SCP-T-split-N | 0.697 | 0.697 | 1 | 1 |
| tablets | shift_-0.25 | TJ+ | 0.668 | 0.668 | 1 | 1 |
| tablets | shift_-0.25 | TJ+N | 0.591 | 0.591 | 1 | 1 |
| tablets | shift_-0.25 | WCP-S | 0.67 | 0.67 | 1 | 1 |
| tablets | shift_0.25 | ASTM-PI | 0.661 | 0.661 | 1 | 1 |
| tablets | shift_0.25 | Gauss-LOO | 0.658 | 0.658 | 1 | 1 |
| tablets | shift_0.25 | SCP-S | 0.613 | 0.613 | 1 | 1 |
| tablets | shift_0.25 | SCP-T-split-N | 0.726 | 0.726 | 1 | 1 |
| tablets | shift_0.25 | TJ+ | 0.675 | 0.675 | 1 | 1 |
| tablets | shift_0.25 | TJ+N | 0.615 | 0.615 | 1 | 1 |
| tablets | shift_0.25 | WCP-S | 0.671 | 0.671 | 1 | 1 |

Table: **Table S8.** Coverage under a ±0.25-channel wavelength shift of the routine spectra after standardisation (α = 0.10; 200 repetitions).


# Table S9. Transfer and model settings

| dataset | setting | method | coverage | coverage_min | IS_median | rmsep | n_under | n_scen |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| corn | hw1 | ASTM-PI | 0.25 | 0.033 | 2.655 | 0.237 | 4 | 4 |
| corn | hw1 | Gauss-LOO | 0.903 | 0.89 | 0.932 | 0.237 | 0 | 4 |
| corn | hw1 | SCP-S | 0.496 | 0.064 | 1.566 | 0.237 | 4 | 4 |
| corn | hw1 | SCP-T-split-N | 1.0 | 1.0 | inf | 0.237 | 0 | 4 |
| corn | hw1 | TJ+ | 0.941 | 0.93 | 1.057 | 0.237 | 0 | 4 |
| corn | hw1 | TJ+N | 0.941 | 0.927 | 1.083 | 0.237 | 0 | 4 |
| corn | hw1 | WCP-S | 0.588 | 0.217 | inf | 0.237 | 4 | 4 |
| corn | hw3 | ASTM-PI | 0.213 | 0.028 | 3.314 | 0.348 | 4 | 4 |
| corn | hw3 | Gauss-LOO | 0.909 | 0.896 | 1.21 | 0.348 | 0 | 4 |
| corn | hw3 | SCP-S | 0.404 | 0.056 | 2.363 | 0.348 | 4 | 4 |
| corn | hw3 | SCP-T-split-N | 1.0 | 1.0 | inf | 0.348 | 0 | 4 |
| corn | hw3 | TJ+ | 0.962 | 0.951 | 1.313 | 0.348 | 0 | 4 |
| corn | hw3 | TJ+N | 0.954 | 0.938 | 1.272 | 0.348 | 0 | 4 |
| corn | hw3 | WCP-S | 0.509 | 0.217 | inf | 0.348 | 4 | 4 |
| corn | hw5 | ASTM-PI | 0.17 | 0.032 | 4.362 | 0.503 | 4 | 4 |
| corn | hw5 | Gauss-LOO | 0.903 | 0.896 | 1.549 | 0.503 | 0 | 4 |
| corn | hw5 | SCP-S | 0.314 | 0.053 | 4.002 | 0.503 | 4 | 4 |
| corn | hw5 | SCP-T-split-N | 1.0 | 1.0 | inf | 0.503 | 0 | 4 |
| corn | hw5 | TJ+ | 0.967 | 0.955 | 1.735 | 0.503 | 0 | 4 |
| corn | hw5 | TJ+N | 0.962 | 0.95 | 1.512 | 0.503 | 0 | 4 |
| corn | hw5 | WCP-S | 0.44 | 0.233 | inf | 0.503 | 4 | 4 |
| corn | lv+2 | ASTM-PI | 0.189 | 0.033 | 3.136 | 0.283 | 4 | 4 |
| corn | lv+2 | Gauss-LOO | 0.905 | 0.893 | 1.047 | 0.283 | 0 | 4 |
| corn | lv+2 | SCP-S | 0.436 | 0.059 | 1.872 | 0.283 | 4 | 4 |
| corn | lv+2 | SCP-T-split-N | 1.0 | 1.0 | inf | 0.283 | 0 | 4 |
| corn | lv+2 | TJ+ | 0.952 | 0.943 | 1.18 | 0.283 | 0 | 4 |
| corn | lv+2 | TJ+N | 0.949 | 0.939 | 1.2 | 0.283 | 0 | 4 |
| corn | lv+2 | WCP-S | 0.552 | 0.237 | inf | 0.283 | 4 | 4 |
| corn | lv-2 | ASTM-PI | 0.313 | 0.051 | 2.488 | 0.275 | 4 | 4 |
| corn | lv-2 | Gauss-LOO | 0.904 | 0.894 | 1.06 | 0.275 | 0 | 4 |
| corn | lv-2 | SCP-S | 0.516 | 0.083 | 1.616 | 0.275 | 4 | 4 |
| corn | lv-2 | SCP-T-split-N | 1.0 | 1.0 | inf | 0.275 | 0 | 4 |
| corn | lv-2 | TJ+ | 0.951 | 0.943 | 1.161 | 0.275 | 0 | 4 |
| corn | lv-2 | TJ+N | 0.944 | 0.933 | 1.191 | 0.275 | 0 | 4 |
| corn | lv-2 | WCP-S | 0.589 | 0.203 | 2.741 | 0.275 | 4 | 4 |
| mango | lv+2 | ASTM-PI | 0.737 | 0.737 | 5.054 | 1.108 | 1 | 1 |
| mango | lv+2 | Gauss-LOO | 0.898 | 0.898 | 4.538 | 1.108 | 0 | 1 |
| mango | lv+2 | SCP-S | 0.721 | 0.721 | 5.186 | 1.108 | 1 | 1 |
| mango | lv+2 | SCP-T-split-N | 0.902 | 0.902 | 4.989 | 1.108 | 0 | 1 |
| mango | lv+2 | TJ+ | 0.899 | 0.899 | 4.612 | 1.108 | 0 | 1 |
| mango | lv+2 | TJ+N | 0.898 | 0.898 | 4.535 | 1.108 | 0 | 1 |
| mango | lv+2 | WCP-S | 0.734 | 0.734 | inf | 1.108 | 1 | 1 |
| mango | lv-2 | ASTM-PI | 0.757 | 0.757 | 5.016 | 1.106 | 1 | 1 |
| mango | lv-2 | Gauss-LOO | 0.896 | 0.896 | 4.587 | 1.106 | 0 | 1 |
| mango | lv-2 | SCP-S | 0.745 | 0.745 | 5.117 | 1.106 | 1 | 1 |
| mango | lv-2 | SCP-T-split-N | 0.906 | 0.906 | 4.968 | 1.106 | 0 | 1 |
| mango | lv-2 | TJ+ | 0.9 | 0.9 | 4.642 | 1.106 | 0 | 1 |
| mango | lv-2 | TJ+N | 0.899 | 0.899 | 4.544 | 1.106 | 0 | 1 |
| mango | lv-2 | WCP-S | 0.793 | 0.793 | inf | 1.106 | 1 | 1 |
| tablets | hw1 | ASTM-PI | 0.943 | 0.943 | 20.805 | 4.767 | 0 | 1 |
| tablets | hw1 | Gauss-LOO | 0.911 | 0.911 | 21.754 | 4.767 | 0 | 1 |
| tablets | hw1 | SCP-S | 0.928 | 0.928 | 20.589 | 4.767 | 0 | 1 |
| tablets | hw1 | SCP-T-split-N | 0.912 | 0.912 | 23.102 | 4.767 | 0 | 1 |
| tablets | hw1 | TJ+ | 0.913 | 0.913 | 21.903 | 4.767 | 0 | 1 |
| tablets | hw1 | TJ+N | 0.916 | 0.916 | 20.449 | 4.767 | 0 | 1 |
| tablets | hw1 | WCP-S | 0.939 | 0.939 | 22.007 | 4.767 | 0 | 1 |
| tablets | hw3 | ASTM-PI | 0.906 | 0.906 | 22.434 | 5.39 | 0 | 1 |
| tablets | hw3 | Gauss-LOO | 0.91 | 0.91 | 24.192 | 5.39 | 0 | 1 |
| tablets | hw3 | SCP-S | 0.884 | 0.884 | 22.73 | 5.39 | 1 | 1 |
| tablets | hw3 | SCP-T-split-N | 0.92 | 0.92 | 33.539 | 5.39 | 0 | 1 |
| tablets | hw3 | TJ+ | 0.916 | 0.916 | 24.22 | 5.39 | 0 | 1 |
| tablets | hw3 | TJ+N | 0.916 | 0.916 | 23.243 | 5.39 | 0 | 1 |
| tablets | hw3 | WCP-S | 0.909 | 0.909 | 24.208 | 5.39 | 0 | 1 |
| tablets | hw5 | ASTM-PI | 0.867 | 0.867 | 25.273 | 5.98 | 1 | 1 |
| tablets | hw5 | Gauss-LOO | 0.912 | 0.912 | 27.218 | 5.98 | 0 | 1 |
| tablets | hw5 | SCP-S | 0.837 | 0.837 | 26.267 | 5.98 | 1 | 1 |
| tablets | hw5 | SCP-T-split-N | 0.915 | 0.915 | 37.461 | 5.98 | 0 | 1 |
| tablets | hw5 | TJ+ | 0.925 | 0.925 | 27.284 | 5.98 | 0 | 1 |
| tablets | hw5 | TJ+N | 0.924 | 0.924 | 26.505 | 5.98 | 0 | 1 |
| tablets | hw5 | WCP-S | 0.87 | 0.87 | 29.995 | 5.98 | 1 | 1 |
| tablets | lv+2 | ASTM-PI | 0.898 | 0.898 | 22.363 | 5.326 | 0 | 1 |
| tablets | lv+2 | Gauss-LOO | 0.908 | 0.908 | 24.135 | 5.326 | 0 | 1 |
| tablets | lv+2 | SCP-S | 0.876 | 0.876 | 23.175 | 5.326 | 1 | 1 |
| tablets | lv+2 | SCP-T-split-N | 0.918 | 0.918 | 26.722 | 5.326 | 0 | 1 |
| tablets | lv+2 | TJ+ | 0.91 | 0.91 | 24.74 | 5.326 | 0 | 1 |
| tablets | lv+2 | TJ+N | 0.918 | 0.918 | 21.987 | 5.326 | 0 | 1 |
| tablets | lv+2 | WCP-S | 0.907 | 0.907 | inf | 5.326 | 0 | 1 |
| tablets | lv-2 | ASTM-PI | 0.903 | 0.903 | 29.591 | 6.999 | 0 | 1 |
| tablets | lv-2 | Gauss-LOO | 0.909 | 0.909 | 31.299 | 6.999 | 0 | 1 |
| tablets | lv-2 | SCP-S | 0.912 | 0.912 | 29.915 | 6.999 | 0 | 1 |
| tablets | lv-2 | SCP-T-split-N | 0.908 | 0.908 | 37.834 | 6.999 | 0 | 1 |
| tablets | lv-2 | TJ+ | 0.912 | 0.912 | 32.295 | 6.999 | 0 | 1 |
| tablets | lv-2 | TJ+N | 0.916 | 0.916 | 28.684 | 6.999 | 0 | 1 |
| tablets | lv-2 | WCP-S | 0.92 | 0.92 | 30.799 | 6.999 | 0 | 1 |

Table: **Table S9.** Sensitivity to the PDS window (hw1 = 3 channels, hw3 = 7, hw5 = 11; main analysis 5) and to the number of PLS components (±2).


# Table S10. Computing time

| dataset | kind | m | n_test | n_channels | step | median_s | p90_s | peak_mem_MB | source_model_fit_s |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| corn | pds | 20 | 10 | 700 | point prediction only (1 transfer fit) | 0.0046 | 0.0061 | 0.8785 | 0.1027 |
| corn | pds | 20 | 10 | 700 | SCP-T-split (1 fit) | 0.0047 | 0.0065 | 0.7389 | 0.1027 |
| corn | pds | 20 | 10 | 700 | TJ+N incl. m LOO + 5 CV fits | 0.1469 | 0.1572 | 1.2104 | 0.1027 |
| tablets | pds | 50 | 410 | 650 | point prediction only (1 transfer fit) | 0.0243 | 0.0298 | 14.3825 | 0.2743 |
| tablets | pds | 50 | 410 | 650 | SCP-T-split (1 fit) | 0.0259 | 0.0265 | 14.3831 | 0.2743 |
| tablets | pds | 50 | 410 | 650 | TJ+N incl. m LOO + 5 CV fits | 2.7857 | 2.9018 | 15.2063 | 0.2743 |
| mango | sbc | 50 | 675 | 103 | point prediction only (1 transfer fit) | 0.0004 | 0.0005 | 1.1246 | 1.4279 |
| mango | sbc | 50 | 675 | 103 | SCP-T-split (1 fit) | 0.0004 | 0.0004 | 1.1246 | 1.4279 |
| mango | sbc | 50 | 675 | 103 | TJ+N incl. m LOO + 5 CV fits | 0.0635 | 0.0742 | 3.1352 | 1.4279 |

Table: **Table S10.** Wall-clock time and peak memory (one CPU core, median of 20 runs).


# Table S11. Batch designs, every combination

| Setting | Pipeline | Design | TJ+N | TJ+B | Gauss-LOO | Split | ANOVA-PI | Gauss-LGO | ASTM-PI | TJ+N, same batches | ICC |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| inst_15014 | PDS | chrono 5×4 | 0.927 | unb. | 0.804* | 0.903 | 0.840* | 0.905 | 0.424* | 0.933 | 0.62 |
| inst_15014 | PDS | 2×10 | 0.897 | unb. | 0.733* | 0.872* | 0.803* | 0.984 | 0.335* | 0.926 | 0.59 |
| inst_15014 | PDS | 5×4 | 0.916 | unb. | 0.846* | 0.894 | 0.878* | 0.945 | 0.364* | 0.926 | 0.58 |
| inst_15014 | PDS | 10×2 | 0.925 | 0.981 | 0.889* | 0.901 | 0.906 | 0.926 | 0.363* | 0.932 | 0.56 |
| inst_15014 | PDS | 15×1 | 0.976 | 0.976 | 0.928 | unb. | 0.936 | 0.928 | 0.351* | 0.977 | 0.55 |
| inst_15014 | PDS | 20×1 | 0.943 | 0.943 | 0.921 | 0.914 | 0.928 | 0.921 | 0.382* | 0.943 | 0.54 |
| inst_15014 | SBC | chrono 5×4 | 0.763* | unb. | 0.755* | 0.800* | 0.797* | 0.868* | 0.757* | 0.919 | 0.69 |
| inst_15014 | SBC | 2×10 | 0.672* | unb. | 0.662* | 0.700* | 0.759* | 0.997 | 0.643* | 0.907 | 0.63 |
| inst_15014 | SBC | 5×4 | 0.824* | unb. | 0.822* | 0.845* | 0.876* | 0.927 | 0.719* | 0.916 | 0.61 |
| inst_15014 | SBC | 10×2 | 0.882* | 0.947 | 0.876* | 0.889 | 0.905 | 0.910 | 0.744* | 0.921 | 0.60 |
| inst_15014 | SBC | 15×1 | 0.940 | 0.940 | 0.903 | unb. | 0.920 | 0.903 | 0.748* | 0.959 | 0.60 |
| inst_15014 | SBC | 20×1 | 0.906 | 0.906 | 0.899 | 0.910 | 0.912 | 0.899 | 0.758* | 0.926 | 0.59 |
| inst_15016 | PDS | chrono 5×4 | 0.932 | unb. | 0.775* | 0.911 | 0.813* | 0.889 | 0.394* | 0.938 | 0.57 |
| inst_15016 | PDS | 2×10 | 0.907 | unb. | 0.762* | 0.875* | 0.838* | 0.971 | 0.291* | 0.927 | 0.56 |
| inst_15016 | PDS | 5×4 | 0.918 | unb. | 0.855* | 0.904 | 0.893 | 0.951 | 0.254* | 0.932 | 0.55 |
| inst_15016 | PDS | 10×2 | 0.935 | 0.982 | 0.901 | 0.904 | 0.919 | 0.933 | 0.262* | 0.940 | 0.55 |
| inst_15016 | PDS | 15×1 | 0.968 | 0.968 | 0.920 | unb. | 0.929 | 0.920 | 0.263* | 0.972 | 0.54 |
| inst_15016 | PDS | 20×1 | 0.930 | 0.930 | 0.910 | 0.908 | 0.919 | 0.910 | 0.272* | 0.933 | 0.55 |
| inst_15016 | SBC | chrono 5×4 | 0.919 | unb. | 0.877* | 0.923 | 0.904 | 0.943 | 0.807* | 0.908 | 0.43 |
| inst_15016 | SBC | 2×10 | 0.774* | unb. | 0.753* | 0.799* | 0.827* | 0.999 | 0.705* | 0.906 | 0.47 |
| inst_15016 | SBC | 5×4 | 0.871* | unb. | 0.859* | 0.874* | 0.902 | 0.945 | 0.760* | 0.915 | 0.46 |
| inst_15016 | SBC | 10×2 | 0.891 | 0.950 | 0.886* | 0.900 | 0.910 | 0.913 | 0.770* | 0.917 | 0.46 |
| inst_15016 | SBC | 15×1 | 0.936 | 0.936 | 0.898 | unb. | 0.916 | 0.898 | 0.771* | 0.948 | 0.46 |
| inst_15016 | SBC | 20×1 | 0.900 | 0.900 | 0.899 | 0.906 | 0.913 | 0.899 | 0.783* | 0.911 | 0.46 |
| inst_15029 | PDS | chrono 5×4 | 0.937 | unb. | 0.799* | 0.909 | 0.687* | 0.908 | 0.212* | 0.923 | 0.53 |
| inst_15029 | PDS | 2×10 | 0.877* | unb. | 0.761* | 0.868* | 0.841* | 0.994 | 0.298* | 0.925 | 0.56 |
| inst_15029 | PDS | 5×4 | 0.904 | unb. | 0.861* | 0.896 | 0.893 | 0.952 | 0.335* | 0.921 | 0.54 |
| inst_15029 | PDS | 10×2 | 0.924 | 0.974 | 0.908 | 0.907 | 0.922 | 0.943 | 0.386* | 0.928 | 0.55 |
| inst_15029 | PDS | 15×1 | 0.959 | 0.959 | 0.917 | unb. | 0.926 | 0.917 | 0.368* | 0.964 | 0.54 |
| inst_15029 | PDS | 20×1 | 0.932 | 0.932 | 0.923 | 0.911 | 0.931 | 0.923 | 0.415* | 0.933 | 0.53 |
| inst_15029 | SBC | chrono 5×4 | 0.735* | unb. | 0.681* | 0.767* | 0.834* | 0.896 | 0.320* | 0.913 | 0.36 |
| inst_15029 | SBC | 2×10 | 0.723* | unb. | 0.709* | 0.742* | 0.794* | 0.997 | 0.707* | 0.908 | 0.61 |
| inst_15029 | SBC | 5×4 | 0.827* | unb. | 0.823* | 0.839* | 0.869* | 0.917 | 0.748* | 0.915 | 0.61 |
| inst_15029 | SBC | 10×2 | 0.888* | 0.945 | 0.879* | 0.897 | 0.904 | 0.908 | 0.771* | 0.923 | 0.61 |
| inst_15029 | SBC | 15×1 | 0.932 | 0.932 | 0.892 | unb. | 0.907 | 0.892 | 0.772* | 0.956 | 0.60 |
| inst_15029 | SBC | 20×1 | 0.908 | 0.908 | 0.899 | 0.900 | 0.911 | 0.899 | 0.781* | 0.924 | 0.59 |
| season | NONE | chrono 5×4 | 0.914 | unb. | 0.923 | 0.915 | 0.916 | 0.973 | 0.746* | 0.906 | 0.64 |
| season | NONE | 2×10 | 0.870* | unb. | 0.871* | 0.878* | 0.880* | 1.000 | 0.750* | 0.908 | 0.56 |
| season | NONE | 5×4 | 0.897 | unb. | 0.900 | 0.903 | 0.911 | 0.956 | 0.754* | 0.910 | 0.55 |
| season | NONE | 10×2 | 0.900 | 0.950 | 0.898 | 0.901 | 0.903 | 0.918 | 0.747* | 0.911 | 0.55 |
| season | NONE | 15×1 | 0.946 | 0.946 | 0.910 | unb. | 0.905 | 0.910 | 0.762* | 0.945 | 0.47 |
| season | SBC | chrono 5×4 | 0.853* | unb. | 0.860* | 0.863* | 0.902 | 0.951 | 0.725* | 0.907 | 0.63 |
| season | SBC | 2×10 | 0.676* | unb. | 0.675* | 0.693* | 0.776* | 0.999 | 0.634* | 0.913 | 0.58 |
| season | SBC | 5×4 | 0.824* | unb. | 0.830* | 0.838* | 0.890 | 0.944 | 0.689* | 0.920 | 0.56 |
| season | SBC | 10×2 | 0.884* | 0.950 | 0.878* | 0.879* | 0.911 | 0.917 | 0.714* | 0.930 | 0.55 |
| season | SBC | 15×1 | 0.933 | 0.933 | 0.898 | unb. | 0.920 | 0.898 | 0.721* | 0.953 | 0.49 |

Table: **Table S11.** Standards from K consignments × n_g fruit (α = 0.10; 300 repetitions). Coverage for fruit from consignments without standards (consignment-weighted); * flagged as too narrow (upper 95% bootstrap limit < 0.90); unb.: unbounded in more than half of the repetitions. Last two columns: TJ+N coverage for the remaining fruit of the sampled consignments, and the intra-consignment correlation (ICC) of the errors of the transferred predictor. Confidence intervals for every cell are in results/summary/E10_summary.csv.


# Table S12. Simpler interval formulas

| Data set | Pipeline | Method | Too narrow α=0.05 | Too narrow α=0.10 | Too narrow α=0.20 | Median IS relative to TJ+N (α=0.10) |
|:--|--:|--:|--:|--:|--:|--:|
| corn | pds | ASTM-T | 0/24 | 0/24 | 0/24 | 1.017 |
| corn | pds | Boot-T | 7/24 | 3/24 | 2/24 | 0.993 |
| corn | pds | Gauss-LOO | 6/24 | 0/24 | 0/24 | 0.941 |
| corn | pds | Gauss-LOO-N | 0/24 | 0/24 | 0/24 | 0.913 |
| corn | pds | SCP-T-split-N | 0/24 | 0/24 | 0/24 | 1.185 |
| corn | pds | TJ+ | 0/24 | 0/24 | 0/24 | 1.021 |
| corn | pds | TJ+N | 0/24 | 0/24 | 0/24 | 1.0 |
| corn | sbc | ASTM-T | 0/24 | 0/24 | 0/24 | 1.524 |
| corn | sbc | Boot-T | 24/24 | 19/24 | 12/24 | 0.968 |
| corn | sbc | Gauss-LOO | 8/24 | 1/24 | 0/24 | 0.957 |
| corn | sbc | Gauss-LOO-N | 7/24 | 1/24 | 0/24 | 0.951 |
| corn | sbc | OLS-PI | 5/24 | 1/24 | 0/24 | 0.955 |
| corn | sbc | SCP-T-split-N | 0/24 | 0/24 | 0/24 | 1.133 |
| corn | sbc | TJ+ | 0/24 | 0/24 | 0/24 | 1.013 |
| corn | sbc | TJ+N | 0/24 | 0/24 | 0/24 | 1.0 |
| mango | sbc | ASTM-T | 0/4 | 0/4 | 0/4 | 1.01 |
| mango | sbc | Boot-T | 4/4 | 4/4 | 3/4 | 1.006 |
| mango | sbc | Gauss-LOO | 0/4 | 0/4 | 1/4 | 1.01 |
| mango | sbc | Gauss-LOO-N | 0/4 | 0/4 | 2/4 | 0.995 |
| mango | sbc | OLS-PI | 0/4 | 0/4 | 3/4 | 1.007 |
| mango | sbc | SCP-T-split-N | 0/4 | 0/4 | 0/4 | 1.091 |
| mango | sbc | TJ+ | 0/4 | 0/4 | 0/4 | 1.015 |
| mango | sbc | TJ+N | 0/4 | 0/4 | 0/4 | 1.0 |
| mango_inst | pds | ASTM-T | 0/12 | 0/12 | 0/12 | 1.126 |
| mango_inst | pds | Boot-T | 0/12 | 0/12 | 0/12 | 1.223 |
| mango_inst | pds | Gauss-LOO | 0/12 | 0/12 | 0/12 | 1.123 |
| mango_inst | pds | Gauss-LOO-N | 0/12 | 0/12 | 3/12 | 0.953 |
| mango_inst | pds | SCP-T-split-N | 0/12 | 0/12 | 0/12 | 1.222 |
| mango_inst | pds | TJ+ | 0/12 | 0/12 | 0/12 | 1.197 |
| mango_inst | pds | TJ+N | 0/12 | 0/12 | 0/12 | 1.0 |
| mango_inst | sbc | ASTM-T | 4/12 | 0/12 | 0/12 | 0.966 |
| mango_inst | sbc | Boot-T | 12/12 | 11/12 | 6/12 | 0.964 |
| mango_inst | sbc | Gauss-LOO | 4/12 | 0/12 | 0/12 | 0.966 |
| mango_inst | sbc | Gauss-LOO-N | 6/12 | 0/12 | 0/12 | 0.986 |
| mango_inst | sbc | OLS-PI | 3/12 | 0/12 | 0/12 | 0.964 |
| mango_inst | sbc | SCP-T-split-N | 0/12 | 0/12 | 0/12 | 1.08 |
| mango_inst | sbc | TJ+ | 0/12 | 0/12 | 0/12 | 0.982 |
| mango_inst | sbc | TJ+N | 0/12 | 0/12 | 0/12 | 1.0 |
| tablets | pds | ASTM-T | 4/12 | 0/12 | 1/12 | 1.052 |
| tablets | pds | Boot-T | 8/12 | 7/12 | 8/12 | 1.031 |
| tablets | pds | Gauss-LOO | 5/12 | 0/12 | 1/12 | 1.058 |
| tablets | pds | Gauss-LOO-N | 2/12 | 1/12 | 0/12 | 0.992 |
| tablets | pds | SCP-T-split-N | 0/12 | 0/12 | 0/12 | 1.067 |
| tablets | pds | TJ+ | 0/12 | 0/12 | 0/12 | 1.057 |
| tablets | pds | TJ+N | 0/12 | 0/12 | 0/12 | 1.0 |
| tablets | sbc | ASTM-T | 8/12 | 1/12 | 1/12 | 1.005 |
| tablets | sbc | Boot-T | 10/12 | 8/12 | 6/12 | 0.991 |
| tablets | sbc | Gauss-LOO | 8/12 | 1/12 | 1/12 | 1.005 |
| tablets | sbc | Gauss-LOO-N | 8/12 | 1/12 | 1/12 | 0.988 |
| tablets | sbc | OLS-PI | 8/12 | 1/12 | 1/12 | 0.995 |
| tablets | sbc | SCP-T-split-N | 0/12 | 0/12 | 0/12 | 1.072 |
| tablets | sbc | TJ+ | 0/12 | 0/12 | 0/12 | 1.017 |
| tablets | sbc | TJ+N | 0/12 | 0/12 | 0/12 | 1.0 |

Table: **Table S12.** Simpler interval formulas on identical standards (200 repetitions; standards drawn at random).


# Table S13. Closeness to nominal and per-set reliability

| Method | Non-inferior α=0.05 | α=0.10 | α=0.20 | Training-conditional share, median (min), α=0.10 |
|:--|--:|--:|--:|--:|
| TJ+N | 64/64 | 64/64 | 64/64 | 0.88 (0.74) |
| TJ+ | 64/64 | 64/64 | 64/64 | 0.88 (0.76) |
| Gauss-LOO | 62/64 | 63/64 | 62/64 | 0.82 (0.73) |
| SCP-T-split-N | 64/64 | 64/64 | 64/64 | 0.91 (0.74) |
| ASTM-PI | 11/64 | 11/64 | 11/64 | 0.00 (0.00) |

Table: **Table S13.** Main scenarios with random standards (corn, tablets, mango season shift and mango instruments; 64 scenario-pipeline combinations). Non-inferior: lower limit of the 95% CI of coverage ≥ nominal − 0.02. Last column: share of standard sets (repetitions) with realised coverage ≥ 0.85 on the test samples, median (minimum) over scenarios. Unbounded intervals count as covering.


# Table S14. Harvest-maturity case study, all settings

| Setting | Pipeline | Design | Immature % | Point | ASTM-PI | Gauss-LOO | TJ+N | TJ+B |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| inst_15014 | PDS | 2×10 | 25 | 39.8 / 0 | 25.6 / 24 | 8.0 / 63 | 2.3 / 78 | 0.0 / 100 |
| inst_15014 | PDS | 10×2 | 25 | 36.7 / 0 | 20.4 / 27 | 2.3 / 78 | 1.4 / 79 | 0.4 / 89 |
| inst_15014 | PDS | 20×1 | 24 | 31.9 / 0 | 16.1 / 28 | 1.6 / 78 | 1.3 / 73 | 1.3 / 73 |
| inst_15014 | SBC | 2×10 | 25 | 31.5 / 0 | 8.2 / 34 | 7.8 / 36 | 7.8 / 37 | 0.0 / 100 |
| inst_15014 | SBC | 10×2 | 25 | 31.2 / 0 | 5.4 / 38 | 2.1 / 51 | 2.1 / 52 | 0.7 / 61 |
| inst_15014 | SBC | 20×1 | 24 | 27.6 / 0 | 5.0 / 38 | 1.8 / 52 | 1.9 / 53 | 1.9 / 53 |
| inst_15016 | PDS | 2×10 | 24 | 49.2 / 0 | 36.2 / 23 | 12.0 / 69 | 5.3 / 80 | 0.0 / 100 |
| inst_15016 | PDS | 10×2 | 24 | 58.7 / 0 | 44.4 / 24 | 5.0 / 88 | 4.8 / 86 | 1.1 / 94 |
| inst_15016 | PDS | 20×1 | 24 | 65.4 / 0 | 51.3 / 24 | 5.2 / 91 | 4.3 / 88 | 4.3 / 88 |
| inst_15016 | SBC | 2×10 | 24 | 44.5 / 0 | 12.0 / 40 | 9.8 / 44 | 9.4 / 49 | 0.0 / 100 |
| inst_15016 | SBC | 10×2 | 24 | 38.1 / 0 | 8.4 / 41 | 3.8 / 54 | 4.6 / 57 | 2.0 / 69 |
| inst_15016 | SBC | 20×1 | 24 | 37.6 / 0 | 8.4 / 41 | 3.7 / 53 | 4.5 / 57 | 4.5 / 57 |
| inst_15029 | PDS | 2×10 | 24 | 69.3 / 0 | 52.8 / 22 | 19.9 / 67 | 12.0 / 77 | 0.0 / 100 |
| inst_15029 | PDS | 10×2 | 24 | 75.0 / 0 | 53.8 / 25 | 6.0 / 81 | 7.9 / 79 | 2.3 / 90 |
| inst_15029 | PDS | 20×1 | 23 | 74.2 / 0 | 49.5 / 26 | 3.0 / 82 | 6.8 / 78 | 6.8 / 78 |
| inst_15029 | SBC | 2×10 | 24 | 44.0 / 0 | 12.4 / 37 | 12.8 / 41 | 11.5 / 43 | 0.0 / 100 |
| inst_15029 | SBC | 10×2 | 24 | 41.5 / 0 | 9.9 / 39 | 5.8 / 50 | 5.0 / 52 | 2.4 / 62 |
| inst_15029 | SBC | 20×1 | 23 | 39.7 / 0 | 9.9 / 38 | 4.6 / 52 | 4.1 / 54 | 4.1 / 54 |
| season | SBC | 2×10 | 14 | 42.1 / 0 | 10.9 / 23 | 9.8 / 25 | 10.6 / 25 | 0.0 / 100 |
| season | SBC | 10×2 | 14 | 34.3 / 0 | 4.3 / 26 | 0.9 / 34 | 1.1 / 34 | 0.3 / 41 |

Table: **Table S14.** Screening at 14% dry matter with 90% intervals, fruit from consignments without standards (200 repetitions). Each cell: percentage of immature fruit passed as mature / percentage of all fruit referred for re-measurement. Bootstrap CIs: results/summary/E14_summary.csv.


# Fig. S1

![**Fig. S1.** Ablation of TJ+N: mean coverage (left) and median interval score relative to TJ+N (right).](figures/fig5_ablation.png){width=13cm}


# Fig. S2

![**Fig. S2.** Coverage within thirds of the difficulty σ(x) of the test spectra (main pipelines, α = 0.10).](figures/fig7_conditional_coverage.png){width=13cm}


# Fig. S3

![**Fig. S3.** Miss rate by Q-residual quintile of the test spectra (first 100 repetitions).](figures/fig8_error_analysis.png){width=13cm}


# Fig. S4

![**Fig. S4.** Distribution over repetitions of the realised coverage for one scenario per data set; the guarantee concerns the mean.](figures/fig10_coverage_distribution.png){width=13cm}


# Fig. S5

![**Fig. S5.** Share of standard sets whose realised coverage reached 0.85, by number of standards (median over scenarios).](figures/fig_training_conditional.png){width=13cm}


# Fig. S6

![**Fig. S6.** TJ+N coverage for new consignments against the intra-consignment correlation of the errors, by design. Within the narrow ICC range observed, the design (number of consignments) rather than the ICC determined coverage.](figures/fig_batch_mechanism.png){width=13cm}


# Fig. S7

![**Fig. S7.** Median interval width relative to RMSEP for methods that were not too narrow.](figures/fig4_width_vs_m.png){width=13cm}


# Fig. S8

![**Fig. S8.** Training and validation loss of the 1D-CNN (mango, seasons 1–3).](figures/figS1_cnn_training.png){width=13cm}


# Fig. S9

![**Fig. S9.** Mean Friedman ranks of the scenario median interval score over the 40 main scenarios (descriptive).](figures/figS2_friedman_ranks.png){width=13cm}


# Fig. S10

![**Fig. S10.** Wall-clock time per test batch (one CPU core, median of 20 runs).](figures/fig9_timing.png){width=13cm}

