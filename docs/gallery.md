# Template Gallery / 模板图库

Open [`docs/gallery.html`](gallery.html) for the visual gallery.

制作视频的方向由四层决定：

- Story Template / 叙事模板：决定故事顺序。
- Scene Component / 镜头类型：决定每个画面怎么表达。
- Optional Illustration / 可选插图：如果用户有图片生成模型，可为部分镜头补充插图提示词。
- Visual Theme / 视觉皮肤：决定颜色、质感和商业气质。
- Motion Grammar / 出场语法：决定元素如何进入、组装、强调和退出。

设计质量检查：所有主题都必须先说明颜色策略、文字对比、信息密度、字体字号和装饰角色。不要把视觉主题简化成背景色加卡片。

## Story Templates / 叙事模板

### 每日简报 / Daily Briefing

适合 3 到 5 条公开信号的快速整理。

- Key: `daily_briefing`
- Flow: `cover_hook -> signal_grid -> source_proof -> insight_stack -> next_watch`
- 示例：早间 AI 新闻、公开市场雷达、行业日报。

### 单事件深讲 / Single Event Deep Dive

适合把一个事件讲清楚：背景、机制、证据、结论。

- Key: `single_event_deep_dive`
- Flow: `cover_hook -> context_panel -> mechanism_xray -> evidence_quote -> conclusion_stamp`
- 示例：新品发布、政策变化、研究结果。

### 突发更新 / Breaking Update

适合短时间内说明一个新事实和下一步验证。

- Key: `breaking_update`
- Flow: `impact_headline -> source_proof -> proof_chips -> next_watch`
- 示例：官方公告、临时更新、盘中快讯。

### 产品发布 / Product Launch

适合说明产品是什么、解决谁的问题、工作流如何改变。

- Key: `product_launch`
- Flow: `product_plate -> before_after_surface -> use_case_grid -> verification_rail -> cta_end`
- 示例：工具上线、硬件发布、功能改版。

### 公司动态 / Company Update

适合围绕一个主体讲动作、证据、指标和风险。

- Key: `company_update`
- Flow: `entity_map -> source_proof -> metric_stack -> risk_matrix -> next_watch`
- 示例：公司公告、融资、合作、财报摘要。

### 市场雷达 / Market Radar

适合把多组指标放在同一张冷静的信息板上。

- Key: `market_radar`
- Flow: `market_ledger -> pulse_monitor -> signal_grid -> risk_matrix -> conclusion_stamp`
- 示例：市场宽度、行业强弱、资金与风险信号。

### 证据链 / Evidence Chain

适合从来源、主张、验证路径一路讲到可信结论。

- Key: `evidence_chain`
- Flow: `verification_rail -> source_proof -> evidence_quote -> mechanism_xray -> conclusion_stamp`
- 示例：传闻核验、模型评测、信息源复查。

### 横向比较 / Comparison

适合比较两个工具、公司、方案或信号。

- Key: `comparison`
- Flow: `compare_split -> metric_stack -> before_after_surface -> conclusion_stamp`
- 示例：A/B 产品对比、两类资产对比。

### 时间线 / Timeline

适合讲一个过程怎样一步步演化。

- Key: `timeline`
- Flow: `timeline_ribbon -> milestone_stack -> source_proof -> next_watch`
- 示例：版本发布、政策进程、研究到产品。

### 风险观察 / Risk Watch

适合把机会、不确定性、反证和检查点拆开。

- Key: `risk_watch`
- Flow: `risk_matrix -> verification_rail -> proof_chips -> next_watch`
- 示例：主题过热、数据冲突、风险提示。

### 榜单盘点 / Top Five

适合做每日或每周 Top 列表，强调排序与证据。

- Key: `top_five`
- Flow: `ranking_board -> source_proof -> metric_stack -> cta_end`
- 示例：五条新闻、五个产品、五个信号。

### 周度复盘 / Weekly Review

适合把一周的主题、变化和下周观察收束在一起。

- Key: `weekly_review`
- Flow: `week_calendar -> signal_grid -> market_ledger -> conclusion_stamp -> next_watch`
- 示例：周末总结、周一视频选题、周报。

## Scene Components / 镜头类型

### 开场与冲击 / Opening and impact

- `cover_hook` - 开场钩子 / Cover Hook: 一句强判断建立观看理由。 Visual grammar: `cinematic_anchor`.
- `impact_headline` - 冲击标题 / Impact Headline: 把刚发生的变化放到第一视觉层。 Visual grammar: `cinematic_anchor`.

### 背景与洞察 / Context and insight

- `context_panel` - 背景面板 / Context Panel: 先框定故事发生的上下文。 Visual grammar: `runtime_lens`.
- `insight_stack` - 洞察堆栈 / Insight Stack: 把几条判断叠成一个清晰观点。 Visual grammar: `signal_board`.

### 多信号组织 / Signal groups

- `signal_grid` - 信号网格 / Signal Grid: 并列展示多条弱信号，不强行讲因果。 Visual grammar: `signal_board`.
- `use_case_grid` - 场景网格 / Use Case Grid: 展示产品能进入哪些使用场景。 Visual grammar: `official_product_plate`.
- `three_takeaways` - 三点总结 / Three Takeaways: 把结论压成三条可记住的信息。 Visual grammar: `signal_board`.

### 数字与图表 / Numbers and charts

- `metric_stack` - 指标堆栈 / Metric Stack: 纵向堆叠数字和短标签。 Visual grammar: `market_ledger`.
- `big_number` - 大数字 / Big Number: 让一个关键数字成为画面主角。 Visual grammar: `data_on_plate`.
- `mini_chart` - 迷你图表 / Mini Chart: 用小趋势线表达变化方向。 Visual grammar: `data_on_plate`.
- `pulse_monitor` - 脉冲监测 / Pulse Monitor: 表达状态、节奏和压力变化。 Visual grammar: `data_on_plate`.

### 账本与表格 / Ledgers and tables

- `market_ledger` - 市场账本 / Market Ledger: 用行项目承载密集指标。 Visual grammar: `market_ledger`.
- `data_table` - 数据表 / Data Table: 用列结构展示更规整的数据。 Visual grammar: `market_ledger`.

### 来源证明 / Source proof

- `source_proof` - 来源证明 / Source Proof: 突出原始来源、日期和证据线。 Visual grammar: `verification_rail`.
- `evidence_quote` - 证据摘句 / Evidence Quote: 把一条关键证据做成引用板。 Visual grammar: `verification_rail`.

### 证据标签 / Proof chips

- `proof_chips` - 证据标签 / Proof Chips: 压缩来源、日期、标签和可信度。 Visual grammar: `verification_rail`.

### 验证轨道 / Validation rails

- `verification_rail` - 验证轨道 / Verification Rail: 沿多个检查点推进可信度。 Visual grammar: `verification_rail`.

### 时间结构 / Timelines

- `timeline_ribbon` - 时间丝带 / Timeline Ribbon: 沿一条轨道展示阶段。 Visual grammar: `timeline_ribbon`.
- `milestone_stack` - 里程碑堆叠 / Milestone Stack: 把阶段卡片纵向推进。 Visual grammar: `timeline_ribbon`.
- `week_calendar` - 周历 / Week Calendar: 按一周节奏总结信号。 Visual grammar: `timeline_ribbon`.

### 机制解释 / Mechanisms

- `mechanism_xray` - 机制透视 / Mechanism X-Ray: 拆开输入、机制和结果。 Visual grammar: `mechanism_xray`.
- `stack_layers` - 层级堆叠 / Stack Layers: 用层叠关系说明系统构成。 Visual grammar: `mechanism_xray`.
- `funnel` - 漏斗 / Funnel: 把多输入收敛到一个结果。 Visual grammar: `mechanism_xray`.

### 对比结构 / Comparisons

- `compare_split` - 对比分屏 / Compare Split: 左右并置比较两个对象。 Visual grammar: `before_after_surface`.
- `before_after_surface` - 前后对照 / Before After: 把旧状态和新状态并列出来。 Visual grammar: `before_after_surface`.

### 风险结构 / Risk matrices

- `risk_matrix` - 风险矩阵 / Risk Matrix: 拆开上行、下行、未知和验证。 Visual grammar: `verification_rail`.

### 排名结构 / Rankings

- `ranking_board` - 排名板 / Ranking Board: 用排序展示列表型内容。 Visual grammar: `market_ledger`.

### 观察清单 / Watch lists

- `watchlist` - 观察清单 / Watchlist: 列出接下来要看的对象。 Visual grammar: `signal_board`.
- `next_watch` - 下一步观察 / Next Watch: 用明确检查点收尾。 Visual grammar: `signal_board`.

### 主体与地图 / Entity maps

- `entity_map` - 主体关系图 / Entity Map: 展示谁和谁相关。 Visual grammar: `runtime_lens`.
- `geographic_map` - 地域图 / Geographic Map: 把事件放到区域或地理语境里。 Visual grammar: `runtime_lens`.

### 产品展示 / Product plates

- `product_plate` - 产品主视觉 / Product Plate: 给产品或对象一个高级展示位。 Visual grammar: `official_product_plate`.

### 结论收束 / Conclusions

- `conclusion_stamp` - 结论印章 / Conclusion Stamp: 把最后判断落得很清楚。 Visual grammar: `market_ledger`.
- `cta_end` - 行动收尾 / CTA End: 引导下一步查看、复盘或订阅。 Visual grammar: `cinematic_anchor`.

## Optional Illustration / 可选插图

如果用户有 GPT Image 或其他图片生成模型，可以把插图当作可选生产素材；事实、数字、来源和最终文字仍由脚本与渲染器确定。

### 开场主视觉 / Hero anchor

- Scene: `cover_hook` - 开场钩子 / Cover Hook
- Fit: 用一张有气氛的竖版插图先建立对象、场景和情绪，标题、日期和来源仍由渲染器叠加。
- Prompt role: 9:16 cinematic editorial hero background, one clear subject, strong negative space, no text.
- Integration: Full-bleed background or masked hero object behind the deterministic hook text.

### 证据切片 / Evidence cutaway

- Scene: `source_proof` - 来源证明 / Source Proof
- Fit: 把来源证明做得更像真实审稿桌面或资料切片，但引用、日期和链接不要让生图模型绘制。
- Prompt role: abstract research desk, paper stack, verification marks, soft depth of field, no readable words.
- Integration: Small side plate or translucent cutaway beside source labels rendered by code.

### 指标氛围 / Metric atmosphere

- Scene: `metric_stack` - 指标堆栈 / Metric Stack
- Fit: 为数字镜头增加材质、空间和行业暗示，让密集数据不显得像裸表格。
- Prompt role: premium data-room backdrop, luminous abstract bars, finance or product context, no exact chart labels.
- Integration: Low-contrast backdrop; exact numbers, charts, and captions stay deterministic.

### 机制透视 / Mechanism x-ray

- Scene: `mechanism_xray` - 机制透视 / Mechanism X-Ray
- Fit: 把抽象过程画成分层结构，帮助观众理解输入、机制和结果之间的关系。
- Prompt role: clean layered x-ray cutaway of a system, translucent materials, arrows implied by composition, no text.
- Integration: Masked center illustration with code-rendered labels and connector lines on top.

### 产品物件 / Product object

- Scene: `product_plate` - 产品主视觉 / Product Plate
- Fit: 在产品发布或功能说明里给对象一个更高级的材质镜头，减少纯文字发布会感。
- Prompt role: minimal premium product render on a clean stage, soft reflections, accurate object mood, no fake UI.
- Integration: Cropped object plate with callouts, proof chips, and CTA rendered separately.

### 对比世界 / Comparison worlds

- Scene: `compare_split` - 对比分屏 / Compare Split
- Fit: 让左右两侧拥有不同色温、材质或空间隐喻，帮助观众一眼读出前后或 A/B 差异。
- Prompt role: two contrasting vertical environments divided clearly, old versus new mood, no text or icons.
- Integration: Split background; deterministic labels and comparison metrics sit above both halves.

### 结论符号 / Verdict symbol

- Scene: `conclusion_stamp` - 结论印章 / Conclusion Stamp
- Fit: 用一个象征性收束画面强化记忆点，但不让模型生成最终判断文字。
- Prompt role: symbolic final checkpoint, sealed decision object, premium editorial lighting, no words.
- Integration: Dimmed end-card background behind the final watch item or verdict stamp.

## Visual Themes / 视觉皮肤

- `editorial_dark` - 深色编辑部 / Editorial Dark: 适合严肃新闻、研究札记、夜间复盘。
  - Type: Noto Serif SC / Source Han Serif SC + Georgia / New York
  - Scale: 标题 72 / 正文 40 / 标签 24
  - Text/media: 文字 64% / 画面 36%
  - Color: Dark restrained: ink field, warm proof accent, teal source status.
  - Contrast: High contrast for body text; muted copy stays green-gray, never pale gray.
  - Density: Editorial, spacious, one source-backed idea per frame.
  - Ornament: 青绿色小色块，配少量金色证据点。
  - Emphasis: 只给关键判断加一条短强调线。
- `executive_light` - 高管浅色 / Executive Light: 适合周报、简报、面向决策者的解释。
  - Type: Noto Sans SC / Source Han Sans SC + SF Pro / Helvetica Neue
  - Scale: 标题 66 / 正文 37 / 标签 24
  - Text/media: 文字 56% / 画面 44%
  - Color: Restrained: cool neutral surface, blue actions, ochre confirmation.
  - Contrast: AA-first dark text on cool light surfaces; secondary copy stays above muted-gray washout.
  - Density: Boardroom brief, readable at a glance.
  - Ornament: 克制蓝色标签，配少量金色确认点。
  - Emphasis: 只在结论行下方放一条细蓝线。
- `market_terminal` - 市场终端 / Market Terminal: 适合金融、KPI、市场宽度和密集数字。
  - Type: Noto Sans Mono CJK SC / Sarasa Gothic SC + SF Mono / Menlo
  - Scale: 标题 60 / 正文 34 / 标签 22
  - Text/media: 文字 48% / 画面 52%
  - Color: Terminal-native: dark field, green state, yellow exception.
  - Contrast: Bright data on dark panels with muted labels kept legible.
  - Density: Dense data, compact labels, short holds.
  - Ornament: 终端括号、状态点和紧凑数据轨。
  - Emphasis: 用绿色指标轨强调正在变化的数值。
- `product_keynote` - 产品发布会 / Product Keynote: 适合产品、功能、硬件和对象主视觉。
  - Type: Noto Sans SC / HarmonyOS Sans SC + SF Pro / Helvetica Neue
  - Scale: 标题 76 / 正文 39 / 标签 24
  - Text/media: 文字 50% / 画面 50%
  - Color: Restrained product: cool neutral base, teal status, violet timing accent.
  - Contrast: Deep ink headlines and darker muted copy on tinted panels; no white-card glare.
  - Density: Launch update, three clean reads, one mechanism per frame.
  - Ornament: 青绿色状态标签，配紫色时间轨和少量复查点。
  - Emphasis: 只有功能名或时间轴需要强调时使用短紫线。
- `data_magazine` - 数据杂志 / Data Magazine: 适合图表型专题和慢一点的编辑节奏。
  - Type: Noto Serif SC / Source Han Serif SC + Georgia / Source Serif
  - Scale: 标题 70 / 正文 37 / 标签 23
  - Text/media: 文字 58% / 画面 42%
  - Color: Neutral data page with teal evidence and rust editorial emphasis.
  - Contrast: Ink-forward copy, restrained warm accent, no beige page wash.
  - Density: Measured editorial, chart-forward, slower read.
  - Ornament: 杂志页码、暖色小标签和图表注释。
  - Emphasis: 用赭色线条强调一条证据短语。
- `social_pop` - 社媒高能 / Social Pop: 适合榜单、轻快盘点和更鲜明的社交包装。
  - Type: Noto Sans SC Black / Source Han Sans Heavy + Arial Black / Helvetica Neue
  - Scale: 标题 78 / 正文 40 / 标签 26
  - Text/media: 文字 50% / 画面 50%
  - Color: Full palette: dark violet base, yellow hook, cyan motion, pink risk.
  - Contrast: Large high-contrast text with muted copy kept bright enough for mobile.
  - Density: High-energy social, short captions, bold labels.
  - Ornament: 高饱和贴纸标签和强数字标记。
  - Emphasis: 用荧光笔式下划线强调情绪钩子。

## Motion Grammars / 出场语法

- `soft_assembly` - Soft Assembly: A calm commercial default: shell first, title second, cards or proof details stagger into a readable hold.
  - Default families: cover, context, grid
  - Entrance: soft fade with a small upward settle
  - Emphasis: staggered content assembly
  - Exit: short fade-through
- `evidence_trace` - Evidence Trace: Proof-oriented motion: draw the rail or path first, then reveal stops, labels, and evidence cards in sequence.
  - Default families: proof, chips, rail, timeline
  - Entrance: rail draw-on before nodes
  - Emphasis: node and card stagger
  - Exit: source line holds before fade-through
- `product_reveal` - Product Reveal: A product or object gets a premium reveal with a soft plate entrance, light camera push, and restrained callouts.
  - Default families: product, map
  - Entrance: matte-like plate reveal with gentle scale
  - Emphasis: callout pins after the anchor is visible
  - Exit: slow push into the final product read
- `data_tween` - Data Tween: Numbers, rows, and tiny charts animate as evidence changes rather than appearing as static slides.
  - Default families: metric, ledger, ranking
  - Entrance: metric rows stagger in
  - Emphasis: value and sparkline fill
  - Exit: final values hold long enough to read
- `mechanism_scan` - Mechanism Scan: Layered explanations reveal structure before claims, then use a scan or connector pass to show causality.
  - Default families: mechanism, split, matrix
  - Entrance: layer peel or split reveal
  - Emphasis: focus rail, divider, or scan pass
  - Exit: consequence layer settles last
- `verdict_lock` - Verdict Lock: Conclusion motion compresses supporting details into a final practical watch item or verdict.
  - Default families: list, stamp
  - Entrance: verdict plate enters after the setup
  - Emphasis: supporting checks stagger below
  - Exit: final stamp hold

## Composition Examples / 组合示例

### 公开市场复盘 / Market recap

- Story: `market_radar`
- Scene: `market_ledger`
- Visual: `market_terminal`
- Result frames: 01 市场账本, 02 强弱结构, 03 验证轨道, 04 结论收束

### 产品发布短片 / Product launch

- Story: `product_launch`
- Scene: `product_plate`
- Visual: `product_keynote`
- Result frames: 01 产品主视觉, 02 使用场景, 03 前后对照, 04 行动收尾

### 证据链解释 / Evidence explainer

- Story: `evidence_chain`
- Scene: `verification_rail`
- Visual: `executive_light`
- Result frames: 01 来源证明, 02 证据摘句, 03 验证路径, 04 机制解释

