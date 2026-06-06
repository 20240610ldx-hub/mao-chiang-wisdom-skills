from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from debate_arena.cli import _config_from_args, build_parser
from debate_arena.config import DebateConfig, parse_bool
from debate_arena.envfile import load_env_file
from debate_arena.loader import load_text
from debate_arena.llm_client import FakeLLMClient, extract_json_list, extract_json_object
from debate_arena.orchestrator import run_debate


class DebateArenaTests(unittest.TestCase):
    def test_parse_bool(self) -> None:
        self.assertTrue(parse_bool("true"))
        self.assertFalse(parse_bool("off"))
        self.assertTrue(parse_bool(None, default=True))

    def test_load_text_rejects_empty_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text("   ", encoding="utf-8")
            with self.assertRaises(Exception):
                load_text(path)

    def test_extract_json_from_fenced_response(self) -> None:
        self.assertEqual(extract_json_object("```json\n{\"a\": 1}\n```"), {"a": 1})
        self.assertEqual(extract_json_list("prefix [\"x\", \"y\"] suffix"), ["x", "y"])

    def test_load_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text(
                "DEBATE_ARENA_TEST_VALUE='from-file'\n"
                "export DEBATE_ARENA_TEST_EMPTY=\n",
                encoding="utf-8",
            )
            self.assertTrue(load_env_file(path, override=True))
            import os

            self.assertEqual(os.environ["DEBATE_ARENA_TEST_VALUE"], "from-file")
            self.assertEqual(os.environ["DEBATE_ARENA_TEST_EMPTY"], "")

    def test_run_debate_with_fake_llm(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            skill_a = tmp_path / "skill_a" / "SKILL.md"
            skill_b = tmp_path / "skill_b" / "SKILL.md"
            out = tmp_path / "outputs" / "debate.md"
            skill_a.parent.mkdir()
            skill_b.parent.mkdir()
            skill_a.write_text("# Principle Skill\n\nPrefer stable principles.", encoding="utf-8")
            skill_b.write_text("# Evidence Skill\n\nPrefer empirical correction.", encoding="utf-8")

            config = DebateConfig(
                skill_a_path=skill_a,
                skill_b_path=skill_b,
                output_path=out,
                issue_count=3,
                word_limit=100,
                enable_fact_check=True,
                enable_judge=True,
                llm_provider="fake",
            )
            transcript = run_debate(config, FakeLLMClient())

            self.assertTrue(out.exists())
            markdown = out.read_text(encoding="utf-8")
            self.assertEqual(len(transcript.debate_plan.issues), 3)
            self.assertIn("# Debate Arena Transcript", markdown)
            self.assertIn("## 5. Q/A Transcript", markdown)
            self.assertIn("## 7. Judge Report", markdown)
            self.assertIn("Winner: Draw", markdown)

    def test_cli_fake_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            skill_a = tmp_path / "a.md"
            skill_b = tmp_path / "b.md"
            out = tmp_path / "debate.md"
            skill_a.write_text("# A\n\nA method.", encoding="utf-8")
            skill_b.write_text("# B\n\nB method.", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "debate_arena",
                    "run",
                    "--skill-a",
                    str(skill_a),
                    "--skill-b",
                    str(skill_b),
                    "--out",
                    str(out),
                    "--llm",
                    "fake",
                    "--issues",
                    "3",
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.exists())

    def test_cli_participants_dir_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            participants = tmp_path / "participants"
            skill_a = participants / "skill_a" / "SKILL.md"
            skill_b = participants / "skill_b" / "SKILL.md"
            out = tmp_path / "debate.md"
            skill_a.parent.mkdir(parents=True)
            skill_b.parent.mkdir(parents=True)
            skill_a.write_text("# Folder A\n\nUse folder convention.", encoding="utf-8")
            skill_b.write_text("# Folder B\n\nUse folder convention.", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "debate_arena",
                    "run",
                    "--participants-dir",
                    str(participants),
                    "--out",
                    str(out),
                    "--llm",
                    "fake",
                    "--issues",
                    "3",
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.exists())

    def test_cli_repo_defaults_use_canonical_skills(self) -> None:
        args = build_parser().parse_args(["run", "--llm", "fake"])
        config = _config_from_args(args)

        self.assertEqual(
            config.skill_a_path,
            Path("skills") / "chiang-kai-shek-wisdom" / "SKILL.md",
        )
        self.assertEqual(
            config.skill_b_path,
            Path("skills") / "mao-zedong-wisdom" / "SKILL.md",
        )


if __name__ == "__main__":
    unittest.main()
