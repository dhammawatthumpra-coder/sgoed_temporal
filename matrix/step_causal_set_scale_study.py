"""
SGOED v15 — Track 2: Scale & Significance of Causal-Set Branching dimension
===========================================================================
Three parts (per the approved blueprint):

1. Fine p-grid near 4D at N=250, >=10 seeds/point:
   p in [0.005, 0.008, 0.012, 0.016, 0.020, 0.025, 0.030]
2. Finite-size scaling N in {250, 500, 1000}:
   - fixed-p  (p in {0.02, 0.03}): dimension invariant -> p-property
   - fixed-k  (k in {2.0, 5.0, 7.5}, p = k/N): invariant -> percolation scaling
3. Calibration grid extended to d = 8, rebuilt PER N (finite-size effect
   in the sprinkling box).

Acceptance (auto-verdict at the end):
   PASS : some p-range gives d_MM = 4.0 ± 0.1 over >=10 seeds AND survives
          N -> 1000 under the correct scaling variable.
   NEG  : strong N-dependence without scaling invariance -> record as
          random-percolation limitation.

Technical note: transitive closure uses Python-int bitset reachability
(O(E * N/word)), avoiding both int8 matmul overflow (N>15) and the
N=1000^3 matrix-multiply cost.
"""
import json
import numpy as np


def sprinkle_rho(seed, N, dim, T=10.0, L=10.0):
    rng = np.random.RandomState(seed)
    pts = rng.uniform(0.0, 1.0, (N, dim))
    pts[:, 0] *= T
    pts[:, 1:] *= L
    C = 0
    for i in range(N):
        dt = pts[i + 1:, 0] - pts[i, 0]
        if dim == 1:
            dsp = np.zeros(N - i - 1)
        else:
            dsp = np.sqrt(((pts[i + 1:, 1:] - pts[i, 1:]) ** 2).sum(axis=1))
        C += int((dt > dsp).sum())
    return C / (N * (N - 1) / 2)


def bern_closure_rho(seed, N, p):
    rng = np.random.RandomState(seed)
    ii, jj = np.triu_indices(N, 1)
    keep = rng.rand(len(ii)) < p
    children = [[] for _ in range(N)]
    for i, j in zip(ii[keep], jj[keep]):
        children[i].append(int(j))
    reach = [1 << i for i in range(N)]
    C = 0
    for i in range(N - 1, -1, -1):
        for j in children[i]:
            reach[i] |= reach[j]
        C += (reach[i] & ~(1 << i)).bit_count()
    return C / (N * (N - 1) / 2)


def calibration(N, seeds=10):
    ds = np.arange(1, 9, dtype=float)
    rhos = [1.0]  # chain anchor d=1
    for d in range(2, 9):
        vals = [sprinkle_rho(s, N, d) for s in range(42, 42 + seeds)]
        rhos.append(float(np.mean(vals)))
    return ds, np.array(rhos)


def read_dim(rho, ds, rhos):
    if rho >= rhos[0]:
        return 1.0
    if rho <= rhos[-1]:
        return 8.0
    idx = np.searchsorted(-rhos, -rho)
    d_lo, d_hi = ds[idx - 1], ds[idx]
    r_lo, r_hi = rhos[idx - 1], rhos[idx]
    return float(d_lo + (rho - r_lo) / (r_hi - r_lo) * (d_hi - d_lo))


if __name__ == "__main__":
    # ---- sanity self-tests ----
    assert abs(bern_closure_rho(1, 200, 1.0) - 1.0) < 1e-9, "chain closure != 1"
    r2 = np.mean([sprinkle_rho(s, 250, 2) for s in range(42, 45)])
    assert abs(r2 - 0.252) < 0.03, f"2D sprinkle drifted: {r2:.4f}"

    Ns = [250, 500, 1000]
    cal = {}
    for N in Ns:
        ds, rhos = calibration(N, seeds=10)
        cal[str(N)] = {"d": ds.tolist(), "rho": rhos.tolist()}
        print(f"cal N={N}: " + " ".join(f"d={int(d)}:rho={r:.4f}" for d, r in zip(ds, rhos)))

    out = {"calibration": cal, "fine_grid": {}, "fixed_p": {}, "fixed_k": {}}

    # ---- 1) fine grid at N=250 ----
    fine_p = [0.005, 0.008, 0.012, 0.016, 0.020, 0.025, 0.030]
    ds250, rho250 = np.array(cal["250"]["d"]), np.array(cal["250"]["rho"])
    print("\nFINE GRID (N=250, 12 seeds/point):")
    for p in fine_p:
        dims = [read_dim(bern_closure_rho(s, 250, p), ds250, rho250) for s in range(42, 54)]
        m, sd = float(np.mean(dims)), float(np.std(dims))
        print(f"  p={p:.3f}: d_MM = {m:.2f} ± {sd:.2f}")
        out["fine_grid"][str(p)] = {"mean": m, "std": sd}
    best_p = min(out["fine_grid"], key=lambda s: abs(out["fine_grid"][s]["mean"] - 4.0))
    out["fine_best"] = {"p": best_p, **out["fine_grid"][best_p]}
    print(f"  -> nearest to 4D: p={best_p} -> d={out['fine_grid'][best_p]['mean']:.2f}")

    # ---- 2) finite-size scaling ----
    for kind, labels, vals in [("fixed_p", [0.02, 0.03], [0.02, 0.03]),
                               ("fixed_k", [2.0, 5.0, 7.5], [2.0, 5.0, 7.5])]:
        print(f"\n{kind.upper()} SCALING ({'p' if kind=='fixed_p' else 'k'}):")
        for v in vals:
            dims_by_N = []
            for N in Ns:
                p = v if kind == "fixed_p" else v / N
                dn = np.array(cal[str(N)]["d"])
                rn = np.array(cal[str(N)]["rho"])
                dims = [read_dim(bern_closure_rho(s, N, p), dn, rn) for s in range(42, 52)]
                m = float(np.mean(dims))
                dims_by_N.append(m)
                print(f"  {kind[-1]}={v:>4} N={N:5d}: d_MM = {m:.2f}")
            out[kind][str(v)] = {f"N{N}": round(d, 3) for N, d in zip(Ns, dims_by_N)}
            out[kind][str(v)]["std_across_N"] = round(float(np.std(dims_by_N)), 3)

    # ---- 3) acceptance verdict ----
    fp = out["fixed_p"]
    fk = out["fixed_k"]
    best_p_val = float(best_p)
    best_d = out["fine_grid"][best_p]["mean"]
    n4 = sum(1 for s in out["fine_grid"].values() if abs(s["mean"] - 4.0) <= 0.1)
    n4_seeds = None
    if n4 > 0:
        p4 = best_p_val
        dims4 = [read_dim(bern_closure_rho(s, 250, p4), ds250, rho250) for s in range(42, 54)]
        n4_seeds = sum(1 for d in dims4 if abs(d - 4.0) <= 0.1)
    verdict = []
    verdict.append(f"fine-grid: {n4}/7 points within d=4.0±0.1; nearest={best_p_val} -> d={best_d:.2f}")
    if n4_seeds is not None:
        verdict.append(f"seeds within 4.0±0.1 at p={p4}: {n4_seeds}/12")
    verdict.append("fixed-p std across N: " + ", ".join(
        f"p={k}:{v['std_across_N']:.3f}" for k, v in fp.items()))
    verdict.append("fixed-k std across N: " + ", ".join(
        f"k={k}:{v['std_across_N']:.3f}" for k, v in fk.items()))
    verdict.append("across-N drift fixed-k(k=2.0): "
                   f"{fk['2.0']['N250']:.2f} -> {fk['2.0']['N1000']:.2f}")
    verdict.append("across-N drift fixed-p(p=0.02): "
                   f"{fp['0.02']['N250']:.2f} -> {fp['0.02']['N1000']:.2f}")
    print("\n" + "=" * 60)
    for line in verdict:
        print(line)
    out["verdict"] = verdict

    with open(r"F:\_Ai\sgoed\V5\matrix\step_causal_set_scale_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_causal_set_scale_results.json")