---
name: simplified-technical-language
description: "Chinese clear-writing skill for explicit use. Use when the user names simplified-technical-language or explicitly asks for clear, concise Chinese drafting, rewriting, or a light editing pass. Draft directly when no source text exists. Do not apply to ordinary chat or unprompted review. Run the full normative audit only when the user explicitly asks to verify strict conformance. Never claim official ASD-STE100 certification."
metadata:
  version: 1.0.1
---

# 按需使用的简明表达

用于中文为主的技术内容的起草和轻量改写。仅在用户点名本 Skill，或明确要求“写清楚、写简洁、轻量润色”时使用。普通对话不套用本规范；原文已经清楚时原样返回。

## 核心规则

1. 先保留事实、条件、例外、否定、数字、单位和语气。
2. 保留代码、命令、路径、标识符、界面原文和 Markdown 结构。
3. 一句话只表达一个中心。
4. 主体和动作不清楚时才补明；自然的被动句不必改主动。
5. 条件放在动作前，连续步骤按实际顺序写。
6. 同一事物使用同一名称，不轮换近义词。
7. 删除空话、重复和无依据的形容。
8. 句子难懂时才拆，不以固定字数为目标。
9. 保留作者原本的语气，不强制改变段落长度或输出格式。
10. 不为简短删除信息，不添加原文没有的原因、结论或风险。

## 工作流程

先判断是否存在原文。

- **有原文**：完整阅读，确认条件、数字、否定和受保护内容；只做理解所必需的修改；完成后回读，核对含义没有变化。
- **无原文，需要从零起草**：确认主题、读者和必须包含的事实。信息足够就直接写；缺少会阻塞成稿的关键信息时集中询问，无法确认的内容标记“待确认”，不得编造。直接按核心规则起草，不虚构原文，也不输出改写对照。

无法确认含义时保留原文或标记待确认，只问真正阻塞任务的问题。

## 严格审查（仅在明确要求时）

只有用户明确要求“确保文档符合严格规范”或“按完整规则核对”时，才进入本流程，并读取 `references/style-guide.md`。普通的“检查一下、润色一下”不属于严格审查，不加载完整规则。

审查时仅针对用户指定的标准；未指定时使用本仓库的可选规则，并说明它不是官方标准。需要统一术语时读取 `references/terms.md`；用户明确要求机械检查时才运行 `scripts/check_writing.py`。

默认最多报告 5 个最影响理解、事实保真或明确规范要求的问题，不逐条挑错，不把句长、被动语态或个人风格偏好当作必改项。未经用户要求，不直接修改原文。检查器和本 Skill 都不能证明技术含义正确或官方合规。

## 输出

默认只输出最终成稿，不附加规则说明、自评或修改理由。用户要求对比时，再列原文、改写和实际依据。审查任务按问题表输出，并单列必须人工确认的语义风险。
