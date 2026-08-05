---
name: own-harvest-pipeline
description: Own-harvest pipeline DESIGN (D-065.3 split ruling — design+build authorized as idle-window paper/container work, zero sessions). Python-restricted per OQ-9c. Built-and-idle until the pre-registered trigger fires; NO harvested task enters the pool before supervisor ratification of this design AND the first constructed batch's D-028 screen results.
status: DRAFT for ratification (built-and-idle; activation gated on the D-065.3 trigger)
author: worker, under D-065.3 authorization
last-updated: 2026-08-05
---

# Own-harvest pipeline — design for ratification

**Authority and gates.** D-065.3 authorized *design and build* only: paper +
container work in idle windows, **zero sessions**. Two gates stand between
this document and a harvested task in the accrual pool: **(1) supervisor
ratification** of this design and of the first constructed batch's screen
results; **(2) the pre-registered activation trigger** (D-065.3, verbatim in
the ledger): at 60 cumulative screened rows across admitted feeds, recompute
expected total defect supply with the tightened yield CI; activate only if
the point estimate falls below n_max + 10 % (48.4); else re-evaluate every
30 rows. Per D-067.3, that recompute presents supply and discordance
consequences together.

## 1. Sourcing (candidate discovery — counts before identities)

- **Scope: Python only** (OQ-9c restriction; the validated toolchain and the
  strongest measured usable rate — cumulative 16/22 ≈ 73 %).
- **Query shape:** GitHub search for repos with a merged PR after the
  **D-023a recency gate (`created_at > 2026-03-01`)** that (a) closes a
  linked issue, (b) modifies at least one test file AND at least one
  non-test source file, (c) lands on the default branch.
- **Contamination controls (design §6, applied at sourcing):**
  - *Recency gate* — the PR **merge date** is the task date; the same gate
    that governs the external feeds. Non-negotiable (§6.1).
  - *Low-prominence preference* — star band **50–5,000**; very-high-star
    repos excluded (§6.2).
  - *Similarity screen* — task text embedded and excluded at **cosine >
    0.85** against SWE-bench-family items (§6.3).
  - *Distinctness* — repos already contributing rows to MultiLang or
    SWE-rebench are excluded (no double-provenance).
- **Blindness (OQ-10/D-056 discipline):** sourcing runs **counts-first**;
  candidate identities are pulled only under this document's fixed
  construction rules, and harvested rows enter the **existing global D-056
  ordering keyed on PR merge date** (UTC-normalized, ties
  `instance_id`→source=`own-harvest`) — no hand-picking by content, ever.

## 2. Record construction (label generation)

For each candidate PR, emit a **SWE-rebench-shaped record** (so every
existing tool — screen, evaluator, review flow — works unchanged):

- `base_commit` = first parent of the merge commit;
- `patch` = the PR's non-test diff (the gold fix); `test_patch` = the PR's
  test-file diff;
- `problem_statement` = the linked issue body, **scrubbed at construction
  per prereg §4.4** (fix pointers stripped and logged — including the PR
  itself, which is the one reference guaranteed to exist);
- container: repo-pinned image built from `python:3.12-slim` +
  repo-declared install (pyproject/requirements), recorded as
  `install_config.install`; `test_cmd` = `pytest -rA` scoped per repo
  layout; `log_parser` = `parse_log_pytest`;
- `FAIL_TO_PASS` / `PASS_TO_PASS` **derived, not asserted**: run the suite
  at base+test_patch (failing set = F2P candidates) and at
  base+patch+test_patch (must all pass; survivors of both runs = P2P).
  A candidate whose derived F2P is empty, or whose fix run does not clear
  the F2P set, is **discarded and counted** (label-integrity taxonomy,
  D-049 categories).

## 3. Verification — the D-028 screen as the OUTPUT gate

Every constructed record must **PASS the same committed D-028 screen the
external feeds face** (`screen-runner` flow: F2P all-fail at base under
test_patch-only, P2P non-empty all-pass, exec on this rig with the
ENV-PATH/crash/caps taxonomy). D-038 oracle-authoritative discipline applies
downstream unchanged. Screen verdicts, discard counts, and per-candidate
provenance (query, PR URL, merge date, star count, similarity score) are
committed per batch. **The screen is the gate — a record we constructed gets
no benefit of the doubt an external record wouldn't get.**

## 4. Cost, cadence, and what this never does

Container + API-search work only, in idle windows; **no sessions, no
authoring, no reviews**. The pipeline never runs an agent on a harvested
task before (a) ratification and (b) trigger activation; until then its
output is a committed, screened, **quarantined** candidate set
(`results/step3/own-harvest/candidates/`, excluded from the ordering until
activation is ruled).

## 5. Open items for the ratification pass

1. Star band (50–5,000 proposed) and whether forks/monorepos are excluded.
2. Embedding model for the similarity screen (proposal: a local
   sentence-transformer, versioned in the record) — no third-party API.
3. Whether harvested rows, once activated, back-fill the ordering by merge
   date (proposed; keeps D-056 semantics) or append after the frozen 215.
4. Batch size for the first constructed batch (proposal: 15 candidates).
