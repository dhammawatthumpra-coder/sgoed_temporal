"""
v7 feedback-coupling — FINE scan of the transition region (2026-08-30).

Pinpoints the critical g_YX at which the back-reaction drives the observer Y
into the stability gate (Y_max_extent -> 10). d=3 only, N=6, g_XY=0.8.

g_YX scanned: 1.00 .. 2.00 step 0.10 (11 points), 5 seeds each.
Records per-seed Y_max_extent so we can count how many seeds hit the gate.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = [42, 43, 44, 45, 46]
GYX_LIST = [round(1.0 + 0.1 * k, 2) for k in range(11)]  # 1.00..2.00
t0 = time.time()
out = {'feedback': {}, 'meta': {}}

print(f"=== FINE SCAN d=3, N=6, gXY=0.8, gYX={GYX_LIST} ===", flush=True)
for gYX in GYX_LIST:
    rows = []
    for s in SEEDS:
        r = run_simulation(6, D, 3, 0.8, gYX, s)
        rows.append(r)
    m = {k: float(np.mean([r[k] for r in rows])) for k in
         ['ratio_mean', 'alignment_rate', 'X_max_extent', 'Y_max_extent',
          'acceptance_rate']}
    m['ratio_std'] = float(np.std([r['ratio_mean'] for r in rows]))
    m['per_seed_Ymax'] = [round(r['Y_max_extent'], 3) for r in rows]
    m['n_hit_gate'] = sum(1 for y in m['per_seed_Ymax'] if y >= 9.9)
    out['feedback'][f"gYX={gYX}"] = m
    print(f"  gYX={gYX:>4}: ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f} "
          f"align={m['alignment_rate']*100:.0f}% Ymax={m['Y_max_extent']:.3f} "
          f"hit={m['n_hit_gate']}/5  per_seed_Ymax={m['per_seed_Ymax']}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'source': 'code/sgoed_core_v7.py run_simulation, full recompute, '
                         'trajectory mean'}
with open('AUDIT_v7_feedback_fine_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_feedback_fine_results.json")
