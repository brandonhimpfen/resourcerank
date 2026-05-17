from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .profiles import load_profile
from .schema import Resource
from .scorer import ResourceScorer


def read_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_output(data: dict, output: str | None) -> None:
    rendered = json.dumps(data, indent=2, ensure_ascii=False)
    if output:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def evaluate_command(args: argparse.Namespace) -> int:
    resource_data = read_json(args.input)
    profile = load_profile(args.profile)
    resource = Resource.from_dict(resource_data)
    scorer = ResourceScorer(profile)
    result = scorer.evaluate(resource)
    write_output(result.to_dict(), args.output)
    return 0


def profile_command(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    write_output(profile, args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resourcerank",
        description="Evaluate resources for curated lists, directories, datasets, newsletters, and knowledge bases.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    evaluate = sub.add_parser("evaluate", help="Evaluate a resource from a JSON input file.")
    evaluate.add_argument("--input", "-i", required=True, help="Path to resource JSON input.")
    evaluate.add_argument("--profile", "-p", help="Path to review profile JSON.")
    evaluate.add_argument("--output", "-o", help="Optional path for JSON review output.")
    evaluate.set_defaults(func=evaluate_command)

    profile = sub.add_parser("show-profile", help="Show the active review profile.")
    profile.add_argument("--profile", "-p", help="Path to review profile JSON.")
    profile.add_argument("--output", "-o", help="Optional path for profile JSON output.")
    profile.set_defaults(func=profile_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"resourcerank error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
