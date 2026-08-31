"""v12 workplan step 1: D significance at N=24 (30 seeds) and N=48 (25 seeds)."""
import numpy as np
from sgoed_graph_core_v12 import run_v12


def run_scan(N, seeds, therm=40, meas=20):
    Ds, Fs, specs, aligns = [], [], [], []
    for s in seeds:
        D, F, spec, align, W = run_v12(
            N=N, d=3, g_xy=1.5, lambda_cond=0.15,
            n_therm=therm, n_measure=meas, seed=s
        )
        Ds.append(D)
        Fs.append(F)
        specs.append(spec)
        aligns.append(align)
    Ds, specs = np.array(Ds), np.array(specs)
    sig = abs(Ds.mean()) / (Ds.std() + 1e-9)
    print(f"N={N} ({len(seeds)} seeds): D={Ds.mean():+.1f} +/- {Ds.std():.1f} "
          f"| significance={sig:.2f} | spec={specs.mean():.2f} +/- {specs.std():.2f} "
          f"| align={np.mean(aligns)*100:.0f}%")
    neg = int((Ds < 0).sum())
    print(f"  seeds with D<0: {neg}/{len(seeds)} | F_net mean={np.mean(Fs):+.2f}")
    print(f"  per-seed D: {[f'{x:+.0f}' for x in Ds]}")
    print(f"  per-seed spec: {[f'{x:.1f}' for x in specs]}")
    return Ds, specs


print("=" * 72)
print(" STEP 1a: N=24, 30 seeds (n_therm=40)")
print("=" * 72)
run_scan(24, list(range(42, 72)))

print()
print("=" * 72)
print(" STEP 1b: N=48, 25 seeds (n_therm=40, n_measure=20)")
print("=" * 72)
run_scan(48, list(range(42, 67)))
