"""
v7 feedback-coupling scan — HIGH g_YX regime (2026-08-30).

Extends AUDIT_v7_feedback.py to search for the critical g_YX at which the
back-reaction destabilizes the temporal direction. Focus on d=3 (baseline)
and d=5 (most sensitive in the previous scan), N=6, g_XY=0.8.

g_YX scanned: 0.5, 1.0, 1.5, 2.0, 3.0, 5.0  (5 seeds each).
Observables (trajectory mean): ratio_mean, alignment_rate, X_max_extent,
Y_max_extent, acceptance_rate.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = [42, 43, 44, 45, 46]
GYX_LIST = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
t0 = time.time()
out = {'feedback': {}, 'meta': {}}

def scan(tag, N, d, gXY):
    print(f"=== {tag} (N={N}, d={d}, gXY={gXY}) ===", flush=True)
    for gYX in GYX_LIST:
        rows = []
        for s in SEEDS:
            r = run_simulation(N, D, d, gXY, gYX, s)
            rows.append(r)
        m = {k: float(np.mean([r[k] for r in rows])) for k in
             ['ratio_mean', 'alignment_rate', 'X_max_extent', 'Y_max_extent',
              'acceptance_rate']}
        m['ratio_std'] = float(np.std([r['ratio_mean'] for r in rows]))
        # per-seed detail for alignment + Y extent
        m['per_seed_ratio'] = [round(r['ratio_mean'], 3) for r in rows]
        m['per_seed_align'] = [int(r['alignment_rate'] > 0.5) for r in rows]
        m['per_seed_Ymax'] = [round(r['Y_max_extent'], 3) for r in rows]
        out['feedback'][f"{tag}|gYX={gYX}"] = m
        print(f"  gYX={gYX:>4}: ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f} "
              f"align={m['alignment_rate']*100:.0f}% Xmax={m['X_max_extent']:.2f} "
              f"Ymax={m['Y_max_extent']:.3f} acc={m['acceptance_rate']:.3f}", flush=True)
        print(f"           seeds ratio={m['per_seed_ratio']} "
              f"align={m['per_seed_align']} Ymax={m['per_seed_Ymax']}", flush=True)

scan('N6_d3', 6, 3, 0.8)
scan('N6_d5', 6, 5, 0.8)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'source': 'code/sgoed_core_v7.py run_simulation, full recompute, '
                         'trajectory mean'}
with open('AUDIT_v7_feedback_high_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_feedback_high_results.json")
