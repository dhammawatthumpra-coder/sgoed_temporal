"""
v7 feedback — eigenvalue condensation diagnostic (2026-08-30).

Tests the hypothesis that the Y -> gate bistability comes from eigenvalue
condensation: in the "small" basin Y's eigenvalues are spread out, while in
the "gate" basin a single eigenvalue dominates.

For each seed, run v7 at a given g_YX (n_therm=40), take the FINAL Y matrices,
and for the Y matrix with the largest extent report:
  - extent = Tr(Y^2)/N
  - eigenvalues sorted by |.| descending
  - c = lambda_max^2 / sum(lambda^2)   (fraction of extent in the top eigenvalue)
    c ~ 1/N (spread)  vs  c ~ 1 (condensed)

N=6, d=3, g_XY=0.8. g_YX in {0.5 (small basin), 1.3 (transition)}.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
import numpy as np
import sgoed_core_v7 as v7

D = 6
N = 6
d = 3
GXY = 0.8
N_THERM, N_MEAS, EPS = 40, 30, 0.25
t0 = time.time()
out = {'results': {}, 'meta': {}}

def run_get_eigs(gYX, seed):
    rng = np.random.RandomState(seed)
    X = np.zeros((D, N, N))
    for mu in range(D):
        A = rng.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    Y = np.zeros((d, N, N))
    for a in range(d):
        A = rng.randn(N, N) * 0.3
        Y[a] = (A + A.T) / 2
    S = v7.action_v7(X, Y, GXY, gYX)
    for sweep in range(N_THERM + N_MEAS):
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    old = X[mu, i, j]
                    X[mu, i, j] = old + EPS * rng.randn()
                    if i != j: X[mu, j, i] = X[mu, i, j]
                    Sn = v7.action_v7(X, Y, GXY, gYX)
                    dS = Sn - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = Sn
                    else:
                        X[mu, i, j] = old
                        if i != j: X[mu, j, i] = old
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    old = Y[a, i, j]
                    Y[a, i, j] = old + EPS * rng.randn()
                    if i != j: Y[a, j, i] = Y[a, i, j]
                    Sn = v7.action_v7(X, Y, GXY, gYX)
                    dS = Sn - S
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S = Sn
                    else:
                        Y[a, i, j] = old
                        if i != j: Y[a, j, i] = old
    # find Y with largest extent
    extents = np.array([np.trace(Y[a] @ Y[a]).real / N for a in range(d)])
    a_max = int(np.argmax(extents))
    evals = np.linalg.eigvalsh(Y[a_max])  # ascending
    evals = evals[::-1]  # descending
    top = evals[0]**2 / np.sum(evals**2)
    return {'extent': float(extents[a_max]), 'eigenvalues': evals.tolist(),
            'c_top': float(top)}

print("=== EIGENVALUE CONDENSATION DIAGNOSTIC ===", flush=True)
for gYX, seeds in [(0.5, [42, 43, 44, 45, 46]), (1.3, [42, 43, 44, 45, 46, 100, 101])]:
    print(f"\n--- gYX={gYX} (n_therm={N_THERM}) ---", flush=True)
    for s in seeds:
        r = run_get_eigs(gYX, s)
        out['results'][f"gYX={gYX}|seed={s}"] = r
        ev = r['eigenvalues']
        print(f"  seed={s:>3}: extent={r['extent']:.3f}  c_top={r['c_top']:.3f}  "
              f"eigs(desc)={[round(x,2) for x in ev[:3]]}", flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'N': N, 'D': D, 'd': d, 'gXY': GXY,
               'n_therm': N_THERM}
with open('AUDIT_v7_eigenvalue_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_eigenvalue_results.json")
