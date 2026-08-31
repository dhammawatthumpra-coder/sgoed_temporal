"""
Independent re-verification script — Claude audit, 2026-08-30.
Uses ONLY code/sgoed_core.py (already verified byte-identical logic
across run_experiments.py and code/sgoed_core.py). Does not read or
trust manuscript_v5.tex, data/sgoed_v5_results.json, or any prior
agent's summary. Every number below is freshly computed and printed
with full seed-level provenance.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core import run_simulation
import numpy as np

SEEDS = [42, 43, 44, 45, 46]
D = 6
t_start = time.time()
out = {'phase_diagram': {}, 'fss': {}, 'n8_tuning': {}}

def summarize(rows):
    ratios = [r['ratio'] for r in rows]
    aligns = [r['alignment'] for r in rows]
    m, sd = float(np.mean(ratios)), float(np.std(ratios))
    return {'ratios': ratios, 'aligns': aligns, 'mean': m, 'std': sd,
            'cv': (sd/m*100) if m else 0.0, 'align_rate': sum(aligns)/len(aligns)}

print("=== PHASE DIAGRAM (N=6, D=6, g_XY=0.8) ===", flush=True)
for dd in [2, 3, 4, 5]:
    rows = []
    for s in SEEDS:
        r = run_simulation(6, D, dd, 0.8, s)
        rows.append(r)
        print(f"  d={dd} seed={s} ratio={r['ratio']:.4f} align={r['alignment']}", flush=True)
    summ = summarize(rows)
    out['phase_diagram'][dd] = summ
    print(f"  -> d={dd} mean={summ['mean']:.3f} std={summ['std']:.3f} "
          f"cv={summ['cv']:.1f}% align={summ['align_rate']*100:.0f}%", flush=True)

print("\n=== FINITE-SIZE SCALING (d=3, g_XY=0.8) ===", flush=True)
for NN in [4, 5, 6, 7, 8]:
    rows = []
    for s in SEEDS:
        r = run_simulation(NN, D, 3, 0.8, s)
        rows.append(r)
        print(f"  N={NN} seed={s} ratio={r['ratio']:.4f} align={r['alignment']}", flush=True)
    summ = summarize(rows)
    out['fss'][NN] = summ
    print(f"  -> N={NN} mean={summ['mean']:.3f} std={summ['std']:.3f} "
          f"cv={summ['cv']:.1f}% align={summ['align_rate']*100:.0f}%", flush=True)

print("\n=== N=8 TUNING (d=3) ===", flush=True)
for g in [0.80, 1.05, 1.10, 1.15]:
    rows = []
    for s in SEEDS:
        r = run_simulation(8, D, 3, g, s)
        rows.append(r)
        print(f"  g={g} seed={s} ratio={r['ratio']:.4f} align={r['alignment']}", flush=True)
    summ = summarize(rows)
    out['n8_tuning'][g] = summ
    print(f"  -> g={g} mean={summ['mean']:.3f} std={summ['std']:.3f} "
          f"cv={summ['cv']:.1f}% align={summ['align_rate']*100:.0f}%", flush=True)

from scipy import stats as spstats
r3 = out['phase_diagram'][3]['ratios']
r4 = out['phase_diagram'][4]['ratios']
t_stat, p_val = spstats.ttest_rel(r3, r4)
out['paired_ttest_d3_d4'] = {'t': float(t_stat), 'p': float(p_val),
                              'ratios_d3': r3, 'ratios_d4': r4}
print(f"\n=== PAIRED T-TEST d=3 vs d=4 (N=6, g=0.8) ===")
print(f"  t={t_stat:.4f}  p={p_val:.4f}")

elapsed = time.time() - t_start
out['_meta'] = {'elapsed_sec': elapsed, 'seeds': SEEDS, 'D': D,
                 'source': 'code/sgoed_core.py run_simulation, defaults '
                           'n_therm=20 n_meas=30 eps=0.25 max_extent=10.0'}
with open('AUDIT_verified_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_verified_results.json")
