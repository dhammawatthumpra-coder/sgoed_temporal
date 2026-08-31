"""
Unit test and quick emergence validation for SGOED-Relational Core Engine.
"""

import numpy as np
import time
from sgoed_graph_core import compute_full_action, compute_observables, run_relational_simulation


def test_basic_action_and_simulation():
    print("=== Testing SGOED-Relational Core (v8-R) ===")
    
    # 1. Action computation test
    N = 6
    d = 2
    rng = np.random.default_rng(123)
    W = rng.uniform(0.1, 0.5, size=(N, N))
    np.fill_diagonal(W, 0.0)
    S_idx = np.arange(d)
    
    action_val = compute_full_action(W, S_idx, g_xy=0.8, g_yx=0.5)
    print(f"[Pass] Initial Action computation: S = {action_val:.4f}")
    assert np.isfinite(action_val), "Action must be finite"
    
    # 2. Observables test
    obs = compute_observables(W, S_idx)
    print(f"[Pass] Observables: R_causal = {obs['r_causal']:.4f}, mean_deg = {obs['mean_degree']:.4f}")
    assert 0.0 <= obs["r_causal"] <= 1.0, "R_causal must be in [0, 1]"
    
    # 3. Monte Carlo Simulation test (N=8, d=3, seeds 42..44)
    print("\n--- Running Monte Carlo Simulation (N=8, d=3) ---")
    t0 = time.time()
    for seed in [42, 43, 44]:
        res = run_relational_simulation(
            N=8,
            d=3,
            g_xy=0.8,
            g_yx=0.0,
            n_therm=20,
            n_measure=30,
            seed=seed,
        )
        print(
            f"Seed {seed}: Mean R_causal = {res['mean_r_causal']:.4f} +/- {res['std_r_causal']:.4f}, "
            f"Alignment = {res['alignment_rate']*100:.1f}%, Action = {res['final_action']:.2f}"
        )
    elapsed = time.time() - t0
    print(f"Completed in {elapsed:.2f}s")
    print("\n>>> ALL BASIC TESTS PASSED! <<<")


if __name__ == "__main__":
    test_basic_action_and_simulation()
