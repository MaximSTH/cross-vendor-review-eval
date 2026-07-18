#!/usr/bin/env python3
"""Canary suite runner (design doc §9, D-014).

Build acceptance: all four canaries score correctly end-to-end.
Band 2/3 canaries currently run against the fixture-driven MockJudgeBackend
(OQ-1: real judge backend awaits supervisor decision); they validate routing and
blinding, and must be re-run against the real backend once OQ-1 is closed.

Usage: python3 canary/run_canaries.py   (exit 0 = all pass)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from harness.scoring import band2, pipeline  # noqa: E402
from harness.scoring.band3 import render_cards_html  # noqa: E402
from harness.scoring.models import (  # noqa: E402
    AnswerKey, Band, Claim, Condition, DefectRegion, ReviewOutput, SessionMeta, Verdict,
)

CASES = ROOT / "canary" / "cases" / "canaries.json"
OUT = ROOT / "results" / "canary_cards.html"


def _parse(fix: dict) -> tuple[AnswerKey, ReviewOutput, dict | None]:
    ak = fix["answer_key"]
    key = AnswerKey(
        case_id=ak["case_id"],
        is_defective=ak["is_defective"],
        regions=tuple(DefectRegion(**r) for r in ak["regions"]),
        annotation=ak["annotation"],
    )
    rv = fix["review"]
    sess = SessionMeta(condition=Condition(rv["session"]["condition"]),
                       vendor=rv["session"]["vendor"],
                       model_id=rv["session"]["model_id"],
                       harness_version=rv["session"]["harness_version"],
                       batch_id=rv["session"]["batch_id"])
    claims = tuple(Claim(description=c["description"], file=c["file"], line=c["line"])
                   for c in rv["claims"])
    return key, ReviewOutput(session=sess, claims=claims), fix.get("judge_script")


def main(real: bool = False) -> int:
    fixtures = json.loads(CASES.read_text())["canaries"]
    failures, cards = [], []

    real_router = None
    real_block_reason = None
    if real:
        from harness.judges import JudgeCallError, make_real_router
        try:
            real_router = make_real_router()
        except JudgeCallError as e:  # e.g. GEMINI_API_KEY unset (D-019)
            real_block_reason = str(e)

    for fix in fixtures:
        key, review, script = _parse(fix)
        router = None
        if script:
            # D-015 guard: the fixture panel must exclude the claim's author.
            if review.session.vendor.lower() in {f.lower() for f in script}:
                print(f"  [FAIL] {fix['id']:<28} fixture defect: judge_script "
                      f"includes authoring family {review.session.vendor}")
                failures.append(fix["id"])
                continue
            if real and real_router is None:
                print(f"  [BLOCKED] {fix['id']:<26} {real_block_reason}")
                failures.append(fix["id"])
                continue
            router = real_router if real else band2.PanelRouter({
                family: band2.MockJudgeBackend(family, lambda _p, ans=answer: ans)
                for family, answer in script.items()
            })
        try:
            result, card = pipeline.score_case(key, review, router=router)
        except Exception as e:  # real-backend family unavailable (e.g. OQ-6)
            print(f"  [BLOCKED] {fix['id']:<26} {type(e).__name__}: {str(e)[:120]}")
            failures.append(fix["id"])
            continue
        if card:
            cards.append(card)

        if real and "expect_real" in fix:
            # Supervisor-ruled real-mode pass SET (OQ-4): verdict-only check.
            allowed = {Verdict(v) for v in fix["expect_real"]["verdicts"]}
            ok = result.verdict in allowed
            expected_desc = "one of {" + ", ".join(sorted(v.value for v in allowed)) + "}"
        else:
            expected_verdict = Verdict(fix["expect"]["verdict"])
            expected_band = Band(fix["expect"]["band"])
            ok = result.verdict is expected_verdict and result.band is expected_band
            expected_desc = f"{expected_verdict.value} (band {expected_band.value})"
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {fix['id']:<28} -> {result.verdict.value} (band {result.band.value})"
              + ("" if ok else f"  EXPECTED {expected_desc}"))
        if real and result.judge_verdicts:
            # Full Band 2/3 trace (supervisor-requested for real runs; canary
            # fixtures are known-outcome, not study data — card blindness is
            # unaffected).
            for v in result.judge_verdicts:
                print(f"            judge[{v.judge_family}]: "
                      f"{'MATCH' if v.is_match else 'NO MATCH'} — {v.reasoning[:100]}")
            agreed = len({v.is_match for v in result.judge_verdicts}) == 1
            routing = ("agreed -> resolved in Band 2" if agreed
                       else "disagreement -> escalated to Band 3 (card written)")
            print(f"            panel: {routing}")
        if not ok:
            failures.append(fix["id"])

    if cards:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(render_cards_html(cards, title="Canary Band-3 cards"))
        print(f"\n  Band 3 card(s) written: {OUT.relative_to(ROOT)}")

    mode = "REAL rotating judge backend" if real else "mock judges"
    print(f"\n  {len(fixtures) - len(failures)}/{len(fixtures)} canaries pass via {mode}.")
    if not real:
        print("  D-015 binding note: build acceptance requires re-running canaries 3-4"
              "\n  against the real rotating judge backend (--real). Not yet claimable.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(real="--real" in sys.argv))
