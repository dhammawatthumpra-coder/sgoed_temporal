"""
R_hyper vs random baseline audit (self-written, data honesty).
================================================================
Question: does R_hyper ~ 0.5 really evidence an "arrow of time"?
Key subtlety: R_hyper = sum|T_ijk - T_kji|/(sum T_ijk+T_kji) measures the
MAGNITUDE of mirror asymmetry, NOT whether directions are consistent.
Tests:
  1. R_real vs R of value-shuffled T (histogram preserved, positions destroyed)
  2. R_real vs R of iid-uniform T (analytic baseline: E[R] = 0.386 for U[0,1])
  3. R under mirror-pair swap (must be INVARIANT by symmetry - shows R is
     direction-blind)
  4. Directional consistency D = sum_{i<k} sign(flow_ik - flow_ki): the real
     arrow-of-time observable (random -> ~0, global arrow -> large |D|)
  5. Alignment + degree-imbalance std vs null
"""
import numpy as np
from numba import njit
from sgoed_hypergraph_core_v10 import run_v10


@njit(fastmath=True)
def compute_R(T):
    N = T.shape[0]
    dsum = 0.0
    tsum = 0.0
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(i + 1, N):
                if k == j:
                    continue
                dsum += abs(T[i, j, k] - T[k, j, i])
                tsum += T[i, j, k] + T[k, j, i]
    return dsum / (tsum + 1e-7)


@njit(fastmath=True)
def direction_consistency(T):
    """D = sum over unordered {i,k} of sign of net flow i->k minus k->i.
    Random: D ~ 0.  Global arrow: |D| large."""
    N = T.shape[0]
    D = 0.0
    for i in range(N):
        for k in range(i + 1, N):
            f = 0.0
            for j in range(N):
                if j != i and j != k:
                    f += T[i, j, k] - T[k, j, i]
            if f > 0:
                D += 1.0
            elif f < 0:
                D -= 1.0
    return D


@njit(fastmath=True)
def degree_imbalance_std(T):
    N = T.shape[0]
    out = np.zeros(N)
    inn = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if k != i and k != j:
                    out[i] += T[i, j, k]
                    inn[k] += T[i, j, k]
    imb = out - inn
    return float(np.std(imb))


def alignment_fraction(T, d):
    """v9-style: frac of measures where obs_flow*sys_flow <= 0 (on final T)."""
    N = T.shape[0]
    out = np.zeros(N)
    inn = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if k != i and k != j:
                    out[i] += T[i, j, k]
                    inn[k] += T[i, j, k]
    obs_flow = np.mean(out[:d] - inn[:d])
    sys_flow = np.mean(out[d:] - inn[d:])
    return 1.0 if (obs_flow * sys_flow <= 0.0 and abs(obs_flow) > 0.05) else 0.0


def value_shuffle(T, rng):
    N = T.shape[0]
    mask = np.ones((N, N, N), dtype=bool)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if k == i or k == j:
                    mask[i, j, k] = False
    vals = T[mask]
    T2 = T.copy()
    T2[mask] = rng.permutation(vals)
    return T2


def mirror_swap(T, rng):
    """Randomly swap each mirror pair (i,j,k)<->(k,j,i). R invariant by |a-b|."""
    N = T.shape[0]
    T2 = T.copy()
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(i + 1, N):
                if k == j:
                    continue
                if rng.uniform() < 0.5:
                    T2[i, j, k], T2[k, j, i] = T2[k, j, i], T2[i, j, k]
    return T2


if __name__ == "__main__":
    print("=" * 74)
    print(" 1. REAL hypergraph (N=32, d=3, g_xy=0.8, seed 42)")
    print("=" * 74)
    r_h, r_std, align, dmm_old, l_max, obs_ext, T = run_v10(
        N=32, d=3, g_xy=0.8, g_yx=0.0, n_therm=60, n_measure=40, seed=42
    )
    R_real = compute_R(T)
    D_real = direction_consistency(T)
    imb_real = degree_imbalance_std(T)
    aln_real = alignment_fraction(T, d=3)
    print(f"  R_hyper = {R_real:.4f} | D_direction = {D_real:+.0f} | "
          f"deg-imb std = {imb_real:.4f} | alignment = {aln_real}")

    rng = np.random.default_rng(123)

    print()
    print("=" * 74)
    print(" 2. NULL TESTS")
    print("=" * 74)

    # 2a. value shuffle (position structure destroyed, histogram preserved)
    R_sh, D_sh, imb_sh, aln_sh = [], [], [], []
    for rep in range(10):
        Ts = value_shuffle(T, rng)
        R_sh.append(compute_R(Ts))
        D_sh.append(direction_consistency(Ts))
        imb_sh.append(degree_imbalance_std(Ts))
        aln_sh.append(alignment_fraction(Ts, d=3))
    print(f"  [shuffle values] R = {np.mean(R_sh):.4f} +/- {np.std(R_sh):.4f} | "
          f"D = {np.mean(D_sh):+.1f} +/- {np.std(D_sh):.1f} | "
          f"imb-std = {np.mean(imb_sh):.4f} | align = {np.mean(aln_sh)*100:.0f}%")

    # 2b. iid uniform in the same support as thermalized T
    lo, hi = float(T.min()), float(T.max())
    R_u, D_u, imb_u = [], [], []
    for rep in range(10):
        Tu = rng.uniform(lo, hi, T.shape)
        for i in range(Tu.shape[0]):
            for j in range(Tu.shape[0]):
                Tu[i, i, j] = 0.0
                Tu[i, j, i] = 0.0
                Tu[j, i, i] = 0.0
        R_u.append(compute_R(Tu))
        D_u.append(direction_consistency(Tu))
        imb_u.append(degree_imbalance_std(Tu))
    print(f"  [iid uniform {lo:.3f}-{hi:.3f}] R = {np.mean(R_u):.4f} +/- {np.std(R_u):.4f} | "
          f"D = {np.mean(D_u):+.1f} +/- {np.std(D_u):.1f} | "
          f"imb-std = {np.mean(imb_u):.4f}")

    # 2c. mirror swap (direction scramble, R must be invariant)
    R_sw, D_sw = [], []
    for rep in range(10):
        Ts = mirror_swap(T, rng)
        R_sw.append(compute_R(Ts))
        D_sw.append(direction_consistency(Ts))
    print(f"  [mirror swap]    R = {np.mean(R_sw):.4f} +/- {np.std(R_sw):.4f} (INVARIANT by design) | "
          f"D = {np.mean(D_sw):+.1f} +/- {np.std(D_sw):.1f}")

    print()
    print("=" * 74)
    print(" 3. VERDICT")
    print("=" * 74)
    print(f"  R_real = {R_real:.4f} vs shuffle {np.mean(R_sh):.4f} vs uniform {np.mean(R_u):.4f} "
          f"(E[R_iid U[0,1]] = 0.386 analytic)")
    print(f"  D_real = {D_real:+.0f} (max possible = {32*31/2:.0f}) vs shuffle {np.mean(D_sh):+.1f} vs uniform {np.mean(D_u):+.1f}")
    print(f"  imb-std real {imb_real:.4f} vs shuffle {np.mean(imb_sh):.4f} vs uniform {np.mean(imb_u):.4f}")
