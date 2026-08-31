"""
v7 feedback — CLEAN transition scan with n_therm=40 (2026-08-30).

Re-runs the Y -> gate transition because the thermalization check showed
n_therm=20 was insufficient at the transition (some seeds were frozen
mid-transition). n_therm=40 stabilizes Y_max_extent (verified in
AUDIT_thermalization_results.json).

d=3, N=6, g_XY=0.8. g_YX in {1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6}, 30 fresh
seeds (100..129). Reports the full per-seed Y_max distribution so we can
distinguish a continuous crossover from a genuine bimodality.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = list(range(100, 130))
GYX_LIST = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
N_THERM = 40
t0 = time.time()
out = {'feedback': {}, 'meta': {}}

print(f"=== CLEAN TRANSITION d=3 N=6 gXY=0.8, n_therm={N_THERM}, n=30 ===", flush=True)
for gYX in GYX_LIST:
    ym = []; rm = []; al = []
    for s in SEEDS:
        r = run_simulation(6, D, 3, 0.8, gYX, s, n_therm=N_THERM, n_meas=30)
        ym.append(r['Y_max_extent']); rm.append(r['ratio_mean']); al.append(r['alignment_rate'])
    ym = np.array(ym); rm = np.array(rm); al = np.array(al)
    hit = ym >= 9.9
    small = ym < 2.0
    m = {
        'Ymax_mean': float(ym.mean()), 'Ymax_std': float(ym.std()),
        'n_hit_gate': int(hit.sum()), 'frac_hit_gate': float(hit.mean()),
        'n_small': int(small.sum()), 'n_between': int(((~hit) & (~small)).sum()),
        'ratio_mean': float(rm.mean()), 'ratio_std': float(rm.std()),
        'align_rate': float(al.mean()),
        'Ymax_distribution': ym.tolist(),
    }
    out['feedback'][f"gYX={gYX}"] = m
    hist, edges = np.histogram(ym, bins=[0, 1, 2, 4, 6, 8, 9.5, 9.9, 10.1])
    print(f"  gYX={gYX:>4}: hit={m['n_hit_gate']:>2}/30 ({m['frac_hit_gate']*100:.0f}%)  "
          f"small={m['n_small']:>2}/30  between={m['n_between']:>2}/30  "
          f"ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f} align={m['align_rate']*100:.0f}%",
          flush=True)
    print(f"           Ymax hist: {hist.tolist()}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'n_therm': N_THERM,
               'source': 'code/sgoed_core_v7.py, full recompute, n_therm=40 trajectory mean'}
with open('AUDIT_v7_transition_clean_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_transition_clean_results.json")
