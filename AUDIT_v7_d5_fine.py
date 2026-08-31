"""
v7 feedback — d=5 fine scan g_YX 1.4..1.9 step 0.05 (2026-08-30).

Pinpoints the d=5 critical g_YX (previously estimated ~1.5-1.8 from coarse
data). n_therm=40, n=30 seeds, d=5, N=6, g_XY=0.8.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = list(range(100, 130))
GYX_LIST = [round(1.4 + 0.05 * k, 2) for k in range(11)]  # 1.40..1.90
N_THERM = 40
t0 = time.time()
out = {'d5_fine': {}, 'meta': {}}

print(f"=== d=5 FINE SCAN gYX=1.40..1.90 step0.05 n_therm={N_THERM} n=30 ===", flush=True)
for gYX in GYX_LIST:
    ym = []; rm = []; al = []
    for s in SEEDS:
        r = run_simulation(6, D, 5, 0.8, gYX, s, n_therm=N_THERM, n_meas=30)
        ym.append(r['Y_max_extent']); rm.append(r['ratio_mean']); al.append(r['alignment_rate'])
    ym = np.array(ym); rm = np.array(rm); al = np.array(al)
    hit = ym >= 9.9
    m = {'Ymax_mean': float(ym.mean()), 'n_hit_gate': int(hit.sum()),
         'frac_hit_gate': float(hit.mean()),
         'ratio_mean': float(rm.mean()), 'align_rate': float(al.mean()),
         'Ymax_distribution': ym.tolist()}
    out['d5_fine'][f"gYX={gYX}"] = m
    print(f"  gYX={gYX:>4}: hit={m['n_hit_gate']:>2}/30 ({m['frac_hit_gate']*100:.0f}%)  "
          f"ratio={m['ratio_mean']:.3f} align={m['align_rate']*100:.0f}%", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'n_therm': N_THERM, 'source': 'sgoed_core_v7.py, n_therm=40, d=5 fine'}
with open('AUDIT_v7_d5_fine_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_d5_fine_results.json")
