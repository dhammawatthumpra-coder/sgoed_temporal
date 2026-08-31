"""
SGOED — SOC growth laws (blueprint ①): self-tuned dimension?
============================================================
Can an adaptive linking rule make d_MM stable across N without a
fixed external parameter?

  A (degree-saturating feedback):
      p(u,k) = p0 / (1 + (deg_in(u)/k0)^gamma)
      -> anti-preferential: hubs stop accumulating links -> homogeneity.
  B (critical branching feedback):
      p_k = min(1.0, k_target / |past|)  -> each newborn keeps the mean
      link count O(k_target) (branching at fixed ratio).

Audit gates (as specified):
  Gate 1: std_across N in {250,500,1000} x 10 seeds.
          pass <= 0.05, fail > 0.10 (0.05-0.10 borderline).
  Gate 2: report the converged dimension without editing the number.

Note: B-as-specified is the fixed-mean-degree family (related to the
earlier fixed-k percolation that FAILED invariance) — confirmed here
empirically rather than assumed.
"""
import json
import numpy as np
import sys
sys.path.insert(0, ".")
from step_causal_set_scale_study import calibration, read_dim

Ns = [250, 500, 1000]
SEEDS = range(42, 52)          # 10 seeds


def gen_A(N, seed, p0, k0, gamma):
    rng = np.random.RandomState(seed)
    deg = np.zeros(N)
    children = [[] for _ in range(N)]
    for k in range(1, N):
        p = p0 / (1.0 + (deg[:k] / k0) ** gamma)
        pick = rng.rand(k) < p
        for u in np.nonzero(pick)[0]:
            children[k].append(int(u))
            deg[u] += 1
    return children


def gen_B(N, seed, k_target):
    rng = np.random.RandomState(seed)
    children = [[] for _ in range(N)]
    for k in range(1, N):
        pk = min(1.0, k_target / k)
        pick = rng.rand(k) < pk
        for u in np.nonzero(pick)[0]:
            children[k].append(int(u))
    return children


def closure_rho(N, children):
    """Relation fraction after transitive closure (bitset reachability)."""
    reach = [1 << i for i in range(N)]
    C = 0
    for i in range(N - 1, -1, -1):
        for j in children[i]:
            reach[i] |= reach[j]
        C += (reach[i] & ~(1 << i)).bit_count()
    return C / (N * (N - 1) / 2)


def audit(name, gen):
    rows = {}
    for N in Ns:
        ds, rhos = calibration(N, seeds=8)
        dims = []
        for s in SEEDS:
            rho = closure_rho(N, gen(N, s))
            dims.append(read_dim(rho, ds, rhos))
        rows[str(N)] = [float(np.mean(dims)), float(np.std(dims))]
    means = [rows[str(N)][0] for N in Ns]
    std_acr = float(np.std(means))
    verdict = "PASS" if std_acr <= 0.05 else ("FAIL" if std_acr > 0.10 else "BORDERLINE")
    print(f"[{name:28s}] d(N=250/500/1000)=" +
          "/".join(f"{m:.2f}" for m in means) +
          f"  std_across_N={std_acr:.3f} -> {verdict}")
    return {"d": {str(N): rows[str(N)] for N in Ns}, "std_across_N": std_acr,
            "verdict": verdict}


if __name__ == "__main__":
    out = {}
    print("A (degree-saturating): p(u,k)=p0/(1+(deg/k0)^gamma)")
    for key, p0, k0, g in [("A_p005_k5_g2", 0.05, 5.0, 2.0),
                           ("A_p010_k5_g2", 0.10, 5.0, 2.0),
                           ("A_p005_k10_g1", 0.05, 10.0, 1.0),
                           ("A_p010_k10_g2", 0.10, 10.0, 2.0)]:
        out[key] = audit(key, lambda N, s, a=p0, b=k0, c=g: gen_A(N, s, a, b, c))
    print("\nB (critical branching): p_k = min(1, k_target/k)")
    for kt in [2.0, 5.0, 10.0]:
        key = f"B_kt{int(kt)}"
        out[key] = audit(key, lambda N, s, k=kt: gen_B(N, s, k))
    with open("step_growth_soc_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_growth_soc_results.json")