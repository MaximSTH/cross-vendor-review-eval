---
name: pilot-report
description: Step 2b pilot report (protocol §6) — measured throughput/variance, defect yield, corpus supply, F-001, catch-audit, quota verdict, models observed, limitations, final-n per §7, and a three-branch go/no-go for Step 3. Drafted 2026-07-23; supervisor rules on their schedule.
status: draft
author: Maxim St-Hilaire (methodology owner) — drafted by worker
---

# Pilot report — Step 2b (P0 + P1)

**Status: draft for supervisor review. No Step-3 decision executes until the
supervisor rules, on their schedule.** All numbers trace to committed
artifacts: `results/pilot/sessions.jsonl` (provenance), `scoring.jsonl`,
`p1-checkpoint.md`, `raw/` (transcripts + eval), and the decision log
(D-001–D-053).

## 1. What the pilot answered (protocol §1)

| Question | Answer |
|---|---|
| Does one recency-gated task flow end-to-end? | **Yes** — proven at P0 and ×5 at P1 (author → hidden test → A1/A2/B → three-band scoring → Band 3 card). |
| Sustainable sessions/week under real limits? | **Declaration-bound at 15** (D-026); measured pilot rate exceeds it, so the ceiling binds — see §2. |
| Free-tier Gemini quota feasible at Band 2 volume? | **Unmeasured — Band 2 volume was zero** (all cases decided at Band 1). See §7. |
| Band 3 card rulable from the card alone? | **Yes** — batch p1-b1 (2 catch-audit cards) ruled by the supervisor from the cards; no interface defect raised. |
| Corpus source ratified + final n? | Corpus **stands (D-023) pending a Step-3 Hanoi re-ratification** given the supply finding (§4); final n in §8. |

## 2. Throughput & variance (protocol §3, D-021/D-026)

**Sessions run:** 24 logged review/authoring sessions (P1) — anthropic 13,
openai 11 — plus **1 discarded** (worker error, launched a review arm with write
capability; caught, verified no tree mutation, re-run; D-041) and P0's sessions.
All consumed sessions count against the ceiling (D-031g).

**Session wall-clock:** 87 min total across the 24; mean **216 s**, range
**38–551 s** (authoring 184–551 s; reviews 38–332 s; the fastest were empty-claim
reviews, the slowest cross-vendor reviews on large repos).

**Sustainable sessions/week (D-021b rule):**
`min(observed × 7 × 0.7, owner-declared ceiling)`. The pilot's days were
heavily interrupted (supervisor-availability-gated), not dedicated; even so,
any reasonable reading of the observed session rate, ×7×0.7, **exceeds the
declared ceiling of 15**, so **the ceiling binds**.

> **Binding statement (D-026, stated where n is computed):** final-n is
> **declaration-driven** — the sustainable rate used for sizing is the owner's
> **declared 15 sessions/week**, which is **less than** the measured
> pilot-days rate. 15 is a *declaration*, not a measured throughput; it is used
> because D-021b takes the `min()` precisely so that atypically-dedicated (or
> here, atypically-interrupted-but-still-fast) pilot days do not inflate the
> plan.

**Run-to-run variance (k=2 repeats, D-021a):** the two pre-registered repeat
positions (3 and 4, seed 1607515562) **both resolved to authoring successes**,
so **catch-rate run-to-run variance was not measured** (no defect to catch).
The repeats measured **verbosity (claim-count) variance**:

| pos | arm | run 1 | run 2 |
|---|---|---|---|
| 3 | A2 (fresh same-vendor) | 0 claims | 2 claims |
| 3 | B (cross-vendor) | 1 | 1 |
| 4 | A2 | 1 | 1 |
| 4 | B | 1 | 0 |

Cross- vs same-vendor did **not** predict stability (pos3 cross stable, same
swung; pos4 same stable, cross swung). A1 run-2 is **`n/a` (structural)** —
the in-session arm cannot be cleanly repeated on an append-only CLI session
(D-042). **Limitation, not omission** (§9); §8 carries the fix.

## 3. Defect yield (protocol §3; §7 sizing input)

| pos | task | authoring vendor | oracle |
|---|---|---|---|
| 1 | haraka__Haraka-3535 | anthropic | authoring success |
| 2 | NVIDIA__NemoClaw-330 | openai | **CONFIRMED DEFECTIVE** |
| 3 | thlorenz__doctoc-329 | anthropic | authoring success |
| 4 | openai__codex-plugin-cc-83 | openai | authoring success |
| 5 | aralroca__next-translate-1259 | anthropic | **CONFIRMED DEFECTIVE** |

**Defect yield = 2/5 (0.40).** Authoring runs per harvested defect ≈ **2.5**.
Bundled-pass tasks are **authoring successes** (neither the defective nor the
false-alarm sample, D-031a) — throughput data only, artifacts retained for
possible later admission under an augmented suite. Yield feeds §8 directly:
each harvested defect costs ≈ 2.5 authoring + 3 review = **5.5 sessions**.

## 4. Corpus supply — a headline finding (promoted from Step-3 input)

Filling 5 positions (+ replacements) required **walking 17 post-gate JS/TS rows;
5 were usable (PASS) → ~29% usable rate** — far below what the OQ-9 evidence
table implied when it credited SWE-bench-Live/MultiLang with regression-test
filtering.

**Corpus-integrity failure taxonomy — five distinct modes, four
feed-attributable:**

| # | mode | attribution | instances |
|---|---|---|---|
| 1 | Label integrity — whole-suite-as-F2P | feed | youtube-3708 |
| 2 | Label integrity — phantom F2P names | feed | Gladys-2504 |
| 3 | Label integrity — F2P passes at base | feed | vueuse, gsd-2-2643, AionUi |
| 4 | Missing image (registry 404) | feed | anything-llm, mongoose, proj4js |
| 5 | Eval-harness failure (shipped test cmd runs no tests) | feed | bruno-7620, gsd-2-3258 |
| — | platform_infeasible — hard (crash) / time (process-per-test) | **rig** | oh-my-pi (bun); gsd-2-2738 |

Modes 1–5 are **feed defects** that would silently corrupt any SWE-bench-derived
evaluation trusting these labels without executing them; the rig-relative
exclusions are **not** feed defects and are rerunnable on native amd64 (the §7
replication host). The **ground-truth validity screen (D-028)** — adopted into
intake during the pilot — is what caught modes 1–3 pre-session; the
oracle-authoritative evaluator (D-038) and the ERROR-vs-FAIL discipline caught
the rest without a single false "defective" verdict reaching the record.

## 5. Central finding — F-001 "diff-anchoring"

> **When the authored fix lands in a different location than the true defect,
> reviewers critique the change in front of them and miss the real bug
> elsewhere.**

A claim about **reviewer behavior**, and the practitioner takeaway. Three
instances to date:

1. **P0 (doctoc-328):** patch machine-confirmed defective; **all three arms
   returned zero claims** — unanimous miss.
2. **P1 pos2 (NemoClaw):** author fixed 1 of 4 credential locations; both
   mechanical "catches" were on the authored block and were **overturned by the
   Band 3 audit** (P-002 coincidental localization; P-003 inverted claim).
3. **P1 pos5 (next-translate):** author fixed `appWithI18n.tsx`; the real defect
   is in `DynamicNamespaces.tsx`/`I18nProvider.tsx` → **unanimous no_catch.**

**n-caveat (binding):** n is tiny (2 P1 defective cases + P0). Diff-anchoring is
reported as the **observed central pattern with n stated** and as the **sharpest
hypothesis for the main study to size** — **not** as an established rate. §8's
sizing is built to estimate the per-arm diff-anchoring miss-rate.

## 6. Catch-audit — the mechanical metric's validity check (D-039)

Band 1 (mechanical, ±5, sweep-stable) on the two defective cases, with the Band 3
human catch-audit applied:

| pos | A1 | A2 | B | audited catches |
|---|---|---|---|---|
| 2 | no_catch | catch → **no_catch** (P-002) | catch → **no_catch** (P-003) | **0/2** |
| 5 | no_catch | no_catch | no_catch | (no catches) |

**Catch-audit human–Band1 agreement: 0/2.** Both mechanical catches in the
pilot were **diff-anchoring artifacts**, not detections — precisely the failure
the audit (D-039) was pre-registered to measure. The primary mechanical metric
(D-005) is **untouched**; the audit is a validity layer, reported alongside it.
**Precedent taxonomy** (append-only): **P-002 coincidental localization**
(semantically-unrelated claim on a coincidentally-correct line); **P-003
inverted claim** (right location, but asserts the correct fix is the bug —
counter-productive to follow).

## 7. Quota feasibility verdict (D-019)

**Verdict: UNMEASURED — Band 2 never executed.** All P1 cases (and P0) were
decided at **Band 1**: every reviewer claim was either fully-localized (→
mechanical catch/no_catch) or the case had no claims. **No partially-localized
claim ever routed to Band 2**, so the free-tier Gemini judge stack did not run,
and free-tier daily-quota feasibility against Band 2 volume **could not be
measured**. Consequence: the D-019 quota question is **carried unresolved into
Step 3**; the semantic-catch layer (OQ-21), if adopted, is what would generate
judge volume and must be quota-checked before adoption. No judge-model
discontinuity check (D-019 alias ruling) was triggered.

## 8. Final-n computation (§7 pre-registered rule, cut order applied)

**Inputs:** ceiling **15 sessions/week** (D-026); **5.5 sessions per harvested
defect** (§3); design target ≈ **900 sessions** (~600 review + ~300 authoring,
both directions).

**Design target at the ceiling:** 900 / 15 = **60 weeks (~14 months)** —
infeasible as a bounded study on subscription-only throughput.

**§7 cut order applied** (correct-sample → repeats → per-direction n; **headline
A2-vs-B on defective cases protected first**):

1. **Correct sample (false alarms) — CUT.** It has **no construction path**
   under the ratified corpus anyway (D-031b: §6.4 needs augmented tests; no
   candidate feed ships them). Cut is forced, not chosen.
2. **Repeats — reduced to defective-only** (D-052 §7 note) or cut for sizing.
3. **Per-direction n — set to the schedule.**

**Largest n a bounded window supports (A2/B protected, no correct-sample, no
repeats):**

| window | sessions | confirmed-defective cases |
|---|---|---|
| 12 wk | 180 | ~33 |
| 16 wk | 240 | ~44 |
| 20 wk | 300 | ~55 |
| 26 wk | 390 | ~71 |

**Power note (Wilson):** ~30–40 defective cases → ±~15 pp 95% CI per arm,
detecting a **>~20 pp** A2-vs-B (or A1-vs-B) condition delta; ~50+ tightens to
~12 pp. Diff-anchoring in the pilot produced a **0/2** audited-catch rate — if
that magnitude holds, a >20 pp delta is well within reach at n≈40. **These
counts assume the ~29% corpus usable rate holds** — harvesting n defective
cases means screening ≈ `n / (0.29 × 0.40)` ≈ **8.6 rows per defect** including
the usable-rate and defect-yield losses; the corpus decision (§9) gates whether
that harvest cost is acceptable.

## 9. Limitations (stated plainly)

- **Repeat placement:** both k=2 repeats landed on non-defective tasks →
  **catch-rate run-to-run variance unmeasured** (D-052). Fix pre-registered for
  Step 3: repeat on confirmed-defective cases.
- **A1 non-repeatability:** the in-session self-review arm cannot be cleanly
  repeated (append-only session); recorded as a structural property of the A1
  condition, not a gap (D-042). A1 also **holds strictly more information** than
  A2/B by construction (§4 design), making cross-condition comparisons
  **conservative** against the cross-review hypothesis (D-031e).
- **Rig-relative exclusions:** bun (hard) and process-per-test-isolation (time)
  tasks are unrunnable under amd64 emulation on the pilot host — **not** feed
  defects; rerunnable on native amd64 (the §7 replication). VM was resized
  2→8 GiB mid-pilot to make evaluation reliable (D-045); the memory *flag* alone
  was cosmetic — the safeguard is the `parsed==0`→ERROR + completeness check.
- **OpenAI model-ID basis:** `codex exec --json` emits no model ID; the arm's
  model (**gpt-5.6-sol @ xhigh reasoning**) is **config-introspected**, not
  stream-reported (D-012 gap, closed via `~/.codex/config.toml` snapshot; §10).
- **n is tiny:** every finding is reported with n; none is an established rate.
- **Corpus language mix:** JS/TS only (P1); the paired design neutralizes it in
  the headline comparison but it is a recorded covariate. Two P1 cases share a
  repo with earlier tasks (pos3↔P0; pos4 is an OpenAI-owned repo with OpenAI
  arms) — reported covariates, selected by the fixed rule, never hand-excluded.

## 10. Models observed (D-012) — see `models-observed.md`

The **Anthropic reviewer is an opus-4.8[1m] + haiku-4.5 stack** as operated
(Claude Code delegates subtasks) — vendor-stack, not single model. The
**OpenAI reviewer is GPT-5.6 Sol @ xhigh reasoning effort**, config-confirmed.
No within-P1 model drift observed. Full per-position/per-arm table in the
artifact.

---

## 11. Go/no-go recommendation for Step 3 — three branches, decision inputs neutral

The pipeline is **proven and hardened**; the pilot surfaced **two publishable
findings** (F-001 diff-anchoring; the corpus-integrity taxonomy) and a **hard
throughput/supply constraint**. Three coherent branches:

### Branch A — Full study (design target)
- **What:** ~50 defective/direction × 2 × 3 conditions + correct sample; ≈900
  sessions.
- **Cost:** ~60 weeks at 15/week — **or** move to the §7 **version-pinned API
  replication ($1.5k–4k)** to buy throughput and remove drift.
- **Decision inputs:** Is a >1-year subscription-only timeline acceptable? Is
  API budget available (which *also* fixes the D-012 OpenAI-ID gap and pins
  versions)? Is the correct-sample/false-alarm arm wanted enough to build test
  augmentation (D-031b)?

### Branch B — Lean study (protect the headline)
- **What:** A2-vs-B (and A1-vs-B) catch-rate on **~40 confirmed-defective
  cases**, ~16 weeks at 15/week; no correct-sample (forced cut), repeats on
  defective cases only; diff-anchoring miss-rate as the primary estimand.
- **Cost:** feasible on subscriptions in a semester; **contingent on the corpus
  decision** (§9) — at ~29% usable × 40% yield, ~40 defects needs screening
  ~340 rows, which the current feed cannot supply post-gate (39 JS/TS rows).
  **This branch requires corpus re-ratification** (D-023 fallback / own-harvest
  / multi-language) to enlarge supply.
- **Decision inputs:** Is a >20 pp effect the target (n≈40 suffices)? Which
  corpus expansion (SWE-rebench fallback, own-harvest Python, full MultiLang)?

### Branch C — Pilot as terminal deliverable
- **What:** publish the **practitioner write-up** (F-001 + corpus taxonomy +
  catch-audit validity result) as a standalone piece; the repo stays open (MIT,
  already public); no further sessions.
- **Cost:** near-zero additional; the findings stand on the pilot's n with the
  caveats already written.
- **Decision inputs:** Is the diff-anchoring pattern + the corpus-integrity
  finding a sufficient contribution on their own? Is the marginal value of a
  powered catch-rate number worth Branch A/B cost given that the *direction* is
  already visible (0/2 audited catches)?

**Worker framing (neutral):** the pilot's **most transferable outputs are
branch-independent** — they publish in C, and they are the backbone of A/B. The
binding constraints are **throughput (15/week)** and **corpus supply (~29%)**;
both point the same way — subscription-only + current-feed cannot reach the
design target, so A effectively requires **API budget**, B requires **corpus
expansion**, and C requires **neither**. The worker takes **no position on which
branch**; the decision is the supervisor's, on their schedule.

---

## Appendix — Step-3 pre-registration queue

Carried items, each to be pre-registered **before** any Step-3 execution:

1. **Semantic-catch layer (OQ-21):** extend Band 2 judges to mechanically-caught
   claims → `semantic_catch` secondary verdict, calibrated by the human
   catch-audit. **Blocking check:** judge-call volume vs D-019 free-tier quota.
2. **Model-tier arm (OQ-23):** same-vendor premium-tier (Fable-class) review as
   a routing axis distinct from cross-vendor (separates tier from vendor
   diversity). Adds an arm + a judge-rotation cell.
3. **False-alarm construction (D-031b):** the correct-patch sample has no
   construction path under the ratified corpus; options — test augmentation for
   a small correct sample / descope false-alarm to secondary (catch-rate sole
   headline) / corpus re-ratification.
4. **Scanner freeze:** apply the **four D-018 quotation channels** (commit-subject
   D-036, test-file mock D-050, package.json scripts D-050, source-code
   runner-name regex D-053) as exec-context patterns; freeze at Step-3 start.
5. **Repeat-on-defective rule (D-052 §7):** place k=2 repeats on
   confirmed-defective cases so catch-rate variance is measurable.
6. **Problem-statement scrubbing (D-035b):** strip fix-pointing references
   (related-PR links, commit URLs) from problem statements as a uniform,
   documented input transformation, from Step 3.
7. **Config-introspection provenance (D-053):** snapshot codex `model` +
   `model_reasoning_effort` per session (not the full config); the standing fix
   for the D-012 OpenAI-ID gap.
8. **Corpus re-ratification (D-028c):** the Hanoi decision — enlarge/replace the
   feed given the ~29% usable rate — with this report open.
