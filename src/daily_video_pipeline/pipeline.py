from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .config import ProjectConfig
from .fetchers import fetch_sources, load_demo_items
from .models import RunArtifacts
from .renderer import render_video
from .script_writer import build_markdown, build_scenes
from .selection import select_items


def run_pipeline(
    config: ProjectConfig,
    *,
    run_date: str | None = None,
    demo_items_path: Path | None = None,
    skip_video: bool = False,
) -> RunArtifacts:
    tz = ZoneInfo(config.timezone)
    now = datetime.now(tz)
    day = run_date or now.date().isoformat()
    slug = _slug(config.name)
    output_dir = config.output_dir / day / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    warnings: list[str] = []
    if demo_items_path:
        items = load_demo_items(demo_items_path)
    else:
        items, warnings = fetch_sources(config.sources)

    selected = select_items(
        items,
        keywords=config.keywords,
        blocked_terms=config.blocked_terms,
        freshness_hours=config.freshness_hours,
        max_items=config.max_items,
    )
    if not selected:
        raise RuntimeError("No eligible items found. Check sources, freshness window, or blocked terms.")

    scenes = build_scenes(selected, project_name=config.name, run_date=day)
    manifest_path = output_dir / "manifest.json"
    script_path = output_dir / "script.md"
    script_path.write_text(build_markdown(selected, scenes, run_date=day), encoding="utf-8")
    manifest_path.write_text(
        json.dumps(
            {
                "date": day,
                "project": config.name,
                "items": [item.to_dict() for item in selected],
                "scenes": [scene.to_dict() for scene in scenes],
                "warnings": warnings,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    video_path: Path | None = None
    if not skip_video:
        video_path = render_video(
            scenes,
            output_dir=output_dir,
            video_config=config.video,
            narration_config=config.narration,
            music_config=config.music,
        )

    return RunArtifacts(
        output_dir=str(output_dir),
        manifest_path=str(manifest_path),
        script_path=str(script_path),
        video_path=str(video_path) if video_path else None,
        warnings=tuple(warnings),
    )


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "daily-video"
