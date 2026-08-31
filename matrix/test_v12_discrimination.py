"""
Rigorous Discrimination Battery for v12 Graph Non-Linear Condensation.
Tests:
1. Baseline (Uncoupled, g_xy=0, lambda_cond=0)
2. Real Coupled v12 (g_xy=1.5, lambda_cond=0.15)
3. Shuffle Null Test (Permuting W values to verify Discrimination)
"""

import time
import numpy as np
from sgoed_graph_core_v12 import run_v12, compute_v12_invariants


def run_v12_discrimination_test():
    print("==========================================================================")
    print("   v12 Graph Non-Linear Condensation & Direction Discrimination Audit     ")
    print("==========================================================================")

    N = 16
    d = 3
    seeds = [42, 43, 44, 45, 46]

    # 1. Baseline: g_xy = 0.0, lambda_cond = 0.0
    print("\n--- 1. Baseline (Uncoupled Null: g_xy=0.0, lambda_cond=0.0) ---")
    base_D = []
    base_spec = []
    for s in seeds:
        D, F_net, spec, align, W = run_v12(N=N, d=d, g_xy=0.0, lambda_cond=0.0, seed=s)
        base_D.append(D)
        base_spec.append(spec)
    print(f"Baseline Net Direction D: {np.mean(base_D):+5.2f} +/- {np.std(base_D):4.2f}")
    print(f"Baseline Spectral Ratio : {np.mean(base_spec):5.2f} +/- {np.std(base_spec):4.2f}")

    # 2. Coupled v12 with Non-linear Quartic & Condensation
    print("\n--- 2. Coupled v12 (g_xy=1.5, lambda_cond=0.15) ---")
    real_D = []
    real_spec = []
    real_align = []
    shuffle_D = []
    shuffle_spec = []

    for s in seeds:
        D, F_net, spec, align, W = run_v12(N=N, d=d, g_xy=1.5, lambda_cond=0.15, seed=s)
        real_D.append(D)
        real_spec.append(spec)
        real_align.append(align)

        # Shuffle Test: randomly permute elements of W
        flat_W = W.flatten()
        np.random.shuffle(flat_W)
        W_shuffled = flat_W.reshape((N, N))
        for i in range(N):
            W_shuffled[i, i] = 0.0

        D_shuf, _, spec_shuf, _ = compute_v12_invariants(W_shuffled, d=d)
        shuffle_D.append(D_shuf)
        shuffle_spec.append(spec_shuf)

    print(f"Real v12 Net Direction D: {np.mean(real_D):+5.2f} +/- {np.std(real_D):4.2f}  [Shuffle Null: {np.mean(shuffle_D):+5.2f} +/- {np.std(shuffle_D):4.2f}]")
    print(f"Real Spectral Ratio     : {np.mean(real_spec):5.2f} +/- {np.std(real_spec):4.2f}  [Shuffle Null: {np.mean(shuffle_spec):5.2f} +/- {np.std(shuffle_spec):4.2f}]")
    print(f"Observer Flow Alignment : {np.mean(real_align)*100:5.1f}%")

    # Statistical Separation (Z-Score)
    z_spec = (np.mean(real_spec) - np.mean(base_spec)) / (np.std(base_spec) + 1e-6)
    print(f"\n>>> Spectral Condensation Separation: {z_spec:+5.1f} Sigma above Baseline! <<<")


if __name__ == "__main__":
    run_v12_discrimination_test()
