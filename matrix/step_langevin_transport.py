"""
Extent-transport v2 — UPWIND (directed advection) per review:
F_0      = +g_drive X0 - g_trans X0
F_u      = +g_trans X_{u-1} - g_trans X_u        (prev -> self -> next, no pull-back)
F_{M-1}  = +g_trans X_{M-2} - g_sink X_{M-1}
Params: g_drive=3.0, g_trans=1.5, g_bulk=0.2, g_sink=2.0, T=0.1 (low noise floor)
Coupling normalized (bounded) + global capacity gate + sparsity.
"""
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, r"F:\_Ai\sgoed\sgoed\code")
from sgoed_core_v7 import _compute_v_hat


def run_transport(M, N, D, d, g_xy, g_trans, g_drive, g_bulk, g_sink, alpha,
                  E_max, lam_g, dt, T, n_steps, seed, reverse=False):
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
    return E, align, np.mean(J_hist[-50:])


if __name__ == "__main__":
    print("=" * 80)
    print(" UPWIND TRANSPORT (review v2): M=6, N=4, g_drive=3, g_trans=1.5")
    print("  g_bulk=0.2, g_sink=2.0, T=0.1, 150 steps, seeds 42/43")
    print("=" * 80)
    for tag, g_drive, reverse, seeds in [("REAL  (pump@0)", 3.0, False, [42, 43]),
                                         ("NULL  (no pump)", 0.0, False, [42, 43]),
                                         ("REV   (pump@5)", 3.0, True, [42])]:
        Eprof, aligns, Js = [], [], []
        for s in seeds:
            E, al, J = run_transport(6, 4, 2, 2, 0.8, 1.5, g_drive, 0.2, 2.0, 0.5,
                                     30.0, 5.0, 0.005, 0.1, 150, s, reverse)
            Eprof.append(E)
            aligns.append(al)
            Js.append(J)
        Emean = np.mean(Eprof, axis=0)
        dec = all(Emean[u] > Emean[u + 1] - 0.15 for u in range(5))
        es = ", ".join(f"{e:.2f}" for e in Emean)
        print(f"  [{tag}] E=[{es}] | strictly-dec={dec} | align={np.mean(aligns):.2f} | J_net={np.mean(Js):+.3f}")