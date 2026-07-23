---
name: p1-checkpoint
description: P1 completion checkpoint — all 5 positions run, oracle outcomes, per-arm scoring, findings, session/throughput tally. The supervisor's review anchor at P1 close.
status: active
---

# P1 completion checkpoint (2026-07-23)

**All 5 positions complete.** Authorized under D-026; run across 2026-07-21→23
in supervised + unattended windows. This is the review anchor; the full pilot
report (protocol §6) is drafted from here.

## Oracle outcomes (defect yield 2/5)

| pos | task | authoring vendor | oracle | sample |
|---|---|---|---|---|
| 1 | `haraka__Haraka-3535` | anthropic | RESOLVED | authoring success — neither |
| 2 | `NVIDIA__NemoClaw-330` | openai | **CONFIRMED DEFECTIVE** | defective |
| 3 | `thlorenz__doctoc-329` | anthropic | RESOLVED | authoring success — neither |
| 4 | `openai__codex-plugin-cc-83` | openai | RESOLVED | authoring success — neither |
| 5 | `aralroca__next-translate-1259` | anthropic | **CONFIRMED DEFECTIVE** | defective |

Vendor balance authored: anthropic 3 / openai 2 (D-027b). Defect yield **2/5**
(a §7 sizing input: authoring runs per harvested defect ≈ 2.5).

## Scoring — the two defective cases (Band 1, ±5, sweep-stable)

| pos | A1 (self) | A2 (fresh same-vendor) | B (cross-vendor) | audited catches |
|---|---|---|---|---|
| 2 | no_catch (0 claims) | **catch→no_catch** (P-002) | **catch→no_catch** (P-003) | **0/2** |
| 5 | no_catch | no_catch | no_catch | — (no catches) |

**Both defective cases → zero audited catches.** pos2 by audit overturning two
mechanical catches (coincidental localization P-002, inverted claim P-003);
pos5 by unanimous mechanical no_catch. Catch-audit human–Band1 agreement: **0/2**
(F-001).

**Central finding F-001 — "diff-anchoring":** when the authored fix lands in a
different location than the true defect, reviewers critique the change in front
of them and miss the real bug elsewhere. All three instances: P0 (unanimous
zero claims), pos2, pos5. Stated with n; the main-study sizing hypothesis.

## k=2 repeats (positions 3, 4 — both non-defective)

Both pre-registered repeat positions resolved → **catch-rate run-to-run
variance UNMEASURED**; repeats measured **verbosity variance** only (D-052).
Cross/same-vendor did not predict stability. §7 note for Step 3: repeat on
confirmed-defective cases.

## Sessions & throughput

- **24 logged sessions** (anthropic 13 / openai 11) + **1 discarded**
  (worker-error, D-041) + **1 A1-not-repeatable** structural gap (pos3/5 A1 r2,
  D-042; pos4 too). All consumed sessions count vs the D-021b ceiling (D-031g).
- **Session wall-clock:** 87 min total, mean 216 s, range 38–551 s.
- **Throughput caveat (binding, per D-026):** the ~24 sessions spread across 3
  calendar days of heavily-interrupted windows do **not** yield a clean
  sessions/day; W1's first-batch overhead (pre-registration, 3 escalations,
  corpus screening) is excluded from the rate (logged in `p1-log.md`).
  Final-n is **declaration-driven** (ceiling 15 < any measured rate), per
  D-021b — stated where n is computed, not as a measured quantity.

## Corpus-integrity finding (headline, promoted from Step-3 input)

Screening the post-gate JS/TS pool measured a **~29% usable rate** (5 PASS of
17 rows walked to fill 5 positions + replacements). **Five distinct
failure modes, four feed-attributable** (label integrity ×3, missing image,
eval-harness failure) + one rig-relative (`platform_infeasible` hard/time).
Far below the OQ-9 evidence table's implied filtering. Full taxonomy + skip
trail in DECISIONS.md (D-049) and `p1-brief.md`. **Corpus re-ratification
(D-023) remains a Step-3 Hanoi decision (D-028c), not a mid-pilot swerve.**

## Instruments validated / hardened during P1

- **Ground-truth screen (D-028)** adopted; caught label defects pre-session.
- **Oracle-authoritative eval (D-038)** — test_patch resets oracle files;
  `parsed==0`→HARNESS-ERROR (D-045); memory headroom + **VM resized 2→8 GiB**.
- **Incoherence heuristic (D-047)** — a coherence check at every pipeline stage;
  three saves (intake, procedure, evaluation), all false verdicts caught.
- **Read-only review arms** both stacks (D-031f codex, D-041 claude).
- **D-018 exec-context adjudications** — 4 quotation channels catalogued
  (commit-subject, test-file mock, package.json, source regex), all batched for
  the pilot-close scanner freeze (D-036/D-050).
- **models-observed table (D-012)** + codex model-ID gap closed via config
  introspection (gpt-5.6-sol @ xhigh).

## Open for supervisor (nothing blocking; queued for return)

- Step-3 pre-registration items: OQ-21 (semantic-catch layer + quota check),
  OQ-23 (model-tier arm), D-031b (false-alarm sample construction), D-052 §7
  (repeats on defective cases), scanner-freeze application of the 4 channels.
- The pilot report (§6) drafts from this checkpoint; final-n computation and
  go/no-go recommendation are the remaining deliverables.

## Band 3

Only batch **p1-b1** (pos2's 2 catches) generated cards; **ruled by the
supervisor** (both no_catch). No other case produced catches (pos5 unanimous
no_catch; pos1/3/4 authoring successes, not scored). **No audit cards pending.**
