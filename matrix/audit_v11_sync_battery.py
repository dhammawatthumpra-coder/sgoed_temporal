"""
Comprehensive Audit for Phase 3: v11-Ecosystem (Multi-Universe Time Synchronization).
(Documented in SGOED_v10_ecosystem_notes.md)
Tests Synchronization Transition across M=2, 3, 4 Universes and Inter-Coupling g_inter.
"""

import time
import json
import numpy as np
from sgoed_ecosystem_core_v11 import run_v11_ecosystem


def run_ecosystem_sync_battery():
    print("==========================================================================")
    print("   SGOED-Relational Phase 3: v11-Ecosystem Full Battery Audit (Sync)      ")
    print("==========================================================================")

    # 1. Synchronization Transition Scan (M=3 Universes, g_inter = 0.0 -> 1.0)
    g_inter_values = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
    seeds = [42, 43, 44, 45, 46]
    sync_results = {}

    print("\n--- 1. Testing Relational Time Synchronization Transition (M=3, N_k=10) ---")
    for g_in in g_inter_values:
        t0 = time.time()
        r_loc_list = []
        phi_list = []
        r_cross_list = []

        for s in seeds:
            r_loc, r_std, phi_s, phi_std, r_cr, aln, act = run_v11_ecosystem(
                M=3, N_k=10, d=2, g_xy=0.8, g_inter=g_in,
                n_therm=25, n_measure=35, seed=s
            )
            r_loc_list.append(r_loc)
            phi_list.append(phi_s)
            r_cross_list.append(r_cr)

        elapsed = time.time() - t0
        avg_r_loc = float(np.mean(r_loc_list))
        avg_phi = float(np.mean(phi_list))
        std_phi = float(np.std(phi_list))
        avg_r_cr = float(np.mean(r_cross_list))

        sync_results[f"g_inter_{g_in:.1f}"] = {
            "g_inter": g_in,
            "mean_R_local": avg_r_loc,
            "mean_phi_sync": avg_phi,
            "std_phi_sync": std_phi,
            "mean_R_cross": avg_r_cr,
            "time_seconds": elapsed,
        }

        print(
            f"g_inter={g_in:3.1f} | Inter-Sync Phi: {avg_phi:+6.3f} +/- {std_phi:5.3f} | "
            f"R_local: {avg_r_loc:.4f} | R_cross: {avg_r_cr:.4f} | Time: {elapsed:.2f}s"
        )

    # 2. Scaling with Universe Count (M = 2, 3, 4, 5 with g_inter = 0.5)
    print("\n--- 2. Testing Ecosystem Scaling with Universe Count (M=2..5, g_inter=0.5) ---")
    m_values = [2, 3, 4, 5]
    m_results = {}

    for M in m_values:
        t0 = time.time()
        phi_list = []
        r_loc_list = []

        for s in seeds:
            r_loc, r_std, phi_s, phi_std, r_cr, aln, act = run_v11_ecosystem(
                M=M, N_k=8, d=2, g_xy=0.8, g_inter=0.5,
                n_therm=25, n_measure=35, seed=s
            )
            phi_list.append(phi_s)
            r_loc_list.append(r_loc)

        elapsed = time.time() - t0
        avg_phi = float(np.mean(phi_list))
        std_phi = float(np.std(phi_list))
        avg_r_loc = float(np.mean(r_loc_list))

        m_results[f"M_{M}"] = {
            "M": M,
            "mean_phi_sync": avg_phi,
            "std_phi_sync": std_phi,
            "mean_R_local": avg_r_loc,
            "time_seconds": elapsed,
        }

        print(
            f"M={M} Universes | Sync Phi: {avg_phi:+6.3f} +/- {std_phi:5.3f} | "
            f"R_local: {avg_r_loc:.4f} | Time: {elapsed:.2f}s"
        )

    full_report = {
        "sync_transition": sync_results,
        "universe_count_scaling": m_results,
    }

    out_file = r"F:\_Ai\sgoed\sgoed\matrix\audit_v11_sync_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2)
    print(f"\n[Done] Saved full ecosystem sync audit to: {out_file}")


if __name__ == "__main__":
    run_ecosystem_sync_battery()
