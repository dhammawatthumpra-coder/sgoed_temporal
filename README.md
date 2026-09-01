# SGOED — Arrow-of-Time Quest & Preprints (`sgoed_temporal`)

**SGOED_temporal** — the time-emergent extension of the atemporal SGOED framework.

This repository holds the audited result of the SGOED quest for the arrow of
time, packaged as **two Zenodo-ready preprints** plus the full workspace that
backs them. Everything is reproducible with fixed seeds.

## What is here

| Path | Content |
|---|---|
| **`preprints/`** | the shippable release units (see its [README](preprints/README.md) for the Zenodo/GitHub publishing workflow) |
| `preprints/v6_condensation/` | **Preprint v6** — *Temporal Emergence from Dynamical Observer Coupling* (matrix observer model: eigenvalue condensation, bistability/hysteresis) — manuscript (md/tex/pdf), engine, audit scripts, results |
| `preprints/v7_arrow_of_time/` | **Preprint v7** — *The Arrow of Time Is Not in the Ensemble* (equilibrium symmetry; 3 process routes; the 4D audit; relational light-cone invariance) — manuscript (md/tex/pdf), 18 scripts + 15 result JSONs, the v8–v14 audit-evidence slice, audit toolbox (Supplement A) and methodology handbook (Supplement B) |
| `manuscript_v6.*` / `manuscript_v7.*` | working copies of the manuscripts at repo root (same as in `preprints/`) |
| `code/`, `matrix/`, `data/` | full workspace: experiment scripts, result JSONs, notes (`SGOED_*_notes.md`, `SGOED_TIME_EMERGENCE_SUMMARY.md`) |

## Headline results (audited — see the manuscripts)

1. **Equilibrium Monte Carlo is time-symmetric.** Eleven structural
   observables (R, D, d_MM, d_s, G, cycle ratio, time-reversal, order,
   repulsion, dynamic order, entropy rate) all fail under a six-gate audit.
2. **Real time comes from process, not the ensemble:**
   - *Past Hypothesis* — rank-1 initial state relaxes with dS/S0 = 0.98 (~100× random)
   - *Sequential Growth* — chain inheritance 1.000 ± 0.000, deterministic, scale-free M = 8–32
   - *Upwind Transport* — decay 5849×, current J = +5.773 ± 0.016, reversal- and null-audited
3. **The 4D question closes negatively** in every audited framework (matrix
   SSB, bounded noncommutativity, Lorentzian real-time dynamics, random
   percolation — whose “d≈4 at N=250” is a finite-size artifact —, SOC and
   curvature-feedback self-tuning). One structural discovery: **relational
   light-cone locality ⇒ scale-invariant causal dimension** (std across N of
   0.002–0.013 vs 0.26–0.82 for percolation).
4. **Methodology as a product:** a six-gate auditing protocol and a 12-trap
   catalog, shipped as a runnable toolbox
   (`preprints/v7_arrow_of_time/code/audit_gates.py`, Supplement A) and an
   open handbook (Supplement B).

**Stated plainly:** engineered toy models, not emergence claims.

## Archival note (important for readers)

The older v5-era material in `code/`, `data/`, and the historical notes
**is archival and superseded**. In particular, the v5 claims of a
“phase diagram” and a “two-regime crossover at N≈7” failed the
reproducibility audit during the v5→v6 correction and **must not be cited
against the current manuscripts** (see `SGOED_PROJECT_SUMMARY.md`). Always
quote the releases from `preprints/`.

## Versioning & publishing

- Releases are tagged: `v6.0.0` (condensation preprint) and `v7.0.0`
  (arrow-of-time preprint); Zenodo records + `.zenodo.json` metadata per
  release (see `preprints/README.md`).
- License: **CC BY 4.0** · Citation: `CITATION.cff` (fill in the minted DOIs).
- Reproduce: start at `preprints/README.md` — each preprint ships its own
  scripts, results, and fixed seeds.