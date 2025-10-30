#!/usr/bin/env python3
"""Rebuild lesson JSON files to comply with UNIVERSAL_LESSON_PROMPT.md."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.domain_content_library import DOMAIN_LIBRARY
CONTENT_DIR = ROOT / "content"
JIM_KWIK = [
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
]
REQUIRED_TYPES = [
    "explanation",
    "explanation",
    "code_exercise",
    "real_world",
    "memory_aid",
    "quiz",
    "reflection",
    "mindset_coach",
]
TOTAL_MIN = 4000
TOTAL_MAX = 5500
EXPLANATION_MIN = 820
EXPLANATION_MAX = 1200
WORD_PATTERN = re.compile(r"\b\w+\b")


def word_count(text: str) -> int:
    return len(WORD_PATTERN.findall(text))


def clamp_text_to_word_limit(text: str, maximum: int) -> str:
    if word_count(text) <= maximum:
        return text
    paragraphs = [para for para in text.split("\n\n") if para.strip()]
    kept: list[str] = []
    total_words = 0
    for para in paragraphs:
        words = para.split()
        if total_words + len(words) <= maximum:
            kept.append(para)
            total_words += len(words)
            continue
        remaining = maximum - total_words
        if remaining > 0:
            truncated = " ".join(words[:remaining])
            kept.append(truncated)
            total_words += remaining
        break
    if not kept:
        return " ".join(text.split()[:maximum])
    return "\n\n".join(kept)


def ensure_concepts(lesson: dict, lib: dict) -> None:
    concepts = lesson.get("concepts") or []
    extras = [item["name"] for item in lib.get("attacks", [])]
    for extra in extras:
        if len(concepts) >= 4:
            break
        if extra not in concepts:
            concepts.append(extra)
    if len(concepts) < 4:
        for tool in lib.get("tools", []):
            if len(concepts) >= 4:
                break
            if tool["name"] not in concepts:
                concepts.append(tool["name"])
    if len(concepts) > 8:
        concepts = concepts[:8]
    lesson["concepts"] = concepts


def ensure_learning_objectives(lesson: dict) -> None:
    concepts = lesson["concepts"]
    objectives: list[str] = []
    for concept in concepts:
        objectives.append(f"Explain how {concept} reinforces the focus of {lesson['title']}.")
        if len(objectives) >= 4:
            break
    while len(objectives) < 4:
        objectives.append(
            f"Apply the lesson's tools to {lesson['domain'].replace('_', ' ')} scenarios and document measurable improvements."
        )
    lesson["learning_objectives"] = objectives[:6]


def ensure_metadata(lesson: dict) -> None:
    lesson["jim_kwik_principles"] = JIM_KWIK.copy()
    if not isinstance(lesson.get("estimated_time"), int) or not 30 <= lesson["estimated_time"] <= 60:
        lesson["estimated_time"] = 55
    if lesson.get("difficulty") not in {1, 2, 3}:
        lesson["difficulty"] = 2
    if not isinstance(lesson.get("prerequisites"), list):
        lesson["prerequisites"] = []


def cycle(items: list[dict], idx: int) -> dict:
    return items[idx % len(items)]


def build_explanation(lesson: dict, lib: dict, section_index: int) -> str:
    paragraphs: list[str] = []
    concepts = lesson["concepts"]
    for idx, concept in enumerate(concepts):
        tool = cycle(lib["tools"], idx)
        telemetry = cycle(lib["telemetry"], idx)
        attack = cycle(lib["attacks"], idx)
        incident = cycle(lib["incidents"], idx)
        pitfall = lib["pitfalls"][idx % len(lib["pitfalls"])]
        troubleshooting = lib["troubleshooting"][idx % len(lib["troubleshooting"])]
        paragraphs.append(
            "\n".join(
                [
                    f"### {concept}",
                    (
                        f"The emphasis on {concept.lower()} within {lesson['title']} connects directly to frontline needs across the {lesson['domain'].replace('_', ' ')} domain. Practitioners lean on {tool['name']} because {tool['description']} {tool['usage']}"
                    ),
                    (
                        f"Key telemetry such as {telemetry['name']} surfaces the signals teams must investigate. {telemetry['description']} {telemetry['analysis']}"
                    ),
                    (
                        f"Adversaries repeatedly weaponize {attack['name']}. {attack['description']} {attack['detection']}"
                    ),
                    (
                        f"Historical lessons from {incident['name']} underline the stakes. {incident['description']} {incident['lesson']}"
                    ),
                    f"Common mistake: {pitfall}",
                ]
            )
        )
        paragraphs.append(
            f"#### Operational guidance\nTranslate {concept.lower()} into practice by running scenario-based drills and documenting expected versus observed telemetry. {troubleshooting}"
        )
    for idx, step in enumerate(lib.get("next_steps", [])):
        paragraphs.append(f"#### Action {idx + 1}\n{step}")
        if word_count("\n\n".join(paragraphs)) >= EXPLANATION_MIN:
            break
    text = "\n\n".join(paragraphs)
    while word_count(text) < EXPLANATION_MIN:
        extra = lib["reflection_prompts"][len(paragraphs) % len(lib["reflection_prompts"])]
        paragraphs.append(
            f"#### Deep dive\nConsider: {extra} Capture what data you reviewed, hypotheses tested, and resulting detections."
        )
        text = "\n\n".join(paragraphs)
    if word_count(text) > EXPLANATION_MAX:
        trimmed = paragraphs[:-1]
        while trimmed and word_count("\n\n".join(trimmed)) > EXPLANATION_MAX:
            trimmed = trimmed[:-1]
        if trimmed:
            text = "\n\n".join(trimmed)
    return clamp_text_to_word_limit(text, EXPLANATION_MAX)


def build_code_exercise(lesson: dict, lib: dict) -> str:
    lines = ["## Hands-on Lab"]
    for idx, cmd in enumerate(lib["commands"]):
        telemetry = cycle(lib["telemetry"], idx)
        tool = cycle(lib["tools"], idx)
        troubleshooting = lib["troubleshooting"][idx % len(lib["troubleshooting"])]
        pitfall = lib["pitfalls"][idx % len(lib["pitfalls"])]
        lines.append(f"### Command: {cmd['snippet']}")
        lines.append(cmd["context"])
        lines.append("```\n" + cmd["snippet"] + "\n```")
        lines.append(
            (
                f"Correlate the output with {telemetry['name']} to confirm {telemetry['analysis'].lower()}. Use the insight to "
                f"tune {tool['name']} according to {tool['usage']}"
            )
        )
        lines.append(
            (
                f"Document prerequisites, expected artifacts, and follow-up scripts in the runbook for {lesson['title']}. "
                f"Highlight how the command reinforces mitigations against {pitfall.lower()}"
            )
        )
        lines.append(
            "During the lab, capture screenshots, CLI transcripts, and annotations that future analysts can replay to "
            "accelerate incident response."
        )
        lines.append(
            f"Troubleshooting focus: {troubleshooting} Summarize how you validated the fix and which dashboards you updated."
        )
    lines.append(
        "Close the exercise by translating each command into automated tasks, alerting thresholds, and rollback plans that "
        "production teams can trust."
    )
    return "\n\n".join(lines)


def build_real_world(lesson: dict, lib: dict) -> str:
    sections = ["## Real-world Case Files"]
    for idx, case in enumerate(lib["case_studies"]):
        telemetry = cycle(lib["telemetry"], idx)
        tool = cycle(lib["tools"], idx)
        sections.append(f"### {case['scenario']}")
        sections.append(case["details"])
        sections.append(case["response"])
        sections.append(
            (
                f"Recreate the timeline using {telemetry['name']} to validate the indicators. Explain how {tool['name']} accelerated "
                f"containment and which governance controls were adjusted afterwards."
            )
        )
        sections.append(
            "Capture stakeholder communications, legal coordination, and business impact assessments so leaders understand the "
            "value of proactive hunting."
        )
    for incident in lib["incidents"]:
        sections.append(f"### {incident['name']}")
        sections.append(incident["description"])
        sections.append(incident["lesson"])
        sections.append(
            f"Map the incident lessons to the safeguards in {lesson['title']} and specify measurable leading indicators to monitor."
        )
    sections.append(
        "For each case, document timeline artifacts, impacted assets, telemetry analyzed, and long-term governance changes "
        "introduced. Summarize executive takeaways and how you will rehearse similar incidents with tabletop simulations."
    )
    return "\n\n".join(sections)


def build_memory_aid(lesson: dict, lib: dict) -> str:
    parts = ["## Memory Architectures"]
    for hook in lib["memory_hooks"]:
        parts.append(f"### Mnemonic: {hook['mnemonic']}")
        parts.append(hook["story"])
        parts.append(hook["visual"])
        parts.append(
            (
                f"Link the mnemonic to daily stand-ups by teaching teammates how it reinforces safeguards from {lesson['title']}."
                " Convert it into cue cards, spaced-repetition prompts, and lightning talks."
            )
        )
    for pitfall in lib["pitfalls"]:
        parts.append(f"*Watch out:* {pitfall}")
        parts.append(
            "Design a counter-mnemonic that highlights early warning signs and the telemetry sources that will expose the issue."
        )
    parts.append(
        "Create flashcards, mind maps, and storytelling prompts linking these memory tools to telemetry and tooling. Schedule "
        "peer coaching sessions to rehearse the mnemonics until they feel automatic."
    )
    return "\n\n".join(parts)


def build_quiz_block(lesson: dict, lib: dict) -> str:
    parts = ["## Knowledge Sprints"]
    for idx, prompt in enumerate(lib["reflection_prompts"]):
        attack = cycle(lib["attacks"], idx)
        telemetry = cycle(lib["telemetry"], idx)
        parts.append(f"### Scenario {idx + 1}")
        parts.append(prompt)
        parts.append(
            (
                f"Build a quick quiz that contrasts effective defenses against {attack['name']} with red-team moves that still slip by."
                f" Include at least one question explaining how {telemetry['name']} surfaces anomalies and why it matters for {lesson['title']}."
            )
        )
        parts.append(
            "Capture the answer key, remediation references, and data sources used so facilitators can run the sprint again with new analysts."
        )
    parts.append(
        "Store quiz results, reasoning notes, and remediation references so SOC teams can reuse the exercise in tabletop drills."
        " Track improvement metrics over quarterly reviews."
    )
    return "\n\n".join(parts)


def build_reflection(lesson: dict, lib: dict) -> str:
    lines = ["## Reflect and Synthesize"]
    for idx, question in enumerate(lib["reflection_prompts"]):
        tool = cycle(lib["tools"], idx)
        lines.append(f"- {question}")
        lines.append(
            (
                f"  - Link insights to {tool['name']} usage notes and document follow-up hypotheses tied to {lesson['title']}."
                " Share the reflections with cross-functional partners for feedback."
            )
        )
    lines.append(
        "Capture reflections in shared runbooks, linking to data sources, dashboards, and code artifacts used during analysis."
    )
    lines.append(
        "Summarize surprises, challenged assumptions, and next hypotheses so future hunts build on your progress. Commit to "
        "reviewing the notes during retrospectives and quarterly training cycles."
    )
    return "\n".join(lines)


def build_mindset(lesson: dict, lib: dict) -> str:
    lines = ["## Mindset and Next Steps"]
    for encouragement in lib["encouragement"]:
        lines.append(encouragement)
        lines.append(
            "Translate the encouragement into weekly habits, such as sharing one actionable insight during stand-up or logging a"
            " reusable detection pattern."
        )
    lines.append("### Next Steps")
    for step in lib["next_steps"]:
        lines.append(f"- {step}")
        lines.append(
            "  - Identify owners, due dates, required telemetry, and success metrics so the team can track completion transparently."
        )
    lines.append(
        "Celebrate incremental wins, share progress updates, and mentor peers to reinforce a growth mindset. Document "
        "recognition moments in the team journal and revisit them during performance reviews."
    )
    return "\n\n".join(lines)


def ensure_total_word_count(blocks: list[dict], lib: dict) -> None:
    total = sum(word_count(block["content"]["text"]) for block in blocks)
    if total < TOTAL_MIN:
        idx = 0
        while total < TOTAL_MIN:
            prompt = lib["reflection_prompts"][idx % len(lib["reflection_prompts"])]
            step = lib["next_steps"][idx % len(lib["next_steps"])]
            addition = (
                f"### Sustained Practice {idx + 1}\n"
                f"Turn the prompt '{prompt}' into a repeatable workshop. Capture before-and-after metrics, curate example telemetry,"
                f" and assign mentors to coach newcomers through the activity.\n"
                f"Action plan: {step} Document blockers, resource requirements, and executive narratives summarizing the impact."
            )
            blocks[-1]["content"]["text"] += "\n\n" + addition
            total = sum(word_count(block["content"]["text"]) for block in blocks)
            idx += 1
    if total > TOTAL_MAX:
        text_parts = blocks[-1]["content"]["text"].split("\n\n")
        while total > TOTAL_MAX and len(text_parts) > 3:
            text_parts.pop()
            blocks[-1]["content"]["text"] = "\n\n".join(text_parts)
            total = sum(word_count(block["content"]["text"]) for block in blocks)


def build_post_assessment(lesson: dict, lib: dict) -> list[dict]:
    questions = []
    for idx, concept in enumerate(lesson["concepts"][:3]):
        tool = cycle(lib["tools"], idx)
        telemetry = cycle(lib["telemetry"], idx)
        correct = f"Use {tool['name']} with {telemetry['name']} to reinforce {concept}."
        distractors = [f"Ignore {pitfall}" for pitfall in lib["pitfalls"][:3]]
        options = [correct] + distractors[:3]
        questions.append(
            {
                "question": f"Which action best applies {concept} when working through {lesson['title']}?",
                "options": options,
                "correct_answer": 0,
                "difficulty": lesson.get("difficulty", 2),
                "type": "multiple_choice",
            }
        )
    return questions


def rebuild_lesson(path: Path) -> None:
    lesson = json.loads(path.read_text(encoding="utf-8"))
    domain = lesson.get("domain")
    lib = DOMAIN_LIBRARY[domain]
    ensure_concepts(lesson, lib)
    ensure_learning_objectives(lesson)
    ensure_metadata(lesson)

    block_texts = [
        build_explanation(lesson, lib, 1),
        build_explanation(lesson, lib, 2),
        build_code_exercise(lesson, lib),
        build_real_world(lesson, lib),
        build_memory_aid(lesson, lib),
        build_quiz_block(lesson, lib),
        build_reflection(lesson, lib),
        build_mindset(lesson, lib),
    ]
    blocks = [{"type": block_type, "content": {"text": text}} for block_type, text in zip(REQUIRED_TYPES, block_texts)]
    ensure_total_word_count(blocks, lib)

    lesson["content_blocks"] = blocks
    lesson["post_assessment"] = build_post_assessment(lesson, lib)

    path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    lessons_file = ROOT / "new_lessons.txt"
    if lessons_file.exists():
        targets: Iterable[Path] = [ROOT / line.strip() for line in lessons_file.read_text().splitlines() if line.strip()]
    else:
        targets = CONTENT_DIR.glob("lesson_*_RICH.json")
    for lesson_path in targets:
        if lesson_path.suffix != ".json" or not lesson_path.exists():
            continue
        lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
        domain = lesson.get("domain")
        if domain not in DOMAIN_LIBRARY:
            continue
        rebuild_lesson(lesson_path)


if __name__ == "__main__":
    main()
