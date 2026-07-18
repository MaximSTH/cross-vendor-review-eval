# P0 brief — single case end to end (authorized 2026-07-18, tonight only)

**Authorization bounds:** P0 only; supervised window until ~22:00 supervisor
time; one fix-and-rerun cycle authorized for mechanical failures while the
supervisor is present; hard stop at window close regardless of outcome. No P1,
no second task.

## Task (selected before any session, by the pre-registered rule)

- **Selection rule applied (§8 / D-023d):** SWE-bench-Live/MultiLang, combined
  JS+TS slice, `created_at` > 2026-03-01 (D-023a operative gate), ordered
  `created_at` ASC, ties by instance_id → **first row**.
- **Selected:** `thlorenz__doctoc-328` — repo `thlorenz/doctoc`, JS,
  created 2026-03-13T04:30:10Z, base commit `6393281f839d`.
- Slice size at selection: 39 post-gate JS/TS tasks (17 js + 22 ts), queried
  live via HF datasets-server (metadata only).
- Record carries: `FAIL_TO_PASS`/`PASS_TO_PASS`, `test_patch`, official
  `patch` (ground-truth defect location source), `docker_image`, `test_cmds`,
  `log_parser` — RepoLaunch flow to be validated per D-023c.

## Authoring vendor (coin flip, recorded before any session)

- Flip: `secrets.choice(['anthropic','openai'])` → **openai (Codex CLI)
  authors.**
- Therefore: A1 = Codex in-session self-review; A2 = Codex fresh session;
  B = Claude Code cold. Band 2 panels per D-015 rotation on the reviewing
  session's family.

## Session plan

1. Checkout `thlorenz/doctoc` at base commit into an isolated work dir
   (outside both public repos).
2. Validate RepoLaunch Docker flow: pull task `docker_image`, run
   `PASS_TO_PASS` baseline (D-023c condition; failure → SWE-rebench fallback
   triggers, P0 halts for supervisor).
3. Authoring session (Codex): problem statement only — no hints, no test
   patch. Capture patch + runtime-reported version.
4. A1 in-session ask, then A2/B with the ratified prompt (§8 pin), verbatim,
   interleaver order.
5. Hidden tests (with `test_patch` applied) decide defective/correct — after
   all reviews are captured.
6. Three-band scoring; D-018 + format scans; D-020 judge audits if Band 2;
   secret-hygiene scan on all artifacts; provenance JSONL to
   `results/pilot/`.
7. Band 3 card (if any) delivered by file path per protocol §4.
