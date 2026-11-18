# 简明技术语言

[English](README.md) | 简体中文

面向支持基于文件的 `SKILL.md` 技能的任何 AI Agent 的中文优先技术写作规范。

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

```text
使用 simplified-technical-language 将以下内容改写成简明技术中文。保留必要英文，只输出最终版本。
```

```text
使用 simplified-technical-language 检查这份文档。输出问题表，不要修改原文。
```

中文技术写作、审查和术语检查也可能自动触发这个技能。

## 内容

- `SKILL.md` — 执行流程、优先级和输出模式。
- `references/style-guide.md` — 适用范围、规则、中英边界、检查清单和示例。
- `references/terms.md` — 可维护的个人术语表。
- `scripts/check_writing.py` — 可选启发式检查器，仅使用 Python 3 标准库。

```bash
python scripts/check_writing.py --doctype procedure document.md
python scripts/check_writing.py --selftest
```

检查器不联网。检查结果仅供参考，需要人工复核。

## 范围

ASD-STE100 只适用于英语。本项目把其原则适配为中文优先写作，与 ASD 无隶属关系，也不认证官方合规。中文的 40/50 计数单位句长阈值是本地默认值，不是官方 STE 换算。

官方参考：https://www.asd-ste100.org/about_STE.html
