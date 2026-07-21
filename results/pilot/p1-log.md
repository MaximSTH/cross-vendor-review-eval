---
name: p1-log
description: P1 execution log — working windows (pause/resume), limit-hit events, version drift, and per-session provenance pointers. Wall-clock elapsed is not session time; the throughput measure depends on the distinction.
status: active
---

# P1 execution log

Authorization: **D-026** (P1 GO, 2026-07-21, through ~2026-07-25).
Protocol: `docs/pilot-protocol.md` §2 (P1), §3 (measurements).
Ceiling declared (D-021b): **15 sessions/week**.

## Version drift since P0 (D-012 covariate — recorded, not corrected)

Both vendor CLIs auto-updated between P0 (2026-07-18) and P1 open
(2026-07-21). This is the designed-for case, not an incident: D-012 pins
nothing and analyzes drift as a covariate; D-012(b) interleaving is what keeps
the drift landing on all arms approximately equally.

| Stack | P0 (`results/pilot/raw/*-version.txt`) | P1 open | Delta |
|---|---|---|---|
| Codex CLI | `codex-cli 0.139.0` | `codex-cli 0.144.5` | 5 patch releases |
| Claude Code | `2.1.210` | `2.1.215` | 5 patch releases |

Runtime-reported **model** IDs are captured per session by the runner and are
the authoritative covariate; the CLI versions above are the harness half of
the pair. P0-vs-P1 comparisons must not be read as within-version.

Judge-stack note (D-019 alias ruling): any runtime-reported **judge** version
change during P1 triggers the before/after Band 2 agreement-rate discontinuity
check. No Band 2 volume yet (P0 reached Band 1 only), so no baseline exists —
first P1 Band 2 case establishes it.

## Environment readiness at P1 open (2026-07-21)

- colima running, macOS Virtualization.Framework, runtime docker — **aarch64**;
  task images are amd64 and run under emulation (slower; noted in provenance).
- Docker server 29.5.2.
- `CVRE_GEMINI_JUDGE_KEY` present in environment (presence checked only; value
  never read, per D-019 key handling).

## Working windows

| # | Open (owner tz) | Close | Sessions run | Notes |
|---|---|---|---|---|
| W1 | 2026-07-21 ~11:45 | — | **0** | P1 GO received; D-026 logged. Task 1 blocked on OQ-10/11/12 → ruled in-window → D-027, batch fixed. Task 1 step-2 baseline then found **ground-truth breakage** (41 of 44 F2P already pass at base; P2P empty) → **protocol §5 escalation, P1 paused at OQ-14**. Zero authoring/review sessions run. |

**Session count for throughput purposes: 0.** Window W1 was spent on
pre-registration and corpus validation, neither of which is a session. The
throughput denominator must not be inflated by it.

## Execution-environment incidents (not limit-hits; recorded per §3 discipline)

| When | What | Consequence |
|---|---|---|
| 2026-07-21 W1 | **Orphaned container.** `TaskStop` on a screen run killed the driving Python but *not* the `docker run` it had spawned; `thlorenz__doctoc-329`'s container ran unattended for ~22 min. | Burned CPU and contended with concurrent screen runs under amd64 emulation. Killed manually. **Standing lesson:** stopping a runner does not stop its containers — check `docker ps` after any interrupted run, especially before timing anything. No session wall-clock was measured during the window, so no throughput figure is contaminated. |

## Discarded sessions (worker error — counted against usage, never scored)

| # | When | Arm | Why discarded | Usage consumed |
|---|---|---|---|---|
| D1 | 2026-07-21 07:53:11Z | position 1, arm B (openai) | **Worker launched the reviewer with `-s workspace-write`.** That flag exists for the *authoring* condition (P0 finding); a review arm needs read access only, and write capability would let a reviewer mutate the tree under evaluation. Stopped ~40s in, before any tool call that wrote. Re-run with `-s read-only`. | ~40s of one codex session |

**Verified before re-running, not assumed:** the B tree's `git diff` was
byte-identical to `authored.patch` and no `codex exec` process survived the
stop — so the re-run started from an uncontaminated tree. (The orphaned-
container incident above is why that check now happens every time a run is
killed.)

*Why this is logged at all:* the discarded attempt consumed real subscription
usage against the D-021b ceiling. Counting only successful sessions would
flatter the throughput figure P1 exists to measure.

## Limit-hit events (D-021a day-3 conditional depends on this table)

| # | Reported | Vendor | Deferred | Voided | Evidence |
|---|---|---|---|---|---|
| **L1 (counts as event 1 — D-031c)** | 2026-07-21, supervisor-reported ("limit window has reset") | anthropic (assumed; not observable from session artifacts) | **Nothing** | **Nothing** | A1 completed at **06:11:09Z** with `exit=0`, `subtype: success`, `is_error: false`, 19 turns, and a well-formed 2-claim block. The supervisor's report arrived after that timestamp. No limit signature appears in `a1-stderr.txt`, the result JSON, or the 202-entry session transcript. |

**Handling (branch (a) of the supervisor's instruction).** A1 completed and
emitted its structured claims before any limit effect, so it is scored
normally and the flow proceeded to A2/B. **No session was voided and task 1
has no missing A1 cell.**

*Recorded honestly, because the distinction matters for D-021a's day-3
conditional:* the worker cannot independently confirm a limit-hit **event**
from its own artifacts — nothing in the session record shows a throttle. What
is confirmed is the **absence of any effect on a session**. This row is
therefore counted as a supervisor-reported limit window with **zero
session-level consequence**, and it is deliberately not treated as a
zero-consequence event being silently dropped from the count. **Ruled (D-031c): it counts as event 1** toward D-021a's day-3 conditional,
supervisor-reported basis noted. Rationale: the conditional protects against
**capacity contention**, and zero-consequence-this-time is **luck, not
absence**.

**Consequence, stated now so it is not a surprise later:** D-021a makes the
**second k=2 repeat conditional on zero limit-hit events by day 3.** With
event 1 on the board on day 1, that condition is **already failed** unless the
supervisor rules otherwise — so the pilot should expect **one** k=2 repeat
(position 3), not two. Flagged rather than discovered at the deadline.

## Per-task provenance

*(task id → brief, sessions.jsonl rows, scoring json — none yet)*
