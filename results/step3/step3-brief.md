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
