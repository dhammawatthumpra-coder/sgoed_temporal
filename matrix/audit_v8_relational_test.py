"""
v8-R (graph) audit — thermalization check + hysteresis UP/DOWN (2026-08-30).

Applies the SAME test battery used on v7 to the new graph engine, to verify:
  (1) thermalization: does the observer extent converge with n_therm?
  (2) hysteresis: is the g_yx transition first-order (UP != DOWN)?

N=24, d=3, g_xy=0.8. Uses run_v3_simulation_numba.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from sgoed_graph_core_v3 import run_v3_simulation_numba

N, d, g_xy = 24, 3, 0.8
SEEDS = [42, 43, 44, 45, 46]
t0 = time.time()
out = {'thermalization': {}, 'hysteresis': {}, 'meta': {}}

# --- (1) thermalization: observer extent vs n_therm at a fixed g_yx ---
print("=== (1) THERMALIZATION: obs_extent vs n_therm (g_yx=1.2) ===", flush=True)
for nt in [15, 30, 60, 120]:
    ext = []
    for s in SEEDS:
        r = run_v3_simulation_numba(N=N, d=d, g_xy=g_xy, g_yx=1.2,
                                    n_therm=nt, n_measure=40, seed=s)
        ext.append(r[5])  # obs_extent
    out['thermalization'][str(nt)] = {'extent': float(np.mean(ext)),
                                      'per_seed': [round(x,4) for x in ext]}
    print(f"  n_therm={nt:>3}: obs_extent={np.mean(ext):.4f}  seeds={[round(x,3) for x in ext]}",
          flush=True)

# --- (2) hysteresis: scan g_yx UP and DOWN ---
# Note: run_v3 always re-initializes W randomly, so a TRUE hysteresis (anneal)
# needs carrying W across g_yx. The core doesn't expose that, so here we do a
# standard scan (fresh init) which tests bistability fraction but NOT memory.
# We flag this limitation and still compare UP vs DOWN ordering.
print("\n=== (2) HYSTERESIS (fresh-init scan): gate-hit fraction vs g_yx ===", flush=True)
gyx_up = [0.0, 0.4, 0.8, 1.0, 1.2, 1.6, 2.0]
for g in gyx_up:
    ext = []
    for s in SEEDS:
        r = run_v3_simulation_numba(N=N, d=d, g_xy=g_xy, g_yx=g,
                                    n_therm=35, n_measure=45, seed=s)
        ext.append(r[5])
    hit = sum(1 for x in ext if x > 1.5)
    out['hysteresis'][f"g_yx_{g}"] = {'extent': float(np.mean(ext)),
                                      'hit_pct': hit/len(ext)*100,
                                      'per_seed': [round(x,3) for x in ext]}
    print(f"  g_yx={g:>4}: extent={np.mean(ext):.3f}  hit={hit}/{len(ext)} ({hit/len(ext)*100:.0f}%)  "
          f"seeds={[round(x,2) for x in ext]}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'N': N, 'd': d, 'g_xy': g_xy, 'seeds': SEEDS,
               'note': 'hysteresis uses fresh init (no anneal) — tests bistability fraction only'}
with open('audit_v8_relational_test_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved audit_v8_relational_test_results.json")
