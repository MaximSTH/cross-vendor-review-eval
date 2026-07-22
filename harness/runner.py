"""Session runner: drives the shipped subscription CLIs and records provenance.

D-012: sessions run on the auto-updating subscription CLIs. Every session
records the model ID and harness version the CLI reports at runtime; the runner
never pins or assumes a version. No session is executed until pilot
authorization (Step 2b gate) — this module is exercised by tests with an
injected executor until then.

Command templates are config, not design: exact flags may be adjusted at pilot
without a decision-log entry, as long as the prompt (OQ-3) and the recorded
provenance fields do not change.
"""

from __future__ import annotations

import json
import re
import subprocess  # noqa: S404 — drives local CLIs by design
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from .scoring.models import Claim

Executor = Callable[[list[str], Optional[str], Optional[Path]], "ExecResult"]


@dataclass(frozen=True)
class ExecResult:
    stdout: str
    stderr: str
    returncode: int


def _default_executor(cmd: list[str], stdin: Optional[str], cwd: Optional[Path],
                      env: Optional[dict] = None) -> ExecResult:
    import os
    merged = {**os.environ, **env} if env else None
    proc = subprocess.run(cmd, input=stdin, cwd=cwd, capture_output=True,
                          text=True, timeout=3600, env=merged)
    return ExecResult(proc.stdout, proc.stderr, proc.returncode)


@dataclass(frozen=True)
class VendorCLI:
    """One vendor stack. Templates take the prompt via stdin."""
    family: str                     # anthropic | openai | google
    review_cmd: tuple[str, ...]     # headless review invocation
    version_cmd: tuple[str, ...]    # prints harness + model info


# Defaults are best-effort; verified and adjusted at pilot (mechanics, not design).
#
# SANDBOX LAUNCH RULE (D-031f) — standing, not per-run judgement:
#   AUTHORING arms run with write access (`codex exec -s workspace-write`).
#     The default read-only sandbox silently produces no patch (P0 finding).
#   REVIEW arms run READ-ONLY (`codex exec -s read-only`).
#     A reviewer needs read access only; write capability would let it mutate
#     the tree under evaluation, corrupting the patch being reviewed and
#     everything scored downstream. A P1 position-1 launch used
#     workspace-write for arm B by mistake; it was caught ~40s in, the tree was
#     verified byte-identical to the authored patch, and the session was
#     discarded and re-run. Hence a rule rather than a habit.
#   JUDGE invocations get neither (D-020): tools disabled/isolated entirely.
AUTHORING_SANDBOX_FLAGS = {"openai": ("-s", "workspace-write")}
REVIEW_SANDBOX_FLAGS = {"openai": ("-s", "read-only")}
# D-041: Claude review arms enforce read-only by DISALLOWING edit tools. The
# authoring arm keeps them (it must write the patch). `--permission-mode
# acceptEdits` on a review arm permits tree edits under review (the Claude analog
# of workspace-write) -- forbidden. Verified: no review arm actually edited, but
# the capability is closed by construction going forward.
REVIEW_DISALLOWED_TOOLS = {"anthropic": ("Edit", "Write", "NotebookEdit")}

VENDOR_CLIS = {
    "anthropic": VendorCLI("anthropic",
                           ("claude", "-p", "--output-format", "text"),
                           ("claude", "--version")),
    "openai": VendorCLI("openai",
                        ("codex", "exec", "-s", "read-only", "-"),
                        ("codex", "--version")),
    "google": VendorCLI("google",
                        ("antigravity", "exec", "-"),
                        ("antigravity", "--version")),
}

# Case-insensitive fence tag: models occasionally emit ```JSON. Shared with
# judges.py (cross-vendor review 2026-07-15: was duplicated + case-sensitive).
JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)


class ClaimFormatError(ValueError):
    """Reviewer output did not carry a valid structured claims block."""


def extract_claims(output: str) -> tuple[Claim, ...]:
    """Parse the LAST fenced ```json claims block from reviewer output.

    The prompt requires the block to be the final element; taking the last
    match tolerates earlier fenced examples the agent may have echoed.
    Every malformed shape raises ClaimFormatError — never a bare TypeError —
    so run_review_session records format errors instead of crashing
    (cross-vendor review 2026-07-15, Medium).
    """
    matches = JSON_BLOCK_RE.findall(output)
    if not matches:
        raise ClaimFormatError("no fenced json claims block in reviewer output")
    try:
        payload = json.loads(matches[-1])
    except json.JSONDecodeError as e:
        raise ClaimFormatError(f"claims block is not valid JSON: {e}") from e
    if not isinstance(payload, dict) or "claims" not in payload:
        raise ClaimFormatError('claims block must be an object with a "claims" list')
    if not isinstance(payload["claims"], list):
        raise ClaimFormatError('"claims" must be a list (got '
                               f'{type(payload["claims"]).__name__})')
    claims = []
    for i, c in enumerate(payload["claims"]):
        if not isinstance(c, dict) or "description" not in c:
            raise ClaimFormatError(f"claim {i} missing description")
        line = c.get("line")
        if line is not None and not isinstance(line, int):
            raise ClaimFormatError(f"claim {i} line must be int or null")
        file = c.get("file")
        if file is not None and not isinstance(file, str):
            raise ClaimFormatError(f"claim {i} file must be string or null")
        claims.append(Claim(description=str(c["description"]),
                            file=file, line=line))
    return tuple(claims)


def probe_version(cli: VendorCLI, executor: Executor = _default_executor) -> str:
    """Runtime-reported version string (D-012). Never cached across sessions."""
    result = executor(list(cli.version_cmd), None, None)
    reported = (result.stdout or result.stderr).strip()
    return reported or "UNREPORTED"


@dataclass
class SessionRecord:
    """One session's provenance + output; serialized to the run log (JSONL)."""
    case_id: str
    condition: str
    family: str
    reported_version: str
    started_at: str
    finished_at: str = ""
    returncode: int = -1
    claims: list[dict] = field(default_factory=list)
    claim_format_error: str = ""
    raw_output_path: str = ""       # full transcript saved separately, never inlined

    def to_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True)


def run_review_session(
    cli: VendorCLI,
    case_id: str,
    condition: str,
    prompt: str,
    workdir: Path,
    raw_dir: Path,
    executor: Executor = _default_executor,
    now: Callable[[], str] = lambda: datetime.now(timezone.utc).isoformat(),
) -> tuple[SessionRecord, tuple[Claim, ...]]:
    """Run one review session and record provenance. Injected executor in tests."""
    record = SessionRecord(
        case_id=case_id, condition=condition, family=cli.family,
        reported_version=probe_version(cli, executor), started_at=now(),
    )
    result = executor(list(cli.review_cmd), prompt, workdir)
    record.finished_at = now()
    record.returncode = result.returncode

    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"{case_id}.{condition}.{cli.family}.txt"
    raw_path.write_text(result.stdout + ("\n--- stderr ---\n" + result.stderr if result.stderr else ""))
    record.raw_output_path = str(raw_path)

    claims: tuple[Claim, ...] = ()
    try:
        claims = extract_claims(result.stdout)
        record.claims = [{"file": c.file, "line": c.line, "description": c.description}
                         for c in claims]
    except ClaimFormatError as e:
        record.claim_format_error = str(e)
    return record, claims


def append_log(record: SessionRecord, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as f:
        f.write(record.to_json() + "\n")
