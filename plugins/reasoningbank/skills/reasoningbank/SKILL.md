---
name: reasoningbank
description: "Capture and persist only evidence-backed, high-signal learning data from the current reasoning trajectory/conversation to improve future agent behavior in this workspace: major lessons, critical failures, corrections, successful milestone patterns, and durable technical preferences. Trigger only at major learning milestones (explicit user correction, meaningful mistake/rework, or important success), never for routine/trivial tasks. Write structured entries to .deliverables/reasoningbank/sessions/{session-key}/ as mm-dd-yyyy-{short-name}.md so records are reusable as future RL-style training signals."
---

# Reasoningbank High Signal

Capture only evidence-backed insights that improve future technical execution.

## Operating Mode
- Run this skill autonomously at the end of non-trivial tasks.
- Run this skill after meaningful correction loops (rejection, rework, changed direction).
- Run this skill after notable wins (clear strategy that worked) or failures (preventable friction).
- Skip entry creation when signal is weak; do not force a log.

## Output Contract
- Write entries to `.deliverables/reasoningbank/sessions/{session-key}/`.
- File name must be `mm-dd-yyyy-{short-name}.md`.
- Track active session in `.deliverables/reasoningbank/.current-session`.
- Use `scripts/create_reasoningbank_entry.py` to resolve session key and generate the path/scaffold before writing.

## High-Signal Filter (Hard Gate)
Keep an item only if all are true:
1. Actionable: changes future implementation, planning, validation, or risk handling.
2. Specific: tied to concrete constraints/tools/workflows/quality bars.
3. Non-trivial: not generic best practice or boilerplate.
4. Evidenced: supported by explicit statements, corrections, or outcomes in this conversation.
5. Generalizable: captures a reusable pattern/approach that can transfer to similar future tasks.

Drop:
- Tone/style preferences that do not affect deliverable acceptance.
- One-off logistics with no likely reuse.
- Restatements of completed work.
- Vague claims without evidence.

## Extraction Workflow
0. Read `references/high-signal-rubric.md` before extracting; treat it as mandatory scoring/filter guidance.

1. Gather evidence units from the conversation:
- explicit requirements
- corrections/rejections
- repeated asks
- success/failure outcomes
- mistakes and recovery moves

2. Convert to candidate insights grouped by:
- lessons learned
- success patterns to repeat
- failure/friction patterns to avoid
- durable technical preferences
- candidate operating rules

3. Score each candidate 0-2 on:
- Impact
- Reusability
- Confidence

4. Keep only candidates with score >= 5.

5. Merge duplicates and keep total content tight.
6. Prefer correction/recovery patterns and approaches that can be reused in similar contexts.
7. Assign one entry-level `RL Signal Score` (0-10) based on impact, reusability, evidence strength, and durability.

## Required Entry Structure
Each entry must contain these sections in order:
1. Header metadata bullets: `Date`, `Source`, `Session Key`, `Entry ID`, `Signal standard`
2. `Context Snapshot`
3. `Lessons Learned`
4. `Success Patterns to Repeat`
5. `Failures / Friction to Avoid`
6. `Durable Technical Preferences`
7. `Rule Updates for Future Runs`
8. `RL Signal Score`
9. `Rejected Low-Signal Candidates`

For insight bullets in sections 3-7, include fields:
- `insight` (or `pattern`/`rule`)
- `why_it_matters`
- `evidence`
- `generalization` (how to reuse this on similar tasks)
- `confidence` (`High|Medium|Low`)

For section 8 (`RL Signal Score`), include:
- `score` (0-10)
- `breakdown`:
  - `impact` (0-2)
  - `reusability` (0-2)
  - `evidence_strength` (0-2)
  - `durability` (0-2)
  - `bonus` (0-2; use only for unusually high leverage)
- `rationale` (1-3 concise sentences)

## Quality Bar
- Prefer 5-12 total high-signal items across sections 2-6.
- No fluff, no social commentary, no generic advice.
- Every retained item must include evidence.
- Prioritize entries that preserve reusable patterns over one-off observations.
- `RL Signal Score` must be evidence-backed; inflate neither score nor rationale.
- If insufficient signal, create no entry and state: `Insufficient signal for durable insight extraction.` in normal response.
