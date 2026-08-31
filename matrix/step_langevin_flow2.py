"""Langevin flow with GROWTH pump (F=+gX) at unit 0."""
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, r"F:\_Ai\sgoed\V5\code")
from step_langevin_flow import grad_num, measure


def langevin_flow2(M, N, D, d, g_inter, g_drive, gamma, dt, T, n_steps, seed):
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
    noise = np.sqrt(2.0 * T * dt)
    for step in range(n_steps):
        gX, gY = grad_num(Xs, Ys, g_inter)
        for u in range(M):
            F = np.zeros_like(Xs[u])
            if u == 0 and g_drive > 0.0:
                F = g_drive * Xs[u]  # growth pump, balanced by gamma
            Xs[u] += dt * (-gX[u] + F) - gamma * dt * Xs[u] + noise * rng.randn(*Xs[u].shape)
            Ys[u] += dt * (-gY[u]) - gamma * dt * Ys[u] + noise * rng.randn(*Ys[u].shape)
            for mu in range(D):
                Xs[u, mu] = (Xs[u, mu] + Xs[u, mu].T) / 2
            for a in range(d):
                Ys[u, a] = (Ys[u, a] + Ys[u, a].T) / 2
    return Xs, Ys


if __name__ == "__main__":
    print("GROWTH pump at unit 0: M=8, N=4, 2 seeds")
    for gd, gm in [(0.5, 0.5), (1.0, 1.0)]:
        Eprof, aligns = [], []
        for s in [42, 43]:
            Xs, Ys = langevin_flow2(8, 4, 2, 2, 5.0, gd, gm, 0.005, 0.5, 150, s)
            E, al = measure(Xs, Ys)
            Eprof.append(E)
            aligns.append(al)
        Emean = np.mean(Eprof, axis=0)
        dec = all(Emean[u] > Emean[u + 1] - 0.3 for u in range(7))
        es = ", ".join(f"{e:.1f}" for e in Emean)
        print(f"  drive={gd} gamma={gm}: E=[{es}] | decreasing={dec} | align={np.mean(aligns):.2f}")
