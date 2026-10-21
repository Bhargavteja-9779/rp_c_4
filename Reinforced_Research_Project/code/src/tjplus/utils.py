"""Small utilities: seeding, hardware detection, logging, timing."""
import logging, os, random, time
from contextlib import contextmanager
import numpy as np

def set_seed(seed: int):
    random.seed(seed); np.random.seed(seed % (2**32 - 1))
    try:
        import torch
        torch.manual_seed(seed)
    except ImportError:
        pass

def detect_device() -> str:
    """Return 'cuda', 'mps' or 'cpu' depending on available hardware (no NVIDIA assumption)."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"

def get_logger(name="tjplus", logfile=None):
    log = logging.getLogger(name)
    if not log.handlers:
        log.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        h = logging.StreamHandler(); h.setFormatter(fmt); log.addHandler(h)
        if logfile:
            os.makedirs(os.path.dirname(logfile), exist_ok=True)
            fh = logging.FileHandler(logfile); fh.setFormatter(fmt); log.addHandler(fh)
    return log

@contextmanager
def timer(store: dict, key: str):
    t0 = time.perf_counter()
    yield
    store[key] = store.get(key, 0.0) + time.perf_counter() - t0
