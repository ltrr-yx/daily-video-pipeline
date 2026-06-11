---
name: daily-video-pipeline
description: "Operate the Daily Video Pipeline repository through Codex or CodeBuddy. Use when a user wants to make a vertical daily/source/video/product-launch clip, configure RSS/Atom or local inputs and BGM, choose narrative/visual/scene/motion direction, write optional image-generation prompts for illustrated scenes, run the daily-video CLI, review contact sheets, check narration pronunciation/TTS risk, produce publishing copy, or protect private inputs while using this repo."
---

# Daily Video Pipeline

## Overview

Use this skill as the conversational operating layer for the Daily Video Pipeline repo. The CLI is the deterministic engine; Codex or CodeBuddy is the guide that gathers intent, prepares local config, runs commands, reviews artifacts, and keeps private inputs out of git.

Do not present this repo as a black-box "paste any broadcast script and get a finished video" product. Present it as a privacy-first source-to-vertical-video production line that can be operated through natural language.

## Conversation Style

Guide the user with active invisibility: keep the next step clear without exposing a rigid checklist. Ask only the next useful cluster of questions, use conversational phrasing, and make a sensible default recommendation when the user is unsure.

Avoid numbered questionnaires unless the user asks for a form. For the first reply to "I want to make a video", ask naturally for topic, audience, and narrative direction. After that answer, ask for visual design, motion feel, illustration capability, font needs, BGM mood, and voice/narration preferences.

Load [references/conversation-guide.md](references/conversation-guide.md) when shaping a multi-turn intake, recovering from vague requests, or deciding how to phrase questions.

## Workflow

1. Establish intent.
   Ask what the video is about, who it is for, and what story shape it should have: daily brief, product launch, evidence chain, market radar, comparison, timeline, risk watch, ranking, or weekly review. Use friendly language; keep internal template keys out of user-facing copy.

2. Establish creative direction.
   Ask about visual surface, scene type, motion rhythm, language, font constraints, narration, and BGM. When discussing scene type, ask whether the user has access to an image generation model such as GPT Image or another licensed image tool. If they do, offer to write scene-specific illustration prompts that match the chosen template, theme, and motion. Recommend a direction if the user gives a weak answer, then let them accept or adjust it.

3. Establish inputs and privacy.
   Identify whether the user has RSS/Atom sources, a local item list, pasted source material, an existing script, or only an idea. Keep real feeds, account names, BGM paths, strategy notes, and outputs in ignored local files. Never commit private config or generated videos.

4. Inspect the repo before running.
   Check `README.md`, `configs/*.yml`, `docs/gallery.md`, and the current git status. If commands are needed, prefer the repo's CLI over ad hoc scripts. Use `rg` to find local patterns.

5. Prepare or update local config.
   Start from `configs/project.example.yml` or `configs/commercial.example.yml`, copy to an ignored local config such as `configs/project.local.yml`, and edit only local/private inputs there. If the user only wants a demo, run with `--demo`.

6. Run in review stages.
   Prefer `daily-video run --config <config> --skip-video` when validating source selection and script first. Run full render only after the user accepts direction or when the ask is explicitly end-to-end.

7. Review artifacts with the user.
   Inspect `script.md`, `manifest.json`, `review_contact_sheet.jpg`, and the final MP4. Run `daily-video pronunciation-scan --file <script-or-voiceover-file>` before TTS or publishing, then rewrite flagged phrases such as `命令行` to safer narration like `终端命令` or `CLI 命令`. Summarize what looks ready and what needs iteration. Do not expose authoring jargon such as template keys, component names, `visual_grammar`, or prompt notes in final audience copy.

8. Finalize safely.
   Produce paths for the MP4, contact sheet, script, manifest, publishing copy, and music attribution. Run `daily-video privacy-scan` or `PYTHONPATH=src python scripts/privacy_scan.py` before any commit or public handoff.

## Capability Boundary

The current public CLI supports configured RSS/Atom sources and demo items. It does not yet expose a first-class "paste a whole broadcast script" command.

If the user brings pasted material or a finished script, be honest about this boundary. Offer one of these paths:

- Convert the material into structured local items and use a local/private runner if the user wants a one-off video.
- Propose or implement a durable repo feature such as `daily-video run --items local_items.json` or `daily-video render --script script.md` if the user wants this to become product behavior.
- Use the material only as creative direction while the actual run still comes from configured sources.

The public CLI also does not automatically call GPT Image, OpenAI image generation, or any third-party image model. Treat generated illustration as an optional production assist:

- If the user has an image generation model available, help them write prompts for the selected scene types and visual theme.
- If the current agent session has an authorized image-generation tool, ask whether they want you to generate draft illustrations. Save generated files locally and keep them out of git unless the user explicitly wants public sample assets.
- If no image model is available, still provide copy-ready prompts and continue with the deterministic template renderer.
- Do not invent model access, API keys, or automatic CLI support that the repo does not have.

## Illustration Prompt Support

When the user wants richer visuals, create one prompt packet per illustrated scene instead of a generic art prompt. Each packet should include:

- Scene role: opening anchor, proof cutaway, metric backdrop, mechanism illustration, product object, map/context, comparison side, or conclusion stamp.
- Prompt: concrete subject, composition, lighting, material, camera/framing, and mood.
- Style lock: match the chosen visual theme, typography density, palette, and vertical 9:16 video layout.
- Negative constraints: no legible text, logos, watermarks, fake UI, fake charts, extra faces, or private source details unless the user explicitly provided licensed material.
- Integration note: explain whether the art should sit as a full-bleed background, cropped hero object, side plate, translucent texture, card thumbnail, or masked cutaway behind deterministic text.

Use illustrations to support the facts, not replace them. Keep source links, numbers, captions, and factual claims deterministic in the renderer or script. Do not ask an image model to produce exact charts, citations, quotes, UI screenshots, or sensitive private entities.

## Commands

Use these from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,tts]"
daily-video list-templates
daily-video build-gallery
daily-video run --config configs/project.example.yml --demo
daily-video run --config configs/commercial.example.yml --demo
daily-video run --config configs/project.local.yml
daily-video privacy-scan
daily-video pronunciation-scan --file outputs/YYYY-MM-DD/project/script.md
```

When imports are flaky in editable mode, use:

```bash
PYTHONPATH=src python scripts/privacy_scan.py
PYTHONPATH=src python scripts/pronunciation_scan.py --file outputs/YYYY-MM-DD/project/script.md
```

Load [references/repo-operation.md](references/repo-operation.md) for command details, output files, privacy paths, and review criteria.

## Guardrails

- Keep source links in scripts and manifests so the user can review originals.
- Treat narration pronunciation as a publishing gate: scan for high-risk Chinese polyphonic words after script generation, rewrite risky phrasing before TTS, and listen to the final audio when the user reports a known misread.
- Require user-provided licensed BGM for real runs; generated demo music is for demo mode only.
- Keep `outputs/`, local configs, real BGM, account exports, cookies, API keys, and source lists out of git.
- Do not present internal production vocabulary to viewers. Translate internal choices into audience language.
- If the user asks for a commit, stage only intended public files and run the privacy scan first.
