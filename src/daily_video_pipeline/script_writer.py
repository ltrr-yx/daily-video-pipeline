from __future__ import annotations

import textwrap
from datetime import datetime

from .models import NewsItem, ScriptScene


def build_scenes(items: list[NewsItem], *, project_name: str, run_date: str) -> list[ScriptScene]:
    scenes = [
        ScriptScene(
            title=f"{project_name}",
            kicker=run_date,
            body="Today's source-driven briefing, generated from your configured feeds.",
            source_label="configured sources",
        )
    ]
    for index, item in enumerate(items, start=1):
        scenes.append(
            ScriptScene(
                title=item.title,
                kicker=f"Signal {index:02d}",
                body=_summary_or_fallback(item),
                source_label=f"{item.source_name} · {item.published_at.date().isoformat()}",
            )
        )
    return scenes


def build_markdown(items: list[NewsItem], scenes: list[ScriptScene], *, run_date: str) -> str:
    lines = [f"# Daily Video Script - {run_date}", ""]
    lines.append("## Voiceover")
    lines.append("")
    for scene in scenes:
        lines.append(f"- {scene.kicker}: {scene.title}. {scene.body}")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    for item in items:
        lines.append(f"- [{item.title}]({item.url}) - {item.source_name}")
    lines.append("")
    return "\n".join(lines)


def narration_text(scenes: list[ScriptScene]) -> str:
    return " ".join(f"{scene.title}. {scene.body}" for scene in scenes)


def _summary_or_fallback(item: NewsItem) -> str:
    summary = item.summary.strip()
    if not summary:
        return "A fresh item from this source. Open the original link before publishing final commentary."
    return textwrap.shorten(summary, width=220, placeholder="...")
