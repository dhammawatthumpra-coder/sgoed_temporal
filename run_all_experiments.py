"""
SGOED v5: Master Experiment Runner
Runs Phase Diagram, FSS, N=8 Tuning, and Statistical Tests.
Saves all results to data/sgoed_v5_results.json
"""
import sys
import os
import json
import time
import numpy as np
from scipy import stats

# Add current directory to path to import core
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))
from sgoed_core import run_simulation

# Global Constants
D = 6
SEEDS = [42, 43, 44, 45, 46]
DATA_DIR = "data"

def run_config(N, d, gXY, label=""):
    """Runs a configuration across all seeds and returns summary stats."""
    ratios = []
    alignments = 0
    entropies = []
    
    for seed in SEEDS:
        res = run_simulation(N, D, d, gXY, seed)
        ratios.append(res['ratio'])
        entropies.append(res['entropy_norm'])
        if res['alignment']: alignments += 1
        
    mean_r = np.mean(ratios)
    std_r = np.std(ratios)
    align_rate = alignments / len(SEEDS)
    
    print(f"  {label}: ratio={mean_r:.3f} ± {std_r:.3f}, align={align_rate*100:.0f}%")
    
    return {
        'mean': float(mean_r),
        'std': float(std_r),
        'cv': float(std_r / mean_r * 100) if mean_r > 0 else 0.0,
        'align_rate': float(align_rate),
        'ratios': [float(r) for r in ratios]
    }

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    results = {
        'phase_diagram': {},
        'fss_fixed': {},
        'n8_tuning': {},
        'stats_paired_ttest': {}
    }
    
    print("="*80)
    print("🚀 SGOED v5: RUNNING ALL EXPERIMENTS")
    print("="*80)
    
    # 1. Phase Diagram (d=2,3,4,5 | N=6, g=0.8)
    print("\n[1/4] Phase Diagram by Observer Dimension (N=6, g=0.8)")
    for d in [2, 3, 4, 5]:
        results['phase_diagram'][str(d)] = run_config(6, d, 0.8, f"d={d}")
        
    # 2. Finite-Size Scaling Fixed g (N=4,5,6,7,8 | d=3, g=0.8)
    print("\n[2/4] Finite-Size Scaling with Fixed g=0.8 (d=3)")
    for N in [4, 5, 6, 7, 8]:
        results['fss_fixed'][str(N)] = run_config(N, 3, 0.8, f"N={N}")
        
    # 3. N=8 Parameter Tuning (g=0.8, 1.05, 1.10, 1.15 | N=8, d=3)
    print("\n[3/4] N=8 Parameter Tuning (d=3)")
    for g in [0.80, 1.05, 1.10, 1.15]:
        results['n8_tuning'][str(g)] = run_config(8, 3, g, f"g={g}")
        
    # 4. Statistical Significance (Paired t-test d=3 vs d=4 at N=6, g=0.8)
    print("\n[4/4] Statistical Significance (Paired t-test)")
    r3 = results['phase_diagram']['3']['ratios']
    r4 = results['phase_diagram']['4']['ratios']
    t_stat, p_value = stats.ttest_rel(r3, r4)
    
    results['stats_paired_ttest'] = {
        't_stat': float(t_stat),
        'p_value': float(p_value),
        'mean_diff': float(np.mean(r4) - np.mean(r3)),
        'conclusion': "No significant difference (p > 0.05)" if p_value > 0.05 else "Significant difference (p < 0.05)"
    }
    print(f"  t-stat = {t_stat:.3f}, p-value = {p_value:.3f}")
    print(f"  Conclusion: {results['stats_paired_ttest']['conclusion']}")
    
    # Save to JSON
    out_path = os.path.join(DATA_DIR, "sgoed_v5_results.json")
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "="*80)
    print(f"✅ ALL EXPERIMENTS COMPLETE. Results saved to {out_path}")
    print("="*80)

if __name__ == "__main__":
    main()
