# Decision brief — cross-vendor AI code review pilot

*The formal report ([`report.md`](report.md)) remains the artifact of record; this one-page brief presents it in plain language for a first-time reader.*

We ran a small, careful test of an idea: when one AI writes a code fix, does a **different** AI reviewer catch the bugs the author missed? Here is what we found and the choice it puts in front of us.

---

## What we measured

*(A "session" = one AI run — either authoring a fix or reviewing one.)*

- **6 real coding tasks** taken all the way through — an AI wrote a fix, hidden tests judged it, and three reviewers examined it. **3 of the 6 fixes had a genuine, test-confirmed bug.**
- **In all 3 buggy cases, the reviewers missed the real bug.** They critiqued the change they were shown and overlooked the actual defect, which sat in a different part of the code. Using a *different* vendor's AI did not rescue this.
- **The automatic scorer credited 2 "catches." A human check found both were false** — one was a coincidence (right line, unrelated comment), one was backwards (it called the correct fix a mistake). Real catches: **0 of 2**.
- **The public task dataset we drew from was only ~29% usable** — of 17 tasks we inspected, 5 were sound; the other 12 were broken in five distinct ways (mislabeled tests, missing files, tests that don't run). A widely-cited "curated" source, unusable most of the time.
- **Sustainable pace is about 15 sessions per week**, and each confirmed bug costs roughly **5.5 sessions** to produce and review (only ~2 of every 5 authored fixes turn out buggy). That sets the price of any larger study.

## What it means

The headline is a caution, not a catch rate: an AI reviewer tends to **grade the change in front of it rather than hunt the underlying bug**, so its silence or approval is not evidence the bug is gone. Separately, the pilot exposed that a trusted benchmark source is mostly broken — a finding useful to anyone building on it. Both results are solid in *direction* even though the sample is small; what we do **not** yet have is a precise, powered number for how much cross-vendor review helps.

## The three choices

| Choice | What it costs | What gets published |
|---|---|---|
| **1. Full study** | ~900 sessions ≈ **60 weeks** at our pace — *or* about **$1.5k–4k** in API fees to run it faster on fixed model versions. | A complete paper with statistically powered catch-rate numbers for cross-vendor vs. same-vendor review. |
| **2. Lean study** | ~40 confirmed-bug cases ≈ **16 weeks** on our current subscriptions (no extra dollars) — **but requires a better task source**, since the current one can't supply enough usable tasks. | A paper answering the core question at moderate confidence, plus the two pilot findings. |
| **3. Publish now** | **Near zero** — no more runs. | A standalone practitioner write-up of what we already found; the code and data stay public. |

The two constraints pull the same way: our pace and the thin task supply mean the full study effectively needs **money**, the lean study needs a **bigger task source**, and publishing now needs **neither**.

## What stays true regardless of the choice

- **The two findings stand:** reviewers anchor on the diff and miss the real bug; and the benchmark source is ~29% usable. Both are already written up and publishable on their own.
- **The pipeline works** — it ran six tasks end to end, cleanly, and every step is recorded.
- **Everything is public** (open-source license), and we make **no claim about how widely AI code review is used** — only what this data shows.
