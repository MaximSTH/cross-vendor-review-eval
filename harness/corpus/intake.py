"""Corpus intake: recency-gated candidate filtering (design doc §3, §6, D-010).

The corpus SOURCE is fixed at pilot (Step 2b) and logged — this module supplies
the source-agnostic machinery: the contamination filters and the deterministic
selection rule (§8 cherry-picking threat: task set selected by fixed documented
rule before any review runs).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Optional


@dataclass(frozen=True)
class CandidateTask:
    task_id: str
    repo: str
    url: str
    merged_at: date                 # when the source issue/PR merged
    stars: int
    license: str = ""
    notes: str = ""


@dataclass
class FilterReport:
    """What was dropped and why — no silent truncation (§6, evidence discipline)."""
    kept: list[CandidateTask] = field(default_factory=list)
    dropped: dict[str, list[str]] = field(default_factory=dict)  # reason -> task_ids

    def drop(self, task: CandidateTask, reason: str) -> None:
        self.dropped.setdefault(reason, []).append(task.task_id)


def recency_gate(
    candidates: list[CandidateTask],
    training_cutoffs: dict[str, date],
    report: Optional[FilterReport] = None,
) -> list[CandidateTask]:
    """Keep only tasks merged strictly after EVERY evaluated model's cutoff.

    The primary contamination defense (§6.1). `training_cutoffs` maps family ->
    latest known training-cutoff date; values are recorded with the corpus.
    """
    if not training_cutoffs:
        raise ValueError("recency gate requires at least one training cutoff")
    gate = max(training_cutoffs.values())
    report = report if report is not None else FilterReport()
    kept = []
    for c in candidates:
        if c.merged_at > gate:
            kept.append(c)
        else:
            report.drop(c, f"merged_at {c.merged_at} <= gate {gate}")
    report.kept = kept
    return kept


def star_cap(
    candidates: list[CandidateTask],
    max_stars: int,
    report: Optional[FilterReport] = None,
) -> list[CandidateTask]:
    """Prefer low-prominence repos (§6.2, per SWE-PRBench's RQS rationale)."""
    report = report if report is not None else FilterReport()
    kept = []
    for c in candidates:
        if c.stars <= max_stars:
            kept.append(c)
        else:
            report.drop(c, f"stars {c.stars} > cap {max_stars}")
    report.kept = kept
    return kept


def select_first_n(
    candidates: list[CandidateTask],
    n: int,
    report: Optional[FilterReport] = None,
) -> list[CandidateTask]:
    """The fixed selection rule (§8): oldest-first by merged_at, ties by task_id.

    Deterministic and documented — no hand-picking. Applied AFTER all filters.
    Candidates beyond n are recorded in the report, same as every other
    dropping step (no silent drops — cross-vendor review 2026-07-15).
    """
    report = report if report is not None else FilterReport()
    ordered = sorted(candidates, key=lambda c: (c.merged_at.isoformat(), c.task_id))
    kept, beyond = ordered[:n], ordered[n:]
    for c in beyond:
        report.drop(c, f"beyond selection cap n={n}")
    report.kept = kept
    return kept


# --- Ground-truth validity screen (D-028) --------------------------------
# Operationalizes D-010's "bundled-test results never certify correctness" at
# the corpus gate. Pure predicate over already-parsed results; container
# execution lives in the screen runner, so this stays source-agnostic and
# unit-testable.

SCREEN_PASS = "PASS"
SCREEN_FAIL = "FAIL"      # ground truth is broken -> task is inadmissible
SCREEN_ERROR = "ERROR"    # could not measure -> verdict unknown, NOT a task defect

# D-030b: an ERROR may retire a task ONLY when its cause is diagnosed and
# recorded. An undiagnosed ERROR always halts and escalates. Diagnoses are
# rig-relative where the cause is our execution environment, never a claim
# about the task itself (D-030a).
DIAGNOSIS_IMAGE_MISSING = "image_missing"           # verified registry 404
DIAGNOSIS_PLATFORM_INFEASIBLE = "platform_infeasible"  # verified illegal-instruction etc.

DIAGNOSED_CAUSES = frozenset({DIAGNOSIS_IMAGE_MISSING, DIAGNOSIS_PLATFORM_INFEASIBLE})

PLATFORM_INFEASIBLE_WORDING = (
    "infeasible under this study's execution environment: "
    "amd64 emulation on Apple Silicon"
)


class UndiagnosedScreenError(RuntimeError):
    """An ERROR with no recorded cause reached selection (D-030b).

    Raised rather than skipped: an unexplained failure to measure must never
    silently shape the task set. It halts and escalates.
    """


@dataclass(frozen=True)
class ScreenResult:
    verdict: str
    reason: str = ""
    f2p_passing_at_base: tuple[str, ...] = ()
    f2p_not_reported: tuple[str, ...] = ()
    p2p_not_passing_at_base: tuple[str, ...] = ()
    diagnosis: str = ""   # set only on ERROR; must be in DIAGNOSED_CAUSES

    @property
    def admissible(self) -> bool:
        return self.verdict == SCREEN_PASS

    @property
    def diagnosed(self) -> bool:
        """A diagnosed ERROR may retire/skip a task; an undiagnosed one may not."""
        return self.verdict == SCREEN_ERROR and self.diagnosis in DIAGNOSED_CAUSES


def screen_ground_truth(
    fail_to_pass: list[str],
    pass_to_pass: list[str],
    parsed_at_base: dict[str, str],
) -> ScreenResult:
    """Admissible iff, at base_commit with ONLY the test patch applied, every
    declared F2P test is reported and fails, and P2P is non-empty with every
    reported P2P test passing (D-028a).

    `parsed_at_base` maps test name -> "pass" | "fail" | "skip", as produced by
    the task record's own `log_parser`.

    An empty parse is SCREEN_ERROR, never SCREEN_FAIL: it means the results
    never reached the parser (wrong emit path, build failure), which says
    nothing about the task's ground truth. Conflating the two would retire
    healthy tasks and trigger spurious replacements under D-028b — the exact
    false positive recorded in D-028's implementation note.
    """
    if not parsed_at_base:
        return ScreenResult(SCREEN_ERROR,
                            "parser reported no tests (emit/build problem, not ground truth)")
    if not fail_to_pass:
        return ScreenResult(SCREEN_FAIL, "no FAIL_TO_PASS tests declared")

    f2p_passing = tuple(t for t in fail_to_pass if parsed_at_base.get(t) == "pass")
    f2p_missing = tuple(t for t in fail_to_pass if t not in parsed_at_base)
    p2p_bad = tuple(t for t in pass_to_pass
                    if t in parsed_at_base and parsed_at_base[t] != "pass")

    reasons = []
    if f2p_passing:
        reasons.append(f"{len(f2p_passing)}/{len(fail_to_pass)} F2P tests already pass at base")
    if f2p_missing:
        reasons.append(f"{len(f2p_missing)}/{len(fail_to_pass)} F2P tests not reported")
    if not pass_to_pass:
        reasons.append("PASS_TO_PASS is empty")
    if p2p_bad:
        reasons.append(f"{len(p2p_bad)}/{len(pass_to_pass)} P2P tests do not pass at base")

    if reasons:
        return ScreenResult(SCREEN_FAIL, "; ".join(reasons),
                            f2p_passing, f2p_missing, p2p_bad)
    return ScreenResult(SCREEN_PASS)


def select_screened(
    candidates: list[CandidateTask],
    n: int,
    screen: Callable[[CandidateTask], ScreenResult],
    report: Optional[FilterReport] = None,
) -> tuple[list[CandidateTask], list[tuple[str, str]]]:
    """D-028b replacement rule: walk the fixed §8 ordering, keep the first `n`
    candidates that pass the screen.

    Returns (selected, skipped) where `skipped` is [(task_id, reason), ...] —
    every screened-out row is recorded, never silently dropped (§5 forbids
    silent task swaps). Positions are fixed by order of selection, so a
    replacement inherits its position's vendor assignment and k=2 flag
    (D-030d: the seeded repeat draw selected positions, not tasks).

    Raises UndiagnosedScreenError if any candidate returns an ERROR without a
    recorded diagnosis (D-030b) — such a row neither skips nor retires.
    """
    report = report if report is not None else FilterReport()
    ordered = sorted(candidates, key=lambda c: (c.merged_at.isoformat(), c.task_id))
    selected: list[CandidateTask] = []
    skipped: list[tuple[str, str]] = []
    for c in ordered:
        if len(selected) == n:
            report.drop(c, f"beyond selection cap n={n}")
            continue
        result = screen(c)
        if result.admissible:
            selected.append(c)
            continue
        if result.verdict == SCREEN_ERROR and not result.diagnosed:
            raise UndiagnosedScreenError(
                f"{c.task_id}: undiagnosed screen ERROR ({result.reason!r}) — "
                "halts and escalates per D-030b; it must not skip or retire a task"
            )
        detail = f"{result.verdict}: {result.reason}"
        if result.diagnosed:
            detail = f"{result.verdict} [{result.diagnosis}]: {result.reason}"
        skipped.append((c.task_id, detail))
        report.drop(c, f"ground-truth screen {detail}")
    report.kept = selected
    return selected, skipped
