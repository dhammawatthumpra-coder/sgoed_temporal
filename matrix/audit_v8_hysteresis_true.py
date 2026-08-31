"""
v8-R (graph) — TRUE hysteresis via anneal, UP vs DOWN (2026-08-30).

Uses sgoed_graph_core_v4.run_v4 to carry the graph W across g_yx, so the
system remembers its state. A first-order transition shows a hysteresis loop:
the critical g_yx on the UP sweep differs from the DOWN sweep.

N=24, d=3, g_xy=0.8, n_therm=240. Single seed per chain (anneal is seed-fixed).
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from sgoed_graph_core_v4 import run_v4

N, d, g_xy = 24, 3, 0.8
N_THERM, N_MEAS = 240, 40
SEED = 42
UP = [0.0, 0.4, 0.8, 1.0, 1.2, 1.6, 2.0]
DOWN = list(reversed(UP))
t0 = time.time()
out = {'up': {}, 'down': {}, 'meta': {}}

def anneal(gseq):
    W = None
    recs = []
    for g in gseq:
        res = run_v4(N=N, d=d, g_xy=g_xy, g_yx=g, n_therm=N_THERM, n_measure=N_MEAS,
                     seed=SEED, W_init=W)
        W = res[6]
        recs.append((g, res[5]))  # obs_extent
    return recs

print(f"=== TRUE HYSTERESIS (anneal, carry W) N={N}, d={d}, n_therm={N_THERM} ===", flush=True)
for direction, gseq in [('up', UP), ('down', DOWN)]:
    print(f"\n--- {direction.upper()} ---", flush=True)
    recs = anneal(gseq)
    for g, ext in recs:
        out[direction][f"g_yx_{g}"] = {'g_yx': g, 'obs_extent': float(ext)}
        print(f"  g_yx={g:>4}: obs_extent={ext:.4f}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'N': N, 'd': d, 'g_xy': g_xy,
               'n_therm': N_THERM, 'seed': SEED, 'up': UP, 'down': DOWN}
with open('audit_v8_hysteresis_true_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved audit_v8_hysteresis_true_results.json")
