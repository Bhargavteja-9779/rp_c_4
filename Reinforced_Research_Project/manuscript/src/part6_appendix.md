# Appendix A. Proof of Proposition 1 {.unnumbered}

**Setting.** Let $Z_1,\dots,Z_m$ be the transfer standards and $Z_{m+1}=(\mathbf{x}^T_{m+1},\mathbf{x}^S_{m+1},y_{m+1})$ the future sample. Its master spectrum $\mathbf{x}^S_{m+1}$ is never used by the procedure; it enters only the argument, as the spectrum the sample *would* give on the master instrument. For any index set $S\subseteq\{1,\dots,m+1\}$, let $\mu_S$ and $\sigma_S$ be the deployed predictor (Eq. (1)) and the difficulty function obtained by applying the transfer algorithm $\mathcal{T}$ to $\{Z_k:k\in S\}$. The source model $f$ and the function $\sigma$ of Eq. (4) are fixed beforehand from source data. $\mathcal{T}$ is *symmetric*, i.e. invariant to the order of its inputs; this holds for PDS, DS and SBC, which are least-squares fits on the set of standards. Because $\sigma\ge\varepsilon>0$, all normalised scores are well defined.

**Step 1 (scores).** For $i\neq j$, write $-ij$ for the set $\{1,\dots,m+1\}\backslash \{i,j\}$ and define
$$R_{ij}=\frac{|y_i-\mu_{-ij}(\mathbf{x}^T_i)|}{\sigma_{-ij}(\mathbf{x}^T_i)}.$$
The fit that excludes $i$ and $m+1$ is exactly the leave-one-out fit $\mu_{-i}$ of Eq. (2), computed from the $m$ standards without standard $i$. Hence $R_i=R_{i,m+1}$, and for the future sample $|y_{m+1}-\mu_{-i}(\mathbf{x}^T_{m+1})|/\sigma_{-i}(\mathbf{x}^T_{m+1})=R_{m+1,i}$.

**Step 2 (miscoverage implies many lost comparisons).** Let $U_i=\mu_{-i}(\mathbf{x})+\sigma_{-i}(\mathbf{x})R_i$ and $L_i=\mu_{-i}(\mathbf{x})-\sigma_{-i}(\mathbf{x})R_i$ with $\mathbf{x}=\mathbf{x}^T_{m+1}$.
- *Upper tail.* If $y_{m+1}$ exceeds the upper bound in Eq. (3), the $\lceil(1-\alpha)(m+1)\rceil$-th smallest $U_i$, then $y_{m+1}>U_i$ for at least $(1-\alpha)(m+1)$ indices $i$.
- *Lower tail.* If $y_{m+1}$ is below the lower bound, the $k$-th smallest $L_i$ with $k=\lfloor\alpha(m+1)\rfloor$, then $y_{m+1}<L_i$ for at least $m-k+1\ge(1-\alpha)(m+1)$ indices.

In both cases $|y_{m+1}-\mu_{-i}(\mathbf{x})|/\sigma_{-i}(\mathbf{x})>R_i$, i.e. $R_{m+1,i}>R_{i,m+1}$, for at least $(1-\alpha)(m+1)$ indices. Therefore
$$\{y_{m+1}\notin\hat C(\mathbf{x}^T_{m+1})\}\subseteq\Big\{\textstyle\sum_{i\le m}\mathbf{1}[R_{m+1,i}>R_{i,m+1}]\ge(1-\alpha)(m+1)\Big\}.$$

**Step 3 (tournament bound).** Call a point $j\in\{1,\dots,m+1\}$ *strange* if $\sum_{i\neq j}\mathbf{1}[R_{ji}>R_{ij}]\ge(1-\alpha)(m+1)$. By the counting lemma in the proof of Theorem 1 of Barber et al. [@barber2021], at most $2\alpha(m+1)$ points can be strange, for any realisation of the scores.

**Step 4 (exchangeability).** The $Z_k$ are exchangeable and $\mathcal{T}$ is symmetric. Hence the joint law of the matrix $(R_{ij})$ is invariant under a simultaneous permutation of rows and columns, and every point is equally likely to be strange. Thus $\Pr\{Z_{m+1}\text{ strange}\}=\mathbb{E}[\#\text{strange}]/(m+1)\le 2\alpha$. Combining with Step 2 gives $\Pr\{y_{m+1}\notin\hat C\}\le 2\alpha$. $\square$

**Remarks.**
- The normalisation enters only through the definition of the scores. Steps 2–4 hold for any score of the form $|y_i-\mu_{-ij}(\mathbf{x}_i)|/\sigma_{-ij}(\mathbf{x}_i)$ with $\sigma>0$, provided the pair $(\mu,\sigma)$ is produced by a symmetric algorithm.
- Fitting the transfer on all $m$ standards and reusing it to compute residuals (TJ-insample) breaks Step 1: the residual of standard $i$ is then computed with a fit that has seen $i$, and the exchangeability with the future sample's residual is lost. The resulting under-coverage is observed in Section 4.2.
- Ties between scores have probability zero for continuous data; with ties, the strict inequalities in Step 2 make the interval only more conservative.
- If the standards are chosen by a data-dependent design such as Kennard–Stone, they are no longer exchangeable with a random future sample, and Step 4 does not apply.
