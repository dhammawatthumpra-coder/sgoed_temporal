"""
v7 feedback-coupling — n=30 transition scan (2026-08-30).

Tests whether the Y -> gate transition around g_YX = 1.3..1.6 is a genuine
bistability (each seed lands in one of two basins: Y small vs Y ~ gate) and
estimates the fraction of seeds that hit the gate with a credible sample.

d=3, N=6, g_XY=0.8. g_YX in {1.3, 1.4, 1.5, 1.6}, 30 fresh seeds (100..129).
Records the full per-seed Y_max_extent distribution (not just the mean).
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = list(range(100, 130))  # 30 fresh seeds
GYX_LIST = [1.3, 1.4, 1.5, 1.6]
t0 = time.time()
out = {'feedback': {}, 'meta': {}}

print(f"=== n=30 TRANSITION SCAN d=3, N=6, gXY=0.8, gYX={GYX_LIST} ===", flush=True)
for gYX in GYX_LIST:
    rows = []
    for s in SEEDS:
        r = run_simulation(6, D, 3, 0.8, gYX, s)
        rows.append(r)
    ymax = np.array([r['Y_max_extent'] for r in rows])
    ratio = np.array([r['ratio_mean'] for r in rows])
    align = np.array([r['alignment_rate'] for r in rows])

    # gate-hit: Y extent pinned at >= 9.9 (the gate ceiling)
    hit = ymax >= 9.9
    # "small" basin: Y extent stayed near its confined value (~0.5-0.7)
    small = ymax < 2.0
    m = {
        'Ymax_mean': float(ymax.mean()),
        'Ymax_std': float(ymax.std()),
        'Ymax_min': float(ymax.min()),
        'Ymax_max': float(ymax.max()),
        'n_hit_gate': int(hit.sum()),
        'frac_hit_gate': float(hit.mean()),
        'n_small': int(small.sum()),
        'n_between': int(((~hit) & (~small)).sum()),  # intermediate basin
        'ratio_mean': float(ratio.mean()), 'ratio_std': float(ratio.std()),
        'align_rate': float(align.mean()),
        'Ymax_distribution': ymax.tolist(),
        'ratio_distribution': ratio.tolist(),
    }
    out['feedback'][f"gYX={gYX}"] = m
    # histogram of Y_max to visualize bimodality
    hist, edges = np.histogram(ymax, bins=[0, 1, 2, 4, 6, 8, 9.5, 9.9, 10.1])
    print(f"  gYX={gYX:>4}: hit={m['n_hit_gate']:>2}/30 ({m['frac_hit_gate']*100:.0f}%)  "
          f"small={m['n_small']:>2}/30  between={m['n_between']:>2}/30  "
          f"ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f} align={m['align_rate']*100:.0f}%",
          flush=True)
    print(f"           Ymax hist (bins 0-1,1-2,2-4,4-6,6-8,8-9.5,9.5-9.9,9.9-10.1): {hist.tolist()}",
          flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'gYX_list': GYX_LIST,
               'source': 'code/sgoed_core_v7.py run_simulation, full recompute, '
                         'trajectory mean'}
with open('AUDIT_v7_feedback_n30_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_feedback_n30_results.json")
