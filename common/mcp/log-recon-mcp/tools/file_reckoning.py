"""File reckoning tool for bounded large-file exploration."""

from __future__ import annotations

import re
from collections import deque
from pathlib import Path
from typing import Literal

from mcp_app import mcp


def _ensure_file(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    if not p.is_file():
        raise ValueError(f"Path is not a file: {p}")
    return p


def _head_lines(path: Path, *, max_lines: int, encoding: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding=encoding, errors="replace") as f:
        for idx, line in enumerate(f, start=1):
            rows.append({"line": idx, "text": line.rstrip("\n")})
            if len(rows) >= max_lines:
                break
    return rows


def _tail_lines(path: Path, *, max_lines: int, encoding: str) -> list[dict[str, object]]:
    lines: deque[tuple[int, str]] = deque(maxlen=max_lines)
    with path.open("r", encoding=encoding, errors="replace") as f:
        for idx, line in enumerate(f, start=1):
            lines.append((idx, line.rstrip("\n")))
    return [{"line": ln, "text": txt} for ln, txt in lines]


def _range_lines(
    path: Path,
    *,
    start_line: int,
    end_line: int,
    max_lines: int,
    encoding: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding=encoding, errors="replace") as f:
        for idx, line in enumerate(f, start=1):
            if idx < start_line:
                continue
            if idx > end_line:
                break
            rows.append({"line": idx, "text": line.rstrip("\n")})
            if len(rows) >= max_lines:
                break
    return rows


def _search_lines(
    path: Path,
    *,
    query: str,
    regex: bool,
    ignore_case: bool,
    before: int,
    after: int,
    max_matches: int,
    encoding: str,
) -> list[dict[str, object]]:
    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(query, flags) if regex else None
    before_buffer: deque[tuple[int, str]] = deque(maxlen=max(0, before))
    rows: list[dict[str, object]] = []
    pending_after = 0
    seen = set()
    match_count = 0
    reached_limit = False

    def _matched(text: str) -> bool:
        if pattern is not None:
            return bool(pattern.search(text))
        if ignore_case:
            return query.lower() in text.lower()
        return query in text

    with path.open("r", encoding=encoding, errors="replace") as f:
        for idx, raw in enumerate(f, start=1):
            line = raw.rstrip("\n")
            is_match = _matched(line) if not reached_limit else False

            if is_match:
                for ln, txt in before_buffer:
                    if ln not in seen:
                        rows.append({"line": ln, "text": txt, "kind": "before"})
                        seen.add(ln)
                if idx not in seen:
                    rows.append({"line": idx, "text": line, "kind": "match"})
                    seen.add(idx)
                    match_count += 1
                pending_after = max(pending_after, after)
                if match_count >= max_matches:
                    reached_limit = True
            elif pending_after > 0 and idx not in seen:
                rows.append({"line": idx, "text": line, "kind": "after"})
                seen.add(idx)
                pending_after -= 1

            before_buffer.append((idx, line))
            if reached_limit and pending_after == 0:
                break

    return rows


def _extract_lines(
    path: Path,
    *,
    query: str,
    ignore_case: bool,
    max_matches: int,
    encoding: str,
) -> list[dict[str, object]]:
    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(query, flags)
    rows: list[dict[str, object]] = []

    with path.open("r", encoding=encoding, errors="replace") as f:
        for idx, raw in enumerate(f, start=1):
            line = raw.rstrip("\n")
            m = pattern.search(line)
            if not m:
                continue
            row: dict[str, object] = {"line": idx, "text": line}
            if m.groupdict():
                row["groups"] = m.groupdict()
            else:
                row["groups"] = list(m.groups())
            rows.append(row)
            if len(rows) >= max_matches:
                break
    return rows


def _stats(path: Path, *, encoding: str) -> dict[str, object]:
    line_count = 0
    non_empty = 0
    max_len = 0
    first_non_empty = ""
    last_non_empty = ""

    with path.open("r", encoding=encoding, errors="replace") as f:
        for raw in f:
            line_count += 1
            text = raw.rstrip("\n")
            if text.strip():
                non_empty += 1
                if not first_non_empty:
                    first_non_empty = text
                last_non_empty = text
            max_len = max(max_len, len(text))

    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "lines": line_count,
        "non_empty_lines": non_empty,
        "max_line_length": max_len,
        "first_non_empty_line": first_non_empty,
        "last_non_empty_line": last_non_empty,
    }


@mcp.tool(name="file_reckoning")
def file_reckoning(
    path: str,
    action: Literal["head", "tail", "range", "search", "extract", "stats"] = "head",
    query: str = "",
    start_line: int = 1,
    end_line: int = 200,
    max_lines: int = 200,
    max_matches: int = 100,
    before: int = 0,
    after: int = 0,
    regex: bool = False,
    ignore_case: bool = False,
    encoding: str = "utf-8",
) -> dict[str, object]:
    """Reckon signal from large files with bounded, context-efficient reads.

    When to use:
    - Large log/text files where full reads would be slow or noisy.
    - Iterative investigation workflows where you need quick, bounded slices.
    - Pattern discovery and extraction tasks that benefit from targeted search.

    When not to use:
    - Small files where a direct full read is simpler and sufficient.
    - Binary files or structured formats that should be parsed by specialized tools.
    - Workflows that require mutating files (this tool is read-only).

    Agent-oriented guidance:
    - Use this tool as the default for log/text files that may be large.
    - Avoid full-file ingestion; iterate with small windows and targeted queries.
    - Start with `stats`, then `head`/`tail`, then narrow with `search`, then structure with `extract`.
    - Prefer `max_lines`/`max_matches` limits to keep responses compact and relevant.

    Actions:
    - head: first `max_lines` lines
    - tail: last `max_lines` lines
    - range: lines `start_line`..`end_line` (capped by `max_lines`)
    - search: filter by `query` (plain text or regex), optional context with `before`/`after`
    - extract: regex capture extraction from matching lines
    - stats: lightweight file summary (size, line count, shape hints)
    """
    p = _ensure_file(path)
    max_lines = max(1, min(max_lines, 5000))
    max_matches = max(1, min(max_matches, 5000))
    before = max(0, min(before, 100))
    after = max(0, min(after, 100))
    start_line = max(1, start_line)
    end_line = max(start_line, end_line)

    if action in {"search", "extract"} and not query:
        raise ValueError("`query` is required for search/extract actions.")

    if action == "head":
        return {"action": action, "path": str(p), "rows": _head_lines(p, max_lines=max_lines, encoding=encoding)}
    if action == "tail":
        return {"action": action, "path": str(p), "rows": _tail_lines(p, max_lines=max_lines, encoding=encoding)}
    if action == "range":
        return {
            "action": action,
            "path": str(p),
            "rows": _range_lines(
                p,
                start_line=start_line,
                end_line=end_line,
                max_lines=max_lines,
                encoding=encoding,
            ),
        }
    if action == "search":
        return {
            "action": action,
            "path": str(p),
            "query": query,
            "rows": _search_lines(
                p,
                query=query,
                regex=regex,
                ignore_case=ignore_case,
                before=before,
                after=after,
                max_matches=max_matches,
                encoding=encoding,
            ),
        }
    if action == "extract":
        return {
            "action": action,
            "path": str(p),
            "query": query,
            "rows": _extract_lines(
                p,
                query=query,
                ignore_case=ignore_case,
                max_matches=max_matches,
                encoding=encoding,
            ),
        }
    return {"action": action, "stats": _stats(p, encoding=encoding)}
