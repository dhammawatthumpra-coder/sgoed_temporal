"""
v7 feedback — relative-coupling test + N-dependence (2026-08-30).

Two questions:
  (3) Does the critical g_YX (where Y hits the gate) scale with g_XY? We scan
      g_YX at g_XY=1.15 and compare the transition location with the g_XY=0.8
      result. If the rule is g_YX ~ alpha*g_XY, the transition should shift
      up in proportion.
  (4) Does the transition location depend on system size N?

n_therm=40 (per the thermalization finding: n_therm=20 was insufficient at
the transition). d=3, D=6. 5 seeds each (pilot; n=30 can follow if needed).

Configs:
  relative: N=6, g_XY=1.15, g_YX in {1.5, 1.7, 1.9, 2.2, 2.5}
  N-dependence: g_XY=0.8, N in {4, 8}, g_YX in {1.3, 1.6, 1.9}
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = [42, 43, 44, 45, 46]
t0 = time.time()
out = {'relative': {}, 'N_dependence': {}, 'meta': {}}

def scan(tag, N, d, gXY, gYX_list):
    print(f"=== {tag} (N={N}, gXY={gXY}) ===", flush=True)
    for gYX in gYX_list:
        ym, rm, al = [], [], []
        for s in SEEDS:
            r = run_simulation(N, D, d, gXY, gYX, s, n_therm=40, n_meas=30)
            ym.append(r['Y_max_extent']); rm.append(r['ratio_mean'])
            al.append(r['alignment_rate'])
        hit = sum(1 for y in ym if y >= 9.9)
        rec = {'gYX': gYX, 'Ymax_mean': float(np.mean(ym)),
               'ratio_mean': float(np.mean(rm)), 'align': float(np.mean(al)),
               'n_hit_gate': hit, 'per_seed_Ymax': [round(x,3) for x in ym]}
        out[tag][f"{gYX}"] = rec
        print(f"  gYX={gYX:>4}: Ymax={np.mean(ym):.3f} hit={hit}/5 "
              f"ratio={np.mean(rm):.3f} align={np.mean(al)*100:.0f}% "
              f"seeds_Ymax={[round(x,3) for x in ym]}", flush=True)

# (3) relative: g_XY = 1.15
scan('relative', 6, 3, 1.15, [1.5, 1.7, 1.9, 2.2, 2.5])

# (4) N-dependence: g_XY = 0.8, N = 4 and 8
scan('N_dependence', 4, 3, 0.8, [1.3, 1.6, 1.9])
scan('N_dependence_N8', 8, 3, 0.8, [1.3, 1.6, 1.9])

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'n_therm': 40,
               'source': 'code/sgoed_core_v7.py run_simulation, full recompute, '
                         'n_therm=40 trajectory mean'}
with open('AUDIT_v7_relative_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_relative_results.json")
