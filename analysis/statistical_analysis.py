"""Run-level statistical helpers for the replication package.

Only apply an inferential method when the experimental unit and raw observations
support it. Nested packet/event measurements must not be treated as independent
runs.
"""

import numpy as np
import pandas as pd
from scipy import stats


def bootstrap_median_ci(values, confidence_level=0.95, n_resamples=10000, seed=2026):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or len(values) < 2:
        raise ValueError("At least two independent run-level values are required.")

    result = stats.bootstrap(
        (values,),
        np.median,
        confidence_level=confidence_level,
        n_resamples=n_resamples,
        method="percentile",
        random_state=np.random.default_rng(seed),
    )
    return float(result.confidence_interval.low), float(result.confidence_interval.high)


def paired_service_test(df):
    """Paired mitigated-vs-unmitigated service comparison by pair_id."""
    required = {"pair_id", "condition", "throughput_mbps"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    pivot = df.pivot(index="pair_id", columns="condition", values="throughput_mbps").dropna()
    if not {"mitigated", "unmitigated"}.issubset(pivot.columns):
        raise ValueError("Both mitigated and unmitigated observations are required.")

    differences = pivot["mitigated"] - pivot["unmitigated"]
    statistic, p_value = stats.wilcoxon(
        pivot["mitigated"],
        pivot["unmitigated"],
        alternative="two-sided",
    )
    ci_low, ci_high = bootstrap_median_ci(differences.to_numpy())

    return {
        "n_pairs": int(len(pivot)),
        "median_difference_mbps": float(np.median(differences)),
        "bootstrap_95_ci_mbps": (ci_low, ci_high),
        "wilcoxon_w": float(statistic),
        "p_value": float(p_value),
    }


def timing_run_medians(df):
    """Reduce nested timing events to one median per independent run."""
    required = {"run_id", "L_D", "L_C", "L_E", "L_Total"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    run_level = df.groupby("run_id")[["L_D", "L_C", "L_E", "L_Total"]].median()

    rows = []
    for column in run_level.columns:
        values = run_level[column].to_numpy()
        ci_low, ci_high = bootstrap_median_ci(values)
        rows.append(
            {
                "metric": column,
                "n_runs": len(values),
                "median_ms": float(np.median(values)),
                "iqr_ms": float(np.percentile(values, 75) - np.percentile(values, 25)),
                "min_ms": float(np.min(values)),
                "max_ms": float(np.max(values)),
                "ci_low_ms": ci_low,
                "ci_high_ms": ci_high,
            }
        )

    return pd.DataFrame(rows)
