"""
v13 critical check (self-written, data honesty).
1. Baseline (g_f=0, g_b=0) vs asymmetric (g_b=0.2, p_b=2): D, G, D_root
2. G = sum|out-in|/sum W (labeling-invariant) discrimination
3. D permutation test: does D change under sys-label permutation?
4. D_root: what is it really? (argmax out_deg -> positive by construction?)
"""
import numpy as np
from sgoed_graph_core_v13 import run_v13


def G_metric(W):
    out = W.sum(1)
    inn = W.sum(0)
    return float(np.sum(np.abs(out - inn))) / (W.sum() + 1e-9)


def D_metric(W, N):
    D = 0
    for i in range(N):
        for j in range(i + 1, N):
            f = W[i, j] - W[j, i]
            if abs(f) > 1e-4:
                D += np.sign(f)
    return D


def D_root_metric(W, N):
    out = W.sum(1)
    inn = W.sum(0)
    root = int(np.argmax(out))
    return float(out[root] - inn[root]), root, out[root], inn[root]


print("=" * 78)
print(" 1. N=32, 10 seeds: baseline (0,0) vs forward (1.5,0) vs asym (1.5,0.2,p2)")
print("=" * 78)
for g_f, g_b, p_b, tag in [(0.0, 0.0, 2, "baseline (0,0)"),
                           (1.5, 0.0, 2, "forward only"),
                           (1.5, 0.2, 2, "asym g_b=0.2 p2")]:
    Ds, Gs, Droots, specs = [], [], [], []
    for s in range(42, 52):
        D, Dr, spec, align, W = run_v13(N=32, d=3, g_f=g_f, g_b=g_b, p_b=p_b,
                                        n_therm=120, n_measure=30, seed=s)
        Ds.append(D)
        Gs.append(G_metric(W))
        Droots.append(Dr)
        specs.append(spec)
    print(f"  [{tag}]")
    print(f"    D      : {np.mean(Ds):+6.1f} +/- {np.std(Ds):5.1f}  (sig {abs(np.mean(Ds))/(np.std(Ds)+1e-9):.1f})")
    print(f"    G      : {np.mean(Gs):.3f} +/- {np.std(Gs):.3f}")
    print(f"    D_root : {np.mean(Droots):+6.1f} (N=32) | spec: {np.mean(specs):.2f}")

print()
print("=" * 78)
print(" 2. D permutation test (asym g_b=0.2, seed 42)")
print("=" * 78)
D, Dr, spec, align, W = run_v13(N=32, d=3, g_f=1.5, g_b=0.2, p_b=2,
                                n_therm=120, n_measure=30, seed=42)
N = 32
D0 = D_metric(W, N)
rng = np.random.default_rng(1)
Ds = []
for rep in range(10):
    perm = list(range(3)) + list(rng.permutation(range(3, N)))
    Wp = W[np.ix_(perm, perm)]
    Ds.append(D_metric(Wp, N))
print(f"  D original = {D0:+.0f} | sys-label perm: {np.mean(Ds):+.1f} +/- {np.std(Ds):.1f} "
      f"range [{min(Ds):+.0f}, {max(Ds):+.0f}]")

print()
print("=" * 78)
print(" 3. D_root anatomy (asym g_b=0.2, seed 42): is it trivially positive?")
print("=" * 78)
Dr, root, out_r, in_r = D_root_metric(W, N)
print(f"  D_root = {Dr:+.1f} (root node {root}, out={out_r:.1f}, in={in_r:.1f})")
print(f"  -> node with max out_deg: out-in = {Dr:+.1f}")
print(f"  argmax out_deg node: is it an observer node? {root < 3}")
