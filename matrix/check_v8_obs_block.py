"""
Observer-block direction check for graph v8 (self-written, data honesty).
v8 notes 4.5 claims: R_obs -> 1.0, obs_flow -> -37 (observer becomes a sink).
Question: is this a REAL directional structure, or also a histogram artifact?
  - D_obs: sign consistency of net flow INSIDE the observer block
  - R_obs real vs R_obs of value-shuffled obs block (histogram preserved)
  - obs_flow real vs shuffled
"""
import numpy as np
from numba import njit
from sgoed_graph_core_v8 import run_v8


@njit(fastmath=True)
def R_region(W, nodes):
    dsum = 0.0
    tsum = 0.0
    for ii in range(len(nodes)):
        i = nodes[ii]
        for jj in range(ii + 1, len(nodes)):
            j = nodes[jj]
            dsum += abs(W[i, j] - W[j, i])
            tsum += W[i, j] + W[j, i]
    return dsum / (tsum + 1e-7)


@njit(fastmath=True)
def D_region(W, nodes):
    D = 0
    for ii in range(len(nodes)):
        i = nodes[ii]
        for jj in range(ii + 1, len(nodes)):
            j = nodes[jj]
            f = W[i, j] - W[j, i]
            if f > 0:
                D += 1
            elif f < 0:
                D -= 1
    return D


def obs_flow(W, d):
    N = W.shape[0]
    out = np.zeros(N)
    inn = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out[i] += W[i, j]
                inn[j] += W[i, j]
    return float(np.mean(out[:d] - inn[:d]))


def shuffle_block(W, nodes, rng):
    W2 = W.copy()
    vals = W2[np.ix_(nodes, nodes)]
    mask = ~np.eye(len(nodes), dtype=bool)
    W2[np.ix_(nodes, nodes)][mask] = rng.permutation(vals[mask])
    return W2


if __name__ == "__main__":
    for g_yx in [0.0, 3.0, 5.0]:
        print(f"--- g_yx = {g_yx} ---")
        rng = np.random.default_rng(7)
        d = 3
        obs_nodes = list(range(d))
        for s in [42, 43, 44]:
            r_mean, r_std, aln, _, _, ext, W = run_v8(
                N=24, d=3, g_xy=0.8, g_yx=g_yx, n_therm=240, n_measure=20, seed=s
            )
            N = W.shape[0]
            R_obs = R_region(W, obs_nodes)
            D_obs = D_region(W, obs_nodes)
            of = obs_flow(W, d)
            # shuffle obs block values (histogram preserved)
            R_obs_sh, D_obs_sh, of_sh = [], [], []
            for rep in range(8):
                Ws = shuffle_block(W, obs_nodes, rng)
                R_obs_sh.append(R_region(Ws, obs_nodes))
                D_obs_sh.append(D_region(Ws, obs_nodes))
                of_sh.append(obs_flow(Ws, d))
            print(f"  seed {s}: R_obs={R_obs:.3f} (shuffle {np.mean(R_obs_sh):.3f}) | "
                  f"D_obs={D_obs:+d}/{len(obs_nodes)*(len(obs_nodes)-1)//2} "
                  f"(shuffle {np.mean(D_obs_sh):+.1f}) | obs_flow={of:+.2f} (shuffle {np.mean(of_sh):+.2f})")
