# Daily Video Pipeline

A privacy-first template for turning your own daily information sources into a short vertical video with optional narration and BGM.

This repository intentionally does not include private feeds, watchlists, holdings, investment rules, account lists, or generated historical outputs. Clone it, add your own local config, and keep that config out of git.

## What It Does

- Fetches user-configured RSS/Atom sources or reads a local JSON item list.
- Selects recent items with optional keyword scoring and blocked terms.
- Writes a source-linked script packet.
- Renders a 1080x1920 MP4 from composable commercial story templates.
- Mixes local licensed BGM under narration or a silent track.
- Includes privacy, pronunciation, and publishing review gates before commit/publish.

## Commercial Template System

The public version ships with a composable direction system rather than a few fixed samples:

- 12 story templates for daily briefs, product launches, evidence chains, market radar, comparisons, timelines, risk watches, rankings, and weekly reviews.
- 30+ scene components for cover hooks, source proof, metric stacks, timeline ribbons, comparison splits, risk matrices, ledgers, product plates, and conclusion stamps.
- 6 visual themes: editorial dark, executive light, market terminal, product keynote, data magazine, and social pop.
- 6 motion grammars: soft assembly, evidence trace, product reveal, data tween, mechanism scan, and verdict lock. Use `video.motion: auto` to let scene families pick the right entrance logic.

Open the visual gallery to understand the combinations before rendering:

- [`docs/gallery.html`](docs/gallery.html) for illustrated story flows, scene module sketches, and visual skin previews.
- [`docs/gallery.md`](docs/gallery.md) for a GitHub-readable text index.
- [`docs/production_principles.md`](docs/production_principles.md) for the audience-output boundary: internal editorial guidance stays out of final frames, narration, and publishing copy.

List them locally:

```bash
daily-video list-templates
daily-video build-gallery
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,tts]"
cp configs/project.example.yml configs/project.local.yml
```

Edit `configs/project.local.yml` with your own sources and BGM path. Keep the file local.

Or let the CLI create the local config and run setup checks:

```bash
daily-video init
```

Run the safe demo:

```bash
daily-video run --config configs/project.example.yml --demo
```

Run the richer commercial-style demo:

```bash
daily-video run --config configs/commercial.example.yml --demo
```

Run with your own sources:

```bash
daily-video run --config configs/project.local.yml
```

Run with a local item list you already collected:

```bash
daily-video run --config configs/project.local.yml --items local_items.json
```

`local_items.json` uses the same shape as [`examples/demo_items.json`](examples/demo_items.json): each item has `title`, `url`, `source_name`, `published_at`, `summary`, and optional `tags`.

After rendering, run the publishing gate:

```bash
daily-video review --output outputs/YYYY-MM-DD/project-name
```

The review checks required artifacts, media metadata, pronunciation risks, stale draft files, and private terms from `.privacy-blocklist.local`. It writes `review_report.md` inside the output directory.

## Codex / CodeBuddy Skill

This repo includes a guided agent skill at [`skills/daily-video-pipeline`](skills/daily-video-pipeline). Use it when you want Codex or CodeBuddy to operate the pipeline conversationally: clarify the video topic and audience, choose story/visual/motion direction, prepare local config, run the CLI, review the contact sheet, and keep private inputs out of git.

If your agent supports repo-local skills, point it at that folder. Otherwise copy the folder into your agent's skills directory and invoke:

```bash
daily-video install-skill
```

```text
Use $daily-video-pipeline to help me make a publishable vertical video from my sources.
```

Before committing:

```bash
daily-video privacy-scan
# or: python scripts/privacy_scan.py

daily-video pronunciation-scan --file outputs/YYYY-MM-DD/project/script.md
# or: python scripts/pronunciation_scan.py --file outputs/YYYY-MM-DD/project/script.md
```

For personal source domains, topic labels, account names, or private terms you never want to leak, put one term per line in `.privacy-blocklist.local`. That file is ignored by git.

Run the pronunciation scan before TTS or publishing. It flags Chinese polyphonic words that local or online TTS voices may read incorrectly, such as `命令行` where `行` should be read as `hang2`.

## Suggested Public Structure

```text
configs/                 public examples only
examples/                demo data that is safe to commit
src/daily_video_pipeline collection, scoring, script, render, privacy scan
assets/bgm/              ignored local BGM files
outputs/                 ignored generated runs
docs/                    architecture and privacy notes
tests/                   pipeline and privacy tests
```

## Notes

- This is a publishing pipeline, not financial advice or trading automation.
- Source links are preserved in the manifest and script so users can review originals before publishing.
- BGM must be user-provided or generated in demo mode. Do not commit copyrighted audio.
- Every video run writes `review_contact_sheet.jpg` for quick visual review.
