# Cross-vendor review report — harness build (D-014 gate)

**Target:** `harness/`, `canary/`, `tests/` at commit `608ec8b`.
**Protocol:** meta-layer-starter cross-vendor review — worker self-check in
fresh context + peer vendor (Codex CLI), anchored-observations rubric, brief at
[`2026-07-15-harness-build-brief.md`](2026-07-15-harness-build-brief.md).
**Deviation noted:** both legs ran in parallel rather than self-check-first;
each reviewed the same committed snapshot independently, so neither leg saw the
other's findings — the delta below is still an independent-legs comparison.

**Protocol incident worth recording:** Codex initially refused the dispatched
prompt — the rubric's "do not execute" read as forbidding even read-only
inspection — and asked for explicit permission rather than improvising. Re-run
with a read-only permissions clarification; full review delivered. (Upstream
rubric wording improvement candidate for meta-layer-starter.)

## Findings and dispositions

| # | Leg | Severity | Finding | Disposition |
|---|-----|----------|---------|-------------|
| C1 | Codex | High | `JudgePayload` carried `case_id` — a third artifact beyond the D-015 ratified two; the structural test locked the leak in | **Fixed** — field removed, structural test now asserts exactly `{defect_annotation, claim_text}` |
| C2 | Codex | High | Anonymizer missed spaced model forms ("gpt 5", "gemini 2.5 pro", "claude 3.5 sonnet" left tails) | **Fixed** — version-tail + redaction-run collapse passes; tested on Codex's own counterexamples |
| S1 | Self | High | Bare codenames (Sonnet/Opus/Haiku/Fable) unredacted entirely — live model names pass the lint | **Fixed** — standalone tokens added (over-redaction accepted as the safe direction); tested |
| S4 | Self | High (metric-affecting) | Band 2 loop short-circuited to Band 3 on first judge disagreement, missing a later agreed catch → undercounts the headline A2-vs-B metric | **Fixed** — all semantic claims judged; priority agreed-catch > escalation > no-catch; regression test |
| C3 | Codex | Medium | Band-3 card showed `claim.file` unanonymized and differed from the judge artifact | **Fixed** — shared `format_claim()`; cards render the byte-identical anonymized string judges receive |
| C4+S6 | Both | Medium | `extract_claims` could raise bare `TypeError`/crash later (`"claims": null`, non-string `file`), violating record-not-raise | **Fixed** — full shape validation, all paths raise `ClaimFormatError`; tests |
| C5 | Codex | Medium | `PanelRouter` allowed >2 non-authoring families (violates "exactly the two") | **Fixed** — `!= 2` enforced; 4-family rejection test |
| S8 | Self | Medium | JSON fence regex case-sensitive + duplicated across runner/judges | **Fixed** — shared `JSON_BLOCK_RE`, case-insensitive; test |
| S9 | Self | Medium | `select_first_n` dropped candidates silently, contradicting the no-silent-drops contract | **Fixed** — threads `FilterReport`; test |
| S10 | Self | Medium | `judges.py` — the module physically implementing the D-015 binding condition — had zero test coverage | **Fixed** — 7-test suite via injected executor (verdict parse, all error paths, payload-content check) |
| C6+S12 | Both | Low | Scheduler property test tolerated same-arm pairs; D-012 says never a block | **Fixed** — tightened to no-pairs; green |
| S11 | Self | Low | Scheduler docstring implied a reachable 2-in-a-row case that can't occur under the current call contract | **Fixed** — docstring honest about strict alternation |
| S3 | Self | Anchored, deferred | `_BULLET_RE` covers Claude Code transcript furniture only; no Codex/Gemini patterns | **Deferred to pilot with rationale** — claims reach judges as JSON-extracted fields (raw transcripts never enter payloads by construction); real Codex/Gemini furniture must be sampled from pilot sessions and added with tests, not guessed. Documented in code. |

No-anchor observations (both legs): declined per protocol (card CSS theming;
scheduler generality) — none carried a rule citation.

## External claims — verified this session

| Claim | Method | Result |
|---|---|---|
| `claude -p`, `--output-format`, `--version`, `--disallowedTools` exist | `claude --help` | ✅ confirmed |
| `codex exec [PROMPT]`, `--skip-git-repo-check` exist | `codex exec --help` | ✅ confirmed |
| Empty scratch dir isolates judges | Live probe: bare `claude -p` asked to read an absolute repo path from an empty dir | ❌ **refuted** — it read the file. Empty dir is convenience, not isolation. |
| `--disallowedTools` blocks the leak | Same probe, hardened invocation | ✅ confirmed — read blocked; judge config now pins the disallow list. ~~Residual: MCP connectors not covered~~ **Closed per D-017 (2026-07-16):** `mcp__*` added to the Anthropic judge's disallow list under the all-tools-disabled ruling (wildcard coverage re-probed at pilot). Codex has no supported tools-disable flag (probed — OQ-7); the Gemini binary is account-ineligible entirely (OQ-6). Full three-family closure pends those two rulings. |
| `antigravity` CLI flags | — | ⛔ not installed (OQ-5); unverifiable locally |

## Residual delta (the load-bearing signal)

Self-check (fresh-context, same vendor): 12 anchored observations.
Peer vendor (Codex): 6 anchored observations. Overlap: 4 findings
(anonymizer gaps, extraction robustness, scheduler test, with differing
specifics). **Unique to peer:** the `case_id` payload leak (C1) — the single
most direct D-015 violation — and the exactly-two panel gap (C5).
**Unique to self-check:** the Band-2 short-circuit metric bug (S4), the
zero-coverage judges module (S10), silent selection drops (S9), and the
refuted isolation claim. Read: the fresh-eyes self-check was broader; the
cross-vendor leg still caught the binding-condition violation the author
(and the author's own fresh session) walked past — consistent with the very
premise this benchmark exists to measure.

## Gate status after this review

- 67 unit tests green; 4/4 canaries pass (mock judges).
- **Build acceptance still not claimable:** real-backend canary re-run blocked
  on OQ-5 (Google judge authorization) and OQ-4 (canary-4 real-mode
  criterion); OQ-3 (prompt) awaits ratification.

*Update 2026-07-18:* all blockers ruled (OQ-3 ratified; OQ-4 criterion set;
OQ-6/OQ-7 resolved by D-019/D-020). Real-backend run: **4/4 PASS**, canary 4
agreed `no_catch` within the OQ-4 pass set. 79 tests green. Step 2a acceptance
pends supervisor review of that run.
