"""
SGOED handoff TODO #3 — Past Hypothesis + growth, correct mechanism
====================================================================
Previous attempt failed: unit 0 was THERMALIZED from random init, so the
"past hypothesis" direction never entered the model (v_hat came from
randomized Y, not from the special rank-1 initial condition).

Fixed design:
  - unit 0 = SPECIAL origin: Y[0,0] = 2*I (large trace -> v_hat0 = (1,0)),
    Y[0,1] = 0  (rank-1 / low-entropy initial state)
  - FROZEN: unit 0 is NOT thermalized (the origin is the given past)
  - units 1..M-1 born and adapt to the frozen origin (prefix-sum coupling)
Controls:
  (a) special + frozen        -> the intended mechanism
  (b) special + thermalized   -> does freezing matter?
  (c) random + frozen         -> does specialness matter?
Measure: origin alignment (the arrow direction MUST come from the initial
condition), chain inheritance, determinism.
"""
import sys
import numpy as np
sys.path.insert(0, r"F:\_Ai\sgoed\sgoed\code")
from sgoed_core_v7 import action_v7, _compute_v_hat


def growth_variant(M, N=4, D=2, d=2, g_inter=20.0, therm=60, seed=42,
                   special=True, freeze=True):
    rng = np.random.RandomState(seed)
    Xs = np.zeros((M, D, N, N))
    Ys = np.zeros((M, d, N, N))

    def init_random(u, scaleX=0.5):
        for mu in range(D):
            A = rng.randn(N, N) * scaleX
            Xs[u, mu] = (A + A.T) / 2
        for a in range(d):
            A = rng.randn(N, N) * 0.3
            Ys[u, a] = (A + A.T) / 2

    # ---- origin ----
    if special:
        for mu in range(D):
            A = rng.randn(N, N) * 0.5
            Xs[0, mu] = (A + A.T) / 2
        Ys[0, 0] = 2.0 * np.eye(N)          # rank-1 direction e0
        Ys[0, 1] = np.zeros((N, N))
    else:
        init_random(0)
    if not freeze:                          # thermalize origin (old failure mode)
        S = action_v7(Xs[0], Ys[0], 0.8, 0.0)
        for _ in range(therm):
            for mu in range(D):
                for i in range(N):
                    for j in range(i, N):
                        old = Xs[0, mu, i, j]
                        Xs[0, mu, i, j] = old + 0.25 * rng.randn()
                        if i != j:
                            Xs[0, mu, j, i] = Xs[0, mu, i, j]
                        S2 = action_v7(Xs[0], Ys[0], 0.8, 0.0)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Xs[0, mu, i, j] = old
                            if i != j:
                                Xs[0, mu, j, i] = old
            for a in range(d):
                for i in range(N):
                    for j in range(i, N):
                        old = Ys[0, a, i, j]
                        Ys[0, a, i, j] = old + 0.25 * rng.randn()
                        if i != j:
                            Ys[0, a, j, i] = Ys[0, a, i, j]
                        S2 = action_v7(Xs[0], Ys[0], 0.8, 0.0)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Ys[0, a, i, j] = old
                            if i != j:
                                Ys[0, a, j, i] = old
    vsum = [_compute_v_hat(Ys[0], D)]

    def inter(u):
        vu = _compute_v_hat(Ys[u], D)
        return -g_inter * float(vu @ vsum[0]) if g_inter > 0 else 0.0

    # ---- sequential births ----
    for u in range(1, M):
        init_random(u)
        S = action_v7(Xs[u], Ys[u], 0.8, 0.0) + inter(u)
        for _ in range(therm):
            for mu in range(D):
                for i in range(N):
                    for j in range(i, N):
                        old = Xs[u, mu, i, j]
                        Xs[u, mu, i, j] = old + 0.25 * rng.randn()
                        if i != j:
                            Xs[u, mu, j, i] = Xs[u, mu, i, j]
                        S2 = action_v7(Xs[u], Ys[u], 0.8, 0.0) + inter(u)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Xs[u, mu, i, j] = old
                            if i != j:
                                Xs[u, mu, j, i] = old
            for a in range(d):
                for i in range(N):
                    for j in range(i, N):
                        old = Ys[u, a, i, j]
                        Ys[u, a, i, j] = old + 0.25 * rng.randn()
                        if i != j:
                            Ys[u, a, j, i] = Ys[u, a, i, j]
                        S2 = action_v7(Xs[u], Ys[u], 0.8, 0.0) + inter(u)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Ys[u, a, i, j] = old
                            if i != j:
                                Ys[u, a, j, i] = old
        vsum[0] = vsum[0] + _compute_v_hat(Ys[u], D)
    return Xs, Ys


if __name__ == "__main__":
    import json
    out = {}
    # per-unit origin alignment for one seed (diagnose consensus drift)
    for g_inter in [20.0, 40.0, 100.0]:
        Xs, Ys = growth_variant(16, g_inter=g_inter, therm=120, freeze=True,
                                special=True, seed=42)
        V = np.array([_compute_v_hat(Ys[u], 2) for u in range(16)])
        dots = np.round(np.abs(V @ V[0]), 3)
        print(f"[g={g_inter:5.1f} therm=120 seed=42] per-unit |v.u.v0|={dots.tolist()} "
              f"mean_late={np.mean(dots[8:]):.3f}")
        out[f"perunit_g{g_inter}"] = {"dots": dots.tolist(),
                                      "mean_late": float(np.mean(dots[8:]))}
    for tag, special, freeze in [("(a) special+frozen", True, True),
                                 ("(b) special+thermalized", True, False),
                                 ("(c) random+frozen", False, True)]:
        a0s, chs = [], []
        for seed in range(42, 48):          # 6 seeds, therm 120
            Xs, Ys = growth_variant(16, special=special, freeze=freeze, seed=seed,
                                    g_inter=40.0, therm=120)
            V = np.array([_compute_v_hat(Ys[u], 2) for u in range(16)])
            a0 = np.mean(np.abs(V[1:] @ V[0]))
            ch = np.mean(np.abs(np.einsum("ij,ij->i", V[1:], V[:-1])))
            a0s.append(float(a0))
            chs.append(float(ch))
        print(f"[{tag:24s}] align_origin={np.mean(a0s):.4f}±{np.std(a0s):.4f} "
              f"chain={np.mean(chs):.4f}±{np.std(chs):.4f}")
        out[tag] = {"align_origin": [float(np.mean(a0s)), float(np.std(a0s))],
                    "chain": [float(np.mean(chs)), float(np.std(chs))]}
    with open(r"F:\_Ai\sgoed\sgoed\matrix\step_growth_past_hypothesis_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_growth_past_hypothesis_results.json")