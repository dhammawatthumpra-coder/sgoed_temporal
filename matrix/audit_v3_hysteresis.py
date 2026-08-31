"""
First-Order Phase Transition & Hysteresis Audit for SGOED-Relational v3.
Scans Back-Reaction Coupling g_YX UP and DOWN to detect Hysteresis Loop and Bistability.
"""

import time
import json
import numpy as np
from sgoed_graph_core_v3 import run_v3_simulation_numba


def run_hysteresis_audit():
    print("==========================================================================")
    print(" SGOED-Relational v3: Observer Feedback & Hysteresis Audit (g_YX 0.0->2.0)")
    print("==========================================================================")

    # Simulation parameters
    N = 24
    d = 3
    g_xy = 0.8
    g_yx_values = [0.0, 0.4, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    seeds = [42, 43, 44, 45, 46]

    results = {}

    print(f"\n--- Scanning g_YX across {len(g_yx_values)} points (N={N}, d={d}) ---")
    t0 = time.time()

    for g_yx in g_yx_values:
        r_list = []
        align_list = []
        obs_extent_list = []
        gate_hit_count = 0

        for s in seeds:
            mean_r, std_r, align, d_mm, l_max, obs_extent = run_v3_simulation_numba(
                N=N, d=d, g_xy=g_xy, g_yx=g_yx,
                n_therm=35, n_measure=45, seed=s
            )
            r_list.append(mean_r)
            align_list.append(align)
            obs_extent_list.append(obs_extent)
            
            # Check if observer entered condensed / gate hit regime (extent > 1.5)
            if obs_extent > 1.5:
                gate_hit_count += 1

        avg_r = float(np.mean(r_list))
        avg_align = float(np.mean(align_list))
        avg_extent = float(np.mean(obs_extent_list))
        hit_pct = float(gate_hit_count / len(seeds) * 100.0)

        results[f"g_yx_{g_yx:.1f}"] = {
            "g_yx": g_yx,
            "mean_r_causal": avg_r,
            "alignment": avg_align,
            "observer_extent": avg_extent,
            "gate_hit_percentage": hit_pct,
        }

        print(
            f"g_YX = {g_yx:3.1f} | Obs Internal Extent: {avg_extent:6.3f} | "
            f"Gate Hit %: {hit_pct:5.1f}% | R_causal: {avg_r:.4f} (Align: {avg_align*100:5.1f}%)"
        )

    elapsed = time.time() - t0
    print(f"\nCompleted scan in {elapsed:.2f} seconds ({elapsed/len(g_yx_values):.2f}s per point).")

    out_file = r"F:\_Ai\sgoed\V5\matrix\audit_v3_hysteresis_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"[Done] Saved hysteresis audit to: {out_file}")


if __name__ == "__main__":
    run_hysteresis_audit()
