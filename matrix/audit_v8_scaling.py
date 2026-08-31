"""
Scaling Audit for SGOED-Relational Engine (v8-R)
Tests Temporal Emergence & Execution Speed across N = 8, 16, 32, 64.
"""

import time
import json
import numpy as np
from sgoed_graph_core import run_relational_simulation


def run_scaling_audit():
    print("==========================================================")
    print(" SGOED-Relational v8-R: Multi-Scale Temporal Emergence Audit ")
    print("==========================================================")
    
    n_sizes = [8, 16, 32, 64]
    d_observer = 3
    seeds = [42, 43, 44, 45, 46]
    results = {}
    
    for n in n_sizes:
        print(f"\n>>> Running for N = {n}, d = {d_observer} across {len(seeds)} seeds...")
        t0 = time.time()
        seed_r = []
        seed_align = []
        seed_deg = []
        
        for seed in seeds:
            res = run_relational_simulation(
                N=n,
                d=d_observer,
                g_xy=0.8,
                g_yx=0.0,
                n_therm=25,
                n_measure=35,
                seed=seed,
            )
            seed_r.append(res["mean_r_causal"])
            seed_align.append(res["alignment_rate"])
            seed_deg.append(res["mean_degree"])
            
        elapsed = time.time() - t0
        mean_r = float(np.mean(seed_r))
        std_r = float(np.std(seed_r))
        mean_align = float(np.mean(seed_align))
        mean_deg = float(np.mean(seed_deg))
        
        results[f"N_{n}"] = {
            "N": n,
            "d": d_observer,
            "mean_r_causal": mean_r,
            "std_r_causal": std_r,
            "mean_alignment": mean_align,
            "mean_degree": mean_deg,
            "elapsed_seconds": elapsed,
            "time_per_seed": elapsed / len(seeds),
        }
        
        print(
            f"Result N={n:2d}: Mean R_causal = {mean_r:.4f} +/- {std_r:.4f} | "
            f"Alignment = {mean_align*100:5.1f}% | Time = {elapsed:.2f}s ({elapsed/len(seeds):.2f}s/seed)"
        )

    # Save summary
    out_file = r"F:\_Ai\sgoed\sgoed\matrix\audit_v8_scaling_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[Done] Saved scaling audit results to: {out_file}")


if __name__ == "__main__":
    run_scaling_audit()
