"""
v13/v12 cycle-ratio (feed-forward) test (self-written, data honesty).
Cycle ratio = #cyclic triples / (#cyclic + #acyclic) over unordered triples.
  d_ij = sign(W_ij - W_ji); cyclic iff d_ij * d_jk * d_ki > 0.
  - feed-forward (arrow of time): ratio << 0.5
  - random: ratio ~ 0.5
Invariant to labeling by construction (cycle count is label-independent).
"""
import numpy as np
from sgoed_graph_core_v13 import run_v13
from sgoed_graph_core_v12 import run_v12


def cycle_ratio(W, eps=1e-6):
    N = W.shape[0]
    d = np.zeros((N, N))
    diff = W - W.T
    d[diff > eps] = 1.0
    d[diff < -eps] = -1.0
    cyc = 0
    acyc = 0
    for i in range(N):
        for j in range(i + 1, N):
            dij = d[i, j]
            if dij == 0:
                continue
            for k in range(j + 1, N):
                djk = d[j, k]
                dki = d[k, i]
                if djk == 0 or dki == 0:
                    continue
                p = dij * djk * dki
                if p > 0:
                    cyc += 1
                else:
                    acyc += 1
    total = cyc + acyc
    return cyc / total if total > 0 else 0.5, cyc, acyc


def value_shuffle(W, rng):
    N = W.shape[0]
    mask = ~np.eye(N, dtype=bool)
    vals = W[mask]
    W2 = W.copy()
    W2[mask] = rng.permutation(vals)
    return W2


print("=" * 78)
print(" CYCLE RATIO (feed-forward test) — N=32, 10 seeds")
print("=" * 78)
rng = np.random.default_rng(9)
configs = []

# v13 runs
for g_f, g_b, p_b, tag in [(0.0, 0.0, 2, "v13 baseline (0,0)"),
                           (1.5, 0.0, 2, "v13 forward only"),
                           (1.5, 0.2, 2, "v13 asym g_b=0.2")]:
    crs, nulls = [], []
    for s in range(42, 52):
        D, Dr, spec, align, W = run_v13(N=32, d=3, g_f=g_f, g_b=g_b, p_b=p_b,
                                        n_therm=120, n_measure=30, seed=s)
        cr, c, a = cycle_ratio(W)
        crs.append(cr)
        nc, _, _ = cycle_ratio(value_shuffle(W, rng))
        nulls.append(nc)
    print(f"  [{tag:22s}] cycle_ratio={np.mean(crs):.4f} +/- {np.std(crs):.4f} | "
          f"null(shuffle)={np.mean(nulls):.4f} +/- {np.std(nulls):.4f}")

# v12 runs
for g_xy, lam, tag in [(0.0, 0.0, "v12 baseline (0,0)"),
                       (1.5, 0.15, "v12 full (lam=0.15)")]:
    crs, nulls = [], []
    for s in range(42, 52):
        D, F, spec, align, W = run_v12(N=32, d=3, g_xy=g_xy, lambda_cond=lam,
                                       n_therm=40, n_measure=20, seed=s)
        cr, c, a = cycle_ratio(W)
        crs.append(cr)
        nc, _, _ = cycle_ratio(value_shuffle(W, rng))
        nulls.append(nc)
    print(f"  [{tag:22s}] cycle_ratio={np.mean(crs):.4f} +/- {np.std(crs):.4f} | "
          f"null(shuffle)={np.mean(nulls):.4f} +/- {np.std(nulls):.4f}")

print()
print("=" * 78)
print(" PERMUTATION INVARIANCE SANITY (v13 asym seed 42)")
print("=" * 78)
D, Dr, spec, align, W = run_v13(N=32, d=3, g_f=1.5, g_b=0.2, p_b=2,
                                n_therm=120, n_measure=30, seed=42)
cr0, _, _ = cycle_ratio(W)
print(f"  original cycle_ratio = {cr0:.4f}")
for rep in range(5):
    perm = rng.permutation(32)
    cr, _, _ = cycle_ratio(W[np.ix_(perm, perm)])
    print(f"  perm {rep}: {cr:.4f}")
