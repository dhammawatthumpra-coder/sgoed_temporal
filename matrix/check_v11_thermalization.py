"""Thermalization + baseline check for v11 ecosystem (self-written, data honesty)."""
import numpy as np
from sgoed_ecosystem_core_v11 import run_v11_ecosystem

seeds = [42, 43, 44, 45, 46]

print("=== 1. Baseline at g_inter=0.0 (is Phi_sync really ~0 noise?) ===")
for therm in [25, 100]:
    phis = []
    for s in seeds:
        r_loc, r_std, phi_s, phi_std, r_cr, aln, act = run_v11_ecosystem(
            M=3, N_k=10, d=2, g_xy=0.8, g_inter=0.0,
            n_therm=therm, n_measure=50, seed=s)
        phis.append(phi_s)
    print(f"  n_therm={therm:3d}: mean_phi={np.mean(phis):+.3f} std={np.std(phis):.3f} "
          f"per_seed={[f'{p:+.2f}' for p in phis]}")

print("=== 2. Transition point g_inter=0.1: does phi depend on n_therm? ===")
for therm in [25, 100, 200]:
    phis = []
    for s in seeds:
        r_loc, r_std, phi_s, phi_std, r_cr, aln, act = run_v11_ecosystem(
            M=3, N_k=10, d=2, g_xy=0.8, g_inter=0.1,
            n_therm=therm, n_measure=50, seed=s)
        phis.append(phi_s)
    print(f"  n_therm={therm:3d}: mean_phi={np.mean(phis):+.3f} std={np.std(phis):.3f} "
          f"per_seed={[f'{p:+.2f}' for p in phis]}")

print("=== 3. Random W baseline: phi_sync of uncorrelated universes ===")
M, N_k, d = 3, 10, 2
N_total = M * N_k
rng = np.random.default_rng(7)
for trial in range(5):
    W = rng.uniform(0.05, 0.3, (N_total, N_total))
    for i in range(N_total):
        W[i, i] = 0.0
    from sgoed_ecosystem_core_v11 import compute_ecosystem_observables
    r_loc, phi_s, r_cr, aln = compute_ecosystem_observables(W, M, N_k, d)
    print(f"  random W #{trial}: phi_sync={phi_s:+.3f} R_local={r_loc:.3f}")
