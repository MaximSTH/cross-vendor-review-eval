#!/usr/bin/env bash
# render-doc.sh — minimal, self-contained Markdown → HTML exporter for this repo.
#
# Fresh for this project; no external stylesheets, no other-project deps.
# GitHub-flavored Markdown via `npx marked --gfm`; one inline CSS string;
# output is a single self-contained .html (no external assets) under exports/.
# Reusable for any repo doc — e.g. the report and the practitioner write-up:
#
#   tools/render-doc.sh results/pilot/decision-brief.md
#   tools/render-doc.sh results/pilot/report.md
#   tools/render-doc.sh results/pilot/practitioner-writeup.md "My Title"
#
# Args: <input.md> [title]   (title defaults to the file's first H1, else name)

set -euo pipefail

IN="${1:?usage: render-doc.sh <input.md> [title]}"
[ -f "$IN" ] || { echo "render-doc: no such file: $IN" >&2; exit 1; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTDIR="$ROOT/exports"
mkdir -p "$OUTDIR"
BASE="$(basename "$IN")"; BASE="${BASE%.md}"
OUT="$OUTDIR/$BASE.html"

# Title: explicit arg → first markdown H1 → filename.
TITLE="${2:-}"
if [ -z "$TITLE" ]; then
  TITLE="$(grep -m1 '^# ' "$IN" | sed 's/^# //')"
  [ -z "$TITLE" ] && TITLE="$BASE"
fi

# Render GFM body (npx --yes so it fetches marked if absent; no repo install).
BODY="$(npx --yes marked --gfm -i "$IN")"

# One inline CSS string: clean, readable, light/dark aware, self-contained.
read -r -d '' CSS <<'CSS' || true
:root{color-scheme:light dark;--fg:#1a1a1a;--muted:#555;--bg:#fff;--accent:#0b5cad;
--line:#e2e2e2;--codebg:#f4f5f7;--thbg:#f0f2f5}
@media (prefers-color-scheme:dark){:root{--fg:#e6e6e6;--muted:#a6a6a6;--bg:#16181c;
--accent:#6db3f2;--line:#33363c;--codebg:#22252b;--thbg:#22252b}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:820px;margin:0 auto;padding:3rem 1.4rem 5rem}
h1{font-size:1.9rem;line-height:1.2;margin:.2em 0 .6em}
h2{font-size:1.35rem;margin:1.9em 0 .5em;padding-bottom:.25em;border-bottom:1px solid var(--line)}
h3{font-size:1.08rem;margin:1.5em 0 .4em}
p,li{color:var(--fg)}
em{color:var(--muted)}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
code{background:var(--codebg);padding:.12em .38em;border-radius:4px;
font:0.88em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
pre{background:var(--codebg);padding:1rem;border-radius:8px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{margin:1em 0;padding:.4em 1.1em;border-left:3px solid var(--accent);
color:var(--muted)}
table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:.95rem;
display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:.55em .8em;text-align:left;vertical-align:top}
th{background:var(--thbg);font-weight:600}
hr{border:0;border-top:1px solid var(--line);margin:2.2em 0}
CSS

# Assemble a single self-contained HTML file (no external requests).
{
  printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
  printf '<title>%s</title>\n<style>\n%s\n</style>\n</head>\n<body>\n<main>\n' "$TITLE" "$CSS"
  printf '%s\n' "$BODY"
  printf '</main>\n</body>\n</html>\n'
} > "$OUT"

echo "$OUT"
