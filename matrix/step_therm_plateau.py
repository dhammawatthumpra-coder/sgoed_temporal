"""v12 n_therm plateau check (N=32, 3 seeds): spec/D_root/G at 240/480/960."""
import numpy as np
from sgoed_graph_core_v12 import run_v12


def G_metric(W):
    out = W.sum(1)
    inn = W.sum(0)
    return float(np.sum(np.abs(out - inn))) / (W.sum() + 1e-9)


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


for therm in [240, 480, 960]:
    specs, drs, gs = [], [], []
    for s in [42, 43, 44]:
        D, F, spec, align, W = run_v12(N=32, d=3, g_xy=1.5, lambda_cond=0.15,
                                       n_therm=therm, n_measure=20, seed=s)
        specs.append(spec)
        drs.append(D_root_metric(W))
        gs.append(G_metric(W))
    print(f"  n_therm={therm:4d}: spec={np.mean(specs):6.2f} +/- {np.std(specs):.2f} | "
          f"D_root={np.mean(drs):+.3f} +/- {np.std(drs):.3f} | "
          f"G={np.mean(gs):.4f} +/- {np.std(gs):.4f}")
