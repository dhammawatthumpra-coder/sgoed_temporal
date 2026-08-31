"""
v7 feedback — HYSTERESIS with n=30 seeds (2026-08-30).

Confirms the hysteresis loop width with a credible sample (n=5 -> n=30).
Same anneal-continuation method as AUDIT_v7_hysteresis.py, but focused on the
transition band g_YX in {0.8, 1.0, 1.1, 1.2, 1.3, 1.4} (UP and DOWN).

N=6, d=3, g_XY=0.8. n_therm=40. 30 seeds (100..129).
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
import numpy as np
import sgoed_core_v7 as v7

D = 6
SEEDS = list(range(100, 130))
UP = [0.8, 1.0, 1.1, 1.2, 1.3, 1.4]
DOWN = list(reversed(UP))
N_THERM, N_MEAS, EPS = 40, 30, 0.25
N = 6
t0 = time.time()
out = {'up': {}, 'down': {}, 'meta': {}}

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

print(f"=== HYSTERESIS n=30, d=3, N=6, gXY=0.8, gYX {UP} ===", flush=True)
for direction, gseq in [('up', UP), ('down', DOWN)]:
    print(f"\n--- {direction.upper()} (n=30) ---", flush=True)
    per_g = {}
    for s in SEEDS:
        recs = anneal_chain(s, gseq)
        for rec in recs:
            per_g.setdefault(rec['gYX'], []).append(rec['Ymax'])
    for g in gseq:
        vals = np.array(per_g[g])
        hit = (vals >= 9.9).sum()
        out[direction][str(g)] = {
            'Ymax_mean': float(vals.mean()), 'n_hit_gate': int(hit),
            'frac_hit_gate': float(hit / len(vals))}
        print(f"  gYX={g:>4}: Ymax={vals.mean():.3f}  hit={hit}/30 ({hit/len(vals)*100:.0f}%)",
              flush=True)

elapsed = time.time() - t0
out['meta'] = {'elapsed_sec': elapsed, 'seeds': SEEDS, 'up': UP, 'down': DOWN,
               'n_therm': N_THERM}
with open('AUDIT_v7_hysteresis_n30_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nTotal elapsed: {elapsed:.1f}s. Saved AUDIT_v7_hysteresis_n30_results.json")
