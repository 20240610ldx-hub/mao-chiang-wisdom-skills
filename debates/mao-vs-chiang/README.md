# Mao vs. Chiang Debate Artifacts

This directory publishes two generated comparisons of the Mao Zedong and
Chiang Kai-shek reasoning Skills. They are methodology simulations, not real
historical dialogue or verified quotation collections.

## Artifacts

- [Formal Debate Arena transcript](formal-debate-2026-05-17.md), generated
  May 17, 2026. Fact-checking was disabled and the automated judge was enabled.
  It scored Side A (Chiang) 86 and Side B (Mao) 85. The one-point result is an
  output of a single model and rubric, not a historical verdict.
- [Experimental free dialogue](free-dialogue-2026-05-19.md), generated
  May 19, 2026 with a custom prompt. It did not use the standard Arena
  fact-check or judge stages.
- [Free-dialogue prompt](free-dialogue-prompt.md), published so the shorter
  experimental artifact can be inspected and reproduced.

## Provenance

Both historical artifacts used the Skill snapshots preserved under
`inputs/2026-05-17/`. Those snapshots differ from the current canonical Skills
under the repository root. They are immutable run inputs for auditability, not
installation targets.

[provenance.json](provenance.json) records SHA-256 hashes for the artifacts,
prompt, archived inputs, and current canonical Skills. Local absolute paths in
the free-dialogue HTML comment are retained because the original file is
published byte-for-byte; they describe the generation environment and are not
installation requirements.

## Responsible Use

The transcripts may contain model-generated factual claims or purported
quotations. Treat those statements as unverified unless checked against primary
documents. Do not use the judge result as evidence of political, moral, or
historical superiority.
