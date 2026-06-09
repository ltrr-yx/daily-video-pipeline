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
    duration = max(seconds_per_scene * len(scenes), 1.0)

    frame_dir = output_dir / "frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    for index, scene in enumerate(scenes):
        frame_path = frame_dir / f"scene_{index:02d}.png"
        _draw_scene(scene, frame_path, index=index, width=width, height=height, video_config=video_config)
        frame_paths.append(frame_path)

    concat_path = output_dir / "frames.txt"
    _write_concat_file(concat_path, frame_paths, seconds_per_scene)
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
) -> None:
    palette = video_config.get("palette") or {}
    bg = tuple(palette.get("background", [18, 22, 24]))
    fg = tuple(palette.get("foreground", [245, 245, 240]))
    accent = tuple(palette.get("accent", [68, 180, 166]))
    muted = tuple(palette.get("muted", [160, 168, 166]))

    image = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(image)
    font_regular = _font(video_config.get("font_path"), 44)
    font_title = _font(video_config.get("font_path"), 76)
    font_small = _font(video_config.get("font_path"), 34)

    margin = int(width * 0.08)
    draw.rectangle((0, 0, width, 18), fill=accent)
    draw.text((margin, 120), scene.kicker.upper(), font=font_small, fill=accent)

    y = 210
    for line in _wrap(draw, scene.title, font_title, width - margin * 2):
        draw.text((margin, y), line, font=font_title, fill=fg)
        y += 92

    y += 50
    for line in _wrap(draw, scene.body, font_regular, width - margin * 2):
        draw.text((margin, y), line, font=font_regular, fill=fg)
        y += 60

    bottom = height - 210
    draw.line((margin, bottom, width - margin, bottom), fill=muted, width=2)
    draw.text((margin, bottom + 42), scene.source_label, font=font_small, fill=muted)
    draw.text((margin, height - 90), f"{index + 1:02d}", font=font_small, fill=accent)
    image.save(path)


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


def _write_concat_file(path: Path, frames: list[Path], seconds_per_scene: float) -> None:
    lines: list[str] = []
    for frame in frames:
        lines.append(f"file '{frame.resolve().as_posix()}'")
        lines.append(f"duration {seconds_per_scene}")
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
