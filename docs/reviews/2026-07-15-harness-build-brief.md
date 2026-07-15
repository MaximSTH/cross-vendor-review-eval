# Session brief — harness build review (D-014 gate)

**Artifact under review:** the build-phase harness of `cross-vendor-review-eval`
— everything under `harness/`, `canary/`, `tests/` at commit `608ec8b`.

**Scope claims (what this code is supposed to do):**

1. **Three-band scoring** per design doc §5: Band 1 deterministic file+line
   matching (±5 primary, ±1/±10 sweep, D-016 cap k=5 ranked-as-submitted);
   Band 2 blinded judge panel with per-case rotation excluding the claim
   author's family (D-015); Band 3 self-contained adjudication cards, blind to
   authorship end to end, failing closed on identifier leaks.
2. **D-015 binding condition:** judges receive exactly the anonymized claim +
   answer-key annotation, nothing else (structural test).
3. **Session runner** (no real sessions until pilot): runtime version logging
   per D-012, stdin prompt, structured-claim extraction, format errors recorded
   not raised, raw transcripts out-of-band.
4. **Scheduler:** author-first ordering, no same-arm blocks (D-012 interleaving).
5. **Corpus intake:** recency gate on the max cutoff, star cap, deterministic
   oldest-first selection, no silent drops.
6. **Canary suite:** 4 fixtures exercising every band; mock judges validate
   routing/blinding; real-backend re-run pending OQ-4/OQ-5.

**Out of scope for this review:** the design doc's methodology choices (locked
via DECISIONS.md D-001..D-016), pilot-gated corpus source, prompt wording (OQ-3
with supervisor).

**Known open items (do not re-report):** OQ-3 prompt ratification; OQ-4 canary-4
real-mode criterion; OQ-5 Google judge execution blocked; `JUDGE_CMDS["google"]`
flags unverified pending OQ-5.
