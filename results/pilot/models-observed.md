---
name: models-observed
description: Per-position, per-arm runtime-reported model IDs from the P1 session logs (D-012 field-study requirement — "which models actually ran" is a reported result, not an assumption). Includes subagent models where the CLI delegated.
status: active
---

# Models observed — P1 (D-012 requirement)

Compiled from `results/pilot/sessions.jsonl` `reported_models` fields. Under
D-012 the study runs auto-updating subscription CLIs and pins nothing; **which
models actually ran is a reported result.** Claude Code reports **both** the
main model and any **subagent model it delegated to** — both are recorded.

| pos | arm | family | models observed (runtime-reported) |
|---|---|---|---|
| 1 | author+A1 | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 1 | A1 | anthropic | claude-opus-4-8[1m] |
| 1 | A2 | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 1 | B | openai | codex-cli default (**GPT-5.6 Sol inferred**, see gap) |
| 2 | author+A1 | openai | codex-cli default (**GPT-5.6 Sol inferred**) |
| 2 | A1 | openai | codex-cli default (**inferred**) |
| 2 | A2 | openai | codex-cli default (**inferred**) |
| 2 | B | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 3 | author+A1 | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 3 | A1 r1 | anthropic | claude-opus-4-8[1m] |
| 3 | A2 r1 | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 3 | A2 r2 | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 3 | B r1 | openai | codex-cli default (**inferred**) |
| 3 | B r2 | openai | codex-cli default (**inferred**) |
| 5 | author+A1 | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 5 | A1 r1 | anthropic | claude-opus-4-8[1m] |
| 5 | A2 r1 | anthropic | claude-opus-4-8[1m] + claude-haiku-4-5 (subagent) |
| 5 | B r1 | openai | codex-cli default (**inferred**) |

## Observations for the write-up

1. **Anthropic stack is a two-model system as operated.** Claude Code runs
   `claude-opus-4-8[1m]` as the main model and **delegates subtasks to
   `claude-haiku-4-5`**. The "Anthropic reviewer" is therefore an
   opus+haiku *stack*, not a single model — exactly the "vendor stack, not
   model" framing D-012/§8 commits to. Reported, not hidden.

2. **D-012 FIDELITY GAP — OpenAI arm model ID is inferred, not runtime-emitted.**
   `codex exec --json` does **not** emit a resolved model ID in its event
   stream, so the OpenAI arm's model ("GPT-5.6 Sol") is **inferred from the
   OQ-9 evidence table** (the codex-cli default at pilot time), **not**
   runtime-reported per session. This is a real gap against D-012's
   "runtime-reported model ID + harness version logged per session"
   requirement — recorded honestly. **Remediation candidate for the main
   study:** probe the codex config/session for the resolved model
   (`codex` may expose it via `--config`/session metadata) and assert a
   non-inferred ID per session, or pin+record via API replication (§7).
   Until then the OpenAI model ID is a documented inference, and any
   mid-study codex-default change would be **invisible** to the per-session
   log — the exact drift D-012 exists to catch, currently uncatchable on the
   OpenAI side.

3. **No within-P1 version drift observed** in the reported IDs (CLI *versions*
   drifted P0→P1 per the log; the model IDs above are stable across P1). The
   judge stack has not run yet (no Band 2 traffic), so no judge-model
   discontinuity check (D-019) has been triggered.
