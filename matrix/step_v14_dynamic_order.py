"""
v14 dynamic order test (self-written): does alignment unfold in time with a
stable ordering, or all at once (no internal time)?
Tracks v_hat of each unit during thermalization; align_time[u] = first sweep
where |v_hat_u . v_ref| > 0.9.  Stable ordering across seeds would mean a real
time-ordering; random ordering = noise.
"""
import sys
import numpy as np
sys.path.insert(0, ".")
from sgoed_matrix_ecosystem_v14 import action_v14
from sgoed_core_v7 import _compute_v_hat

sys.path.insert(0, r"F:\_Ai\sgoed\V5\code")


def run_track(M, N, D, d, g_inter, n_therm, seed, rec_every=3):
    rng = np.random.RandomState(seed)
    Xs = np.zeros((M, D, N, N))
    Ys = np.zeros((M, d, N, N))
    for u in range(M):
        for mu in range(D):
            A = rng.randn(N, N) * 0.5
            Xs[u, mu] = (A + A.T) / 2
        for a in range(d):
            A = rng.randn(N, N) * 0.3
            Ys[u, a] = (A + A.T) / 2
    S = action_v14(Xs, Ys, g_inter)
    traj = []
    for sweep in range(n_therm + 5):
        for u in range(M):
            for mu in range(D):
                for i in range(N):
                    for j in range(i, N):
                        old = Xs[u, mu, i, j]
                        Xs[u, mu, i, j] = old + 0.15 * rng.randn()
                        if i != j:
                            Xs[u, mu, j, i] = Xs[u, mu, i, j]
                        S2 = action_v14(Xs, Ys, g_inter)
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
                        Ys[u, a, i, j] = old + 0.15 * rng.randn()
                        if i != j:
                            Ys[u, a, j, i] = Ys[u, a, i, j]
                        S2 = action_v14(Xs, Ys, g_inter)
                        dS = S2 - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Ys[u, a, i, j] = old
                            if i != j:
                                Ys[u, a, j, i] = old
        if sweep % rec_every == 0:
            traj.append(np.array([_compute_v_hat(Ys[u], D) for u in range(M)]))
    return np.array(traj)  # (T, M, D)


def align_times(traj, thresh=0.9):
    """First time each unit aligns with the final reference direction."""
    T, M, D = traj.shape
    vref = traj[-1, 0].copy()
    # fix reference sign: align with mean of final v_hats
    vmean = traj[-1].mean(axis=0)
    if np.dot(vref, vmean) < 0:
        vref = -vref
    times = []
    for u in range(M):
        found = None
        for t in range(T):
            if abs(float(np.dot(traj[t, u], vref))) > thresh:
                found = t
                break
        times.append(found if found is not None else T)
    return np.array(times), vref


print("=" * 78)
print(" DYNAMIC ORDER: M=8, g_inter=20 (align full), n_therm=60, 3 seeds")
print("=" * 78)
all_orders = []
for s in [42, 43, 44]:
    traj = run_track(8, 4, 2, 2, 20.0, 60, s, rec_every=3)
    times, vref = align_times(traj)
    T = traj.shape[0]
    # align progress: mean |vhat dot vref| over units vs time
    prog = [np.mean([abs(float(traj[t, u] @ vref)) for u in range(8)]) for t in range(T)]
    order = np.argsort(times)
    all_orders.append(order)
    print(f"  seed {s}: align_time per unit = {times}  (T={T})")
    print(f"           mean|dot| progress: first={prog[0]:.2f} mid={prog[T//2]:.2f} "
          f"last={prog[-1]:.2f} | order(align)={order}")

# cross-seed consistency of ordering
o1, o2, o3 = all_orders
from scipy.stats import spearmanr
r12 = spearmanr(o1, o2).statistic
r13 = spearmanr(o1, o3).statistic
r23 = spearmanr(o2, o3).statistic
print(f"  ordering consistency (Spearman): seed12={r12:+.2f} seed13={r13:+.2f} "
      f"seed23={r23:+.2f}  -> {'STABLE (real order)' if min(abs(r12),abs(r13),abs(r23)) > 0.6 else 'random (no identity)'}")
