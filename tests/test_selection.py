from __future__ import annotations

from datetime import datetime, timedelta, timezone

from daily_video_pipeline.models import NewsItem
from daily_video_pipeline.selection import select_items


def test_select_items_filters_old_and_blocked_items() -> None:
    now = datetime(2026, 6, 9, tzinfo=timezone.utc)
    items = [
        NewsItem(
            title="Fresh public update",
            url="https://example.com/a",
            source_name="demo",
            published_at=now - timedelta(hours=1),
            summary="useful workflow details",
        ),
        NewsItem(
            title="Old update",
            url="https://example.com/b",
            source_name="demo",
            published_at=now - timedelta(days=10),
        ),
        NewsItem(
            title="Blocked topic",
            url="https://example.com/c",
            source_name="demo",
            published_at=now,
            summary="contains private-term",
        ),
    ]

    selected = select_items(
        items,
        keywords=("workflow",),
        blocked_terms=("private-term",),
        freshness_hours=72,
        max_items=5,
        now=now,
    )

    assert [item.url for item in selected] == ["https://example.com/a"]
    assert selected[0].score > 0
