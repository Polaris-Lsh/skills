# Skills

English | [简体中文](README.zh-CN.md)

A small collection of on-demand skills for AI agents that support filesystem-based `SKILL.md`.

## Available skills

### Simplified Technical Language

Chinese clear-writing skill for drafting, light editing, and optional strict review.

- Invoked explicitly; it does not apply itself to ordinary chat.
- Drafts directly when no source text exists.
- Preserves facts, conditions, code, and author voice.
- Strict normative review only on request.

Read the [English guide](simplified-technical-language/README.md) or [中文说明](simplified-technical-language/README.zh-CN.md).

## Install

Paste this into an agent with file and GitHub access:

```text
Install the Agent Skill at https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language into your user-level skills directory. Read `SKILL.md`, copy the whole folder, do not run bundled scripts, then report the install path and how to invoke it.
```

CLI alternative:

```bash
npx -y skills add https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language -g -y
```

## Update

Update a CLI-managed global installation:

```bash
npx -y skills update simplified-technical-language -g -y
```

Skills imported manually into an agent must be replaced manually. To stay on a fixed version, install from a version tag instead of `main`. See [Releases](https://github.com/Polaris-Lsh/skills/releases).

## Repository layout

```text
skills/
├── simplified-technical-language/
│   ├── SKILL.md
│   ├── README.md
│   ├── README.zh-CN.md
│   ├── references/
│   └── scripts/
├── scripts/validate_repo.py
├── .github/workflows/
├── CHANGELOG.md
├── SECURITY.md
└── LICENSE
```

## Quality and security

Pull requests and pushes to `main` run repository validation and the checker's self-tests. Bundled scripts must not require secrets or make undeclared network calls.

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
