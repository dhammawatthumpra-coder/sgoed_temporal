"""
Thermalization convergence check (2026-08-30).

Question: does n_therm=20 (used everywhere) suffice for the observables to
converge? We re-run the SAME seeds with increasing thermalization
n_therm in {20, 40, 80, 160} and check whether the observables stabilize.

Two probes:
  A) v7 at the feedback transition (g_YX=1.5, N=6, d=3) — the place where
     Y_max was seen to scatter broadly across seeds; the weakest point.
  B) v6 at N=8, d=3, g=0.8 — a representative "healthy" config.

For each probe we report ratio_mean and Y_max_extent (probe A) / X_max_extent
(probe B) as a function of n_therm, for a few fixed seeds.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
import numpy as np

NTHERM = [20, 40, 80, 160]
SEEDS = [42, 43, 44]
out = {'probeA_v7_transition': {}, 'probeB_v6_N8': {}, 'meta': {}}
t0 = time.time()

# --- Probe A: v7 feedback transition ---
print("=== PROBE A: v7, N=6 d=3 gXY=0.8 gYX=1.5 (Y transition) ===", flush=True)
from sgoed_core_v7 import run_simulation as run7
for nt in NTHERM:
    rm, ymax = [], []
    for s in SEEDS:
        r = run7(6, 6, 3, 0.8, 1.5, s, n_therm=nt, n_meas=30)
        rm.append(r['ratio_mean']); ymax.append(r['Y_max_extent'])
    out['probeA_v7_transition'][str(nt)] = {
        'ratio_mean': float(np.mean(rm)), 'Ymax_mean': float(np.mean(ymax)),
        'per_seed_ratio': rm, 'per_seed_Ymax': ymax}
    print(f"  n_therm={nt:>3}: ratio={np.mean(rm):.3f} Ymax={np.mean(ymax):.3f} "
          f"seeds ratio={[round(x,3) for x in rm]} Ymax={[round(x,3) for x in ymax]}",
          flush=True)

# --- Probe B: v6 N=8 healthy ---
print("\n=== PROBE B: v6, N=8 d=3 gXY=0.8 (healthy) ===", flush=True)
from sgoed_core_v6 import run_simulation as run6
for nt in NTHERM:
    rm, wf, acc = [], [], []
    for s in SEEDS:
        r = run6(8, 6, 3, 0.8, s, n_therm=nt, n_meas=30)
        rm.append(r['ratio_mean']); wf.append(r['wall_fraction']); acc.append(r['acceptance_rate'])
    out['probeB_v6_N8'][str(nt)] = {
        'ratio_mean': float(np.mean(rm)), 'wall_fraction': float(np.mean(wf)),
        'acceptance_rate': float(np.mean(acc)), 'per_seed_ratio': rm}
    print(f"  n_therm={nt:>3}: ratio={np.mean(rm):.3f} wall_frac={np.mean(wf):.3f} "
          f"acc={np.mean(acc):.3f} seeds={[round(x,3) for x in rm]}",
          flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'seeds': SEEDS, 'n_therm_list': NTHERM}
with open('AUDIT_thermalization_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_thermalization_results.json")
