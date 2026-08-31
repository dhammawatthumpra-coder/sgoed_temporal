"""
SGOED v15 — dynamical probe: real-time evolution in T (Kim-Nishimura style)
===========================================================================
Phase-2 equilibrium showed: with the pseudo-Euclidean signature the time
matrix SHRINKS (it is minimized away) — the real-time version of the
Lorentzian IKKT treats T as an advancing CLOCK, not a minimized variable.

Here: T = tau(t) * R (R fixed random symmetric matrix, tau grows as a
monotonic scheduler). At each tau the SPACE matrices relax (MC) at fixed T.
Signs:
  eucl        : all comm terms + (control — clock should do nothing)
  lorentz ts+ : space-space -1, time-space +1  (Kim-Nishimura sign)
  lorentz ts- : space-space -1, time-space -1  (T feeds space expansion)
  eng3        : same as ts+ but driver weights 1.0 on 3 spaces, 0.1 on 6
                (detectability control: can we SEE a 3-of-9 split at all?)

Question: does any sign yield a "3 expanding + 6 not" pattern as tau grows?
Exploratory probe: n_seeds=6, n_eq=10 (significance needs a full run later).
"""
import json
import numpy as np


def fixed_time_matrix(N, seed):
    rng = np.random.RandomState(seed + 1000)
    A = rng.randn(N, N) * 0.5
    return (A + A.T) / 2


def action_dyn(X, T, mode, sign_ts, g_drive, w, max_extent=10.0, lam=1.0, r0=1.0):
    """X: (Dm, N, N) space matrices (index 0..Dm-1). T: fixed time matrix."""
    Dm, N, _ = X.shape
    S = 0.0
    for mu in range(Dm):
        # time-space              (+sign_ts)   and space-space pairs:
        for nu in range(mu + 1, Dm):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            s = -1.0 if (mode in ("lorentz", "eng3")) else 1.0
            S += s * float(np.trace(comm @ comm.T).real)
        comm_t = X[mu] @ T - T @ X[mu]
        S += sign_ts * float(np.trace(comm_t @ comm_t.T).real)
        tr2 = float(np.trace(X[mu] @ X[mu]).real)
        S += lam * (tr2 - N * r0 ** 2) ** 2
        if mode in ("sym", "lorentz", "eng3"):
            X2 = X[mu] @ X[mu]
            ext = float(np.trace(X2).real) / N
            if ext < max_extent:
                S -= g_drive * w[mu] * float(np.trace(X2 @ X2).real)
            else:
                S += 100.0 * (ext - max_extent) ** 2
    return S


def run_dyn(D, N, mode, sign_ts=+1.0, g_drive=0.8, seed=42, n_steps=16,
            n_eq=25, eps=0.25, tau_max=1.5, w=None):
    Dm = D - 1
    rng = np.random.RandomState(seed)
    X = np.zeros((Dm, N, N))
    for mu in range(Dm):
        A = rng.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    if w is None:
        w = np.ones(Dm)
    R = fixed_time_matrix(N, seed)
    taus = np.linspace(0.3, tau_max, n_steps)
    radii = []
    for tau in taus:
        T = tau * R
        S = action_dyn(X, T, mode, sign_ts, g_drive, w)
        for _ in range(n_eq):
            for mu in range(Dm):
                for i in range(N):
                    for j in range(i, N):
                        old = X[mu, i, j]
                        X[mu, i, j] = old + eps * rng.randn()
                        if i != j:
                            X[mu, j, i] = X[mu, i, j]
                        S2 = action_dyn(X, T, mode, sign_ts, g_drive, w)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            X[mu, i, j] = old
                            if i != j:
                                X[mu, j, i] = old
        radii.append([float(np.trace(X[mu] @ X[mu]).real) / N for mu in range(Dm)])
    return np.array(radii), taus


def summarize(radii):
    """radii: (n_steps, Dm) -> sorted final radii + 3-of-9 gap + convergence drift."""
    r_final = np.sort(radii[-1])[::-1]
    n = len(r_final)
    top_k = max(1, n // 3)
    gap3 = float(np.mean(r_final[:top_k]) / (np.mean(r_final[top_k:]) + 1e-8))
    iso_all = float(np.std(r_final) / (np.mean(r_final) + 1e-8))
    drift = float(np.abs(np.mean(radii[-1]) - np.mean(radii[-2])) /
                  (np.mean(radii[-1]) + 1e-8))
    return r_final, gap3, iso_all, drift


if __name__ == "__main__":
    out = {}
    configs = [
        ("t10 eucl  (control)", 10, "sym", +1.0, None),
        ("t10 lorentz ts+ (KN)", 10, "lorentz", +1.0, None),
        ("t10 eng3  (detect-cntl)", 10, "eng3", +1.0,
         np.array([1.0, 1.0, 1.0, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02])),
    ]
    for tag, D, mode, sign_ts, w in configs:
        g3s, isos, finals, drifts = [], [], [], []
        for s in range(42, 48):  # 6 seeds — exploratory
            radii, _ = run_dyn(D=D, N=6, mode=mode, sign_ts=sign_ts, g_drive=0.8, seed=s, w=w)
            rf, g3, iso, dr = summarize(radii)
            g3s.append(g3)
            isos.append(iso)
            finals.append(rf)
            drifts.append(dr)
        rfinal = np.mean(finals, axis=0)
        print(f"[{tag:23s}] final sorted={np.round(rfinal, 2)} "
              f"top3-gap={np.mean(g3s):.2f}±{np.std(g3s):.2f} "
              f"iso_all={np.mean(isos):.3f} drift={np.mean(drifts):.3f}")
        out[tag] = {"final_sorted": rfinal.tolist(), "top3_gap_mean": float(np.mean(g3s)),
                    "top3_gap_std": float(np.std(g3s)), "iso_all": float(np.mean(isos)),
                    "drift": float(np.mean(drifts))}
    with open(r"F:\_Ai\sgoed\V5\matrix\sgoed_matrix_v15_dyn_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> sgoed_matrix_v15_dyn_results.json")