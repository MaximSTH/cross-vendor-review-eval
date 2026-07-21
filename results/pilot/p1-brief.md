---
name: p1-brief
description: P1 batch brief — the 5 tasks, authoring-vendor assignment, and k=2 repeat positions, all fixed by pre-registered rule before any P1 session ran.
status: active
---

# P1 brief — 5-task throughput batch

**Authorization:** D-026 (P1 GO, 2026-07-21, through ~2026-07-25).
**Selection rules:** D-027 (resolving OQ-10/11/12). Everything on this page was
fixed **before any P1 session ran**; the raw selection output is committed at
`results/pilot/raw/p1-selection.json`.

## Rule applied (§8 / `harness/corpus/intake.py::select_first_n`)

SWE-bench-Live/MultiLang, combined **js + ts** splits (D-027a),
`created_at > 2026-03-01` (D-023a operative gate), ordered `created_at` ASC,
ties by `instance_id` → **rows 2–6** (row 1 is P0's task).

- Combined post-gate pool: **39** (js 17 + ts 22), re-verified live 2026-07-21,
  unchanged from the 2026-07-18 evidence table.
- **Rule self-check:** re-running the rule from scratch returned
  `thlorenz__doctoc-328` as row 1 — P0's task. Feed stable, rule correctly
  applied.

## Authoring assignment (D-027b)

Recorded coin flip → **position 1 = anthropic**; alternating thereafter.
Result: **anthropic 3 / openai 2**.

Reminder (from P0, carried forward): Codex authoring requires
`codex exec -s workspace-write`; the default read-only sandbox silently
produces no patch. Judge invocations (D-020) deliberately do **not** get
workspace-write.

## Repeat assignment (D-027c)

Seeded random draw of 2 of 5. **Seed `1607515562` → positions 3 and 4.**
The two fall on opposite authoring directions, so run-to-run variance is
measured in both. The **second** repeat executes only if no limit-hit events
have occurred by day 3 (D-021a) — see the limit-hit table in
`results/pilot/p1-log.md`.

**Open:** what a repeat re-runs (whole flow vs review arms only) is **OQ-13**,
to be ruled before the position-3 repeat. Not blocking tasks 1–5.

## The batch

| # | instance_id | repo | lang | created_at | base_commit | authors | k=2 |
|---|---|---|---|---|---|---|---|
| 1 | `code-charity__youtube-3708` | code-charity/youtube | js | 2026-03-16T12:49:20Z | `fdd34af1f2bf` | **anthropic** | — |
| 2 | `NVIDIA__NemoClaw-330` | NVIDIA/NemoClaw | ts | 2026-03-18T17:52:30Z | `4a1b7499759f` | **openai** | — |
| 3 | `thlorenz__doctoc-329` | thlorenz/doctoc | js | 2026-03-19T14:31:57Z | `428cf4189b60` | **anthropic** | ✅ |
| 4 | `can1357__oh-my-pi-489` | can1357/oh-my-pi | ts | 2026-03-20T09:08:07Z | `c412de1782eb` | **openai** | ✅ |
| 5 | `aralroca__next-translate-1259` | aralroca/next-translate | js | 2026-03-22T06:21:20Z | `f1fbf473b42c` | **anthropic** | — |

**Recorded covariate (D-027):** task 3 is the **same repository** as P0's task
(`thlorenz/doctoc`). Selected by the fixed rule; excluding it would be the
hand-picking §8 forbids. Reported, not corrected.

## Per-task flow (unchanged from P0)

1. Clone repo at `base_commit` into an isolated work dir outside both repos.
2. RepoLaunch: pull task `docker_image`, run `PASS_TO_PASS` baseline.
3. Authoring session (assigned vendor): problem statement only — no hints, no
   test patch. Capture patch + runtime-reported model ID.
4. A1 in-session self-review, then A2 (fresh, same vendor) and B (cross-vendor)
   with the ratified prompt (§8 pin) verbatim, in interleaver order.
5. Hidden tests (with `test_patch` applied) decide defective/correct — **after**
   all reviews are captured.
6. D-018 compliance scan (with D-025 exec-context patterns and its adjudication
   procedure), format-failure check (D-021), three-band scoring, D-020 judge
   audits if Band 2, secret-hygiene scan on every artifact.
7. Band 3 cards, if any, batch per protocol §4 — delivered as file paths only.
