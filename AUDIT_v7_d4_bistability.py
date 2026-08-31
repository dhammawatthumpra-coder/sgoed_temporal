"""
v7 feedback — d=4 bistability check (2026-08-30).

Completes the d-dependence map of the Y -> gate transition:
  d=3: critical g_YX ~ 1.1-1.2  (done)
  d=5: critical g_YX ~ 1.5-1.8  (done)
  d=4: unknown -> expected between 1.2 and 1.5.

d=4, N=6, g_XY=0.8. g_YX in {1.2, 1.3, 1.4, 1.5, 1.6}, n_therm=40, 30 seeds.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = list(range(100, 130))
GYX_LIST = [1.2, 1.3, 1.4, 1.5, 1.6]
N_THERM = 40
t0 = time.time()
out = {'d4': {}, 'meta': {}}

print(f"=== d=4 BISTABILITY N=6 gXY=0.8 n_therm={N_THERM} n=30 ===", flush=True)
for gYX in GYX_LIST:
    ym = []; rm = []; al = []
    for s in SEEDS:
        r = run_simulation(6, D, 4, 0.8, gYX, s, n_therm=N_THERM, n_meas=30)
        ym.append(r['Y_max_extent']); rm.append(r['ratio_mean']); al.append(r['alignment_rate'])
    ym = np.array(ym); rm = np.array(rm); al = np.array(al)
    hit = ym >= 9.9
    small = ym < 2.0
    m = {'Ymax_mean': float(ym.mean()), 'Ymax_std': float(ym.std()),
         'n_hit_gate': int(hit.sum()), 'frac_hit_gate': float(hit.mean()),
         'n_small': int(small.sum()), 'n_between': int(((~hit) & (~small)).sum()),
         'ratio_mean': float(rm.mean()), 'ratio_std': float(rm.std()),
         'align_rate': float(al.mean()), 'Ymax_distribution': ym.tolist()}
    out['d4'][f"gYX={gYX}"] = m
    hist, _ = np.histogram(ym, bins=[0, 1, 2, 4, 6, 8, 9.5, 9.9, 10.1])
    print(f"  gYX={gYX:>4}: hit={m['n_hit_gate']:>2}/30 ({m['frac_hit_gate']*100:.0f}%)  "
          f"small={m['n_small']:>2}/30  between={m['n_between']:>2}/30  "
          f"ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f} align={m['align_rate']*100:.0f}%",
          flush=True)
    print(f"           Ymax hist: {hist.tolist()}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'n_therm': N_THERM, 'source': 'sgoed_core_v7.py, n_therm=40, d=4'}
with open('AUDIT_v7_d4_bistability_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_d4_bistability_results.json")
