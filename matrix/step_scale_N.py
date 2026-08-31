"""
v12 scale check at N=64/96 (self-written).
Q1: does sink-hub (G, D_root, hub_imb, spec) scale with N?
Q2: does lambda_c shift with N?
"""
import sys
import numpy as np
from sgoed_graph_core_v12 import run_v12

N = int(sys.argv[1]) if len(sys.argv) > 1 else 64
lams = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [0.02, 0.03]
seeds = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [42]
therm = int(sys.argv[4]) if len(sys.argv) > 4 else 30
meas = int(sys.argv[5]) if len(sys.argv) > 5 else 5


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
    hub_imb = float(imb[hub])
    # sigma ratio
    s = np.linalg.svd(W, compute_uv=False)
    spec = s[0] / s[1]
    return Dr, G, hub_imb, spec


print(f"N={N} | lam={lams} | seeds={seeds} | therm={therm} meas={meas}")
print(f"  {'lam':>6} | {'spec':>7} | {'D_root':>7} | {'G':>6} | {'hub_imb':>9}")
for lam in lams:
    for s in seeds:
        D, F, spec_r, align, W = run_v12(N=N, d=3, g_xy=1.5, lambda_cond=lam,
                                         n_therm=therm, n_measure=meas, seed=s)
        Dr, G, hub_imb, spec = metrics(W, N)
        print(f"  {lam:6.3f} | {spec:7.2f} | {Dr:+7.2f} | {G:6.3f} | {hub_imb:+9.1f}  (seed {s})")
