from __future__ import annotations

from daily_video_pipeline.fetchers import load_demo_items
from daily_video_pipeline.script_writer import build_scenes
from daily_video_pipeline.templates import SCENE_COMPONENTS, STORY_TEMPLATES, VISUAL_THEMES


def test_commercial_template_registry_has_expected_breadth() -> None:
    assert len(STORY_TEMPLATES) >= 12
    assert len(SCENE_COMPONENTS) >= 30
    assert len(VISUAL_THEMES) >= 6


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
