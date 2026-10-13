"""PLS1 regression via NIPALS with all-component coefficients, Hotelling T^2 and Q residuals."""
import numpy as np

class PLS1:
    """Single-response PLS (NIPALS). After fit, `coef_[:, a-1]` holds the regression vector with a LVs."""

    def __init__(self, n_components):
        self.A = int(n_components)

    def fit(self, X, y):
        X = np.asarray(X, float); y = np.asarray(y, float).ravel()
        n, p = X.shape
        A = min(self.A, n - 1, p)
        self.x_mean_, self.y_mean_ = X.mean(0), y.mean()
        E = X - self.x_mean_; f = y - self.y_mean_
        W = np.zeros((p, A)); P = np.zeros((p, A)); q = np.zeros(A)
        for a in range(A):
            w = E.T @ f
            nw = np.linalg.norm(w)
            if nw < 1e-14:
                A = a; W, P, q = W[:, :a], P[:, :a], q[:a]; break
            w /= nw
            t = E @ w; tt = t @ t
            pa = E.T @ t / tt; qa = f @ t / tt
            E -= np.outer(t, pa); f = f - qa * t
            W[:, a], P[:, a], q[a] = w, pa, qa
        self.A_ = A
        self.R_ = W @ np.linalg.inv(P.T @ W)          # X-rotations: T = Xc R
        self.P_, self.q_ = P, q
        self.coef_ = np.cumsum(self.R_ * q, axis=1)    # (p, A): coefficients for 1..A LVs
        T = (X - self.x_mean_) @ self.R_
        self.t_var_ = T.var(0, ddof=1) + 1e-300
        self.n_train_ = n
        self.n_use = A
        return self

    def predict_all(self, X):
        """Predictions for every number of LVs: (n, A)."""
        return (np.asarray(X, float) - self.x_mean_) @ self.coef_ + self.y_mean_

    def predict(self, X, a=None):
        a = self.n_use if a is None else a
        return (np.asarray(X, float) - self.x_mean_) @ self.coef_[:, a - 1] + self.y_mean_

    def diagnostics(self, X, a=None):
        """Hotelling T^2 (score space) and Q (squared X residual) for `a` LVs."""
        a = self.n_use if a is None else a
        Xc = np.asarray(X, float) - self.x_mean_
        T = Xc @ self.R_[:, :a]
        t2 = (T ** 2 / self.t_var_[:a]).sum(1)
        Q = ((Xc - T @ self.P_[:, :a].T) ** 2).sum(1)
        return t2, Q

    def leverage(self, X, a=None):
        t2, _ = self.diagnostics(X, a)
        return 1.0 / self.n_train_ + t2 / (self.n_train_ - 1)
