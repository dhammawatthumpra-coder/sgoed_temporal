"""
SGOED — R-regime significance scan (commutator-compatibility growth)
====================================================================
Confirm the "real growth states -> stable d ~ 3.5" result with more seeds
and an alignment-threshold sweep. States are generated ONCE per (N, seed)
and reused across (f, theta) — the cone/closure step is cheap.

Grid:
  N       250 / 500 / 1000
  seeds   8 at N<=500, 5 at N=1000 (state-gen cost grows fast in M)
  f x theta  0.5 x {0.7,0.8,0.9} , 1.0 x {0.7,0.8,0.9}
  therm   35 (inheritance >= ~0.9 keeps the alignment cascade meaningful)
Gate 1: std_across_N <= 0.05 PASS / > 0.10 FAIL (for each f x theta).
Also report the alignment-passing pair fraction (mechanism support).
"""
import json
import sys
import numpy as np
sys.path.insert(0, ".")
sys.path.insert(0, ".")
from step_causal_set_scale_study import calibration, read_dim
from step_sequential_growth import sequential_growth
from step_growth_commutator import dcomp_growth
from sgoed_core_v7 import _compute_v_hat

Ns = [250, 500, 1000]
SEEDS = {250: range(42, 50), 500: range(42, 50), 1000: range(42, 47)}
THETA = [0.7, 0.8, 0.9]


def cone_rho(N, Dc, V, c, theta):
    """Relation fraction after cone + alignment + transitive closure."""
    t = np.linspace(0.0, 10.0, N)
    dt = t[:, None] - t[None, :]
    children = [[] for _ in range(N)]
    for k in range(1, N):
        hit = Dc[:k, k] <= (c * dt[:k, k]) ** 2
        hit = hit & (np.abs(V[:k] @ V[k]) > theta)
        for u in np.nonzero(hit)[0]:
            children[k].append(int(u))
    reach = [1 << i for i in range(N)]
    C = 0
    for i in range(N - 1, -1, -1):
        for j in children[i]:
            reach[i] |= reach[j]
        C += (reach[i] & ~(1 << i)).bit_count()
    return C / (N * (N - 1) / 2)


if __name__ == "__main__":
    out = {}
    # ---- generate states once per (N, seed) ----
    states = {}
    align_frac = {}
    for N in Ns:
        for s in SEEDS[N]:
            Xs, Ys = sequential_growth(N, 4, 2, 2, 20.0, 35, s)
            Dc = dcomp_growth(Xs)
            V = np.array([_compute_v_hat(Ys[u], 2) for u in range(N)])
            states[(N, s)] = (Dc, V)
            align_frac[(N, s)] = float(np.mean(np.abs(np.einsum("ij,ij->i", V[1:], V[:-1])) > 0.9))
        print(f"states ready for N={N} ({len(SEEDS[N])} seeds)", flush=True)
    print("mean adjacent alignment (theta>0.9): " +
          ", ".join(f"N={N}:{np.mean([align_frac[(N, s)] for s in SEEDS[N]]):.3f}" for N in Ns))

    c_ref = 0.7043   # from the original run (N=250 states, same generator)
    for f in (0.5, 1.0):
        for th in THETA:
            rows = {}
            for N in Ns:
                ds, rhos = calibration(N, seeds=8)
                dims = []
                for s in SEEDS[N]:
                    Dc, V = states[(N, s)]
                    rho = cone_rho(N, Dc, V, f * c_ref, th)
                    dims.append(read_dim(rho, ds, rhos))
                rows[str(N)] = [float(np.mean(dims)), float(np.std(dims))]
            means = [rows[str(N)][0] for N in Ns]
            std_acr = float(np.std(means))
            verdict = "PASS" if std_acr <= 0.05 else ("FAIL" if std_acr > 0.10 else "BORDER")
            print(f"[f={f} th={th}] d={means[0]:.2f}/{means[1]:.2f}/{means[2]:.2f} "
                  f"std_acr={std_acr:.3f} -> {verdict}", flush=True)
            out[f"f{f}_th{th}"] = {"d": {str(N): rows[str(N)] for N in Ns},
                                   "std_across_N": std_acr, "verdict": verdict}
    with open("step_growth_commutator_scan_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_growth_commutator_scan_results.json")