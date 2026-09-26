"""Core Q1 quality-score calculation; data loading is in the full support script."""

import numpy as np
from scipy.stats import spearmanr


def ecdf(reference, values):
    reference = np.sort(np.asarray(reference, dtype=float))
    reference = reference[np.isfinite(reference)]
    values = np.asarray(values, dtype=float)
    left = np.searchsorted(reference, values, side="left")
    right = np.searchsorted(reference, values, side="right")
    scores = (left + right) / (2 * len(reference))
    scores[~np.isfinite(values)] = np.nan
    return scores


def calculate_quality_scores(frame, train_mask, fields, core_fields):
    """Return Q_full under equal/redundancy weights and the five-signal DQ0.

    ``train_mask`` identifies the fixed A1 reference-training rows. For the
    four QuRating facets, ``fields`` contains the aggregate key ``qurater``;
    its source columns are qurater_facet_0 ... qurater_facet_3.
    """
    train_mask = np.asarray(train_mask, dtype=bool)
    n_rows = len(frame)
    core_u = np.column_stack([
        ecdf(frame.loc[train_mask, name], frame[name]) for name in core_fields
    ])
    dq0 = np.nanmean(core_u, axis=1)
    high_core = train_mask & (dq0 >= np.nanquantile(dq0[train_mask], 0.80))

    utilities = np.full((n_rows, len(fields)), np.nan, dtype=np.float32)
    for j, name in enumerate(fields):
        if name == "qurater":
            facets = []
            for k in range(4):
                raw = frame[f"qurater_facet_{k}"].to_numpy(dtype=float)
                rank = ecdf(raw[train_mask], raw)
                target = np.nanmedian(rank[high_core])
                facets.append(1 - np.abs(rank - target))
            utilities[:, j] = np.nanmean(facets, axis=0)
            continue

        raw = frame[name].to_numpy(dtype=float)
        if name in {"rps_doc_word_count", "rps_doc_num_sentences"}:
            raw = np.log1p(np.maximum(raw, 0))
        rank = ecdf(raw[train_mask], raw)
        if name in core_fields:
            utilities[:, j] = rank
        else:
            target = np.nanmedian(rank[high_core])
            utilities[:, j] = 1 - np.abs(rank - target)

    coverage = np.sum(np.isfinite(utilities), axis=1)
    utilities = np.where(np.isfinite(utilities), utilities, 0.5)
    weights_w0 = np.full(len(fields), 1 / len(fields))
    correlations = spearmanr(utilities[train_mask], axis=0).statistic
    redundancy = np.maximum(0, np.abs(correlations) - 0.5)
    np.fill_diagonal(redundancy, 0)
    weights_w1 = 1 / (1 + redundancy.sum(axis=1))
    weights_w1 /= weights_w1.sum()

    return {
        "Q_full_W0": utilities @ weights_w0,
        "Q_full_W1": utilities @ weights_w1,
        "DQ0": dq0,
        "coverage": coverage,
        "W1": weights_w1,
    }
