# Evaluation Records

This directory publishes evaluation records for the two released skills, with emphasis on dialogue tests.

## Mao Zedong

- [Dialogue test](mao-zedong/runtime-dialogue-test.md): DeepSeek runtime dialogue transcript, 19 cases.
- [Runtime evaluation summary](mao-zedong/runtime-evaluation.md): full runtime evaluation summary, `21/25`.
- [Runtime judgment JSON](mao-zedong/runtime-judgment.json): case-level automated judgment record.
- [Initial evaluation](mao-zedong/initial-evaluation.md): SkillEval-MDF-v1.1 review.
- [Scorecard JSON](mao-zedong/scorecard.json): machine-readable scorecard.
- [Artifact facts JSON](mao-zedong/artifact-facts.json): artifact integrity metadata with local generation paths, file sizes, and SHA256 hashes.

## Chiang Kai-shek

- [Dialogue test](chiang-kai-shek/runtime-dialogue-test.md): generated DeepSeek dialogue transcript, 12 cases.
- [Runtime evaluation summary](chiang-kai-shek/runtime-evaluation.md): full runtime evaluation summary.
- [Runtime judgment JSON](chiang-kai-shek/runtime-judgment.json): case-level automated judgment record.
- [Initial evaluation](chiang-kai-shek/initial-evaluation.md): SkillEval-MDF-v1.1 review.
- [Scorecard JSON](chiang-kai-shek/scorecard.json): machine-readable scorecard.
- [Artifact facts JSON](chiang-kai-shek/artifact-facts.json): artifact integrity metadata with local generation paths, file sizes, and SHA256 hashes.

## Notes

`artifact-facts.json` is included for provenance only. Its local filesystem paths document where the evaluated artifacts were generated and are not installation requirements. Raw source materials, PDFs, extraction shards, and distillation pipeline internals remain outside this public repository.
