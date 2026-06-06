# Debate Arena

`debate_arena` is a reusable two-Skill debate runner. It profiles two local
`SKILL.md` files, generates a debatable topic, assigns opposing positions, runs
opening statements, issue rounds, rebuttals, cross-examination, and closings,
then optionally adds fact-check and judge reports.

The default participants in this repository are the current canonical Skills:

```text
skills/chiang-kai-shek-wisdom/SKILL.md
skills/mao-zedong-wisdom/SKILL.md
```

Historical transcripts under `debates/` may have been generated from older
archived snapshots. See their local provenance files before comparing results.

## Install

From the repository root:

```powershell
pip install -e .
```

## Run

Deterministic offline structure check:

```powershell
python -m debate_arena run --llm fake --issues 3
```

The installed command is equivalent:

```powershell
debate-arena run --llm fake --issues 3
```

For a real OpenAI-compatible run, copy
`debate_arena/examples/.env.example` to `.env`, set the key locally, and run:

```powershell
python -m debate_arena run `
  --config .\debate_arena\examples\sample_config.yaml
```

The CLI reads `DEBATE_ARENA_API_KEY`, `DEBATE_ARENA_BASE_URL`, and
`DEBATE_ARENA_MODEL`, with `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and
`OPENAI_MODEL` as fallbacks.

## Custom Skills

Use any two local Skill files:

```powershell
python -m debate_arena run `
  --skill-a .\path\to\first\SKILL.md `
  --skill-b .\path\to\second\SKILL.md `
  --language zh-CN `
  --issues 4 `
  --fact-check true `
  --judge true `
  --out .\output\debate_arena\custom.md
```

Alternatively, `--participants-dir` accepts a directory containing
`skill_a/SKILL.md` and `skill_b/SKILL.md`.

## Output and Limits

The Markdown output includes metadata, generated topic and positions, three to
five issues, a Q/A transcript, optional fact-checking, and an automated judge
report. All roles currently share one configured model.

Generated debate is a model simulation of reasoning frameworks. It is not a
real historical conversation, verified quotation record, political verdict, or
substitute for primary-source research. An enabled judge measures the generated
run under its rubric; it does not certify either historical figure or Skill as
objectively superior.
