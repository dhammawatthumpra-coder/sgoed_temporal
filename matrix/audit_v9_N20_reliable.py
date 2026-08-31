"""
v9-R N=20 dimension re-run with proper thermalization (n_therm=200).
"""
import numpy as np, time
from sgoed_hypergraph_core_v9 import run_v9

SEEDS = [42, 43, 44, 45, 46]
N = 20
t0 = time.time()
r_, a_, d_, l_, e_ = [], [], [], [], []
for s in SEEDS:
    r = run_v9(N=N, d=3, g_xy=0.8, g_yx=0.0, n_therm=200, n_measure=30, seed=s)
    r_.append(r[0]); a_.append(r[2]); d_.append(r[3]); l_.append(r[4]); e_.append(r[5])
    print(f"  seed={s}: R={r[0]:.4f} d_MM={r[3]:.2f} L_max={r[4]:.1f} obs_ext={r[5]:.4f}", flush=True)

print(f"\n=== N={N} n_therm=200 (5 seeds) ===")
print(f"  R={np.mean(r_):.4f}±{np.std(r_):.4f} align={np.mean(a_):.3f} "
      f"d_MM={np.mean(d_):.2f}±{np.std(d_):.2f} [{ [round(x,2) for x in d_] }] "
      f"L_max={np.mean(l_):.1f} obs_ext={np.mean(e_):.4f} ({(time.time()-t0)/60:.1f} min)")

import json
json.dump({'N_20': {'R': float(np.mean(r_)), 'align': float(np.mean(a_)),
                    'd_MM': float(np.mean(d_)), 'd_MM_std': float(np.std(d_)),
                    'per_seed_dMM': [round(x,2) for x in d_],
                    'L_max': float(np.mean(l_)), 'obs_extent': float(np.mean(e_))}},
          open('audit_v9_N20_reliable.json','w'), indent=2)
print("Saved audit_v9_N20_reliable.json")