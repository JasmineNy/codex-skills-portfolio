#!/usr/bin/env python3
"""Check whether translated text follows the company terminology glossary."""

from __future__ import annotations

import argparse
import csv
import pathlib
import sys


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def split_forbidden(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def load_glossary(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters="\t,")
        reader = csv.DictReader(handle, dialect=dialect)
        rows = list(reader)

    required = {"source_term", "approved_english"}
    fieldnames = set(reader.fieldnames or [])
    missing = required - fieldnames
    if missing:
        joined = ", ".join(sorted(missing))
        raise ValueError(f"Glossary is missing required column(s): {joined}")
    return rows


def find_spans(text: str, needle: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    while True:
        idx = text.find(needle, start)
        if idx == -1:
            return spans
        spans.append((idx, idx + len(needle)))
        start = idx + max(len(needle), 1)


def span_covered(span: tuple[int, int], covered: list[tuple[int, int]]) -> bool:
    start, end = span
    return any(start >= cover_start and end <= cover_end for cover_start, cover_end in covered)


def forbidden_outside_approved(target_text: str, forbidden: str, approved: str) -> bool:
    forbidden_spans = find_spans(target_text, forbidden)
    if not forbidden_spans:
        return False
    approved_spans = find_spans(target_text, approved)
    return any(not span_covered(span, approved_spans) for span in forbidden_spans)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check approved English terms when source terms appear."
    )
    parser.add_argument("--glossary", required=True, type=pathlib.Path)
    parser.add_argument("--source", required=True, type=pathlib.Path)
    parser.add_argument("--target", required=True, type=pathlib.Path)
    args = parser.parse_args()

    source_text = read_text(args.source)
    target_text = read_text(args.target)
    rows = load_glossary(args.glossary)

    entries: list[tuple[int, dict[str, str], list[tuple[int, int]]]] = []
    for row in rows:
        source_term = row.get("source_term", "").strip()
        approved = row.get("approved_english", "").strip()
        if not source_term or not approved:
            continue
        spans = find_spans(source_text, source_term)
        if spans:
            entries.append((len(source_term), row, spans))

    issues: list[str] = []
    covered_source_spans: list[tuple[int, int]] = []
    for _, row, spans in sorted(entries, key=lambda item: item[0], reverse=True):
        source_term = row.get("source_term", "").strip()
        approved = row.get("approved_english", "").strip()
        uncovered_spans = [span for span in spans if not span_covered(span, covered_source_spans)]
        if not uncovered_spans:
            continue

        if approved not in target_text:
            issues.append(
                f"MISSING approved term: source '{source_term}' requires '{approved}'"
            )
        else:
            covered_source_spans.extend(spans)

        for forbidden in split_forbidden(row.get("forbidden_translations", "")):
            if forbidden_outside_approved(target_text, forbidden, approved):
                issues.append(
                    f"FORBIDDEN translation: '{forbidden}' appears; use '{approved}' for '{source_term}'"
                )

    if issues:
        print("Terminology issues found:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("No terminology issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
