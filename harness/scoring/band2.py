"""Band 2 — blinded LLM judge panel (design doc §5, D-013).

Judge inputs are vendor-anonymized before any judge sees them: self-preference
bias concentrates on the self diagonal and anonymization suppresses it
(arXiv:2603.04582); an unblinded judge would reintroduce the measured bias one
layer up.

The judge backend is pluggable (OQ-1: which families, accessed how, is an open
supervisor decision). MockJudgeBackend exists so routing logic is testable
end-to-end now; canaries 3-4 re-run against the real backend once OQ-1 is
decided.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Protocol

from .models import AnswerKey, Claim, JudgeVerdict

# Vendor / model / harness identifiers that must never reach a judge.
# Extend before pilot; the canary suite exercises the common ones.
# Standalone model-name tokens (sonnet, opus, ...) are included because spaced
# forms like "claude 3.5 sonnet" would otherwise leave trailing model tokens
# after the leading marker is redacted (cross-vendor review 2026-07-15, High).
# Over-redaction (e.g. "magnum opus") is the safe direction here.
_VENDOR_MARKERS = [
    r"anthropic", r"claude(?:[ -]?(?:code|sonnet|opus|haiku|fable))?",
    r"\bsonnet\b", r"\bopus\b", r"\bhaiku\b", r"\bfable\b",
    r"openai", r"codex(?:[ -]?cli)?", r"gpt[-\w.]*", r"\bo[134][\w-]*\b",
    r"google", r"gemini[-\w.]*", r"gemma[-\w.]*", r"antigravity(?:[ -]?cli)?",
    r"copilot", r"deepseek[-\w.]*", r"llama[-\w.]*", r"mistral[-\w.]*",
]
_MARKER_RE = re.compile("|".join(f"(?:{m})" for m in _VENDOR_MARKERS), re.IGNORECASE)

# Post-passes: swallow version/tier tails left after a redacted marker
# ("[REDACTED] 2.5 pro"), then collapse redaction runs to one placeholder.
_VERSION_TAIL_RE = re.compile(
    r"\[REDACTED\](?:[\s-]+(?:\d[\w.]*|pro|mini|nano|flash|ultra|turbo|max|high|lite))+",
    re.IGNORECASE,
)
_REDACTED_RUN_RE = re.compile(r"\[REDACTED\](?:[\s,/&+-]*\[REDACTED\])+")

# Tool-specific transcript furniture that leaks which harness produced the text.
# Two passes: bullets/box-drawing at line starts first, then tool-call brackets
# anywhere (they can trail a bullet on the same line).
# KNOWN GAP (self-review 2026-07-15, anchored; deferred to pilot): the glyph
# set below covers Claude Code's output style only. Claims reach judges as
# JSON-extracted description fields — raw transcripts never enter payloads by
# construction — so this is defense-in-depth, but Codex/Gemini furniture
# patterns must be sampled from REAL pilot sessions and added here with tests
# before any full run. Guessing them now would be untestable.
_BULLET_RE = re.compile(r"^\s*(?:●|⏺|└|├|╭|╰|│)+\s?", re.MULTILINE)
_TOOLCALL_RE = re.compile(r"\[tool[_ ]?(?:use|call|result)[^\]]*\]\s*", re.IGNORECASE)


def anonymize(text: str) -> str:
    """Strip vendor/model/harness identifiers and tool-specific formatting."""
    text = _BULLET_RE.sub("", text)
    text = _TOOLCALL_RE.sub("", text)
    text = _MARKER_RE.sub("[REDACTED]", text)
    text = _VERSION_TAIL_RE.sub("[REDACTED]", text)
    return _REDACTED_RUN_RE.sub("[REDACTED]", text)


@dataclass(frozen=True)
class JudgePayload:
    """Exactly what a judge is allowed to see. Built only via build_payload().

    D-015 binding condition (supervisor-ratified): judges receive exactly two
    artifacts — the anonymized claim and the answer-key annotation. Never the
    patch/diff, never repo content, no case identifiers. Adding any field here
    reopens the D-015 interpretation and goes to DECISIONS.md first. A
    structural test enforces this field set. (Cross-vendor review 2026-07-15,
    High finding: an earlier version leaked case_id as a third artifact.)
    """
    defect_annotation: str
    claim_text: str


def format_claim(claim: Claim) -> str:
    """Canonical display form of a claim: location prefix + description.

    Shared by judge payloads and Band-3 cards so the human rules on exactly
    the artifact the judges saw (design doc §5; cross-vendor review finding).
    """
    if claim.file is not None and claim.line is not None:
        return f"{claim.file}:{claim.line} — {claim.description}"
    if claim.file is not None:
        return f"{claim.file} (line unspecified) — {claim.description}"
    return claim.description


def build_payload(key: AnswerKey, claim: Claim) -> JudgePayload:
    return JudgePayload(
        defect_annotation=anonymize(key.annotation),
        claim_text=anonymize(format_claim(claim)),
    )


class JudgeBackend(Protocol):
    family: str

    def judge(self, payload: JudgePayload) -> JudgeVerdict: ...


class MockJudgeBackend:
    """Fixture-driven judge for routing tests and canaries (pre-OQ-1)."""

    def __init__(self, family: str, decide: Callable[[JudgePayload], bool]):
        self.family = family
        self._decide = decide

    def judge(self, payload: JudgePayload) -> JudgeVerdict:
        is_match = self._decide(payload)
        return JudgeVerdict(
            judge_family=self.family,
            is_match=is_match,
            reasoning=f"mock[{self.family}] fixture decision",
        )


@dataclass(frozen=True)
class PanelOutcome:
    verdicts: tuple[JudgeVerdict, ...]
    agreed: bool
    is_match: bool  # meaningful only when agreed


class JudgePanel:
    """>=2 judges from distinct families; disagreement escalates to Band 3."""

    def __init__(self, backends: list[JudgeBackend]):
        if len(backends) < 2:
            raise ValueError("Band 2 requires judges from at least two families (D-013)")
        families = [b.family for b in backends]
        if len(set(families)) < 2:
            raise ValueError(f"judge families must be distinct, got {families}")
        self.backends = backends

    def evaluate(self, payload: JudgePayload) -> PanelOutcome:
        verdicts = tuple(b.judge(payload) for b in self.backends)
        answers = {v.is_match for v in verdicts}
        agreed = len(answers) == 1
        return PanelOutcome(verdicts=verdicts, agreed=agreed,
                            is_match=(answers == {True}))


class PanelRouter:
    """D-015: per-case rotation — the panel is exactly the families that did NOT
    author the judged output.

    There is no neutral family: all three vendor stacks are under test. The
    judged output in Band 2 is the reviewer's claim, so the excluded family is
    the reviewing session's (under A1/A2 this coincides with the patch author's;
    under B it follows the claim's author — the judge never sees the patch).
    Authorship is used for panel assignment ONLY; judge inputs remain fully
    anonymized per D-013.
    """

    def __init__(self, backends: dict[str, JudgeBackend]):
        self.backends = {family.lower(): b for family, b in backends.items()}

    def panel_for(self, output_author_family: str) -> JudgePanel:
        author = output_author_family.lower()
        others = [b for fam, b in self.backends.items() if fam != author]
        # D-015 says EXACTLY the two non-authoring families — more configured
        # families would silently widen panels (cross-vendor review, Medium).
        if len(others) != 2:
            raise ValueError(
                f"rotation for author '{output_author_family}' leaves "
                f"{len(others)} judge(s); D-015 requires exactly the two "
                f"non-authoring families")
        return JudgePanel(others)
