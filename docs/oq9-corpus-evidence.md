---
name: oq9-corpus-evidence
description: OQ-9 corpus-source evidence table — live-verified 2026-07-18 against the recency gate, harvest effort, and UTBoost test-quality concerns. Supervisor selects; selection logs as a D-entry before P0.
status: active
author: Maxim St-Hilaire (methodology owner) — verification by worker, 2026-07-18
---

# OQ-9 corpus evidence table (live-verified 2026-07-18)

Verification method: vendor cutoffs fetched from primary vendor docs; feed
freshness measured **directly against the HuggingFace parquet files via DuckDB
queries on `created_at`** — not estimated from README prose. No task content
harvested; metadata queries only.

## The recency gate

D-010 rule: tasks postdate **every** evaluated model's training cutoff.

| Model (role) | Vendor-stated cutoff | Source |
|---|---|---|
| Claude Opus 4.8 / Sonnet 5 / Fable 5 (author/reviewer) | "Jan 2026" (month granularity) | platform.claude.com model overview |
| **GPT-5.6 Sol** — current Codex CLI default (author/reviewer) | **"Feb 16, 2026"** | developers.openai.com/api/docs/models/gpt-5.6-sol |
| gemini-3.5-flash (judge only; never sees tasks/patches per D-015) | "January 2025" | ai.google.dev model card + changelog (alias confirmed 2026-05-19) |

Hard gate = **> 2026-02-16** (max across models). **Recommended operative
gate: > 2026-03-01** — a two-week buffer absorbing Anthropic's
month-granularity and the vendors' "training data is broader than knowledge
cutoff" hedge. Judge cutoff is an outlier but irrelevant to task
contamination (judges receive only anonymized claim + annotation).

## Candidates

| | (b1) SWE-bench-Live / MultiLang | (b2) SWE-rebench-leaderboard | (b3) SWE-bench-Live / Python core | (a/c) Own harvest (fallback) |
|---|---|---|---|---|
| **Live status** | Active — README news 2026-05-16; HF touched 2026-06-28 | Active — HF modified 2026-06-01 | **Stale** — untouched since 2025-09-18 despite "monthly" README claim | n/a — we build it |
| **Tasks past 2026-03-01** | **322 of 743, measured** (max created_at 2026-04-22) | **~110+, approximate** — `2026_03` split holds issues dated to 2026-05-11; exact count rate-limited, needs one re-query before P0 | **0** (max created_at 2025-09-02) — fails gate outright | Unbounded, but every task self-collected |
| **Languages** | C, C++, C#, Go, Java, JS, Rust, TS — **no Python** | Python only | Python | Python (per OQ-9c) |
| **Harness** | Docker per-instance images via RepoLaunch (arXiv:2603.05026) | SWE-bench-fork compatible; 7.5k+ prebuilt Docker images (base pipeline) | swebench-compatible | SWE-bench methodology, self-built |
| **Test-quality vs UTBoost concern** | Invalid instances filtered by running regression tests ×3; **no UTBoost-style augmentation** | LLM-based test-patch-validity scoring + contamination marking vs model release dates; **no UTBoost-style augmentation**; self-admits "not every problem guaranteed solvable" | UTBoost audited the *static* SWE-bench, found mislabeled passes | Whatever we build — highest control, highest effort |
| **License** | MIT | CC-BY-4.0 | MIT | n/a |
| **Harvest tooling effort** | Low — download + filter by created_at | Low — download + filter; one exact-count query outstanding | n/a | **High** — weeks of collection/validation tooling; delays pilot |
| **External provenance (OQ-9 pre-commitment)** | ✅ third-party (Microsoft), dates independently measurable | ✅ third-party (Nebius), dates independently measurable | ✅ but fails gate | ❌ researcher degree of freedom returns |

Also checked and disqualified as "continuously-refreshed feeds": SWE-Factory
(a benchmark-construction *tool*, one static dataset) and R2E-Gym (static
procedural gym). SWE-rebench-V2 (multilingual, 32k tasks) disqualified for
recency: 0 of 360 stratified-sampled rows postdate 2026-03-01 — it is a
training corpus, not a recency-curated eval feed.

## UTBoost note (applies to every candidate)

No candidate ships UTBoost-hardened test suites. The design's own mitigation
(§6.4) therefore carries the load for all options: "passed bundled tests" =
not-confirmed-defective, never certified-correct; residual risk disclosed.
Whether feed-native filtering (regression-test ×3, or LLM validity scores)
plus §6.4 satisfies the OQ-9 pre-commitment's "UTBoost hardening" clause is a
supervisor call, flagged honestly rather than assumed.

## Worker recommendation (supervisor decides)

**Primary: (b1) SWE-bench-Live/MultiLang.** Largest *measured* post-gate
count (322), freshest maintenance, MIT, external provenance, low tooling
effort. Cost: no Python — the pilot's P0 must validate the RepoLaunch Docker
flow on a non-Python task; JS/TS tasks (39 post-gate) are closest to the
methodology's home stack. **Secondary: (b2) SWE-rebench-leaderboard** if
Python-first simplicity outranks measured count — condition: exact post-gate
count re-queried before P0 (one metadata query). Fallback (c) stands as
pre-registered. Both externals beat own-harvest under the OQ-9 pre-committed
preference order, subject to the UTBoost-clause call above.
