"""
v12 critical check (self-written, data honesty):
1. Baseline (g_xy=0, lambda_cond=0) vs Real at N=24/32/48: sigma-ratio & D
   with per-seed values (is D consistently negative = real arrow, or noise?)
2. D significance: mean vs std across seeds
3. Thermalization check at N=32 (n_therm 40 vs 120)
"""
import numpy as np
from sgoed_graph_core_v12 import run_v12


def scan(N, g_xy, lam, seeds, n_therm=40):
    Ds, Fs, specs, aligns = [], [], [], []
    for s in seeds:
        D, F, spec, align, W = run_v12(
            N=N, d=3, g_xy=g_xy, lambda_cond=lam, n_therm=n_therm, n_measure=20, seed=s
        )
        Ds.append(D)
        Fs.append(F)
        specs.append(spec)
        aligns.append(align)
    return np.array(Ds), np.array(Fs), np.array(specs), np.array(aligns)


seeds = [42, 43, 44, 45, 46]
print("=" * 80)
print(" 1. BASELINE (uncoupled) vs REAL at N=24/32/48 (per-seed, 5 seeds)")
print("=" * 80)
for N in [24, 32, 48]:
    Db, Fb, Sb, Ab = scan(N, 0.0, 0.0, seeds)
    Dr, Fr, Sr, Ar = scan(N, 1.5, 0.15, seeds)
    print(f"\n N={N}: maxD={N*(N-1)//2}")
    print(f"   baseline: D={Db.mean():+7.1f} +/- {Db.std():5.1f}  spec={Sb.mean():5.2f} +/- {Sb.std():.2f}")
    print(f"            per-seed D: {[f'{x:+.0f}' for x in Db]}")
    print(f"   real    : D={Dr.mean():+7.1f} +/- {Dr.std():5.1f}  spec={Sr.mean():5.2f} +/- {Sr.std():.2f}  align={Ar.mean()*100:.0f}%")
    print(f"            per-seed D: {[f'{x:+.0f}' for x in Dr]}")
    sig = abs(Dr.mean()) / (Dr.std() + 1e-9)
    print(f"   -> D significance: |mean|/std = {sig:.2f}  |  spec real/baseline sep: "
          f"{(Sr.mean()-Sb.mean())/(Sb.std()+1e-9):.1f} sigma")

print()
print("=" * 80)
print(" 2. THERMALIZATION check at N=32 (n_therm 40 vs 120)")
print("=" * 80)
for therm in [40, 120]:
    Ds, Fs, Ss, As = scan(32, 1.5, 0.15, seeds, n_therm=therm)
    print(f"   n_therm={therm:3d}: D={Ds.mean():+7.1f} +/- {Ds.std():5.1f} | spec={Ss.mean():5.2f} +/- {Ss.std():.2f} | align={As.mean()*100:.0f}%")
