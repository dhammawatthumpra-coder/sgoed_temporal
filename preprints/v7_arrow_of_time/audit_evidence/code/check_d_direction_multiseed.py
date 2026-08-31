"""Multi-seed D_direction check for graph v8 (the only non-null signal found)."""
import numpy as np
from numba import njit
from sgoed_graph_core_v8 import run_v8
from sgoed_hypergraph_core_v10 import run_v10


@njit(fastmath=True)
def D_direction(W):
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


print("graph v8 (N=16, d=3, g_xy=0.8, n_therm=240):")
Ds = []
for s in [42, 43, 44, 45, 46]:
    r_mean, r_std, aln, _, _, ext, W = run_v8(
        N=16, d=3, g_xy=0.8, g_yx=0.0, n_therm=240, n_measure=40, seed=s
    )
    d = D_direction(W)
    Ds.append(d)
    print(f"  seed {s}: D = {d:+.0f} (max {16*15/2:.0f}) | R = {r_mean:.4f} | align = {aln:.2f}")
print(f"  -> mean D = {np.mean(Ds):+.1f} +/- {np.std(Ds):.1f} | p(|D|~22) under null sigma~7.3")

print()
print("hypergraph v10 (N=32, d=3, g_xy=0.8, n_therm=60):")
Ds = []
for s in [42, 43, 44, 45, 46]:
    r_h, r_std, align, dmm, l_max, ext, T = run_v10(
        N=32, d=3, g_xy=0.8, g_yx=0.0, n_therm=60, n_measure=40, seed=s
    )
    # pairwise projection W_eff (as in previous audit)
    N = T.shape[0]
    W_eff = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                ssum = 0.0
                for k in range(N):
                    if k != i and k != j:
                        ssum += T[i, k, j] + T[i, j, k]
                W_eff[i, j] = ssum
    d = D_direction(W_eff)
    Ds.append(d)
    print(f"  seed {s}: D = {d:+.0f} (max {N*(N-1)/2:.0f}) | R = {r_h:.4f} | align = {align:.2f}")
print(f"  -> mean D = {np.mean(Ds):+.1f} +/- {np.std(Ds):.1f} (null: -6 +/- 13)")
