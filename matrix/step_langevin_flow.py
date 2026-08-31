"""
Non-Equilibrium Flow with REAL dissipation (Langevin dynamics) — v14 matrix units.
Update:  X <- X + dt*(-grad S + F_drive) - gamma*X*dt + noise
  - F_drive: pump at unit 0 (source) — pushes along its own direction
  - gamma  : friction/dissipation (sink — pulls all X toward 0)
  - coupling (in S): align v_hat between units (flow channel 0 -> M-1)
Steady state is NON-equilibrium: energy pumped at 0, dissipated everywhere.
Measure: extent gradient E(0) > E(1) > ... (flow direction) + v_hat alignment.
"""
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, r"F:\_Ai\sgoed\V5\code")
from sgoed_matrix_ecosystem_v14 import action_v14
from sgoed_core_v7 import _compute_v_hat


def grad_num(Xs, Ys, g_inter, eps=1e-4):
    M, D, N, _ = Xs.shape
    d = Ys.shape[1]
    gX = np.zeros_like(Xs)
    gY = np.zeros_like(Ys)
    for u in range(M):
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    old = Xs[u, mu, i, j]
                    Xs[u, mu, i, j] = old + eps
                    if i != j:
                        Xs[u, mu, j, i] = Xs[u, mu, i, j]
                    Sp = action_v14(Xs, Ys, g_inter)
                    Xs[u, mu, i, j] = old - eps
                    if i != j:
                        Xs[u, mu, j, i] = Xs[u, mu, i, j]
                    Sm = action_v14(Xs, Ys, g_inter)
                    gX[u, mu, i, j] = (Sp - Sm) / (2 * eps)
                    if i != j:
                        gX[u, mu, j, i] = gX[u, mu, i, j]
                    Xs[u, mu, i, j] = old
                    if i != j:
                        Xs[u, mu, j, i] = old
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    old = Ys[u, a, i, j]
                    Ys[u, a, i, j] = old + eps
                    if i != j:
                        Ys[u, a, j, i] = Ys[u, a, i, j]
                    Sp = action_v14(Xs, Ys, g_inter)
                    Ys[u, a, i, j] = old - eps
                    if i != j:
                        Ys[u, a, j, i] = Ys[u, a, i, j]
                    Sm = action_v14(Xs, Ys, g_inter)
                    gY[u, a, i, j] = (Sp - Sm) / (2 * eps)
                    if i != j:
                        gY[u, a, j, i] = gY[u, a, i, j]
                    Ys[u, a, i, j] = old
                    if i != j:
                        Ys[u, a, j, i] = old
    return gX, gY


def langevin_flow(M, N, D, d, g_inter, g_drive, gamma, dt, T, n_steps, seed):
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
                # pump: push unit 0 along its own dominant direction
                nX = np.linalg.norm(Xs[u]) + 1e-8
                F = g_drive * (Xs[u] / nX)
            Xs[u] += dt * (-gX[u] + F) - gamma * dt * Xs[u] + noise * rng.randn(*Xs[u].shape)
            Ys[u] += dt * (-gY[u]) - gamma * dt * Ys[u] + noise * rng.randn(*Ys[u].shape)
            for mu in range(D):
                Xs[u, mu] = (Xs[u, mu] + Xs[u, mu].T) / 2
            for a in range(d):
                Ys[u, a] = (Ys[u, a] + Ys[u, a].T) / 2
    return Xs, Ys


def measure(Xs, Ys):
    M, D, N, _ = Xs.shape
    E = [float(np.trace(Xs[u, 0] @ Xs[u, 0])) / N for u in range(M)]
    vhats = [_compute_v_hat(Ys[u], D) for u in range(M)]
    align = np.mean([abs(float(vhats[u] @ vhats[0])) for u in range(M)])
    return E, align


if __name__ == "__main__":
    print("=" * 78)
    print(" LANGEVIN NON-EQUILIBRIUM FLOW: M=8, N=4, pump@0, friction gamma")
    print("=" * 78)
    for g_drive, gamma, tag in [(0.5, 0.1, "weak drive "),
                                (2.0, 0.1, "strong drive"),
                                (2.0, 0.5, "drive+strong friction")]:
        Eprof, aligns = [], []
        for s in [42, 43]:
            Xs, Ys = langevin_flow(8, 4, 2, 2, 5.0, g_drive, gamma, 0.005, 0.5, 150, s)
            E, al = measure(Xs, Ys)
            Eprof.append(E)
            aligns.append(al)
        Emean = np.mean(Eprof, axis=0)
        grad = all(Emean[u] > Emean[u + 1] - 0.3 for u in range(7))
        print(f"  [{tag}] E=[{', '.join(f'{e:.1f}' for e in Emean)}] | "
              f"decreasing: {grad} | align={np.mean(aligns):.2f}")
