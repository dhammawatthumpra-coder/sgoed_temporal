"""
SGOED — commutator-compatibility growth (review test)
====================================================
Relation u<k iff  D_comp(u,k) <= (c * dt)^2  (dt = birth time over [0,T]),
with D_comp(u,k) = (1/(d_sp*N)) * sum_a |Tr([X_u^a, X_k^a]^2)|  (commutator
metric: "states that share a frame commute -> compatible").

Regimes:
  K  torus-engineered states (shared A,B frame from the birth rule)
     -> commutator is EXACTLY a torus metric (sin^2(Delta s)) -> invariance
        expected (same value as the difference-metric light-cone).
  R  real sequential-growth states (X nearly independent per unit)
     -> commutator distance nearly constant -> horizon rule -> chain-like
        expected (repeats Leg1 with a different metric).

Gates: std_across N in {250,500,1000} <=0.05 PASS / >0.10 FAIL.
"""
import json
import sys
import numpy as np
from numba import njit
sys.path.insert(0, ".")
sys.path.insert(0, r"F:\_Ai\sgoed\V5\code")
from step_causal_set_scale_study import calibration, read_dim
from step_sequential_growth import sequential_growth
from sgoed_core_v7 import _compute_v_hat

Ns = [250, 500, 1000]


@njit(fastmath=True)
def dcomp_njit(X, Dc):
    """(M,D,Nn,Nn) -> upper-triangular commutator distance (numba loop)."""
    M, D, Nn, _ = X.shape
    for u in range(M):
        for k in range(u + 1, M):
            s = 0.0
            for mu in range(D):
                comm = X[u, mu] @ X[k, mu] - X[k, mu] @ X[u, mu]
                t = 0.0
                for i in range(Nn):
                    for j in range(Nn):
                        t += comm[i, j] * comm[j, i]
                s += abs(t)
            Dc[u, k] = s / (D * Nn)


def torus_states(N, seed, d_sp=3, Nm=5, sigma=2.0, T=10.0, L=10.0, n_grid=2000):
    rng = np.random.RandomState(seed)
    dt_ = T / (n_grid - 1)
    walk = np.cumsum(rng.normal(0.0, sigma * np.sqrt(dt_), (n_grid, d_sp)), axis=0) % L
    idx = np.round(np.linspace(0, n_grid - 1, N)).astype(int)
    s = walk[idx]
    w = 2.0 * np.pi / L
    X = np.zeros((N, d_sp, Nm, Nm))
    TrAB = np.zeros(d_sp)
    for a in range(d_sp):
        A = rng.randn(Nm, Nm) * 0.5
        B = rng.randn(Nm, Nm) * 0.5
        A = (A + A.T) / 2
        B = (B + B.T) / 2
        ca, sa = np.cos(w * s[:, a]), np.sin(w * s[:, a])
        for u in range(N):
            X[u, a] = ca[u] * A + sa[u] * B
        comm = A @ B - B @ A
        TrAB[a] = abs(float(np.trace(comm @ comm).real))
    return X, s, w, TrAB


def dcomp_torus(N, s, w, TrAB, d_sp, Nm):
    """Vectorized: D(u,k) = sum_a |TrAB_a| sin^2(w (s_u-s_k)) / (d_sp*Nm)."""
    ds = s[:, None, :] - s[None, :, :]                     # (N,N,d_sp)
    m = np.abs(TrAB)[None, None, :] * np.sin(w * ds) ** 2
    return m.sum(axis=2) / (d_sp * Nm)


def dcomp_growth(X):
    """Commutator distance for a state family X (M, D, Nn, Nn), numba loop."""
    M, D, Nn, _ = X.shape
    Dc = np.zeros((M, M))
    dcomp_njit(np.ascontiguousarray(X), Dc)
    return Dc


def cone_poset(N, seed, Dcomp, c, T=10.0, theta=0.0, V=None):
    t = np.linspace(0.0, T, N)
    dt = t[:, None] - t[None, :]
    children = [[] for _ in range(N)]
    for k in range(1, N):
        hit = Dcomp[:k, k] <= (c * dt[:k, k]) ** 2
        if theta > 0.0 and V is not None:
            hit = hit & (np.abs(V[:k] @ V[k]) > theta)
        for u in np.nonzero(hit)[0]:
            children[k].append(int(u))
    # transitive closure via bitset reachability
    reach = [1 << i for i in range(N)]
    C = 0
    for i in range(N - 1, -1, -1):
        for j in children[i]:
            reach[i] |= reach[j]
        C += (reach[i] & ~(1 << i)).bit_count()
    return C / (N * (N - 1) / 2)


def audit(name, maker, seeds):
    rows = {}
    for N in Ns:
        ds, rhos = calibration(N, seeds=8)
        dims = [read_dim(maker(N, s), ds, rhos) for s in seeds]
        rows[str(N)] = [float(np.mean(dims)), float(np.std(dims))]
    means = [rows[str(N)][0] for N in Ns]
    std_acr = float(np.std(means))
    verdict = "PASS" if std_acr <= 0.05 else ("FAIL" if std_acr > 0.10 else "BORDER")
    print(f"[{name:24s}] d={means[0]:.2f}/{means[1]:.2f}/{means[2]:.2f} "
          f"std_acr={std_acr:.3f} -> {verdict}")
    return {"d": {str(N): rows[str(N)] for N in Ns}, "std_across_N": std_acr,
            "verdict": verdict}


if __name__ == "__main__":
    out = {}

    # ---- regime K: torus-engineered states ----
    print("K  torus-engineered states (commutator = torus metric)")
    for c in [0.05, 0.15, 0.4]:
        def make(N, s, c=c):
            X, s_pos, w, TrAB = torus_states(N, s)
            return cone_poset(N, s, dcomp_torus(N, s_pos, w, TrAB, 3, 5), c)
        out[f"K_c{c}"] = audit(f"K c={c}", make, range(42, 52))   # 10 seeds

    # ---- regime R: real growth states ----
    print("\nR  real sequential-growth states (X independent)")
    RSS = range(42, 45)                       # 3 seeds, therm=40
    c_refs = []
    states = {}                               # (N, seed) -> (Dc, V), built ONCE
    for N in Ns:
        for s in RSS:
            Xs, Ys = sequential_growth(N, 4, 2, 2, 20.0, 40, s)
            Dc = dcomp_growth(Xs)
            V = np.array([_compute_v_hat(Ys[u], 2) for u in range(N)])
            states[(N, s)] = (Dc, V)
            if N == 250:
                c_refs.append(float(np.sqrt(Dc[Dc > 0].mean()) / (0.5 * 10.0)))
    c_ref = float(np.mean(c_refs))
    print(f"   c_ref = {c_ref:.4f} (from mean commutator distance of real states)")

    for f in [0.5, 1.0, 2.0]:
        rows = {}
        for N in Ns:
            ds, rhos = calibration(N, seeds=8)
            dims = []
            for s in RSS:
                Dc, V = states[(N, s)]
                rho = cone_poset(N, s, Dc, f * c_ref, theta=0.9, V=V)
                dims.append(read_dim(rho, ds, rhos))
            rows[str(N)] = [float(np.mean(dims)), float(np.std(dims))]
        means = [rows[str(N)][0] for N in Ns]
        std_acr = float(np.std(means))
        verdict = "PASS" if std_acr <= 0.05 else ("FAIL" if std_acr > 0.10 else "BORDER")
        print(f"[{'R c=' + str(f) + 'xc_ref':24s}] d={means[0]:.2f}/{means[1]:.2f}/{means[2]:.2f} "
              f"std_acr={std_acr:.3f} -> {verdict}")
        out[f"R_x{f}"] = {"d": {str(N): rows[str(N)] for N in Ns},
                          "std_across_N": std_acr, "verdict": verdict}

    with open(r"F:\_Ai\sgoed\V5\matrix\step_growth_commutator_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_growth_commutator_results.json")