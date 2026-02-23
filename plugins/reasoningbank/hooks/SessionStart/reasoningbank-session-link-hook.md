# SessionStart Hook - Reasoningbank Session Link

Ensure reasoningbank entries are linked to a single active session key.

## Objective
Initialize and maintain deterministic session scoping so SessionEnd can evaluate only relevant contenders.

## Steps
1. Ensure `.deliverables/reasoningbank/` exists.
2. Ensure `.deliverables/reasoningbank/.current-session` contains a non-empty session key.
3. If missing/empty, create a new key with format `yyyy-mm-ddthh-mm-ssz-<shortid>` and write it to `.current-session`.
4. Ensure `.deliverables/reasoningbank/sessions/{session-key}/` exists.

## Usage Notes
- Keep one active session key per session.
- Reasoningbank entries for this session must be written under `.deliverables/reasoningbank/sessions/{session-key}/`.
- Do not backfill or reassign previous-session entries during SessionStart.

No output required.
