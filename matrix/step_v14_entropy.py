"""
v14 entropy production test (self-written).
Arrow-of-time via stochastic thermodynamics: during thermalization the action S
(energy at T=1) decreases from a random initial state to equilibrium.
  - total entropy produced: dS = S_init - S_eq
  - rate: time constant (sweep to half-decrease)
Compare: coupled (g_inter>0) vs null (g_inter=0) — does coupling change the
"flow of time" (entropy production)?
"""
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, "../code")
from sgoed_matrix_ecosystem_v14 import action_v14


def run_S_traj(M, N, D, d, g_inter, n_therm, seed):
    rng = np.random.RandomState(seed)
    Xs = np.zeros((M, D, N, N))
    Ys = np.zeros((M, d, N, N))
    for u in range(M):
        for mu in range(D):
            A = rng.randn(N, N) * 0.5
            Xs[u, mu] = (A + A.T) / 2
        for a in range(d):
            A = rng.randn(N, N) * 0.3
            Ys[u, a] = (A + A.T) / 2
    S = action_v14(Xs, Ys, g_inter)
    S_traj = [S]
    for sweep in range(n_therm):
        for u in range(M):
            for mu in range(D):
                for i in range(N):
                    for j in range(i, N):
                        old = Xs[u, mu, i, j]
                        Xs[u, mu, i, j] = old + 0.15 * rng.randn()
                        if i != j:
                            Xs[u, mu, j, i] = Xs[u, mu, i, j]
                        S2 = action_v14(Xs, Ys, g_inter)
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
                        Ys[u, a, i, j] = old + 0.15 * rng.randn()
                        if i != j:
                            Ys[u, a, j, i] = Ys[u, a, i, j]
                        S2 = action_v14(Xs, Ys, g_inter)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Ys[u, a, i, j] = old
                            if i != j:
                                Ys[u, a, j, i] = old
        S_traj.append(S)
    return np.array(S_traj)


def analyze(S_traj):
    S_init = S_traj[0]
    S_eq = S_traj[-10:].mean()
    dS = S_init - S_eq
    # half-life: first sweep where S < S_init - dS/2
    half = None
    for t, s in enumerate(S_traj):
        if s < S_init - dS / 2:
            half = t
            break
    return S_init, S_eq, dS, half if half is not None else len(S_traj)


print("=" * 78)
print(" ENTROPY PRODUCTION: M=8, N=4, n_therm=60, 3 seeds")
print("=" * 78)
print(f"  {'g_inter':>7} | {'S_init':>9} | {'S_eq':>9} | {'dS (total)':>10} | "
      f"{'dS/S_init':>9} | {'half-life':>8}")
for g in [0.0, 5.0, 20.0]:
    dSs, rels, halves = [], [], []
    for s in [42, 43, 44]:
        S_traj = run_S_traj(8, 4, 2, 2, g, 60, s)
        Si, Seq, dS, half = analyze(S_traj)
        dSs.append(dS)
        rels.append(dS / Si)
        halves.append(half)
    print(f"  {g:7.1f} | {Si:9.1f} | {Seq:9.1f} | {np.mean(dSs):10.1f} | "
          f"{np.mean(rels):9.3f} | {np.mean(halves):8.1f}")
