"""Band 1 — mechanical scoring. Deterministic path/coordinate comparison.

No model in the loop, by design (design doc §5, D-013). This band decides:
  * everything on test-confirmed-correct changes (false alarm vs clean pass),
  * catches by fully-localized claims (file + line within tolerance),
  * mechanical no-catch when ALL claims are fully localized and none match.
It routes to Band 2 only when a partially-localized claim on a defective change
leaves coordinates unable to decide.
"""

from __future__ import annotations

import posixpath
from dataclasses import dataclass
from typing import Optional

from .models import AnswerKey, Band, Claim, DefectRegion, Verdict

# Pre-registered primary tolerance: ±5 (OQ-2 ratified, D-015). Band 1 is
# additionally rescored at the sweep tolerances for the sensitivity appendix —
# deterministic rescoring only, never a design change.
DEFAULT_TOLERANCE = 5
SWEEP_TOLERANCES = (1, 5, 10)


def normalize_path(path: str) -> str:
    """Normalize a repo-relative path for comparison.

    Strips git-diff prefixes (a/, b/), leading ./ segments, and collapses
    separators. Comparison is case-sensitive (repos are).
    """
    p = path.strip().replace("\\", "/")
    if p.startswith(("a/", "b/")):
        p = p[2:]
    while p.startswith("./"):
        p = p[2:]
    return posixpath.normpath(p)


def claim_matches_region(claim: Claim, region: DefectRegion, tolerance: int) -> bool:
    """True iff a fully-localized claim hits the region within ±tolerance lines."""
    if not claim.fully_localized:
        return False
    if normalize_path(claim.file) != normalize_path(region.path):
        return False
    return region.line_start - tolerance <= claim.line <= region.line_end + tolerance


@dataclass(frozen=True)
class Band1Outcome:
    verdict: Optional[Verdict]      # None => Band 1 cannot decide, route to Band 2
    band: Band
    matched_claim: Optional[Claim] = None
    band2_claims: tuple[Claim, ...] = ()
    note: str = ""


def score(key: AnswerKey, claims: tuple[Claim, ...], tolerance: int = DEFAULT_TOLERANCE) -> Band1Outcome:
    """Apply the mechanical rules. Returns verdict=None only when Band 2 is needed."""
    if not key.is_defective:
        # Any defect claim against a test-confirmed-correct change is a false
        # alarm regardless of localization — mechanically decidable.
        if claims:
            return Band1Outcome(Verdict.FALSE_ALARM, Band.MECHANICAL,
                                note=f"{len(claims)} claim(s) on correct change")
        return Band1Outcome(Verdict.CLEAN_PASS, Band.MECHANICAL)

    # Defective change: look for a mechanical catch first.
    for claim in claims:
        for region in key.regions:
            if claim_matches_region(claim, region, tolerance):
                return Band1Outcome(Verdict.CATCH, Band.MECHANICAL, matched_claim=claim)

    # No mechanical catch. Claims lacking precise coordinates cannot be
    # dismissed mechanically — they may describe the real failure mode.
    semantic = tuple(c for c in claims if not c.fully_localized)
    if semantic:
        return Band1Outcome(None, Band.JUDGE, band2_claims=semantic,
                            note="partially-localized claim(s) need semantic matching")

    # Every claim carried coordinates and none matched: coordinates decide.
    return Band1Outcome(Verdict.NO_CATCH, Band.MECHANICAL,
                        note="all claims fully localized; none within tolerance")


def sensitivity_sweep(
    key: AnswerKey,
    claims: tuple[Claim, ...],
    tolerances: tuple[int, ...] = SWEEP_TOLERANCES,
) -> dict[int, Optional[Verdict]]:
    """Rescore Band 1 at each sweep tolerance (D-015 / OQ-2 amendment).

    Returns tolerance -> Band 1 verdict (None where Band 1 routes to Band 2).
    Reported in the appendix; the ±5 primary result is never revised by this.
    """
    return {t: score(key, claims, tolerance=t).verdict for t in tolerances}
