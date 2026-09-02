"""Walk every \\texttt{...path...} in a rendered .tex, resolve relative to the
.tex's own directory, and assert the referenced file exists on disk. Globs
(trailing ``*``) pass if at least one file matches.

Run on BOTH rendered outputs before every commit/tag:

    python build/verify_paths.py manuscript_v7.tex \\
        preprints/v7_arrow_of_time/manuscript_v7.tex

Exit code 0 iff every referenced path resolves.
"""
import glob
import re
import sys
from pathlib import Path

PATH_RE = re.compile(r"\\texttt\{([^}]*\.(?:py|json|md|bib)[^}]*)\}")
MD_PATH_RE = re.compile(r"`([^`\n]+\.(?:py|json|md))`")


def path_refs(text, is_md):
    return sorted(set(MD_PATH_RE.findall(text) if is_md else PATH_RE.findall(text)))


def check(tex_path):
    tex_path = Path(tex_path)
    base = tex_path.parent
    is_md = tex_path.suffix == ".md"
    text = tex_path.read_text(encoding="utf-8")
    bad = []
    refs = path_refs(text, is_md)
    for raw in refs:
        p = raw.replace(r"\_", "_")
        if "*" in p:
            if not glob.glob(str(base / p)):
                bad.append(raw)
            continue
        if not (base / p).exists():
            bad.append(raw)
    n = len(refs)
    if bad:
        print(f"FAIL {tex_path}: {len(bad)}/{n} dead path(s)")
        for p in bad:
            print("   ", p)
        return False
    print(f"OK   {tex_path}: all {n} referenced paths resolve")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python build/verify_paths.py <tex> [<tex> ...]")
    ok = all(check(p) for p in sys.argv[1:])
    sys.exit(0 if ok else 1)
