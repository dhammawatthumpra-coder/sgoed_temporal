"""
v7 feedback-coupling scan (2026-08-30).

Tests whether adding a back-reaction X -> Y preserves the stability of the
temporal direction selected by the observer. Uses code/sgoed_core_v7.py.

Baseline: N=6, D=6, d=3, g_XY=0.8. Scan g_YX in {0.0, 0.1, 0.3, 0.5}.
Also scans d=2 and d=5 at g_YX=0.5 to see whether observer dimension matters.

Observables per config (trajectory mean over measurement window, 5 seeds):
  ratio_mean       — temporal hierarchy in X (main question)
  alignment_rate   — whether X_max still equals v_max
  X_max_extent     — largest X extent (gate saturation check)
  Y_max_extent     — largest Y extent (does Y blow up under back-reaction?)
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = [42, 43, 44, 45, 46]
t0 = time.time()
out = {'feedback': {}, 'meta': {}}

def scan(tag, N, d, gXY, gYX_list):
    print(f"=== {tag} (N={N}, d={d}, gXY={gXY}) ===", flush=True)
    for gYX in gYX_list:
        rows = []
        for s in SEEDS:
            r = run_simulation(N, D, d, gXY, gYX, s)
            rows.append(r)
        m = {k: float(np.mean([r[k] for r in rows])) for k in
             ['ratio_mean', 'alignment_rate', 'X_max_extent', 'Y_max_extent',
              'acceptance_rate']}
        sd = float(np.std([r['ratio_mean'] for r in rows]))
        m['ratio_std'] = sd
        out['feedback'][f"{tag}|gYX={gYX}"] = m
        print(f"  gYX={gYX:>4}: ratio={m['ratio_mean']:.3f}±{sd:.3f} "
              f"align={m['alignment_rate']*100:.0f}% Xmax={m['X_max_extent']:.2f} "
              f"Ymax={m['Y_max_extent']:.3f} acc={m['acceptance_rate']:.3f}", flush=True)

# Main scan: N=6, d=3, gXY=0.8
scan('N6_d3', 6, 3, 0.8, [0.0, 0.1, 0.3, 0.5])

# Observer-dimension dependence of feedback at max gYX=0.5
scan('N6_d2', 6, 2, 0.8, [0.0, 0.5])
scan('N6_d5', 6, 5, 0.8, [0.0, 0.5])

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS,
               'source': 'code/sgoed_core_v7.py run_simulation, full recompute, '
                         'trajectory mean'}
with open('AUDIT_v7_feedback_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_feedback_results.json")
