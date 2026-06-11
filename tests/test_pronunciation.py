from __future__ import annotations

from pathlib import Path

from daily_video_pipeline.cli import main
from daily_video_pipeline.pronunciation import scan_text


def test_pronunciation_scan_flags_command_line_polyphone() -> None:
    findings = scan_text("然后用命令行生成视频。")

    assert [finding.term for finding in findings] == ["命令行"]
    assert "hang2" in findings[0].expected
    assert "终端命令" in findings[0].suggestion


def test_pronunciation_scan_passes_plain_text() -> None:
    assert scan_text("然后在终端里生成视频。") == []


def test_pronunciation_cli_returns_nonzero_for_warning(tmp_path: Path, capsys) -> None:
    script_path = tmp_path / "voiceover.txt"
    script_path.write_text("你可以直接跑命令行。", encoding="utf-8")

    code = main(["pronunciation-scan", "--file", str(script_path)])
    captured = capsys.readouterr()

    assert code == 1
    assert "命令行" in captured.err
