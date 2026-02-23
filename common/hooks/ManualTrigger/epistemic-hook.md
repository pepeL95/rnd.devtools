# ManualTrigger Hook - Recency-Weighted Insight Extraction

## Objective
Extract high-signal, evidence-backed learnings with strong bias toward what happened most recently before hook invocation, while linking prior conversation evidence when it materially strengthens generalization.

This is not a recap.
This is not sentiment logging.
This is not style/tone preference collection.

## Scope
Use only evidence in this conversation.
Do not infer personality traits or invent preferences.
Every retained item must be traceable to explicit user statements, corrections, rejections, or observed outcomes.

## Temporal Weighting (Required)
Treat the moment this hook is invoked as `t0`.

1. Define the **recent run window** as turns closest to `t0` (latest request + work loop + latest feedback).
2. Prefer insights from this window by default.
3. Link older evidence only when it confirms recurrence, strengthens confidence, or improves transferability.
4. Downweight older signals unless they are clearly repeated or causal.

Candidate scoring (0-2 each):
- `impact`
- `reusability`
- `confidence`
- `recency_weight` (2 = from recent run window, 1 = adjacent prior context, 0 = old/unrelated)

Keep only candidates with total score >= 6.

## Hard Filters (All Required)
1. Actionable: changes implementation/planning/validation/risk handling.
2. Specific: tied to concrete constraints, tools, workflows, or quality bars.
3. Non-trivial: not generic engineering advice.
4. Evidenced: direct conversational support exists.
5. Generalizable: reusable on similar future tasks.

Reject:
- Tone/style preferences unless they affect acceptance.
- One-off logistics with no transfer value.
- Restatements of completed work.
- Vague claims without evidence.

## Output Contract (Reasoningbank-Compatible)
When persisted to disk, use:
- `.deliverables/reasoningbank/sessions/{session-key}/mm-dd-yyyy-{short-name}.md`

Session key resolution (plugin optional):
1. If `.deliverables/reasoningbank/.current-session` exists and is non-empty, use it.
2. Else if reasoningbank generator script exists at `plugins/reasoningbank/skills/reasoningbank/scripts/create_reasoningbank_entry.py`, use it to create/resolve session key.
3. Else create fallback session key with format `yyyy-mm-ddthh-mm-ssz-<shortid>`, write it to `.deliverables/reasoningbank/.current-session`, ensure `.deliverables/reasoningbank/sessions/{session-key}/` exists, and write entry directly.

Write deliverable content using this exact structure:

1. Header metadata bullets: `Date`, `Source`, `Session Key`, `Entry ID`, `Signal standard`
2. `Context Snapshot`
3. `Lessons Learned`
4. `Success Patterns to Repeat`
5. `Failures / Friction to Avoid`
6. `Durable Technical Preferences`
7. `Rule Updates for Future Runs`
8. `RL Signal Score`
9. `Rejected Low-Signal Candidates`

For bullets in sections 3-7, include:
- `insight` (or `pattern`/`rule`)
- `why_it_matters`
- `evidence` (must cite whether from recent window vs prior linked context)
- `generalization`
- `confidence` (`High|Medium|Low`)

For section 8 (`RL Signal Score`), include:
- `score` (0-10)
- `breakdown`: `impact`, `reusability`, `evidence_strength`, `durability`, `bonus` (each 0-2)
- `rationale`

## Quality Bar
- Prefer 5-12 total high-signal items across sections 3-7.
- Prioritize recent-run learnings first; add older links only when they improve transfer value.
- No fluff, no social commentary, no generic advice.
- Every retained item must include evidence.

If signal is insufficient, output:
`Insufficient signal for durable insight extraction from current conversation.`
