# SkillEval-MDF-v1.1 Evaluation Report

Skill: `mao-zedong-wisdom`
Slug: `mao-zedong`
Evaluation Type: `Imported Runtime Evaluation`
Evaluation Date: `2026-05-15`
Evaluator: `mind-skill-evaluator`

## Executive Review

Overall Score: `79.0/100`
Grade: `B` - `promising, needs targeted revision`
Release Recommendation: `Release after artifact integrity cleanup`

One-line Judgment: `Usable prototype with targeted repairs required before broad release.`
Strongest Advantage: `Source Fidelity`
Largest Risk: `Runtime Robustness & Generalization`
Next Priority: `Improve Runtime Robustness & Generalization.`

## Visual Scorecard

| Metric | Score | Weight | Grade | Evidence | Bar |
|---|---:|---:|---|---|---|
| Source Fidelity | 12.0/12 | 12 | S | Source lineage or framework source lists are present. | ############### |
| Cognitive Distillation Depth | 11.6/12 | 12 | S | Framework principle counts are in range: [7, 6]. | ##############- |
| Operational Decision Utility | 12.0/12 | 12 | S | Skill includes a decision framework section. | ############### |
| Voice & Embodiment Authenticity | 12.0/12 | 12 | S | Expression DNA completeness: [10, 10]. | ############### |
| Boundary & Misuse Resistance | 12.0/12 | 12 | S | Boundary rules are present. | ############### |
| Runtime Robustness & Generalization | 10/25 | 25 | F (provisional) | Legacy dialogue logs available: 1. | ######--------- |
| Cross-Lingual & Cultural Fit | 8.0/8 | 8 | S | English section exists. | ############### |
| Engineering Reusability & Artifact Integrity | 5.0/7 | 7 | B | output/{slug}/SKILL.md exists. | ###########---- |

## Detailed Metric Review

### Source Fidelity

Score: `12.0/12`

Evidence:
- Source lineage or framework source lists are present.
- Framework source count: 19.
- 12/12 principles have supporting extracts.
- Existing quality review verdict is PASS.

Deductions:
- No material deductions found

Fix Priority: `P2`

### Cognitive Distillation Depth

Score: `11.6/12`

Evidence:
- Framework principle counts are in range: [7, 6].
- Average uniqueness score: 4.42.
- Reasoning patterns found across frameworks: 8.
- Decision framework exists.
- Values, anti-patterns, and tensions meet minimum counts.
- Distill confidence meets the project threshold.

Deductions:
- No material deductions found

Fix Priority: `P2`

### Operational Decision Utility

Score: `12.0/12`

Evidence:
- Skill includes a decision framework section.
- Framework has 5 decision steps.
- Decision-rule markers found: 22.
- Application examples are present.
- When-not-to-use guidance exists.

Deductions:
- No material deductions found

Fix Priority: `P2`

### Voice & Embodiment Authenticity

Score: `12.0/12`

Evidence:
- Expression DNA completeness: [10, 10].
- First-person embodiment rules are present.
- Anti-formula rules are present.
- Structural naturalness rules are present.
- Voice calibration examples are present.
- Paragraph rhythm and conversational markers are explicitly represented.

Deductions:
- No material deductions found

Fix Priority: `P2`

### Boundary & Misuse Resistance

Score: `12.0/12`

Evidence:
- Boundary rules are present.
- Posthumous-event boundary is present.
- Living-figure boundary is present.
- Data/fact verification boundary is present.
- Structural hardship guidance is present.
- Known Blind Spots section exists.
- Blind-spot mitigations found: 8.

Deductions:
- No material deductions found

Fix Priority: `P2`

### Runtime Robustness & Generalization

Score: `10/25`

Evidence:
- Legacy dialogue logs available: 1.

Deductions:
- No DeepSeek runtime judgment is available; legacy logs are provisional evidence only.

Fix Priority: `P1`

### Cross-Lingual & Cultural Fit

Score: `8.0/8`

Evidence:
- English section exists.
- Chinese section exists.
- Both zh/en framework JSON files are parseable.
- Frontmatter description is bilingual.
- Cultural context is represented.

Deductions:
- No material deductions found

Fix Priority: `P2`

### Engineering Reusability & Artifact Integrity

Score: `5.0/7`

Evidence:
- output/{slug}/SKILL.md exists.
- gallery/{slug}/SKILL.md exists.
- Validation stages passed: sources, principles, frameworks, skill.
- gallery/index.json contains an entry for this slug.

Deductions:
- Output and gallery SKILL.md hashes do not match or one side is missing.
- Validation stages failed: gallery.

Fix Priority: `P2`

## Initial Post-Distillation Assessment

This is a `Imported Runtime Evaluation`. Runtime claims are provisional: `True`. Dialogue logs: `1`; dialogue turns: `19`. Gallery sync: `False`.

## Failure Modes

1. Failure Mode: `Runtime Robustness & Generalization underperformance`
   Symptom: No DeepSeek runtime judgment is available; legacy logs are provisional evidence only.
   Risk: The Skill's practical value or maintainability is lower than its conceptual quality.
   Repair: Address the listed deductions and rerun the evaluator.

2. Failure Mode: `Runtime overclaiming`
   Symptom: Reports imply stable behavior without enough dialogue logs.
   Risk: A strong static Skill may still fail under multi-turn use.
   Repair: Add at least 8 varied test turns and review them against the post-review tuning guide.

3. Failure Mode: `Artifact drift`
   Symptom: Output and gallery copies diverge, or validation fails.
   Risk: Users may install a different Skill than the one that passed review.
   Repair: Resync artifacts or clearly mark which copy is canonical.

## Release Recommendation

Release Status: `Release after artifact integrity cleanup`
Packaging: `Ship as an independent evaluator skill and generated report bundle, not as a /distill gate.`
README Selling Points: `English rubric, visual scorecard, artifact integrity checks, runtime provisional labeling.`
Example Prompts: `Evaluate output/wang-yangming as a full SkillEval-MDF-v1 report.`
Disclaimers: `Runtime robustness is provisional without at least 8 dialogue turns.`

## P0/P1/P2 Roadmap

P0 Must Fix: `None`
P1 Strongly Recommended: `Runtime Robustness & Generalization`
P2 Later: `Source Fidelity, Cognitive Distillation Depth, Operational Decision Utility, Voice & Embodiment Authenticity, Boundary & Misuse Resistance, Cross-Lingual & Cultural Fit, Engineering Reusability & Artifact Integrity`
