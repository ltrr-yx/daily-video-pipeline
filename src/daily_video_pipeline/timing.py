from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import re
from pathlib import Path
from typing import Any

from .models import ScriptScene


TIME_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}:\d{2}[,.]\d{3})"
)


class TimelineAlignmentError(RuntimeError):
    """Raised when subtitles cannot be matched back to scene narration."""


@dataclass(frozen=True)
class SubtitleCue:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class SceneTiming:
    index: int
    title: str
    start: float
    end: float
    duration: float
    source_text: str
    anchor: str


def parse_vtt(path: str | Path) -> list[SubtitleCue]:
    return parse_vtt_text(Path(path).read_text(encoding="utf-8"))


def parse_vtt_text(text: str) -> list[SubtitleCue]:
    lines = text.splitlines()
    cues: list[SubtitleCue] = []
    index = 0
    while index < len(lines):
        match = TIME_RE.search(lines[index].strip())
        if not match:
            index += 1
            continue
        start = parse_timestamp(match.group("start"))
        end = parse_timestamp(match.group("end"))
        index += 1
        text_lines: list[str] = []
        while index < len(lines) and lines[index].strip():
            line = lines[index].strip()
            if not line.startswith(("NOTE", "STYLE", "REGION")):
                text_lines.append(line)
            index += 1
        cue_text = " ".join(text_lines).strip()
        if cue_text:
            cues.append(SubtitleCue(start=start, end=end, text=cue_text))
    if not cues:
        raise TimelineAlignmentError("No WebVTT cues were found.")
    return cues


def parse_timestamp(value: str) -> float:
    hours, minutes, seconds = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def build_subtitle_scene_timeline(
    scenes: list[ScriptScene],
    cues: list[SubtitleCue],
    *,
    media_duration: float | None = None,
    min_anchor_chars: int = 8,
    max_anchor_chars: int = 48,
) -> list[SceneTiming]:
    if not scenes:
        return []
    cue_stream = _CueStream.from_cues(cues)
    if not cue_stream.text:
        raise TimelineAlignmentError("Subtitle cues did not contain usable text.")

    matches: list[tuple[int, int, str]] = []
    search_from = 0
    for scene in scenes:
        scene_text = normalize_timing_text(f"{scene.title} {scene.body}")
        if len(scene_text) < min_anchor_chars:
            raise TimelineAlignmentError(f"Scene narration is too short to align: {scene.title!r}")
        offset, anchor = _find_scene_anchor(
            cue_stream.text,
            scene_text,
            search_from=search_from,
            min_chars=min_anchor_chars,
            max_chars=max_anchor_chars,
        )
        matches.append((offset, offset + len(anchor), anchor))
        search_from = offset + max(len(anchor), 1)

    starts: list[float] = []
    source_texts: list[str] = []
    for index, (offset, _, _) in enumerate(matches):
        cue = cue_stream.cue_at(offset)
        starts.append(0.0 if index == 0 else cue.start)
        source_texts.append(cue.text)

    for index, (earlier, later) in enumerate(zip(starts, starts[1:]), start=1):
        if later <= earlier:
            raise TimelineAlignmentError(
                f"Scene starts are not increasing around scene {index}: {earlier:.3f}, {later:.3f}"
            )

    last_cue_end = max(cue.end for cue in cues)
    composition_end = max(last_cue_end, media_duration or 0.0)
    if starts[-1] >= composition_end:
        raise TimelineAlignmentError(
            f"Last scene starts after the narration ends: {starts[-1]:.3f} >= {composition_end:.3f}"
        )

    timings: list[SceneTiming] = []
    for index, scene in enumerate(scenes):
        start = starts[index]
        end = starts[index + 1] if index + 1 < len(starts) else composition_end
        timings.append(
            SceneTiming(
                index=index,
                title=scene.title,
                start=round_seconds(start),
                end=round_seconds(end),
                duration=round_seconds(end - start),
                source_text=source_texts[index],
                anchor=matches[index][2],
            )
        )
    return timings


def apply_scene_timing(scenes: list[ScriptScene], timings: list[SceneTiming]) -> list[ScriptScene]:
    if len(scenes) != len(timings):
        raise TimelineAlignmentError(
            f"Scene/timing count mismatch: {len(scenes)} scenes, {len(timings)} timing entries."
        )
    return [replace(scene, duration=timing.duration) for scene, timing in zip(scenes, timings)]


def timeline_to_dict(
    timings: list[SceneTiming],
    *,
    subtitle_path: str | None = None,
    audio_path: str | None = None,
    media_duration: float | None = None,
    status: str = "synced",
    reason: str | None = None,
) -> dict[str, Any]:
    composition_duration = timings[-1].end if timings else 0.0
    payload: dict[str, Any] = {
        "status": status,
        "subtitle_path": subtitle_path,
        "audio_path": audio_path,
        "media_duration": round_seconds(media_duration) if media_duration is not None else None,
        "composition_duration": round_seconds(composition_duration),
        "scenes": [asdict(timing) for timing in timings],
    }
    if reason:
        payload["reason"] = reason
    return payload


def normalize_timing_text(value: str) -> str:
    return "".join(char.casefold() for char in value if char.isalnum())


def round_seconds(value: float) -> float:
    return round(value + 1e-9, 3)


def _find_scene_anchor(
    stream: str,
    scene_text: str,
    *,
    search_from: int,
    min_chars: int,
    max_chars: int,
) -> tuple[int, str]:
    upper = min(max_chars, len(scene_text))
    for size in range(upper, min_chars - 1, -4):
        anchor = scene_text[:size]
        offset = stream.find(anchor, search_from)
        if offset >= 0:
            return offset, anchor
    fallback = scene_text[: min(upper, 18)]
    raise TimelineAlignmentError(f"Could not align scene narration from subtitle text: {fallback!r}")


@dataclass(frozen=True)
class _CueSpan:
    start_offset: int
    end_offset: int
    cue: SubtitleCue


@dataclass(frozen=True)
class _CueStream:
    text: str
    spans: tuple[_CueSpan, ...]

    @classmethod
    def from_cues(cls, cues: list[SubtitleCue]) -> "_CueStream":
        parts: list[str] = []
        spans: list[_CueSpan] = []
        offset = 0
        for cue in cues:
            normalized = normalize_timing_text(cue.text)
            if not normalized:
                continue
            parts.append(normalized)
            start = offset
            offset += len(normalized)
            spans.append(_CueSpan(start, offset, cue))
        return cls("".join(parts), tuple(spans))

    def cue_at(self, offset: int) -> SubtitleCue:
        for span in self.spans:
            if span.start_offset <= offset < span.end_offset:
                return span.cue
        if self.spans and offset == self.spans[-1].end_offset:
            return self.spans[-1].cue
        raise TimelineAlignmentError(f"No cue found for subtitle offset {offset}.")
