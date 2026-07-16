"""Tests for the session runner (injected executor — no real CLI calls, D-014
pilot gate) and corpus intake filters."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.corpus.intake import (
    CandidateTask, FilterReport, recency_gate, select_first_n, star_cap,
)
from harness.runner import (
    VENDOR_CLIS, ClaimFormatError, ExecResult, extract_claims, probe_version,
    run_review_session,
)

GOOD_OUTPUT = """I explored the repo and found one issue.

```json
{"claims": [{"file": "src/x.py", "line": 12, "description": "off-by-one"}]}
```
"""


class TestExtractClaims(unittest.TestCase):
    def test_parses_valid_block(self):
        claims = extract_claims(GOOD_OUTPUT)
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0].file, "src/x.py")
        self.assertEqual(claims[0].line, 12)

    def test_empty_claims_list_is_valid(self):
        claims = extract_claims('```json\n{"claims": []}\n```')
        self.assertEqual(claims, ())

    def test_takes_last_block(self):
        out = ('```json\n{"claims": [{"description": "echoed example"}]}\n```\n'
               'final answer:\n```json\n{"claims": []}\n```')
        self.assertEqual(extract_claims(out), ())

    def test_missing_block_raises(self):
        with self.assertRaises(ClaimFormatError):
            extract_claims("I think it looks fine.")

    def test_malformed_json_raises(self):
        with self.assertRaises(ClaimFormatError):
            extract_claims('```json\n{"claims": [}\n```')

    def test_non_int_line_raises(self):
        with self.assertRaises(ClaimFormatError):
            extract_claims('```json\n{"claims": [{"description": "d", "line": "12"}]}\n```')

    def test_null_locations_allowed(self):
        claims = extract_claims('```json\n{"claims": [{"description": "vague", "file": null, "line": null}]}\n```')
        self.assertIsNone(claims[0].file)
        self.assertFalse(claims[0].fully_localized)

    def test_claims_null_raises_format_error_not_typeerror(self):
        # Peer review 2026-07-15 (Medium): "claims": null hit enumerate() and
        # raised TypeError, bypassing the record-not-raise contract.
        with self.assertRaises(ClaimFormatError):
            extract_claims('```json\n{"claims": null}\n```')

    def test_non_string_file_raises_format_error(self):
        # Self-review 2026-07-15: "file": 123 crashed later in normalize_path.
        with self.assertRaises(ClaimFormatError):
            extract_claims('```json\n{"claims": [{"description": "d", "file": 123}]}\n```')

    def test_uppercase_fence_tag_accepted(self):
        claims = extract_claims('```JSON\n{"claims": []}\n```')
        self.assertEqual(claims, ())


class TestRunner(unittest.TestCase):
    def _executor(self, calls):
        def fake(cmd, stdin, cwd):
            calls.append((tuple(cmd), stdin, cwd))
            if "--version" in cmd:
                return ExecResult("cli 9.9.9 (model: test-model-2026-07)", "", 0)
            return ExecResult(GOOD_OUTPUT, "", 0)
        return fake

    def test_probe_version_reports_runtime_string(self):
        v = probe_version(VENDOR_CLIS["anthropic"], self._executor([]))
        self.assertIn("9.9.9", v)

    def test_session_records_provenance_and_claims(self):
        calls = []
        with TemporaryDirectory() as tmp:
            record, claims = run_review_session(
                VENDOR_CLIS["openai"], case_id="c1", condition="B",
                prompt="PROMPT", workdir=Path(tmp), raw_dir=Path(tmp) / "raw",
                executor=self._executor(calls), now=lambda: "T0",
            )
        self.assertEqual(record.family, "openai")
        self.assertIn("9.9.9", record.reported_version)
        self.assertEqual(record.returncode, 0)
        self.assertEqual(len(claims), 1)
        self.assertEqual(record.claims[0]["line"], 12)
        self.assertEqual(record.claim_format_error, "")
        # prompt goes via stdin to the review command, in the workdir
        review_calls = [c for c in calls if "--version" not in c[0]]
        self.assertEqual(review_calls[0][1], "PROMPT")

    def test_format_error_is_recorded_not_raised(self):
        def bad(cmd, stdin, cwd):
            if "--version" in cmd:
                return ExecResult("v1", "", 0)
            return ExecResult("no block here", "", 0)
        with TemporaryDirectory() as tmp:
            record, claims = run_review_session(
                VENDOR_CLIS["anthropic"], "c2", "A2", "P", Path(tmp),
                Path(tmp) / "raw", executor=bad, now=lambda: "T0")
        self.assertEqual(claims, ())
        self.assertIn("no fenced json", record.claim_format_error)


def _cand(tid, merged, stars=100):
    return CandidateTask(task_id=tid, repo="r", url="u",
                         merged_at=merged, stars=stars)


class TestCorpusFilters(unittest.TestCase):
    CUTOFFS = {"anthropic": date(2026, 1, 31), "openai": date(2026, 3, 1),
               "google": date(2026, 2, 15)}

    def test_recency_gate_uses_latest_cutoff(self):
        cands = [_cand("old", date(2026, 2, 20)),   # after 2 cutoffs, not all
                 _cand("edge", date(2026, 3, 1)),   # equal to gate -> dropped
                 _cand("new", date(2026, 3, 2))]
        report = FilterReport()
        kept = recency_gate(cands, self.CUTOFFS, report)
        self.assertEqual([c.task_id for c in kept], ["new"])
        self.assertEqual(sum(len(v) for v in report.dropped.values()), 2)

    def test_recency_gate_requires_cutoffs(self):
        with self.assertRaises(ValueError):
            recency_gate([_cand("x", date(2026, 5, 1))], {})

    def test_star_cap_drops_prominent_repos(self):
        kept = star_cap([_cand("a", date(2026, 4, 1), stars=50),
                         _cand("b", date(2026, 4, 1), stars=50_000)], 1000)
        self.assertEqual([c.task_id for c in kept], ["a"])

    def test_selection_rule_is_deterministic(self):
        cands = [_cand("z", date(2026, 4, 2)), _cand("a", date(2026, 4, 2)),
                 _cand("m", date(2026, 4, 1))]
        picked = select_first_n(cands, 2)
        self.assertEqual([c.task_id for c in picked], ["m", "a"])

    def test_selection_records_dropped_tail(self):
        # Self-review 2026-07-15: selection was the one step with silent drops.
        report = FilterReport()
        cands = [_cand(f"t{i}", date(2026, 4, 1 + i)) for i in range(5)]
        select_first_n(cands, 3, report)
        dropped = [tid for ids in report.dropped.values() for tid in ids]
        self.assertEqual(sorted(dropped), ["t3", "t4"])


class TestCLIJudgeBackend(unittest.TestCase):
    """Self-review 2026-07-15: judges.py had zero coverage — the module that
    physically implements the D-015 binding condition."""

    def _backend(self, stdout="", stderr="", rc=0, family="anthropic", seen=None):
        from harness.judges import CLIJudgeBackend

        def fake(cmd, stdin, cwd):
            if seen is not None:
                seen.append((tuple(cmd), stdin, cwd))
            return ExecResult(stdout, stderr, rc)
        return CLIJudgeBackend(family, executor=fake)

    def _payload(self, claim="off-by-one in pagination"):
        from harness.scoring.band2 import JudgePayload
        return JudgePayload(defect_annotation="loop stops early", claim_text=claim)

    def test_parses_verdict(self):
        b = self._backend('```json\n{"is_match": true, "reasoning": "same bug"}\n```')
        v = b.judge(self._payload())
        self.assertTrue(v.is_match)
        self.assertEqual(v.judge_family, "anthropic")

    def test_prompt_carries_only_the_two_artifacts(self):
        seen = []
        b = self._backend('```json\n{"is_match": false, "reasoning": "no"}\n```',
                          seen=seen)
        b.judge(self._payload(claim="CLAIMTEXT"))
        (_cmd, stdin, cwd) = seen[-1]
        self.assertIn("CLAIMTEXT", stdin)
        self.assertIn("loop stops early", stdin)
        self.assertNotIn("case", stdin.lower().replace("in case", ""))  # no case ids
        self.assertTrue(str(cwd).startswith("/") and "judge-" in str(cwd))

    def test_nonzero_exit_raises(self):
        from harness.judges import JudgeCallError
        with self.assertRaises(JudgeCallError):
            self._backend(rc=1, stderr="boom").judge(self._payload())

    def test_missing_block_raises(self):
        from harness.judges import JudgeCallError
        with self.assertRaises(JudgeCallError):
            self._backend("I think yes?").judge(self._payload())

    def test_malformed_json_raises(self):
        from harness.judges import JudgeCallError
        with self.assertRaises(JudgeCallError):
            self._backend('```json\n{"is_match": }\n```').judge(self._payload())

    def test_missing_is_match_raises(self):
        from harness.judges import JudgeCallError
        with self.assertRaises(JudgeCallError):
            self._backend('```json\n{"reasoning": "sure"}\n```').judge(self._payload())

    def test_unknown_family_rejected(self):
        from harness.judges import CLIJudgeBackend
        with self.assertRaises(ValueError):
            CLIJudgeBackend("acme")

    def test_tool_use_in_transcript_invalidates_judgment(self):
        # D-020: any tool invocation in a judge transcript invalidates.
        from harness.judges import JudgeComplianceError
        transcript = ('exec\n$ cat /etc/hosts\n'
                      '```json\n{"is_match": true, "reasoning": "peeked"}\n```')
        with self.assertRaises(JudgeComplianceError):
            self._backend(transcript, family="openai").judge(self._payload())


class TestGeminiAPIJudge(unittest.TestCase):
    """D-019: Google judge is a bare API call — tools-disabled by construction."""

    def _backend(self, status=200, answer='```json\n{"is_match": true, "reasoning": "ok"}\n```',
                 raw=None, seen=None):
        from harness.judges import GeminiAPIJudgeBackend
        import json as _json
        body = raw if raw is not None else _json.dumps(
            {"candidates": [{"content": {"parts": [{"text": answer}]}}]})

        def fake_post(url, headers, payload):
            if seen is not None:
                seen.append((url, headers, payload))
            return status, body
        return GeminiAPIJudgeBackend(api_key="test-key", http_post=fake_post)

    def _payload(self):
        from harness.scoring.band2 import JudgePayload
        return JudgePayload(defect_annotation="ann", claim_text="claim")

    def test_parses_api_verdict(self):
        v = self._backend().judge(self._payload())
        self.assertTrue(v.is_match)
        self.assertEqual(v.judge_family, "google")

    def test_missing_key_raises(self):
        import os
        from harness.judges import GeminiAPIJudgeBackend, JudgeCallError
        old = os.environ.pop("GEMINI_API_KEY", None)
        try:
            with self.assertRaises(JudgeCallError):
                GeminiAPIJudgeBackend()
        finally:
            if old is not None:
                os.environ["GEMINI_API_KEY"] = old

    def test_http_error_raises(self):
        from harness.judges import JudgeCallError
        with self.assertRaises(JudgeCallError):
            self._backend(status=429, raw='{"error": "quota"}').judge(self._payload())

    def test_request_carries_only_payload_prompt(self):
        seen = []
        self._backend(seen=seen).judge(self._payload())
        (_url, headers, body) = seen[-1]
        text = body["contents"][0]["parts"][0]["text"]
        self.assertIn("ann", text)
        self.assertIn("claim", text)
        self.assertIn("x-goog-api-key", headers)


class TestReviewerCompliance(unittest.TestCase):
    """D-018: post-hoc test-suite-invocation scan."""

    def test_detects_test_suite_invocations(self):
        from harness.compliance import scan_reviewer_transcript
        for cmd in ("pytest -x tests/", "python3 -m unittest discover",
                    "npm test", "go test ./...", "cargo test", "make test",
                    "yarn test --watch=false", "dotnet test"):
            self.assertTrue(scan_reviewer_transcript(f"I ran `{cmd}` to check"),
                            cmd)

    def test_clean_transcript_passes(self):
        from harness.compliance import scan_reviewer_transcript
        clean = ("I read src/x.py, ran the linter, and inspected the diff. "
                 "The unit under test is the pagination helper. I did not "
                 "protest the design.")
        self.assertEqual(scan_reviewer_transcript(clean), [])


if __name__ == "__main__":
    unittest.main()
