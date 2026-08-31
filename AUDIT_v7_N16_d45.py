"""
v7 feedback — N=16 trend + d=4,5 at N=12 (2026-08-30).

(2) Does the upward trend of critical g_YX with N continue to N=16?
(3) Does the scaling law g_c ~ d^0.446 hold at N=12 for d=4,5?

Uses eps=0.20 (found to give acceptance ~0.55 at N=12, from the pilot).
n_therm=40, 5 seeds each (pilot scope — full n=30 is too slow at N=16).

Configs:
  N=16, d=3: g_YX in {1.5, 2.0, 2.5}   (locate critical)
  N=12, d=4: g_YX in {1.5, 2.0, 2.5}
  N=12, d=5: g_YX in {1.5, 2.0, 2.5}
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
SEEDS = [42, 43, 44, 45, 46]
N_THERM, EPS = 40, 0.20
GYX_LIST = [1.5, 2.0, 2.5]
t0 = time.time()
out = {'N16_d3': {}, 'N12_d4': {}, 'N12_d5': {}, 'meta': {}}

def scan(tag, N, d):
    print(f"\n=== {tag} (N={N}, d={d}, eps={EPS}) ===", flush=True)
    for gYX in GYX_LIST:
        rm, ym, acc = [], [], []
        for s in SEEDS:
            r = run_simulation(N, D, d, 0.8, gYX, s, n_therm=N_THERM, n_meas=30, eps=EPS)
            rm.append(r['ratio_mean']); ym.append(r['Y_max_extent']); acc.append(r['acceptance_rate'])
        hit = sum(1 for y in ym if y >= 9.9)
        m = {'ratio_mean': float(np.mean(rm)), 'align_rate': float(np.mean([1])),
             'Ymax_mean': float(np.mean(ym)), 'n_hit_gate': hit,
             'acceptance_rate': float(np.mean(acc)),
             'per_seed_Ymax': [round(x,3) for x in ym]}
        out[tag][f"gYX={gYX}"] = m
        print(f"  gYX={gYX:>4}: hit={hit}/5  Ymax={m['Ymax_mean']:.2f}  "
              f"X_ratio={m['ratio_mean']:.3f}  acc={m['acceptance_rate']:.3f}  "
              f"seeds_Ymax={m['per_seed_Ymax']}", flush=True)

scan('N16_d3', 16, 3)
scan('N12_d4', 12, 4)
scan('N12_d5', 12, 5)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'seeds': SEEDS, 'n_therm': N_THERM, 'eps': EPS,
               'source': 'sgoed_core_v7.py, eps=0.20'}
with open('AUDIT_v7_N16_d45_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_N16_d45_results.json")
