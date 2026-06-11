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
- `video.motion` picks the motion grammar. `auto` maps scene families to their default motion grammar.
- Each generated scene carries a component key, visual grammar, motion grammar, bullets, metrics, proof text, source label, and duration.
- Illustration prompts, when used, should only provide atmosphere, objects, material, or background context. Exact titles, numbers, charts, citations, quotes, and conclusions should remain script or renderer output.
- The renderer creates multiple motion frames per scene from a normalized `0..1` progress value, then assembles them with ffmpeg so elements stage in with visible rhythm instead of popping on as static slides.
- Every render also writes `review_contact_sheet.jpg` in the output folder for quick visual QA.

## Audience Boundary

Internal editorial guidance must not appear in final frames, narration, captions, or audience-facing publishing copy. Template keys, component names, `visual_grammar`, `motion_grammar`, prompt notes, plate roles, renderer phases, and user-provided production guidance are authoring data only. See [`production_principles.md`](production_principles.md).

## Commands

```bash
daily-video list-templates
daily-video run --config configs/project.example.yml --demo
daily-video run --config configs/commercial.example.yml --demo
```

Use local ignored configs for real source lists and licensed BGM.
