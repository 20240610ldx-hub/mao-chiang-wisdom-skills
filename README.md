# Mao + Chiang Wisdom Skills

Installable Codex Skills distilled from Mao Zedong and Chiang Kai-shek, packaged as a public GitHub column for decision-making, strategic reasoning, resilience, governance, and self-discipline analysis.

This repository publishes the finished skills only. Raw PDFs, source extraction artifacts, shard outputs, and pipeline internals are intentionally not included.

## 简体中文

### 项目简介

这是一个公开的 Codex Skills 专栏，收录两套可安装的思想家智慧技能：

- [毛泽东智慧 Skill](skills/mao-zedong-wisdom/SKILL.md)：适用于弱势方战略、高不确定性决策、矛盾分析、调查研究、实践反馈、群众路线与持久战规划。
- [蒋介石智慧 Skill](skills/chiang-kai-shek-wisdom/SKILL.md)：适用于资源受限下的战略忍耐、弱势方外交、组织整顿、自力自主、退省建攻与修身纪律。

这些 Skill 的目标不是表演式角色扮演，而是把人物的认知框架、表达纹理和价值取向提炼成可执行的推理方法。用户用中文提问时，Skill 会优先使用中文区；用户用英文或其他语言提问时，Skill 会优先使用英文区。

### 安装方式

将需要的目录复制到你的 Codex skills 目录，并确保每个目录内的文件名严格为 `SKILL.md`：

```text
skills/mao-zedong-wisdom/SKILL.md
skills/chiang-kai-shek-wisdom/SKILL.md
```

Codex 的 skill discovery 只识别准确命名的 `SKILL.md`。不要把文件改名为 `README.md`、`SKILL.zh.md` 或 `SKILL.en.md`。

### 质量状态

- 毛泽东 Skill：来源、原则、框架和 skill 校验通过；当前发布使用 `output/mao-zedong/SKILL.md` 作为 canonical 版本；runtime 评测为 imported evidence，尚未做完整自动 judge 复评。
- 蒋介石 Skill：skill 与 gallery 校验通过；output/gallery 哈希一致；已完成 12 轮 runtime evaluation，评分 `25/25`。

对话测试与评测记录见 [evaluations/](evaluations/)。

### 使用边界

这些 Skill 会避免伪造历史人物对身后事件、现代人物或未验证数据的具体判断。涉及在世政治人物、具体政策数字、法律事实或新闻事件时，Skill 应转向方法论分析，并提醒用户核验权威来源。

本项目不代表对任何政治人物的崇拜、背书或现实政治立场；它关注的是历史文本中可迁移的决策方法和行动框架。

## 繁體中文

### 專案簡介

這是一個公開的 Codex Skills 專欄，收錄兩套可安裝的思想家智慧技能：

- [毛澤東智慧 Skill](skills/mao-zedong-wisdom/SKILL.md)：適用於弱勢方戰略、高不確定性決策、矛盾分析、調查研究、實踐回饋、群眾路線與持久戰規劃。
- [蔣介石智慧 Skill](skills/chiang-kai-shek-wisdom/SKILL.md)：適用於資源受限下的戰略忍耐、弱勢方外交、組織整頓、自力自主、退省建攻與修身紀律。

這些 Skill 的目標不是表演式角色扮演，而是把人物的認知框架、表達紋理和價值取向提煉成可執行的推理方法。使用者用中文提問時，Skill 會優先使用中文區；使用者用英文或其他語言提問時，Skill 會優先使用英文區。

### 安裝方式

將需要的目錄複製到你的 Codex skills 目錄，並確保每個目錄內的檔名嚴格為 `SKILL.md`：

```text
skills/mao-zedong-wisdom/SKILL.md
skills/chiang-kai-shek-wisdom/SKILL.md
```

Codex 的 skill discovery 只識別準確命名的 `SKILL.md`。不要把檔案改名為 `README.md`、`SKILL.zh.md` 或 `SKILL.en.md`。

### 品質狀態

- 毛澤東 Skill：來源、原則、框架和 skill 校驗通過；目前發布使用 `output/mao-zedong/SKILL.md` 作為 canonical 版本；runtime 評測為 imported evidence，尚未做完整自動 judge 複評。
- 蔣介石 Skill：skill 與 gallery 校驗通過；output/gallery 雜湊一致；已完成 12 輪 runtime evaluation，評分 `25/25`。

對話測試與評測記錄見 [evaluations/](evaluations/)。

### 使用邊界

這些 Skill 會避免偽造歷史人物對身後事件、現代人物或未驗證資料的具體判斷。涉及在世政治人物、具體政策數字、法律事實或新聞事件時，Skill 應轉向方法論分析，並提醒使用者核驗權威來源。

本專案不代表對任何政治人物的崇拜、背書或現實政治立場；它關注的是歷史文本中可遷移的決策方法和行動框架。

## English

### Overview

This public Codex Skills column contains two installable thinker-wisdom skills:

- [Mao Zedong Wisdom Skill](skills/mao-zedong-wisdom/SKILL.md): for underdog strategy, high-uncertainty decisions, contradiction analysis, investigation, practice feedback, mass-line reasoning, and protracted engagement planning.
- [Chiang Kai-shek Wisdom Skill](skills/chiang-kai-shek-wisdom/SKILL.md): for strategic endurance under resource constraints, weak-side diplomacy, organizational reform, self-reliance, retreat-reflect-rebuild cycles, and self-discipline.

These skills are not theatrical roleplay. They distill cognitive frameworks, expressive texture, and value orientation into executable reasoning methods. When the user writes in Chinese, each skill should use its Chinese section; when the user writes in English or another language, it should use its English section.

### Installation

Copy the desired directory into your Codex skills directory, keeping the file name exactly as `SKILL.md`:

```text
skills/mao-zedong-wisdom/SKILL.md
skills/chiang-kai-shek-wisdom/SKILL.md
```

Codex skill discovery only recognizes the exact `SKILL.md` filename. Do not rename it to `README.md`, `SKILL.zh.md`, or `SKILL.en.md`.

### Quality Status

- Mao Zedong Skill: source, principle, framework, and skill validation passed; this release uses `output/mao-zedong/SKILL.md` as the canonical version; runtime evaluation is imported evidence and has not yet received a full automated judge rerun.
- Chiang Kai-shek Skill: skill and gallery validation passed; output/gallery hashes match; completed a 12-case runtime evaluation with a `25/25` score.

Dialogue tests and evaluation records are available in [evaluations/](evaluations/).

### Usage Boundaries

These skills should not fabricate a historical figure's concrete opinion about posthumous events, modern people, or unverified data. For living political figures, policy numbers, legal facts, or news events, the skill should shift to methodology-level analysis and ask the user to verify authoritative sources.

This project is not an endorsement, worship, or real-world political position toward any political figure. It focuses on decision methods and action frameworks that can be transferred from historical texts.

## License

MIT. See [LICENSE](LICENSE).
