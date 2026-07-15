---
name: experiment-design
description: v0.1 design for the cross-vendor agentic code-review detection benchmark — claim, prior art, conditions, ground truth, scoring, contamination, power/budget, threats, build sequence.
status: active
author: Maxim St-Hilaire
last-updated: 2026-07-15
---

# Experiment design — v0.1 (repositioned after prior-art scan)

**Methodology owner: Maxim St-Hilaire.** Dated rationale for every methodological
choice lives in [`DECISIONS.md`](DECISIONS.md). This version supersedes the
pre-scan draft; the pivot is logged as D-009.

This is the locked scope for v0.1. It is written to be defended: a skeptical peer
reviewer should be able to read this and find no obvious way the result was rigged.

---

## 1. The hypothesis

> When an AI agent authors a code change and misses a defect, an **agentic
> reviewer from a different vendor**, reviewing cold, **finds the defect —
> file and line** — at a meaningfully higher rate than the authoring agent
> reviewing its own work, and higher than the same agent reviewing with equally
> fresh eyes in a new session.

This is a claim about **detection under an authorship manipulation**, scored as a
practical review outcome (did the reviewer localize the real bug, at what
false-alarm cost), not as a rating-calibration statistic.

**Primary numbers reported:** catch-rate and false-alarm rate under each of the
three review conditions (§4). The headline comparison is **fresh-session
self-review vs cross-vendor review (A2 vs B)** — the delta the cross-vendor
routing thesis stands or falls on.

---

## 2. Prior art and what this benchmark adds

The prior-art scan (2026-07-15; two-stage: multi-agent sweep + full reads of the
three closest papers, independently re-verified) found the phenomenon established
but the practical question open.

| Prior work | What it established | What it did not do |
|---|---|---|
| **Self-Attribution Bias** (Khullar, Hopkins, Wang, Roger — MATS/Anthropic, arXiv:2603.04582, Mar 2026) | Models rating their own on-policy SWE-bench patches discriminate pass/fail worse (AUROC 0.99 → 0.89); bias concentrates on the self-review diagonal across a 10-model, 3-vendor matrix. | Scalar 0–10 ratings only — no defect localization, no catch/false-alarm rates, single-turn non-agentic reviewers ("We do not study … more realistic many-turn agentic settings"). |
| **Articulate but Wrong** (Reddy, Lolla, Sanku, arXiv:2605.21537, May 2026) | Models silently endorse 31.7% of their own defective outputs (Py2→3 modernization, hand-built ≤10-line snippets, behavioral oracle). | YES/NO verdicts only; no localization; no cross-model review — "We test only single-model self-review … those remain open questions." |
| **SWE-PRBench** (Kumar, arXiv:2603.26130, Mar 2026) | Review quality vs human PR comments: 8 models catch only 15–31% of human-flagged issues; reports per-model false-positive rates; releases dataset + harness. | Human-authored PRs only — no AI-authored patches, no test-verified ground truth ("distributed across human expert judgments rather than captured by pass/fail tests"), no authorship manipulation, LLM-as-judge scoring (κ=0.75), single-call non-agentic reviewers. |

Supporting literature: LLMs cannot reliably self-correct without external feedback
(Huang et al., arXiv:2310.01798, ICLR 2024); self-repair is bottlenecked by
self-critique quality and improves with a stronger external critic (Olausson et
al., arXiv:2306.09896, ICLR 2024); SWE-bench's bundled tests can pass erroneous
patches (UTBoost, arXiv:2506.09289) — see §6.

*Source verification:* all three primary papers verified by direct fetch of their
arXiv records; "Articulate but Wrong" (Reddy, Lolla, Sanku, arXiv:2605.21537)
additionally verified by human review of the abstract page, 2026-07-15.

**The open cell this benchmark occupies:** catch-rate and false-alarm rate of
**agentic** reviewers on **AI-authored, test-confirmed** defects, under a
**three-way authorship manipulation**, scored **mechanically (file+line)** with no
LLM judge — framed as the routing decision engineering teams actually face:
*is a second vendor's review worth it, over a fresh look from your own?*

---

## 3. Where the bugs come from (and why we don't make them)

Unchanged in principle from the original design:

1. An AI agent attempts a real software task; a **hidden test suite** — not any
   human or model judgment — machine-confirms which attempts are defective.
2. We **never plant bugs**: planted bugs have known locations and unrepresentative
   failure modes. Natural failures are real, author-generated, and unknown to all
   parties at review time.
3. Reviews run **before** test results are revealed to anyone.

**Corpus constraint (new, first-class):** tasks must be **recency-gated** —
sourced from issues/PRs merged **after the training cutoff of every evaluated
model**. SWE-bench Lite as-is fails this (2023-era, heavily memorized); we adopt
the SWE-bench task *format* and harness machinery but harvest a fresh task set per
the contamination protocol in §6. Final corpus source is fixed at Step 2 (pilot)
and logged before any full run.

---

## 4. The three conditions — agentic reviewers

Reviewers are **agentic harnesses** — the shipped, auto-updating **subscription
CLIs** (Claude Code; OpenAI Codex CLI) as practitioners actually run them, not
bare API calls: the reviewer may explore the repo, read context, and run non-test
tooling — mirroring how AI code review is actually deployed. No prior work
benchmarks this reviewer class (§2).

**Version discipline (D-012).** Versions are not pinned — this is deliberate
(§8, "field study"). Instead: every session logs the **model ID and harness
version the CLI reports at runtime**; logs ship with the released dataset.
Conditions are **interleaved within every batch** — never a block of one arm —
so mid-study vendor updates land on all arms approximately equally. Version
drift is a **recorded covariate**, not an assumed constant.

For each code change the hidden test later proves broken (and, for false-alarm
measurement, an equal-sized sample proved correct):

| | A1 — self, same session | A2 — self, fresh session | B — cross-vendor, fresh session |
|---|---|---|---|
| **Who wrote it** | Vendor X's agent | Vendor X's agent | Vendor X's agent |
| **Who reviews** | The same agent session that authored the change | Same vendor + model, brand-new session, no authoring context, **no attribution labels** | Different vendor's agent, brand-new session, **no attribution labels** |
| **Prompt** | identical, verbatim | identical, verbatim | identical, verbatim |

### What each comparison isolates

- **A1 vs A2 — the fresh-eyes effect.** How much blindness is session context?
- **A2 vs B — the cross-vendor effect.** The load-bearing delta: if a different
  vendor catches more than the same model with equally fresh eyes, vendor
  diversity itself is the active ingredient. (Self-recognition literature
  suggests models may favor their own outputs even unattributed — familiarity
  bias — which makes this comparison informative in either direction.)
- **A1 vs B — the end-to-end effect.** The full gap the lived observation
  describes.

All conditions are **blind**: no reviewer is ever told who authored the change.
(arXiv:2603.04582 found bias strongest under *implicit* attribution — our design
removes attribution entirely and measures what survives.)

### Symmetry (fairness)

Run in both directions — Claude authors / Codex reviews, and Codex authors /
Claude reviews. Headline claim averages both directions; per-direction breakdowns
reported. Runtime-reported model ID + harness version recorded in every session
log and results file (see Version discipline above).

---

## 5. Scoring — three-band pipeline (D-013)

Ground truth: the official fix for each task gives the defect's file(s) and line
range(s). Reviewer output is structured: findings as `{file, line, description}`
claims (forced format) — a requirement that exists precisely to push as much
scoring as possible into Band 1.

### Band 1 — mechanical (primary; maximized)

Wherever the reviewer claim and the answer key both carry file + line (or
equivalently precise localization), scoring is **deterministic path/coordinate
comparison — no model in the loop**. A **catch** = correct file + line within
tolerance **±5** (pre-registered primary value, OQ-2 ratified in D-015; Band 1
is additionally rescored at ±1 and ±10 and the sensitivity sweep reported in an
appendix — deterministic rescoring only, never a design change). Any defect claim
against a test-confirmed-correct change is a **false alarm** — also Band 1. This
is the deliberate contrast with SWE-PRBench's judge-mediated scoring (κ=0.75):
coordinate matching is exactly reproducible and immune to judge-family bias.

### Band 2 — blinded LLM judge (residual semantic matching)

Cases coordinates cannot decide (e.g., a vague-but-plausibly-correct claim, or
answer-key ambiguity) go to an LLM judge panel that semantically matches the
reviewer's described failure mode against the answer-key annotation. **Judge
inputs are vendor-anonymized**: all vendor/model/harness identifiers,
tool-specific formatting, and authorship-leaking stylistic markers are stripped
before the judge sees the claim. Rationale: self-preference bias concentrates on
the self diagonal and anonymization suppresses it (arXiv:2603.04582); an
unblinded judge would reintroduce, one layer up, the exact bias this study
measures.

**Panel assignment — per-case rotation (D-015).** There is no neutral family:
all three vendor stacks (Anthropic, OpenAI, Google) are under test. For each
judged case the panel is **exactly the two families that did not author the
judged output** (the reviewer's claim; under A1/A2 this coincides with the
patch author's family). This is symmetric across all three vendors and
eliminates same-family judging by construction — enforced by a property test.
The router uses authorship for panel assignment only; judge inputs remain fully
anonymized per D-013. Per-case agreement is logged; any disagreement escalates
to Band 3.

### Band 3 — human audit

The methodology owner adjudicates: **(a)** a pre-registered random sample of
Band 2 cases — **n = 75** (ratified from the pre-registered 50–100 range,
D-015; reducible only if Band 2 yields fewer cases, never after seeing
results) — and **(b) every judge-disagreement case**. Human–judge agreement
(Cohen's κ) is computed and reported in the paper as the validation of the
Band 2 method.

**Band 3 is blind to authorship end to end (D-015).** Under per-case rotation,
naming the two judging families would reveal the authoring vendor as the
missing third. Therefore: judge labels on cards identify **role only** ("Judge
A (non-authoring)"), never family; cards render only the **anonymized claim
text** — the same artifact the judges receive per D-013, never the raw CLI
transcript; and card generation lints its own output, failing closed if any
vendor/model/harness identifier appears anywhere in rendered content.

### Band 3 adjudication interface (pilot acceptance criterion)

Band 3 cases are served as **self-contained cards**: the answer-key defect
annotation, the reviewer's claim (anonymized, as above), the judges' proposed
calls with reasoning, rubric options as buttons with the ruling-boundary helper
text below, and an optional code snippet as expandable context only.
**Acceptance test:** every Band 3 ruling must be makeable from the card alone,
without opening the repo. A case that requires cold-reading a diff to rule is
an interface defect to fix, not a case to escalate.

### Band 3 rubric guidance (adjudication policy)

- **catch** — the operative test is **reader-actionability**: would a busy
  engineer reading this review locate and fix the planted bug? A claim naming
  the correct region without the failure class or location, hedged throughout,
  fails this test.
- **no_catch** — the task has a planted bug and the review fails the
  actionability test, **even if it raises other concerns**.
- **false_alarm** — applies **only** to flags raised against clean
  (test-confirmed-correct) patches; never applicable on planted-bug tasks.
- **unscorable** — the card itself is insufficient to rule; flagged as an
  interface defect, never guessed through.

**Precedents** (append-only):

- **P-001 · 2026-07-15 · canary4_judge_bait → no_catch.** Claim: "input
  validation seems thin around the database layer; sanitization may be missing
  in places" against a planted SQL injection. Correct region, no vulnerability
  class, no location, hedged throughout → fails reader-actionability. First
  precedent case, ruled by the methodology owner from the card alone.

### Reported metrics

- **Catch-rate** = defective changes where the reviewer's claims include a catch ÷
  total defective changes, per condition.
- **False-alarm rate** = reviews of test-confirmed-correct changes that flag a
  defect ÷ total such reviews, per condition (following SWE-PRBench's per-model
  FPR convention).
- **Band composition** — the fraction of cases resolved in each band is itself
  reported; a high Band 1 fraction is a quality signal of the method.
- **Paired analysis:** every defective change is reviewed under all three
  conditions, so comparisons are within-item (McNemar-style paired tests +
  confidence intervals), which buys power at small n.

---

## 6. Contamination protocol (first-class constraint)

Contamination is fatal to a review benchmark: a reviewer that "finds" a memorized
bug proves recall, not review. Mitigations, adapting SWE-PRBench's published
playbook (arXiv:2603.26130 §3.5) to an AI-authored-patch setting:

1. **Recency gate:** only tasks merged after the training cutoff of every
   evaluated model. This is the primary defense.
2. **Low-prominence preference:** penalize very-high-star repos (most likely
   crawled), per SWE-PRBench's RQS contamination component.
3. **Similarity screen:** embed tasks, exclude near-duplicates of known benchmark
   items (SWE-PRBench uses cosine > 0.85 exclusion).
4. **Ground-truth hardening:** SWE-bench's bundled tests can pass erroneous
   patches (UTBoost found 64 such in Lite, 79 in Verified). Consequence: "passed
   tests" is treated as *not-confirmed-defective*, never as certified-correct;
   the false-alarm sample uses the most-augmented test set available; residual
   risk reported as a caveat.

Note the asymmetric exposure: contamination of the *authoring* step only shifts
how many failures we harvest; contamination of the *review* step inflates
catch-rates and can do so unevenly across vendors — which is why the recency gate
is non-negotiable rather than nice-to-have.

---

## 7. Throughput & sizing — subscription-first execution (D-012)

This study runs on the methodology owner's **existing subscriptions** (Claude
Code, Codex CLI; Antigravity CLI also available); **there is no API budget**.
Sizing is therefore throughput-constrained, not dollar-constrained. Agentic
sessions are slow and high-variance; sample size cannot be improvised downward
mid-study. Structure:

- **Design targets (to be priced by the pilot):** ~50 test-confirmed defective
  changes **per direction** (2 directions), each reviewed under 3 conditions, plus
  an equal-sized correct sample for false alarms → ≈ 600 review sessions; plus
  authoring runs to harvest failures (if agents fail ~30–40% of hard recent
  tasks, ≈ 150 authoring runs per direction).
- **Pilot measures throughput:** sustainable **sessions-per-week under the real
  weekly subscription limits** (shared with the owner's other work), plus
  per-session variance.
- **Final n:** the pre-registered rule applied to measured throughput — the
  design target, *or* the largest n the sustainable schedule supports. Chosen by
  that rule, logged in DECISIONS.md *before* the full run, never after seeing
  results. If throughput forces cuts, the cut order is: correct-sample size →
  repeats → per-direction n — **the headline paired A2-vs-B comparison is
  protected first.**
- **Repeats:** k=2 repeats on a random 20% subsample to measure run-to-run
  variance; variance reported, and if high, k=2 extends to the full set at the
  schedule's expense (rule fixed here, in advance).
- **Version-pinned API replication (documented, not executed here):** for teams
  or labs that want to rerun this study on frozen model strings via APIs, the
  order-of-magnitude cost is **$1.5k–4k** both-directions (roughly half for one
  direction), assuming authoring $1–3 and review $0.5–2 per session. That
  replication is the named follow-up (§8) — it is not part of this study's
  execution.
- **Reporting:** Wilson CIs on all rates; paired tests for condition deltas; n,
  realized throughput, version-drift log, and every deviation from this section
  disclosed in the results.

---

## 8. Threats to validity

| Threat | Mitigation |
|---|---|
| **Training contamination** — reviewer recalls the bug/fix. | §6 protocol; recency gate is primary. Residual risk disclosed. |
| **Fresh-eyes confound** — "any new session would do." | Condition A2 separates fresh-context from cross-vendor effects. |
| **Reviewer asymmetry** — one vendor simply reviews better. | Symmetric both-directions design; per-direction reporting. |
| **Harness confound** — agentic harnesses differ in more than the model. | Acknowledged openly: B compares *vendor stacks* (model + harness), which is the deployable unit teams actually route between. Framed as such, never as a pure model comparison. |
| **Version drift** — auto-updating subscription CLIs change mid-study. | Deliberate design choice: this is a **field study of shipped consumer vendor stacks as practitioners actually operate them** — auto-updating, subscription-billed — stated plainly in limitations. Conditions interleaved within every batch so updates land on all arms ≈equally; runtime-reported model ID + harness version logged per session and shipped with the dataset; drift analyzed as a recorded covariate. The **version-pinned API replication is the named follow-up study.** |
| **Ground-truth noise** — bundled tests pass broken patches (UTBoost). | §6.4: augmented tests for the correct sample; "not-confirmed-defective" framing. |
| **Localization tolerance gaming** — loose N = easy catches. | N fixed in advance; sensitivity to N reported. |
| **Sample size / variance** — agentic runs are noisy. | §7: paired design, repeats subsample, pre-registered n rule, CIs. |
| **Prompt sensitivity.** | Identical prompt across conditions; committed in repo. |
| **Cherry-picking tasks.** | Task set selected by fixed documented rule before any review runs. |
| **LLM-judge bias.** | Not applicable by construction — primary scoring is mechanical (§5). |

---

## 9. Build sequence

- [x] **Step 1 — skeleton + design doc.**
- [x] **Step 1.5 — prior-art scan.** Done 2026-07-15: multi-agent sweep, full
      reads of arXiv:2603.04582, 2605.21537, 2603.26130, independent external
      cross-check, design repositioned (D-009). Gate passed.
- [ ] **Step 2a — build (authorized 2026-07-15, D-014).** Session harness
      (scheduler with within-batch condition interleaving + runtime version
      logging), three-band scoring pipeline (§5), Band 3 adjudication card
      interface, canary suite (below). Open design questions arising mid-build
      are logged in DECISIONS.md as open questions — never resolved unilaterally;
      work that can proceed independently continues.
      **Acceptance:** all four canaries score correctly end-to-end, AND the
      harness + scoring code itself passes cross-vendor review per
      meta-layer-starter's protocol, report attached.
      - [x] canaries 1–4 pass via fixture judges (validates routing + blinding
            only — D-015 binding note)
      - [ ] **canaries re-run against the real rotating judge backend (D-015)
            — build acceptance is claimable only after this passes**
      - [ ] cross-vendor review of harness + scoring code, report attached
- [ ] **Step 2b — pilot (separately gated: requires explicit supervisor
      authorization, expected ~2 weeks out).** One recency-gated task flows
      through real sessions: agent authors → hidden test sorts → three agentic
      review conditions → score. Measures sustainable throughput + variance;
      fixes corpus source and final n (§7 rule); logged before scaling.
      **Additional acceptance:** every Band 3 ruling makeable from the card
      alone (§5 interface criterion).
- [ ] **Step 3 — full run.** Both directions, results table, CIs.
- [ ] **Step 4 — writeup.** Results + method + caveats; arXiv (cs.SE) version
      positioning against §2.

### Canary suite (build acceptance, D-014)

Known-outcome seeded tasks exercising every band:

1. **Mechanical catch** — an exact-localization catch that must score "catch" in
   Band 1, with no model in the loop.
2. **Clean patch** — a test-confirmed-correct change where any defect flag must
   score "false alarm."
3. **Vague-but-correct** — a claim describing the real failure mode without
   precise coordinates; must route to Band 2 and resolve correctly.
4. **Judge bait** — a case constructed to split the judge panel; must escalate
   to Band 3.

The build is not "done" until all four score correctly end-to-end.

## 10. Definition of done (v0.1)

A recency-gated corpus; three blind review conditions with agentic reviewers; one
honest catch-rate + false-alarm number per condition, paired CIs; every
methodological choice pre-registered in this document and DECISIONS.md and held to.
