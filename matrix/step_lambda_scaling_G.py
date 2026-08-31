"""
v12 workplan: lambda->0 scaling + global invariant metric G (self-written).
G = sum_i |out_i - in_i| / sum_{i!=j} W_ij  (global imbalance fraction)
  - permutation-invariant by construction (sum of node properties)
  - 0 = fully balanced, 1 = all flow concentrated in one direction
Q1: lambda -> 0: does condensation/D_root/G decay continuously (engineered)
    or show a jump/plateau (phase transition / possible emergence)?
Q2: G invariant sanity + discrimination baseline vs real.
"""
import numpy as np
from sgoed_graph_core_v12 import run_v12


def G_metric(W):
    out = W.sum(1)
    inn = W.sum(0)
    imb = out - inn
    return float(np.sum(np.abs(imb))) / (W.sum() + 1e-9)


def D_root_metric(W):
    N = W.shape[0]
    imb = W.sum(1) - W.sum(0)
    hub = int(np.argmax(np.abs(imb)))
    Dr = 0.0
    for j in range(N):
        if j == hub:
            continue
        f = W[hub, j] - W[j, hub]
        if abs(f) > 1e-4:
            Dr += np.sign(f)
    return Dr / (N - 1)


print("=" * 80)
print(" Q2 first: G permutation invariance sanity (N=32 real, seed 42)")
print("=" * 80)
D, F, spec, align, W = run_v12(N=32, d=3, g_xy=1.5, lambda_cond=0.15,
                               n_therm=40, n_measure=20, seed=42)
g0 = G_metric(W)
rng = np.random.default_rng(3)
gperms = []
for rep in range(6):
    perm = rng.permutation(32)
    gperms.append(G_metric(W[np.ix_(perm, perm)]))
print(f"  G original = {g0:.4f} | perms = {[f'{g:.4f}' for g in gperms]} "
      f"-> invariant: {max(abs(g - g0) for g in gperms) < 1e-12}")

print()
print("=" * 80)
print(" Q1: lambda_cond -> 0 scaling (N=32, 10 seeds, n_therm=40)")
print("=" * 80)
lams = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.08, 0.12, 0.2, 0.3]
print(f"  {'lambda':>7} | {'spec':>7} | {'D_root':>7} | {'G':>7} | {'S':>6}")
for lam in lams:
    specs, drs, gs, Ss = [], [], [], []
    for s in range(42, 52):
        D, F, spec, align, W = run_v12(N=32, d=3, g_xy=1.5, lambda_cond=lam,
                                       n_therm=40, n_measure=20, seed=s)
        specs.append(spec)
        drs.append(D_root_metric(W))
        gs.append(G_metric(W))
        imb = W.sum(1) - W.sum(0)
        Ss.append(((imb > 1e-6).sum() - (imb < -1e-6).sum()) / 32)
    print(f"  {lam:7.3f} | {np.mean(specs):7.2f} | {np.mean(drs):+7.2f} | "
          f"{np.mean(gs):7.4f} | {np.mean(Ss):+6.2f}")
