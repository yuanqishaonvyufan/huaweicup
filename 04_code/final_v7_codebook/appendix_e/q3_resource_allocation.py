"""Core Q3 loss, FLOPs budget, and bounded N-D-quality allocation functions."""

import numpy as np
from scipy.optimize import brentq, minimize_scalar


def loss(n, d, p):
    return p["E"] + p["A"] * n ** (-p["alpha"]) + p["B"] * d ** (-p["beta"])


def quality_cost(q, family):
    if family == "exponential":
        return 1e7 * np.exp(6 * q)
    if family == "power":
        return 5e9 * q**4
    if family == "logarithmic":
        return 2e9 * np.log1p(10 * q)
    raise ValueError(family)


def resource_cost(n, d, q, context_length, family="exponential", q0=0.5):
    return (
        6e18 * n * d
        + 0.0002 * context_length * 1e18 * n * d
        + 1e9 * d * max(0.0, quality_cost(q, family) - quality_cost(q0, family))
    )


def analytic_nd_optimum(budget_1e18, context_length, p, n_bounds, d_bounds):
    """Optimal N-D split at fixed quality under the rectangular support bounds."""
    k = 6 + 0.0002 * context_length
    total = budget_1e18 / k
    n0, n1 = n_bounds
    d0, d1 = d_bounds
    if total < n0 * d0:
        return None
    if total >= n1 * d1:
        return n1, d1
    lo, hi = max(n0, total / d1), min(n1, total / d0)
    n = np.clip(
        (p["alpha"] * p["A"] / (p["beta"] * p["B"])) ** (1 / (p["alpha"] + p["beta"]))
        * total ** (p["beta"] / (p["alpha"] + p["beta"])),
        lo, hi,
    )
    return float(n), float(total / n)


def optimize_quality_and_split(budget_1e18, context_length, family, quality_return,
                               p, n_bounds, d_bounds, q_cap=1.0):
    """Search quality, solving the conditional N-D allocation at each q."""
    if quality_return == 0:
        n, d = analytic_nd_optimum(budget_1e18, context_length, p, n_bounds, d_bounds)
        return n, d, 0.5, loss(n, d, p)

    k = 6 + 0.0002 * context_length
    q_hi = q_cap
    n0, n1 = n_bounds
    d0, d1 = d_bounds

    def fixed_q(q):
        r = (quality_cost(q, family) - quality_cost(0.5, family)) / 1e9
        if (k * n0 + r) * d0 > budget_1e18:
            return None
        hi = min(n1, (budget_1e18 / d0 - r) / k)
        lo = max(n0, min(hi, (budget_1e18 / d1 - r) / k))

        def gradient(log_n):
            n = np.exp(log_n)
            d = budget_1e18 / (k * n + r)
            return (-p["alpha"] * p["A"] * n ** (-p["alpha"])
                    + p["beta"] * p["B"] * d ** (-p["beta"]) * k * n / (k * n + r))

        if hi <= lo * (1 + 1e-12) or gradient(np.log(lo)) >= 0:
            n = lo
        elif gradient(np.log(hi)) <= 0:
            n = hi
        else:
            n = np.exp(brentq(gradient, np.log(lo), np.log(hi), xtol=1e-13))
        return float(n), float(min(d1, budget_1e18 / (k * n + r)))

    if fixed_q(q_hi) is None:
        q_hi = brentq(
            lambda q: (k * n0 + (quality_cost(q, family) - quality_cost(0.5, family)) / 1e9)
            * d0 - budget_1e18,
            0.5, q_cap,
        )

    def objective(q):
        nd = fixed_q(q)
        return loss(*nd, p) - quality_return * (q - 0.5) if nd else 1e10

    grid = np.linspace(0.5, q_hi, 101)
    values = np.array([objective(q) for q in grid])
    candidates = [(0.5, values[0]), (q_hi, values[-1])]
    for i in range(1, len(grid) - 1):
        if values[i] <= values[i - 1] and values[i] <= values[i + 1]:
            result = minimize_scalar(
                objective, bounds=(grid[i - 1], grid[i + 1]), method="bounded",
                options={"xatol": 1e-10},
            )
            candidates.append((result.x, result.fun))
    minimum = min(value for _, value in candidates)
    best_q = min(q for q, value in candidates if value <= minimum + 1e-10)
    n, d = fixed_q(best_q)
    return n, d, float(best_q), float(objective(best_q))
