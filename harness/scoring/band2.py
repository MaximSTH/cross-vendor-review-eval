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
_VENDOR_MARKERS = [
    r"anthropic", r"claude(?:[ -]?(?:code|sonnet|opus|haiku|fable))?",
    r"openai", r"codex(?:[ -]?cli)?", r"gpt[-\w.]*", r"\bo[134][\w-]*\b",
    r"google", r"gemini[-\w.]*", r"gemma[-\w.]*", r"antigravity(?:[ -]?cli)?",
    r"copilot", r"deepseek[-\w.]*", r"llama[-\w.]*", r"mistral[-\w.]*",
]
_MARKER_RE = re.compile("|".join(f"(?:{m})" for m in _VENDOR_MARKERS), re.IGNORECASE)

# Tool-specific transcript furniture that leaks which harness produced the text.
# Two passes: bullets/box-drawing at line starts first, then tool-call brackets
# anywhere (they can trail a bullet on the same line).
_BULLET_RE = re.compile(r"^\s*(?:●|⏺|└|├|╭|╰|│)+\s?", re.MULTILINE)
_TOOLCALL_RE = re.compile(r"\[tool[_ ]?(?:use|call|result)[^\]]*\]\s*", re.IGNORECASE)


def anonymize(text: str) -> str:
    """Strip vendor/model/harness identifiers and tool-specific formatting."""
    text = _BULLET_RE.sub("", text)
    text = _TOOLCALL_RE.sub("", text)
    return _MARKER_RE.sub("[REDACTED]", text)


@dataclass(frozen=True)
class JudgePayload:
    """Exactly what a judge is allowed to see. Built only via build_payload().

    D-015 binding condition (supervisor-ratified): judges receive exactly two
    artifacts — the anonymized claim and the answer-key annotation. Never the
    patch/diff, never repo content. Adding any field here reopens the D-015
    interpretation and goes to DECISIONS.md first. A structural test enforces
    this field set.
    """
    case_id: str
    defect_annotation: str
    claim_text: str


def build_payload(key: AnswerKey, claim: Claim) -> JudgePayload:
    return JudgePayload(
        case_id=key.case_id,
        defect_annotation=anonymize(key.annotation),
        claim_text=anonymize(claim.description),
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
        if len(others) < 2:
            raise ValueError(
                f"rotation for author '{output_author_family}' leaves "
                f"{len(others)} judge(s); need >=2 non-authoring families (D-015)")
        return JudgePanel(others)
