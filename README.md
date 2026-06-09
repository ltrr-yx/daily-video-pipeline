# Daily Video Pipeline

A privacy-first template for turning your own daily information sources into a short vertical video with optional narration and BGM.

This repository intentionally does not include private feeds, watchlists, holdings, investment rules, account lists, or generated historical outputs. Clone it, add your own local config, and keep that config out of git.

## What It Does

- Fetches user-configured RSS/Atom sources.
- Selects recent items with optional keyword scoring and blocked terms.
- Writes a source-linked script packet.
- Renders a 1080x1920 MP4 from simple editorial scenes.
- Mixes local licensed BGM under narration or a silent track.
- Includes a privacy scan before commit/publish.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,tts]"
cp configs/project.example.yml configs/project.local.yml
```

Edit `configs/project.local.yml` with your own sources and BGM path. Keep the file local.

Run the safe demo:

```bash
daily-video run --config configs/project.example.yml --demo
```

Run with your own sources:

```bash
daily-video run --config configs/project.local.yml
```

Before committing:

```bash
daily-video privacy-scan
# or: python scripts/privacy_scan.py
```

For personal source domains, topic labels, account names, or private terms you never want to leak, put one term per line in `.privacy-blocklist.local`. That file is ignored by git.

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
