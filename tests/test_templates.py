from __future__ import annotations

from datetime import datetime, timezone

from daily_video_pipeline.fetchers import load_demo_items
from daily_video_pipeline.models import NewsItem
from daily_video_pipeline.script_writer import build_markdown, build_scenes, narration_text, scene_readability_snapshot
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
        "color_strategy",
        "contrast",
        "density",
        "card_radius",
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


def test_motion_overrides_support_component_family_and_readable_aliases() -> None:
    items = load_demo_items("examples/demo_items.json")

    scenes = build_scenes(
        items,
        project_name="Demo",
        run_date="2026-06-10",
        story_config={
            "template": "product_launch",
            "motion": "soft_assembly",
            "motion_overrides": {
                "product": "data_tween",
                "product_plate": "product_reveal",
                "proof": "evidence_trace",
                "conclusion": "verdict_lock",
            },
        },
    )

    motion_by_component = {scene.component: scene.motion_grammar for scene in scenes}
    assert motion_by_component["product_plate"] == "product_reveal"
    assert motion_by_component["verification_rail"] == "evidence_trace"
    assert motion_by_component["cta_end"] == "verdict_lock"
    assert motion_by_component["before_after_surface"] == "soft_assembly"


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


def test_narration_text_uses_chinese_sentence_pause() -> None:
    scene = build_scenes(
        load_demo_items("examples/demo_items.json"),
        project_name="Demo",
        run_date="2026-06-10",
        story_config={"template": "daily_briefing"},
    )[0]
    revised_scene = type(scene)(
        title="自动对齐",
        kicker=scene.kicker,
        eyebrow=scene.eyebrow,
        body="少一点手动调整，多一点稳定出片。",
        source_label=scene.source_label,
        component=scene.component,
        visual_grammar=scene.visual_grammar,
        motion_grammar=scene.motion_grammar,
        proof=scene.proof,
        source_url=scene.source_url,
        metrics=scene.metrics,
        bullets=scene.bullets,
        tags=scene.tags,
        duration=scene.duration,
    )

    assert narration_text([revised_scene]) == "自动对齐。少一点手动调整，多一点稳定出片。"


def test_narration_adds_visual_bridge_for_short_dense_screen_copy() -> None:
    scene = type(
        build_scenes(
            load_demo_items("examples/demo_items.json"),
            project_name="Demo",
            run_date="2026-06-10",
            story_config={"template": "daily_briefing"},
        )[0]
    )(
        title="自动对齐",
        kicker="",
        eyebrow="",
        body="今天这个仓库会用语音时间切画面，还留下时间轴复查。",
        source_label="audio_timeline.json",
        component="mechanism_xray",
        visual_grammar="mechanism_xray",
        motion_grammar="mechanism_scan",
        proof="先生成字幕时间，再按时间渲染每一幕。",
        metrics=(),
        bullets=("生成语音", "读取时间", "同步画面"),
        tags=(),
        duration=4.0,
    )

    text = narration_text([scene])
    snapshot = scene_readability_snapshot(scene)

    assert "这页就看三步：生成语音、读取时间、同步画面。" in text
    assert snapshot["bridge"] == "这页就看三步：生成语音、读取时间、同步画面。"
    assert snapshot["gap_seconds"] < 2.2


def test_narration_does_not_dump_long_visual_cards_into_voiceover() -> None:
    scene = type(
        build_scenes(
            load_demo_items("examples/demo_items.json"),
            project_name="Demo",
            run_date="2026-06-10",
            story_config={"template": "daily_briefing"},
        )[0]
    )(
        title="今日信号",
        kicker="",
        eyebrow="",
        body="今天先看三个公开来源里的共同变化。",
        source_label="source digest",
        component="signal_grid",
        visual_grammar="signal_board",
        motion_grammar="soft_assembly",
        proof="",
        metrics=(),
        bullets=(
            "这是一条太长的卡片文字，不适合整句塞进口播里",
            "第二条也很长，应该留在画面上给观众自己读",
            "第三条仍然很长，口播只需要概括它们的关系",
        ),
        tags=(),
        duration=4.0,
    )

    assert "画面里" not in narration_text([scene])


def test_script_markdown_uses_same_voiceover_strategy() -> None:
    scene = type(
        build_scenes(
            load_demo_items("examples/demo_items.json"),
            project_name="Demo",
            run_date="2026-06-10",
            story_config={"template": "daily_briefing"},
        )[0]
    )(
        title="自动对齐",
        kicker="",
        eyebrow="",
        body="今天这个仓库会用语音时间切画面，还留下时间轴复查。",
        source_label="audio_timeline.json",
        component="mechanism_xray",
        visual_grammar="mechanism_xray",
        motion_grammar="mechanism_scan",
        proof="先生成字幕时间，再按时间渲染每一幕。",
        metrics=(),
        bullets=("生成语音", "读取时间", "同步画面"),
        tags=(),
        duration=4.0,
    )

    markdown = build_markdown([], [scene], run_date="2026-06-10")

    assert "- 自动对齐。今天这个仓库会用语音时间切画面，还留下时间轴复查。这页就看三步：生成语音、读取时间、同步画面。" in markdown
