from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class PronunciationRule:
    term: str
    expected: str
    reason: str
    suggestion: str


@dataclass(frozen=True)
class PronunciationFinding:
    term: str
    expected: str
    reason: str
    suggestion: str
    line: int
    column: int
    path: str = "<text>"

    def to_dict(self) -> dict[str, str | int]:
        return asdict(self)


DEFAULT_RULES: tuple[PronunciationRule, ...] = (
    PronunciationRule(
        term="命令行",
        expected="命令行：行读 hang2",
        reason="Some Chinese TTS voices read 行 as xing2 in this technical phrase.",
        suggestion="For narration, rewrite as 终端命令 or CLI 命令 before synthesis.",
    ),
    PronunciationRule(
        term="数据行",
        expected="数据行：行读 hang2",
        reason="Table or dataset row contexts can be misread as xing2.",
        suggestion="For narration, rewrite as 数据里的这一行 or 表格行 if needed.",
    ),
    PronunciationRule(
        term="表格行",
        expected="表格行：行读 hang2",
        reason="Table row contexts can be misread as xing2.",
        suggestion="For narration, rewrite as 表格里的这一行 if needed.",
    ),
    PronunciationRule(
        term="多行",
        expected="多行：行读 hang2",
        reason="Layout/code row contexts can be misread as xing2.",
        suggestion="For narration, rewrite as 多排 or 多个文本行 if needed.",
    ),
    PronunciationRule(
        term="日日更",
        expected="日日更：建议改说 每天更新",
        reason="This shorthand can sound clipped, heavy, or collapse in TTS pacing.",
        suggestion="For narration, rewrite as 每天更新 or 天天更新.",
    ),
    PronunciationRule(
        term="单行",
        expected="单行：行读 hang2",
        reason="Layout/code row contexts can be misread as xing2.",
        suggestion="For narration, rewrite as 一行文本 if needed.",
    ),
    PronunciationRule(
        term="重复",
        expected="重复：重读 chong2",
        reason="重 is a common polyphonic character in narration.",
        suggestion="If a TTS voice misreads it, rewrite as 反复 or 再做一遍.",
    ),
    PronunciationRule(
        term="重排",
        expected="重排：重读 chong2",
        reason="重 is a common polyphonic character in editing and layout copy.",
        suggestion="For narration, rewrite as 重新排列.",
    ),
    PronunciationRule(
        term="调仓",
        expected="调仓：调读 diao4",
        reason="调 is a common polyphonic character in finance narration.",
        suggestion="If a TTS voice misreads it, rewrite as 调整仓位.",
    ),
    PronunciationRule(
        term="调色",
        expected="调色：调读 tiao2",
        reason="调 is a common polyphonic character in video-production narration.",
        suggestion="If a TTS voice misreads it, rewrite as 色彩调整.",
    ),
)


def scan_text(
    text: str,
    *,
    path: str = "<text>",
    rules: tuple[PronunciationRule, ...] = DEFAULT_RULES,
) -> list[PronunciationFinding]:
    findings: list[PronunciationFinding] = []
    for rule in rules:
        start = 0
        while True:
            index = text.find(rule.term, start)
            if index < 0:
                break
            line, column = _line_column(text, index)
            findings.append(
                PronunciationFinding(
                    term=rule.term,
                    expected=rule.expected,
                    reason=rule.reason,
                    suggestion=rule.suggestion,
                    line=line,
                    column=column,
                    path=path,
                )
            )
            start = index + len(rule.term)
    return sorted(findings, key=lambda item: (item.path, item.line, item.column, item.term))


def scan_file(path: str | Path) -> list[PronunciationFinding]:
    file_path = Path(path)
    return scan_text(file_path.read_text(encoding="utf-8"), path=str(file_path))


def format_finding(finding: PronunciationFinding) -> str:
    return (
        f"{finding.path}:{finding.line}:{finding.column}: pronunciation warning: "
        f"`{finding.term}` expected {finding.expected}. "
        f"{finding.reason} Suggestion: {finding.suggestion}"
    )


def _line_column(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    line_start = text.rfind("\n", 0, index) + 1
    return line, index - line_start + 1
