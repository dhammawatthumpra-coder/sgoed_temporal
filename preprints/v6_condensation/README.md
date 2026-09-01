# Preprint — v6: Temporal Emergence from Dynamical Observer Coupling

**Zenodo release unit #1** — the matrix-model core: a dynamical observer $Y$
creates a temporal direction in a main system $X$ via directional coupling
$-g_{XY}\,\hat v_\mu^2\,\mathrm{Tr}(X_\mu^4)$, with IKKT-like stability gates.

## Headline results (audited in the manuscript)

- Eigenvalue **condensation ratio** $4.55\pm0.35$ vs baseline $1.10\pm0.05$
  (~60σ); $\lambda_{\max}/\lambda_{2\mathrm{nd}}\approx 20$ (rank-1).
- Robust healthy emergence for $d\in\{2..5\}$, $N\in\{4..16\}$ (a
  larger-$N$ extension to $N\in\{9,10,12,14,16\}$, Section 4.3), fixed
  $g_{XY}=0.8$; alignment of temporal direction with observer direction =
  100% in all healthy cases.
- A **30-seed follow-up** for the observer-dimension study shows a weak
  downward trend of the ratio with $d$ (slope $\approx -0.08$, $p=0.003$,
  $R^2=0.07$); the earlier $n=5$ pairwise significance ($p=0.049$) was a
  small-sample fluctuation ($t=0.52$, $p=0.61$ at $n=30$).
- First-order **bistability + hysteresis** (anneal-carry verified).
- Mechanism: the coupling is a discrete winner-take-all over dimensions —
  the only sense in which the model "chooses a direction". Engineered, not
  emergent (stated plainly in the manuscript).

## Files

```
manuscript_v6.md        manuscript source (Markdown; LaTeX math) —
                        generated from the .tex (which is authoritative)
manuscript_v6.tex       LaTeX source — edit THIS, then rebuild the .md
manuscript_v6.pdf       compiled PDF
build_md_from_tex.py    md rebuild script (pandoc -> assembler)
references.bib          bibliography
LICENSE, CITATION.cff
code/
  sgoed_core_v6.py      correctness-first v6 engine (delta sampler, full-action check)
  sgoed_core_v7.py      v7 core (back-reaction; used by the audit scripts)
  run_experiments_v5_legacy.py   *LEGACY v5 runner (withdrawn sampler — do not reuse)*
  AUDIT_v6_full_rerun.py    audited re-run (headline numbers)
  AUDIT_v7_feedback.py      feed-back audit (bistability/hysteresis)
results/
  AUDIT_v6_results.json
  AUDIT_v7_feedback_results.json
```

## Rebuild the Markdown from the .tex

```bash
# (requires pandoc)
pandoc manuscript_v6.tex -t markdown -o _v6_body_raw.md
pandoc manuscript_v6.tex -t markdown --standalone -o _v6_standalone.md
python build_md_from_tex.py
rm -f _v6_body_raw.md _v6_standalone.md
```

## Reproduce

```bash
cd code
python AUDIT_v6_full_rerun.py     # -> the reported ratio/alignment results
python AUDIT_v7_feedback.py       # -> feedback/bistability results
```

Requires numpy (any recent version); seeds fixed inside the scripts.

## Note

The full workspace (all versions v6–v17 notes, figures, LaTeX build logs)
lives in the parent project repository; this folder is the self-contained
release slice. See `../README.md` for the relationship to the v7 preprint.