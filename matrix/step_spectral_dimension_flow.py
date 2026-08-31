"""
SGOED v15 — Track 3: Spectral dimension on FLOW networks
=========================================================
Question (per review): does a network WITH flow give a different d_s
profile than the same structure at equilibrium? (CDT ballpark: d_s -> 4.)

Setups (random-walk return probability P(t) = Tr(T^t)/N,
d_s(t) = -2 d ln P / d ln t, discrete log-derivative):
  1. chain M=64: symmetric (bias=0 -> plateau ~1) vs flow-biased
     (bias=eps>0 -> drift: exponential suppression of returns).
  2. k-ary tree (Bethe-like): undirected (reference plateau ~3) vs
     directed-outward with flow strength alpha (alpha=1: pure outward,
     transient: returns die -> d_s diverges).
Null = symmetric version of the SAME structure; flow = asymmetry.

Plain expectation to verify: on a flow network d_s tracks the DRIFT /
transience, not the geometry — consistent with the earlier d_s
null-compatibility, now with a mechanism.
"""
import json
import numpy as np


def ds_curve(T, Tmax=1200):
    N = T.shape[0]
    P = np.zeros(Tmax + 1)
    Tk = np.eye(N)
    for t in range(Tmax + 1):
        if t > 0:
            Tk = Tk @ T
        P[t] = np.trace(Tk) / N
    ts = np.arange(1, Tmax)                       # t = 1 .. Tmax-1
    safe = np.log(np.maximum(P, 1e-300))
    dlnP = safe[2:] - safe[1:Tmax]
    dlnt = np.log(ts + 1) - np.log(ts)
    ds = -2.0 * dlnP / dlnt
    return P, ds


def chain_T(M, bias):
    T = np.zeros((M, M))
    for i in range(M):
        if i == 0:
            T[0, 1] = 1.0
        elif i == M - 1:
            T[M - 1, M - 2] = 1.0
        else:
            T[i, i + 1] = 0.5 + bias
            T[i, i - 1] = 0.5 - bias
    return T


def tree_T(depth, branch, alpha):
    """alpha=0.5: undirected reference; alpha=1: pure outward flow."""
    n = (branch ** (depth + 1) - 1) // (branch - 1)
    T = np.zeros((n, n))
    for i in range(n):
        nb = []
        if i > 0:
            nb.append((i - 1) // branch)          # parent
        for b in range(branch):
            c = branch * i + 1 + b
            if c < n:
                nb.append(c)                      # children
        nch = branch if branch * i + 1 < n else 0
        if alpha == 0.5:
            for v in nb:
                T[i, v] = 1.0 / len(nb)
        else:
            for v in nb:
                T[i, v] = (1.0 - alpha) / max(len(nb) - nch, 1) if v < i else alpha / max(nch, 1)
    # rows may be empty for outward-flow leaves (alpha=1): mass leaves the graph
    for i in range(n):
        s = T[i].sum()
        if s > 0:
            T[i] /= s
    return T


def report(tag, T, name, Tmax=1200, plateau=(60, 300)):
    # LAZY walk (Hermite: T <- 0.5I + 0.5T) — the chain/tree are bipartite,
    # so P(t)=0 on odd t (parity conservation) and log(0) corrupts d_s with
    # ~+/-690 oscillations. Lazy breaks the bipartiteness; standard for the
    # heat-kernel / diffusion analogue.
    N = T.shape[0]
    T = 0.5 * np.eye(N) + 0.5 * T
    P, ds = ds_curve(T, Tmax)
    sel = [10, 50, 200, 800]
    vals = {str(t): round(float(ds[t - 1]), 3) for t in sel if t - 1 < len(ds)}
    plat = float(np.nanmean(ds[plateau[0]:plateau[1]])) if len(ds) > plateau[1] else np.nan
    print(f"[{tag:28s}] d_s(t=10,50,200,800)={list(vals.values())} "
          f"plateau(60-300)={plat:.2f} P_tail={P[-1]:.2e}")
    return {"d_s": vals, "plateau": plat, "P_tail": float(P[-1])}


if __name__ == "__main__":
    out = {}
    print("CHAIN M=64: symmetry vs flow bias")
    for bias in [0.0, 0.1, 0.2]:
        T = chain_T(64, bias)
        r = report(f"chain bias={bias}", T, "c", plateau=(80, 600))
        out[f"chain_bias_{bias}"] = r

    print("\n3-ARY TREE depth=6: undirected vs outward flow")
    for alpha in [0.5, 0.8, 1.0]:
        T = tree_T(6, 3, alpha)
        r = report(f"tree alpha={alpha}", T, "t", plateau=(60, 400))
        out[f"tree_alpha_{alpha}"] = r

    with open(r"F:\_Ai\sgoed\sgoed\matrix\step_spectral_dimension_flow_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_spectral_dimension_flow_results.json")