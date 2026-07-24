---
name: handoff
description: Session handoff — pilot-complete state, the three Step-3 decision branches + pre-registration queue, standing rules, and operational nuance not in the ledger. Written 2026-07-23 at pilot close.
status: active
---

# HANDOFF — written 2026-07-23, pilot complete

For a successor who has read [`DECISIONS.md`](DECISIONS.md) (D-001–D-053) and
the pilot report ([`results/pilot/report.md`](../results/pilot/report.md)) but
lived none of it. The decision log is the SSOT; this file adds only **state,
bounds, and operational nuance** — the things that are true but not written as
D-entries.

*(Supersedes the 2026-07-18 window-close handoff, which covered D-001–D-025 and
the pre-P1 frozen state. That state is now history: P0 and P1 are both done.)*

## Current state — the one-paragraph version

**The pilot is COMPLETE and the report is drafted.** P0 + P1 ran end to end:
6 tasks, 3 confirmed-defective. Two publishable findings emerged — **F-001
diff-anchoring** (reviewers grade the diff and miss defects located elsewhere;
all 3 defective cases) and the **corpus-integrity taxonomy** (~29% usable feed,
5 failure modes, 4 feed-attributable). The catch-audit came back **0/2** (both
mechanical catches were diff-anchoring artifacts). Everything is committed and
pushed to the public repo. **The supervisor has RULED (2026-07-24): Branch B
modified — a sequential design — plus the C+ deliverable in parallel.** The
mandate (next section) is to **pre-register and draft**, not execute; **no
Step-3 session runs until the supervisor's go after ratification.**

## ⇒ SUPERVISOR RULING — the successor's mandate (2026-07-24)

**The go/no-go is decided.** The three-branch question in the report (§11) is
resolved: **Branch B, modified — a sequential design — PLUS the Branch-C
deliverable in parallel ("C+").** The "open decision" section further below is
retained only for the reasoning; **this ruling governs.** Everything here is a
**mandate to pre-register and draft — not to execute.** No Step-3 session runs
until the supervisor's explicit go **after** the pre-registration below is
ratified.

### Track C+ — publish now, no new sessions

1. **Practitioner write-up → publication.** `results/pilot/practitioner-writeup.md`
   proceeds to publication as-is (D-022 clean; render via `tools/render-doc.sh`).
2. **arXiv methods-and-findings note** — draft as a **separate deliverable**:
   the **corpus-integrity taxonomy**, the **catch-audit metric-validity result**
   (localization catch-rate is an upper bound; audit it), and **F-001
   diff-anchoring as a documented phenomenon with n stated** (2 P1 defective
   cases + P0; never as an established rate). **No new sessions required.**

### Track Sequential-B — ALL items pre-registered BEFORE any session

Draft each for supervisor ratification; none is self-approving.

1. **Revised ceiling declaration** — re-declare sustainable sessions/week **with
   the pilot's measured basis stated** (the 87-min/24-session wall-clock and the
   interrupted-days caveat; the old 15 was a bare declaration). **Exact number
   is declared by the supervisor at Step-3 start** — do not assume it.
2. **Corpus expansion — existing feeds first.** (a) **SWE-rebench**: run the
   exact post-gate-count re-query deferred at OQ-9. (b) **Full MultiLang pool**
   beyond JS/TS (the pilot's ~29% usable rate was measured on JS/TS only).
   **Own-harvest only on *demonstrated* insufficiency** of the existing feeds —
   not by default. Re-ratification is the D-028c Hanoi decision, now authorized
   *in principle* but still requiring the evidence table + a D-entry.
3. **Group-sequential stopping design** — draft a design with **interim looks at
   pre-registered n thresholds** and **corrected significance levels**
   (alpha-spending), **citing standard methodology** (e.g. O'Brien-Fleming /
   Pocock / Lan-DeMets). For supervisor ratification before any session. This
   replaces the pilot's fixed-n framing and is what makes "Sequential-B" a
   sequential study.
4. **Repeats on confirmed-defective cases** (D-052) — so catch-rate run-to-run
   variance is actually measured this time; do not let repeats land on authoring
   successes.
5. **Apply the Step-3 pre-registration queue** (report appendix): **scanner
   freeze** (the four D-018 quotation channels, below), **problem-statement
   scrubbing** (D-035b), **config-introspection provenance** (D-053).
6. **Semantic-catch layer DEFERRED** — the OQ-21 decision waits until the
   **quota question is measurable** (i.e. until Band 2 actually generates judge
   volume). Do not adopt it pre-emptively; the pilot never exercised Band 2.

**Standing bound unchanged:** design-level ambiguity → DECISIONS.md OQ → wait
for the supervisor. The mandate authorizes *drafting and pre-registration*, not
execution; the first Step-3 session waits for the supervisor's go after
ratification.

## What is done (do not redo)

- **Build + P0:** complete and accepted (pre-2026-07-18 history).
- **P1:** 5 tasks, full flow each, all scored. Positions: 1 haraka (success),
  2 NemoClaw (**defective**), 3 doctoc-329 (success), 4 codex-plugin-cc
  (success), 5 next-translate (**defective**). 24 sessions + 1 discarded.
  Provenance: `results/pilot/sessions.jsonl`, `scoring.jsonl`,
  `raw/p1-pos{1..5}/`, `p1-checkpoint.md`, `p1-log.md`, `p1-brief.md`.
- **Both deliverables drafted:** `results/pilot/report.md` (§6, full) and
  `results/pilot/practitioner-writeup.md` (branch-independent standalone).
- **Band 3:** one batch (`results/band3/cards-p1-b1.html`, pos2's 2 catches),
  **ruled by the supervisor** (both no_catch, `band3-rulings.json`). No cards
  pending.

## The decision (NOW RULED — see the mandate above) — Step 3 go/no-go (report §11)

*Resolved 2026-07-24: Branch B modified (sequential) + C+. Retained below for
the reasoning that fed the ruling.* The three branches the supervisor chose
across:

- **A — Full study** (~900 sessions, ~60 wk at 15/wk → effectively needs the
  §7 **API-replication budget $1.5–4k** to be feasible; also fixes the D-012
  OpenAI-model-ID gap and pins versions).
- **B — Lean study** (~40 confirmed-defective cases, ~16 wk; correct-sample
  force-cut; **requires corpus re-ratification** because the current feed's
  post-gate JS/TS supply is 39 rows and ~29% usable).
- **C — Terminal** (publish the practitioner write-up; repo stays open; no more
  sessions).

Binding constraints: **throughput (declared 15/wk, D-026) and corpus supply
(~29%)**. A needs budget, B needs corpus expansion, C needs neither.

**Do not execute any branch, screen any new task, or run any session until the
supervisor's explicit ruling.** Standing-rule territory (below) is the only
thing that proceeds without a fresh authorization.

### Step-3 pre-registration queue (report appendix — none adopted yet)

Each must be pre-registered as a D-entry **before** any Step-3 execution:
1. Semantic-catch layer (OQ-21) — Band 2 over mechanical catches → quota-check
   first (D-019).
2. Model-tier arm (OQ-23) — same-vendor premium (Fable-class) as a routing axis.
3. False-alarm construction (D-031b) — augment tests / descope to secondary /
   re-ratify corpus.
4. **Scanner freeze** — apply the **four D-018 quotation channels** (see nuance
   below) as exec-context patterns, then freeze.
5. Repeat-on-defective rule (D-052) — k=2 repeats must land on defective cases.
6. Problem-statement scrubbing (D-035b) — strip fix-pointing links, uniformly.
7. Config-introspection provenance (D-053) — snapshot codex model+effort per
   session.
8. Corpus re-ratification (D-028c) — the Hanoi decision, report open.

## Standing rules (proceed without re-authorization)

- Editing docs/code/tests locally; pushing to the public repo; logging open
  questions. **Design-level ambiguity is never resolved unilaterally** — it goes
  to DECISIONS.md as an OQ and waits for the supervisor. This has fired many
  times (see the OQ chain) and is the single most important discipline here.
- **Cite by commit/file, never by chat position** (the supervisor verifies).
- **Secret-hygiene gate is release-blocking (D-019):** run
  `scan_artifact_for_secrets` over every artifact before commit. It is a gate,
  not hygiene, because logs ship with the dataset (D-012). Bearer/`$VAR` refs
  pass since D-037; the gate targets **data artifacts**, not the harness source
  (which necessarily contains the gate's own patterns).
- **Never repair a task's oracle** (D-049e): the harness runs each task's
  shipped test command verbatim; a command that won't execute is a *recorded
  finding*, never patched into working order. Repairing the oracle is authoring
  the benchmark.

## Operational nuance NOT in the ledger (the reason this file exists)

- **D-018 quotation channels — the scanner cries wolf on read content.** The
  compliance scan flags test-runner *names*; four channels are pure quotation,
  not invocation, and are adjudicated clean (D-036/D-050/D-053), to be folded
  into exec-context patterns **at the freeze**: (1) a **git-log commit-subject**
  line naming a runner; (2) a **test-file mock** (`jest.fn()`); (3)
  **package.json scripts/devDeps**; (4) a **source-code regex literal listing
  runners** (a repo's own command-classifier). When a reviewer scan comes back
  `ambiguous`, adjudicate on the **executed command list, blind to the claim** —
  if the runner name only appears in read/quoted content and the only executed
  commands are git/read/`tsc --noEmit`/`node --check` (permitted static
  tooling), it is clean.

- **Compliance scans require the FULL session transcript, never the CLI summary
  (D-031d).** `claude --output-format json` and Codex's final message carry
  **only final text, no tool calls** — a D-018 scan over them is a silent
  false-negative (would pass a session that ran the whole suite). Reconstruct
  the transcript from: the **session JSONL**
  (`~/.claude/projects/<slug>/<session_id>.jsonl`) for Claude, the **`--json`
  event stream** for Codex. This is done in every arm's logging step; do not
  skip it.

- **Codex model ID via config introspection (D-053).** `codex exec --json`
  emits **no** model ID. The resolved model+effort live in
  `~/.codex/config.toml` (`model = "gpt-5.6-sol"`,
  `model_reasoning_effort = "xhigh"`). Snapshot **only those two lines** per
  session (`codex-model-snapshot.txt`), **never the full config** — it carries
  local project paths, MCP/notify commands, trust levels (no secrets, but
  over-sharing for a public dataset).

- **VM memory: the colima VM must be ≥8 GiB.** It was resized 2→8 GiB mid-pilot
  (D-045). At 2 GiB, Node test suites OOM non-deterministically under emulation
  and the runner is `Killed` mid-run → `parsed=0`. **`--memory=6g` on the docker
  run is cosmetic if the VM is smaller** — Docker can't hand out RAM the VM
  lacks. The real safeguard is (a) VM size, and (b) the discipline that
  **`parsed==0` is HARNESS-ERROR, never CONFIRMED DEFECTIVE** (D-030/D-038/D-045).
  A screened-PASS task reading "defective with 0 parsed" is the incoherence tell
  (D-047) — suspect the measurement, re-run with headroom, do **not** record the
  verdict.

- **Docker/emulation basics.** colima runs Docker; task images are amd64 under
  emulation (slow). `/private/tmp` is **not** mounted into the VM — pipe files
  into containers via stdin (the eval/screen scripts base64 the patch inline).
  Two rig-relative exclusions exist (D-030/D-048): **bun** binaries crash
  (`Illegal instruction`) and **`--experimental-test-isolation=process` × 1000s
  of tests** is time-infeasible; both are `platform_infeasible`, rerunnable on
  native amd64.

- **Orphan + lid discipline (learned twice).** Stopping a runner (TaskStop)
  **does not stop the `docker run` it spawned** — the container keeps burning
  CPU. After any interrupted run: `docker ps`, then `docker kill` the survivor,
  then confirm `(clean)`. Before the laptop lid closes, containers die anyway —
  so **stop cleanly, record the in-flight row as INTERRUPTED-to-rerun (never a
  verdict), commit, push.** This happened 3× in P1; the log has the incidents.

- **Oracle-authoritative evaluation (D-038).** The evaluator resets the
  test_patch's files before applying it: `git checkout HEAD -- f 2>/dev/null ||
  rm -f f` (restore if it exists at base, remove if the model created a
  colliding new file). The model must never supply oracle test files. Ground-
  truth defect regions come from the **gold patch's `-` side** (base coords);
  reviewer claims are matched at ±5 (sweep ±1/±10). The reusable evaluator is
  `results/pilot/raw/evaluate.py`; the screen is `raw/p1-gt-screen/`.

- **Session mechanics.** Authoring: Codex `-s workspace-write` (read-only
  silently produces no patch); Claude `--permission-mode acceptEdits`. Reviews
  are **read-only** both stacks (D-031f/D-041): Codex `-s read-only`, Claude
  `--disallowedTools Edit Write NotebookEdit`. A1 = resume the authoring session
  (Codex `exec resume -c sandbox_mode="read-only"`; Claude `--resume <id>`).
  A2/B = fresh clones with the authored patch applied on a **post-setup baseline
  commit** (D-034: commit build artifacts behind HEAD with `--no-verify` to
  dodge husky hooks, so the reviewed `git diff` is exactly the authored change +
  its untracked tests, no lockfile noise).

## The one-sentence version

The pilot is done, the report is ruled — **Sequential-B + C+** — and the
successor's job is to **draft and pre-register** the sequential study (revised
ceiling, corpus expansion, group-sequential stopping design, repeats-on-defective,
the freeze/scrub/provenance queue; semantic-catch deferred) and to **ship the C+
deliverables** (practitioner write-up + arXiv note), while **no Step-3 session
runs until the supervisor's go after ratification.**
