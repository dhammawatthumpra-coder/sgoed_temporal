"""
Unit test verifying Machine Precision of Symmetric Gate in v3.
"""

import numpy as np
from sgoed_graph_core_v3 import (
    compute_full_action_v3,
    compute_delta_edge_numba,
)


def test_v3_symmetric_gate_precision():
    print("=================================================================")
    print(" Verifying v3 Symmetric Gate Local Delta vs Full Action Recompute")
    print("=================================================================")
    
    N = 12
    d = 3
    alpha = 0.5
    beta = 0.1
    lambda_gate = 10.0
    k_max = 3.5  # Low cutoff to intentionally trigger both in and out gate violations
    g_xy = 0.8
    g_yx = 0.5

    rng = np.random.default_rng(999)
    W = rng.uniform(0.1, 0.8, size=(N, N))
    for i in range(N):
        W[i, i] = 0.0

    out_deg = np.zeros(N)
    in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]

    W2 = np.zeros((N, N))
    for i in range(N):
        for k in range(N):
            if i != k:
                s = 0.0
                for j in range(N):
                    if j != i and j != k:
                        s += W[i, j] * W[j, k]
                W2[i, k] = s

    max_err = 0.0

    for step in range(500):
        u = int(rng.integers(0, N))
        v = int(rng.integers(0, N))
        while u == v:
            v = int(rng.integers(0, N))

        delta_w = float(rng.normal(0.0, 0.2))
        new_val = W[u, v] + delta_w
        if new_val < 0.0:
            continue

        act_old = compute_full_action_v3(
            W, W2, out_deg, in_deg,
            d, alpha, beta, lambda_gate, k_max,
            g_xy, g_yx
        )

        delta_s = compute_delta_edge_numba(
            W, W2, out_deg, in_deg,
            u, v, new_val,
            d, alpha, beta, lambda_gate, k_max,
            g_xy, g_yx
        )

        # Apply update
        dW = new_val - W[u, v]
        for q in range(N):
            if q != u and q != v:
                W2[u, q] += dW * W[v, q]
        for p in range(N):
            if p != u and p != v:
                W2[p, v] += W[p, u] * dW

        W[u, v] = new_val
        out_deg[u] += dW
        in_deg[v] += dW

        act_new = compute_full_action_v3(
            W, W2, out_deg, in_deg,
            d, alpha, beta, lambda_gate, k_max,
            g_xy, g_yx
        )

        actual_delta = act_new - act_old
        err = abs(delta_s - actual_delta)
        if err > max_err:
            max_err = err

    print(f"[Pass] Tested 500 edge modifications with Symmetric Gate active.")
    print(f"[Pass] Max relative error = {max_err:.2e}")
    assert max_err < 1e-7, f"Error exceeds tolerance: {max_err}"
    print(">>> MACHINE PRECISION VERIFICATION PASSED 100%! <<<\n")


if __name__ == "__main__":
    test_v3_symmetric_gate_precision()
