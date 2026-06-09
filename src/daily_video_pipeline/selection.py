from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import NewsItem


def select_items(
    items: list[NewsItem],
    *,
    keywords: tuple[str, ...],
    blocked_terms: tuple[str, ...],
    freshness_hours: int,
    max_items: int,
    now: datetime | None = None,
) -> list[NewsItem]:
    now = now or datetime.now(timezone.utc)
    fresh_after = now - timedelta(hours=freshness_hours)
    deduped: dict[str, NewsItem] = {}

    for item in items:
        if item.published_at < fresh_after:
            continue
        haystack = f"{item.title}\n{item.summary}".lower()
        if any(term.lower() in haystack for term in blocked_terms):
            continue
        key = item.url or item.title.lower()
        scored = NewsItem(
            title=item.title,
            url=item.url,
            source_name=item.source_name,
            published_at=item.published_at,
            summary=item.summary,
            tags=item.tags,
            score=_score(item, keywords, now),
        )
        if key not in deduped or scored.score > deduped[key].score:
            deduped[key] = scored

    return sorted(deduped.values(), key=lambda item: item.score, reverse=True)[:max_items]


def _score(item: NewsItem, keywords: tuple[str, ...], now: datetime) -> float:
    text = f"{item.title}\n{item.summary}\n{' '.join(item.tags)}".lower()
    keyword_score = sum(2.0 for keyword in keywords if keyword.lower() in text)
    hours_old = max(0.0, (now - item.published_at).total_seconds() / 3600)
    recency_score = max(0.0, 3.0 - hours_old / 24)
    summary_score = min(len(item.summary) / 240, 1.5)
    return round(keyword_score + recency_score + summary_score, 3)
