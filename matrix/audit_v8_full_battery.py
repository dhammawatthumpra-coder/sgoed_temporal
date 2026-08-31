"""
v8-R (graph) full battery — hysteresis + X robustness + d/N dependence (2026-08-30).

Runs the SAME test battery used on v7, on the graph engine (v5 with extent gate):
  (1) TRUE hysteresis (anneal carry W, extent gate at 16)
  (2) X robustness: R_causal / alignment / obs_extent vs g_yx up to 5.0
  (3) d-dependence: critical g_yx at d = 2,3,4,5
  (4) N-dependence: critical g_yx at N = 16,24,48

Saves everything to audit_v8_full_battery_results.json.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from sgoed_graph_core_v5 import run_v5

g_xy = 0.8
EXT_MAX = 16.0
LAMBDA_EXT = 10.0
N_THERM, N_MEAS = 240, 40
t0 = time.time()
out = {'hysteresis': {}, 'x_robustness': {}, 'd_dependence': {}, 'N_dependence': {}, 'meta': {}}

def fresh(N, d, g_yx, seeds):
    """Fresh-init runs (X robustness: independent samples, no memory)."""
    r = []; a = []; e = []
    for s in seeds:
        res = run_v5(N=N, d=d, g_xy=g_xy, g_yx=g_yx, n_therm=N_THERM, n_measure=N_MEAS,
                     seed=s, extent_max_obs=EXT_MAX, lambda_extent=LAMBDA_EXT)
        r.append(res[0]); a.append(res[2]); e.append(res[5])
    return float(np.mean(r)), float(np.mean(a)), float(np.mean(e))

def anneal(N, d, gseq, seed):
    W = None; recs = []
    for g in gseq:
        res = run_v5(N=N, d=d, g_xy=g_xy, g_yx=g, n_therm=N_THERM, n_measure=N_MEAS,
                     seed=seed, W_init=W, extent_max_obs=EXT_MAX, lambda_extent=LAMBDA_EXT)
        W = res[6]; recs.append((g, res[5]))
    return recs

# (1) hysteresis
print("=== (1) TRUE HYSTERESIS (anneal, extent gate 16) ===", flush=True)
UP = [0.0, 0.4, 0.8, 1.0, 1.2, 1.6, 2.0]
DOWN = list(reversed(UP))
for direction, gseq in [('up', UP), ('down', DOWN)]:
    print(f"  --- {direction.upper()} ---", flush=True)
    for g, ext in anneal(24, 3, gseq, 42):
        out['hysteresis'][f"{direction}_{g}"] = {'g_yx': g, 'obs_extent': float(ext)}
        print(f"    g_yx={g:>4}: extent={ext:.4f}", flush=True)

# (2) X robustness: fresh init, g_yx up to 5
print("\n=== (2) X ROBUSTNESS (fresh init, N=24 d=3) ===", flush=True)
for g in [0.0, 0.8, 1.2, 2.0, 3.0, 5.0]:
    r, a, e = fresh(24, 3, g, [42, 43, 44, 45, 46])
    out['x_robustness'][f"g_yx_{g}"] = {'R_causal': r, 'alignment': a, 'obs_extent': e}
    print(f"  g_yx={g:>4}: R_causal={r:.4f}  align={a:.3f}  obs_extent={e:.3f}", flush=True)

# (3) d-dependence: critical g_yx (fresh init, 5 seeds) at d=2,3,4,5
print("\n=== (3) d-DEPENDENCE (N=24) ===", flush=True)
for d in [2, 3, 4, 5]:
    row = {}
    for g in [0.4, 0.8, 1.2, 1.6, 2.0]:
        r, a, e = fresh(24, d, g, [42, 43, 44, 45, 46])
        row[f"g_yx_{g}"] = {'obs_extent': e}
        print(f"  d={d} g_yx={g:>4}: extent={e:.3f}", flush=True)
    out['d_dependence'][f"d_{d}"] = row

# (4) N-dependence: critical g_yx at N=16,24,48 (d=3)
print("\n=== (4) N-DEPENDENCE (d=3) ===", flush=True)
for N in [16, 24, 48]:
    row = {}
    for g in [0.4, 0.8, 1.2, 1.6, 2.0]:
        r, a, e = fresh(N, 3, g, [42, 43, 44, 45, 46])
        row[f"g_yx_{g}"] = {'obs_extent': e}
        print(f"  N={N:>3} g_yx={g:>4}: extent={e:.3f}", flush=True)
    out['N_dependence'][f"N_{N}"] = row

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'g_xy': g_xy, 'extent_max_obs': EXT_MAX,
               'n_therm': N_THERM, 'seeds': [42,43,44,45,46]}
with open('audit_v8_full_battery_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved audit_v8_full_battery_results.json")
