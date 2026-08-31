"""
SGOED-Relational Core Engine (v8-R)
===================================
A Causal Graph & Relational Dynamics Engine for Temporal Emergence
Replacing N x N Matrix Containers with Relational Networks.

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-30
"""

import numpy as np


def compute_full_action(
    W: np.ndarray,
    S_idx: np.ndarray,
    alpha: float = 0.5,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max: float = 5.0,
    g_xy: float = 0.8,
    g_yx: float = 0.0,
    eps: float = 1e-7,
) -> float:
    """
    Computes the exact full action for the relational graph state W.
    
    W: (N, N) non-negative weighted adjacency matrix
    S_idx: array of node indices representing the observer subgraph S
    """
    N = W.shape[0]
    
    # 1. Base Graph Action: Sparsity + Transitivity Commutator-like Loop
    # S_sparsity = alpha * sum_{i!=j} w_ij^2
    w_no_diag = W.copy()
    np.fill_diagonal(w_no_diag, 0.0)
    s_sparsity = alpha * np.sum(w_no_diag ** 2)
    
    # Transitivity: (w_ij * w_jk - w_ik)^2
    # W2 = W @ W (where W2_ik = sum_j w_ij * w_jk)
    W2 = w_no_diag @ w_no_diag
    s_trans = beta * np.sum((W2 - w_no_diag) ** 2)
    s_base = s_sparsity + s_trans

    # 2. Stability Capacity Gate (prevents runaway out-degree)
    out_deg = np.sum(w_no_diag, axis=1)
    in_deg = np.sum(w_no_diag, axis=0)
    gate_viol = np.maximum(0.0, out_deg - k_max)
    s_gate = lambda_gate * np.sum(gate_viol ** 2)

    # 3. Directional Observer Coupling (Y -> X)
    # v_hat = normalized (out_deg - in_deg) on S
    diff_s = out_deg[S_idx] - in_deg[S_idx]
    norm_v = np.sqrt(np.sum(diff_s ** 2)) + eps
    v_hat = diff_s / norm_v  # shape (d,)
    
    # Non-observer nodes
    mask_not_s = np.ones(N, dtype=bool)
    mask_not_s[S_idx] = False
    not_s_idx = np.where(mask_not_s)[0]
    
    # Coupling energy: -g_xy * sum_{a in S} v_hat_a * sum_{j not in S} w_aj^2
    w_s_to_rest = w_no_diag[S_idx][:, not_s_idx]
    s_coupling = -g_xy * np.sum(v_hat * np.sum(w_s_to_rest ** 2, axis=1))

    # 4. Observer Back-Reaction Feedback (X -> Y)
    # Feedback to internal S edges based on inbound flow from rest of graph
    if g_yx > 0.0 and len(S_idx) > 1:
        inbound_from_rest = np.sum(w_no_diag[not_s_idx][:, S_idx], axis=0)  # shape (d,)
        w_internal_s = w_no_diag[np.ix_(S_idx, S_idx)]
        s_feedback = -g_yx * np.sum(np.sum(w_internal_s ** 2, axis=0) * inbound_from_rest)
    else:
        s_feedback = 0.0

    return float(s_base + s_gate + s_coupling + s_feedback)


def compute_observables(W: np.ndarray, S_idx: np.ndarray, eps: float = 1e-7) -> dict:
    """
    Computes key observables for temporal emergence in the relational graph.
    """
    N = W.shape[0]
    w_no_diag = W.copy()
    np.fill_diagonal(w_no_diag, 0.0)
    
    # 1. Causal Asymmetry Ratio R_causal
    upper_tri = np.triu_indices(N, k=1)
    diff = np.abs(w_no_diag[upper_tri] - w_no_diag.T[upper_tri])
    total = w_no_diag[upper_tri] + w_no_diag.T[upper_tri]
    r_causal = float(np.sum(diff) / (np.sum(total) + eps))

    # 2. Directed Flow Alignment (Observer vs Global System Flow)
    out_deg = np.sum(w_no_diag, axis=1)
    in_deg = np.sum(w_no_diag, axis=0)
    net_flow = out_deg - in_deg
    
    # Observer preferred direction sign
    observer_flow = np.mean(net_flow[S_idx])
    system_flow = np.mean(net_flow[[i for i in range(N) if i not in S_idx]])
    
    # Alignment is 1.0 if system develops directed flow aligned with observer bias
    alignment = 1.0 if (observer_flow * system_flow <= 0.0 and np.abs(observer_flow) > 0.1) else 0.0

    # 3. Mean degree and maximum capacity
    mean_deg = float(np.mean(out_deg))
    max_deg = float(np.max(out_deg))

    return {
        "r_causal": r_causal,
        "alignment": alignment,
        "mean_degree": mean_deg,
        "max_degree": max_deg,
        "observer_flow": float(observer_flow),
        "system_flow": float(system_flow),
    }


def run_relational_simulation(
    N: int = 10,
    d: int = 3,
    g_xy: float = 0.8,
    g_yx: float = 0.0,
    alpha: float = 0.5,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max: float = 5.0,
    n_therm: int = 30,
    n_measure: int = 40,
    step_size: float = 0.15,
    seed: int = 42,
) -> dict:
    """
    Runs a full Metropolis-Hastings Monte Carlo simulation on the Relational Graph.
    Uses trajectory averaging over the measurement window.
    """
    rng = np.random.default_rng(seed)
    
    # Initialize random non-negative edge weights
    W = rng.uniform(0.1, 0.5, size=(N, N))
    np.fill_diagonal(W, 0.0)
    
    # Designate the first d nodes as the Observer Subgraph S
    S_idx = np.arange(d)
    
    # Thermalization
    current_action = compute_full_action(
        W, S_idx, alpha, beta, lambda_gate, k_max, g_xy, g_yx
    )
    
    total_sweeps = n_therm + n_measure
    recorded_r = []
    recorded_align = []
    recorded_mean_deg = []
    
    for sweep in range(total_sweeps):
        # Update all off-diagonal edges
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                old_val = W[i, j]
                delta = rng.normal(0.0, step_size)
                new_val = old_val + delta
                
                # Enforce non-negativity
                if new_val < 0.0:
                    continue
                
                W[i, j] = new_val
                new_action = compute_full_action(
                    W, S_idx, alpha, beta, lambda_gate, k_max, g_xy, g_yx
                )
                
                delta_s = new_action - current_action
                # Metropolis acceptance criterion (beta_inv = 1.0)
                if delta_s <= 0.0 or rng.uniform(0.0, 1.0) < np.exp(-delta_s):
                    current_action = new_action
                else:
                    W[i, j] = old_val
        
        # Record trajectory measurements
        if sweep >= n_therm:
            obs = compute_observables(W, S_idx)
            recorded_r.append(obs["r_causal"])
            recorded_align.append(obs["alignment"])
            recorded_mean_deg.append(obs["mean_degree"])

    return {
        "mean_r_causal": float(np.mean(recorded_r)),
        "std_r_causal": float(np.std(recorded_r)),
        "alignment_rate": float(np.mean(recorded_align)),
        "mean_degree": float(np.mean(recorded_mean_deg)),
        "final_action": float(current_action),
    }
