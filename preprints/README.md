# SGOED V5 — Preprints (Zenodo-ready)

Two self-contained preprint folders, one per Zenodo release (each gets its
own DOI). Each folder carries ONLY what is needed to read and reproduce its
manuscript — the full live workspace remains in `V5/` and `V5/matrix/`.

| Folder | Manuscript | Content |
|---|---|---|
| [`v6_condensation/`](v6_condensation/) | manuscript_v6 (md/tex/pdf) | Matrix observer coupling: condensation, bistability, hysteresis (Part 1) |
| [`v7_arrow_of_time/`](v7_arrow_of_time/) | manuscript_v7 (md) | The arrow-of-time quest: equilibrium symmetry, 3 process routes, 4D audit, light-cone invariance (Part 2) |

**Relationship between the two:** v6 establishes the reproducible core
(eigenvalue condensation as a discrete direction choice, ~60σ over baseline).
v7 builds the time-arrow quest on top of that core and reports the full
audit: equilibrium Monte Carlo is time-symmetric; real time comes only from
initial conditions or asymmetric process rules; relational light-cone
locality is the necessary condition for scale-invariant causal dimension.
Both manuscripts state plainly that these are toy-level, engineered
constructions — not emergence claims.

**Reproduction:** Python 3, `numpy`; `numba` needed for two scripts in v7
(the rest are pure Python/numpy). All seeds fixed; each `step_*.py` runs
standalone from inside `code/` (scripts insert their folder into
`sys.path`). Precomputed results are included under `results/`.

**License & citation:** see `LICENSE` and `CITATION.cff` in each folder.