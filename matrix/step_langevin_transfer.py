"""
Extent-transfer non-equilibrium flow (Langevin) — v14 matrix units.
Action:
  S = sum_u S_v7(X_u,Y_u)
      - g_a * sum_u (v_u . v_{u+1})                 [align chain]
      - g_t * sum_u (E_u - E_{u+1}) * (v_u . v_{u+1}) [extent transfer: flow downhill]
      - g_p * E_0                                     [pump at source, via gradient]
Langevin: X <- X + dt*(-grad S) - gamma*X*dt + noise  (dissipation real)
Expect: E decreases monotonically 0 -> M-1 (time flowing downhill) + aligned.
"""
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, r"F:\_Ai\sgoed\sgoed\code")
from sgoed_matrix_ecosystem_v14 import action_v14
from sgoed_core_v7 import action_v7, _compute_v_hat


def make_action(g_a, g_t, g_p, g_xy=0.8):
    def act(Xs, Ys):
        M, D, N, _ = Xs.shape
        S = 0.0
        vhats = []
        E = []
        for u in range(M):
            S += action_v7(Xs[u], Ys[u], g_xy, 0.0)
            vhats.append(_compute_v_hat(Ys[u], D))
            E.append(float(np.trace(Xs[u, 0] @ Xs[u, 0])) / N)
        if g_a > 0.0:
            for u in range(M - 1):
                S -= g_a * float(vhats[u] @ vhats[u + 1])
        if g_t > 0.0:
            for u in range(M - 1):
                S -= g_t * (E[u] - E[u + 1]) * float(vhats[u] @ vhats[u + 1])
        if g_p > 0.0:
            S -= g_p * E[0]
        return S
    return act


def grad_num(Xs, Ys, act, eps=1e-4):
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
                    Sp = act(Xs, Ys)
                    Xs[u, mu, i, j] = old - eps
                    if i != j:
                        Xs[u, mu, j, i] = Xs[u, mu, i, j]
                    Sm = act(Xs, Ys)
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
                    Sp = act(Xs, Ys)
                    Ys[u, a, i, j] = old - eps
                    if i != j:
                        Ys[u, a, j, i] = Ys[u, a, i, j]
                    Sm = act(Xs, Ys)
                    gY[u, a, i, j] = (Sp - Sm) / (2 * eps)
                    if i != j:
                        gY[u, a, j, i] = gY[u, a, i, j]
                    Ys[u, a, i, j] = old
                    if i != j:
                        Ys[u, a, j, i] = old
    return gX, gY


def langevin(M, N, D, d, act, gamma, dt, T, n_steps, seed):
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
        gX, gY = grad_num(Xs, Ys, act)
        for u in range(M):
            Xs[u] += dt * (-gX[u]) - gamma * dt * Xs[u] + noise * rng.randn(*Xs[u].shape)
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
    print("EXTENT-TRANSFER FLOW (Langevin): M=8, N=4, pump@0 via action, gamma=0.5")
    for g_t, tag in [(0.0, "null (no transfer)"), (1.0, "transfer g_t=1  "),
                     (3.0, "transfer g_t=3  ")]:
        act = make_action(g_a=5.0, g_t=g_t, g_p=2.0)
        Eprof, aligns = [], []
        for s in [42, 43]:
            Xs, Ys = langevin(8, 4, 2, 2, act, 0.5, 0.005, 0.5, 150, s)
            E, al = measure(Xs, Ys)
            Eprof.append(E)
            aligns.append(al)
        Emean = np.mean(Eprof, axis=0)
        dec = all(Emean[u] > Emean[u + 1] - 0.3 for u in range(7))
        es = ", ".join(f"{e:.1f}" for e in Emean)
        print(f"  [{tag}] E=[{es}] | decreasing={dec} | align={np.mean(aligns):.2f}")
