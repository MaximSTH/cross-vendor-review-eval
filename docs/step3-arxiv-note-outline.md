---
name: step3-arxiv-note-outline
description: Outline for the C+ arXiv methods-and-findings note (cs.SE) — a SEPARATE deliverable from the practitioner write-up. Three contributions: the corpus-integrity taxonomy, the catch-audit metric-validity result (localization catch-rate is an upper bound), and F-001 diff-anchoring as a documented phenomenon with n stated. No new sessions required. Draft outline for supervisor review.
status: draft
author: Maxim St-Hilaire (methodology owner) — drafted by worker for review
last-updated: 2026-07-24
---

# C+ arXiv note — outline for review

**What this is (HANDOFF "Track C+", item 2).** A **methods-and-findings note**,
drafted as a **separate deliverable** from the practitioner write-up
(`results/pilot/practitioner-writeup.md`, which proceeds to publication as-is,
D-022 clean). The note targets **arXiv cs.SE** and makes **three contributions**,
each already established in the pilot record — **no new sessions required**:

1. The **corpus-integrity taxonomy** — five distinct failure modes, four
   feed-attributable, in a curated externally-provenanced SWE-bench-derived feed;
   ~29% usable.
2. The **catch-audit metric-validity result** — a localization (file+line)
   catch-rate is an **upper bound**; audit it. 0/2 mechanical catches survived
   human audit in the pilot.
3. **F-001 "diff-anchoring"** as a **documented phenomenon with n stated** —
   reviewers grade the presented diff and miss the true defect elsewhere; **2 P1
   defective cases + P0**, reported as an observed pattern and a hypothesis to
   size, **never as an established rate**.

**Relationship to the practitioner write-up.** The practitioner piece is the
plain-language, branch-independent standalone. **This note is the archival,
method-forward version**: same three findings, but framed for a
software-engineering-research audience — precise definitions, the pipeline
disciplines that produced the findings (ERROR-vs-FAIL, incoherence heuristic,
oracle-authoritative evaluation), positioning against the three motivating papers,
and reusable recommendations for anyone building SWE-bench-derived review
evaluations. Overlap is expected and fine; the two are different registers of the
same pilot. **Per the 2026-07-24 supervisor ruling the two *accompany* each other
and *cite each other* — neither supersedes the other** (mechanics in Drafting
notes). **The note reuses no un-audited claim** — every number carries its n.

**Binding constraints on the whole note (D-022, non-negotiable):**
- **No adoption claims without adoption data.** The practice is **"advocated and
  publicly tooled"** (cite `meta-layer-starter`, cite the bias papers) — never
  "increasingly used by teams." Applies to abstract, intro, and any generated
  outreach text.
- **Every rate carries its n; nothing is an established rate.** n = 6 end-to-end
  cases (P0 + 5 P1), 3 confirmed-defective (P0 + pos2 + pos5); 2 mechanical
  catches audited; ~29% usable measured on JS/TS.
- **Field-snapshot framing, not a pinned-model comparison** — consumer
  subscription stacks as operated, auto-updating, versions logged not pinned
  (D-012). The Anthropic reviewer is an **opus-4.8[1m] + haiku-4.5 stack**; the
  OpenAI reviewer is **GPT-5.6 Sol @ xhigh** (config-introspected, D-053).

---

## Proposed section-by-section outline

### Title (candidates)
- *"When the reviewer grades the diff: diff-anchoring and metric validity in
  cross-vendor AI code review"*, or
- *"A benchmark instance that exists is not one that runs: corpus-integrity and
  catch-metric validity findings from a cross-vendor AI-review pilot."*
- Title choice is a supervisor call; both foreground a *methods/validity*
  contribution over a (deliberately absent) headline catch-rate.

### Abstract (~150 words)
- One sentence of motivation (advocated + tooled; the two bias papers), then the
  three findings **with n stated in the abstract itself**, then the explicit
  non-claim: **no powered catch-rate is reported** and none is implied. The
  abstract must not contain a number that could be read as an established rate.

### 1. Introduction & positioning
- The routing question teams face: *is a second vendor's review worth it over a
  fresh look from your own?* (design §1–§2).
- **Prior art (the three papers), stated as motivation, not contribution**
  (D-009): Self-Attribution Bias (arXiv:2603.04582), Articulate but Wrong
  (arXiv:2605.21537), SWE-PRBench (arXiv:2603.26130). The open cell: **agentic**
  reviewers, **AI-authored test-confirmed** defects, **mechanical file+line**
  scoring, **no LLM judge** in the primary metric.
- **What this note claims:** not the routing answer (the pilot is underpowered by
  design for that), but **three methods/validity findings** that any builder of
  such a benchmark needs — and that are robust at small n because they are about
  *failure modes and definitions*, not effect sizes.
- **Explicit scope disclaimer up front** (the honesty spine): pilot scale, n
  reported throughout, no adoption claim, JS/TS + specific shipped stacks.

### 2. Setup (compact — enough to read the findings)
- Author → hidden test → three blind review conditions (A1 self-session, A2 fresh
  same-vendor, B cross-vendor) → three-band mechanical-first scoring (design
  §4–§5). Identical verbatim prompt (design §8, OQ-3).
- Ground truth = the gold patch's `-`-side defect region; catch = file+line within
  ±5 (±1/±10 sweep), **no model in the primary metric** (D-005).
- Corpus = recency-gated (>2026-03-01) slice of SWE-bench-Live/MultiLang, JS/TS
  (D-023/D-027a). Field-snapshot version discipline (D-012).
- Keep this section short; it exists to make §3–§5 legible, not to re-derive the
  design doc.

### 3. Finding I — corpus-integrity taxonomy (feed defects at ~29% usable)
- **The measurement:** filling the pilot's task slots required walking **17
  post-gate JS/TS rows; 5 usable → ~29%** (report §4; D-051 walk trail).
- **The taxonomy — five modes, four feed-attributable, one rig-relative** (the
  D-049 standing catalog, the note's central table):
  1. Label integrity — **whole-suite-as-F2P**, P2P empty (`youtube-3708`).
  2. Label integrity — **phantom F2P names** (`Gladys-2504`).
  3. Label integrity — **F2P passes at base** (`vueuse`, `gsd-2-2643`, `AionUi`).
  4. **Missing image** — registry 404 (`anything-llm`, `mongoose`, `proj4js`).
  5. **Eval-harness failure** — shipped test command runs no tests (`bruno-7620`,
     `gsd-2-3258`: jest absent / invalid node flags / failing pretest typecheck).
  - Rig-relative (NOT feed defects; rerunnable on native amd64): **platform
    infeasible** — hard (`oh-my-pi` bun crash) and time (process-per-test ×
    thousands under emulation). Stated as a **reproducibility caveat about the
    rig**, cleanly separated from feed defects.
- **What made this measurable rather than noise — the pipeline disciplines**
  (this is the methods contribution, reusable by others):
  - the **execution-based admission screen** (D-028): run the task at base with
    only the test patch; require declared-F2P to fail and P2P to pass *before*
    trusting any label;
  - **ERROR ≠ FAIL** (D-028/D-030/D-045): a failure to *measure* (parsed==0,
    OOM, missing image) is never a finding about the task;
  - the **incoherence heuristic** (D-040/D-047): a stage output that contradicts
    an upstream-verified fact indicts the *measurement*, not the task — it caught
    three would-be false verdicts across intake/procedure/evaluation;
  - the **oracle-repair boundary** (D-049e): a non-running shipped test command is
    a *recorded finding about the feed*, **never** patched into working order —
    repairing the oracle is authoring the benchmark.
- **The transferable claim:** *a benchmark instance that "exists" in a dataset is
  not one that runs and means what its labels claim.* Any evaluation on a
  SWE-bench-derived feed that skips execution-based admission is, at some rate,
  scoring against labels that do not hold. **Correction to prior belief:** the
  OQ-9 evidence table credited this feed with "invalid instances filtered by
  running regression tests ×3"; the pilot shows that filter did not catch these
  modes (report §4; D-028d). State this as a correction, precisely and without
  overreach.
- **Live-verified supply appendix hook:** the post-gate pool is 322/743 MultiLang
  (283 non-JS/TS) + 110 SWE-rebench (Python), re-verified 2026-07-24
  (`step3-preregistration.md` §2). Cite so readers can reproduce the supply
  numbers; the ~29% *usable* rate is the JS/TS measurement, flagged as such.

### 4. Finding II — catch-metric validity: localization catch-rate is an upper bound
- **The mechanism.** Band 1 scores a **catch** on a file+line coordinate match,
  *regardless of what the claim says* (D-005 — this is deliberate; coordinate
  matching is reproducible and judge-bias-free, the whole point of the primary
  metric). But a coordinate match can be **semantically empty**.
- **The pre-registered validity layer** (D-039): a **human catch-audit** of Band-1
  catches against the **reader-actionability** standard (P-001): *would a busy
  engineer following this claim find and fix the bug?* Symmetric with the Band-2
  human audit; agreement reported alongside Band-2 κ. Primary metric **untouched**
  — the audit is a validity layer over it.
- **The result: 0 of 2** mechanical catches survived the audit (report §6;
  D-043). Both were diff-anchoring artifacts:
  - **P-002 coincidental localization** — a semantically-unrelated claim
    (error-handling nit) on a coincidentally-correct line; a reader following it
    would not find the credential leak.
  - **P-003 inverted claim** — right location, but asserts the *correct* fix is
    the bug; a reader could revert the right approach and reintroduce the defect.
- **The catch-definition dependency chain** (D-044c — the methods-section spine):
  the vendor comparison is only as meaningful as the definition of "catch"; if a
  catch can be semantically empty, a raw localization catch-rate measures
  coordinate coincidence, not detection. **Therefore a localization catch-rate is
  an upper bound**, and a benchmark reporting one needs a validity layer (human
  audit, or a calibrated semantic check) to state how many "catches" are real.
- **n discipline:** 2 audited catches is tiny; the note reports the **direction
  and the two named failure modes**, and frames the audit as the *calibration
  instrument* a powered study would carry — **not** a "0% real-catch rate."
- **Forward hook (kept out of the results, into a one-line "future work"):** a
  semantic-catch layer over all catches, calibrated by this audit, is a natural
  extension — explicitly **deferred** pending judge-quota feasibility (OQ-21;
  `step3-preregistration.md` §4.6). Mentioned as future work, not a finding.

### 5. Finding III — F-001 "diff-anchoring" (documented phenomenon, n stated)
- **The statement** (D-F001, verbatim): *when the authored fix lands in a
  different location than the true defect, reviewers critique the change in front
  of them and miss the real bug elsewhere.* A claim about **reviewer behavior**,
  not about the harness or corpus.
- **The three instances, cited** (report §5; the note states n = **2 P1 defective
  cases + P0** every time it names the phenomenon):
  1. **P0 (`doctoc-328`):** patch machine-confirmed defective; **all three arms
     zero claims** — unanimous miss.
  2. **P1 pos2 (`NemoClaw-330`):** author fixed 1 of 4 credential locations; both
     mechanical "catches" on the authored block, **overturned by the audit**
     (P-002/P-003) → 0 audited catches.
  3. **P1 pos5 (`next-translate-1259`):** author fixed `appWithI18n.tsx`; the true
     defect is in `DynamicNamespaces.tsx`/`I18nProvider.tsx` → **unanimous
     no_catch**.
- **Why it connects §4 to §5:** diff-anchoring is *why* the catch-audit matters —
  a mechanical catch can be the reviewer critiquing the diff at a
  coincidentally-correct line (P-002) rather than finding the defect. The two
  findings are one story: **the metric over-counts exactly the behavior the
  phenomenon predicts.**
- **The hard n-caveat, stated in the section and again in limitations
  (binding):** n is tiny (2 P1 + P0). Reported as the **observed central pattern
  with n stated** and as the **sharpest hypothesis for a powered study to size**
  — the design is built to estimate the per-arm diff-anchoring miss-rate — **not**
  as an established rate. **Cross-vendor did not rescue it** in any pilot case, but
  that is a direction at n=3, not a measured null.

### 6. Threats to validity / limitations (plain, up front — the note's ethic)
- n is tiny; JS/TS only; specific shipped stacks and versions (field snapshot, not
  pinned); the OpenAI model-ID was config-introspected not stream-reported (D-053
  gap, closed); two P1 cases share repos with earlier tasks (reported covariates,
  fixed-rule-selected, never hand-excluded); Band 2 never ran (quota unmeasured);
  audit was made with run-context exposure in the pilot (main-study fix:
  card-alone-before-analysis, D-044b). **A1 holds strictly more information than
  A2/B by construction, making cross-condition comparisons conservative** (D-031e)
  — state it as a property, not a caveat.
- **No adoption claim; no powered result claimed.** The contribution is
  methods/validity + a documented phenomenon, explicitly.

### 7. Reproducibility & artifacts
- MIT-licensed public repo; full decision log (D-001…D-053); every session
  transcript, the evaluator (`raw/evaluate.py`), the screen, the Band-3 cards +
  rulings. Live-verified corpus supply queries (`step3-preregistration.md` §2).
- **Motivating prior art cited, verified by direct fetch** (design §2 source note):
  arXiv:2603.04582, 2605.21537, 2603.26130.

### 8. Future work (one paragraph, no commitments in the note)
- The powered study (Sequential-B) is *ongoing/planned*, not reported here; name
  it as future work with the diff-anchoring miss-rate as its target estimand.
  Semantic-catch layer and multi-language corpus expansion mentioned as extensions
  (deferred / in progress, `step3-preregistration.md`). **Do not report any
  Step-3 result** — none exists; the note is C+ (the pilot as a terminal
  publishable deliverable) running *in parallel* with Sequential-B, per the
  ruling.

---

## Drafting notes (for when the outline is ratified into prose)

- **Reuse, don't re-measure.** Every claim maps to a committed artifact + a
  D-entry; the note is an *assembly and framing* task, not a new-data task. The
  practitioner write-up is the register-shifting starting point for §§3–5.
- **The two documents must not contradict.** Keep the note's numbers identical to
  the practitioner write-up and the report; if a number is refined, refine both.
- **Render/export** via `tools/render-doc.sh` (self-contained HTML) for
  circulation, same as the report/write-up/decision-brief.
- **Author line / venue.** cs.SE; author + acknowledgement text is a supervisor
  call. arXiv **comments field** is outreach text and is bound by D-022 (no
  adoption claim) like everything else.
- **Note↔write-up relationship — RULED 2026-07-24 (supervisor): accompany, with
  reciprocal citation.** The C+ note and the practitioner write-up are **two
  documents for two audiences** (cs.SE archival vs practitioner), not one
  superseding the other. **They cite each other:** the note names the practitioner
  write-up as its plain-language companion (§7 Reproducibility); the write-up gains
  a one-line pointer to the archival note. Both remain D-022-clean and
  numerically identical. *Sequencing note (worker):* the reciprocal pointer is
  **added to the publish-ready practitioner write-up only once the note itself
  exists** (a live cite, not a dangling reference to an unwritten paper) — i.e. at
  note-drafting time, not now, to avoid shipping a broken citation. Flagged so the
  timing is explicit, not an omission.
