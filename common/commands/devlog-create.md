# devlog-create

Generate a devlog entry to synthesise the **important** changes made in this work session

## Core principles

- `Atomicity`: one entry = one coherent unit of work; cluster related changes together.
- `Compactness`: minimal text, maximum signal.
- `Development focus`: capture technical changes and their impact.
- `Dev-team centric`: assume competent peers; write for fast continuation.

Include when relevant: blockers, TODOs, next steps, temporary patches/workarounds (and removal conditions).

## Qualifying criteria for devlog entry (default: skip)

Do **not** create an entry for trivial or low-signal sessions.
Most work sessions should not produce a new devlog entry.

Create or update a devlog entry only if at least one is true:

- A non-trivial technical decision was made (design, API, data model, infra, or operational behavior).
- Module architecture changed in a meaningful way (new boundaries, responsibilities, interfaces, or flow), not incremental refactoring.
- A new module/component was introduced, or there was a major fix/security patch with system-level impact.
- A blocker was discovered or resolved, and the team needs updated TODOs/next steps.
- A significant risk, workaround, or dependency change affects delivery, reliability, or maintainability.
- The team must align on a cross-surface contract/integration (for example backend/frontend contract, schema changes, event payloads, auth flow).

## Atomicity and logical clustering

- Do not force the entire session into one entry.
- Do not create one entry per tiny change.
- Group items into one entry only when they share the same objective, scope, and outcome.
- Split into separate entries when work streams have different objectives, owners, risks, or integration contracts.
- If two changes can be reviewed, rolled back, or handed off independently, they should be separate atomic entries.
- If uncertain, prefer updating one existing related entry plus a short `Follow-up` note instead of creating multiple new entries.

## Output target

- Write to `devlog/YYYY-MM-DD--short-title.md`.
- If an entry for the same effort already exists, update it instead of creating a duplicate.

## Guardrails

- Do not invent outcomes or test results.
- Do not copy large terminal output into devlog.
- Prefer updating an existing related entry over creating fragmented logs.

## Entry structure

```markdown
---
title: {the tile of the devlog entry}
date: {current date}
author: agent
---

{The body of the devlog entry, following the guidelines provided in this document}
```
