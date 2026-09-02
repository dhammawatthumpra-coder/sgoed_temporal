"""One-shot converter: root manuscript_v7.tex -> build/manuscript_v7.tex.tmpl.

Replaces every literal path (the 27 \\texttt{...} refs found by inspection) with
<<FILE:key>>/<<DIR:key>> tokens from build/manifest.yaml, and wraps the two
spots where the root and preprint phrasings differ structurally in
<<IF:preprint>>...<<ELSE>>...<<ENDIF>> blocks.

After conversion the template must contain zero raw path-like \\texttt{}.
"""
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
manifest = yaml.safe_load((Path(__file__).parent / "manifest.yaml").read_text(encoding="utf-8"))

text = (REPO / "manuscript_v7.tex").read_text(encoding="utf-8")

# ---- 1. structural IF/ELSE spots (root phrasing preserved verbatim) ----

# 1a. section 2.1: hysteresis glob sentence
old = r"\texttt{AUDIT\_v7\_hysteresis*} at the repo root"
new = ("<<FILE:hysteresis_glob>>"
       "<<IF:preprint>> in <<DIR:evidence_dir>>"
       "<<ELSE>> at the repo root<<ENDIF>>")
assert text.count(old) == 1, f"glob sentence found {text.count(old)}x"
text = text.replace(old, new)

# 1b. appendix A: hysteresis script + results sentence
old = (r"\texttt{AUDIT\_v7\_hysteresis.py} +" + "\n" +
       r"  \texttt{AUDIT\_v7\_hysteresis\_results.json} (repo root)")
new = ("<<FILE:hysteresis_script>>"
       "<<IF:preprint>> + its result JSON"
       "<<ELSE>> +\n  <<FILE:hysteresis_results>> (repo root)<<ENDIF>>")
assert text.count(old) == 1, f"hysteresis sentence found {text.count(old)}x"
text = text.replace(old, new)

# ---- 2. the per-version-notes phrase (root says matrix/, must map to its own
# dir token before the generic evidence_dir replacement below) ----
old = "the per-version notes in \\texttt{matrix/}"
new = "the per-version notes in <<DIR:version_notes_dir>>"
assert text.count(old) == 1, f"version notes phrase found {text.count(old)}x"
text = text.replace(old, new)

# ---- 3. generic path replacement from the manifest (token replaces the
# WHOLE \texttt{...} unit; the renderer adds \texttt back per target) ----
total = 0
for key, entry in manifest.items():
    rp = entry["root_path"]
    if key in ("hysteresis_glob", "hysteresis_script", "hysteresis_results",
               "evidence_dir", "version_notes_dir"):
        continue  # already handled above / render-only
    escaped = "\\texttt{" + rp.replace("_", r"\_") + "}"
    token = f"<<FILE:{key}>>"
    n = text.count(escaped)
    text = text.replace(escaped, token)
    total += n
    print(f"  {key:38s} x{n}")

# evidence_dir: remaining bare \texttt{matrix/} occurrences
n = text.count(r"\texttt{matrix/}")
text = text.replace(r"\texttt{matrix/}", "<<DIR:evidence_dir>>")
print(f"  {'evidence_dir':38s} x{n}")
total += n

print("total tokens:", total)

# ---- 4. no raw path-like \texttt{} may remain ----
leftover = re.findall(r"\\texttt\{([^}]*\.(?:py|json|md|bib)[^}]*)\}", text)
if leftover:
    print("LEFTOVER RAW PATHS:", leftover)
    sys.exit(1)

out = Path(__file__).parent / "manuscript_v7.tex.tmpl"
out.write_text(text, encoding="utf-8")
print("written:", out)
