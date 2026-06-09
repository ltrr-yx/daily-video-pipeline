# Privacy Model

This repository is designed as a clean template. It should never become a redacted copy of a private workflow.

## Rules

1. Public examples must use placeholder or demo sources.
2. Real source lists live in `configs/project.local.yml` or another ignored file.
3. Real BGM files live under `assets/bgm/` and are ignored.
4. Runtime outputs live under `outputs/` and are ignored.
5. Put personal source names, domains, account handles, topic labels, and private terms in `.privacy-blocklist.local`.
6. Run `daily-video privacy-scan` before commit.

## Why This Shape

Private daily pipelines often mix three things that should be separated before open sourcing:

- reusable mechanics: fetching, selecting, scripting, rendering, audio mixing
- personal preferences: source list, topic filters, visual taste, publish cadence
- sensitive context: accounts, portfolio exports, private notes, generated history

Only the first category belongs in this repository.
