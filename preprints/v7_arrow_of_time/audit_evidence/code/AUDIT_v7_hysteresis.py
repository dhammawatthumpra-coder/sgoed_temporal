"""
v7 feedback — HYSTERESIS test for first-order transition (2026-08-30).

Question: is the Y -> gate transition first-order? A first-order transition
shows hysteresis: the critical g_YX when sweeping UP (starting from Y small)
differs from when sweeping DOWN (starting from Y at the gate).

Method: anneal continuously — run the chain at a sequence of g_YX values,
carrying the final X,Y configuration of each step as the initial condition of
the next (no re-randomization). Two chains per seed:
  UP:   g_YX = 0.5 -> 0.8 -> 1.0 -> 1.1 -> 1.2 -> 1.3 -> 1.4 -> 1.6 -> 1.8 -> 2.0
  DOWN: g_YX = 2.0 -> 1.8 -> 1.6 -> 1.4 -> 1.3 -> 1.2 -> 1.1 -> 1.0 -> 0.8 -> 0.5

At each step: n_therm=40, n_meas=30, then record Y_max_extent and ratio.
If first-order, the UP chain stays in the "small" basin longer (higher g_YX
before jumping) than the DOWN chain stays in the "gate" basin (lower g_YX
before falling back) -> a hysteresis loop opens.

N=6, d=3, g_XY=0.8. 5 seeds.
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
import numpy as np
import sgoed_core_v7 as v7

D = 6
SEEDS = [42, 43, 44, 45, 46]
UP = [0.5, 0.8, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 1.8, 2.0]
DOWN = list(reversed(UP))
N_THERM, N_MEAS, EPS = 40, 30, 0.25
t0 = time.time()
out = {'up': {}, 'down': {}, 'meta': {}}

def anneal_chain(seed, gseq):
    """Run Metropolis at successive g_YX, carrying X,Y across steps."""
    rng = np.random.RandomState(seed)
    N = 6
    X = np.zeros((D, N, N))
    for mu in range(D):
        A = rng.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    Y = np.zeros((3, N, N))
    for a in range(3):
        A = rng.randn(N, N) * 0.3
        Y[a] = (A + A.T) / 2

    S = v7.action_v7(X, Y, 0.8, gseq[0])
    records = []
    for gYX in gseq:
        S = v7.action_v7(X, Y, 0.8, gYX)  # recompute with new gYX
        # Metropolis
        for sweep in range(N_THERM + N_MEAS):
            for mu in range(D):
                for i in range(N):
                    for j in range(i, N):
                        old = X[mu, i, j]
                        X[mu, i, j] = old + EPS * rng.randn()
                        if i != j: X[mu, j, i] = X[mu, i, j]
                        Sn = v7.action_v7(X, Y, 0.8, gYX)
                        dS = Sn - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = Sn
                        else:
                            X[mu, i, j] = old
                            if i != j: X[mu, j, i] = old
            for a in range(3):
                for i in range(N):
                    for j in range(i, N):
                        old = Y[a, i, j]
                        Y[a, i, j] = old + EPS * rng.randn()
                        if i != j: Y[a, j, i] = Y[a, i, j]
                        Sn = v7.action_v7(X, Y, 0.8, gYX)
                        dS = Sn - S
                        if dS < 0 or rng.rand() < np.exp(-dS):
                            S = Sn
                        else:
                            Y[a, i, j] = old
                            if i != j: Y[a, j, i] = old
        # observables from final config
        ext = np.array([np.trace(X[mu] @ X[mu]).real / N for mu in range(D)])
        extY = np.array([np.trace(Y[a] @ Y[a]).real / N for a in range(3)])
        k = int(np.argmax(ext))
        ratio = ext[k] / (np.delete(ext, k).mean() + 1e-8)
        records.append({'gYX': gYX, 'Ymax': float(extY.max()), 'ratio': float(ratio)})
    return records

print("=== HYSTERESIS: d=3, N=6, gXY=0.8, anneal UP vs DOWN (n_therm=40) ===", flush=True)
for direction, gseq in [('up', UP), ('down', DOWN)]:
    print(f"\n--- {direction.upper()} sweep ---", flush=True)
    per_g = {}
    for s in SEEDS:
        recs = anneal_chain(s, gseq)
        for rec in recs:
            per_g.setdefault(rec['gYX'], []).append(rec['Ymax'])
    for g in gseq:
        vals = per_g[g]
        out[direction][str(g)] = {
            'Ymax_mean': float(np.mean(vals)),
            'per_seed_Ymax': [round(x, 3) for x in vals]}
        print(f"  gYX={g:>4}: Ymax={np.mean(vals):.3f}  seeds={[round(x,3) for x in vals]}",
              flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'seeds': SEEDS, 'up': UP, 'down': DOWN,
               'n_therm': N_THERM, 'source': 'sgoed_core_v7 action_v7, anneal chain'}
with open('AUDIT_v7_hysteresis_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_hysteresis_results.json")
