"""Verbosity-visible metrics (D-016).

Catch-rate alone can be inflated by shotgunning claims; the cap bounds that,
and these metrics make verbosity differences visible rather than laundered:
  * mean claims-per-task, per vendor (and per condition),
  * precision-on-buggy-tasks: of all claims submitted against defective
    changes, the fraction that actually match a defect region.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from . import band1
from .models import AnswerKey, Claim


@dataclass(frozen=True)
class ReviewStat:
    """One scored review's raw counts, tagged for grouping."""
    vendor: str
    condition: str
    is_defective_task: bool
    n_claims: int
    n_matching_claims: int


def count_matching_claims(key: AnswerKey, claims: Iterable[Claim],
                          tolerance: int = band1.DEFAULT_TOLERANCE) -> int:
    """How many submitted claims mechanically match some defect region."""
    if not key.is_defective:
        return 0
    return sum(
        1 for c in claims
        if any(band1.claim_matches_region(c, r, tolerance) for r in key.regions)
    )


def make_stat(key: AnswerKey, vendor: str, condition: str,
              claims: tuple[Claim, ...],
              tolerance: int = band1.DEFAULT_TOLERANCE) -> ReviewStat:
    return ReviewStat(
        vendor=vendor, condition=condition,
        is_defective_task=key.is_defective, n_claims=len(claims),
        n_matching_claims=count_matching_claims(key, claims, tolerance),
    )


def mean_claims_per_task(stats: list[ReviewStat]) -> dict[str, float]:
    """Per-vendor mean number of claims submitted per review."""
    by_vendor: dict[str, list[int]] = {}
    for s in stats:
        by_vendor.setdefault(s.vendor, []).append(s.n_claims)
    return {v: sum(ns) / len(ns) for v, ns in by_vendor.items()}


def precision_on_buggy_tasks(stats: list[ReviewStat]) -> dict[str, float]:
    """Per-vendor: matching claims / total claims, over defective tasks only.

    Vendors with zero claims on buggy tasks get precision reported as 0.0 with
    the zero denominator visible to callers via mean_claims_per_task.
    """
    by_vendor: dict[str, tuple[int, int]] = {}
    for s in stats:
        if not s.is_defective_task:
            continue
        hit, total = by_vendor.get(s.vendor, (0, 0))
        by_vendor[s.vendor] = (hit + s.n_matching_claims, total + s.n_claims)
    return {v: (hit / total if total else 0.0) for v, (hit, total) in by_vendor.items()}
