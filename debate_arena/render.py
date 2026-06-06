from __future__ import annotations

from .models import DebateTranscript, DebateTurn


def render_markdown(transcript: DebateTranscript) -> str:
    metadata = transcript.metadata
    plan = transcript.debate_plan
    lines: list[str] = [
        "# Debate Arena Transcript",
        "",
        "## 1. Metadata",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Generated At | {_cell(metadata.get('generated_at'))} |",
        f"| Language | {_cell(metadata.get('language'))} |",
        f"| Skill A | {_cell(transcript.skill_a_profile.name)} |",
        f"| Skill B | {_cell(transcript.skill_b_profile.name)} |",
        f"| Topic Mode | {_cell(metadata.get('topic_mode', 'auto'))} |",
        f"| Fact Check | {_cell('enabled' if metadata.get('fact_check_enabled') else 'disabled')} |",
        f"| Judge | {_cell('enabled' if metadata.get('judge_enabled') else 'disabled')} |",
        "",
        "## 2. Generated Debate Topic",
        "",
        f"**Topic:** {plan.topic}",
        "",
        f"**Rationale:** {plan.topic_rationale}",
        "",
        "## 3. Assigned Positions",
        "",
        "| Side | Debater | Position |",
        "|---|---|---|",
        f"| A | {_cell(plan.side_a_name)} | {_cell(plan.side_a_position)} |",
        f"| B | {_cell(plan.side_b_name)} | {_cell(plan.side_b_position)} |",
        "",
        "## 4. Debate Issues",
        "",
    ]
    for index, issue in enumerate(plan.issues, start=1):
        lines.extend(
            [
                f"### Issue {index}: {issue.question}",
                "",
                f"- Why it matters: {issue.why_it_matters}",
                f"- Expected tension: {issue.expected_tension}",
                "",
            ]
        )
    if plan.risk_notes:
        lines.extend(["**Risk Notes:**", ""])
        lines.extend(f"- {note}" for note in plan.risk_notes)
        lines.append("")

    lines.extend(["## 5. Q/A Transcript", ""])
    _append_turn_group(lines, "### Round 1: Opening Statement", _turns(transcript, "opening"))
    _append_turn_group(lines, "### Round 2: Issue-Based Arguments", _turns(transcript, "issue"))
    _append_turn_group(lines, "### Round 3: Rebuttal", _turns(transcript, "rebuttal"))
    _append_turn_group(lines, "### Round 4: Cross-Examination", _turns(transcript, "cross_exam"))
    _append_turn_group(lines, "### Round 5: Closing Statement", _turns(transcript, "closing"))

    lines.extend(["## 6. Fact Check Report", ""])
    lines.append(transcript.fact_check.strip() if transcript.fact_check else "Fact check disabled.")
    lines.extend(["", "## 7. Judge Report", ""])
    lines.append(transcript.judge_report.strip() if transcript.judge_report else "Judge disabled.")
    lines.extend(
        [
            "",
            "## 8. Skill Improvement Suggestions",
            "",
            "See the Skill Improvement Suggestions subsection in the judge report.",
            "",
        ]
    )
    return "\n".join(lines)


def render_compact_transcript(transcript: DebateTranscript) -> str:
    chunks: list[str] = []
    for turn in transcript.turns:
        issues = f" [{', '.join(turn.referenced_issue_ids)}]" if turn.referenced_issue_ids else ""
        chunks.append(
            f"{turn.round_name}{issues}\n"
            f"Speaker: {turn.speaker}\n"
            f"Q: {turn.prompt_question}\n"
            f"A: {turn.answer}"
        )
    return "\n\n".join(chunks)


def _append_turn_group(lines: list[str], heading: str, turns: list[DebateTurn]) -> None:
    lines.extend([heading, ""])
    if not turns:
        lines.extend(["No turns recorded.", ""])
        return
    for turn in turns:
        issue_label = f" [{', '.join(turn.referenced_issue_ids)}]" if turn.referenced_issue_ids else ""
        lines.extend(
            [
                f"#### {turn.round_name} - {turn.speaker}{issue_label}",
                "",
                f"**Q:** {turn.prompt_question}",
                "",
                f"**A:** {turn.answer}",
                "",
            ]
        )


def _turns(transcript: DebateTranscript, round_id: str) -> list[DebateTurn]:
    return [turn for turn in transcript.turns if turn.round_id == round_id]


def _cell(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", "<br>")
