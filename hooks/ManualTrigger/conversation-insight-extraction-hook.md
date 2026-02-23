# High-Signal Conversation Insight Extraction

## Objective

Extract only actionable, non-obvious signals that improve future technical execution.

This is not a recap.
This is not sentiment logging.
This is not style/tone preference collection.

## Scope

Use only evidence present in the current conversation.
Do not infer personality traits or invent preferences.
Every insight must be traceable to explicit user statements, corrections, acceptance/rejection patterns, or observed outcomes.

## Hard Filters (Drop Anything That Fails)

Keep an item only if it is:

1. Actionable: changes implementation, planning, validation, or communication decisions.
2. Specific: tied to concrete constraints, tools, architecture, workflows, or quality bars.
3. Non-trivial: not generic engineering common sense.
4. Supported: has direct evidence in this conversation.

Reject:

- Tone/style likes/dislikes unless they affect deliverable acceptance.
- One-off logistics with no future value.
- Reworded summaries of what was already done.
- Vague claims without evidence.

## Extraction Pipeline

1. Identify evidence units:

- explicit requirements
- corrections/rejections
- repeated asks
- success/failure outcomes
- risk concerns

2. Convert evidence into candidate insights:

- constraint insights
- workflow insights
- quality-bar insights
- failure-pattern insights
- success-pattern insights

3. Score each candidate (0-2 each):

- Impact: does this materially change future outcomes?
- Reusability: likely to matter beyond this exact task?
- Confidence: strength of evidence from this conversation?

4. Keep only candidates with total score >= 5.

5. Merge duplicates and produce final, concise insights.

## Output Format (Required)

Return exactly these sections:

### 1) Lessons Learned

Bullets. Each bullet must include:

- `insight`: one sentence
- `why_it_matters`: one sentence
- `evidence`: short quote or paraphrase with turn context
- `confidence`: High | Medium | Low

### 2) Successes to Repeat

Bullets with:

- `pattern`
- `observed_result`
- `reuse_rule`

### 3) Failures / Friction to Avoid

Bullets with:

- `failure_pattern`
- `impact`
- `prevention_rule`

### 4) Durable User Preferences (Technical Only)

Include only preferences that affect technical output acceptance (e.g., file placement, format strictness, validation expectations, execution style).
For each item:

- `preference`
- `evidence`
- `how_to_apply_next_time`

### 5) Operating Rules Update Proposal

Propose 3-7 candidate rules for future turns:

- `rule`
- `rationale`
- `trigger`

## Quality Bar

Before finalizing, verify:

- No fluff, no social commentary, no generic advice.
- Every item has evidence.
- Insights are short, concrete, and decision-useful.
- Total items are limited to the highest-signal set (prefer 5-12 total across sections).

If high-signal evidence is insufficient, output:
`Insufficient signal for durable insight extraction from current conversation.`
