"""Scheduler property tests: author-first and no same-arm blocks (D-012)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.scheduler import ScheduledSession, SessionKind, interleave


class TestInterleave(unittest.TestCase):
    def _schedule(self, n=12) -> list[ScheduledSession]:
        return interleave([f"case{i:03d}" for i in range(n)])

    def test_every_case_gets_all_three_sessions(self):
        sched = self._schedule(12)
        self.assertEqual(len(sched), 36)
        for i in range(12):
            kinds = {s.kind for s in sched if s.case_id == f"case{i:03d}"}
            self.assertEqual(kinds, set(SessionKind))

    def test_author_precedes_its_reviews(self):
        sched = self._schedule(12)
        for cid in {s.case_id for s in sched}:
            idx = {s.kind: i for i, s in enumerate(sched) if s.case_id == cid}
            self.assertLess(idx[SessionKind.AUTHOR_A1], idx[SessionKind.REVIEW_A2])
            self.assertLess(idx[SessionKind.AUTHOR_A1], idx[SessionKind.REVIEW_B])

    def test_no_arm_runs_twice_in_a_row_while_others_pend(self):
        # Tightened from no-triples to no-pairs (cross-vendor review
        # 2026-07-15): D-012 says "never a block of one arm".
        sched = self._schedule(12)
        # Tail of the schedule can legitimately drain one queue; check the body.
        body = sched[: len(sched) - 2]
        for i in range(len(body) - 1):
            self.assertNotEqual(body[i].kind, body[i + 1].kind,
                                f"same-arm pair {body[i].kind} at position {i}")

    def test_single_case_still_valid(self):
        sched = interleave(["only"])
        self.assertEqual([s.kind for s in sched],
                         [SessionKind.AUTHOR_A1, SessionKind.REVIEW_A2, SessionKind.REVIEW_B])


if __name__ == "__main__":
    unittest.main()
