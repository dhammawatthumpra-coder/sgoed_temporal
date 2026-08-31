"""
SGOED-Relational Core v7 — Sparse Graph Engine (target O(E))
=============================================================
Correctness-first sparse engine. Key insight learned from v7 attempts:

  * DEGREE is the FULL weight sum (no threshold) — matches v3-v6 exactly.
  * The threshold w_min is used ONLY to decide which edges are swept
    (sparse scan), never in the degree/action computation.

Delta is verified against full action to 3e-14 (see the Phase-1 test).

Per-edge cost:
  * sparsity O(1), gate O(1)
  * transitivity O(k) via CSR neighbor list (k = mean degree)
  * coupling/feedback/extent O(d*N + d^2) recomputed (d small)

Sweep iterates ACTIVE edges only (CSR), so total is O(E*k) per sweep when
the graph is sparse.

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-30
"""
import numpy as np
from numba import njit


@njit(fastmath=True)
def build_csr(W, N, w_min):
    """CSR of active edges (W[i,j] > w_min) for the sparse sweep."""
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
    """CSR of active edges in the TRANSPOSED graph: for node j, list of i with
    W[i,j] > w_min (i.e. in-neighbors of j). Used for the O(k) transitivity
    column update (replaces the O(N) in-neighbor scan)."""
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
def coup_fb_ext(W, out_deg, in_deg, d, g_xy, g_yx, extent_max_obs, lambda_extent, eps=1e-7):
    N = W.shape[0]
    diff = np.zeros(d)
    nsq = 0.0
    for a in range(d):
        diff[a] = out_deg[a] - in_deg[a]
        nsq += diff[a] ** 2
    norm = np.sqrt(nsq) + eps
    sc = 0.0
    for a in range(d):
        vh = diff[a] / norm
        rest = 0.0
        for q in range(d, N):
            rest += W[a, q] ** 2
        sc += -g_xy * vh * rest
    sf = 0.0
    if g_yx > 0.0 and d > 1:
        inbound = np.zeros(d)
        for a in range(d):
            for q in range(d, N):
                inbound[a] += W[q, a]
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
def delta_edge_v7(
    W, W2, row_ptr, col_idx, row_ptr_t, col_idx_t, out_deg, in_deg,
    i, j, new_val,
    d, alpha, beta, lambda_gate, k_max, g_xy, g_yx,
    extent_max_obs, lambda_extent, eps=1e-7
):
    N = W.shape[0]
    old_val = W[i, j]
    dW = new_val - old_val
    if dW == 0.0 or new_val < 0.0:
        return 0.0

    # sparsity O(1)
    d_sp = alpha * (new_val ** 2 - old_val ** 2)

    # transitivity O(k): W2 row i via out-neighbors of j, col j via in-neighbors of i
    d_tr = 0.0
    for t in range(row_ptr[j], row_ptr[j + 1]):
        k = col_idx[t]
        if k != i and k != j:
            old_w2 = W2[i, k]
            new_w2 = old_w2 + dW * W[j, k]
            d_tr += beta * ((new_w2 - W[i, k]) ** 2 - (old_w2 - W[i, k]) ** 2)
    # column j via in-neighbors of i (transposed CSR, O(k))
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

    # coupling + feedback + extent (recomputed O(d*N + d^2))
    ode = out_deg.copy(); ide = in_deg.copy()
    ode_n = out_deg.copy(); ide_n = in_deg.copy()
    ode_n[i] += dW; ide_n[j] += dW
    W[i, j] = new_val
    cfe_n = coup_fb_ext(W, ode_n, ide_n, d, g_xy, g_yx, extent_max_obs, lambda_extent, eps)
    W[i, j] = old_val
    cfe_o = coup_fb_ext(W, ode, ide, d, g_xy, g_yx, extent_max_obs, lambda_extent, eps)
    d_cfe = cfe_n - cfe_o

    return d_sp + d_tr + d_gate + d_cfe


@njit(fastmath=True)
def run_v7_numba(
    N, d, g_xy, g_yx, alpha, beta, lambda_gate, k_max_base,
    n_therm, n_measure, step_size, seed, extent_max_obs, lambda_extent, w_min
):
    np.random.seed(seed)
    k_max = k_max_base * np.sqrt(N / 8.0)
    W = np.random.uniform(0.1, 0.5, (N, N))
    for i in range(N):
        W[i, i] = 0.0

    # full degree (no threshold) — built once, updated incrementally
    out_deg = np.zeros(N); in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]
    # W2 built once, updated incrementally (O(N) per accept)
    W2 = build_W2(W, N)

    recorded_r = np.zeros(n_measure)
    recorded_align = np.zeros(n_measure)
    recorded_extent = np.zeros(n_measure)
    record_idx = 0

    total_sweeps = n_therm + n_measure
    for sweep in range(total_sweeps):
        row_ptr, col_idx = build_csr(W, N, w_min)
        row_ptr_t, col_idx_t = build_csr_transpose(W, N, w_min)
        E = row_ptr[N]

        # sweep over ACTIVE edges only
        for t in range(E):
            i = 0
            while i < N and not (row_ptr[i] <= t < row_ptr[i + 1]):
                i += 1
            j = col_idx[t]
            old_val = W[i, j]
            new_val = old_val + np.random.normal(0.0, step_size)
            if new_val < 0.0:
                continue
            dS = delta_edge_v7(
                W, W2, row_ptr, col_idx, row_ptr_t, col_idx_t,
                out_deg, in_deg, i, j, new_val,
                d, alpha, beta, lambda_gate, k_max, g_xy, g_yx,
                extent_max_obs, lambda_extent
            )
            if dS <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-dS):
                dW = new_val - old_val
                # W2 incremental update O(k): row i (out-neighbors of j) +
                # col j (in-neighbors of i), using OLD W.
                for t2 in range(row_ptr[j], row_ptr[j + 1]):
                    k = col_idx[t2]
                    if k != i and k != j:
                        W2[i, k] += dW * W[j, k]
                for t2 in range(row_ptr_t[i], row_ptr_t[i + 1]):
                    p = col_idx_t[t2]
                    if p != i and p != j:
                        W2[p, j] += W[p, i] * dW
                # (W2[i,j] is invariant: W@W excludes the diagonal)
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


def run_v7(N=16, d=3, g_xy=0.8, g_yx=0.0,
           alpha=0.5, beta=0.1, lambda_gate=10.0, k_max_base=5.0,
           n_therm=240, n_measure=40, step_size=0.15, seed=42,
           extent_max_obs=16.0, lambda_extent=10.0, w_min=0.01):
    return run_v7_numba(
        N, d, g_xy, g_yx, alpha, beta, lambda_gate, k_max_base,
        n_therm, n_measure, step_size, seed, extent_max_obs, lambda_extent, w_min
    )
