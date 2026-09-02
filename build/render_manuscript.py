"""Render build/manuscript_v7.tex.tmpl -> target-specific manuscript_v7.tex.

Tokens:
  <<FILE:key>> / <<DIR:key>>
      replaced by the target-specific path from build/manifest.yaml
      (underscores escaped for LaTeX).
  <<IF:preprint>>A<<ELSE>>B<<ENDIF>>   (also <<IF:root>>)
      target-specific sentence fragments for spots where the two targets
      phrase a sentence differently, not just the path value.

Safety net: any \\texttt{...} that looks like a file path (.py/.json/.md/.bib)
but did NOT come from a token fails the build. Hardcoded paths are exactly how
the desync incidents of 2026-09-01/02 happened -- this closes that loophole.

The preprint target also copies every manifest file from its single physical
copy (copy_from, root layout) into the preprint bundle (copy_to), applying the
optional per-entry `adapt` substitutions (e.g. sys.path layout lines).

Usage:  python build/render_manuscript.py
"""
import re
import shutil
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
PREPRINT_DIR = REPO / "preprints" / "v7_arrow_of_time"
TMPL = Path(__file__).resolve().parent / "manuscript_v7.tex.tmpl"

FILE_TOKEN = re.compile(r"<<FILE:([A-Za-z0-9_]+)>>")
DIR_TOKEN = re.compile(r"<<DIR:([A-Za-z0-9_]+)>>")
IF_TOKEN = re.compile(r"<<IF:(root|preprint)>>(.*?)<<ELSE>>(.*?)<<ENDIF>>", re.S)
# matches any \texttt{...} whose content looks like a file path -- used for the
# "did we miss one?" check on the RENDERED output
RAW_PATH_RE = re.compile(r"\\texttt\{([^}]*\.(?:py|json|md|bib)[^}]*)\}")


def fail(msg):
    sys.exit("FATAL: " + msg)


def render(text, target, manifest):
    def sub_token(escaped):
        def repl(m):
            key = m.group(1)
            entry = manifest.get(key)
            if entry is None:
                fail(f"token <<{m.group(0)[2:-2]}>> has no manifest entry")
            p = entry[f"{target}_path"]
            return escaped(p)
        return repl

    def if_repl(m):
        want, pre, post = m.group(1), m.group(2), m.group(3)
        for branch in (pre, post):
            if "<<IF:" in branch:
                fail("nested <<IF:...>> is not supported")
        return pre if want == target else post

    text = IF_TOKEN.sub(if_repl, text)
    text = FILE_TOKEN.sub(
        sub_token(lambda p: "\\texttt{" + p.replace("_", r"\_") + "}"), text)
    text = DIR_TOKEN.sub(
        sub_token(lambda p: "\\texttt{" + p.replace("_", r"\_") + "}"), text)
    return text


def check_raw_paths(text, source):
    leftover = RAW_PATH_RE.findall(text)
    if leftover:
        fail(
            f"{source}: {len(leftover)} hardcoded path(s) not using "
            "<<FILE:...>> tokens:\n   " + "\n   ".join(leftover)
        )


def copy_bundle(manifest):
    for key, entry in manifest.items():
        if "copy_from" not in entry:
            continue
        src = REPO / entry["copy_from"]
        dst = PREPRINT_DIR / entry["copy_to"]
        if not src.exists():
            fail(f"manifest copy_from missing on disk: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text(encoding="utf-8")
        for find, repl in entry.get("adapt", []):
            if find not in content:
                fail(f"adapt pattern not found in {src}: {find!r}")
            content = content.replace(find, repl)
        dst.write_text(content, encoding="utf-8")
    print(f"[copy] {sum(1 for e in manifest.values() if 'copy_from' in e)} "
          f"bundle files refreshed from repo-root originals")


def main():
    manifest = yaml.safe_load((Path(__file__).parent / "manifest.yaml").read_text(encoding="utf-8"))
    tmpl = TMPL.read_text(encoding="utf-8")

    # safety net on the SOURCE: any raw path-like \texttt{} in the template
    # means someone typed a path by hand instead of adding a manifest token
    check_raw_paths(tmpl, "template")

    root_tex = render(tmpl, "root", manifest)
    out_root = REPO / "manuscript_v7.tex"
    out_root.write_text(root_tex, encoding="utf-8")
    print(f"[root] rendered {out_root}")

    pre_tex = render(tmpl, "preprint", manifest)
    out_pre = PREPRINT_DIR / "manuscript_v7.tex"
    out_pre.write_text(pre_tex, encoding="utf-8")
    print(f"[preprint] rendered {out_pre}")

    copy_bundle(manifest)


if __name__ == "__main__":
    main()
