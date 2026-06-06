from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import DebateConfig
from .errors import InvalidLLMOutput
from .llm_client import LLMClient, extract_json_list, extract_json_object, make_llm_client
from .loader import load_text
from .models import DebatePlan, DebateTranscript, DebateTurn, SkillProfile
from .prompting import render_prompt
from .render import render_compact_transcript, render_markdown


def run_debate(config: DebateConfig, llm: LLMClient | None = None) -> DebateTranscript:
    runner = DebateRunner(config, llm or make_llm_client(config.llm_provider, model=config.model))
    return runner.run()


class DebateRunner:
    def __init__(self, config: DebateConfig, llm: LLMClient) -> None:
        self.config = config
        self.llm = llm
        self.skill_a_text = ""
        self.skill_b_text = ""

    def run(self) -> DebateTranscript:
        self.skill_a_text = load_text(self.config.skill_a_path)
        self.skill_b_text = load_text(self.config.skill_b_path)

        skill_a_profile = self._profile_skill(self.skill_a_text, "A")
        skill_b_profile = self._profile_skill(self.skill_b_text, "B")
        debate_plan = self._generate_debate_plan(skill_a_profile, skill_b_profile)

        transcript = DebateTranscript(
            metadata=self._metadata(),
            skill_a_profile=skill_a_profile,
            skill_b_profile=skill_b_profile,
            debate_plan=debate_plan,
        )

        self._run_opening(transcript)
        self._run_issue_arguments(transcript)
        self._run_rebuttal(transcript)
        self._run_cross_examination(transcript)
        self._run_closing(transcript)

        if self.config.enable_fact_check:
            transcript.fact_check = self._run_fact_check(transcript)
        if self.config.enable_judge:
            transcript.judge_report = self._run_judge(transcript)

        markdown = render_markdown(transcript)
        self.config.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.output_path.write_text(markdown, encoding="utf-8")
        return transcript

    def _metadata(self) -> dict[str, Any]:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "language": self.config.language,
            "topic_mode": self.config.topic_mode,
            "fact_check_enabled": self.config.enable_fact_check,
            "judge_enabled": self.config.enable_judge,
            "word_limit": self.config.word_limit,
            "skill_a_path": str(self.config.skill_a_path),
            "skill_b_path": str(self.config.skill_b_path),
        }

    def _profile_skill(self, skill_text: str, skill_id: str) -> SkillProfile:
        prompt = render_prompt("skill_profiler.md", skill_text=skill_text)
        data = self._complete_json_object(prompt, purpose=f"profile:{skill_id}")
        return SkillProfile.from_dict(data, skill_id=skill_id)

    def _generate_debate_plan(self, profile_a: SkillProfile, profile_b: SkillProfile) -> DebatePlan:
        prompt = render_prompt(
            "topic_generator.md",
            skill_a_profile=profile_a,
            skill_b_profile=profile_b,
            issue_count=self.config.issue_count,
            language=self.config.language,
        )
        data = self._complete_json_object(prompt, purpose="topic")
        plan = DebatePlan.from_dict(data)
        if not plan.topic:
            raise InvalidLLMOutput("Topic generator returned an empty topic.")
        if not 3 <= len(plan.issues) <= 5:
            raise InvalidLLMOutput("Topic generator must return 3-5 debate issues.")
        return plan

    def _run_opening(self, transcript: DebateTranscript) -> None:
        for side in ("A", "B"):
            question = (
                "Please present your opening statement on the debate topic, "
                "defending your assigned position and addressing the main issues."
            )
            answer = self._run_debater(side, transcript, "Opening Statement", question)
            transcript.turns.append(DebateTurn("opening", "Opening Statement", side, question, answer))

    def _run_issue_arguments(self, transcript: DebateTranscript) -> None:
        for issue in transcript.debate_plan.issues:
            question_a = (
                f"On Issue {issue.issue_id}, how does your framework answer this question: "
                f"{issue.question} Also pre-empt the strongest objection from B."
            )
            answer_a = self._run_debater("A", transcript, f"Issue {issue.issue_id}", question_a)
            transcript.turns.append(
                DebateTurn("issue", f"Issue {issue.issue_id} - A Side", "A", question_a, answer_a, [issue.issue_id])
            )
            question_b = (
                f"On Issue {issue.issue_id}, how does your framework answer this question: "
                f"{issue.question} Also respond to A's answer."
            )
            answer_b = self._run_debater("B", transcript, f"Issue {issue.issue_id}", question_b)
            transcript.turns.append(
                DebateTurn("issue", f"Issue {issue.issue_id} - B Side", "B", question_b, answer_b, [issue.issue_id])
            )

    def _run_rebuttal(self, transcript: DebateTranscript) -> None:
        for side in ("A", "B"):
            opponent = "B" if side == "A" else "A"
            question = f"Identify Side {opponent}'s two strongest claims so far, then rebut them directly."
            answer = self._run_debater(side, transcript, "Rebuttal", question)
            transcript.turns.append(DebateTurn("rebuttal", "Rebuttal", side, question, answer))

    def _run_cross_examination(self, transcript: DebateTranscript) -> None:
        for asking_side, answering_side in (("A", "B"), ("B", "A")):
            questions = self._generate_cross_exam_questions(asking_side, answering_side, transcript)
            for question in questions:
                answer = self._run_debater(answering_side, transcript, f"{asking_side} asks {answering_side}", question)
                transcript.turns.append(
                    DebateTurn("cross_exam", f"{asking_side} asks {answering_side}", answering_side, question, answer)
                )

    def _run_closing(self, transcript: DebateTranscript) -> None:
        for side in ("A", "B"):
            question = "Give your closing statement. Do not introduce major new arguments."
            answer = self._run_debater(side, transcript, "Closing Statement", question)
            transcript.turns.append(DebateTurn("closing", "Closing Statement", side, question, answer))

    def _run_debater(
        self,
        side: str,
        transcript: DebateTranscript,
        round_name: str,
        question: str,
    ) -> str:
        plan = transcript.debate_plan
        profile = transcript.skill_a_profile if side == "A" else transcript.skill_b_profile
        skill_text = self.skill_a_text if side == "A" else self.skill_b_text
        position = plan.side_a_position if side == "A" else plan.side_b_position
        prompt = render_prompt(
            "debater.md",
            skill_text=skill_text,
            skill_profile=profile,
            position=position,
            topic=plan.topic,
            issues=[issue.to_dict() for issue in plan.issues],
            previous_transcript=render_compact_transcript(transcript),
            round_name=round_name,
            question=question,
            word_limit=self.config.word_limit,
        )
        return self.llm.complete(prompt, purpose=f"debater:{side}:{round_name}").strip()

    def _generate_cross_exam_questions(
        self,
        asking_side: str,
        opponent_side: str,
        transcript: DebateTranscript,
    ) -> list[str]:
        prompt = render_prompt(
            "cross_examiner.md",
            asking_side=asking_side,
            opponent_side=opponent_side,
            topic=transcript.debate_plan.topic,
            issues=[issue.to_dict() for issue in transcript.debate_plan.issues],
            previous_transcript=render_compact_transcript(transcript),
            question_count=self.config.cross_exam_questions_each,
        )
        items = self._complete_json_list(prompt, purpose="cross_exam")
        questions = [str(item).strip() for item in items if str(item).strip()]
        if len(questions) != self.config.cross_exam_questions_each:
            raise InvalidLLMOutput("Cross-examiner returned the wrong number of questions.")
        return questions

    def _run_fact_check(self, transcript: DebateTranscript) -> str:
        prompt = render_prompt("fact_checker.md", transcript=render_compact_transcript(transcript))
        return self.llm.complete(prompt, purpose="fact_check").strip()

    def _run_judge(self, transcript: DebateTranscript) -> str:
        prompt = render_prompt(
            "judge.md",
            skill_a_profile=transcript.skill_a_profile,
            skill_b_profile=transcript.skill_b_profile,
            debate_plan=transcript.debate_plan,
            transcript=render_compact_transcript(transcript),
            fact_check_report=transcript.fact_check or "Fact check disabled.",
        )
        return self.llm.complete(prompt, purpose="judge").strip()

    def _complete_json_object(self, prompt: str, *, purpose: str) -> dict[str, Any]:
        raw = self.llm.complete(prompt, purpose=purpose)
        try:
            return extract_json_object(raw)
        except ValueError:
            repair_prompt = _repair_prompt(raw, "Return only a valid JSON object.")
            repaired = self.llm.complete(repair_prompt, purpose=f"{purpose}:repair")
            try:
                return extract_json_object(repaired)
            except ValueError as exc:
                self._save_debug_output(purpose, raw, repaired)
                raise InvalidLLMOutput(f"Invalid JSON object from {purpose}. Raw output saved to debug folder.") from exc

    def _complete_json_list(self, prompt: str, *, purpose: str) -> list[Any]:
        raw = self.llm.complete(prompt, purpose=purpose)
        try:
            return extract_json_list(raw)
        except ValueError:
            repair_prompt = _repair_prompt(raw, "Return only a valid JSON list.")
            repaired = self.llm.complete(repair_prompt, purpose=f"{purpose}:repair")
            try:
                return extract_json_list(repaired)
            except ValueError as exc:
                self._save_debug_output(purpose, raw, repaired)
                raise InvalidLLMOutput(f"Invalid JSON list from {purpose}. Raw output saved to debug folder.") from exc

    def _save_debug_output(self, purpose: str, raw: str, repaired: str) -> None:
        debug_dir = self.config.output_path.parent / "debug"
        debug_dir.mkdir(parents=True, exist_ok=True)
        safe_purpose = "".join(char if char.isalnum() or char in "-_" else "_" for char in purpose)
        path = debug_dir / f"{safe_purpose}.txt"
        path.write_text(f"RAW OUTPUT:\n{raw}\n\nREPAIRED OUTPUT:\n{repaired}\n", encoding="utf-8")


def _repair_prompt(raw_output: str, instruction: str) -> str:
    return (
        "The previous response was not valid JSON for the requested schema.\n"
        f"{instruction}\n\n"
        "Previous response:\n"
        f"{raw_output}"
    )
