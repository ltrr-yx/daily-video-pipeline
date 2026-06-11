# Daily Video Pipeline CLI Smoke Test

This is the command path I would try as a user after downloading the repo.

## Prerequisites

On macOS:

```bash
brew install ffmpeg
python3 --version
```

The project expects Python 3.10+ and `ffmpeg` on `PATH`.

## Install

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ".[tts]"
```

If the editable install in the README fails to expose `daily_video_pipeline`
in your environment, use the non-editable install above.

## See Available Story Styles

```bash
source .venv/bin/activate
daily-video list-templates
```

## Render The Built-In Demo

The intended command is:

```bash
source .venv/bin/activate
daily-video run --config configs/project.example.yml --demo
```

In the current local terminal, the packaged command could not locate
`examples/demo_items.json` after non-editable install. This source-checkout
command worked:

```bash
source .venv/bin/activate
PYTHONPATH=src daily-video run --config configs/project.example.yml --demo
```

## Fast Local Preview

For a short preview, create a local config such as
`configs/cli-smoke.local.yml` with a short template:

```yaml
project:
  name: "CLI Smoke Demo"
  language: "zh-CN"
  timezone: "Asia/Shanghai"
  output_dir: "outputs"

selection:
  max_items: 3
  freshness_hours: 168
  keywords: ["workflow", "data", "audio", "video"]

story:
  template: "breaking_update"
  seconds_per_scene: 1

privacy:
  blocked_terms: []

video:
  width: 1080
  height: 1920
  fps: 30
  theme: "social_pop"
  motion: "auto"
  seconds_per_scene: 1
  font_path: ""

narration:
  enabled: false
  engine: "auto"
  voice: "zh-CN-YunyangNeural"

music:
  path: ""
  volume: 0.18
  generate_demo_bgm_if_missing: true

sources:
  - name: "Example RSS feed"
    type: "rss"
    url: "https://example.com/feed.xml"
    enabled: false
    priority: 1.0
    tags: ["example"]
```

Then run:

```bash
source .venv/bin/activate
PYTHONPATH=src daily-video run \
  --config configs/cli-smoke.local.yml \
  --demo \
  --date 2026-06-10 \
  --json
```

Open the result:

```bash
open outputs/2026-06-10/cli-smoke-demo/daily-video.mp4
open outputs/2026-06-10/cli-smoke-demo/review_contact_sheet.jpg
```

## Actual Result From This Run

The smoke command generated:

- `outputs/2026-06-10/cli-smoke-demo/daily-video.mp4`
- `outputs/2026-06-10/cli-smoke-demo/review_contact_sheet.jpg`
- `outputs/2026-06-10/cli-smoke-demo/script.md`
- `outputs/2026-06-10/cli-smoke-demo/manifest.json`

`ffprobe` reported a 1080x1920 H.264/AAC video at 30 fps with duration
`9.612993` seconds.

## Current CLI Gaps Found

- `pip install -e ".[dev,tts]"` reported success in this terminal, but the
  console script still raised `ModuleNotFoundError: No module named
  'daily_video_pipeline'`.
- `pip install ".[tts]"` fixed imports, but `daily-video run --demo` looked
  for `examples/demo_items.json` under `.venv/lib/python3.13/`, so packaged
  demo lookup is not robust.
- The CLI does not currently accept an arbitrary narration script as direct
  input. It generates `script.md` from configured sources or the built-in demo
  items.
