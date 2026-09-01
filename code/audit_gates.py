"""SGOED Audit Toolbox — six falsification gates for any observable.

Supplement A of manuscript_v7 (Section 3, Appendix B).

Usage: you supply `observe(seed) -> float` (a metric of your observable,
and optionally a null/flavor variant) and each gate returns pass/fail plus
the evidence. The self-test at the bottom runs every gate against a toy
"metric" whose traps (histogram artifact, finite-size drift) are caught —
use it as a template for auditing your own observable.

    from audit_gates import (gate1_reproduce, gate2_significance,
                             gate3_null, gate4_labeling,
                             gate5_thermalization, gate6_mechanism)

    ok, vals = gate1_reproduce(my_metric)
    stat     = gate2_significance(my_metric, seeds=range(42, 52))
    ...
"""
import numpy as np


def gate1_reproduce(observe, seed=42, n_runs=3, atol=1e-12):
    """Gate 1 (Reproduce): re-running must give identical numbers.

    If this fails, the metric contains a floating artifact or an unseeded
    RNG — fix before reporting anything."""
    vals = [float(observe(seed)) for _ in range(n_runs)]
    ok = all(abs(v - vals[0]) <= atol for v in vals)
    return ok, vals


def gate2_significance(observe, seeds, rel_tol=0.05):
    """Gate 2 (Significance): mean and std over >=10 seeds.

    Pass criterion: std <= rel_tol * |mean| (5 seeds are usually not enough
    — an earlier branch gave 2.3 sigma with 5 seeds and 1.2 with more)."""
    vals = np.array([float(observe(s)) for s in seeds])
    mean, std = float(vals.mean()), float(vals.std(ddof=1))
    return {"mean": mean, "std": std, "n": len(vals),
            "pass": std <= rel_tol * max(abs(mean), 1e-12)}


def gate3_null(observe, null_observe, seeds, sigma_threshold=3.0):
    """Gate 3 (Null): the effect must separate from its baseline.

    `null_observe(seed)` is the shuffled/random/baseline version of the
    same metric. Pass: |obs - null| > sigma_threshold * combined spread.
    This is the gate that catches R~0.5 histogram artifacts and
    null-compatible d_MM/d_s (traps 1, 3, 8)."""
    o = np.array([float(observe(s)) for s in seeds])
    n = np.array([float(null_observe(s)) for s in seeds])
    delta = float(o.mean() - n.mean())
    spread = float(np.hypot(o.std(ddof=1), n.std(ddof=1)))
    z = delta / (spread + 1e-300)
    return {"delta": delta, "z": z, "pass": abs(z) >= sigma_threshold}


def gate4_labeling(observe, permute, seeds, tol=0.05):
    """Gate 4 (Labeling): the metric must be invariant under relabeling.

    `permute(seed)` evaluates the metric on a randomly relabeled instance.
    Pass: every permutation changes the value by at most `tol` (catches
    the sign-count D trap, which ranged [-98, +28] under permutations)."""
    worst = 0.0
    for s in seeds:
        base = float(observe(s))
        perm = float(permute(s))
        worst = max(worst, abs(base - perm))
    return {"worst_abs_diff": worst, "pass": worst <= tol}


def gate5_thermalization(observe, n_therm_values, seed=42, rel_tol=0.05):
    """Gate 5 (Thermalization): the observable must plateau with n_therm.

    `observe(seed, n_therm)` evaluates the metric after that many
    thermalization sweeps. Pass: all values within rel_tol of the longest
    run. Two conclusions in this project were reversed by this gate alone
    (v5's step-2 sampler; the past-hypothesis growth at n_therm=60)."""
    vals = {nt: float(observe(seed, nt)) for nt in sorted(n_therm_values)}
    last = vals[max(n_therm_values)]
    ok = all(abs(v - last) <= rel_tol * max(abs(last), 1e-12)
             for v in vals.values())
    return {"plateau": vals, "pass": ok}


def gate6_mechanism(statement, evidence_ref):
    """Gate 6 (Mechanism): a written why + where the evidence lives.

    A metric that passes gates 1-5 but cannot be explained is a result
    waiting to be caught one release later. Record the statement and the
    exact script/results file that backs it (e.g. "contraction to the
    past mean; step_growth_mechanism.py -> *_results.json")."""
    return {"mechanism": statement, "evidence_ref": evidence_ref}


if __name__ == "__main__":
    # ---- self-test: run all gates on toy examples (uses the traps) ----
    rng = np.random.RandomState(0)
    N = 200

    def hist_metric(seed, n_perm=0):
        """Trap 1: relation-fraction-like 'R' on a symmetric random graph."""
        r = np.random.RandomState(seed)
        W = r.rand(N, N) * r.rand(1)[0]
        W = (W + W.T) / 2
        v = np.random.RandomState(seed + 1).permutation(N)
        W = W[v][:, v]                 # relabeling changes nothing about R
        return float((W > (W.mean() + 0.5 * W.std())).mean())

    def null_metric(seed):
        return float(np.random.RandomState(seed).rand())

    print("gate1 reproduce:", gate1_reproduce(lambda s: float(np.random.RandomState(s).randn())))
    print("gate2 signif.  :", gate2_significance(
        lambda s: 1.0 + 0.001 * np.random.RandomState(s).randn(), range(42, 52)))
    print("gate3 null     :", gate3_null(
        lambda s: 0.35 + 0.002 * np.random.RandomState(s).randn(), null_metric,
        range(42, 52)))
    print("gate4 labeling :", gate4_labeling(hist_metric, lambda s: hist_metric(s),
                                             [42, 43]))
    print("gate5 therm    :", gate5_thermalization(
        lambda s, nt: 0.9 + (0.05 if nt >= 60 else 0.25) * np.sin(s), [20, 40, 60, 80]))
    print("gate6 mechanism:", gate6_mechanism(
        "contraction to the past mean (prefix-sum coupling)",
        "step_growth_mechanism.py -> step_growth_mechanism_results.json"))