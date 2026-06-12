from __future__ import annotations

from array import array
import math
import sys
import wave

from PIL import Image, ImageDraw

from daily_video_pipeline.models import ScriptScene
from daily_video_pipeline.renderer import (
    _audience_header_label,
    _align_scenes_to_narration,
    _build_audio,
    _build_narration,
    _fit_text_block,
    _font,
    _text_block_height,
    _write_demo_bgm,
)


def test_grid_card_text_block_fits_long_market_signal() -> None:
    image = Image.new("RGB", (1080, 1920))
    draw = ImageDraw.Draw(image)
    text = "市场宽度偏弱：沪深合计约1084家上涨、4127家下跌"
    candidates = [
        (_font(None, 32), 7, 3),
        (_font(None, 30), 6, 3),
        (_font(None, 26), 5, 4),
    ]

    font, line_gap, lines = _fit_text_block(draw, text, 386, 128, candidates)

    assert len(lines) <= 4
    assert _text_block_height(draw, lines, font, line_gap) <= 128
    assert not any(line.startswith("084") for line in lines)


def test_audience_header_label_does_not_use_internal_kicker() -> None:
    scene = ScriptScene(
        title="Key signals",
        kicker="Signals · 5 sources",
        eyebrow="A Share Midday Recap",
        body="Body",
        source_label="market source digest",
    )
    fallback_scene = ScriptScene(
        title="Key signals",
        kicker="Signals · 5 sources",
        eyebrow="",
        body="Body",
        source_label="",
    )

    assert _audience_header_label(scene) == "A Share Midday Recap"
    assert _audience_header_label(fallback_scene) == "Daily update"


def test_align_scenes_to_narration_returns_subtitle_timed_scenes(tmp_path) -> None:
    subtitle_path = tmp_path / "narration_edge.srt"
    subtitle_path.write_text(
        """1
00:00:00,000 --> 00:00:02,200
Opening signal. The first scene starts here.

2
00:00:02,200 --> 00:00:06,000
Second signal. The spoken boundary controls the cut.
""",
        encoding="utf-8",
    )
    narration_path = tmp_path / "narration_edge.mp3"
    narration_path.write_bytes(b"fake")
    scenes = [
        ScriptScene(
            title="Opening signal",
            body="The first scene starts here.",
            kicker="",
            source_label="",
            duration=5.0,
        ),
        ScriptScene(
            title="Second signal",
            body="The spoken boundary controls the cut.",
            kicker="",
            source_label="",
            duration=5.0,
        ),
    ]

    aligned, payload = _align_scenes_to_narration(
        scenes,
        subtitles_path=subtitle_path,
        narration_path=narration_path,
        media_duration=6.4,
        video_config={},
        narration_config={"enabled": True, "timing": {"enabled": True, "strict": True}},
    )

    assert [scene.duration for scene in aligned] == [2.2, 4.2]
    assert payload is not None
    assert payload["status"] == "synced"
    assert payload["composition_duration"] == 6.4
    assert payload["scenes"][1]["start"] == 2.2


def test_edge_tts_narration_passes_prosody_options(monkeypatch, tmp_path) -> None:
    commands = []

    def fake_run(cmd):
        commands.append(cmd)
        (tmp_path / "narration_edge.mp3").write_bytes(b"audio")
        (tmp_path / "narration_edge.srt").write_text(
            "1\n00:00:00,000 --> 00:00:01,000\nHello.\n",
            encoding="utf-8",
        )

    monkeypatch.setattr("daily_video_pipeline.renderer._run", fake_run)

    audio_path, subtitle_path = _build_narration(
        [ScriptScene(title="Hello", body="World", kicker="", source_label="")],
        tmp_path,
        {
            "enabled": True,
            "engine": "edge-tts",
            "voice": "zh-CN-XiaoxiaoNeural",
            "rate": "+6%",
            "pitch": "+2Hz",
            "volume": "+0%",
        },
        duration=1.0,
    )

    assert audio_path.name == "narration_edge.mp3"
    assert subtitle_path is not None
    command = commands[0]
    assert command[command.index("--voice") + 1] == "zh-CN-XiaoxiaoNeural"
    assert command[command.index("--rate") + 1] == "+6%"
    assert command[command.index("--pitch") + 1] == "+2Hz"
    assert command[command.index("--volume") + 1] == "+0%"


def test_demo_bgm_is_stereo_music_bed(tmp_path) -> None:
    path = tmp_path / "demo_bgm.wav"

    _write_demo_bgm(path, duration=2.0, volume=0.18)

    with wave.open(str(path), "rb") as wav:
        assert wav.getnchannels() == 2
        assert wav.getframerate() == 44100
        raw = wav.readframes(wav.getnframes())

    samples = array("h")
    samples.frombytes(raw)
    if sys.byteorder == "big":
        samples.byteswap()
    left = samples[0::2]
    right = samples[1::2]
    assert max(abs(value) for value in left) > 200
    assert sum(abs(left[index] - right[index]) for index in range(0, len(left), 400)) > 1000

    chunk_size = len(left) // 8
    rms_values = []
    for index in range(8):
        chunk = left[index * chunk_size : (index + 1) * chunk_size]
        rms_values.append(math.sqrt(sum(value * value for value in chunk) / max(len(chunk), 1)))
    assert max(rms_values) - min(rms_values) > 40


def test_local_bgm_mix_applies_fades(monkeypatch, tmp_path) -> None:
    commands = []
    bgm_path = tmp_path / "licensed_bgm.mp3"
    narration_path = tmp_path / "narration.m4a"
    bgm_path.write_bytes(b"bgm")
    narration_path.write_bytes(b"narration")

    def fake_run(cmd):
        commands.append(cmd)
        (tmp_path / "audio.m4a").write_bytes(b"mixed")

    monkeypatch.setattr("daily_video_pipeline.renderer._run", fake_run)

    audio_path = _build_audio(
        tmp_path,
        {"path": str(bgm_path), "volume": 0.09},
        narration_path,
        duration=12.0,
    )

    assert audio_path == tmp_path / "audio.m4a"
    filter_complex = commands[0][commands[0].index("-filter_complex") + 1]
    assert "volume=0.09" in filter_complex
    assert "afade=t=in:st=0:d=0.800" in filter_complex
    assert "afade=t=out:st=11.200:d=0.800" in filter_complex
    assert "amix=inputs=2" in filter_complex
