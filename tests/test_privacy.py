from __future__ import annotations

from pathlib import Path

from daily_video_pipeline.privacy import scan_tree


def test_privacy_scan_blocks_sensitive_paths(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "portfolio.json").write_text("{}", encoding="utf-8")

    findings = scan_tree(tmp_path)

    assert findings
    assert "sensitive path name" in findings[0].reason


def test_privacy_scan_uses_extra_blocklist(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("This mentions a private source label.", encoding="utf-8")

    findings = scan_tree(tmp_path, extra_terms=("private source label",))

    assert findings
    assert "extra private blocklist term" in findings[0].reason
