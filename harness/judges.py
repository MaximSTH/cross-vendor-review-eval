"""Real Band 2 judge backends: headless, single-shot CLI calls (D-013, D-015).

Judges are NOT agentic: one prompt in, one verdict out, no repo access — the
D-015 binding condition (judges see exactly the anonymized claim and the
answer-key annotation, never patch or repo content) is enforced structurally
by JudgePayload and physically here by running the CLI in an empty scratch
directory with only the payload text on stdin.

Which binary serves each family is runner config (mechanics, per OQ-1
resolution): anthropic -> claude, openai -> codex, google -> gemini
(the Antigravity CLI is not installed on this machine; gemini is the same
model family).
"""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

from .runner import Executor, _default_executor
from .scoring.band2 import JudgePayload
from .scoring.models import JudgeVerdict

JUDGE_CMDS: dict[str, tuple[str, ...]] = {
    "anthropic": ("claude", "-p"),
    "openai": ("codex", "exec", "--skip-git-repo-check", "-"),
    "google": ("gemini", "-p"),
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

_JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


class JudgeCallError(RuntimeError):
    """The judge CLI failed or returned an unparseable verdict."""


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
        # Empty scratch dir: even an agentic-capable CLI has nothing to read.
        with tempfile.TemporaryDirectory(prefix="judge-") as scratch:
            result = self._executor(list(JUDGE_CMDS[self.family]), prompt, Path(scratch))
        if result.returncode != 0:
            raise JudgeCallError(
                f"{self.family} judge exited {result.returncode}: {result.stderr[:500]}")
        matches = _JSON_BLOCK_RE.findall(result.stdout)
        if not matches:
            raise JudgeCallError(f"{self.family} judge returned no verdict block")
        try:
            verdict = json.loads(matches[-1])
        except json.JSONDecodeError as e:
            raise JudgeCallError(f"{self.family} judge verdict not valid JSON: {e}") from e
        if not isinstance(verdict.get("is_match"), bool):
            raise JudgeCallError(f"{self.family} judge verdict missing boolean is_match")
        return JudgeVerdict(
            judge_family=self.family,
            is_match=verdict["is_match"],
            reasoning=str(verdict.get("reasoning", "")),
        )
