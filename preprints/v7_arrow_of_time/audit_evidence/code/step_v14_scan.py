"""v14 g_inter scan (M=6, N=4, 3 seeds): alignment + per-unit condensation."""
import sys
import time
import numpy as np
sys.path.insert(0, ".")
from sgoed_matrix_ecosystem_v14 import run_v14, unit_observables

print("=" * 78)
print(" v14 g_inter scan: M=6, N=4, D=2, d=2, n_therm=50 (3 seeds)")
print("=" * 78)
print(f"  {'g_inter':>7} | {'A (align)':>9} | {'spec':>5} | {'exts_std':>8} | {'vdot':>6}")
for g in [0.0, 0.05, 0.1, 0.2, 0.5]:
    As, specs, estds, vdots = [], [], [], []
    for s in [42, 43, 44]:
        Xs, Ys = run_v14(M=6, N=4, g_inter=g, n_therm=50, n_measure=10, seed=s)
        exts, spec, vhats, A, cs = unit_observables(Xs, Ys)
        As.append(A)
        specs.append(spec.mean())
        estds.append(exts.std())
        # v_hat dot products (observer directions)
        vd = 0.0
        for u in range(6):
            for v in range(u + 1, 6):
                vd += float(vhats[u] @ vhats[v])
        vdots.append(vd / 15.0)
    print(f"  {g:7.2f} | {np.mean(As):+9.3f} | {np.mean(specs):5.1f} | "
          f"{np.mean(estds):8.3f} | {np.mean(vdots):+6.2f}")

print()
print("=" * 78)
print(" Null comparison: A of random (unconnected) vs coupled at g=0.5")
print("=" * 78)
# random X (no thermalize) alignment baseline
rng = np.random.default_rng(0)
c0 = []
for rep in range(5):
    Xr = np.zeros((6, 2, 4, 4))
    for u in range(6):
        A = rng.randn(4, 4) * 0.5
        Xr[u, 0] = (A + A.T) / 2
    for u in range(6):
        for v in range(u + 1, 6):
            Au, Av = Xr[u, 0], Xr[v, 0]
            c0.append(float(np.trace(Au @ Av)) / (np.linalg.norm(Au) * np.linalg.norm(Av) + 1e-8))
print(f"  random initial alignment: {np.mean(c0):+.3f} +/- {np.std(c0):.3f}")
