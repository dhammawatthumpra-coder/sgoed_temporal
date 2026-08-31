"""
Sequential Growth (CSG-style) on v14 matrix-units (self-written).
Time = BIRTH ORDER: units are born one by one; older units are FROZEN (past),
new units thermalize against them (future adapts to past).
  - unit 0 = origin (creates the first direction)
  - unit k born -> coupled to units 0..k-1 -> aligns with the inherited past
Arrow is asymmetric by construction (birth is not reversible).
Measure: fraction of units aligned with the ORIGIN (unit 0) + chain inheritance.
"""
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, "../code")
from sgoed_matrix_ecosystem_v14 import action_v14
from sgoed_core_v7 import action_v7, _compute_v_hat


def sequential_growth(M, N, D, d, g_inter, n_therm_new, seed):
    rng = np.random.RandomState(seed)
    Xs = np.zeros((M, D, N, N))
    Ys = np.zeros((M, d, N, N))

    def init_unit(u):
        for mu in range(D):
            A = rng.randn(N, N) * 0.5
            Xs[u, mu] = (A + A.T) / 2
        for a in range(d):
            A = rng.randn(N, N) * 0.3
            Ys[u, a] = (A + A.T) / 2

    vhat_cache = []  # frozen v_hat per born unit (past never changes)
    vsum = []        # prefix sum of vhat_cache -> inter_energy in O(1)

    def inter_energy(u):
        # coupling of unit u to all older units j < u (past is frozen):
        # sum_j (vu.vj) = vu . (sum_j vj)  -- prefix-sum makes this O(1).
        S = 0.0
        if g_inter > 0.0 and u > 0:
            vu = _compute_v_hat(Ys[u], D)
            S -= g_inter * float(vu @ vsum[u - 1])
        return S

    # unit 0: origin (thermalize alone)
    init_unit(0)
    S = action_v7(Xs[0], Ys[0], 0.8, 0.0)
    for _ in range(n_therm_new):
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    old = Xs[0, mu, i, j]
                    Xs[0, mu, i, j] = old + 0.25 * rng.randn()
                    if i != j:
                        Xs[0, mu, j, i] = Xs[0, mu, i, j]
                    S2 = action_v7(Xs[0], Ys[0], 0.8, 0.0)
                    dS = S2 - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = S2
                    else:
                        Xs[0, mu, i, j] = old
                        if i != j:
                            Xs[0, mu, j, i] = old
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    old = Ys[0, a, i, j]
                    Ys[0, a, i, j] = old + 0.25 * rng.randn()
                    if i != j:
                        Ys[0, a, j, i] = Ys[0, a, i, j]
                    S2 = action_v7(Xs[0], Ys[0], 0.8, 0.0)
                    dS = S2 - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = S2
                    else:
                        Ys[0, a, i, j] = old
                        if i != j:
                            Ys[0, a, j, i] = old
    vhat_cache.append(_compute_v_hat(Ys[0], D))
    vsum.append(vhat_cache[0])

    # units 1..M-1 born sequentially, adapting to frozen past
    for u in range(1, M):
        init_unit(u)
        S = action_v7(Xs[u], Ys[u], 0.8, 0.0) + inter_energy(u)
        for _ in range(n_therm_new):
            for mu in range(D):
                for i in range(N):
                    for j in range(i, N):
                        old = Xs[u, mu, i, j]
                        Xs[u, mu, i, j] = old + 0.25 * rng.randn()
                        if i != j:
                            Xs[u, mu, j, i] = Xs[u, mu, i, j]
                        S2 = action_v7(Xs[u], Ys[u], 0.8, 0.0) + inter_energy(u)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Xs[u, mu, i, j] = old
                            if i != j:
                                Xs[u, mu, j, i] = old
            for a in range(d):
                for i in range(N):
                    for j in range(i, N):
                        old = Ys[u, a, i, j]
                        Ys[u, a, i, j] = old + 0.25 * rng.randn()
                        if i != j:
                            Ys[u, a, j, i] = Ys[u, a, i, j]
                        S2 = action_v7(Xs[u], Ys[u], 0.8, 0.0) + inter_energy(u)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Ys[u, a, i, j] = old
                            if i != j:
                                Ys[u, a, j, i] = old
        vhat_cache.append(_compute_v_hat(Ys[u], D))
        vsum.append(vsum[-1] + vhat_cache[-1])
    return Xs, Ys


if __name__ == "__main__":
    print("=" * 80)
    print(" SEQUENTIAL GROWTH: M=8 units born one-by-one (past frozen)")
    print("=" * 80)
    for g in [0.0, 1.0, 5.0, 20.0]:
        fracs_align, fracs_chain = [], []
        for s in [42, 43, 44]:
            Xs, Ys = sequential_growth(8, 4, 2, 2, g, 30, s)
            vhats = [_compute_v_hat(Ys[u], 2) for u in range(8)]
            v0 = vhats[0]
            n_align = sum(1 for u in range(1, 8) if abs(float(vhats[u] @ v0)) > 0.9)
            n_chain = sum(1 for u in range(1, 8) if abs(float(vhats[u] @ vhats[u - 1])) > 0.9)
            fracs_align.append(n_align / 7)
            fracs_chain.append(n_chain / 7)
        print(f"  g={g:5.1f}: units aligned with ORIGIN (unit 0): {np.mean(fracs_align):.2f} | "
              f"chain inheritance (v_k~v_k-1): {np.mean(fracs_chain):.2f}")
