import csv
import json
import re
from pathlib import Path
from textwrap import dedent
from typing import List
from uuid import uuid4

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
LESSON_CSV = ROOT / "lesson_ideas.csv"

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

DOMAIN_CONTEXT = {
    "blue_team": {
        "tools": [
            "sigma convert -t splunk detection.yml",
            "wazuh-control info",
            "splunk search 'index=security earliest=-24h'",
        ],
        "real_world": (
            "A managed security provider tuned Sigma analytics to catch a living-off-"
            "the-land attack that bypassed their default SIEM alerts."
        ),
        "distractors": [
            "Password spraying",
            "Web skimming",
            "USB drop campaign",
            "Single sign-on onboarding",
            "Marketing attribution",
        ],
    },
    "osint": {
        "tools": [
            "misp-modules --list",
            "opencti-cli feed push",
            "stix2-py generate bundle.json",
        ],
        "real_world": (
            "Threat intel teams track ransomware infrastructure by pivoting through"
            " certificate transparency logs and passive DNS histories."
        ),
        "distractors": [
            "Endpoint isolation",
            "Kernel rootkits",
            "Mobile device management",
            "Bluetooth pairing",
            "Zero trust microsegmentation",
        ],
    },
    "ai_security": {
        "tools": [
            "python -m venv ml-sec-lab",
            "pip install adversarial-robustness-toolbox",
            "python attack_demo.py --eps 0.3",
        ],
        "real_world": (
            "A fintech startup discovered poisoned training data when a fraud model"
            " suddenly approved anomalous wire transfers after a supply chain compromise."
        ),
        "distractors": [
            "Network load balancing",
            "Fiber channel zoning",
            "GPU mining",
            "USB device redirection",
            "SSL termination",
        ],
    },
    "iot_security": {
        "tools": [
            "binwalk -e firmware.bin",
            "iot-inspector capture start",
            "scapy -f ics_sniff.py",
        ],
        "real_world": (
            "Incident responders traced an ICS intrusion to insecure Modbus commands"
            " issued through an exposed remote maintenance interface."
        ),
        "distractors": [
            "Email encryption gateways",
            "Browser cookie banners",
            "Office macro policies",
            "CRM data deduplication",
            "Mobile push notifications",
        ],
    },
    "web3_security": {
        "tools": [
            "slither analyze contract.sol",
            "myth analyze --solc solc-select",
            "foundry test --fork-url $RPC_URL",
        ],
        "real_world": (
            "DeFi investigators identified a reentrancy exploit draining liquidity"
            " pools when flash loan volume spiked against an under-audited protocol."
        ),
        "distractors": [
            "DNS MX record",
            "Endpoint patch baselines",
            "Office phishing training",
            "Windows GPO hardening",
            "Mobile app sandboxing",
        ],
    },
}


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug[:80]


def parse_topics(raw_topics: str) -> List[str]:
    cleaned = raw_topics.strip().strip('"')
    parts = [part.strip().strip('"') for part in cleaned.split(",")]
    return [p for p in parts if p]


def build_concepts(topics: List[str]) -> List[str]:
    unique = []
    for item in topics:
        if item not in unique:
            unique.append(item)
    return unique[:8] if unique else []


def generate_learning_objectives(title: str, topics: List[str]) -> List[str]:
    objectives = []
    for topic in topics[:5]:
        objectives.append(f"Explain how {topic.lower()} fits into {title.lower()}.")
    if not objectives:
        objectives.append(f"Summarize the core components of {title.lower()}.")
    return objectives


def mnemonic_from_title(title: str) -> str:
    words = [w for w in re.split(r"\W+", title) if w]
    if not words:
        return ""
    acronym = "".join(word[0].upper() for word in words[:6])
    return f"Use the acronym {acronym} to remember the major pillars of this lesson."


def question_options(correct: str, domain: str) -> List[str]:
    context = DOMAIN_CONTEXT.get(domain, {})
    distractors = list(context.get("distractors", []))
    fallback = [
        "Inventory management",
        "Marketing analytics",
        "Customer onboarding",
        "Physical office seating",
        "Sales enablement",
    ]
    while len(distractors) < 3:
        distractors.append(fallback.pop(0))
    options = distractors[:3] + [correct]
    return options


def build_post_assessment(title: str, topics: List[str], domain: str, difficulty: int):
    questions = []
    selected = topics[:3] if topics else [title]
    for idx, topic in enumerate(selected):
        options = question_options(topic, domain)
        correct_index = 3  # we append correct answer last
        question = {
            "question": f"Which option best describes {topic}?",
            "options": options,
            "correct_answer": correct_index,
            "difficulty": min(3, difficulty + (1 if idx == 2 else 0)),
            "type": "multiple_choice",
        }
        questions.append(question)
    return questions


def compose_content_blocks(title: str, topics: List[str], domain: str, notes: str) -> List[dict]:
    context = DOMAIN_CONTEXT.get(domain, {})
    overview_points = "\n".join(f"- {topic}" for topic in topics[:6])
    tools_text = "\n".join(f"$ {cmd}" for cmd in context.get("tools", []))

    explanation_intro = dedent(
        f"""
        ### Why this lesson matters
        {title} connects strategic goals with day-to-day operations. Practitioners often
        encounter fragmented telemetry and competing priorities, and this lesson teaches
        a cohesive approach. Expect to translate the following focus areas into action:

        {overview_points if overview_points else '- Core principles and key workflows'}
        """
    ).strip()

    explanation_depth = dedent(
        f"""
        ### Deep technical walkthrough
        Each topic is explored using practitioner-centric language. We show how the
        capability surfaces in real environments, the metrics that track success, and the
        trade-offs defenders or analysts must balance. Throughout, the narrative references
        current frameworks (MITRE ATT&CK, NIST CSF, OWASP SAMM) so you can map the
        material to existing governance programs.
        """
    ).strip()

    code_exercise = dedent(
        f"""
        ### Hands-on exploration
        Practice the workflow with the following lab-style commands and checkpoints.

        {tools_text if tools_text else 'Document the workflow in your runbook and simulate it using lab data.'}

        After each run, write down:
        1. What telemetry or artifact you collected.
        2. How the output confirms or disproves a hypothesis.
        3. Which follow-up automation you would implement next.
        """
    ).strip()

    real_world = dedent(
        f"""
        ### Field insights
        {context.get('real_world', notes or 'Practitioners apply these techniques across enterprises and regulated industries.')}

        Document how the scenario unfolded, the telemetry that surfaced the issue, and
        the remediation pattern that ultimately closed the gap.
        """
    ).strip()

    memory_aid = dedent(
        f"""
        ### Remember with intention
        {mnemonic_from_title(title)}

        Create a storyboard that pairs each letter with a real indicator or workflow.
        The stronger the story, the faster you will recall the procedure under pressure.
        """
    ).strip()

    quiz_text = dedent(
        f"""
        ### Quick knowledge check
        1. Which activity validates success criteria for this lesson?
           - A) Ignore telemetry and wait for alerts
           - B) Capture artefacts, test hypotheses, and adjust detections
           - C) Disable monitoring tools during maintenance
           - D) Archive data without reviewing it
           **Answer:** B

        2. How do you reduce false positives while scaling coverage?
           - A) Deploy tooling without tuning
           - B) Iterate on analytics with production feedback loops
           - C) Eliminate all anomaly detections
           - D) Only run reports monthly
           **Answer:** B

        3. Why should you pair qualitative notes with quantitative dashboards?
           - A) It slows the team down
           - B) Auditors prefer incomplete records
           - C) Narrative context clarifies what the metrics mean
           - D) It reduces data availability
           **Answer:** C
        """
    ).strip()

    reflection = dedent(
        """
        ### Reflect and plan
        - Which data sources will you audit first?
        - How will you brief leadership on the risks highlighted here?
        - What automation can you prototype in the next sprint?
        """
    ).strip()

    mindset = dedent(
        f"""
        ### Keep momentum
        Celebrate incremental improvements. Share discoveries with peers, document what
        surprised you, and map the lessons into tabletop exercises or purple-team drills.
        Confidence grows each time you apply the material under realistic constraints.
        """
    ).strip()

    blocks = [
        {"block_id": str(uuid4()), "type": "explanation", "title": "Lesson orientation", "content": {"text": explanation_intro}},
        {"block_id": str(uuid4()), "type": "explanation", "title": "Technical depth", "content": {"text": explanation_depth}},
        {"block_id": str(uuid4()), "type": "code_exercise", "title": "Lab practice", "content": {"text": code_exercise}},
        {"block_id": str(uuid4()), "type": "real_world", "title": "Operational reality", "content": {"text": real_world}},
        {"block_id": str(uuid4()), "type": "memory_aid", "title": "Memory builder", "content": {"text": memory_aid}},
        {"block_id": str(uuid4()), "type": "quiz", "title": "Knowledge check", "content": {"text": quiz_text}},
        {"block_id": str(uuid4()), "type": "reflection", "title": "Reflection", "content": {"text": reflection}},
        {"block_id": str(uuid4()), "type": "mindset_coach", "title": "Mindset", "content": {"text": mindset}},
    ]
    return blocks


def generate_lesson(row: dict) -> dict:
    title = row["title"].strip()
    domain = row["domain"].strip()
    difficulty = int(row["difficulty"].strip())
    order_index = int(row["order_index"].strip())
    topics = parse_topics(row.get("topics", ""))
    notes = row.get("notes", "").strip()

    lesson = {
        "lesson_id": str(uuid4()),
        "domain": domain,
        "title": title,
        "subtitle": notes or f"Applying {title}",
        "difficulty": difficulty,
        "estimated_time": 30 + difficulty * 10,
        "order_index": order_index,
        "prerequisites": [],
        "concepts": build_concepts(topics),
        "learning_objectives": generate_learning_objectives(title, topics),
        "post_assessment": build_post_assessment(title, topics, domain, difficulty),
        "jim_kwik_principles": JIM_KWIK,
        "content_blocks": compose_content_blocks(title, topics, domain, notes),
    }
    return lesson


def write_lesson_file(row: dict, lesson: dict) -> Path:
    domain = row["domain"].strip()
    order_index = int(row["order_index"].strip())
    slug = slugify(row["title"])
    filename = f"lesson_{domain}_{order_index:02d}_{slug}_RICH.json"
    path = CONTENT_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)
    return path


def update_csv(rows: List[dict], processed_numbers: set[int]):
    fieldnames = rows[0].keys() if rows else []
    updated_path = LESSON_CSV
    with updated_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            number = int(row["lesson_number"].strip())
            if number in processed_numbers:
                row["status"] = "completed"
            writer.writerow(row)


def main():
    rows = []
    with LESSON_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    processed = set()
    for row in rows:
        if row.get("status", "").strip().lower() == "completed":
            continue
        lesson = generate_lesson(row)
        path = write_lesson_file(row, lesson)
        print(f"Created lesson: {path.relative_to(ROOT)}")
        processed.add(int(row["lesson_number"].strip()))

    if processed:
        update_csv(rows, processed)
        print(f"Updated {len(processed)} rows to completed in lesson_ideas.csv")
    else:
        print("No new lessons were generated.")


if __name__ == "__main__":
    main()
