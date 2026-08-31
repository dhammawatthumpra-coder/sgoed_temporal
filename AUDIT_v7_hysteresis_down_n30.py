"""
v7 feedback — DOWN sweep only, n=30, incremental save (2026-08-30).

Re-runs just the DOWN hysteresis sweep (g_YX 1.4 -> 0.8) that was killed by
the time limit in the combined run. Saves results incrementally after each
seed so partial data survives any interruption.

N=6, d=3, g_XY=0.8, n_therm=40, 30 seeds (100..129).
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
import numpy as np
import sgoed_core_v7 as v7

D = 6
SEEDS = list(range(100, 130))
DOWN = [1.4, 1.3, 1.2, 1.1, 1.0, 0.8]
N_THERM, N_MEAS, EPS = 40, 30, 0.25
N = 6
OUTFILE = 'AUDIT_v7_hysteresis_down_n30_results.json'
t0 = time.time()

def anneal_chain(seed, gseq):
    rng = np.random.RandomState(seed)
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
        S = v7.action_v7(X, Y, 0.8, gYX)
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
        extY = np.array([np.trace(Y[a] @ Y[a]).real / N for a in range(3)])
        records.append({'gYX': gYX, 'Ymax': float(extY.max())})
    return records

print(f"=== DOWN SWEEP ONLY n=30 (gYX {DOWN}) ===", flush=True)
per_g = {g: [] for g in DOWN}
for idx, s in enumerate(SEEDS):
    recs = anneal_chain(s, DOWN)
    for rec in recs:
        per_g[rec['gYX']].append(rec['Ymax'])
    # incremental save
    snapshot = {str(g): {'Ymax_mean': float(np.mean(v)), 'n': len(v),
                         'n_hit_gate': int(sum(1 for x in v if x >= 9.9)),
                         'values': v} for g, v in per_g.items() if v}
    json.dump(snapshot, open(OUTFILE, 'w'), indent=2)
    print(f"  [seed {s}] done ({idx+1}/30) | "
          + " | ".join(f"g{g}: {np.mean(per_g[g]):.2f}" for g in DOWN), flush=True)

elapsed = time.time() - t0
final = {str(g): {'Ymax_mean': float(np.mean(v)),
                  'n_hit_gate': int(sum(1 for x in v if x >= 9.9)),
                  'frac_hit_gate': float(sum(1 for x in v if x >= 9.9) / len(v)),
                  'values': v} for g, v in per_g.items()}
final['meta'] = {'elapsed_sec': elapsed, 'seeds': SEEDS, 'down': DOWN, 'n_therm': N_THERM}
json.dump(final, open(OUTFILE, 'w'), indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved {OUTFILE}")
