# log-recon-mcp

Lightweight MCP server using FastMCP, with a log exploration tool for large files.

## Project Layout

- `server.py`: thin entrypoint that starts the server and imports all tools
- `mcp_app.py`: shared `FastMCP` app instance
- `tools/file_reckoning.py`: large-file exploration tool
- `tools/script_runna.py`: bash wrapper with context-aware output modes
- `tools/health.py`: liveness/readiness ping tool

## Run in `devtools` conda env

```bash
conda activate devtools
pip install -e .
python server.py
```

This starts the MCP server over STDIO (FastMCP default).

## Main Tool: `file_reckoning`

`file_reckoning` is designed for incremental analysis so an agent does not need to load an entire file.

Use this as the default entrypoint for large logs/text files when extracting signal with minimal context usage.

Parameters:

- `path` (required): file path
- `action`: `head | tail | range | search | extract | stats`
- `query`: required for `search` and `extract`
- `start_line`, `end_line`: used by `range`
- `max_lines`: cap result rows for `head`, `tail`, `range`
- `max_matches`: cap match rows for `search`, `extract`
- `before`, `after`: context lines around `search` matches
- `regex`: treat `query` as regex in `search`
- `ignore_case`: case-insensitive `search`/`extract`
- `encoding`: default `utf-8`

Suggested usage pattern for sub-agents:

1. Run `stats` to understand file shape.
2. Run `head`/`tail` with small `max_lines` (for example `50`).
3. Run `search` with bounded `max_matches` and optional context.
4. Run `extract` with capture groups to pull structured signals.

Agent usage policy:

1. Do not ingest full files directly when file size is unknown or large.
2. Use `stats` first, then progressively narrow scope.
3. Keep `max_lines` and `max_matches` small unless there is a clear reason to increase.
4. Use `search` + `before/after` to capture surrounding evidence for key events/errors.
5. Use `extract` once stable patterns are found to produce structured context.

## Script Tool: `script_runna`

Thin bash wrapper to avoid context pollution from large script output.

Parameters:

- `script` (required): bash script/command string to run
- `output_dir`: default `/temp/script-runna/logs` (falls back to `/tmp/script-runna/logs` if needed)
- `inline_output_epsilon`: max bytes for inline output response (default `4000`)
- `timeout_seconds`: script timeout (default `1800`)
- `cwd`: optional working directory
- `return_mode`: `auto | path_only | inline_only` (default `auto`)

Behavior:

- Always writes combined `stdout` + `stderr` to a log file.
- `auto`: returns inline output only if size is `<= inline_output_epsilon`; otherwise returns `output_file`.
- `path_only`: always returns `output_file` path, never inline content.
- `inline_only`: always returns inline output (still writes log file).

Recommended chaining:

1. Run `script_runna`.
2. If `output_file` is returned, inspect with `file_reckoning` using `stats`, `tail`, or `search`.

Agent usage policy:

1. Default to `script_runna` for installs, builds, tests, migrations, and any command likely to produce long output.
2. Prefer `script_runna` whenever raw command output is intermediate and will be summarized.
3. Reserve direct shell execution (`exec_command`) for short, low-output checks (`pwd`, `ls`, compact `rg`).
4. Prefer `return_mode="path_only"` for noisy commands (`pip install`, builds, tests, package managers, verbose scripts).
5. Prefer `return_mode="auto"` for exploratory commands where short output might be useful.
6. Use `return_mode="inline_only"` only when full immediate output is explicitly needed.
7. For large outputs, do not re-run inline; inspect the log via `file_reckoning` instead.
