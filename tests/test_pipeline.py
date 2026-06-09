from __future__ import annotations

from pathlib import Path

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
