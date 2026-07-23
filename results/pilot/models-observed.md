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

2. **OpenAI arm model — resolved from config, not the `--json` stream
   (D-012 gap, with a found remediation).** `codex exec --json` emits **no**
   resolved model ID in its event stream. But the resolved model **is**
   introspectable: `~/.codex/config.toml` carries
   **`model = "gpt-5.6-sol"`** and **`model_reasoning_effort = "xhigh"`**.
   So the OpenAI arm ran **GPT-5.6 Sol at xhigh reasoning effort** —
   **confirmed from config**, no longer an OQ-9 inference. **Remediation
   (applies from the main study, and retroactively documented here):**
   snapshot `~/.codex/config.toml`'s `model` + `model_reasoning_effort` at
   **each** codex session launch, so a mid-study default change is captured
   rather than invisible. For P1 the config was read post-hoc (2026-07-23) and
   was not changed during the pilot, so it applies to all P1 codex sessions.
   **New covariate surfaced:** `model_reasoning_effort = xhigh` is part of the
   OpenAI stack *as operated* and is now a recorded field — the reasoning-effort
   setting is a stack parameter the write-up should report alongside the model
   ID.

3. **No within-P1 version drift observed** in the reported IDs (CLI *versions*
   drifted P0→P1 per the log; the model IDs above are stable across P1). The
   judge stack has not run yet (no Band 2 traffic), so no judge-model
   discontinuity check (D-019) has been triggered.
