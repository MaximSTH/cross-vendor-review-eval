---
name: handoff
description: Session handoff — current state, active authorizations and bounds, open items, and in-flight nuance not yet in DECISIONS.md. Written 2026-07-18 at supervised-window close.
status: active
---

# HANDOFF — written 2026-07-18, window close

For a successor who has read [`DECISIONS.md`](DECISIONS.md) (D-001–D-025) and
[`pilot-protocol.md`](pilot-protocol.md) but lived none of it. The decision
log is the SSOT; this file adds only state, bounds, and nuance.

## Current state

- **Repo is PUBLIC:** github.com/MaximSTH/cross-vendor-review-eval, published
  2026-07-18 *before results existed* (deliberate). History rewritten to the
  owner's noreply email first (D-024, map in `hash-map.md`); local git config
  already uses the noreply address — never change it back.
- **Build: complete and accepted** (Step 2a, provenance `e1f7beb`). 83 unit
  tests green; mock canaries 4/4 (permanent, OQ-4); real-backend canaries 4/4.
- **P0: run and ACCEPTED** (2026-07-18, single-night authorization). Task
  `thlorenz__doctoc-328` (selected by the pre-registered rule, brief at
  `results/pilot/p0-brief.md`). Outcome: authored patch machine-confirmed
  **defective** (2/2 FAIL_TO_PASS failing), and **all three review arms
  returned zero claims** — a unanimous miss, cleanly captured. Scoring +
  provenance: `results/pilot/p0-scoring.json`, `results/pilot/raw/`.
  D-023c RepoLaunch validation PASSED → corpus is confirmed
  SWE-bench-Live/MultiLang; the SWE-rebench fallback did NOT trigger.

## Active authorizations and their bounds

- **Execution is FROZEN.** P0's authorization expired at window close. No
  reviewer sessions, no authoring sessions, no corpus harvesting beyond what
  intake tests require. **P1 authorization comes only from the supervisor,
  expected July 20–21 (from Da Nang).**
- Things that are standing (need no re-authorization): editing docs/code/tests
  locally, pushing to the public repo, logging open questions.
- Things that always need the supervisor: any design-doc change (via
  DECISIONS.md), any session execution, anything touching the ratified prompt
  (OQ-3 pin — reopening ratification), any new judge-input content (D-015
  binding condition).

## Open items (in priority order)

1. **P1 (on authorization):** 5 tasks per D-021, k=2 repeats on two tasks
   (second conditional on zero limit-hits by day 3), interleaved, with the
   supervisor's **normal-week ceiling declaration** collected at go (D-021b —
   still undeclared).
2. **Scanner pattern work (D-025):** exec-context patterns are seeded and
   regression-tested (`tests/fixtures/d018-false-positive-transcript.txt`);
   refinements during P1 are logged; **everything freezes at pilot close.**
   Same freeze applies to the anonymizer's vendor-furniture list (band2.py)
   and the judge tool-markers (compliance.py) — all need sampling from real
   P1 transcripts before freeze.
3. **Quota measurement (D-019/D-021c):** free-tier Gemini daily cap vs Band 2
   volume — P0 never reached Band 2 (zero claims → Band 1 everywhere), so
   quota remains unmeasured. P1 must capture it if any case reaches Band 2.
4. **Pilot report** (`results/pilot/report.md`, per protocol §6) — start it
   from the P0 findings; final-n computation waits for P1 throughput.

## In-flight nuance not yet in DECISIONS.md

- **Codex authoring needs `-s workspace-write`** — `codex exec` defaults to a
  read-only sandbox; P0's one authorized fix-and-rerun cycle was consumed
  discovering this. It is a P0 finding for the pilot report, not a D-entry.
  Judge invocations (D-020) deliberately do NOT get workspace-write.
- **A1 mechanics:** in-session self-review = `codex exec resume --last` in
  the authoring directory. A2/B run in separately cloned trees with
  `authored.patch` applied uncommitted (`git apply`), deps installed, so the
  change is visible via `git diff`. Rebuild trees fresh per case.
- **Colima runs Docker** (installed 2026-07-18); task images are amd64 and
  run under emulation — slower, works; noted in provenance. `/private/tmp`
  is NOT mounted into the colima VM — pipe files into containers via tar on
  stdin (see the P0 pattern), don't use `-v` from scratch dirs.
- **Session-scratch layout** (ephemeral, outside both repos): task record,
  prompts, transcripts land in the session scratchpad and are copied into
  `results/pilot/raw/` (secret-scanned) before commit. Raw transcripts of the
  P0 sessions are already committed.
- **Numbering discipline:** two supervisor ruling messages arrived with
  already-used D-numbers (→ D-023, D-025); the convention is: keep content
  verbatim, take the next free number, note the collision in-entry. Check the
  log's tail before assigning numbers.
- **Cite by commit/file, never by chat position** (OQ-3 correction note) —
  the supervisor verifies citations.
- **Context discipline (standing):** compact summaries + file paths in chat;
  no transcript dumps; Band 3 cards are delivered as file paths only, never
  inline.
- **D-022 (no adoption claims)** governs ALL outreach text from this repo,
  including the README if it is ever expanded.
- The supervisor rules fast and precisely; present evidence + option lists,
  take a position, and never resolve design-level ambiguity unilaterally —
  the permission layer has enforced this once already (incident preserved in
  D-017).

## The one-sentence version

The benchmark is public, the pipeline is proven end to end on a real task
whose defective patch fooled all three review arms, and everything now waits
— frozen — for the supervisor's P1 go from Da Nang.
