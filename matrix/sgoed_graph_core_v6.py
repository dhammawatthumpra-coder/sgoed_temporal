"""
SGOED-Relational Core v6 — Normalized Feedback (v7-style direction)
====================================================================
Hypothesis test: does normalizing the back-reaction direction (like v7
normalizes v_hat) stop the runaway R_causal growth?

v5 feedback:  s_fb += -g_yx * (W[b,a]^2) * inbound[a]      (raw magnitude)
v6 feedback:  s_fb += -g_yx * (W[b,a]^2) * w_hat[a]        (normalized)

where w_hat[a] = inbound[a] / ||inbound||  (direction only, like v7's v_hat).

Everything else identical to v5 (extent gate kept). This isolates the effect
of normalizing the feedback direction on the emergent causal asymmetry.
"""
import numpy as np
from numba import njit

from sgoed_graph_core_v5 import (
    compute_coupling_numba,
    compute_spacetime_dimensions,
    compute_obs_extent,
    compute_full_action_v5,
    compute_delta_edge_v5,
    run_v5_numba,
    _recalc_degrees,
    _recalc_W2,
)


@njit(fastmath=True)
def compute_feedback_numba_normalized(W, d, g_yx, eps=1e-7):
    """Back-reaction with NORMALIZED inbound direction (v7-style)."""
    N = W.shape[0]
    inbound = np.zeros(d)
    for a in range(d):
        for q in range(d, N):
            inbound[a] += W[q, a]
    norm = 0.0
    for a in range(d):
        norm += inbound[a] ** 2
    norm = np.sqrt(norm) + eps
    w_hat = inbound / norm

    s_fb = 0.0
    for a in range(d):
        for b in range(d):
            if a != b:
                s_fb += -g_yx * (W[b, a] ** 2) * w_hat[a]
    return s_fb


@njit(fastmath=True)
def compute_full_action_v6(
    W, W2, out_deg, in_deg, d, alpha, beta, lambda_gate, k_max,
    g_xy, g_yx, extent_max_obs, lambda_extent, eps=1e-7
):
    N = W.shape[0]
    s_sparsity = 0.0
    for i in range(N):
        for j in range(N):
            if i != j:
                s_sparsity += alpha * (W[i, j] ** 2)
    s_trans = 0.0
    for i in range(N):
        for k in range(N):
            if i != k:
                s_trans += beta * ((W2[i, k] - W[i, k]) ** 2)
    s_gate = 0.0
    for i in range(N):
        if out_deg[i] > k_max:
            s_gate += lambda_gate * ((out_deg[i] - k_max) ** 2)
        if in_deg[i] > k_max:
            s_gate += lambda_gate * ((in_deg[i] - k_max) ** 2)
    s_coup = compute_coupling_numba(W, out_deg, in_deg, d, g_xy, eps)
    s_fb = compute_feedback_numba_normalized(W, d, g_yx, eps) if (g_yx > 0.0 and d > 1) else 0.0
    obs_extent = compute_obs_extent(W, d)
    s_ext = lambda_extent * ((obs_extent - extent_max_obs) ** 2) if obs_extent > extent_max_obs else 0.0
    return s_sparsity + s_trans + s_gate + s_coup + s_fb + s_ext


@njit(fastmath=True)
def compute_delta_edge_v6(
    W, W2, out_deg, in_deg, i, j, new_val,
    d, alpha, beta, lambda_gate, k_max, g_xy, g_yx,
    extent_max_obs, lambda_extent, eps=1e-7
):
    """Delta for v6: identical to v5 except feedback uses normalized inbound."""
    N = W.shape[0]
    old_val = W[i, j]
    dW = new_val - old_val
    if new_val < 0.0 or dW == 0.0:
        return 0.0

    delta_sparsity = alpha * (new_val ** 2 - old_val ** 2)

    delta_trans = 0.0
    for q in range(N):
        if q != i and q != j:
            old_w2_iq = W2[i, q]
            new_w2_iq = old_w2_iq + dW * W[j, q]
            delta_trans += beta * ((new_w2_iq - W[i, q]) ** 2 - (old_w2_iq - W[i, q]) ** 2)
    for p in range(N):
        if p != i and p != j:
            old_w2_pj = W2[p, j]
            new_w2_pj = old_w2_pj + W[p, i] * dW
            delta_trans += beta * ((new_w2_pj - W[p, j]) ** 2 - (old_w2_pj - W[p, j]) ** 2)
    old_w2_ij = W2[i, j]
    delta_trans += beta * ((old_w2_ij - new_val) ** 2 - (old_w2_ij - old_val) ** 2)

    out_i = out_deg[i]; out_i_new = out_i + dW
    old_gate_out = lambda_gate * ((out_i - k_max) ** 2) if out_i > k_max else 0.0
    new_gate_out = lambda_gate * ((out_i_new - k_max) ** 2) if out_i_new > k_max else 0.0
    in_j = in_deg[j]; in_j_new = in_j + dW
    old_gate_in = lambda_gate * ((in_j - k_max) ** 2) if in_j > k_max else 0.0
    new_gate_in = lambda_gate * ((in_j_new - k_max) ** 2) if in_j_new > k_max else 0.0
    delta_gate = (new_gate_out - old_gate_out) + (new_gate_in - old_gate_in)

    W[i, j] = new_val; out_deg[i] = out_i_new; in_deg[j] = in_j_new
    coup_new = compute_coupling_numba(W, out_deg, in_deg, d, g_xy, eps)
    W[i, j] = old_val; out_deg[i] = out_i; in_deg[j] = in_j
    coup_old = compute_coupling_numba(W, out_deg, in_deg, d, g_xy, eps)
    delta_coupling = coup_new - coup_old

    delta_feedback = 0.0
    if g_yx > 0.0 and d > 1:
        W[i, j] = new_val
        fb_new = compute_feedback_numba_normalized(W, d, g_yx, eps)
        W[i, j] = old_val
        fb_old = compute_feedback_numba_normalized(W, d, g_yx, eps)
        delta_feedback = fb_new - fb_old

    delta_extent = 0.0
    if i < d and j < d and i != j:
        obs_extent = compute_obs_extent(W, d)
        n_edges = d * (d - 1) if d > 1 else 1
        new_extent = obs_extent + (new_val ** 2 - old_val ** 2) / n_edges
        g_old = lambda_extent * ((obs_extent - extent_max_obs) ** 2) if obs_extent > extent_max_obs else 0.0
        g_new = lambda_extent * ((new_extent - extent_max_obs) ** 2) if new_extent > extent_max_obs else 0.0
        delta_extent = g_new - g_old

    return delta_sparsity + delta_trans + delta_gate + delta_coupling + delta_feedback + delta_extent


@njit(fastmath=True)
def run_v6_numba(
    N, d, g_xy, g_yx, alpha, beta, lambda_gate, k_max_base,
    n_therm, n_measure, step_size, seed, W_init, use_init,
    extent_max_obs, lambda_extent
):
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
                dS = compute_delta_edge_v6(
                    W, W2, out_deg, in_deg, i, j, new_val,
                    d, alpha, beta, lambda_gate, k_max, g_xy, g_yx,
                    extent_max_obs, lambda_extent
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
            recorded_r[record_idx] = r_causal
            recorded_align[record_idx] = align
            recorded_d_mm[record_idx] = d_mm
            recorded_l_max[record_idx] = l_max
            recorded_obs_extent[record_idx] = compute_obs_extent(W, d)
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


def run_v6(N=16, d=3, g_xy=0.8, g_yx=0.0,
           alpha=0.5, beta=0.1, lambda_gate=10.0, k_max_base=5.0,
           n_therm=240, n_measure=40, step_size=0.15, seed=42,
           W_init=None, extent_max_obs=np.inf, lambda_extent=10.0):
    if W_init is None:
        W_init = np.zeros((N, N))
        use_init = 0
    else:
        use_init = 1
    return run_v6_numba(
        N, d, g_xy, g_yx, alpha, beta, lambda_gate, k_max_base,
        n_therm, n_measure, step_size, seed, W_init, use_init,
        extent_max_obs, lambda_extent
    )
