# Visual Design Guide

Use this when shaping promo, launch, repo-update, or template-gallery videos for the Daily Video Pipeline.

This repo is a product tool, not a generic marketing template pack. Visual design should feel like a capable production desk: clear, precise, calm, and good enough that creators trust the output.

## Physical Scene

Before choosing a theme, write one sentence:

- Who is watching?
- Where are they watching?
- What must they understand in the first two seconds?

For repo-update promo clips, the answer is usually: a creator or technical operator is watching on a phone, deciding whether this pipeline can save them manual video work.

## Color Strategy

Pick the color strategy before picking colors.

- Use restrained product color by default: cool neutral base, one action/status color, one secondary emphasis color.
- For repo-update and product clips, prefer `product_keynote` or `executive_light`.
- In `product_keynote`, use teal for sync/status and violet for timing or sequence. Do not let violet dominate the surface.
- Reserve dark themes for serious news, market dashboards, terminal-style stories, or night review.
- Do not use near-black backgrounds with large pure-white cards.
- Do not use pale gray body copy on tinted light panels. Body copy must stay deep enough to read on mobile.

## Typography

- Keep one strong sans family for product surfaces unless the brief truly needs editorial voice.
- Headline, body, and label sizes must differ by visible steps. Avoid flat type where everything looks like the same weight.
- Headline text should fit comfortably in the frame. If a long Chinese phrase wraps awkwardly, rewrite the phrase before shrinking everything.
- Avoid repeated all-caps English labels such as `VERDICT`, `SOURCE EVIDENCE`, or `VISUAL ANCHOR` in public-facing videos. Prefer natural labels like `Ready to use`, `Source evidence`, or localized Chinese labels.
- For Chinese narration, join title and body with Chinese punctuation. Avoid English periods between Chinese sentences.

## Layout

- One frame should have one dominant read: problem, mechanism, proof, or payoff.
- Use cards only when the content is a grouped object. Do not turn every piece of text into a white card.
- Cards should have modest radius, usually 8 to 12 px in source token terms. Avoid huge rounded blocks.
- Prefer tinted panels and quiet rails over stark white rectangles.
- Do not use a border plus a large soft shadow as the default card style.
- Leave room for subtitles, source labels, and the footer progress line.

## Repo-Update Promo Shape

For a short update aimed at people who make videos:

- Open with the problem they already feel.
- Show the improvement in one sentence.
- Close with who benefits and why it matters.
- Keep the spoken copy conversational. Avoid internal terms such as `visual_grammar`, `motion_grammar`, component keys, renderer internals, or template names.
- Avoid shorthand that TTS may clip or misread. Use `每天更新` instead of `日日更`; use `少一点手动调整` instead of `少手调`.

## Voice And TTS

- For short promo clips, prefer a lighter conversational Mandarin voice such as `zh-CN-XiaoxiaoNeural`.
- A small positive rate and pitch bump can help promo clips feel less heavy, for example `rate: "+6%"` and `pitch: "+2Hz"`.
- Keep spoken copy and on-screen copy roughly balanced. If a mechanism, timeline, proof, or matrix screen contains short bullets that are not spoken, add one conversational bridge sentence such as `这页就看三步：...` instead of cutting away as soon as the title/body narration ends.
- If the screen contains long dense cards, do not dump every card into narration. Shorten the cards, split the scene, or let the voice summarize the relationship between them.
- Run pronunciation scan before synthesis. If the user reports a misread, rewrite the phrase instead of trying to force the same wording.
- Listen for clipped compounds, wrong stress, and awkward title/body pauses.

## BGM

- Treat generated demo music as a render-path placeholder, not as publishing audio.
- For repo-update and product promo clips, choose licensed local music with a light corporate, technology explainer, or optimistic product-demo feel.
- Avoid alarm-like synths, horror pads, aggressive trailer hits, heavy club drops, obvious AI-generated loops, or anything that competes with Mandarin narration.
- Keep BGM under the voice. Start around `volume: 0.08` to `0.12` for narration-led clips, then raise only if the voice still feels clear.
- Add music attribution beside the generated output when the license requires it, but keep the audio file itself in an ignored local path such as `assets/bgm/`.

## Motion

- Product videos should use motion to explain state, not decorate.
- Use `soft_assembly`, `mechanism_scan`, or `verdict_lock` for repo updates.
- Motion rhythm should reveal structure first, then detail, then payoff.
- Avoid identical entrance timing on every element when the scene roles are different.

## Gallery And Templates

When changing themes, visual grammars, fonts, or renderer layout:

- Update `VISUAL_THEMES` with color strategy, contrast, density, font, type scale, text/media ratio, ornament, and emphasis guidance.
- Regenerate `docs/gallery.html` and `docs/gallery.md`.
- The gallery should show the selection dimensions: Story, Scene, Optional Illustration, Visual, Motion, and Render.
- The theme preview must show more than colors. It should communicate contrast, density, type scale, radius, and emphasis behavior.
- Use the gallery as a design QA surface. If the preview looks like generic white cards, the rendered videos probably will too.

## Final QA

- Inspect `review_contact_sheet.jpg` before sharing a video.
- Confirm body text contrast is readable at phone size.
- Check that source/footer text does not collide with the main content.
- Watch the final MP4 or at least verify its latest manifest, duration, contact sheet, and narration settings.
- Generated outputs stay out of git unless the user explicitly asks to commit them.
