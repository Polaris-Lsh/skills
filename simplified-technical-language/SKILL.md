---
name: simplified-technical-language
description: "Write, rewrite, and review Chinese-first technical prose with executable ASD-STE100-inspired rules, retaining or generating English only when necessary. This skill should be used for 中文技术写作、简明中文、技术笔记、README、设计说明、实验记录、操作步骤、错误说明、提示词、报告润色、术语统一、语言规范检查、中英混写边界、STE 中文适配， and bilingual technical rewriting. It preserves technical meaning and never claims official ASD-STE100 compliance for Chinese. It is not for literary, marketing, or persuasive copy."
agent_created: true
metadata:
  version: 1.0.0
---

# 中文优先的 STE 启发式写作

## 目标

用明确、简短、一致的中文写技术内容。仅在代码、标识符、界面原文、标准名称、必要术语或目标读者需要时保留或使用英文。

把本规范视为 ASD-STE100 Issue 9 的本地适配，不视为官方翻译或认证方案。STE 只规范英语。未经官方标准和受控词典核验，不声称文本“符合 ASD-STE100”或“通过 STE 认证”。

## 选择任务

- **写作**：直接写可使用的中文成稿，不先展示冗长草稿。
- **改写**：保留事实和技术含义，只调整表达。默认只输出最终文本。
- **检查**：报告问题、位置、依据和建议，不直接改原文。
- **对照**：只列出实际改动，给出原文、改写和规则编号。
- **必要英译**：先还原事实和逻辑，再写 STE 风格英文。需要完整英文规则时，配合使用可用的英文 STE 规范，不得声称官方合规。

未指定任务时，根据动词判断：出现“检查、审查、lint”时执行检查；出现“对照、依据、为什么”时执行对照；其余润色请求执行改写。

## 遵守优先级

1. 保留事实、条件、例外、范围、否定、数字、单位和引用。
2. 保留要求强度和不确定性。不得互换“必须、不得、建议、可以、可能、预计”。
3. 保留代码、命令、标识符、路径、URL、产品名、界面标签和 Markdown 结构。
4. 明确执行者、动作、对象、条件和结果，消除歧义。
5. 统一术语和句式。
6. 缩短文本。不得为缩短而删除必要信息。

无法确认技术含义时，保留原文并提出一个具体问题。不得猜测执行者、原因、步骤、风险或结论。

## 执行流程

1. 识别读者、文本类型、执行者、动作、条件、结果和风险。
2. 读取 `references/style-guide.md`，应用其中的规则编号和检查清单。
3. 读取 `references/terms.md`，统一已有术语。发现新术语时，先保持全文一致，再建议加入术语表。
4. 把连续动作拆成编号步骤，把条件放在动作前，把警告放在相关操作前。
5. 默认使用中文叙述。按中英文边界保留必要英文，不逐句生成中英双文。
6. 逐句回读原文，核对事实、逻辑、情态、数字、单位和受保护内容。
7. 对本地文件或明确要求的机械检查运行 `scripts/check_writing.py`，再进行人工语义复核。短文本可直接检查，不为运行脚本创建临时文件。

## 输出格式

### 写作或改写

只输出可直接使用的成稿。保留标题、列表、表格、代码块和其他 Markdown 结构。原文已经清晰时原样返回，不制造修改。

无法安全改写的句子保持原样，并在成稿后加一行 `保留原文：...`，说明需要确认的问题。

### 检查

```markdown
| 位置 | 严重度 | 规则 | 问题 | 建议 |
|---|---|---|---|---|
| 第 2 句 | 应改 | S1 / 单句单动作 | 一个步骤包含两个连续动作 | 拆成两个编号步骤 |
```

在表后分别列出：

- **必须人工确认**：可能改变技术含义的歧义。
- **检查器未覆盖**：术语语义、事实保真、修饰关系、代词指向和必要英文。
- **无问题项**：仅在有助于审查时简述，不编造问题。

没有发现问题时，写“未发现本规范可检查的语言问题”，不要写“完全符合 STE”。

### 对照

```markdown
| 原文 | 改写 | 依据 |
|---|---|---|
| 对日志进行分析。 | 分析日志。 | V2 / 使用直接动词 |
```

只展示实际改动。最后单列保留原文的句子及原因。

## 使用检查器

将 `<skill-dir>` 替换为本 Skill 所在目录：

```bash
python <skill-dir>/scripts/check_writing.py document.md
python <skill-dir>/scripts/check_writing.py --doctype procedure document.md
python <skill-dir>/scripts/check_writing.py --json document.md
python <skill-dir>/scripts/check_writing.py --selftest
```

检查器只提供启发式初筛。中文指令句默认 40 个计数单位，中文描述句默认 50 个计数单位；英文分别采用 20 词和 25 词。中文阈值是本地建议，不是官方换算。可通过参数调整。

退出码 `0` 不表示官方合规，退出码 `1` 表示硬性结构发现超过基线，退出码 `2` 表示参数或文件错误。所有警告都需要结合语境复核。

## 维护规范

- 把稳定的个人用词决定写入 `references/terms.md`，记录定义和使用条件。
- 把反复出现的语言问题转化为带编号的规则，加入 `references/style-guide.md`。
- 把一次性语境偏好留在当前任务中，不固化为全局规则。
- 修改规则后运行检查器自测，并用一组真实文本验证误报。
- 不复制官方受控词典，不把个人词表称为官方批准词汇。
