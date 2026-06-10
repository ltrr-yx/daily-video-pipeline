from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .pronunciation import format_finding, scan_file, scan_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="daily-video")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Fetch configured sources or local items and render a daily video.")
    run_parser.add_argument("--config", required=True, help="Path to project YAML config.")
    run_parser.add_argument("--date", help="Run date in YYYY-MM-DD format.")
    source_group = run_parser.add_mutually_exclusive_group()
    source_group.add_argument("--demo", action="store_true", help="Use examples/demo_items.json instead of fetching feeds.")
    source_group.add_argument("--items", help="Path to a local JSON item list instead of fetching feeds.")
    run_parser.add_argument("--skip-video", action="store_true", help="Write manifest/script without rendering MP4.")
    run_parser.add_argument("--json", action="store_true", help="Print artifact paths as JSON.")

    scan_parser = subparsers.add_parser("privacy-scan", help="Scan the repository for accidental private content.")
    scan_parser.add_argument("--root", default=".", help="Repository root.")
    scan_parser.add_argument(
        "--extra-blocklist",
        default=".privacy-blocklist.local",
        help="Ignored local file with personal source names, domains, topic labels, or holdings terms to block.",
    )
    pronunciation_parser = subparsers.add_parser(
        "pronunciation-scan",
        help="Scan narration text for Chinese polyphonic words that TTS may misread.",
    )
    pronunciation_source = pronunciation_parser.add_mutually_exclusive_group(required=True)
    pronunciation_source.add_argument("--text", help="Narration text to scan.")
    pronunciation_source.add_argument("--file", help="UTF-8 narration or script file to scan.")
    pronunciation_parser.add_argument("--json", action="store_true", help="Print findings as JSON.")
    pronunciation_parser.add_argument(
        "--allow-warnings",
        action="store_true",
        help="Return exit code 0 even when pronunciation warnings are found.",
    )
    subparsers.add_parser("list-templates", help="List built-in story templates, scene components, and visual themes.")
    gallery_parser = subparsers.add_parser("build-gallery", help="Generate docs/gallery.html and docs/gallery.md.")
    gallery_parser.add_argument("--output-dir", default="docs", help="Directory to write gallery files.")
    review_parser = subparsers.add_parser("review", help="Run publishing checks for a completed output directory.")
    review_parser.add_argument("--output", required=True, help="Output directory containing manifest/script/video artifacts.")
    review_parser.add_argument(
        "--extra-blocklist",
        default=".privacy-blocklist.local",
        help="Local private-term blocklist to apply to output review.",
    )
    review_parser.add_argument("--json", action="store_true", help="Print the review report as JSON.")
    review_parser.add_argument("--no-write-report", action="store_true", help="Do not write review_report.md.")
    init_parser = subparsers.add_parser("init", help="Create a local config and run setup checks.")
    init_parser.add_argument("--template", default="configs/project.example.yml", help="Example config to copy.")
    init_parser.add_argument("--local-config", default="configs/project.local.yml", help="Ignored local config path to create.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite the local config if it already exists.")
    init_parser.add_argument("--json", action="store_true", help="Print setup results as JSON.")
    skill_parser = subparsers.add_parser("install-skill", help="Install the repo-local Codex skill into a skills directory.")
    skill_parser.add_argument("--target-root", default=str(Path.home() / ".codex" / "skills"), help="Directory containing Codex skills.")
    skill_parser.add_argument("--force", action="store_true", help="Overwrite an existing installed skill.")
    skill_parser.add_argument("--json", action="store_true", help="Print installation result as JSON.")

    args = parser.parse_args(argv)
    if args.command == "run":
        from .config import load_config
        from .pipeline import run_pipeline

        config = load_config(args.config)
        demo_path = None
        if args.demo:
            demo_path = Path(__file__).resolve().parents[2] / "examples" / "demo_items.json"
        items_path = Path(args.items).resolve() if args.items else None
        try:
            artifacts = run_pipeline(
                config,
                run_date=args.date,
                demo_items_path=demo_path,
                items_path=items_path,
                skip_video=args.skip_video,
            )
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        payload = {
            "output_dir": artifacts.output_dir,
            "manifest_path": artifacts.manifest_path,
            "script_path": artifacts.script_path,
            "video_path": artifacts.video_path,
            "review_path": artifacts.review_path,
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
            if artifacts.review_path:
                print(f"Review contact sheet: {artifacts.review_path}")
            for warning in artifacts.warnings:
                print(f"Warning: {warning}", file=sys.stderr)
        return 0

    if args.command == "privacy-scan":
        from .privacy import load_extra_blocklist, scan_tree

        root = Path(args.root).resolve()
        extra_terms = load_extra_blocklist(root / args.extra_blocklist)
        findings = scan_tree(root, extra_terms=extra_terms)
        if findings:
            for finding in findings:
                print(f"{finding.path}: {finding.reason}", file=sys.stderr)
            return 1
        print("privacy scan passed")
        return 0

    if args.command == "pronunciation-scan":
        findings = scan_text(args.text, path="<text>") if args.text else scan_file(args.file)
        if args.json:
            print(json.dumps([finding.to_dict() for finding in findings], ensure_ascii=False, indent=2))
        elif findings:
            for finding in findings:
                print(format_finding(finding), file=sys.stderr)
        else:
            print("pronunciation scan passed")
        return 0 if not findings or args.allow_warnings else 1

    if args.command == "list-templates":
        from .templates import MOTION_GRAMMARS, SCENE_COMPONENTS, STORY_TEMPLATES, VISUAL_THEMES

        print("Story templates")
        for key, template in STORY_TEMPLATES.items():
            print(f"- {key}: {template.name} ({len(template.components)} scenes)")
        print("\nScene components")
        for key, component in SCENE_COMPONENTS.items():
            print(f"- {key}: {component.name} / {component.family} / {component.visual_grammar}")
        print("\nVisual themes")
        for key, theme in VISUAL_THEMES.items():
            print(f"- {key}: {theme['name']}")
        print("\nMotion grammars")
        for key, motion in MOTION_GRAMMARS.items():
            print(f"- {key}: {motion.name} / {motion.entrance}")
        return 0

    if args.command == "build-gallery":
        from .gallery import write_gallery

        html_path, md_path = write_gallery(args.output_dir)
        print(f"Gallery HTML: {html_path}")
        print(f"Gallery Markdown: {md_path}")
        return 0

    if args.command == "review":
        from .review import review_output

        report = review_output(
            args.output,
            extra_blocklist_path=args.extra_blocklist,
            write_report=not args.no_write_report,
        )
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"Review: {'PASS' if report.passed else 'FAIL'}")
            if report.report_path:
                print(f"Report: {report.report_path}")
            for issue in report.issues:
                stream = sys.stderr if issue.level == "error" else sys.stdout
                print(f"{issue.level.upper()}: {issue.path}: {issue.message}", file=stream)
        return 0 if report.passed else 1

    if args.command == "init":
        from .setup_tools import init_project

        try:
            result = init_project(template=args.template, local_config=args.local_config, force=args.force)
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            verb = "created" if result.created else "exists"
            print(f"Local config {verb}: {result.local_config}")
            for check in result.checks:
                label = "ok" if check.ok else "missing"
                print(f"{check.name}: {label} ({check.message})")
        return 0 if all(check.ok for check in result.checks) else 1

    if args.command == "install-skill":
        from .setup_tools import install_skill

        try:
            result = install_skill(repo_root=_repo_root(), target_root=args.target_root, force=args.force)
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(result.message)
            print(f"Skill: {result.destination}")
        return 0

    return 2


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


if __name__ == "__main__":
    raise SystemExit(main())
