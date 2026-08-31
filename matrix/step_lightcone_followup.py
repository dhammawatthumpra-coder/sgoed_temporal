"""
Follow-up to step_growth_lightcone: two discriminating checks.
(a) UNIFORM scatter (not a walk) on the torus: should read ~ 1+d_sp
    exactly (the calibration geometry) -> validates the whole pipeline
    matrix -> D_space -> cone -> d_MM. The low 1.17/1.21 readout of the
    walk leg is then attributable to walk correlation, not the machinery.
(b) sigma-scan of the walk (spatial diffusion rate): d_MM should rise
    monotonically with sigma (more spatial spread -> fewer causal pairs
    -> higher dimension): the diffusion/light-speed ratio is the control.
All checks come with the same M {250,500,1000} invariance audit.
"""
import json
import sys
import numpy as np
sys.path.insert(0, ".")
from step_causal_set_scale_study import calibration, read_dim
from step_growth_lightcone import leg2_poset

Ms = [250, 500, 1000]
out = {}


def audit(name, maker):
    print(f"\n{name}")
    rows = {}
    for M in Ms:
        ds, rhos = calibration(M, seeds=8)
        dims = [read_dim(int(maker(M, s).sum()) / (M * (M - 1) / 2), ds, rhos)
                for s in range(42, 48)]
        m, sd = float(np.mean(dims)), float(np.std(dims))
        rows[str(M)] = {"d_mean": m, "d_std": sd}
        print(f"  M={M:5d}: d_MM = {m:.2f} ± {sd:.2f}")
    rows["std_across_N"] = round(float(np.std([rows[str(M)]["d_mean"] for M in Ms])), 3)
    out[name] = rows
    return rows


r_u1 = audit("uniform scatter circle (d_sp=1)  [expect ~2]",
             lambda M, s: leg2_poset(M, s, 1, walk=False))
r_u3 = audit("uniform scatter 3-torus (d_sp=3) [expect ~4]",
             lambda M, s: leg2_poset(M, s, 3, walk=False))

print("\nsigma-scan of the walk (d_sp=3, M=500):")
sig = {}
for sigma in [0.3, 1.0, 2.0, 4.0]:
    ds, rhos = calibration(500, seeds=8)
    dims = [read_dim(int(leg2_poset(500, s, 3, sigma=sigma).sum()) / (500 * 499 / 2), ds, rhos)
            for s in range(42, 48)]
    m = float(np.mean(dims))
    sig[str(sigma)] = round(m, 3)
    print(f"  sigma={sigma:>4}: d_MM = {m:.2f}")
out["sigma_scan"] = sig

print("\nc-scan: light speed is the aspect-ratio knob (target: d=1+d_sp)")
cscan = {}
ds, rhos = calibration(500, seeds=8)
for name, d_sp, walk_flag in [("uniform d_sp=1 [target 2]", 1, False),
                              ("walk    d_sp=3 sigma=2 [target 4]", 3, True)]:
    for val in [0.05, 0.1, 0.2, 0.4, 0.8]:
        dims = [read_dim(int(leg2_poset(500, s, d_sp, c=val, sigma=2.0, walk=walk_flag).sum())
                         / (500 * 499 / 2), ds, rhos) for s in range(42, 48)]
        m = float(np.mean(dims))
        print(f"  {name:28s} c={val:<5}: d_MM = {m:.2f}")
        cscan[f"{name}|c={val}"] = round(m, 3)
out["c_scan"] = cscan

with open(r"F:\_Ai\sgoed\sgoed\matrix\step_lightcone_followup_results.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nsaved -> step_lightcone_followup_results.json")