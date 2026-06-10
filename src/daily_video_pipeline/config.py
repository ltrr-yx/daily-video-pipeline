from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .models import Source


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    timezone: str
    language: str
    output_dir: Path
    max_items: int
    freshness_hours: int
    keywords: tuple[str, ...]
    blocked_terms: tuple[str, ...]
    sources: tuple[Source, ...]
    story: dict[str, Any]
    video: dict[str, Any]
    narration: dict[str, Any]
    music: dict[str, Any]


def _as_tuple(value: Any) -> tuple[str, ...]:
    if not value:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def load_config(path: str | Path) -> ProjectConfig:
    config_path = Path(path).resolve()
    with config_path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    project = raw.get("project", {})
    selection = raw.get("selection", {})
    privacy = raw.get("privacy", {})
    story = raw.get("story", {})
    video = raw.get("video", {})
    narration = raw.get("narration", {})
    music = raw.get("music", {})

    sources = []
    for item in raw.get("sources", []):
        if not item:
            continue
        sources.append(
            Source(
                name=str(item["name"]),
                type=str(item.get("type", "rss")).lower(),
                url=str(item["url"]),
                enabled=bool(item.get("enabled", True)),
                priority=float(item.get("priority", 1.0)),
                tags=_as_tuple(item.get("tags")),
            )
        )

    output_dir = Path(project.get("output_dir", "outputs"))
    if not output_dir.is_absolute():
        output_dir = config_path.parent.parent / output_dir

    return ProjectConfig(
        name=str(project.get("name", "daily-video")),
        timezone=str(project.get("timezone", "UTC")),
        language=str(project.get("language", "zh-CN")),
        output_dir=output_dir,
        max_items=int(selection.get("max_items", 5)),
        freshness_hours=int(selection.get("freshness_hours", 72)),
        keywords=_as_tuple(selection.get("keywords")),
        blocked_terms=_as_tuple(privacy.get("blocked_terms")),
        sources=tuple(sources),
        story=dict(story),
        video=dict(video),
        narration=dict(narration),
        music=dict(music),
    )
