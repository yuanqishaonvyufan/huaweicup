"""Core Q1 M1 fit/predict functions; 13 response columns are supplied as y."""

import numpy as np
from scipy.linalg import helmert


def fit_m1(p, y):
    """Fit linear mixture response in 16 orthonormal coordinates."""
    basis = helmert(17, full=False).T
    p_mean = p.mean(axis=0)
    y_mean = y.mean(axis=0)
    z = (p - p_mean) @ basis
    coef, *_ = np.linalg.lstsq(z, y - y_mean, rcond=None)
    return {"basis": basis, "p_mean": p_mean, "y_mean": y_mean, "coef": coef}


def predict_m1(model, p):
    z = (p - model["p_mean"]) @ model["basis"]
    return model["y_mean"] + z @ model["coef"]
