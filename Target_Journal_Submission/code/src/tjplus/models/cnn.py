"""Small 1D-CNN regressor for NIR spectra (model-class generalisation; mango only)."""
import numpy as np
import torch
from torch import nn
from ..preprocessing.spectra import snv

class Net(nn.Module):
    def __init__(self, p, p_drop=0.2):
        super().__init__()
        self.f = nn.Sequential(
            nn.Conv1d(1, 16, 7, padding=3), nn.ReLU(),
            nn.Conv1d(16, 32, 7, stride=2, padding=3), nn.ReLU(), nn.Dropout(p_drop),
            nn.Flatten(), nn.Linear(32 * ((p + 1) // 2), 64), nn.ReLU(), nn.Dropout(p_drop), nn.Linear(64, 1))

    def forward(self, x):
        return self.f(x[:, None, :])[:, 0]

class CNNRegressor:
    def __init__(self, epochs=150, lr=1e-3, batch=128, seed=0, device="cpu", patience=20):
        self.epochs, self.lr, self.batch, self.seed, self.device, self.patience = epochs, lr, batch, seed, device, patience

    def _prep(self, X):
        Z = snv(X)
        return (Z - self.mu_) / self.sd_

    def fit(self, X, y, X_val, y_val):
        torch.manual_seed(self.seed); np.random.seed(self.seed)
        Z = snv(X); self.mu_, self.sd_ = Z.mean(0), Z.std(0) + 1e-8
        self.ym_, self.ys_ = y.mean(), y.std()
        Xt = torch.tensor(self._prep(X), dtype=torch.float32); yt = torch.tensor((y - self.ym_) / self.ys_, dtype=torch.float32)
        Xv = torch.tensor(self._prep(X_val), dtype=torch.float32); yv = (y_val - self.ym_) / self.ys_
        self.net = Net(X.shape[1]).to(self.device)
        opt = torch.optim.Adam(self.net.parameters(), lr=self.lr, weight_decay=1e-5)
        g = torch.Generator().manual_seed(self.seed)
        best, best_state, wait, self.history_ = np.inf, None, 0, []
        for ep in range(self.epochs):
            self.net.train()
            perm = torch.randperm(len(Xt), generator=g)
            tl = 0.0
            for i in range(0, len(Xt), self.batch):
                idx = perm[i:i + self.batch]
                opt.zero_grad()
                loss = ((self.net(Xt[idx].to(self.device)) - yt[idx].to(self.device)) ** 2).mean()
                loss.backward(); opt.step(); tl += loss.item() * len(idx)
            self.net.eval()
            with torch.no_grad():
                vl = float(((self.net(Xv.to(self.device)).cpu().numpy() - yv) ** 2).mean())
            self.history_.append((ep, tl / len(Xt), vl))
            if vl < best - 1e-6:
                best, wait = vl, 0
                best_state = {k: v.detach().clone() for k, v in self.net.state_dict().items()}
            else:
                wait += 1
                if wait >= self.patience:
                    break
        self.net.load_state_dict(best_state); self.net.eval()
        return self

    def predict(self, X):
        with torch.no_grad():
            Z = torch.tensor(self._prep(X), dtype=torch.float32).to(self.device)
            return self.net(Z).cpu().numpy() * self.ys_ + self.ym_

    def predict_mc(self, X, T=100, seed=0):
        torch.manual_seed(seed)
        self.net.train()  # enable dropout
        with torch.no_grad():
            Z = torch.tensor(self._prep(X), dtype=torch.float32).to(self.device)
            P = np.stack([self.net(Z).cpu().numpy() for _ in range(T)]) * self.ys_ + self.ym_
        self.net.eval()
        return P.mean(0), P.var(0)

    def n_params(self):
        return sum(p.numel() for p in self.net.parameters())
