"""
v12 labeling-invariant direction metrics (self-written, data honesty).
D (sign count over i<j) is labeling-dependent. Test 4 INVARIANT metrics:
  1. S  = (n_source - n_sink)/N   (node imbalance signs - permutation invariant)
  2. D_root = hub net direction normalized: node with max|out-in| vs all others
  3. imb_norm = mean|out-in| / mean W  (imbalance magnitude, scale-free)
  4. F_norm = F_net / sum(W)      (total asymmetry fraction)
Sanity: metrics must be invariant under label permutation.
Compare: real (lambda=0.15) vs baseline (uncoupled).
"""
import numpy as np
from sgoed_graph_core_v12 import run_v12


def invariants(W, d=3):
    N = W.shape[0]
    out = W.sum(1)
    inn = W.sum(0)
    imb = out - inn
    n_src = int((imb > 1e-6).sum())
    n_snk = int((imb < -1e-6).sum())
    S = (n_src - n_snk) / N
    h = int(np.argmax(np.abs(imb)))
    D_root = 0.0
    for j in range(N):
        if j == h:
            continue
        f = W[h, j] - W[j, h]
        if abs(f) > 1e-4:
            D_root += np.sign(f)
    D_root_norm = D_root / (N - 1)
    mw = W.sum() / (N * (N - 1)) + 1e-9
    imb_norm = np.mean(np.abs(imb)) / mw
    F_net = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            F_net += W[i, j] - W[j, i]
    F_norm = F_net / (W.sum() + 1e-9)
    return S, D_root_norm, imb_norm, F_norm


def run_scan(N, g_xy, lam, seeds, therm=40):
    res = {k: [] for k in ["S", "D_root", "imb_norm", "F_norm", "spec", "align"]}
    for s in seeds:
        D, F, spec, align, W = run_v12(N=N, d=3, g_xy=g_xy, lambda_cond=lam,
                                       n_therm=therm, n_measure=20, seed=s)
        S, Dr, imb, Fn = invariants(W)
        res["S"].append(S)
        res["D_root"].append(Dr)
        res["imb_norm"].append(imb)
        res["F_norm"].append(Fn)
        res["spec"].append(spec)
        res["align"].append(align)
    return res


seeds10 = list(range(42, 52))
print("=" * 78)
print(" 1. N=32: REAL (lambda=0.15) vs BASELINE (uncoupled), 10 seeds")
print("=" * 78)
for tag, g, lam in [("baseline", 0.0, 0.0), ("real", 1.5, 0.15)]:
    r = run_scan(32, g, lam, seeds10)
    print(f"\n  [{tag}]")
    print(f"    S (src-sink)/N      : {np.mean(r['S']):+.3f} +/- {np.std(r['S']):.3f}")
    print(f"    D_root (hub dir)    : {np.mean(r['D_root']):+.3f} +/- {np.std(r['D_root']):.3f}")
    print(f"    imb_norm (|out-in|) : {np.mean(r['imb_norm']):.3f} +/- {np.std(r['imb_norm']):.3f}")
    print(f"    F_norm (asym frac)  : {np.mean(r['F_norm']):+.4f} +/- {np.std(r['F_norm']):.4f}")
    print(f"    spec                : {np.mean(r['spec']):.2f} +/- {np.std(r['spec']):.2f}")
    print(f"    align               : {np.mean(r['align'])*100:.0f}%")

print()
print("=" * 78)
print(" 2. PERMUTATION INVARIANCE SANITY (real N=32 seed 42)")
print("=" * 78)
_, _, _, _, W = run_v12(N=32, d=3, g_xy=1.5, lambda_cond=0.15,
                        n_therm=40, n_measure=20, seed=42)
base = invariants(W)
print(f"    original: S={base[0]:+.3f} D_root={base[1]:+.3f} imb={base[2]:.3f} F={base[3]:+.4f}")
rng = np.random.default_rng(5)
for rep in range(5):
    perm = rng.permutation(W.shape[0])
    Wp = W[np.ix_(perm, perm)]
    v = invariants(Wp)
    print(f"    perm {rep}: S={v[0]:+.3f} D_root={v[1]:+.3f} imb={v[2]:.3f} F={v[3]:+.4f}")

print()
print("=" * 78)
print(" 3. N=48: real vs baseline (10 seeds)")
print("=" * 78)
for tag, g, lam in [("baseline", 0.0, 0.0), ("real", 1.5, 0.15)]:
    r = run_scan(48, g, lam, seeds10, therm=40)
    print(f"\n  [{tag}]")
    print(f"    S (src-sink)/N      : {np.mean(r['S']):+.3f} +/- {np.std(r['S']):.3f}")
    print(f"    D_root (hub dir)    : {np.mean(r['D_root']):+.3f} +/- {np.std(r['D_root']):.3f}")
    print(f"    imb_norm (|out-in|) : {np.mean(r['imb_norm']):.3f} +/- {np.std(r['imb_norm']):.3f}")
    print(f"    F_norm (asym frac)  : {np.mean(r['F_norm']):+.4f} +/- {np.std(r['F_norm']):.4f}")
    print(f"    spec                : {np.mean(r['spec']):.2f} +/- {np.std(r['spec']):.2f}")
