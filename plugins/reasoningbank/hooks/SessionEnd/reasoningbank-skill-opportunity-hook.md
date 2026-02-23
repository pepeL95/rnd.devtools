# SessionEnd Hook - Reasoningbank Skill Opportunity Scan

At session end, review `.deliverables/reasoningbank/` and assess whether any **high-value** skill should be created from accumulated learnings.

## Objective

Identify only skill opportunities with strong expected reuse and clear execution benefit.

Default stance: **propose none** unless evidence is compelling.

## Inputs

- Files under `.deliverables/reasoningbank/` (if present)
- Current session context

If the directory is missing or empty, stop.

## Hard Gate (All Required)

Propose a skill only if all conditions are true:

1. Pattern repeats across entries or is likely to recur in this workspace.
2. Pattern is operational (workflow/decision/risk-control), not generic advice.
3. Encoding as a skill would reduce future errors/time materially.
4. Scope is stable enough to define triggers and steps.
5. Evidence quality is high (explicit outcomes/corrections, not vague notes).
6. Supporting entries include strong `RL Signal Score` values (prefer score >= 7/10).

If any condition fails, do not propose a skill.

## Rejection Bias

Reject candidates that are:

- One-off incidents
- Trivial fixes
- Tool-specific noise without durable value
- Purely stylistic/tone preferences
- Better handled as a rule tweak rather than a new skill

## Evaluation Process

1. Scan reasoningbank entries and cluster recurring patterns.
2. Score each cluster (0-2 each):

- Reuse frequency
- Outcome impact
- Implementation clarity
- Durability over time
- RL signal strength from supporting entries

3. Keep only clusters with score >= 8/10.
4. Compare survivors against "rule update" alternative.
5. Propose at most 1-2 skills per session; prefer 0.

## Output Format (Required)

Return exactly one of the following:

### Option A: No Skill Recommendation

`No high-value skill opportunities identified from reasoningbank at this session end.`

### Option B: Skill Opportunity Recommendations

For each recommendation:

- `name`: short hyphen-case skill name
- `problem`: recurring high-cost issue it solves
- `reusable_pattern`: what generalizable pattern is captured
- `trigger`: when this skill should activate
- `expected_roi`: concrete time/risk reduction rationale
- `evidence`: 2-4 entry filenames from `.deliverables/reasoningbank/`
- `rl_score_signal`: summarized score evidence from supporting entries (min/avg/max)
- `why_not_rule_only`: why a rule/hook update is insufficient
- `confidence`: High | Medium | Low

## Safety Constraint

This hook only identifies opportunities. It must not create skills automatically.
