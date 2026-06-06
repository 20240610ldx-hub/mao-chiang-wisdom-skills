from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from importlib import resources
from typing import Any


def load_prompt(name: str) -> str:
    prompt_path = resources.files("debate_arena.prompts").joinpath(name)
    return prompt_path.read_text(encoding="utf-8")


def render_prompt(name: str, **values: Any) -> str:
    template = load_prompt(name)
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", _prompt_value(value))
    return template


def _prompt_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if is_dataclass(value):
        return json.dumps(asdict(value), ensure_ascii=False, indent=2)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)
