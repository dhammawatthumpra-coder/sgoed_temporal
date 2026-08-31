"""
SGOED-Relational v12 Ablation Study: Engineered vs True Emergent Condensation
============================================================================
Tests 4 Conditions across N = 16, 24, 32 (10 seeds each, n_therm=120):
1. Baseline: g_xy = 0.0, lambda_cond = 0.0 (Uncoupled Null)
2. Quartic Coupling ONLY: g_xy = 1.5, lambda_cond = 0.0 (Pure Emergence Test)
3. Relational Condensation: Observer-directed SVD term -lambda * sum_a v_hat_a * Tr_a((WW^T)^2)
4. Global Engineered Condensation: g_xy = 1.5, lambda_cond = 0.15 (v12 Baseline)

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-31
"""

import time
import json
import numpy as np
from numba import njit


@njit(fastmath=True)
def compute_action_ablation(
    W: np.ndarray,
    mode: int,  # 1: Baseline, 2: Quartic Only, 3: Relational Cond, 4: Global Cond
    d: int = 3,
    alpha: float = 0.5,
    beta: float = 0.1,
    lambda_gate: float = 10.0,
    k_max: float = 6.0,
    g_xy: float = 1.5,
    lambda_cond: float = 0.15,
    eps: float = 1e-7,
):
    N = W.shape[0]

    # 1. Sparsity
    s_sparsity = 0.0
    for i in range(N):
        for j in range(N):
            if i != j:
                s_sparsity += alpha * (W[i, j] ** 2)

    # 2. Transitivity Loop (W^2 - W)^2
    s_trans = 0.0
    for i in range(N):
        for k in range(N):
            if i == k:
                continue
            w2_ik = 0.0
            for j in range(N):
                if j != i and j != k:
                    w2_ik += W[i, j] * W[j, k]
            s_trans += beta * ((w2_ik - W[i, k]) ** 2)

    # 3. Capacity Gate
    s_gate = 0.0
    out_deg = np.zeros(N)
    in_deg = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out_deg[i] += W[i, j]
                in_deg[j] += W[i, j]
        if out_deg[i] > k_max:
            s_gate += lambda_gate * ((out_deg[i] - k_max) ** 2)
        if in_deg[i] > k_max:
            s_gate += lambda_gate * ((in_deg[i] - k_max) ** 2)

    # 4. Observer Coupling
    s_coupling = 0.0
    diff_s = np.zeros(d)
    sum_sq = 0.0
    for a in range(d):
        diff_s[a] = out_deg[a] - in_deg[a]
        sum_sq += diff_s[a] ** 2
    norm_v = np.sqrt(sum_sq) + eps

    v_hat = np.zeros(d)
    for a in range(d):
        v_hat[a] = diff_s[a] / norm_v

    if mode in [2, 3, 4]:
        for a in range(d):
            sum_rest_quartic = 0.0
            for j in range(d, N):
                sum_rest_quartic += W[a, j] ** 4
            s_coupling += -g_xy * v_hat[a] * sum_rest_quartic

    # 5. Condensation Term
    s_cond = 0.0
    if mode == 4:  # Global Engineered SVD
        # Compute Tr((W W^T)^2)
        M = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                s = 0.0
                for k in range(N):
                    s += W[i, k] * W[j, k]
                M[i, j] = s
        tr_m2 = 0.0
        for i in range(N):
            for j in range(N):
                tr_m2 += M[i, j] ** 2
        s_cond = -lambda_cond * tr_m2

    elif mode == 3:  # Relational Observer-Driven SVD
        # S_cond = -lambda_cond * sum_a v_hat_a * (row_norm_a)^4
        for a in range(d):
            row_norm_sq = 0.0
            for j in range(N):
                if j != a:
                    row_norm_sq += W[a, j] ** 2
            s_cond += -lambda_cond * v_hat[a] * (row_norm_sq ** 2)

    return s_sparsity + s_trans + s_gate + s_coupling + s_cond


@njit(fastmath=True)
def run_ablation_simulation(
    mode: int,
    N: int = 16,
    d: int = 3,
    g_xy: float = 1.5,
    lambda_cond: float = 0.15,
    n_therm: int = 120,
    n_measure: int = 60,
    step_size: float = 0.15,
    seed: int = 42,
):
    np.random.seed(seed)
    k_max = 6.0 * np.sqrt(N / 8.0)

    W = np.random.uniform(0.05, 0.3, (N, N))
    for i in range(N):
        W[i, i] = 0.0

    current_action = compute_action_ablation(
        W, mode, d, 0.5, 0.1, 10.0, k_max, g_xy, lambda_cond
    )

    total_sweeps = n_therm + n_measure

    for sweep in range(total_sweeps):
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue

                old_val = W[i, j]
                delta = np.random.normal(0.0, step_size)
                new_val = old_val + delta
                if new_val < 0.0:
                    continue

                W[i, j] = new_val
                new_action = compute_action_ablation(
                    W, mode, d, 0.5, 0.1, 10.0, k_max, g_xy, lambda_cond
                )

                delta_s = new_action - current_action
                if delta_s <= 0.0 or np.random.uniform(0.0, 1.0) < np.exp(-delta_s):
                    current_action = new_action
                else:
                    W[i, j] = old_val

    return W


def evaluate_invariants(W: np.ndarray, d: int = 3):
    N = W.shape[0]
    D = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            diff = W[i, j] - W[j, i]
            if abs(diff) > 1e-4:
                D += np.sign(diff)

    vals = np.linalg.svd(W, compute_uv=False)
    spectral_ratio = float(vals[0] / vals[1]) if len(vals) >= 2 and vals[1] > 1e-5 else 1.0
    
    out_deg = np.sum(W, axis=1)
    in_deg = np.sum(W, axis=0)
    obs_flow = np.mean(out_deg[:d] - in_deg[:d])
    sys_flow = np.mean(out_deg[d:] - in_deg[d:])
    aligned = 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.05) else 0.0

    return float(D), float(spectral_ratio), float(aligned)


def run_full_ablation_audit():
    print("==========================================================================")
    print("   SGOED-Relational v12 Ablation Audit (Engineered vs True Emergence)     ")
    print("==========================================================================")

    modes = {
        1: "1. Baseline (Uncoupled Null)",
        2: "2. Quartic Coupling ONLY (Pure Emergence Test)",
        3: "3. Relational Observer SVD",
        4: "4. Global SVD (v12 Baseline)",
    }

    sizes = [16, 24, 32]
    seeds = [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
    
    all_results = {}

    for N in sizes:
        print(f"\n==================== SYSTEM SIZE N = {N:2d} (10 SEEDS) ====================")
        all_results[f"N_{N}"] = {}

        for m, m_name in modes.items():
            t0 = time.time()
            d_list = []
            spec_list = []
            align_list = []

            for s in seeds:
                W = run_ablation_simulation(
                    mode=m, N=N, d=3, g_xy=1.5, lambda_cond=0.15,
                    n_therm=120, n_measure=60, seed=s
                )
                D, spec, align = evaluate_invariants(W, d=3)
                d_list.append(D)
                spec_list.append(spec)
                align_list.append(align)

            elapsed = time.time() - t0
            avg_d = float(np.mean(d_list))
            std_d = float(np.std(d_list))
            avg_spec = float(np.mean(spec_list))
            std_spec = float(np.std(spec_list))
            avg_align = float(np.mean(align_list))

            all_results[f"N_{N}"][f"mode_{m}"] = {
                "name": m_name,
                "mean_D": avg_d,
                "std_D": std_d,
                "mean_spectral_ratio": avg_spec,
                "std_spectral_ratio": std_spec,
                "alignment_pct": avg_align * 100.0,
                "time_seconds": elapsed,
            }

            print(
                f"{m_name:<46} | "
                f"Spectral Ratio: {avg_spec:5.2f} +/- {std_spec:4.2f} | "
                f"Net D: {avg_d:+6.1f} +/- {std_d:4.1f} | "
                f"Align: {avg_align*100:5.1f}% | Time: {elapsed:.1f}s"
            )

    out_file = r"F:\_Ai\sgoed\V5\matrix\audit_v12_ablation_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n[Done] Saved ablation audit results to: {out_file}")


if __name__ == "__main__":
    run_full_ablation_audit()
