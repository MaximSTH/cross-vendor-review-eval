---
name: step3-brief
description: Step-3 (Sequential-B) execution brief — the living execution record required by D-063. Holds the ratification record, the alternation phase flip (seed + outcome), the per-language validation results (D-055 gate), the fixed pool + D-056 selection ordering + seeds, admitted languages, and the skip trail as it accrues. Every section is appended, never rewritten; each execution step lands here AFTER the pushed trail that authorizes it.
status: live (execution in progress)
started: 2026-07-29
---

# Step-3 execution brief

**Authority.** Pre-registration RATIFIED as amended through `34488d0`; GO issued
2026-07-29 (**D-063**). Execution order per prereg §6: (1) per-language
validation samples (D-055) → (2) pool fix + D-056 ordering + identity pull →
(3) sessions per the ratified design. **The pushed, public, timestamped trail
precedes every execution step.**

---

## 1. Alternation phase — recorded coin flip (D-063 ratification amendment)

Per the D-027 precedent (pilot `coin_flip_position1`), the alternation phase —
which vendor authors position 1 of the D-056 selection order — is set by one
recorded coin flip, not by hand.

- **Procedure (declared before the draw):** one 32-bit OS-entropy seed
  (`secrets.randbits(32)`); `random.Random(seed).randrange(2)`; mapping
  declared in the committed command before execution: **0 → anthropic
  authors position 1; 1 → openai authors position 1**.
- **Seed (recorded):** `2649229146`
- **Outcome:** bit = `1` → **position 1 is authored Codex-side (openai)**.
- **Rule thereafter (prereg §3.1):** authoring direction alternates
  deterministically down the D-056 order — position 1 openai, position 2
  anthropic, position 3 openai, … Skipped/replaced cases do not shift the
  phase: direction is a function of the case's position index in the selection
  order, and the skip trail (§5 below) records every skip.

Reproduce: `python3 -c "import random; print(['anthropic','openai'][random.Random(2649229146).randrange(2)])"`

## 2. Per-language validation samples (D-055) — execution step 1

Candidate languages (D-063): **SWE-rebench Python** + **MultiLang
go / cs / cpp / java / rust**. (MultiLang `c` is not a candidate: 6 post-gate
rows cannot support a ~10-row validation sample; JS/TS are already validated by
the pilot.)

**Sample selection rule (declared before any row is pulled):** for each
candidate language, the **first ~10 post-gate rows in `created_at` ASC order,
ties by `instance_id`** (the D-056 ordering discipline applied to the
validation sample), from the same queries recorded in prereg §2's footnote.
Validation is **container work, not sessions** (D-055); rows pulled here are
identities *for validation only* — the study pool is fixed at step 2.

**Sample drawn 2026-07-29** (`validation/sample-selection.json`): 10 rows per
language, post-gate totals at draw time matching the prereg §2 live-verified
counts exactly (go 66, cs 58, cpp 53, java 52, rust 48, SWE-rebench 110).

**Runner** (`validation/screen-runner.py`): the pilot's D-028 screen flow
verbatim for MultiLang; SWE-rebench path via per-instance eval images +
`install_config.test_cmd` + the standard pytest parser. **Declared operational
caps (D-048):** per-row image pull ≤ 60 min, container run ≤ 60 min; a timeout
is recorded **INFEASIBLE — `platform_infeasible(time)`, never a label
verdict** (D-030/D-048). Verdicts: PASS / FAIL (label integrity) / ERROR
(harness) / INFEASIBLE. Images dropped after each row (re-pullable; VM disk
bound). Rig note: pilot-era `sweb.eval` image caches (~95 GB) were pruned to
make room; an unrelated project's containers on the shared VM were untouched.

**Status:** RUNNING (launched 2026-07-29, background; order python → go → cs
→ cpp → java → rust). Per-language usable-rate table lands here when complete.

**Pass-2 interim table (completed 2026-07-30 01:47; reconciled 2026-08-05
after a supervision gap — the runner finished cleanly; its completion
notification was lost with the local harness process, work was NOT
interrupted).** PASS/FAIL/INFEASIBLE are settled; ERROR rows are VOID
(harness/rig artifacts, never label verdicts) and re-run in pass 3:

| language | PASS | FAIL | INFEASIBLE | ERROR (void) | usable so far |
|---|---:|---:|---:|---:|---:|
| python | 6 | 2 | 2 (crash: keras/TF AVX) | 0 | **6/10 settled** |
| go | 3 | 4 | 1 (time: kyverno) | 2 | ≥3/10, 2 pending |
| cs | 0 | 9 | 1 (time: SubtitleEdit) | 0 | **0/10 settled** |
| cpp | 2 | 3 | 2 (time) | 3 | ≥2/10, 3 pending |
| java | 1 | 9 | 0 | 0 | **1/10 settled** |
| rust | 0 | 1 | 1 (time: ruffle) | 8 | 8 pending |

**Pass-3 rig finding (logged before re-run):** the three INFEASIBLE(time)
rows' images (kyverno 13.3 GB, organicmaps 42.3 GB, ruffle 37.5 GB) survived
the per-row `docker rmi` (timeout-kill race) and filled the 100 GiB VM disk —
**all 8 rust ERRORs and the ClickHouse cpp ERROR are disk-exhaustion pull
failures**, void. Fixed by removing the stuck images (~93 GB reclaimed; no
sweb containers were running — D-058 orphan check clean). Also added: a
narrow Go-runtime-fatal signature (`fatal error:` + `runtime/mgc.go`, only
with zero parsed tests) classifies as platform_infeasible(crash) — the
envoy-gateway go row is a Go GC-worker crash under emulation. Two rows were
flagged for human adjudication as candidate D-049 `eval_harness_failure`
(feed-side, not our harness): cpp DirectXShaderCompiler (its suite ran —
4470 passes visible in the build log — but the record's canonical print/parse
path yields nothing) and cpp esphome-15060 (pytest dies at collection on the
repo's own module). **ADJUDICATED (D-064.1, 2026-08-05): both are
`eval_harness_failure` — reproduced on passes 2 and 3; they count non-usable
(feed defect) in the table; machine verdicts in `screen.json` stay ERROR with
this adjudication as the overlay.** envoy-gateway's classification is held
pending one rerun under the D-064.2 capture fix (build-log head+tail).

**Harness fixes logged mid-screen (2026-07-29, first pass; incoherence
discipline).** The first pass surfaced two rig/harness issues, fixed in
`screen-runner.py` and pushed before the resume: **(1) PATH clobbering** —
`bash -l` sources the image profile, which resets PATH over the Docker ENV
PATH; the go toolchain lives in ENV PATH, so **all 9 go ERRORs were
`go: command not found`**, a harness artifact, never a label verdict (fix:
inject the image's ENV PATH from `docker inspect`; the login profile is still
sourced — the bun/JS case — so both PATH sources apply). **(2) Emulation
crashes** — keras/TF rows core-dump under amd64 emulation (AVX absent): now
classified **INFEASIBLE `platform_infeasible(crash)`** (the D-030 bun
precedent), not ERROR. Settled PASS/FAIL/INFEASIBLE verdicts from the first
pass were produced by unaffected code paths and stand; **ERROR rows re-run
under the fixed harness** (the runner caches only settled verdicts).

### 2.1 FINAL per-language table (passes 1–4 complete, 2026-08-05; adjudication overlays D-064 applied)

| language | PASS | FAIL (label) | INFEASIBLE (rig) | feed defect (adjudicated) | **usable** | Wilson 95% CI |
|---|---:|---:|---|---:|---:|---|
| **python** | 6 | 2 | 2 (crash: keras/TF AVX) | 0 | **6/10** | [0.31, 0.83] |
| **go** | 4 | 4 | 2 (time: kyverno; crash: envoy-gateway, `fatal error: fault` ×3 runs, D-064.2 rerun) | 0 | **4/10** | [0.17, 0.69] |
| **cs** | 0 | 9 | 1 (time) | 0 | **0/10** | [0.00, 0.28] |
| **cpp** | 2 | 4 | 2 (time) | 2 (D-064.1: DXC, esphome) | **2/10** | [0.06, 0.51] |
| **java** | 1 | 9 | 0 | 0 | **1/10** | [0.02, 0.40] |
| **rust** | 0 | 7 | 2 (time) + 1 pending¹ | 0 | **0/10** | [0.00, 0.28] |

¹ `harper-2962`: machine ERROR; **proposed** `platform_infeasible(emulation-spawn)` —
cargo-nextest `__double-spawn: No such file or directory` under QEMU (build
succeeded; evidence committed). Classification with the supervisor; usable
count unaffected. Note also: rust/cs FAIL rows are dominated by "F2P not
reported despite large parsed suites" (harper-2973 108/111 missing of 4742
parsed; gleam-5482 1552/1558 missing of 3757) — consistent with feed-side
record/parser name inconsistency; refining FAIL→eval_harness_failure would
not change any admission outcome, so it is recorded, not pursued.

Pilot comparator (JS/TS): 5/17 ≈ 29% [0.13, 0.53]. Screen cost: container
time only, **0 sessions**.

### 2.2 Supply picture (§2.5) — own-harvest evidence table (for D-028c re-ratification)

Under the proposed admissions (python + go; JS/TS already validated), with the
pilot defect yield 0.40 (2/5; 95% CI [0.12, 0.77]) composed on measured
usable rates:

| source | pool (post-gate) | usable rate (measured) | E[screen-PASS] | E[defects] |
|---|---:|---:|---:|---:|
| SWE-rebench python | 110 | 0.60 | 66.0 | 26.4 |
| MultiLang go | 66 | 0.40 | 26.4 | 10.6 |
| MultiLang js/ts | 39 | 0.29 (pilot) | 11.5 | 4.6 |
| **TOTAL admitted** | **215** | | **103.9** | **41.5** |
| (cpp if admitted) | +53 | 0.20 | +10.6 | +4.2 → 45.8 |

**Reading: expected defect supply from admitted external feeds is ~41.5 <
n_max = 44 even if every admitted post-gate row is screened** (yield-CI range
~12–80 — dominated by the 5-row pilot yield sample). The §2.5
demonstrated-insufficiency condition is met on point estimates; per D-062 the
under-running/own-harvest path was already declared the likely one. This
table is the §2.5 evidence table for the supervisor's D-028c own-harvest
re-ratification decision.

## 3. Pool fix + selection ordering (D-056) — execution step 2

PENDING step-1 admissions. Will record: admitted languages, the frozen pool
(per-language post-gate counts at freeze time), the full D-056 ordering
(`created_at` ASC, ties `instance_id`→source), all seeds (repeat draw, A1
subsample per D-061 — seeds recorded before use), and the identity pull.

## 4. Session log pointers — execution step 3

PENDING. Sessions per the ratified design: 15/week sizing, surplus ≤30 logged
(D-057), alternation per §1, D-058 stop protocol standing. Mandatory data-freeze
checkpoint at every look (m = 4/8/12/16) per prereg §4.8; manifests will be
committed under `results/step3/looks/`.

## 5. Skip trail

Accrues from step 2 onward: every skipped/replaced/infeasible case with its
D-049 classification, in order, so the realized pool is reconstructible against
the declared ordering.
