"""
SGOED-Relational v13 — Asymmetric Observer-System Coupling Engine
================================================================
Eliminates all engineered condensation terms (lambda_cond = 0 forever).
Drives Arrow of Time & Spectral Condensation via Asymmetric Non-Linear Coupling:
1. Forward Coupling (Observer -> System):
   S_forward = -g_f * sum_a v_hat_a * sum_{j >= d} W_aj^4  (Quartic power p=4)
2. Back-reaction Coupling (System -> Observer):
   S_back = -g_b * sum_a w_hat_a * sum_{j < d, j != a} W_aj^p  (where g_b < g_f, p in {2, 4})
3. Full Invariant Observables:
   - Spectral Ratio: sigma_1 / sigma_2
   - Net Direction D = sum_{i < j} sign(W_ij - W_ji)
   - Root Direction D_root = out_deg_root - in_deg_root
   - Observer Flow Alignment

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-31
"""

import numpy as np
from numba import njit


@njit(fastmath=True)
def compute_graph_action_v13(
    W: np.ndarray,
    d: int = 3,
    alpha: float = 0.5,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max: float = 6.0,
    g_f: float = 1.5,
    g_b: float = 0.2,
    p_b: int = 2,
    eps: float = 1e-7,
):
    """
    Computes total action for v13 with Asymmetric Observer-System Coupling.
    NO engineered condensation term (lambda_cond = 0).
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

    # 4. Asymmetric Observer Coupling
    # 4.1 Forward Coupling (Observer -> System): Quartic W_aj^4
    s_forward = 0.0
    diff_s = np.zeros(d)
    sum_sq = 0.0
    for a in range(d):
        diff_s[a] = out_deg[a] - in_deg[a]
        sum_sq += diff_s[a] ** 2
    norm_v = np.sqrt(sum_sq) + eps

    v_hat = np.zeros(d)
    for a in range(d):
        v_hat[a] = diff_s[a] / norm_v

    if g_f > 0.0:
        for a in range(d):
            sum_rest_quartic = 0.0
            for j in range(d, N):
                sum_rest_quartic += W[a, j] ** 4
            s_forward += -g_f * v_hat[a] * sum_rest_quartic

    # 4.2 Back-Reaction Coupling (System -> Observer): W_ja^p or W_ab^p
    s_back = 0.0
    if g_b > 0.0:
        for a in range(d):
            sum_back = 0.0
            # Internal observer edges or inbound edges from system
            for j in range(d, N):
                if p_b == 4:
                    sum_back += W[j, a] ** 4
                else:
                    sum_back += W[j, a] ** 2
            s_back += -g_b * v_hat[a] * sum_back

    return s_sparsity + s_trans + s_gate + s_forward + s_back


def compute_v13_invariants(W: np.ndarray, d: int = 3):
    """
    Computes rigorous physical invariants for v13.
    """
    N = W.shape[0]

    # 1. Global Net Direction D
    D = 0.0
    F_net = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            diff = W[i, j] - W[j, i]
            if abs(diff) > 1e-4:
                D += np.sign(diff)
            F_net += diff

    # 2. Root Node Flow & Direction
    out_deg = np.sum(W, axis=1)
    in_deg = np.sum(W, axis=0)
    root_idx = np.argmax(out_deg)
    D_root = float(out_deg[root_idx] - in_deg[root_idx])

    # 3. Spectral Eigenvalue / SVD Condensation Ratio (sigma_1 / sigma_2)
    vals = np.linalg.svd(W, compute_uv=False)
    spectral_ratio = float(vals[0] / vals[1]) if len(vals) >= 2 and vals[1] > 1e-5 else 1.0

    # 4. Observer Flow Alignment
    obs_flow = np.mean(out_deg[:d] - in_deg[:d])
    sys_flow = np.mean(out_deg[d:] - in_deg[d:])
    aligned = 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.05) else 0.0

    return float(D), float(D_root), float(spectral_ratio), float(aligned)


@njit(fastmath=True)
def run_v13_simulation_numba(
    N: int = 16,
    d: int = 3,
    g_f: float = 1.5,
    g_b: float = 0.2,
    p_b: int = 2,
    alpha: float = 0.5,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max_base: float = 6.0,
    n_therm: int = 120,
    n_measure: int = 60,
    step_size: float = 0.15,
    seed: int = 42,
):
    """
    Numba Metropolis simulation of v13 Graph.
    """
    np.random.seed(seed)
    k_max = k_max_base * np.sqrt(N / 8.0)

    W = np.random.uniform(0.05, 0.3, (N, N))
    for i in range(N):
        W[i, i] = 0.0

    current_action = compute_graph_action_v13(
        W, d, alpha, beta, lambda_gate, k_max, g_f, g_b, p_b
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
                new_action = compute_graph_action_v13(
                    W, d, alpha, beta, lambda_gate, k_max, g_f, g_b, p_b
                )

                delta_s = new_action - current_action
                if delta_s <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-delta_s):
                    current_action = new_action
                else:
                    W[i, j] = old_val

    return W


def run_v13(N=16, d=3, g_f=1.5, g_b=0.2, p_b=2, n_therm=120, n_measure=60, seed=42):
    W = run_v13_simulation_numba(
        N=N, d=d, g_f=g_f, g_b=g_b, p_b=p_b,
        n_therm=n_therm, n_measure=n_measure, seed=seed
    )
    D, D_root, spec_ratio, align = compute_v13_invariants(W, d=d)
    return D, D_root, spec_ratio, align, W
