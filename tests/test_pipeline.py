from __future__ import annotations

import json
from pathlib import Path

import pytest

from daily_video_pipeline.config import load_config
from daily_video_pipeline.pipeline import run_pipeline


def test_demo_pipeline_writes_manifest_and_script(tmp_path: Path) -> None:
    config = load_config("configs/project.example.yml")
    patched = config.__class__(
        name=config.name,
        timezone=config.timezone,
        language=config.language,
        output_dir=tmp_path / "outputs",
        max_items=config.max_items,
        freshness_hours=24 * 365,
        keywords=config.keywords,
        blocked_terms=config.blocked_terms,
        sources=config.sources,
        story=config.story,
        video=config.video,
        narration=config.narration,
        music=config.music,
    )

    artifacts = run_pipeline(
        patched,
        run_date="2026-06-09",
        demo_items_path=Path("examples/demo_items.json"),
        skip_video=True,
    )

    assert Path(artifacts.manifest_path).exists()
    assert Path(artifacts.script_path).exists()
    assert artifacts.video_path is None
    manifest_text = Path(artifacts.manifest_path).read_text(encoding="utf-8")
    assert '"component": "cover_hook"' in manifest_text
    assert '"visual_grammar":' in manifest_text
    assert '"motion_grammar":' in manifest_text
    assert '"motion": "auto"' in manifest_text


def test_pipeline_accepts_local_items_file(tmp_path: Path) -> None:
    config = load_config("configs/project.example.yml")
    items_path = tmp_path / "local_items.json"
    items_path.write_text(
        json.dumps(
            [
                {
                    "title": "Local item drives a video",
                    "url": "https://example.com/local",
                    "source_name": "Local Notebook",
                    "published_at": "2026-06-09T01:00:00Z",
                    "summary": "This item came from a user-maintained local list.",
                    "tags": ["local"],
                }
            ]
        ),
        encoding="utf-8",
    )
    patched = config.__class__(
        name=config.name,
        timezone=config.timezone,
        language=config.language,
        output_dir=tmp_path / "outputs",
        max_items=config.max_items,
        freshness_hours=24 * 365,
        keywords=config.keywords,
        blocked_terms=config.blocked_terms,
        sources=config.sources,
        story=config.story,
        video=config.video,
        narration=config.narration,
        music=config.music,
    )

    artifacts = run_pipeline(
        patched,
        run_date="2026-06-09",
        items_path=items_path,
        skip_video=True,
    )

    script_text = Path(artifacts.script_path).read_text(encoding="utf-8")
    assert "Local item drives a video" in script_text
    assert "Local Notebook" in script_text


def test_pipeline_blocks_narration_render_when_pronunciation_is_risky(tmp_path: Path) -> None:
    config = load_config("configs/project.example.yml")
    risky_items_path = tmp_path / "risky_items.json"
    risky_items_path.write_text(
        json.dumps(
            [
                {
                    "title": "你可以直接跑命令行",
                    "url": "https://example.com/cli-video",
                    "source_name": "Demo Source",
                    "published_at": "2026-06-09T01:00:00Z",
                    "summary": "这个流程会生成视频。",
                    "tags": ["demo"],
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    patched = config.__class__(
        name=config.name,
        timezone=config.timezone,
        language=config.language,
        output_dir=tmp_path / "outputs",
        max_items=config.max_items,
        freshness_hours=24 * 365,
        keywords=config.keywords,
        blocked_terms=config.blocked_terms,
        sources=config.sources,
        story=config.story,
        video=config.video,
        narration={"enabled": True, "engine": "say"},
        music=config.music,
    )

    with pytest.raises(RuntimeError, match="Pronunciation warnings found"):
        run_pipeline(
            patched,
            run_date="2026-06-09",
            demo_items_path=risky_items_path,
            skip_video=False,
        )

    output_dir = tmp_path / "outputs" / "2026-06-09" / "my-daily-brief"
    assert (output_dir / "script.md").exists()
    warning_text = (output_dir / "pronunciation_warnings.json").read_text(encoding="utf-8")
    assert "命令行" in warning_text
