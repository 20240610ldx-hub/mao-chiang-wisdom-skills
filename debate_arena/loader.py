from __future__ import annotations

from pathlib import Path

from .errors import LoaderError


def load_text(path: str | Path) -> str:
    path = Path(path)
    if not path.exists():
        raise LoaderError(f"Skill file does not exist: {path}")
    if not path.is_file():
        raise LoaderError(f"Skill path is not a file: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise LoaderError(f"Skill file is empty: {path}")
    return text
