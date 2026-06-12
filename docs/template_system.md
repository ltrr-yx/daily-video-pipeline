# Template System

The repository now uses a composable video direction model instead of a few fixed videos.

## Layers

- **Story templates** decide the narrative order. The first public set contains 12 templates such as daily briefing, product launch, market radar, evidence chain, comparison, timeline, risk watch, top five, and weekly review.
- **Scene components** decide how one screen expresses information. The registry contains 30+ components: cover hooks, source proof, metric stacks, comparison splits, timeline ribbons, mechanism x-rays, ledgers, risk matrices, rankings, product plates, and conclusion stamps.
- **Optional illustration prompts** help users who have GPT Image or another image generation model create richer background art or object plates for selected scene components. This is production guidance, not automatic CLI image generation.
- **Visual themes** decide the commercial surface. The first 6 are editorial dark, executive light, market terminal, product keynote, data magazine, and social pop.
- **Motion grammars** decide how each screen enters, assembles, emphasizes, and exits. They are registered in code so renderers follow the same structure users choose in config.

This gives users many combinations without copying whole video scripts.

## Gallery

Use the gallery when choosing a direction:

- [`gallery.html`](gallery.html) shows illustrated story template flows, scene component sketches, and visual theme previews.
- [`gallery.md`](gallery.md) lists the same registry in a GitHub-readable format.

Regenerate both files after changing the registry:

```bash
daily-video build-gallery
```

## Runtime Behavior

- `story.template` in config picks the narrative template.
- `video.theme` picks the visual skin.
- `video.motion` picks the global motion grammar. `auto` maps scene families to their default motion grammar.
- `story.motion_overrides` pins motion grammar for selected scene component keys or scene family keys. Exact component keys take priority over family keys.
- Each generated scene carries a component key, visual grammar, motion grammar, bullets, metrics, proof text, source label, and duration.
- Illustration prompts, when used, should only provide atmosphere, objects, material, or background context. Exact titles, numbers, charts, citations, quotes, and conclusions should remain script or renderer output.
- When narration subtitles are available, the renderer uses subtitle cue starts to update scene durations before frame rendering and writes `audio_timeline.json` as the timing audit trail.
- The renderer creates multiple motion frames per scene from a normalized `0..1` progress value, then assembles them with ffmpeg so elements stage in with visible rhythm instead of popping on as static slides.
- Every render also writes `review_contact_sheet.jpg` in the output folder for quick visual QA.

## Narration Timing

The timing path is built around one source of truth:

```text
scene narration + visual text load -> Edge TTS subtitle cues -> audio_timeline.json -> frame durations
```

This avoids hand-maintained timing drift between script, audio, and visuals. It also keeps the public pipeline low-cost: the default path uses subtitles produced during local TTS synthesis rather than paid cloud ASR. If a future workflow brings non-TTS audio, a local forced-alignment or Whisper-style step can produce the same subtitle/timeline input.

Before synthesis, the script writer compares the amount of visible text with the amount of spoken text. When a mechanism, timeline, proof, or matrix scene has short structural bullets that are visible but not spoken, it can add one audience-facing bridge sentence, for example `这页就看三步：生成语音、读取时间、同步画面。`. This keeps dense screens on pace with narration without forcing every card into the voiceover.

If a screen is too dense to bridge naturally, the right fix is to split the scene, shorten the visible cards, or rewrite the voiceover summary. The renderer writes a `readability` object into each synced scene in `audio_timeline.json` with estimated visual units, spoken units, visual seconds, spoken seconds, remaining gap, and any bridge sentence used.

Default config keeps the renderer forgiving:

```yaml
narration:
  timing:
    enabled: true
    strict: false
```

Use `strict: true` in production lanes when a missing or unmatchable subtitle file should fail the render instead of falling back to fixed scene durations.

## Motion Overrides

Use `story.motion_overrides` when one template needs different motion language for different scene roles:

```yaml
story:
  template: "product_launch"
  motion_overrides:
    proof: "evidence_trace"
    product: "product_reveal"
    conclusion: "verdict_lock"
```

The override key can be either a component key or a scene family key. Component keys are listed by `daily-video list-templates` and include values such as `source_proof`, `verification_rail`, `product_plate`, `conclusion_stamp`, and `cta_end`. Family keys include `proof`, `product`, `metric`, `timeline`, `mechanism`, `split`, `list`, and `stamp`; `proof` also covers proof-like rail and chip scenes, and `conclusion` is accepted as a readable alias for the `stamp` family.

Family-level overrides are useful when a whole class of scenes should share a motion grammar:

```yaml
story:
  template: "evidence_chain"
  motion_overrides:
    proof: "evidence_trace"
    mechanism: "mechanism_scan"
    conclusion: "verdict_lock"
```

For a runnable example, see [`../configs/motion-overrides.example.yml`](../configs/motion-overrides.example.yml).

## Audience Boundary

Internal editorial guidance must not appear in final frames, narration, captions, or audience-facing publishing copy. Template keys, component names, `visual_grammar`, `motion_grammar`, prompt notes, plate roles, renderer phases, and user-provided production guidance are authoring data only. See [`production_principles.md`](production_principles.md).

## Commands

```bash
daily-video list-templates
daily-video run --config configs/project.example.yml --demo
daily-video run --config configs/commercial.example.yml --demo
daily-video run --config configs/motion-overrides.example.yml --demo
```

Use local ignored configs for real source lists and licensed BGM.
