"""
SGOED v14 — Matrix Ecosystem (Atom-Molecule Hybrid)
===================================================
M "atom" units, each a v7-core matrix (X_u, Y_u) with real condensation.
"Molecule" = inter-unit alignment coupling on the actual eigen-directions:
    S_inter = -g_inter * sum_{u<v} c_uv * E_u * E_v
    c_uv = Tr(X_u X_v) / (|X_u| |X_v|)   (normalized overlap of unit directions)
    E_u  = Tr(X_u^2) / N                 (unit extent = "age" proxy)
Design: coupling acts on REAL matrix directions (not node degree), so units
should align into a coherent "molecule" — and E_u provides an order axis.
"""
import numpy as np
import sys
sys.path.insert(0, r"F:\_Ai\sgoed\sgoed\code")
from sgoed_core_v7 import action_v7, _compute_v_hat


def action_v14(Xs, Ys, g_inter, g_xy=0.8, g_yx=0.0, g_repel=0.0, max_extent=10.0):
    """Xs: (M, D, N, N), Ys: (M, d, N, N).
    Inter coupling = ALIGN observer directions (v_hat) + REPEL extents (push, not pull):
        S_inter = -g_inter * sum_{u<v} (v_hat_u . v_hat_v)
                  + g_repel * sum_{u<v} (E_u - E_v)^2 / Ebar^2
    Align synchronizes clocks; repel spreads ages (order axis), bounded by gate.
    """
    M = Xs.shape[0]
    D = Xs.shape[1]
    N = Xs.shape[2]
    S = 0.0
    vhats = []
    exts = []
    for u in range(M):
        S += action_v7(Xs[u], Ys[u], g_xy, g_yx, max_extent=max_extent)
        vhats.append(_compute_v_hat(Ys[u], D))
        exts.append(float(np.trace(Xs[u, 0] @ Xs[u, 0])) / N)
    if g_inter > 0.0 or g_repel > 0.0:
        Ebar = float(np.mean(exts)) + 1e-8
        for u in range(M):
            for v in range(u + 1, M):
                if g_inter > 0.0:
                    S -= g_inter * float(vhats[u] @ vhats[v])
                if g_repel > 0.0:
                    S += g_repel * (exts[u] - exts[v]) ** 2 / Ebar ** 2
    return S


def run_v14(M=8, N=4, D=2, d=2, g_xy=0.8, g_yx=0.0, g_inter=0.1, g_repel=0.0,
            n_therm=80, n_measure=20, step=0.15, seed=42):
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
    S = action_v14(Xs, Ys, g_inter, g_xy, g_yx, g_repel)

    def sweep(therm):
        nonlocal S
        for u in range(M):
            for mu in range(D):
                for i in range(N):
                    for j in range(i, N):
                        old = Xs[u, mu, i, j]
                        Xs[u, mu, i, j] = old + step * rng.randn()
                        if i != j:
                            Xs[u, mu, j, i] = Xs[u, mu, i, j]
                        S2 = action_v14(Xs, Ys, g_inter, g_xy, g_yx, g_repel)
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
                        Ys[u, a, i, j] = old + step * rng.randn()
                        if i != j:
                            Ys[u, a, j, i] = Ys[u, a, i, j]
                        S2 = action_v14(Xs, Ys, g_inter, g_xy, g_yx, g_repel)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Ys[u, a, i, j] = old
                            if i != j:
                                Ys[u, a, j, i] = old

    for _ in range(n_therm):
        sweep(True)
    for _ in range(n_measure):
        sweep(False)
    return Xs, Ys


def unit_observables(Xs, Ys, g_xy=0.8, max_extent=10.0):
    """Per-unit condensation + inter-unit alignment."""
    M, D, N, _ = Xs.shape
    # per-unit: extent of X[0], spectral ratio, v_hat from Y
    exts = []
    specs = []
    vhats = []
    for u in range(M):
        A = Xs[u, 0]
        exts.append(float(np.trace(A @ A)) / N)
        ev = np.linalg.eigvalsh(A)
        specs.append(abs(ev[-1]) / (abs(ev[-2]) + 1e-8))
        vhats.append(_compute_v_hat(Ys[u], D))
    # inter-unit alignment: mean c_uv (normalized Tr overlap of X[0])
    cs = []
    for u in range(M):
        for v in range(u + 1, M):
            Au, Av = Xs[u, 0], Xs[v, 0]
            c = float(np.trace(Au @ Av)) / (np.linalg.norm(Au) * np.linalg.norm(Av) + 1e-8)
            cs.append(c)
    A_align = float(np.mean(cs))
    return np.array(exts), np.array(specs), np.array(vhats), A_align, np.array(cs)


if __name__ == "__main__":
    # quick self-test: g_inter=0 -> units independent
    Xs, Ys = run_v14(M=4, N=4, g_inter=0.0, n_therm=30, n_measure=10, seed=1)
    exts, specs, vhats, A, cs = unit_observables(Xs, Ys)
    print(f"[v14] g_inter=0: alignment A = {A:+.3f} (expect ~0) | "
          f"spec mean = {specs.mean():.2f} | exts = {[f'{e:.2f}' for e in exts]}")
