# cross-vendor-review-eval

**A benchmark for the review-routing question: when an AI agent writes code and
misses a bug, who actually *finds* it — the author, the same model with fresh
eyes, or an agent from a different vendor?**

Recent work established that AI models go easy on their own outputs
(self-attribution bias, arXiv:2603.04582; silent self-endorsement of defects,
arXiv:2605.21537). This benchmark measures what that means **in practice**: the
**catch-rate** (did the reviewer localize the real defect — file and line?) and
**false-alarm rate** of **agentic reviewers** (Claude Code, Codex CLI) on
**AI-authored, test-confirmed** defects, under a three-way authorship
manipulation. Detection, not repair; mechanical scoring first, with a blinded,
human-audited judge panel only where coordinates can't decide.

> Companion repo: `meta-layer-starter` (link on publish) — a full operating layer
> for supervised, multi-vendor agent development (review protocols, pre-ship gates,
> supervision rules, design/persona templates). Cross-vendor review is that layer's
> load-bearing premise; this benchmark prices that premise as an engineering
> decision.

**Methodology: Maxim St-Hilaire.** Every design choice is dated and justified in
[`docs/DECISIONS.md`](docs/DECISIONS.md) — including the prior-art scan that
repositioned v0.1 (D-009).

---

## The question, in one paragraph

Two 2026 papers showed the phenomenon: a model reviewing its own work is
measurably blind to its own defects, and the blindness sits on the "reviewing
yourself" diagonal. But nobody has measured the version engineering teams need:
with real agentic review harnesses, on genuinely AI-authored bugs confirmed by
hidden tests, **does routing review to a second vendor catch more real defects
than a fresh look from your own model — and at what false-alarm cost?** That is
the routing decision this benchmark prices.

## How it stays honest

- **No planted bugs.** Agents attempt real, recent tasks and fail naturally;
  hidden test suites — not humans, not models — confirm which attempts are broken.
- **Reviews happen before the tests are revealed.** At review time nobody knows
  whether the change is broken. Hindsight cheating is impossible.
- **Three-way, fully blind comparison.** (A1) author reviews own work in-session;
  (A2) same model, brand-new session; (B) different-vendor agent, cold. No
  reviewer is ever told who wrote the code.
- **Mechanical-first, three-band scoring.** Reviewers must name file + line;
  claims are matched to ground-truth fix locations by coordinates wherever
  possible (no model in the loop). Residual cases go to a vendor-anonymized
  judge panel from ≥2 model families; a pre-registered human-audited sample
  validates the judges (κ reported).
- **A field study of shipped stacks.** Sessions run on the auto-updating
  subscription CLIs practitioners actually use; every session logs its
  runtime-reported model + harness version, conditions are interleaved within
  every batch, and version drift is analyzed as a recorded covariate. A
  version-pinned API replication is the named follow-up.
- **False alarms count.** Every condition also reviews known-correct changes —
  crying wolf is measured, not free.
- **Symmetric pairing.** Both directions (Claude authors / Codex reviews, and the
  reverse), so no vendor is flattered by design.
- **Contamination is a first-class constraint.** Tasks postdate every evaluated
  model's training cutoff (a memorized bug proves recall, not review).

## Status

| | |
|---|---|
| **Phase** | v0.1 — scope locked 2026-07-15; build complete, Step 2a accepted 2026-07-18 (real canaries 4/4); **pilot not yet authorized** |
| **Corpus** | Recency-gated SWE-bench-style tasks (source fixed at pilot; SWE-bench Lite as-is rejected for contamination) |
| **Vendors** | Anthropic (Claude Code) ↔ OpenAI (Codex CLI) — shipped subscription CLIs, versions logged at runtime |
| **Next step** | Pilot protocol proposal under supervisor review (`docs/pilot-protocol.md`); pilot go/no-go is a separate supervisor decision |

## What's here

```
README.md                     ← you are here
LICENSE                       ← MIT
docs/experiment-design.md     ← the full v0.1 design: claim, prior art, conditions, scoring,
                                contamination protocol, power/budget, threats to validity
docs/DECISIONS.md             ← dated rationale for every methodological choice
harness/                      ← (empty) the pipeline code lands here
data/                         ← (empty) task sets + per-run records
results/                      ← (empty) catch-rate / false-alarm tables and writeup
```

## Definition of done (v0.1)

A recency-gated corpus; three blind review conditions with agentic reviewers; one
honest catch-rate + false-alarm number per condition with paired confidence
intervals; every methodological choice pre-registered and held to.

---

*Positioning against arXiv:2603.04582, 2605.21537, and 2603.26130 (SWE-PRBench)
is detailed in `docs/experiment-design.md` §2.*
