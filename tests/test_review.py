from __future__ import annotations

from pathlib import Path

from daily_video_pipeline.review import review_output


def test_review_flags_pronunciation_risk_in_output_text(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "manifest.json").write_text("{}", encoding="utf-8")
    (output_dir / "script.md").write_text("可以直接跑命令行。", encoding="utf-8")
    (output_dir / "review_contact_sheet.jpg").write_bytes(b"not-an-image")
    (output_dir / "daily-video.mp4").write_bytes(b"not-a-video")

    report = review_output(output_dir, write_report=False)

    assert not report.passed
    assert any("命令行" in issue.message for issue in report.issues)


def test_review_writes_report_for_missing_artifacts(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    report = review_output(output_dir)

    assert not report.passed
    assert Path(report.report_path or "").exists()
    assert "missing required video artifact" in Path(report.report_path or "").read_text(encoding="utf-8")
