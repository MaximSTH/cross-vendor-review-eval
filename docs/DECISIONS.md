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

**Ratified 2026-07-15 (supervisor), with one binding condition.** Rationale for
the record: the judged artifact is the claim text, whose stylistic fingerprint
belongs to its author — the reviewer; that is the leak vector rotation closes.
**Binding condition:** judges receive exactly two artifacts — the anonymized
claim and the answer-key annotation. Never the patch/diff, never repo content.
Any future design change that would put patch content in front of judges
reopens this interpretation and goes to this log first. Enforced by a
structural test on the judge input bundle.

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

## D-016 · 2026-07-15 · Claims cap k=5 (ranked) + verbosity metrics

**Chosen over:** an unbounded claims list.

**Why (supervisor directive):** Under the P-001 boundary rules, missed-bug
flags on buggy tasks carry no penalty, so an unbounded list lets a reviewer
shotgun claims and inflate catch-rate at zero cost. Closure: (a) the prompt
caps claims at a pre-registered **k = 5**, ranked most-confident first —
justification: each task plants a single defect, and k=5 matches the standard
top-5 convention in fault-localization evaluation while bounding shotgun
strategies; (b) scoring computes catch-rate against the ranked list as
submitted (harness truncates at k defensively and records truncation); (c)
results additionally report per-vendor **mean claims-per-task** and
**precision-on-buggy-tasks**, so verbosity differences are visible rather than
laundered into catch-rate.

## D-017 · 2026-07-16 · Judge execution: env-var trust for Gemini; ALL judges run tools-fully-disabled

**Chosen over:** interactive one-time trust (unreproducible machine state) and
installing Antigravity for judging (both rejected by supervisor).

**Why (supervisor ruling):** The Google judge uses the environment-variable
trust mechanism (`GEMINI_CLI_TRUST_WORKSPACE=true`), explicitly authorized for
judge scratch-dir invocations and documented in provenance with every run.
Stronger requirement, all three families: **judge invocations run with tools
fully disabled — no file access, no command execution, no MCP/connectors.**
Judges receive self-contained text and return a verdict; there is no
legitimate tool use in that job. Where a CLI supports it, pin explicit
disallow flags and **verify by probe** (the Anthropic judge's probe pattern
extended to OpenAI and Google). This also closes the MCP residual from the
2026-07-15 D-014 review report (closure noted there).

*Execution record (2026-07-16):* Anthropic judge — hardened + probe-verified
(`mcp__*` added to the disallow list). OpenAI judge — probes show `codex exec`
reads absolute paths under default and under `-c 'sandbox_permissions=[]'`;
no supported tools-disable flag found → OQ-7. Google judge — the env-var
mechanism is **moot**: `gemini` hard-fails `IneligibleTierError` on this
account (migrated to Antigravity) before any prompt; Antigravity is not
installed and was ruled out for judging by this very decision → OQ-6. D-017's
tools-disabled requirement stands; its Google-execution choice needs re-ruling.
OQ-6 → resolved by D-019 (API judge); OQ-7 → resolved by D-020 (behavioral
enforcement + amended wording).

*Incident record (2026-07-16, supervisor-directed to keep here):* with OQ-7
still open, the worker attempted the real canary run, which would have
executed the Codex judge without the required isolation. The harness
permission layer blocked the command on exactly the standing rule
(design-level gaps are ruled, never resolved unilaterally). The block was
correct; the run waited for the D-020 ruling. Standing rule working as
designed.

## D-018 · 2026-07-16 · Reviewer compliance enforcement — post-hoc test-suite-invocation scan

**Why (supervisor ruling, attached to OQ-3 ratification):** The prompt's
no-test-suite rule is instruction-only and reviewer CLIs can ignore it. Every
reviewer session transcript is scanned post-hoc for test-suite invocation
(pytest, unittest, npm test, go test, and equivalents — pattern list
maintained in code, `harness/compliance.py`). Violating sessions are
**excluded and re-run**; exclusions are counted and reported per vendor.
Pre-registered rule: exclusion happens **before scoring, blind to what the
review claimed.**

## D-019 · 2026-07-16 · Google judge runs on a free-tier Gemini API key

**Chosen over:** the two OQ-6 logged options (Antigravity reversal; two-family
pool) — neither adopted.

**Why (supervisor ruling):** A judge is a self-contained text completion, so
the agentic CLI was never a requirement — and a bare API call satisfies
D-017's tools-disabled rule **by construction**: no filesystem, no commands,
no MCP exists in that execution path. Consistent with D-012, which constrains
budget, not API usage; the tier is $0. The pilot additionally measures
free-tier daily-quota feasibility against expected Band 2 volume.
**Pre-registered fallback** if the free tier is unavailable or
quota-infeasible: reverse D-017's no-Antigravity clause as a documented
exception, with the same probe-verified tools-disable requirement as the
Anthropic judge. **The two-family pool is rejected permanently** — it
reintroduces same-family judging or collapses to a one-judge panel; struck
from all future option lists.

*Alias ruling (2026-07-18, supervisor — appended per directive):* the
`gemini-flash-latest` switch is **ratified**, with one pre-registered
addition: the judge is a **measurement instrument**, so if the resolved judge
model changes mid-pilot or mid-study, that is flagged in provenance and Band 2
judge-agreement rates are compared before/after the shift for discontinuity,
reported in the write-up. The same principle extends to the other two judge
stacks: **any runtime-reported judge version change triggers the same check.**

*Key handling (2026-07-18, supervisor):* the key is exported as
**`CVRE_GEMINI_JUDGE_KEY`** — deliberately not the standard `GEMINI_API_KEY`
name, so no Google CLI or SDK auto-reads it and the reviewer arm's auth path
stays untouched. Read from the environment under that exact name only; the
key value is never shared with the worker agent, never written to a file.
Release-blocking tests assert provenance logs and shipped artifacts contain
neither the key nor request auth headers (logs are published per D-012, so
this is a release gate, not hygiene).

## D-020 · 2026-07-16 · Codex judge: behavioral enforcement; D-017 wording amended

**Why (supervisor ruling):** No supported tools-disable flag exists for
`codex exec` (OQ-7 probes). Enforcement is behavioral: **(a)** invoked from an
empty scratch directory outside any repo path, payload via stdin only;
**(b)** post-hoc transcript assertion — any tool invocation of any kind in a
judge transcript **invalidates that judgment**, triggers a re-run, and is
counted in a reported audit metric; **(c)** D-017's wording is amended to
"tools disabled by flag where supported; where not supported, isolated by
environment and audited by transcript, violations invalidating." The
Anthropic judge keeps flag enforcement **plus** the same transcript audit as
belt-and-suspenders. The asymmetry is stated plainly in limitations (design
doc §8, first paragraph) — one sentence, not buried.

## D-021 · 2026-07-18 · Pilot scope ratified with amendments; format-failed sessions pre-registered

**Chosen over:** the OQ-8 proposal as drafted.

**Why (supervisor ruling):** Pilot scope is P0 + P1 as proposed, amended:
**(a)** P1 = 5 tasks ratified; the k=2 repeat extends to **two** tasks, the
second executing **only if no limit-hit events have occurred by day 3** —
pre-registered, not discretionary. **(b)** 0.7 safety factor ratified, but
sustainable sessions/week = **min(observed × 7 × 0.7, owner-declared
normal-week ceiling)** — pilot days are atypically dedicated; the ceiling is
declared at pilot go. **(c)** 50% quota-feasibility threshold ratified as
proposed. **(d)** Format-failure trigger amended: escalate if **any single
vendor exceeds 20% or aggregate exceeds 30%, whichever first.**

**Pre-registered before P0 — scoring treatment of format-failed sessions:**
they are **excluded and re-run** (mirroring D-018's
exclude-before-scoring-blind rule), never scored as empty claims; per-vendor
format-failure counts are a reported metric. If the re-run also fails format,
the session is recorded as **unscorable-format**, reported, never silently
dropped.

## D-022 · 2026-07-18 · Write-up honesty rule: no adoption claims without adoption data

**Why (supervisor standing rule, logged for the drafting phase):** Write-up
motivation must **never claim industry adoption without adoption data**. The
practice is **"advocated and publicly tooled"** — cite `meta-layer-starter`,
cite the bias papers (arXiv:2603.04582, arXiv:2605.21537) — never
"increasingly used by teams." Applies to the abstract, the introduction, and
**any outreach text generated from the repo** (README, talk abstracts, press
pitches, arXiv comments).

## D-023 · 2026-07-18 · Corpus ruling: recency gate, UTBoost-clause interpretation, SWE-bench-Live/MultiLang selected

*(Numbering note: the supervisor designated this ruling "D-022"; that number
was already assigned to the adoption-claims rule earlier the same day
(commit 1c37d36), so this entry logs as D-023 with content unchanged.)*

**Why (supervisor ruling, on the OQ-9 evidence table):**

**(a)** Operative recency gate ratified at **> 2026-03-01** (buffer over the
2026-02-16 hard max, per Anthropic month-granularity).

**(b)** UTBoost clause interpretation, ratified verbatim: D-010 adopted
UTBoost's treatment stance — bundled-test passes are never certified-correct —
**as a pipeline rule, not a feed-shipping requirement.** Feed-native filtering
plus our §6.4 rule satisfies the pre-commitment.

**(c)** Corpus selected: **(b1) SWE-bench-Live/MultiLang**, conditional on P0
validating the RepoLaunch Docker flow. Rationale for the record: largest
measured post-gate supply (322), freshest, external provenance per the OQ-9
pre-committed preference; the language mix is neutralized in the headline
comparison by the paired design (same task, all three arms) and recorded as a
covariate. **Pre-registered fallback:** (b2) SWE-rebench, triggering only if
P0's RepoLaunch validation fails — the exact-count re-query runs only if the
fallback triggers.

**(d)** P0's task comes from the **JS/TS slice**.

## D-024 · 2026-07-18 · Pre-publication history rewrite: author/committer email → GitHub noreply

**Why (supervisor ruling):** Email privacy — GitHub blocked the publication
push because commits carried the owner's private email; publication must
precede results (design-public-before-results). **Scope:** all 17 commits at
ruling time, plus the hash-map commit added per the ruling's ordering (18
total rewritten). Author and committer email → the owner's GitHub noreply
address; names, messages, content, and dates unchanged. **Hash map:**
`docs/hash-map.md` — old→new for every rewritten commit, dry-run-predicted
and verified identical against the real rewrite. Every commit hash cited in
docs was updated via the map; the repo's local git config now uses the
noreply address so all future commits are clean at birth. Secrets scan re-run
on the rewritten history before push.

## D-025 · 2026-07-18 · D-018 boundary: quotation is not invocation; adjudication procedure pre-registered

*(Numbering note: the supervisor designated this ruling "D-024"; that number
was already assigned to the history-rewrite entry the same day, so this entry
logs as D-025 with content unchanged — second collision, same handling as
D-023's.)*

**Why (supervisor ruling, option (a) on the P0 A2 scan hit):** A2 run 1
stands: every pattern hit is quotation (repo documentation — the target repo
ships its own `AGENTS.md` recommending `npm test` — and CI workflow YAML),
zero execution lines; the rule's object is oracle access and none occurred.

**Amendments, all binding before P1:**

1. The scanner gains **exec-context-aware patterns**; the P0 A2 transcript is
   committed as the false-positive regression fixture
   (`tests/fixtures/d018-false-positive-transcript.txt`).
2. **Pre-registered adjudication procedure for all future runs:** pattern hit
   → automated exec-context check → if still ambiguous, human adjudication on
   the transcript excerpt **before scoring is computed or revealed** —
   inclusion decisions are never made downstream of scores. Tonight's ruling
   is noted in-entry as the exception that motivated the rule:
   outcome-irrelevant here (all arms scored identically; pilot data
   regardless), impermissible in the main study.
3. Scanner patterns **freeze at pilot close** alongside everything else;
   refinements during P1 are logged, none after.

## D-026 · 2026-07-21 · P1 authorized; D-021b normal-week ceiling declared at 15 sessions/week

**Why (supervisor ruling, at pilot go):** Two inputs delivered together.

**(a) P1 GO.** Authorized per protocol §2 and D-021: 5 tasks through the full
flow, at whatever pace the owner's availability tolerates, through
**~2026-07-25**. Interleaved per D-012, k=2 repeat rules per D-021a, all
logging per protocol §3. Execution proceeds across multiple working windows;
each pause and resume is logged (`results/pilot/p1-log.md`) since wall-clock
elapsed is not session time and the throughput measure depends on the
distinction.

**(b) D-021b ceiling declared: 15 sessions/week.** The owner's honest
sustainable estimate for normal working weeks alongside their job. Applied per
D-021b as `min(observed × 7 × 0.7, 15)`.

*Recorded implication (worker note, not a design change):* P1 is ~20 sessions
over ~4 days ≈ 5 sessions/day, so `observed × 7 × 0.7 ≈ 24.5`, and the
**declared ceiling of 15 will bind** unless observed throughput falls below
~3.06 sessions/day. Consequence: final n via §7's rule is driven by the
declaration rather than by the pilot's measurement. This is exactly what
D-021b was written to do (pilot days are atypically dedicated) and is flagged
here only so the pilot report states it plainly rather than presenting 15 as a
measured quantity. The measured `observed × 7 × 0.7` is reported alongside it
regardless.

*Accepted 2026-07-21 (supervisor):* the note is binding — **the pilot report
states plainly that final-n is declaration-driven (15 < measured), per
D-021b's design.** Not a caveat buried in an appendix; the sentence appears
where final n is computed.

## D-027 · 2026-07-21 · P1 selection rules ratified (OQ-10/11/12); 5 tasks fixed before any session

**Why (supervisor ruling, all three worker recommendations adopted as
proposed):** Task 1 could not start without these; each closes a
pre-registration gap rather than making a new methodological choice.

**(a) OQ-10 — P1 slice: continue JS/TS.** P1 takes the next rows after P0's in
the same combined JS+TS ordering. Rationale as logged: RepoLaunch is validated
(D-023c) on JS only; an unvalidated build toolchain would consume the pilot
window and contaminate the wall-clock measure P1 exists to produce.
**Binding disclosure inherited:** the pilot report must state that throughput
was measured on the cheapest-to-build slice and may under-estimate main-study
cost once Java/Go/Rust enter, and §7's final-n computation carries that
caveat.

**(b) OQ-11 — authoring vendor: balanced 3/2 by alternation.** One recorded
coin flip sets position 1; assignment alternates down the fixed task order.
Preserves D-006 symmetry as far as odd n permits; exactly one auditable random
element.

**(c) OQ-12 — k=2 repeats: seeded random draw of 2 of 5**, seed recorded
before use, faithful to §7's "random subsample."

**Selection executed 2026-07-21, before any P1 session** (script and output
preserved: `results/pilot/p1-brief.md`, provenance in
`results/pilot/raw/p1-selection.json`):

- Combined post-gate JS+TS pool: **39** (js 17 + ts 22) — unchanged from the
  2026-07-18 evidence table.
- **Rule self-check passed:** re-running the §8 rule from scratch returned
  `thlorenz__doctoc-328` as row 1 — P0's task — confirming both feed stability
  and correct rule application. P1 = rows 2–6.
- Coin flip → **position 1 = anthropic**; alternation gives anthropic 3 /
  openai 2.
- Repeat seed **1607515562** → **positions 3 and 4**, which fall on opposite
  authoring directions, so run-to-run variance is measured in both.

*Recorded covariate, not acted on:* position 3 is `thlorenz__doctoc-329` —
the **same repository** as P0's task (`doctoc-328`). The selection rule is
fixed and documented, so excluding it would be exactly the hand-picking §8
forbids. It is logged here and reported as a covariate; sessions are
independent, but two of the pilot's six cases sharing a repo is a fact the
write-up states rather than hides.

**Flagged, not blocking (→ OQ-13):** what a "k=2 repeat" repeats — the whole
task flow (author + A1 + A2 + B) or the review arms only — is unspecified in
D-021a and protocol §2. Must be ruled before the position-3 repeat runs, not
after.

## D-028 · 2026-07-21 · Ground-truth validity screen adopted at the corpus gate; replacement rule; D-023 not reopened mid-pilot

**Why (supervisor ruling on OQ-14, all three worker proposals adopted):** the
P1 task-1 baseline found a curated feed shipping FAIL_TO_PASS/PASS_TO_PASS
labels that do not survive execution (41 of 44 declared F2P tests already
passing at `base_commit`; P2P empty). D-010 committed to treating bundled-test
results as never-certifying-correct; this ruling operationalizes that stance
**at the corpus gate** rather than leaving it to downstream interpretation.

**(a) Screen adopted into intake, as proposed.** A task is admissible iff, at
`base_commit` with **only the test patch applied**, every declared F2P test is
**reported and fails**, and P2P is **non-empty** with every reported P2P test
**passing**. Rows failing the screen never enter the task set.

**(b) Replacement rule.** A screened-out task is replaced by the **next row in
the same fixed §8 ordering that passes the screen**. Every skipped row and its
screen-failure reason is recorded in the brief — §5's no-silent-task-swaps
requirement is met by the record, and §8's "fixed documented rule before any
review runs" survives intact because **the screen is blind to review
outcomes**: it executes before any patch is authored and cannot be influenced
by, or influence, any review result. A replacement **inherits its position's**
authoring-vendor assignment (D-027b) and k=2 flag (D-027c); the position is
fixed, only the task moves.

**(c) D-023 is NOT reopened mid-pilot.** The screen's **pass rate across the
post-gate pool is measured and reported**; corpus re-ratification is a **Step-3
input for the pilot report**, alongside the D-023 pre-registered fallback
(SWE-rebench) if usable supply warrants it. Deliberately not a pilot-blocking
question.

**(d) The finding is a first-class pilot-report result, not plumbing**
(supervisor directive). A curated, externally-provenanced feed exhibiting
F2P/P2P integrity failures at this rate is paper-relevant: it bears directly
on every SWE-bench-derived evaluation that trusts these labels without
executing them, and it corrects the OQ-9 evidence table, which credited this
feed with filtering invalid instances by running regression tests ×3.

*Screen-implementation note — recorded near-miss (supervisor-directed, same
convention as every other earned rule in this log: the incident that produced
the rule is preserved with it).* **The first screen implementation would have
retired a healthy task through a harness defect of the screen itself.**

- **What happened:** the first implementation assumed test results always land
  in `reports/*.json` and ignored each record's shipped `print_cmds` and
  `rebuild_cmds`. On `NVIDIA__NemoClaw-330` — whose results go to
  `vitest-results.json` in two directories — nothing reached the parser.
- **What it produced:** `parsed=0`, scored **FAIL**, i.e. "this task's ground
  truth is broken." Under D-028b that verdict retires the task and pulls in a
  replacement. The task was in fact **healthy**: the corrected screen returns
  **PASS with 303 tests parsed**, every F2P failing and every P2P passing.
- **What caught it:** the incoherence between `parsed=0` and a *declared* 300
  PASS_TO_PASS tests. A task may ship broken labels; it cannot ship zero
  tests. The two numbers cannot both be true, and the disagreement points at
  the measuring instrument rather than the thing measured.
- **Why the rule now exists structurally:** `parsed == 0` is classified
  **ERROR (harness/emit), never FAIL (ground truth)**, because only one of
  those two verdicts is permitted to retire a task. Enforced by
  `test_empty_parse_is_ERROR_not_FAIL` and
  `test_error_row_is_skipped_but_recorded_as_ERROR` in
  `tests/test_gt_screen.py`.
- **Standing consequence:** an ERROR verdict never retires a task and never
  triggers a replacement. It halts that task pending diagnosis, and the
  diagnosis is recorded. A screen that cannot measure a task is a fact about
  the screen.

*Original note, retained:* the first screen implementation assumed test results
always land in `reports/*.json` and ignored each record's shipped `print_cmds`
and `rebuild_cmds`. It returned `parsed=0` on `NVIDIA__NemoClaw-330` and
scored it FAIL — a **false positive that would have retired a healthy task and
triggered a spurious replacement.** Corrected flow uses the record's own
fields in order: `git apply <test_patch>` → `rebuild_cmds` → `test_cmds` →
`print_cmds`. A screen result of `parsed == 0` is now classified **ERROR
(harness/emit problem), never FAIL (ground truth)** — the two must not be
conflated, because only one of them retires a task. Task 1's FAIL is
unaffected: its `print_cmds` is exactly `cat reports/jest-results.json`, the
command the first implementation happened to run.

*Cost note:* the screen adds no subscription cost — it is container compute,
not a session. To protect the throughput measurement, pool-wide screening runs
**only while no session is running**; concurrent container load under amd64
emulation would inflate the very wall-clock figure P1 exists to measure.

## D-029 · 2026-07-21 · OQ-13 ruled: a k=2 repeat re-runs the review arms only

**Why (supervisor ruling, adopting the worker's reasoning verbatim):** the
estimand is **reviewer detection**; re-authoring yields a different defect and
hence a **second sample, not a repeat.**

**Mechanics:** a k=2 repeat holds the **original authored patch fixed** and
re-runs **A1/A2/B** against it. Cost ~3 sessions per repeat rather than ~4.

*Stated cost, for the limitations section:* **authoring run-to-run variance
goes unmeasured in the pilot.** If it is wanted later it is a separate line
item, never a relabelled repeat.

*Note on A1 under this ruling:* A1 is defined as in-session self-review inside
the authoring session, so re-running A1 against a fixed patch means resuming
that authoring session (P0 mechanics: `codex exec resume --last`, or the
Anthropic-side equivalent) rather than authoring anew. Where a resumed
in-session A1 is not reproducible for a given stack, that is recorded per
session rather than substituted with a fresh-session review — A1 and A2 differ
precisely in context, and silently swapping one for the other would collapse
the D-004 distinction the design exists to measure.

## D-030 · 2026-07-21 · OQ-15 ruled: `platform_infeasible` exclusion; ERROR handling unified; mixed-implementation screen results void

**Why (supervisor ruling on OQ-15 and on the worker's flagged asymmetry):**

**(a) `platform_infeasible` exclusion class adopted.** A task whose screen
ERROR is **diagnosed** as host/emulation incapacity is excluded and replaced
per D-028b, with the diagnosis recorded. The exclusion is recorded
**rig-relative**, never as a property of the task: the wording is
*"infeasible under this study's execution environment: amd64 emulation on
Apple Silicon."* The write-up inherits a **one-sentence limitation** to that
effect. Rationale: the task is not defective and would run elsewhere; claiming
otherwise would misreport the corpus.

**(b) ERROR handling unified into one rule** (ratifying the worker's
diagnosed/undiagnosed distinction and removing the asymmetry between selected
tasks and replacement candidates):

> A **diagnosed** ERROR — verified registry 404, verified illegal-instruction
> under emulation, or any other identified and recorded cause — may skip a
> replacement candidate or retire a selected task, with the reason recorded.
> An **undiagnosed** ERROR **always halts and escalates**, and never does
> either.

This preserves what D-028's ERROR class was built for: an unexplained failure
to measure is never allowed to look like a finding about the thing measured.
It only ever relaxes on evidence.

**(c) Position 4 unblocks** under (a): `can1357__oh-my-pi-489` is excluded as
`platform_infeasible` (bun binary → `Illegal instruction (core dumped)` under
amd64 emulation; diagnosed, verified) and replaced per D-028b.

**(d) The seeded repeat draw selected *positions*, not tasks** (D-027c), so
**position 4's replacement task inherits the k=2 repeat flag.** Recorded
explicitly because the alternative reading — repeat follows the excluded task
— would silently drop a repeat the draw pre-registered.

**(e) All final screen verdicts come from the single rewritten runner.**
Earlier results produced by the three superseded screen implementations are
**void for the record** and are retained only as the incident trail in D-028's
near-miss note. No verdict from a superseded implementation may be cited as
evidence.

**(f) Net-supply number and category overlaps** (label corruption, missing
images, platform-infeasible, and their intersections) are reported in the
pilot report as the **D-023 Step-3 input**, per D-028c. Not a pilot-blocking
question.

*Screen defect trail, for the record — three defects, all in the screen, none
in the corpus, none of which retired a task:* (1) results assumed at
`reports/*.json`, ignoring shipped `print_cmds` → `NVIDIA__NemoClaw-330`;
(2) non-login shell, so image PATH setup never applied and `bun` was not found
→ `can1357__oh-my-pi-489` (which then failed again for the genuine platform
reason once PATH was fixed); (3) commands joined with `" ; "`, destroying an
embedded heredoc → `GladysAssistant__Gladys-2504`. Final runner: each command
on its own line, login shell, test patch base64-encoded inline so stdin stays
free, build/test noise redirected by `exec` rather than a `{ }` group (which
also breaks heredocs). **The ERROR/FAIL separation is what made all three
recoverable; under the original single-verdict design each would have entered
the record as a corpus finding.**

## D-031 · 2026-07-21 · OQ-16 ruled: bundled-pass tasks enter neither sample; false-alarm construction gap is a Step-3 input; four standing procedures ratified

**(a) OQ-16 ruled: option (a).** A task whose authored patch passes the
bundled tests is an **authoring success**: it contributes **throughput data
only** and enters **neither** the defective sample nor the false-alarm sample.
Artifacts (sessions, transcripts, claims, evaluation result) are **retained**,
so the case can be admitted later without re-running anything if an augmented
suite is ever constructed for it.

*Rationale, recorded verbatim per supervisor directive:* scoring A1's and A2's
claims as false alarms **would contradict §6.4 — those claims may describe real
defects the bundled suite does not cover. A1's own output says as much: it
noted that none of its added tests would have caught its first finding.
Treating that as a false alarm would record a reviewer as wrong on the strength
of a test suite the design has already committed to not trusting for that
purpose.** Scoring reviewers wrong on a suite D-010 distrusts inverts the
design.

**(b) The false-alarm construction gap is a first-class Step-3 input**,
alongside the D-028/D-030 corpus findings. The pilot report states plainly:
**under the ratified corpus, the correct-patch sample has no construction
path** — §7 budgets an equal-sized correct sample, §6.4 requires augmented
tests for it, and no candidate feed in the OQ-9 table ships them. The report
names the options without choosing among them:

1. **Test augmentation** for a small correct sample;
2. **Descope false-alarm cost to secondary**, with catch-rate as the sole
   headline metric;
3. **Corpus re-ratification.**

**No decision mid-pilot.**

**Backlog rulings from the same checkpoint:**

**(c) The supervisor-side limit event counts toward D-021a's day-3
conditional.** Logged as **event 1**, with its supervisor-reported basis noted.
Rationale: the conditional protects against **capacity contention**, and
zero-consequence-this-time is **luck, not absence**. (Resolves the question the
worker declined to self-answer in `p1-log.md`.)

**(d) Transcript sourcing for D-018 scans is standing procedure.** A reviewer
CLI's summary output (`claude --output-format json`) carries only final text
and **no tool calls**, so it **cannot support a D-018 scan** — a verdict
computed from it would have nothing behind it. Scans run against the **full
session transcript**: the session JSONL for Claude Code, the `--json` event
stream for Codex. Encoded in `harness/compliance.py`.

**(e) A1's information asymmetry is promoted from limitations into the design
section's description of the A1 condition** (§4), in these words: **"A1 holds
strictly more information than A2/B by construction, making cross-condition
comparisons conservative against the cross-review hypothesis."** It is a
property of the condition, not a caveat about a run.

**(f) Sandbox flags are a standing launch rule.** **Authoring** arms run with
write access (`codex exec -s workspace-write`; the default read-only sandbox
silently produces no patch — P0 finding). **Review** arms run **read-only**
(`codex exec -s read-only`): a reviewer needs read access only, and write
capability would let it mutate the tree under evaluation. Encoded in
`harness/runner.py` alongside the CLI templates, with the rationale in-code.

**(g) Discarded-session accounting ratified.** **All consumed sessions count
against the D-021b ceiling**, including sessions discarded for worker error.
Counting only successful sessions would flatter the throughput figure P1 exists
to measure.

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
implementation detail. Draft v2 (with the D-016 cap) lives at
`harness/prompts/review-prompt.md`; the shotgun gap is closed per D-016; the
full text has been sent to the supervisor inline for sign-off on the exact
string. **RATIFIED 2026-07-16 (supervisor).** The prompt body is pinned
verbatim in design doc §8; any future edit to that string reopens
ratification, no exceptions. Reviewer compliance enforcement added as D-018.

*Correction note (2026-07-16):* a worker status message referenced the inline
prompt as "two turns back" — the pointer was wrong (it was three messages
back), so the supervisor's verification against the referenced location
failed. The inline send itself and the D-016 logging both occurred on
2026-07-15 (commit ac1dd43). Prompt re-sent inline 2026-07-16. Lesson logged:
status messages cite artifacts by commit/file, not by conversational position.

## OQ-4 · 2026-07-15 · Canary 4 pass criterion under REAL judges — **RULED 2026-07-16 (supervisor)**

The judge-bait fixture guarantees a panel split only with scripted mock judges;
real judges may legitimately agree. The D-015 binding acceptance item ("all
four canaries pass against the real backend") therefore needs a defined pass
criterion for canary 4 in real mode. **Proposal:** canary 4 passes iff it does
NOT score `catch` — i.e., either Band-3 escalation (judges split) or an agreed
`no_catch` (consistent with precedent P-001); an agreed `catch` is a failure of
the judge method and blocks acceptance. Awaiting ratification; mock-mode
expectation (must escalate to Band 3) unchanged.

**Ruling:** Real-mode pass set for canary 4 is exactly **{no_catch, pending_human}**.
`catch` fails — judges too lenient on a hedged, non-localized claim,
contradicting P-001. `false_alarm` fails — planted-bug task; per the boundary
rules that outcome indicates a pipeline defect. `unscorable` fails —
well-formed fixture; indicates extraction breakage. Additionally: because
real-judge agreement would leave Band 3 routing unexercised in real mode, the
mock-fixture routing test is **retained permanently** in the suite — marked as
such so it is never retired as redundant.

## OQ-5 · 2026-07-15 · ~~Google-family judge execution~~ — **RESOLVED by D-017**

## OQ-6 · 2026-07-16 · ~~Google-family judge~~ — **RESOLVED by D-019**

`gemini` CLI: `IneligibleTierError — no longer supported for Gemini Code
Assist for individuals; migrate to Antigravity` (probe 2026-07-16; also the
true cause of the earlier `--skip-trust` crash). Antigravity: not installed;
rejected for judging by D-017. Consequence: the real-backend canary run
cannot exercise any panel containing the Google family (all panels for
anthropic- or openai-authored claims). Options, supervisor to rule:
(a) reverse the D-017 no-Antigravity clause and use Antigravity CLI as the
Google judge (tools-disabled flags to be probed there), (b) drop to a
two-family judge pool — which breaks D-015 rotation for google-authored
claims and reduces anthropic/openai-authored panels below "exactly two
non-authoring" unless the design is amended, or (c) defer Google-family
judging to a machine/account where one of the paths works.

## OQ-7 · 2026-07-16 · ~~Codex judge tools-disable~~ — **RESOLVED by D-020**

Probes (2026-07-16, empty scratch dir, absolute-path read request): default
`codex exec` → read succeeded; `-c 'sandbox_permissions=[]'` → read succeeded;
sandbox modes (`read-only`/`workspace-write`) govern writes, not reads;
`--ephemeral`/`--ignore-user-config` reduce state, not capability. D-017
requires tools fully disabled for all judges. Options, supervisor to rule:
(a) accept the structural guarantee alone for the OpenAI judge (payload is
self-contained; claims carry only repo-relative paths that resolve nowhere in
the scratch dir; capability ≠ behavior), documented in provenance and the
paper's limitations; (b) wrap the codex judge in an OS-level sandbox
(macOS `sandbox-exec` deny-read profile) — probe-verifiable but deprecated
API, brittle across OS updates; (c) escalate to any newer codex flag the
vendor ships (re-probe at pilot).

## OQ-8 · 2026-07-18 · ~~Pilot scope + thresholds~~ — **RESOLVED by D-021**

§9's pilot is "one case end to end," but §7's throughput/variance measures
cannot come from n=1. The pilot-protocol proposal (`pilot-protocol.md` §2)
adds a P1 batch of **5 tasks (~20 sessions over 3–5 days, k=2 repeat on one
task)** after the single-case P0. Also proposed there and needing the same
ratification: the 0.7 sessions/week safety factor, the 50%-of-quota
feasibility threshold, and the 30% claim-format-failure escalation trigger.
Supervisor ratifies scope + thresholds (or amends) at pilot go/no-go.

## OQ-9 · 2026-07-18 · ~~Corpus source shortlist~~ — **RESOLVED by D-023** (evidence: `oq9-corpus-evidence.md`)

§3/D-010 fix the corpus source at pilot. Candidates to evaluate and present
with evidence at pilot start (recency-gate compliance vs all model cutoffs,
harvest tooling effort, hidden-test quality per UTBoost concerns):
(a) fresh tasks harvested with SWE-bench's open methodology from
repos passing an RQS-style screen (adapting SWE-PRBench §3.5 mitigations);
(b) any maintained continuously-refreshed SWE-bench-style feed whose task
dates postdate all cutoffs — to be verified live at pilot time, not assumed
from memory; (c) fallback: own harvest per (a) restricted to Python for
harness simplicity. Worker presents the evidence table; supervisor picks;
choice logged as a D-entry before P0.

**Process ratified 2026-07-18 (supervisor); decision rule pre-committed:** a
verified external continuously-refreshed feed **beats own-harvest** when both
pass the recency gate and UTBoost hardening — external task provenance
removes a researcher degree of freedom. Own-harvest (Python-restricted per
option c) is the fallback. "Verified live, not assumed from memory" stands as
written. The selection itself logs as a D-entry before P0.

## OQ-10 · 2026-07-21 · ~~P1 task-selection scope~~ — **RESOLVED by D-027a**

**Why this is open, not mechanical:** D-023c ratifies the corpus as
SWE-bench-Live/MultiLang; D-023**d** scopes the JS/TS restriction to **P0's**
task explicitly ("P0's task comes from the JS/TS slice"). P1's slice is
therefore undecided. The §8 selection rule itself (`select_first_n` —
`created_at` ASC, ties by `instance_id`, applied after filters,
`harness/corpus/intake.py`) is fixed and not in question; only the pool it is
applied to is.

**Live re-verification 2026-07-21 (metadata only, counts only — no task
identities retrieved, deliberately; see the blindness note below):** post-gate
(`created_at > 2026-03-01`) supply is unchanged from the 2026-07-18 evidence
table — js 17 + ts 22 = **39**; multilang total ≈322 (c 6, cpp 53, go 66,
js 17, rust 48, java 52, ts 22; the `csharp` split returned a
datasets-server error and is uncounted). Feed stable; both readings have
ample supply for 5 tasks.

**Options:**
(a) **Continue the JS/TS slice** — P1 takes the next rows after P0's in the
    same combined JS+TS ordering.
(b) **Full MultiLang pool** — apply the same rule across all splits, matching
    the ratified corpus and the main study's intended composition.

**Worker recommendation: (a), with a disclosure requirement.** RepoLaunch was
validated (D-023c) on a JS task only; Java/Go/Rust/C++ bring different build
toolchains, and P1's job is to measure throughput, not to debug toolchains —
a build failure in an unvalidated language would consume the pilot window and
contaminate the wall-clock measure it exists to produce. Homogeneity also
keeps a 5-task variance estimate interpretable. **The cost, stated plainly:**
a JS/TS-only pilot measures session cost on the cheapest-to-build slice, so
the throughput figure may under-estimate main-study cost once Java/Go/Rust
enter. If (a) is ruled, the pilot report must say so in those words, and §7's
final-n computation inherits the caveat. If the supervisor weights
main-study realism higher than pilot-window safety, (b) is the coherent
alternative and the worker will not argue further.

**Blindness note (why no task identities were fetched):** retrieving the
candidate rows under both readings *before* the rule is fixed would let the
selection rule be chosen with knowledge of which tasks each yields — the
precise researcher degree of freedom §8's "fixed documented rule before any
review runs" exists to remove. Counts are decision-relevant; identities are
not. Identities are pulled only after this ruling.

## OQ-11 · 2026-07-21 · ~~Authoring-vendor assignment across P1's 5 tasks~~ — **RESOLVED by D-027b**

**Why this is open:** P0 used a single recorded coin flip for one task. With
5 tasks there is no logged rule, and the choice is design-level: D-006 commits
to a **symmetric both-directions** design, which 5 independent coin flips can
defeat outright (a 5–0 or 4–1 draw has probability 12/32 ≈ 37.5%, leaving one
direction with ≤1 case and the paired A2-vs-B comparison — §7's protected
headline — effectively unmeasured in the pilot).

**Options:**
(a) **Independent coin flip per task** (P0 precedent extended).
(b) **Balanced 3/2 by alternation:** one recorded coin flip decides whether
    position 1 is anthropic- or openai-authored; assignment then alternates
    down the fixed task order, yielding 3/2.
(c) **Balanced 3/2 by seeded random draw** of which 3 positions go to the
    direction the flip selects.

**Worker recommendation: (b).** It preserves D-006 symmetry as far as an odd
n permits, keeps exactly one recorded random element (auditable, same shape as
P0's flip), and is deterministic thereafter. It also composes well with
OQ-12(a): under alternation, positions 1 and 2 are opposite directions, so a
repeat rule anchored at the head of the order measures run-to-run variance in
both directions for free. Note (b) is a *pilot* rule; the main study's
assignment at full n is a separate question not raised here.

## OQ-12 · 2026-07-21 · ~~Which two P1 tasks receive the k=2 repeats~~ — **RESOLVED by D-027c**

**Why this is open, and why it is time-critical:** D-021a pre-registers *that*
two tasks get k=2 (the second conditional on zero limit-hits by day 3) but not
*which*. "Pre-registered, not discretionary" is satisfiable only if the rule
is fixed **before task 1 runs** — choosing after seeing outcomes is the
degree of freedom the clause exists to close.

**A tension worth surfacing:** design doc §7 specifies repeats on a *random*
20% subsample; D-021a's pilot instance is 2 of 5 = 40% and says nothing about
randomness. A deterministic pilot rule is defensible but drifts from §7's
wording.

**Options:**
(a) **Positions 1 and 2** of the fixed task order. Simplest and fully
    auditable; the first repeat runs earliest, so the day-3 conditional on the
    second is comfortably evaluable; pairs with OQ-11(b) to cover both
    directions.
(b) **Seeded random draw of 2 of 5**, seed recorded in the P1 brief before any
    session. Faithful to §7's "random subsample"; immune to a
    "they repeated the convenient ones" objection. Cost: a draw of positions
    4 and 5 pushes both repeats late in the window.

**Worker recommendation: (b), seed recorded in the brief.** The pilot's job
includes rehearsing the main study's procedures, and §7's randomness is the
procedure. (a) is genuinely fine on the merits and better on scheduling; if
the supervisor prefers it, the pilot report should note the deviation from
§7's wording in one sentence.

## OQ-13 · 2026-07-21 · ~~What does a k=2 repeat re-run?~~ — **RESOLVED by D-029**

**Why this is open:** D-021a and protocol §2 say "k=2 repeats on two tasks"
without stating the unit. Two readings, materially different in both cost and
in what variance they measure:

(a) **Whole flow** — re-author the task and re-run A1/A2/B. Measures total
    end-to-end variance including authoring-patch variance (a different patch
    means a different defect, so the second run is arguably a different case).
    Cost: ~4 extra sessions per repeat, ~8 total.
(b) **Review arms only** — hold the authored patch fixed, re-run A1/A2/B
    against it. Isolates *reviewer* run-to-run variance, which is what the
    headline catch-rate metric is made of. Cost: ~3 extra sessions per repeat.

**Worker recommendation: (b).** §7 introduces repeats to measure "run-to-run
variance" of the thing being estimated, and the estimand is reviewer
detection, not authoring. Under (a) the two runs can carry *different defects*
in different locations, so the comparison is not a repeat of the same
measurement — it is a second sample. (b) also costs less against a 15/wk
ceiling. Cost of (b), stated: authoring variance goes unmeasured in the pilot;
if that is wanted it is a separate line item, not a relabelled repeat.
**Not blocking task 1** — needed before the position-3 repeat.

## OQ-14 · 2026-07-21 · ~~Ground-truth breakage in the corpus feed~~ — **RESOLVED by D-028**

**Status: P1 EXECUTION PAUSED.** No authoring or review session has been run
for any P1 task. Raised under protocol §5 ("evidence of ground-truth breakage
→ stop, log, escalate — touches §6").

**What was found.** Running the per-task step-2 baseline on P1 task 1
(`code-charity__youtube-3708`) — test patch applied at `base_commit`, no
authored patch — produced:

- **41 of its 44 declared `FAIL_TO_PASS` tests already PASS at base commit.**
  Only 3 actually fail. `PASS_TO_PASS` is **empty (0 tests)**.
- The suite parses to exactly 44 tests total, i.e. the feed has labelled the
  repository's **entire test suite** as FAIL_TO_PASS and left PASS_TO_PASS
  empty.

Evidence: `results/pilot/raw/p1-gt-screen/` (per-task baseline runs, parsed
against each task's own shipped `log_parser`).

**Why this is fatal for that task, not cosmetic.** The defective /
not-confirmed-defective determination is the study's ground truth (§6.4). With
41 already-green tests in the oracle, the standard fail→pass resolution
criterion is meaningless for this task, and a patch's verdict would turn on
tests unrelated to the reported bug.

**Scope — this is a feed-level property, not one bad row.** Metadata across
the 39 post-gate JS/TS rows shows the signature is recurrent:

| Signature | Count | Examples |
|---|---|---|
| `P2P == 0` with whole-suite-sized F2P | **3 of 39** | `code-charity__youtube-3708` (F2P 44), `Mintplex-Labs__anything-llm-5252` (F2P 105), `gsd-build__gsd-2-3258` (F2P 975) |
| Implausibly large F2P with non-zero P2P | ≥4 | `can1357__oh-my-pi-489` (**F2P 1527** — this is P1 task 4, a k=2 repeat position), `nodejs__undici-5000` (1115), `nodejs__undici-5011` (1471), `gsd-build__get-shit-done-2107` (615) |
| Healthy shape (small F2P, large P2P) | majority | `NVIDIA__NemoClaw-330` (3/300), `thlorenz__doctoc-329` (8/169), `aralroca__next-translate-1259` (1/146) |

The OQ-9 evidence table credited this feed with "invalid instances filtered by
running regression tests ×3." That filter demonstrably did not catch these
rows. The finding is a correction to the OQ-9 evidence, and belongs in the
write-up as one — the corpus was chosen partly on that filtering claim.

**P0 is unaffected — checked, not assumed.** `thlorenz__doctoc-328` has
F2P 2 / P2P 64, the healthy shape. P0's accepted result stands.

**What is running now (blind, no ruling needed):** the empirical screen is
executing against **all 5** P1 tasks. It is outcome-blind by construction — it
runs before any patch is authored, so it cannot be influenced by, or
influence, any review result.

**Decisions needed (design-level — not resolved here):**

1. **Adopt an empirical ground-truth validity screen into intake?** Proposed
   rule: a task is admissible iff, at `base_commit` with only the test patch
   applied, **every** F2P test is reported and fails, **and** P2P is non-empty
   and every reported P2P test passes. This is a §6.4 hardening addition and
   changes the corpus pipeline, so it is a D-entry, not a worker call.
2. **Replacement rule for screened-out tasks.** §5 forbids silent task swaps.
   Proposed: the next row in the same fixed §8 ordering that passes the
   screen, with every skipped row and its failure reason recorded in the brief
   — preserving "fixed documented rule before any review runs" because the
   screen is blind to review outcomes.
3. **Does the screen re-open the corpus choice (D-023)?** If a material
   fraction of the feed fails the screen, the post-gate *usable* supply drops
   below the 322 that justified selecting MultiLang over SWE-rebench.
   Recommendation: **no reversal now** — measure the screen's pass rate on the
   pilot's tasks, report it, and treat corpus re-ratification as a Step-3
   input rather than a pilot-blocking question.

**Worker recommendation:** adopt (1) and (2) as stated, hold (3) for the pilot
report. The screen costs one container run per task, which the per-task flow
already performs — near-zero added cost against the 15/wk ceiling.

## OQ-15 · 2026-07-21 · ~~Platform-infeasible tasks~~ — **RESOLVED by D-030**

**Why this is open, and why it is NOT a D-028 screen FAIL:** P1 position 4
(`can1357__oh-my-pi-489`) returned screen verdict **ERROR**, correctly — the
task's ground truth is *unknown*, not broken. Diagnosis:

- The task's `test_cmds`/`rebuild_cmds` drive **`bun`**. Under a non-login
  shell `bun` is not on PATH (first diagnosis); under `bash -lc` it resolves to
  `/root/.bun/bin/bun` and then dies with **`Illegal instruction (core
  dumped)`**.
- Cause: the pilot host is Apple Silicon (aarch64); task images are amd64 and
  run under emulation (recorded in HANDOFF and in `p1-log.md`). The emulation
  layer does not support the CPU instructions bun's binary requires.
- This is **not fixable in the screen or the harness.** It is a property of the
  host/emulation pair. D-028's ERROR class exists precisely so this does not
  masquerade as a ground-truth defect — and it worked: the task was not
  retired.

**Scope, measured across the 39 post-gate JS/TS pool** (runner inferred from
`test_cmds` + `rebuild_cmds`): vitest 12, other 13, tap 5, jest 5, **bun 4**.
The bun rows are **row 5 (`can1357__oh-my-pi-489`, P1 position 4), row 20
(`code-yeongyu__oh-my-openagent-3013`), row 31 (`reactjs__react-rails-1418`),
row 34 (`wxt-dev__wxt-2267`)** — ~10% of the pool, permanently unrunnable on
this host.

**The gap needing a ruling:** D-028b's replacement rule is triggered by screen
**FAIL**. D-028's standing consequence is that **ERROR never retires a task**.
Both are right as written, and together they leave position 4 blocked with no
defined exit. Options:

(a) **Add a `platform_infeasible` exclusion class** — a task whose ERROR is
    diagnosed as host/emulation incapacity (not a screen defect) is excluded
    and replaced per D-028b, with the diagnosis recorded. Keeps ERROR's
    never-retire-on-unknown property intact: the task is retired on a
    *diagnosed known cause*, not on an unexplained empty parse.
(b) **Run bun tasks on an amd64 host** (cloud VM or Rosetta-capable path) —
    preserves full corpus coverage, but introduces a *second execution
    environment* mid-pilot, which is a version/environment covariate the study
    would then have to carry and report per D-012.
(c) **Restrict the corpus to runner families verified on this host** — cleanest
    for the pilot, but it is a corpus-scope change (D-023 territory) and
    silently narrows generality.

**Worker recommendation: (a) for the pilot, and report the ~10% infeasible
rate as a finding.** It is the smallest change that unblocks P1, it keeps the
ERROR/FAIL separation honest, and the exclusion is *outcome-blind* exactly as
D-028's screen is — diagnosed before any patch exists. (b) is the right answer
for the main study if bun-family coverage matters, but adopting it mid-pilot
adds an environment covariate to a 5-task throughput sample that cannot absorb
it. (c) should not be chosen without reopening D-023, which ruling (c) of
D-028 deliberately deferred to Step 3.

**Pilot-report relevance:** "~10% of a curated post-gate slice is unrunnable on
a current-generation developer laptop" is a real finding about reproducibility
of SWE-bench-derived feeds on consumer hardware, and belongs alongside the
D-028 label-integrity finding rather than in a footnote.

**Status: P1 position 4 is BLOCKED pending this ruling.** Positions 1, 2, 3, 5
proceed. Position 4 also carries a k=2 repeat flag (D-027c), so its resolution
affects the repeat plan; the other repeat (position 3) is unaffected.

## OQ-16 · 2026-07-21 · ~~Position 1's authored patch RESOLVED the task~~ — **RESOLVED by D-031a**

**The situation.** P1 position 1 (`haraka__Haraka-3535`, anthropic-authored)
ran end to end. Hidden-test evaluation **after** all three reviews were
captured: **both F2P tests pass, zero P2P regressions** → the patch
**resolved** the task. Per §6.4 that is **not-confirmed-defective**, never
certified-correct. Reviews already captured: **A1 2 claims, A2 3 claims, B 0
claims** (all D-018 clean, all format-valid).

**The gap.** §5 Band 1 says: *"Any defect claim against a
**test-confirmed-correct** change is a false alarm."* But §6.4 and D-010 say a
bundled-test pass is **not-confirmed-defective, never certified-correct**, and
§6.4 requires the false-alarm sample to use *"the most-augmented test set
available."* This patch passed **bundled tests only** — no augmentation exists
for this feed (OQ-9 evidence: no candidate corpus ships UTBoost-hardened
suites). So the case satisfies neither branch cleanly: it is not a defect
case, and it is not a *test-confirmed-correct* case either.

Scoring A1's and A2's claims as **false alarms** would directly contradict
§6.4 — those claims may describe real defects the bundled suite does not
cover. A1's own output says as much: it noted that none of its added tests
would have caught its first finding. Treating that as a false alarm would
record a reviewer as wrong on the strength of a test suite the design has
already committed to not trusting for that purpose.

**Options:**

(a) **Authoring success → not a defect case.** The case contributes
    **throughput data only** (4 sessions, wall-clock, format/compliance
    counters) and enters **neither** the defective sample nor the false-alarm
    sample. Consistent with §7, which budgets ~150 authoring runs per
    direction precisely because many succeed and yield no defect.

(b) **Enter the false-alarm sample as-is**, scoring the 5 claims as false
    alarms. Maximizes usable cases; **contradicts §6.4** as argued above.

(c) **Hold the case pending augmented tests** — quarantine it, and admit it to
    the false-alarm sample only if an augmented suite is ever constructed for
    this task.

**Worker recommendation: (a), with (c) as the disposition of the artifacts** —
the case is recorded and its reviews retained, so if an augmented suite is
built later the case can be admitted without re-running anything. (b) should
be rejected: it would produce the study's first false-alarm numbers out of
exactly the evidence D-010 was written to distrust.

**Consequence that needs stating regardless of the ruling — this is the larger
finding.** The design targets *"an equal-sized correct sample for false
alarms"* (§7), and §6.4 requires augmented tests for it. **No candidate feed
ships augmented suites** (OQ-9 evidence table, all four candidates). So under
the current corpus the **false-alarm arm has no construction path**, and the
"clean-patch false alarm" canary validates the *pipeline*, not the *sample*.
This affects the §7 final-n computation, which budgets for that sample. It is
a Step-3 input alongside the D-028/D-030 corpus findings, and it is
**pilot-report material whichever way OQ-16 is ruled.**

**Status:** position 1 scoring is **BLOCKED** pending this ruling. Its
sessions, transcripts, evaluation result, and compliance verdicts are all
captured and committed — nothing needs re-running. **Positions 2–5 proceed**;
the question is about disposition of a completed case, not about whether to
keep running.

## OQ-17 · 2026-07-21 · Authored-patch capture is contaminated by setup and misses untracked files — position 2 blocked

**Status: position 2 BLOCKED before its review arms.** No reviewer has seen
this patch; nothing needs re-running except patch capture (the authoring
session's work is intact in the tree).

**Two defects in the worker's capture procedure, found on position 2:**

**(1) Setup noise dominates the "authored" patch.** `authored.patch` is
captured as `git diff` after the session. On position 2 that yields **2014
lines, of which 99.8% is `package-lock.json`** — regenerated by the worker's
own `npm install` during tree setup, **before** the session began. The agent's
actual change is **two lines**:

| file | change |
|---|---|
| `bin/lib/onboard.js` | +1 −1 |
| `scripts/setup.sh` | +1 −1 |
| `package-lock.json` | **+1594 −91 — worker setup artifact** |

The authoring agent explicitly disclaimed it: *"The pre-existing
`package-lock.json` modification was left untouched."*

Why this is experimentally material rather than cosmetic: A2 and B review
**the working tree**. Handing a reviewer a 1685-line lockfile diff with a
two-line security fix buried inside it changes the review task fundamentally —
it is a needle-in-haystack test, not the intended review. Position 1 escaped
this only by luck: `npm install` happened not to touch Haraka's lockfile.

**(2) Untracked files are silently dropped.** `git diff` reports only tracked
modifications. Position 2's agent created
**`test/credential-exposure.test.js` (23 lines, untracked)** — a regression
test central to its fix — and it is **absent from `authored.patch`**.
Reviewers would have reviewed a change the author did not write, and the
evaluation would have run without the author's own test.

**Proposed fix (mechanical, no design content):**

- Capture a **post-setup baseline commit** in each tree immediately after
  `npm install`/build and before the session, so the authored diff is exactly
  the session's own work. This is strictly better than blacklisting lockfiles:
  it is general, and it cannot be fooled by any other build artifact.
- Capture with `git add -N .` before `git diff`, so untracked files appear as
  new-file diffs.
- Re-capture position 2's patch from the existing tree by both rules — the
  session does not need re-running.
- Position 1's patch is **unaffected and needs no action**: its `git status`
  showed three tracked modifications and no untracked files, so its capture
  was complete and lockfile-free. Verified, not assumed.

**Supervisor call needed on one point only:** whether position 2's
re-captured patch may proceed to its review arms **as the same case**, or
whether the authoring session must be re-run under the corrected procedure.
Worker recommendation: **proceed as the same case.** The agent's work is
untouched by the capture bug; re-running would discard a valid authoring
session and consume ceiling for no methodological gain. If the supervisor
prefers a clean re-run for procedural purity, that is a defensible call and
costs one session.

## OQ-18 · 2026-07-21 · Authoring-step contamination: the agent web-searched and fetched the upstream fix PR

**What happened.** Position 2's authoring session (Codex) performed web
searches and **fetched the actual upstream pull request that fixes the task**:

- `site:github.com/NVIDIA/NemoClaw pull 191 provider-specific credential environment variable`
- `https://github.com/NVIDIA/NemoClaw/pull/191`

**The channel is the problem statement itself.** The feed's issue text ends
with:

> Related PRs that partially address this:
> - #148 — replace shell string interpolation with argv arrays
> - #191 — use provider-specific credential environment variable

So the task hands the author a **direct pointer to its own fix**, and the
authoring CLI has network access by default. The design's "problem statement
only — no hints, no test patch" (protocol §2, brief) is satisfied literally
while being defeated in substance.

**Why this needs a ruling rather than a shrug.** §6 states that contamination
of the *authoring* step "only shifts how many failures we harvest" — which is
true for **harvest yield**, and is the reason this is not an emergency. But it
is not harmless here:

1. It bears on **whether a defect is harvested at all** — an author handed the
   real fix is far less likely to produce the natural failure D-003 requires,
   and D-003's whole point is that defects must be *natural* and unknown to
   all parties.
2. Position 2's fix matches the upstream approach (`--credential
   NVIDIA_API_KEY`, env-var lookup form) — consistent with having read it.
3. It is **vendor-asymmetric in practice**: whether an authoring stack browses
   the web is a property of the stack and its defaults, so contamination
   exposure may differ systematically between the Anthropic and OpenAI arms —
   which lands on the D-006 symmetry commitment.

**Options:**

(a) **Accept and record** — treat as within §6's authoring-contamination
    tolerance, log per-session network use as a covariate, disclose.
(b) **Disable network access for authoring sessions** going forward, and
    record which positions ran with it. Changes the authoring condition
    mid-pilot (P0 and position 1 ran with network available).
(c) **Scrub fix-pointing references** (PR/commit links) from problem
    statements before authoring, leaving network access alone.
(d) (b) **and** (c).

**Worker recommendation: (a) for the pilot, (c) + measurement as the Step-3
proposal.** Changing the authoring condition mid-pilot breaks comparability
across the five positions for the sake of a sample too small to benefit;
scrubbing is the cleaner intervention because the *pointer* is the active
ingredient, and it can be applied uniformly from Step 3. Whichever is chosen,
**per-session network/tool use should be recorded from now on** — it is cheap,
and without it the covariate cannot be reconstructed later.

**Also needs a ruling: does position 2 remain in the batch?** Worker
recommendation: **yes**, recorded as network-contaminated, since excluding it
would be a post-hoc drop on a property the protocol never pre-registered — and
the D-028b replacement machinery is for screen failures, not for outcomes we
dislike.

**Status:** position 2 is blocked on OQ-17 regardless; this ruling determines
whether it proceeds contaminated-but-recorded, and what the other four
positions do.
