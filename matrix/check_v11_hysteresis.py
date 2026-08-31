"""Hysteresis / first-order check for v11 ecosystem via g_inter anneal with state carry."""
import numpy as np
from sgoed_ecosystem_core_v11 import (
    compute_ecosystem_action,
    compute_ecosystem_observables,
)

STEP = 0.15


def anneal_scan(M, N_k, d, g_xy, g_seq, n_therm, n_measure, seed, W_init=None):
    np.random.seed(seed)
    N_total = M * N_k
    k_max = 6.0 * np.sqrt(N_k / 8.0)
    if W_init is None:
        W = np.random.uniform(0.05, 0.3, (N_total, N_total))
        for i in range(N_total):
            W[i, i] = 0.0
    else:
        W = W_init.copy()

    results = []
    for g in g_seq:
        cur_act = compute_ecosystem_action(W, M, N_k, d, g_xy=g_xy, g_inter=g)
        for _ in range(n_therm):
            for i in range(N_total):
                for j in range(N_total):
                    if i == j:
                        continue
                    old = W[i, j]
                    new = old + np.random.normal(0.0, STEP)
                    if new < 0.0:
                        continue
                    W[i, j] = new
                    na = compute_ecosystem_action(W, M, N_k, d, g_xy=g_xy, g_inter=g)
                    ds = na - cur_act
                    if ds <= 0.0 or np.random.uniform() < np.exp(-ds):
                        cur_act = na
                    else:
                        W[i, j] = old
        phis = []
        for _ in range(n_measure):
            for i in range(N_total):
                for j in range(N_total):
                    if i == j:
                        continue
                    old = W[i, j]
                    new = old + np.random.normal(0.0, STEP)
                    if new < 0.0:
                        continue
                    W[i, j] = new
                    na = compute_ecosystem_action(W, M, N_k, d, g_xy=g_xy, g_inter=g)
                    ds = na - cur_act
                    if ds <= 0.0 or np.random.uniform() < np.exp(-ds):
                        cur_act = na
                    else:
                        W[i, j] = old
            r_loc, phi_s, r_cr, aln = compute_ecosystem_observables(W, M, N_k, d)
            phis.append(phi_s)
        results.append(float(np.mean(phis)))
    return results, W


if __name__ == "__main__":
    M, N_k, d = 3, 8, 2
    g_up = [0.0, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.3, 0.5, 0.8, 1.0]
    g_down = list(reversed(g_up))

    for seed in [42, 43]:
        print(f"--- seed {seed} ---")
        phi_up, W_end = anneal_scan(M, N_k, d, 0.8, g_up, 15, 8, seed)
        phi_down, _ = anneal_scan(M, N_k, d, 0.8, g_down, 15, 8, seed, W_init=W_end)
        for gu, gd, pu, pd in zip(g_up, g_down, phi_up, phi_down):
            print(f"  g={gu:4.2f}: up={pu:+.3f}   g={gd:4.2f}: down={pd:+.3f}")
        loop = max(abs(u - d) for u, d in zip(phi_up, phi_down))
        print(f"  max |up-down| = {loop:.3f}")
