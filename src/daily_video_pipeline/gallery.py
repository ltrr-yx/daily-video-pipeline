from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from .templates import SCENE_COMPONENTS, STORY_TEMPLATES, VISUAL_THEMES, SceneComponent, StoryTemplate


STORY_I18N = {
    "daily_briefing": {
        "zh": "每日简报",
        "fit": "适合 3 到 5 条公开信号的快速整理。",
        "example": "示例：早间 AI 新闻、公开市场雷达、行业日报。",
    },
    "single_event_deep_dive": {
        "zh": "单事件深讲",
        "fit": "适合把一个事件讲清楚：背景、机制、证据、结论。",
        "example": "示例：新品发布、政策变化、研究结果。",
    },
    "breaking_update": {
        "zh": "突发更新",
        "fit": "适合短时间内说明一个新事实和下一步验证。",
        "example": "示例：官方公告、临时更新、盘中快讯。",
    },
    "product_launch": {
        "zh": "产品发布",
        "fit": "适合说明产品是什么、解决谁的问题、工作流如何改变。",
        "example": "示例：工具上线、硬件发布、功能改版。",
    },
    "company_update": {
        "zh": "公司动态",
        "fit": "适合围绕一个主体讲动作、证据、指标和风险。",
        "example": "示例：公司公告、融资、合作、财报摘要。",
    },
    "market_radar": {
        "zh": "市场雷达",
        "fit": "适合把多组指标放在同一张冷静的信息板上。",
        "example": "示例：市场宽度、行业强弱、资金与风险信号。",
    },
    "evidence_chain": {
        "zh": "证据链",
        "fit": "适合从来源、主张、验证路径一路讲到可信结论。",
        "example": "示例：传闻核验、模型评测、信息源复查。",
    },
    "comparison": {
        "zh": "横向比较",
        "fit": "适合比较两个工具、公司、方案或信号。",
        "example": "示例：A/B 产品对比、两类资产对比。",
    },
    "timeline": {
        "zh": "时间线",
        "fit": "适合讲一个过程怎样一步步演化。",
        "example": "示例：版本发布、政策进程、研究到产品。",
    },
    "risk_watch": {
        "zh": "风险观察",
        "fit": "适合把机会、不确定性、反证和检查点拆开。",
        "example": "示例：主题过热、数据冲突、风险提示。",
    },
    "top_five": {
        "zh": "榜单盘点",
        "fit": "适合做每日或每周 Top 列表，强调排序与证据。",
        "example": "示例：五条新闻、五个产品、五个信号。",
    },
    "weekly_review": {
        "zh": "周度复盘",
        "fit": "适合把一周的主题、变化和下周观察收束在一起。",
        "example": "示例：周末总结、周一视频选题、周报。",
    },
}

COMPONENT_I18N = {
    "cover_hook": ("开场钩子", "一句强判断建立观看理由。"),
    "impact_headline": ("冲击标题", "把刚发生的变化放到第一视觉层。"),
    "signal_grid": ("信号网格", "并列展示多条弱信号，不强行讲因果。"),
    "source_proof": ("来源证明", "突出原始来源、日期和证据线。"),
    "evidence_quote": ("证据摘句", "把一条关键证据做成引用板。"),
    "proof_chips": ("证据标签", "压缩来源、日期、标签和可信度。"),
    "metric_stack": ("指标堆栈", "纵向堆叠数字和短标签。"),
    "big_number": ("大数字", "让一个关键数字成为画面主角。"),
    "mini_chart": ("迷你图表", "用小趋势线表达变化方向。"),
    "market_ledger": ("市场账本", "用行项目承载密集指标。"),
    "data_table": ("数据表", "用列结构展示更规整的数据。"),
    "timeline_ribbon": ("时间丝带", "沿一条轨道展示阶段。"),
    "milestone_stack": ("里程碑堆叠", "把阶段卡片纵向推进。"),
    "week_calendar": ("周历", "按一周节奏总结信号。"),
    "compare_split": ("对比分屏", "左右并置比较两个对象。"),
    "before_after_surface": ("前后对照", "把旧状态和新状态并列出来。"),
    "context_panel": ("背景面板", "先框定故事发生的上下文。"),
    "mechanism_xray": ("机制透视", "拆开输入、机制和结果。"),
    "stack_layers": ("层级堆叠", "用层叠关系说明系统构成。"),
    "funnel": ("漏斗", "把多输入收敛到一个结果。"),
    "verification_rail": ("验证轨道", "沿多个检查点推进可信度。"),
    "entity_map": ("主体关系图", "展示谁和谁相关。"),
    "geographic_map": ("地域图", "把事件放到区域或地理语境里。"),
    "product_plate": ("产品主视觉", "给产品或对象一个高级展示位。"),
    "use_case_grid": ("场景网格", "展示产品能进入哪些使用场景。"),
    "three_takeaways": ("三点总结", "把结论压成三条可记住的信息。"),
    "risk_matrix": ("风险矩阵", "拆开上行、下行、未知和验证。"),
    "watchlist": ("观察清单", "列出接下来要看的对象。"),
    "next_watch": ("下一步观察", "用明确检查点收尾。"),
    "ranking_board": ("排名板", "用排序展示列表型内容。"),
    "pulse_monitor": ("脉冲监测", "表达状态、节奏和压力变化。"),
    "conclusion_stamp": ("结论印章", "把最后判断落得很清楚。"),
    "cta_end": ("行动收尾", "引导下一步查看、复盘或订阅。"),
    "insight_stack": ("洞察堆栈", "把几条判断叠成一个清晰观点。"),
}

THEME_I18N = {
    "editorial_dark": ("深色编辑部", "适合严肃新闻、研究札记、夜间复盘。"),
    "executive_light": ("高管浅色", "适合周报、简报、面向决策者的解释。"),
    "market_terminal": ("市场终端", "适合金融、KPI、市场宽度和密集数字。"),
    "product_keynote": ("产品发布会", "适合产品、功能、硬件和对象主视觉。"),
    "data_magazine": ("数据杂志", "适合图表型专题和慢一点的编辑节奏。"),
    "social_pop": ("社媒高能", "适合榜单、轻快盘点和更鲜明的社交包装。"),
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
    "cover": ("开场与冲击", "Opening and impact"),
    "context": ("背景与洞察", "Context and insight"),
    "grid": ("多信号组织", "Signal groups"),
    "metric": ("数字与图表", "Numbers and charts"),
    "ledger": ("账本与表格", "Ledgers and tables"),
    "proof": ("来源证明", "Source proof"),
    "chips": ("证据标签", "Proof chips"),
    "rail": ("验证轨道", "Validation rails"),
    "timeline": ("时间结构", "Timelines"),
    "mechanism": ("机制解释", "Mechanisms"),
    "split": ("对比结构", "Comparisons"),
    "matrix": ("风险结构", "Risk matrices"),
    "ranking": ("排名结构", "Rankings"),
    "list": ("观察清单", "Watch lists"),
    "map": ("主体与地图", "Entity maps"),
    "product": ("产品展示", "Product plates"),
    "stamp": ("结论收束", "Conclusions"),
}

COMPOSITION_EXAMPLES = (
    {
        "title": "公开市场复盘",
        "subtitle": "Market recap",
        "story": "market_radar",
        "component": "market_ledger",
        "theme": "market_terminal",
        "result": "市场宽度先修复，主线仍需成交验证。",
    },
    {
        "title": "产品发布短片",
        "subtitle": "Product launch",
        "story": "product_launch",
        "component": "product_plate",
        "theme": "product_keynote",
        "result": "把对象、场景和验证点放进同一条短片。",
    },
    {
        "title": "证据链解释",
        "subtitle": "Evidence explainer",
        "story": "evidence_chain",
        "component": "verification_rail",
        "theme": "executive_light",
        "result": "来源、主张、验证和结论顺序清楚。",
    },
)


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
        "# Template Gallery / 模板图库",
        "",
        "Open [`docs/gallery.html`](gallery.html) for the visual gallery.",
        "",
        "制作视频的方向由三层决定：",
        "",
        "- Story Template / 叙事模板：决定故事顺序。",
        "- Scene Component / 镜头类型：决定每个画面怎么表达。",
        "- Visual Theme / 视觉皮肤：决定颜色、质感和商业气质。",
        "",
        "## Story Templates / 叙事模板",
        "",
    ]
    for template in STORY_TEMPLATES.values():
        meta = STORY_I18N[template.key]
        flow = " -> ".join(template.components)
        lines.extend(
            [
                f"### {meta['zh']} / {template.name}",
                "",
                meta["fit"],
                "",
                f"- Key: `{template.key}`",
                f"- Flow: `{flow}`",
                f"- {meta['example']}",
                "",
            ]
        )

    lines.extend(["## Scene Components / 镜头类型", ""])
    for family in FAMILY_ORDER:
        items = [component for component in SCENE_COMPONENTS.values() if component.family == family]
        if not items:
            continue
        zh, en = FAMILY_LABELS[family]
        lines.extend([f"### {zh} / {en}", ""])
        for component in items:
            name_zh, purpose_zh = COMPONENT_I18N[component.key]
            lines.append(
                f"- `{component.key}` - {name_zh} / {component.name}: {purpose_zh} "
                f"Visual grammar: `{component.visual_grammar}`."
            )
        lines.append("")

    lines.extend(["## Visual Themes / 视觉皮肤", ""])
    for key, theme in VISUAL_THEMES.items():
        name_zh, usage_zh = THEME_I18N[key]
        lines.append(f"- `{key}` - {name_zh} / {theme['name']}: {usage_zh}")
    lines.extend(["", "## Composition Examples / 组合示例", ""])
    for example in COMPOSITION_EXAMPLES:
        lines.append(
            f"- {example['title']}: `{example['story']}` + `{example['component']}` + "
            f"`{example['theme']}` -> {example['result']}"
        )
    lines.append("")
    return "\n".join(lines)


def build_gallery_html() -> str:
    story_cards = "\n".join(_story_card(template) for template in STORY_TEMPLATES.values())
    scene_sections = "\n".join(_scene_family_section(family) for family in FAMILY_ORDER)
    theme_cards = "\n".join(_theme_card(key, theme) for key, theme in VISUAL_THEMES.items())
    combo_rows = "\n".join(_composition_row(example) for example in COMPOSITION_EXAMPLES)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daily Video Pipeline - Gallery / 模板图库</title>
  <style>
    :root {{
      --bg: #edf2f4;
      --surface: #fbfcfb;
      --surface-2: #f4f8f7;
      --ink: #101418;
      --text: #26323a;
      --muted: #5f6c73;
      --line: #cfd8dd;
      --line-strong: #aebdc5;
      --green: #0e9f6e;
      --green-dark: #087957;
      --blue: #1d63d8;
      --gold: #b7791f;
      --red: #c64f45;
      --radius: 8px;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(180deg, #f7faf9 0%, var(--bg) 42%, #e6edf0 100%);
    }}
    .shell {{
      width: min(1240px, calc(100% - 40px));
      margin: 0 auto;
      padding: 34px 0 72px;
    }}
    .hero {{
      color: #eef8f2;
      background: #071014;
      border: 1px solid #20343a;
      border-radius: var(--radius);
      padding: 30px;
      display: grid;
      grid-template-columns: minmax(260px, .82fr) minmax(420px, 1.18fr);
      gap: 28px;
      align-items: center;
    }}
    .hero h1 {{
      margin: 0 0 14px;
      font-size: 48px;
      line-height: 1.08;
      letter-spacing: 0;
      text-wrap: balance;
    }}
    .hero p {{
      margin: 0;
      max-width: 56ch;
      color: #b7c9c5;
      font-size: 17px;
      line-height: 1.62;
      text-wrap: pretty;
    }}
    .hero-meta {{
      margin-top: 22px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .metric-chip {{
      display: inline-flex;
      align-items: baseline;
      gap: 8px;
      padding: 8px 10px;
      background: #0e2025;
      border: 1px solid #244047;
      border-radius: var(--radius);
      color: #dff8ec;
      font-size: 13px;
    }}
    .metric-chip strong {{ font-size: 20px; color: #ffffff; }}
    .process {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }}
    .process-step {{
      min-height: 152px;
      padding: 16px;
      border-radius: var(--radius);
      background: #0e2025;
      border: 1px solid #25464c;
      position: relative;
    }}
    .process-step::after {{
      content: "→";
      position: absolute;
      right: -15px;
      top: 50%;
      transform: translateY(-50%);
      color: #6fe0aa;
      font-size: 26px;
      font-weight: 800;
      z-index: 1;
    }}
    .process-step:last-child::after {{ display: none; }}
    .process-step span {{
      display: inline-grid;
      place-items: center;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      color: #06120f;
      background: #24d293;
      font-weight: 850;
      margin-bottom: 18px;
    }}
    .process-step h2 {{
      margin: 0 0 7px;
      font-size: 18px;
      line-height: 1.16;
      color: #ffffff;
    }}
    .process-step p {{
      margin: 0;
      color: #91aaa4;
      font-size: 13px;
      line-height: 1.45;
    }}
    nav {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 24px 0 42px;
      padding: 10px;
      background: rgba(237, 242, 244, .92);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      backdrop-filter: blur(14px);
    }}
    nav a {{
      text-decoration: none;
      color: var(--ink);
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 8px 12px;
      font-size: 13px;
      font-weight: 750;
    }}
    section {{ margin-top: 56px; }}
    .section-head {{
      display: grid;
      grid-template-columns: minmax(260px, .85fr) minmax(320px, 1.15fr);
      gap: 32px;
      align-items: end;
      border-bottom: 1px solid var(--line);
      padding-bottom: 18px;
      margin-bottom: 18px;
    }}
    .section-head h2 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.16;
      letter-spacing: 0;
      text-wrap: balance;
    }}
    .section-head p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.62;
      max-width: 74ch;
    }}
    .eyebrow {{
      display: block;
      margin-bottom: 8px;
      color: var(--green-dark);
      font-size: 13px;
      font-weight: 820;
    }}
    .story-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 14px;
    }}
    .story-card, .scene-card, .theme-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      overflow: hidden;
    }}
    .story-card {{
      padding: 16px;
      display: grid;
      gap: 14px;
      min-height: 348px;
    }}
    .card-meta {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 780;
    }}
    .story-card h3, .scene-card h4, .theme-card h3 {{
      margin: 0;
      color: var(--ink);
      line-height: 1.2;
      text-wrap: balance;
    }}
    .story-card h3 {{ font-size: 22px; }}
    .story-card p, .scene-card p, .theme-card p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.52;
    }}
    .story-flow {{
      display: grid;
      gap: 7px;
      margin: 0;
      padding: 0;
      list-style: none;
    }}
    .story-flow li {{
      display: grid;
      grid-template-columns: 28px 1fr;
      gap: 8px;
      align-items: center;
      min-height: 34px;
      padding: 7px;
      border: 1px solid #dbe5e9;
      border-radius: var(--radius);
      background: var(--surface-2);
    }}
    .story-flow b {{
      display: grid;
      place-items: center;
      width: 24px;
      height: 24px;
      border-radius: 6px;
      background: #dff5eb;
      color: #0b6d51;
      font-size: 12px;
    }}
    .story-flow span {{
      color: var(--text);
      font-size: 13px;
      font-weight: 720;
      overflow-wrap: anywhere;
    }}
    .sample-line {{
      padding: 10px 12px;
      border-radius: var(--radius);
      background: #eef7f2;
      color: #254338;
      font-size: 13px;
      line-height: 1.48;
    }}
    .family {{
      margin-top: 28px;
    }}
    .family-title {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      margin-bottom: 12px;
    }}
    .family-title h3 {{
      margin: 0;
      font-size: 23px;
    }}
    .family-title span {{
      color: var(--muted);
      font-size: 13px;
      font-weight: 720;
    }}
    .scene-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(244px, 1fr));
      gap: 14px;
    }}
    .svg-wrap {{
      background: #071014;
      border-bottom: 1px solid #233a40;
    }}
    svg {{ display: block; width: 100%; height: auto; }}
    .scene-body, .theme-body {{
      padding: 14px;
    }}
    .scene-card h4 {{
      margin-top: 10px;
      font-size: 18px;
    }}
    .pill {{
      display: inline-flex;
      max-width: 100%;
      padding: 5px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f4f8f7;
      color: #31424a;
      font-size: 11px;
      font-weight: 800;
      overflow-wrap: anywhere;
    }}
    .theme-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 16px;
    }}
    .theme-card h3 {{ font-size: 21px; margin-top: 10px; }}
    .swatch-row {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 6px;
      margin-top: 14px;
    }}
    .swatch {{
      min-height: 40px;
      border-radius: 6px;
      border: 1px solid rgba(0,0,0,.14);
      display: flex;
      align-items: end;
      padding: 5px;
      color: rgba(0,0,0,.7);
      font-size: 10px;
      font-weight: 760;
    }}
    .swatch.dark-label {{ color: rgba(255,255,255,.78); }}
    .composition-list {{
      display: grid;
      gap: 24px;
    }}
    .composition-row {{
      padding: 18px 0 24px;
      border-bottom: 1px solid var(--line);
    }}
    .composition-row:first-child {{
      border-top: 1px solid var(--line);
    }}
    .composition-head {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: baseline;
      margin-bottom: 14px;
    }}
    .composition-head h3 {{
      margin: 0;
      font-size: 24px;
    }}
    .composition-head span {{
      color: var(--muted);
      font-weight: 760;
    }}
    .combo-panels {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}
    .combo-panel {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      overflow: hidden;
      min-width: 0;
    }}
    .combo-panel h4 {{
      margin: 0;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      font-size: 14px;
      color: var(--text);
    }}
    .combo-copy {{
      padding: 10px 12px 12px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }}
    code {{
      color: #0f513d;
      background: #e6f3ec;
      padding: 2px 5px;
      border-radius: 5px;
      font-size: 12px;
    }}
    footer {{
      margin-top: 56px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }}
    @media (max-width: 980px) {{
      .hero, .section-head {{ grid-template-columns: 1fr; }}
      .process {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .process-step:nth-child(2)::after {{ display: none; }}
      .combo-panels {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 620px) {{
      .shell {{ width: min(100% - 24px, 1240px); padding-top: 18px; }}
      .hero {{ padding: 20px; }}
      .hero h1 {{ font-size: 34px; }}
      .process, .combo-panels {{ grid-template-columns: 1fr; }}
      .process-step::after {{ display: none; }}
      .theme-grid {{ grid-template-columns: 1fr; }}
      .composition-head {{ display: block; }}
      nav {{ position: static; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      html {{ scroll-behavior: auto; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header class="hero">
      <div>
        <h1>三步选出视频方向</h1>
        <p>先选叙事模板，再选每个画面的镜头类型，最后套上视觉皮肤。用户只需要替换成本地信源、BGM 和配置，就能生成自己的短视频。</p>
        <div class="hero-meta" aria-label="Gallery counts">
          <span class="metric-chip"><strong>{len(STORY_TEMPLATES)}</strong> 叙事模板</span>
          <span class="metric-chip"><strong>{len(SCENE_COMPONENTS)}</strong> 镜头类型</span>
          <span class="metric-chip"><strong>{len(VISUAL_THEMES)}</strong> 视觉皮肤</span>
        </div>
      </div>
      <div class="process" aria-label="Video direction process">
        <article class="process-step"><span>1</span><h2>Story Template<br>叙事模板</h2><p>决定故事顺序：开场、证据、机制、风险、结论。</p></article>
        <article class="process-step"><span>2</span><h2>Scene Component<br>镜头类型</h2><p>决定单个画面怎么承载信息：账本、轨道、图表、对比。</p></article>
        <article class="process-step"><span>3</span><h2>Visual Theme<br>视觉皮肤</h2><p>决定气质：市场终端、产品发布会、数据杂志、社媒高能。</p></article>
        <article class="process-step"><span>4</span><h2>Rendered Video<br>输出视频</h2><p>组合成带 BGM 的竖版视频，并保留审片图 / contact sheet。</p></article>
      </div>
    </header>

    <nav aria-label="Gallery sections">
      <a href="#story-templates">叙事模板 Story</a>
      <a href="#scene-components">镜头类型 Scene</a>
      <a href="#visual-themes">视觉皮肤 Visual</a>
      <a href="#composition-rule">组合示例 Composition</a>
    </nav>

    <section id="story-templates">
      <div class="section-head">
        <div><span class="eyebrow">Story Template / 叙事模板</span><h2>先决定这条视频怎么讲</h2></div>
        <p>Story 层不是画面风格，而是编辑顺序。它回答：先抓注意力，还是先给证据？是做市场雷达，还是做单事件深讲？</p>
      </div>
      <div class="story-grid">{story_cards}</div>
    </section>

    <section id="scene-components">
      <div class="section-head">
        <div><span class="eyebrow">Scene Component / 镜头类型</span><h2>再决定每个画面长什么样</h2></div>
        <p>Scene 层是真正进入视频画面的模块。每个子类型都配了不同示意图，帮助用户判断它适合承载数字、证据、机制、对比还是结论。</p>
      </div>
      {scene_sections}
    </section>

    <section id="visual-themes">
      <div class="section-head">
        <div><span class="eyebrow">Visual Theme / 视觉皮肤</span><h2>最后选择商业气质</h2></div>
        <p>Visual 层不改变事实和结构，只改变色彩、密度、对比和质感。这里的预览用同一套信息构图展示不同皮肤落地后的效果。</p>
      </div>
      <div class="theme-grid">{theme_cards}</div>
    </section>

    <section id="composition-rule">
      <div class="section-head">
        <div><span class="eyebrow">Composition Rule / 组合示例</span><h2>三层组合后，会生成具体视频方向</h2></div>
        <p>每组从 Story、Scene、Visual 各选一个，最后给出一个结果画面。真实运行时会继续替换成用户自己的信源、脚本、BGM 和输出目录。</p>
      </div>
      <div class="composition-list">{combo_rows}</div>
    </section>

    <footer>
      Generated from <code>src/daily_video_pipeline/templates.py</code>. Regenerate with <code>daily-video build-gallery</code>. 示例内容只使用公开安全的泛化场景，不包含私人持仓、私人信源或个人投资观点。
    </footer>
  </main>
</body>
</html>
"""


def _story_card(template: StoryTemplate) -> str:
    meta = STORY_I18N[template.key]
    steps = "\n".join(
        f"<li><b>{idx}</b><span>{escape(_component_label(key))}</span></li>"
        for idx, key in enumerate(template.components, 1)
    )
    return f"""<article class="story-card">
  <div class="card-meta"><span><code>{escape(template.key)}</code></span><span>{len(template.components)} scenes</span></div>
  <div>
    <h3>{escape(meta["zh"])} / {escape(template.name)}</h3>
    <p>{escape(meta["fit"])}</p>
  </div>
  <ol class="story-flow">{steps}</ol>
  <div class="sample-line">{escape(meta["example"])}</div>
</article>"""


def _scene_family_section(family: str) -> str:
    items = [component for component in SCENE_COMPONENTS.values() if component.family == family]
    if not items:
        return ""
    zh, en = FAMILY_LABELS[family]
    cards = "\n".join(_scene_card(component) for component in items)
    return f"""<div class="family">
  <div class="family-title"><h3>{escape(zh)}</h3><span>{escape(en)}</span></div>
  <div class="scene-grid">{cards}</div>
</div>"""


def _scene_card(component: SceneComponent) -> str:
    name_zh, purpose_zh = COMPONENT_I18N[component.key]
    return f"""<article class="scene-card">
  <div class="svg-wrap">{_component_svg(component)}</div>
  <div class="scene-body">
    <span class="pill">{escape(component.visual_grammar)}</span>
    <h4>{escape(name_zh)} / {escape(component.name)}</h4>
    <p>{escape(purpose_zh)}</p>
    <p style="margin-top:9px"><code>{escape(component.key)}</code></p>
  </div>
</article>"""


def _theme_card(key: str, theme: dict[str, Any]) -> str:
    name_zh, usage_zh = THEME_I18N[key]
    swatches = "\n".join(
        _swatch(name, theme[name])
        for name in ("background", "panel", "foreground", "accent", "accent2", "danger")
    )
    return f"""<article class="theme-card">
  <div class="svg-wrap">{_theme_svg(key, theme)}</div>
  <div class="theme-body">
    <div class="card-meta"><span><code>{escape(key)}</code></span><span>{escape(theme["name"])}</span></div>
    <h3>{escape(name_zh)} / {escape(theme["name"])}</h3>
    <p>{escape(usage_zh)}</p>
    <div class="swatch-row">{swatches}</div>
  </div>
</article>"""


def _composition_row(example: dict[str, str]) -> str:
    story = STORY_TEMPLATES[example["story"]]
    component = SCENE_COMPONENTS[example["component"]]
    theme = VISUAL_THEMES[example["theme"]]
    story_meta = STORY_I18N[story.key]
    comp_name, _ = COMPONENT_I18N[component.key]
    theme_name, _ = THEME_I18N[example["theme"]]
    return f"""<article class="composition-row">
  <div class="composition-head">
    <h3>{escape(example["title"])}</h3>
    <span>{escape(example["subtitle"])}</span>
  </div>
  <div class="combo-panels">
    <div class="combo-panel"><h4>1. Story</h4>{_mini_story_svg(story)}<div class="combo-copy">叙事骨架：{escape(story_meta["zh"])}<br><code>{escape(story.key)}</code></div></div>
    <div class="combo-panel"><h4>2. Scene</h4>{_component_svg(component)}<div class="combo-copy">镜头模块：{escape(comp_name)}<br><code>{escape(component.key)}</code></div></div>
    <div class="combo-panel"><h4>3. Visual</h4>{_theme_svg(example["theme"], theme)}<div class="combo-copy">视觉皮肤：{escape(theme_name)}<br><code>{escape(example["theme"])}</code></div></div>
    <div class="combo-panel"><h4>4. Result</h4>{_result_svg(example, component, theme)}<div class="combo-copy">输出方向：{escape(example["result"])}</div></div>
  </div>
</article>"""


def _component_label(key: str) -> str:
    if key not in SCENE_COMPONENTS:
        return key
    name_zh, _ = COMPONENT_I18N[key]
    return f"{name_zh} / {SCENE_COMPONENTS[key].name}"


def _swatch(name: str, value: tuple[int, int, int]) -> str:
    label_class = " dark-label" if sum(value) < 390 else ""
    label = {
        "background": "bg",
        "panel": "panel",
        "foreground": "ink",
        "accent": "a1",
        "accent2": "a2",
        "danger": "risk",
    }.get(name, name)
    return f'<span class="swatch{label_class}" title="{escape(name)}" style="background:{_rgb(value)}">{escape(label)}</span>'


def _component_svg(component: SceneComponent) -> str:
    key = component.key
    return {
        "cover_hook": _svg_cover_hook,
        "impact_headline": _svg_impact_headline,
        "signal_grid": _svg_signal_grid,
        "source_proof": _svg_source_proof,
        "evidence_quote": _svg_evidence_quote,
        "proof_chips": _svg_proof_chips,
        "metric_stack": _svg_metric_stack,
        "big_number": _svg_big_number,
        "mini_chart": _svg_mini_chart,
        "market_ledger": _svg_market_ledger,
        "data_table": _svg_data_table,
        "timeline_ribbon": _svg_timeline_ribbon,
        "milestone_stack": _svg_milestone_stack,
        "week_calendar": _svg_week_calendar,
        "compare_split": _svg_compare_split,
        "before_after_surface": _svg_before_after,
        "context_panel": _svg_context_panel,
        "mechanism_xray": _svg_mechanism_xray,
        "stack_layers": _svg_stack_layers,
        "funnel": _svg_funnel,
        "verification_rail": _svg_verification_rail,
        "entity_map": _svg_entity_map,
        "geographic_map": _svg_geographic_map,
        "product_plate": _svg_product_plate,
        "use_case_grid": _svg_use_case_grid,
        "three_takeaways": _svg_three_takeaways,
        "risk_matrix": _svg_risk_matrix,
        "watchlist": _svg_watchlist,
        "next_watch": _svg_next_watch,
        "ranking_board": _svg_ranking_board,
        "pulse_monitor": _svg_pulse_monitor,
        "conclusion_stamp": _svg_conclusion_stamp,
        "cta_end": _svg_cta_end,
        "insight_stack": _svg_insight_stack,
    }.get(key, _svg_context_panel)()


def _svg_frame(inner: str, label: str = "") -> str:
    label_text = f'<text x="30" y="31" font-size="12" font-weight="800" fill="#7ce0aa">{escape(label)}</text>' if label else ""
    return f"""<svg viewBox="0 0 420 260" role="img" aria-label="{escape(label or 'scene preview')}">
  <rect width="420" height="260" fill="#071014"/>
  <rect x="18" y="18" width="384" height="224" rx="10" fill="#0c2025" stroke="#234047"/>
  {label_text}
  {inner}
</svg>"""


def _svg_cover_hook() -> str:
    return _svg_frame(
        '<rect x="42" y="55" width="86" height="13" rx="7" fill="#23d293"/>'
        '<rect x="42" y="94" width="236" height="24" rx="6" fill="#edf9f3"/>'
        '<rect x="42" y="128" width="184" height="16" rx="5" fill="#86a59f"/>'
        '<circle cx="315" cy="135" r="51" fill="#17343a" stroke="#f0c85a" stroke-width="4"/>'
        '<path d="M286 135h58M315 106v58" stroke="#23d293" stroke-width="5"/>',
        "cover hook",
    )


def _svg_impact_headline() -> str:
    return _svg_frame(
        '<rect x="42" y="56" width="64" height="13" rx="7" fill="#f0c85a"/>'
        '<rect x="42" y="89" width="276" height="38" rx="7" fill="#edf9f3"/>'
        '<rect x="42" y="143" width="230" height="18" rx="5" fill="#86a59f"/>'
        '<rect x="42" y="184" width="330" height="24" rx="6" fill="#19323a" stroke="#e65b54"/>'
        '<circle cx="342" cy="104" r="18" fill="#e65b54"/>',
        "impact",
    )


def _svg_signal_grid() -> str:
    cells = []
    for idx, (x, y) in enumerate(((42, 60), (214, 60), (42, 144), (214, 144)), 1):
        color = "#23d293" if idx != 4 else "#f0c85a"
        cells.append(f'<rect x="{x}" y="{y}" width="150" height="62" rx="9" fill="#112c33" stroke="#31555d"/>')
        cells.append(f'<circle cx="{x + 24}" cy="{y + 29}" r="8" fill="{color}"/>')
        cells.append(f'<rect x="{x + 44}" y="{y + 20}" width="74" height="9" rx="5" fill="#edf9f3"/>')
        cells.append(f'<rect x="{x + 44}" y="{y + 38}" width="52" height="7" rx="4" fill="#86a59f"/>')
    return _svg_frame("".join(cells), "signal grid")


def _svg_source_proof() -> str:
    return _svg_frame(
        '<rect x="48" y="64" width="318" height="122" rx="10" fill="#112c33" stroke="#23d293"/>'
        '<rect x="70" y="84" width="88" height="12" rx="6" fill="#23d293"/>'
        '<rect x="70" y="116" width="226" height="12" rx="6" fill="#edf9f3"/>'
        '<rect x="70" y="144" width="178" height="9" rx="5" fill="#86a59f"/>'
        '<path d="M294 147l18 18 38 -48" fill="none" stroke="#f0c85a" stroke-width="6"/>',
        "source proof",
    )


def _svg_evidence_quote() -> str:
    return _svg_frame(
        '<rect x="50" y="58" width="320" height="142" rx="10" fill="#112c33" stroke="#31555d"/>'
        '<text x="74" y="105" font-size="54" fill="#23d293" font-weight="900">“</text>'
        '<rect x="116" y="90" width="194" height="14" rx="7" fill="#edf9f3"/>'
        '<rect x="116" y="119" width="220" height="10" rx="5" fill="#86a59f"/>'
        '<rect x="116" y="145" width="156" height="10" rx="5" fill="#86a59f"/>'
        '<rect x="246" y="176" width="88" height="14" rx="7" fill="#f0c85a"/>',
        "quote",
    )


def _svg_proof_chips() -> str:
    chips = []
    for idx, (x, y, w) in enumerate(((46, 66, 116), (178, 66, 148), (46, 126, 142), (205, 126, 116), (94, 186, 186))):
        color = ("#23d293", "#64c7ff", "#f0c85a", "#23d293", "#e65b54")[idx]
        chips.append(f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="18" fill="#112c33" stroke="{color}"/>')
        chips.append(f'<circle cx="{x + 22}" cy="{y + 18}" r="7" fill="{color}"/>')
        chips.append(f'<rect x="{x + 40}" y="{y + 14}" width="{max(34, w - 68)}" height="8" rx="4" fill="#edf9f3"/>')
    return _svg_frame("".join(chips), "proof chips")


def _svg_metric_stack() -> str:
    rows = []
    for idx, (y, value) in enumerate(((58, "+2.4"), (108, "81%"), (158, "14"))):
        rows.append(f'<rect x="46" y="{y}" width="328" height="39" rx="9" fill="#112c33" stroke="#31555d"/>')
        rows.append(f'<text x="70" y="{y + 28}" font-size="25" font-weight="850" fill="{"#23d293" if idx == 0 else "#edf9f3"}">{value}</text>')
        rows.append(f'<rect x="162" y="{y + 15}" width="74" height="9" rx="5" fill="#86a59f"/>')
        rows.append(f'<path d="M270 {y + 26}l22 -10 20 11 24 -18 24 12" fill="none" stroke="#f0c85a" stroke-width="3"/>')
    return _svg_frame("".join(rows), "metrics")


def _svg_big_number() -> str:
    return _svg_frame(
        '<text x="52" y="142" font-size="78" font-weight="900" fill="#23d293">204</text>'
        '<rect x="58" y="160" width="166" height="12" rx="6" fill="#edf9f3"/>'
        '<rect x="58" y="187" width="246" height="9" rx="5" fill="#86a59f"/>'
        '<circle cx="322" cy="132" r="42" fill="#17343a" stroke="#f0c85a" stroke-width="4"/>',
        "big number",
    )


def _svg_mini_chart() -> str:
    return _svg_frame(
        '<rect x="50" y="62" width="316" height="142" rx="10" fill="#112c33" stroke="#31555d"/>'
        '<path d="M78 176h252M78 82v94" stroke="#31555d" stroke-width="3"/>'
        '<path d="M84 158l42 -34 35 18 50 -56 44 44 66 -70" fill="none" stroke="#23d293" stroke-width="6"/>'
        '<path d="M84 160l42 -36 35 18 50 -54 44 44 66 -70v96H84z" fill="#23d293" opacity=".12"/>'
        '<circle cx="321" cy="60" r="8" fill="#f0c85a"/>',
        "mini chart",
    )


def _svg_market_ledger() -> str:
    rows = []
    for idx, y in enumerate((58, 96, 134, 172), 1):
        rows.append(f'<rect x="46" y="{y}" width="328" height="29" rx="7" fill="#112c33" stroke="#31555d"/>')
        rows.append(f'<text x="64" y="{y + 20}" font-size="13" font-weight="850" fill="#23d293">0{idx}</text>')
        rows.append(f'<rect x="105" y="{y + 10}" width="126" height="8" rx="4" fill="#edf9f3"/>')
        rows.append(f'<rect x="300" y="{y + 10}" width="48" height="8" rx="4" fill="#f0c85a"/>')
    return _svg_frame("".join(rows), "ledger")


def _svg_data_table() -> str:
    grid = ['<rect x="48" y="58" width="324" height="144" rx="10" fill="#112c33" stroke="#31555d"/>']
    for x in (150, 250):
        grid.append(f'<path d="M{x} 58v144" stroke="#31555d" stroke-width="2"/>')
    for y in (92, 128, 164):
        grid.append(f'<path d="M48 {y}h324" stroke="#31555d" stroke-width="2"/>')
    for x in (70, 170, 270):
        grid.append(f'<rect x="{x}" y="72" width="54" height="8" rx="4" fill="#23d293"/>')
    for y in (105, 141, 177):
        for x in (70, 170, 270):
            grid.append(f'<rect x="{x}" y="{y}" width="58" height="7" rx="4" fill="#edf9f3"/>')
    return _svg_frame("".join(grid), "table")


def _svg_timeline_ribbon() -> str:
    stops = []
    for idx, x in enumerate((70, 154, 238, 322)):
        stops.append(f'<circle cx="{x}" cy="110" r="12" fill="{"#f0c85a" if idx == 3 else "#23d293"}"/>')
        stops.append(f'<rect x="{x - 32}" y="{142 + (idx % 2) * 20}" width="64" height="24" rx="6" fill="#112c33" stroke="#31555d"/>')
    return _svg_frame('<path d="M70 110h252" stroke="#23d293" stroke-width="5"/>' + "".join(stops), "timeline")


def _svg_milestone_stack() -> str:
    cards = []
    for idx, y in enumerate((58, 112, 166)):
        cards.append(f'<rect x="{78 + idx * 24}" y="{y}" width="{256 - idx * 48}" height="35" rx="8" fill="#112c33" stroke="{"#23d293" if idx == 2 else "#31555d"}"/>')
        cards.append(f'<rect x="{100 + idx * 24}" y="{y + 13}" width="96" height="8" rx="4" fill="#edf9f3"/>')
    return _svg_frame("".join(cards), "milestones")


def _svg_week_calendar() -> str:
    cells = []
    for row in range(2):
        for col in range(4):
            idx = row * 4 + col
            x = 52 + col * 80
            y = 70 + row * 66
            color = "#23d293" if idx in (1, 4, 6) else "#31555d"
            if idx < 7:
                cells.append(f'<rect x="{x}" y="{y}" width="58" height="44" rx="7" fill="#112c33" stroke="{color}"/>')
                cells.append(f'<rect x="{x + 13}" y="{y + 16}" width="32" height="8" rx="4" fill="#edf9f3"/>')
    return _svg_frame("".join(cells), "week")


def _svg_compare_split() -> str:
    return _svg_frame(
        '<rect x="48" y="62" width="134" height="128" rx="10" fill="#112c33" stroke="#31555d"/>'
        '<rect x="238" y="62" width="134" height="128" rx="10" fill="#112c33" stroke="#23d293"/>'
        '<rect x="72" y="98" width="70" height="12" rx="6" fill="#edf9f3"/>'
        '<rect x="262" y="98" width="70" height="12" rx="6" fill="#edf9f3"/>'
        '<path d="M191 126h39" stroke="#f0c85a" stroke-width="5"/>'
        '<path d="M222 113l14 13 -14 13" fill="none" stroke="#f0c85a" stroke-width="5"/>',
        "compare",
    )


def _svg_before_after() -> str:
    return _svg_frame(
        '<rect x="46" y="68" width="138" height="112" rx="10" fill="#162831" stroke="#e65b54"/>'
        '<rect x="236" y="68" width="138" height="112" rx="10" fill="#112c33" stroke="#23d293"/>'
        '<text x="75" y="104" font-size="15" font-weight="850" fill="#e65b54">BEFORE</text>'
        '<text x="266" y="104" font-size="15" font-weight="850" fill="#23d293">AFTER</text>'
        '<rect x="76" y="130" width="72" height="9" rx="5" fill="#86a59f"/>'
        '<rect x="266" y="130" width="72" height="9" rx="5" fill="#edf9f3"/>',
        "before after",
    )


def _svg_context_panel() -> str:
    return _svg_frame(
        '<rect x="46" y="58" width="110" height="144" rx="10" fill="#112c33" stroke="#23d293"/>'
        '<rect x="178" y="72" width="178" height="24" rx="6" fill="#edf9f3"/>'
        '<rect x="178" y="114" width="128" height="12" rx="6" fill="#86a59f"/>'
        '<rect x="178" y="144" width="156" height="12" rx="6" fill="#86a59f"/>'
        '<path d="M156 130h36" stroke="#f0c85a" stroke-width="4"/>',
        "context",
    )


def _svg_mechanism_xray() -> str:
    return _svg_frame(
        '<circle cx="210" cy="130" r="58" fill="#17343a" stroke="#23d293" stroke-width="4"/>'
        '<ellipse cx="210" cy="130" rx="96" ry="24" fill="none" stroke="#31555d" stroke-width="3"/>'
        '<path d="M92 130h76M252 130h76" stroke="#f0c85a" stroke-width="5"/>'
        '<rect x="56" y="94" width="74" height="28" rx="7" fill="#112c33" stroke="#31555d"/>'
        '<rect x="290" y="138" width="74" height="28" rx="7" fill="#112c33" stroke="#31555d"/>',
        "x-ray",
    )


def _svg_stack_layers() -> str:
    layers = []
    for idx, y in enumerate((72, 112, 152)):
        layers.append(f'<rect x="{72 + idx * 24}" y="{y}" width="{276 - idx * 48}" height="32" rx="8" fill="#112c33" stroke="{"#23d293" if idx == 2 else "#31555d"}"/>')
        layers.append(f'<rect x="{96 + idx * 24}" y="{y + 12}" width="90" height="8" rx="4" fill="#edf9f3"/>')
    return _svg_frame("".join(layers), "layers")


def _svg_funnel() -> str:
    return _svg_frame(
        '<path d="M82 66h256l-52 58H134z" fill="#112c33" stroke="#31555d" stroke-width="3"/>'
        '<path d="M134 124h152l-42 52h-68z" fill="#123238" stroke="#23d293" stroke-width="3"/>'
        '<rect x="176" y="184" width="68" height="16" rx="8" fill="#f0c85a"/>'
        '<rect x="126" y="87" width="72" height="8" rx="4" fill="#edf9f3"/>',
        "funnel",
    )


def _svg_verification_rail() -> str:
    stops = []
    for idx, x in enumerate((68, 160, 252, 344)):
        stops.append(f'<circle cx="{x}" cy="90" r="12" fill="{"#f0c85a" if idx == 3 else "#23d293"}"/>')
        stops.append(f'<rect x="{x - 38}" y="124" width="76" height="42" rx="7" fill="#112c33" stroke="#31555d"/>')
        stops.append(f'<rect x="{x - 24}" y="142" width="48" height="7" rx="4" fill="#86a59f"/>')
    return _svg_frame('<path d="M68 90h276" stroke="#23d293" stroke-width="5"/>' + "".join(stops), "verify")


def _svg_entity_map() -> str:
    return _svg_frame(
        '<circle cx="210" cy="130" r="35" fill="#112c33" stroke="#23d293" stroke-width="4"/>'
        '<circle cx="100" cy="84" r="22" fill="#17343a" stroke="#f0c85a" stroke-width="3"/>'
        '<circle cx="318" cy="82" r="22" fill="#17343a" stroke="#64c7ff" stroke-width="3"/>'
        '<circle cx="111" cy="188" r="22" fill="#17343a" stroke="#23d293" stroke-width="3"/>'
        '<circle cx="318" cy="184" r="22" fill="#17343a" stroke="#f0c85a" stroke-width="3"/>'
        '<path d="M121 92l58 25M297 91l-58 25M130 178l50 -30M298 175l-56 -28" stroke="#31555d" stroke-width="4"/>',
        "entity map",
    )


def _svg_geographic_map() -> str:
    return _svg_frame(
        '<path d="M86 88c42 -38 92 -20 114 14 34 -34 86 -24 116 12 34 40 2 92 -48 98 -54 7 -82 -24 -118 -10 -56 21 -102 -12 -98 -58 2 -22 14 -40 34 -56z" fill="#112c33" stroke="#31555d" stroke-width="3"/>'
        '<circle cx="160" cy="120" r="9" fill="#23d293"/><circle cx="250" cy="146" r="9" fill="#f0c85a"/><circle cx="292" cy="104" r="9" fill="#64c7ff"/>'
        '<path d="M160 120c32 18 58 22 90 26" fill="none" stroke="#23d293" stroke-width="3"/>',
        "map",
    )


def _svg_product_plate() -> str:
    return _svg_frame(
        '<rect x="82" y="54" width="256" height="150" rx="14" fill="#112c33" stroke="#23d293" stroke-width="3"/>'
        '<circle cx="210" cy="128" r="45" fill="#17343a" stroke="#f0c85a" stroke-width="4"/>'
        '<rect x="176" y="118" width="68" height="22" rx="11" fill="#23d293"/>'
        '<path d="M108 128h58M254 128h58" stroke="#64c7ff" stroke-width="3"/>'
        '<rect x="148" y="214" width="124" height="8" rx="4" fill="#86a59f"/>',
        "product",
    )


def _svg_use_case_grid() -> str:
    blocks = []
    for idx, (x, y) in enumerate(((50, 62), (250, 62), (50, 158), (250, 158))):
        blocks.append(f'<rect x="{x}" y="{y}" width="120" height="48" rx="9" fill="#112c33" stroke="#31555d"/>')
        blocks.append(f'<rect x="{x + 20}" y="{y + 19}" width="58" height="8" rx="4" fill="#edf9f3"/>')
    blocks.append('<circle cx="210" cy="130" r="32" fill="#17343a" stroke="#23d293" stroke-width="4"/>')
    return _svg_frame("".join(blocks), "use cases")


def _svg_three_takeaways() -> str:
    cards = []
    for idx, x in enumerate((48, 160, 272), 1):
        cards.append(f'<rect x="{x}" y="76" width="92" height="118" rx="10" fill="#112c33" stroke="#31555d"/>')
        cards.append(f'<text x="{x + 20}" y="110" font-size="23" font-weight="900" fill="#23d293">{idx}</text>')
        cards.append(f'<rect x="{x + 20}" y="135" width="48" height="9" rx="5" fill="#edf9f3"/>')
        cards.append(f'<rect x="{x + 20}" y="158" width="36" height="7" rx="4" fill="#86a59f"/>')
    return _svg_frame("".join(cards), "3 takeaways")


def _svg_risk_matrix() -> str:
    labels = ("UP", "RISK", "OPEN", "CHECK")
    cells = []
    for idx, (x, y) in enumerate(((48, 62), (220, 62), (48, 144), (220, 144))):
        color = ("#23d293", "#e65b54", "#64c7ff", "#f0c85a")[idx]
        cells.append(f'<rect x="{x}" y="{y}" width="150" height="58" rx="9" fill="#112c33" stroke="{color}"/>')
        cells.append(f'<text x="{x + 20}" y="{y + 36}" font-size="17" font-weight="850" fill="#edf9f3">{labels[idx]}</text>')
    return _svg_frame("".join(cells), "risk matrix")


def _svg_watchlist() -> str:
    rows = []
    for idx, y in enumerate((70, 108, 146, 184)):
        color = "#f0c85a" if idx == 3 else "#23d293"
        rows.append(f'<circle cx="76" cy="{y}" r="8" fill="{color}"/>')
        rows.append(f'<rect x="102" y="{y - 6}" width="{230 - idx * 28}" height="12" rx="6" fill="#edf9f3"/>')
    return _svg_frame("".join(rows), "watchlist")


def _svg_next_watch() -> str:
    return _svg_frame(
        '<path d="M70 178c48 -38 86 -38 134 0s86 38 146 0" fill="none" stroke="#31555d" stroke-width="4"/>'
        '<circle cx="102" cy="156" r="11" fill="#23d293"/><circle cx="210" cy="178" r="11" fill="#f0c85a"/><circle cx="322" cy="148" r="11" fill="#64c7ff"/>'
        '<rect x="72" y="66" width="240" height="18" rx="6" fill="#edf9f3"/>'
        '<rect x="72" y="102" width="166" height="11" rx="6" fill="#86a59f"/>',
        "next watch",
    )


def _svg_ranking_board() -> str:
    rows = []
    for idx, w in enumerate((246, 208, 172, 126, 90)):
        y = 56 + idx * 34
        rows.append(f'<text x="56" y="{y + 20}" font-size="15" font-weight="850" fill="#23d293">{idx + 1}</text>')
        rows.append(f'<rect x="90" y="{y}" width="{w}" height="22" rx="7" fill="#112c33" stroke="#31555d"/>')
        rows.append(f'<rect x="90" y="{y}" width="{max(38, w - 76)}" height="22" rx="7" fill="#23d293" opacity=".45"/>')
    return _svg_frame("".join(rows), "ranking")


def _svg_pulse_monitor() -> str:
    return _svg_frame(
        '<rect x="48" y="70" width="324" height="120" rx="10" fill="#112c33" stroke="#31555d"/>'
        '<path d="M70 130h44l18 -36 26 72 22 -52 18 16h42l24 -30 20 58 22 -28h44" fill="none" stroke="#23d293" stroke-width="5"/>'
        '<rect x="70" y="86" width="86" height="9" rx="5" fill="#edf9f3"/>'
        '<circle cx="344" cy="94" r="8" fill="#f0c85a"/>',
        "pulse",
    )


def _svg_conclusion_stamp() -> str:
    return _svg_frame(
        '<rect x="74" y="72" width="272" height="100" rx="12" fill="#112c33" stroke="#23d293" stroke-width="4"/>'
        '<text x="210" y="116" text-anchor="middle" font-size="24" font-weight="900" fill="#23d293">VERDICT</text>'
        '<rect x="126" y="136" width="168" height="10" rx="5" fill="#edf9f3"/>'
        '<circle cx="88" cy="204" r="7" fill="#23d293"/><rect x="108" y="198" width="200" height="10" rx="5" fill="#86a59f"/>',
        "stamp",
    )


def _svg_cta_end() -> str:
    return _svg_frame(
        '<rect x="72" y="70" width="276" height="120" rx="12" fill="#112c33" stroke="#31555d"/>'
        '<rect x="112" y="104" width="196" height="18" rx="6" fill="#edf9f3"/>'
        '<rect x="136" y="144" width="148" height="32" rx="16" fill="#23d293"/>'
        '<path d="M270 160h-28M260 148l14 12 -14 12" fill="none" stroke="#06120f" stroke-width="4"/>'
        '<circle cx="318" cy="84" r="10" fill="#f0c85a"/>',
        "cta",
    )


def _svg_insight_stack() -> str:
    cards = []
    for idx, (x, y) in enumerate(((86, 70), (66, 104), (106, 138))):
        color = "#23d293" if idx == 2 else "#31555d"
        cards.append(f'<rect x="{x}" y="{y}" width="228" height="50" rx="9" fill="#112c33" stroke="{color}"/>')
        cards.append(f'<rect x="{x + 22}" y="{y + 18}" width="116" height="8" rx="4" fill="#edf9f3"/>')
    return _svg_frame("".join(cards), "insights")


def _mini_story_svg(story: StoryTemplate) -> str:
    steps = []
    for idx, key in enumerate(story.components[:5], 1):
        y = 58 + (idx - 1) * 34
        steps.append(f'<rect x="48" y="{y}" width="324" height="24" rx="7" fill="#112c33" stroke="#31555d"/>')
        steps.append(f'<text x="64" y="{y + 17}" font-size="12" font-weight="850" fill="#23d293">{idx}</text>')
        steps.append(f'<rect x="94" y="{y + 8}" width="{110 + idx * 18}" height="7" rx="4" fill="#edf9f3"/>')
    return _svg_frame("".join(steps), story.key)


def _theme_svg(key: str, theme: dict[str, Any]) -> str:
    bg = _rgb(theme["background"])
    panel = _rgb(theme["panel"])
    panel_alt = _rgb(theme["panel_alt"])
    fg = _rgb(theme["foreground"])
    muted = _rgb(theme["muted"])
    accent = _rgb(theme["accent"])
    accent2 = _rgb(theme["accent2"])
    danger = _rgb(theme["danger"])
    name = escape(THEME_I18N[key][0])
    return f"""<svg viewBox="0 0 640 420" role="img" aria-label="{name} preview">
  <rect width="640" height="420" fill="{bg}"/>
  <rect x="28" y="28" width="584" height="364" rx="14" fill="{panel}" stroke="{panel_alt}" stroke-width="2"/>
  <rect x="54" y="54" width="134" height="20" rx="10" fill="{accent}"/>
  <rect x="54" y="102" width="302" height="28" rx="7" fill="{fg}"/>
  <rect x="54" y="146" width="236" height="16" rx="8" fill="{muted}"/>
  <rect x="54" y="204" width="360" height="112" rx="12" fill="{panel_alt}"/>
  <rect x="82" y="232" width="112" height="18" rx="9" fill="{fg}"/>
  <rect x="82" y="270" width="72" height="12" rx="6" fill="{muted}"/>
  <path d="M250 276l36 -18 28 22 42 -36 48 24" fill="none" stroke="{accent2}" stroke-width="7" stroke-linecap="round"/>
  <circle cx="520" cy="86" r="20" fill="{danger}"/>
  <rect x="462" y="204" width="92" height="24" rx="12" fill="{accent}"/>
  <rect x="462" y="246" width="72" height="16" rx="8" fill="{muted}"/>
  <rect x="462" y="280" width="106" height="16" rx="8" fill="{fg}"/>
</svg>"""


def _result_svg(example: dict[str, str], component: SceneComponent, theme: dict[str, Any]) -> str:
    bg = _rgb(theme["background"])
    panel = _rgb(theme["panel"])
    panel_alt = _rgb(theme["panel_alt"])
    fg = _rgb(theme["foreground"])
    muted = _rgb(theme["muted"])
    accent = _rgb(theme["accent"])
    accent2 = _rgb(theme["accent2"])
    danger = _rgb(theme["danger"])
    body = _result_body(example["story"], fg, muted, accent, accent2, danger, panel_alt)
    return f"""<svg viewBox="0 0 420 260" role="img" aria-label="{escape(example["title"])} result preview">
  <rect width="420" height="260" fill="{bg}"/>
  <rect x="22" y="18" width="376" height="224" rx="10" fill="{panel}" stroke="{panel_alt}"/>
  <rect x="42" y="40" width="86" height="13" rx="7" fill="{accent}"/>
  <rect x="42" y="70" width="210" height="20" rx="6" fill="{fg}"/>
  <rect x="42" y="102" width="164" height="10" rx="5" fill="{muted}"/>
  {body}
</svg>"""


def _result_body(story_key: str, fg: str, muted: str, accent: str, accent2: str, danger: str, panel_alt: str) -> str:
    if story_key == "market_radar":
        rows = []
        for idx, y in enumerate((134, 162, 190), 1):
            rows.append(f'<rect x="42" y="{y}" width="336" height="20" rx="6" fill="{panel_alt}"/>')
            rows.append(f'<rect x="58" y="{y + 7}" width="{112 + idx * 22}" height="6" rx="3" fill="{fg}"/>')
            rows.append(f'<rect x="314" y="{y + 7}" width="38" height="6" rx="3" fill="{accent2}"/>')
        return "".join(rows)
    if story_key == "product_launch":
        return (
            f'<rect x="68" y="124" width="284" height="84" rx="12" fill="{panel_alt}"/>'
            f'<circle cx="210" cy="166" r="28" fill="{accent}" opacity=".9"/>'
            f'<rect x="92" y="150" width="70" height="9" rx="5" fill="{fg}"/>'
            f'<rect x="258" y="150" width="70" height="9" rx="5" fill="{fg}"/>'
            f'<path d="M162 166h36M222 166h36" stroke="{accent2}" stroke-width="4"/>'
        )
    return (
        f'<path d="M60 150h300" stroke="{accent}" stroke-width="5"/>'
        f'<circle cx="76" cy="150" r="10" fill="{accent}"/>'
        f'<circle cx="170" cy="150" r="10" fill="{accent}"/>'
        f'<circle cx="266" cy="150" r="10" fill="{accent2}"/>'
        f'<circle cx="344" cy="150" r="10" fill="{danger}"/>'
        f'<rect x="74" y="184" width="220" height="18" rx="6" fill="{panel_alt}"/>'
        f'<rect x="92" y="190" width="124" height="6" rx="3" fill="{fg}"/>'
    )


def _rgb(value: tuple[int, int, int]) -> str:
    return f"rgb({value[0]}, {value[1]}, {value[2]})"
