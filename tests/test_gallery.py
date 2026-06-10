from __future__ import annotations

from daily_video_pipeline.gallery import build_gallery_html, build_gallery_markdown, write_gallery
from daily_video_pipeline.templates import SCENE_COMPONENTS, STORY_TEMPLATES, VISUAL_THEMES


def test_gallery_html_includes_registered_assets() -> None:
    html = build_gallery_html()

    for key in STORY_TEMPLATES:
        assert key in html
    for key in SCENE_COMPONENTS:
        assert key in html
    for key in VISUAL_THEMES:
        assert key in html


def test_gallery_markdown_lists_three_layers() -> None:
    markdown = build_gallery_markdown()

    assert "Story Template / 叙事模板" in markdown
    assert "Scene Component / 镜头类型" in markdown
    assert "Visual Theme / 视觉皮肤" in markdown
    assert "Composition Examples / 组合示例" in markdown


def test_write_gallery_creates_html_and_markdown(tmp_path) -> None:
    html_path, md_path = write_gallery(tmp_path)

    assert html_path.exists()
    assert md_path.exists()
    assert "三步选出视频方向" in html_path.read_text(encoding="utf-8")
    assert "# Template Gallery / 模板图库" in md_path.read_text(encoding="utf-8")
