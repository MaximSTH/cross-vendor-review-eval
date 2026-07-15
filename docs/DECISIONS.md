---
name: decisions
description: Dated log of every methodological decision in this benchmark — what was chosen, what it was chosen over, and why. One entry per decision, append-only.
status: active
---

# Decision log

Methodology owner: **Maxim St-Hilaire**. Append-only — decisions are superseded by
new entries, never edited away. This log exists so that every choice in
[`experiment-design.md`](experiment-design.md) has a dated, defensible rationale.

---

## D-001 · 2026-07-15 · Corpus: SWE-bench Lite, not a static bug corpus

**Chosen over:** Defects4J (Java), BugsInPy (Python), BugsJS (JavaScript).

**Why:** The hypothesis is about an AI being blind to defects in *its own* work.
Static corpora contain human-authored bugs — there is no AI author, so self-review
cannot be run at all. SWE-bench supplies real tasks plus hidden tests, letting an AI
author code and fail naturally; those machine-confirmed failures are the bug set.
Static corpora remain candidates for a v0.2 contamination/rigor control.

## D-002 · 2026-07-15 · Measure detection, not repair

**Why:** The lived claim is "the reviewer *catches* what the author missed" —
a detection claim. Repair ability is a different (and heavily benchmarked) skill.
Scoring detection against known defect locations keeps the metric mechanical.

## D-003 · 2026-07-15 · No planted bugs

**Chosen over:** asking an AI (or human) to insert defects.

**Why:** A planted bug's location is known to its planter, which invalidates the
review; planted bugs are also unrepresentative of natural failure modes. Natural
failures confirmed by hidden tests are real, author-generated, and unknown to all
parties at review time.

## D-004 · 2026-07-15 · Three review conditions, not two

**Chosen over:** the original two-condition design (self-review vs cross-vendor).

**Why:** A two-condition design cannot answer the strongest rebuttal — "any fresh
session would catch it; the second vendor is irrelevant." Added A2 (same model,
fresh session) so the fresh-eyes effect and the cross-vendor effect are measured
separately. Identified in pre-build design review, before any harness code existed.

## D-005 · 2026-07-15 · Structured reviewer output; no LLM-as-judge in the primary metric

**Chosen over:** free-prose reviews scored by another LLM.

**Why:** LLM judges import their own biases and are a standard reviewer objection.
Forcing `{file, line, description}` output makes the catch/no-catch decision a
mechanical coordinate match against ground truth. An LLM-judged "semantic match"
may be reported as a clearly-labeled secondary metric only.

## D-006 · 2026-07-15 · Symmetric vendor pairing (Claude ↔ OpenAI, both directions)

**Why:** Running only one direction confounds "cross-vendor review helps" with "one
vendor is simply a better reviewer." Both-directions design isolates the self-vs-
cross variable. Vendors chosen: Anthropic (Claude) and OpenAI — the most widely
used pairing and the one this methodology was developed against.

## D-007 · 2026-07-15 · Generic, identical review prompts — the benchmark tests the premise, not the meta-layer harness

**Chosen over:** having the cross-vendor reviewer run the full `meta-layer-starter`
review protocol.

**Why:** The meta layer is a broad operating layer (protocols, gates, supervision,
templates); it is not benchmarkable as a whole. What *is* measurable is its
load-bearing premise — that a different-vendor reviewer catches defects the author
missed. Testing that premise with a bare, identical prompt in every condition keeps
the comparison immune to the "your side got better instructions" objection, and a
positive result validates the premise behind the layer without grading its own
homework. A protocol-equipped reviewer arm remains a possible (optional) follow-up
study.

## D-008 · 2026-07-15 · MIT license (renumbered from D-007 when D-007 was inserted)

**Why:** Maximum-adoption license for a benchmark whose value grows with external
use and citation. No copyleft friction for labs or companies reproducing the runs.

## D-009 · 2026-07-15 · Repositioned v0.1 after prior-art scan: from premise-proving to routing benchmark

**Chosen over:** the original design, which tested whether cross-vendor review
catches defects self-review misses — as a novel finding.

**Why:** The prior-art gate (Step 1.5) found the premise already established:
arXiv:2603.04582 (Mar 2026) showed rating-based self-review blindness on
SWE-bench with a 10-model cross-vendor matrix; arXiv:2605.21537 (May 2026) showed
31.7% silent self-endorsement of defective outputs. An external cross-check
additionally surfaced SWE-PRBench (arXiv:2603.26130), which scores review quality
against human PR comments. Full reads of all three (independently verified — one
false "paper doesn't exist" alarm was itself refuted by direct fetch) established
the open cell: **agentic** reviewers, **AI-authored test-confirmed** defects,
**three-way authorship manipulation**, **mechanical file+line catch-rate +
false-alarm scoring, no LLM judge**, framed as a review-routing decision. v0.1 now
claims exactly that cell and cites all three papers as motivation. The original
"premise" framing survives only as motivation, never as the claimed contribution.

## D-010 · 2026-07-15 · Contamination is a first-class design constraint; corpus must be recency-gated

**Chosen over:** using SWE-bench Lite as-is (original plan), or static corpora
(Defects4J/BugsInPy — already excluded by D-001, now doubly excluded).

**Why:** A reviewer that "finds" a memorized bug proves recall, not review; review-
step contamination inflates catch-rates and possibly unevenly across vendors.
Tasks must postdate every evaluated model's training cutoff. Adopts SWE-PRBench's
published mitigation playbook (recency window, low-star preference, similarity
screen) plus ground-truth hardening per UTBoost (arXiv:2506.09289): "passed
bundled tests" is treated as not-confirmed-defective, never certified-correct.
Raised by external design review; accepted without reservation.

## D-011 · 2026-07-15 · Power & budget fixed by pre-registered rule before harness code

**Chosen over:** building the harness first and sizing the study to whatever
budget remains.

**Why:** Agentic sessions are expensive and high-variance; improvising n downward
after seeing costs (or worse, results) is the exact failure a skeptical reviewer
looks for. The pilot (Step 2) prices a real session; final n follows a rule fixed
in the design doc §7 *before* any full run; the cut order under a budget cap is
also pre-registered (headline A2-vs-B paired comparison protected first). Raised
by external design review; accepted.

## D-012 · 2026-07-15 · Subscription-first execution; version drift is a covariate, not a constant

**Chosen over:** API execution with pinned model versions (the D-011-era working
assumption).

**Why (supervisor directive):** The study runs on the owner's existing
subscriptions (Claude Code, Codex CLI; Antigravity CLI available) — there is no
API budget. Consequences, all deliberate: (a) versions are not pinned — every
session logs the runtime-reported model ID + harness version, logs ship with the
released dataset; (b) conditions are interleaved within every batch (never a
block of one arm) so mid-study vendor updates land on all arms approximately
equally; (c) version drift is analyzed as a recorded covariate. Framing
throughout: a **field study of shipped consumer vendor stacks as practitioners
actually operate them** — auto-updating, subscription-billed — stated plainly in
limitations. The version-pinned API replication (~$1.5k–4k, documented in §7) is
the named follow-up for teams/labs, not part of this study. Sizing is
throughput-constrained: the pilot measures sustainable sessions/week under real
weekly limits; final n = pre-registered rule applied to measured throughput; cut
order unchanged; headline paired A2-vs-B comparison protected first.

## D-013 · 2026-07-15 · Three-band scoring pipeline (supersedes D-005 in part)

**Chosen over:** D-005's binary rule (mechanical primary metric; LLM judge as
secondary diagnostic only).

**Why (supervisor directive):** A single mechanical band either drops
imprecisely-localized-but-correct claims or forces a judge on everything. The
three-band structure quarantines judgment instead: **Band 1** — deterministic
file+line comparison, no model in the loop, maximized by the forced structured
output; **Band 2** — blinded LLM judges for residual semantic matching, inputs
vendor-anonymized (self-preference bias concentrates on the self diagonal and
anonymization suppresses it, arXiv:2603.04582 — an unblinded judge would
reintroduce the measured bias one layer up), ≥2 judge families, per-case
agreement logged, disagreement escalates; **Band 3** — human audit by the
methodology owner of a pre-registered random n=75 Band 2 sample (proposed from
the 50–100 range) plus every judge disagreement, with human–judge κ reported as
the validation of Band 2. D-005's core commitment (no LLM judge in the
mechanical band; judge never silently authoritative) survives strengthened:
judges are now blinded, plural, and human-audited.

## D-014 · 2026-07-15 · Build authorized; pilot separately gated; interface + canary acceptance criteria

**Why (supervisor directive):** Build phase (harness, scoring pipeline,
adjudication interface, canary suite) is authorized as of item-0 commit. Pilot
execution is a **separate go decision** — no pilot sessions until explicit
supervisor authorization (expected ~2 weeks out). Mid-build design ambiguities
are logged below as open questions, never resolved unilaterally. Acceptance
criteria: **(build)** all four canaries — mechanical catch, clean-patch false
alarm, vague-but-correct → Band 2, judge-bait → Band 3 — score correctly
end-to-end, and the harness + scoring code itself passes cross-vendor review per
meta-layer-starter's protocol with the report attached; **(pilot)** every Band 3
ruling makeable from its self-contained card alone — a case requiring cold-reading
a diff is an interface defect, not an escalation.

## D-015 · 2026-07-15 · Rotating judge panels; Band 3 blind end to end; OQ-1/OQ-2 resolved; n=75 ratified

**Chosen over:** the OQ-1 proposal of a "neutral" Google judge.

**Why (supervisor ruling):** There is no neutral family — Antigravity is a
vendor under test like the others. Panel assignment is **per-case rotation**:
the panel is exactly the two families that did not author the judged output.
The router uses authorship for panel assignment only; judge inputs remain fully
anonymized per D-013. Symmetric across all three vendors; same-family judging
eliminated by construction; enforced by a property test.

*Recorded interpretation:* "the output" = the judged artifact, i.e. the
reviewer's claim, so the excluded family is the reviewing session's. Under
A1/A2 this coincides with the patch author's family; under B it follows the
claim's author (the judge sees only annotation + claim, never the patch).
Excluding both reviewer and patch-author families would leave a one-judge panel
under B, violating D-013. Flagged for supervisor correction if intended
otherwise.

**Band 3 blindness (same ruling):** under rotation, naming the judging families
reveals the authoring vendor as the missing third. Cards therefore label judges
by role only ("Judge A (non-authoring)"), render only the anonymized claim text
(the same artifact judges receive), and card generation lints its rendered
output, failing closed on any vendor/model/harness identifier. Ruling-boundary
helper text (catch / no_catch / false_alarm / unscorable, reader-actionability
policy) is embedded in every card set; precedent P-001 (canary4 → no_catch)
recorded in design doc §5.

**OQ-2 resolved (ratified with amendment):** ±5 is the pre-registered primary
tolerance; Band 1 additionally rescored at ±1 and ±10, sensitivity sweep
reported in an appendix. Deterministic rescoring only; no design change.

**Band 3 sample ratified:** n = 75.

**Binding acceptance note:** canaries 3–4 passing against fixture judges
validates routing and blinding only. Build acceptance is claimable **only**
after all four canaries pass against the real rotating judge backend. Carried
as an explicit unchecked item in the design doc §9 build gate.

---

# Open questions (awaiting supervisor decision — build proceeds around them)

## OQ-1 · 2026-07-15 · ~~Band 2 judge backend~~ — **RESOLVED by D-015**

Superseded: the "neutral Google judge" proposal was rejected; per-case rotation
adopted. Remaining mechanics (how each family's CLI is invoked headless as a
judge) are implementation, not design, and live in the runner config.

## OQ-2 · 2026-07-15 · ~~Localization tolerance N~~ — **RESOLVED by D-015**

±5 primary, ±1/±10 sensitivity sweep in appendix.

## OQ-3 · 2026-07-15 · Review prompt — exact wording requires ratification

§8 names prompt sensitivity as a threat and commits the identical, verbatim
prompt to the repo. The prompt is therefore an experimental artifact, not an
implementation detail. A draft lives at `harness/prompts/review-prompt.md`;
it must be ratified (or amended) by the supervisor before pilot authorization.
