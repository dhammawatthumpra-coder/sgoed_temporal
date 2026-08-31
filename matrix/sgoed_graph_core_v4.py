"""
SGOED-Relational Core v4 — Anneal Support & Corrected Thermalization
=====================================================================
Extends v3 (sgoed_graph_core_v3.py) without modifying it. Adds:

1. W_init parameter: carry the graph state across g_yx (anneal) so a TRUE
   hysteresis loop (memory effect) can be measured, not just a fresh-init scan.
2. Returns W: the final graph is exposed so the caller can feed it as W_init
   of the next chain step.
3. Corrected thermalization default: n_therm=240 (v3 used 35, which we found
   is far from equilibrium — the observer extent was still growing at
   n_therm=120 and only plateaus around n_therm >= 240, extent ~16).

Reuses the machine-precision delta/full-action kernels from v3 (verified to
<1e-13 relative error in test_v3_symmetric_gate.py).

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-30
"""

import numpy as np
from numba import njit

from sgoed_graph_core_v3 import (
    compute_coupling_numba,
    compute_feedback_numba,
    compute_full_action_v3,
    compute_delta_edge_numba,
    compute_spacetime_dimensions,
)


@njit(fastmath=True)
def _recalc_degrees(W, N):
    out_deg = np.zeros(N)
    in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]
    return out_deg, in_deg


@njit(fastmath=True)
def _recalc_W2(W, N):
    W2 = np.zeros((N, N))
    for i in range(N):
        for k in range(N):
            if i != k:
                s = 0.0
                for j in range(N):
                    if j != i and j != k:
                        s += W[i, j] * W[j, k]
                W2[i, k] = s
    return W2


@njit(fastmath=True)
def run_v4_numba(
    N, d, g_xy, g_yx,
    alpha, beta, lambda_gate, k_max_base,
    n_therm, n_measure, step_size, seed,
    W_init, use_init
):
    """Run v4. use_init=0 -> random init (reproduces v3); use_init=1 -> anneal
    from W_init. Returns (..., W_final)."""
    np.random.seed(seed)
    k_max = k_max_base * np.sqrt(N / 8.0)

    if use_init == 1:
        W = W_init.copy()
    else:
        W = np.random.uniform(0.1, 0.5, (N, N))
        for i in range(N):
            W[i, i] = 0.0
    out_deg, in_deg = _recalc_degrees(W, N)
    W2 = _recalc_W2(W, N)

    total_sweeps = n_therm + n_measure
    recorded_r = np.zeros(n_measure)
    recorded_align = np.zeros(n_measure)
    recorded_d_mm = np.zeros(n_measure)
    recorded_l_max = np.zeros(n_measure)
    recorded_obs_extent = np.zeros(n_measure)
    record_idx = 0

    for sweep in range(total_sweeps):
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                old_val = W[i, j]
                delta = np.random.normal(0.0, step_size)
                new_val = old_val + delta
                if new_val < 0.0:
                    continue
                dS = compute_delta_edge_numba(
                    W, W2, out_deg, in_deg, i, j, new_val,
                    d, alpha, beta, lambda_gate, k_max, g_xy, g_yx
                )
                if dS <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-dS):
                    dW = new_val - old_val
                    for q in range(N):
                        if q != i and q != j:
                            W2[i, q] += dW * W[j, q]
                    for p in range(N):
                        if p != i and p != j:
                            W2[p, j] += W[p, i] * dW
                    W[i, j] = new_val
                    out_deg[i] += dW
                    in_deg[j] += dW

        if sweep >= n_therm:
            diff_sum = 0.0
            tot_sum = 0.0
            for i in range(N):
                for j in range(i + 1, N):
                    diff_sum += abs(W[i, j] - W[j, i])
                    tot_sum += W[i, j] + W[j, i]
            r_causal = diff_sum / (tot_sum + 1e-7)

            obs_flow = 0.0
            for a in range(d):
                obs_flow += (out_deg[a] - in_deg[a]) / d
            sys_flow = 0.0
            num_sys = N - d
            for j in range(d, N):
                sys_flow += (out_deg[j] - in_deg[j]) / num_sys
            align = 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.1) else 0.0

            d_mm, l_max = compute_spacetime_dimensions(W)

            obs_internal_sum = 0.0
            for a in range(d):
                for b in range(d):
                    if a != b:
                        obs_internal_sum += W[a, b] ** 2
            obs_extent = obs_internal_sum / (d * (d - 1) if d > 1 else 1.0)

            recorded_r[record_idx] = r_causal
            recorded_align[record_idx] = align
            recorded_d_mm[record_idx] = d_mm
            recorded_l_max[record_idx] = l_max
            recorded_obs_extent[record_idx] = obs_extent
            record_idx += 1

    return (
        float(np.mean(recorded_r)),
        float(np.std(recorded_r)),
        float(np.mean(recorded_align)),
        float(np.mean(recorded_d_mm)),
        float(np.mean(recorded_l_max)),
        float(np.mean(recorded_obs_extent)),
        W,
    )


def run_v4(N=16, d=3, g_xy=0.8, g_yx=0.0,
           alpha=0.5, beta=0.1, lambda_gate=10.0, k_max_base=5.0,
           n_therm=240, n_measure=40, step_size=0.15, seed=42,
           W_init=None):
    """v4 entry point. If W_init is None, initialize randomly (reproducing v3);
    otherwise anneal from the supplied graph. Returns a tuple of
    (mean_r, std_r, align, d_mm, l_max, obs_extent, W_final)."""
    if W_init is None:
        W_init = np.zeros((N, N))
        use_init = 0
    else:
        use_init = 1
    return run_v4_numba(
        N, d, g_xy, g_yx,
        alpha, beta, lambda_gate, k_max_base,
        n_therm, n_measure, step_size, seed,
        W_init, use_init
    )
