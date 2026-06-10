from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StoryTemplate:
    key: str
    name: str
    description: str
    components: tuple[str, ...]


@dataclass(frozen=True)
class SceneComponent:
    key: str
    name: str
    family: str
    visual_grammar: str
    purpose: str


@dataclass(frozen=True)
class MotionGrammar:
    key: str
    name: str
    description: str
    default_families: tuple[str, ...]
    entrance: str
    emphasis: str
    exit: str


STORY_TEMPLATES: dict[str, StoryTemplate] = {
    "daily_briefing": StoryTemplate(
        "daily_briefing",
        "Daily Briefing",
        "Three to five signals with a fast editorial open and a watch-next close.",
        ("cover_hook", "signal_grid", "source_proof", "insight_stack", "next_watch"),
    ),
    "single_event_deep_dive": StoryTemplate(
        "single_event_deep_dive",
        "Single Event Deep Dive",
        "One story explained through context, mechanism, evidence, and consequence.",
        ("cover_hook", "context_panel", "mechanism_xray", "evidence_quote", "conclusion_stamp"),
    ),
    "breaking_update": StoryTemplate(
        "breaking_update",
        "Breaking Update",
        "Short urgent update with immediate fact, source proof, and next check.",
        ("impact_headline", "source_proof", "proof_chips", "next_watch"),
    ),
    "product_launch": StoryTemplate(
        "product_launch",
        "Product Launch",
        "What shipped, who it helps, proof, and why the workflow changes.",
        ("product_plate", "before_after_surface", "use_case_grid", "verification_rail", "cta_end"),
    ),
    "company_update": StoryTemplate(
        "company_update",
        "Company Update",
        "Entity-led update with action, evidence, impact, and watch signal.",
        ("entity_map", "source_proof", "metric_stack", "risk_matrix", "next_watch"),
    ),
    "market_radar": StoryTemplate(
        "market_radar",
        "Market Radar",
        "Multiple indicators arranged as a calm market board.",
        ("market_ledger", "pulse_monitor", "signal_grid", "risk_matrix", "conclusion_stamp"),
    ),
    "evidence_chain": StoryTemplate(
        "evidence_chain",
        "Evidence Chain",
        "Source to claim to validation with proof stops.",
        ("verification_rail", "source_proof", "evidence_quote", "mechanism_xray", "conclusion_stamp"),
    ),
    "comparison": StoryTemplate(
        "comparison",
        "Comparison",
        "Two approaches, products, companies, or signals compared side by side.",
        ("compare_split", "metric_stack", "before_after_surface", "conclusion_stamp"),
    ),
    "timeline": StoryTemplate(
        "timeline",
        "Timeline",
        "Sequence of milestones and what changes at the end.",
        ("timeline_ribbon", "milestone_stack", "source_proof", "next_watch"),
    ),
    "risk_watch": StoryTemplate(
        "risk_watch",
        "Risk Watch",
        "Opportunity, uncertainty, contradiction, and next validation.",
        ("risk_matrix", "verification_rail", "proof_chips", "next_watch"),
    ),
    "top_five": StoryTemplate(
        "top_five",
        "Top Five",
        "Ranked countdown for daily or weekly lists.",
        ("ranking_board", "source_proof", "metric_stack", "cta_end"),
    ),
    "weekly_review": StoryTemplate(
        "weekly_review",
        "Weekly Review",
        "Week-level synthesis across themes, changes, and next week signals.",
        ("week_calendar", "signal_grid", "market_ledger", "conclusion_stamp", "next_watch"),
    ),
}


SCENE_COMPONENTS: dict[str, SceneComponent] = {
    "cover_hook": SceneComponent("cover_hook", "Cover Hook", "cover", "cinematic_anchor", "Open with one strong claim."),
    "impact_headline": SceneComponent("impact_headline", "Impact Headline", "cover", "cinematic_anchor", "Make the immediate change obvious."),
    "signal_grid": SceneComponent("signal_grid", "Signal Grid", "grid", "signal_board", "Group several weak signals."),
    "source_proof": SceneComponent("source_proof", "Source Proof", "proof", "verification_rail", "Show the originating source and evidence line."),
    "evidence_quote": SceneComponent("evidence_quote", "Evidence Quote", "proof", "verification_rail", "Pull one source-backed proof sentence."),
    "proof_chips": SceneComponent("proof_chips", "Proof Chips", "chips", "verification_rail", "Compress source, date, and tag proof."),
    "metric_stack": SceneComponent("metric_stack", "Metric Stack", "metric", "market_ledger", "Stack numbers and short labels."),
    "big_number": SceneComponent("big_number", "Big Number", "metric", "data_on_plate", "Feature one number or count."),
    "mini_chart": SceneComponent("mini_chart", "Mini Chart", "metric", "data_on_plate", "Show a compact trend-like shape."),
    "market_ledger": SceneComponent("market_ledger", "Market Ledger", "ledger", "market_ledger", "Present rows of indicators."),
    "data_table": SceneComponent("data_table", "Data Table", "ledger", "market_ledger", "Use dense but readable rows."),
    "timeline_ribbon": SceneComponent("timeline_ribbon", "Timeline Ribbon", "timeline", "timeline_ribbon", "Show milestones along a rail."),
    "milestone_stack": SceneComponent("milestone_stack", "Milestone Stack", "timeline", "timeline_ribbon", "Stack phase cards vertically."),
    "week_calendar": SceneComponent("week_calendar", "Week Calendar", "timeline", "timeline_ribbon", "Summarize week-level signals."),
    "compare_split": SceneComponent("compare_split", "Compare Split", "split", "before_after_surface", "Compare two sides."),
    "before_after_surface": SceneComponent("before_after_surface", "Before After", "split", "before_after_surface", "Show old state versus new state."),
    "context_panel": SceneComponent("context_panel", "Context Panel", "context", "runtime_lens", "Set up the story frame."),
    "mechanism_xray": SceneComponent("mechanism_xray", "Mechanism X-Ray", "mechanism", "mechanism_xray", "Reveal cause and effect layers."),
    "stack_layers": SceneComponent("stack_layers", "Stack Layers", "mechanism", "mechanism_xray", "Layer inputs, mechanism, and outcome."),
    "funnel": SceneComponent("funnel", "Funnel", "mechanism", "mechanism_xray", "Narrow inputs into one outcome."),
    "verification_rail": SceneComponent("verification_rail", "Verification Rail", "rail", "verification_rail", "Move through evidence stops."),
    "entity_map": SceneComponent("entity_map", "Entity Map", "map", "runtime_lens", "Show who is connected to the story."),
    "geographic_map": SceneComponent("geographic_map", "Geographic Map", "map", "runtime_lens", "Place the story geographically or regionally."),
    "product_plate": SceneComponent("product_plate", "Product Plate", "product", "official_product_plate", "Give a launch or object a premium slot."),
    "use_case_grid": SceneComponent("use_case_grid", "Use Case Grid", "grid", "official_product_plate", "Show practical usage lanes."),
    "three_takeaways": SceneComponent("three_takeaways", "Three Takeaways", "grid", "signal_board", "Summarize into three useful points."),
    "risk_matrix": SceneComponent("risk_matrix", "Risk Matrix", "matrix", "verification_rail", "Separate upside, downside, unknowns, and checks."),
    "watchlist": SceneComponent("watchlist", "Watchlist", "list", "signal_board", "List what to watch next."),
    "next_watch": SceneComponent("next_watch", "Next Watch", "list", "signal_board", "End with concrete next checks."),
    "ranking_board": SceneComponent("ranking_board", "Ranking Board", "ranking", "market_ledger", "Rank selected items."),
    "pulse_monitor": SceneComponent("pulse_monitor", "Pulse Monitor", "metric", "data_on_plate", "Show a heartbeat-like signal state."),
    "conclusion_stamp": SceneComponent("conclusion_stamp", "Conclusion Stamp", "stamp", "market_ledger", "Land the verdict cleanly."),
    "cta_end": SceneComponent("cta_end", "CTA End", "stamp", "cinematic_anchor", "Close with one action or review prompt."),
    "insight_stack": SceneComponent("insight_stack", "Insight Stack", "context", "signal_board", "Stack compact insight cards."),
}


MOTION_GRAMMARS: dict[str, MotionGrammar] = {
    "soft_assembly": MotionGrammar(
        "soft_assembly",
        "Soft Assembly",
        "A calm commercial default: shell first, title second, cards or proof details stagger into a readable hold.",
        ("cover", "context", "grid"),
        "soft fade with a small upward settle",
        "staggered content assembly",
        "short fade-through",
    ),
    "evidence_trace": MotionGrammar(
        "evidence_trace",
        "Evidence Trace",
        "Proof-oriented motion: draw the rail or path first, then reveal stops, labels, and evidence cards in sequence.",
        ("proof", "chips", "rail", "timeline"),
        "rail draw-on before nodes",
        "node and card stagger",
        "source line holds before fade-through",
    ),
    "product_reveal": MotionGrammar(
        "product_reveal",
        "Product Reveal",
        "A product or object gets a premium reveal with a soft plate entrance, light camera push, and restrained callouts.",
        ("product", "map"),
        "matte-like plate reveal with gentle scale",
        "callout pins after the anchor is visible",
        "slow push into the final product read",
    ),
    "data_tween": MotionGrammar(
        "data_tween",
        "Data Tween",
        "Numbers, rows, and tiny charts animate as evidence changes rather than appearing as static slides.",
        ("metric", "ledger", "ranking"),
        "metric rows stagger in",
        "value and sparkline fill",
        "final values hold long enough to read",
    ),
    "mechanism_scan": MotionGrammar(
        "mechanism_scan",
        "Mechanism Scan",
        "Layered explanations reveal structure before claims, then use a scan or connector pass to show causality.",
        ("mechanism", "split", "matrix"),
        "layer peel or split reveal",
        "focus rail, divider, or scan pass",
        "consequence layer settles last",
    ),
    "verdict_lock": MotionGrammar(
        "verdict_lock",
        "Verdict Lock",
        "Conclusion motion compresses supporting details into a final practical watch item or verdict.",
        ("list", "stamp"),
        "verdict plate enters after the setup",
        "supporting checks stagger below",
        "final stamp hold",
    ),
}


MOTION_DEFAULTS_BY_FAMILY: dict[str, str] = {
    family: grammar.key
    for grammar in MOTION_GRAMMARS.values()
    for family in grammar.default_families
}


VISUAL_THEMES: dict[str, dict[str, Any]] = {
    "editorial_dark": {
        "name": "Editorial Dark",
        "background": (13, 18, 20),
        "panel": (24, 31, 34),
        "panel_alt": (34, 42, 45),
        "foreground": (244, 242, 235),
        "muted": (160, 168, 166),
        "accent": (70, 188, 172),
        "accent2": (230, 184, 91),
        "danger": (219, 101, 83),
        "style": {
            "font_zh": "Noto Serif SC / Source Han Serif SC",
            "font_en": "Newsreader / Georgia",
            "font_stack": "Noto Serif SC, Source Han Serif SC, Newsreader, Georgia, serif",
            "type_scale": "Headline 76 / Body 40 / Label 24",
            "headline_size": 76,
            "body_size": 40,
            "label_size": 24,
            "text_ratio": 64,
            "media_ratio": 36,
            "ornament": "Thin cyan tabs with amber proof ticks.",
            "underline": "One short accent underline below the key claim.",
        },
    },
    "executive_light": {
        "name": "Executive Light",
        "background": (246, 241, 231),
        "panel": (255, 251, 242),
        "panel_alt": (235, 228, 215),
        "foreground": (13, 25, 38),
        "muted": (87, 99, 111),
        "accent": (25, 103, 210),
        "accent2": (176, 122, 50),
        "danger": (184, 75, 63),
        "style": {
            "font_zh": "Noto Sans SC / Source Han Sans SC",
            "font_en": "Inter / SF Pro",
            "font_stack": "Inter, Noto Sans SC, Source Han Sans SC, system-ui, sans-serif",
            "type_scale": "Headline 68 / Body 38 / Label 24",
            "headline_size": 68,
            "body_size": 38,
            "label_size": 24,
            "text_ratio": 56,
            "media_ratio": 44,
            "ornament": "Quiet blue chips with restrained gold checks.",
            "underline": "Fine blue rule under the conclusion line only.",
        },
    },
    "market_terminal": {
        "name": "Market Terminal",
        "background": (5, 13, 18),
        "panel": (11, 28, 35),
        "panel_alt": (18, 44, 52),
        "foreground": (231, 247, 238),
        "muted": (124, 154, 146),
        "accent": (23, 214, 132),
        "accent2": (236, 198, 83),
        "danger": (234, 82, 82),
        "style": {
            "font_zh": "Noto Sans Mono CJK SC / Sarasa Gothic SC",
            "font_en": "IBM Plex Mono / SF Mono",
            "font_stack": "IBM Plex Mono, SFMono-Regular, Noto Sans Mono CJK SC, monospace",
            "type_scale": "Headline 60 / Body 34 / Label 22",
            "headline_size": 60,
            "body_size": 34,
            "label_size": 22,
            "text_ratio": 48,
            "media_ratio": 52,
            "ornament": "Terminal brackets, status dots, and tight data rails.",
            "underline": "Green metric rail under the changing value.",
        },
    },
    "product_keynote": {
        "name": "Product Keynote",
        "background": (244, 246, 248),
        "panel": (255, 255, 255),
        "panel_alt": (232, 238, 245),
        "foreground": (8, 16, 26),
        "muted": (92, 105, 120),
        "accent": (55, 105, 246),
        "accent2": (116, 84, 240),
        "danger": (204, 73, 73),
        "style": {
            "font_zh": "Noto Sans SC / HarmonyOS Sans SC",
            "font_en": "Inter / Helvetica",
            "font_stack": "Inter, Helvetica Neue, Noto Sans SC, HarmonyOS Sans SC, sans-serif",
            "type_scale": "Headline 82 / Body 40 / Label 24",
            "headline_size": 82,
            "body_size": 40,
            "label_size": 24,
            "text_ratio": 42,
            "media_ratio": 58,
            "ornament": "Blue stage tabs with small floating proof dots.",
            "underline": "Thicker short underline beneath the feature name.",
        },
    },
    "data_magazine": {
        "name": "Data Magazine",
        "background": (252, 248, 238),
        "panel": (241, 234, 218),
        "panel_alt": (222, 212, 195),
        "foreground": (31, 30, 27),
        "muted": (97, 91, 82),
        "accent": (18, 92, 129),
        "accent2": (196, 95, 43),
        "danger": (168, 61, 58),
        "style": {
            "font_zh": "Noto Serif SC / Source Han Serif SC",
            "font_en": "IBM Plex Serif / Georgia",
            "font_stack": "IBM Plex Serif, Noto Serif SC, Source Han Serif SC, Georgia, serif",
            "type_scale": "Headline 72 / Body 38 / Label 23",
            "headline_size": 72,
            "body_size": 38,
            "label_size": 23,
            "text_ratio": 58,
            "media_ratio": 42,
            "ornament": "Editorial folios, warm chips, and chart captions.",
            "underline": "Ochre underline for one evidence phrase.",
        },
    },
    "social_pop": {
        "name": "Social Pop",
        "background": (18, 17, 26),
        "panel": (35, 31, 52),
        "panel_alt": (50, 43, 74),
        "foreground": (255, 249, 238),
        "muted": (189, 180, 204),
        "accent": (255, 198, 41),
        "accent2": (38, 205, 255),
        "danger": (255, 95, 123),
        "style": {
            "font_zh": "Noto Sans SC Black / Source Han Sans Heavy",
            "font_en": "Space Grotesk / Arial Black",
            "font_stack": "Space Grotesk, Noto Sans SC, Source Han Sans SC, Arial Black, sans-serif",
            "type_scale": "Headline 84 / Body 42 / Label 26",
            "headline_size": 84,
            "body_size": 42,
            "label_size": 26,
            "text_ratio": 50,
            "media_ratio": 50,
            "ornament": "Bright sticker chips and punchy number tags.",
            "underline": "Highlighter underline below the emotional hook.",
        },
    },
}


def get_story_template(key: str | None) -> StoryTemplate:
    if not key or key == "auto":
        return STORY_TEMPLATES["daily_briefing"]
    return STORY_TEMPLATES.get(key, STORY_TEMPLATES["daily_briefing"])


def get_component(key: str) -> SceneComponent:
    return SCENE_COMPONENTS.get(key, SCENE_COMPONENTS["insight_stack"])


def get_motion_grammar(key: str | None) -> MotionGrammar:
    if not key or key == "auto":
        return MOTION_GRAMMARS["soft_assembly"]
    return MOTION_GRAMMARS.get(key, MOTION_GRAMMARS["soft_assembly"])


def resolve_motion_key(key: str | None, family: str) -> str:
    if key and key != "auto":
        return key if key in MOTION_GRAMMARS else "soft_assembly"
    return MOTION_DEFAULTS_BY_FAMILY.get(family, "soft_assembly")


def get_theme(key: str | None) -> dict[str, Any]:
    return dict(VISUAL_THEMES.get(key or "editorial_dark", VISUAL_THEMES["editorial_dark"]))
