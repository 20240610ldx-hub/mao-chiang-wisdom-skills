"""Debate Arena package."""

from .config import DebateConfig
from .orchestrator import run_debate

__all__ = ["DebateConfig", "run_debate"]
