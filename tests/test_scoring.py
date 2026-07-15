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


class TestJudgeInputBundle(unittest.TestCase):
    """D-015 binding condition: judges receive exactly two artifacts —
    the anonymized claim and the answer-key annotation. Never patch/diff,
    never repo content. Structural: adding any field fails this test and
    goes to DECISIONS.md first."""

    def test_payload_fields_are_exactly_the_ratified_bundle(self):
        import dataclasses
        fields = {f.name for f in dataclasses.fields(band2.JudgePayload)}
        self.assertEqual(fields, {"case_id", "defect_annotation", "claim_text"},
                         "JudgePayload changed: reopens D-015 interpretation, "
                         "log the decision before changing this test")

    def test_build_payload_anonymizes_both_artifacts(self):
        key = AnswerKey(case_id="c", is_defective=True,
                        regions=(DefectRegion("f.py", 1, 2),),
                        annotation="Claude Code introduced a null deref")
        payload = band2.build_payload(key, Claim("gpt-5 style off-by-one"))
        self.assertNotIn("claude", payload.defect_annotation.lower())
        self.assertNotIn("gpt", payload.claim_text.lower())


class TestClaimsCap(unittest.TestCase):
    """D-016: ranked list as submitted, truncated at k."""

    def test_catch_beyond_cap_is_not_counted(self):
        from harness.scoring.pipeline import MAX_CLAIMS_PER_REVIEW
        filler = [Claim(f"miss {i}", file="src/x.py", line=900 + i)
                  for i in range(MAX_CLAIMS_PER_REVIEW)]
        winning = Claim("real one", file="src/x.py", line=15)  # ranked 6th
        result, _ = pipeline.score_case(_key(), _review(filler + [winning]))
        self.assertIs(result.verdict, Verdict.NO_CATCH)
        self.assertTrue(any("truncated 1 claim" in n for n in result.notes))

    def test_catch_within_cap_counts(self):
        claims = [Claim("miss", file="src/x.py", line=900),
                  Claim("real one", file="src/x.py", line=15)]
        result, _ = pipeline.score_case(_key(), _review(claims))
        self.assertIs(result.verdict, Verdict.CATCH)
        self.assertFalse(any("truncated" in n for n in result.notes))


class TestVerbosityMetrics(unittest.TestCase):
    """D-016: mean claims-per-task and precision-on-buggy-tasks."""

    def test_metrics_expose_shotgunning(self):
        from harness.scoring import metrics
        buggy, clean = _key(), _key(defective=False)
        stats = [
            # sniper: 1 claim, 1 hit
            metrics.make_stat(buggy, "sniper", "B", (Claim("d", file="src/x.py", line=15),)),
            # shotgun: 5 claims, 1 hit
            metrics.make_stat(buggy, "shotgun", "B", tuple(
                [Claim("d", file="src/x.py", line=15)] +
                [Claim(f"m{i}", file="src/x.py", line=800 + i) for i in range(4)])),
            metrics.make_stat(clean, "sniper", "B", ()),
            metrics.make_stat(clean, "shotgun", "B", (Claim("ghost"),)),
        ]
        mean = metrics.mean_claims_per_task(stats)
        self.assertEqual(mean["sniper"], 0.5)
        self.assertEqual(mean["shotgun"], 3.0)
        prec = metrics.precision_on_buggy_tasks(stats)
        self.assertEqual(prec["sniper"], 1.0)
        self.assertEqual(prec["shotgun"], 0.2)


FAMILIES = ("anthropic", "openai", "google")


class TestRotation(unittest.TestCase):
    """D-015: no judge ever scores its own family's output."""

    def _router(self, judged: list[str]):
        def make(family):
            def decide(_payload, fam=family):
                judged.append(fam)
                return True
            return band2.MockJudgeBackend(family, decide)
        return band2.PanelRouter({f: make(f) for f in FAMILIES})

    def test_panel_never_contains_output_author_family(self):
        for author in FAMILIES:
            judged: list[str] = []
            router = self._router(judged)
            sess = SessionMeta(condition=Condition.A2, vendor=author, model_id="m",
                               harness_version="h", batch_id="b")
            review = ReviewOutput(session=sess, claims=(Claim("vague claim"),))
            pipeline.score_case(_key(), review, router=router)
            self.assertNotIn(author, judged, f"author family {author} judged its own output")
            self.assertEqual(sorted(judged), sorted(set(FAMILIES) - {author}))

    def test_rotation_is_symmetric_across_all_three_vendors(self):
        panels = {a: sorted(b.family for b in self._router([]).panel_for(a).backends)
                  for a in FAMILIES}
        for author, families in panels.items():
            self.assertEqual(len(families), 2)
            self.assertNotIn(author, families)

    def test_two_family_router_rejects_author_inside_it(self):
        router = band2.PanelRouter({
            "anthropic": band2.MockJudgeBackend("anthropic", lambda _p: True),
            "google": band2.MockJudgeBackend("google", lambda _p: True),
        })
        with self.assertRaises(ValueError):
            router.panel_for("anthropic")  # would leave a one-judge panel
        # author outside the dict: both backends are non-authoring, fine
        self.assertEqual(len(router.panel_for("openai").backends), 2)

    def test_panel_and_router_are_mutually_exclusive(self):
        router = self._router([])
        panel = router.panel_for("anthropic")
        sess = SessionMeta(condition=Condition.B, vendor="openai", model_id="m",
                           harness_version="h", batch_id="b")
        with self.assertRaises(ValueError):
            pipeline.score_case(_key(), ReviewOutput(session=sess, claims=(Claim("x"),)),
                                panel=panel, router=router)


class TestSensitivitySweep(unittest.TestCase):
    def test_sweep_reports_per_tolerance_verdicts(self):
        from harness.scoring.band1 import sensitivity_sweep
        # region 10-20; line 5 catches at ±5/±10, misses at ±1
        sweep = sensitivity_sweep(_key(), (Claim("d", file="src/x.py", line=5),))
        self.assertEqual(sweep, {1: Verdict.NO_CATCH, 5: Verdict.CATCH, 10: Verdict.CATCH})

    def test_sweep_preserves_band2_routing_as_none(self):
        from harness.scoring.band1 import sensitivity_sweep
        sweep = sensitivity_sweep(_key(), (Claim("vague"),))
        self.assertEqual(sweep, {1: None, 5: None, 10: None})


class TestCardBlindness(unittest.TestCase):
    """D-015: Band 3 is blind to authorship end to end."""

    def _card(self, **overrides):
        from harness.scoring.band3 import AdjudicationCard
        from harness.scoring.models import JudgeVerdict
        defaults = dict(
            case_id="case-77", condition="B",
            defect_annotation="Claude Code's patch concatenates SQL from user input.",
            claim=Claim("The gpt-5 reviewer thinks sanitization may be missing."),
            judge_verdicts=(
                JudgeVerdict("openai", True, "matches the injection annotation"),
                JudgeVerdict("google", False, "too vague, per Gemini analysis"),
            ),
        )
        defaults.update(overrides)
        return AdjudicationCard(**defaults)

    def test_vendor_laced_inputs_render_clean(self):
        from harness.scoring.band3 import lint_blindness, render_cards_html
        page = render_cards_html([self._card()])
        self.assertEqual(lint_blindness(page), [])
        self.assertNotIn("openai", page.lower())
        self.assertNotIn("gemini", page.lower())

    def test_judge_labels_are_role_only(self):
        from harness.scoring.band3 import render_cards_html
        page = render_cards_html([self._card()])
        self.assertIn("Judge A (non-authoring)", page)
        self.assertIn("Judge B (non-authoring)", page)

    def test_unanonymizable_leak_raises(self):
        from harness.scoring.band3 import render_cards_html
        # A vendor marker in a field the renderer escapes but cannot redact
        # (case_id is an identifier, not prose) must fail closed.
        with self.assertRaises(ValueError):
            render_cards_html([self._card(case_id="claude-code-run-12")])

    def test_rubric_help_is_present(self):
        from harness.scoring.band3 import render_cards_html
        page = render_cards_html([self._card()])
        self.assertIn("reader-actionability", page)
        self.assertIn("false_alarm", page)


if __name__ == "__main__":
    unittest.main()
