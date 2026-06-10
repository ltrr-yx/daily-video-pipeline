from __future__ import annotations

import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import ScriptScene
from .script_writer import narration_text
from .templates import get_component, get_theme


def render_video(
    scenes: list[ScriptScene],
    *,
    output_dir: Path,
    video_config: dict,
    narration_config: dict,
    music_config: dict,
) -> Path:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required to render video. Install ffmpeg and try again.")

    width = int(video_config.get("width", 1080))
    height = int(video_config.get("height", 1920))
    seconds_per_scene = float(video_config.get("seconds_per_scene", 5))
    fps = int(video_config.get("fps", 30))

    frame_dir = output_dir / "frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    frame_paths: list[Path] = []
    frame_durations: list[float] = []
    for index, scene in enumerate(scenes):
        beat_durations = _beat_durations(scene, seconds_per_scene)
        for phase, beat_duration in enumerate(beat_durations):
            frame_path = frame_dir / f"scene_{index:02d}_beat_{phase:02d}.png"
            _draw_scene(
                scene,
                frame_path,
                index=index,
                width=width,
                height=height,
                video_config=video_config,
                phase=phase,
                total_phases=len(beat_durations),
            )
            frame_paths.append(frame_path)
            frame_durations.append(beat_duration)

    duration = max(sum(frame_durations), 1.0)
    _make_contact_sheet(frame_paths, output_dir / "review_contact_sheet.jpg")

    concat_path = output_dir / "frames.txt"
    _write_concat_file(concat_path, frame_paths, frame_durations)
    silent_video = output_dir / "video_silent.mp4"
    _run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-vf",
            f"fps={fps},format=yuv420p",
            "-r",
            str(fps),
            str(silent_video),
        ]
    )

    narration_path = _build_narration(scenes, output_dir, narration_config, duration)
    audio_path = _build_audio(output_dir, music_config, narration_path, duration)
    video_path = output_dir / "daily-video.mp4"
    _run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(silent_video),
            "-i",
            str(audio_path),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            str(video_path),
        ]
    )
    return video_path


def _draw_scene(
    scene: ScriptScene,
    path: Path,
    *,
    index: int,
    width: int,
    height: int,
    video_config: dict,
    phase: int,
    total_phases: int,
) -> None:
    theme = _theme(video_config)
    bg = theme["background"]
    fg = theme["foreground"]
    accent = theme["accent"]
    muted = theme["muted"]
    panel = theme["panel"]

    image = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(image)
    fonts = {
        "small": _font(video_config.get("font_path"), 30),
        "label": _font(video_config.get("font_path"), 34),
        "body": _font(video_config.get("font_path"), 42),
        "title": _font(video_config.get("font_path"), 72),
        "hero": _font(video_config.get("font_path"), 88),
        "metric": _font(video_config.get("font_path"), 96),
    }

    margin = int(width * 0.075)
    _draw_background_grid(draw, width, height, theme)
    _draw_header(draw, scene, width, margin, fonts, theme, index=index)

    component = get_component(scene.component)
    family = component.family
    content_box = (margin, 210, width - margin, height - 265)
    if family == "cover":
        _render_cover(draw, scene, content_box, fonts, theme, phase)
    elif family in {"grid", "context"}:
        _render_grid(draw, scene, content_box, fonts, theme, phase)
    elif family in {"proof", "chips", "rail"}:
        _render_proof(draw, scene, content_box, fonts, theme, phase)
    elif family == "metric":
        _render_metric(draw, scene, content_box, fonts, theme, phase)
    elif family == "split":
        _render_split(draw, scene, content_box, fonts, theme, phase)
    elif family == "timeline":
        _render_timeline(draw, scene, content_box, fonts, theme, phase)
    elif family == "matrix":
        _render_matrix(draw, scene, content_box, fonts, theme, phase)
    elif family == "mechanism":
        _render_mechanism(draw, scene, content_box, fonts, theme, phase)
    elif family in {"ledger", "ranking"}:
        _render_ledger(draw, scene, content_box, fonts, theme, phase)
    elif family in {"product", "map"}:
        _render_product_or_map(draw, scene, content_box, fonts, theme, phase)
    elif family in {"list", "stamp"}:
        _render_stamp(draw, scene, content_box, fonts, theme, phase)
    else:
        _render_grid(draw, scene, content_box, fonts, theme, phase)

    _draw_footer(draw, scene, width, height, margin, fonts, theme, phase, total_phases)
    image.save(path)


def _theme(video_config: dict) -> dict:
    theme = get_theme(video_config.get("theme"))
    palette = video_config.get("palette") or {}
    for key in ("background", "panel", "panel_alt", "foreground", "muted", "accent", "accent2", "danger"):
        if key in palette:
            theme[key] = tuple(palette[key])
    return theme


def _draw_background_grid(draw: ImageDraw.ImageDraw, width: int, height: int, theme: dict) -> None:
    panel_alt = theme["panel_alt"]
    accent = theme["accent"]
    for x in range(80, width, 180):
        draw.line((x, 0, x, height), fill=_blend(theme["background"], panel_alt, 0.18), width=1)
    for y in range(160, height, 220):
        draw.line((0, y, width, y), fill=_blend(theme["background"], panel_alt, 0.14), width=1)
    draw.rectangle((0, 0, width, 18), fill=accent)


def _draw_header(
    draw: ImageDraw.ImageDraw,
    scene: ScriptScene,
    width: int,
    margin: int,
    fonts: dict,
    theme: dict,
    *,
    index: int,
) -> None:
    accent = theme["accent"]
    muted = theme["muted"]
    top = 86
    _pill(draw, (margin, top, margin + 260, top + 52), scene.kicker.upper(), fonts["small"], theme)
    grammar = _fit_text(draw, scene.visual_grammar.replace("_", " ").upper(), fonts["small"], 360)
    draw.text((width - margin - 455, top + 10), grammar, font=fonts["small"], fill=muted)
    draw.text((width - margin - 52, top + 8), f"{index + 1:02d}", font=fonts["label"], fill=accent)


def _draw_footer(
    draw: ImageDraw.ImageDraw,
    scene: ScriptScene,
    width: int,
    height: int,
    margin: int,
    fonts: dict,
    theme: dict,
    phase: int,
    total_phases: int,
) -> None:
    y = height - 205
    muted = theme["muted"]
    accent = theme["accent"]
    draw.line((margin, y, width - margin, y), fill=_blend(muted, theme["background"], 0.28), width=2)
    if phase >= 2:
        _draw_text(draw, scene.source_label, margin, y + 35, width - margin * 2 - 170, fonts["label"], muted, max_lines=1)
    progress_w = 132
    progress_x = width - margin - progress_w
    draw.rounded_rectangle((progress_x, y + 48, progress_x + progress_w, y + 60), radius=6, fill=_blend(muted, theme["background"], 0.3))
    fill_w = int(progress_w * ((phase + 1) / max(total_phases, 1)))
    draw.rounded_rectangle((progress_x, y + 48, progress_x + fill_w, y + 60), radius=6, fill=accent)


def _render_cover(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    accent = theme["accent"]
    accent2 = theme["accent2"]
    fg = theme["foreground"]
    muted = theme["muted"]
    draw.rounded_rectangle((x1, y1 + 420, x2, y2 - 120), radius=28, outline=_blend(accent, theme["background"], 0.55), width=3)
    draw.arc((x2 - 360, y1 + 70, x2 + 240, y1 + 670), 120, 330, fill=_blend(accent2, theme["background"], 0.2), width=18)
    if phase >= 0:
        draw.text((x1, y1 + 40), scene.eyebrow or scene.kicker, font=fonts["label"], fill=accent)
    if phase >= 1:
        _draw_text(draw, scene.title, x1, y1 + 130, x2 - x1 - 50, fonts["hero"], fg, line_gap=20, max_lines=4)
    if phase >= 2:
        _draw_text(draw, scene.body, x1, y1 + 560, x2 - x1 - 80, fonts["body"], muted, line_gap=16, max_lines=4)
    if phase >= 3 and scene.metrics:
        _metric_row(draw, scene.metrics[:3], x1, y2 - 250, x2 - x1, fonts, theme)


def _render_grid(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, _ = box
    _section_title(draw, scene, box, fonts, theme, phase)
    card_w = (x2 - x1 - 28) // 2
    card_h = 230
    bullets = scene.bullets or (scene.body,)
    for idx, bullet in enumerate(bullets[:4]):
        if phase < 1 + idx // 2:
            continue
        col = idx % 2
        row = idx // 2
        cx = x1 + col * (card_w + 28)
        cy = y1 + 430 + row * (card_h + 26)
        _card(draw, (cx, cy, cx + card_w, cy + card_h), theme, outline=idx == 0)
        draw.text((cx + 30, cy + 26), f"{idx + 1:02d}", font=fonts["label"], fill=theme["accent"])
        _draw_text(draw, bullet, cx + 30, cy + 84, card_w - 60, fonts["body"], theme["foreground"], max_lines=3)
    if phase >= 3 and scene.proof:
        _draw_text(draw, scene.proof, x1, y1 + 970, x2 - x1, fonts["label"], theme["muted"], max_lines=3)


def _render_proof(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, phase)
    rail_y = y1 + 590
    draw.line((x1 + 40, rail_y, x2 - 40, rail_y), fill=theme["accent"], width=5)
    stops = scene.bullets[:4] or ("source", "date", "tag", "review")
    span = (x2 - x1 - 80) / max(len(stops) - 1, 1)
    for idx, stop in enumerate(stops):
        if phase < idx:
            continue
        cx = int(x1 + 40 + idx * span)
        draw.ellipse((cx - 18, rail_y - 18, cx + 18, rail_y + 18), fill=theme["accent2"] if idx == len(stops) - 1 else theme["accent"])
        _draw_text(draw, stop, cx - 90, rail_y + 46, 180, fonts["small"], theme["muted"], max_lines=2, align="center")
    if phase >= 2:
        quote_box = (x1, y1 + 780, x2, min(y2 - 90, y1 + 1150))
        _card(draw, quote_box, theme, outline=True)
        draw.text((x1 + 36, quote_box[1] + 26), "SOURCE EVIDENCE", font=fonts["small"], fill=theme["accent"])
        _draw_text(draw, scene.proof or scene.body, x1 + 36, quote_box[1] + 88, x2 - x1 - 72, fonts["body"], theme["foreground"], max_lines=5)


def _render_metric(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, phase)
    metrics = scene.metrics or (("score", "0.0"), ("sources", "0"), ("items", "0"))
    top = y1 + 430
    for idx, (label, value) in enumerate(metrics[:4]):
        if phase < idx:
            continue
        card = (x1, top + idx * 190, x2, top + idx * 190 + 150)
        _card(draw, card, theme, outline=idx == 0)
        draw.text((card[0] + 34, card[1] + 30), value, font=fonts["metric"], fill=theme["accent"] if idx == 0 else theme["foreground"])
        draw.text((card[0] + 360, card[1] + 58), label.upper(), font=fonts["label"], fill=theme["muted"])
        _sparkline(draw, (card[0] + 640, card[1] + 44, card[2] - 34, card[3] - 34), theme, idx)
    if phase >= 3:
        _draw_text(draw, scene.body, x1, y2 - 210, x2 - x1, fonts["label"], theme["muted"], max_lines=3)


def _render_split(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, phase)
    gap = 28
    mid = (x1 + x2) // 2
    left = (x1, y1 + 440, mid - gap // 2, y2 - 150)
    right = (mid + gap // 2, y1 + 440, x2, y2 - 150)
    labels = scene.bullets or ("Before", "After")
    if phase >= 1:
        _card(draw, left, theme)
        draw.text((left[0] + 30, left[1] + 30), "BEFORE", font=fonts["small"], fill=theme["muted"])
        _draw_text(draw, labels[0], left[0] + 30, left[1] + 115, left[2] - left[0] - 60, fonts["body"], theme["foreground"], max_lines=6)
    if phase >= 2:
        _card(draw, right, theme, outline=True)
        draw.text((right[0] + 30, right[1] + 30), "AFTER", font=fonts["small"], fill=theme["accent"])
        _draw_text(draw, labels[min(1, len(labels) - 1)], right[0] + 30, right[1] + 115, right[2] - right[0] - 60, fonts["body"], theme["foreground"], max_lines=6)
    if phase >= 3:
        draw.line((mid, y1 + 470, mid, y2 - 190), fill=theme["accent2"], width=4)


def _render_timeline(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, phase)
    rail_x = x1 + 72
    rail_top = y1 + 440
    rail_bottom = y2 - 170
    draw.line((rail_x, rail_top, rail_x, rail_bottom), fill=theme["accent"], width=5)
    bullets = scene.bullets[:4] or ("Signal", "Proof", "Impact", "Next check")
    step = (rail_bottom - rail_top) / max(len(bullets) - 1, 1)
    for idx, bullet in enumerate(bullets):
        if phase < idx:
            continue
        cy = int(rail_top + idx * step)
        draw.ellipse((rail_x - 18, cy - 18, rail_x + 18, cy + 18), fill=theme["accent2"] if idx == len(bullets) - 1 else theme["accent"])
        card = (rail_x + 58, cy - 70, x2, cy + 80)
        _card(draw, card, theme)
        _draw_text(draw, bullet, card[0] + 24, card[1] + 35, card[2] - card[0] - 48, fonts["label"], theme["foreground"], max_lines=2)


def _render_matrix(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, _ = box
    _section_title(draw, scene, box, fonts, theme, phase)
    labels = ("Upside", "Evidence", "Risk", "Next check")
    bullets = scene.bullets or labels
    card_w = (x2 - x1 - 28) // 2
    card_h = 235
    for idx, label in enumerate(labels):
        if phase < idx:
            continue
        cx = x1 + (idx % 2) * (card_w + 28)
        cy = y1 + 440 + (idx // 2) * (card_h + 28)
        _card(draw, (cx, cy, cx + card_w, cy + card_h), theme, outline=idx == 3)
        draw.text((cx + 28, cy + 28), label.upper(), font=fonts["small"], fill=theme["accent"] if idx != 2 else theme["danger"])
        _draw_text(draw, bullets[min(idx, len(bullets) - 1)], cx + 28, cy + 88, card_w - 56, fonts["label"], theme["foreground"], max_lines=3)


def _render_mechanism(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, phase)
    labels = scene.bullets or ("Input", "Mechanism", "Consequence")
    band_h = 190
    top = y1 + 455
    for idx, label in enumerate(labels[:3]):
        if phase < idx:
            continue
        y = top + idx * 245
        _card(draw, (x1 + idx * 34, y, x2 - idx * 34, y + band_h), theme, outline=idx == 2)
        draw.text((x1 + idx * 34 + 32, y + 28), label.upper(), font=fonts["small"], fill=theme["accent"])
        body = scene.proof if idx == 1 else scene.body
        _draw_text(draw, body, x1 + idx * 34 + 32, y + 86, x2 - x1 - 110, fonts["label"], theme["foreground"], max_lines=2)
        if idx < 2 and phase >= idx + 1:
            cx = (x1 + x2) // 2
            draw.polygon([(cx - 18, y + band_h + 34), (cx + 18, y + band_h + 34), (cx, y + band_h + 72)], fill=theme["accent2"])


def _render_ledger(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, _ = box
    _section_title(draw, scene, box, fonts, theme, phase)
    rows = scene.bullets[:5] or (scene.title,)
    top = y1 + 430
    for idx, row in enumerate(rows):
        if phase < min(idx, 3):
            continue
        y = top + idx * 145
        _card(draw, (x1, y, x2, y + 112), theme, outline=idx == 0)
        draw.text((x1 + 26, y + 32), f"{idx + 1:02d}", font=fonts["label"], fill=theme["accent"])
        _draw_text(draw, row, x1 + 105, y + 32, x2 - x1 - 260, fonts["label"], theme["foreground"], max_lines=1)
        value = scene.metrics[idx % len(scene.metrics)][1] if scene.metrics else f"{idx + 1}"
        draw.text((x2 - 150, y + 28), value, font=fonts["label"], fill=theme["accent2"])


def _render_product_or_map(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, phase)
    plate = (x1 + 60, y1 + 470, x2 - 60, y1 + 960)
    _card(draw, plate, theme, outline=True)
    cx = (plate[0] + plate[2]) // 2
    cy = (plate[1] + plate[3]) // 2
    draw.ellipse((cx - 92, cy - 92, cx + 92, cy + 92), outline=theme["accent"], width=5)
    draw.rounded_rectangle((cx - 165, cy - 42, cx + 165, cy + 42), radius=24, fill=_blend(theme["accent"], theme["panel"], 0.25), outline=theme["accent"])
    if phase >= 1:
        draw.text((plate[0] + 48, plate[1] + 42), "VISUAL ANCHOR", font=fonts["small"], fill=theme["accent"])
        draw.line((plate[0] + 90, cy, cx - 178, cy), fill=theme["accent"], width=3)
        draw.line((cx + 178, cy, plate[2] - 90, cy), fill=theme["accent"], width=3)
        _draw_text(draw, scene.proof, plate[0] + 70, plate[3] - 112, plate[2] - plate[0] - 140, fonts["small"], theme["muted"], max_lines=2, align="center")
    if phase >= 2:
        for idx, bullet in enumerate(scene.bullets[:3]):
            bx = x1 + idx * ((x2 - x1) // 3)
            _pill(draw, (bx + 20, y2 - 250, bx + 285, y2 - 190), bullet, fonts["small"], theme)


def _render_stamp(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, phase: int) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, phase)
    if phase >= 1:
        stamp = (x1 + 60, y1 + 500, x2 - 60, y1 + 900)
        _card(draw, stamp, theme, outline=True)
        draw.text((stamp[0] + 42, stamp[1] + 42), "VERDICT", font=fonts["small"], fill=theme["accent"])
        _draw_text(draw, scene.body, stamp[0] + 42, stamp[1] + 110, stamp[2] - stamp[0] - 84, fonts["body"], theme["foreground"], max_lines=4)
    if phase >= 2:
        for idx, bullet in enumerate(scene.bullets[:4]):
            y = y1 + 980 + idx * 92
            draw.ellipse((x1 + 15, y + 15, x1 + 43, y + 43), fill=theme["accent2"] if idx == 3 else theme["accent"])
            _draw_text(draw, bullet, x1 + 70, y, x2 - x1 - 90, fonts["label"], theme["muted"], max_lines=1)


def _section_title(
    draw: ImageDraw.ImageDraw,
    scene: ScriptScene,
    box: tuple[int, int, int, int],
    fonts: dict,
    theme: dict,
    phase: int,
) -> None:
    x1, y1, x2, _ = box
    if phase >= 0:
        draw.text((x1, y1), scene.eyebrow or scene.kicker, font=fonts["label"], fill=theme["accent"])
    if phase >= 1:
        _draw_text(draw, scene.title, x1, y1 + 74, x2 - x1, fonts["title"], theme["foreground"], line_gap=14, max_lines=2)
    if phase >= 2:
        _draw_text(draw, scene.body, x1, y1 + 285, x2 - x1, fonts["label"], theme["muted"], line_gap=10, max_lines=2)


def _metric_row(
    draw: ImageDraw.ImageDraw,
    metrics: tuple[tuple[str, str], ...],
    x: int,
    y: int,
    width: int,
    fonts: dict,
    theme: dict,
) -> None:
    gap = 18
    card_w = (width - gap * (len(metrics) - 1)) // max(len(metrics), 1)
    for idx, (label, value) in enumerate(metrics):
        left = x + idx * (card_w + gap)
        _card(draw, (left, y, left + card_w, y + 145), theme)
        draw.text((left + 22, y + 24), value, font=fonts["title"], fill=theme["accent"])
        draw.text((left + 22, y + 96), label.upper(), font=fonts["small"], fill=theme["muted"])


def _sparkline(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], theme: dict, offset: int) -> None:
    x1, y1, x2, y2 = box
    points = []
    width = x2 - x1
    height = y2 - y1
    for idx in range(6):
        x = x1 + int(width * idx / 5)
        y = y2 - int(height * ((idx + 1 + offset) % 5 + 1) / 6)
        points.append((x, y))
    draw.line(points, fill=theme["accent2"], width=4)
    for point in points:
        draw.ellipse((point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5), fill=theme["accent2"])


def _card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], theme: dict, *, outline: bool = False) -> None:
    fill = theme["panel"]
    line = theme["accent"] if outline else _blend(theme["muted"], theme["background"], 0.22)
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=line, width=3 if outline else 1)


def _pill(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font: ImageFont.ImageFont, theme: dict) -> None:
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=_blend(theme["accent"], theme["panel"], 0.22), outline=theme["accent"])
    text = _fit_text(draw, text, font, box[2] - box[0] - 30)
    tw = _text_width(draw, text, font)
    x = box[0] + max(16, (box[2] - box[0] - tw) // 2)
    y = box[1] + max(6, (box[3] - box[1] - 28) // 2)
    draw.text((x, y), text, font=font, fill=theme["accent"])


def _draw_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    max_width: int,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    *,
    line_gap: int = 12,
    max_lines: int = 4,
    align: str = "left",
) -> int:
    lines = _wrap(draw, text, font, max_width)
    lines = lines[:max_lines]
    for line in lines:
        tx = x
        if align == "center":
            tx = x + max(0, (max_width - _text_width(draw, line, font)) // 2)
        draw.text((tx, y), line, font=font, fill=fill)
        box = draw.textbbox((tx, y), line, font=font)
        y += box[3] - box[1] + line_gap
    return y


def _fit_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    value = text.strip()
    if _text_width(draw, value, font) <= max_width:
        return value
    suffix = "..."
    while value and _text_width(draw, value + suffix, font) > max_width:
        value = value[:-1]
    return (value + suffix) if value else suffix


def _blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _beat_durations(scene: ScriptScene, fallback_duration: float) -> list[float]:
    duration = max(float(scene.duration or fallback_duration), 2.4)
    first = min(0.45, duration * 0.16)
    second = min(0.75, duration * 0.22)
    third = min(0.9, duration * 0.24)
    hold = max(0.8, duration - first - second - third)
    return [round(first, 3), round(second, 3), round(third, 3), round(hold, 3)]


def _make_contact_sheet(frame_paths: list[Path], path: Path) -> None:
    if not frame_paths:
        return
    hold_frames = [frame for frame in frame_paths if frame.name.endswith("beat_03.png")]
    if not hold_frames:
        hold_frames = frame_paths[-6:]
    thumbs = []
    for frame in hold_frames[:8]:
        image = Image.open(frame).convert("RGB")
        image.thumbnail((216, 384))
        thumbs.append(image.copy())
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 216, rows * 384), (10, 10, 10))
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((idx % cols) * 216, (idx // cols) * 384))
    sheet.save(path)


def _font(configured_path: str | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        configured_path,
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    if not text:
        return [""]
    words = text.split()
    if len(words) <= 1:
        chunks = textwrap.wrap(text, width=18) or [text]
    else:
        chunks = []
        line = ""
        for word in words:
            trial = f"{line} {word}".strip()
            if line and _text_width(draw, trial, font) > max_width:
                chunks.append(line)
                line = word
            else:
                line = trial
        if line:
            chunks.append(line)
    final: list[str] = []
    for chunk in chunks:
        while _text_width(draw, chunk, font) > max_width and len(chunk) > 8:
            cut = max(8, int(len(chunk) * max_width / max(_text_width(draw, chunk, font), 1)))
            final.append(chunk[:cut])
            chunk = chunk[cut:]
        final.append(chunk)
    return final


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def _write_concat_file(path: Path, frames: list[Path], durations: list[float]) -> None:
    lines: list[str] = []
    for frame, duration in zip(frames, durations):
        lines.append(f"file '{frame.resolve().as_posix()}'")
        lines.append(f"duration {duration}")
    lines.append(f"file '{frames[-1].resolve().as_posix()}'")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _build_narration(
    scenes: list[ScriptScene],
    output_dir: Path,
    narration_config: dict,
    duration: float,
) -> Path:
    narration_path = output_dir / "narration.m4a"
    if not narration_config.get("enabled", False):
        return _silent_audio(narration_path, duration)

    engine = str(narration_config.get("engine", "auto"))
    voice = str(narration_config.get("voice", "zh-CN-YunyangNeural"))
    text_path = output_dir / "narration.txt"
    text_path.write_text(narration_text(scenes), encoding="utf-8")

    if engine in {"auto", "edge-tts"}:
        edge_output = output_dir / "narration_edge.mp3"
        try:
            _run(
                [
                    sys.executable,
                    "-m",
                    "edge_tts",
                    "--voice",
                    voice,
                    "--text",
                    text_path.read_text(encoding="utf-8"),
                    "--write-media",
                    str(edge_output),
                ]
            )
            return edge_output
        except Exception:
            if engine == "edge-tts":
                raise

    say = shutil.which("say")
    if engine in {"auto", "say"} and say:
        aiff_path = output_dir / "narration.aiff"
        _run([say, "-o", str(aiff_path), "-f", str(text_path)])
        _run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(aiff_path), str(narration_path)])
        return narration_path

    return _silent_audio(narration_path, duration)


def _build_audio(output_dir: Path, music_config: dict, narration_path: Path, duration: float) -> Path:
    audio_path = output_dir / "audio.m4a"
    music_path = music_config.get("path")
    volume = float(music_config.get("volume", 0.18))
    generate_tone = bool(music_config.get("generate_demo_tone_if_missing", False))

    if music_path and Path(str(music_path)).expanduser().exists():
        bgm_path = Path(str(music_path)).expanduser()
        _run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-stream_loop",
                "-1",
                "-i",
                str(bgm_path),
                "-i",
                str(narration_path),
                "-t",
                str(duration),
                "-filter_complex",
                f"[0:a]volume={volume}[bgm];[1:a]volume=1.0[narr];[bgm][narr]amix=inputs=2:duration=first:dropout_transition=2[a]",
                "-map",
                "[a]",
                "-c:a",
                "aac",
                str(audio_path),
            ]
        )
        return audio_path

    if generate_tone:
        tone_path = output_dir / "demo_bgm.wav"
        _run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                f"sine=frequency=220:duration={duration}",
                "-af",
                f"volume={volume}",
                str(tone_path),
            ]
        )
        _run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(tone_path),
                "-i",
                str(narration_path),
                "-filter_complex",
                "[0:a][1:a]amix=inputs=2:duration=first[a]",
                "-map",
                "[a]",
                "-c:a",
                "aac",
                str(audio_path),
            ]
        )
        return audio_path

    return _silent_audio(audio_path, duration)


def _silent_audio(path: Path, duration: float) -> Path:
    _run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-t",
            str(duration),
            "-c:a",
            "aac",
            str(path),
        ]
    )
    return path


def _run(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        command = json.dumps(cmd, ensure_ascii=False)
        raise RuntimeError(f"Command failed: {command}") from exc
