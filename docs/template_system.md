# Template System

The repository now uses a composable video direction model instead of a few fixed videos.

## Layers

- **Story templates** decide the narrative order. The first public set contains 12 templates such as daily briefing, product launch, market radar, evidence chain, comparison, timeline, risk watch, top five, and weekly review.
- **Scene components** decide how one screen expresses information. The registry contains 30+ components: cover hooks, source proof, metric stacks, comparison splits, timeline ribbons, mechanism x-rays, ledgers, risk matrices, rankings, product plates, and conclusion stamps.
- **Visual themes** decide the commercial surface. The first 6 are editorial dark, executive light, market terminal, product keynote, data magazine, and social pop.

This gives users many combinations without copying whole video scripts.

## Runtime Behavior

- `story.template` in config picks the narrative template.
- `video.theme` picks the visual skin.
- Each generated scene carries a component key, visual grammar, bullets, metrics, proof text, source label, and duration.
- The renderer creates multiple beat frames per scene, then assembles them with ffmpeg so each scene has a visible rhythm instead of a single static slide.
- Every render also writes `review_contact_sheet.jpg` in the output folder for quick visual QA.

## Commands

```bash
daily-video list-templates
daily-video run --config configs/project.example.yml --demo
daily-video run --config configs/commercial.example.yml --demo
```

Use local ignored configs for real source lists and licensed BGM.
