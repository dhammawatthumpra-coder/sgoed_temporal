"""
Audit script for SGOED-Relational Engine v3:
Measures Temporal Emergence, Alignment, and Emergent Spacetime Dimension (d_MM).
"""

import time
import json
import numpy as np
from sgoed_graph_core_v3 import run_v3


def run_dimension_audit():
    print("==========================================================================")
    print("   SGOED-Relational v3: Spacetime Dimension & Scaling Audit (N=16..256)   ")
    print("==========================================================================")

    # Warmup
    print("[Warmup] JIT Compilation...")
    _ = run_v3(N=8, d=2, n_therm=2, n_measure=2, seed=1)
    print("[Warmup] JIT Ready!\n")

    sizes = [16, 32, 64, 128, 256]
    seeds = [42, 43, 44, 45, 46]
    
    summary = {}

    for N in sizes:
        print(f">>> Evaluating N = {N:3d} across {len(seeds)} seeds...")
        t0 = time.time()
        
        r_list = []
        align_list = []
        d_mm_list = []
        l_max_list = []

        for s in seeds:
            mean_r, std_r, align, d_mm, l_max = run_v3(
                N=N, d=3, g_xy=0.8, g_yx=0.0,
                n_therm=25, n_measure=35, seed=s
            )
            r_list.append(mean_r)
            align_list.append(align)
            d_mm_list.append(d_mm)
            l_max_list.append(l_max)

        elapsed = time.time() - t0
        avg_r = float(np.mean(r_list))
        avg_align = float(np.mean(align_list))
        avg_d_mm = float(np.mean(d_mm_list))
        avg_l_max = float(np.mean(l_max_list))

        summary[f"N_{N}"] = {
            "N": N,
            "mean_r_causal": avg_r,
            "alignment": avg_align,
            "dimension_d_mm": avg_d_mm,
            "longest_chain_L_max": avg_l_max,
            "elapsed_seconds": elapsed,
            "time_per_seed": elapsed / len(seeds),
        }

        print(
            f"N={N:3d} | Time: {elapsed/len(seeds):6.3f}s/seed | "
            f"R_causal: {avg_r:.4f} | Alignment: {avg_align*100:5.1f}% | "
            f"Dimension d_MM: {avg_d_mm:.2f}D | Proper Time (L_max): {avg_l_max:.1f}"
        )

    out_file = r"F:\_Ai\sgoed\sgoed\matrix\audit_v3_dimensions_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[Done] Saved complete dimension audit to: {out_file}")


if __name__ == "__main__":
    run_dimension_audit()
