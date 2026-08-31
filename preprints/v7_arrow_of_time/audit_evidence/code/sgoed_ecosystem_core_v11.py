"""
SGOED-Relational Phase 3: v11-Ecosystem Core Engine
===================================================
A Distributed Multi-Universe Ecosystem for Relational Time Synchronization & Relativity.
(Documented in SGOED_v10_ecosystem_notes.md)

Features:
- M Distributed Sub-Universes (G_1, G_2, ..., G_M), each with N_k nodes.
- Local Observers S_1, S_2, ..., S_M (d nodes each) generating local temporal directions.
- Inter-Universe Causal Bridges & Entanglement Coupling (g_inter).
- Relational Time Synchronization Index (Phi_sync) and Cross-Universe Causal Flow.
- Numba JIT Acceleration with Incremental Matrix Block Updates.

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-31
"""

import numpy as np
from numba import njit


@njit(fastmath=True)
def compute_ecosystem_action(
    W: np.ndarray,
    M: int,
    N_k: int,
    d: int,
    alpha_intra: float = 0.5,
    alpha_inter: float = 0.8,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max: float = 6.0,
    g_xy: float = 0.8,
    g_inter: float = 0.6,
    eps: float = 1e-7,
):
    """
    Computes total action for an M-Universe ecosystem.
    W: Total adjacency matrix of shape (N_total, N_total) where N_total = M * N_k.
    """
    N_total = M * N_k

    # 1. Sparsity Energy (Intra-Universe vs Inter-Universe bridges)
    s_sparsity = 0.0
    for i in range(N_total):
        u_i = i // N_k  # Universe index for node i
        for j in range(N_total):
            if i == j:
                continue
            u_j = j // N_k
            w_sq = W[i, j] ** 2
            if u_i == u_j:
                s_sparsity += alpha_intra * w_sq
            else:
                s_sparsity += alpha_inter * w_sq

    # 2. Intra-Universe Transitivity Loop: (W_k^2 - W_k)^2 for each Universe k
    s_trans = 0.0
    for m in range(M):
        start_idx = m * N_k
        end_idx = start_idx + N_k
        for i in range(start_idx, end_idx):
            for k in range(start_idx, end_idx):
                if i == k:
                    continue
                w2_ik = 0.0
                for j in range(start_idx, end_idx):
                    if j != i and j != k:
                        w2_ik += W[i, j] * W[j, k]
                s_trans += beta * ((w2_ik - W[i, k]) ** 2)

    # 3. Capacity Gate
    s_gate = 0.0
    out_deg = np.zeros(N_total)
    in_deg = np.zeros(N_total)
    for i in range(N_total):
        for j in range(N_total):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]
        if out_deg[i] > k_max:
            s_gate += lambda_gate * ((out_deg[i] - k_max) ** 2)
        if in_deg[i] > k_max:
            s_gate += lambda_gate * ((in_deg[i] - k_max) ** 2)

    # 4. Local Observer Coupling within each Universe k (S_k -> G_k)
    s_local_coupling = 0.0
    v_hat_vectors = np.zeros((M, d))

    for m in range(M):
        start_idx = m * N_k
        diff_s = np.zeros(d)
        sum_sq = 0.0
        for a in range(d):
            node_a = start_idx + a
            diff_s[a] = out_deg[node_a] - in_deg[node_a]
            sum_sq += diff_s[a] ** 2
        norm_v = np.sqrt(sum_sq) + eps
        
        for a in range(d):
            v_hat_vectors[m, a] = diff_s[a] / norm_v
            node_a = start_idx + a
            sum_rest_sq = 0.0
            for j in range(start_idx + d, start_idx + N_k):
                sum_rest_sq += W[node_a, j] ** 2
            s_local_coupling += -g_xy * v_hat_vectors[m, a] * sum_rest_sq

    # 5. Inter-Universe Entanglement & Temporal Synchronization Coupling (g_inter)
    s_inter_sync = 0.0
    if M > 1 and g_inter > 0.0:
        for m in range(M):
            for l in range(m + 1, M):
                dot_v = 0.0
                for a in range(d):
                    dot_v += v_hat_vectors[m, a] * v_hat_vectors[l, a]
                
                m_start, m_end = m * N_k, (m + 1) * N_k
                l_start, l_end = l * N_k, (l + 1) * N_k
                
                sum_bridges_sq = 0.0
                for i in range(m_start, m_end):
                    for j in range(l_start, l_end):
                        sum_bridges_sq += W[i, j] ** 2 + W[j, i] ** 2
                
                s_inter_sync += -g_inter * dot_v * sum_bridges_sq

    return s_sparsity + s_trans + s_gate + s_local_coupling + s_inter_sync


@njit(fastmath=True)
def compute_ecosystem_observables(W: np.ndarray, M: int, N_k: int, d: int, eps: float = 1e-7):
    """
    Computes Key Observables for Phase 3 Ecosystem:
    - mean_R_local: Average causal asymmetry ratio inside individual universes
    - phi_sync: Inter-observer time synchronization index in [-1.0, 1.0]
    - R_cross: Inter-universe causal asymmetry
    - mean_align: Percentage of universes with healthy internal arrow of time
    """
    N_total = M * N_k
    out_deg = np.zeros(N_total)
    in_deg = np.zeros(N_total)
    for i in range(N_total):
        for j in range(N_total):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]

    r_locals = np.zeros(M)
    align_locals = np.zeros(M)
    v_hat_vectors = np.zeros((M, d))

    for m in range(M):
        start_idx = m * N_k
        end_idx = start_idx + N_k
        
        diff_sum = 0.0
        tot_sum = 0.0
        for i in range(start_idx, end_idx):
            for j in range(i + 1, end_idx):
                diff_sum += abs(W[i, j] - W[j, i])
                tot_sum += W[i, j] + W[j, i]
        r_locals[m] = diff_sum / (tot_sum + eps)

        diff_s = np.zeros(d)
        sum_sq = 0.0
        for a in range(d):
            node_a = start_idx + a
            diff_s[a] = out_deg[node_a] - in_deg[node_a]
            sum_sq += diff_s[a] ** 2
        norm_v = np.sqrt(sum_sq) + eps

        for a in range(d):
            v_hat_vectors[m, a] = diff_s[a] / norm_v

        obs_flow = 0.0
        for a in range(d):
            obs_flow += (out_deg[start_idx + a] - in_deg[start_idx + a]) / d
        sys_flow = 0.0
        num_sys = N_k - d
        for j in range(start_idx + d, end_idx):
            sys_flow += (out_deg[j] - in_deg[j]) / num_sys
        align_locals[m] = 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.05) else 0.0

    n_pairs = M * (M - 1) // 2 if M > 1 else 1
    sum_dot = 0.0
    for m in range(M):
        for l in range(m + 1, M):
            dot_val = 0.0
            for a in range(d):
                dot_val += v_hat_vectors[m, a] * v_hat_vectors[l, a]
            sum_dot += dot_val
    phi_sync = sum_dot / float(n_pairs) if M > 1 else 1.0

    diff_cross = 0.0
    tot_cross = 0.0
    for m in range(M):
        for l in range(m + 1, M):
            m_start, m_end = m * N_k, (m + 1) * N_k
            l_start, l_end = l * N_k, (l + 1) * N_k
            for i in range(m_start, m_end):
                for j in range(l_start, l_end):
                    diff_cross += abs(W[i, j] - W[j, i])
                    tot_cross += W[i, j] + W[j, i]
    r_cross = diff_cross / (tot_cross + eps) if tot_cross > 0 else 0.0

    return float(np.mean(r_locals)), float(phi_sync), float(r_cross), float(np.mean(align_locals))


@njit(fastmath=True)
def run_v11_ecosystem_simulation_numba(
    M: int = 3,
    N_k: int = 12,
    d: int = 3,
    g_xy: float = 0.8,
    g_inter: float = 0.6,
    alpha_intra: float = 0.5,
    alpha_inter: float = 0.8,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max_base: float = 6.0,
    n_therm: int = 30,
    n_measure: int = 40,
    step_size: float = 0.15,
    seed: int = 42,
):
    """
    Simulates the Phase 3 v11 Multi-Universe Ecosystem.
    """
    np.random.seed(seed)
    N_total = M * N_k
    k_max = k_max_base * np.sqrt(N_k / 8.0)

    W = np.random.uniform(0.05, 0.3, (N_total, N_total))
    for i in range(N_total):
        W[i, i] = 0.0

    current_action = compute_ecosystem_action(
        W, M, N_k, d, alpha_intra, alpha_inter, beta, lambda_gate, k_max, g_xy, g_inter
    )

    total_sweeps = n_therm + n_measure
    rec_r_local = np.zeros(n_measure)
    rec_phi_sync = np.zeros(n_measure)
    rec_r_cross = np.zeros(n_measure)
    rec_align = np.zeros(n_measure)
    record_idx = 0

    for sweep in range(total_sweeps):
        for i in range(N_total):
            for j in range(N_total):
                if i == j:
                    continue

                old_val = W[i, j]
                delta = np.random.normal(0.0, step_size)
                new_val = old_val + delta
                if new_val < 0.0:
                    continue

                W[i, j] = new_val
                new_action = compute_ecosystem_action(
                    W, M, N_k, d, alpha_intra, alpha_inter, beta, lambda_gate, k_max, g_xy, g_inter
                )

                delta_s = new_action - current_action
                if delta_s <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-delta_s):
                    current_action = new_action
                else:
                    W[i, j] = old_val

        if sweep >= n_therm:
            r_loc, phi_s, r_cr, aln = compute_ecosystem_observables(W, M, N_k, d)
            rec_r_local[record_idx] = r_loc
            rec_phi_sync[record_idx] = phi_s
            rec_r_cross[record_idx] = r_cr
            rec_align[record_idx] = aln
            record_idx += 1

    return (
        float(np.mean(rec_r_local)),
        float(np.std(rec_r_local)),
        float(np.mean(rec_phi_sync)),
        float(np.std(rec_phi_sync)),
        float(np.mean(rec_r_cross)),
        float(np.mean(rec_align)),
        float(current_action),
    )


def run_v11_ecosystem(M=3, N_k=12, d=3, g_xy=0.8, g_inter=0.6, n_therm=30, n_measure=40, seed=42):
    """Python wrapper for Phase 3 v11-Ecosystem simulation."""
    return run_v11_ecosystem_simulation_numba(
        M=M, N_k=N_k, d=d, g_xy=g_xy, g_inter=g_inter,
        n_therm=n_therm, n_measure=n_measure, seed=seed
    )
