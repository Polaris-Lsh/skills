#!/usr/bin/env python3
"""Heuristic checks for Chinese-first, STE-inspired technical prose.

This tool does not contain the official ASD-STE100 dictionary. It does not
certify compliance, prove semantic fidelity, or replace human review.
Only Python's standard library is required.
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    severity: str
    message: str
    excerpt: str


@dataclass
class Block:
    line: int
    text: str
    kind: str = "paragraph"
    numbered: bool = False


RULE_NAMES = {
    "semicolon",
    "long-sentence",
    "paragraph-length",
    "multiple-instructions",
    "vague-reference",
    "vague-wording",
    "promotional-language",
    "nominalization",
    "ambiguous-coordination",
    "double-negation",
    "chinese-passive",
    "english-passive",
    "english-contraction",
    "mixed-english",
}

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+")
LIST_ITEM = re.compile(r"^\s*(?P<marker>[-+*]|\d+[.)])\s+(?P<body>.*)$")
TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-{3,}")
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

CN_ACTIONS = (
    "重新构建", "重新启动", "打开", "关闭", "读取", "写入", "保存", "删除",
    "移除", "创建", "配置", "设置", "检查", "验证", "确认", "运行", "执行",
    "启动", "停止", "重启", "安装", "更新", "上传", "下载", "构建", "编译",
    "测试", "部署", "复制", "移动", "选择", "点击", "输入", "添加", "修改",
    "备份", "恢复", "提交", "推送", "拉取", "等待", "查看", "记录", "清理",
    "连接", "断开", "重试", "返回", "分析", "优化", "重建",
)
CN_ACTION = r"(?:" + "|".join(re.escape(item) for item in CN_ACTIONS) + r")"
CN_INSTRUCTION_START = re.compile(
    r"^(?:请\s*)?(?:不要|禁止|不得|避免|确保|" + CN_ACTION + r")"
)
CN_CONDITION = re.compile(r"^(?:如果|若|当)[^，。！？]*[，,]\s*(.+)$")
CN_MULTIPLE = re.compile(
    r"(?:然后|接着|随后|并且|同时)|并(?=" + CN_ACTION + r")|"
    r"[，,]\s*再\s*(?=" + CN_ACTION + r")"
)

EN_ACTIONS = (
    "add", "apply", "avoid", "attach", "check", "clean", "click", "close",
    "configure", "connect", "copy", "create", "define", "delete", "deploy",
    "disconnect", "download", "enter", "exclude", "include", "inspect",
    "install", "keep", "load", "make", "move", "open", "parse", "press",
    "pull", "push", "read", "rebuild", "remove", "replace", "report",
    "restart", "return", "review", "run", "save", "select", "send", "set",
    "start", "stop", "test", "update", "upload", "use", "verify", "wait",
    "write",
)
EN_INSTRUCTION_START = re.compile(r"^(?:" + "|".join(EN_ACTIONS) + r")\b", re.I)
EN_SECOND_ACTION = re.compile(
    r"\b(?:and\s+then|then|and)\s+(?:" + "|".join(EN_ACTIONS) + r")\b",
    re.I,
)

PASSIVE_EN = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+"
    r"(?:\w+ed|given|taken|made|done|found|seen|known|shown|written|built|"
    r"sent|set|run|read|kept|held|left|put|cut|lost|paid|said|sold|told|"
    r"thought|brought|bought|caught|taught|broken|chosen|driven|forgotten)\b",
    re.I,
)
CONTRACTION = re.compile(
    r"\b(?:don['’]t|can['’]t|won['’]t|isn['’]t|aren['’]t|doesn['’]t|"
    r"didn['’]t|couldn['’]t|shouldn['’]t|wouldn['’]t|it['’]s|"
    r"we['’]re|you['’]re|they['’]re)\b",
    re.I,
)

VAGUE_REFERENCE = re.compile(r"^(?:这|那)(?:使|导致|说明|意味着|会|可能|可以)")
VAGUE_WORDING = re.compile(
    r"相关|适当|酌情|等等|诸如此类|一定程度(?:上)?|某些|必要时|视情况而定"
)
PROMOTIONAL = re.compile(
    r"强大|无缝|极致|领先|革命性|颠覆性|轻松|一键|高效|智能|简单地|飞速|完美|最佳"
)
NOMINALIZATION = re.compile(
    r"对[^，。！？]{1,24}进行(?:分析|检查|验证|修改|处理|配置|优化|测试|部署|评估|实现|操作)"
    r"|进行(?:分析|检查|验证|修改|处理|配置|优化|测试|部署|评估|实现|操作)"
)
AMBIGUOUS_COORDINATION = re.compile(r"和/或|及/或|\band/or\b|\(s\)", re.I)
DOUBLE_NEGATION = re.compile(r"并非不|不得不|不是没有|并非没有")
MIXED_ENGLISH = re.compile(r"\b(?:cache|config|repo|log)\b", re.I)


def mask_inline(text):
    """Protect code and link targets while retaining one countable token."""
    text = re.sub(r"`[^`\n]+`", " CODE ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"<https?://[^>]+>", " URL ", text)
    text = re.sub(r"\bhttps?://[^\s)]+", " URL ", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def make_blocks(text):
    """Create Markdown-aware prose blocks and omit protected code."""
    lines = text.splitlines()
    blocks = []
    paragraph = []
    paragraph_line = 1
    in_fence = False
    in_frontmatter = bool(lines and lines[0].strip() == "---")

    def flush():
        nonlocal paragraph
        if paragraph:
            blocks.append(Block(paragraph_line, " ".join(paragraph), "paragraph"))
            paragraph = []

    for index, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if index == 1 and in_frontmatter:
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if FENCE.match(raw):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            flush()
            continue
        if HEADING.match(raw):
            flush()
            blocks.append(Block(index, stripped, "heading"))
            continue
        match = LIST_ITEM.match(raw)
        if match:
            flush()
            blocks.append(Block(
                index,
                match.group("body"),
                "list",
                match.group("marker")[0].isdigit(),
            ))
            continue
        if stripped.startswith(">"):
            flush()
            quote = re.sub(r"^\s*(?:>\s*)+", "", raw)
            if quote:
                blocks.append(Block(index, quote, "quote"))
            continue
        if TABLE_SEPARATOR.match(raw) or stripped.startswith("<"):
            flush()
            continue
        if raw.startswith("    ") or raw.startswith("\t"):
            flush()
            continue
        if not paragraph:
            paragraph_line = index
        paragraph.append(stripped)
    flush()
    return blocks


def split_sentences(text):
    """Split Chinese sentences and English terminal punctuation conservatively."""
    parts = re.split(r"(?<=[。！？!?])|(?<=[.])\s+", text)
    return [part.strip() for part in parts if part.strip()]


def count_units(text, chinese):
    """Count local Chinese units or English words; punctuation is excluded."""
    if chinese:
        han = len(CJK.findall(text))
        remainder = CJK.sub(" ", text)
        tokens = re.findall(r"[A-Za-z0-9]+(?:[-_./:+][A-Za-z0-9]+)*", remainder)
        return han + len(tokens)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-_./:+][A-Za-z0-9]+)*", text))


def looks_like_instruction(sentence, numbered, doctype):
    if doctype == "procedure":
        return True
    if doctype == "description":
        return False
    if numbered:
        return True
    clean = re.sub(r"^(?:警告|注意|说明|WARNING|CAUTION|NOTE)[:：.]?\s*", "", sentence.strip())
    if CJK.search(clean):
        if CN_INSTRUCTION_START.match(clean):
            return True
        condition = CN_CONDITION.match(clean)
        if condition:
            return bool(CN_INSTRUCTION_START.match(condition.group(1)))
        return False
    if EN_INSTRUCTION_START.match(clean):
        return True
    if clean.lower().startswith("if ") and "," in clean:
        return bool(EN_INSTRUCTION_START.match(clean.split(",", 1)[1].strip()))
    return False


def inside_parentheses(sentence, position):
    for match in re.finditer(r"[（(][^（）()]*[）)]", sentence):
        if match.start() < position < match.end():
            return True
    return False


def excerpt(text, limit=160):
    return text if len(text) <= limit else text[:limit - 3] + "..."


def analyze(path, text, doctype="auto", cn_instruction=40, cn_description=50):
    blocks = make_blocks(text)
    findings = []

    def add(block, rule, severity, message, sentence=None):
        findings.append(Finding(
            path,
            block.line,
            rule,
            severity,
            message,
            excerpt(sentence if sentence is not None else block.text),
        ))

    for block in blocks:
        if block.kind == "heading":
            continue
        masked = mask_inline(block.text)
        sentences = split_sentences(masked)
        if block.kind == "paragraph" and len(sentences) > 6:
            add(block, "paragraph-length", "error",
                "段落超过 6 句。按主题拆分段落。")

        for sentence in sentences:
            chinese = bool(CJK.search(sentence))
            instruction = looks_like_instruction(sentence, block.numbered, doctype)

            if ";" in sentence or "；" in sentence:
                add(block, "semicolon", "error",
                    "避免使用分号。按逻辑拆成独立句子。", sentence)

            if chinese:
                limit = cn_instruction if instruction else cn_description
                units = count_units(sentence, True)
                if units > limit:
                    add(block, "long-sentence", "error",
                        "中文%s有 %d 个计数单位，本地审查阈值为 %d。" %
                        ("操作句" if instruction else "描述句", units, limit),
                        sentence)
            else:
                limit = 20 if instruction else 25
                words = count_units(sentence, False)
                if words > limit:
                    add(block, "long-sentence", "error",
                        "英文%s有 %d 词，审查阈值为 %d。" %
                        ("操作句" if instruction else "描述句", words, limit),
                        sentence)

            if instruction:
                multiple = CN_MULTIPLE.search(sentence) if chinese else EN_SECOND_ACTION.search(sentence)
                if multiple:
                    add(block, "multiple-instructions", "warning",
                        "可能包含多个连续动作。除非动作同时发生，否则拆成独立步骤。", sentence)

            if chinese:
                if VAGUE_REFERENCE.search(sentence):
                    add(block, "vague-reference", "warning",
                        "句首指代可能指向整个前句。必要时重复明确的名词。", sentence)
                if VAGUE_WORDING.search(sentence):
                    add(block, "vague-wording", "warning",
                        "发现模糊限定词。给出判据、范围或具体对象。", sentence)
                if PROMOTIONAL.search(sentence):
                    add(block, "promotional-language", "warning",
                        "发现宣传或程度措辞。删除它，或给出可核验的判据。", sentence)
                if NOMINALIZATION.search(sentence):
                    add(block, "nominalization", "warning",
                        "发现名词化动作。语义相同时使用直接动词。", sentence)
                if DOUBLE_NEGATION.search(sentence):
                    add(block, "double-negation", "warning",
                        "发现双重否定。确认含义后改成直接表达。", sentence)
                if "被" in sentence:
                    add(block, "chinese-passive", "warning",
                        "可能使用被动语态。执行者已知且重要时，考虑主动语态。", sentence)
                for match in MIXED_ENGLISH.finditer(sentence):
                    if inside_parentheses(sentence, match.start()):
                        continue
                    add(block, "mixed-english", "warning",
                        "确认 '%s' 是否为必要英文。普通叙述优先使用术语表中的中文。" %
                        match.group(0), sentence)
            else:
                if PASSIVE_EN.search(sentence):
                    add(block, "english-passive", "warning",
                        "可能使用被动语态。仅在执行者未知或无关紧要时保留。", sentence)
                if CONTRACTION.search(sentence):
                    add(block, "english-contraction", "warning",
                        "展开英文缩写形式，保留完整形式。", sentence)

            if AMBIGUOUS_COORDINATION.search(sentence):
                add(block, "ambiguous-coordination", "warning",
                    "避免和/或、and/or 或 (s)。明确写出允许的组合或数量。", sentence)

    return findings


def selftest():
    cases = [
        ("semicolon", "打开文件；检查结果。", "semicolon", True),
        ("protected-code", "运行 `a;b`。", "semicolon", False),
        ("multiple-actions", "打开文件，然后检查结果。", "multiple-instructions", True),
        ("vague-reference", "服务更新缓存。这可能导致延迟。", "vague-reference", True),
        ("nominalization", "对日志进行分析。", "nominalization", True),
        ("coordination", "选择 A 和/或 B。", "ambiguous-coordination", True),
        ("mixed-english", "在 config 里设置 cache。", "mixed-english", True),
        ("protected-identifiers", "在 `config` 里设置 `cache`。", "mixed-english", False),
        ("english-passive", "The file is deleted by the agent.", "english-passive", True),
        ("double-negation", "这个配置并非不能修改。", "double-negation", True),
        ("clean-chinese", "如果缓存为空，重新构建索引。", None, False),
        ("clean-english", "If the cache is empty, rebuild the index.", None, False),
    ]
    for name, text, rule, expected in cases:
        rules = {finding.rule for finding in analyze("<selftest>", text)}
        if rule is None:
            assert not rules, "%s: unexpected findings %s" % (name, sorted(rules))
        elif expected:
            assert rule in rules, "%s: missing %s" % (name, rule)
        else:
            assert rule not in rules, "%s: unexpected %s" % (name, rule)

    long_cn = "该模块" + "处理用户上传的实验数据并生成对应的分析结果" * 3 + "。"
    assert "long-sentence" in {
        finding.rule for finding in analyze("<selftest>", long_cn)
    }, "long Chinese sentence was not detected"

    long_en = (
        "Open the file and read every line before you save the final version "
        "of the report in the shared project folder today."
    )
    assert "long-sentence" in {
        finding.rule for finding in analyze("<selftest>", long_en)
    }, "long English instruction was not detected"

    paragraph = "第一句说明对象。" * 7
    assert "paragraph-length" in {
        finding.rule for finding in analyze("<selftest>", paragraph)
    }, "long paragraph was not detected"
    print("Self-test passed: 15 cases.")


def parse_disable(value, parser):
    disabled = {item.strip() for item in value.split(",") if item.strip()}
    unknown = disabled - RULE_NAMES
    if unknown:
        parser.error("Unknown rule(s): %s" % ", ".join(sorted(unknown)))
    return disabled


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check Chinese-first, STE-inspired prose. No certification or dictionary check."
    )
    parser.add_argument("files", nargs="*", help="UTF-8 text or Markdown files. Omit to read stdin.")
    parser.add_argument("--doctype", choices=("auto", "procedure", "description"), default="auto")
    parser.add_argument("--json", action="store_true", help="Write one JSON report to stdout.")
    parser.add_argument("--baseline", type=int, default=0, help="Allowed error findings before exit 1.")
    parser.add_argument("--disable", default="", metavar="RULES", help="Comma-separated rule names.")
    parser.add_argument("--cn-instruction", type=int, default=40, metavar="N")
    parser.add_argument("--cn-description", type=int, default=50, metavar="N")
    parser.add_argument("--selftest", action="store_true", help="Run built-in regression tests.")
    args = parser.parse_args(argv)

    if args.baseline < 0:
        parser.error("--baseline must be zero or greater")
    if args.cn_instruction <= 0 or args.cn_description <= 0:
        parser.error("Chinese sentence thresholds must be greater than zero")
    disabled = parse_disable(args.disable, parser)

    if args.selftest:
        selftest()
        return 0

    sources = []
    if args.files:
        for name in args.files:
            try:
                sources.append((name, Path(name).read_text(encoding="utf-8-sig")))
            except (OSError, UnicodeError) as exc:
                print("%s: %s" % (name, exc), file=sys.stderr)
                return 2
    else:
        sources.append(("<stdin>", sys.stdin.read()))

    findings = []
    for name, text in sources:
        findings.extend(analyze(
            name,
            text,
            args.doctype,
            args.cn_instruction,
            args.cn_description,
        ))
    findings = [finding for finding in findings if finding.rule not in disabled]
    findings.sort(key=lambda item: (item.file, item.line, item.rule, item.excerpt))
    errors = sum(finding.severity == "error" for finding in findings)
    warnings = sum(finding.severity == "warning" for finding in findings)

    if args.json:
        print(json.dumps({
            "errors": errors,
            "warnings": warnings,
            "findings": [asdict(finding) for finding in findings],
            "notice": "Heuristic checks only. Not official ASD-STE100 certification.",
        }, ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print("%s:%d: %s %s: %s" % (
                finding.file,
                finding.line,
                finding.severity.upper(),
                finding.rule,
                finding.message,
            ))
            print("  " + finding.excerpt)
        print("Summary: %d error(s), %d warning(s)." % (errors, warnings))
        print("Scope: heuristic checks only, not official STE certification.")
    return 1 if errors > args.baseline else 0


if __name__ == "__main__":
    sys.exit(main())
