# 简明技术语言

[English](README.md) | 简体中文

按需调用的中文简明表达 Skill，适用于支持基于文件的 `SKILL.md` 技能的 Agent。它帮助起草或轻量改写技术中文，同时保留原意和作者语气，不强制固定句长，也不要求完整执行 ASD-STE100 规则。

## 用途

- 没有原文时，从零起草中文技术内容。
- 有原文时，用尽量少的修改让文字更清楚、更简洁。
- 被要求时，只指出最影响理解的少数问题。
- 不介入普通聊天和未被要求的写作。
- 只有明确要求时，才进行严格规范性审查。

## 适用场景

适合中文技术笔记、README、设计说明、操作步骤、错误消息、报告等需要清楚表达的技术文本。不适用于文学、营销或说服性写作。

## 安装

把下面这段发给任何能访问文件和 GitHub 的 Agent：

```text
安装这个 Agent Skill：https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language。放入你的用户级 skills 目录，读取 `SKILL.md`，复制整个文件夹，不要运行附带脚本，然后报告安装路径和调用方式。
```

支持 WorkBuddy、Claude Code、Codex、Cursor、GitHub Copilot、Gemini CLI、OpenCode 等兼容 Agent。不需要 API Key。

也可以用 CLI：

```bash
npx -y skills add https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language -g -y
```

## 使用

### 从零起草

```text
使用 simplified-technical-language 为这个项目起草一段简明中文 README。只询问阻塞成稿的事实，只输出草稿。
```

### 轻量改写

```text
使用 simplified-technical-language 做一次轻量润色。保留原意、条件和必要英文，不强制句长，只输出最终文本。
```

### 严格审查

```text
使用 simplified-technical-language 按仓库内的规范做一次严格审查。只报告实质违规和待确认事实，不要修改原文。
```

这个 Skill 不会介入普通聊天。严格审查是单独的任务，只在文档必须满足严格规范时提出；轻量改写不会加载完整规则。

## 内容

- `SKILL.md` — 按需调用流程、核心规则，以及起草和改写分支。
- `references/style-guide.md` — 完整规则，仅在明确要求严格审查时加载。
- `references/terms.md` — 术语参考，仅在需要时加载。
- `scripts/check_writing.py` — 可选启发式检查器，仅使用 Python 3 标准库。

```bash
python scripts/check_writing.py --doctype procedure document.md
```

## 范围

ASD-STE100 只适用于英语。本项目把其原则适配为中文优先写作，与 ASD 无隶属关系，也不认证官方合规。默认模式有意比完整 STE 更轻。

官方参考：https://www.asd-ste100.org/about_STE.html
