"""
v7 feedback — N-dependence of critical g_YX (2026-08-30).

Tests whether smaller N is more fragile (hits the gate at lower g_YX).
N=4 and N=8, d=3, g_XY=0.8. g_YX in {1.0, 1.3, 1.6, 1.9}, n_therm=40, 30 seeds.

NOTE: N=12 was requested but is deferred — v7 uses full recompute, and N=12
(144 matrix elements x O(N^2) action per update) is prohibitively slow. It
requires a delta-sampler optimization first.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = list(range(100, 130))
GYX_LIST = [1.0, 1.3, 1.6, 1.9]
N_THERM = 40
t0 = time.time()
out = {'N4': {}, 'N8': {}, 'meta': {}}

for N in [4, 8]:
    print(f"\n=== N={N} CRITICAL gYX scan d=3 gXY=0.8 n_therm={N_THERM} n=30 ===", flush=True)
    for gYX in GYX_LIST:
        ym = []; rm = []; al = []
        for s in SEEDS:
            r = run_simulation(N, D, 3, 0.8, gYX, s, n_therm=N_THERM, n_meas=30)
            ym.append(r['Y_max_extent']); rm.append(r['ratio_mean']); al.append(r['alignment_rate'])
        ym = np.array(ym); rm = np.array(rm); al = np.array(al)
        hit = ym >= 9.9
        m = {'Ymax_mean': float(ym.mean()), 'n_hit_gate': int(hit.sum()),
             'frac_hit_gate': float(hit.mean()),
             'ratio_mean': float(rm.mean()), 'align_rate': float(al.mean()),
             'Ymax_distribution': ym.tolist()}
        out[f"N{N}"][f"gYX={gYX}"] = m
        print(f"  gYX={gYX:>4}: hit={m['n_hit_gate']:>2}/30 ({m['frac_hit_gate']*100:.0f}%)  "
              f"ratio={m['ratio_mean']:.3f} align={m['align_rate']*100:.0f}%",
              flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'n_therm': N_THERM, 'source': 'sgoed_core_v7.py, n_therm=40'}
with open('AUDIT_v7_Ndep_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_Ndep_results.json")
