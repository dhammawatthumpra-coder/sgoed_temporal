"""
SGOED-Relational Phase 2: v9-R Causal Hypergraph Core Engine
============================================================
A 3-Uniform Directed Hypergraph & Causal Poset Engine for Many-Body Spacetime Emergence.

Features:
- 3-Body Causal Triads: T[i, j, k] >= 0 representing multi-event relations i -> j -> k
- Normalized Observer Coupling & Feedback (Universal stability rule from v8-R)
- Symmetric Hyper-Capacity Gate + Observer-Extent Gate
- Fast Numba JIT Acceleration with Dynamic Scaling
- Causal Poset Dimension & Simplicial Geometry Analytics

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-30
"""

import numpy as np
from numba import njit


@njit(fastmath=True)
def compute_hyper_action_numba(
    T: np.ndarray,
    d: int,
    alpha: float = 0.5,
    beta: float = 0.05,
    lambda_gate: float = 10.0,
    k_max: float = 8.0,
    lambda_obs: float = 10.0,
    obs_gate_max: float = 16.0,
    g_xy: float = 0.8,
    g_yx: float = 0.0,
    eps: float = 1e-7,
):
    """
    Computes exact total action for 3-uniform directed hypergraph T of shape (N, N, N).
    """
    N = T.shape[0]

    # 1. Sparsity Energy: sum_{i!=j!=k} T_{ijk}^2
    s_sparsity = 0.0
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if k != i and k != j:
                    s_sparsity += alpha * (T[i, j, k] ** 2)

    # 2. Simplicial Closure / Associativity Energy: (sum_m T[i,j,m]*T[j,k,m] - T[i,j,k])^2
    s_trans = 0.0
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if k == i or k == j:
                    continue
                closure_sum = 0.0
                for m in range(N):
                    if m != i and m != j and m != k:
                        closure_sum += T[i, j, m] * T[j, k, m]
                s_trans += beta * ((closure_sum - T[i, j, k]) ** 2)

    # 3. Symmetric Capacity Gate (Out-degree & In-degree)
    s_gate = 0.0
    out_deg = np.zeros(N)
    in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if k != i and k != j:
                    val = T[i, j, k]
                    out_deg[i] += val
                    in_deg[k] += val

    for i in range(N):
        if out_deg[i] > k_max:
            s_gate += lambda_gate * ((out_deg[i] - k_max) ** 2)
        if in_deg[i] > k_max:
            s_gate += lambda_gate * ((in_deg[i] - k_max) ** 2)

    # 4. Normalized Directional Observer Coupling (Y -> X)
    diff_s = np.zeros(d)
    sum_diff_sq = 0.0
    for a in range(d):
        diff_s[a] = out_deg[a] - in_deg[a]
        sum_diff_sq += diff_s[a] ** 2
    norm_v = np.sqrt(sum_diff_sq) + eps

    s_coupling = 0.0
    for a in range(d):
        v_hat_a = diff_s[a] / norm_v
        sum_rest_sq = 0.0
        for j in range(d, N):
            for k in range(d, N):
                if j != k:
                    sum_rest_sq += T[a, j, k] ** 2
        s_coupling += -g_xy * v_hat_a * sum_rest_sq

    # 5. Normalized Observer Feedback (X -> Y) + Observer Extent Gate
    s_feedback = 0.0
    s_obs_gate = 0.0
    if d > 1:
        # Inbound flow from system into observer
        inbound = np.zeros(d)
        sum_inbound_sq = 0.0
        for a in range(d):
            for j in range(d, N):
                for k in range(d, N):
                    if j != k:
                        inbound[a] += T[j, k, a]
            sum_inbound_sq += inbound[a] ** 2
        norm_w = np.sqrt(sum_inbound_sq) + eps

        # Internal observer triad extent
        internal_obs_sum = 0.0
        n_obs_triads = d * (d - 1) * (d - 2) if d > 2 else 1
        for a in range(d):
            w_hat_a = inbound[a] / norm_w
            for b in range(d):
                if b == a:
                    continue
                for c in range(d):
                    if c != a and c != b:
                        t_sq = T[a, b, c] ** 2
                        internal_obs_sum += t_sq
                        if g_yx > 0.0:
                            s_feedback += -g_yx * t_sq * w_hat_a

        obs_extent = internal_obs_sum / float(n_obs_triads)
        if obs_extent > obs_gate_max:
            s_obs_gate = lambda_obs * ((obs_extent - obs_gate_max) ** 2)

    return s_sparsity + s_trans + s_gate + s_coupling + s_feedback + s_obs_gate


@njit(fastmath=True)
def compute_hyper_observables(T: np.ndarray, d: int, threshold: float = 0.2):
    """
    Computes Hypergraph Observables & Spacetime Dimension:
    - R_hyper: 3-body Causal Asymmetry Ratio
    - Alignment: Observer vs System Hyper-Flow
    - d_MM: Myrheim-Meyer Causal Set Dimension
    - L_max: Proper Time Longest Chain
    - obs_extent: Observer Internal Triad Extent
    """
    N = T.shape[0]

    # 1. 3-body Causal Asymmetry Ratio R_hyper
    diff_sum = 0.0
    tot_sum = 0.0
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(i + 1, N):
                if k == j:
                    continue
                diff_sum += abs(T[i, j, k] - T[k, j, i])
                tot_sum += T[i, j, k] + T[k, j, i]
    r_hyper = diff_sum / (tot_sum + 1e-7)

    # 2. Directed Degrees & Flow Alignment
    out_deg = np.zeros(N)
    in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if k != i and k != j:
                    out_deg[i] += T[i, j, k]
                    in_deg[k] += T[i, j, k]

    obs_flow = 0.0
    for a in range(d):
        obs_flow += (out_deg[a] - in_deg[a]) / d

    sys_flow = 0.0
    num_sys = N - d
    for j in range(d, N):
        sys_flow += (out_deg[j] - in_deg[j]) / num_sys

    alignment = 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.05) else 0.0

    # 3. Causal Poset & Myrheim-Meyer Dimension
    # Project 3-hyperedge to 2-node causal dominance: C_ik = 1 if sum_j (T_ijk - T_kji) > threshold
    C = np.zeros((N, N))
    for i in range(N):
        for k in range(N):
            if i != k:
                flow_ik = 0.0
                for j in range(N):
                    if j != i and j != k:
                        flow_ik += T[i, j, k] - T[k, j, i]
                if flow_ik > threshold:
                    C[i, k] = 1.0

    n_pairs = 0
    n_intervals = 0
    for i in range(N):
        for k in range(N):
            if C[i, k] == 1.0:
                n_pairs += 1
                for m in range(N):
                    if m != i and m != k and C[i, m] == 1.0 and C[m, k] == 1.0:
                        n_intervals += 1

    if n_pairs > 0:
        ratio = n_intervals / float(n_pairs)
        d_mm = 1.0 + 3.0 * ratio / (1.0 + ratio) * 2.5  # Dimension estimator
    else:
        d_mm = 1.0

    chain_len = np.zeros(N)
    for _ in range(N):
        for i in range(N):
            for k in range(N):
                if C[i, k] == 1.0 and chain_len[k] < chain_len[i] + 1:
                    chain_len[k] = chain_len[i] + 1
    l_max = float(np.max(chain_len))

    # 4. Observer Internal Extent
    internal_obs_sum = 0.0
    n_obs_triads = d * (d - 1) * (d - 2) if d > 2 else 1
    for a in range(d):
        for b in range(d):
            if b == a:
                continue
            for c in range(d):
                if c != a and c != b:
                    internal_obs_sum += T[a, b, c] ** 2
    obs_extent = internal_obs_sum / float(n_obs_triads)

    return r_hyper, alignment, d_mm, l_max, obs_extent


@njit(fastmath=True)
def run_v9_hypergraph_simulation_numba(
    N: int = 12,
    d: int = 3,
    g_xy: float = 0.8,
    g_yx: float = 0.0,
    alpha: float = 0.5,
    beta: float = 0.05,
    lambda_gate: float = 10.0,
    k_max_base: float = 8.0,
    lambda_obs: float = 10.0,
    obs_gate_max: float = 16.0,
    n_therm: int = 30,
    n_measure: int = 40,
    step_size: float = 0.15,
    seed: int = 42,
):
    """
    Monte Carlo Simulation for v9-R Causal Hypergraph.
    """
    np.random.seed(seed)
    k_max = k_max_base * np.sqrt(N / 8.0)

    # Initialize 3-hypergraph tensor T of shape (N, N, N)
    T = np.random.uniform(0.05, 0.3, (N, N, N))
    for i in range(N):
        for j in range(N):
            T[i, i, j] = 0.0
            T[i, j, i] = 0.0
            T[j, i, i] = 0.0

    current_action = compute_hyper_action_numba(
        T, d, alpha, beta, lambda_gate, k_max, lambda_obs, obs_gate_max, g_xy, g_yx
    )

    total_sweeps = n_therm + n_measure
    recorded_r = np.zeros(n_measure)
    recorded_align = np.zeros(n_measure)
    recorded_d_mm = np.zeros(n_measure)
    recorded_l_max = np.zeros(n_measure)
    recorded_extent = np.zeros(n_measure)
    record_idx = 0

    for sweep in range(total_sweeps):
        # Update triads
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                for k in range(N):
                    if k == i or k == j:
                        continue

                    old_val = T[i, j, k]
                    delta = np.random.normal(0.0, step_size)
                    new_val = old_val + delta
                    if new_val < 0.0:
                        continue

                    T[i, j, k] = new_val
                    new_action = compute_hyper_action_numba(
                        T, d, alpha, beta, lambda_gate, k_max, lambda_obs, obs_gate_max, g_xy, g_yx
                    )

                    delta_s = new_action - current_action
                    if delta_s <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-delta_s):
                        current_action = new_action
                    else:
                        T[i, j, k] = old_val

        # Record trajectory measurements
        if sweep >= n_therm:
            r_h, align, d_mm, l_max, obs_ext = compute_hyper_observables(T, d)
            recorded_r[record_idx] = r_h
            recorded_align[record_idx] = align
            recorded_d_mm[record_idx] = d_mm
            recorded_l_max[record_idx] = l_max
            recorded_extent[record_idx] = obs_ext
            record_idx += 1

    return (
        float(np.mean(recorded_r)),
        float(np.std(recorded_r)),
        float(np.mean(recorded_align)),
        float(np.mean(recorded_d_mm)),
        float(np.mean(recorded_l_max)),
        float(np.mean(recorded_extent)),
        float(current_action),
    )


def run_v9(N=12, d=3, g_xy=0.8, g_yx=0.0, n_therm=30, n_measure=40, seed=42):
    """Python wrapper for v9-R Hypergraph simulation."""
    return run_v9_hypergraph_simulation_numba(
        N=N, d=d, g_xy=g_xy, g_yx=g_yx,
        n_therm=n_therm, n_measure=n_measure, seed=seed
    )
