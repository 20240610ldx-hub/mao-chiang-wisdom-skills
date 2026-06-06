from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any, Protocol

from .errors import LLMConfigurationError, LLMRuntimeError


class LLMClient(Protocol):
    def complete(self, prompt: str, *, purpose: str) -> str:
        """Return a completion for a single prompt."""


class OpenAICompatibleClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        temperature: float = 0.2,
        timeout_seconds: int = 120,
    ) -> None:
        self.api_key = api_key or os.getenv("DEBATE_ARENA_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = (
            base_url
            or os.getenv("DEBATE_ARENA_BASE_URL")
            or os.getenv("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        ).rstrip("/")
        self.model = model or os.getenv("DEBATE_ARENA_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds
        if not self.api_key:
            raise LLMConfigurationError(
                "LLM provider is not configured. Set OPENAI_API_KEY or use --llm fake for a deterministic dry run."
            )

    def complete(self, prompt: str, *, purpose: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a precise Debate Arena runtime component. "
                        "Follow the user's requested output format exactly."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
        }
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LLMRuntimeError(f"LLM request failed for {purpose}: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise LLMRuntimeError(f"LLM request failed for {purpose}: {exc.reason}") from exc

        try:
            data = json.loads(body)
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMRuntimeError(f"Unexpected LLM response for {purpose}: {body[:500]}") from exc


class FakeLLMClient:
    """Deterministic client for tests and local dry runs."""

    def complete(self, prompt: str, *, purpose: str) -> str:
        if purpose.startswith("profile:"):
            side = purpose.split(":", 1)[1]
            name = _extract_heading(prompt) or f"Fake Skill {side}"
            return json.dumps(
                {
                    "skill_id": side,
                    "name": name,
                    "domain": "reasoning framework",
                    "core_worldview": [f"{name} treats decisions as tradeoffs under constraints."],
                    "core_values": ["clarity", "practical action", "intellectual honesty"],
                    "preferred_methods": ["separate facts from interpretation", "test assumptions"],
                    "strategic_assumptions": ["bad framing creates bad decisions"],
                    "rhetorical_style": ["direct", "analytical", "brief"],
                    "likely_debate_strengths": ["clear structure", "strong boundary setting"],
                    "likely_debate_weaknesses": ["may underweight emotional context"],
                    "forbidden_behaviors": ["fabricated quotations", "unsupported certainty"],
                    "factual_boundaries": ["mark uncertain claims as interpretation"],
                },
                ensure_ascii=False,
            )
        if purpose == "topic":
            issue_count = _extract_int(prompt, r"Number of issues:\s*(\d+)", default=3)
            issues = [
                {
                    "issue_id": f"I{index + 1}",
                    "question": f"How should the two frameworks handle decision pressure dimension {index + 1}?",
                    "why_it_matters": "It forces both sides to turn principles into action.",
                    "expected_tension": "One side will emphasize discipline while the other stresses empirical correction.",
                }
                for index in range(issue_count)
            ]
            return json.dumps(
                {
                    "topic": "When principles conflict with changing evidence, which should guide action first?",
                    "topic_rationale": "The topic creates tension between stable commitments and adaptive correction.",
                    "side_a_name": "Skill A",
                    "side_a_position": "Stable principles should guide the first move.",
                    "side_b_name": "Skill B",
                    "side_b_position": "Fresh evidence should revise the first move quickly.",
                    "issues": issues,
                    "risk_notes": ["Dry-run output uses synthetic claims only."],
                },
                ensure_ascii=False,
            )
        if purpose.startswith("debater:"):
            parts = purpose.split(":")
            side = parts[1] if len(parts) > 1 else "A"
            question = _extract_after(prompt, "Current question:")
            return (
                f"I answer as Side {side}: the decisive point is to keep the assigned position visible, "
                f"test the opponent's assumption, and avoid claims beyond the Skill. Question addressed: {question[:180]}"
            )
        if purpose == "cross_exam":
            count = _extract_int(prompt, r"Generate exactly\s*(\d+)", default=2)
            return json.dumps(
                [f"What assumption in your position would change your conclusion? ({index + 1})" for index in range(count)],
                ensure_ascii=False,
            )
        if purpose == "fact_check":
            return (
                "| Claim | Speaker | Risk Type | Risk Level | Comment |\n"
                "|---|---|---|---|---|\n"
                "| No high-risk factual claims detected in fake run. | All | none | low | Dry-run answers are synthetic. |"
            )
        if purpose == "judge":
            return (
                "### Scorecard\n\n"
                "| Dimension | A Score | B Score | Notes |\n"
                "|---|---:|---:|---|\n"
                "| Position Clarity | 8 | 8 | Both sides stayed visible. |\n"
                "| Argument Structure | 12 | 12 | Both used simple structured answers. |\n"
                "| Evidence Quality | 10 | 10 | Fake run avoids factual claims. |\n"
                "| Rebuttal Effectiveness | 11 | 11 | Rebuttals are limited by dry-run responses. |\n"
                "| Cross-Examination | 8 | 8 | Questions target assumptions. |\n"
                "| Logical Rigor | 12 | 12 | Reasoning is coherent but generic. |\n"
                "| Skill Fidelity | 11 | 11 | Fake profiles are followed, but not rich. |\n"
                "| Rule Compliance | 5 | 5 | No rule violations. |\n"
                "| Total | 77 | 77 | Draw. |\n\n"
                "### Final Verdict\n\n"
                "Winner: Draw\n\n"
                "Reason: This deterministic dry run verifies structure rather than debate quality.\n\n"
                "### Skill Improvement Suggestions\n\n"
                "#### For Skill A\n\n"
                "- Add sharper source-grounded methods for handling conflicting evidence.\n\n"
                "#### For Skill B\n\n"
                "- Add clearer limits on when adaptation becomes drift."
            )
        if purpose.endswith(":repair"):
            return "[]"
        return "Fake completion."


def make_llm_client(provider: str, *, model: str | None = None) -> LLMClient:
    provider = (provider or "openai").strip().lower()
    if provider == "fake":
        return FakeLLMClient()
    if provider in {"openai", "openai-compatible"}:
        return OpenAICompatibleClient(model=model)
    raise LLMConfigurationError(f"Unsupported LLM provider: {provider}")


def extract_json_object(text: str) -> dict[str, Any]:
    value = _extract_json_value(text)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object.")
    return value


def extract_json_list(text: str) -> list[Any]:
    value = _extract_json_value(text)
    if not isinstance(value, list):
        raise ValueError("Expected a JSON list.")
    return value


def _extract_json_value(text: str) -> Any:
    stripped = _strip_code_fence(text.strip())
    decoder = json.JSONDecoder()
    for index, char in enumerate(stripped):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(stripped[index:])
            return value
        except json.JSONDecodeError:
            continue
    raise ValueError(f"No valid JSON value found in response: {text[:300]}")


def _strip_code_fence(text: str) -> str:
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    return text


def _extract_heading(prompt: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", prompt, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(r"name:\s*(.+)", prompt, flags=re.IGNORECASE)
    return match.group(1).strip() if match else None


def _extract_int(prompt: str, pattern: str, *, default: int) -> int:
    match = re.search(pattern, prompt, flags=re.IGNORECASE)
    if not match:
        return default
    try:
        return int(match.group(1))
    except ValueError:
        return default


def _extract_after(prompt: str, marker: str) -> str:
    if marker not in prompt:
        return ""
    return prompt.split(marker, 1)[1].strip().splitlines()[0].strip()
