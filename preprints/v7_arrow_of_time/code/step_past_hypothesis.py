"""
Past Hypothesis test (self-written): arrow of time from relaxation of a
special (low-entropy) initial state, on the v7 matrix model.
Initial states:
  - random  : high entropy (baseline — what we always did)
  - rank1   : X_mu = c * u u^T  (single direction — very special/low entropy)
  - uniform : near-constant matrix (deterministic — lowest entropy)
Measure relaxation S(t): half-life, total dS, and how "long" the flow of time is.
"""
import sys
import numpy as np
sys.path.insert(0, ".")
from sgoed_core_v7 import action_v7


def relax(N, D, d, gXY, init_type, n_sweeps, seed, max_extent=10.0):
    rng = np.random.RandomState(seed)
    X = np.zeros((D, N, N))
    for mu in range(D):
        if init_type == "random":
            A = rng.randn(N, N) * 0.5
            X[mu] = (A + A.T) / 2
        elif init_type == "rank1":
            u = rng.randn(N)
            u /= np.linalg.norm(u)
            X[mu] = 4.0 * np.outer(u, u)  # rank-1, large extent
        elif init_type == "uniform":
            X[mu] = 1.0 * np.ones((N, N)) + 0.01 * rng.randn(N, N)
            np.fill_diagonal(X[mu], 0.0)
    Y = np.zeros((d, N, N))
    for a in range(d):
        A = rng.randn(N, N) * 0.3
        Y[a] = (A + A.T) / 2
    S = action_v7(X, Y, gXY, 0.0, max_extent=max_extent)
    S_traj = [S]
    for sweep in range(n_sweeps):
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    old = X[mu, i, j]
                    X[mu, i, j] = old + 0.25 * rng.randn()
                    if i != j:
                        X[mu, j, i] = X[mu, i, j]
                    S2 = action_v7(X, Y, gXY, 0.0, max_extent=max_extent)
                    dS = S2 - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = S2
                    else:
                        X[mu, i, j] = old
                        if i != j:
                            X[mu, j, i] = old
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    old = Y[a, i, j]
                    Y[a, i, j] = old + 0.25 * rng.randn()
                    if i != j:
                        Y[a, j, i] = Y[a, i, j]
                    S2 = action_v7(X, Y, gXY, 0.0, max_extent=max_extent)
                    dS = S2 - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = S2
                    else:
                        Y[a, i, j] = old
                        if i != j:
                            Y[a, j, i] = old
        S_traj.append(S)
    return np.array(S_traj)


def analyze(S_traj):
    S0 = S_traj[0]
    Seq = S_traj[-10:].mean()
    dS = S0 - Seq
    half = None
    for t, s in enumerate(S_traj):
        if s < S0 - dS / 2:
            half = t
            break
    # how far from equilibrium initially (relative relaxation needed)
    return S0, Seq, dS, half if half is not None else len(S_traj)


print("=" * 80)
print(" PAST HYPOTHESIS: v7 matrix relaxation (N=4, D=2, d=2, 3 seeds)")
print("=" * 80)
for gXY in [0.0, 0.8]:
    print(f"\n--- gXY = {gXY} ---")
    for init in ["random", "rank1", "uniform"]:
        dSs, halves, S0s = [], [], []
        for s in [42, 43, 44]:
            S_traj = relax(4, 2, 2, gXY, init, 60, s)
            S0, Seq, dS, half = analyze(S_traj)
            dSs.append(dS)
            halves.append(half)
            S0s.append(S0)
        print(f"  [{init:7s}] S0={np.mean(S0s):8.1f} | dS_total={np.mean(dSs):8.1f} "
              f"| half-life={np.mean(halves):5.1f} sweeps | dS/S0={np.mean(dSs)/np.mean(S0s):.2f}")
