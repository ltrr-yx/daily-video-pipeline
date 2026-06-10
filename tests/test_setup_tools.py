from __future__ import annotations

from pathlib import Path

from daily_video_pipeline.setup_tools import init_project, install_skill


def test_init_project_creates_local_config(tmp_path: Path) -> None:
    template = tmp_path / "project.example.yml"
    template.write_text("project:\n  name: demo\n", encoding="utf-8")
    local_config = tmp_path / "project.local.yml"

    result = init_project(template=template, local_config=local_config)

    assert result.created
    assert local_config.read_text(encoding="utf-8") == "project:\n  name: demo\n"
    assert any(check.name == "python" for check in result.checks)


def test_install_skill_copies_repo_skill(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    source = repo_root / "skills" / "daily-video-pipeline"
    source.mkdir(parents=True)
    (source / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
    target_root = tmp_path / "skills"

    result = install_skill(repo_root=repo_root, target_root=target_root)

    assert result.installed
    assert (target_root / "daily-video-pipeline" / "SKILL.md").read_text(encoding="utf-8") == "# Skill\n"
