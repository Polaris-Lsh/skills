#!/usr/bin/env python3
"""Validate skill metadata, repository documentation, and relative links."""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
LINK_PATTERN = re.compile(
    r"!?\[[^\]]*\]\((?:<([^>]+)>|([^)\s]+))(?:\s+['\"][^'\"]*['\"])?\)"
)


def clean_value(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        value = value[1:-1]
    return value


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("must start with a YAML frontmatter block")

    closing = text.find("\n---", 4)
    if closing == -1:
        raise ValueError("frontmatter has no closing ---")

    fields = {}
    parent = None
    for line in text[4:closing].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace():
            if parent == "metadata" and ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = clean_value(value)
            continue

        if ":" not in line:
            raise ValueError("invalid frontmatter line: %s" % line)

        parent = None
        key, value = line.split(":", 1)
        key = key.strip()
        value = clean_value(value)
        if key == "metadata" and not value:
            parent = "metadata"
        else:
            fields[key] = value

    return fields


def check_links(document, root, errors):
    text = document.read_text(encoding="utf-8-sig")
    for match in LINK_PATTERN.finditer(text):
        target = (match.group(1) or match.group(2)).strip()
        if not target or target.startswith(("#", "/", "mailto:", "data:")):
            continue
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue

        relative = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not relative:
            continue

        destination = (document.parent / relative).resolve()
        try:
            destination.relative_to(root)
        except ValueError:
            errors.append("%s: link escapes repository: %s" % (document, target))
            continue
        if not destination.exists():
            errors.append("%s: broken relative link: %s" % (document, target))


def check_required_file(path, errors):
    if not path.is_file():
        errors.append("missing required file: %s" % path)


def validate_skill(skill_dir, errors):
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        errors.append("missing SKILL.md: %s" % skill_dir)
        return None

    try:
        fields = read_frontmatter(skill_file)
    except ValueError as exc:
        errors.append("%s: %s" % (skill_file, exc))
        return None

    name = fields.get("name", "")
    description = fields.get("description", "")
    version = fields.get("version", "")

    if not NAME_PATTERN.fullmatch(name):
        errors.append("%s: name must use lowercase letters, digits, and hyphens" % skill_file)
    if name != skill_dir.name:
        errors.append("%s: name '%s' does not match folder '%s'" % (skill_file, name, skill_dir.name))
    if not description:
        errors.append("%s: description is required" % skill_file)
    elif len(description) > 1024:
        errors.append("%s: description exceeds 1024 characters" % skill_file)
    if not VERSION_PATTERN.fullmatch(version):
        errors.append("%s: metadata.version must be semantic version, got '%s'" % (skill_file, version))

    for filename in ("README.md", "README.zh-CN.md"):
        check_required_file(skill_dir / filename, errors)

    return {"name": name, "version": version, "path": skill_dir}


def discover_skills(root, requested):
    if requested:
        return [root / name for name in requested]
    return sorted(path.parent for path in root.glob("*/SKILL.md"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skill", action="append", help="Validate only this skill folder; repeat as needed.")
    parser.add_argument("--tag", help="Require the release tag to match every selected skill version.")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    errors = []
    skills = discover_skills(root, args.skill)

    for filename in ("README.md", "README.zh-CN.md", "LICENSE", "SECURITY.md", "CHANGELOG.md"):
        check_required_file(root / filename, errors)
    for filename in ("README.md", "README.zh-CN.md"):
        document = root / filename
        if document.is_file():
            check_links(document, root, errors)

    if not skills:
        errors.append("no skills found under %s" % root)

    names = set()
    versions = set()
    for skill_dir in skills:
        result = validate_skill(skill_dir, errors)
        if not result:
            continue
        if result["name"] in names:
            errors.append("duplicate skill name: %s" % result["name"])
        names.add(result["name"])
        versions.add(result["version"])
        for filename in ("README.md", "README.zh-CN.md"):
            document = skill_dir / filename
            if document.is_file():
                check_links(document, root, errors)

    if args.tag:
        tag_version = args.tag[1:] if args.tag.startswith("v") else args.tag
        if not VERSION_PATTERN.fullmatch(tag_version):
            errors.append("tag is not a semantic version: %s" % args.tag)
        elif versions != {tag_version}:
            errors.append(
                "tag %s does not match skill version(s): %s" %
                (args.tag, ", ".join(sorted(versions)) or "none")
            )

    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        print("Validation failed with %d error(s)." % len(errors), file=sys.stderr)
        return 1

    print("Validated %d skill(s): %s" % (len(skills), ", ".join(sorted(names))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
