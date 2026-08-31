"""
Advanced Spacetime Dimension Audit for SGOED-Relational Hypergraph
==================================================================
Threshold-Free Invariant Dimension Estimators:
1. Spectral Dimension (d_s): via Heat Kernel & Random Walk Return Probability P(tau) ~ tau^(-d_s/2)
   (Standard Quantum Gravity Dimension in CDT / Loop Quantum Gravity).
2. Continuous Weighted Myrheim-Meyer (d_MM_cont): Zero-threshold diamond counting.
3. Proper Time (L_max).

Author: Sutipong Chanpengpad & Antigravity AI
Date: 2026-08-31
"""

import time
import json
import numpy as np
from numba import njit
from sgoed_hypergraph_core_v10 import run_v10


@njit(fastmath=True)
def project_hypergraph_to_transition_matrix(T: np.ndarray, eps: float = 1e-7):
    """
    Projects 3-hypergraph T to an effective Transition Probability Matrix P for Random Walks.
    P[i, j] = probability of diffusing from node i to node j.
    """
    N = T.shape[0]
    W_eff = np.zeros((N, N))
    
    for i in range(N):
        for j in range(N):
            if i != j:
                s = 0.0
                for k in range(N):
                    if k != i and k != j:
                        s += T[i, k, j] + T[i, j, k]
                W_eff[i, j] = s

    P = np.zeros((N, N))
    for i in range(N):
        row_sum = 0.0
        for j in range(N):
            row_sum += W_eff[i, j]
        if row_sum > eps:
            for j in range(N):
                P[i, j] = W_eff[i, j] / row_sum
        else:
            for j in range(N):
                P[i, j] = 1.0 / N

    return P, W_eff


def compute_spectral_dimension(P: np.ndarray, tau_steps=np.array([2, 3, 4, 5, 6, 7, 8])):
    """
    Computes Spectral Dimension d_s from the return probability P_return(tau) = Tr(P^tau) / N.
    In d-dimensional spacetime, P_return(tau) ~ tau^(-d_s / 2).
    Therefore, d_s = -2 * d(ln P_return) / d(ln tau).
    """
    N = P.shape[0]
    p_returns = []
    
    P_mat = P.copy()
    temp = np.eye(N)
    max_tau = int(np.max(tau_steps))
    
    for t in range(1, max_tau + 1):
        temp = temp @ P_mat
        if t in tau_steps:
            p_ret = float(np.trace(temp) / N)
            p_returns.append(max(p_ret, 1e-12))

    log_tau = np.log(tau_steps)
    log_pret = np.log(p_returns)

    # Linear fit: slope = -d_s / 2  --> d_s = -2 * slope
    slope, _ = np.polyfit(log_tau, log_pret, 1)
    d_s = -2.0 * slope

    return float(d_s), p_returns


@njit(fastmath=True)
def compute_continuous_dmm(W_eff: np.ndarray, eps: float = 1e-7):
    """
    Continuous Weighted Myrheim-Meyer Dimension (Zero-Threshold).
    Weights causal pairs by net asymmetric flow: F_ij = max(0, W_eff[i, j] - W_eff[j, i])
    """
    N = W_eff.shape[0]
    F = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                diff = W_eff[i, j] - W_eff[j, i]
                if diff > 0.0:
                    F[i, j] = diff

    total_pairs = np.sum(F)
    total_diamonds = 0.0
    for i in range(N):
        for k in range(N):
            if F[i, k] > 0.0:
                for m in range(N):
                    if m != i and m != k and F[i, m] > 0.0 and F[m, k] > 0.0:
                        total_diamonds += F[i, m] * F[m, k]

    if total_pairs > eps:
        ratio = total_diamonds / (total_pairs ** 1.5 + eps)
        d_cont = 1.0 + 3.0 * np.log1p(ratio * N) / np.log1p(N)
    else:
        d_cont = 1.0

    return float(d_cont)


def run_advanced_dimension_audit():
    print("==========================================================================")
    print("   Advanced Threshold-Free Spacetime Dimension Audit (Spectral & Continuous)")
    print("==========================================================================")

    sizes = [12, 16, 24, 32, 48]
    seeds = [42, 43, 44, 45, 46]
    
    results = {}

    for N in sizes:
        print(f"\n>>> Evaluating Invariant Dimensions for N = {N:2d} across {len(seeds)} seeds...")
        t0 = time.time()
        
        ds_list = []
        dmm_cont_list = []
        r_list = []
        l_max_list = []

        for s in seeds:
            # Fast v10 hypergraph simulation with sufficient thermalization
            r_h, r_std, align, d_mm_old, l_max, obs_ext, T = run_v10(
                N=N, d=3, g_xy=0.8, g_yx=0.0,
                n_therm=60, n_measure=40, seed=s
            )
            
            # Project to Random Walk Transition Matrix
            P, W_eff = project_hypergraph_to_transition_matrix(T)
            
            # 1. Spectral Dimension (Threshold-Free!)
            d_s, _ = compute_spectral_dimension(P)
            
            # 2. Continuous Weighted Myrheim-Meyer (Zero-Threshold!)
            d_cont = compute_continuous_dmm(W_eff)

            ds_list.append(d_s)
            dmm_cont_list.append(d_cont)
            r_list.append(r_h)
            l_max_list.append(l_max)

        elapsed = time.time() - t0
        avg_ds = float(np.mean(ds_list))
        std_ds = float(np.std(ds_list))
        avg_dcont = float(np.mean(dmm_cont_list))
        std_dcont = float(np.std(dmm_cont_list))
        avg_r = float(np.mean(r_list))
        avg_lmax = float(np.mean(l_max_list))

        results[f"N_{N}"] = {
            "N": N,
            "mean_d_spectral": avg_ds,
            "std_d_spectral": std_ds,
            "mean_d_mm_continuous": avg_dcont,
            "std_d_mm_continuous": std_dcont,
            "mean_r_hyper": avg_r,
            "mean_L_max": avg_lmax,
            "elapsed_seconds": elapsed,
            "time_per_seed": elapsed / len(seeds),
        }

        print(
            f"N={N:2d} | Time: {elapsed/len(seeds):5.2f}s/seed | "
            f"Spectral Dim (d_s): {avg_ds:4.2f} +/- {std_ds:4.2f} | "
            f"Continuous d_MM: {avg_dcont:4.2f} +/- {std_dcont:4.2f} | "
            f"R_hyper: {avg_r:.4f} | L_max: {avg_lmax:.1f}"
        )

    out_file = r"F:\_Ai\sgoed\V5\matrix\audit_spectral_dimension_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[Done] Saved advanced dimension audit to: {out_file}")


if __name__ == "__main__":
    run_advanced_dimension_audit()
