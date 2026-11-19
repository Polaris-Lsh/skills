# Security Policy

## Supported versions

Only the latest released version of a skill receives security fixes. Older tags are kept for reproducibility but are not actively maintained.

## Reporting a vulnerability

Do not report security issues in a public issue.

Use GitHub's private vulnerability reporting:

https://github.com/Polaris-Lsh/skills/security/advisories/new

Include the affected skill and version, a minimal reproduction, the potential impact, and any suggested mitigation. Reports will be reviewed before details are disclosed publicly.

## Scope

This repository distributes instructions and scripts that run with the permissions of the agent that loads them. `simplified-technical-language/scripts/check_writing.py` uses only the Python standard library and makes no network calls, but an agent using the skill may still read local files or use other tools.

Review `SKILL.md` and bundled scripts before installing a version from an untrusted fork. Do not include credentials, tokens, private documents, or other secrets in issues, pull requests, examples, or test fixtures.
