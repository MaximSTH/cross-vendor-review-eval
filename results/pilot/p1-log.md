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
| W1 | 2026-07-21 ~11:45 | 2026-07-21 ~15:10 (pause) | **5 run, 1 discarded** | P1 GO received; D-026 logged. Task 1 blocked on OQ-10/11/12 → ruled in-window → D-027, batch fixed. Task 1 step-2 baseline then found **ground-truth breakage** (41 of 44 F2P already pass at base; P2P empty) → **protocol §5 escalation, P1 paused at OQ-14**. Zero authoring/review sessions run. |

**W1 sessions (all against the D-021b ceiling, D-031g):**

| arm | family | wall-clock | outcome |
|---|---|---|---|
| pos1 author | anthropic | 9m11s | patch, 3 files |
| pos1 A1 | anthropic | 6m41s | 2 claims, D-018 clean |
| pos1 A2 | anthropic | 5m22s | 3 claims, D-018 clean |
| pos1 B | openai | 1m09s | 0 claims, D-018 clean |
| pos1 B (discarded) | openai | ~40s | worker error: workspace-write on a review arm |
| pos2 author | openai | 3m04s | patch capture defective → OQ-17 |

**Wall-clock caveat for the throughput computation:** W1 spanned ~3.5 hours of
elapsed time for ~26 minutes of session time. The remainder was
pre-registration, corpus screening, and three escalations — **first-batch
costs that will not recur per-task**. The sessions/week figure must be built
from session time and realistic per-task overhead, not from W1's elapsed
hours, or it will understate throughput badly.

## Pause — W1 close, 2026-07-21

**Boundary:** position 2's authoring session completed; the next arm (pos2 A1)
had **not** started. Clean boundary, no session interrupted, no tree in a
half-applied state.

**State at pause:**
- Position 1: complete through evaluation. Authoring success (D-031a) —
  throughput data only, artifacts retained.
- Position 2: authoring complete, **blocked on OQ-17 and OQ-18** before its
  review arms. The authoring work is intact in the tree; only patch *capture*
  is defective, and re-capture needs no session.
- Positions 3, 5: screened PASS, not started. Position 4: replacement not yet
  selected (walk resumes at row 11).

**Deliberately NOT done during the pause,** per the supervisor's "nothing new
starts while I'm away": the position-4 replacement screen. It was previously
slated for an offline window; the later instruction supersedes, and container
screening is new work rather than continuation.

**Resume:** on the supervisor's morning word, with OQ-17 and OQ-18 rulings.

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

**Consequence flagged on day 1, and subsequently ruled:** under D-021a as
originally written, event 1 would have eliminated the **second** k=2 repeat.
**Amended by D-032** (before day 3's evaluation and before either repeat ran):
the condition now tests for a limit event that **voided or deferred a
session**, which event 1 did not. Both repeats are expected to execute. Event 1
remains logged and counted here regardless.

## Per-task provenance

*(task id → brief, sessions.jsonl rows, scoring json — none yet)*


## Working window W2 — 2026-07-22

Positions 2 and 3 executed. Session tally this window: pos2 (author+A1+A2+B = 4),
pos3 run1 (author+A1+A2+B = 4) + pos3 run2 (A2, B = 2) = 10 sessions. Running
P1 total: **18 sessions + 1 discarded** (pos1 4, pos2 4, pos3 10).

Notable results:
- **pos2 CONFIRMED DEFECTIVE** — first real defect case; Band 1 A1 no_catch /
  A2 catch / B catch (both catches "right line", reasons questionable → OQ-19 →
  D-039 mechanical-catch audit; carded p1-b1).
- **pos3 run-to-run variance** (k=2, review arms only): B (cross-vendor)
  perfectly stable (`transform.js:43` both runs); A2 (fresh same-vendor) 0→2
  claims; A1 run2 pending OQ-20.

## Pause — W2 close, 2026-07-22

**Boundary:** position 3 run 1 complete; run 2's A2 and B complete; **A1 run 2
blocked on OQ-20** (in-session repeat mechanics). Position 3 oracle evaluation
deliberately **not run** — the blind boundary holds scoring until all reviews
(incl. A1 run 2) are captured or OQ-20 rules A1 run 2 out.

**Open for supervisor (in priority order):**
1. **OQ-20** — A1 k=2 repeat mechanics (blocks pos3 completion). Worker rec: (b).
2. **Band 3 batch p1-b1** — `results/band3/cards-p1-b1.html`, 2 mechanical-catch
   cards awaiting in-browser rulings + exported `band3-rulings.json`.
3. **OQ-16 companion** (false-alarm construction gap), **OQ-19 done**; no others
   block.

**Remaining P1 work:** pos3 oracle+scoring (after OQ-20), position 4
(replacement — screen of rows 11–15 was interrupted; re-run needed), position 5.

**Nothing new starts during the pause.** Position-4 replacement screening is
container work slated for an idle window, not the pause.
