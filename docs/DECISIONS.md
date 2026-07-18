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
2026-07-15 (commit 608ec8b). Prompt re-sent inline 2026-07-16. Lesson logged:
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

## OQ-9 · 2026-07-18 · Corpus source shortlist for pilot ratification

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
