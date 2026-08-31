# Preprint — v7: The Arrow of Time Is Not in the Ensemble
## An Audited Toy-Model Quest across Equilibrium Matrices, Sequential Growth, and Causal Sets

**Zenodo release unit #2** — the time-arrow quest built on the v6 core:
equilibrium Monte Carlo is time-symmetric; the arrow comes only from
initial conditions or asymmetric process rules; and relational light-cone
locality is the discovered necessary condition for scale-invariant causal
dimension. All claims audited (reproduce, seeds ≥ 6–12, null, labeling,
thermalization, mechanism) and reported with plain epistemic boundaries.

## Headline results (audited in the manuscript)

1. **11 structural observables** (R, D, d_MM, d_s, G, cycle, time-reversal,
   order, repulsion, dynamic order, entropy rate) fail at equilibrium — an
   exhaustive negative for "arrow from the final state".
2. **Three process routes give real directional time:**
   - Past Hypothesis: $dS/S_0 = 0.98$ (rank-1 initial state; ~100× random);
   - Sequential Growth: chain inheritance $1.000\pm0.000$, deterministic,
     scale-free ($M=8$–$32$); mechanism = contraction to the past-mean
     (prefix-sum coupling); with a rank-1 frozen origin: origin alignment
     $0.9995\pm0.0002$ (therm 120);
   - Upwind Transport: extent decay **5849×** ($E: 28.8\to0.005$),
     $J=+5.773\pm0.016$ (8 seeds × 500 steps), reversal-symmetric
     ($-6.025$), null $J\approx0$.
3. **The 4D question, audited:** Euclidean IKKT-like actions are isotropic
   without the engineered $\hat v$; pseudo-Euclidean splits 1+3 only as an
   engineered $\eta$; Lorentzian real-time bosonic dynamics is unbounded
   (needs the fermion regulator of the literature); random-percolation
   "d≈4 at N=250" is a finite-size artifact (fails the N→1000 audit in both
   scalings); SOC & curvature (c_eff) self-tuning feedbacks fail (collapse
   or drift).
4. **Positive structural discovery:** the **relational light-cone law** makes
   causal dimension scale-invariant (std across $N$: $0.002$–$0.013$ vs
   $0.26$–$0.82$ for percolation) — including the new **commutator-compatibility
   metric on real growth states** ($d\approx3.5$, std $0.008$, θ-robust).
   Epistemic boundary (stated in §4.6): the stability is real; the dimension
   *value* remains parameter-steered (light speed / diffusion aspect;
   self-calibrated $c_{\mathrm{ref}}$) — no spontaneous dimensional
   selection was found anywhere.

## Files

```
manuscript_v7.md        manuscript source (Markdown; LaTeX math)
manuscript_v7.tex       LaTeX source (built from the .md; see below)
manuscript_v7.pdf       compiled PDF
build_tex.py            md -> tex assembler (v6-template style preamble)
references.bib          bibliography
SUPPLEMENT_B_AUDIT_HANDBOOK.md
                        **open methodology handbook** — six-gate checklist,
                        the full 12-trap catalog, and an 8-step auditing
                        workflow (Thai; curated for the community to apply
                        to any emergent metric)
LICENSE, CITATION.cff
notes/
  SGOED_TIME_EMERGENCE_SUMMARY.md   living result log (updates 1–17), the
                                    full numeric record referenced by App. A
  SGOED_v8..v14_notes.md            audit records behind the NEGATIVE claims
                                    (11 observables, App. B trap catalog)
audit_evidence/
  code/                       20 scripts: v8 graph, v9/v10 hypergraph, v11
                              ecosystem, v12/v13 graph, v14 hybrid — the
                              artifacts behind "11 observables fail" and the
                              trap catalog (R, D, d_MM, d_s, time-reversal,
                              seeds-significance)
  results/                    8 *_results.json (per-trap evidence)
code/                   all experiment scripts (see manuscript App. A);
  18 step_*.py / sgoed_*.py scripts, run standalone from this directory
  audit_gates.py        **Supplement A — the six-gate audit toolbox**
                        (functions + self-test; use gates 1–6 on any metric)
results/                15 precomputed *_results.json (one per script)
```

## Reproduce

```bash
cd code
python step_past_hypothesis.py            # Route 1 (Past Hypothesis)
python step_sequential_growth.py          # Route 2 (growth; sanitiy check)
python step_growth_mechanism.py           # Route 2 mechanism + M=32
python step_growth_past_hypothesis.py     # Route 2 + rank-1 frozen origin
python step_langevin_transport_tuned.py   # Route 3 (transport)
python step_transport_robust.py           # Route 3 robustness (8×500 + scan)
python step_causal_set_scale_study.py     # 4D percolation audit (N→1000)
python step_growth_lightcone.py           # light-cone invariance (legs 1–2)
python step_lightcone_followup.py         # uniform scatter + c/σ scans
python step_growth_commutator.py          # commutator metric (K + R regimes)
python step_growth_commutator_scan.py     # R-regime significance scan
python step_growth_soc.py / step_growth_ceff.py
python step_causal_set_dmm.py / sgoed_matrix_v15.py / step_v15_*.py
python step_spectral_dimension_flow.py    # d_s on flow networks
```

Requires Python 3, `numpy`; `numba` for `step_growth_commutator*` (and
`step_causal_set_scale_study`'s helpers are pure numpy). Some scripts import
helpers from siblings in `code/` — always run from inside `code/` (they
insert their own directory into `sys.path`). Seeds fixed; heavy runs
(N=1000 growth/transport) take minutes on one CPU.

## Build the PDF from the Markdown

```bash
# (requires pandoc and latexmk)
pandoc manuscript_v7.md -t latex -o _v7_body.tex     # 1. body fragment
python build_tex.py                                  # 2. assemble .tex
latexmk -pdf manuscript_v7.tex                       # 3. compile (.pdf)
rm -f manuscript_v7.{aux,out,log,fls,fdb_latexmk,bbl,blg} _v7_body.tex
```

## Note

The full workspace (notes v1–v17, all intermediate scripts, manuscript
history) lives in the parent project repository; this folder is the
self-contained release slice. See `../README.md` for the relationship to
the v6 preprint.