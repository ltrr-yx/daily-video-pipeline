from __future__ import annotations

from array import array
import json
import math
import shutil
import subprocess
import sys
import wave
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
    review_paths: list[Path] = []
    for index, scene in enumerate(scenes):
        scene_duration = max(float(scene.duration or seconds_per_scene), 2.4)
        frame_count = _motion_frame_count(scene_duration, video_config)
        frame_duration = scene_duration / frame_count
        for frame_index in range(frame_count):
            progress = frame_index / max(frame_count - 1, 1)
            frame_path = frame_dir / f"scene_{index:02d}_frame_{frame_index:02d}.png"
            _draw_scene(
                scene,
                frame_path,
                index=index,
                width=width,
                height=height,
                video_config=video_config,
                progress=progress,
                frame_index=frame_index,
                total_frames=frame_count,
            )
            frame_paths.append(frame_path)
            frame_durations.append(round(frame_duration, 3))
        review_paths.append(frame_paths[-1])

    duration = max(sum(frame_durations), 1.0)
    _make_contact_sheet(review_paths or frame_paths, output_dir / "review_contact_sheet.jpg")

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
    progress: float,
    frame_index: int,
    total_frames: int,
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
        "caption": _font(video_config.get("font_path"), 26),
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
        _render_cover(draw, scene, content_box, fonts, theme, progress)
    elif family in {"grid", "context"}:
        _render_grid(draw, scene, content_box, fonts, theme, progress)
    elif family in {"proof", "chips", "rail"}:
        _render_proof(draw, scene, content_box, fonts, theme, progress)
    elif family == "metric":
        _render_metric(draw, scene, content_box, fonts, theme, progress)
    elif family == "split":
        _render_split(draw, scene, content_box, fonts, theme, progress)
    elif family == "timeline":
        _render_timeline(draw, scene, content_box, fonts, theme, progress)
    elif family == "matrix":
        _render_matrix(draw, scene, content_box, fonts, theme, progress)
    elif family == "mechanism":
        _render_mechanism(draw, scene, content_box, fonts, theme, progress)
    elif family in {"ledger", "ranking"}:
        _render_ledger(draw, scene, content_box, fonts, theme, progress)
    elif family in {"product", "map"}:
        _render_product_or_map(draw, scene, content_box, fonts, theme, progress)
    elif family in {"list", "stamp"}:
        _render_stamp(draw, scene, content_box, fonts, theme, progress)
    else:
        _render_grid(draw, scene, content_box, fonts, theme, progress)

    _draw_footer(draw, scene, width, height, margin, fonts, theme, progress)
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
    top = 86
    tag = _audience_header_label(scene).upper()
    tag_width = min(420, max(220, _text_width(draw, tag, fonts["small"]) + 58))
    _pill(draw, (margin, top, margin + tag_width, top + 52), tag, fonts["small"], theme)
    draw.text((width - margin - 52, top + 8), f"{index + 1:02d}", font=fonts["label"], fill=accent)


def _audience_header_label(scene: ScriptScene) -> str:
    for value in (scene.eyebrow, scene.source_label):
        label = value.strip()
        if label:
            return label
    return "Daily update"


def _draw_footer(
    draw: ImageDraw.ImageDraw,
    scene: ScriptScene,
    width: int,
    height: int,
    margin: int,
    fonts: dict,
    theme: dict,
    progress: float,
) -> None:
    y = height - 205
    muted = theme["muted"]
    accent = theme["accent"]
    draw.line((margin, y, width - margin, y), fill=_blend(muted, theme["background"], 0.28), width=2)
    source_alpha = _stage(progress, 0.72, 0.86)
    if source_alpha > 0:
        _draw_text(draw, scene.source_label, margin, y + 35, width - margin * 2 - 170, fonts["label"], _fade(theme, muted, source_alpha), max_lines=1)
    progress_w = 132
    progress_x = width - margin - progress_w
    draw.rounded_rectangle((progress_x, y + 48, progress_x + progress_w, y + 60), radius=6, fill=_blend(muted, theme["background"], 0.3))
    fill_w = int(progress_w * progress)
    draw.rounded_rectangle((progress_x, y + 48, progress_x + fill_w, y + 60), radius=6, fill=accent)


def _render_cover(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    accent = theme["accent"]
    accent2 = theme["accent2"]
    fg = theme["foreground"]
    muted = theme["muted"]
    shell = _stage(progress, 0.04, 0.22)
    draw.rounded_rectangle((x1, y1 + 420, x2, y2 - 120), radius=28, outline=_fade(theme, accent, shell * 0.55), width=3)
    arc = _stage(progress, 0.14, 0.46)
    draw.arc((x2 - 360, y1 + 70, x2 + 240, y1 + 670), 120, 120 + int(210 * arc), fill=_fade(theme, accent2, 0.35), width=18)

    eyebrow = _stage(progress, 0.08, 0.24)
    if eyebrow > 0:
        draw.text((x1, y1 + 40 + int(18 * (1 - eyebrow))), _audience_header_label(scene), font=fonts["label"], fill=_fade(theme, accent, eyebrow))
    title = _stage(progress, 0.22, 0.52)
    if title > 0:
        _draw_text(draw, scene.title, x1, y1 + 130 + int(38 * (1 - title)), x2 - x1 - 50, fonts["hero"], _fade(theme, fg, title), line_gap=20, max_lines=4)
    body = _stage(progress, 0.50, 0.72)
    if body > 0:
        _draw_text(draw, scene.body, x1, y1 + 560 + int(24 * (1 - body)), x2 - x1 - 80, fonts["body"], _fade(theme, muted, body), line_gap=16, max_lines=4)
    metrics = _stage(progress, 0.70, 0.92)
    if scene.metrics and metrics > 0:
        _metric_row(draw, scene.metrics[:3], x1, y2 - 250 + int(22 * (1 - metrics)), x2 - x1, fonts, theme, progress=metrics)


def _render_grid(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, _ = box
    _section_title(draw, scene, box, fonts, theme, progress)
    card_w = (x2 - x1 - 28) // 2
    card_h = 250
    bullets = scene.bullets or (scene.body,)
    for idx, bullet in enumerate(bullets[:4]):
        reveal = _stage(progress, 0.42 + idx * 0.07, 0.64 + idx * 0.07)
        if reveal <= 0:
            continue
        col = idx % 2
        row = idx // 2
        cx = x1 + col * (card_w + 28)
        cy = y1 + 410 + row * (card_h + 24) + int(28 * (1 - reveal))
        _card(draw, (cx, cy, cx + card_w, cy + card_h), theme, outline=idx == 0, alpha=reveal)
        draw.text((cx + 30, cy + 26), f"{idx + 1:02d}", font=fonts["label"], fill=_fade(theme, theme["accent"], reveal))
        _draw_text_in_box(
            draw,
            bullet,
            cx + 30,
            cy + 88,
            card_w - 60,
            card_h - 122,
            [
                (fonts["small"], 6, 3),
                (fonts["caption"], 5, 4),
            ],
            _fade(theme, theme["foreground"], reveal),
        )
    proof = _stage(progress, 0.78, 0.94)
    if scene.proof and proof > 0:
        _draw_text(draw, scene.proof, x1, y1 + 970 + int(16 * (1 - proof)), x2 - x1, fonts["label"], _fade(theme, theme["muted"], proof), max_lines=3)


def _render_proof(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, progress)
    rail_y = y1 + 590
    rail = _stage(progress, 0.28, 0.56)
    rail_end = x1 + 40 + int((x2 - x1 - 80) * rail)
    draw.line((x1 + 40, rail_y, rail_end, rail_y), fill=_fade(theme, theme["accent"], max(rail, 0.12)), width=5)
    stops = scene.bullets[:4] or ("source", "date", "tag", "review")
    span = (x2 - x1 - 80) / max(len(stops) - 1, 1)
    for idx, stop in enumerate(stops):
        reveal = _stage(progress, 0.38 + idx * 0.08, 0.58 + idx * 0.08)
        if reveal <= 0:
            continue
        cx = int(x1 + 40 + idx * span)
        radius = int(10 + 8 * reveal)
        draw.ellipse((cx - radius, rail_y - radius, cx + radius, rail_y + radius), fill=_fade(theme, theme["accent2"] if idx == len(stops) - 1 else theme["accent"], reveal))
        _draw_text(draw, stop, cx - 90, rail_y + 46 + int(14 * (1 - reveal)), 180, fonts["small"], _fade(theme, theme["muted"], reveal), max_lines=2, align="center")
    quote = _stage(progress, 0.66, 0.88)
    if quote > 0:
        quote_box = (x1, y1 + 780, x2, min(y2 - 90, y1 + 1150))
        quote_box = _shift_box(quote_box, int(24 * (1 - quote)))
        _card(draw, quote_box, theme, outline=True, alpha=quote)
        draw.text((quote_box[0] + 36, quote_box[1] + 26), "SOURCE EVIDENCE", font=fonts["small"], fill=_fade(theme, theme["accent"], quote))
        _draw_text(draw, scene.proof or scene.body, quote_box[0] + 36, quote_box[1] + 88, quote_box[2] - quote_box[0] - 72, fonts["body"], _fade(theme, theme["foreground"], quote), max_lines=5)


def _render_metric(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, progress)
    metrics = scene.metrics or (("score", "0.0"), ("sources", "0"), ("items", "0"))
    top = y1 + 430
    for idx, (label, value) in enumerate(metrics[:4]):
        reveal = _stage(progress, 0.36 + idx * 0.08, 0.58 + idx * 0.08)
        if reveal <= 0:
            continue
        card = (x1, top + idx * 190 + int(26 * (1 - reveal)), x2, top + idx * 190 + 150 + int(26 * (1 - reveal)))
        _card(draw, card, theme, outline=idx == 0, alpha=reveal)
        draw.text((card[0] + 34, card[1] + 30), value, font=fonts["metric"], fill=_fade(theme, theme["accent"] if idx == 0 else theme["foreground"], reveal))
        draw.text((card[0] + 360, card[1] + 58), label.upper(), font=fonts["label"], fill=_fade(theme, theme["muted"], reveal))
        _sparkline(draw, (card[0] + 640, card[1] + 44, card[2] - 34, card[3] - 34), theme, idx, progress=reveal)
    body = _stage(progress, 0.78, 0.94)
    if body > 0:
        _draw_text(draw, scene.body, x1, y2 - 210 + int(18 * (1 - body)), x2 - x1, fonts["label"], _fade(theme, theme["muted"], body), max_lines=3)


def _render_split(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, progress)
    gap = 28
    mid = (x1 + x2) // 2
    left = (x1, y1 + 440, mid - gap // 2, y2 - 150)
    right = (mid + gap // 2, y1 + 440, x2, y2 - 150)
    labels = scene.bullets or ("Before", "After")
    left_reveal = _stage(progress, 0.34, 0.58)
    if left_reveal > 0:
        left_box = _shift_box(left, int(28 * (1 - left_reveal)))
        _card(draw, left_box, theme, alpha=left_reveal)
        draw.text((left_box[0] + 30, left_box[1] + 30), "BEFORE", font=fonts["small"], fill=_fade(theme, theme["muted"], left_reveal))
        _draw_text(draw, labels[0], left_box[0] + 30, left_box[1] + 115, left_box[2] - left_box[0] - 60, fonts["body"], _fade(theme, theme["foreground"], left_reveal), max_lines=6)
    right_reveal = _stage(progress, 0.52, 0.76)
    if right_reveal > 0:
        right_box = _shift_box(right, int(28 * (1 - right_reveal)))
        _card(draw, right_box, theme, outline=True, alpha=right_reveal)
        draw.text((right_box[0] + 30, right_box[1] + 30), "AFTER", font=fonts["small"], fill=_fade(theme, theme["accent"], right_reveal))
        _draw_text(draw, labels[min(1, len(labels) - 1)], right_box[0] + 30, right_box[1] + 115, right_box[2] - right_box[0] - 60, fonts["body"], _fade(theme, theme["foreground"], right_reveal), max_lines=6)
    divider = _stage(progress, 0.74, 0.92)
    if divider > 0:
        y_end = y1 + 470 + int((y2 - 190 - (y1 + 470)) * divider)
        draw.line((mid, y1 + 470, mid, y_end), fill=_fade(theme, theme["accent2"], divider), width=4)


def _render_timeline(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, progress)
    rail_x = x1 + 72
    rail_top = y1 + 440
    rail_bottom = y2 - 170
    rail = _stage(progress, 0.30, 0.62)
    draw.line((rail_x, rail_top, rail_x, rail_top + int((rail_bottom - rail_top) * rail)), fill=_fade(theme, theme["accent"], max(rail, 0.12)), width=5)
    bullets = scene.bullets[:4] or ("Signal", "Proof", "Impact", "Next check")
    step = (rail_bottom - rail_top) / max(len(bullets) - 1, 1)
    for idx, bullet in enumerate(bullets):
        reveal = _stage(progress, 0.40 + idx * 0.09, 0.62 + idx * 0.09)
        if reveal <= 0:
            continue
        cy = int(rail_top + idx * step)
        radius = int(10 + 8 * reveal)
        draw.ellipse((rail_x - radius, cy - radius, rail_x + radius, cy + radius), fill=_fade(theme, theme["accent2"] if idx == len(bullets) - 1 else theme["accent"], reveal))
        card = (rail_x + 58, cy - 70 + int(20 * (1 - reveal)), x2, cy + 80 + int(20 * (1 - reveal)))
        _card(draw, card, theme, alpha=reveal)
        _draw_text(draw, bullet, card[0] + 24, card[1] + 35, card[2] - card[0] - 48, fonts["label"], _fade(theme, theme["foreground"], reveal), max_lines=2)


def _render_matrix(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, _ = box
    _section_title(draw, scene, box, fonts, theme, progress)
    labels = ("Upside", "Evidence", "Risk", "Next check")
    bullets = scene.bullets or labels
    card_w = (x2 - x1 - 28) // 2
    card_h = 235
    for idx, label in enumerate(labels):
        reveal = _stage(progress, 0.34 + idx * 0.08, 0.58 + idx * 0.08)
        if reveal <= 0:
            continue
        cx = x1 + (idx % 2) * (card_w + 28)
        cy = y1 + 440 + (idx // 2) * (card_h + 28) + int(24 * (1 - reveal))
        _card(draw, (cx, cy, cx + card_w, cy + card_h), theme, outline=idx == 3, alpha=reveal)
        draw.text((cx + 28, cy + 28), label.upper(), font=fonts["small"], fill=_fade(theme, theme["accent"] if idx != 2 else theme["danger"], reveal))
        _draw_text(draw, bullets[min(idx, len(bullets) - 1)], cx + 28, cy + 88, card_w - 56, fonts["label"], _fade(theme, theme["foreground"], reveal), max_lines=3)


def _render_mechanism(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, progress)
    labels = scene.bullets or ("Input", "Mechanism", "Consequence")
    band_h = 190
    top = y1 + 455
    for idx, label in enumerate(labels[:3]):
        reveal = _stage(progress, 0.34 + idx * 0.14, 0.58 + idx * 0.14)
        if reveal <= 0:
            continue
        y = top + idx * 245 + int(28 * (1 - reveal))
        _card(draw, (x1 + idx * 34, y, x2 - idx * 34, y + band_h), theme, outline=idx == 2, alpha=reveal)
        draw.text((x1 + idx * 34 + 32, y + 28), label.upper(), font=fonts["small"], fill=_fade(theme, theme["accent"], reveal))
        body = scene.proof if idx == 1 else scene.body
        _draw_text(draw, body, x1 + idx * 34 + 32, y + 86, x2 - x1 - 110, fonts["label"], _fade(theme, theme["foreground"], reveal), max_lines=2)
        arrow = _stage(progress, 0.50 + idx * 0.14, 0.64 + idx * 0.14)
        if idx < 2 and arrow > 0:
            cx = (x1 + x2) // 2
            draw.polygon([(cx - 18, y + band_h + 34), (cx + 18, y + band_h + 34), (cx, y + band_h + 72)], fill=_fade(theme, theme["accent2"], arrow))


def _render_ledger(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, _ = box
    _section_title(draw, scene, box, fonts, theme, progress)
    rows = scene.bullets[:5] or (scene.title,)
    top = y1 + 430
    for idx, row in enumerate(rows):
        reveal = _stage(progress, 0.34 + idx * 0.07, 0.56 + idx * 0.07)
        if reveal <= 0:
            continue
        y = top + idx * 145 + int(20 * (1 - reveal))
        _card(draw, (x1, y, x2, y + 112), theme, outline=idx == 0, alpha=reveal)
        draw.text((x1 + 26, y + 32), f"{idx + 1:02d}", font=fonts["label"], fill=_fade(theme, theme["accent"], reveal))
        _draw_text(draw, row, x1 + 105, y + 32, x2 - x1 - 260, fonts["label"], _fade(theme, theme["foreground"], reveal), max_lines=1)
        value = scene.metrics[idx % len(scene.metrics)][1] if scene.metrics else f"{idx + 1}"
        draw.text((x2 - 150, y + 28), value, font=fonts["label"], fill=_fade(theme, theme["accent2"], reveal))


def _render_product_or_map(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, progress)
    plate = (x1 + 60, y1 + 470, x2 - 60, y1 + 960)
    plate_reveal = _stage(progress, 0.26, 0.58)
    plate_box = _shift_box(plate, int(30 * (1 - plate_reveal)))
    _card(draw, plate_box, theme, outline=True, alpha=plate_reveal)
    cx = (plate_box[0] + plate_box[2]) // 2
    cy = (plate_box[1] + plate_box[3]) // 2
    draw.ellipse((cx - 92, cy - 92, cx + 92, cy + 92), outline=_fade(theme, theme["accent"], plate_reveal), width=5)
    draw.rounded_rectangle((cx - 165, cy - 42, cx + 165, cy + 42), radius=24, fill=_blend(theme["panel"], theme["accent"], 0.25 * plate_reveal), outline=_fade(theme, theme["accent"], plate_reveal))
    callout = _stage(progress, 0.54, 0.78)
    if callout > 0:
        draw.text((plate_box[0] + 48, plate_box[1] + 42), "VISUAL ANCHOR", font=fonts["small"], fill=_fade(theme, theme["accent"], callout))
        draw.line((plate_box[0] + 90, cy, cx - 178, cy), fill=_fade(theme, theme["accent"], callout), width=3)
        draw.line((cx + 178, cy, plate_box[2] - 90, cy), fill=_fade(theme, theme["accent"], callout), width=3)
        _draw_text(draw, scene.proof, plate_box[0] + 70, plate_box[3] - 112, plate_box[2] - plate_box[0] - 140, fonts["small"], _fade(theme, theme["muted"], callout), max_lines=2, align="center")
    chips = _stage(progress, 0.72, 0.92)
    if chips > 0:
        for idx, bullet in enumerate(scene.bullets[:3]):
            reveal = _stage(progress, 0.72 + idx * 0.06, 0.88 + idx * 0.06)
            if reveal <= 0:
                continue
            bx = x1 + idx * ((x2 - x1) // 3)
            _pill(draw, (bx + 20, y2 - 250 + int(16 * (1 - reveal)), bx + 285, y2 - 190 + int(16 * (1 - reveal))), bullet, fonts["small"], theme)


def _render_stamp(draw: ImageDraw.ImageDraw, scene: ScriptScene, box: tuple[int, int, int, int], fonts: dict, theme: dict, progress: float) -> None:
    x1, y1, x2, y2 = box
    _section_title(draw, scene, box, fonts, theme, progress)
    stamp_reveal = _stage(progress, 0.36, 0.66)
    if stamp_reveal > 0:
        stamp = (x1 + 60, y1 + 500, x2 - 60, y1 + 900)
        stamp = _shift_box(stamp, int(26 * (1 - stamp_reveal)))
        _card(draw, stamp, theme, outline=True, alpha=stamp_reveal)
        draw.text((stamp[0] + 42, stamp[1] + 42), "VERDICT", font=fonts["small"], fill=_fade(theme, theme["accent"], stamp_reveal))
        _draw_text(draw, scene.body, stamp[0] + 42, stamp[1] + 110, stamp[2] - stamp[0] - 84, fonts["body"], _fade(theme, theme["foreground"], stamp_reveal), max_lines=4)
    checks = _stage(progress, 0.62, 0.94)
    if checks > 0:
        for idx, bullet in enumerate(scene.bullets[:4]):
            reveal = _stage(progress, 0.62 + idx * 0.06, 0.78 + idx * 0.06)
            if reveal <= 0:
                continue
            y = y1 + 980 + idx * 92 + int(14 * (1 - reveal))
            draw.ellipse((x1 + 15, y + 15, x1 + 43, y + 43), fill=_fade(theme, theme["accent2"] if idx == 3 else theme["accent"], reveal))
            _draw_text(draw, bullet, x1 + 70, y, x2 - x1 - 90, fonts["label"], _fade(theme, theme["muted"], reveal), max_lines=1)


def _section_title(
    draw: ImageDraw.ImageDraw,
    scene: ScriptScene,
    box: tuple[int, int, int, int],
    fonts: dict,
    theme: dict,
    progress: float,
) -> None:
    x1, y1, x2, _ = box
    eyebrow = _stage(progress, 0.06, 0.20)
    if eyebrow > 0:
        draw.text((x1, y1 + int(14 * (1 - eyebrow))), _audience_header_label(scene), font=fonts["label"], fill=_fade(theme, theme["accent"], eyebrow))
    title = _stage(progress, 0.20, 0.44)
    if title > 0:
        _draw_text(draw, scene.title, x1, y1 + 74 + int(30 * (1 - title)), x2 - x1, fonts["title"], _fade(theme, theme["foreground"], title), line_gap=14, max_lines=2)
    body = _stage(progress, 0.42, 0.62)
    if body > 0:
        _draw_text(draw, scene.body, x1, y1 + 285 + int(18 * (1 - body)), x2 - x1, fonts["label"], _fade(theme, theme["muted"], body), line_gap=10, max_lines=2)


def _metric_row(
    draw: ImageDraw.ImageDraw,
    metrics: tuple[tuple[str, str], ...],
    x: int,
    y: int,
    width: int,
    fonts: dict,
    theme: dict,
    *,
    progress: float = 1.0,
) -> None:
    gap = 18
    card_w = (width - gap * (len(metrics) - 1)) // max(len(metrics), 1)
    for idx, (label, value) in enumerate(metrics):
        reveal = _stage(progress, idx * 0.15, 0.42 + idx * 0.15)
        if reveal <= 0:
            continue
        left = x + idx * (card_w + gap)
        cy = y + int(16 * (1 - reveal))
        _card(draw, (left, cy, left + card_w, cy + 145), theme, alpha=reveal)
        draw.text((left + 22, cy + 24), value, font=fonts["title"], fill=_fade(theme, theme["accent"], reveal))
        draw.text((left + 22, cy + 96), label.upper(), font=fonts["small"], fill=_fade(theme, theme["muted"], reveal))


def _sparkline(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], theme: dict, offset: int, *, progress: float = 1.0) -> None:
    x1, y1, x2, y2 = box
    points = []
    width = x2 - x1
    height = y2 - y1
    for idx in range(6):
        x = x1 + int(width * idx / 5)
        y = y2 - int(height * ((idx + 1 + offset) % 5 + 1) / 6)
        points.append((x, y))
    visible = max(2, min(len(points), int(1 + (len(points) - 1) * _clamp(progress))))
    visible_points = points[:visible]
    draw.line(visible_points, fill=_fade(theme, theme["accent2"], progress), width=4)
    for point in visible_points:
        draw.ellipse((point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5), fill=_fade(theme, theme["accent2"], progress))


def _card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], theme: dict, *, outline: bool = False, alpha: float = 1.0) -> None:
    fill = _blend(theme["background"], theme["panel"], _clamp(alpha))
    line_base = theme["accent"] if outline else _blend(theme["muted"], theme["background"], 0.22)
    line = _fade(theme, line_base, alpha)
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


def _draw_text_in_box(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    max_width: int,
    max_height: int,
    candidates: list[tuple[ImageFont.ImageFont, int, int]],
    fill: tuple[int, int, int],
    *,
    align: str = "left",
) -> int:
    font, line_gap, lines = _fit_text_block(draw, text, max_width, max_height, candidates)
    for line in lines:
        tx = x
        if align == "center":
            tx = x + max(0, (max_width - _text_width(draw, line, font)) // 2)
        draw.text((tx, y), line, font=font, fill=fill)
        box = draw.textbbox((tx, y), line, font=font)
        y += box[3] - box[1] + line_gap
    return y


def _fit_text_block(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_height: int,
    candidates: list[tuple[ImageFont.ImageFont, int, int]],
) -> tuple[ImageFont.ImageFont, int, list[str]]:
    fallback: tuple[ImageFont.ImageFont, int, list[str]] | None = None
    for font, line_gap, max_lines in candidates:
        lines = _wrap(draw, text, font, max_width)
        visible_lines = _ellipsize_lines(draw, lines, font, max_width, max_lines)
        if fallback is None:
            fallback = (font, line_gap, visible_lines)
        if len(lines) <= max_lines and _text_block_height(draw, visible_lines, font, line_gap) <= max_height:
            return font, line_gap, visible_lines
        if _text_block_height(draw, visible_lines, font, line_gap) <= max_height:
            fallback = (font, line_gap, visible_lines)
    if fallback is None:
        font, line_gap, _ = candidates[-1]
        return font, line_gap, [""]
    return fallback


def _ellipsize_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    font: ImageFont.ImageFont,
    max_width: int,
    max_lines: int,
) -> list[str]:
    if len(lines) <= max_lines:
        return lines
    visible = lines[:max_lines]
    visible[-1] = _with_ellipsis(draw, visible[-1], font, max_width)
    return visible


def _text_block_height(draw: ImageDraw.ImageDraw, lines: list[str], font: ImageFont.ImageFont, line_gap: int) -> int:
    height = 0
    for idx, line in enumerate(lines):
        box = draw.textbbox((0, 0), line, font=font)
        height += box[3] - box[1]
        if idx < len(lines) - 1:
            height += line_gap
    return height


def _with_ellipsis(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    suffix = "..."
    value = text.strip()
    while value and _text_width(draw, value + suffix, font) > max_width:
        value = value[:-1]
    return (value + suffix) if value else suffix


def _fit_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    value = text.strip()
    if _text_width(draw, value, font) <= max_width:
        return value
    suffix = "..."
    while value and _text_width(draw, value + suffix, font) > max_width:
        value = value[:-1]
    return (value + suffix) if value else suffix


def _blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = _clamp(t)
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _fade(theme: dict, color: tuple[int, int, int], alpha: float) -> tuple[int, int, int]:
    return _blend(theme["background"], color, alpha)


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _smoothstep(value: float) -> float:
    t = _clamp(value)
    return t * t * (3 - 2 * t)


def _stage(progress: float, start: float, end: float) -> float:
    if end <= start:
        return 1.0 if progress >= end else 0.0
    t = _clamp((progress - start) / (end - start))
    return 1 - (1 - t) ** 3


def _shift_box(box: tuple[int, int, int, int], y_offset: int) -> tuple[int, int, int, int]:
    return (box[0], box[1] + y_offset, box[2], box[3] + y_offset)


def _motion_frame_count(duration: float, video_config: dict) -> int:
    configured = video_config.get("motion_frames_per_scene")
    if configured:
        return max(4, int(configured))
    return max(12, min(36, int(round(duration * 5))))


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
        chunks = _wrap_unspaced(draw, text, font, max_width)
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


def _wrap_unspaced(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    chunks: list[str] = []
    line = ""
    for char in text:
        trial = line + char
        if line and _text_width(draw, trial, font) > max_width:
            if char.isdigit() and line[-1].isdigit():
                digit_start = len(line)
                while digit_start > 0 and line[digit_start - 1].isdigit():
                    digit_start -= 1
                if digit_start > 0:
                    chunks.append(line[:digit_start])
                    line = line[digit_start:] + char
                    continue
            chunks.append(line)
            line = char
        else:
            line = trial
    if line:
        chunks.append(line)
    return chunks or [text]


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
    generate_demo_bgm = bool(
        music_config.get(
            "generate_demo_bgm_if_missing",
            music_config.get("generate_demo_tone_if_missing", False),
        )
    )

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

    if generate_demo_bgm:
        demo_bgm_path = output_dir / "demo_bgm.wav"
        _write_demo_bgm(demo_bgm_path, duration, volume)
        _run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(demo_bgm_path),
                "-i",
                str(narration_path),
                "-filter_complex",
                "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[a]",
                "-map",
                "[a]",
                "-c:a",
                "aac",
                str(audio_path),
            ]
        )
        return audio_path

    return _silent_audio(audio_path, duration)


def _write_demo_bgm(path: Path, duration: float, volume: float, sample_rate: int = 44100) -> Path:
    duration = max(float(duration), 0.25)
    sample_count = int(math.ceil(duration * sample_rate))
    level = _clamp(max(float(volume), 0.32), 0.10, 0.42)
    chord_len = 2.8
    transition_len = 0.55
    progression = (
        (220.00, 261.63, 329.63, 440.00),
        (174.61, 220.00, 261.63, 349.23),
        (196.00, 246.94, 293.66, 392.00),
        (164.81, 196.00, 246.94, 329.63),
    )
    samples = array("h")

    for index in range(sample_count):
        t = index / sample_rate
        remaining = duration - t
        global_env = _smoothstep(min(1.0, t / 1.0, remaining / 1.2))
        chord_index = int(t / chord_len) % len(progression)
        chord_pos = t % chord_len
        transition = _smoothstep((chord_pos - (chord_len - transition_len)) / transition_len)
        chord = progression[chord_index]
        next_chord = progression[(chord_index + 1) % len(progression)]

        left_current, right_current = _demo_chord_sample(chord, t, chord_index)
        left_next, right_next = _demo_chord_sample(next_chord, t, chord_index + 1)
        left = left_current * (1 - transition) + left_next * transition
        right = right_current * (1 - transition) + right_next * transition

        step_len = 0.35
        step = int(t / step_len)
        step_pos = (t % step_len) / step_len
        arp_note = chord[(step + chord_index) % len(chord)] * 2
        pluck_env = math.exp(-step_pos * 5.4) * _smoothstep(min(1.0, step_pos / 0.08))
        pan = math.sin(2 * math.pi * 0.17 * t)
        pluck = (
            math.sin(2 * math.pi * arp_note * t)
            + 0.35 * math.sin(2 * math.pi * arp_note * 2 * t)
        ) * 0.12 * pluck_env
        shimmer = math.sin(2 * math.pi * chord[-1] * 4 * t) * 0.018 * pluck_env

        left += pluck * (0.85 - 0.12 * pan) + shimmer * 0.7
        right += pluck * (0.85 + 0.12 * pan) + shimmer

        left_value = int(max(-1.0, min(1.0, left * level * global_env)) * 32767)
        right_value = int(max(-1.0, min(1.0, right * level * global_env)) * 32767)
        samples.append(left_value)
        samples.append(right_value)

    if sys.byteorder == "big":
        samples.byteswap()
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(samples.tobytes())
    return path


def _demo_chord_sample(chord: tuple[float, ...], t: float, chord_index: int) -> tuple[float, float]:
    left = 0.0
    right = 0.0
    for note_index, frequency in enumerate(chord):
        phase = note_index * 0.73 + chord_index * 0.29
        slow_mod = 0.76 + 0.24 * math.sin(2 * math.pi * (0.035 + note_index * 0.008) * t + phase)
        tone = (
            math.sin(2 * math.pi * frequency * t + phase) * 0.044
            + math.sin(2 * math.pi * frequency * 2 * t + phase * 0.5) * 0.010
        ) * slow_mod
        pan = -0.22 + note_index * (0.44 / max(len(chord) - 1, 1))
        left += tone * (1 - pan)
        right += tone * (1 + pan)
    root = chord[0] / 2
    bass = math.sin(2 * math.pi * root * t) * 0.075
    return left + bass * 0.95, right + bass * 0.88


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
