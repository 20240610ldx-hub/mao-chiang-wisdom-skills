# Evaluation Records

This directory publishes evaluation records for the two released skills, with emphasis on dialogue tests.

## Mao Zedong

- [Dialogue test](mao-zedong/runtime-dialogue-test.md): imported DeepSeek dialogue transcript, 19 cases.
- [Runtime evaluation summary](mao-zedong/runtime-evaluation.md): imported coverage; judge was disabled for this run.
- [Runtime judgment JSON](mao-zedong/runtime-judgment.json): sanitized metadata and aggregate record.
- [Initial evaluation](mao-zedong/initial-evaluation.md): SkillEval-MDF-v1.1 review.
- [Scorecard JSON](mao-zedong/scorecard.json): machine-readable scorecard.

## Chiang Kai-shek

- [Dialogue test](chiang-kai-shek/runtime-dialogue-test.md): generated DeepSeek dialogue transcript, 12 cases.
- [Runtime evaluation summary](chiang-kai-shek/runtime-evaluation.md): full runtime evaluation summary.
- [Runtime judgment JSON](chiang-kai-shek/runtime-judgment.json): case-level automated judgment record.
- [Initial evaluation](chiang-kai-shek/initial-evaluation.md): SkillEval-MDF-v1.1 review.
- [Scorecard JSON](chiang-kai-shek/scorecard.json): machine-readable scorecard.

## Notes

`artifact-facts.json` is intentionally not published because it is an internal pipeline artifact map with local filesystem paths and development metadata. Raw source materials and extraction artifacts remain outside this public repository.
