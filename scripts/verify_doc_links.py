#!/usr/bin/env python3
"""Fail if a relative Markdown link points to a missing repository file."""

from __future__ import annotations

import re
import sys
from pathlib import Path


LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("#", "http://", "https://", "mailto:")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        for target in LINK.findall(document.read_text(encoding="utf-8")):
            target = target.strip().strip("<>")
            if target.startswith(SKIP_PREFIXES):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            if not (document.parent / path_part).resolve().exists():
                failures.append(f"{document.relative_to(root)} -> {target}")
    if failures:
        print("Broken relative Markdown links:", *failures, sep="\n")
        return 1
    print("All relative Markdown links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
