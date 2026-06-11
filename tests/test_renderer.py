from __future__ import annotations

from array import array
import math
import sys
import wave

from PIL import Image, ImageDraw

from daily_video_pipeline.models import ScriptScene
from daily_video_pipeline.renderer import (
    _audience_header_label,
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
