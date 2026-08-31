"""
SGOED v15 — Track 2: Matrix-Driven Relational Light-Cone growth law + audit
==========================================================================
Rule (per blueprint): unit k (born after u) links to u iff
   1) |v_hat_u . v_hat_k| > theta_align   (time-direction agreement)
   2) D_space(u,k) <= (c_light * (k-u))^2 ,  D_space = (1/N) Tr((X_u-X_k)^2)

Two legs, audited at M = {250, 500, 1000} (same 6 seeds):

  LEG 1 "as-specified": states from the REAL sequential-growth matrix MC.
        Expectation (to be verified): X_u are near-independent draws ->
        D_space ~ constant -> the cone becomes a horizon artifact -> drift.

  LEG 2 "bounded manifold": growth on a bounded spatial manifold
        (circle d_sp=1, 3-torus d_sp=3); matrices carry the coordinates
        X_u^a = A_a cos(w s_a(u)) + B_a sin(w s_a(u)); birth-time rescaled
        to a FIXED cosmic interval T (causet continuum limit: M only
        refines sampling of the same geometry). Expect d -> 1 + d_sp stable.

Calibration (doubles as the estimator) is REUSED per-M from the scale
study, at the same N, so density/boundary effects cancel on both sides.
"""
import json
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, ".")
from step_causal_set_scale_study import calibration, read_dim
from step_sequential_growth import sequential_growth


def frobenius_dist2(X):
    """X: (M, K, N, N) -> (M,M) mean Frobenius^2 per unit pair, normalized by K*N."""
    M, K, N, _ = X.shape
    Xf = X.reshape(M, K * N * N).astype(np.float64)
    G = Xf @ Xf.T
    n2 = np.einsum("ii->i", G)
    dist2 = (n2[:, None] + n2[None, :] - 2.0 * G) / (K * N)
    return dist2


def leg1_poset(M, seed, c=1.0, theta=0.9, therm=10):
    Xs, Ys = sequential_growth(M, 4, 2, 2, 20.0, therm, seed)
    vhats = []
    for u in range(M):
        v = np.zeros(2)
        v[:2] = [np.trace(Ys[u, 0]).real, np.trace(Ys[u, 1]).real]
        n = np.linalg.norm(v)
        vhats.append(v / (n + 1e-8) if n > 1e-8 else np.zeros(2))
    vhats = np.array(vhats)
    dist2 = frobenius_dist2(Xs)
    R = np.zeros((M, M), dtype=np.int8)
    for u in range(M):
        ks = np.arange(u + 1, M)
        align = np.abs(vhats[u] @ vhats[ks].T) > theta
        cone = dist2[u, ks] <= (c * (ks - u)) ** 2
        R[u, ks] = (align & cone).astype(np.int8)
    return R


def leg2_poset(M, seed, d_sp, c=1.0, T=10.0, L=10.0, sigma=2.0, Nm=5, n_grid=2000,
               walk=True):
    rng = np.random.RandomState(seed)
    if walk:
        dt = T / (n_grid - 1)
        walk_p = np.cumsum(rng.normal(0.0, sigma * np.sqrt(dt), (n_grid, d_sp)), axis=0) % L
        idx = np.round(np.linspace(0, n_grid - 1, M)).astype(int)
        s = walk_p[idx]              # same geometry, denser sampling in M
    else:
        s = rng.uniform(0.0, L, (M, d_sp))   # uniform scatter (sprinkle-like)
    w = 2.0 * np.pi / L
    X = np.zeros((M, d_sp, Nm, Nm))
    for a in range(d_sp):
        A = rng.randn(Nm, Nm) * 0.5
        B = rng.randn(Nm, Nm) * 0.5
        A = (A + A.T) / 2
        B = (B + B.T) / 2
        ca = np.cos(w * s[:, a])
        sa = np.sin(w * s[:, a])
        for u in range(M):
            X[u, a] = ca[u] * A + sa[u] * B
    dist2 = frobenius_dist2(X)
    t = np.linspace(0.0, T, M)
    R = np.zeros((M, M), dtype=np.int8)
    for u in range(M):
        ks = np.arange(u + 1, M)
        cone = dist2[u, ks] <= (c * (t[ks] - t[u])) ** 2
        R[u, ks] = cone.astype(np.int8)
    return R


if __name__ == "__main__":
    Ms = [250, 500, 1000]
    seeds = range(42, 48)
    out = {}

    def audit(tag, maker, Ms_grid):
        print(f"\n{tag}")
        rows = {}
        for M in Ms_grid:
            ds, rhos = calibration(M, seeds=8)
            dims = []
            for s in seeds:
                R = maker(M, s)
                C = int(R.sum())
                rho = C / (M * (M - 1) / 2)
                dims.append(read_dim(rho, ds, rhos))
            m, sd = float(np.mean(dims)), float(np.std(dims))
            rows[str(M)] = {"d_mean": m, "d_std": sd}
            print(f"  M={M:5d}: d_MM = {m:.2f} ± {sd:.2f}")
        std_across = float(np.std([rows[str(M)]["d_mean"] for M in Ms_grid]))
        rows["std_across_N"] = round(std_across, 3)
        out[tag] = rows
        return rows

    # LEG1 uses the cached-v_hat sequential growth (O(1) inter-coupling now;
    # the previous naive recompute was O(u)/proposal -> O(M^2)).
    r1 = audit("LEG1 as-specified (real growth states, theta=0.9)",
               lambda M, s: leg1_poset(M, s), Ms)
    r2a = audit("LEG2 circle (d_sp=1)",
                lambda M, s: leg2_poset(M, s, 1), Ms)
    r2b = audit("LEG2 3-torus (d_sp=3)",
                lambda M, s: leg2_poset(M, s, 3), Ms)

    verdict = [
        f"LEG1 std_across_N = {r1['std_across_N']}",
        f"LEG2 circle std_across_N = {r2a['std_across_N']} (expect ~2 stable)",
        f"LEG2 torus  std_across_N = {r2b['std_across_N']} (expect ~4 stable)",
    ]
    print("\n" + "=" * 60)
    for v in verdict:
        print(v)
    out["verdict"] = verdict
    with open("step_growth_lightcone_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_growth_lightcone_results.json")