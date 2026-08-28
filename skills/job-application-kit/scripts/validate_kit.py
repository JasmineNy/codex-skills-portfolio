#!/usr/bin/env python3
"""Validate a text-only job-application kit response."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


REQUIRED_HEADINGS = [
    "## 岗位结论",
    "## 分段打招呼话术",
    "## 简历推荐",
    "## 已读未回跟进",
    "## 素材状态",
]
FALSE_ATTACHMENT_PATTERN = re.compile(r"已附(?:上|件)|请查收|已发送|附件(?:中|里)")
FORBIDDEN_OUTPUT_PATTERN = re.compile(r"output/job-application-kits|已生成.{0,8}(?:文件夹|投递包)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a text-only job-application kit")
    parser.add_argument("input_file", nargs="?", type=Path, help="UTF-8 response file; omit to read stdin")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def extract_marker(text: str, name: str) -> str | None:
    pattern = re.compile(
        rf"<!--\s*{re.escape(name)}:start\s*-->(.*?)<!--\s*{re.escape(name)}:end\s*-->",
        re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def compact_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def paragraph_count(text: str) -> int:
    return len([part for part in re.split(r"\n\s*\n", text.strip()) if part.strip()])


def validate(text: str) -> dict[str, object]:
    errors: list[str] = []
    checks: dict[str, object] = {}

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"Missing required heading: {heading}")

    for marker, minimum, maximum, required_paragraphs in [
        ("greeting", 80, 140, 3),
        ("one-shot", 80, 140, 3),
        ("follow-up", 30, 80, 1),
    ]:
        value = extract_marker(text, marker)
        if value is None:
            errors.append(f"Missing message marker: {marker}")
            continue
        length = compact_length(value)
        paragraphs = paragraph_count(value)
        checks[f"{marker}_length"] = length
        checks[f"{marker}_paragraphs"] = paragraphs
        if not minimum <= length <= maximum:
            errors.append(f"{marker} length {length} is outside {minimum}-{maximum}")
        if paragraphs < required_paragraphs:
            errors.append(f"{marker} must contain at least {required_paragraphs} paragraph(s)")

    if FALSE_ATTACHMENT_PATTERN.search(text):
        errors.append("Response falsely claims an attachment is available or sent")
    if FORBIDDEN_OUTPUT_PATTERN.search(text):
        errors.append("Text-only mode must not claim a per-job folder or package was created")
    if "AI作品集：未登记" not in text:
        errors.append("Material status must state AI作品集：未登记")
    if "专业图：未登记" not in text:
        errors.append("Material status must state 专业图：未登记")
    if not re.search(r"(主选|修订后主选).{0,120}(ready|可直接投递|需修订|暂不可直接投递)", text, re.DOTALL):
        errors.append("Resume recommendation must include a primary selection and readiness label")

    return {"status": "pass" if not errors else "fail", "errors": errors, "checks": checks}


def fixture() -> str:
    return """## 岗位结论

匹配度82分，建议优先投递。优势是伙伴经营和经营分析；差距是收入结果所有权。

## 分段打招呼话术

### BOSS分段版
<!-- greeting:start -->
您好，关注到贵司生态运营岗位，我有5年以上企业科技行业经验。

长期负责伙伴分层经营、联合BP及经营指标分析，也能协同销售和产品推动复杂事项闭环。

曾负责37+项指标并推动经营驾驶舱上线。如方向匹配，希望有机会进一步交流。
<!-- greeting:end -->

### 首条一次发全版
<!-- one-shot:start -->
您好，关注到贵司生态运营岗位，我有5年以上ToB企业科技经验。

经历覆盖伙伴经营、渠道治理与经营分析，能够连接总部、销售、产品和合作伙伴。

曾负责37+项指标及经营驾驶舱业务设计。如岗位仍在招聘，期待进一步沟通。
<!-- one-shot:end -->

## 简历推荐

- 主选（ready，可直接投递）：阿里云销售运营版。
- 备选（需修订）：渠道运营经理版。

## 已读未回跟进
<!-- follow-up:start -->
您好，补充说明一下，我也做过伙伴经营驾驶舱和跨区域项目。如岗位仍在招聘，希望有机会进一步交流。
<!-- follow-up:end -->

## 素材状态

- AI作品集：未登记
- 专业图：未登记
"""


def self_test() -> int:
    positive = validate(fixture())
    unsafe = validate(fixture().replace("希望有机会进一步交流。", "已附上简历，希望有机会进一步交流。", 1))
    result = {
        "status": "pass" if positive["status"] == "pass" and unsafe["status"] == "fail" else "fail",
        "text_fixture": positive,
        "false_attachment_fixture": unsafe,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


def main() -> int:
    args = parse_args()
    if args.self_test:
        return self_test()
    if args.input_file:
        text = args.input_file.expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    result = validate(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
