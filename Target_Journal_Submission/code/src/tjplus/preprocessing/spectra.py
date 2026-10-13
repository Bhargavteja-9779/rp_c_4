"""Per-spectrum preprocessing (stateless, hence leakage-free) for NIR spectra."""
import numpy as np
from scipy.signal import savgol_filter

def snv(X):
    X = np.asarray(X, float)
    return (X - X.mean(1, keepdims=True)) / (X.std(1, keepdims=True) + 1e-12)

PREPROCESSORS = {
    "none": lambda X: np.asarray(X, float),
    "snv": snv,
    "sg1": lambda X: savgol_filter(np.asarray(X, float), 11, 2, deriv=1, axis=1),
    "sg2": lambda X: savgol_filter(np.asarray(X, float), 13, 2, deriv=2, axis=1),
}

def preprocess(name, X):
    return PREPROCESSORS[name](X)
