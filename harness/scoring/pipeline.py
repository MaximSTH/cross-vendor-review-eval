"""Three-band scoring pipeline: Band 1 mechanical → Band 2 blinded panel → Band 3 human.

Routing rules live in band1/band2; this module only orchestrates and records.
"""

from __future__ import annotations

from typing import Optional

from . import band1, band2
from .band3 import AdjudicationCard
from .models import AnswerKey, Band, CaseResult, ReviewOutput, Verdict

# D-016: pre-registered claims cap. The prompt instructs reviewers to submit at
# most k claims ranked most-confident first; the harness enforces the same cap
# defensively — scoring uses the ranked list AS SUBMITTED, truncated at k.
MAX_CLAIMS_PER_REVIEW = 5


def score_case(
    key: AnswerKey,
    review: ReviewOutput,
    panel: Optional[band2.JudgePanel] = None,
    router: Optional[band2.PanelRouter] = None,
    tolerance: int = band1.DEFAULT_TOLERANCE,
) -> tuple[CaseResult, Optional[AdjudicationCard]]:
    """Score one (answer key, review output) pair.

    Pass `router` for D-015 per-case panel rotation (excludes the reviewing
    session's family — the author of the judged claim); `panel` is for direct
    use in tests. Returns the result plus an adjudication card iff the case
    escalated to Band 3.
    """
    if router is not None:
        if panel is not None:
            raise ValueError("pass panel or router, not both")
        panel = router.panel_for(review.session.vendor)

    # D-016 cap: ranked list as submitted, truncated at k.
    claims = review.claims[:MAX_CLAIMS_PER_REVIEW]
    truncated = len(review.claims) - len(claims)

    result, card = _score(key, review, claims, panel, tolerance)
    if truncated:
        result.notes.append(f"truncated {truncated} claim(s) beyond cap k={MAX_CLAIMS_PER_REVIEW} (D-016)")
    return result, card


def _score(key, review, claims, panel, tolerance):
    b1 = band1.score(key, claims, tolerance)

    if b1.verdict is not None:  # Band 1 decided
        result = CaseResult(
            case_id=key.case_id, condition=review.session.condition,
            verdict=b1.verdict, band=Band.MECHANICAL,
            matched_claim=b1.matched_claim,
        )
        if b1.note:
            result.notes.append(b1.note)
        return result, None

    # Band 2 needed.
    if panel is None:
        result = CaseResult(
            case_id=key.case_id, condition=review.session.condition,
            verdict=Verdict.PENDING_JUDGE, band=Band.JUDGE,
            band2_claims=b1.band2_claims,
            notes=["no judge backend configured"],
        )
        return result, None

    # Judge each semantic claim; first agreed MATCH is a catch. Any
    # disagreement escalates the case to Band 3 (conservative: humans see it).
    all_verdicts = []
    for claim in b1.band2_claims:
        payload = band2.build_payload(key, claim)
        outcome = panel.evaluate(payload)
        all_verdicts.extend(outcome.verdicts)
        if not outcome.agreed:
            result = CaseResult(
                case_id=key.case_id, condition=review.session.condition,
                verdict=Verdict.PENDING_HUMAN, band=Band.HUMAN,
                band2_claims=b1.band2_claims, judge_verdicts=tuple(all_verdicts),
                notes=["judge disagreement -> Band 3"],
            )
            card = AdjudicationCard(
                case_id=key.case_id, condition=review.session.condition.value,
                defect_annotation=key.annotation, claim=claim,
                judge_verdicts=outcome.verdicts, source="judge_disagreement",
            )
            return result, card
        if outcome.is_match:
            result = CaseResult(
                case_id=key.case_id, condition=review.session.condition,
                verdict=Verdict.CATCH, band=Band.JUDGE,
                matched_claim=claim, band2_claims=b1.band2_claims,
                judge_verdicts=tuple(all_verdicts),
            )
            return result, None

    # Judges agreed every semantic claim is not the defect.
    result = CaseResult(
        case_id=key.case_id, condition=review.session.condition,
        verdict=Verdict.NO_CATCH, band=Band.JUDGE,
        band2_claims=b1.band2_claims, judge_verdicts=tuple(all_verdicts),
    )
    return result, None
