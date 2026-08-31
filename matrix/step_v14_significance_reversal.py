"""v14: significance (g=0 vs 0.5) + reversed-start test."""
import sys
import numpy as np
sys.path.insert(0, ".")
from sgoed_matrix_ecosystem_v14 import run_v14, unit_observables, action_v14

print("=" * 78)
print(" 1. SIGNIFICANCE: A(g=0) vs A(g=0.5), M=6, 5 seeds")
print("=" * 78)
A0, A5 = [], []
for s in [42, 43, 44, 45, 46]:
    Xs, Ys = run_v14(M=6, N=4, g_inter=0.0, n_therm=50, n_measure=10, seed=s)
    exts, spec, vhats, A, cs = unit_observables(Xs, Ys)
    A0.append(A)
    Xs, Ys = run_v14(M=6, N=4, g_inter=0.5, n_therm=50, n_measure=10, seed=s)
    exts, spec, vhats, A, cs = unit_observables(Xs, Ys)
    A5.append(A)
A0, A5 = np.array(A0), np.array(A5)
print(f"  g=0  : A = {A0.mean():+.3f} +/- {A0.std():.3f}")
print(f"  g=0.5: A = {A5.mean():+.3f} +/- {A5.std():.3f}")
sep = (A5.mean() - A0.mean()) / np.sqrt(A0.std() ** 2 + A5.std() ** 2 + 1e-9)
print(f"  separation: {sep:.2f} sigma (pooled)")

print()
print("=" * 78)
print(" 2. REVERSED-START: run g=0.5, then restart with Y -> -Y (flip v_hat)")
print("=" * 78)
s = 42
Xs, Ys = run_v14(M=6, N=4, g_inter=0.5, n_therm=50, n_measure=10, seed=s)
exts, spec, vhats, A1, cs = unit_observables(Xs, Ys)
print(f"  run1: A = {A1:+.3f} | v_hat mean dot = "
      f"{np.mean([vhats[u] @ vhats[v] for u in range(6) for v in range(u+1,6)]):+.3f}")

# reversed: same X init, flipped observer directions
rng = np.random.RandomState(s + 1000)
Ys_r = -Ys.copy()  # flip direction
Xs_r = Xs.copy()
# re-thermalize briefly with flipped observer
def flip_run(Xs, Ys, n_therm=25, n_measure=5, step=0.15, g_inter=0.5):
    rng2 = np.random.RandomState(s + 2000)
    S = action_v14(Xs, Ys, g_inter)
    for _ in range(n_therm + n_measure):
        for u in range(6):
            for mu in range(2):
                for i in range(4):
                    for j in range(i, 4):
                        old = Xs[u, mu, i, j]
                        Xs[u, mu, i, j] = old + step * rng2.randn()
                        if i != j:
                            Xs[u, mu, j, i] = Xs[u, mu, i, j]
                        S2 = action_v14(Xs, Ys, g_inter)
                        dS = S2 - S
                        if dS < 0 or rng2.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Xs[u, mu, i, j] = old
                            if i != j:
                                Xs[u, mu, j, i] = old
            for a in range(2):
                for i in range(4):
                    for j in range(i, 4):
                        old = Ys[u, a, i, j]
                        Ys[u, a, i, j] = old + step * rng2.randn()
                        if i != j:
                            Ys[u, a, j, i] = Ys[u, a, i, j]
                        S2 = action_v14(Xs, Ys, g_inter)
                        dS = S2 - S
                        if dS < 0 or rng2.rand() < np.exp(-dS):
                            S = S2
                        else:
                            Ys[u, a, i, j] = old
                            if i != j:
                                Ys[u, a, j, i] = old
    return Xs, Ys

Xs_r, Ys_r = flip_run(Xs_r, Ys_r)
exts, spec, vhats_r, A_r, cs = unit_observables(Xs_r, Ys_r)
print(f"  reversed: A = {A_r:+.3f} | v_hat dot mean = "
      f"{np.mean([vhats_r[u] @ vhats_r[v] for u in range(6) for v in range(u+1,6)]):+.3f}")
# did observer direction flip back?
dot_back = np.mean([float(vhats_r[u] @ vhats[u]) for u in range(6)])
print(f"  corr(v_hat_rev, v_hat_orig) = {dot_back:+.3f}  "
      f"({'flipped BACK (attractor)' if dot_back > 0.3 else 'stayed flipped (symmetric)'})")
