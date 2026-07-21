---
name: p1-brief
description: P1 batch brief — the 5 task positions, authoring-vendor assignment, k=2 repeat positions, and the full ground-truth screen trail including every skipped row and its reason.
status: active
---

# P1 brief — 5-task throughput batch

**Authorization:** D-026 (P1 GO, 2026-07-21, through ~2026-07-25).
**Selection rules:** D-027 (OQ-10/11/12), D-028 (screen + replacement),
D-030 (platform_infeasible + unified ERROR handling).

Everything on this page was fixed **before any P1 session ran**. Raw
provenance: `results/pilot/raw/p1-selection.json` (selection),
`results/pilot/raw/p1-gt-screen/` (screen verdicts, runner, pool, image
availability).

## Rule applied (§8 / `harness/corpus/intake.py`)

SWE-bench-Live/MultiLang, combined **js + ts** splits (D-027a),
`created_at > 2026-03-01` (D-023a), ordered `created_at` ASC, ties by
`instance_id`, **rows 2 onward** (row 1 = P0's task), each admitted only if it
passes the D-028 ground-truth screen.

- Combined post-gate pool: **39** (js 17 + ts 22), re-verified live 2026-07-21.
- **Rule self-check:** re-running the rule from scratch returned
  `thlorenz__doctoc-328` as row 1 — P0's task. Feed stable, rule correct.

## Authoring assignment (D-027b)

Recorded coin flip → **position 1 = anthropic**; alternating thereafter →
**anthropic 3 / openai 2**. A replacement inherits its **position's**
assignment; the position is fixed, only the task moves.

Carried forward from P0: Codex authoring requires
`codex exec -s workspace-write` (the default read-only sandbox silently
produces no patch). Judge invocations (D-020) deliberately do **not** get it.

## Repeat assignment (D-027c, D-029, D-030d)

Seeded draw, **seed `1607515562` → positions 3 and 4**. The draw selected
**positions, not tasks**, so position 4's *replacement* inherits the k=2 flag
(D-030d). The second repeat executes only if no limit-hit events have occurred
by day 3 (D-021a).

Per **D-029**, a repeat holds the original authored patch fixed and re-runs
**the review arms only** (A1/A2/B). Authoring variance is deliberately
unmeasured; that is a stated limitation, not an omission.

## The batch (final)

| # | instance_id | repo | lang | base_commit | authors | k=2 | screen |
|---|---|---|---|---|---|---|---|
| 1 | `haraka__Haraka-3535` | haraka/Haraka | js | `37f2d18c2f75` | **anthropic** | — | PASS (F2P 2 fail, P2P 358 pass, 361 parsed) |
| 2 | `NVIDIA__NemoClaw-330` | NVIDIA/NemoClaw | ts | `4a1b7499759f` | **openai** | — | PASS (F2P 3 fail, P2P 300 pass, 303 parsed) |
| 3 | `thlorenz__doctoc-329` | thlorenz/doctoc | js | `428cf4189b60` | **anthropic** | ✅ | PASS (F2P 8 fail, P2P 169 pass, 177 parsed) |
| 4 | *pending replacement* | — | — | — | **openai** | ✅ | walk resumes at row 11 |
| 5 | `aralroca__next-translate-1259` | aralroca/next-translate | js | `f1fbf473b42c` | **anthropic** | — | PASS (F2P 1 fail, P2P 146 pass, 147 parsed) |

**Recorded covariate (D-027):** position 3 shares a repository with P0's task
(`thlorenz/doctoc`). Selected by the fixed rule; excluding it would be the
hand-picking §8 forbids. Reported, not corrected.

## Skip trail — every row excluded, with reason (D-028b, §5)

Positions are filled by walking the fixed ordering. Nothing is skipped
silently.

| row | instance_id | verdict | why |
|---|---|---|---|
| 2 | `code-charity__youtube-3708` | **FAIL** | **41 of 44 declared F2P tests already PASS at base; P2P empty.** The feed labelled the repo's entire suite as F2P. Originally position 1. |
| 7 | `Mintplex-Labs__anything-llm-5252` | **ERROR** `image_missing` | Declared `docker_image` returns 404. Verified directly against the Docker Hub registry, not inferred from a pull failure. Diagnosed → may skip (D-030b). |
| 8 | `Automattic__mongoose-16153` | **ERROR** `image_missing` | Same; verified 404. |
| 9 | `GladysAssistant__Gladys-2504` | **FAIL** | **Both declared F2P test names exist nowhere in the suite after the shipped test_patch applies cleanly.** The file contains two differently-named tests, and all 3444 tests pass at base — the task has **no failing oracle at all**. Distinct sub-signature from row 2's. |
| 5 | `can1357__oh-my-pi-489` | **ERROR** `platform_infeasible` | `bun` binary → `Illegal instruction (core dumped)`. **Infeasible under this study's execution environment: amd64 emulation on Apple Silicon** — not a property of the task, which would run on amd64 hardware (D-030a). Originally position 4; its k=2 flag transfers to the replacement. |

Diagnosis discipline (D-030b): every skip above rests on an identified,
verified cause. An **undiagnosed** ERROR halts and escalates instead — enforced
by `UndiagnosedScreenError`, not by convention.

## Screen verdicts are single-implementation (D-030e)

All verdicts above come from the final runner
(`results/pilot/raw/p1-gt-screen/gt-screen-runner.py`). Results from the three
superseded screen implementations are **void for the record**; the defects
that produced them are preserved in D-028's near-miss note, and none of them
retired a task.

## Per-task flow

1. Clone repo at `base_commit` into an isolated work dir outside both repos.
2. **D-028 ground-truth screen** (done above — admission gate, outcome-blind).
3. Authoring session (assigned vendor): problem statement only — no hints, no
   test patch. Capture patch + runtime-reported model ID + wall-clock.
4. A1 in-session self-review, then A2 (fresh, same vendor) and B (cross-vendor)
   with the ratified prompt (§8 pin) verbatim, in interleaver order.
5. Hidden tests decide defective / not-confirmed-defective — **after** all
   reviews are captured.
6. D-018 compliance scan (D-025 exec-context patterns + adjudication
   procedure), format-failure check (D-021), three-band scoring, D-020 judge
   audits if Band 2, secret-hygiene scan on every artifact.
7. Band 3 cards batch per protocol §4 — delivered as file paths only.

**Measurement-integrity rule (worker, standing):** pool-wide screening and any
other container work runs **only while no session is running**. Concurrent
amd64-emulated containers inflate the session wall-clock that P1 exists to
measure.
