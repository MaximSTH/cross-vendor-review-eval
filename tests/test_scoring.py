"""Unit tests for the three-band scoring pipeline. Run: python3 -m unittest discover tests"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.scoring import band1, band2, pipeline
from harness.scoring.models import (
    AnswerKey, Band, Claim, Condition, DefectRegion, ReviewOutput, SessionMeta, Verdict,
)


def _key(defective=True, regions=((("src/x.py"), 10, 20),), annotation="bug"):
    regs = tuple(DefectRegion(path=p, line_start=a, line_end=b) for p, a, b in regions) if defective else ()
    return AnswerKey(case_id="t", is_defective=defective, regions=regs, annotation=annotation)


def _review(claims, condition=Condition.B):
    sess = SessionMeta(condition=condition, vendor="v", model_id="m", harness_version="h", batch_id="b")
    return ReviewOutput(session=sess, claims=tuple(claims))


class TestBand1(unittest.TestCase):
    def test_exact_catch(self):
        out = band1.score(_key(), (Claim("d", file="src/x.py", line=15),))
        self.assertIs(out.verdict, Verdict.CATCH)
        self.assertIs(out.band, Band.MECHANICAL)

    def test_tolerance_boundaries(self):
        self.assertIs(band1.score(_key(), (Claim("d", file="src/x.py", line=5),), tolerance=5).verdict,
                      Verdict.CATCH)   # 10 - 5
        self.assertIs(band1.score(_key(), (Claim("d", file="src/x.py", line=25),), tolerance=5).verdict,
                      Verdict.CATCH)   # 20 + 5
        self.assertIs(band1.score(_key(), (Claim("d", file="src/x.py", line=4),), tolerance=5).verdict,
                      Verdict.NO_CATCH)
        self.assertIs(band1.score(_key(), (Claim("d", file="src/x.py", line=26),), tolerance=5).verdict,
                      Verdict.NO_CATCH)

    def test_git_prefix_and_dot_slash_normalization(self):
        for path in ("a/src/x.py", "b/src/x.py", "./src/x.py", "src/./x.py"):
            out = band1.score(_key(), (Claim("d", file=path, line=12),))
            self.assertIs(out.verdict, Verdict.CATCH, path)

    def test_wrong_file_is_mechanical_no_catch(self):
        out = band1.score(_key(), (Claim("d", file="src/y.py", line=12),))
        self.assertIs(out.verdict, Verdict.NO_CATCH)
        self.assertIs(out.band, Band.MECHANICAL)

    def test_unlocalized_claim_routes_to_band2(self):
        out = band1.score(_key(), (Claim("something about x"),))
        self.assertIsNone(out.verdict)
        self.assertIs(out.band, Band.JUDGE)
        self.assertEqual(len(out.band2_claims), 1)

    def test_file_without_line_routes_to_band2(self):
        out = band1.score(_key(), (Claim("d", file="src/x.py"),))
        self.assertIsNone(out.verdict)

    def test_clean_patch_any_claim_is_false_alarm(self):
        out = band1.score(_key(defective=False), (Claim("ghost bug"),))
        self.assertIs(out.verdict, Verdict.FALSE_ALARM)

    def test_clean_patch_no_claims_is_clean_pass(self):
        out = band1.score(_key(defective=False), ())
        self.assertIs(out.verdict, Verdict.CLEAN_PASS)

    def test_localized_catch_beats_band2_routing(self):
        claims = (Claim("vague"), Claim("d", file="src/x.py", line=11))
        out = band1.score(_key(), claims)
        self.assertIs(out.verdict, Verdict.CATCH)


class TestAnonymizer(unittest.TestCase):
    def test_strips_vendor_markers(self):
        text = ("Claude Code (claude-opus-4) and OpenAI Codex CLI running gpt-5.2 "
                "disagree; Gemini via Antigravity CLI abstains.")
        red = band2.anonymize(text)
        for marker in ("claude", "openai", "codex", "gpt", "gemini", "antigravity"):
            self.assertNotIn(marker, red.lower(), marker)

    def test_strips_tool_formatting(self):
        red = band2.anonymize("● [tool_use: Grep] found it\n└ result line")
        self.assertNotIn("●", red)
        self.assertNotIn("[tool_use", red)

    def test_preserves_technical_content(self):
        red = band2.anonymize("Null deref in src/db/query.py line 120 on empty WHERE clause")
        self.assertIn("src/db/query.py", red)
        self.assertIn("120", red)


class TestPanelAndPipeline(unittest.TestCase):
    def _panel(self, a: bool, b: bool):
        return band2.JudgePanel([
            band2.MockJudgeBackend("fam1", lambda _p, r=a: r),
            band2.MockJudgeBackend("fam2", lambda _p, r=b: r),
        ])

    def test_panel_requires_two_distinct_families(self):
        with self.assertRaises(ValueError):
            band2.JudgePanel([band2.MockJudgeBackend("same", lambda _p: True),
                              band2.MockJudgeBackend("same", lambda _p: True)])

    def test_agreed_match_is_band2_catch(self):
        result, card = pipeline.score_case(_key(), _review([Claim("vague but right")]),
                                           panel=self._panel(True, True))
        self.assertIs(result.verdict, Verdict.CATCH)
        self.assertIs(result.band, Band.JUDGE)
        self.assertIsNone(card)

    def test_agreed_nonmatch_is_band2_no_catch(self):
        result, card = pipeline.score_case(_key(), _review([Claim("vague and wrong")]),
                                           panel=self._panel(False, False))
        self.assertIs(result.verdict, Verdict.NO_CATCH)
        self.assertIsNone(card)

    def test_disagreement_escalates_with_card(self):
        result, card = pipeline.score_case(_key(), _review([Claim("contested")]),
                                           panel=self._panel(True, False))
        self.assertIs(result.verdict, Verdict.PENDING_HUMAN)
        self.assertIs(result.band, Band.HUMAN)
        self.assertIsNotNone(card)
        self.assertEqual(card.case_id, "t")
        self.assertEqual(len(card.judge_verdicts), 2)

    def test_no_panel_marks_pending_judge(self):
        result, card = pipeline.score_case(_key(), _review([Claim("vague")]), panel=None)
        self.assertIs(result.verdict, Verdict.PENDING_JUDGE)
        self.assertIsNone(card)

    def test_judge_payload_is_anonymized(self):
        seen = {}

        def spy(payload):
            seen["text"] = payload.claim_text
            return True

        panel = band2.JudgePanel([band2.MockJudgeBackend("fam1", spy),
                                  band2.MockJudgeBackend("fam2", spy)])
        pipeline.score_case(_key(), _review([Claim("Claude Code saw a gpt-style bug")]), panel=panel)
        self.assertNotIn("claude", seen["text"].lower())
        self.assertNotIn("gpt", seen["text"].lower())


if __name__ == "__main__":
    unittest.main()
