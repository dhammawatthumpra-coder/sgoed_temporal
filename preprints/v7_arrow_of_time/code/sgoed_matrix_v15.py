"""
SGOED v15 probe (phase 2) — SSB without v_hat: pseudo-Euclidean signature
==========================================================================
Phase-1 result (no v_hat): any expansion is isotropic (ratio ~1.05);
the only anisotropic state needs the engineered v_hat steering. So the
Kim-Nishimura 4D route is not reachable with the Euclidean action.

This phase tests the physically-motivated alternative: the Lorentzian /
pseudo-Euclidean signature of the commutator term, which is what actually
drives the split in Lorentzian IKKT (Kim-Nishimura-Tsuchiya). With real
matrices both signs of Tr(comm@comm.T) are bounded below, so MC is safe:

  comm weight s(mu,nu):  +1 for time-space pairs  (wants commutation)
                         -1 for space-space pairs (wants non-commutation)

Index 0 = time (T), indices 1..D-1 = space. Driver stays SYMMETRIC over
all directions (no steering). Question: does the thermal ensemble show a
time/space split at D=4, and does SO(D-1) among the spaces survive?
"""
import json
import numpy as np


def comm_weight(mu, nu, mode):
    """Signature of the commutator term (Euclidean: all +1)."""
    if mode == "lorentz" and mu >= 1 and nu >= 1:
        return -1.0
    return 1.0


def action_probe(X, mode, g_drive, max_extent=10.0, lam=1.0, r0=1.0, g_comm=1.0):
    D, N, _ = X.shape
    S = 0.0
    for mu in range(D):
        for nu in range(mu + 1, D):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            S += g_comm * comm_weight(mu, nu, mode) * float(np.trace(comm @ comm.T).real)
        tr2 = float(np.trace(X[mu] @ X[mu]).real)
        S += lam * (tr2 - N * r0 ** 2) ** 2
    if mode in ("sym", "lorentz"):
        for mu in range(D):
            X2 = X[mu] @ X[mu]
            ext = float(np.trace(X2).real) / N
            if ext < max_extent:
                S -= g_drive * float(np.trace(X2 @ X2).real)
            else:
                S += 10.0 * (ext - max_extent) ** 2
    return S


def run(D=4, N=6, mode="lorentz", g_drive=0.8, seed=42, n_therm=60, n_meas=20,
        eps=0.25, g_comm=1.0):
    rng = np.random.RandomState(seed)
    X = np.zeros((D, N, N))
    for mu in range(D):
        A = rng.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    S = action_probe(X, mode, g_drive, g_comm=g_comm)

    def sweep():
        nonlocal S
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    old = X[mu, i, j]
                    X[mu, i, j] = old + eps * rng.randn()
                    if i != j:
                        X[mu, j, i] = X[mu, i, j]
                    S2 = action_probe(X, mode, g_drive, g_comm=g_comm)
                    dS = S2 - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = S2
                    else:
                        X[mu, i, j] = old
                        if i != j:
                            X[mu, j, i] = old

    exts = []
    winners = []
    for t in range(n_therm + n_meas):
        sweep()
        if t >= n_therm:
            e = np.array([float(np.trace(X[mu] @ X[mu]).real) / N for mu in range(D)])
            exts.append(e)
            winners.append(int(np.argmax(e)))
    E = np.mean(np.array(exts), axis=0)
    k = int(np.argmax(E))
    ratio = float(E[k] / (np.mean(np.delete(E, k)) + 1e-8))
    m = np.unique(winners, return_counts=True)
    winner_mode = int(m[0][np.argmax(m[1])])
    return E, ratio, winner_mode


def batch(tag, mode, D, N, g_drive=0.8, seeds=range(42, 52)):
    ratios, exts_all, wmodes = [], [], []
    for s in seeds:
        E, ratio, wm = run(D=D, N=N, mode=mode, g_drive=g_drive, seed=s)
        ratios.append(ratio)
        exts_all.append(E)
        wmodes.append(wm)
    Emean = np.mean(exts_all, axis=0)
    iso_space = float(np.std(Emean[1:]) / (np.mean(Emean[1:]) + 1e-8))
    win_counts = {i: wmodes.count(i) for i in sorted(set(wmodes))}
    print(f"[{tag:18s}] ext={np.round(Emean, 3)} ratio={np.mean(ratios):.2f}±{np.std(ratios):.2f} "
          f"iso_space={iso_space:.3f} winner={win_counts}")
    return {"tag": tag, "ext": Emean.tolist(), "ratio_mean": float(np.mean(ratios)),
            "ratio_std": float(np.std(ratios)), "iso_space": iso_space,
            "winner_hist": win_counts}


if __name__ == "__main__":
    out = {}
    for label, mode, D in [
        ("eucl    D=4 (control)", "sym", 4),
        ("lorentz D=4 (1+3)", "lorentz", 4),
        ("eucl    D=10 (control)", "sym", 10),
        ("lorentz D=10 (1+9)", "lorentz", 10),
    ]:
        out[label] = batch(label, mode, D, N=6)
    with open("sgoed_matrix_v15_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> sgoed_matrix_v15_results.json")