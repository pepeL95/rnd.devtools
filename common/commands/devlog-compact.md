# devlog-compact

Triage and compact `devlog/` into durable technical memory.
Primary outcome: `devlog/` must be leaner after triage (less noise, less duplication, same or better decision coverage).

## What devlog is for

- Preserve important engineering context that should survive a session.
- Capture decisions, blockers, TODOs, outcomes, and constraints that affect future work.
- Exclude routine chatter, duplicate status updates, and low-value recap.

## Scope

- Target directory: `devlog/`.
- Focus on housekeeping only: prune, update, reduce, merge.
- Do not rewrite technical facts; preserve decisions, dates, and outcomes.

## Non-negotiable outcome

- End state must be smaller and clearer than start state.
- Prefer reducing entry count and total text volume whenever safe.
- If no reduction is possible, explain exactly why and list blockers.

## Required behavior

1. Inventory entries in `devlog/` sorted by date in filename.
2. Baseline current size:

- Count files and total lines before edits.

3. Classify each entry:

- `keep`: still relevant and concise.
- `update`: stale metadata/status but still useful.
- `merge`: overlaps with another entry for same effort/time window.
- `prune`: duplicate, obsolete, or superseded with no unique value.

4. Compact aggressively but safely:

- Merge related short entries into one canonical entry.
- Replace repeated narrative with a tight summary.
- Keep links/paths to key artifacts (PRs, docs, scripts, runbooks).
- Prefer deleting or merging over lightly editing noisy entries.

5. Reconcile interconnected dependencies across entries:

- Cross-check blockers, TODOs, and statuses between related logs.
- If a blocker in one entry is resolved by work recorded in another entry, remove or mark it resolved.
- Collapse dependency chains into a single current status to avoid contradictory state.

6. Sync with active session progress:

- Review current session work (changes, completed steps, new decisions).
- Update affected devlog entries so status/blockers/next actions reflect latest reality.
- Add only verified progress; do not speculate.

7. Apply signal filter before keeping content:

- Keep only content that is actionable, specific, and evidenced by work/output.
- Prefer reusable patterns, decisions, and lessons over one-off narration.
- Drop filler, social commentary, and "what I did" text without technical consequence.

8. Ensure every kept/merged entry has:

- Date, scope, current status, decisions made, next actions.

9. Maintain traceability:

- When pruning or merging, add a short note in the surviving entry listing absorbed/removed filenames.

10. Verify leaner end state:

- Recount files and total lines after edits.
- Confirm net reduction in file count, line count, or both.
- If not reduced, provide a strict justification.

## Output format

- `Summary`: files scanned, kept, updated, merged, pruned.
- `Size delta`: files before/after, lines before/after, net reduction.
- `Changes`: per-file actions with one-line rationale.
- `Dependency updates`: blockers/TODOs/statuses updated due to other entries or active session progress.
- `Open follow-ups`: missing info or entries that need human confirmation.

## Guardrails

- Never delete entries with unique incident context, postmortems, or irreversible decisions.
- If uncertain, mark `needs-review` instead of pruning.
- Keep language concise; remove filler and repetitive status text.
- Do not fabricate outcomes or infer decisions not present in source entries.
