#!/usr/bin/env python3
"""Utility script to audit lesson JSON files against the universal lesson prompt.

This check is intentionally strict so that we can quickly surface content that was
generated without following the production requirements in
``UNIVERSAL_LESSON_PROMPT.md``.  The script prints a human-readable report and
returns a non-zero exit code when violations are detected.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

VALID_DOMAINS = {
    "fundamentals",
    "osint",
    "dfir",
    "malware",
    "active_directory",
    "system",
    "linux",
    "cloud",
    "pentest",
    "red_team",
    "blue_team",
    "threat_hunting",
    "ai_security",
    "iot_security",
    "web3_security",
}

EXPECTED_JIM_KWIK = {
    "active_learning",
    "minimum_effective_dose",
    "teach_like_im_10",
    "memory_hooks",
    "meta_learning",
    "connect_to_what_i_know",
    "reframe_limiting_beliefs",
    "gamify_it",
    "learning_sprint",
    "multiple_memory_pathways",
}

REQUIRED_BLOCK_TYPES = [
    "explanation",
    "explanation",
    "code_exercise",
    "real_world",
    "memory_aid",
    "quiz",
    "reflection",
    "mindset_coach",
]

VALID_BLOCK_TYPES = {
    "explanation",
    "video",
    "diagram",
    "quiz",
    "simulation",
    "reflection",
    "memory_aid",
    "real_world",
    "code_exercise",
    "mindset_coach",
}


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


@dataclass
class LessonAudit:
    path: Path
    errors: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.errors.append(message)

    @property
    def ok(self) -> bool:
        return not self.errors


def iter_lessons(content_dir: Path) -> Iterable[Path]:
    yield from sorted(content_dir.glob("lesson_*_RICH.json"))


def validate_lesson(path: Path) -> LessonAudit:
    audit = LessonAudit(path)

    try:
        lesson = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        audit.add(f"Invalid JSON: {exc}")
        return audit

    # Basic metadata checks
    if lesson.get("domain") not in VALID_DOMAINS:
        audit.add(f"Invalid domain: {lesson.get('domain')!r}")

    if lesson.get("difficulty") not in {1, 2, 3}:
        audit.add(f"Difficulty must be 1, 2, or 3 (found {lesson.get('difficulty')!r})")

    estimated_time = lesson.get("estimated_time")
    if not isinstance(estimated_time, int) or not 30 <= estimated_time <= 60:
        audit.add(f"estimated_time must be an int between 30 and 60 (found {estimated_time!r})")

    prerequisites = lesson.get("prerequisites")
    if prerequisites is None or not isinstance(prerequisites, list):
        audit.add("prerequisites must be an array")

    concepts = lesson.get("concepts", [])
    if not (4 <= len(concepts) <= 8):
        audit.add(f"concepts must contain between 4 and 8 entries (found {len(concepts)})")

    jim_kwik_principles = lesson.get("jim_kwik_principles", [])
    if set(jim_kwik_principles) != EXPECTED_JIM_KWIK:
        missing = EXPECTED_JIM_KWIK.difference(jim_kwik_principles)
        extra = set(jim_kwik_principles).difference(EXPECTED_JIM_KWIK)
        if missing:
            audit.add(f"jim_kwik_principles missing: {sorted(missing)}")
        if extra:
            audit.add(f"jim_kwik_principles contain invalid values: {sorted(extra)}")

    # Assessment checks
    post_assessment = lesson.get("post_assessment", [])
    if not isinstance(post_assessment, list) or len(post_assessment) < 3:
        audit.add("post_assessment must include at least 3 questions")
    else:
        for idx, question in enumerate(post_assessment, start=1):
            if question.get("type") != "multiple_choice":
                audit.add(f"post_assessment question {idx} must be multiple_choice")
            options = question.get("options")
            if not isinstance(options, list) or len(options) != 4:
                audit.add(f"post_assessment question {idx} must provide exactly 4 options")
            correct = question.get("correct_answer")
            if correct not in {0, 1, 2, 3}:
                audit.add(f"post_assessment question {idx} must specify correct_answer 0-3")

    # Content block checks
    content_blocks = lesson.get("content_blocks", [])
    if len(content_blocks) < len(REQUIRED_BLOCK_TYPES):
        audit.add(
            f"content_blocks must contain at least {len(REQUIRED_BLOCK_TYPES)} entries (found {len(content_blocks)})"
        )

    type_counts = defaultdict(int)
    explanation_lengths: list[int] = []
    total_word_count = 0

    for block in content_blocks:
        block_type = block.get("type")
        type_counts[block_type] += 1

        if block_type not in VALID_BLOCK_TYPES:
            audit.add(f"Invalid content block type: {block_type!r}")

        content = block.get("content") or {}
        text = content.get("text", "")
        total_word_count += word_count(text)

        if block_type == "explanation":
            explanation_lengths.append(word_count(text))

    # Ensure required block pattern is present (at least the counts required in order)
    for required in REQUIRED_BLOCK_TYPES:
        if type_counts[required] == 0:
            audit.add(f"Missing required content block type: {required}")

    for idx, length in enumerate(explanation_lengths, start=1):
        if not 800 <= length <= 1200:
            audit.add(
                f"Explanation block {idx} should contain 800-1200 words (found {length})"
            )

    if not 4000 <= total_word_count <= 5500:
        audit.add(
            f"Total content word count should be 4,000-5,500 words (found {total_word_count})"
        )

    return audit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=CONTENT_DIR,
        help="Directory containing lesson_*.json files",
    )
    args = parser.parse_args()

    violations: list[LessonAudit] = []
    lesson_paths = list(iter_lessons(args.content_dir))
    for path in lesson_paths:
        audit = validate_lesson(path)
        if not audit.ok:
            violations.append(audit)

    if violations:
        print("=" * 80)
        print("LESSON PROMPT COMPLIANCE REPORT")
        print("=" * 80)
        for audit in violations:
            print(f"\n📄 {audit.path.relative_to(args.content_dir.parent)}")
            for error in audit.errors:
                print(f"  ❌ {error}")

        print("\nSUMMARY")
        print("=" * 80)
        print(f"Lessons checked: {len(lesson_paths)}")
        print(f"Lessons failing requirements: {len(violations)}")
        return 1

    print("All lessons comply with UNIVERSAL_LESSON_PROMPT.md requirements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
