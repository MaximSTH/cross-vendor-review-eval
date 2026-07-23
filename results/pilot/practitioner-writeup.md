---
name: practitioner-writeup
description: Branch-independent practitioner write-up of the pilot findings — diff-anchoring, the corpus-integrity taxonomy, and the mechanical-catch audit's validity result. Written to stand alone (the terminal-branch publishable piece; the backbone of the paper in the other branches).
status: draft
author: Maxim St-Hilaire
---

# When an AI reviewer grades the diff instead of finding the bug

*A small, careful pilot on cross-vendor AI code review — what it found, and
what it did not claim.*

## The question

AI code review is **advocated and publicly tooled** — this work grows out of
the `meta-layer-starter` operating layer, and it is motivated by two published
results on review bias: rating-based self-review blindness on SWE-bench
(arXiv:2603.04582) and ~31.7% silent self-endorsement of defective outputs
(arXiv:2605.21537). A load-bearing premise behind "route your review to a
*different* vendor" is that a cross-vendor reviewer catches defects the author
missed. This pilot tests that premise mechanically, on **AI-authored,
test-confirmed** defects, with **no LLM judge in the primary metric** — the
catch/no-catch decision is a deterministic file+line coordinate match against
the known defect location.

We make **no claim about industry adoption.** The practice is advocated and
tooled; whether teams use it is not something this data speaks to.

## The setup, briefly

An AI agent (Claude Code or OpenAI Codex, as shipped on consumer subscriptions)
authors a fix for a real, recent GitHub issue. A hidden test suite decides
whether the fix actually worked. Then three reviewers examine the change, blind
to authorship, with an identical bare prompt:

- **A1** — the same agent session that wrote the fix (self-review),
- **A2** — a fresh session of the same vendor (fresh eyes, same model),
- **B** — a fresh session of a *different* vendor (cross-vendor).

A reviewer "catches" the defect if it names the right file and line. That's it —
no semantic credit, no judge, by design.

**Scale caveat, stated up front:** this is a **pilot**. Six end-to-end cases
(one P0 + five P1), of which **three carried a confirmed defect**. Every number
below is reported with its n. Nothing here is an established rate; the value is
in the **patterns and the failure modes**, which are sharp even at small n.

## Finding 1 — "diff-anchoring": reviewers grade the change, not the bug

The clearest pattern, and the practitioner takeaway:

> **When the authored fix lands in a different location than the true defect,
> reviewers critique the change in front of them and miss the real bug
> elsewhere.**

All three confirmed-defect cases show it:

- **A credential leak** (an API key passed as a command-line argument, visible
  in the process list) appeared in **four** places in the code; the author fixed
  **one**. Both non-authoring reviewers commented on the one fixed spot — one
  flagged an unrelated error-handling nit at that line; the other argued the
  *correct* fix was itself a bug. **Neither pointed at the three unfixed
  locations.** A human audit ruled both "catches" as non-catches.

- **A stale-translation bug** lived in a React effect missing a dependency; the
  author fixed a **different file entirely**. All three reviewers critiqued the
  author's file. **None** located the real defect. Unanimous miss.

- In the earliest case, the author's patch was confirmed broken and **all three
  reviewers returned zero findings.** Unanimous miss.

The mechanism is consistent: an AI reviewer handed a diff tends to **evaluate
that diff** — is this change good? — rather than **hunt the defect** the change
was supposed to fix, when the defect sits outside what it was shown. For a team
routing review work, that is the caveat worth internalizing: a reviewer's
silence, or its approval of a change, is **not** evidence the underlying bug is
gone — especially when the fix and the bug are not in the same place.

We call this **diff-anchoring.** At this n it is a hypothesis, not a rate — but
it reproduced in every defective case we ran, across both vendor directions.

## Finding 2 — the mechanical "catch" can be empty, and you have to check

Because the primary metric is a coordinate match, a claim scores a **catch** if
its file+line fall near the defect — *regardless of what the claim says.* The
pilot pre-registered a human audit of every mechanical catch against a
**reader-actionability** standard: *would a busy engineer following this claim
actually find and fix the bug?*

**Result: both mechanical catches in the pilot failed the audit (0 of 2).**
Two named ways a coordinate-match can be hollow:

- **Coincidental localization** — a semantically-unrelated claim that happens
  to land on the right line (the error-handling nit above).
- **Inverted claim** — a claim at the right place that asserts the *correct*
  approach is the bug; following it would **reintroduce** the defect.

The lesson is methodological and transferable: **a localization-based catch rate
is an upper bound.** Coordinate matching is reproducible and bias-free — which
is exactly why it is the right primary metric — but it counts diff-anchoring
artifacts as catches. If you benchmark AI reviewers this way, you need a
validity layer (human audit, or a calibrated semantic check) to know how many
"catches" are real. In this pilot, at face value the catch rate was inflated by
**every** catch it recorded.

## Finding 3 — a curated benchmark feed was ~29% usable, in five distinct ways

To run the study we screened a recency-gated slice of a maintained,
externally-provenanced SWE-bench-style feed. To fill our handful of task slots
we walked **17 candidate tasks and found 5 usable — about 29%.** The
unusable majority failed in **five distinct, diagnosable ways**, four of them
defects in the *feed's own labels or artifacts*:

1. **Whole-suite mislabelling** — the entire test suite tagged as the "must now
   pass" set, with no "must still pass" set at all.
2. **Phantom test names** — the declared failing tests do not exist in the suite
   after the feed's own test patch is applied.
3. **Already-passing "failing" tests** — the tests that are supposed to fail
   before the fix already pass at the base commit, so there is no defect to
   confirm.
4. **Missing container images** — the declared Docker image 404s from the
   registry.
5. **Non-running test commands** — the shipped test command executes no tests
   (a missing runner; invalid flags; a failing pre-test typecheck).

(A sixth category — tasks that only fail to run under CPU emulation on Apple
Silicon — is **not** a feed defect; those run fine on native hardware and are
excluded rig-relatively.)

The transferable point: **a benchmark instance that "exists" in a dataset is not
a benchmark instance that runs and means what its labels claim.** We caught all
of these with a cheap admission screen — execute the task at its base commit and
verify that the declared-failing tests actually fail and the declared-passing
tests actually pass, *before* trusting any label. Any evaluation built on a
SWE-bench-derived feed that skips this step is, at some rate, scoring against
labels that do not hold. Ours held for 29% of what we screened.

We also drew a hard line worth stating: **we never repaired a task's broken test
command to make it run.** Repairing the oracle is authoring the benchmark — it
would manufacture a passing instance and destroy the task's status as an
independent artifact. A non-running task is a *recorded finding about the feed*,
not a task to fix into shape.

## What this pilot deliberately does not say

- It does **not** report a catch rate for cross-vendor vs same-vendor review —
  the confirmed-defect n (three) is far too small, and every mechanical catch
  it saw was an audit artifact. It reports the **direction and the mechanism**
  (diff-anchoring), not a number.
- It does **not** claim AI code review is or is not adopted by teams. The
  practice is advocated and publicly tooled; usage is out of scope.
- It does **not** generalize beyond JavaScript/TypeScript tasks, nor beyond the
  specific shipped vendor stacks and versions it logged (a Claude opus+haiku
  stack; an OpenAI GPT-5.6-Sol stack). It is a **field snapshot** of consumer
  tools as operated, not a pinned-model comparison.

## The takeaways a practitioner can use today

1. **Don't read reviewer silence — or reviewer approval of a change — as "the
   bug is fixed."** In every defective case here, reviewers anchored on the diff
   and missed a defect that lived elsewhere. Cross-vendor did not rescue this.
2. **If you score AI reviewers by whether they name the right location, audit a
   sample of the "catches."** A coordinate match can be a coincidence or an
   inverted claim; treat the raw catch rate as an upper bound.
3. **If you build on a SWE-bench-style feed, run an execution-based admission
   screen first.** A meaningful fraction of curated instances carry labels that
   do not survive running them. Do not repair the oracle to boost yield.

---

*Method, full decision log, and every session transcript are public
(MIT-licensed) at the project repository. Motivating prior art:
arXiv:2603.04582, arXiv:2605.21537, arXiv:2603.26130. This write-up states
findings at pilot scale with n reported throughout; it makes no adoption claim.*
