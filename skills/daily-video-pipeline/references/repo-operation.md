# Repo Operation

## Truth Sources

Inspect these before acting:

- `README.md` for public usage and quick start.
- `configs/project.example.yml` and `configs/commercial.example.yml` for safe config shape.
- `docs/gallery.md` or `docs/gallery.html` for available templates, themes, and motion options.
- `docs/privacy.md` and `docs/architecture.md` for public/private boundaries.
- `src/daily_video_pipeline/cli.py` for supported commands.

## Local Setup

Use the repo's normal commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,tts]"
```

If the environment already has `.venv`, do not recreate it unless it is broken.

## Config Setup

For real user work:

```bash
cp configs/project.example.yml configs/project.local.yml
```

Edit local config only. Keep these private:

- real RSS/Atom URLs
- account names and source labels
- private topic filters, watchlists, strategy notes, holdings, or customer lists
- local BGM file paths
- output videos, frames, logs, and captions

## Run Modes

Demo:

```bash
daily-video run --config configs/project.example.yml --demo
daily-video run --config configs/commercial.example.yml --demo
```

Real run:

```bash
daily-video run --config configs/project.local.yml
```

Script/manifest review before rendering:

```bash
daily-video run --config configs/project.local.yml --skip-video
```

JSON paths for downstream automation:

```bash
daily-video run --config configs/project.local.yml --json
```

## Output Review

A completed run should produce:

- `manifest.json`
- `script.md`
- `daily-video.mp4`
- `review_contact_sheet.jpg`
- narration/audio artifacts when enabled

Review for:

- source links preserved
- title and body text fitting the frame
- no internal authoring jargon visible to viewers
- no known TTS-prone polyphonic words left in the narration
- BGM licensed and not committed
- narration clear and aligned with video duration
- contact sheet suitable for quick human review

## Pronunciation Scan

Before TTS or publishing, scan the narration/script for Chinese polyphonic words that are often misread by TTS:

```bash
daily-video pronunciation-scan --file outputs/YYYY-MM-DD/project/script.md
```

Fallback:

```bash
PYTHONPATH=src python scripts/pronunciation_scan.py --file outputs/YYYY-MM-DD/project/script.md
```

If the scan flags a phrase, rewrite the spoken copy instead of relying on the TTS voice to infer pronunciation. Example: replace `命令行` with `终端命令` or `CLI 命令` in narration when the intended reading is `命令 hang`.

## Privacy Scan

Before public commits or handoff:

```bash
daily-video privacy-scan
```

Fallback:

```bash
PYTHONPATH=src python scripts/privacy_scan.py
```

If the scan fails, fix the leak instead of broadening the allowlist. Add personal terms to `.privacy-blocklist.local` when the user names sensitive sources, accounts, topic labels, holdings, or strategy terms.

## Pasted Broadcast Content

The current CLI does not expose a dedicated pasted-script path. If the user brings an already-written broadcast:

1. Explain that the public CLI is source/config driven.
2. Offer to convert the content into structured local items for a private one-off run.
3. If they want durable behavior, propose adding a public feature such as `--items local_items.json` or `render --script script.md`.
4. Do not silently fake support for a mode the CLI does not have.
