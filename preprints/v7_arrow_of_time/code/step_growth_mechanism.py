"""
SGOED handoff TODO #2 — Sequential growth: WHY is inheritance 1.000?
====================================================================
Mechanism hypothesis: the inter-coupling is S = -g (v_u . SUM_{j<u} v_j)
(prefix-sum), so each newborn aligns to the MEAN direction of all past
units -> the mean becomes a contraction fixed point -> chain inheritance
and origin alignment both -> 1, deterministically, at any M.

Quantities (S seeds x M units, D=2 unit vectors):
  - origin alignment   mean_u |v_u . v_0|
  - chain inheritance  mean_u |v_u . v_{u-1}|
  - contraction        mean over u>=M/2 of |v_u - mean(v_0..v_{u-1})|
  - |v_u . v_0| trend  mean over the last 8 units (approaches 1?)
  - inter-seed determinism: mean |v_u(seed0) - v_u(seed1)|
"""
import json
import sys
import numpy as np
sys.path.insert(0, ".")
from step_sequential_growth import sequential_growth
from sgoed_core_v7 import _compute_v_hat


def analyze(M, g, therm, seeds):
    VV = []
    for s in seeds:
        Xs, Ys = sequential_growth(M, 4, 2, 2, g, therm, s)
        VV.append(np.array([_compute_v_hat(Ys[u], 2) for u in range(M)]))
    return np.array(VV)          # (S, M, 2)


def report(M, g, therm=60, seeds=(42, 43, 44)):
    VV = analyze(M, g, therm, seeds)
    S, U, _ = VV.shape
    v0 = VV[:, 0]                                          # (S,2)
    dot0 = np.abs(np.einsum("suk,sk->su", VV, v0))         # (S,U)
    align0 = float(np.mean(dot0[:, 1:]))
    chain = float(np.mean(np.abs(np.sum(VV[:, 1:] * VV[:, :-1], axis=2))))
    mean_past = np.cumsum(VV, axis=1) / np.arange(1, U + 1)[None, :, None]
    cont = np.mean(np.linalg.norm(VV[:, U // 2:] - mean_past[:, U // 2 - 1:-1], axis=2))
    trend_late = float(np.mean(dot0[:, -min(8, U - 1):]))
    det = float(np.mean(np.abs(VV[0] - VV[1])))
    print(f"[M={M:3d} g={g:5.1f}] align_origin={align0:.4f} chain={chain:.4f} "
          f"contraction={cont:.4f} |v.v0|_late={trend_late:.4f} "
          f"inter-seed={det:.1e}")
    return {"align_origin": align0, "chain": chain, "contraction": float(cont),
            "dot_v0_late": trend_late, "inter_seed_abs_diff": det}


if __name__ == "__main__":
    out = {}
    for M in [16, 32]:
        for g in [1.0, 5.0, 20.0, 60.0]:
            r = report(M, g, therm=60)
            out[f"M{M}_g{g}"] = r
    with open("step_growth_mechanism_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_growth_mechanism_results.json")