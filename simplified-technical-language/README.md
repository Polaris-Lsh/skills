# Simplified Technical Language

English | [简体中文](README.zh-CN.md)

On-demand Chinese clear-writing skill for any agent that supports filesystem-based `SKILL.md` skills. It helps draft or lightly edit technical Chinese without changing the author's meaning or voice. It does not enforce fixed sentence lengths or full ASD-STE100 rules.

## What it does

- Drafts Chinese technical text from scratch when no source text exists.
- Makes existing text clearer and shorter through minimal edits.
- Gives focused feedback on the few issues that most affect understanding.
- Leaves ordinary chat and unprompted writing alone.
- Runs a strict normative review only when explicitly requested.

## When to use

Use it for Chinese technical notes, READMEs, design documents, procedures, error messages, reports, or other text where clarity matters. It is not intended for literary, marketing, or persuasive writing.

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

### Draft from scratch

```text
Use simplified-technical-language to draft a concise Chinese README section for this project. Ask only for facts that block the draft, and return the draft only.
```

### Light edit

```text
Use simplified-technical-language for one light clarity pass. Keep the meaning, conditions, and necessary English. Do not enforce sentence limits. Return only the final text.
```

### Strict review

```text
Use simplified-technical-language for a strict review against the bundled style guide. Report only material violations and unresolved facts; do not edit.
```

The skill is not applied to ordinary chat. A strict review is a separate task: request it only when the document must satisfy a strict standard. Light editing does not load the full rules.

## Contents

- `SKILL.md` — on-demand workflow, core rules, and drafting/editing branches.
- `references/style-guide.md` — full rules; load only for an explicitly requested strict review.
- `references/terms.md` — terminology reference; load only when needed.
- `scripts/check_writing.py` — optional heuristic checker using only the Python 3 standard library.

```bash
python scripts/check_writing.py --doctype procedure document.md
```

## Scope

ASD-STE100 applies to English. This project adapts its principles for Chinese-first writing and is not affiliated with ASD. It does not certify official compliance. The default mode is intentionally lighter than full STE.

Official reference: https://www.asd-ste100.org/about_STE.html
