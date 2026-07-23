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

## D-032 · 2026-07-21 · D-021a amended: the second k=2 repeat's condition is session-consequence, not event-count

**Amendment (supervisor).** D-021a's condition for executing the **second**
k=2 repeat changes from:

> ~~"no limit-hit events have occurred by day 3"~~

to:

> **"no limit event that voided or deferred a session by day 3."**

**Rationale, on the record:** the conditional exists to protect the pilot
window from **genuine capacity contention**. Event 1 was a supervisor-side
session-window reset with **zero session consequence**, occurring during
deliberately atypical double-loading. Letting it eliminate a pre-registered
measurement would let a **formality overrule the condition's purpose**.

**Timing — explicitly noted, because it is what makes this an honest
clarification rather than results-contingent tinkering:** the amendment is
made **before day 3's evaluation** and **before either repeat has run**. No
repeat data exists to be influenced by it, and no outcome of the pilot is yet
known that could motivate it. (Position 1 is complete but is an authoring
success scored into neither sample per D-031a; positions 2–5 have no review
data at all.)

**Event 1 stays logged and counted in the §3 record either way** — the
amendment changes what the condition *tests*, not what the log *contains*.

*Standing consequence:* both k=2 repeats (positions 3 and 4) are expected to
execute unless a limit event actually voids or defers a session before day 3.

## D-033 · 2026-07-21 · Credential-fixture handling for security-fix tasks

**Why:** position 2's task is a credential-exposure fix (an API key visible in
the process list), so its patch, transcripts, and any fixtures the agent writes
are likely to contain credential-shaped strings — and every one of those
artifacts is published to a public repo.

**Ruled (supervisor, as proposed):** hits from
`scan_artifact_for_secrets` on these artifacts are **adjudicated per hit**, not
blanket-suppressed and not blanket-blocking. **Ambiguous hits go to the
supervisor before commit.** The **D-019 release gate remains blocking** — this
is a release gate, not hygiene, because the logs ship per D-012.

*Also ratified as standing practice:* recording the **base commit's own
context** when it bears on interpretation — e.g. position 2's base is
`chore(test): migrate root test suite from node:test to vitest`, which is
worth knowing before reading anything odd in that task's test behaviour.

## D-034 · 2026-07-22 · OQ-17 ruled: post-setup baseline commit is standing setup procedure

**Ruled (supervisor):** position 2 **proceeds as the same case**; the fix is
mechanical, no re-authoring — the authored work is intact, only diff
construction was wrong. The review artifact is the agent's **true change**: the
two-line fix **plus its untracked regression test**, per the D-031 precedent
(author-written tests stay in the reviewed diff, disclosed).

**Standing setup procedure for every task, from now on:**

1. Clone at `base_commit`, run `rebuild_cmds` / `npm install`.
2. **`git add -A && git commit` a post-setup baseline** — so every build
   artifact (lockfiles above all) is *behind* the diff HEAD.
3. Run the authoring session.
4. Capture the authored patch as `git add -N . && git diff <baseline>` — so
   **untracked files appear as new-file diffs** and **no setup artifact leaks
   into the patch**.

This is strictly better than blacklisting `package-lock.json`: general, and
unfoolable by any other build output.

**Near-miss, logged explicitly (same convention as the D-028/D-030 screen
defects — the incident that earns the rule is preserved with it):** on
position 2, `git diff` after the session produced **2014 lines, 99.8% of it a
`package-lock.json` regenerated by the worker's own `npm install` before the
session**, with the agent's actual two-line fix buried inside and its 23-line
regression test **omitted entirely** (untracked). **A2 and B reviewing that
diff would have been a garbage measurement** — a needle-in-haystack task, not
the intended review, against an artifact missing the author's own test.
**Position 1 escaped only by verified luck** (its `npm install` happened not to
touch Haraka's lockfile; checked, not assumed). The baseline-commit step
removes the luck.

## D-035 · 2026-07-22 · OQ-18 ruled: authoring contamination accepted-and-recorded for the pilot; fix-pointing scrub pre-registered for Step 3; per-session network logging starts now

**Ruled (supervisor):**

**(a) Pilot: accept and record.** Position 2's authoring session satisfied
"problem statement only" **literally** while the statement itself pointed at
the fix (the feed's issue text lists "Related PRs: #148, #191"; the agent
fetched PR #191). That is a **corpus property, not an agent violation** —
position 2 stays in the batch, recorded as network-contaminated.

**(b) Step 3 onward: pre-registered fix-pointing scrub.** Related-PR
references and equivalents (commit links, "fixed in", upstream-patch URLs) are
**scrubbed from problem statements before authoring** as a **uniformly
applied, documented input transformation** — logged as such so it is
transparent rather than silent. Not applied mid-pilot (would change the
authoring condition across positions).

**(c) Per-session network/tool-use logging starts now, all arms.** Recorded as
a covariate for two reasons: D-003's **unknown-to-all-parties** property must
be *audited*, not assumed; and browsing behaviour may differ systematically by
vendor stack, which lands on **D-006 symmetry**. Cheap now, unreconstructable
later.

**Binding blinding note (supervisor):** **do not prejudge position 2's oracle
outcome from the fetch.** The hidden tests still run **only after all arms
land**, and if the patch bundled-passes it enters **OQ-16's neither-sample
bucket (D-031a)** like any other authoring success. The fetch is logged as a
covariate; it does **not** pre-classify the case.

## D-036 · 2026-07-22 · D-018 adjudication (position 2 A2): commit-subject vitest hit is quotation, not invocation; scanner refinement logged

**Pre-registered D-025 procedure applied, before scoring.** Position 2's A2
(openai, fresh) scanned **ambiguous** on `\bvitest\b`. Automated exec-context
check ran; still ambiguous → human adjudication on the transcript excerpt,
**blind to what the review claimed** (adjudicated on the command list only; the
ground-truth score does not exist yet — hidden tests run after all arms land).

**Finding.** The sole `vitest` occurrence is **line 213 of the transcript —
the base commit's own subject line**, `4a1b74997 chore(test): migrate root
test suite from node:test to vitest (#653)`, surfaced by the agent's routine
`git log --oneline`. **No `vitest` command was executed.** Every command is
read-only inspection: `git status/diff/show/log`, `sed`, `rg`, `node --check`,
`openshell provider create --help`. **Adjudication: A2 is D-018 clean, not
excluded.** This is D-025's "quotation is not invocation" recurring through a
**new channel** — a base-commit subject line containing a test-runner name,
rather than P0's `AGENTS.md`/CI-YAML channel.

**Scanner refinement (logged per D-025.3 — refinements during P1 are logged,
frozen at pilot close).** The exec-context filter should treat a pattern hit as
**quotation** when it appears inside `git log`/`git show` commit-metadata
output (subject lines, `Author:`/`Date:` blocks). Recorded here now; the code
change is batched with the other pilot scanner refinements before the freeze,
not applied mid-session (changing the scanner between two arms of the same
batch would make the arms incomparable — same reasoning as the OQ-3 prompt
pin).

*Method note that paid off:* D-033's ratified practice of recording the base
commit's context ("base is the vitest migration") made this adjudication
immediate rather than an investigation — the very substring the scanner
flagged was already documented as expected.

## D-037 · 2026-07-22 · Secret gate refined for precision: bearer/basic requires a token-shaped value (D-033 adjudication)

**Adjudication (D-033 framework).** Position 2's five Codex transcripts tripped
the D-019 `auth-header` gate. All five hits are the same class:
`Authorization: Bearer $NVIDIA_API_KEY` / `$NEMOCLAW_PROBE_API_KEY` —
**shell-variable references, not secret values.** No real token exists (the
`SECRET_ENV_NAMES` exact-value check is clean; no token-shaped string is
present). They appear because the **task itself is a credential-exposure fix**,
so authors and reviewers quote `Bearer $VAR` header lines from the code under
review. **Adjudicated benign, all five.**

**Ruling (supervisor): refine the gate for precision, do not edit the
artifacts.** A narrowed transcript is a narrowed experimental record; a
narrowed *pattern* is a better instrument. The false-positive class **recurs
across the corpus's credential-handling tasks**, and a release gate that cries
wolf gets waved through — so precision is the security-preserving choice, not
the lax one.

**Change.** The `authorization: (bearer|basic)` branch now requires a
**token-shaped value**: ≥16 chars from the base64/token alphabet whose first
character is alphanumeric and is not preceded by a variable/placeholder sigil
(`$ { < % ' "`). A `$VARIABLE`, `${VAR}`, `%VAR%`, `<placeholder>`, or quoted
reference **passes**; a JWT, `sk-…`, or base64 `Basic` credential **still
fires**. Scope is the bearer/basic branch **only** (the exact ruling); the
Gemini-specific API-key header keeps its strict header-name match, and a
leaked judge-key **value** is caught independently by the env-value check
regardless of header context.

**Binding condition (supervisor): paired regression, both permanent.**
`tests/test_runner_corpus.py::test_auth_header_ignores_variable_references_but_still_flags_tokens`
asserts the benign `Bearer $VAR` excerpt (the exact P1 position-2 class)
**passes** and a token-shaped `Bearer <value>` (plus JWT and `Basic`) **still
flags**. A narrowed security control ships with proof of **retained
detection**, not merely reduced noise. Suite: **99 green**.

**Outcome.** The five held transcripts re-scanned **clean** under the refined
gate and are **released, committed, and pushed** — the artifacts are the
unedited experimental record, and the gate is more precise than before, not
weaker.

*Gate-scope note (recorded because implementing this ruling surfaced it):*
the release gate targets **pilot data artifacts** — transcripts, session logs,
results files, Band 3 cards — per its own docstring. It is **not** run as a
blocker over the harness source, its tests, or this decision log, which
**necessarily contain the very patterns the gate detects** (the regex literal;
the mandated token-shaped regression fixture; documentation of the control).
This is pre-existing and definitional, not new: the prior regex and its prior
test already contained gate-matching strings. The fixture tokens are
**synthetic**, never real secrets. This entry's prose is nonetheless worded to
avoid the literal header string so the decision log itself stays gate-clean.

*Scanner-freeze note:* this is a security-gate precision fix ruled and
implemented now (position 2 scoring was blocked on it), distinct from the
D-036 exec-context refinement which is batched for the pilot-close freeze.
Recorded so the freeze accounting stays honest about what changed mid-pilot
and why.

## D-038 · 2026-07-22 · Oracle test files are authoritative; standing evaluation procedure (with a self-correction)

**Why:** position 2's authoring agent independently created a regression test
at the **exact path the hidden `test_patch` also creates**
(`test/credential-exposure.test.js`). Applying the authored patch then the
test_patch failed (`TESTPATCH_RC=1`) — the oracle never ran — and a naive
reading would have mislabelled the case **CONFIRMED DEFECTIVE** when the true
cause was a **patch collision**, a harness error.

**Standing procedure (SWE-bench semantics).** The `test_patch` is
**authoritative**; the model must never supply oracle test files. For every
file the test_patch touches, reset it to base **before** applying test_patch,
using the idiom that handles both cases correctly:

```
git checkout HEAD -- '<f>' 2>/dev/null || rm -f '<f>'
```

— restore the base version if the file exists at `base_commit` (discarding the
model's edits to an oracle file), or remove it if the model created a net-new
colliding file. A `TESTPATCH_RC != 0` after this is a **HARNESS-ERROR verdict**
(unknown), never CONFIRMED DEFECTIVE — the same ERROR-vs-FAIL discipline as
D-030. Encoded in the evaluator (`results/pilot/raw/evaluate.py`).

**Self-correction, logged (the fix's own near-miss).** The first version of
this reset ran `git checkout -- f` **and** `rm -f f` unconditionally. On
position 1 — whose oracle file `test/transaction.js` **exists at base** (the
author modified it) — the unconditional `rm` **deleted a file the test_patch
needed to modify**, producing `TESTPATCH_RC=1` and a spurious "verdict CHANGED"
on a case that is in fact unchanged. Caught because a *resolved* case suddenly
reading *defective* under a procedure change is exactly the incoherence that
warrants re-checking the procedure, not the case. The conditional idiom above
is the fix; both positions then evaluated cleanly.

**Re-verification (both positions, corrected procedure):**
- **Position 1** (`haraka__Haraka-3535`): `TESTPATCH_RC=0`, 361 tests, both
  F2P pass, no P2P regression → **RESOLVED, authoring success (D-031a)** —
  **verdict unchanged** from its original evaluation. The original had by luck
  applied cleanly (author's test additions did not collide with the oracle's),
  so its verdict was already correct; this confirms it rather than revises it.
- **Position 2** (`NVIDIA__NemoClaw-330`): `TESTPATCH_RC=0`, 303 tests, **3/3
  F2P fail**, no P2P regression → **CONFIRMED DEFECTIVE.** Stable across runs.

*Ground-truth-noise observation (recorded, §6.4-relevant):* two runs of
position 2's evaluation differed by **one P2P test** (1 regression vs 0) while
the 3/3 F2P-fail verdict was identical both times. A single non-deterministic
P2P test is exactly the bundled-suite noise §6.4 and the k=2 repeats exist to
surface; the **defective verdict is robust to it**. Logged, not smoothed over.

## OQ-19 · 2026-07-22 · ~~First real scored case: mechanical catches, right line wrong reason~~ — **RESOLVED by D-039/D-040**

**Position 2 is the pilot's first CONFIRMED DEFECTIVE case.** Ground-truth
defect (from the gold patch): the credential is passed as `KEY=VALUE` to
`openshell --credential` (visible in `ps`), in **four locations** — three
`onboard.js` provider blocks (nvidia-nim 808–814, vllm-local 824–833,
ollama-local 844–853) and `runner.py` action_apply (209–216). The authored
patch fixed **only the nvidia-nim block** (plus a `setup.sh` file not in the
oracle), missing the other three — a natural incomplete fix.

**Band 1 mechanical result (±5, and stable across the ±1/±10 sweep):**

| arm | claims | Band 1 | matched on |
|---|---|---|---|
| A1 (self, openai) | 0 | **no_catch** | — |
| A2 (fresh, openai) | 3 | **catch** | `onboard.js:812` ∈ 808–814 |
| B (cross, claude) | 2 | **catch** | `onboard.js:811` ∈ 808–814 |

**The nuance worth a ruling.** Both catches are coordinate matches inside the
nvidia-nim region, but neither claim is clearly *about the planted defect*:

- **A2's** matching claim (`812`) is *"provider-creation errors are
  unconditionally ignored"* — an error-handling observation at the right line,
  not the credential exposure.
- **B's** matching claim (`811`) is *"passing bare `--credential
  NVIDIA_API_KEY` breaks credential setup"* — but the gold fix uses **exactly**
  the bare-name form, so B is arguing the *correct* approach is a bug. Right
  line; the claim's substance is backwards.
- **Neither** arm localized the actual incompleteness (the vllm/ollama/runner.py
  regions the author missed). A2 gestured *"still embedded elsewhere"* but at
  `537`/`setup.sh`, not the missed regions.

Under the mechanical design (D-005) both are catches, full stop — Band 1 does
not inspect reason, and Band 2 only receives **partially-localized** claims
(there are none here), so this case **generates no Band 2/3 traffic** and the
"right-line/wrong-reason" question is never adjudicated. That is the mechanical
metric behaving exactly as pre-registered — but it means the pilot's first
substantive reviewer disagreement is scored **catch/catch** without the
reader-actionability check the design reserves for Band 3.

**Question for the supervisor (design-level; not resolved here):** is this the
intended, disclosed behavior of the mechanical band — coordinate matches count
regardless of stated reason, and reader-actionability is validated **only** on
the Band-2-sampled subset — or should **fully-localized catches on defective
tasks also be eligible for the Band 3 audit sample**, so "right line, wrong
reason" is measurable rather than invisible? Worker leans **disclosed as-is for
the primary metric** (it is the reviewer-objection-proof mechanical rule D-005
was built to be) **plus** adding a small **pre-registered Band 3 audit of
mechanical catches** as a validation of the catch metric — symmetric with the
Band 2 human audit. No mid-pilot change either way; this is a Step-3 /
write-up input, surfaced now because the first real case is where it becomes
concrete.

## D-039 · 2026-07-22 · OQ-19 ruled: Band 3 audit of mechanical catches (symmetric with the Band 2 human audit)

**Ruled (supervisor), pre-registered now, effective immediately and applied
retroactively to position 2.**

**The primary metric is untouched.** Band 1's mechanical coordinate match stays
the primary catch/no-catch rule — D-005's objection-proofness is the design's
spine and is not being softened.

**Added: a Band 3 audit of mechanical catches**, symmetric with the existing
Band 2 human audit. A pre-registered sample of Band 1 **catch** verdicts is
rendered as cards and human-adjudicated against the **P-001 reader-actionability
standard**; the **agreement rate is reported alongside Band 2's κ** as the
validity check on the mechanical metric.

**Sampling rule (worker proposal, ratified):** **all** Band 1 catches during
the **pilot** (volume is small and every one is informative); a **fixed random
fraction** in the **main study** (fraction fixed in the design doc before the
main run, same discipline as the n=75 Band 2 sample). Cards use the same
blindness discipline as Band 2/Band 3 (role-only judge labels — N/A here since
these are mechanical, anonymized claim text, blindness-lint fail-closed).

**Framing, logged verbatim per supervisor directive:** *"'right line, wrong
reason' is invisible to localization scoring by design; the audit measures its
prevalence rather than assuming it away."*

**Position 2's two catches are catch-audit cases 1 and 2** (A2 `onboard.js:812`,
B `onboard.js:811`) and are carded in the first Band 3 batch. No mid-pilot
change to the primary metric; the audit is a validity layer over it.

## D-040 · 2026-07-22 · OQ-19 companion: D-038 accepted; incoherence heuristic added to the ledger

**Accepted (supervisor):** D-038 in full, **including the honest record that
the first fix attempt was itself wrong** (unconditional reset deleted a base
oracle file). The **incoherence heuristic** joins the ledger's catch list of
reusable checks:

> **A verdict that flips under a mere procedure change indicts the procedure,
> not the case.** When a previously-`RESOLVED` case reads `DEFECTIVE` (or vice
> versa) only because the harness changed, suspect the harness first.

This sits alongside the other earned checks now standing in the log:
- **ERROR ≠ FAIL** — a failure to *measure* is never a finding about the thing
  measured (D-028/D-030).
- **parsed==0 vs declared-N incoherence** — a task cannot have zero tests and N
  declared tests both (D-028 near-miss).
- **incoherence-under-procedure-change** — this entry (D-040).

The **flaky-P2P observation** (position 2: 1 vs 0 P2P regressions across two
runs, F2P verdict identical) is logged as **§6.4 bundled-suite noise**; the
**defective verdict is robust to it**.

## D-041 · 2026-07-22 · D-031f extended to Claude review arms: enforce read-only via disallowed edit tools

**Why (mechanics, extending the D-031f standing launch rule to the other
stack):** D-031f made review arms read-only on the OpenAI side (`codex exec -s
read-only`). The Claude review arms were launched with `--permission-mode
acceptEdits`, which **permits** file edits — the Claude analog of the very
`workspace-write` mistake D-031f exists to prevent. A reviewer that edits the
tree under review corrupts the reviewed artifact.

**Verified before changing anything (incoherence/least-surprise discipline):**
all six Claude/Codex review trees run so far (pos1 A2/B, pos2 A2/B, pos3 A2/B)
were compared **byte-for-byte** against their `authored.patch`. **All six are
identical — no reviewer edited anything.** The capability was unused, so the
completed arms **stand**; this is a latent-risk closure, not a
re-run.

**Standing rule going forward:** Claude review arms run with edit tools
disallowed — `claude -p ... --disallowedTools Edit Write NotebookEdit` — so
read-only is enforced by construction rather than by luck. Recorded next to the
sandbox rule in `harness/runner.py`. Authoring arms keep edit capability
(they must write the patch). The already-run arms' verified cleanliness is the
evidence that no result is affected.

## OQ-20 · 2026-07-22 · ~~k=2 repeat mechanics for the in-session A1 arm~~ — **RESOLVED by D-042**

**The gap D-029 anticipated, now concrete.** D-029 ruled a k=2 repeat re-runs
**review arms only** against the original authored patch, to measure reviewer
run-to-run variance. For **A2 and B** this is clean: each run 2 is a brand-new
fresh session on the same patch (A2 fresh same-vendor, B fresh cross-vendor).
For **A1 it is not clean:** A1 is *in-session self-review* — run 1 was produced
by **resuming the authoring session**. Resuming that same session a second time
for run 2 resumes it **as it now is** — already containing A1 run 1 — so
run-2's context strictly differs from run-1's (which resumed a session
containing only authoring). A1 run 2 is therefore **not a clean repeat of A1
run 1**; it is "self-review, having already just self-reviewed."

D-029 explicitly left this to per-session recording: *"Where a resumed
in-session A1 is not reproducible for a given stack, that is recorded per
session rather than substituted with a fresh-session review."*

**Options:**
(a) **Run A1 run 2 by resuming again, record the context-creep caveat.** The
    variance measured for A1 then includes the "already reviewed once" effect.
    Honest if labelled; A1's repeat is interpreted with the caveat.
(b) **Repeat only A2 and B; record A1 as not-cleanly-repeatable** for the
    in-session arm, per D-029's provision. A1 contributes one run; the variance
    estimate covers A2/B (the fresh arms, which are also where the headline
    A2-vs-B comparison lives).
(c) **Fork the authoring session before A1 run 1** so run 2 resumes from the
    same pre-review state — **not available**: Claude Code sessions are
    append-only; there is no mid-session fork on this stack.

**Worker recommendation: (b).** The repeat exists to quantify reviewer
run-to-run variance, and the arms that variance most affects — and that carry
the protected A2-vs-B headline — are the **fresh** arms, which repeat cleanly.
A1's in-session definition makes a clean repeat impossible on this stack (c is
out), and (a) measures a subtly different quantity ("review-again variance")
under the same label. (b) repeats what can be honestly repeated and records the
A1 limitation explicitly — which is exactly what D-029 provided for. If the
supervisor prefers (a), the A1 run-2 record will carry the context-creep caveat
in-line.

**Status:** position 3 run 1 is complete (A1 2 claims, A2 0, B 1 — A1 and B
both flag `lib/transform.js:43`). Run 2 of **A2 and B** is unambiguous and
proceeds now under either ruling; only **A1 run 2** waits on this.

## D-042 · 2026-07-22 · OQ-20 ruled: A1 is structurally not-cleanly-repeatable (option b)

**Ruled (supervisor): option (b).** The A2/B k=2 repeats stand as cleanly
executed. A1 is **recorded as not-cleanly-repeatable** for the in-session
condition.

**Structural reason, logged verbatim per directive:** *an append-only session
cannot re-review without contamination from its own first review, so a
"repeat" of A1 is not the same measurement. This is a property of the A1
condition (consistent with its information-asymmetry framing in the design
section — A1 is constitutively unique per task), not a gap in execution.*

**Do not resume-with-caveat** — a caveated non-repeat is worse than an honest
structural exclusion. The variance table's **A1 run-2 cell records `n/a
(structural)`**, not a value and not a caveated value.

## D-043 · 2026-07-22 · Band 3 batch p1-b1 ruled: both catches → no_catch; catch-audit taxonomy established

**Rulings ingested** (`results/band3/band3-rulings.json`;
computation `results/band3/catch-audit-p1-b1.json`). Both position-2 mechanical
catches ruled **no_catch** by human audit against P-001 reader-actionability.
**Catch-audit agreement rate for p1-b1: 0/2 (0%)** — Band 1 said catch, the
human audit said no_catch on both. Tiny batch; reported as-is, alongside Band
2's κ, as the validity check on the mechanical metric (D-039). The result
**empirically confirms** the OQ-19 concern: coordinate matching can be
semantically empty.

**Standing precedent taxonomy (append-only, from the rulings' notes):**
- **P-002 · coincidental localization** — a semantically unrelated claim on a
  coincidentally-correct line. (`NemoClaw-330/A2`: claim describes
  error-swallowing; defect is credential exposure; same line by coincidence. A
  reader following it would not find the leak.)
- **P-003 · inverted claim** — right location and topic, but **asserting the
  correct fix is the bug**; counter-productive to follow, not merely
  non-actionable. (`NemoClaw-330/B`: claims the correct bare-env-var fix is
  itself broken; a reader could revert the right approach and reintroduce the
  leak.)

**Card design ratified: single-claim per catch.** Standing rationale: the
audit's unit is **the catch**, and P-001 rules on **claims**; carding the
specific claim that earned the mechanical catch is the faithful unit.

## D-044 · 2026-07-22 · Process notes + D-041 acceptance

**(a) D-041 accepted.** The `acceptEdits` catch, the byte-for-byte verification
that completed review arms did not edit their trees (so completed work stands),
and the tool-disallow enforcement going forward. **Filed beside the codex
`workspace-write` incident (D-031f) as the same failure class — a review arm
granted write capability — caught independently on the second stack.** Two
stacks, one lesson: review arms are read-only by construction, never by launch
convention.

**(b) Audit-blinding pre-registration for Step 3 (process note, not a
mid-pilot change).** The pilot's Band 3 audit rulings were made by a supervisor
**exposed to run context via checkpoints**. For the main study, pre-register
that **audit cards are ruled before reading any arm analysis** — the card-alone
discipline (D-014) extended to the reviewer's own analysis, closing the
context-exposure path the pilot necessarily had.

**(c) Write-up methods note (capture verbatim).** The supervisor's step-back —
*"why does the busy-programmer [reader-actionability] standard matter if the
goal is comparing vendors?"* → the **catch-definition dependency chain**: the
vendor comparison is only as meaningful as the definition of "catch"; if a
catch can be semantically empty (P-002/P-003), the headline metric measures
coordinate coincidence, not detection; the reader-actionability standard is
what ties "catch" to the lived claim the study is about. This is the methods
section's plain-language justification for the audit.

## OQ-21 · 2026-07-22 · [Step 3] Extend Band 2 judge panel to mechanically-caught claims → `semantic_catch` secondary verdict

**Logged for Step 3; no mid-pilot change.** Proposal: extend Band 2's blinded
judge panel to **also** evaluate mechanically-caught claims — semantic match of
the claim against the answer-key annotation, under the **same rotation and
anonymization** rules (D-013/D-015) — yielding a **`semantic_catch`** secondary
verdict **alongside the untouched Band 1 primary**.

**Rationale:** p1-b1 demonstrated (0/2) that Band 1 catches can be semantically
empty. An automated semantic layer over **all** catches, **calibrated by the
Band 3 human audit and its reported agreement rate**, converts the audit from a
spot-check into the **calibration for a full secondary metric** — the mechanical
primary stays objection-proof (D-005), and the secondary reports how many
catches are semantically real.

**Blocking check before adoption:** projected **judge-call volume** for
"all catches, both non-authoring families each" must be checked against
**D-019's free-tier Gemini quota** measurement — a semantic layer over every
catch multiplies judge calls and may breach the 50% quota-feasibility threshold
(D-021c). Quantify at Step 3 sizing before committing.

## D-045 · 2026-07-22 · Evaluation OOM near-miss: `parsed==0` is HARNESS-ERROR; memory headroom standardized

**A false CONFIRMED DEFECTIVE, caught.** Position 3's first oracle evaluation
returned `parsed==0` with all 8 F2P `MISSING`, and the evaluator labelled it
**CONFIRMED DEFECTIVE**. It is not. The tap runner was **`Killed` (OOM)** under
amd64 emulation — the colima VM has only **2 GiB** — after emitting
`TAP version 14 / 1..9`, writing a **0-byte** results file. Re-run with
container memory headroom (`--memory=6g`, lifting the cgroup cap): **177 tests,
all 8 F2P pass, no P2P regression → RESOLVED, authoring success (D-031a).**

**Two fixes:**
1. **`evaluate.py` verdict logic corrected.** `parsed==0` is now a
   **HARNESS-ERROR** ("failure to measure — verdict UNKNOWN, not defective"),
   never CONFIRMED DEFECTIVE — the same ERROR-vs-FAIL discipline as D-030/D-038.
   The prior logic conflated "test_patch applied but nothing parsed" with
   "patch is defective"; a runner Killed before writing results parses to
   nothing and says nothing about the patch.
2. **Memory headroom standard.** All oracle evaluations run with `--memory=6g`.
   The oracle eval is **not a session**, so this does not touch the throughput
   wall-clock measurement (which is measured on the CLI review/authoring
   sessions only). Positions 1 and 2 had produced valid parses without it
   (they did not OOM), so their verdicts stand; headroom makes evaluation
   reliable rather than luck-of-the-memory-state.

**Caught by the incoherence heuristic (D-040), again:** a task that **passed
the ground-truth screen** (its F2P fail and P2P pass at base) cannot coherently
read "defective with zero parsed tests" — a 0-parse on a screen-PASS task
indicts the measurement, not the patch. That tell is what prompted the
diagnosis instead of recording the false verdict.

**AMENDMENT (2026-07-23, supervisor ruling): the `--memory=6g` remedy was
partly cosmetic; the real fix is VM-level memory.** A `--memory=6g` container
cap **cannot be honored on a 1.9 GiB colima VM** — Docker cannot hand out
memory the VM does not have. So no run since that flag was added ever received
6 GiB; the runs that succeeded did so by **fitting within 1.9 GiB**, not by
headroom. The **actual** safeguard against a false verdict is the
**`parsed==0` → HARNESS-ERROR** rule plus the **completeness check
(`not_reported == 0`)** — a run either completes and parses fully, or it is
caught as ERROR. The genuine remedy, applied at the next container-job
boundary: **the colima VM was resized 2 GiB → 8 GiB** (host has the RAM), so
evaluations are *reliably* within memory rather than luck-of-fit.

**Checked-not-assumed sweep — every verdict recorded since the `6g` flag,
stated per-verdict (not assumed):**

| verdict (since 6g flag) | parsed / not_reported | fit or headroom? | stands? |
|---|---|---|---|
| **pos3 oracle → RESOLVED** (D-045) | 177 parsed, 0 F2P missing, 8/8 pass | **fit within 1.9 GiB** (complete run; 177 = screen's count) | **stands** |
| **row 11 `vueuse` → FAIL** | 1378 parsed, 0 not_reported | **fit** (complete; 1 F2P passes at base = real GT fail) | **stands** |
| **row 12 `gsd-2-2643` → FAIL** | 4573 parsed, 0 not_reported | **fit** (complete; 2 F2P pass at base) | **stands** |
| **row 14 `AionUi-1818` → FAIL** | 1755 parsed, P2P 0 missing, 11 F2P genuinely absent | **fit** (complete; 11 missing are absent test *names*, not OOM — P2P fully reported) | **stands** |
| **row 15 `bruno-7620` → ERROR** | **0 parsed** | **did NOT fit** (OOM under 1.9 GiB) | **re-verified under 8 GiB** (in progress at ruling time) |

**Conclusion: "fit, verdicts stand" for all four completed verdicts** — each
completed with `not_reported == 0`, which is the actual proof of a valid run,
independent of the (unhonorable) memory flag. Only `bruno` (the sole
`parsed==0`) required real headroom and is re-screened at 8 GiB; its 1.9 GiB
ERROR is discarded as an OOM non-result, not a verdict. The `--memory=6g` flag
is retained (harmless, and correct once a host/VM can honor it) but is **not**
the safeguard — the ERROR-on-`parsed==0` discipline and VM sizing are.

**Environment-reliability finding (pilot-report material):** the evaluation
harness OOMs non-deterministically at 2 GiB under emulation on Node test suites
run in parallel. Recorded alongside the platform-infeasibility (D-030) and
label-integrity (D-028) findings as a **reproducibility caveat for
SWE-bench-derived evaluation on consumer hardware.**

## D-046 · 2026-07-22 · Position 3 is an authoring success; the k=2 repeat landed on a non-defective task

**Position 3 (`thlorenz__doctoc-329`, anthropic): RESOLVED → authoring success
(D-031a)** — throughput data only, enters neither the defective nor the
false-alarm sample; reviews retained. **Second authoring success in three
completed positions** (pos1 success, pos2 defective, pos3 success); running
defect yield **1/3** — a §7 sizing input (authoring runs per harvested defect).

**Consequence for the k=2 repeat (recorded, not corrected):** position 3 was a
repeat position (D-027c), but its patch **resolved**, so there is **no defect
to catch** and the repeat measures **claim-count / verbosity run-to-run
variance, not catch-rate variance.** The observed variance stands as data:

| arm | run 1 | run 2 |
|---|---|---|
| A1 (self) | 2 claims (`transform-html.js:77`, `transform.js:43`) | **n/a (structural, D-042)** |
| A2 (fresh same-vendor) | **0 claims** | **2 claims** (`transform.js:112`, `transform.js:43`) |
| B (cross-vendor) | 1 claim (`transform.js:43`) | 1 claim (`transform.js:43`) |

Cross-vendor B was claim-stable across runs; fresh same-vendor A2 was not (0→2).
Catch-rate variance from the repeats depends on **position 4** landing a
defect; if both repeat positions resolve, the pilot measures verbosity variance
but not catch-rate variance, and that is stated in the report rather than
presented as if catch-rate variance were measured.

## D-047 · 2026-07-22 · The incoherence heuristic generalized to a design principle (third save)

**Third save recorded.** The incoherence heuristic (D-040) has now caught a
false verdict at **each pipeline stage**:

1. **Intake** — `parsed==0` vs a declared 300 P2P tests: a task cannot have
   zero tests and 300 declared tests both (D-028 near-miss, `NemoClaw-330`).
2. **Selection/procedure** — a `RESOLVED` case reading `DEFECTIVE` only because
   the harness changed: the procedure is indicted, not the case (D-040, pos1
   under the first oracle-reset attempt).
3. **Evaluation** — a **screen-PASS** task reading `DEFECTIVE` with `parsed==0`:
   a task whose F2P demonstrably fail and P2P pass at base cannot coherently be
   defective-with-nothing-parsed; the measurement is indicted (D-045, pos3 OOM).

**Generalization for the write-up — present as a design principle, not three
incidents.** *Every pipeline stage carries a coherence check against
upstream-verified facts.* Each stage (intake → selection → evaluation →
scoring) has, upstream of it, facts already verified (declared test counts, a
prior verdict, a screen result). Before a stage's output is trusted, it is
checked for coherence against those facts; an output that contradicts an
upstream-verified fact indicts the stage's **measurement**, not the underlying
task — and triggers diagnosis rather than recording. This converted three
would-be false verdicts (two defective, one procedural) into diagnosed harness
bugs. It is the operational form of the ERROR-vs-FAIL discipline (D-030): a
failure to measure coherently is never a finding about the thing measured.

## D-048 · 2026-07-23 · `platform_infeasible (time)` — a D-030a sub-category for practically-unbounded runtime under emulation

**Ruled in advance (supervisor).** Extends D-030's `platform_infeasible`
diagnosed-exclusion class with a second sub-category.

**Row 13 of the position-4 replacement walk, `gsd-build__gsd-2-2738`, is
excluded as `platform_infeasible (time)`.** Mechanism recorded exactly: its
`test_cmds` run Node with **`--experimental-test-isolation=process`** across
**4,296 PASS_TO_PASS tests** — **one emulated process spawned per test** under
amd64 emulation on Apple Silicon. This is impractical **by construction**, not
merely slow: process-per-test × thousands × emulation is unbounded practical
runtime (observed: one container ran ~1 h without completing, `docker top`
unresponsive, then killed). The container was killed at the boundary; the
orphan check confirmed no sweb container survived.

**The two sub-categories of D-030a `platform_infeasible`:**
- **hard-infeasible (D-030 original)** — the binary cannot execute at all
  (`bun` → `Illegal instruction (core dumped)`; the CPU/emulation lacks the
  required instructions).
- **time-infeasible (this entry)** — the binary runs, but practical runtime is
  unbounded under emulation (process-per-test isolation × thousands of tests).

Both retire on a **diagnosed** cause (never an undiagnosed halt — D-030b), both
are **rig-relative** (a property of *this study's execution environment: amd64
emulation on Apple Silicon*, D-030a), and **both are explicitly rerunnable on
native amd64 hardware** — recorded here for the **version-pinned API/native
replication story** (design §7): the replication host runs these natively, so
neither sub-category is a property of the task or a permanent corpus loss.

**Walk consequence:** rows 11 (`vueuse`, FAIL — complete run, 1378 parsed) and
12 (`gsd-2-2643`, FAIL) precede it; row 13 now skipped on diagnosis. Selection
continues at rows 14–15 (screening at ruling time).

## OQ-22 · 2026-07-23 · ~~Position-4 replacement supply exhausted through row 15~~ — **RESOLVED by D-049**

**Held per supervisor ruling** ("if both [14/15] fail, surface the
shrinking-supply picture and hold"). Rows 11–15 yielded **zero PASS**:

| row | task | verdict |
|---|---|---|
| 11 | `vueuse-5336` | FAIL (ground-truth; 1 F2P passes at base; complete run, 1378 parsed) |
| 12 | `gsd-2-2643` | FAIL (ground-truth; 2 F2P pass at base; complete, 4573 parsed) |
| 13 | `gsd-2-2738` | **platform_infeasible (time)** (D-048) |
| 14 | `AionUi-1818` | FAIL (ground-truth; 2 F2P pass + 11 F2P absent names; complete, 1755 parsed) |
| 15 | `bruno-7620` | **ERROR — diagnosed `eval_harness_failure`** (see below) |

**bruno-7620 diagnosis (still `parsed=0` under the 8 GiB VM — not OOM):** its
shipped `test_cmds` (`npm test --workspaces --if-present -- --verbose`) **fails
to execute any tests.** Two failure modes in the raw output: `jest: not found`
in several workspaces, and `node: bad option: --verbose` in others (their test
scripts are `node … $(npx which jest) --verbose`; when `npx which jest` returns
empty, `--verbose` falls through to `node`). Root cause: **jest is not resolved
after the rebuild chain.** No tests run → `parsed=0`. **Diagnosed** (so not an
undiagnosed halt), but its skip *category* needs a ruling: the `node: bad
option` failure is a **task-shipping incompatibility** (independent of
platform); the `jest: not found` could be rig-relative (build flakiness under
emulation) or task-intrinsic (missing/hoisted dep). Worker did **not** hand-fix
the test command — that would modify the oracle.

**Full post-gate screen tally, rows 2–15 (14 of 39 screened):**

- **PASS = 4** (rows 3,4,6,10 → filled positions 1,2,3,5)
- FAIL (ground-truth) = 5 · image_missing = 2 · platform_infeasible = 2 · eval_harness_failure = 1
- **Usable (PASS) rate ≈ 29 % (4/14).**

**Position 4 still needs its 5th PASS, from rows 16–39 (24 unscreened).**

**Why this is a genuine escalation, not just "keep walking":**
1. **The measured usable rate (~29%) is far below what the OQ-9 evidence table
   implied** — it credited SWE-bench-Live/MultiLang with "invalid instances
   filtered by running regression tests ×3." The pilot is measuring a very
   different number. This is first-class **D-023 Step-3 re-ratification input**,
   sharper now than at OQ-14.
2. **Continuing to row 16+ costs real container time** (each large TS suite is
   many minutes under emulation; row 13 alone burned ~1 h before diagnosis),
   and may hit more infeasible/broken rows before a PASS.
3. The bruno classification (new `eval_harness_failure` category) wants a
   ruling before it is applied as a standing diagnosed-skip.

**Options for the supervisor:**
(a) **Continue the walk to row 16+** under the standing green light until the
    next PASS fills position 4 (worker proceeds autonomously, batching any new
    diagnosed-skips, surfacing only a fresh escalation).
(b) **Pause P1 at n=4 usable positions** (pos1/2/3/5 complete or in flight) and
    treat position 4 as unfillable-within-budget — report P1 on 4 tasks with
    the supply finding as the headline corpus result.
(c) **Re-ratify the corpus now** (D-023 fallback to SWE-rebench, or the §7
    options) rather than spend more of the window walking a 29%-usable feed.

**Worker recommendation: (a) with a cap** — continue the walk, but **cap it at
screening through row ~22** (a further ~7 rows); if no PASS fills position 4 by
then, escalate to (b)/(c) rather than walking the full remaining 24. This
bounds the cost while giving position 4 a fair chance, and every skipped row is
recorded. The bruno `eval_harness_failure` category is adopted provisionally
for the walk (diagnosed, recorded) pending the supervisor's category ruling.

**Status: HELD. No further screening or sessions until the supervisor picks
(a)/(b)/(c).** Positions 1–3 complete, position 5 task selected (screened PASS,
not yet run). P1 total: 18 sessions + 1 discarded.

## D-049 · 2026-07-23 · OQ-22 ruled: capped walk with resequencing; eval_harness_failure adopted; oracle-repair boundary

**Ruled (supervisor): option (a), capped at row 22, with resequencing.**

**(a) Resequence — position 5 before the row-16–22 screen.** Position 5 is
already screened and selected; **sessions are the scarce resource** against both
the D-021b ceiling and the calendar, so position 5's full flow runs **first**,
not idling behind container work. The row-16–22 screen runs **after position 5
completes, or in the supervisor's offline windows — never alongside sessions**
(the D-045/measurement contention rule).

**(b) Cap and stop-rule.** The replacement walk screens **through row 22**
(~7 more rows). If a PASS lands, **position 4 runs its full flow with the k=2
repeat** (D-030d position-inheritance). If rows 16–22 yield **zero PASS**:
**do not grind rows 23–39.** P1 **closes at n=4 usable positions**
(pos1/2/3/5); **position 4 is recorded as unfillable under measured supply**;
the **second k=2 repeat is recorded as unmeasured, with the reason**; and the
**supply finding graduates from a Step-3 input to the pilot's headline corpus
result.**

**(c) Corpus re-ratification stays a Hanoi decision** (D-028c): with the pilot
report open, not a mid-pilot swerve. Option (c) from OQ-22 is **not** taken now.

**(d) `eval_harness_failure` adopted as a standing diagnosed-skip category**,
provisional for the walk, **classified precisely: a FEED DEFECT** — the shipped
test command runs no tests (jest absent, node flags invalid) — **distinct from
`platform_infeasible`'s rig-relative class.** It is therefore the **fifth
distinct corpus-integrity failure mode**, and the **fourth attributable to the
feed itself.**

**(e) Oracle-repair boundary, logged (supervisor directive):** the worker's
refusal to hand-fix bruno's test command was correct — **repairing the oracle
is authoring the benchmark.** Standing boundary: the harness runs each task's
**shipped** test command verbatim; a command that does not execute is a
**recorded finding about the feed**, never something the worker patches into
working order. Patching it would manufacture a passing task and destroy the
task's status as an independent, externally-provenanced artifact.

## Findings taxonomy — corpus-integrity failure modes (updated per D-049d)

Standing catalog for the pilot report. **Five distinct modes; four
feed-attributable, one rig-relative:**

1. **Label integrity — whole-suite-as-F2P** (feed): the entire suite labelled
   FAIL_TO_PASS, P2P empty (`youtube-3708`; D-028).
2. **Label integrity — phantom F2P names** (feed): declared F2P test names exist
   nowhere in the suite after the test_patch applies (`Gladys-2504`; D-028).
3. **Label integrity — F2P-passes-at-base** (feed): declared F2P tests already
   pass at base, so there is no failing oracle (`vueuse-5336`, `gsd-2-2643`,
   `AionUi-1818`; the general D-028 screen FAIL).
4. **Missing image** (feed): the declared `docker_image` returns a registry 404
   (`anything-llm-5252`, `mongoose-16153`; D-030 `image_missing`).
5. **Eval-harness failure** (feed): the shipped test command runs no tests
   (`bruno-7620`: jest absent / invalid node flags; D-049 `eval_harness_failure`).

*Rig-relative (NOT feed defects; rerunnable on native amd64 — the replication
story):* **platform_infeasible** — hard (`oh-my-pi-489` bun crash) and time
(`gsd-2-2738` process-per-test × emulation); D-030/D-048.

*(Modes 1–3 are all "label integrity" sub-types but are listed separately
because each is a distinct diagnostic signature and the pilot report reports
their individual prevalence.)*

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

## OQ-17 · 2026-07-21 · ~~Authored-patch capture contaminated by setup~~ — **RESOLVED by D-034**

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

## OQ-18 · 2026-07-21 · ~~Authoring-step contamination: agent fetched the upstream fix PR~~ — **RESOLVED by D-035**

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
