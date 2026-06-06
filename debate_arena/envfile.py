from __future__ import annotations

import os
from pathlib import Path

from .errors import ConfigError


def load_env_file(path: str | Path, *, override: bool = False) -> bool:
    env_path = Path(path)
    if not env_path.exists():
        return False
    if not env_path.is_file():
        raise ConfigError(f"Env path is not a file: {env_path}")

    text = env_path.read_text(encoding="utf-8-sig")
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            raise ConfigError(f"Invalid env line {line_number} in {env_path}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            raise ConfigError(f"Invalid env line {line_number} in {env_path}: empty key")
        if not override and key in os.environ:
            continue
        os.environ[key] = _parse_env_value(value.strip())
    return True


def _parse_env_value(value: str) -> str:
    if not value:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value
