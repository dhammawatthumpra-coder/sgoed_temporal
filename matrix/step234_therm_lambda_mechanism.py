"""v12 workplan steps 2/3/4: therm 240, lambda_cond scan, D<0 mechanism."""
import numpy as np
from sgoed_graph_core_v12 import run_v12

print("=" * 72)
print(" STEP 2: N=32, n_therm=240 vs 40 (spec plateau?)")
print("=" * 72)
for therm in [40, 120, 240]:
    Ds, specs = [], []
    for s in [42, 43, 44, 45, 46]:
        D, F, spec, align, W = run_v12(
            N=32, d=3, g_xy=1.5, lambda_cond=0.15,
            n_therm=therm, n_measure=40, seed=s
        )
        Ds.append(D)
        specs.append(spec)
    print(f"  n_therm={therm:3d}: D={np.mean(Ds):+7.1f} +/- {np.std(Ds):5.1f} | "
          f"spec={np.mean(specs):5.2f} +/- {np.std(specs):.2f}")

print()
print("=" * 72)
print(" STEP 4: lambda_cond scaling at N=32 (10 seeds, n_therm=40)")
print("=" * 72)
for lam in [0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]:
    Ds, specs = [], []
    for s in range(42, 52):
        D, F, spec, align, W = run_v12(
            N=32, d=3, g_xy=1.5, lambda_cond=lam,
            n_therm=40, n_measure=40, seed=s
        )
        Ds.append(D)
        specs.append(spec)
    sig = abs(np.mean(Ds)) / (np.std(Ds) + 1e-9)
    print(f"  lam={lam:.2f}: D={np.mean(Ds):+7.1f} +/- {np.std(Ds):5.1f} (sig {sig:4.1f}) | "
          f"spec={np.mean(specs):5.2f} +/- {np.std(specs):.2f}")

print()
print("=" * 72)
print(" STEP 3: D<0 mechanism -- region analysis (N=32, seed 42, n_therm=120)")
print("=" * 72)
D, F, spec, align, W = run_v12(N=32, d=3, g_xy=1.5, lambda_cond=0.15,
                               n_therm=120, n_measure=40, seed=42)
N = W.shape[0]
d = 3
obs = list(range(d))
sys = list(range(d, N))


def D_between(W, A, B):
    Ds = 0
    for i in A:
        for j in B:
            if i == j:
                continue
            f = W[i, j] - W[j, i]
            if abs(f) > 1e-4:
                Ds += np.sign(f)
    return Ds


D_oo = D_between(W, obs, obs)
D_os = D_between(W, obs, sys)
D_ss = D_between(W, sys, sys)
out = W.sum(axis=1)
inn = W.sum(axis=0)
print(f"  D_total={D:+.0f}  (max {N*(N-1)//2})")
print(f"  D_obs-obs={D_oo:+.0f} ({len(obs)*(len(obs)-1)//2} pairs) | "
      f"D_obs-sys={D_os:+.0f} ({d*(N-d)} pairs) | D_sys-sys={D_ss:+.0f} ({(N-d)*(N-d-1)//2} pairs)")
print(f"  observer nodes out-in: {[f'{out[i]-inn[i]:+.2f}' for i in obs]}")
print(f"  sys nodes out-in:      {[f'{out[j]-inn[j]:+.2f}' for j in sys]}")
# top nodes by row norm (who is the hub?)
row_norm = np.linalg.norm(W, axis=1)
top = np.argsort(row_norm)[::-1][:6]
print(f"  top-6 nodes by row-norm: {top}  norms={[f'{row_norm[t]:.2f}' for t in top]}")
print(f"  their out-in: {[f'{out[t]-inn[t]:+.2f}' for t in top]}")
# which pairs dominate negative D?
neg_pairs = 0
pos_pairs = 0
for i in range(N):
    for j in range(i + 1, N):
        f = W[i, j] - W[j, i]
        if abs(f) > 1e-4:
            if f < 0:
                neg_pairs += 1
            else:
                pos_pairs += 1
print(f"  pairs: negative={neg_pairs}, positive={pos_pairs}")
# correlation: is D<0 driven by node index ordering (i<j -> W_ij < W_ji)?
avg_ratio = []
for i in range(N):
    for j in range(i + 1, N):
        avg_ratio.append(W[i, j] / (W[j, i] + 1e-9))
print(f"  mean W_ij/W_ji (i<j) = {np.mean(avg_ratio):.3f} -> "
      f"{'low-index nodes receive MORE (D<0)' if np.mean(avg_ratio) < 1 else 'low-index send MORE'}")
