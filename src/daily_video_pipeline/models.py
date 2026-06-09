from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Source:
    name: str
    type: str
    url: str
    enabled: bool = True
    priority: float = 1.0
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class NewsItem:
    title: str
    url: str
    source_name: str
    published_at: datetime
    summary: str = ""
    tags: tuple[str, ...] = ()
    score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["published_at"] = self.published_at.astimezone(timezone.utc).isoformat()
        payload["tags"] = list(self.tags)
        return payload


@dataclass(frozen=True)
class ScriptScene:
    title: str
    kicker: str
    body: str
    source_label: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class RunArtifacts:
    output_dir: str
    manifest_path: str
    script_path: str
    video_path: str | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)
