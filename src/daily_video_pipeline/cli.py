from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import load_config
from .pipeline import run_pipeline
from .privacy import load_extra_blocklist, scan_tree


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="daily-video")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Fetch configured sources and render a daily video.")
    run_parser.add_argument("--config", required=True, help="Path to project YAML config.")
    run_parser.add_argument("--date", help="Run date in YYYY-MM-DD format.")
    run_parser.add_argument("--demo", action="store_true", help="Use examples/demo_items.json instead of fetching feeds.")
    run_parser.add_argument("--skip-video", action="store_true", help="Write manifest/script without rendering MP4.")
    run_parser.add_argument("--json", action="store_true", help="Print artifact paths as JSON.")

    scan_parser = subparsers.add_parser("privacy-scan", help="Scan the repository for accidental private content.")
    scan_parser.add_argument("--root", default=".", help="Repository root.")
    scan_parser.add_argument(
        "--extra-blocklist",
        default=".privacy-blocklist.local",
        help="Ignored local file with personal source names, domains, topic labels, or holdings terms to block.",
    )

    args = parser.parse_args(argv)
    if args.command == "run":
        config = load_config(args.config)
        demo_path = None
        if args.demo:
            demo_path = Path(__file__).resolve().parents[2] / "examples" / "demo_items.json"
        artifacts = run_pipeline(config, run_date=args.date, demo_items_path=demo_path, skip_video=args.skip_video)
        payload = {
            "output_dir": artifacts.output_dir,
            "manifest_path": artifacts.manifest_path,
            "script_path": artifacts.script_path,
            "video_path": artifacts.video_path,
            "warnings": list(artifacts.warnings),
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"Output: {artifacts.output_dir}")
            print(f"Manifest: {artifacts.manifest_path}")
            print(f"Script: {artifacts.script_path}")
            if artifacts.video_path:
                print(f"Video: {artifacts.video_path}")
            for warning in artifacts.warnings:
                print(f"Warning: {warning}", file=sys.stderr)
        return 0

    if args.command == "privacy-scan":
        root = Path(args.root).resolve()
        extra_terms = load_extra_blocklist(root / args.extra_blocklist)
        findings = scan_tree(root, extra_terms=extra_terms)
        if findings:
            for finding in findings:
                print(f"{finding.path}: {finding.reason}", file=sys.stderr)
            return 1
        print("privacy scan passed")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
