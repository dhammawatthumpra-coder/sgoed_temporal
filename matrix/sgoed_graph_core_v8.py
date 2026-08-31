"""
SGOED-Relational Core v8 — Tuned Sparse Engine (O(d^2) coupling/feedback)
=========================================================================
Tuned version of v7. Two optimizations identified by profiling (build_csr was
only ~34%; the delta loop dominates):

1. coupling/feedback/extent computed from RUNNING SUM state in O(d^2), not
   O(d*N): we maintain rest_sq[a] = sum_{q>=d} W[a,q]^2 and
   inbound[a] = sum_{q>=d} W[q,a], updated incrementally (O(1)) when an edge
   touches the observer (i<d or j<d).

2. rows[E] precomputed -> O(1) edge-to-row lookup instead of "while i<N".

DEGREE is still a full (threshold-free) weight sum, matching v3-v6 exactly.
W2 stays incremental as in v7.

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-30
"""
import numpy as np
from numba import njit


@njit(fastmath=True)
def build_csr(W, N, w_min):
    deg = np.zeros(N, dtype=np.int32)
    for i in range(N):
        for j in range(N):
            if i != j and W[i, j] > w_min:
                deg[i] += 1
    row_ptr = np.zeros(N + 1, dtype=np.int32)
    for i in range(N):
        row_ptr[i + 1] = row_ptr[i] + deg[i]
    E = row_ptr[N]
    col_idx = np.zeros(E, dtype=np.int32)
    pos = np.zeros(N, dtype=np.int32)
    for i in range(N):
        for j in range(N):
            if i != j and W[i, j] > w_min:
                col_idx[row_ptr[i] + pos[i]] = j
                pos[i] += 1
    return row_ptr, col_idx


@njit(fastmath=True)
def build_csr_transpose(W, N, w_min):
    deg = np.zeros(N, dtype=np.int32)
    for j in range(N):
        for i in range(N):
            if i != j and W[i, j] > w_min:
                deg[j] += 1
    row_ptr = np.zeros(N + 1, dtype=np.int32)
    for j in range(N):
        row_ptr[j + 1] = row_ptr[j] + deg[j]
    E = row_ptr[N]
    col_idx = np.zeros(E, dtype=np.int32)
    pos = np.zeros(N, dtype=np.int32)
    for j in range(N):
        for i in range(N):
            if i != j and W[i, j] > w_min:
                col_idx[row_ptr[j] + pos[j]] = i
                pos[j] += 1
    return row_ptr, col_idx


@njit(fastmath=True)
def build_rows(row_ptr, N, E):
    """O(1) edge->row lookup."""
    rows = np.zeros(E, dtype=np.int32)
    for i in range(N):
        for t in range(row_ptr[i], row_ptr[i + 1]):
            rows[t] = i
    return rows


@njit(fastmath=True)
def build_W2(W, N):
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
def compute_obs_extent(W, d):
    s = 0.0
    for a in range(d):
        for b in range(d):
            if a != b:
                s += W[a, b] ** 2
    return s / (d * (d - 1) if d > 1 else 1.0)


@njit(fastmath=True)
def cfe_from_state(W, out_deg, in_deg, rest_sq, inbound, d,
                   g_xy, g_yx, extent_max_obs, lambda_extent, eps=1e-7):
    """Coupling + feedback + extent from running-sum state in O(d^2)."""
    # coupling: -g_xy * sum_a v_hat[a] * rest_sq[a]
    diff = np.zeros(d)
    nsq = 0.0
    for a in range(d):
        diff[a] = out_deg[a] - in_deg[a]
        nsq += diff[a] ** 2
    norm = np.sqrt(nsq) + eps
    sc = 0.0
    for a in range(d):
        sc += -g_xy * (diff[a] / norm) * rest_sq[a]

    # feedback: -g_yx * sum_{a!=b} W[b,a]^2 * (inbound[a]/norm_in)
    sf = 0.0
    if g_yx > 0.0 and d > 1:
        nn = 0.0
        for a in range(d):
            nn += inbound[a] ** 2
        nn = np.sqrt(nn) + eps
        for a in range(d):
            for b in range(d):
                if a != b:
                    sf += -g_yx * (W[b, a] ** 2) * (inbound[a] / nn)

    oe = compute_obs_extent(W, d)
    se = lambda_extent * ((oe - extent_max_obs) ** 2) if oe > extent_max_obs else 0.0
    return sc + sf + se


@njit(fastmath=True)
def delta_edge_v8(
    W, W2, row_ptr, col_idx, row_ptr_t, col_idx_t,
    out_deg, in_deg, rest_sq, inbound,
    i, j, new_val,
    d, alpha, beta, lambda_gate, k_max, g_xy, g_yx,
    extent_max_obs, lambda_extent, eps=1e-7
):
    N = W.shape[0]
    old_val = W[i, j]
    dW = new_val - old_val
    if dW == 0.0 or new_val < 0.0:
        return 0.0

    d_sp = alpha * (new_val ** 2 - old_val ** 2)

    # transitivity O(k)
    d_tr = 0.0
    for t in range(row_ptr[j], row_ptr[j + 1]):
        k = col_idx[t]
        if k != i and k != j:
            old_w2 = W2[i, k]
            new_w2 = old_w2 + dW * W[j, k]
            d_tr += beta * ((new_w2 - W[i, k]) ** 2 - (old_w2 - W[i, k]) ** 2)
    for t in range(row_ptr_t[i], row_ptr_t[i + 1]):
        p = col_idx_t[t]
        if p != i and p != j:
            old_w2 = W2[p, j]
            new_w2 = old_w2 + W[p, i] * dW
            d_tr += beta * ((new_w2 - W[p, j]) ** 2 - (old_w2 - W[p, j]) ** 2)
    d_tr += beta * ((W2[i, j] - new_val) ** 2 - (W2[i, j] - old_val) ** 2)

    # gate O(1)
    oi = out_deg[i]; oi_n = oi + dW
    ij = in_deg[j]; ij_n = ij + dW
    d_gate = 0.0
    if oi_n > k_max: d_gate += lambda_gate * (oi_n - k_max) ** 2
    if oi > k_max: d_gate -= lambda_gate * (oi - k_max) ** 2
    if ij_n > k_max: d_gate += lambda_gate * (ij_n - k_max) ** 2
    if ij > k_max: d_gate -= lambda_gate * (ij - k_max) ** 2

    # coupling+feedback+extent: O(d^2) via running sums
    ode_n = out_deg.copy(); ide_n = in_deg.copy()
    rs_n = rest_sq.copy(); ib_n = inbound.copy()
    ode_n[i] += dW; ide_n[j] += dW
    if i < d and j >= d:
        rs_n[i] += new_val ** 2 - old_val ** 2
    if i >= d and j < d:
        ib_n[j] += dW
    W[i, j] = new_val
    cfe_n = cfe_from_state(W, ode_n, ide_n, rs_n, ib_n, d, g_xy, g_yx, extent_max_obs, lambda_extent, eps)
    W[i, j] = old_val
    cfe_o = cfe_from_state(W, out_deg, in_deg, rest_sq, inbound, d, g_xy, g_yx, extent_max_obs, lambda_extent, eps)
    d_cfe = cfe_n - cfe_o

    return d_sp + d_tr + d_gate + d_cfe


@njit(fastmath=True)
def run_v8_numba(
    N, d, g_xy, g_yx, alpha, beta, lambda_gate, k_max_base,
    n_therm, n_measure, step_size, seed, extent_max_obs, lambda_extent, w_min
):
    np.random.seed(seed)
    k_max = k_max_base * np.sqrt(N / 8.0)
    W = np.random.uniform(0.1, 0.5, (N, N))
    for i in range(N):
        W[i, i] = 0.0

    out_deg = np.zeros(N); in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]
    W2 = build_W2(W, N)

    # running-sum state for coupling/feedback (O(1) per accept)
    rest_sq = np.zeros(d)
    inbound = np.zeros(d)
    for a in range(d):
        for q in range(d, N):
            rest_sq[a] += W[a, q] ** 2
            inbound[a] += W[q, a]

    recorded_r = np.zeros(n_measure)
    recorded_align = np.zeros(n_measure)
    recorded_extent = np.zeros(n_measure)
    record_idx = 0

    total_sweeps = n_therm + n_measure
    for sweep in range(total_sweeps):
        row_ptr, col_idx = build_csr(W, N, w_min)
        row_ptr_t, col_idx_t = build_csr_transpose(W, N, w_min)
        E = row_ptr[N]
        rows = build_rows(row_ptr, N, E)

        for t in range(E):
            i = rows[t]
            j = col_idx[t]
            old_val = W[i, j]
            new_val = old_val + np.random.normal(0.0, step_size)
            if new_val < 0.0:
                continue
            dS = delta_edge_v8(
                W, W2, row_ptr, col_idx, row_ptr_t, col_idx_t,
                out_deg, in_deg, rest_sq, inbound, i, j, new_val,
                d, alpha, beta, lambda_gate, k_max, g_xy, g_yx,
                extent_max_obs, lambda_extent
            )
            if dS <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-dS):
                dW = new_val - old_val
                for t2 in range(row_ptr[j], row_ptr[j + 1]):
                    k = col_idx[t2]
                    if k != i and k != j:
                        W2[i, k] += dW * W[j, k]
                for t2 in range(row_ptr_t[i], row_ptr_t[i + 1]):
                    p = col_idx_t[t2]
                    if p != i and p != j:
                        W2[p, j] += W[p, i] * dW
                W[i, j] = new_val
                out_deg[i] += dW
                in_deg[j] += dW
                if i < d and j >= d:
                    rest_sq[i] += new_val ** 2 - old_val ** 2
                if i >= d and j < d:
                    inbound[j] += dW

        if sweep >= n_therm:
            diff_sum = 0.0
            tot_sum = 0.0
            for i in range(N):
                for j in range(i + 1, N):
                    diff_sum += abs(W[i, j] - W[j, i])
                    tot_sum += W[i, j] + W[j, i]
            recorded_r[record_idx] = diff_sum / (tot_sum + 1e-7)
            obs_flow = 0.0
            for a in range(d):
                obs_flow += (out_deg[a] - in_deg[a]) / d
            sys_flow = 0.0
            for j in range(d, N):
                sys_flow += (out_deg[j] - in_deg[j]) / (N - d)
            recorded_align[record_idx] = 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.1) else 0.0
            recorded_extent[record_idx] = compute_obs_extent(W, d)
            record_idx += 1

    return (
        float(np.mean(recorded_r)), float(np.std(recorded_r)),
        float(np.mean(recorded_align)), 0.0, 0.0,
        float(np.mean(recorded_extent)), W,
    )


def run_v8(N=16, d=3, g_xy=0.8, g_yx=0.0,
           alpha=0.5, beta=0.1, lambda_gate=10.0, k_max_base=5.0,
           n_therm=240, n_measure=40, step_size=0.15, seed=42,
           extent_max_obs=16.0, lambda_extent=10.0, w_min=0.01):
    return run_v8_numba(
        N, d, g_xy, g_yx, alpha, beta, lambda_gate, k_max_base,
        n_therm, n_measure, step_size, seed, extent_max_obs, lambda_extent, w_min
    )