# Architecture

The public project keeps the reusable mechanism and moves private judgment into local ignored files.

```mermaid
flowchart LR
  A["configs/project.local.yml"] --> B["fetch RSS/Atom sources"]
  B --> C["dedupe and score recent items"]
  C --> D["script scenes and source manifest"]
  D --> E["Pillow frame render"]
  E --> F["ffmpeg video assembly"]
  G["local BGM or demo tone"] --> H["audio mix"]
  I["optional narration"] --> H
  H --> F
  F --> J["outputs/YYYY-MM-DD/project/daily-video.mp4"]
```

## Public Boundary

Keep in source control:

- generic collection adapters
- example configuration with disabled placeholder sources
- demo items with fake domains
- video rendering code
- privacy scan tooling
- docs and tests

Keep local only:

- real source lists and account names
- private source domains
- personal topic filters and watchlists
- portfolio or account exports
- private strategy notes
- generated reports, videos, frames, captions, and logs
- API tokens and cookies

## Extension Points

- Add new source adapters in `src/daily_video_pipeline/fetchers.py`.
- Add selection logic in `src/daily_video_pipeline/selection.py`.
- Add templates in `src/daily_video_pipeline/script_writer.py` or `renderer.py`.
- Add personal publish steps in a separate ignored local script.
