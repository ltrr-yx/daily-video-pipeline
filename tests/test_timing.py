from __future__ import annotations

import pytest

from daily_video_pipeline.models import ScriptScene
from daily_video_pipeline.timing import (
    TimelineAlignmentError,
    apply_scene_timing,
    build_subtitle_scene_timeline,
    parse_vtt_text,
)


def _scene(title: str, body: str) -> ScriptScene:
    return ScriptScene(title=title, body=body, kicker="", source_label="", duration=5.0)


def test_vtt_scene_timeline_uses_spoken_scene_boundaries() -> None:
    cues = parse_vtt_text(
        """WEBVTT

00:00:00.000 --> 00:00:02.400
第一条 Anthropic 改口了 这件事影响开发者

00:00:02.400 --> 00:00:05.800
第二条 Fable 发布新模型 它把视频工作流压短

00:00:05.800 --> 00:00:08.900
第三条 AI 经济影响开始进入正式测算
"""
    )
    scenes = [
        _scene("第一条 Anthropic 改口了", "这件事影响开发者"),
        _scene("第二条 Fable 发布新模型", "它把视频工作流压短"),
        _scene("第三条 AI 经济影响", "开始进入正式测算"),
    ]

    timings = build_subtitle_scene_timeline(scenes, cues, media_duration=9.2)
    aligned = apply_scene_timing(scenes, timings)

    assert [timing.start for timing in timings] == [0.0, 2.4, 5.8]
    assert [scene.duration for scene in aligned] == [2.4, 3.4, 3.4]
    assert timings[1].source_text.startswith("第二条 Fable")


def test_vtt_scene_timeline_fails_when_scene_anchor_is_missing() -> None:
    cues = parse_vtt_text(
        """WEBVTT

00:00:00,000 --> 00:00:01,000
Only the opener is spoken.
"""
    )

    with pytest.raises(TimelineAlignmentError, match="Could not align"):
        build_subtitle_scene_timeline(
            [
                _scene("Only the opener", "is spoken"),
                _scene("Missing scene", "never appears"),
            ],
            cues,
        )
