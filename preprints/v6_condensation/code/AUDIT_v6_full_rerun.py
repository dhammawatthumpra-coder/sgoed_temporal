"""
Independent re-verification of the v6 correctness-first sampler — 2026-08-30.
Companion to AUDIT_full_rerun.py (which audits v5 sgoed_core.py).

Uses ONLY code/sgoed_core_v6.py. Does not read or trust manuscript_v5.tex,
AUDIT_verified_results.json, or any prior agent summary. Every number is
freshly computed from run_simulation(...) and printed with seed-level provenance.

NOTE ON ESTIMANDS (v5 vs v6):
  - v5 returns `ratio` / `alignment` from the FINAL configuration only
    (a single snapshot after n_therm + n_meas sweeps).
  - v6 returns `ratio_mean` / `alignment_rate` averaged over the measurement
    trajectory (n_meas=30 recorded points). These are DIFFERENT estimators and
    are deliberately kept distinct here so the two audits can be compared.

Key mapping used below (v6 -> comparable column names):
  ratio_mean    -> ratio   (trajectory mean, not final snapshot)
  ratio_std     -> std per seed (within-run trajectory std; NOT across seeds)
  alignment_rate-> alignment (fraction of trajectory points aligned, 0..1)

The across-seed summary (mean / std / cv / align_rate over 5 seeds) is computed
identically to the v5 audit for direct comparison.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sgoed_core_v6 import run_simulation
import numpy as np

SEEDS = [42, 43, 44, 45, 46]
D = 6
t_start = time.time()
out = {'phase_diagram': {}, 'fss': {}, 'n8_tuning': {}, 'meta': {}}

def summarize(rows):
    """rows: list of per-seed dicts from run_simulation(record_trajectory=True)."""
    ratios = [r['ratio_mean'] for r in rows]
    aligns = [r['alignment_rate'] for r in rows]
    m, sd = float(np.mean(ratios)), float(np.std(ratios))
    return {
        'ratios': ratios,           # per-seed trajectory means
        'aligns': aligns,           # per-seed alignment fractions
        'mean': m,                  # across-seed mean of ratio_mean
        'std': sd,                  # across-seed std of ratio_mean
        'cv': (sd / m * 100) if m else 0.0,
        'align_rate': float(np.mean(aligns)),  # across-seed mean alignment
        # extra diagnostics v6 provides (kept for provenance)
        'wall_fraction': [float(r['wall_fraction']) for r in rows],
        'acceptance_rate': [float(r['acceptance_rate']) for r in rows],
        'tau_int': [float(r['tau_int']) for r in rows],
        'n_eff': [float(r['n_eff']) for r in rows],
    }

def run_grid(tag, configs):
    print(f"=== {tag} ===", flush=True)
    for key, (N, d, g) in configs.items():
        rows = []
        for s in SEEDS:
            r = run_simulation(N, D, d, g, s)
            rows.append(r)
            print(f"  {key} seed={s} ratio_mean={r['ratio_mean']:.4f} "
                  f"align={r['alignment_rate']:.3f}", flush=True)
        summ = summarize(rows)
        out[tag][key] = summ
        print(f"  -> {key} mean={summ['mean']:.3f} std={summ['std']:.3f} "
              f"cv={summ['cv']:.1f}% align={summ['align_rate']*100:.1f}%", flush=True)

# Phase diagram (N=6, D=6, g=0.8), d = 2,3,4,5
run_grid('phase_diagram', {str(d): (6, d, 0.8) for d in [2, 3, 4, 5]})

# Finite-size scaling (d=3, g=0.8), N = 4,5,6,7,8
print("", flush=True)
run_grid('fss', {str(N): (N, 3, 0.8) for N in [4, 5, 6, 7, 8]})

# N=8 tuning (d=3), g = 0.80, 1.05, 1.10, 1.15
print("", flush=True)
run_grid('n8_tuning', {f"{g:.2f}": (8, 3, g) for g in [0.80, 1.05, 1.10, 1.15]})

# Paired t-test d=3 vs d=4 (N=6, g=0.8), using per-seed trajectory means
from scipy import stats as spstats
r3 = out['phase_diagram']['3']['ratios']
r4 = out['phase_diagram']['4']['ratios']
t_stat, p_val = spstats.ttest_rel(r3, r4)
out['paired_ttest_d3_d4'] = {'t': float(t_stat), 'p': float(p_val),
                              'ratios_d3': r3, 'ratios_d4': r4}
print(f"\n=== PAIRED T-TEST d=3 vs d=4 (N=6, g=0.8) ===")
print(f"  t={t_stat:.4f}  p={p_val:.4f}")

elapsed = time.time() - t_start
out['meta'] = {'elapsed_sec': elapsed, 'seeds': SEEDS, 'D': D,
               'source': 'code/sgoed_core_v6.py run_simulation, defaults '
                         'n_therm=20 n_meas=30 eps=0.25 max_extent=10.0',
               'estimand': 'trajectory mean over measurement window (n_meas=30)'}
with open('AUDIT_v6_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v6_results.json")
