"""Post-hoc compliance scans.

D-018 — reviewer sessions: the prompt's no-test-suite rule is instruction-only;
transcripts are scanned for test-suite invocation. Violating sessions are
excluded BEFORE scoring, blind to what the review claimed, then re-run;
exclusions counted and reported per vendor.

D-020 — judge sessions: any tool invocation of any kind in a judge transcript
invalidates that judgment, triggers a re-run, and is counted in a reported
audit metric.

Pattern lists are maintained here in code (supervisor directive). The judge
tool-marker sets are seeded from known transcript shapes and MUST be refined
against real pilot transcripts — same policy as the anonymizer's furniture
list (see band2.py).
"""

from __future__ import annotations

import re

# --- D-018: reviewer test-suite invocation -------------------------------

REVIEWER_TEST_INVOCATION_PATTERNS: tuple[str, ...] = (
    r"\bpytest\b",
    r"\bpython3?\s+-m\s+unittest\b",
    r"\bunittest\s+discover\b",
    r"\bnpm\s+(?:run\s+)?test\b",
    r"\byarn\s+test\b",
    r"\bpnpm\s+test\b",
    r"\bgo\s+test\b",
    r"\bcargo\s+test\b",
    r"\bmvn\s+(?:-[^\s]+\s+)*test\b",
    r"\bgradle(?:w)?\s+(?:[^\s]+\s+)*test\b",
    r"\brspec\b",
    r"\bjest\b",
    r"\bvitest\b",
    r"\btox\b",
    r"\bmake\s+test\b",
    r"\bctest\b",
    r"\bphpunit\b",
    r"\bdotnet\s+test\b",
)
_REVIEWER_RES = [re.compile(p, re.IGNORECASE) for p in REVIEWER_TEST_INVOCATION_PATTERNS]


def scan_reviewer_transcript(transcript: str) -> list[str]:
    """Return the test-suite invocation patterns matched in a reviewer
    transcript. Non-empty => the session is excluded and re-run (D-018)."""
    return [rx.pattern for rx in _REVIEWER_RES if rx.search(transcript)]


# --- D-020: judge tool-use audit ------------------------------------------

# Seed markers per family; refined at pilot from real transcripts. The Google
# judge is a bare API call (D-019): no tool path exists, nothing to audit.
JUDGE_TOOL_MARKERS: dict[str, tuple[str, ...]] = {
    "openai": (
        r"^\s*\$\s+\S",            # codex exec command echo lines
        r"^\s*exec\s*$",           # codex exec event header
        r"\bapply_patch\b",
        r"^\s*tool(?:\s+call)?\b",
    ),
    "anthropic": (
        r"^\s*●",                  # tool-use bullet in transcript output
        r"\[tool_(?:use|call|result)",
        r"\bRunning tool\b",
    ),
    "google": (),
}


def audit_judge_transcript(family: str, transcript: str) -> list[str]:
    """Return tool-invocation markers found in a judge transcript.

    Non-empty => the judgment is INVALID: re-run and count in the reported
    audit metric (D-020)."""
    markers = JUDGE_TOOL_MARKERS.get(family.lower(), ())
    hits = []
    for p in markers:
        if re.search(p, transcript, re.MULTILINE | re.IGNORECASE):
            hits.append(p)
    return hits
