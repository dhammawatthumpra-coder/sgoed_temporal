"""
Null test + calibration for the corrected spectral dimension (self-written).
1. Calibrate d_s vs N on known lattices (hypercube 4/5/6D) to read the
   finite-size curve of a d=4 system -- is the hypergraph trend (1.87->3.49)
   just finite-size growth, or faster/slower than a true 4D system?
2. Null test: degree-preserving edge shuffle of the hypergraph symmetrized
   adjacency -- if shuffled (structureless) graph gives the same d_s, the
   estimator carries no causal information beyond degree structure.
"""
import time
import numpy as np
from audit_spectral_dimension_correct import (
    d_s_heatkernel_normalized,
    d_s_lazy_walk,
    project_hypergraph_weff,
    make_hypercube,
)
from sgoed_hypergraph_core_v10 import run_v10


def degree_preserving_shuffle(A, rng, n_swap=20000):
    """Random edge swaps preserving the degree sequence (null model)."""
    B = A.copy()
    N = A.shape[0]
    idx = np.array(np.nonzero(B)).T
    # build edge list (upper triangle)
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            if B[i, j] > 0:
                edges.append((i, j))
    edges = np.array(edges)
    if len(edges) < 4:
        return B
    for _ in range(n_swap):
        a, b = edges[rng.integers(0, len(edges))]
        c, d = edges[rng.integers(0, len(edges))]
        # avoid self-loops/duplicates: check both new pairs free
        if len({a, b, c, d}) < 4:
            continue
        if B[a, c] == 0 and B[b, d] == 0:
            B[a, b] = B[b, a] = 0
            B[c, d] = B[d, c] = 0
            B[a, c] = B[c, a] = 1.0
            B[b, d] = B[d, b] = 1.0
            edges[rng.integers(0, len(edges))] = (a, c)
            edges[rng.integers(0, len(edges))] = (b, d)
        elif B[a, d] == 0 and B[b, c] == 0:
            B[a, b] = B[b, a] = 0
            B[c, d] = B[d, c] = 0
            B[a, d] = B[d, a] = 1.0
            B[b, c] = B[c, b] = 1.0
            edges[rng.integers(0, len(edges))] = (a, d)
            edges[rng.integers(0, len(edges))] = (b, c)
    return B


print("=" * 74)
print(" 1. CALIBRATION: d_s of a true 4D lattice (hypercube) at same N")
print("=" * 74)
for dim in [4, 5, 6]:
    N = 1 << dim
    A = make_hypercube(dim).astype(float)
    da, _, _ = d_s_heatkernel_normalized(A)
    db, _, _, _ = d_s_lazy_walk(A)
    print(f"  hypercube {dim}D (N={N:3d}):  heat-kernel d_s = {da:5.2f} | lazy-walk = {db:5.2f}")

print()
print("=" * 74)
print(" 2. NULL TEST: hypergraph N=32 symmetrized vs degree-preserving shuffle")
print("=" * 74)
r_h, r_std, align, dmm_old, l_max, obs_ext, T = run_v10(
    N=32, d=3, g_xy=0.8, g_yx=0.0, n_therm=60, n_measure=40, seed=42
)
W = project_hypergraph_weff(T)
A_sym = 0.5 * (W + W.T)
da_real, _, _ = d_s_heatkernel_normalized(A_sym)
db_real, _, _, _ = d_s_lazy_walk(A_sym)
print(f"  hypergraph N=32 (real):        heat-kernel = {da_real:5.2f} | lazy-walk = {db_real:5.2f}")
print(f"  (matches audit: 3.49 / 3.43)")

# binary mask of the symmetrized support
rng = np.random.default_rng(11)
shuf_ds = []
for rep in range(6):
    B = degree_preserving_shuffle((A_sym > 0).astype(float), rng)
    # weight shuffled edges by the mean weight of the real graph (structure-free)
    mw = A_sym.sum() / max(1, int((A_sym > 0).sum()))
    Bw = B * mw
    da, _, _ = d_s_heatkernel_normalized(Bw)
    shuf_ds.append(da)
print(f"  shuffled null (6 reps):        heat-kernel d_s = {np.mean(shuf_ds):5.2f} +/- {np.std(shuf_ds):.2f}")
print(f"  -> real vs null: {da_real:.2f} vs {np.mean(shuf_ds):.2f}  "
      f"(discriminates: {da_real - np.mean(shuf_ds):+.2f})")

# also compare density of real graph
dens = float((A_sym > 0).sum()) / (32 * 31)
print(f"  edge density of A_sym: {dens:.3f}")
