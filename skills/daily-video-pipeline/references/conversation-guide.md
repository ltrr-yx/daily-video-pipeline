# Conversation Guide

## Active Invisibility

Guide without making the user feel they are filling out a form. Ask the smallest useful set of questions, confirm what you understood, and recommend a default when the user is vague.

Do not say "Question 1, question 2, question 3" unless the user asks for a checklist. Speak like a producer sitting next to the user.

## First Turn

If the user says "I want to make a video", start with topic, audience, and story shape:

> Sounds good. What is this video mainly about, and who should feel it was made for? Also, do you want it to feel more like a fast daily brief, a product launch, a proof/evidence story, or a deeper explainer?

If the user already gives a topic but not the audience:

> I get the topic. Who are we trying to convince or help with this one: existing followers, potential users, investors, internal teammates, or a broader short-video audience?

If the user gives only an audience:

> Great, then let's anchor the message. What should this audience understand, believe, or do after watching?

## Second Turn

After topic, audience, and story shape are clear, ask for creative direction:

> I have enough to choose a story structure. For the visual side, do you want this to feel more editorial and serious, product-keynote clean, data-heavy, or social and punchy? Also, do you have access to an image generation model such as GPT Image? If yes, I can write scene-by-scene illustration prompts; if not, I will keep it fully template-rendered. Should the motion feel calm and premium, evidence-tracing, or fast reveal?

Ask about BGM and voice as production choices, not as technical settings:

> For sound, should the music sit quietly under narration, feel energetic, or stay minimal? If you have a licensed local BGM file, point me to it; otherwise I can render a demo-only bed and mark it as not for publishing.

## Mapping User Language Internally

Use user-facing words in conversation, then map them internally:

- "daily news", "today's recap", "morning brief" -> `daily_briefing`
- "launch", "repo announcement", "show the product" -> `product_launch`
- "prove this", "source-backed", "verification" -> `evidence_chain`
- "market scan", "radar", "what moved" -> `market_radar`
- "A vs B", "before/after" -> `comparison`
- "how it unfolded" -> `timeline`
- "what could go wrong" -> `risk_watch`
- "top items" -> `top_five`
- "weekly synthesis" -> `weekly_review`

For visual tone:

- serious premium -> `editorial_dark` or `executive_light`
- product demo -> `product_keynote`
- charts and metrics -> `data_magazine` or `market_terminal`
- more social -> `social_pop`

For generated illustration use:

- opening anchor -> full-bleed or cropped hero illustration behind deterministic title text
- proof/evidence -> abstract source desk, document cutaway, or verification still; keep citations as renderer text
- metric/data -> atmospheric backdrop or small thematic object; keep numbers and charts deterministic
- mechanism/process -> layered cutaway, x-ray metaphor, or system diagram background
- product/object -> clean hero object or material render; avoid fake UI unless the user provides licensed screenshots
- map/context -> regional texture, city/industry context, or entity network backdrop
- comparison -> two visual worlds separated by a clear divider
- conclusion -> symbolic stamp, checkpoint, or final watch-object background

For motion:

- calm premium -> `soft_assembly`
- source/evidence -> `evidence_trace`
- product reveal -> `product_reveal`
- data movement -> `data_tween`
- system/process explanation -> `mechanism_scan`
- final verdict -> `verdict_lock`

## Review Language

When showing review results, speak in finished-video terms:

- "The opening hook is clear."
- "The source proof needs a stronger visible citation."
- "The BGM is too prominent under narration."
- "This line feels like internal tool language; I will rewrite it for viewers."

Avoid saying:

- "The component registry picked `source_proof`."
- "The visual grammar is leaking."
- "The prompt notes are visible."

When offering image prompts, make it clear that they are production prompts, not final audience copy. A concise handoff can look like:

> If you can generate images, I will give you three prompts: a 9:16 opening hero, one mechanism cutaway, and one conclusion background. The video text, source labels, and numbers will stay in the renderer so the art does not need to draw exact words or charts.

## When the User Is Unsure

Choose a default and explain it briefly:

> Since this is for a public repo launch, I would use a product-launch structure, product-keynote visuals, calm premium motion, Chinese narration, and a quiet licensed BGM bed. That gives it a commercial launch feel without turning it into an ad that overpromises.

If the user is unsure about image generation, default to no generated art:

> We can keep this template-rendered first. If you later have GPT Image or another image model available, I can add prompt packets for the opening, mechanism, and ending scenes without changing the factual script.
