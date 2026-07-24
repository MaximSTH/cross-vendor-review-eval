---
name: step3-preregistration
description: Step-3 (Sequential-B) pre-registration PACKAGE — draft for supervisor ratification. Group-sequential stopping design, corpus expansion plan with live-verified counts (2026-07-24), and the non-deferred queue items (ceiling re-declaration, repeat-on-defective, scanner freeze, problem-statement scrub, config-introspection provenance). NOTHING here executes until ratified; every design-level choice is surfaced as an open question, none resolved unilaterally.
status: draft
author: Maxim St-Hilaire (methodology owner) — drafted by worker for review
last-updated: 2026-07-24
---

# Step-3 pre-registration package — Sequential-B

**Standing state.** The supervisor has ruled (2026-07-24, HANDOFF): **Branch B,
modified — a sequential design — plus the C+ deliverable in parallel.** This
document is the **pre-registration to be ratified before any Step-3 session
runs.** It is paper only. **No session, no screening, no live-repo harvesting
happens on the strength of this draft** — the first Step-3 session waits for the
supervisor's explicit go *after* ratification (HANDOFF mandate; standing rule).

**Discipline reminder, applied throughout.** Every genuinely design-level choice
below is presented in the house OQ form — options, worker recommendation, **no
resolution** — and collected in §5. The worker resolves none of them. On the
supervisor's word these become ledger entries (OQ-24…) in
[`DECISIONS.md`](DECISIONS.md); they are held in this document for the paper-first
review pass so the supervisor shapes their framing before anything is appended to
the append-only ledger.

**What this package covers** (the Sequential-B mandate, HANDOFF "Track
Sequential-B", items 1–6):

1. Revised ceiling declaration — §4.1 (the *number* is the supervisor's to declare
   at Step-3 start; this drafts the **measured basis** only).
2. Corpus expansion — §2, with **live-verified counts (2026-07-24)**.
3. Group-sequential stopping design — §3 (the core new artifact).
4. Repeats on confirmed-defective cases — §4.2.
5. The queue items (scanner freeze, problem-statement scrub, config-introspection
   provenance) — §4.3–§4.5.
6. Semantic-catch layer — §4.6, recorded **DEFERRED**, not adopted.

Everything traces to committed artifacts and the ledger; nothing restates a
D-entry as if new.

---

## 1. What Sequential-B is, in one paragraph

Branch B (pilot report §11, "Lean study") protects the **headline paired
comparison** — fresh-session same-vendor review vs cross-vendor review (A2 vs B),
and A1 vs B — on **confirmed-defective cases only**, with the correct/false-alarm
sample force-cut (it has no construction path under the ratified corpus, D-031b)
and repeats on defective cases (D-052). The **modification** the supervisor
ordered is that it is **sequential, not fixed-n**: instead of committing to a
single pre-computed n, the study accrues confirmed-defective cases and takes
**pre-registered interim looks**, stopping as soon as a pre-registered evidence
boundary is crossed — for **efficacy or for futility** — with the family-wise
type-I error protected by an **alpha-spending function** (Lan-DeMets;
O'Brien-Fleming- or Pocock-type). This replaces the pilot's fixed-n framing
(report §8) and is what makes Sequential-B a sequential study. The motivation is
not statistical fashion: **throughput is the binding constraint** (declared
15 sessions/week, D-026), so the scarcest resource is sessions, and a design that
can stop early — especially stop early **for futility**, given the pilot's 0/2
audited-catch signal (report §6, F-001) — spends the fewest of them.

---

## 2. Corpus expansion plan — with live-verified counts (2026-07-24)

**Mandate (HANDOFF Sequential-B item 2):** existing feeds first — (a) run the
SWE-rebench post-gate re-query deferred at OQ-9; (b) open the full MultiLang pool
beyond JS/TS. **Own-harvest only on *demonstrated* insufficiency**, never by
default; re-ratification is the D-028c Hanoi decision, now authorized *in
principle* but still requiring the evidence table + a D-entry.

**Blindness preserved (OQ-10 note).** Everything in this section is **counts
only** — `num_rows_total` under the recency gate, per split. **No task
identities, no task content were retrieved.** Identities are pulled only after
the selection ordering (§2.4 / OQ) is fixed, exactly as at OQ-10: counts are
decision-relevant, identities are not, and pulling identities before the rule is
fixed is the researcher degree of freedom §8 exists to remove.

**Verification method.** HuggingFace datasets-server `/filter` endpoint,
`where="created_at" > '2026-03-01'` (the D-023a operative recency gate), per
config/split; split sizes from `/info`. Reproducible; the exact queries are
recorded in this section's footnote. This is the same "measured live, not from
memory" method as the OQ-9 evidence table (`oq9-corpus-evidence.md`).

### 2.1 SWE-bench-Live/MultiLang — full pool, post-gate, per language

| language | post-gate (>2026-03-01) | split size | note |
|---|---:|---:|---|
| c | 6 | 37 | |
| cpp | 53 | 74 | |
| **cs** | **58** | 87 | **new — OQ-9 could not count csharp** (datasets-server error then) |
| go | 66 | 138 | |
| java | 52 | 109 | |
| **js** | **17** | 93 | the pilot's slice … |
| **ts** | **22** | 111 | … JS+TS = **39** (pilot post-gate pool, unchanged) |
| rust | 48 | 94 | |
| **TOTAL** | **322** | **743** | **identical to OQ-9's "322 of 743, measured"** |

**Reading.** The feed is **stable** — the MultiLang post-gate total is 322/743,
byte-for-byte the OQ-9 number, 27 days later. Two facts are *new*: **csharp is
now countable at 58** (it errored at OQ-9), and the **non-JS/TS post-gate supply
is 283** (322 − 39). That is the pool "beyond JS/TS" the mandate points at.

### 2.2 SWE-rebench-leaderboard — the OQ-9 deferred re-query, now exact

OQ-9 recorded "~110+, approximate — exact count rate-limited, needs one re-query
before P0." **Re-query run 2026-07-24:**

- `nebius/SWE-rebench-leaderboard` monthly splits `2025_01…2026_03` + `test`.
- **`test` (860) = the exact sum of the 15 monthly splits (860)** → `test` is the
  union; no separate held-out set to double-count.
- Post-gate (`created_at > 2026-03-01`): **`2026_03` = 110 (all of it);
  `2026_02` = 0; `2026_01` = 0; `test` = 110.** The `2026_03` split's `created_at`
  values run **2026-03-01 → 2026-05-12** (min/max over a 100-row sample), i.e. the
  whole split postdates the gate.
- **SWE-rebench post-gate supply = 110, Python only.**

This resolves the OQ-9 outstanding query: **exactly 110**, not "~110+", and it is
the entire `2026_03` snapshot.

### 2.3 Supply arithmetic against the sequential n_max

The pilot measured, on **JS/TS under the subscription stacks**: usable
(screen-PASS) rate **≈ 29%** (5 PASS / 17 screened, report §4/§8) and defect
yield **≈ 40%** (2 defective / 5 usable, report §3). Composed:
**≈ 0.29 × 0.40 ≈ 0.116 confirmed-defective per screened row**, i.e.
**≈ 8.6 screened rows per harvested defect** (report §8).

| pool (post-gate) | rows | defects at pilot rates (÷8.6) |
|---|---:|---:|
| MultiLang JS/TS (pilot slice) | 39 | ~4.5 |
| MultiLang non-JS/TS | 283 | ~33 |
| MultiLang full | 322 | ~37 |
| SWE-rebench (Python) | 110 | ~13 |
| **MultiLang + SWE-rebench (distinct provenance)** | **432** | **~50** |

**So the *arithmetic* supports n_max up to ~44–50 defective cases** from existing
feeds — **if** the pilot's usable and yield rates hold beyond JS/TS. They are
**not measured beyond JS/TS**, and three things make that extrapolation
load-bearing rather than safe:

1. **Build toolchain is validated on JS only** (RepoLaunch, D-023c/D-027a). Java,
   Go, Rust, C, C++, C#, and Python each bring a different build/test toolchain;
   an unvalidated one consumes the window and can corrupt the throughput measure —
   the exact reason P1 stayed JS/TS (OQ-10).
2. **The platform_infeasible modes are language-specific and rig-relative**
   (D-030/D-048): `bun` crashes under amd64 emulation, process-per-test isolation
   is time-infeasible. Each new language has its own infeasibility profile on the
   Apple-Silicon-emulation rig, unmeasured today.
3. **Label-integrity rates (the five feed-defect modes, D-049 taxonomy) were
   measured on JS/TS**; there is no guarantee other languages fail at the same
   ~29%-usable rate.

### 2.4 Proposed expansion sequencing (draft — the choices are OQ-25/26)

1. **Extend the D-028 ground-truth screen + D-038 evaluator to Python and to the
   non-JS/TS MultiLang languages**, and **measure per-language usable rate on a
   small pre-registered screening sample per language *before* admitting that
   language to the task pool.** Rationale: §2.3's three caveats mean per-language
   usable rate is an unknown to be *measured cheaply* (container compute, not
   sessions — D-028 cost note), not assumed. A language whose validation sample
   is unusable/infeasible is recorded and set aside, exactly as `bun` was.
2. **Prefer the external feeds (MultiLang, SWE-rebench) over own-harvest**, per
   the OQ-9 pre-committed preference order (external third-party provenance beats
   self-collection). **Own-harvest triggers only on *demonstrated* insufficiency**
   — defined in §2.5.
3. **Fix the selection ordering across the now-multi-source, multi-language pool
   before pulling any identity** (OQ-26). The §8 rule (`created_at` ASC, ties by
   `instance_id`) was written for a single pool; a multi-source/multi-language
   pool needs its interleaving rule stated first.

### 2.5 "Demonstrated insufficiency" — the own-harvest trigger (draft)

Own-harvest (OQ-9c, Python-restricted) is authorized *in principle* (HANDOFF) but
gated on evidence. Proposed operational definition, to be ratified: **the combined
MultiLang + SWE-rebench post-gate pool, after the per-language validation gate
(§2.4.1) and the D-028/D-038 screen, cannot supply the ratified n_max
confirmed-defective cases within the ratified stopping horizon.** Only then does
the D-028c Hanoi re-ratification fire, and only with the evidence table + a
D-entry (never a mid-run swerve). Until that evidence exists, existing feeds
carry the study.

> **Footnote — exact queries (reproducibility).** Dataset servers:
> `datasets-server.huggingface.co`. MultiLang: `dataset=SWE-bench-Live/MultiLang`,
> `config=default`, `split∈{c,cpp,cs,go,java,js,rust,ts}`. SWE-rebench:
> `dataset=nebius/SWE-rebench-leaderboard`, `config=default`,
> `split∈{2026_01,2026_02,2026_03,test}`. Filter:
> `where=%22created_at%22%20%3E%20%272026-03-01%27` (URL-encoded
> `"created_at" > '2026-03-01'`). Sizes from `/info` `dataset_info.splits`. Run
> 2026-07-24 ~07:00 UTC.

---

## 3. Group-sequential stopping design (the core new artifact)

This is the mandate's item 3 — "interim looks at pre-registered n thresholds and
corrected significance levels (alpha-spending), citing standard methodology." It
replaces report §8's fixed-n table. **Statistical scaffolding is fully specified
here; the design-level parameter choices are surfaced as OQ-24 and locked by the
supervisor.**

### 3.1 Estimand, endpoint, accrual unit

- **Design.** Paired, within-item: every confirmed-defective case is reviewed
  under **A1, A2, B** (design §4/§5), so each condition delta is a
  **within-case paired comparison** (McNemar-style on a binary catch outcome),
  which buys power at small n (design §5 "Paired analysis").
- **Headline comparison (protected first, §7 cut order).** **A2 vs B** — fresh
  same-vendor vs cross-vendor. Secondary: **A1 vs B**. Both averaged over the two
  authoring directions (D-006 symmetry), per-direction breakdown reported.
- **Accrual unit.** The **confirmed-defective case** (one per ~8.6 screened rows;
  each unit = ~5.5 sessions: ~2.5 authoring + 3 review, report §3/§8).
- **Statistical information.** For a paired-binary (McNemar) endpoint, information
  accrues with the **discordant-pair count**, not the raw case count. Lan-DeMets
  spending (§3.3) is defined on the **information fraction**, which lets interim
  looks be scheduled on discordant pairs even though the study *plans* in
  defective-case units. This matters because at the pilot-observed magnitudes
  (both arms ≈ 0 audited catches) discordance is rare — see §3.6 (futility).
- **Primary endpoint — OQ-24a (not resolved here).** Band-1 **mechanical** catch
  (the D-005 primary metric, objection-proof, untouched) vs the **audited** catch
  (D-039 reader-actionability). The pilot showed these diverge hard (0/2 audited;
  report §6). Worker leans: **Band-1 mechanical as the pre-registered primary
  endpoint** (it is the reviewer-objection-proof spine, D-005), with the
  **audited-catch delta as a pre-registered co-primary/key-secondary** so
  diff-anchoring is measured rather than assumed. See §5.

### 3.2 Max information, look schedule

- **n_max (max planned confirmed-defective cases) — OQ-24b.** Proposals anchored
  on report §8: **33** (~12 wk), **44** (~16 wk, the Branch-B figure), **55**
  (~20 wk). Worker leans **44** (the ratified Branch-B target; ±15 pp per-arm
  Wilson CI, powered for a >20 pp delta per report §8). **This n_max also sets the
  corpus harvest target** (§2.3): 44 defects ≈ 380 screened rows.
- **Number and spacing of interim looks — OQ-24c.** Proposal: **K = 4** looks at
  information fractions **0.25 / 0.50 / 0.75 / 1.00** (n ≈ 11 / 22 / 33 / 44 at
  n_max = 44). Lan-DeMets makes the *exact* timing flexible (looks can land at the
  realized information at each analysis, not forced to exact fractions), which
  suits agentic accrual that arrives in ragged batches.

### 3.3 Alpha-spending function (efficacy boundary)

- **Framework — Lan-DeMets (1983) error-spending.** The family-wise two-sided
  type-I error **α = 0.05** is *spent* across looks by a spending function
  α*(t) of the information fraction t, so the actual number and timing of looks
  need not be fixed in advance — only the spending function is pre-registered.
  This is the standard flexible generalization of Pocock (1977) and
  O'Brien-Fleming (1979).
- **Spending shape — OQ-24d.** Two standard choices:
  - **O'Brien-Fleming-type (worker recommendation).** Spends α *conservatively
    early* — very hard to stop at look 1, easy only at the end — which **protects
    the final analysis** and inflates the maximum sample size only ~**1.02×** over
    the fixed design. Best when you want early stopping reserved for
    *overwhelming* evidence and otherwise pay almost nothing in n_max. Illustrative
    nominal two-sided boundaries for K=4 (O'Brien-Fleming): look 1 ≈ 0.0001,
    look 2 ≈ 0.004, look 3 ≈ 0.019, look 4 ≈ 0.043 (these are *illustrative*; the
    **exact** constants are locked at ratification — see §3.7).
  - **Pocock-type.** Spends α *evenly* — a roughly constant nominal boundary
    (≈ 0.018 at every look for K=4) — so early stopping is easier, at the cost of
    ~**1.17–1.20×**
    n_max inflation and a *higher* final-look bar. Preferable only if stopping-early
    value outweighs the n_max penalty.
  - Worker leans **O'Brien-Fleming**: under a hard throughput ceiling the n_max
    penalty is the expensive thing, and the pilot signal (§3.6) makes a *futility*
    stop more likely than an efficacy stop anyway — so cheap-final-look + small
    n_max inflation is the right trade.

### 3.4 Futility boundary — OQ-24e

- **Why it is central, not optional.** At the pilot-observed magnitudes both arms
  caught **~0** (audited); F-001 is "cross-vendor does *not* rescue diff-anchoring"
  (report §5–§6). If that holds, the paired A2-vs-B delta is **near zero**, and the
  scientifically honest early outcome is a **futility stop** — "the data have
  effectively ruled out a delta ≥ the pre-registered δ, stop spending sessions." A
  design with no futility boundary would grind all n_max sessions to conclude
  "no difference," which is exactly the waste Sequential-B exists to avoid.
- **Proposal (worker recommendation): non-binding beta-spending futility** (e.g.
  a Hwang-Shih-DeCani or Lan-DeMets β-spending boundary) alongside the efficacy
  boundary. *Non-binding* so a futility crossing is a strong recommendation to
  stop that the supervisor may override (agentic runs are noisy; a hard binding
  futility stop on a small discordant count is brittle). The alternative
  (**efficacy-only**) is defensible if the supervisor wants the diff-anchoring
  *miss-rate* (§3.5), not the paired delta, to be the thing the study is powered
  for — in which case futility on the paired delta is less relevant.

### 3.5 The diff-anchoring miss-rate as a one-sample estimand

F-001 (report §5, D-F001) is arguably the study's sharpest quantity, and it is a
**one-sample rate**, not a paired delta: *of confirmed-defective cases whose
authored fix is in a different location than the true defect, in what fraction do
reviewers (per arm) miss the true defect?* This is monitorable with **repeated
confidence intervals** across the same looks (report the Wilson interval per arm
at each look; no additional α to spend because it is estimation, not a second
hypothesis test) — or, if the supervisor wants it as a *primary* powered
endpoint, it becomes its own sequential test and the paired delta demotes to
secondary. Flagged in OQ-24a; recorded here because the pilot's real signal lives
in this quantity.

### 3.6 Multiplicity across the co-primary comparisons — OQ-24f

Two headline comparisons (A2-vs-B, A1-vs-B) share the α. Options:
(a) **Hierarchical gatekeeping (worker recommendation):** test **A2-vs-B first**
    at full α (it is the §7-protected headline); test A1-vs-B only if A2-vs-B
    crosses — no α split, full power on the protected comparison.
(b) **Bonferroni split** (α/2 each) — simpler, symmetric, but halves power on the
    protected comparison for a secondary the design already ranks below it.
Worker leans (a): §7 explicitly protects A2-vs-B first, and gatekeeping encodes
that ranking without spending power on it.

### 3.7 Estimation at stopping, and how the constants get locked

- **Bias-corrected reporting (standard, pre-registered).** A naïve CI/point
  estimate computed at a data-dependent stopping time is biased outward.
  Group-sequential reporting therefore uses the **stagewise-ordering adjusted
  confidence interval and median-unbiased estimate** (Jennison & Turnbull 2000);
  both the naïve and adjusted numbers are reported, the adjusted one is the
  headline. Band composition, verbosity, false-alarm-descope, and compliance
  metrics report as in design §5 (unchanged).
- **The exact boundary constants are LOCKED before session 1, with committed
  provenance.** Once the supervisor rules OQ-24 (endpoint, n_max, K, spending
  shape, futility), the exact boundaries are computed with a **named, versioned
  tool** — R **`gsDesign`** or **`rpact`** — the script + its output committed to
  the repo (same discipline as the seeded selection draws, D-027c, and the canary
  provenance). No boundary is hand-typed into the analysis; §3.3's illustrative
  numbers are placeholders for the tool's output. **This computation is not a
  session and not screening** — it is paper/code, runnable now once OQ-24 is
  ruled.

### 3.8 What this replaces and preserves

- **Replaces:** report §8's fixed-n table (12/16/20/26-wk × fixed n). The
  sequential design subsumes it — the same windows become *maximum* horizons, with
  early stopping on top.
- **Preserves, unchanged:** §7's cut order (correct-sample cut → repeats reduced →
  per-direction n; A2-vs-B protected first); the paired within-item design; the
  three-band scoring pipeline (D-013); the mechanical primary metric (D-005); the
  D-039 catch-audit as a validity layer. Sequential monitoring changes *when the
  study stops*, not *what it measures*.

---

## 4. The non-deferred queue items

### 4.1 Revised ceiling declaration — measured basis only (item 1)

The old "15 sessions/week" (D-026) was a **bare declaration**; the pilot now has a
**measured basis** to declare against. Facts to state at re-declaration (all from
report §2, committed in `sessions.jsonl`):

- **24 logged sessions**, **87 min total wall-clock**, mean **216 s**, range
  **38–551 s** (authoring 184–551 s; reviews 38–332 s).
- **Interrupted-days caveat (binding, D-026):** pilot days were
  supervisor-availability-gated, **not** dedicated; even so `observed × 7 × 0.7`
  **exceeds 15**, so the D-021b `min()` binds and **final-n is
  declaration-driven** — stated where n is computed, per D-026.
- **JS/TS-only caveat (D-027a):** throughput was measured on the
  cheapest-to-build slice; multi-language expansion (§2) may raise per-session
  cost once Java/Go/Rust/Python toolchains enter.

**The exact number is the supervisor's to declare at Step-3 start** (HANDOFF: "do
not assume it"). This draft supplies only the basis; it declares nothing. Once
declared, it is the n_max-to-calendar mapping input for §3.2.

### 4.2 Repeats on confirmed-defective cases (item 4 / D-052)

The pilot's failure: both seeded k=2 repeats landed on **authoring successes**, so
**catch-rate run-to-run variance went unmeasured** (D-052). The fix, because
defectiveness is only known *after* the oracle runs:

- **Draw the k=2 repeat subsample from the *confirmed-defective* set**, not from
  all authored tasks — a seeded random draw (seed recorded before use, D-027c
  discipline), applied *after* cases confirm defective.
- **A repeat re-runs the review arms only** against the fixed authored patch
  (D-029): **A2 and B repeat cleanly** (fresh sessions); **A1 is `n/a
  (structural)`** on an append-only session (D-042) — unchanged rulings.
- This measures the thing the pilot could not: **catch-rate** (not just verbosity)
  run-to-run variance, on cases that actually carry a defect.
- **Interaction with §3:** repeats consume sessions inside the horizon; §7's cut
  order already ranks "repeats" below the protected A2-vs-B n, so under an early
  futility stop repeats are the first thing curtailed. Pre-register the repeat
  fraction (e.g. 20%, design §7) **as a fraction of the confirmed-defective set**.

### 4.3 Scanner freeze — the four D-018 quotation channels (item 5)

Apply the **four adjudicated-clean quotation channels** as exec-context patterns,
then **freeze the scanner** at Step-3 start (D-025.3). All four are the same
underlying rule — *a test-runner name in read/quoted content is not an
invocation; only an execution-context occurrence counts* (HANDOFF nuance):

1. **git-log commit-subject** naming a runner (D-036 — `4a1b74997 chore(test):
   migrate … to vitest`).
2. **test-file mock API** — `jest.fn()`, `jest.mock()`, `vi.fn()`, etc. in read
   test source (D-050).
3. **package.json `scripts`/`devDependencies`** content — `"test": "… jest …"`,
   `"jest": "27.3.1"` (D-050).
4. **source-code runner-name regex/string literal** — a repo's own command
   classifier listing runners (D-053 — `codex-companion.mjs`).

**Freeze mechanics (draft):** fold the four channels into the exec-context filter
in `harness/compliance.py`; add each pilot transcript excerpt as a
false-positive **regression fixture** (the D-025.1 pattern:
`tests/fixtures/d018-*`); assert the paired **retained-detection** test (a real
executed `jest`/`pytest`/`npm test` command still fires) — the D-037 discipline
that a narrowed pattern ships with proof it still catches the real thing. Then
**freeze**: no scanner change after Step-3 start; any later ambiguity is
adjudicated by the standing D-025 procedure (exec-context check → human
adjudication on the executed-command list, blind to the claim), never by editing
the scanner mid-run.

### 4.4 Problem-statement scrubbing (item 5 / D-035b)

**Uniformly** strip fix-pointing references from problem statements **before
authoring**, as a documented input transformation, from Step 3 (never mid-pilot —
D-035b). Scope (draft):

- **Strip:** "Related PRs" lists, "fixed in #N / commit `abc`", upstream-patch
  URLs, and equivalent direct pointers to the task's own fix (the exact channel
  that contaminated pos2, D-035a — the feed handed the author `#191`).
- **Do not strip:** the bug description, reproduction, and expected behavior — the
  legitimate problem statement.
- **Log the transformation per task** (before/after, what was removed) so it is
  transparent, not silent — a recorded covariate, applied identically to every
  task in both authoring directions (D-006 symmetry; the scrub must not be
  vendor-conditional).
- **Pair with per-session network/tool logging** (already standing since D-035c):
  the scrub removes the *pointer*; network logging audits whether an author
  reached the fix anyway. Both are needed — D-003's "unknown to all parties"
  property is *audited*, not assumed.

### 4.5 Config-introspection provenance (item 5 / D-053)

Close the D-012 OpenAI-arm model-ID gap at each session: snapshot **only** the two
fields **`model`** and **`model_reasoning_effort`** from `~/.codex/config.toml`
(pilot: `gpt-5.6-sol` @ `xhigh`) into a per-session `codex-model-snapshot.txt`.
**Never the full config** (it carries local paths, MCP/notify commands, trust
levels — over-sharing for a public dataset; D-053 redaction discipline). This is
introspection, not pinning — it preserves the D-012 field-study framing while
making a mid-study codex-default change *captured* rather than invisible.
Reasoning-effort (`xhigh`) is a recorded stack covariate.

### 4.6 Semantic-catch layer — DEFERRED (item 6 / OQ-21)

**Recorded deferred, not adopted.** The OQ-21 decision (extend Band 2 judges over
mechanical catches → a `semantic_catch` secondary verdict) **waits until the quota
question is measurable** — i.e. until Band 2 actually generates judge volume. The
pilot **never exercised Band 2** (report §7: all cases decided at Band 1; Gemini
free-tier quota feasibility **unmeasured**). Do **not** adopt the semantic layer
pre-emptively: it multiplies judge calls and may breach the D-019/D-021c 50%
free-tier quota threshold, and that breach cannot be checked until real Band 2
traffic exists. **Blocking check before any future adoption:** projected
judge-call volume vs the measured free-tier quota. Carried, not chosen.

**Also carried, not adopted** (report appendix / DECISIONS OQ-23, D-031b): the
**model-tier arm** (OQ-23, a named follow-up routing axis, not in Sequential-B's
scope) and the **false-alarm construction** question (D-031b — in Branch B the
correct sample is **force-cut**, report §8, so no construction path is built now).

---

## 5. Open questions for ratification (worker resolves none)

Collected in house OQ form. On the supervisor's word these are logged to
[`DECISIONS.md`](DECISIONS.md) as OQ-24…OQ-26 (or reshaped as directed) and ruled
as D-entries before any session. **The first Step-3 session waits for the go
*after* these are ruled.**

**OQ-24 — the sequential design parameters** (§3). *Each option carries a
one-line plain-language gloss — what it means, what it risks — so the ruling is on
substance, not vocabulary.*

- **(a) Primary endpoint** — what counts as "the number the study is about":
  - *Band-1 mechanical catch as primary* **(worker lean)** — *count a catch
    whenever the reviewer names the right file+line, ignore whether the comment is
    sensible. Fully reproducible, immune to judge bias. Risk: over-counts — the
    pilot's 2 mechanical catches were both coincidences, so the headline can look
    better than reality unless the audit is read beside it.*
  - *Audited catch as co-primary* — *also require a human to confirm the catch
    would actually help an engineer find the bug. The headline then reflects real
    detection. Risk: puts human judgment back into the primary number (slower,
    subjective — the very thing the mechanical metric avoids) and needs audit
    volume small-n may not supply.*
  - *Diff-anchoring miss-rate — reported one-sample quantity* **(worker lean)** —
    *track with confidence intervals how often reviewers miss a bug sitting
    outside the fix, but don't power the study on it. Cheap. Risk: leaves the
    study's sharpest signal as description, not a tested claim.*
  - *…or diff-anchoring miss-rate as the primary powered endpoint* — *make "do
    reviewers miss off-diff bugs?" the main hypothesis and demote A2-vs-B to
    secondary. Targets the strongest observed effect. Risk: reframes the study
    away from the routing question (A2-vs-B) that motivated it.*

- **(b) n_max** — the most confirmed-defective cases before a forced stop:
  - *33 (~12 wk)* — *cheapest/fastest. Risk: wide CIs (~±18 pp); only a large
    effect is detectable.*
  - *44 (~16 wk)* **(worker lean)** — *the Branch-B target; ~±15 pp CI, powered
    for a >20 pp delta. Risk: needs ~380 rows screened → corpus expansion (§2) is
    a hard precondition.*
  - *55 (~20 wk)* — *tighter numbers (~±12 pp). Risk: more sessions against the
    15/wk ceiling and more corpus supply to find.*

- **(c) Looks — how many times the data is checked, and when:**
  - *K=4 at 0.25 / 0.50 / 0.75 / 1.00* **(worker lean)** — *four regularly-spaced
    checks; good early-stop coverage without over-checking. Risk: each added look
    spends a little α, nudging the final-look bar up.*
  - *fewer (e.g. K=2) or more (e.g. K=6)* — *fewer looks preserve α but stop-early
    less often; more looks catch a signal sooner but each look is weaker evidence
    and adds analysis overhead.*

- **(d) Spending shape — how the 5% error budget is spread across looks:**
  - *O'Brien-Fleming-type* **(worker lean)** — *make early stopping very hard,
    easy only near the end. Keeps the max sample ~2% above a fixed design and
    protects the final analysis. Risk: even a dramatic early result won't stop the
    study — you pay most of the sessions anyway.*
  - *Pocock-type* — *spread the stop-early chances evenly; easier to stop on a
    clear early signal. Risk: inflates the max sample ~17–20% and raises the
    final-look bar, so not stopping early costs more for less.*

- **(e) Futility — whether the study can stop early for *no* effect:**
  - *non-binding β-spending futility* **(worker lean)** — *add a rule that
    recommends stopping once a cross-vendor benefit is effectively ruled out, but
    you may override it. Given the pilot's 0/2 signal this is the likely early
    exit and saves the most sessions. Risk: a futility flag on a small, noisy
    discordant count could point at stopping a live effect — mitigated by
    "non-binding" (your call).*
  - *efficacy-only* — *no futility rule; stop early only for a positive result,
    else run to n_max. Simpler, never cuts a real effect short. Risk: if
    cross-vendor doesn't help (the pilot's direction), you grind all n_max
    sessions to conclude "no difference" — the waste Sequential-B exists to avoid.*

- **(f) Multiplicity — sharing the error budget across the two headline
  comparisons (A2-vs-B, A1-vs-B):**
  - *hierarchical gatekeeping, A2-vs-B first* **(worker lean)** — *test the
    protected A2-vs-B at full strength; test A1-vs-B only if the first passes. No
    power lost on the headline. Risk: if A2-vs-B doesn't pass, A1-vs-B is not
    formally testable (still reported descriptively).*
  - *Bonferroni split (α/2 each)* — *test both at once, each at half the error
    budget; both get a formal test regardless. Risk: halves power on the headline
    A2-vs-B for a secondary the design already ranks below it.*

**OQ-25 — corpus expansion scope & per-language validation** (§2.4). *Plain: JS/TS
alone (39 rows) cannot feed n_max=44; we need more languages and/or SWE-rebench
Python — but the pilot's ~29%-usable rate was only measured on JS/TS, and other
languages have unvalidated build toolchains and unknown emulation-infeasibility.*
- Which languages/sources enter, and the **per-language validation-sample size**
  before a language is admitted. **Worker lean:** admit languages incrementally,
  each validated on a small pre-registered screening sample first *(what it means:
  spend cheap container compute — not sessions — to measure a new language's real
  usable rate before betting the study on it; what it risks: a few weeks of
  screening before harvesting starts)*; external feeds before own-harvest; hold
  own-harvest behind the §2.5 "demonstrated insufficiency" trigger.

**OQ-26 — selection ordering over the expanded pool** (§2.4.3). *Plain: with more
than one source/language, "which task is next" needs a single fixed rule written
before any task identity is seen — otherwise the choice of rule could be
influenced by which tasks it yields (the exact bias §8 forbids).*
- Options, each glossed:
  - **(a) single global `created_at` ASC across all sources** (ties by
    `instance_id`, source as further tiebreak) — *simplest, one honest ordering;
    risk: language/source mix falls where the dates land, so D-006 direction
    balance and the language covariate are left to chance.*
  - **(b) per-language quota, `created_at` ordering within each** — *directly
    controls the language covariate and authoring-direction balance; risk: quotas
    are extra pre-registered parameters and can strand a usable task outside its
    filled quota.*
  - **(c) stratified by source, then language** — *keeps each feed's contribution
    legible; risk: most machinery of (b) with an added source layer.*
- **Worker takes no lean** until OQ-25 fixes which languages are in — the ordering
  rule depends on the pool it orders. **No identities are pulled until this is
  ruled** (OQ-10 blindness).

**Not an OQ — a declaration:** the revised sessions/week ceiling (§4.1) is the
supervisor's to **declare** at Step-3 start, against the measured basis this draft
supplies.

---

## 6. Execution gate (unchanged standing rule)

Nothing in this package executes until the supervisor **(a)** rules OQ-24/25/26
and declares the §4.1 ceiling, **(b)** ratifies this package, and **(c)** gives an
explicit go. Until then: no session, no screening, no live-repo harvesting; the
boundary-constant computation (§3.7) and the corpus **count** queries (§2, done)
are the only paper/code steps that proceed, because neither is a session, screening,
or an identity pull. Design-level ambiguity that surfaces during ratification goes
to DECISIONS.md as a fresh OQ and waits — the single most important discipline
here (HANDOFF standing rules).
