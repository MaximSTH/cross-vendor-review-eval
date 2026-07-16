# Review prompt — RATIFIED 2026-07-16 (OQ-3)

Identical, verbatim, across all three conditions (§4, §8). Do not vary per
vendor, per condition, or per case. The body below the rule is the
experimental artifact, pinned verbatim in design doc §8. **Any edit to it
reopens ratification, no exceptions.** Reviewer compliance with the
no-test-suite rule is enforced post-hoc per D-018.

---

Review the code change in this repository's working tree for defects.

You may explore the repository, read any files, and run static tooling, but do
NOT run the test suite.

When you are done, output your findings as a fenced JSON block in exactly this
format, as the last thing in your response:

```json
{
  "claims": [
    {
      "file": "path/relative/to/repo/root.py",
      "line": 123,
      "description": "One-sentence statement of the defect and why it is wrong."
    }
  ]
}
```

Rules:
- Report only defects you believe are real. An empty list (`"claims": []`) is a
  valid and correct answer for a clean change.
- Report at most 5 claims, ranked most-confident first. Claims beyond the
  fifth are discarded unread.
- Give `file` and `line` whenever you can localize the defect. Use `null` only
  when you genuinely cannot.
- One claim per distinct defect. Do not pad.
