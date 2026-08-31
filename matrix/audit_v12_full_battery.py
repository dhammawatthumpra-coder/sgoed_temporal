"""
Comprehensive Multi-Scale Audit for SGOED-Relational v12 Graph.
Tests Spectral Condensation, Global Net Direction D, and Shuffle Discrimination across N=8, 16, 24, 32, 48.
"""

import time
import json
import numpy as np
from sgoed_graph_core_v12 import run_v12, compute_v12_invariants


def run_v12_full_battery():
    print("==========================================================================")
    print("   SGOED-Relational v12: Multi-Scale Spectral Condensation Full Audit     ")
    print("==========================================================================")

    sizes = [8, 16, 24, 32, 48]
    seeds = [42, 43, 44, 45, 46]
    results = {}

    for N in sizes:
        t0 = time.time()
        real_d_list = []
        real_spec_list = []
        real_align_list = []
        shuf_d_list = []
        shuf_spec_list = []

        for s in seeds:
            D, F_net, spec, align, W = run_v12(
                N=N, d=3, g_xy=1.5, lambda_cond=0.15,
                n_therm=40, n_measure=40, seed=s
            )
            real_d_list.append(D)
            real_spec_list.append(spec)
            real_align_list.append(align)

            # Shuffle Null Test
            flat_W = W.flatten()
            np.random.shuffle(flat_W)
            W_shuf = flat_W.reshape((N, N))
            for i in range(N):
                W_shuf[i, i] = 0.0

            d_sh, _, spec_sh, _ = compute_v12_invariants(W_shuf, d=3)
            shuf_d_list.append(d_sh)
            shuf_spec_list.append(spec_sh)

        elapsed = time.time() - t0
        avg_spec = float(np.mean(real_spec_list))
        std_spec = float(np.std(real_spec_list))
        avg_shuf_spec = float(np.mean(shuf_spec_list))
        avg_d = float(np.mean(real_d_list))
        avg_shuf_d = float(np.mean(shuf_d_list))
        avg_align = float(np.mean(real_align_list))

        results[f"N_{N}"] = {
            "N": N,
            "mean_spectral_ratio": avg_spec,
            "std_spectral_ratio": std_spec,
            "shuffle_null_spectral_ratio": avg_shuf_spec,
            "mean_net_direction_D": avg_d,
            "shuffle_null_D": avg_shuf_d,
            "alignment_pct": avg_align * 100.0,
            "time_per_seed": elapsed / len(seeds),
        }

        print(
            f"N={N:2d} | Time: {elapsed/len(seeds):5.2f}s/seed | "
            f"Spectral Ratio: {avg_spec:5.2f} +/- {std_spec:4.2f} (Null: {avg_shuf_spec:4.2f}) | "
            f"Net D: {avg_d:+6.1f} (Null: {avg_shuf_d:+5.1f}) | Align: {avg_align*100:5.1f}%"
        )

    out_file = r"F:\_Ai\sgoed\sgoed\matrix\audit_v12_full_battery_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[Done] Saved full v12 battery audit to: {out_file}")


if __name__ == "__main__":
    run_v12_full_battery()
