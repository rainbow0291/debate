#!/usr/bin/env python3
"""
PostToolUse hook for the news-issue-debate plugin.

Fires after a Write tool call. If the written file looks like an issue-brief
draft (filename contains "issue-brief" and ends in .md), do a cheap heuristic
check that both the 찬성 and 반대 sections either contain a source link/name
or explicitly say 확인 불가 — instead of being empty/unsourced. This is a
safety net against a half-finished brief slipping out, not a substitute for
actually reading the content.

Exit code convention (Claude Code hooks): 0 = allow, 2 = block and feed the
stderr message back to Claude as the reason, anything else = non-blocking
warning shown to the user only.
"""
import json
import os
import re
import sys


def read_hook_input():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def looks_like_issue_brief(file_path):
    if not file_path:
        return False
    name = os.path.basename(file_path).lower()
    return "issue-brief" in name and name.endswith(".md")


def section_text(content, header_pattern):
    """Grab the text between a section header and the next '###' or '---'."""
    m = re.search(header_pattern + r"(.*?)(\n###|\n---|\Z)", content, re.S)
    return m.group(1) if m else ""


def section_ok(text):
    if not text.strip():
        return False
    if "확인 불가" in text:
        return True
    # crude "has a source" signal: a URL, or a bullet with an em/en dash
    # followed by something (used as "argument — source" in the template)
    return bool(re.search(r"https?://", text)) or bool(re.search(r"[-–—]\s*\S", text))


def main():
    data = read_hook_input()
    if data.get("tool_name") != "Write":
        sys.exit(0)

    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path", "")
    if not looks_like_issue_brief(file_path):
        sys.exit(0)

    content = tool_input.get("content")
    if content is None:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            sys.exit(0)  # can't read it, don't block on a guess

    pro_text = section_text(content, r"###\s*찬성.*?논거")
    con_text = section_text(content, r"###\s*반대.*?논거")

    problems = []
    if not pro_text.strip():
        problems.append("찬성 논거 섹션(### 찬성 측 논거)이 없습니다.")
    elif not section_ok(pro_text):
        problems.append(
            "찬성 논거에 출처(링크 등)가 보이지 않습니다. 출처를 달거나, "
            "정말 못 찾았다면 '확인 불가'라고 명시하세요."
        )

    if not con_text.strip():
        problems.append("반대 논거 섹션(### 반대 측 논거)이 없습니다.")
    elif not section_ok(con_text):
        problems.append(
            "반대 논거에 출처(링크 등)가 보이지 않습니다. 출처를 달거나, "
            "정말 못 찾았다면 '확인 불가'라고 명시하세요."
        )

    if problems:
        sys.stderr.write(
            "issue-brief 균형 검사 실패:\n- " + "\n- ".join(problems) +
            "\n출처 없이 발송/출력하지 말고 위 사항을 보완하세요."
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
