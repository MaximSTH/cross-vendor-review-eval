---
name: step3-preregistration
description: Step-3 (Sequential-B) pre-registration PACKAGE — RATIFICATION-READY. All design choices ruled 2026-07-24 (D-054..D-058): group-sequential stopping design with LOCKED efficacy boundary constants (gsDesign-verified), corpus expansion (live-verified counts), ceiling re-declaration, repeat-on-defective, scanner freeze, problem-statement scrub, config-introspection provenance, supervisor stop protocol. HELD before session 1 for the supervisor's external statistical-review pass, then ratification + go. Semantic-catch layer DEFERRED.
status: ratification-ready (held for external statistical review before session 1)
author: Maxim St-Hilaire (methodology owner) — drafted by worker
last-updated: 2026-07-24
---

# Step-3 pre-registration package — Sequential-B

**Standing state (updated 2026-07-24 — all choices ruled).** The supervisor ruled
Branch B modified (sequential) + C+ (HANDOFF), and has now **ruled every design
choice in this package**: OQ-24/25/26 → **D-054/D-055/D-056**, the ceiling
re-declaration → **D-057**, and a new **supervisor stop protocol → D-058**. The
group-sequential **efficacy boundary constants are computed and LOCKED**
(gsDesign 3.10.1, independently cross-validated; §3.3, §3.7). This document is now
the **ratification-ready package**. **One gate remains before session 1:** the
supervisor's **external statistical-review pass** of the sequential design, then
ratification + explicit go. **Nothing executes until then** — no session, no
screening, no live-repo harvesting, no identity pull.

**Discipline note.** Where this document still shows OQ-style option lists (§5),
they are retained as the **record of what was decided over what** — each now
carries its ruling and D-entry. The worker resolved none of them; the supervisor
did. The single item still genuinely open is the **futility-boundary calibration**
(β / target power and β-spending shape), which the rulings left to the
external-review pass (§3.4) — flagged, not resolved.

**What this package covers** (the Sequential-B mandate, HANDOFF "Track
Sequential-B", items 1–6):

1. Revised ceiling declaration — §4.1 (**RULED D-057**: 15/wk sizing, ≤30/wk
   logged surplus, sizing never uses surplus).
2. Corpus expansion — §2, **live-verified counts (2026-07-24)** (**RULED D-055**).
3. Group-sequential stopping design — §3 (**RULED D-054**; efficacy constants
   LOCKED).
4. Repeats on confirmed-defective cases — §4.2.
5. The queue items (scanner freeze, problem-statement scrub, config-introspection
   provenance) — §4.3–§4.5; **supervisor stop protocol** §4.7 (**RULED D-058**).
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
replaces report §8's fixed-n table. **All six parameters are RULED (D-054); the
efficacy boundary constants are computed and LOCKED (§3.3, §3.7).** The only
remaining open item is the futility-boundary *calibration* (§3.4), left to the
external-review pass.

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
- **Primary endpoint — RULED (D-054a).** **Band-1 mechanical catch is the
  pre-registered primary endpoint** (the D-005 objection-proof spine). **Audited
  catch (D-039) is the key secondary, reported alongside it at every look.** The
  **diff-anchoring miss-rate is monitored per arm via repeated Wilson intervals**
  (§3.5) — estimation, **no α spent** on it.

### 3.2 Max information, look schedule

- **n_max — RULED (D-054b): 44 confirmed-defective cases** (~16 wk at 15/week;
  ±15 pp per-arm Wilson CI, powered for a >20 pp delta per report §8). **This n_max
  also sets the corpus harvest target** (§2.3): 44 defects ≈ 380 screened rows.
- **Looks — RULED (D-054c): K = 4** at information fractions
  **0.25 / 0.50 / 0.75 / 1.00** (n ≈ 11 / 22 / 33 / 44 at n_max = 44). Lan-DeMets
  makes the *exact* timing flexible (looks land at the realized information at each
  analysis, not forced to exact fractions), which suits agentic accrual that
  arrives in ragged batches.

### 3.3 Alpha-spending function + LOCKED efficacy boundaries

- **Framework — Lan-DeMets (1983) error-spending.** The family-wise two-sided
  type-I error **α = 0.05** (0.025 per side for the symmetric test) is *spent*
  across looks by a spending function α*(t) of the information fraction t, so the
  number and timing of looks need not be fixed in advance — only the spending
  function is pre-registered. Standard flexible generalization of Pocock (1977) and
  O'Brien-Fleming (1979).
- **Spending shape — RULED (D-054d): O'Brien-Fleming-type** (Lan-DeMets `sfLDOF`).
  It spends α conservatively early (very hard to stop at look 1, easy only at the
  end), protecting the final analysis and inflating n_max only ~1.01–1.02× over a
  fixed design — the right trade under a hard throughput ceiling, and apt given the
  pilot signal makes a *futility* stop (§3.4/§3.6) the more likely early exit.

**LOCKED efficacy Z-boundaries** (computed §3.7; canonical **gsDesign 3.10.1**,
independently cross-validated to <1e-3):

| look | info fraction t | Z-boundary bₖ | nominal two-sided p |
|---:|---:|---:|---:|
| 1 | 0.25 | **4.3326** | 1.47 × 10⁻⁵ |
| 2 | 0.50 | **2.9631** | 3.05 × 10⁻³ |
| 3 | 0.75 | **2.3590** | 1.83 × 10⁻² |
| 4 | 1.00 | **2.0141** | 4.40 × 10⁻² |

Cross a boundary ⇒ reject H0 for the A2-vs-B comparison at that look. The final
bound 2.0141 sits just above the fixed-design 1.9600 — the OBF "cheap final look"
(≈1.01–1.02× max-information inflation). These constants are the ratified efficacy
rule; they do **not** depend on the effect size.

### 3.4 Futility boundary — RULED adopted (D-054e); calibration for external review

- **RULED (D-054e): a non-binding β-spending futility boundary is adopted.** A
  crossing is a **stop *recommendation* escalated to the supervisor, never an
  automatic stop** (this is the hook into the D-058 stop protocol). Rationale on
  the record: at the pilot magnitudes both arms caught ~0 (audited); if
  "cross-vendor does not rescue diff-anchoring" (F-001) holds, the paired A2-vs-B
  delta is near zero and the honest early exit is a **futility stop** — the waste
  an efficacy-only design would incur is exactly what Sequential-B avoids.
- **Two calibration inputs remain OPEN — for the external-review pass**, because
  the ruling adopted the *concept*, not the numbers: **(i)** the calibrating
  alternative (target power / effect size the futility boundary is drawn against);
  **(ii)** the β-spending shape (e.g. sfLDOF vs Hwang-Shih-DeCani). Unlike the
  efficacy boundary, the futility boundary **depends on the assumed alternative**,
  so it cannot be "locked" without these.
- **Provisional futility Z-lower-boundaries** (illustrative, for the review to
  confirm or revise), under **β = 0.10** and calibrating drift **θ_max =
  z₀.₉₇₅+z₀.₉₀ = 3.2415** (90 % power at the design alternative), one-sided sfLDOF
  β-spending: **≈ −0.94 / 0.45 / 1.22 / 1.79** at t = 0.25/0.50/0.75/1.00
  (`boundary_constants.py`). gsDesign `test.type=6` yields a differently-calibrated
  set; reconciling the two is a review-pass task. **These numbers are NOT locked.**

### 3.5 The diff-anchoring miss-rate as a one-sample estimand

F-001 (report §5, D-F001) is arguably the study's sharpest quantity, and it is a
**one-sample rate**, not a paired delta: *of confirmed-defective cases whose
authored fix is in a different location than the true defect, in what fraction do
reviewers (per arm) miss the true defect?* This is monitorable with **repeated
confidence intervals** across the same looks (report the Wilson interval per arm
at each look; no additional α to spend because it is estimation, not a second
hypothesis test). Per D-054a the miss-rate is a **reported estimation quantity**,
not a powered endpoint (the paired A2-vs-B delta stays the headline) — but it is
recorded here because the pilot's real signal lives in this quantity.

### 3.6 Multiplicity across the co-primary comparisons — RULED (D-054f)

Two headline comparisons (A2-vs-B, A1-vs-B) share the α. **RULED: hierarchical
gatekeeping.** **A2-vs-B is tested first at full α** (the §7-protected headline,
using the §3.3 locked boundaries); **A1-vs-B is formally tested only on a crossing
of A2-vs-B**, and is otherwise **reported descriptively**. No α split — full power
on the protected comparison.

### 3.7 Estimation at stopping; the LOCKED constants and their provenance

- **Bias-corrected reporting (pre-registered).** A naïve CI/point estimate at a
  data-dependent stopping time is biased outward. Reporting uses the
  **stagewise-ordering adjusted confidence interval and median-unbiased estimate**
  (Jennison & Turnbull 2000); both naïve and adjusted numbers are reported, the
  adjusted one is the headline. Band composition, verbosity, false-alarm-descope,
  and compliance metrics report as in design §5 (unchanged).
- **Constants LOCKED with committed provenance.** The efficacy boundaries (§3.3)
  are computed and committed under `results/step3/`:
  - `boundary_constants.R` (+ `.R.out`) — **canonical, gsDesign 3.10.1**
    (`sfLDOF`, `test.type=2`), the named tool the ruling required;
  - `boundary_constants.py` (+ `boundary_constants.txt`) — an **independent**
    from-scratch sequential numerical-integration recursion (numpy/scipy) that
    **reproduces gsDesign to <1e-3 at every look**, as a cross-check.
  Same provenance discipline as the seeded selection draws (D-027c) and the canary
  runs. **Self-correction on the record:** the first computation used a
  non-standard sfLDOF characteristic constant and disagreed with gsDesign at early
  looks; the named-tool cross-check caught it (D-054 note). No boundary is
  hand-typed. **This computation is not a session and not screening** — paper/code,
  already done.
- **The futility constants are NOT yet locked** — they await the §3.4 calibration
  in the external-review pass.

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

### 4.1 Revised ceiling declaration — RULED (D-057, supersedes D-026)

**Declared: 15 sessions/week for all sizing and look-schedule math; opportunistic
surplus up to 30/week permitted and logged; sizing never uses the surplus.** The
old bare "15" (D-026) now has the pilot's **measured basis** stated against it
(report §2, `sessions.jsonl`):

- **24 logged sessions**, **87 min total wall-clock**, mean **216 s**, range
  **38–551 s** (authoring 184–551 s; reviews 38–332 s).
- **Interrupted-days caveat (D-026 principle preserved):** pilot days were
  supervisor-availability-gated, **not** dedicated; even so `observed × 7 × 0.7`
  **exceeds 15**, so the D-021b `min()` binds and **final-n stays
  declaration-driven** — stated where n is computed.
- **JS/TS-only caveat (D-027a):** throughput was measured on the
  cheapest-to-build slice; multi-language expansion (§2) may raise per-session
  cost once Java/Go/Rust/Python toolchains enter.

**Two numbers, one discipline:** **15/week** drives every sizing and pacing
computation (n_max=44 → calendar horizon, §7 cut order, §3 look pacing);
**≤30/week** governs only *actual throughput logging* (a good week may accrue
faster, logged per-week in provenance). **Sizing never uses the surplus** — a fast
stretch cannot inflate the plan (the D-021b/D-026 discipline, now an explicit
split).

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

### 4.7 Supervisor stop protocol — RULED (D-058)

A standing three-level stop procedure, **invocable by the supervisor at any time
with a single message**. All three preserve the pilot-proven invariant:
**interrupted work is never a verdict, and any stop leaves a pushed, resumable
state.**

1. **PAUSE** — finish the in-flight session/container, stop at the boundary, log,
   hold for resume. The in-flight unit completes and its result stands.
2. **HALT** — kill in-flight work now: sessions **voided per protocol (never
   scored)**; containers `docker kill`ed with **orphan verification**; an
   interrupted screen marked **INTERRUPTED — never a verdict**; **state committed
   and pushed**; everything resumable.
3. **ABORT-STUDY** — HALT **plus** a written study-termination record: sessions
   completed, **data retained as-is (nothing discarded)**, and an **analysis of
   whatever exists per the stopping design's administrative-termination rules**
   (Jennison & Turnbull 2000): final analysis at the information actually accrued,
   using the α spent through the last completed look and the stagewise-ordering
   adjusted estimate/CI (§3.7) — a recorded, analyzable endpoint, not a discard.

Full text in D-058. The futility boundary (§3.4) feeds level (1)/(2): a futility
crossing is a **stop *recommendation* escalated to the supervisor** (D-054e), who
may then invoke PAUSE/HALT or override.

---

## 5. Decision record — what was ruled (2026-07-24)

**Every choice in this package is now RULED** (ledger: **D-054/D-055/D-056/D-057/
D-058**). The option lists below are retained as the **record of what was decided
over what** — each now marked with its ruling. The worker resolved none; the
supervisor did. **The one item still genuinely open** is the §3.4 futility
*calibration*, held for the external-review pass. **The first Step-3 session waits
for that review + ratification + explicit go.**

| choice | ruling | ledger |
|---|---|---|
| Primary endpoint | Band-1 mechanical (primary); audited catch key-secondary; miss-rate via repeated Wilson CIs | D-054a |
| n_max | 44 confirmed-defective cases | D-054b |
| Looks | K=4 at t=0.25/0.50/0.75/1.00 | D-054c |
| Spending shape | O'Brien-Fleming-type (sfLDOF); **efficacy constants LOCKED** (§3.3) | D-054d |
| Futility | non-binding β-spending, escalated not automatic; **calibration → external review** | D-054e |
| Multiplicity | hierarchical gatekeeping, A2-vs-B first | D-054f |
| Corpus expansion | incremental language admission; external feeds first; ~10-row validation gate | D-055 |
| Selection ordering | global `created_at` ASC, ties `instance_id`→source; language×vendor a reported secondary | D-056 |
| Ceiling | 15/wk sizing; ≤30/wk logged surplus; sizing never uses surplus | D-057 |
| Stop protocol | PAUSE / HALT / ABORT-STUDY | D-058 |

The glossed option lists that produced these rulings follow, retained verbatim for
the record.

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

**OQ-25 — corpus expansion scope & per-language validation** (§2.4) — **RULED
D-055** (incremental admission; external feeds first; ~10-row validation gate).
*Plain: JS/TS
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

**OQ-26 — selection ordering over the expanded pool** (§2.4.3) — **RULED D-056**
(option (a)). *Plain: with more
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
- **Worker took no lean** — RULED (D-056): **option (a)**, global `created_at` ASC,
  ties `instance_id`→source, restricted to admitted languages; language×vendor is a
  reported (descriptive) secondary. **No identities are pulled until execution**
  (OQ-10 blindness).

---

## 6. Execution gate — one item remains

**All package choices are ruled (D-054…D-058) and the efficacy constants are
LOCKED.** Before session 1 there remains, in order:

1. **The supervisor's external statistical-review pass** of the sequential design
   (the held gate) — including the §3.4 **futility calibration**, the one item the
   rulings left open.
2. **Ratification** of this package as revised by that review.
3. **Explicit go.**

Until all three: **no session, no screening, no live-repo harvesting, no identity
pull.** The paper/code steps already completed — the **boundary-constant
computation** (§3.7, `results/step3/`) and the **corpus count queries** (§2) — are
neither sessions, screening, nor identity pulls. Any design-level ambiguity that
surfaces during the review pass goes to DECISIONS.md as a fresh OQ and waits — the
single most important discipline here (HANDOFF standing rules).
