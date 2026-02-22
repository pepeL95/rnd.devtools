# SessionStart Hook - Truth-Seeking Architectural Basis

You have entered an unfamiliar repository.

Your objective is to construct a minimal architectural basis - the smallest set of high-truth signals that allows you to reconstruct and navigate the system later.

Think in linear algebra terms:

- You are not mapping the entire space.
- You are identifying a basis.
- Each signal must expand your span.
- Redundant signals are discarded.
- Low-truth signals are ignored.

Your goal is not coverage.
Your goal is structural truth.

---

## Guiding Principle

At every step, ask:

> What inquiry would most increase my understanding of how this system actually works?

Prioritize:

- Mechanism over description
- Control flow over commentary
- Dependencies over prose
- Constraints over intentions
- Change patterns over static snapshots

Avoid curiosity-driven wandering.
Avoid completeness.
Avoid reading for narrative.

---

## Step 1 - System Shape

Determine:

- Primary language(s)
- Framework(s)
- Runtime/build system
- Entry point(s)
- Overall architectural style

Extract only structural identifiers and relationships.

---

## Step 2 - Structural Axes

Identify enough to answer:

- Where does execution begin?
- How does a request/event propagate?
- What are the main subsystems?
- How do they depend on each other?
- Where does core domain logic live?
- Where does data enter and exit?

Stop once you can trace system behavior at a high level without guessing.

---

## Step 3 - Intent & Evolution

Sample:

- README / AGENTS.md (if present)
- docs index
- Recent ~10-20 commits

Extract only:

- Stated purpose
- Architectural constraints
- Active change zones
- Stability vs volatility patterns

Do not summarize history.
Infer trajectory.

---

## Context Discipline

Only retain signals that:

- Reveal system invariants
- Define boundaries
- Explain coupling
- Clarify control flow
- Expose active change vectors

Discard:

- Implementation detail
- Repetition
- Decorative documentation
- Low-signal commentary

You are constructing a compact, truth-oriented mental model.

No output required.

Stop when you can reason about the system's behavior, boundaries, and likely evolution without additional browsing.
