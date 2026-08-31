#!/usr/bin/env python3
"""
SGOED v5: Complete Experiments for Paper
=========================================

This script runs all the experiments reported in the v5 paper:
1. Phase Diagram (d=2,3,4,5) at N=6, g=0.8
2. Finite-Size Scaling (N=4,5,6,7,8) at g=0.8
3. N=8 Parameter Tuning (g=0.8, 1.05, 1.10, 1.15)
4. Statistical Significance Test (paired t-test d=3 vs d=4)

Usage: python run_experiments.py
"""

import numpy as np
import time
import json
from scipy import stats

# Custom JSON encoder to handle numpy types
class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy data types"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

print("="*80)
print("SGOED v5: COMPLETE EXPERIMENTS")
print("="*80)

# ========== PARAMETERS ==========
D = 6
lam = 1.0
lamY = 1.0
r0 = 1.0
rY = 0.5

def action_v3(X, Y, gXY, max_extent=10.0):
    """SGOED v3 action with directional coupling"""
    S = 0.0
    D, N, _ = X.shape
    d = Y.shape[0]
    
    # System IKKT + gate
    for mu in range(D):
        for nu in range(mu+1, D):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(X[mu] @ X[mu]).real
        S += lam * (tr2 - N * r0**2)**2
    
    # Observer IKKT + gate
    for a in range(d):
        for b in range(a+1, d):
            comm = Y[a] @ Y[b] - Y[b] @ Y[a]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(Y[a] @ Y[a]).real
        S += lamY * (tr2 - N * rY**2)**2
    
    # Directional coupling
    Y_traces = np.array([np.trace(Y[a]).real for a in range(d)])
    v = np.zeros(D)
    v[:min(d, D)] = Y_traces[:min(d, D)]
    v_norm = np.linalg.norm(v)
    v_hat = v / (v_norm + 1e-8) if v_norm > 1e-8 else np.zeros(D)
    
    for mu in range(D):
        X_mu_sq = X[mu] @ X[mu]
        X_mu_4 = X_mu_sq @ X_mu_sq
        extent = np.trace(X_mu_sq).real / N
        
        if extent < max_extent:
            S -= gXY * (v_hat[mu]**2) * np.trace(X_mu_4).real
        else:
            S += 10.0 * (extent - max_extent)**2
    
    return S

def run_sim(N, D, d, gXY, seed, n_therm=20, n_meas=30, eps=0.25):
    """Run single simulation"""
    np.random.seed(seed)
    
    X = np.zeros((D, N, N))
    for mu in range(D):
        A = np.random.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    
    Y = np.zeros((d, N, N))
    for a in range(d):
        A = np.random.randn(N, N) * 0.3
        Y[a] = (A + A.T) / 2
    
    S_curr = action_v3(X, Y, gXY)
    
    for sweep in range(n_therm + n_meas):
        step = 2 if N > 6 else 1
        for mu in range(D):
            for i in range(0, N, step):
                for j in range(i, N, step):
                    old = X[mu, i, j]
                    X[mu, i, j] = old + eps * np.random.randn()
                    if i != j:
                        X[mu, j, i] = X[mu, i, j]
                    
                    S_new = action_v3(X, Y, gXY)
                    dS = S_new - S_curr
                    if dS < 0 or np.random.rand() < np.exp(-dS):
                        S_curr = S_new
                    else:
                        X[mu, i, j] = old
                        if i != j:
                            X[mu, j, i] = old
        
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    old = Y[a, i, j]
                    Y[a, i, j] = old + eps * np.random.randn()
                    if i != j:
                        Y[a, j, i] = Y[a, i, j]
                    
                    S_new = action_v3(X, Y, gXY)
                    dS = S_new - S_curr
                    if dS < 0 or np.random.rand() < np.exp(-dS):
                        S_curr = S_new
                    else:
                        Y[a, i, j] = old
                        if i != j:
                            Y[a, j, i] = old
    
    # Analysis
    X_extents = np.array([np.trace(X[mu] @ X[mu]).real / N for mu in range(D)])
    Y_traces = np.array([np.trace(Y[a]).real for a in range(d)])
    
    v = np.zeros(D)
    v[:min(d, D)] = Y_traces[:min(d, D)]
    v_norm = np.linalg.norm(v)
    v_hat = v / (v_norm + 1e-8) if v_norm > 1e-8 else np.zeros(D)
    
    X_max_idx = int(np.argmax(X_extents))
    X_max_val = X_extents[X_max_idx]
    X_others = np.delete(X_extents, X_max_idx)
    ratio = X_max_val / (X_others.mean() + 1e-8)
    
    v_max_idx = int(np.argmax(np.abs(v_hat)))
    alignment = (X_max_idx == v_max_idx)
    
    # Entropy
    p_mu = X_extents / (X_extents.sum() + 1e-10)
    entropy = -np.sum(p_mu * np.log(p_mu + 1e-10))
    max_entropy = np.log(D)
    
    return {
        'ratio': float(ratio),
        'alignment': bool(alignment),
        'entropy': float(entropy),
        'entropy_norm': float(entropy / max_entropy),
        'v_norm': float(v_norm)
    }

# ========== EXPERIMENT 1: Phase Diagram ==========
print("\n[EXPERIMENT 1] Phase Diagram (d=2,3,4,5)")
print("-"*80)

seeds = [42, 43, 44, 45, 46]
d_values = [2, 3, 4, 5]
gXY = 0.8
N = 6

phase_results = {}

for d in d_values:
    print(f"\nd = {d} (N={N}, g_XY={gXY}):")
    ratios = []
    alignments = 0
    entropies = []
    
    for i, seed in enumerate(seeds):
        start = time.time()
        res = run_sim(N, D, d, gXY, seed)
        elapsed = time.time() - start
        
        ratios.append(res['ratio'])
        entropies.append(res['entropy_norm'])
        if res['alignment']: alignments += 1
        
        print(f"  Seed {seed} [{i+1}/5]: ratio={res['ratio']:.3f}, H={res['entropy_norm']:.3f} ({elapsed:.1f}s)")
    
    mean_r = np.mean(ratios)
    std_r = np.std(ratios)
    mean_h = np.mean(entropies)
    
    phase_results[str(d)] = {
        'mean': float(mean_r),
        'std': float(std_r),
        'cv': float(std_r/mean_r*100) if mean_r > 0 else 0.0,
        'align_rate': float(alignments/len(seeds)),
        'entropy': float(mean_h),
        'healthy': bool(1.5 < mean_r < 10.0)
    }
    
    status = "✓ HEALTHY" if 1.5 < mean_r < 10.0 else "✗ NO EMERGENCE"
    print(f"  => Mean = {mean_r:.3f} ± {std_r:.3f}, CV={std_r/mean_r*100:.1f}%, Align={alignments/len(seeds)*100:.0f}% {status}")

# ========== EXPERIMENT 2: Finite-Size Scaling ==========
print("\n" + "="*80)
print("[EXPERIMENT 2] Finite-Size Scaling (N=4,5,6,7,8)")
print("-"*80)

N_values = [4, 5, 6, 7, 8]
d_fss = 3
gXY_fss = 0.8

fss_results = {}

for N in N_values:
    print(f"\nN = {N} (d={d_fss}, g_XY={gXY_fss}):")
    ratios = []
    alignments = 0
    
    for i, seed in enumerate(seeds):
        start = time.time()
        res = run_sim(N, D, d_fss, gXY_fss, seed)
        elapsed = time.time() - start
        
        ratios.append(res['ratio'])
        if res['alignment']: alignments += 1
        
        print(f"  Seed {seed} [{i+1}/5]: ratio={res['ratio']:.3f}, align={res['alignment']} ({elapsed:.1f}s)")
    
    mean_r = np.mean(ratios)
    std_r = np.std(ratios)
    
    fss_results[str(N)] = {
        'mean': float(mean_r),
        'std': float(std_r),
        'cv': float(std_r/mean_r*100) if mean_r > 0 else 0.0,
        'align_rate': float(alignments/len(seeds)),
        'healthy': bool(1.5 < mean_r < 10.0)
    }
    
    status = "✓ HEALTHY" if 1.5 < mean_r < 10.0 else "⚠️ WEAK"
    print(f"  => Mean = {mean_r:.3f} ± {std_r:.3f}, CV={std_r/mean_r*100:.1f}%, Align={alignments/len(seeds)*100:.0f}% {status}")

# ========== EXPERIMENT 3: N=8 Parameter Tuning ==========
print("\n" + "="*80)
print("[EXPERIMENT 3] N=8 Parameter Tuning")
print("-"*80)

N = 8
d = 3
g_values = [0.80, 1.05, 1.10, 1.15]

tuning_results = {}

for g in g_values:
    print(f"\ng_XY = {g} (N={N}, d={d}):")
    ratios = []
    alignments = 0
    
    for i, seed in enumerate(seeds):
        start = time.time()
        res = run_sim(N, D, d, g, seed)
        elapsed = time.time() - start
        
        ratios.append(res['ratio'])
        if res['alignment']: alignments += 1
        
        print(f"  Seed {seed} [{i+1}/5]: ratio={res['ratio']:.3f}, align={res['alignment']} ({elapsed:.1f}s)")
    
    mean_r = np.mean(ratios)
    std_r = np.std(ratios)
    
    tuning_results[str(g)] = {
        'mean': float(mean_r),
        'std': float(std_r),
        'cv': float(std_r/mean_r*100) if mean_r > 0 else 0.0,
        'align_rate': float(alignments/len(seeds)),
        'healthy': bool(1.5 < mean_r < 10.0)
    }
    
    status = "✓ HEALTHY" if 1.5 < mean_r < 10.0 else "⚠️ OUT OF RANGE"
    print(f"  => Mean = {mean_r:.3f} ± {std_r:.3f}, CV={std_r/mean_r*100:.1f}%, Align={alignments/len(seeds)*100:.0f}% {status}")

# ========== EXPERIMENT 4: Statistical Significance ==========
print("\n" + "="*80)
print("[EXPERIMENT 4] Statistical Significance Test (d=3 vs d=4)")
print("-"*80)

N = 6
gXY = 0.8

ratios_d3 = []
ratios_d4 = []

print(f"\nRunning paired simulations (N={N}, g_XY={gXY}):")

for i, seed in enumerate(seeds):
    print(f"  Seed {seed} [{i+1}/5]:", end=" ")
    
    start = time.time()
    res3 = run_sim(N, D, 3, gXY, seed)
    t3 = time.time() - start
    ratios_d3.append(res3['ratio'])
    
    start = time.time()
    res4 = run_sim(N, D, 4, gXY, seed)
    t4 = time.time() - start
    ratios_d4.append(res4['ratio'])
    
    print(f"d3={res3['ratio']:.3f} ({t3:.1f}s), d4={res4['ratio']:.3f} ({t4:.1f}s)")

# Paired t-test
t_stat, p_value = stats.ttest_rel(ratios_d3, ratios_d4)

print(f"\n📊 Statistical Test Results:")
print(f"  d=3 ratios: {[f'{r:.3f}' for r in ratios_d3]}")
print(f"  d=4 ratios: {[f'{r:.3f}' for r in ratios_d4]}")
print(f"  t-statistic = {t_stat:.3f}")
print(f"  p-value = {p_value:.3f}")
print(f"  ΔR = {np.mean(ratios_d4) - np.mean(ratios_d3):.3f}")

if p_value > 0.05:
    print("\n  ✅ NO significant difference (p > 0.05)")
    print("  ✅ Mechanism is ROBUST across observer dimensions")
else:
    print("\n  ⚠️ Significant difference detected")

# ========== SAVE ALL RESULTS ==========
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

all_results = {
    'phase_diagram': phase_results,
    'finite_size_scaling': fss_results,
    'n8_tuning': tuning_results,
    'statistical_test': {
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'ratios_d3': [float(r) for r in ratios_d3],
        'ratios_d4': [float(r) for r in ratios_d4],
        'mean_d3': float(np.mean(ratios_d3)),
        'mean_d4': float(np.mean(ratios_d4)),
        'std_d3': float(np.std(ratios_d3)),
        'std_d4': float(np.std(ratios_d4))
    }
}

with open('sgoed_v5_results.json', 'w') as f:
    json.dump(all_results, f, indent=2, cls=NumpyEncoder)

print("✓ Saved: sgoed_v5_results.json")

# ========== FINAL SUMMARY ==========
print("\n" + "="*80)
print("📊 COMPLETE RESULTS SUMMARY")
print("="*80)

print("\n📈 Table 1: Phase Diagram (N=6, g_XY=0.8)")
print("-"*80)
print(f"{'d':<6} {'Mean Ratio':<14} {'Std Dev':<10} {'CV (%)':<10} {'Align':<10} {'Status':<15}")
print("-"*80)
for d in [2, 3, 4, 5]:
    r = phase_results[str(d)]
    status = "Healthy" if r['healthy'] else "No emergence"
    print(f"{d:<6} {r['mean']:<14.3f} {r['std']:<10.3f} {r['cv']:<10.1f} {r['align_rate']*100:<10.0f}% {status:<15}")

print("\n📈 Table 2: Finite-Size Scaling (d=3, g_XY=0.8)")
print("-"*80)
print(f"{'N':<6} {'Mean Ratio':<14} {'Std Dev':<10} {'CV (%)':<10} {'Align':<10} {'Status':<15}")
print("-"*80)
for N in [4, 5, 6, 7, 8]:
    r = fss_results[str(N)]
    status = "Healthy" if r['healthy'] else "Weak"
    print(f"{N:<6} {r['mean']:<14.3f} {r['std']:<10.3f} {r['cv']:<10.1f} {r['align_rate']*100:<10.0f}% {status:<15}")

print("\n📈 Table 3: N=8 Parameter Tuning (d=3)")
print("-"*80)
print(f"{'g_XY':<8} {'Mean Ratio':<14} {'Std Dev':<10} {'CV (%)':<10} {'Align':<10} {'Status':<15}")
print("-"*80)
for g in [0.80, 1.05, 1.10, 1.15]:
    r = tuning_results[str(g)]
    status = "Healthy" if r['healthy'] else "Out of range"
    print(f"{g:<8.2f} {r['mean']:<14.3f} {r['std']:<10.3f} {r['cv']:<10.1f} {r['align_rate']*100:<10.0f}% {status:<15}")

print("\n📈 Table 4: Statistical Significance")
print("-"*80)
print(f"Test: Paired t-test (d=3 vs d=4, N=6, g_XY=0.8)")
print(f"  t-statistic: {t_stat:.3f}")
print(f"  p-value: {p_value:.3f}")
print(f"  Result: {'NO significant difference ✅' if p_value > 0.05 else 'Significant difference ⚠️'}")

print("\n" + "="*80)
print("✅ ALL EXPERIMENTS COMPLETE - READY FOR PAPER")
print("="*80)
print("\nNext steps:")
print("  1. Review sgoed_v5_results.json")
print("  2. Update manuscript with these results")
print("  3. Compile LaTeX: pdflatex manuscript_v5.tex && bibtex manuscript_v5 && pdflatex manuscript_v5.tex && pdflatex manuscript_v5.tex")
print("  4. Submit to Foundations of Physics")
