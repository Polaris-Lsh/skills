# Skills

[English](README.md) | 简体中文

一组按需调用的 Agent Skills，适用于支持基于文件的 `SKILL.md` 的 AI Agent。

## 可用技能

### Simplified Technical Language

中文简明表达 Skill，用于从零起草、轻量改写和可选的严格审查。

- 只在明确要求时调用，不自动介入普通聊天。
- 没有原文时直接起草。
- 保留事实、条件、代码和作者语气。
- 只有明确要求时才做严格规范性审查。

阅读 [中文说明](simplified-technical-language/README.zh-CN.md) 或 [English guide](simplified-technical-language/README.md)。

## 安装

把下面这段发给能访问文件和 GitHub 的 Agent：

```text
安装这个 Agent Skill：https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language。放入你的用户级 skills 目录，读取 `SKILL.md`，复制整个文件夹，不要运行附带脚本，然后报告安装路径和调用方式。
```

也可以用 CLI：

```bash
npx -y skills add https://github.com/Polaris-Lsh/skills/tree/main/simplified-technical-language -g -y
```

## 更新

更新由 CLI 管理的全局安装：

```bash
npx -y skills update simplified-technical-language -g -y
```

手动导入到 Agent 的 Skill 需要手动替换。需要固定在某个版本时，请从版本 tag 安装，不要使用 `main`。见 [Releases](https://github.com/Polaris-Lsh/skills/releases)。

## 仓库结构

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

## 质量与安全

推送和针对 `main` 的 Pull Request 会运行仓库校验及检查器自测。附带脚本不得依赖密钥，也不得进行未声明的网络访问。

安全问题请按 [SECURITY.md](SECURITY.md) 私下报告。

## 许可证

[MIT](LICENSE)
