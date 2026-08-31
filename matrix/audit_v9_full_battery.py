"""
Full Battery Audit for SGOED-Relational Phase 2: v9-R Causal Hypergraph.
Tests Multi-Seed Emergence, 4D Spacetime Dimension, and Observer Feedback Hysteresis.
"""

import time
import json
import numpy as np
from sgoed_hypergraph_core_v9 import run_v9


def run_v9_full_battery():
    print("==========================================================================")
    print("   SGOED-Relational Phase 2: v9-R Causal Hypergraph Full Battery Audit    ")
    print("==========================================================================")

    # 1. Multi-Scale Emergence & Spacetime Dimension (N=8, 12, 16, 20)
    sizes = [8, 12, 16, 20]
    seeds = [42, 43, 44, 45, 46]
    scale_results = {}

    print("\n--- 1. Testing Multi-Scale 4D Spacetime Emergence (g_XY=0.8, g_YX=0.0) ---")
    for N in sizes:
        t0 = time.time()
        r_list = []
        align_list = []
        d_mm_list = []
        l_max_list = []

        for s in seeds:
            r_h, r_std, align, d_mm, l_max, obs_ext, act = run_v9(
                N=N, d=3, g_xy=0.8, g_yx=0.0,
                n_therm=25, n_measure=35, seed=s
            )
            r_list.append(r_h)
            align_list.append(align)
            d_mm_list.append(d_mm)
            l_max_list.append(l_max)

        elapsed = time.time() - t0
        avg_r = float(np.mean(r_list))
        avg_align = float(np.mean(align_list))
        avg_d_mm = float(np.mean(d_mm_list))
        avg_l_max = float(np.mean(l_max_list))

        scale_results[f"N_{N}"] = {
            "N": N,
            "mean_r_hyper": avg_r,
            "alignment": avg_align,
            "dimension_d_mm": avg_d_mm,
            "longest_chain_L_max": avg_l_max,
            "time_per_seed": elapsed / len(seeds),
        }

        print(
            f"N={N:2d} | Time: {elapsed/len(seeds):5.2f}s/seed | "
            f"R_hyper: {avg_r:.4f} | Align: {avg_align*100:5.1f}% | "
            f"Spacetime Dim: {avg_d_mm:.2f}D | Proper Time: {avg_l_max:.1f}"
        )

    # 2. Observer Feedback & Bistability Scan (N=12, d=3, g_YX = 0.0 -> 2.0)
    print("\n--- 2. Testing Observer Feedback & Bistability (N=12, d=3) ---")
    g_yx_values = [0.0, 0.4, 0.8, 1.2, 1.6, 2.0]
    feedback_results = {}

    for g_yx in g_yx_values:
        r_list = []
        align_list = []
        ext_list = []
        hit_count = 0

        for s in seeds:
            r_h, r_std, align, d_mm, l_max, obs_ext, act = run_v9(
                N=12, d=3, g_xy=0.8, g_yx=g_yx,
                n_therm=25, n_measure=35, seed=s
            )
            r_list.append(r_h)
            align_list.append(align)
            ext_list.append(obs_ext)
            if obs_ext > 1.5:
                hit_count += 1

        avg_r = float(np.mean(r_list))
        avg_align = float(np.mean(align_list))
        avg_ext = float(np.mean(ext_list))
        hit_pct = float(hit_count / len(seeds) * 100.0)

        feedback_results[f"g_yx_{g_yx:.1f}"] = {
            "g_yx": g_yx,
            "mean_r_hyper": avg_r,
            "alignment": avg_align,
            "obs_extent": avg_ext,
            "gate_hit_pct": hit_pct,
        }

        print(
            f"g_YX={g_yx:3.1f} | Obs Extent: {avg_ext:6.3f} | "
            f"Gate Hit %: {hit_pct:5.1f}% | R_hyper: {avg_r:.4f} (Align: {avg_align*100:5.1f}%)"
        )

    # Save full results
    full_data = {
        "scaling_and_dimension": scale_results,
        "feedback_and_bistability": feedback_results,
    }
    out_file = r"F:\_Ai\sgoed\V5\matrix\audit_v9_full_battery_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=2)
    print(f"\n[Done] Saved full v9 battery audit to: {out_file}")


if __name__ == "__main__":
    run_v9_full_battery()
