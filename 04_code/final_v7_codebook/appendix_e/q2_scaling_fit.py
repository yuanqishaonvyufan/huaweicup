"""Core Q2 five-parameter N-D fit and grouped holdout definitions."""

import itertools

import numpy as np
from scipy.optimize import least_squares


def predict_loss(params, n_params_b, d_tokens_b):
    floor, a, b, alpha, beta = params
    return floor + a * np.asarray(n_params_b) ** (-alpha) + b * np.asarray(d_tokens_b) ** (-beta)


def fit_scaling_law(frame, weights=None):
    n = frame.N_params_B.to_numpy()
    d = frame.D_tokens_B.to_numpy()
    y = frame.val_loss.to_numpy()
    weights = np.ones(len(frame)) if weights is None else np.asarray(weights)
    w = np.sqrt(weights / weights.mean())
    lower = np.array([0, 1e-8, 1e-8, 0.001, 0.001])
    upper = np.array([y.min(), 20, 20, 2, 2])
    starts = [
        [floor, 1, 1, alpha, beta]
        for floor, alpha, beta in itertools.product([0.5, 1.5], [0.1, 0.3, 0.7], [0.1, 0.3])
    ]
    fits = []
    for start in starts:
        fit = least_squares(
            lambda p: (predict_loss(p, n, d) - y) * w,
            np.clip(start, lower + 1e-9, upper - 1e-9),
            bounds=(lower, upper), method="trf", x_scale="jac", max_nfev=5000,
            ftol=1e-11, xtol=1e-11, gtol=1e-11,
        )
        if fit.success and np.isfinite(fit.fun).all():
            fits.append(fit)
    return min(fits, key=lambda fit: float(fit.fun @ fit.fun)).x


def validation_splits(frame):
    """Return LONO, forward-D-rank, and two-dimensional holdout masks."""
    plans = []
    for n in sorted(frame.N_params_B.unique()):
        plans.append(("LONO", f"N{n}", frame.N_params_B.ne(n), frame.N_params_B.eq(n)))
    for cut in (73, 110):
        plans.append(("FORWARD", f"Drank{cut}", frame.D_rank.lt(cut), frame.D_rank.ge(cut)))
    for n in sorted(frame.N_params_B.unique()):
        train = frame.N_params_B.ne(n) & frame.D_rank.lt(98)
        test = frame.N_params_B.eq(n) & frame.D_rank.ge(98)
        plans.append(("BLOCK2D", f"N{n}_D98", train, test))
    return plans


def compare_holdout(train, test):
    """Compare the scaling law with training-mean and log-linear baselines."""
    params = fit_scaling_law(train)
    design = lambda data: np.column_stack([
        np.ones(len(data)), np.log(data.N_params_B), np.log(data.D_tokens_B)
    ])
    log_coef, *_ = np.linalg.lstsq(design(train), train.val_loss, rcond=None)
    predictions = {
        "S1": predict_loss(params, test.N_params_B, test.D_tokens_B),
        "S0": np.full(len(test), train.val_loss.mean()),
        "Slog": design(test) @ log_coef,
    }
    metrics = {
        name: {
            "rmse": float(np.sqrt(np.mean((value - test.val_loss.to_numpy()) ** 2))),
            "mae": float(np.mean(np.abs(value - test.val_loss.to_numpy()))),
        }
        for name, value in predictions.items()
    }
    return params, predictions, metrics
