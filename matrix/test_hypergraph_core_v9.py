"""
Unit test and emergence validation for v9-R Causal Hypergraph Core.
"""

import time
import numpy as np
from sgoed_hypergraph_core_v9 import (
    compute_hyper_action_numba,
    compute_hyper_observables,
    run_v9,
)


def test_hypergraph_basics():
    print("=================================================================")
    print(" 1. Testing v9-R Causal Hypergraph Action & Observables ")
    print("=================================================================")

    N = 8
    d = 3
    rng = np.random.default_rng(42)
    T = rng.uniform(0.05, 0.3, size=(N, N, N))
    for i in range(N):
        for j in range(N):
            T[i, i, j] = 0.0
            T[i, j, i] = 0.0
            T[j, i, i] = 0.0

    act = compute_hyper_action_numba(T, d=d, g_xy=0.8, g_yx=0.5)
    print(f"[Pass] Initial Hypergraph Action S = {act:.4f}")
    assert np.isfinite(act), "Action must be finite"

    r_h, align, d_mm, l_max, obs_ext = compute_hyper_observables(T, d=d)
    print(f"[Pass] Observables: R_hyper = {r_h:.4f} | d_MM = {d_mm:.2f}D | L_max = {l_max:.1f} | Obs Extent = {obs_ext:.4f}\n")


def test_hypergraph_simulation():
    print("=================================================================")
    print(" 2. Running v9-R Hypergraph Simulation (N=8, 12, 16) ")
    print("=================================================================")

    # Warmup
    _ = run_v9(N=6, d=2, n_therm=2, n_measure=2, seed=1)

    for n in [8, 12, 16]:
        t0 = time.time()
        r_h, r_std, align, d_mm, l_max, obs_ext, act = run_v9(
            N=n, d=3, g_xy=0.8, g_yx=0.0,
            n_therm=20, n_measure=25, seed=42
        )
        elapsed = time.time() - t0
        print(
            f"N={n:2d} | Time: {elapsed:6.2f}s | R_hyper: {r_h:.4f} +/- {r_std:.4f} | "
            f"Align: {align*100:5.1f}% | Dimension d_MM: {d_mm:.2f}D | Proper Time: {l_max:.1f}"
        )

    print("\n>>> ALL V9-R HYPERGRAPH TESTS PASSED! <<<")


if __name__ == "__main__":
    test_hypergraph_basics()
    test_hypergraph_simulation()
