from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable

import feedparser

from .models import NewsItem, Source


def parse_datetime(value: object) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            try:
                dt = parsedate_to_datetime(value)
            except Exception:
                return datetime.now(timezone.utc)
    else:
        return datetime.now(timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def fetch_rss(source: Source) -> list[NewsItem]:
    parsed = feedparser.parse(source.url)
    if getattr(parsed, "bozo", False) and not parsed.entries:
        message = getattr(parsed, "bozo_exception", "unknown feed parsing error")
        raise RuntimeError(f"{source.name}: {message}")

    items: list[NewsItem] = []
    for entry in parsed.entries:
        published = (
            entry.get("published")
            or entry.get("updated")
            or entry.get("created")
            or datetime.now(timezone.utc).isoformat()
        )
        summary = entry.get("summary") or entry.get("description") or ""
        items.append(
            NewsItem(
                title=str(entry.get("title") or "Untitled"),
                url=str(entry.get("link") or source.url),
                source_name=source.name,
                published_at=parse_datetime(published),
                summary=_strip_html(str(summary)),
                tags=source.tags,
            )
        )
    return items


def fetch_sources(sources: Iterable[Source]) -> tuple[list[NewsItem], list[str]]:
    items: list[NewsItem] = []
    warnings: list[str] = []
    for source in sources:
        if not source.enabled:
            continue
        try:
            if source.type in {"rss", "atom", "feed"}:
                items.extend(fetch_rss(source))
            else:
                warnings.append(f"Skipped unsupported source type: {source.name} ({source.type})")
        except Exception as exc:  # keep one source failure from breaking the day
            warnings.append(f"{source.name}: {exc}")
    return items, warnings


def load_items_file(path: str | Path) -> list[NewsItem]:
    import json

    with Path(path).open("r", encoding="utf-8") as f:
        raw_items = json.load(f)
    items = []
    for item in raw_items:
        items.append(
            NewsItem(
                title=str(item["title"]),
                url=str(item["url"]),
                source_name=str(item["source_name"]),
                published_at=parse_datetime(item.get("published_at")),
                summary=str(item.get("summary", "")),
                tags=tuple(str(tag) for tag in item.get("tags", [])),
            )
        )
    return items


def load_demo_items(path: str | Path) -> list[NewsItem]:
    return load_items_file(path)


def _strip_html(value: str) -> str:
    import re

    text = re.sub(r"<[^>]+>", " ", value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
