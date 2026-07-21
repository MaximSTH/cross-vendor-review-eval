"""Ground-truth validity screen (D-028) — admissibility and replacement rule."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.corpus.intake import (
    DIAGNOSIS_IMAGE_MISSING, DIAGNOSIS_PLATFORM_INFEASIBLE,
    PLATFORM_INFEASIBLE_WORDING, SCREEN_ERROR, SCREEN_FAIL, SCREEN_PASS,
    CandidateTask, ScreenResult, UndiagnosedScreenError, screen_ground_truth,
    select_screened,
)


def _task(tid: str, day: int) -> CandidateTask:
    return CandidateTask(task_id=tid, repo="r/r", url="u",
                         merged_at=date(2026, 3, day), stars=10)


_OK = {"x": "fail", "y": "pass"}


class ScreenAdmissibility(unittest.TestCase):

    def test_healthy_task_is_admissible(self):
        result = screen_ground_truth(
            ["t_bug"], ["t_old_a", "t_old_b"],
            {"t_bug": "fail", "t_old_a": "pass", "t_old_b": "pass"})
        self.assertEqual(result.verdict, SCREEN_PASS)
        self.assertTrue(result.admissible)

    def test_f2p_already_passing_at_base_is_inadmissible(self):
        """The P1 task-1 signature: feed labelled the whole suite as F2P."""
        result = screen_ground_truth(
            ["t_bug", "t_unrelated_1", "t_unrelated_2"], [],
            {"t_bug": "fail", "t_unrelated_1": "pass", "t_unrelated_2": "pass"})
        self.assertEqual(result.verdict, SCREEN_FAIL)
        self.assertFalse(result.admissible)
        self.assertEqual(result.f2p_passing_at_base,
                         ("t_unrelated_1", "t_unrelated_2"))
        self.assertIn("already pass at base", result.reason)
        self.assertIn("PASS_TO_PASS is empty", result.reason)

    def test_empty_p2p_alone_is_inadmissible(self):
        result = screen_ground_truth(["t_bug"], [], {"t_bug": "fail"})
        self.assertEqual(result.verdict, SCREEN_FAIL)
        self.assertEqual(result.reason, "PASS_TO_PASS is empty")

    def test_p2p_failing_at_base_is_inadmissible(self):
        result = screen_ground_truth(["t_bug"], ["t_old"],
                                     {"t_bug": "fail", "t_old": "fail"})
        self.assertEqual(result.verdict, SCREEN_FAIL)
        self.assertEqual(result.p2p_not_passing_at_base, ("t_old",))

    def test_unreported_f2p_is_inadmissible(self):
        result = screen_ground_truth(["t_bug", "t_ghost"], ["t_old"],
                                     {"t_bug": "fail", "t_old": "pass"})
        self.assertEqual(result.verdict, SCREEN_FAIL)
        self.assertEqual(result.f2p_not_reported, ("t_ghost",))

    def test_no_f2p_declared_is_inadmissible(self):
        result = screen_ground_truth([], ["t_old"], {"t_old": "pass"})
        self.assertEqual(result.verdict, SCREEN_FAIL)
        self.assertIn("no FAIL_TO_PASS", result.reason)

    def test_empty_parse_is_ERROR_not_FAIL(self):
        """Regression: the NVIDIA__NemoClaw-330 false positive (D-028 note).

        An empty parse means results never reached the parser — a harness/emit
        problem. Scoring it FAIL would retire a healthy task and trigger a
        spurious replacement under D-028b.
        """
        result = screen_ground_truth(["t_bug"], ["t_old"], {})
        self.assertEqual(result.verdict, SCREEN_ERROR)
        self.assertNotEqual(result.verdict, SCREEN_FAIL)
        self.assertFalse(result.admissible)


class ReplacementRule(unittest.TestCase):

    def test_walks_the_fixed_ordering_and_records_every_skip(self):
        """D-028b: next row in the same §8 ordering; no silent swaps (§5)."""
        cands = [_task("t1", 1), _task("t2", 2), _task("t3", 3), _task("t4", 4)]
        ok = screen_ground_truth(["x"], ["y"], _OK)
        bad = screen_ground_truth(["x", "z"], [], {"x": "fail", "z": "pass"})
        verdicts = {"t1": bad, "t2": ok, "t3": bad, "t4": ok}

        selected, skipped = select_screened(cands, 2, lambda c: verdicts[c.task_id])

        self.assertEqual([c.task_id for c in selected], ["t2", "t4"])
        self.assertEqual([tid for tid, _ in skipped], ["t1", "t3"])
        self.assertTrue(all(r.startswith(SCREEN_FAIL) for _, r in skipped))

    def test_undiagnosed_error_halts_and_escalates(self):
        """D-030b: an unexplained failure to measure must not shape the task set."""
        cands = [_task("bad", 1), _task("good", 2)]
        verdicts = {"bad": screen_ground_truth(["x"], ["y"], {}),   # ERROR, no diagnosis
                    "good": screen_ground_truth(["x"], ["y"], _OK)}

        with self.assertRaises(UndiagnosedScreenError) as ctx:
            select_screened(cands, 1, lambda c: verdicts[c.task_id])
        self.assertIn("undiagnosed", str(ctx.exception))

    def test_diagnosed_error_skips_with_reason_recorded(self):
        """D-030b: a diagnosed ERROR may skip a candidate, reason recorded."""
        cands = [_task("gone", 1), _task("good", 2)]
        verdicts = {
            "gone": ScreenResult(SCREEN_ERROR, "registry 404",
                                 diagnosis=DIAGNOSIS_IMAGE_MISSING),
            "good": screen_ground_truth(["x"], ["y"], _OK),
        }

        selected, skipped = select_screened(cands, 1, lambda c: verdicts[c.task_id])

        self.assertEqual([c.task_id for c in selected], ["good"])
        self.assertEqual(len(skipped), 1)
        self.assertIn(DIAGNOSIS_IMAGE_MISSING, skipped[0][1])

    def test_platform_infeasible_is_a_diagnosed_cause(self):
        r = ScreenResult(SCREEN_ERROR, PLATFORM_INFEASIBLE_WORDING,
                         diagnosis=DIAGNOSIS_PLATFORM_INFEASIBLE)
        self.assertTrue(r.diagnosed)
        self.assertFalse(r.admissible)

    def test_platform_infeasible_wording_is_rig_relative(self):
        """D-030a: never a claim about the task itself."""
        self.assertIn("this study's execution environment", PLATFORM_INFEASIBLE_WORDING)

    def test_unknown_diagnosis_string_does_not_count_as_diagnosed(self):
        r = ScreenResult(SCREEN_ERROR, "vibes", diagnosis="made_up_cause")
        self.assertFalse(r.diagnosed)

    def test_ordering_is_by_merged_at_then_task_id(self):
        cands = [_task("b", 2), _task("a", 2), _task("c", 1)]
        ok = screen_ground_truth(["x"], ["y"], _OK)
        selected, _ = select_screened(cands, 3, lambda c: ok)
        self.assertEqual([c.task_id for c in selected], ["c", "a", "b"])

    def test_rows_beyond_cap_are_reported_not_silently_dropped(self):
        cands = [_task("t1", 1), _task("t2", 2), _task("t3", 3)]
        ok = screen_ground_truth(["x"], ["y"], _OK)
        from harness.corpus.intake import FilterReport
        report = FilterReport()
        selected, skipped = select_screened(cands, 1, lambda c: ok, report)
        self.assertEqual([c.task_id for c in selected], ["t1"])
        self.assertEqual(skipped, [])
        self.assertIn("beyond selection cap n=1", report.dropped)
        self.assertEqual(report.dropped["beyond selection cap n=1"], ["t2", "t3"])


if __name__ == "__main__":
    unittest.main()
