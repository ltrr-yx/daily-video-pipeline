from __future__ import annotations

from dataclasses import asdict, dataclass, field
import shutil
import sys
from pathlib import Path


@dataclass(frozen=True)
class SetupCheck:
    name: str
    ok: bool
    message: str


@dataclass(frozen=True)
class InitResult:
    local_config: str
    created: bool
    checks: tuple[SetupCheck, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {
            "local_config": self.local_config,
            "created": self.created,
            "checks": [asdict(check) for check in self.checks],
        }


@dataclass(frozen=True)
class SkillInstallResult:
    source: str
    destination: str
    installed: bool
    message: str

    def to_dict(self) -> dict:
        return asdict(self)


def init_project(
    *,
    template: str | Path = "configs/project.example.yml",
    local_config: str | Path = "configs/project.local.yml",
    force: bool = False,
) -> InitResult:
    template_path = Path(template).resolve()
    local_path = Path(local_config).resolve()
    if not template_path.exists():
        raise FileNotFoundError(f"template config not found: {template_path}")
    created = False
    if local_path.exists() and not force:
        created = False
    else:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(template_path, local_path)
        created = True
    return InitResult(str(local_path), created, tuple(run_setup_checks()))


def install_skill(
    *,
    repo_root: str | Path,
    target_root: str | Path | None = None,
    force: bool = False,
) -> SkillInstallResult:
    repo = Path(repo_root).resolve()
    source = repo / "skills" / "daily-video-pipeline"
    if target_root is None:
        target_root = Path.home() / ".codex" / "skills"
    target = Path(target_root).expanduser().resolve() / "daily-video-pipeline"
    if not source.exists():
        raise FileNotFoundError(f"skill source not found: {source}")
    if target.exists() and not force:
        return SkillInstallResult(str(source), str(target), False, "skill already exists; pass --force to refresh it")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=force)
    return SkillInstallResult(str(source), str(target), True, "skill installed")


def run_setup_checks() -> list[SetupCheck]:
    checks = [
        SetupCheck("python", sys.version_info >= (3, 10), f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
        SetupCheck("ffmpeg", bool(shutil.which("ffmpeg")), shutil.which("ffmpeg") or "not found"),
        SetupCheck("ffprobe", bool(shutil.which("ffprobe")), shutil.which("ffprobe") or "not found"),
    ]
    return checks
