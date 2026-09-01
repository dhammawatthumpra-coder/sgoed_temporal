"""
Large-N scan (2026-08-30) — extends v6 beyond N=8 to test whether the
"no crossover" robustness persists.

Configs: d=3, D=6, g_XY=0.8. N in {9, 10, 12, 14, 16}. 5 seeds each.
Uses v6 (trajectory mean). Reports ratio_mean, alignment_rate, wall_fraction,
acceptance_rate, tau_int, n_eff.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v6 import run_simulation
import numpy as np

D = 6
SEEDS = [42, 43, 44, 45, 46]
N_LIST = [9, 10, 12, 14, 16]
t0 = time.time()
out = {'large_n': {}, 'meta': {}}

print(f"=== LARGE-N SCAN d=3, gXY=0.8, N={N_LIST} ===", flush=True)
for N in N_LIST:
    rows = []
    for s in SEEDS:
        r = run_simulation(N, D, 3, 0.8, s)
        rows.append(r)
    m = {k: float(np.mean([r[k] for r in rows])) for k in
         ['ratio_mean', 'alignment_rate', 'wall_fraction', 'acceptance_rate',
          'tau_int', 'n_eff']}
    m['ratio_std'] = float(np.std([r['ratio_mean'] for r in rows]))
    m['per_seed_ratio'] = [round(r['ratio_mean'], 3) for r in rows]
    m['per_seed_align'] = [int(r['alignment_rate'] > 0.5) for r in rows]
    m['per_seed_wall'] = [round(r['wall_fraction'], 3) for r in rows]
    out['large_n'][str(N)] = m
    print(f"  N={N:>2}: ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f} "
          f"align={m['alignment_rate']*100:.0f}% wall={m['wall_fraction']:.3f} "
          f"acc={m['acceptance_rate']:.3f} tau={m['tau_int']:.1f} neff={m['n_eff']:.1f}",
          flush=True)
    print(f"          seeds ratio={m['per_seed_ratio']} align={m['per_seed_align']} "
          f"wall={m['per_seed_wall']}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'D': D, 'seeds': SEEDS, 'N_list': N_LIST,
               'source': 'code/sgoed_core_v6.py run_simulation, trajectory mean'}
with open('AUDIT_large_n_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_large_n_results.json")
