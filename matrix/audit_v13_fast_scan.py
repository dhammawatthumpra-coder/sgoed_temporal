"""
Fast Real-Time Asymmetry Scan for v13.
Uses print(..., flush=True) for immediate visibility.
"""

import time
import json
import numpy as np
from sgoed_graph_core_v13 import run_v13


def run_fast_asymmetry_scan():
    print("==========================================================================", flush=True)
    print("   SGOED-Relational v13: Fast Real-Time Asymmetry Scan                    ", flush=True)
    print("==========================================================================", flush=True)

    g_f = 1.5
    # Key conditions: 0.0 (Pure Forward), 0.2 (Asymmetric), 1.5 (Symmetric)
    g_b_values = [0.0, 0.2, 1.5]
    sizes = [16, 24, 32]
    seeds = [42, 43, 44, 45, 46]

    results = {}

    for N in sizes:
        print(f"\n==================== SYSTEM SIZE N = {N:2d} (5 SEEDS) ====================", flush=True)
        results[f"N_{N}"] = {}

        for p_b in [2, 4]:
            print(f"\n--- Testing Backward Power p_b = {p_b} ---", flush=True)
            for g_b in g_b_values:
                t0 = time.time()
                d_list = []
                d_root_list = []
                spec_list = []
                align_list = []

                for s in seeds:
                    D, D_root, spec, align, W = run_v13(
                        N=N, d=3, g_f=g_f, g_b=g_b, p_b=p_b,
                        n_therm=60, n_measure=40, seed=s
                    )
                    d_list.append(D)
                    d_root_list.append(D_root)
                    spec_list.append(spec)
                    align_list.append(align)

                elapsed = time.time() - t0
                avg_d = float(np.mean(d_list))
                std_d = float(np.std(d_list))
                avg_droot = float(np.mean(d_root_list))
                avg_spec = float(np.mean(spec_list))
                avg_align = float(np.mean(align_list))
                sig_d = abs(avg_d) / (std_d + 1e-6)

                asym_label = "Pure Forward" if g_b == 0.0 else ("Symmetric" if g_b == g_f else "Asymmetric")
                print(
                    f"g_b={g_b:3.1f} ({asym_label:<12}) | "
                    f"Net D: {avg_d:+6.1f} +/- {std_d:4.1f} ({sig_d:3.1f} sigma) | "
                    f"D_root: {avg_droot:+5.2f} | "
                    f"Spec: {avg_spec:4.2f} | "
                    f"Align: {avg_align*100:5.1f}% | Time: {elapsed:.1f}s",
                    flush=True
                )

                cond_name = f"g_f_{g_f}_g_b_{g_b}_p_{p_b}"
                results[f"N_{N}"][cond_name] = {
                    "g_f": g_f,
                    "g_b": g_b,
                    "p_b": p_b,
                    "mean_D": avg_d,
                    "std_D": std_d,
                    "significance_D": sig_d,
                    "mean_D_root": avg_droot,
                    "mean_spectral_ratio": avg_spec,
                    "alignment_pct": avg_align * 100.0,
                    "time_seconds": elapsed,
                }

    out_file = "audit_v13_fast_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[Done] Saved fast asymmetry audit to: {out_file}", flush=True)


if __name__ == "__main__":
    run_fast_asymmetry_scan()
