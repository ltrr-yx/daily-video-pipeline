from __future__ import annotations

from html import escape
from pathlib import Path

from .templates import SCENE_COMPONENTS, STORY_TEMPLATES, VISUAL_THEMES, SceneComponent, StoryTemplate


STORY_EXAMPLES = {
    "daily_briefing": "Example: three morning AI or market signals, one proof point, one watch-next close.",
    "single_event_deep_dive": "Example: one launch, policy change, earnings note, or research result explained end to end.",
    "breaking_update": "Example: a fresh source-backed update that needs a short fact, proof, and next check.",
    "product_launch": "Example: a new product or feature, who it helps, and what workflow changed.",
    "company_update": "Example: a company action, source evidence, impact metrics, risks, and next signal.",
    "market_radar": "Example: a public market breadth recap with sector strength, risks, and a clean verdict.",
    "evidence_chain": "Example: source to claim to validation, with proof stops and a final confidence read.",
    "comparison": "Example: two tools, companies, assets, or signals compared side by side.",
    "timeline": "Example: a release sequence, policy timeline, or research-to-product milestone chain.",
    "risk_watch": "Example: opportunity, contradiction, uncertainty, and the next validation checkpoint.",
    "top_five": "Example: a ranked daily or weekly list with proof and a compact close.",
    "weekly_review": "Example: a week-level synthesis across themes, changes, and next-week signals.",
}

THEME_USAGE = {
    "editorial_dark": "Use for serious news, research notes, and night-editorial recaps.",
    "executive_light": "Use for boardroom explainers, weekly reviews, and clean business summaries.",
    "market_terminal": "Use for finance, KPI recaps, market breadth, and dense numeric hierarchy.",
    "product_keynote": "Use for product launches, workflow demos, and verified object-led stories.",
    "data_magazine": "Use for analytical features, chart-led explainers, and slower editorial pacing.",
    "social_pop": "Use for countdowns, lighter recaps, and high-energy social packages.",
}

FAMILY_ORDER = (
    "cover",
    "context",
    "grid",
    "metric",
    "ledger",
    "proof",
    "chips",
    "rail",
    "timeline",
    "mechanism",
    "split",
    "matrix",
    "ranking",
    "list",
    "map",
    "product",
    "stamp",
)

FAMILY_LABELS = {
    "cover": "Opening and impact",
    "context": "Context and insight",
    "grid": "Signal groups",
    "metric": "Numbers and charts",
    "ledger": "Ledgers and tables",
    "proof": "Source proof",
    "chips": "Proof chips",
    "rail": "Validation rails",
    "timeline": "Timelines",
    "mechanism": "Mechanisms",
    "split": "Comparisons",
    "matrix": "Risk matrices",
    "ranking": "Rankings",
    "list": "Watch lists",
    "map": "Entity maps",
    "product": "Product plates",
    "stamp": "Conclusions",
}


def write_gallery(output_dir: str | Path = "docs") -> tuple[Path, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    html_path = out / "gallery.html"
    md_path = out / "gallery.md"
    html_path.write_text(build_gallery_html(), encoding="utf-8")
    md_path.write_text(build_gallery_markdown(), encoding="utf-8")
    return html_path, md_path


def build_gallery_markdown() -> str:
    lines = [
        "# Template Gallery",
        "",
        "Open [`docs/gallery.html`](gallery.html) for the visual gallery.",
        "",
        "The gallery explains the three-layer video direction system:",
        "",
        "- Story templates define narrative order.",
        "- Scene components define the visual language of each screen.",
        "- Visual themes define the commercial skin.",
        "",
        "## Story Templates",
        "",
    ]
    for template in STORY_TEMPLATES.values():
        flow = " -> ".join(template.components)
        lines.extend(
            [
                f"### {template.name}",
                "",
                template.description,
                "",
                f"- Key: `{template.key}`",
                f"- Flow: `{flow}`",
                f"- Sample use: {STORY_EXAMPLES.get(template.key, 'A source-backed short video package.')}",
                "",
            ]
        )

    lines.extend(["## Scene Components", ""])
    for family in FAMILY_ORDER:
        items = [component for component in SCENE_COMPONENTS.values() if component.family == family]
        if not items:
            continue
        lines.extend([f"### {FAMILY_LABELS.get(family, family.title())}", ""])
        for component in items:
            lines.append(
                f"- `{component.key}` - {component.name}: {component.purpose} "
                f"Visual grammar: `{component.visual_grammar}`."
            )
        lines.append("")

    lines.extend(["## Visual Themes", ""])
    for key, theme in VISUAL_THEMES.items():
        lines.append(f"- `{key}` - {theme['name']}: {THEME_USAGE.get(key, 'A reusable commercial skin.')}")
    lines.append("")
    return "\n".join(lines)


def build_gallery_html() -> str:
    story_cards = "\n".join(_story_card(template) for template in STORY_TEMPLATES.values())
    component_sections = "\n".join(_component_family_section(family) for family in FAMILY_ORDER)
    theme_cards = "\n".join(_theme_card(key, theme) for key, theme in VISUAL_THEMES.items())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daily Video Pipeline - Template Gallery</title>
  <style>
    :root {{
      --paper: #eef2f3;
      --ink: #121417;
      --muted: #687077;
      --line: #d6dde1;
      --panel: #ffffff;
      --dark: #0a1114;
      --green: #17d684;
      --blue: #1d63d8;
      --gold: #c88a2d;
      --red: #c85045;
      --radius: 8px;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(180deg, #f8faf9 0%, var(--paper) 54%, #e4eaed 100%);
    }}
    .shell {{ max-width: 1180px; margin: 0 auto; padding: 40px 24px 72px; }}
    header {{
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(280px, .85fr);
      gap: 28px;
      align-items: stretch;
      margin-bottom: 34px;
    }}
    .hero {{
      min-height: 360px;
      padding: 34px;
      border-radius: var(--radius);
      color: #eef8f2;
      background: #071014;
      border: 1px solid #1a3638;
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: auto 34px 32px 34px;
      height: 3px;
      background: linear-gradient(90deg, var(--green), var(--gold), var(--blue));
    }}
    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: #9ad9bd;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .eyebrow::before {{ content: ""; width: 28px; height: 2px; background: var(--green); }}
    h1 {{ margin: 28px 0 18px; font-size: clamp(42px, 6vw, 76px); line-height: .93; letter-spacing: 0; }}
    .hero p {{ max-width: 660px; margin: 0; color: #c4d4ce; font-size: 18px; line-height: 1.55; }}
    .hero-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 34px;
      max-width: 640px;
    }}
    .hero-chip {{
      padding: 12px;
      border: 1px solid #21434a;
      background: #0d2026;
      border-radius: var(--radius);
      min-height: 76px;
    }}
    .hero-chip strong {{ display: block; color: #f2f6ee; font-size: 24px; }}
    .hero-chip span {{ display: block; color: #86a39c; margin-top: 4px; font-size: 12px; }}
    .guide {{
      padding: 24px;
      border-radius: var(--radius);
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: 0 16px 44px rgba(20, 20, 20, .08);
    }}
    .guide h2 {{ margin: 0 0 18px; font-size: 22px; }}
    .layer-row {{
      display: grid;
      grid-template-columns: 36px 1fr;
      gap: 14px;
      padding: 16px 0;
      border-top: 1px solid var(--line);
    }}
    .layer-row:first-of-type {{ border-top: 0; padding-top: 0; }}
    .layer-no {{
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: #06120f;
      font-weight: 900;
      background: var(--green);
    }}
    .layer-row h3 {{ margin: 0 0 5px; font-size: 16px; }}
    .layer-row p {{ margin: 0; color: var(--muted); line-height: 1.45; }}
    nav {{
      position: sticky;
      top: 0;
      z-index: 4;
      margin: 0 -24px 38px;
      padding: 12px 24px;
      backdrop-filter: blur(16px);
      background: rgba(238, 242, 243, .88);
      border-bottom: 1px solid rgba(216, 208, 194, .8);
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    nav a {{
      color: var(--ink);
      text-decoration: none;
      border: 1px solid var(--line);
      background: rgba(255, 250, 241, .78);
      padding: 9px 12px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
    }}
    section {{ margin-top: 56px; }}
    .section-head {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: end;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 16px;
    }}
    .section-head h2 {{ margin: 0; font-size: clamp(28px, 4vw, 44px); letter-spacing: 0; }}
    .section-head p {{ margin: 0; max-width: 520px; color: var(--muted); line-height: 1.5; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    .story-card, .component-card, .theme-card {{
      background: rgba(255, 250, 241, .88);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: 0 10px 28px rgba(20, 20, 20, .055);
    }}
    .story-card {{ display: flex; flex-direction: column; min-height: 392px; }}
    .card-body {{ padding: 18px; }}
    .meta {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: .07em;
      text-transform: uppercase;
    }}
    h3 {{ margin: 10px 0 8px; font-size: 22px; line-height: 1.12; }}
    .story-card p, .component-card p, .theme-card p {{ margin: 0; color: var(--muted); line-height: 1.48; }}
    .sample {{
      margin-top: 14px;
      padding: 12px;
      border-left: 3px solid var(--gold);
      background: #eef7f2;
      color: #263f36;
      font-size: 13px;
      line-height: 1.45;
    }}
    .svg-wrap {{
      background: #071014;
      border-bottom: 1px solid #203134;
    }}
    svg {{ width: 100%; height: auto; display: block; }}
    .component-family {{ margin-top: 28px; }}
    .component-family h3 {{
      margin: 0 0 12px;
      padding-left: 12px;
      border-left: 4px solid var(--green);
      font-size: 22px;
    }}
    .component-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }}
    .component-card h4, .theme-card h4 {{ margin: 10px 0 6px; font-size: 18px; }}
    .component-card .card-body, .theme-card .card-body {{ padding: 15px; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      max-width: 100%;
      padding: 5px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: #424950;
      background: #f4f8f7;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .05em;
      white-space: nowrap;
    }}
    .theme-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    .swatches {{ display: flex; gap: 7px; margin-top: 14px; }}
    .swatch {{ width: 24px; height: 24px; border-radius: 50%; border: 1px solid rgba(0,0,0,.18); }}
    code {{
      display: inline-block;
      max-width: 100%;
      color: #12342c;
      background: #e6f2eb;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
    }}
    .note {{
      margin-top: 24px;
      padding: 18px;
      border: 1px solid #b8c9df;
      border-radius: var(--radius);
      background: #eef6ff;
      color: #26394e;
      line-height: 1.5;
    }}
    footer {{ margin-top: 56px; color: var(--muted); font-size: 13px; }}
    @media (max-width: 960px) {{
      header {{ grid-template-columns: 1fr; }}
      .grid, .theme-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .component-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 620px) {{
      .shell {{ padding: 24px 16px 56px; }}
      header {{ gap: 16px; }}
      .hero {{ padding: 24px; min-height: 0; }}
      .hero-grid {{ grid-template-columns: 1fr; }}
      .grid, .theme-grid, .component-grid {{ grid-template-columns: 1fr; }}
      .section-head {{ display: block; }}
      .section-head p {{ margin-top: 10px; }}
      nav {{ margin-left: -16px; margin-right: -16px; padding-left: 16px; padding-right: 16px; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="hero">
        <span class="eyebrow">Composable video direction</span>
        <h1>Template Gallery</h1>
        <p>Preview the narrative templates, scene modules, and visual skins that turn public source material into a short commercial-style vertical video.</p>
        <div class="hero-grid" aria-label="Registry counts">
          <div class="hero-chip"><strong>{len(STORY_TEMPLATES)}</strong><span>Story templates</span></div>
          <div class="hero-chip"><strong>{len(SCENE_COMPONENTS)}</strong><span>Scene components</span></div>
          <div class="hero-chip"><strong>{len(VISUAL_THEMES)}</strong><span>Visual themes</span></div>
        </div>
      </div>
      <aside class="guide" aria-label="How to read the gallery">
        <h2>How to read it</h2>
        <div class="layer-row">
          <div class="layer-no">1</div>
          <div><h3>Story template</h3><p>Chooses the narrative route: briefing, deep dive, market radar, evidence chain, comparison, timeline, and more.</p></div>
        </div>
        <div class="layer-row">
          <div class="layer-no">2</div>
          <div><h3>Scene component</h3><p>Chooses what each screen does: grid, metric stack, ledger, proof rail, timeline, matrix, stamp.</p></div>
        </div>
        <div class="layer-row">
          <div class="layer-no">3</div>
          <div><h3>Visual theme</h3><p>Chooses the skin: market terminal, executive light, data magazine, product keynote, social pop, or editorial dark.</p></div>
        </div>
      </aside>
    </header>
    <nav>
      <a href="#story-templates">Story templates</a>
      <a href="#scene-components">Scene components</a>
      <a href="#visual-themes">Visual themes</a>
      <a href="#composition-rule">Composition rule</a>
    </nav>
    <section id="story-templates">
      <div class="section-head">
        <h2>Story Templates</h2>
        <p>Templates are the editorial skeleton. They decide the order of scenes, while the actual sources and facts stay user-owned and local.</p>
      </div>
      <div class="grid">
        {story_cards}
      </div>
    </section>
    <section id="scene-components">
      <div class="section-head">
        <h2>Scene Components</h2>
        <p>Components are eight-second building blocks. Each one has a visual grammar and a purpose, so the renderer can assemble readable motion instead of static slides.</p>
      </div>
      {component_sections}
    </section>
    <section id="visual-themes">
      <div class="section-head">
        <h2>Visual Themes</h2>
        <p>Themes change palette, contrast, and information mood without changing the underlying facts or source links.</p>
      </div>
      <div class="theme-grid">
        {theme_cards}
      </div>
    </section>
    <section id="composition-rule">
      <div class="section-head">
        <h2>Composition Rule</h2>
        <p>One video direction is a simple product of three decisions.</p>
      </div>
      <div class="note">
        Pick <strong>one story template</strong>, fill it with <strong>scene components</strong>, then apply <strong>one visual theme</strong>. Example: <code>market_radar</code> + <code>market_ledger / signal_grid / verification_rail</code> + <code>market_terminal</code> creates a public market recap without exposing private holdings or private source lists.
      </div>
    </section>
    <footer>
      Generated from <code>src/daily_video_pipeline/templates.py</code>. Regenerate with <code>daily-video build-gallery</code>.
    </footer>
  </div>
</body>
</html>
"""


def _story_card(template: StoryTemplate) -> str:
    components = [SCENE_COMPONENTS[key] for key in template.components if key in SCENE_COMPONENTS]
    svg = _story_svg(template, components)
    sample = STORY_EXAMPLES.get(template.key, "Example: a source-backed short video package.")
    return f"""<article class="story-card">
  <div class="svg-wrap">{svg}</div>
  <div class="card-body">
    <div class="meta"><span>{escape(template.key)}</span><span>{len(template.components)} scenes</span></div>
    <h3>{escape(template.name)}</h3>
    <p>{escape(template.description)}</p>
    <div class="sample">{escape(sample)}</div>
  </div>
</article>"""


def _component_family_section(family: str) -> str:
    items = [component for component in SCENE_COMPONENTS.values() if component.family == family]
    if not items:
        return ""
    cards = "\n".join(_component_card(component) for component in items)
    title = FAMILY_LABELS.get(family, family.title())
    return f"""<div class="component-family">
  <h3>{escape(title)}</h3>
  <div class="component-grid">{cards}</div>
</div>"""


def _component_card(component: SceneComponent) -> str:
    return f"""<article class="component-card">
  <div class="svg-wrap">{_component_svg(component.family)}</div>
  <div class="card-body">
    <span class="pill">{escape(component.visual_grammar)}</span>
    <h4>{escape(component.name)}</h4>
    <p>{escape(component.purpose)}</p>
    <p style="margin-top:10px"><code>{escape(component.key)}</code></p>
  </div>
</article>"""


def _theme_card(key: str, theme: dict) -> str:
    swatches = "\n".join(
        f'<span class="swatch" title="{escape(name)}" style="background:{_rgb(theme[name])}"></span>'
        for name in ("background", "panel", "foreground", "accent", "accent2", "danger")
    )
    return f"""<article class="theme-card">
  <div class="svg-wrap">{_theme_svg(theme)}</div>
  <div class="card-body">
    <div class="meta"><span>{escape(key)}</span><span>{escape(theme["name"])}</span></div>
    <h4>{escape(theme["name"])}</h4>
    <p>{escape(THEME_USAGE.get(key, "A reusable commercial skin."))}</p>
    <div class="swatches">{swatches}</div>
  </div>
</article>"""


def _story_svg(template: StoryTemplate, components: list[SceneComponent]) -> str:
    width, height = 760, 245
    step_count = max(1, len(components))
    gap = (width - 120) / max(1, step_count - 1)
    nodes = []
    lines = []
    for idx, component in enumerate(components):
        x = 60 + idx * gap
        y = 112
        if idx > 0:
            prev_x = 60 + (idx - 1) * gap
            lines.append(f'<line x1="{prev_x + 18:.1f}" y1="{y}" x2="{x - 18:.1f}" y2="{y}" stroke="#26454a" stroke-width="4"/>')
        color = _component_color(component.family)
        label = _short_label(component.name, 16)
        nodes.append(
            f'<circle cx="{x:.1f}" cy="{y}" r="22" fill="{color}" stroke="#d9f6ea" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y + 5}" text-anchor="middle" font-size="14" font-weight="800" fill="#06120f">{idx + 1}</text>'
            f'<text x="{x:.1f}" y="{y + 52}" text-anchor="middle" font-size="18" font-weight="750" fill="#eef8f2">{escape(label)}</text>'
            f'<text x="{x:.1f}" y="{y + 77}" text-anchor="middle" font-size="13" fill="#83a09a">{escape(component.visual_grammar)}</text>'
        )
    return f"""<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(template.name)} flow">
  <rect width="{width}" height="{height}" fill="#071014"/>
  <rect x="24" y="22" width="{width - 48}" height="{height - 44}" rx="14" fill="#0d2026" stroke="#203b40"/>
  <text x="42" y="56" font-size="17" font-weight="800" fill="#17d684">{escape(template.key)}</text>
  <text x="{width - 42}" y="56" text-anchor="end" font-size="13" font-weight="800" fill="#83a09a">NARRATIVE FLOW</text>
  {''.join(lines)}
  {''.join(nodes)}
</svg>"""


def _component_svg(family: str) -> str:
    # These sketches are intentionally abstract: they show reading order and motion grammar,
    # not finished video artwork.
    sketch = {
        "cover": _svg_cover,
        "context": _svg_context,
        "grid": _svg_grid,
        "metric": _svg_metric,
        "ledger": _svg_ledger,
        "proof": _svg_proof,
        "chips": _svg_chips,
        "rail": _svg_rail,
        "timeline": _svg_timeline,
        "mechanism": _svg_mechanism,
        "split": _svg_split,
        "matrix": _svg_matrix,
        "ranking": _svg_ranking,
        "list": _svg_list,
        "map": _svg_map,
        "product": _svg_product,
        "stamp": _svg_stamp,
    }.get(family, _svg_context)
    return sketch()


def _svg_frame(inner: str) -> str:
    return f"""<svg viewBox="0 0 420 250" role="img" aria-label="Scene component sketch">
  <rect width="420" height="250" fill="#071014"/>
  <rect x="22" y="22" width="376" height="206" rx="12" fill="#0d2026" stroke="#203b40"/>
  {inner}
</svg>"""


def _svg_cover() -> str:
    return _svg_frame(
        '<rect x="48" y="55" width="82" height="14" rx="7" fill="#17d684"/>'
        '<rect x="48" y="92" width="235" height="20" rx="5" fill="#eef8f2"/>'
        '<rect x="48" y="122" width="186" height="16" rx="4" fill="#83a09a"/>'
        '<circle cx="318" cy="132" r="48" fill="#16393c" stroke="#ecca53" stroke-width="4"/>'
        '<path d="M292 132h52M318 106v52" stroke="#17d684" stroke-width="4"/>'
    )


def _svg_context() -> str:
    return _svg_frame(
        '<rect x="54" y="54" width="118" height="142" rx="10" fill="#102b31" stroke="#17d684"/>'
        '<rect x="192" y="66" width="170" height="28" rx="6" fill="#eef8f2"/>'
        '<rect x="192" y="111" width="132" height="18" rx="5" fill="#83a09a"/>'
        '<rect x="192" y="146" width="150" height="18" rx="5" fill="#83a09a"/>'
        '<path d="M172 126h35" stroke="#ecca53" stroke-width="4"/>'
    )


def _svg_grid() -> str:
    cells = []
    for y in (58, 131):
        for x in (52, 214):
            cells.append(f'<rect x="{x}" y="{y}" width="128" height="55" rx="9" fill="#102b31" stroke="#31545a"/>')
            cells.append(f'<circle cx="{x + 22}" cy="{y + 27}" r="8" fill="#17d684"/>')
            cells.append(f'<rect x="{x + 42}" y="{y + 20}" width="60" height="10" rx="5" fill="#eef8f2"/>')
    return _svg_frame("".join(cells))


def _svg_metric() -> str:
    rows = []
    for idx, y in enumerate((55, 101, 147)):
        color = "#17d684" if idx == 0 else "#eef8f2"
        rows.append(f'<rect x="50" y="{y}" width="320" height="34" rx="8" fill="#102b31" stroke="#31545a"/>')
        rows.append(f'<text x="70" y="{y + 24}" font-size="25" font-weight="850" fill="{color}">{["+2.4", "81%", "14"][idx]}</text>')
        rows.append(f'<path d="M244 {y + 23}l24 -10 22 12 28 -18 24 9" fill="none" stroke="#ecca53" stroke-width="3"/>')
    return _svg_frame("".join(rows))


def _svg_ledger() -> str:
    rows = []
    for idx, y in enumerate((56, 96, 136, 176)):
        rows.append(f'<rect x="48" y="{y}" width="324" height="28" rx="7" fill="#102b31" stroke="#31545a"/>')
        rows.append(f'<text x="65" y="{y + 20}" font-size="13" font-weight="800" fill="#17d684">0{idx + 1}</text>')
        rows.append(f'<rect x="102" y="{y + 9}" width="120" height="8" rx="4" fill="#eef8f2"/>')
        rows.append(f'<rect x="298" y="{y + 9}" width="44" height="8" rx="4" fill="#ecca53"/>')
    return _svg_frame("".join(rows))


def _svg_proof() -> str:
    return _svg_frame(
        '<path d="M58 82h278" stroke="#17d684" stroke-width="5"/>'
        '<circle cx="72" cy="82" r="12" fill="#17d684"/><circle cx="180" cy="82" r="12" fill="#17d684"/><circle cx="318" cy="82" r="12" fill="#ecca53"/>'
        '<rect x="64" y="126" width="292" height="62" rx="9" fill="#102b31" stroke="#17d684"/>'
        '<rect x="86" y="148" width="96" height="10" rx="5" fill="#eef8f2"/>'
        '<rect x="86" y="168" width="198" height="8" rx="4" fill="#83a09a"/>'
    )


def _svg_chips() -> str:
    chips = []
    for idx, (x, y) in enumerate(((54, 63), (181, 63), (54, 124), (181, 124))):
        color = "#17d684" if idx != 2 else "#ecca53"
        chips.append(f'<rect x="{x}" y="{y}" width="112" height="38" rx="19" fill="#102b31" stroke="{color}"/>')
        chips.append(f'<circle cx="{x + 22}" cy="{y + 19}" r="8" fill="{color}"/>')
        chips.append(f'<rect x="{x + 42}" y="{y + 15}" width="42" height="8" rx="4" fill="#eef8f2"/>')
    return _svg_frame("".join(chips))


def _svg_rail() -> str:
    stops = []
    for idx, x in enumerate((72, 158, 244, 330)):
        stops.append(f'<circle cx="{x}" cy="96" r="12" fill="{"#ecca53" if idx == 3 else "#17d684"}"/>')
        stops.append(f'<rect x="{x - 34}" y="128" width="68" height="38" rx="7" fill="#102b31" stroke="#31545a"/>')
    return _svg_frame('<path d="M72 96h258" stroke="#17d684" stroke-width="5"/>' + "".join(stops))


def _svg_timeline() -> str:
    cards = []
    for idx, y in enumerate((55, 101, 147)):
        cards.append(f'<circle cx="92" cy="{y + 16}" r="10" fill="{"#ecca53" if idx == 2 else "#17d684"}"/>')
        cards.append(f'<rect x="126" y="{y}" width="210" height="32" rx="7" fill="#102b31" stroke="#31545a"/>')
        cards.append(f'<rect x="146" y="{y + 12}" width="95" height="8" rx="4" fill="#eef8f2"/>')
    return _svg_frame('<path d="M92 62v116" stroke="#17d684" stroke-width="4"/>' + "".join(cards))


def _svg_mechanism() -> str:
    layers = []
    for idx, y in enumerate((58, 104, 150)):
        layers.append(f'<rect x="{60 + idx * 18}" y="{y}" width="{276 - idx * 36}" height="36" rx="8" fill="#102b31" stroke="{"#17d684" if idx == 2 else "#31545a"}"/>')
        layers.append(f'<rect x="{82 + idx * 18}" y="{y + 14}" width="110" height="8" rx="4" fill="#eef8f2"/>')
    return _svg_frame("".join(layers) + '<path d="M210 94v12M210 140v12" stroke="#ecca53" stroke-width="4"/>')


def _svg_split() -> str:
    return _svg_frame(
        '<rect x="52" y="62" width="138" height="114" rx="10" fill="#102b31" stroke="#31545a"/>'
        '<rect x="230" y="62" width="138" height="114" rx="10" fill="#102b31" stroke="#17d684"/>'
        '<rect x="76" y="94" width="78" height="10" rx="5" fill="#83a09a"/>'
        '<rect x="254" y="94" width="78" height="10" rx="5" fill="#eef8f2"/>'
        '<path d="M195 119h31" stroke="#ecca53" stroke-width="5"/>'
        '<path d="M218 108l12 11 -12 11" fill="none" stroke="#ecca53" stroke-width="5"/>'
    )


def _svg_matrix() -> str:
    cells = []
    labels = ("UP", "RISK", "OPEN", "CHECK")
    for idx, (x, y) in enumerate(((52, 58), (214, 58), (52, 132), (214, 132))):
        stroke = "#ecca53" if idx == 3 else "#31545a"
        cells.append(f'<rect x="{x}" y="{y}" width="128" height="54" rx="9" fill="#102b31" stroke="{stroke}"/>')
        cells.append(f'<text x="{x + 20}" y="{y + 32}" font-size="16" font-weight="850" fill="#eef8f2">{labels[idx]}</text>')
    return _svg_frame("".join(cells))


def _svg_ranking() -> str:
    rows = []
    for idx, w in enumerate((250, 205, 160, 112)):
        y = 55 + idx * 38
        rows.append(f'<text x="58" y="{y + 19}" font-size="16" font-weight="850" fill="#17d684">{idx + 1}</text>')
        rows.append(f'<rect x="92" y="{y}" width="{w}" height="24" rx="7" fill="#102b31" stroke="#31545a"/>')
        rows.append(f'<rect x="92" y="{y}" width="{max(44, w - 80)}" height="24" rx="7" fill="#17d684" opacity=".45"/>')
    return _svg_frame("".join(rows))


def _svg_list() -> str:
    rows = []
    for idx, y in enumerate((61, 101, 141, 181)):
        color = "#ecca53" if idx == 3 else "#17d684"
        rows.append(f'<circle cx="72" cy="{y}" r="8" fill="{color}"/>')
        rows.append(f'<rect x="96" y="{y - 6}" width="{210 - idx * 22}" height="12" rx="6" fill="#eef8f2"/>')
    return _svg_frame("".join(rows))


def _svg_map() -> str:
    return _svg_frame(
        '<circle cx="210" cy="123" r="40" fill="#102b31" stroke="#17d684" stroke-width="4"/>'
        '<circle cx="106" cy="82" r="18" fill="#16393c" stroke="#ecca53" stroke-width="3"/>'
        '<circle cx="314" cy="82" r="18" fill="#16393c" stroke="#17d684" stroke-width="3"/>'
        '<circle cx="110" cy="178" r="18" fill="#16393c" stroke="#17d684" stroke-width="3"/>'
        '<circle cx="318" cy="178" r="18" fill="#16393c" stroke="#ecca53" stroke-width="3"/>'
        '<path d="M126 89l50 21M294 90l-50 21M128 170l48 -28M298 170l-52 -28" stroke="#31545a" stroke-width="4"/>'
    )


def _svg_product() -> str:
    return _svg_frame(
        '<rect x="86" y="52" width="248" height="142" rx="16" fill="#102b31" stroke="#17d684" stroke-width="3"/>'
        '<circle cx="210" cy="122" r="42" fill="#16393c" stroke="#ecca53" stroke-width="4"/>'
        '<rect x="164" y="201" width="92" height="10" rx="5" fill="#83a09a"/>'
        '<path d="M110 126h56M254 126h56" stroke="#17d684" stroke-width="3"/>'
    )


def _svg_stamp() -> str:
    return _svg_frame(
        '<rect x="80" y="72" width="260" height="92" rx="12" fill="#102b31" stroke="#17d684" stroke-width="4"/>'
        '<text x="210" y="116" text-anchor="middle" font-size="23" font-weight="900" fill="#17d684">VERDICT</text>'
        '<rect x="122" y="134" width="176" height="10" rx="5" fill="#eef8f2"/>'
        '<circle cx="108" cy="190" r="7" fill="#17d684"/><rect x="128" y="184" width="176" height="10" rx="5" fill="#83a09a"/>'
    )


def _theme_svg(theme: dict) -> str:
    bg = _rgb(theme["background"])
    panel = _rgb(theme["panel"])
    panel_alt = _rgb(theme["panel_alt"])
    fg = _rgb(theme["foreground"])
    muted = _rgb(theme["muted"])
    accent = _rgb(theme["accent"])
    accent2 = _rgb(theme["accent2"])
    danger = _rgb(theme["danger"])
    return f"""<svg viewBox="0 0 420 250" role="img" aria-label="{escape(theme["name"])} preview">
  <rect width="420" height="250" fill="{bg}"/>
  <rect x="24" y="24" width="372" height="202" rx="12" fill="{panel}" stroke="{panel_alt}"/>
  <rect x="46" y="49" width="94" height="18" rx="9" fill="{accent}"/>
  <rect x="46" y="88" width="242" height="18" rx="5" fill="{fg}"/>
  <rect x="46" y="118" width="176" height="12" rx="6" fill="{muted}"/>
  <rect x="46" y="154" width="310" height="40" rx="8" fill="{panel_alt}"/>
  <rect x="68" y="168" width="84" height="12" rx="6" fill="{fg}"/>
  <path d="M238 178l22 -11 19 13 28 -21 25 12" fill="none" stroke="{accent2}" stroke-width="4"/>
  <circle cx="344" cy="65" r="14" fill="{danger}"/>
</svg>"""


def _rgb(value: tuple[int, int, int]) -> str:
    return f"rgb({value[0]}, {value[1]}, {value[2]})"


def _component_color(family: str) -> str:
    return {
        "cover": "#17d684",
        "context": "#57c0ff",
        "grid": "#17d684",
        "metric": "#ecca53",
        "ledger": "#17d684",
        "proof": "#ecca53",
        "chips": "#57c0ff",
        "rail": "#17d684",
        "timeline": "#57c0ff",
        "mechanism": "#ecca53",
        "split": "#57c0ff",
        "matrix": "#ecca53",
        "ranking": "#17d684",
        "list": "#17d684",
        "map": "#57c0ff",
        "product": "#ecca53",
        "stamp": "#17d684",
    }.get(family, "#17d684")


def _short_label(label: str, limit: int) -> str:
    if len(label) <= limit:
        return label
    return label[: max(1, limit - 1)].rstrip() + "."
