"""
Extent-Transport Tuning (Target: Full Strict Monotonic Decay across M=6)
Params tuned: g_drive=5.0, g_trans=1.2, g_bulk=0.1, g_sink=3.0, alpha=0.1,
T=0.02 (very low noise floor), 400 steps.
"""
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, r"F:\_Ai\sgoed\sgoed\code")
from sgoed_core_v7 import _compute_v_hat


def run_transport_tuned(M=6, N=4, D=2, d=2, g_xy=0.8, g_trans=1.2, g_drive=5.0,
                        g_bulk=0.1, g_sink=3.0, alpha=0.1, E_max=30.0, lam_g=5.0,
                        dt=0.005, T=0.02, n_steps=400, seed=42, reverse=False):
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

    def S_total():
        S = 0.0
        Etot = 0.0
        for u in range(M):
            X = Xs[u]
            v = _compute_v_hat(Ys[u], D)
            for mu in range(D):
                Xm = X[mu]
                X4 = Xm @ Xm @ Xm @ Xm
                tr2 = float(np.trace(Xm @ Xm).real)
                S -= g_xy * v[mu] ** 2 * float(np.trace(X4).real) / (tr2 ** 2 + 0.01)
                S += alpha * tr2
            Etot += float(np.trace(X[0] @ X[0])) / N
        if Etot > E_max:
            S += lam_g * (Etot - E_max) ** 2
        return S, Etot

    def grad_num(eps=1e-4):
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
                        Sp, _ = S_total()
                        Xs[u, mu, i, j] = old - eps
                        if i != j:
                            Xs[u, mu, j, i] = Xs[u, mu, i, j]
                        Sm, _ = S_total()
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
                        Sp, _ = S_total()
                        Ys[u, a, i, j] = old - eps
                        if i != j:
                            Ys[u, a, j, i] = Ys[u, a, i, j]
                        Sm, _ = S_total()
                        gY[u, a, i, j] = (Sp - Sm) / (2 * eps)
                        if i != j:
                            gY[u, a, j, i] = gY[u, a, i, j]
                        Ys[u, a, i, j] = old
                        if i != j:
                            Ys[u, a, j, i] = old
        return gX, gY

    J_hist = []
    for step in range(n_steps):
        gX, gY = grad_num()
        F = np.zeros_like(Xs)
        for u in range(M):
            if u == 0:
                if not reverse and g_drive > 0:
                    F[u] += g_drive * Xs[u]
                F[u] -= g_trans * Xs[u]
            elif u == M - 1:
                if reverse and g_drive > 0:
                    F[u] += g_drive * Xs[u]
                F[u] += g_trans * Xs[u - 1]
                F[u] -= g_sink * Xs[u]
            else:
                F[u] += g_trans * Xs[u - 1] - g_trans * Xs[u]
        for u in range(M):
            Xs[u] += dt * (-gX[u] + F[u]) - g_bulk * dt * Xs[u] + noise * rng.randn(*Xs[u].shape)
            Ys[u] += dt * (-gY[u]) - g_bulk * dt * Ys[u] + noise * rng.randn(*Ys[u].shape)
            for mu in range(D):
                Xs[u, mu] = (Xs[u, mu] + Xs[u, mu].T) / 2
            for a in range(d):
                Ys[u, a] = (Ys[u, a] + Ys[u, a].T) / 2
        Es = [float(np.trace(Xs[u, 0] @ Xs[u, 0])) / N for u in range(M)]
        J_hist.append(float(np.mean(np.array(Es[:-1]) - np.array(Es[1:]))))

    E = [float(np.trace(Xs[u, 0] @ Xs[u, 0])) / N for u in range(M)]
    vhats = [_compute_v_hat(Ys[u], D) for u in range(M)]
    align = np.mean([abs(float(vhats[u] @ vhats[0])) for u in range(M)])
    return E, align, np.mean(J_hist[-100:])


if __name__ == "__main__":
    print("=" * 80)
    print(" TUNED UPWIND TRANSPORT: M=6, N=4, g_drive=5, g_trans=1.2, T=0.02, 400 steps")
    print("=" * 80)
    runs = [("REAL (pump@0)", 5.0, False, [42, 43]),
            ("NULL (no pump)", 0.0, False, [42, 43]),
            ("REV  (pump@5)", 5.0, True, [42])]
    for tag, g_drive, reverse, seeds in runs:
        Eprof, aligns, Js = [], [], []
        for s in seeds:
            E, al, J = run_transport_tuned(M=6, N=4, D=2, d=2, g_xy=0.8, g_trans=1.2,
                                           g_drive=g_drive, g_bulk=0.1, g_sink=3.0, alpha=0.1,
                                           E_max=30.0, lam_g=5.0, dt=0.005, T=0.02,
                                           n_steps=400, seed=s, reverse=reverse)
            Eprof.append(E)
            aligns.append(al)
            Js.append(J)
        Emean = np.mean(Eprof, axis=0)
        if not reverse:
            strictly = all(Emean[u] > Emean[u + 1] for u in range(5))
        else:
            strictly = all(Emean[u] < Emean[u + 1] for u in range(5))
        es = ", ".join(f"{e:.3f}" for e in Emean)
        print(f"  [{tag}] E=[{es}] | strictly_monotonic={strictly} | align={np.mean(aligns):.2f} | J_net={np.mean(Js):+.4f}")
        print(f"          per-seed E0..E5: {[['{:.2f}'.format(v) for v in e] for e in Eprof]}")