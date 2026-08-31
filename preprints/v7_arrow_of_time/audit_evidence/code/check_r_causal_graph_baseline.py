"""
R_causal baseline audit for GRAPH v8 (same R estimator as hypergraph).
Tests whether R_causal ~ 0.47-0.50 evidences an arrow of time in the graph model.
"""
import numpy as np
from numba import njit
from sgoed_graph_core_v8 import run_v8


@njit(fastmath=True)
def compute_R(W):
    N = W.shape[0]
    dsum = 0.0
    tsum = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            dsum += abs(W[i, j] - W[j, i])
            tsum += W[i, j] + W[j, i]
    return dsum / (tsum + 1e-7)


@njit(fastmath=True)
def direction_consistency(W):
    N = W.shape[0]
    D = 0.0
    for i in range(N):
        for k in range(i + 1, N):
            f = W[i, k] - W[k, i]
            if f > 0:
                D += 1.0
            elif f < 0:
                D -= 1.0
    return D


@njit(fastmath=True)
def degree_imbalance_std(W):
    N = W.shape[0]
    out = np.zeros(N)
    inn = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out[i] += W[i, j]
                inn[j] += W[i, j]
    return float(np.std(out - inn))


def value_shuffle(W, rng):
    N = W.shape[0]
    mask = ~np.eye(N, dtype=bool)
    vals = W[mask]
    W2 = W.copy()
    W2[mask] = rng.permutation(vals)
    return W2


def mirror_swap(W, rng):
    N = W.shape[0]
    W2 = W.copy()
    for i in range(N):
        for k in range(i + 1, N):
            if rng.uniform() < 0.5:
                W2[i, k], W2[k, i] = W2[k, i], W2[i, k]
    return W2


if __name__ == "__main__":
    print("=" * 74)
    print(" 1. REAL graph v8 (N=16, d=3, g_xy=0.8, seed 42, n_therm=240)")
    print("=" * 74)
    r_mean, r_std, aln, _, _, ext, W = run_v8(
        N=16, d=3, g_xy=0.8, g_yx=0.0, n_therm=240, n_measure=40, seed=42
    )
    R_real = compute_R(W)
    D_real = direction_consistency(W)
    imb_real = degree_imbalance_std(W)
    print(f"  R_causal(mean over traj) = {r_mean:.4f} | R(final W) = {R_real:.4f} | "
          f"D_direction = {D_real:+.0f} | deg-imb std = {imb_real:.4f}")
    print(f"  alignment_rate = {aln:.3f} | W range [{W.min():.4f}, {W.max():.4f}] | "
          f"fraction zero = {(W == 0).mean():.3f}")

    rng = np.random.default_rng(123)
    print()
    print("=" * 74)
    print(" 2. NULL TESTS")
    print("=" * 74)

    R_sh, D_sh, imb_sh = [], [], []
    for rep in range(10):
        Ws = value_shuffle(W, rng)
        R_sh.append(compute_R(Ws))
        D_sh.append(direction_consistency(Ws))
        imb_sh.append(degree_imbalance_std(Ws))
    print(f"  [shuffle values] R = {np.mean(R_sh):.4f} +/- {np.std(R_sh):.4f} | "
          f"D = {np.mean(D_sh):+.1f} +/- {np.std(D_sh):.1f} | imb-std = {np.mean(imb_sh):.4f}")

    lo, hi = float(W.min()), float(W.max())
    R_u, D_u = [], []
    for rep in range(10):
        Wu = rng.uniform(lo, hi, W.shape)
        np.fill_diagonal(Wu, 0.0)
        R_u.append(compute_R(Wu))
        D_u.append(direction_consistency(Wu))
    print(f"  [iid uniform {lo:.3f}-{hi:.3f}] R = {np.mean(R_u):.4f} +/- {np.std(R_u):.4f} | "
          f"D = {np.mean(D_u):+.1f} +/- {np.std(D_u):.1f}")

    R_sw, D_sw = [], []
    for rep in range(10):
        Ws = mirror_swap(W, rng)
        R_sw.append(compute_R(Ws))
        D_sw.append(direction_consistency(Ws))
    print(f"  [mirror swap]    R = {np.mean(R_sw):.4f} (INVARIANT by design) | "
          f"D = {np.mean(D_sw):+.1f} +/- {np.std(D_sw):.1f}")

    print()
    print("=" * 74)
    print(" 3. VERDICT")
    print("=" * 74)
    print(f"  R_real = {R_real:.4f} vs shuffle {np.mean(R_sh):.4f} vs uniform {np.mean(R_u):.4f}")
    print(f"  D_real = {D_real:+.0f} (max = {16*15/2:.0f}) vs shuffle {np.mean(D_sh):+.1f} vs uniform {np.mean(D_u):+.1f}")
