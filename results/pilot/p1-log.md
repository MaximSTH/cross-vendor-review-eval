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
| W1 | 2026-07-21 ~11:45 | — | 0 (blocked) | P1 GO received; D-026 logged. Task 1 **blocked** on OQ-10/OQ-11/OQ-12 (task-selection scope, vendor assignment, repeat-task rule) — all design-level, all required *before* task 1 to keep D-021a/§8 pre-registration honest. Ruling requested from supervisor in-window. |

## Limit-hit events (D-021a day-3 conditional depends on this table)

*(time, vendor, what was deferred — none yet)*

## Per-task provenance

*(task id → brief, sessions.jsonl rows, scoring json — none yet)*
