from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .privacy import load_extra_blocklist, scan_tree
from .pronunciation import format_finding, scan_file


TEXT_REVIEW_EXTENSIONS = {".md", ".txt", ".vtt"}


@dataclass(frozen=True)
class ReviewIssue:
    level: str
    path: str
    message: str


@dataclass(frozen=True)
class ReviewReport:
    output_dir: str
    passed: bool
    artifacts: dict[str, str | None]
    media_probe: dict[str, Any] = field(default_factory=dict)
    issues: tuple[ReviewIssue, ...] = field(default_factory=tuple)
    report_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = [asdict(issue) for issue in self.issues]
        return payload


def review_output(
    output_dir: str | Path,
    *,
    extra_blocklist_path: str | Path = ".privacy-blocklist.local",
    write_report: bool = True,
) -> ReviewReport:
    root = Path(output_dir).resolve()
    issues: list[ReviewIssue] = []
    if not root.exists():
        issues.append(ReviewIssue("error", str(root), "output directory does not exist"))
        return ReviewReport(str(root), False, {}, issues=tuple(issues))

    artifacts = {
        "manifest": _existing(root / "manifest.json"),
        "script": _existing(root / "script.md"),
        "video": _existing(root / "daily-video.mp4"),
        "contact_sheet": _existing(root / "review_contact_sheet.jpg"),
        "narration": _existing(root / "narration.txt"),
    }
    for label in ("manifest", "script", "video", "contact_sheet"):
        if not artifacts[label]:
            issues.append(ReviewIssue("error", str(root / _artifact_name(label)), f"missing required {label} artifact"))

    warning_path = root / "pronunciation_warnings.json"
    if warning_path.exists():
        issues.append(ReviewIssue("error", str(warning_path), "pronunciation warnings were generated during pipeline run"))

    issues.extend(_pronunciation_issues(root))
    issues.extend(_privacy_issues(root, extra_blocklist_path=extra_blocklist_path))

    media_probe: dict[str, Any] = {}
    video_path = root / "daily-video.mp4"
    if video_path.exists():
        media_probe = _probe_video(video_path, issues)

    stale_names = ("natural_check", "draft", "tmp_probe")
    for path in root.iterdir():
        if any(token in path.name for token in stale_names):
            issues.append(ReviewIssue("warning", str(path), "stale or draft artifact remains in output directory"))

    passed = not any(issue.level == "error" for issue in issues)
    report_path = root / "review_report.md"
    report = ReviewReport(
        output_dir=str(root),
        passed=passed,
        artifacts=artifacts,
        media_probe=media_probe,
        issues=tuple(issues),
        report_path=str(report_path) if write_report else None,
    )
    if write_report:
        report_path.write_text(format_review_markdown(report), encoding="utf-8")
    return report


def format_review_markdown(report: ReviewReport) -> str:
    lines = [
        "# Daily Video Review",
        "",
        f"Status: {'PASS' if report.passed else 'FAIL'}",
        f"Output: `{report.output_dir}`",
        "",
        "## Artifacts",
        "",
    ]
    for label, value in report.artifacts.items():
        lines.append(f"- {label}: `{value or 'missing'}`")
    if report.media_probe:
        lines.extend(["", "## Media Probe", ""])
        for key, value in report.media_probe.items():
            lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Issues", ""])
    if not report.issues:
        lines.append("- none")
    else:
        for issue in report.issues:
            lines.append(f"- {issue.level.upper()}: `{issue.path}` - {issue.message}")
    lines.append("")
    return "\n".join(lines)


def _existing(path: Path) -> str | None:
    return str(path) if path.exists() else None


def _artifact_name(label: str) -> str:
    return {
        "manifest": "manifest.json",
        "script": "script.md",
        "video": "daily-video.mp4",
        "contact_sheet": "review_contact_sheet.jpg",
    }[label]


def _pronunciation_issues(root: Path) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    for path in sorted(root.iterdir()):
        if path.name == "review_report.md":
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_REVIEW_EXTENSIONS:
            continue
        for finding in scan_file(path):
            issues.append(ReviewIssue("error", str(path), format_finding(finding)))
    return issues


def _privacy_issues(root: Path, *, extra_blocklist_path: str | Path) -> list[ReviewIssue]:
    blocklist_path = Path(extra_blocklist_path)
    if not blocklist_path.is_absolute():
        blocklist_path = Path.cwd() / blocklist_path
    findings = scan_tree(root, extra_terms=load_extra_blocklist(blocklist_path))
    return [ReviewIssue("error", str(root / finding.path), finding.reason) for finding in findings]


def _probe_video(video_path: Path, issues: list[ReviewIssue]) -> dict[str, Any]:
    if not shutil.which("ffprobe"):
        issues.append(ReviewIssue("warning", str(video_path), "ffprobe is not available; skipped media metadata check"))
        return {}
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height,avg_frame_rate",
        "-of",
        "json",
        str(video_path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        issues.append(ReviewIssue("error", str(video_path), f"ffprobe failed: {exc.stderr.strip() or exc}"))
        return {}
    raw = json.loads(result.stdout)
    streams = raw.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    audio_stream = next((stream for stream in streams if stream.get("codec_type") == "audio"), {})
    width = int(video_stream.get("width") or 0)
    height = int(video_stream.get("height") or 0)
    if width and height and width >= height:
        issues.append(ReviewIssue("warning", str(video_path), "video is not portrait orientation"))
    if not audio_stream:
        issues.append(ReviewIssue("warning", str(video_path), "no audio stream found"))
    return {
        "duration": raw.get("format", {}).get("duration"),
        "width": width or None,
        "height": height or None,
        "video_codec": video_stream.get("codec_name"),
        "audio_codec": audio_stream.get("codec_name"),
        "frame_rate": video_stream.get("avg_frame_rate"),
    }
