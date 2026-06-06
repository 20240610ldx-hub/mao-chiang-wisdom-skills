from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def _string(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def _optional_string(value: Any) -> str | None:
    text = _string(value)
    return text or None


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_string(item) for item in value if _string(item)]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return [_string(value)]


@dataclass(slots=True)
class SkillProfile:
    skill_id: str
    name: str
    domain: str | None = None
    core_worldview: list[str] = field(default_factory=list)
    core_values: list[str] = field(default_factory=list)
    preferred_methods: list[str] = field(default_factory=list)
    strategic_assumptions: list[str] = field(default_factory=list)
    rhetorical_style: list[str] = field(default_factory=list)
    likely_debate_strengths: list[str] = field(default_factory=list)
    likely_debate_weaknesses: list[str] = field(default_factory=list)
    forbidden_behaviors: list[str] = field(default_factory=list)
    factual_boundaries: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any], skill_id: str) -> "SkillProfile":
        return cls(
            skill_id=skill_id,
            name=_string(data.get("name"), default=f"Skill {skill_id}"),
            domain=_optional_string(data.get("domain")),
            core_worldview=_string_list(data.get("core_worldview")),
            core_values=_string_list(data.get("core_values")),
            preferred_methods=_string_list(data.get("preferred_methods")),
            strategic_assumptions=_string_list(data.get("strategic_assumptions")),
            rhetorical_style=_string_list(data.get("rhetorical_style")),
            likely_debate_strengths=_string_list(data.get("likely_debate_strengths")),
            likely_debate_weaknesses=_string_list(data.get("likely_debate_weaknesses")),
            forbidden_behaviors=_string_list(data.get("forbidden_behaviors")),
            factual_boundaries=_string_list(data.get("factual_boundaries")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DebateIssue:
    issue_id: str
    question: str
    why_it_matters: str
    expected_tension: str

    @classmethod
    def from_dict(cls, data: dict[str, Any], index: int) -> "DebateIssue":
        default_id = f"I{index + 1}"
        return cls(
            issue_id=_string(data.get("issue_id"), default=default_id) or default_id,
            question=_string(data.get("question")),
            why_it_matters=_string(data.get("why_it_matters")),
            expected_tension=_string(data.get("expected_tension")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DebatePlan:
    topic: str
    topic_rationale: str
    side_a_name: str
    side_a_position: str
    side_b_name: str
    side_b_position: str
    issues: list[DebateIssue]
    risk_notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DebatePlan":
        issues_data = data.get("issues") or []
        issues = [
            DebateIssue.from_dict(item, index)
            for index, item in enumerate(issues_data)
            if isinstance(item, dict)
        ]
        return cls(
            topic=_string(data.get("topic")),
            topic_rationale=_string(data.get("topic_rationale")),
            side_a_name=_string(data.get("side_a_name"), default="Skill A"),
            side_a_position=_string(data.get("side_a_position")),
            side_b_name=_string(data.get("side_b_name"), default="Skill B"),
            side_b_position=_string(data.get("side_b_position")),
            issues=issues,
            risk_notes=_string_list(data.get("risk_notes")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DebateTurn:
    round_id: str
    round_name: str
    speaker: str
    prompt_question: str
    answer: str
    referenced_issue_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DebateTranscript:
    metadata: dict[str, Any]
    skill_a_profile: SkillProfile
    skill_b_profile: SkillProfile
    debate_plan: DebatePlan
    turns: list[DebateTurn] = field(default_factory=list)
    fact_check: str | None = None
    judge_report: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "skill_a_profile": self.skill_a_profile.to_dict(),
            "skill_b_profile": self.skill_b_profile.to_dict(),
            "debate_plan": self.debate_plan.to_dict(),
            "turns": [turn.to_dict() for turn in self.turns],
            "fact_check": self.fact_check,
            "judge_report": self.judge_report,
        }
