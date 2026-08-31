"""
Correct spectral dimension, attempt 2 (self-written, data honesty).
===================================================================
Two standard estimators, both on REVERSIBLE diffusion (required for a
well-defined spectral dimension):
  A. Heat kernel on NORMALIZED Laplacian Ln = I - D^-1/2 A D^-1/2  (spec in [0,2])
  B. Lazy random walk return probability  P_lazy = (I + D^-1 A)/2
Both report the dimension-flow curve d_s(t) = -2 d ln P / d ln t and a
representative value = max of the curve (the diffusive plateau), which is
the standard "spectral dimension" quoted in QG literature for finite systems.
Validation: path=1, 2D grid=2, 4D hypercube=4, Sierpinski~1.46, random dense ref.
"""
import json
import numpy as np
from numba import njit
from sgoed_hypergraph_core_v10 import run_v10


@njit(fastmath=True)
def project_hypergraph_weff(T):
    N = T.shape[0]
    W = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                s = 0.0
                for k in range(N):
                    if k != i and k != j:
                        s += T[i, k, j] + T[i, j, k]
                W[i, j] = s
    return W


def d_s_heatkernel_normalized(A, t_lo=0.05, t_hi=60.0, n_t=40):
    N = A.shape[0]
    deg = A.sum(axis=1)
    d_is = np.zeros_like(deg)
    m = deg > 1e-12
    d_is[m] = 1.0 / np.sqrt(deg[m])
    Ln = np.eye(N) - d_is[:, None] * A * d_is[None, :]
    evals = np.clip(np.linalg.eigvalsh(Ln), 0.0, None)
    t_arr = np.logspace(np.log10(t_lo), np.log10(t_hi), n_t)
    logP = np.array([np.log(np.sum(np.exp(-t * evals))) for t in t_arr])
    logt = np.log(t_arr)
    ds = -2.0 * np.gradient(logP, logt)
    # representative value: max of smoothed curve (diffusive plateau)
    k = 3
    ds_sm = np.convolve(ds, np.ones(k) / k, mode="same")
    return float(np.max(ds_sm)), t_arr, ds_sm


def d_s_lazy_walk(A, tau_max=200):
    N = A.shape[0]
    deg = A.sum(axis=1)
    P = np.zeros((N, N))
    m = deg > 1e-12
    P[m] = A[m] / deg[m][:, None]
    P[~m] = 1.0 / N
    P = 0.5 * (np.eye(N) + P)  # lazy: kills bipartite oscillation
    taus = np.array([2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192])
    taus = taus[taus <= tau_max]
    pret = []
    Pn = np.eye(N)
    for t in range(1, int(taus[-1]) + 1):
        Pn = Pn @ P
        if t in taus:
            pret.append(float(np.trace(Pn) / N))
    pret = np.maximum(np.array(pret), 1e-14)
    logt = np.log(taus.astype(float))
    logp = np.log(pret)
    ds = -2.0 * np.gradient(logp, logt)
    # plateau estimate: max of local slopes
    return float(np.max(ds)), taus, ds, pret


def make_path(N):
    W = np.zeros((N, N))
    for i in range(N - 1):
        W[i, i + 1] = W[i + 1, i] = 1.0
    return W


def make_grid(g):
    W = np.zeros((g * g, g * g))
    for i in range(g):
        for j in range(g):
            idx = i * g + j
            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < g and 0 <= nj < g:
                    W[idx, ni * g + nj] = 1.0
    return W


def make_hypercube(dim):
    N = 1 << dim
    W = np.zeros((N, N))
    for i in range(N):
        for b in range(dim):
            W[i, i ^ (1 << b)] = 1.0
    return W


print("=" * 74)
print(" 1. VALIDATION (known answers): method A = heat kernel (normalized), B = lazy walk")
print("=" * 74)
for name, W, expect in [
    ("Path N=128", make_path(128), 1.0),
    ("2D grid 16x16", make_grid(16), 2.0),
    ("4D hypercube N=16", make_hypercube(4), 4.0),
]:
    A = W.astype(float)
    da, _, _ = d_s_heatkernel_normalized(A)
    db, _, _, _ = d_s_lazy_walk(A)
    print(f"  {name:20s} expect {expect}:  A={da:5.2f}   B={db:5.2f}")

# Sierpinski triangle (fractal dim log3/log2 ~ 1.585; spectral ~ 2*log3/log5... ~1.36)
def sierpinski(depth):
    """2D Sierpinski gasket adjacency (standard)."""
    if depth == 0:
        W = np.zeros((3, 3))
        W[0, 1] = W[1, 0] = W[1, 2] = W[2, 1] = W[0, 2] = W[2, 0] = 1.0
        return W
    W0 = sierpinski(depth - 1)
    n = W0.shape[0]
    W = np.zeros((3 * n, 3 * n))
    W[:n, :n] = W0
    W[n:2 * n, n:2 * n] = W0
    W[2 * n:, 2 * n:] = W0
    W[0, 2 * n] = W[2 * n, 0] = 1.0
    W[n - 1, n] = W[n, n - 1] = 1.0
    W[2 * n - 1, 2 * n] = W[2 * n, 2 * n - 1] = 1.0
    return W


A = sierpinski(5).astype(float)
da, _, _ = d_s_heatkernel_normalized(A)
db, _, _, _ = d_s_lazy_walk(A)
print(f"  {'Sierpinski d=5 (expect ~1.4-1.6)':20s}        A={da:5.2f}   B={db:5.2f}")

rng = np.random.default_rng(3)
Wr = rng.uniform(0.1, 1.0, (64, 64))
Wr = 0.5 * (Wr + Wr.T)
np.fill_diagonal(Wr, 0.0)
da, _, _ = d_s_heatkernel_normalized(Wr)
db, _, _, _ = d_s_lazy_walk(Wr)
print(f"  {'Random dense N=64 (ref)':20s}                A={da:5.2f}   B={db:5.2f}")

# ---------------- 2. HYPERGRAPH ----------------
print()
print("=" * 74)
print(" 2. Hypergraph v10: correct d_s (N=8..32, 5 seeds, n_therm=60)")
print("=" * 74)
sizes = [8, 12, 16, 24, 32]
seeds = [42, 43, 44, 45, 46]
results = {}

for N in sizes:
    da_list, db_list, r_list, lmax_list = [], [], [], []
    for s in seeds:
        r_h, r_std, align, dmm_old, l_max, obs_ext, T = run_v10(
            N=N, d=3, g_xy=0.8, g_yx=0.0, n_therm=60, n_measure=40, seed=s
        )
        A = 0.5 * (project_hypergraph_weff(T) + project_hypergraph_weff(T).T)
        da, _, _ = d_s_heatkernel_normalized(A)
        db, _, _, _ = d_s_lazy_walk(A)
        da_list.append(da)
        db_list.append(db)
        r_list.append(r_h)
        lmax_list.append(l_max)
    results[f"N_{N}"] = {
        "N": N,
        "d_s_heatkernel": float(np.mean(da_list)),
        "std": float(np.std(da_list)),
        "d_s_lazywalk": float(np.mean(db_list)),
        "mean_r_hyper": float(np.mean(r_list)),
        "mean_L_max": float(np.mean(lmax_list)),
    }
    print(
        f"  N={N:2d} | heat-kernel d_s: {np.mean(da_list):5.2f} +/- {np.std(da_list):.2f} | "
        f"lazy-walk d_s: {np.mean(db_list):5.2f} | R: {np.mean(r_list):.4f} | Lmax: {np.mean(lmax_list):6.1f}"
    )

out_file = "audit_spectral_dimension_correct_results.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print(f"\n[Done] Saved to: {out_file}")
