"""
Matrix v7 condensation-ratio discrimination audit (self-written, data honesty).
================================================================================
Metric: ratio = max_mu Tr(X_mu^2)/N / mean(rest)  (+ alignment).
Questions:
  1. Baseline at gXY=0 (no coupling): what is ratio naturally?
  2. Null random initial X: what is ratio for uncoupled random matrices?
  3. Real gXY=0.8/1.05: is ratio >> baseline (discriminates)?
  4. Eigenvalue spectrum of the dominant X_mu: genuine condensation
     (single large eigenvalue) or just overall growth?
"""
import numpy as np
import sys
sys.path.insert(0, "../code")
from sgoed_core_v7 import action_v7


def run_with_final(N, D, d, gXY, gYX, seed, n_therm=40, n_meas=10, eps=0.25,
                   max_extent=10.0):
    rng = np.random.RandomState(seed)
    X = np.zeros((D, N, N))
    for mu in range(D):
        A = rng.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    Y = np.zeros((d, N, N))
    for a in range(d):
        A = rng.randn(N, N) * 0.3
        Y[a] = (A + A.T) / 2
    S_curr = action_v7(X, Y, gXY, gYX, max_extent)

    for sweep in range(n_therm + n_meas):
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    old = X[mu, i, j]
                    X[mu, i, j] = old + eps * rng.randn()
                    if i != j:
                        X[mu, j, i] = X[mu, i, j]
                    S_new = action_v7(X, Y, gXY, gYX, max_extent)
                    dS = S_new - S_curr
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S_curr = S_new
                    else:
                        X[mu, i, j] = old
                        if i != j:
                            X[mu, j, i] = old
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    old = Y[a, i, j]
                    Y[a, i, j] = old + eps * rng.randn()
                    if i != j:
                        Y[a, j, i] = Y[a, i, j]
                    S_new = action_v7(X, Y, gXY, gYX, max_extent)
                    dS = S_new - S_curr
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S_curr = S_new
                    else:
                        Y[a, i, j] = old
                        if i != j:
                            Y[a, j, i] = old

    ext = np.array([np.trace(X[mu] @ X[mu]).real / N for mu in range(D)])
    v_hat = np.zeros(D)
    tracesY = np.array([np.trace(Y[a]).real for a in range(d)])
    v_hat[:min(d, D)] = tracesY[:min(d, D)]
    nrm = np.linalg.norm(v_hat)
    v_hat = v_hat / (nrm + 1e-8) if nrm > 1e-8 else np.zeros(D)
    k = int(np.argmax(ext))
    ratio = ext[k] / (np.delete(ext, k).mean() + 1e-8)
    align = int(k == int(np.argmax(np.abs(v_hat))))
    evals = np.linalg.eigvalsh(X[k])
    return ratio, align, ext, evals, X


print("=" * 74)
print(" 1. BASELINE gXY=0.0 (no coupling) vs NULL random initial (sweep 0)")
print("=" * 74)
N, D, d = 8, 3, 2
seeds = [42, 43, 44, 45, 46]

# null: initial random X (no simulation)
ratios0, aligns0 = [], []
for s in seeds:
    rng = np.random.RandomState(s)
    X0 = np.zeros((D, N, N))
    for mu in range(D):
        A = rng.randn(N, N) * 0.5
        X0[mu] = (A + A.T) / 2
    ext0 = np.array([np.trace(X0[mu] @ X0[mu]).real / N for mu in range(D)])
    ratios0.append(ext0.max() / (np.delete(ext0, ext0.argmax()).mean() + 1e-8))
print(f"  [null random init] ratio = {np.mean(ratios0):.3f} +/- {np.std(ratios0):.3f}")

r, a = [], []
for s in seeds:
    ratio, align, ext, ev, X = run_with_final(N, D, d, 0.0, 0.0, s)
    r.append(ratio)
    a.append(align)
print(f"  [baseline gXY=0]  ratio = {np.mean(r):.3f} +/- {np.std(r):.3f} | "
      f"alignment = {np.mean(a)*100:.0f}%")

print()
print("=" * 74)
print(" 2. REAL gXY=0.8 and gXY=1.05 (gate)")
print("=" * 74)
for gxy in [0.8, 1.05]:
    r, a = [], []
    for s in seeds:
        ratio, align, ext, ev, X = run_with_final(N, D, d, gxy, 0.0, s)
        r.append(ratio)
        a.append(align)
    print(f"  gXY={gxy:.2f}: ratio = {np.mean(r):.3f} +/- {np.std(r):.3f} | "
          f"alignment = {np.mean(a)*100:.0f}%")

print()
print("=" * 74)
print(" 3. EIGENVALUE SPECTRUM of dominant X_mu (gXY=0.8 vs baseline)")
print("=" * 74)
ratio, align, ext, ev, X = run_with_final(N, D, d, 0.8, 0.0, 42)
k = int(np.argmax(ext))
print(f"  gXY=0.8 dominant X[{k}] eigenvalues (N=8): "
      f"{np.array2string(ev, precision=3)}")
print(f"  -> |lambda_max|/|lambda_2nd| = {abs(ev[-1])/max(abs(ev[-2]),1e-9):.2f} "
      f"(>>1 = true rank-1 condensation)")
ratio, align, ext, ev, X = run_with_final(N, D, d, 0.0, 0.0, 42)
k = int(np.argmax(ext))
print(f"  gXY=0   dominant X[{k}] eigenvalues: "
      f"{np.array2string(ev, precision=3)}")
print(f"  -> |lambda_max|/|lambda_2nd| = {abs(ev[-1])/max(abs(ev[-2]),1e-9):.2f}")
