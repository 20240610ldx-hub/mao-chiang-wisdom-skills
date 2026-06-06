from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from .config import DebateConfig, load_config_file, parse_bool
from .envfile import load_env_file
from .errors import DebateArenaError
from .orchestrator import run_debate


DEFAULT_SKILL_A_PATH = Path("skills") / "chiang-kai-shek-wisdom" / "SKILL.md"
DEFAULT_SKILL_B_PATH = Path("skills") / "mao-zedong-wisdom" / "SKILL.md"
DEFAULT_OUTPUT_PATH = Path("output") / "debate_arena" / "debate.md"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        try:
            config = _config_from_args(args)
            run_debate(config)
        except DebateArenaError as exc:
            parser.exit(2, f"error: {exc}\n")
        print(f"Wrote debate transcript: {config.output_path}")
        return 0
    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="debate-arena", description="Run automated two-Skill debates.")
    subparsers = parser.add_subparsers(dest="command")
    run = subparsers.add_parser("run", help="Run one complete two-side debate.")
    run.add_argument(
        "--skill-a",
        help="Path to Side A SKILL.md. Defaults to skills/chiang-kai-shek-wisdom/SKILL.md.",
    )
    run.add_argument(
        "--skill-b",
        help="Path to Side B SKILL.md. Defaults to skills/mao-zedong-wisdom/SKILL.md.",
    )
    run.add_argument("--participants-dir", help="Folder containing skill_a/SKILL.md and skill_b/SKILL.md.")
    run.add_argument("--out", help="Output Markdown path. Defaults to output/debate_arena/debate.md.")
    run.add_argument("--config", help="Optional YAML or JSON config file.")
    run.add_argument("--env-file", help="Optional .env file. Defaults to .env when present.")
    run.add_argument("--language", help="Output language, for example zh-CN or en.")
    run.add_argument("--issues", type=int, help="Number of debate issues, 3-5.")
    run.add_argument("--word-limit", type=int, help="Word limit per debater answer.")
    run.add_argument("--fact-check", nargs="?", const="true", help="Enable or disable fact check.")
    run.add_argument("--judge", nargs="?", const="true", help="Enable or disable judge report.")
    run.add_argument("--topic-mode", help="Topic mode. v0.1 supports auto only.")
    run.add_argument("--llm", choices=["openai", "openai-compatible", "fake"], help="LLM provider.")
    run.add_argument("--model", help="Model name for OpenAI-compatible providers.")
    run.set_defaults(command="run")
    return parser


def _config_from_args(args: argparse.Namespace) -> DebateConfig:
    if args.env_file:
        load_env_file(args.env_file, override=True)
    else:
        load_env_file(".env", override=False)

    file_data: dict[str, Any] = load_config_file(args.config) if args.config else {}
    input_section = file_data.get("input") or {}
    runtime = file_data.get("runtime") or {}
    output = file_data.get("output") or {}

    participants_dir_value = (
        args.participants_dir
        or input_section.get("participants_dir")
        or os.getenv("DEBATE_ARENA_PARTICIPANTS_DIR")
    )
    if participants_dir_value:
        participants_dir = Path(participants_dir_value)
        default_skill_a = participants_dir / "skill_a" / "SKILL.md"
        default_skill_b = participants_dir / "skill_b" / "SKILL.md"
    else:
        default_skill_a = DEFAULT_SKILL_A_PATH
        default_skill_b = DEFAULT_SKILL_B_PATH

    skill_a_path = args.skill_a or input_section.get("skill_a_path") or default_skill_a
    skill_b_path = args.skill_b or input_section.get("skill_b_path") or default_skill_b
    output_path = args.out or output.get("markdown_path") or DEFAULT_OUTPUT_PATH

    return DebateConfig(
        skill_a_path=Path(skill_a_path),
        skill_b_path=Path(skill_b_path),
        output_path=Path(output_path),
        language=args.language or runtime.get("language", "zh-CN"),
        topic_mode=args.topic_mode or runtime.get("topic_mode", "auto"),
        issue_count=args.issues if args.issues is not None else runtime.get("issue_count", 4),
        word_limit=args.word_limit if args.word_limit is not None else runtime.get("word_limit", 600),
        cross_exam_questions_each=runtime.get("cross_exam_questions_each", 2),
        enable_fact_check=parse_bool(
            args.fact_check if args.fact_check is not None else runtime.get("enable_fact_check"),
            default=False,
        ),
        enable_judge=parse_bool(args.judge if args.judge is not None else runtime.get("enable_judge"), default=True),
        llm_provider=args.llm or runtime.get("llm_provider") or os.getenv("DEBATE_ARENA_LLM", "openai"),
        model=args.model or runtime.get("model") or os.getenv("DEBATE_ARENA_MODEL") or os.getenv("OPENAI_MODEL"),
    )
