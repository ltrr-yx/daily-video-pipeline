from __future__ import annotations

from datetime import datetime, timezone

from daily_video_pipeline.fetchers import load_demo_items
from daily_video_pipeline.models import NewsItem
from daily_video_pipeline.script_writer import build_markdown, build_scenes, narration_text
from daily_video_pipeline.templates import (
    MOTION_DEFAULTS_BY_FAMILY,
    MOTION_GRAMMARS,
    SCENE_COMPONENTS,
    STORY_TEMPLATES,
    VISUAL_THEMES,
)


def test_commercial_template_registry_has_expected_breadth() -> None:
    assert len(STORY_TEMPLATES) >= 12
    assert len(SCENE_COMPONENTS) >= 30
    assert len(VISUAL_THEMES) >= 6
    assert len(MOTION_GRAMMARS) >= 6


def test_motion_grammars_cover_component_families() -> None:
    missing = sorted({component.family for component in SCENE_COMPONENTS.values()} - set(MOTION_DEFAULTS_BY_FAMILY))

    assert missing == []


def test_visual_themes_include_style_dimensions() -> None:
    required_style_keys = {
        "font_zh",
        "font_en",
        "type_scale",
        "text_ratio",
        "media_ratio",
        "ornament",
        "underline",
    }

    for theme in VISUAL_THEMES.values():
        assert required_style_keys <= set(theme["style"])
        assert theme["style"]["text_ratio"] + theme["style"]["media_ratio"] == 100


def test_story_templates_reference_registered_components() -> None:
    missing = []
    for template in STORY_TEMPLATES.values():
        for component in template.components:
            if component not in SCENE_COMPONENTS:
                missing.append((template.key, component))
    assert missing == []


def test_every_story_template_generates_component_scenes() -> None:
    items = load_demo_items("examples/demo_items.json")
    for key, template in STORY_TEMPLATES.items():
        scenes = build_scenes(
            items,
            project_name="Demo",
            run_date="2026-06-10",
            story_config={"template": key},
        )
        assert len(scenes) == len(template.components)
        assert [scene.component for scene in scenes] == list(template.components)
        assert all(scene.visual_grammar for scene in scenes)
        assert all(scene.motion_grammar in MOTION_GRAMMARS for scene in scenes)


def test_metric_extraction_keeps_decimal_percentages() -> None:
    item = NewsItem(
        title="沪指3986.66点，跌0.58%",
        url="https://example.com",
        source_name="example",
        published_at=datetime(2026, 6, 10, tzinfo=timezone.utc),
        summary="深成指跌1.94%，创业板指跌2.29%。",
    )

    scenes = build_scenes([item], project_name="Demo", run_date="2026-06-10", story_config={"template": "market_radar"})

    values = [value for _, value in scenes[0].metrics]
    assert "0.58%" in values
    assert "6" not in values
    assert "10" not in values
    assert "58%" not in values


def test_metric_extraction_uses_financial_units_before_date_numbers() -> None:
    item = NewsItem(
        title="6月10日午间复盘：沪指3986.66点，成交1.73万亿",
        url="https://example.com",
        source_name="example",
        published_at=datetime(2026, 6, 10, tzinfo=timezone.utc),
        summary="上涨1084家，下跌4127家。",
    )

    scenes = build_scenes([item], project_name="Demo", run_date="2026-06-10", story_config={"template": "market_radar"})

    values = [value for _, value in scenes[0].metrics]
    assert "3986.66点" in values
    assert "1.73万亿" in values
    assert "6" not in values
    assert "10" not in values


def test_audience_script_surfaces_do_not_expose_internal_guidance() -> None:
    items = load_demo_items("examples/demo_items.json")
    scenes = build_scenes(items, project_name="Demo", run_date="2026-06-10", story_config={"template": "market_radar"})
    audience_text = build_markdown(items, scenes, run_date="2026-06-10") + "\n" + narration_text(scenes)

    for internal_term in ("visual_grammar", "motion_grammar", "market_ledger", "data_tween", "signal_board"):
        assert internal_term not in audience_text
    for internal_label in ("Signals ·", "Source proof:", "Metrics:", "Ledger:", "Watch:"):
        assert internal_label not in audience_text
    for production_phrase in ("configured-source", "designed for", "the viewer", "Editorial takeaways"):
        assert production_phrase not in audience_text
