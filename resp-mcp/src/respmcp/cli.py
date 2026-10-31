"""Command line entry point: `respmcp ingest | score | serve | audit`.

Phase 0 provides the command names only. Each command is filled in by the phase
named in its help text (see docs/technical-plan.md, Section 8).
"""

from __future__ import annotations

import argparse
import sys

COMMANDS: dict[str, str] = {
    "ingest": "Fetch sources, save raw files, and load DuckDB (Phase 1 and 2).",
    "score": "Compute quality scores for every observation (Phase 3a).",
    "serve": "Start the MCP server over stdio (Phase 3b).",
    "audit": "Run the reconciliation audit and write docs/audit-<date>.md (Phase 6).",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="respmcp",
        description="Respiratory virus surveillance data, harmonized and served over MCP.",
    )
    sub = parser.add_subparsers(dest="command", metavar="command")
    for name, text in COMMANDS.items():
        sub.add_parser(name, help=text, description=text)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    print(f"'respmcp {args.command}' is not built yet. {COMMANDS[args.command]}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
