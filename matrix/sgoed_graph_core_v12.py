"""
SGOED-Relational v12.1 — Graph Core with Exact Spectral SVD Condensation
========================================================================
Implements the EXACT Graph equivalent of Matrix Tr(X^4):
1. Spectral SVD Condensation: Tr((W W^T)^2) = sum_i sigma_i^4
   (Directly maximizes the 4th moment of Singular Values -> drives Rank-1 Dominance!).
2. Quartic Directional Coupling: -g_xy * sum_a v_hat_a * sum_j W_aj^4
3. Fast O(N^2) computation using Frobenious norm of M = W @ W.T.

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-31
"""

import numpy as np
from numba import njit


@njit(fastmath=True)
def compute_spectral_trace_svd4(W: np.ndarray):
    """
    Computes Tr((W @ W^T)^2) = sum_i sigma_i^4 exactly in O(N^3).
    Let M = W @ W^T (symmetric positive semi-definite).
    Then Tr(M^2) = sum_{i,j} M[i,j]^2.
    """
    N = W.shape[0]
    M = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            s = 0.0
            for k in range(N):
                s += W[i, k] * W[j, k]
            M[i, j] = s

    tr_m2 = 0.0
    for i in range(N):
        for j in range(N):
            tr_m2 += M[i, j] ** 2

    return tr_m2


@njit(fastmath=True)
def compute_graph_action_v12(
    W: np.ndarray,
    d: int = 3,
    alpha: float = 0.5,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max: float = 6.0,
    g_xy: float = 1.0,
    lambda_cond: float = 0.05,
    eps: float = 1e-7,
):
    """
    Computes total action for v12.1 Graph with True SVD Quartic Condensation.
    """
    N = W.shape[0]

    # 1. Sparsity
    s_sparsity = 0.0
    for i in range(N):
        for j in range(N):
            if i != j:
                s_sparsity += alpha * (W[i, j] ** 2)

    # 2. Transitivity Loop (W^2 - W)^2
    s_trans = 0.0
    for i in range(N):
        for k in range(N):
            if i == k:
                continue
            w2_ik = 0.0
            for j in range(N):
                if j != i and j != k:
                    w2_ik += W[i, j] * W[j, k]
            s_trans += beta * ((w2_ik - W[i, k]) ** 2)

    # 3. Capacity Gate
    s_gate = 0.0
    out_deg = np.zeros(N)
    in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]
        if out_deg[i] > k_max:
            s_gate += lambda_gate * ((out_deg[i] - k_max) ** 2)
        if in_deg[i] > k_max:
            s_gate += lambda_gate * ((in_deg[i] - k_max) ** 2)

    # 4. Non-Linear Quartic Observer Coupling (W_aj^4)
    s_coupling = 0.0
    diff_s = np.zeros(d)
    sum_sq = 0.0
    for a in range(d):
        diff_s[a] = out_deg[a] - in_deg[a]
        sum_sq += diff_s[a] ** 2
    norm_v = np.sqrt(sum_sq) + eps

    for a in range(d):
        v_hat_a = diff_s[a] / norm_v
        sum_rest_quartic = 0.0
        for j in range(d, N):
            sum_rest_quartic += W[a, j] ** 4
        s_coupling += -g_xy * v_hat_a * sum_rest_quartic

    # 5. True Spectral SVD Condensation: -lambda_cond * Tr((W @ W.T)^2)
    s_cond = 0.0
    if lambda_cond > 0.0:
        svd_4th_moment = compute_spectral_trace_svd4(W)
        s_cond = -lambda_cond * svd_4th_moment

    return s_sparsity + s_trans + s_gate + s_coupling + s_cond


def compute_v12_invariants(W: np.ndarray, d: int = 3):
    """
    Computes physical invariants: SVD Ratio, Net Direction D, Alignment.
    """
    N = W.shape[0]

    # 1. Net Direction D
    D = 0.0
    F_net = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            diff = W[i, j] - W[j, i]
            if abs(diff) > 1e-4:
                D += np.sign(diff)
            F_net += diff

    # 2. Spectral Eigenvalue / SVD Condensation Ratio (sigma_1 / sigma_2)
    vals = np.linalg.svd(W, compute_uv=False)
    if len(vals) >= 2 and vals[1] > 1e-5:
        spectral_ratio = float(vals[0] / vals[1])
    else:
        spectral_ratio = 1.0

    # 3. Observer Flow Alignment
    out_deg = np.sum(W, axis=1)
    in_deg = np.sum(W, axis=0)
    obs_flow = np.mean(out_deg[:d] - in_deg[:d])
    sys_flow = np.mean(out_deg[d:] - in_deg[d:])
    aligned = 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.05) else 0.0

    return float(D), float(F_net), float(spectral_ratio), float(aligned)


@njit(fastmath=True)
def run_v12_simulation_numba(
    N: int = 16,
    d: int = 3,
    g_xy: float = 1.0,
    lambda_cond: float = 0.02,
    alpha: float = 0.5,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max_base: float = 6.0,
    n_therm: int = 40,
    n_measure: int = 40,
    step_size: float = 0.15,
    seed: int = 42,
):
    """
    Simulates v12 Graph with True Spectral Condensation.
    """
    np.random.seed(seed)
    k_max = k_max_base * np.sqrt(N / 8.0)

    W = np.random.uniform(0.05, 0.3, (N, N))
    for i in range(N):
        W[i, i] = 0.0

    current_action = compute_graph_action_v12(
        W, d, alpha, beta, lambda_gate, k_max, g_xy, lambda_cond
    )

    total_sweeps = n_therm + n_measure

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

                W[i, j] = new_val
                new_action = compute_graph_action_v12(
                    W, d, alpha, beta, lambda_gate, k_max, g_xy, lambda_cond
                )

                delta_s = new_action - current_action
                if delta_s <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-delta_s):
                    current_action = new_action
                else:
                    W[i, j] = old_val

    return W, current_action


def run_v12(N=16, d=3, g_xy=1.0, lambda_cond=0.02, n_therm=40, n_measure=40, seed=42):
    W, act = run_v12_simulation_numba(
        N=N, d=d, g_xy=g_xy, lambda_cond=lambda_cond,
        n_therm=n_therm, n_measure=n_measure, seed=seed
    )
    D, F_net, spec_ratio, align = compute_v12_invariants(W, d=d)
    return D, F_net, spec_ratio, align, W
