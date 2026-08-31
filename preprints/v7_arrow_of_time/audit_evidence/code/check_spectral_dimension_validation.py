"""
Critical validation of audit_spectral_dimension.py claims (self-written, data honesty).
Checks:
  1. compute_spectral_dimension on graphs with KNOWN spectral dimension
     (undirected path -> d_s=1, 2D grid -> d_s=2, complete graph -> d_s->N-1, directed chain)
  2. d_MM_cont on NULL random data (does it discriminate noise from structure?)
  3. p_return(tau) decay shape at N=48 (is d_s~0 real or method artifact?)
  4. N=48 L_max=7.4 anomaly: thermalization scan
"""
import time
import numpy as np
from audit_spectral_dimension import (
    compute_spectral_dimension,
    compute_continuous_dmm,
    project_hypergraph_to_transition_matrix,
)
from sgoed_hypergraph_core_v10 import run_v10


def undirected_p(pair_W):
    """Row-stochastic P from a symmetric weight matrix (as in the audit code path)."""
    N = pair_W.shape[0]
    P = np.zeros((N, N))
    for i in range(N):
        rs = pair_W[i].sum()
        if rs > 1e-12:
            P[i] = pair_W[i] / rs
        else:
            P[i] = 1.0 / N
    return P


print("=" * 70)
print(" 1. METHOD VALIDATION: d_s on graphs with KNOWN answer")
print("=" * 70)

# 1a. Undirected path graph N=32 (known d_s = 1)
N = 32
W_path = np.zeros((N, N))
for i in range(N - 1):
    W_path[i, i + 1] = 1.0
    W_path[i + 1, i] = 1.0
d_s, pr = compute_spectral_dimension(undirected_p(W_path))
print(f"  Path graph (known d_s=1):       d_s = {d_s:6.3f}   (p_return: {[f'{p:.3f}' for p in pr]})")

# 1b. Undirected 2D grid N=36 (known d_s = 2)
g = 6
W_grid = np.zeros((g * g, g * g))
for i in range(g):
    for j in range(g):
        idx = i * g + j
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < g and 0 <= nj < g:
                W_grid[idx, ni * g + nj] = 1.0
d_s, pr = compute_spectral_dimension(undirected_p(W_grid))
print(f"  2D grid 6x6 (known d_s=2):      d_s = {d_s:6.3f}")

# 1c. Complete graph N=32 (known d_s -> large, ~N)
W_comp = np.ones((N, N)) - np.eye(N)
d_s, pr = compute_spectral_dimension(undirected_p(W_comp))
print(f"  Complete graph (known d_s~N):   d_s = {d_s:6.3f}")

# 1d. Directed chain (pure arrow, NO reverse edges): what does the method give?
W_chain = np.zeros((N, N))
for i in range(N - 1):
    W_chain[i, i + 1] = 1.0  # strictly forward
P_chain = undirected_p(W_chain)
d_s, pr = compute_spectral_dimension(P_chain)
print(f"  Directed chain (strict arrow):  d_s = {d_s:6.3f}   (p_return: {[f'{p:.4f}' for p in pr]})")

# 1e. Directed chain WITH slight reverse (realistic)
W_chain2 = W_chain.copy()
for i in range(N - 1):
    W_chain2[i + 1, i] = 0.02
d_s, pr = compute_spectral_dimension(undirected_p(W_chain2))
print(f"  Directed chain + 2% reverse:    d_s = {d_s:6.3f}")

print()
print("=" * 70)
print(" 2. NULL TEST: d_MM_cont on random (structureless) W_eff")
print("=" * 70)
rng = np.random.default_rng(0)
for N in [16, 32]:
    Wr = rng.uniform(0.05, 0.3, (N, N))
    Wr[np.arange(N), np.arange(N)] = 0.0
    # asymmetric: Wr[i,j] = base + noise -> net flow random
    d_null = compute_continuous_dmm(Wr)
    # strongly asymmetric random:
    Wr2 = rng.uniform(0.0, 1.0, (N, N)) * rng.uniform(0.0, 1.0, (N, N))
    Wr2[np.arange(N), np.arange(N)] = 0.0
    d_null2 = compute_continuous_dmm(Wr2)
    print(f"  N={N}: d_cont(random uniform)={d_null:.3f} | d_cont(random asy)={d_null2:.3f}")

print()
print("=" * 70)
print(" 3. N=48 L_max anomaly: thermalization scan")
print("=" * 70)
for therm in [60, 120, 240]:
    t0 = time.time()
    lmaxs, rlist = [], []
    for s in [42, 43]:
        r_h, r_std, align, dmm_old, l_max, obs_ext, T = run_v10(
            N=48, d=3, g_xy=0.8, g_yx=0.0,
            n_therm=therm, n_measure=20, seed=s
        )
        lmaxs.append(l_max)
        rlist.append(r_h)
    print(f"  N=48 n_therm={therm:3d}: L_max={np.mean(lmaxs):8.1f} (seeds {[f'{x:.0f}' for x in lmaxs]}) "
          f"R_hyper={np.mean(rlist):.4f} | {time.time()-t0:.1f}s")
