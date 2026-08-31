"""
Benchmark comparison: SGOED-Relational v1 (Python) vs v2 (Numba JIT Accelerated)
"""

import time
import json
import numpy as np
from sgoed_graph_core import run_relational_simulation as run_v1
from sgoed_graph_core_v2 import run_relational_simulation_numba as run_v2


def run_benchmark():
    print("================================================================")
    print("      SGOED-Relational Engine Benchmark: v1 vs v2 (JIT)        ")
    print("================================================================")

    # Warmup Numba JIT
    print("[Warmup] Compiling Numba JIT functions...")
    _ = run_v2(N=8, d=2, n_therm=2, n_measure=2, seed=1)
    print("[Warmup] JIT Compilation complete.\n")

    test_sizes = [16, 32, 64, 128]
    seeds = [42, 43, 44]
    
    report = {}

    for N in test_sizes:
        print(f"--- Benchmarking N = {N} (3 seeds) ---")
        
        # 1. Test v1 (Only run v1 up to N=64 to avoid extreme lag)
        if N <= 64:
            t0 = time.time()
            v1_r = []
            for s in seeds:
                res = run_v1(N=N, d=3, n_therm=20, n_measure=30, seed=s)
                v1_r.append(res["mean_r_causal"])
            t_v1 = time.time() - t0
            t_v1_seed = t_v1 / len(seeds)
        else:
            t_v1 = None
            t_v1_seed = None
            v1_r = []

        # 2. Test v2 (Numba JIT)
        t0 = time.time()
        v2_r = []
        v2_align = []
        for s in seeds:
            mean_r, std_r, align, deg, act = run_v2(
                N=N, d=3, n_therm=20, n_measure=30, seed=s
            )
            v2_r.append(mean_r)
            v2_align.append(align)
        t_v2 = time.time() - t0
        t_v2_seed = t_v2 / len(seeds)

        speedup = (t_v1_seed / t_v2_seed) if t_v1_seed is not None else "N/A"
        
        report[f"N_{N}"] = {
            "N": N,
            "v1_time_per_seed": t_v1_seed,
            "v2_time_per_seed": t_v2_seed,
            "speedup": speedup if isinstance(speedup, str) else round(speedup, 2),
            "v2_mean_r": float(np.mean(v2_r)),
            "v2_mean_align": float(np.mean(v2_align)),
        }

        if t_v1_seed is not None:
            print(
                f"N={N:3d} | v1: {t_v1_seed:.3f}s/seed | v2: {t_v2_seed:.4f}s/seed | "
                f"Speedup: {speedup:6.1f}x | v2 R_causal: {np.mean(v2_r):.4f} (Align: {np.mean(v2_align)*100:.1f}%)"
            )
        else:
            print(
                f"N={N:3d} | v1: [Skipped O(N^5)] | v2: {t_v2_seed:.4f}s/seed | "
                f"v2 R_causal: {np.mean(v2_r):.4f} (Align: {np.mean(v2_align)*100:.1f}%)"
            )

    # Save benchmark report
    out_file = r"F:\_Ai\sgoed\sgoed\matrix\benchmark_v1_vs_v2_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n[Done] Saved benchmark report to: {out_file}")


if __name__ == "__main__":
    run_benchmark()
