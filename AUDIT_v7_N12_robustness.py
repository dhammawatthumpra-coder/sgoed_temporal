"""
v7 feedback — N=12 X-robustness test (2026-08-30).

Question: at N=12 (larger matrices), does the temporal direction X remain
robust under back-reaction, even when the observer Y is driven into the gate?

N=12, d=3, D=6, g_XY=0.8. g_YX in {0.8, 1.5, 2.0, 3.0, 5.0}, 5 seeds each,
n_therm=40 (pilot showed ~31s/run at N=12).
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
N = 12
SEEDS = [42, 43, 44, 45, 46]
GYX_LIST = [0.8, 1.5, 2.0, 3.0, 5.0]
N_THERM = 40
t0 = time.time()
out = {'N12': {}, 'meta': {}}

print(f"=== N=12 X-ROBUSTNESS d=3 gXY=0.8 n_therm={N_THERM} ===", flush=True)
for gYX in GYX_LIST:
    rm, al, xm, ym, acc = [], [], [], [], []
    for s in SEEDS:
        r = run_simulation(N, D, 3, 0.8, gYX, s, n_therm=N_THERM, n_meas=30)
        rm.append(r['ratio_mean']); al.append(r['alignment_rate'])
        xm.append(r['X_max_extent']); ym.append(r['Y_max_extent'])
        acc.append(r['acceptance_rate'])
    m = {'ratio_mean': float(np.mean(rm)), 'ratio_std': float(np.std(rm)),
         'align_rate': float(np.mean(al)),
         'X_max_extent': float(np.mean(xm)), 'Y_max_extent': float(np.mean(ym)),
         'acceptance_rate': float(np.mean(acc)),
         'per_seed_ratio': [round(x,3) for x in rm],
         'per_seed_Ymax': [round(x,3) for x in ym]}
    out['N12'][f"gYX={gYX}"] = m
    print(f"  gYX={gYX:>4}: X_ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f} "
          f"align={m['align_rate']*100:.0f}% Xmax={m['X_max_extent']:.2f} "
          f"Ymax={m['Y_max_extent']:.3f} acc={m['acceptance_rate']:.3f}", flush=True)
    print(f"           seeds ratio={m['per_seed_ratio']} Ymax={m['per_seed_Ymax']}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'N': N, 'D': D, 'seeds': SEEDS,
               'gYX_list': GYX_LIST, 'n_therm': N_THERM,
               'source': 'sgoed_core_v7.py, full recompute, N=12'}
with open('AUDIT_v7_N12_robustness_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_N12_robustness_results.json")
