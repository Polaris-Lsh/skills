# Simplified Technical Language

English | [简体中文](README.zh-CN.md)

Chinese-first technical writing for any AI agent that supports filesystem-based `SKILL.md` skills.

面向支持 `SKILL.md` 的 AI Agent 的中文技术写作规范。

## Install

Paste this into any agent with file and GitHub access:

```text
Install the Agent Skill at https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language into your user-level skills directory. Read `SKILL.md`, copy the whole folder, do not run bundled scripts, then report the install path and how to invoke it.
```

Works with WorkBuddy, Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, OpenCode, and other compatible agents. No API key is required.

CLI alternative:

```bash
npx -y skills add https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language -g -y
```

## Use

```text
Use simplified-technical-language to rewrite this text in concise technical Chinese. Keep necessary English and output only the final version.
```

```text
Use simplified-technical-language to review this document. Output a findings table; do not edit it.
```

The skill may also activate automatically for Chinese technical writing, review, and terminology checks.

## Contents

- `SKILL.md` — workflow, priorities, and output modes.
- `references/style-guide.md` — scope, rules, bilingual boundaries, checklist, and examples.
- `references/terms.md` — editable personal terminology.
- `scripts/check_writing.py` — optional heuristic checker using only the Python 3 standard library.

```bash
python scripts/check_writing.py --doctype procedure document.md
python scripts/check_writing.py --selftest
```

The checker makes no network calls. Its findings are advisory and require human review.

## Scope

ASD-STE100 applies to English. This project adapts its principles for Chinese-first writing and is not affiliated with ASD. It does not certify official compliance. The Chinese 40/50-unit sentence limits are local defaults, not an official STE conversion.

Official reference: https://www.asd-ste100.org/about_STE.html
