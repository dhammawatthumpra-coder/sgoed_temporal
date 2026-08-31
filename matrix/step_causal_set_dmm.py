"""
SGOED v15 — Track 2: Causal Set + Myrheim-Meyer dimension from Sequential Growth
===============================================================================
1) Calibrate the relation-fraction estimator on KNOWN posets:
   chain (d=1), Poisson Minkowski sprinklings (d=2,3,4) in a [0,10]^d box
   (relation: dt > ||dx||_2; no threshold needed -> avoids the old v9/v10
   threshold-artifact trap).
2) Build the poset of the REAL sequential-growth output
   (birth order u<k, relation iff |v_hat_u . v_hat_k| > 0.9).
   Prediction: inheritance = 1.000 => total order (chain) => d ~= 1.
3) Poisson-branching preview (the review's step 1): Bern(p) links +
   transitive closure -> d(p). Does branching lift the dimension?
"""
import json
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, "../code")
from step_sequential_growth import sequential_growth
from sgoed_core_v7 import _compute_v_hat


def chain_poset(N):
    R = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        R[i, i + 1:] = 1
    return R


def sprinkle_poset(seed, N, dim, T=10.0, L=10.0):
    rng = np.random.RandomState(seed)
    pts = rng.uniform(0.0, 1.0, (N, dim))
    pts[:, 0] *= T
    pts[:, 1:] *= L
    R = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        dt = pts[i + 1:, 0] - pts[i, 0]
        if dim == 2:
            dsp = np.abs(pts[i + 1:, 1] - pts[i, 1])
        else:
            dsp = np.sqrt(((pts[i + 1:, 1:] - pts[i, 1:]) ** 2).sum(axis=1))
        R[i, i + 1:] = (dt > dsp).astype(np.int8)
    return R


def bern_closure_poset(seed, N, p):
    rng = np.random.RandomState(seed)
    R = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        R[i, i + 1:] = (rng.rand(N - i - 1) < p).astype(np.int8)
    # transitive closure by boolean squaring with UNION (R <- R or R^2).
    # Pure squaring without the union step shrinks and collapses to 0.
    Rc = R.copy()
    while True:
        R2 = (Rc.astype(np.int64) @ Rc) > 0
        Rnew = np.clip(Rc + R2.astype(np.int8), 0, 1).astype(np.int8)
        np.fill_diagonal(Rnew, 0)
        if (Rnew == Rc).all():
            break
        Rc = Rnew
    return Rc


def poset_metrics(R, N):
    R64 = R.astype(np.int64)
    C = int(R64.sum())
    I = int((R64 @ R64).sum())
    rho = C / (N * (N - 1) / 2)
    i3 = I / (N * (N - 1) * (N - 2) / 6)
    return rho, i3


def growth_poset(seed, M, g_inter=20.0, therm=100, theta=0.9):
    Xs, Ys = sequential_growth(M, 4, 2, 2, g_inter, therm, seed)
    vhats = [_compute_v_hat(Ys[u], 2) for u in range(M)]
    R = np.zeros((M, M), dtype=np.int8)
    for u in range(M):
        for k in range(u + 1, M):
            if abs(float(vhats[u] @ vhats[k])) > theta:
                R[u, k] = 1
    return R


if __name__ == "__main__":
    N = 250
    # ---- 1) calibration on known posets ----
    cal_rho, cal_i3, cal_d = [1.0], [1.0], [1.0]   # chain = d=1 anchor
    for d in [2, 3, 4, 5, 6]:
        rhos, i3s = [], []
        for s in range(42, 47):
            R = sprinkle_poset(s, N, d)
            rho, i3 = poset_metrics(R, N)
            rhos.append(rho)
            i3s.append(i3)
        cal_rho.append(float(np.mean(rhos)))
        cal_i3.append(float(np.mean(i3s)))
        cal_d.append(d)
        print(f"  cal d={d}: rho={np.mean(rhos):.4f}±{np.std(rhos):.4f} i3={np.mean(i3s):.4f}")
    cal_rho = np.array(cal_rho)
    cal_d = np.array(cal_d)

    def read_dim(rho):
        if rho >= cal_rho[0]:
            return 1.0
        if rho <= cal_rho[-1]:
            return float(cal_d[-1])   # below calibration floor -> d >= 6
        idx = np.searchsorted(-cal_rho, -rho)
        d_lo, d_hi = cal_d[idx - 1], cal_d[idx]
        r_lo, r_hi = cal_rho[idx - 1], cal_rho[idx]
        return float(d_lo + (rho - r_lo) / (r_hi - r_lo) * (d_hi - d_lo))

    out = {"calibration": {"d": cal_d.tolist(), "rho": cal_rho.tolist(),
                           "i3": cal_i3}}

    # ---- 2) real sequential-growth poset ----
    print("\nSEQUENTIAL GROWTH poset (relation: |v.u . v.k| > 0.9):")
    for M in [8, 16]:
        dims = []
        for s in range(42, 48):
            R = growth_poset(s, M)
            rho, i3 = poset_metrics(R, M)
            dims.append(read_dim(rho))
        print(f"  M={M}: d_MM = {np.mean(dims):.2f} ± {np.std(dims):.2f}")
        out[f"growth_M{M}"] = {"d_MM_mean": float(np.mean(dims)), "d_MM_std": float(np.std(dims))}

    # ---- 3) Poisson branching preview ----
    print("\nPOISSON BRANCHING (Bern(p) + transitive closure), N=250:")
    branch = {}
    for p in [0.02, 0.05, 0.1, 0.2, 0.4, 0.7]:
        dims = []
        for s in range(42, 45):
            R = bern_closure_poset(s, N, p)
            rho, i3 = poset_metrics(R, N)
            dims.append(read_dim(rho))
        print(f"  p={p:.2f}: d_MM = {np.mean(dims):.2f} ± {np.std(dims):.2f}")
        branch[str(p)] = {"d_MM_mean": float(np.mean(dims)), "d_MM_std": float(np.std(dims))}
    out["poisson_branching"] = branch

    with open("step_causal_set_dmm_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_causal_set_dmm_results.json")