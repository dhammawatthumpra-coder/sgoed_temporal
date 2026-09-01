# SGOED — Preprints (Zenodo-ready)

This repository is **SGOED_temporal** — the time-emergent extension of the
atemporal SGOED framework (preprints v6/v7). Two self-contained preprint
folders, one per Zenodo release (each gets its own DOI). Each folder
carries ONLY what is needed to read and reproduce its manuscript — the
full live workspace remains in the repo root (`code/`, `matrix/`, …).

| Folder | Manuscript | Content |
|---|---|---|
| [`v6_condensation/`](v6_condensation/) | manuscript_v6 (md/tex/pdf) | Matrix observer coupling: condensation, bistability, hysteresis (Part 1) |
| [`v7_arrow_of_time/`](v7_arrow_of_time/) | manuscript_v7 (md/tex/pdf) | The arrow-of-time quest: equilibrium symmetry, 3 process routes, 4D audit, light-cone invariance (Part 2) |

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

---

## Zenodo metadata (`.zenodo.json`)

Each preprint folder carries its own `.zenodo.json` (the format Zenodo's
GitHub integration reads). Upload via the web form, or — when publishing
through the GitHub→Zenodo integration — the file **at the repo root**
(`.zenodo.json`) is read per tagged commit:

- **tag `v7.0.0`** → root already carries the v7 metadata (current HEAD).
- **tag `v6.0.0`** → before tagging, copy the v6 variant to the root:
  `cp preprints/v6_condensation/.zenodo.json .zenodo.json` (then commit,
  then tag). The v6 `.zenodo.json` is preserved in the v6 preprint folder.

After Zenodo mints the DOIs, fill them into `CITATION.cff` (both folders)
and the `doi/url` fields there. The description fields in `.zenodo.json`
are kept plain-ASCII-safe for the ingest pipeline (the manuscripts carry
the full math).

`related_identifiers` currently point to the two existing Zenodo records
that both manuscripts cite (SGOED Phase 1–2 `10.5281/zenodo.21786260` and
STF `10.5281/zenodo.21763905`, relation `cites`). **After v6.0.0's DOI is
minted** (and before tagging v7.0.0), add a fourth entry to the v7 variant
pointing back to the v6 record (`relation: "cites"` — Zenodo has no
"continues" relation code; `resource_type: "publication-preprint"`), then
re-seal the v7 `.zenodo.json` at root before the v7 tag. The v6 record
cannot point to v7 (v6 DOI comes first).