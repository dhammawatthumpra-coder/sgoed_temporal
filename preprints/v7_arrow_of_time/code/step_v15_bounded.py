"""
SGOED v15 — final route-(ก) probe: bounded (saturating) noncommutativity
========================================================================
Phase-3 dynamical probe blew up: the Lorentzian space-space term
-||comm||^2 is unbounded below, so the bosonic toy has no stationary
state (the real registry in Lorentzian IKKT is the fermion determinant,
which we don't have). Here: bounded saturating per-pair reward

    S_comm = -g * x / (1 + x),   x = ||comm_ij||^2 / (N^3 s0^2)

so the model is bounded ALWAYS (each pair contributes in [-g, 0]).
Question: in a stationary state, does any subset k-of-9 separate
spontaneously (top3-gap >> 1, reproducible, thermalized)?

Configs:
  bsat sym   : symmetric reward on all pairs           -> symmetric?
  bsat w3/9  : pair reward weighted w_i*w_j, 3 dims full, 6 dims x0.05
               (detectability control: can the pair metric SEE a 3-6 split
                in a bounded regime?)
  bsat + T   : fixed time matrix tau*R, ts+ saturating penalty
               (does a time axis induce k-selection?)
"""
import json
import numpy as np


def action_bsat(X, g, s0, g_drive, w, T=None, g_ts=1.0, tau=0.7,
                max_extent=10.0, lam=1.0, r0=1.0):
    Dm, N, _ = X.shape
    denom = N ** 3 * s0 ** 2
    S = 0.0
    for mu in range(Dm):
        tr2 = float(np.trace(X[mu] @ X[mu]).real)
        S += lam * (tr2 - N * r0 ** 2) ** 2
        if g_drive > 0:
            X2 = X[mu] @ X[mu]
            ext = float(np.trace(X2).real) / N
            if ext < max_extent:
                S -= g_drive * w[mu] * float(np.trace(X2 @ X2).real)
            else:
                S += 100.0 * (ext - max_extent) ** 2
    for mu in range(Dm):
        for nu in range(mu + 1, Dm):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            x = float(np.trace(comm @ comm.T).real) / denom
            S -= g * w[mu] * w[nu] * x / (1.0 + x)
    if T is not None:
        for mu in range(Dm):
            comm_t = X[mu] @ T - T @ X[mu]
            y = float(np.trace(comm_t @ comm_t.T).real) / denom
            S += g_ts * y / (1.0 + y)   # ts+ (Kim sign): time wants commuting
    return S


def run_bounded(D=10, N=6, g=1.0, s0=0.5, g_drive=0.25, seed=42,
                n_therm=60, n_meas=20, eps=0.25, w=None, T=None):
    Dm = D - 1
    rng = np.random.RandomState(seed)
    X = np.zeros((Dm, N, N))
    for mu in range(Dm):
        A = rng.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    if w is None:
        w = np.ones(Dm)
    S = action_bsat(X, g, s0, g_drive, w, T=T)

    def sweep():
        nonlocal S
        for mu in range(Dm):
            for i in range(N):
                for j in range(i, N):
                    old = X[mu, i, j]
                    X[mu, i, j] = old + eps * rng.randn()
                    if i != j:
                        X[mu, j, i] = X[mu, i, j]
                    S2 = action_bsat(X, g, s0, g_drive, w, T=T)
                    dS = S2 - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = S2
                    else:
                        X[mu, i, j] = old
                        if i != j:
                            X[mu, j, i] = old

    exts = []
    for t in range(n_therm + n_meas):
        sweep()
        if t >= n_therm:
            exts.append([float(np.trace(X[mu] @ X[mu]).real) / N for mu in range(Dm)])
    E = np.mean(np.array(exts), axis=0)
    return E, sat_level(X, s0)


def sat_level(X, s0):
    """Mean saturation x/(1+x) of the pair rewards (0=off, 1=saturated)."""
    Dm, N, _ = X.shape
    denom = N ** 3 * s0 ** 2
    xs = []
    for mu in range(Dm):
        for nu in range(mu + 1, Dm):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            xs.append(float(np.trace(comm @ comm.T).real) / denom)
    return float(np.mean(np.array(xs) / (1.0 + np.array(xs))))


if __name__ == "__main__":
    out = {}
    configs = [
        ("bsat sym", None, None),
        ("bsat w3/9 (detect)",
         np.array([1.0, 1.0, 1.0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]), None),
        ("bsat + T (ts+)", None, "time"),
    ]
    for tag, w, tmode in configs:
        g3s, isos, finals, sats = [], [], [], []
        for s in range(42, 48):  # 6 seeds — exploratory
            Tmat = None
            if tmode == "time":
                rngz = np.random.RandomState(s + 1000)
                A = rngz.randn(6, 6) * 0.5
                Tmat = 0.7 * (A + A.T) / 2
            E, sbar = run_bounded(seed=s, w=w, T=Tmat)
            rf = np.sort(E)[::-1]
            n = len(rf)
            k = n // 3
            g3s.append(float(np.mean(rf[:k]) / (np.mean(rf[k:]) + 1e-8)))
            isos.append(float(np.std(rf) / (np.mean(rf) + 1e-8)))
            finals.append(rf)
            sats.append(sbar)
        rfinal = np.mean(finals, axis=0)
        print(f"[{tag:18s}] sorted={np.round(rfinal, 3)} "
              f"top3-gap={np.mean(g3s):.2f}±{np.std(g3s):.2f} "
              f"iso_all={np.mean(isos):.3f} sat={np.mean(sats):.2f}")
        out[tag] = {"sorted": rfinal.tolist(), "top3_gap_mean": float(np.mean(g3s)),
                    "top3_gap_std": float(np.std(g3s)), "iso_all": float(np.mean(isos)),
                    "sat_mean": float(np.mean(sats))}
    with open(r"F:\_Ai\sgoed\V5\matrix\sgoed_matrix_v15_bnd_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> sgoed_matrix_v15_bnd_results.json")