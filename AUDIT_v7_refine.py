"""
v7 feedback — n=30 refinement at key points (2026-08-30).

(2) Pinpoints critical g_YX with credible sample at the key configs:
    - N=12, d=5: g_YX in {1.8, 2.0, 2.2, 2.4}  (n=30)
    - N=16, d=3: g_YX in {1.8, 2.0}              (n=15, N=16 is slow ~76s/run)

eps=0.20 (from 12.1), n_therm=40.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v7 import run_simulation
import numpy as np

D = 6
N_THERM, EPS = 40, 0.20
t0 = time.time()
out = {'N12_d5': {}, 'N16_d3': {}, 'meta': {}}

def scan(tag, N, d, gYX_list, seeds):
    print(f"\n=== {tag} (N={N}, d={d}, n={len(seeds)}, eps={EPS}) ===", flush=True)
    for gYX in gYX_list:
        ym, rm, acc = [], [], []
        for s in seeds:
            r = run_simulation(N, D, d, 0.8, gYX, s, n_therm=N_THERM, n_meas=30, eps=EPS)
            ym.append(r['Y_max_extent']); rm.append(r['ratio_mean']); acc.append(r['acceptance_rate'])
        hit = sum(1 for y in ym if y >= 9.9)
        m = {'Ymax_mean': float(np.mean(ym)), 'n_hit_gate': int(hit),
             'frac_hit_gate': float(hit/len(ym)),
             'ratio_mean': float(np.mean(rm)), 'ratio_std': float(np.std(rm)),
             'acceptance_rate': float(np.mean(acc)),
             'Ymax_distribution': [round(x,3) for x in ym]}
        out[tag][f"gYX={gYX}"] = m
        print(f"  gYX={gYX:>4}: hit={hit:>2}/{len(seeds)} ({hit/len(seeds)*100:.0f}%)  "
              f"X_ratio={m['ratio_mean']:.3f}±{m['ratio_std']:.3f}  acc={m['acceptance_rate']:.3f}",
              flush=True)

# N=12, d=5: n=30
scan('N12_d5', 12, 5, [1.8, 2.0, 2.2, 2.4], list(range(100, 130)))
# N=16, d=3: n=15 (compromise for speed)
scan('N16_d3', 16, 3, [1.8, 2.0], list(range(100, 115)))

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'n_therm': N_THERM, 'eps': EPS,
               'source': 'sgoed_core_v7.py, eps=0.20'}
with open('AUDIT_v7_refine_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_refine_results.json")
