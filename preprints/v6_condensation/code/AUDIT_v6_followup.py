"""
Follow-up analyses on v6 (2026-08-30). Two tasks requested by the author:

  (1) Dimensional dilution — increase seeds from 5 to 30 to test whether the
      weak downward trend of the mean ratio with observer dimension d is a
      genuine "dimensional dilution" or statistical noise.

  (2) Gate transition — fine scan of g_XY in [0.80, 1.05] at N=8, d=3 to
      determine whether the entry into saturation is a smooth crossover or a
      sharp transition.

Uses ONLY code/sgoed_core_v6.py (the corrected sampler). Does not read or
trust manuscript_v6.tex or any prior summary. Saves fresh results to
AUDIT_v6_followup_results.json.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core_v6 import run_simulation
import numpy as np

D = 6
t0 = time.time()
out = {'dilution': {}, 'gate_scan': {}, 'meta': {}}

# ---------------------------------------------------------------------------
# (1) Dimensional dilution: d = 2,3,4,5 at N=6, g=0.8, 30 fresh seeds
# ---------------------------------------------------------------------------
SEEDS30 = list(range(100, 130))  # 30 fresh seeds, disjoint from baseline 42-46
print("=== (1) DILUTION: d=2..5, N=6, g=0.8, 30 seeds ===", flush=True)
for d in [2, 3, 4, 5]:
    ratios = []
    for s in SEEDS30:
        r = run_simulation(6, D, d, 0.8, s)
        ratios.append(r['ratio_mean'])
    ratios = np.asarray(ratios)
    out['dilution'][str(d)] = {
        'mean': float(ratios.mean()), 'std': float(ratios.std()),
        'cv': float(ratios.std() / ratios.mean() * 100),
        'n': len(ratios), 'ratios': ratios.tolist(),
    }
    print(f"  d={d} mean={ratios.mean():.3f} std={ratios.std():.3f} "
          f"cv={ratios.std()/ratios.mean()*100:.1f}% n={len(ratios)}", flush=True)

# Trend test: Spearman rank correlation between d and the mean ratio (or a
# linear slope). Also report per-d means for a monotonicity check.
from scipy import stats as spstats
ds = np.array([2, 3, 4, 5], dtype=float)
means = np.array([out['dilution'][str(d)]['mean'] for d in [2, 3, 4, 5]])
rho, p_rho = spstats.spearmanr(ds, means)
# Linear regression slope of per-seed ratio vs d
all_d = np.repeat(ds, 30)
all_r = np.concatenate([out['dilution'][str(d)]['ratios'] for d in [2, 3, 4, 5]])
slope, intercept, r_value, p_slope, std_err = spstats.linregress(all_d, all_r)
out['dilution']['trend'] = {
    'spearman_rho': float(rho), 'spearman_p': float(p_rho),
    'linreg_slope': float(slope), 'linreg_p': float(p_slope),
    'linreg_r2': float(r_value ** 2),
    'per_d_means': {str(d): float(m) for d, m in zip([2, 3, 4, 5], means)},
}
print(f"  trend: spearman rho={rho:.3f} p={p_rho:.4f} | "
      f"linreg slope={slope:.3f}/d p={p_slope:.4f} R2={r_value**2:.3f}", flush=True)

# Paired t-test d=3 vs d=4 with n=30
t34, p34 = spstats.ttest_rel(out['dilution']['3']['ratios'],
                             out['dilution']['4']['ratios'])
out['dilution']['paired_d3_d4'] = {'t': float(t34), 'p': float(p34), 'n': 30}
print(f"  paired d=3 vs d=4 (n=30): t={t34:.4f} p={p34:.4f}", flush=True)

# ---------------------------------------------------------------------------
# (2) Gate transition: fine scan g_XY in [0.80, 1.05], N=8, d=3, 5 seeds
# ---------------------------------------------------------------------------
GS = [round(0.80 + 0.025 * k, 3) for k in range(11)]  # 0.800 .. 1.050
SEEDS5 = [42, 43, 44, 45, 46]
print("\n=== (2) GATE SCAN: g=0.80..1.05 step 0.025, N=8, d=3 ===", flush=True)
for g in GS:
    ratios = []
    for s in SEEDS5:
        r = run_simulation(8, D, 3, g, s)
        ratios.append(r['ratio_mean'])
    ratios = np.asarray(ratios)
    out['gate_scan'][f"{g:.3f}"] = {
        'mean': float(ratios.mean()), 'std': float(ratios.std()),
        'cv': float(ratios.std() / ratios.mean() * 100),
        'ratios': ratios.tolist(),
    }
    print(f"  g={g:.3f} mean={ratios.mean():.3f} std={ratios.std():.3f} "
          f"cv={ratios.std()/ratios.mean()*100:.1f}%", flush=True)

elapsed = time.time() - t0
out['meta'] = {
    'elapsed_sec': elapsed, 'D': D,
    'dilution_seeds': SEEDS30, 'gate_seeds': SEEDS5, 'gate_g': GS,
    'source': 'code/sgoed_core_v6.py run_simulation, trajectory mean',
}
with open('AUDIT_v6_followup_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v6_followup_results.json")
