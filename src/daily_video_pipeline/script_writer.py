from __future__ import annotations

import re
import textwrap

from .models import NewsItem, ScriptScene
from .templates import get_component, get_story_template, resolve_motion_key


def build_scenes(
    items: list[NewsItem],
    *,
    project_name: str,
    run_date: str,
    story_config: dict | None = None,
) -> list[ScriptScene]:
    story_config = story_config or {}
    template = get_story_template(str(story_config.get("template", "daily_briefing")))
    seconds_per_scene = float(story_config.get("seconds_per_scene", 5.0))
    global_motion = str(story_config.get("motion") or story_config.get("motion_grammar") or "auto")
    motion_overrides = story_config.get("motion_overrides") or {}
    scenes: list[ScriptScene] = []

    for index, component_key in enumerate(template.components):
        item = items[min(index, len(items) - 1)]
        component = get_component(component_key)
        override_motion = motion_overrides.get(component_key) or motion_overrides.get(component.family)
        motion_grammar = resolve_motion_key(str(override_motion or global_motion), component.family)
        scenes.append(
            _scene_for_component(
                component_key,
                item=item,
                items=items,
                index=index,
                project_name=project_name,
                run_date=run_date,
                template_name=template.name,
                visual_grammar=component.visual_grammar,
                motion_grammar=motion_grammar,
                duration=seconds_per_scene,
            )
        )
    return scenes


def build_markdown(items: list[NewsItem], scenes: list[ScriptScene], *, run_date: str) -> str:
    lines = [f"# Daily Video Script - {run_date}", ""]
    lines.append("## Voiceover")
    lines.append("")
    for scene in scenes:
        lines.append(f"- {scene.title}. {scene.body}")
        if scene.proof:
            lines.append(f"  Proof: {scene.proof}")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    for item in items:
        lines.append(f"- [{item.title}]({item.url}) - {item.source_name}")
    lines.append("")
    return "\n".join(lines)


def narration_text(scenes: list[ScriptScene]) -> str:
    return " ".join(f"{scene.title}. {scene.body}" for scene in scenes)


def _scene_for_component(
    component: str,
    *,
    item: NewsItem,
    items: list[NewsItem],
    index: int,
    project_name: str,
    run_date: str,
    template_name: str,
    visual_grammar: str,
    motion_grammar: str,
    duration: float,
) -> ScriptScene:
    titles = tuple(_short_title(entry.title, 58) for entry in items[:5])
    source_label = f"{item.source_name} · {item.published_at.date().isoformat()}"
    proof = _summary_or_fallback(item)
    metrics = _metrics_for_item(item, items)

    if component in {"cover_hook", "impact_headline"}:
        return ScriptScene(
            title=_short_title(item.title if items else project_name, 68),
            kicker=template_name,
            eyebrow=run_date,
            body=_impact_line(item),
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=titles[:3],
            tags=item.tags,
            duration=duration,
        )

    if component in {"signal_grid", "three_takeaways", "use_case_grid"}:
        return ScriptScene(
            title="Key signals",
            kicker=f"Signals · {len(items)} sources",
            eyebrow=project_name,
            body="The strongest signals are grouped so the direction is easier to compare.",
            source_label="market source digest",
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=titles[:5],
            tags=item.tags,
            duration=duration,
        )

    if component in {"source_proof", "evidence_quote", "proof_chips"}:
        return ScriptScene(
            title=_short_title(item.title, 64),
            kicker="Source proof",
            eyebrow=item.source_name,
            body=proof,
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=(item.source_name, item.published_at.date().isoformat(), *(item.tags[:2] or ("source",))),
            tags=item.tags,
            duration=duration,
        )

    if component in {"metric_stack", "big_number", "mini_chart", "pulse_monitor"}:
        return ScriptScene(
            title="What moved",
            kicker="Metrics",
            eyebrow=_short_title(item.title, 42),
            body="The key numbers show what changed, how broad the move is, and where pressure is concentrated.",
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=titles[:3],
            tags=item.tags,
            duration=duration,
        )

    if component in {"timeline_ribbon", "milestone_stack", "week_calendar"}:
        return ScriptScene(
            title="Sequence to watch",
            kicker="Timeline",
            eyebrow=run_date,
            body="The sequence is signal first, proof point second, and the next check last.",
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=titles[:4],
            tags=item.tags,
            duration=duration,
        )

    if component in {"compare_split", "before_after_surface"}:
        return ScriptScene(
            title="Before versus after",
            kicker="Comparison",
            eyebrow=_short_title(item.title, 42),
            body=proof,
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=_split_bullets(items),
            tags=item.tags,
            duration=duration,
        )

    if component in {"mechanism_xray", "stack_layers", "funnel"}:
        return ScriptScene(
            title="Mechanism",
            kicker="Cause → effect",
            eyebrow=_short_title(item.title, 42),
            body="Input, mechanism, and consequence are separated so the viewer can see the logic instead of only the headline.",
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=("Input signal", "Mechanism", "Consequence"),
            tags=item.tags,
            duration=duration,
        )

    if component in {"market_ledger", "data_table", "ranking_board"}:
        return ScriptScene(
            title="Ranked evidence",
            kicker="Ledger",
            eyebrow=project_name,
            body="Ranked signals show what mattered most in this recap.",
            source_label="market source digest",
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=titles[:5],
            tags=item.tags,
            duration=duration,
        )

    if component in {"risk_matrix", "watchlist", "next_watch"}:
        return ScriptScene(
            title="Next checks",
            kicker="Watch",
            eyebrow=_short_title(item.title, 42),
            body="The practical watch list is what changed, what could contradict it, and what to check next.",
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=("What changed", "What supports it", "What could break", "Next source check"),
            tags=item.tags,
            duration=duration,
        )

    if component in {"product_plate", "entity_map", "geographic_map", "context_panel"}:
        return ScriptScene(
            title=_short_title(item.title, 64),
            kicker="Context",
            eyebrow=item.source_name,
            body=proof,
            source_label=source_label,
            component=component,
            visual_grammar=visual_grammar,
            motion_grammar=motion_grammar,
            proof=proof,
            source_url=item.url,
            metrics=metrics,
            bullets=titles[:3],
            tags=item.tags,
            duration=duration,
        )

    return ScriptScene(
        title="Practical takeaways",
        kicker="Conclusion",
        eyebrow=project_name,
        body=_impact_line(item),
        source_label=source_label,
        component=component,
        visual_grammar=visual_grammar,
        motion_grammar=motion_grammar,
        proof=proof,
        source_url=item.url,
        metrics=metrics,
        bullets=titles[:3],
        tags=item.tags,
        duration=duration,
    )


def _summary_or_fallback(item: NewsItem) -> str:
    summary = item.summary.strip()
    if not summary:
        return "A fresh item from this source. Open the original link before publishing final commentary."
    return textwrap.shorten(summary, width=220, placeholder="...")


def _impact_line(item: NewsItem) -> str:
    summary = _summary_or_fallback(item)
    return textwrap.shorten(summary, width=150, placeholder="...")


def _short_title(value: str, width: int) -> str:
    return textwrap.shorten(value.strip() or "Untitled signal", width=width, placeholder="...")


def _metrics_for_item(item: NewsItem, items: list[NewsItem]) -> tuple[tuple[str, str], ...]:
    text = f"{item.title} {item.summary}"
    numbers = _extract_metric_values(text)
    metrics: list[tuple[str, str]] = []
    for number in numbers[:2]:
        metrics.append(("mentioned", number))
    metrics.append(("score", f"{item.score:.1f}"))
    metrics.append(("sources", str(len(items))))
    return tuple(metrics[:4])


def _split_bullets(items: list[NewsItem]) -> tuple[str, ...]:
    left = _short_title(items[0].title, 48) if items else "Before"
    right = _short_title(items[1].title, 48) if len(items) > 1 else "After"
    return (left, right)


def _extract_metric_values(text: str) -> list[str]:
    values: list[str] = []
    for pattern in (
        r"[-+]?\d+(?:\.\d+)?%",
        r"[-+]?\d+(?:\.\d+)?(?:万亿|亿元|点|家)",
        r"[$¥]\d+(?:\.\d+)?[MBK]?",
    ):
        for value in re.findall(pattern, text):
            if value not in values:
                values.append(value)
    if values:
        return values
    return re.findall(r"(?<![A-Za-z0-9_.])[-+]?\d+(?:\.\d+)?(?![A-Za-z0-9_])", text)
