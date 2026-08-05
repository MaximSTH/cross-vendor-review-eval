---
name: practitioner-writeup
description: Branch-independent practitioner write-up of the pilot findings — diff-anchoring, the corpus-integrity taxonomy, and the mechanical-catch audit's validity result. Written to stand alone (the terminal-branch publishable piece; the backbone of the paper in the other branches).
status: draft
author: Maxim St-Hilaire
---

# When an AI reviewer grades the diff instead of finding the bug

*I ran a small, careful pilot on cross-vendor AI code review. Every "catch" my
metric recorded turned out to be hollow — and the reviewers missed every real
bug.*

## Start with one bug

An AI coding agent was asked to fix a real security issue in a real open-source
project: an API key was being passed on the command line, where any process on
the machine could read it. The same leak existed in **four** places in the
codebase. The agent fixed **one** of them.

Then three AI reviewers examined the change. One flagged an unrelated
error-handling nitpick — on the fixed line. Another argued that the *correct*
fix was itself a bug; following that advice would have put the leak back. The
third found nothing at all. **None of the three pointed at the three places
where the key was still leaking.**

Two of those reviewer comments landed on the right line of code, so a
naive scorecard would say the defect was "caught" twice. A human reading the
comments would say it was caught zero times.

That case is not an outlier. It is the pattern this pilot found, three times
out of three.

## The question I was testing

A popular idea in AI-assisted development goes like this: models are known to
be too kind to their own output, so route the review to a *different* vendor's
model — fresh eyes from a rival should catch what the author missed. Two recent
papers documented the self-kindness half of that idea (models rating their own
work too favorably; models silently endorsing their own defective outputs).
The routing half — does a second vendor actually catch more real bugs? — is the
premise I set out to test, on a small, honest scale.

**One claim I am not making:** I don't know how many teams actually do this
today. The practice is advocated and the tooling exists; adoption is out of
scope here.

## The setup, in plain terms

1. An AI agent — Claude Code or OpenAI's Codex, the ordinary consumer versions,
   as shipped — writes a fix for a recent, real GitHub issue.
2. A hidden test suite (which no agent ever sees or runs) decides whether the
   fix actually worked. This is the ground truth.
3. Three reviewers then examine the change, without being told who wrote it,
   all given the same one-paragraph instruction — review this change, report
   any defect with its file and line:
   - **A1 — self-review:** the same session that wrote the fix looks it over.
   - **A2 — fresh same-vendor:** a brand-new session of the *same* vendor's
     tool.
   - **B — cross-vendor:** a brand-new session of the *other* vendor's tool.
4. A reviewer scores a "catch" if it names the right file and roughly the right
   line. Nothing else counts. No AI judges the answers; it's a coordinate
   match against the known defect location — deliberately dumb, deliberately
   reproducible, immune to any accusation of judge bias.

**What the reviewers did *not* get matters as much as what they got.** This
project grew out of a supervision framework I build and use
(`meta-layer-starter`), but none of that framework was in the loop here. No
special prompts, no briefs, no protocols, no scaffolding — the reviewers were
bare, stock CLI tools given one short instruction, identical across all three
arms. My harness only did logistics: pick the tasks, apply the patch, collect
the answers, grade them against the hidden tests. It's the exam proctor, not
the exam. If you install the same tools and ask them to review a change, you
are running this experiment.

**Scale, stated up front:** this is a pilot. Six end-to-end cases, of which
**three carried a confirmed defect**. Every number below comes with its n.
Nothing here is an established rate; the value is in the patterns and the
failure modes, which are sharp even at this size — and in the fact that every
transcript, decision, and script is public, so anyone can rerun it.

## Finding 1 — "diff-anchoring": reviewers grade the change, not the bug

The clearest pattern, and the practitioner takeaway:

> **When the fix lands in a different place than the actual bug, reviewers
> critique the change in front of them and miss the real bug elsewhere.**

All three confirmed-defect cases showed it:

- **The credential leak** above: four leak sites, one fixed. Both non-authoring
  reviewers commented on the fixed site; neither found the other three.
- **A stale-translation bug** in a React app: the real defect was an effect
  hook missing a dependency in one file; the author "fixed" a *different file
  entirely*. All three reviewers critiqued the author's file. None located the
  real defect. Unanimous miss.
- **The earliest case:** the author's patch was confirmed broken by the hidden
  tests, and all three reviewers — including the rival vendor — returned zero
  findings. Unanimous miss.

The mechanism is consistent. Hand an AI reviewer a diff and it tends to answer
"is this change good?" rather than "is the bug this change was supposed to fix
actually gone?" — and those are different questions precisely when the fix is
incomplete or in the wrong place, which are among the most dangerous defect
shapes a team can ship.

I call this **diff-anchoring**. At this sample size it is a hypothesis, not a
rate — but it reproduced in every defective case, in both vendor directions,
and cross-vendor review did not rescue it. Whether richer review instructions
or supervision scaffolding *can* rescue it is exactly the follow-up this result
motivates; this pilot tested the floor — the bare tools as shipped — on
purpose.

## Finding 2 — a "catch" on paper can be empty, and you have to check

Because the official metric is a coordinate match, a reviewer comment scores a
catch whenever its file and line land near the defect — *regardless of what
the comment actually says.* Knowing that, I pre-committed to a human audit of
every mechanical catch, with one question: **would a busy engineer who read
this comment actually find and fix the bug?**

**Result: both mechanical catches in the pilot failed the audit — 0 of 2.**

Two named ways a coordinate match can be hollow, both observed:

- **Coincidental localization** — a comment about something unrelated that
  happens to sit on the right line (the error-handling nitpick above).
- **Inverted claim** — a comment at the right place arguing that the *correct*
  approach is the bug; following it would reintroduce the defect.

The transferable lesson: **a location-based catch rate is an upper bound.**
Coordinate matching is the right primary metric — reproducible, no AI judging
AI — but it counts diff-anchoring artifacts as successes. If you benchmark AI
reviewers this way (and most current benchmarks do something like it), you need
a validity layer — a human audit of a sample, at minimum — to know how many of
your "catches" are real. In this pilot, at face value, the catch rate was
inflated by every single catch it recorded.

## Finding 3 — a curated benchmark feed was ~29% usable, in five distinct ways

To get real tasks, I used a maintained, publicly distributed SWE-bench-style
dataset: real GitHub issues, each shipped with a container image, the official
fix, and labels saying which tests should fail before the fix and pass after.
Before trusting any task, I ran a cheap admission screen — execute the task at
its starting commit and check that the labels are actually true.

**Of 17 candidate tasks screened, 5 were usable — about 29%.** The rest failed
in five distinct, diagnosable ways, four of them defects in the dataset's own
labels or artifacts:

1. **Whole-suite mislabelling** — the entire test suite tagged as
   "should-fail-before-fix," with nothing in the "should-still-pass" set.
2. **Phantom test names** — the declared failing tests don't exist in the
   suite at all.
3. **Already-passing "failing" tests** — tests that are supposed to prove the
   bug exists already pass before any fix, so there is no confirmable defect.
4. **Missing container images** — the declared Docker image simply isn't in
   the registry anymore.
5. **Non-running test commands** — the shipped test command executes zero
   tests (missing test runner, invalid flags, a broken pre-test step).

(A sixth category — tasks that only fail under CPU emulation on Apple Silicon —
is my rig's limitation, not the dataset's, and was tracked separately.)

The transferable point: **a benchmark task that "exists" in a dataset is not a
benchmark task that runs and means what its labels claim.** The screen that
caught all of this is cheap — run the tests once before believing the labels.
Any evaluation built on a SWE-bench-derived feed that skips that step is, at
some unknown rate, scoring against labels that don't hold.

One line I refused to cross, worth stating as a principle: **I never repaired a
broken task to make it run.** Fixing a dataset's broken test command is
authoring the benchmark — it manufactures a passing instance and quietly makes
the dataset grade *your* work instead of the model's. A task that won't run is
a finding about the dataset, not a task to fix into shape.

## What this pilot deliberately does not say

- It does **not** report a catch rate for cross-vendor vs. same-vendor review.
  Three confirmed defects is far too few, and every mechanical catch observed
  was a scoring artifact. It reports a direction and a mechanism
  (diff-anchoring), not a number. A pre-registered sequential study to put a
  number on it is underway; its full design is public in the same repository.
- It does **not** claim teams do or don't use cross-vendor review. Out of
  scope.
- It does **not** generalize beyond the JavaScript/TypeScript tasks it ran, nor
  beyond the specific shipped tools it logged (a Claude Opus-class stack; an
  OpenAI GPT-5.6 stack). It is a field snapshot of consumer tools as actually
  operated — not a pinned-model laboratory comparison, and that is a feature:
  it's the configuration practitioners actually run.

## The takeaways you can use today

1. **Don't read reviewer silence — or reviewer approval of a change — as "the
   bug is fixed."** In every defective case here, reviewers anchored on the
   diff and missed a defect living outside it. A second vendor did not change
   that. Tests, not reviews, caught every real defect in this pilot —
   instantly.
2. **If you score AI reviewers by whether they name the right location, audit
   a sample of the "catches" by hand.** A coordinate match can be a
   coincidence or an actively misleading claim. Treat any raw catch rate as an
   upper bound until audited.
3. **If you build anything on a SWE-bench-style dataset, run an
   execution-based admission screen first** — and never repair the tasks to
   boost your yield. A meaningful fraction of curated instances carry labels
   that do not survive being run.

---

*Every method decision, session transcript, and script behind this pilot is
public (MIT-licensed) in the project repository, including the pre-registered
design of the follow-up study. Motivating prior work: arXiv:2603.04582,
arXiv:2605.21537, arXiv:2603.26130. Findings are stated at pilot scale with n
reported throughout; no adoption claims are made.*

*Maxim St-Hilaire is a Staff Product Manager who builds and operates
production agentic workflows; this pilot grew out of the supervision layer he
maintains for multi-vendor AI development.*