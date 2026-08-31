"""
Benincasa-Dowker style chain-count dimension (directed, threshold-free).
=======================================================================
Idea: from a causal matrix C (i precedes j), count k-chains
      C2 = #2-chains, C3 = #3-chains, C4 = #4-chains (weighted).
      Ratio r = C4*C2/C3^2 is density-invariant and a function of the
      causal-set dimension d (Benincasa & Dowker 2010).
1. Calibrate r(d) numerically via Poisson sprinklings in d-dim Minkowski (d=1..6).
2. Apply to the v10 hypergraph (real causal matrix from triads) + null test.
"""
import json
import numpy as np
from numba import njit
from sgoed_hypergraph_core_v10 import run_v10


# ---------- causal matrix from hypergraph (weighted pairwise flow) ----------
@njit(fastmath=True)
def build_causal_matrix(T):
    """C[i,j] = total forward triad flow i -> j (sum over k of T[i,k,j]+T[i,j,k])."""
    N = T.shape[0]
    C = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            s = 0.0
            for k in range(N):
                if k != i and k != j:
                    s += T[i, k, j] + T[i, j, k]
            C[i, j] = s
    return C


def chain_counts(C):
    """Weighted chain counts C2, C3, C4 via matrix powers (distinct nodes auto)."""
    N = C.shape[0]
    C2 = C.sum()
    P2 = C @ C
    C3 = P2.sum()
    P3 = P2 @ C
    C4 = P3.sum()
    return float(C2), float(C3), float(C4)


def bd_ratio(C):
    C2, C3, C4 = chain_counts(C)
    if C3 <= 0:
        return np.nan
    return C4 * C2 / C3 ** 2


# ---------- calibration: sprinklings in d-dim Minkowski ----------
def sprinkle_causal(N, d, rng, T_span=10.0):
    """Uniform sprinkle in d-dim: t in [0,T], x_i in [-T/2,T/2]. Returns causal matrix."""
    t = rng.uniform(0, T_span, N)
    if d > 1:
        x = rng.uniform(-T_span / 2, T_span / 2, (N, d - 1))
        C = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                dt = t[j] - t[i]
                dx = x[j] - x[i]
                if dt > 0.0 and dt > np.sqrt(dx @ dx):
                    C[i, j] = 1.0
    else:
        C = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                if t[j] > t[i]:
                    C[i, j] = 1.0
    return C


def calibrate(d_vals=(1, 2, 3, 4, 5, 6), N=200, reps=8, seed0=100):
    rng = np.random.default_rng(seed0)
    curve = {}
    for d in d_vals:
        rs = []
        for rep in range(reps):
            C = sprinkle_causal(N, d, rng)
            rs.append(bd_ratio(C))
        curve[d] = float(np.mean(rs))
        print(f"  calibration d={d}: r = C4*C2/C3^2 = {curve[d]:.4f}")
    return curve


# ---------- main ----------
print("=" * 74)
print(" 1. CALIBRATION: r(d) from Poisson sprinklings (N=200, 8 reps)")
print("=" * 74)
curve = calibrate()

print()
print("=" * 74)
print(" 2. HYPERGRAPH: real causal matrix vs null (shuffled directions)")
print("=" * 74)
seeds = [42, 43, 44, 45, 46]
results = {}
for N in [12, 16, 24, 32]:
    r_vals, null_vals = [], []
    for s in seeds:
        r_h, r_std, align, dmm_old, l_max, obs_ext, T = run_v10(
            N=N, d=3, g_xy=0.8, g_yx=0.0, n_therm=60, n_measure=40, seed=s
        )
        C = build_causal_matrix(T)
        r_real = bd_ratio(C)
        r_vals.append(r_real)
        # null: shuffle T directions? better: randomize C by replacing with
        # random transitive-free directed graph of same density (Erdos-Renyi DAG)
        rng = np.random.default_rng(s)
        dens = float((C > 0).sum()) / (N * (N - 1))
        Cd = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i != j and rng.uniform() < dens:
                    Cd[i, j] = 1.0
        null_vals.append(bd_ratio(Cd))
    results[f"N_{N}"] = {
        "N": N,
        "r_chain_real": float(np.mean(r_vals)),
        "r_chain_null": float(np.mean(null_vals)),
        "r_std_real": float(np.std(r_vals)),
    }
    print(
        f"  N={N:2d} | r_real = {np.mean(r_vals):.4f} +/- {np.std(r_vals):.4f} | "
        f"r_null(ErdosRenyi-DAG) = {np.mean(null_vals):.4f}"
    )

# map r_real to d via calibration (nearest)
ds_real, ds_null = [], []
for N in [12, 16, 24, 32]:
    r = results[f"N_{N}"]["r_chain_real"]
    rn = results[f"N_{N}"]["r_chain_null"]
    d_est = min(curve, key=lambda dd: abs(curve[dd] - r))
    d_est_n = min(curve, key=lambda dd: abs(curve[dd] - rn))
    ds_real.append(d_est)
    ds_null.append(d_est_n)
    results[f"N_{N}"]["d_BD_est"] = int(d_est)
    print(f"  -> N={N}: d_BD(real) ~ {d_est}D | d_BD(null) ~ {d_est_n}D")

out_file = "audit_bd_dimension_results.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({"calibration": curve, "hypergraph": results}, f, indent=2)
print(f"\n[Done] Saved to: {out_file}")
