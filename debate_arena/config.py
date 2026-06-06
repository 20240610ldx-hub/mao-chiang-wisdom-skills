from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ConfigError


def parse_bool(value: Any, *, default: bool | None = None) -> bool:
    if value is None:
        if default is None:
            raise ConfigError("Boolean value is required.")
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on", "enabled"}:
        return True
    if normalized in {"0", "false", "no", "n", "off", "disabled"}:
        return False
    raise ConfigError(f"Invalid boolean value: {value!r}")


@dataclass(slots=True)
class DebateConfig:
    skill_a_path: Path
    skill_b_path: Path
    output_path: Path
    language: str = "zh-CN"
    topic_mode: str = "auto"
    issue_count: int = 4
    word_limit: int = 600
    cross_exam_questions_each: int = 2
    enable_fact_check: bool = False
    enable_judge: bool = True
    llm_provider: str = "openai"
    model: str | None = None

    def __post_init__(self) -> None:
        self.skill_a_path = Path(self.skill_a_path)
        self.skill_b_path = Path(self.skill_b_path)
        self.output_path = Path(self.output_path)
        self.issue_count = int(self.issue_count)
        self.word_limit = int(self.word_limit)
        self.cross_exam_questions_each = int(self.cross_exam_questions_each)
        if self.topic_mode != "auto":
            raise ConfigError("Only --topic-mode auto is supported in v0.1.")
        if not 3 <= self.issue_count <= 5:
            raise ConfigError("--issues must be between 3 and 5.")
        if self.word_limit <= 0:
            raise ConfigError("--word-limit must be greater than 0.")
        if self.cross_exam_questions_each <= 0:
            raise ConfigError("cross_exam_questions_each must be greater than 0.")


def load_config_file(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise ConfigError(f"Config file does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        import json

        data = json.loads(text)
        return data if isinstance(data, dict) else {}
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    except ImportError:
        return _load_simple_yaml(text)


def _load_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_section: str | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if indent == 0 and not value:
            current_section = key
            data[current_section] = {}
            continue
        parsed_value = _parse_scalar(value)
        if indent > 0 and current_section:
            section = data.setdefault(current_section, {})
            if isinstance(section, dict):
                section[key] = parsed_value
        else:
            data[key] = parsed_value
    return data


def _parse_scalar(value: str) -> Any:
    if not value:
        return ""
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        return int(value)
    except ValueError:
        pass
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def config_from_mapping(data: dict[str, Any]) -> DebateConfig:
    input_section = data.get("input") or {}
    runtime = data.get("runtime") or {}
    output = data.get("output") or {}
    return DebateConfig(
        skill_a_path=input_section.get("skill_a_path"),
        skill_b_path=input_section.get("skill_b_path"),
        output_path=output.get("markdown_path"),
        language=runtime.get("language", "zh-CN"),
        topic_mode=runtime.get("topic_mode", "auto"),
        issue_count=runtime.get("issue_count", 4),
        word_limit=runtime.get("word_limit", 600),
        cross_exam_questions_each=runtime.get("cross_exam_questions_each", 2),
        enable_fact_check=parse_bool(runtime.get("enable_fact_check"), default=False),
        enable_judge=parse_bool(runtime.get("enable_judge"), default=True),
        llm_provider=runtime.get("llm_provider", "openai"),
        model=runtime.get("model"),
    )
