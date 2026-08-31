"""
v7 feedback — g_XY-dependence of critical g_YX (2026-08-30).

Earlier (n=5) we saw g_XY=1.15 makes Y hit the gate MORE easily than
g_XY=0.8 — opposite to a simple "g_YX ~ alpha*g_XY" rule. Here we quantify
the critical g_YX at two g_XY values with n=30, n_therm=40.

d=3, N=6. g_XY in {0.8, 1.15}. g_YX in {0.8, 1.0, 1.2, 1.4}.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = list(range(100, 130))
GYX_LIST = [0.8, 1.0, 1.2, 1.4]
N_THERM = 40
t0 = time.time()
out = {'gXY_0.8': {}, 'gXY_1.15': {}, 'meta': {}}

for gXY in [0.8, 1.15]:
    print(f"\n=== gXY={gXY} CRITICAL gYX scan d=3 N=6 n_therm={N_THERM} n=30 ===", flush=True)
    for gYX in GYX_LIST:
        ym = []; rm = []; al = []
        for s in SEEDS:
            r = run_simulation(6, D, 3, gXY, gYX, s, n_therm=N_THERM, n_meas=30)
            ym.append(r['Y_max_extent']); rm.append(r['ratio_mean']); al.append(r['alignment_rate'])
        ym = np.array(ym); rm = np.array(rm); al = np.array(al)
        hit = ym >= 9.9
        m = {'Ymax_mean': float(ym.mean()), 'n_hit_gate': int(hit.sum()),
             'frac_hit_gate': float(hit.mean()),
             'ratio_mean': float(rm.mean()), 'align_rate': float(al.mean()),
             'Ymax_distribution': ym.tolist()}
        out[f"gXY_{gXY}"][f"gYX={gYX}"] = m
        print(f"  gYX={gYX:>4}: hit={m['n_hit_gate']:>2}/30 ({m['frac_hit_gate']*100:.0f}%)  "
              f"ratio={m['ratio_mean']:.3f} align={m['align_rate']*100:.0f}%",
              flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'n_therm': N_THERM, 'source': 'sgoed_core_v7.py, n_therm=40'}
with open('AUDIT_v7_gXYdep_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_gXYdep_results.json")
