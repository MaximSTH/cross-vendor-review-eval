"""Corpus intake: recency-gated candidate filtering (design doc §3, §6, D-010).

The corpus SOURCE is fixed at pilot (Step 2b) and logged — this module supplies
the source-agnostic machinery: the contamination filters and the deterministic
selection rule (§8 cherry-picking threat: task set selected by fixed documented
rule before any review runs).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


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
