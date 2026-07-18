---
name: pilot-protocol
description: Step 2b pilot protocol PROPOSAL — session cadence, throughput measurement, quota-feasibility check, Band 3 card delivery flow. Paper only; zero execution until supervisor go.
status: draft
author: Maxim St-Hilaire (methodology owner) — drafted by worker for review
last-updated: 2026-07-18
---

# Pilot protocol — PROPOSAL (Step 2b)

**Standing state:** build complete (Step 2a accepted 2026-07-18, provenance
`f801371`); **pilot NOT authorized**. This document is a plan on paper. No
reviewer sessions run, no live-repo harvesting happens, until the supervisor's
explicit go. **Protocol review closed 2026-07-18:** scope and thresholds
ratified with amendments as **D-021**; the OQ-9 corpus process is ratified
with a pre-committed preference order (external verified feed > own-harvest).
The go/no-go itself remains open.

## 1. What the pilot must answer (from §7 and §9)

1. Does one recency-gated task flow end-to-end — author → hidden test →
   A1/A2/B agentic reviews → three-band scoring → (if escalated) Band 3 card?
2. What does a session actually cost in wall-clock and subscription headroom —
   i.e., **sustainable sessions/week** under real shared limits?
3. Is the free-tier Gemini quota feasible at expected Band 2 volume (D-019)?
4. Does the Band 3 card meet its acceptance criterion (rulable from the card
   alone)?
5. Which corpus source is ratified, and what is final n (§7 pre-registered
   rule)?

## 2. Phases

### P0 — single case, end to end (the §9 pilot core)

- One task from the candidate corpus (OQ-9 shortlist; supervisor ratifies the
  source before P0 starts — that ratification is a scheduled decision, logged
  as a D-entry).
- One authoring session (vendor per coin-flip recorded in advance in the
  brief), hidden-test confirmation, then A1 (in-session), A2 (fresh), B
  (cross-vendor) — scheduled by the interleaver even at n=1.
- Post-session: D-018 compliance scan on the reviewer transcript; scoring;
  secret-hygiene scan (`scan_artifact_for_secrets`) over every artifact
  destined for the repo; judge transcripts audited (D-020).
- **Gate:** if P0 fails mechanically (harness bug, not model behavior), fix
  and re-run P0 before P1; model-behavior surprises are data, not defects —
  logged, not patched around.

### P1 — small throughput batch (ratified, D-021)

- **5 tasks** through the full flow, spread over 3–5 calendar days at whatever
  pace the owner's real subscription usage tolerates. Rationale: 1 case cannot
  estimate variance or sessions/week; 5 gives a crude but honest rate at ~20
  sessions (5 × [1 author + 3 reviews]) without meaningfully denting weekly
  limits.
- **k=2 repeats on two tasks** — the second repeat executes **only if no
  limit-hit events have occurred by day 3**. Pre-registered, not
  discretionary (D-021a).
- Sessions interleaved per D-012; every limit-hit event logged (time, vendor,
  what was deferred).
- **Format-failed sessions (pre-registered before P0, D-021):** excluded and
  re-run, mirroring D-018's exclude-before-scoring-blind rule — never scored
  as empty claims. Per-vendor format-failure counts are a reported metric. A
  re-run that also fails format is recorded as **unscorable-format**,
  reported, never silently dropped.

## 3. Measurements & records

| Measure | How | Where it lands |
|---|---|---|
| Wall-clock per session | runner timestamps (already in SessionRecord) | `results/pilot/sessions.jsonl` |
| Sustainable sessions/week | **min(observed × 7 × 0.7, owner-declared normal-week ceiling)** — ceiling declared at pilot go; pilot days are atypically dedicated (ratified, D-021b) | pilot report |
| Run-to-run variance | k=2 repeat on **two** of the 5 P1 tasks; second conditional on zero limit-hits by day 3 (ratified, D-021a) | pilot report |
| Gemini quota feasibility | record free-tier daily request cap observed; feasible iff full-run Band 2 pace ≤ **50%** of daily cap (ratified, D-021c); else D-019 fallback triggers | pilot report |
| Judge model stability | resolved model per verdict (already captured); any change → D-019 discontinuity check (agreement rates before/after) | provenance + write-up |
| D-018 exclusions / D-020 invalidations | compliance scans per session | per-vendor counters |
| Claim-format failure rate | `claim_format_error` fields, per vendor | pilot report; escalate if **any single vendor >20% or aggregate >30%, whichever first** (ratified, D-021d); prompt is NOT edited unilaterally (OQ-3 pin) |

## 4. Band 3 card delivery flow

1. Escalations and the pre-registered audit sample render to
   `results/band3/cards-<batch>.html` (self-contained; blindness-linted at
   render — fails closed).
2. Worker notifies the supervisor in chat with the file path and case count —
   never the card contents inline (cards are the blind instrument; chat is
   not).
3. Supervisor rules in-browser, exports `band3-rulings.json`, drops it at
   `results/band3/`; worker ingests, records rulings, computes human–judge κ.
4. **Acceptance check rides along:** any card the supervisor cannot rule from
   the card alone is logged as an interface defect (D-014 criterion) and
   fixed before the next batch; the defect count is itself reported.
5. Secret-hygiene scan runs on every card file before commit (release gate).

## 5. Abort / escalate criteria (pilot-scoped)

- Harness defect discovered mid-P1 → pause sessions, fix, log; resume same
  task list (no silent task swaps).
- Any evidence of ground-truth breakage (e.g., a "defective" patch that
  inspection shows passed hidden tests) → stop, log, escalate — touches §6.
- Subscription interference with the owner's other work at P1 pace → stop,
  report observed ceiling, propose reduced cadence.
- Anything requiring a design-doc change → DECISIONS.md open question first.

## 6. Pilot deliverable

One pilot report (`results/pilot/report.md`): measured throughput + variance,
quota feasibility verdict, corpus source ratified + harvest evidence, Band 3
acceptance outcome, compliance counters, and the **final-n computation per
§7's pre-registered rule** — ending in a go/no-go recommendation for Step 3
that the supervisor decides.
