"""Band 3 — human adjudication cards (design doc §5, D-014, D-015).

Each escalated case renders as a self-contained card: answer-key annotation,
the reviewer's claim (ANONYMIZED — the same artifact the judges receive, never
the raw CLI transcript), the judges' proposed calls with role-only labels,
rubric options as buttons, optional code snippet as expandable context only.

Band 3 is blind to authorship end to end (D-015): judge labels identify role
only ("Judge A (non-authoring)"), never family — under per-case rotation,
naming the two judging families would reveal the authoring vendor as the
missing third. render_cards_html() lints its own output and refuses to render
any vendor/model/harness identifier.

Acceptance criterion (pilot): every ruling must be makeable from the card alone,
without opening the repo. A card that forces a diff cold-read is an interface
defect, not an escalation.
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass

from .band2 import _MARKER_RE, anonymize
from .models import Claim, JudgeVerdict

RUBRIC_OPTIONS = ("catch", "no_catch", "false_alarm", "unscorable")

# Ruling boundaries (supervisor policy, D-015; precedents live in design doc §5).
RUBRIC_HELP = (
    "catch — reader-actionability test: a busy engineer reading this review would "
    "locate and fix the planted bug. Correct region alone, without failure class or "
    "location, hedged throughout, fails this test. · "
    "no_catch — the task has a planted bug and the review fails the actionability "
    "test, even if it raises other concerns. · "
    "false_alarm — only for flags raised against clean (test-confirmed-correct) "
    "patches; never applicable on planted-bug tasks. · "
    "unscorable — the card itself is insufficient to rule; flag as an interface "
    "defect rather than guessing (do not open the repo)."
)


@dataclass(frozen=True)
class AdjudicationCard:
    case_id: str
    condition: str
    defect_annotation: str          # from the answer key; anonymized at render
    claim: Claim                    # description anonymized at render (D-015)
    judge_verdicts: tuple[JudgeVerdict, ...]
    code_snippet: str = ""          # optional, expandable context only
    source: str = "judge_disagreement"  # or "audit_sample"


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _role_label(index: int) -> str:
    return f"Judge {chr(ord('A') + index)} (non-authoring)"


def _card_html(card: AdjudicationCard, idx: int) -> str:
    judges = "".join(
        f"<div class='judge'><b>{_role_label(j)}</b>: "
        f"{'MATCH' if v.is_match else 'NO MATCH'} — {_esc(anonymize(v.reasoning))}</div>"
        for j, v in enumerate(card.judge_verdicts)
    ) or "<div class='judge'>(audit sample — no judge disagreement)</div>"

    buttons = "".join(
        f"<label><input type='radio' name='ruling-{idx}' value='{opt}'> {opt}</label>"
        for opt in RUBRIC_OPTIONS
    )
    claim_text = anonymize(card.claim.description)
    loc = ""
    if card.claim.file:
        loc = f" <code>{_esc(card.claim.file)}" + (
            f":{card.claim.line}</code>" if card.claim.line is not None else "</code>")

    snippet = ""
    if card.code_snippet:
        snippet = (f"<details><summary>Code context (optional)</summary>"
                   f"<pre>{_esc(anonymize(card.code_snippet))}</pre></details>")

    return f"""
<section class='card' data-case='{_esc(card.case_id)}' data-condition='{_esc(card.condition)}' data-source='{_esc(card.source)}'>
  <h2>{idx + 1}. {_esc(card.case_id)} <small>[{_esc(card.condition)} · {_esc(card.source)}]</small></h2>
  <div class='block key'><h3>Answer key — planted-bug annotation</h3><p>{_esc(anonymize(card.defect_annotation))}</p></div>
  <div class='block claim'><h3>Reviewer's claim (anonymized — as the judges saw it)</h3><p>{_esc(claim_text)}{loc}</p></div>
  <div class='block judges'><h3>Judges</h3>{judges}</div>
  {snippet}
  <div class='block rubric'><h3>Ruling</h3>{buttons}
    <input type='text' class='note' placeholder='optional note' id='note-{idx}'></div>
</section>"""


def lint_blindness(rendered: str) -> list[str]:
    """Return vendor/model/harness identifiers found in rendered card content.

    "[REDACTED]" placeholders are exempt. Any other hit is a blindness defect.
    """
    return [m.group(0) for m in _MARKER_RE.finditer(rendered)]


def render_cards_html(cards: list[AdjudicationCard], title: str = "Band 3 adjudication") -> str:
    """Fully self-contained HTML (inline CSS/JS, no external assets).

    Raises ValueError if any vendor identifier survives into the rendered
    output (D-015 blindness check) — a card that would leak authorship is a
    build defect, not a rendering choice.
    """
    body = "".join(_card_html(c, i) for i, c in enumerate(cards))
    manifest = json.dumps([
        {"case_id": c.case_id, "condition": c.condition, "source": c.source}
        for c in cards
    ])
    page = f"""<!doctype html><html><head><meta charset="utf-8">
<title>{_esc(title)}</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;line-height:1.5}}
 .card{{border:1px solid #ccc;border-radius:8px;padding:1rem 1.25rem;margin-bottom:1.5rem}}
 .block{{margin:.75rem 0}} h2{{margin:.1rem 0 .5rem}} h3{{margin:.2rem 0;font-size:.85rem;
 text-transform:uppercase;letter-spacing:.05em;color:#555}}
 .key{{background:#f6f3e8;padding:.5rem .75rem;border-radius:6px}}
 .claim{{background:#eef3f9;padding:.5rem .75rem;border-radius:6px}}
 .judge{{font-size:.92rem;margin:.2rem 0}}
 .rubric label{{margin-right:1rem;cursor:pointer}}
 .help{{font-size:.85rem;color:#444;background:#f2f2f2;padding:.6rem .8rem;border-radius:6px}}
 .note{{display:block;margin-top:.5rem;width:100%;padding:.3rem}}
 #export{{position:fixed;bottom:1rem;right:1rem;padding:.6rem 1rem;font-size:1rem;cursor:pointer}}
 pre{{overflow-x:auto;background:#f4f4f4;padding:.5rem;border-radius:6px}}
</style></head><body>
<h1>{_esc(title)}</h1>
<p>{len(cards)} case(s). Rule each from the card alone — if a ruling requires opening
the repo, flag it as an interface defect instead of ruling.</p>
<p class='help'><b>Ruling boundaries:</b> {_esc(RUBRIC_HELP)}</p>
{body}
<button id="export">Export rulings (JSON)</button>
<script>
const manifest = {manifest};
document.getElementById('export').addEventListener('click', () => {{
  const rulings = manifest.map((m, i) => {{
    const sel = document.querySelector(`input[name="ruling-${{i}}"]:checked`);
    const note = document.getElementById(`note-${{i}}`).value;
    return {{...m, ruling: sel ? sel.value : null, note}};
  }});
  const blob = new Blob([JSON.stringify(rulings, null, 2)], {{type: 'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'band3-rulings.json';
  a.click();
}});
</script></body></html>"""

    leaks = lint_blindness(page)
    if leaks:
        raise ValueError(f"Band 3 blindness lint failed (D-015): identifiers leaked: {sorted(set(leaks))}")
    return page
