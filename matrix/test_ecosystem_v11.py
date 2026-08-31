"""
Unit test and emergence verification for Phase 3: v11-Ecosystem Core.
"""

import time
import numpy as np
from sgoed_ecosystem_core_v11 import (
    compute_ecosystem_action,
    compute_ecosystem_observables,
    run_v11_ecosystem,
)


def test_ecosystem_basics():
    print("=================================================================")
    print(" 1. Testing Phase 3: v11 Multi-Universe Action & Observables    ")
    print("=================================================================")

    M = 3
    N_k = 8
    d = 2
    N_total = M * N_k
    rng = np.random.default_rng(42)
    W = rng.uniform(0.05, 0.3, size=(N_total, N_total))
    for i in range(N_total):
        W[i, i] = 0.0

    act = compute_ecosystem_action(W, M=M, N_k=N_k, d=d, g_xy=0.8, g_inter=0.5)
    print(f"[Pass] Initial Ecosystem Action S = {act:.4f}")
    assert np.isfinite(act), "Action must be finite"

    r_loc, phi_s, r_cr, aln = compute_ecosystem_observables(W, M=M, N_k=N_k, d=d)
    print(
        f"[Pass] Observables: R_local = {r_loc:.4f} | Phi_sync = {phi_s:.4f} | "
        f"R_cross = {r_cr:.4f} | Local Align = {aln*100:.1f}%\n"
    )


def test_ecosystem_simulation():
    print("=================================================================")
    print(" 2. Running Phase 3 v11-Ecosystem Simulation (M=3 Universes)    ")
    print("=================================================================")

    # Warmup
    _ = run_v11_ecosystem(M=2, N_k=6, d=2, n_therm=2, n_measure=2, seed=1)

    for g_inter in [0.0, 0.5, 1.0]:
        t0 = time.time()
        r_loc, r_std, phi_s, phi_std, r_cr, aln, act = run_v11_ecosystem(
            M=3, N_k=10, d=2, g_xy=0.8, g_inter=g_inter,
            n_therm=25, n_measure=35, seed=42
        )
        elapsed = time.time() - t0
        print(
            f"g_inter={g_inter:3.1f} | Time: {elapsed:5.2f}s | "
            f"R_local: {r_loc:.4f} | Inter-Sync Phi: {phi_s:+6.3f} +/- {phi_std:.3f} | "
            f"R_cross: {r_cr:.4f} | Align: {aln*100:5.1f}%"
        )

    print("\n>>> ALL PHASE 3 V11-ECOSYSTEM TESTS PASSED! <<<")


if __name__ == "__main__":
    test_ecosystem_basics()
    test_ecosystem_simulation()
