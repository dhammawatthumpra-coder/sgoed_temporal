"""
v12 lambda_c fine scan (self-written, data honesty).
Fine scan 0.015..0.055 step 0.005 to locate the condensation threshold jump.
Also: n_therm sensitivity at the critical point (lambda=0.03).
Metrics: spec, D_root, G, S + fraction of seeds condensed (G > 0.8).
"""
import numpy as np
from sgoed_graph_core_v12 import run_v12


def metrics(W, N):
    out = W.sum(1)
    inn = W.sum(0)
    imb = out - inn
    G = float(np.sum(np.abs(imb))) / (W.sum() + 1e-9)
    hub = int(np.argmax(np.abs(imb)))
    Dr = 0.0
    for j in range(N):
        if j == hub:
            continue
        f = W[hub, j] - W[j, hub]
        if abs(f) > 1e-4:
            Dr += np.sign(f)
    Dr /= (N - 1)
    S = ((imb > 1e-6).sum() - (imb < -1e-6).sum()) / N
    return Dr, G, S


print("=" * 84)
print(" FINE lambda_c scan: N=32, 10 seeds, n_therm=40")
print("=" * 84)
lams = [0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045, 0.050, 0.055, 0.060]
print(f"  {'lambda':>6} | {'spec':>6} | {'D_root':>7} | {'G':>6} | {'S':>6} | condensed seeds")
for lam in lams:
    specs, drs, gs, Ss, n_cond = [], [], [], [], 0
    for s in range(42, 52):
        D, F, spec, align, W = run_v12(N=32, d=3, g_xy=1.5, lambda_cond=lam,
                                       n_therm=40, n_measure=20, seed=s)
        Dr, G, S = metrics(W, 32)
        specs.append(spec)
        drs.append(Dr)
        gs.append(G)
        Ss.append(S)
        if G > 0.8:
            n_cond += 1
    print(f"  {lam:6.3f} | {np.mean(specs):6.2f} | {np.mean(drs):+7.2f} | "
          f"{np.mean(gs):6.3f} | {np.mean(Ss):+6.2f} | {n_cond}/10")

print()
print("=" * 84)
print(" n_therm sensitivity at critical lambda=0.030 (10 seeds)")
print("=" * 84)
for therm in [40, 120, 240]:
    specs, gs = [], []
    for s in range(42, 52):
        D, F, spec, align, W = run_v12(N=32, d=3, g_xy=1.5, lambda_cond=0.03,
                                       n_therm=therm, n_measure=20, seed=s)
        Dr, G, S = metrics(W, 32)
        specs.append(spec)
        gs.append(G)
    print(f"  n_therm={therm:3d}: spec={np.mean(specs):6.2f} +/- {np.std(specs):.2f} | "
          f"G={np.mean(gs):.3f} +/- {np.std(gs):.3f} | condensed {int(np.mean([g > 0.8 for g in gs])*10)}/10")
