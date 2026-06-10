# Template Gallery / 模板图库

Open [`docs/gallery.html`](gallery.html) for the visual gallery.

制作视频的方向由三层决定：

- Story Template / 叙事模板：决定故事顺序。
- Scene Component / 镜头类型：决定每个画面怎么表达。
- Visual Theme / 视觉皮肤：决定颜色、质感和商业气质。

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

## Visual Themes / 视觉皮肤

- `editorial_dark` - 深色编辑部 / Editorial Dark: 适合严肃新闻、研究札记、夜间复盘。
- `executive_light` - 高管浅色 / Executive Light: 适合周报、简报、面向决策者的解释。
- `market_terminal` - 市场终端 / Market Terminal: 适合金融、KPI、市场宽度和密集数字。
- `product_keynote` - 产品发布会 / Product Keynote: 适合产品、功能、硬件和对象主视觉。
- `data_magazine` - 数据杂志 / Data Magazine: 适合图表型专题和慢一点的编辑节奏。
- `social_pop` - 社媒高能 / Social Pop: 适合榜单、轻快盘点和更鲜明的社交包装。

## Composition Examples / 组合示例

- 公开市场复盘: `market_radar` + `market_ledger` + `market_terminal` -> 市场宽度先修复，主线仍需成交验证。
- 产品发布短片: `product_launch` + `product_plate` + `product_keynote` -> 把对象、场景和验证点放进同一条短片。
- 证据链解释: `evidence_chain` + `verification_rail` + `executive_light` -> 来源、主张、验证和结论顺序清楚。
