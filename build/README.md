# Manuscript build system

Single source of truth for the manuscripts and every file path they reference.
Born from the path-desync incidents of 2026-09-01/02 (root vs preprint
artifacts drifted three times before this existed).

## Layout

| file | role |
|---|---|
| `manifest.yaml` | the ONE place declaring every referenced file/dir: `root_path` / `preprint_path` (as rendered), `copy_from` (single physical copy, root layout) / `copy_to` (preprint bundle destination), optional `adapt` line-substitutions for layout-specific code (e.g. `sys.path`) |
| `manuscript_v7.tex.tmpl` | the editable master for v7 — paths appear as `<<FILE:key>>` / `<<DIR:key>>` tokens; target-specific phrasings use `<<IF:preprint>>...<<ELSE>>...<<ENDIF>>` |
| `render_manuscript.py` | renders the template into BOTH `manuscript_v7.tex` (root + preprint) and copies every manifest file into the preprint bundle. **Fails the build** on any raw path-like `\texttt{...}` left in the template |
| `verify_paths.py` | resolves every `\texttt{...}` path in a rendered .tex against the filesystem, relative to that .tex's own directory. Run on BOTH outputs before every commit |
| `build_md.py` | regenerates both .md files of a version from their .tex (markdown is a generated artifact — never hand-edit it) |
| `convert_to_tmpl.py` | one-shot: how `manuscript_v7.tex.tmpl` was created from the old root .tex (kept for reproducibility) |

## Workflow (per release)

```bash
# 1. edit build/manuscript_v7.tex.tmpl (NOT the .tex/.md/.pdf)

# 2. render tex for both targets + refresh preprint bundle from manifest
python build/render_manuscript.py

# 3. compile pdf (root)
pdflatex manuscript_v7.tex && bibtex manuscript_v7 && pdflatex manuscript_v7.tex && pdflatex manuscript_v7.tex
#    compile pdf (preprint)
cd preprints/v7_arrow_of_time && pdflatex manuscript_v7.tex && bibtex manuscript_v7 && pdflatex manuscript_v7.tex && pdflatex manuscript_v7.tex && cd ../..

# 4. regenerate markdown for both targets
python build/build_md.py --version v7

# 5. path gate -- must exit 0, otherwise DO NOT commit
python build/verify_paths.py manuscript_v7.tex preprints/v7_arrow_of_time/manuscript_v7.tex

# 6. commit
git add -A && git commit -m "render vX"
```

## Rules

1. `build/manifest.yaml` is the only place a path may be declared. Adding a new
   referenced file = add a manifest entry + use `<<FILE:key>>` in the template.
2. The rendered `.tex`, `.md`, `.pdf` are **generated artifacts** — never edit
   them directly; the renderer/verify gates will not stop you, but the next
   render will silently revert your edit.
3. `verify_paths.py` failing = dead path = the exact class of bug that shipped
   `notes/SGOED_v8..v14_notes.md` (a file that never existed) into the v7
   preprint. Fix the manifest/template, not the verifier.
