#!/usr/bin/env python3
"""Create a session-linked reasoningbank entry scaffold with enforced naming.

Output path format:
.deliverables/reasoningbank/sessions/{session-key}/mm-dd-yyyy-{short-name}.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import uuid
from pathlib import Path


def normalize_short_name(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", raw.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    if not slug:
        raise ValueError("short-name must include at least one alphanumeric character")
    return slug[:80]


def parse_date(raw: str | None) -> str:
    if raw is None:
        return dt.date.today().strftime("%m-%d-%Y")
    try:
        parsed = dt.datetime.strptime(raw, "%m-%d-%Y")
    except ValueError as exc:
        raise ValueError("date must use mm-dd-yyyy") from exc
    return parsed.strftime("%m-%d-%Y")


def normalize_session_key(raw: str) -> str:
    key = re.sub(r"[^a-z0-9-]+", "-", raw.strip().lower())
    key = re.sub(r"-+", "-", key).strip("-")
    if not key:
        raise ValueError("session-key must include at least one alphanumeric character")
    return key[:120]


def generate_session_key() -> str:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dt%H-%M-%Sz").lower()
    return f"{ts}-{uuid.uuid4().hex[:6]}"


def resolve_session_key(base_dir: Path, explicit_key: str | None) -> str:
    session_file = base_dir / ".current-session"
    if explicit_key:
        session_key = normalize_session_key(explicit_key)
        session_file.write_text(f"{session_key}\n", encoding="utf-8")
        return session_key

    if session_file.exists():
        raw = session_file.read_text(encoding="utf-8").strip()
        if raw:
            return normalize_session_key(raw)

    session_key = generate_session_key()
    session_file.write_text(f"{session_key}\n", encoding="utf-8")
    return session_key


def build_template(title: str, date_str: str, session_key: str, entry_id: str) -> str:
    return f"""# {title}

- Date: {date_str}
- Source: conversation-state
- Session Key: {session_key}
- Entry ID: {entry_id}
- Signal standard: high-signal only

## Context Snapshot
- Task:
- Outcome:
- Trigger for capture:

## Lessons Learned
- insight:
  why_it_matters:
  evidence:
  generalization:
  confidence:

## Success Patterns to Repeat
- pattern:
  why_it_matters:
  evidence:
  generalization:
  confidence:

## Failures / Friction to Avoid
- pattern:
  why_it_matters:
  evidence:
  generalization:
  confidence:

## Durable Technical Preferences
- insight:
  why_it_matters:
  evidence:
  generalization:
  confidence:

## Rule Updates for Future Runs
- rule:
  why_it_matters:
  evidence:
  generalization:
  trigger:
  confidence:

## RL Signal Score
- score:
- breakdown:
  impact:
  reusability:
  evidence_strength:
  durability:
  bonus:
- rationale:

## Rejected Low-Signal Candidates
- candidate:
  rejection_reason:
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("short_name", help="Short descriptive name (will be slugified)")
    parser.add_argument("--date", help="Date in mm-dd-yyyy; defaults to today")
    parser.add_argument(
        "--session-key",
        help="Session key for grouping entries; if omitted, uses .current-session or creates one",
    )
    parser.add_argument(
        "--base-dir",
        default=".deliverables/reasoningbank",
        help="Reasoningbank root directory",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite file if it already exists",
    )
    args = parser.parse_args()

    date_str = parse_date(args.date)
    short_name = normalize_short_name(args.short_name)

    out_dir = Path(args.base_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    session_key = resolve_session_key(out_dir, args.session_key)
    entry_id = f"{date_str}-{short_name}"

    session_dir = out_dir / "sessions" / session_key
    session_dir.mkdir(parents=True, exist_ok=True)
    out_path = session_dir / f"{entry_id}.md"
    if out_path.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {out_path}")

    title = short_name.replace("-", " ").title()
    out_path.write_text(
        build_template(title, date_str, session_key=session_key, entry_id=entry_id),
        encoding="utf-8",
    )
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
