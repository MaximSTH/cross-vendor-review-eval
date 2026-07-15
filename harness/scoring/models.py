"""Core data types for the three-band scoring pipeline (design doc §5, D-013)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Verdict(str, Enum):
    CATCH = "catch"                # reviewer localized the real defect
    NO_CATCH = "no_catch"          # defective change, defect not flagged
    FALSE_ALARM = "false_alarm"    # defect flagged on a test-confirmed-correct change
    CLEAN_PASS = "clean_pass"      # correct change, correctly not flagged
    PENDING_JUDGE = "pending_judge"    # Band 2 required but no judge backend configured (OQ-1)
    PENDING_HUMAN = "pending_human"    # escalated to Band 3, awaiting adjudication


class Band(int, Enum):
    MECHANICAL = 1
    JUDGE = 2
    HUMAN = 3


class Condition(str, Enum):
    A1 = "A1"  # self-review, same session as authoring
    A2 = "A2"  # self-review, fresh session, no attribution
    B = "B"    # cross-vendor review, fresh session, no attribution


@dataclass(frozen=True)
class DefectRegion:
    """Ground-truth location of a defect, from the official fix."""
    path: str
    line_start: int
    line_end: int


@dataclass(frozen=True)
class AnswerKey:
    """What the hidden test suite established about one code change."""
    case_id: str
    is_defective: bool
    regions: tuple[DefectRegion, ...] = ()
    annotation: str = ""  # human-readable description of the defect

    def __post_init__(self) -> None:
        if self.is_defective and not self.regions:
            raise ValueError(f"{self.case_id}: defective case needs >=1 defect region")
        if not self.is_defective and self.regions:
            raise ValueError(f"{self.case_id}: correct case must not carry defect regions")


@dataclass(frozen=True)
class Claim:
    """One structured finding from a reviewer: {file, line, description}."""
    description: str
    file: Optional[str] = None
    line: Optional[int] = None

    @property
    def fully_localized(self) -> bool:
        return self.file is not None and self.line is not None


@dataclass(frozen=True)
class SessionMeta:
    """Runtime-reported provenance for one review session (D-012)."""
    condition: Condition
    vendor: str
    model_id: str            # as reported by the CLI at runtime
    harness_version: str     # as reported by the CLI at runtime
    batch_id: str


@dataclass(frozen=True)
class ReviewOutput:
    session: SessionMeta
    claims: tuple[Claim, ...] = ()


@dataclass(frozen=True)
class JudgeVerdict:
    judge_family: str
    is_match: bool
    reasoning: str


@dataclass
class CaseResult:
    case_id: str
    condition: Condition
    verdict: Verdict
    band: Band
    matched_claim: Optional[Claim] = None
    band2_claims: tuple[Claim, ...] = ()       # claims that needed semantic matching
    judge_verdicts: tuple[JudgeVerdict, ...] = ()
    notes: list[str] = field(default_factory=list)
