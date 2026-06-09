from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


SENSITIVE_PATH_FRAGMENTS = (
    "holdings",
    "portfolio",
    "broker",
    "positions.csv",
    "trade_log",
    "watchlist.private",
    ".env",
)

SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|bearer[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
    re.compile(r"(?i)-----BEGIN (RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----"),
)

DEFAULT_SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "outputs",
    "reports",
    "data",
    "logs",
}

TEXT_EXTENSIONS = {
    ".cfg",
    ".css",
    ".env",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class Finding:
    path: Path
    reason: str


def load_extra_blocklist(path: Path) -> tuple[str, ...]:
    if not path.exists():
        return ()
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    return tuple(lines)


def scan_tree(root: Path, *, extra_terms: tuple[str, ...] = ()) -> list[Finding]:
    findings: list[Finding] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in DEFAULT_SKIP_DIRS for part in rel.parts):
            continue
        rel_text = rel.as_posix()
        if rel_text != ".env.example" and any(fragment in rel_text for fragment in SENSITIVE_PATH_FRAGMENTS):
            findings.append(Finding(rel, "sensitive path name"))
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(Finding(rel, f"secret-like content: {pattern.pattern[:24]}..."))
        lowered = text.lower()
        for term in extra_terms:
            if term.lower() in lowered:
                findings.append(Finding(rel, f"extra private blocklist term: {term}"))
    return findings
