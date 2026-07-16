"""Real Band 2 judge backends: headless, single-shot CLI calls (D-013, D-015).

Judges are NOT agentic: one prompt in, one verdict out — the D-015 binding
condition (judges see exactly the anonymized claim and the answer-key
annotation, never patch or repo content) is enforced structurally by
JudgePayload: nothing else is ever sent. Running in an empty scratch directory
is defense-in-depth, NOT proof of isolation — an agentic-capable CLI could in
principle read absolute paths if it chose to (self-review 2026-07-15, external
claim). Pilot task: verify per-CLI tool-restriction flags and pin them here.

Which binary serves each family is runner config (mechanics, per OQ-1
resolution): anthropic -> claude, openai -> codex, google -> gemini
(the Antigravity CLI is not installed on this machine; gemini is the same
model family).
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from . import compliance
from .runner import Executor, JSON_BLOCK_RE, _default_executor
from .scoring.band2 import JudgePayload
from .scoring.models import JudgeVerdict

# D-017: ALL judges run tools-fully-disabled; pin flags where the CLI supports
# it and verify by probe. Probe record:
#   anthropic 2026-07-15/16: bare `claude -p` READ an absolute repo path from
#     an empty dir (refuted the isolation assumption); with the disallow list
#     below the read is blocked (verified). "mcp__*" added per D-017 to cover
#     connectors; wildcard coverage to be re-probed at pilot.
#   openai 2026-07-16: `codex exec` read an absolute path under default AND
#     under -c 'sandbox_permissions=[]'; sandbox modes are write-side only.
#     NO supported tools-disable flag found -> OQ-7, supervisor ruling needed.
#   google 2026-07-16: `gemini` hard-fails IneligibleTierError on this account
#     regardless of the D-017 trust env var (account migrated to Antigravity,
#     which is not installed and was ruled out for judging) -> OQ-6.
_CLAUDE_JUDGE_DISALLOWED = (
    "Read,Bash,Glob,Grep,WebFetch,WebSearch,Task,Write,Edit,NotebookEdit,mcp__*"
)

JUDGE_CMDS: dict[str, tuple[str, ...]] = {
    "anthropic": ("claude", "-p", "--disallowedTools", _CLAUDE_JUDGE_DISALLOWED),
    "openai": ("codex", "exec", "--skip-git-repo-check", "-"),
    "google": ("gemini",),
}

# Per-family env for judge invocations (D-017: documented in provenance —
# results files must record this map verbatim alongside version strings).
JUDGE_ENVS: dict[str, dict[str, str]] = {
    "google": {"GEMINI_CLI_TRUST_WORKSPACE": "true"},  # supervisor-authorized, D-017
}

JUDGE_PROMPT_TEMPLATE = """You are scoring a code-review claim against a known defect. You see only the
two artifacts below — you have no repository access and need none.

KNOWN DEFECT (answer key):
{annotation}

REVIEWER'S CLAIM:
{claim}

Question: does the reviewer's claim describe the SAME underlying defect as the
answer key — such that a busy engineer acting on the claim would locate and fix
that defect?

Answer with ONLY a fenced JSON block:

```json
{{"is_match": true, "reasoning": "one sentence"}}
```
"""

class JudgeCallError(RuntimeError):
    """The judge backend failed or returned an unparseable verdict."""


class JudgeComplianceError(RuntimeError):
    """D-020: tool invocation detected in a judge transcript — the judgment is
    invalid; the caller re-runs and counts it in the reported audit metric."""


class CLIJudgeBackend:
    """One family's judge: single headless CLI call in an empty scratch dir."""

    def __init__(self, family: str, executor: Executor = _default_executor):
        if family not in JUDGE_CMDS:
            raise ValueError(f"no judge command configured for family {family!r}")
        self.family = family
        self._executor = executor

    def judge(self, payload: JudgePayload) -> JudgeVerdict:
        prompt = JUDGE_PROMPT_TEMPLATE.format(
            annotation=payload.defect_annotation, claim=payload.claim_text)
        env = JUDGE_ENVS.get(self.family)
        # Empty scratch dir is defense-in-depth only (see module docstring).
        with tempfile.TemporaryDirectory(prefix="judge-") as scratch:
            if env is None:
                result = self._executor(list(JUDGE_CMDS[self.family]), prompt, Path(scratch))
            else:
                result = self._executor(list(JUDGE_CMDS[self.family]), prompt,
                                        Path(scratch), env)
        if result.returncode != 0:
            raise JudgeCallError(
                f"{self.family} judge exited {result.returncode}: {result.stderr[:500]}")
        # D-020: transcript audit — any tool invocation invalidates.
        hits = compliance.audit_judge_transcript(
            self.family, result.stdout + "\n" + result.stderr)
        if hits:
            raise JudgeComplianceError(
                f"{self.family} judge transcript shows tool use: {hits}")
        return _parse_verdict(self.family, result.stdout)


def _parse_verdict(family: str, text: str) -> JudgeVerdict:
    matches = JSON_BLOCK_RE.findall(text)
    if not matches:
        raise JudgeCallError(f"{family} judge returned no verdict block")
    try:
        verdict = json.loads(matches[-1])
    except json.JSONDecodeError as e:
        raise JudgeCallError(f"{family} judge verdict not valid JSON: {e}") from e
    if not isinstance(verdict.get("is_match"), bool):
        raise JudgeCallError(f"{family} judge verdict missing boolean is_match")
    return JudgeVerdict(
        judge_family=family,
        is_match=verdict["is_match"],
        reasoning=str(verdict.get("reasoning", "")),
    )


# --- D-019: Google judge = free-tier Gemini API call -----------------------

GEMINI_API_MODEL = "gemini-2.5-flash"  # free-tier model; recorded in provenance
_GEMINI_API_URL = ("https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{GEMINI_API_MODEL}:generateContent")


def _default_http_post(url: str, headers: dict, body: dict) -> tuple[int, str]:
    import urllib.error
    import urllib.request
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


class GeminiAPIJudgeBackend:
    """D-019: a bare text-completion API call — tools-disabled by construction
    (no filesystem, no command execution, no MCP exists in this path)."""

    family = "google"

    def __init__(self, api_key: str | None = None, http_post=_default_http_post):
        import os
        self._api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if not self._api_key:
            raise JudgeCallError(
                "google judge needs GEMINI_API_KEY set (free tier, D-019)")
        self._post = http_post

    def judge(self, payload: JudgePayload) -> JudgeVerdict:
        prompt = JUDGE_PROMPT_TEMPLATE.format(
            annotation=payload.defect_annotation, claim=payload.claim_text)
        status, text = self._post(
            _GEMINI_API_URL, {"x-goog-api-key": self._api_key},
            {"contents": [{"parts": [{"text": prompt}]}]})
        if status != 200:
            raise JudgeCallError(f"google judge API returned {status}: {text[:300]}")
        try:
            data = json.loads(text)
            answer = "".join(
                part.get("text", "")
                for part in data["candidates"][0]["content"]["parts"])
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
            raise JudgeCallError(f"google judge API response unparseable: {e}") from e
        return _parse_verdict(self.family, answer)


def make_real_router(executor: Executor = _default_executor):
    """The D-015 rotating router over the three real judge backends
    (D-017/D-019/D-020 isolation per family)."""
    from .scoring.band2 import PanelRouter
    return PanelRouter({
        "anthropic": CLIJudgeBackend("anthropic", executor=executor),
        "openai": CLIJudgeBackend("openai", executor=executor),
        "google": GeminiAPIJudgeBackend(),
    })
