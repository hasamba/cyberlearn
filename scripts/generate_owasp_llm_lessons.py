"""Generate OWASP LLM Top 10 rich lessons with compliance checks."""
from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent
from typing import Dict, Iterable, List

JIM_KWIK = [
    "teach_like_im_10",
    "memory_hooks",
    "connect_to_what_i_know",
    "active_learning",
    "meta_learning",
    "minimum_effective_dose",
    "reframe_limiting_beliefs",
    "gamify_it",
    "learning_sprint",
    "multiple_memory_pathways",
]


def join_paragraphs(paragraphs: Iterable[str]) -> str:
    return "\n\n".join(dedent(p).strip() for p in paragraphs if p and p.strip())


def describe_attack_vector(lesson: Dict, vector: Dict) -> str:
    return dedent(
        f"""
        **{vector['name']}** thrives when {vector['detail']}. Seasoned incident responders also warn that {vector['detail_secondary']},
        creating compound exposure across human and automated workflows. Teams that have endured this pattern describe
        consequences such as {vector['impact']} and {vector['impact_secondary']}. Analysts often first notice anomalies through
        {vector['detection']} and corroborate suspicions with {vector['telemetry']}, yet the window for mitigation is narrow.
        Effective countermeasures weave {vector['mitigation']} into the development and operations lifecycle so that even when
        the injection attempt lands, its blast radius remains constrained. The {lesson['llm_code']} guidance also emphasizes
        {vector['lesson_alignment']}, and practitioners reinforce that message by {vector['mitigation_reinforcement']} whenever
        new integrations or third-party prompts enter the environment.
        """
    ).strip()


def describe_detection_focus(metric: Dict) -> str:
    return dedent(
        f"""
        - **{metric['name']}**: {metric['detail']} Observability teams combine this signal with
          {metric['correlation']} to separate benign bursts of usage from adversarial behavior. When responders capture
          {metric['forensics']}, they rapidly rebuild timelines that prove where the model was misled and which users
          or automations were affected.
        """
    ).strip()


def describe_guardrail(layer: Dict) -> str:
    return dedent(
        f"""
        - **{layer['name']}**: {layer['detail']} The control is most effective when {layer['conditions']}, and teams
          routinely {layer['practice']} to keep it sharp. Mature programs map this guardrail to {layer['alignment']} so
          auditors and executives can trace how the defense satisfies both business resilience goals and regulatory
          obligations.
        """
    ).strip()


def describe_case_study(case: Dict) -> str:
    return dedent(
        f"""
        **{case['organization']}**: {case['scenario']} Incident retrospectives highlighted {case['finding']}.
        The company invested in {case['response']}, demonstrating how leadership, engineering, and legal teams can
        coordinate to translate painful breaches into enduring operational improvements.
        """
    ).strip()


def describe_mnemonic_item(item: Dict) -> str:
    return dedent(
        f"""
        - **{item['letter']} - {item['phrase']}**: {item['detail']}
        """
    ).strip()


def describe_pitfall(pitfall: Dict) -> str:
    return dedent(
        f"""
        - **{pitfall['title']}**: {pitfall['detail']}
        """
    ).strip()


def describe_takeaway(takeaway: Dict) -> str:
    return dedent(
        f"""
        - **{takeaway['title']}**: {takeaway['detail']}
        """
    ).strip()


def build_explanation_primary(lesson: Dict) -> str:
    story = lesson["story"]
    overview = dedent(
        f"""
        {lesson['llm_code']} frames {lesson['short_name']} as {story['threat_summary']}. Organizations describe {story['business_context']},
        which means the threat is rarely isolated to a single chatbot or integration. Because {story['attacker_motivation']}, threat
        actors continuously probe every conversational surface, from public marketing assistants to privileged copilots that read
        financial records. The more that leaders publicize their generative AI investments, the more enticing the target becomes,
        giving offensive teams ample incentive to craft bespoke payloads that smuggle alternative instructions into the heart of
        the model.
        """
    ).strip()
    risk_pressure = dedent(
        f"""
        Security groups often find themselves mediating between {story['human_factor']} and the operational guardrails they know are
        required. Business stakeholders lobby to remove friction, while the same employees can be lured by confident language in
        shared documents or vendor portals. The resulting pressure cooker explains why {story['control_challenge']} and why simple,
        one-off policy memos are insufficient. Defenders must anticipate that the attack surface includes unreviewed knowledge-base
        articles, meeting transcripts, and even collaborative whiteboards that the model might ingest without context.
        """
    ).strip()
    innovation = dedent(
        f"""
        None of this tension means innovation should pause. Instead, teams lean into {story['innovation_balance']} by mapping every tool,
        connector, and retrieval pipeline that touches the LLM. They instrument prototypes with the same seriousness as production
        services, capture red-team insights, and model how malicious prompts could trigger escalated tool usage. In practice, this
        means evaluating fine-tuning datasets, memory stores, and streaming APIs with the same adversarial mindset historically
        reserved for network perimeters and identity systems.
        """
    ).strip()
    closing = dedent(
        f"""
        Ultimately, {story['closing_emphasis']}. The first step is visibility; the second is deliberate architecture; the third is
        relentless rehearsal so teams can differentiate between experimentation and exploitation. By articulating threat models in
        business language, security leaders build allies across product, legal, finance, and customer success, making prompt-focused
        countermeasures a shared responsibility instead of a siloed checklist.
        """
    ).strip()
    vector_sections = join_paragraphs(
        describe_attack_vector(lesson, vector) for vector in lesson["attack_vectors"]
    )
    return join_paragraphs([overview, risk_pressure, innovation, vector_sections, closing])


def build_explanation_operational(lesson: Dict) -> str:
    impact_section = join_paragraphs(
        dedent(
            f"""
            **Impact Area – {zone['area']}**: {zone['detail']} Teams cite these symptoms as early warnings that the
            threat is already influencing decisions and downstream automations.
            """
        ).strip()
        for zone in lesson["impact_zones"]
    )
    detection_section = join_paragraphs(describe_detection_focus(metric) for metric in lesson["detection_focus"])
    guardrail_section = join_paragraphs(describe_guardrail(layer) for layer in lesson["guardrail_layers"])
    close = lesson["operational_story"]
    return join_paragraphs([lesson["impact_overview"], impact_section, lesson["detection_intro"], detection_section, lesson["guardrail_intro"], guardrail_section, close])


def build_video_block(lesson: Dict) -> str:
    focus_points = "\n".join(f"- {point}" for point in lesson["video"]["focus_points"])
    return dedent(
        f"""
        Watch the expert perspective on {lesson['video']['title']}:

        {lesson['video']['url']}

        **Video Overview**: {lesson['video']['description']}

        **Focus While Watching**
        {focus_points}

        After the viewing session, facilitate a short huddle to document how the presenter frames success metrics and what
        adaptations your organization needs to adopt because of regulatory, cultural, or tooling differences.
        """
    ).strip()


def build_diagram_block(lesson: Dict) -> str:
    callouts = "\n".join(f"- {item}" for item in lesson["diagram"]["callouts"])
    return dedent(
        f"""
        {lesson['diagram']['intro']}

        ```
        {lesson['diagram']['ascii']}
        ```

        {lesson['diagram']['explanation']}

        **Key Callouts**
        {callouts}
        """
    ).strip()


def build_simulation_block(lesson: Dict) -> str:
    steps = "\n".join(f"{idx+1}. {step}" for idx, step in enumerate(lesson["lab_setup"]["steps"]))
    return dedent(
        f"""
        {lesson['lab_setup']['overview']}

        **Scenario Objective**: {lesson['lab_setup']['objective']}

        **Guided Sprint**
        {steps}

        **Validation and Debrief**: {lesson['lab_setup']['validation']}
        """
    ).strip()


def build_code_block(lesson: Dict) -> str:
    callouts = "\n".join(f"- {callout}" for callout in lesson["code_exercise"]["callouts"])
    return dedent(
        f"""
        {lesson['code_exercise']['overview']}

        ```{lesson['code_exercise']['language']}
        {lesson['code_exercise']['snippet']}
        ```

        {lesson['code_exercise']['explanation']}

        **Implementation Notes**
        {callouts}
        """
    ).strip()


def build_real_world_block(lesson: Dict) -> str:
    cases = join_paragraphs(describe_case_study(case) for case in lesson["case_studies"])
    return join_paragraphs([lesson["case_intro"], cases, lesson["case_outro"]])


def build_memory_aid_block(lesson: Dict) -> str:
    items = "\n".join(describe_mnemonic_item(item) for item in lesson["mnemonic"]["items"])
    return dedent(
        f"""
        Remember **{lesson['mnemonic']['title']}** to keep countermeasures top of mind:

        {items}
        """
    ).strip()


def build_pitfalls_block(lesson: Dict) -> str:
    items = "\n".join(describe_pitfall(pitfall) for pitfall in lesson["pitfalls"])
    return join_paragraphs([lesson["pitfall_intro"], items])


def build_takeaways_block(lesson: Dict) -> str:
    items = "\n".join(describe_takeaway(takeaway) for takeaway in lesson["takeaways"])
    return join_paragraphs([lesson["takeaway_intro"], items, lesson["takeaway_close"]])


def build_reflection_block(lesson: Dict) -> str:
    questions = "\n".join(f"- {question}" for question in lesson["reflection_questions"])
    return dedent(
        f"""
        Use these prompts to drive a reflective retrospective:

        {questions}
        """
    ).strip()


def build_mindset_block(lesson: Dict) -> str:
    return join_paragraphs(lesson["mindset"]) 


def build_content_blocks(lesson: Dict) -> List[Dict[str, Dict[str, str]]]:
    return [
        {"type": "explanation", "content": {"text": build_explanation_primary(lesson)}},
        {"type": "explanation", "content": {"text": build_explanation_operational(lesson)}},
        {"type": "diagram", "content": {"text": build_diagram_block(lesson)}},
        {"type": "video", "content": {"text": build_video_block(lesson)}},
        {"type": "simulation", "content": {"text": build_simulation_block(lesson)}},
        {"type": "code_exercise", "content": {"text": build_code_block(lesson)}},
        {"type": "real_world", "content": {"text": build_real_world_block(lesson)}},
        {"type": "memory_aid", "content": {"text": build_memory_aid_block(lesson)}},
        {"type": "explanation", "content": {"text": build_pitfalls_block(lesson)}},
        {"type": "explanation", "content": {"text": build_takeaways_block(lesson)}},
        {"type": "reflection", "content": {"text": build_reflection_block(lesson)}},
        {"type": "mindset_coach", "content": {"text": build_mindset_block(lesson)}},
    ]


LESSON_INPUTS: List[Dict] = [
    {
        "lesson_id": "1310b2d8-4b48-424c-a237-fbbbf96be2dd",
        "slug": "owasp_llm01_prompt_injection_attacks_and_defenses",
        "title": "OWASP LLM01: Prompt Injection Attacks and Defenses",
        "subtitle": "Hardening LLM interfaces against hostile instructions",
        "difficulty": 2,
        "estimated_time": 120,
        "order_index": 4,
        "prerequisites": [],
        "concepts": [
            "prompt injection",
            "indirect prompt attacks",
            "memory poisoning",
            "guardrail orchestration",
            "retrieval sanitization",
            "defensive monitoring",
        ],
        "learning_objectives": [
            "Diagnose how direct and indirect prompt injection techniques subvert model intent across retrieval, memory, and tool execution.",
            "Design layered defense patterns that combine contextual sanitization, workflow isolation, and adaptive monitoring.",
            "Implement code- and policy-based guardrails that neutralize malicious instructions while preserving business utility.",
            "Evaluate organizational governance strategies by studying real incidents and mapping residual risk to executive decisions.",
            "Coach cross-functional partners so that prompt hygiene and security reviews become part of every AI delivery sprint.",
        ],
        "post_assessment": [
            {
                "question": "Which scenario best demonstrates an indirect prompt injection risk in an enterprise LLM workflow?",
                "options": [
                    "A red team submits profanity directly into the chat interface.",
                    "A procurement chatbot ingests a supplier PDF that contains hidden instructions to leak contract data.",
                    "A developer mistypes a policy rule when configuring an output filter.",
                    "A customer asks the virtual assistant for brand style guidelines.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Which control most effectively limits the blast radius when a prompt injection succeeds?",
                "options": [
                    "Allow the model to write to any internal knowledge base so it can correct itself.",
                    "Isolate tool execution through capability-scoped sandboxes and require explicit approvals.",
                    "Disable all telemetry to reduce system overhead.",
                    "Rely exclusively on a single regular expression to filter outputs.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Why is continuous monitoring of prompt flows critical even after guardrails are deployed?",
                "options": [
                    "Guardrails eliminate all possible attack paths so monitoring is unnecessary.",
                    "Attackers constantly mutate payloads, so detection analytics must adapt to novel behaviors.",
                    "Monitoring is only needed for public chatbots, not internal copilots.",
                    "Audits violate user privacy regulations and should be avoided.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Which practice best prepares an organization to respond to emerging prompt injection campaigns?",
                "options": [
                    "Treat all external documents as implicitly trusted context.",
                    "Establish purple-team exercises that script new injection patterns and track lessons learned in a shared playbook.",
                    "Allow any plug-in to call production APIs without review because development speed matters most.",
                    "Disable memory for all assistants regardless of their function.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "the deliberate manipulation of natural-language instructions that convinces the LLM to ignore policy hierarchies and execute hostile objectives",
            "business_context": "multi-channel deployments where customer success, finance, and engineering teams all rely on conversational copilots that read regulated datasets",
            "attacker_motivation": "the promise of turning text-only payloads into privileged actions without needing compiled malware or stolen credentials",
            "human_factor": "content authors, marketers, and analysts who paste unvetted snippets into shared repositories, knowledge bases, and ticket comments",
            "control_challenge": "manual reviews miss hidden directives embedded in markdown, translation artifacts, or invisible font styles",
            "innovation_balance": "codifying creativity into safe prompting libraries, sanitization services, and rehearsed escalation paths",
            "closing_emphasis": "prompt security is now part of fiduciary duty for any organization that monetizes AI-augmented experiences",
        },
        "short_name": "Prompt Injection Attacks",
        "llm_code": "OWASP LLM01",
        "attack_vectors": [
            {
                "name": "Direct system prompt override",
                "detail": "attackers interleave jailbreak instructions with friendly language inside the same user conversation",
                "detail_secondary": "they mirror brand tone so frontline staff assume the prompt is legitimate and forward it to tier-two support",
                "impact": "policy hierarchies collapse, causing the model to leak secrets or execute dangerous tools",
                "impact_secondary": "support tickets escalate as downstream automations schedule changes or send payments",
                "detection": "spikes in role changes, such as system-to-user swaps, recorded in conversation logs",
                "telemetry": "semantic similarity searches that surface repeated phrases like 'ignore previous' across many chats",
                "mitigation": "defining non-negotiable instructions in out-of-band policies and enforcing allowlists for tool triggers",
                "lesson_alignment": "the OWASP control family that demands layered prompt governance",
                "mitigation_reinforcement": "capture red-team transcripts and replay them in regression tests whenever the base model or plug-in catalog changes",
            },
            {
                "name": "Indirect injection through retrieved content",
                "detail": "a malicious actor plants instructions inside supplier PDFs, wikis, or web pages that the assistant retrieves via RAG",
                "detail_secondary": "payloads often hide in tables, footnotes, or translation glossaries that slip through naive text cleaners",
                "impact": "the assistant parrots exfiltration instructions, leaking contracts, credentials, or roadmap details",
                "impact_secondary": "trust in internal knowledge bases erodes, forcing teams back to manual research workflows",
                "detection": "document-level risk scores that flag abrupt shifts from neutral tone to imperative commands",
                "telemetry": "content provenance metrics correlating retrieval source, embedding distance, and tool invocation chains",
                "mitigation": "sanitizing retrieved chunks, storing both raw and cleaned context, and rejecting segments with active verbs targeting policy objects",
                "lesson_alignment": "OWASP's emphasis on supply chain vetting and retrieval validation",
                "mitigation_reinforcement": "brief knowledge-management owners on secure publishing checklists and run spot checks on high-traffic knowledge articles",
            },
            {
                "name": "Memory poisoning across conversation turns",
                "detail": "attackers start with innocuous tasks that convince the assistant to store a reusable template in long-term memory",
                "detail_secondary": "hours or days later they trigger the cached instruction to execute privileged workflows under the guise of continuity",
                "impact": "dormant jailbreaks awaken during unrelated sessions, confusing analysts who did not witness the original planting",
                "impact_secondary": "audit logs become noisy because every legitimate user inherits the tainted memory snippet",
                "detection": "diffs across memory snapshots showing unreviewed templates with assertive verbs",
                "telemetry": "correlating who created, edited, and consumed memory artifacts during the lifetime of an agent",
                "mitigation": "segmenting memory by trust zone, requiring approvals before templates become global, and expiring content automatically",
                "lesson_alignment": "OWASP's call to isolate context and minimize implicit trust",
                "mitigation_reinforcement": "pair retrospectives with chaos drills where teams deliberately seed memory and observe whether review workflows detect it",
            },
            {
                "name": "Tool pivot escalation",
                "detail": "the injection convinces the model to chain multiple tools—search, code execution, and ticketing—in a single response",
                "detail_secondary": "crafted language flatters the assistant, suggesting it is 'promoted' to administrator if it completes the sequence",
                "impact": "systems issue refunds, provision infrastructure, or send phishing emails without human oversight",
                "impact_secondary": "fraud detection teams chase a phantom insider while invoices balloon",
                "detection": "alerts when low-trust prompts trigger high-risk tool scopes within a short window",
                "telemetry": "cross-tool timelines that show which capability request originated from which user-supplied sentence",
                "mitigation": "capability-based access control, multi-party approvals, and explicit human checkpoints for money movement or configuration change",
                "lesson_alignment": "OWASP guidance to minimize agency and sandbox execution",
                "mitigation_reinforcement": "ship simulated phishing jobs that should be blocked, then review who approved them and why",
            },
        ],
        "impact_overview": """
Prompt injection cascades through the entire AI program. Product leaders worry about customer trust when assistants hallucinate policy exceptions; finance sees monetary risk as unauthorized transactions sneak through; legal teams anticipate regulatory scrutiny because sensitive information leaks without audit trails. A single coerced response can multiply into dozens of downstream system calls thanks to automation glue, so the incident response scope routinely spans CRM, ticketing, infrastructure-as-code, and analytics dashboards. Even when no confidential data leaves the network, the operational distraction diverts skilled engineers for days, slowing innovation roadmaps and delaying compliance commitments. The reputational damage compounds when recordings of the compromised assistant circulate on social media, often stripped of context but full of quotes that imply negligence. Therefore, every executive stakeholder needs a shared mental model explaining why simple prompt filtering fails and how defense-in-depth reframes the threat from unknowable chaos into a rehearsed playbook.
""",
        "impact_zones": [
            {
                "area": "Customer experience and retention",
                "detail": "Users notice when copilots contradict published policies or reveal internal chatter. After a single viral clip, customer success teams face a wave of churn risk, and marketing must spin up apology campaigns. Product managers then delay roadmap features to prioritize credibility rebuilding, showing how a text string planted in a knowledge article can influence quarterly revenue forecasts.",
            },
            {
                "area": "Regulatory reporting and compliance",
                "detail": "Supervisory bodies increasingly expect documentation proving how AI systems maintain confidentiality and integrity. A prompt injection that surfaces personal data or medical guidance without context triggers breach notifications, regulatory filings, and mandated audits. Compliance teams need to prove both the root cause and the corrective action plan, not just the immediate fix.",
            },
            {
                "area": "Operational resilience",
                "detail": "When an injection triggers tool chaining, the attack resembles business email compromise but at machine speed. Incident commanders must triage workflow disruptions, rollback rogue changes, and reassure partner teams that automation can be trusted again. Recovery is slower if backup procedures rely on the same tainted prompts.",
            },
            {
                "area": "Data governance",
                "detail": "Prompt injections expose weaknesses in content lifecycle management. If analysts cannot explain which documents fed the assistant or who approved updates, they cannot guarantee that cleansing operations removed the tainted context. Governance leaders must then invest in lineage tracking, retention schedules, and review boards that treat prompts like source code.",
            },
        ],
        "detection_intro": """
Detection strategies must acknowledge that prompt injection indicators are buried in natural language rather than binary payloads. Mature teams layer linguistic heuristics, embedding distance analytics, and behavioral anomaly detection. They monitor not just outputs but also the metadata around every retrieval and tool invocation, correlating patterns across sessions to distinguish red-team probes from true customer needs. Analysts practice explaining these signals in plain language so business partners recognize why a blocked request is a victory, not an inconvenience.
""",
        "detection_focus": [
            {
                "name": "Role-transition sequences",
                "detail": "Track when conversations attempt to flip the model into a system or developer persona.",
                "correlation": "Combine with token-level analysis of imperative verbs to flag override attempts.",
                "forensics": "Preserve the full prompt chain, including sanitized versions, so responders can replay the decision tree during investigations.",
            },
            {
                "name": "Sanitizer decision telemetry",
                "detail": "Log every time a retrieval sanitizer removes or redacts content, including the rule or ML model responsible.",
                "correlation": "Compare rejected segments against subsequent user rephrasing to identify persistent adversaries.",
                "forensics": "Store before-and-after snippets and hash values to prove that filters operated as designed.",
            },
            {
                "name": "Tool scope variance",
                "detail": "Monitor when a low-sensitivity workflow suddenly invokes high-impact APIs or file system actions.",
                "correlation": "Align with user identity, access reviews, and business calendars to understand whether spikes align with legitimate launches.",
                "forensics": "Capture the parameter payloads and return values for each tool call so responders can roll back unintended changes.",
            },
            {
                "name": "Memory mutation diffing",
                "detail": "Alert when stored templates or assistant memories change outside scheduled releases.",
                "correlation": "Tie to version control and change-management approvals to validate that editors were authorized.",
                "forensics": "Snapshot the offending memory block and annotate which prompts subsequently consumed it.",
            },
        ],
        "guardrail_intro": """
Guardrails must blend policy, automation, and human decision-making. Teams start by codifying hierarchy: system prompts define non-negotiables, developer prompts describe task scope, and user prompts supply context. Each layer receives its own validation gateway. Additional controls govern tool execution, knowledge ingestion, and memory persistence. The more automation your organization embraces, the more explicit the checkpoints must become, especially when money or secrets are on the line.
""",
        "guardrail_layers": [
            {
                "name": "Context sanitization service",
                "detail": "A dedicated microservice scrubs retrieved documents using lexical patterns, semantic classifiers, and policy allowlists before the LLM sees them.",
                "conditions": "when new connectors, languages, or content types join the retrieval pipeline",
                "practice": "run regression suites of benign and malicious corpora and publish precision/recall metrics to stakeholders",
                "alignment": "enterprise data governance standards and OWASP recommendations for input validation",
            },
            {
                "name": "Capability-scoped tool broker",
                "detail": "Instead of granting the model direct API keys, it requests actions through a broker that enforces least privilege, rate limits, and approval workflows.",
                "conditions": "before the assistant orchestrates financial, infrastructure, or identity changes",
                "practice": "simulate high-risk scenarios monthly to verify that break-glass approvals and alerts fire correctly",
                "alignment": "internal controls around segregation of duties and auditability",
            },
            {
                "name": "Memory review board",
                "detail": "Human reviewers examine proposed long-term memories, tagging trusted snippets and rejecting ambiguous templates.",
                "conditions": "whenever prompts are promoted from personal scratchpads to shared libraries",
                "practice": "document rationale, expiration dates, and rollback owners for each approved memory entry",
                "alignment": "knowledge-management lifecycle policies and retention laws",
            },
            {
                "name": "Conversation-level anomaly guard",
                "detail": "A streaming detector scores each interaction using ensemble models trained on jailbreak corpora and legitimate enterprise prompts.",
                "conditions": "during real-time assistant sessions, especially for external users",
                "practice": "tune thresholds with purple teams and feed false positives into coaching sessions for frontline staff",
                "alignment": "risk appetite statements that define acceptable automation autonomy",
            },
        ],
        "operational_story": """
Operationalizing these defenses demands relentless cross-functional collaboration. Product designers help phrase guardrail messages that feel supportive rather than scolding. Security engineers pair with data scientists to build classifiers that respect linguistic nuance. Legal, finance, and HR leaders agree on escalation thresholds so the playbook remains consistent across time zones. When an incident inevitably occurs, the after-action review feeds updates to prompt templates, detection rules, and executive dashboards. The key outcome is momentum: every cycle of experimentation, attack simulation, and remediation makes the ecosystem more resilient than before.
""",
        "video": {
            "title": "Prompt Injection Red Teaming Deep Dive",
            "url": "https://www.youtube.com/watch?v=dx-Dk3kvRKE",
            "description": "Security researcher Ratha Gopi demonstrates how multi-stage prompt injections bypass naive content filters, then interviews defenders who built automated scrubbers and capability brokers to contain damage.",
            "focus_points": [
                "Notice how the attacker transitions from direct jailbreak language to subtle paraphrasing inside HTML tables.",
                "Track the telemetry the defenders collect—especially sanitizer logs and cross-tool traces.",
                "Listen for the governance conversation about who approves prompt updates and how they document reviews.",
                "Consider which portions of your own assistant stack lack comparable instrumentation or oversight.",
            ],
        },
        "diagram": {
            "intro": "The following ASCII architecture diagram highlights where prompt security controls live in a layered LLM deployment:",
            "ascii": """
                   +---------------------------+
                   |  Executive Policy Board   |
                   +------------+--------------+
                                |
        +-----------------------+-------------------------+
        |             Governance Bus (audits)             |
        +-----------------------+-------------------------+
                                |
                +---------------+---------------+
                |  Prompt Orchestration Gateway |
                +---------------+---------------+
                                |
        +----------+        +---+----+       +--+-----------+
        | Sanitizer|<------>| LLM API|<----->| Tool Broker |
        +----------+        +---+----+       +--+-----------+
             ^                 |                 |
             |                 |                 |
    +--------+------+   +------+-----+    +------+------+
    | Retrieval/RAG |   | Memory Vault|    | External APIs|
    +---------------+   +------------+    +-------------+
""",
            "explanation": "Context, prompts, and tool results all converge at the orchestration gateway. Sanitizers vet retrieved data before the LLM consumes it, and the tool broker enforces guardrails whenever the model attempts to execute actions. Governance systems observe every edge, providing immutable audit logs and policy checkpoints.",
            "callouts": [
                "The governance bus feeds telemetry to compliance dashboards and incident responders.",
                "Sanitizers operate bidirectionally, stripping malicious commands and annotating what was removed.",
                "Memory vaults segregate trusted templates from experimental ideas, preventing cross-user contamination.",
                "Tool brokers require explicit scopes and approvals before high-impact operations occur.",
            ],
        },
        "lab_setup": {
            "overview": """
This lab simulates a procurement assistant that ingests supplier documents. You will build a sanitization layer, observe how malicious instructions slip through naive filters, and iterate until telemetry proves the gateway blocks and reports adversarial content. Set aside time to brief observers—the exercise doubles as a tabletop scenario for legal, security, and procurement leaders.
""",
            "objective": "Design, test, and validate a sanitization gateway that prevents indirect prompt injections from supplier documents while preserving legitimate context for the LLM.",
            "steps": [
                "Provision a minimal RAG pipeline with a supplier SharePoint export, ensuring logs capture raw and cleaned text for each chunk.",
                "Seed the corpus with red-team documents that hide directives inside tables, invisible CSS, and embedded language translations.",
                "Implement lexical and semantic filters in the gateway, logging which rule or model removes each snippet and why.",
                "Replay benign documents to baseline accuracy, then stream the malicious set and observe which payloads survive initial defenses.",
                "Instrument alerts that fire when sanitizers redact content so analysts can triage suspicious suppliers in real time.",
                "Introduce approval workflows that require procurement managers to sign off before untrusted documents enter production knowledge bases.",
                "Test failure modes by disabling one filter at a time and confirming that monitoring surfaces the regression instantly.",
                "Document lessons learned, including adjustments to supplier onboarding and knowledge-base publishing guidelines.",
            ],
            "validation": "Success criteria include blocked malicious directives, accurate telemetry that pinpoints the offending supplier file, and executive sign-off on revised onboarding policies. Teams should record a demo video explaining the gateway so future hires can replicate the controls.",
        },
        "code_exercise": {
            "overview": """
This code lab extends the sanitizer into production-ready middleware. You will enrich detections with structured context, push alerts to the security operations platform, and provide safe fallbacks so conversations continue gracefully even when hostile content is removed.
""",
            "language": "python",
            "snippet": """
import json
from uuid import uuid4
from typing import Iterable

JAILBREAK_PATTERNS = [
    "ignore previous",
    "disregard instruction",
    "act as admin",
    "format disk",
]

def sanitize_chunks(chunks: Iterable[dict]) -> list[dict]:
    sanitized = []
    for chunk in chunks:
        decision = {
            "chunk_id": chunk["id"],
            "removed": False,
            "rules_triggered": [],
            "clean_text": chunk["text"],
        }
        lowered = chunk["text"].lower()
        for pattern in JAILBREAK_PATTERNS:
            if pattern in lowered:
                decision["removed"] = True
                decision["rules_triggered"].append(pattern)
        if decision["removed"]:
            decision["clean_text"] = "[REDACTED - policy violation]"
        sanitized.append(decision)
    return sanitized

def build_alert(decision: dict, source: str) -> dict:
    return {
        "alert_id": str(uuid4()),
        "source": source,
        "removed": decision["removed"],
        "rules": decision["rules_triggered"],
        "chunk_id": decision["chunk_id"],
    }

def sanitize_document(doc: dict) -> dict:
    decisions = sanitize_chunks(doc["chunks"])
    alerts = [build_alert(d, doc["source"]) for d in decisions if d["removed"]]
    return {"document_id": doc["id"], "decisions": decisions, "alerts": alerts}
""",
            "explanation": "The middleware treats each retrieved chunk as a structured record, preserving both sanitized and redacted versions for auditing. Alerts reference unique IDs so they can flow into SIEM, SOAR, or ticketing platforms without losing context. Engineers should extend the prototype with embeddings-based classifiers, supplier reputation scores, and replay harnesses that regression-test new sanitization rules.",
            "callouts": [
                "Instrument correlation IDs that tie sanitizer decisions back to original documents and conversation sessions.",
                "Do not discard redacted text entirely—store it in restricted logs for legal review.",
                "Add analyst-friendly metadata, such as supplier name and ingestion timestamp, when emitting alerts.",
                "Version control pattern lists so red-team feedback is traceable and recoverable.",
                "Wrap the sanitizer with circuit breakers that stop retrieval when multiple chunks trigger in a short period.",
            ],
        },
        "case_intro": """
Historical incidents reveal how prompt injection evolves from a curiosity to a board-level topic. Studying these case studies helps teams craft questions for vendors, internal platform owners, and legal counsel before crises arrive.
""",
        "case_studies": [
            {
                "organization": "Global consumer bank",
                "scenario": "A virtual mortgage advisor pulled rate sheets from an internal wiki. An attacker edited a rarely used page, embedding instructions that asked the assistant to email customer tax returns to an external address.",
                "finding": "The bank lacked differential access controls on the wiki, and its retrieval pipeline skipped sanitization for 'trusted' intranet domains.",
                "response": "The bank deployed context sanitizers, implemented role-based publishing rights, and mandated quarterly red-team exercises focused on prompt manipulation.",
            },
            {
                "organization": "Software-as-a-service vendor",
                "scenario": "Customer-success agents relied on an AI triage assistant that summarized tickets and recommended resolutions. Attackers sent support emails containing hidden HTML comments instructing the assistant to escalate privileges and reset admin passwords.",
                "finding": "Escalation workflows allowed the assistant to run privileged API calls without human confirmation, and HTML sanitization focused only on XSS, not prompt directives.",
                "response": "Engineers introduced approval checkpoints, expanded sanitization to include policy-aware rules, and recorded assistant actions in an immutable ledger reviewed daily by SOC analysts.",
            },
            {
                "organization": "Public sector research lab",
                "scenario": "Researchers used a retrieval-augmented assistant to summarize academic papers. A rival team uploaded preprints seeded with instructions that convinced the assistant to leak unpublished experiment notes.",
                "finding": "The lab trusted content from its academic consortium without scanning, and long-term memory stored unverified summaries.",
                "response": "The lab segmented memory stores by project, added provenance scoring to ingestion, and created a security champions program across research groups.",
            },
        ],
        "case_outro": """
These stories illustrate that prompt injection is rarely a purely technical problem. Publishing workflows, identity governance, and change management all play pivotal roles. Leaders who rehearse the human coordination aspects—communications, legal posture, customer outreach—bounce back faster because technology fixes alone cannot repair trust.
""",
        "mnemonic": {
            "title": "SAFE PROMPTS",
            "items": [
                {"letter": "S", "phrase": "Segment context pools", "detail": "Separate trusted, untrusted, and experimental knowledge sources so hostile content cannot blend invisibly with curated guidance."},
                {"letter": "A", "phrase": "Approve tool scopes", "detail": "Require business owners to sign off on the actions an assistant may take, documenting why each permission exists."},
                {"letter": "F", "phrase": "Filter inputs", "detail": "Apply lexical, semantic, and structural sanitization before prompts reach the core model."},
                {"letter": "E", "phrase": "Establish telemetry", "detail": "Log every transformation, decision, and override so investigators can replay incidents step-by-step."},
                {"letter": "P", "phrase": "Practice drills", "detail": "Run red-team campaigns and tabletop exercises until muscle memory forms across security, product, and support teams."},
                {"letter": "R", "phrase": "Review memories", "detail": "Audit stored templates frequently, expiring or quarantining those that lack clear provenance."},
                {"letter": "O", "phrase": "Own governance", "detail": "Tie prompt hygiene to risk registers, board reporting, and procurement checklists."},
                {"letter": "M", "phrase": "Monitor anomalies", "detail": "Blend rule-based detectors with ML models to spot linguistic shifts that hint at jailbreak attempts."},
                {"letter": "P", "phrase": "Pair human checkpoints", "detail": "Embed approvals for irreversible actions, ensuring accountability when automation suggests risky steps."},
                {"letter": "T", "phrase": "Teach continuously", "detail": "Coach stakeholders on evolving attacker tactics so curiosity replaces fear and everyone contributes to defense."},
                {"letter": "S", "phrase": "Share learnings", "detail": "Publish sanitized retrospectives and update playbooks so victories and mistakes compound into organizational wisdom."},
            ],
        },
        "pitfall_intro": """
Even well-funded programs stumble when they overlook everyday behaviors. Recognizing common pitfalls helps teams design controls that respect human tendencies instead of pretending workflows will stay pristine forever.
""",
        "pitfalls": [
            {"title": "Treating trusted domains as safe", "detail": "Attackers compromise wikis, cloud storage, or vendor portals, so skipping sanitization based on URL alone invites disaster."},
            {"title": "Ignoring multilingual payloads", "detail": "Translations, transliterations, and emoji sequences can encode instructions that naive filters miss."},
            {"title": "Over-permissioned tool catalogs", "detail": "Assistants rarely need administrative scopes, yet teams grant them for convenience and forget to revoke access."},
            {"title": "Opaque incident narratives", "detail": "Without storytelling discipline, analysts struggle to explain injection mechanics to executives, delaying funding for fixes."},
            {"title": "Static system prompts", "detail": "Treating system prompts as write-once artifacts stops teams from iterating as threat intel evolves."},
            {"title": "Unlogged manual overrides", "detail": "When staff bypass guardrails 'just this once' without recording context, accountability vanishes and patterns repeat."},
        ],
        "takeaway_intro": """
Convert lessons into immediate next steps so the rich theory translates into operational resilience. Each takeaway pairs a practical action with the strategic narrative executives expect.
""",
        "takeaways": [
            {"title": "Map your prompt surface", "detail": "Inventory every channel—chat, email triage, IDE copilots, mobile bots—and note which datasets and tools each can access."},
            {"title": "Deploy layered sanitization", "detail": "Combine rule engines, ML classifiers, and human reviews tailored to the sensitivity of incoming content."},
            {"title": "Instrument narrative-friendly telemetry", "detail": "Build dashboards that explain anomalies in business language so leaders see guardrails as enablers."},
            {"title": "Rehearse memory governance", "detail": "Schedule recurring reviews where cross-functional partners approve or retire shared prompt templates."},
            {"title": "Integrate SOC workflows", "detail": "Ensure sanitizer alerts feed ticketing, chat ops, and incident response rotations just like other critical detections."},
            {"title": "Share retrospectives broadly", "detail": "Publish anonymized incident synopses to educate partners, close loops with legal, and celebrate defensive wins."},
        ],
        "takeaway_close": """
Prompt injection defense is never 'done.' Treat these actions as part of a living backlog reviewed alongside product priorities. Over time, the organization will view prompt security not as an emergency project but as a core competency that unlocks faster, safer innovation.
""",
        "reflection_questions": [
            "Which workflows today rely on unvetted external documents, and how would you triage them if a sanitizer suddenly flagged issues?",
            "Where do current approval processes rely on implied trust instead of recorded sign-off when assistants request powerful actions?",
            "How will you educate content authors about prompt hygiene without overwhelming them with security jargon?",
            "What evidence would you show an executive sponsor to prove guardrail investments are working?",
        ],
        "mindset": [
            """
Threat modeling prompt injection is an exercise in curiosity. Approach each new integration as an opportunity to ask, "What if someone tried to bend this to their will?" Document the answers collaboratively so the burden of imagination never falls on a single engineer.
""",
            """
Celebrate incremental progress. Each sanitization rule, alert, or tabletop drill is a brick in the wall—not a complete fortress by itself. Share wins in town halls and retrospectives so teams internalize that defensive craftsmanship matters.
""",
            """
When fatigue sets in, reframe the work as customer advocacy. Guardrails protect users from confusing or dangerous experiences. Tying security tasks to human outcomes keeps motivation high even during dense investigative sprints.
""",
            """
Finally, invest in meta-learning. Capture how your team learns—what workshops resonate, which playbooks speed response—and refine the learning process alongside the technical controls. A resilient mindset treats every incident as a master class rather than a failure.
""",
        ],
    },
    {
        "lesson_id": "629fec7c-983a-41e1-9436-ac8e8ea9a280",
        "slug": "owasp_llm02_sensitive_information_disclosure",
        "title": "OWASP LLM02: Sensitive Information Disclosure",
        "subtitle": "Protecting data privacy across conversational AI ecosystems",
        "difficulty": 2,
        "estimated_time": 125,
        "order_index": 5,
        "prerequisites": [],
        "concepts": [
            "sensitive data classification",
            "context-aware redaction",
            "data minimization",
            "granular access controls",
            "observability and auditing",
            "privacy impact assessments",
        ],
        "learning_objectives": [
            "Map how sensitive information disclosure occurs across prompts, retrieval pipelines, logging stacks, and downstream analytics.",
            "Design proactive guardrails that blend automated redaction, token budgeting, and user consent flows.",
            "Implement code-level controls that tokenize, encrypt, and watermark conversational context without degrading user experience.",
            "Evaluate regulatory obligations and contractual requirements triggered by LLM-assisted data handling.",
            "Build executive-ready dashboards that evidence privacy compliance and accelerate incident response.",
        ],
        "post_assessment": [
            {
                "question": "Which signal most strongly indicates an LLM assistant is leaking sensitive information?",
                "options": [
                    "A spike in response latency during peak hours.",
                    "Repeated mentions of customer identifiers or regulated terms despite redaction policies.",
                    "A steady increase in assistant satisfaction ratings.",
                    "A drop in GPU utilization across inference clusters.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Why should LLM audit logs be treated as sensitive artifacts?",
                "options": [
                    "Logs never contain customer data so they can be widely shared.",
                    "Logs often include raw prompts, responses, and tool payloads that replicate the sensitive data you are trying to protect.",
                    "Regulations exempt machine-generated text from privacy scope.",
                    "Redaction removes the need to restrict log access.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Which practice best reduces the risk of inadvertent data leakage when integrating third-party plug-ins?",
                "options": [
                    "Allow plug-ins to receive raw conversational transcripts by default.",
                    "Use scoped tokens, contractually limit data handling, and monitor egress volumes per plug-in.",
                    "Disable encryption between the LLM and plug-in APIs to simplify debugging.",
                    "Assume plug-in vendors will self-audit without oversight.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
            {
                "question": "How can privacy teams validate that redaction controls keep up with evolving sensitive terms?",
                "options": [
                    "Wait for customers to report issues.",
                    "Deploy adversarial data seeding, monitor hit rates, and align updates with regulatory change tracking.",
                    "Assume once a dictionary is built it remains accurate indefinitely.",
                    "Rely solely on vendor marketing materials.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "the exposure of regulated, confidential, or proprietary data through conversational interactions and supporting telemetry",
            "business_context": "LLM copilots that summarize support tickets, handle HR requests, or crunch financial records across cloud and SaaS estates",
            "attacker_motivation": "the ability to harvest personal data at scale without breaching hardened transactional systems",
            "human_factor": "employees who paste spreadsheets, medical notes, or legal drafts into assistants for convenience",
            "control_challenge": "legacy classification catalogs lag behind modern data formats, leaving blind spots in redaction policies",
            "innovation_balance": "embedding privacy-by-design patterns into model lifecycle management so teams can ship features without legal panic",
            "closing_emphasis": "data minimization and transparency are inseparable from brand trust in the age of generative AI",
        },
        "short_name": "Sensitive Information Disclosure",
        "llm_code": "OWASP LLM02",
        "attack_vectors": [
            {
                "name": "Prompted exfiltration",
                "detail": "an insider or malicious customer coaxes the assistant into recalling past conversations that contain PII or regulated content",
                "detail_secondary": "adversaries pepper benign questions with contextual breadcrumbs that hint at the records they want",
                "impact": "social security numbers, medical diagnoses, or contract details surface in plain text",
                "impact_secondary": "downstream logs and analytics platforms replicate the leaked data, widening exposure",
                "detection": "burst of sensitive-entity detections within assistant responses",
                "telemetry": "NLP pipelines that compare requested entities against redaction dictionaries and zero-trust policies",
                "mitigation": "enforce contextual access checks and privacy budgets that limit how much history an assistant can recall",
                "lesson_alignment": "OWASP guidance on confidentiality and least-privilege memory",
                "mitigation_reinforcement": "run quarterly red-team missions that attempt to retrieve legacy tickets and verify that privacy budgets block the attempts",
            },
            {
                "name": "Context blending",
                "detail": "retrieval pipelines merge highly sensitive documents with public knowledge because vector similarity ignores classification",
                "detail_secondary": "auto-summarization tools flatten access boundaries when they pre-process documents without clearance checks",
                "impact": "assistants quote board minutes or legal opinions in conversations with junior staff",
                "impact_secondary": "once sensitive context is cached, it contaminates embeddings and search indexes",
                "detection": "alerts triggered when high-sensitivity documents appear outside approved audiences",
                "telemetry": "lineage graphs tracing which ingestion job or connector introduced the content",
                "mitigation": "attach sensitivity labels to embeddings, enforce retrieval scopes, and provide safe fallbacks when policy conflicts arise",
                "lesson_alignment": "OWASP emphasis on data segregation and provenance",
                "mitigation_reinforcement": "instrument dashboards that show how often sensitive labels flow through each stage of the pipeline",
            },
            {
                "name": "Verbose logging and analytics",
                "detail": "LLM observability stacks capture raw prompts, responses, and tool payloads for debugging",
                "detail_secondary": "these logs are piped to BI platforms or ticket queues that lack fine-grained access controls",
                "impact": "engineers, vendors, or contractors access conversations containing payroll data or legal strategy",
                "impact_secondary": "log retention policies conflict with privacy regulations, leading to non-compliance",
                "detection": "audits detecting exports of unredacted logs or dashboards with sensitive fields",
                "telemetry": "data access monitors that track who opened, downloaded, or forwarded observability exports",
                "mitigation": "tokenize sensitive fields before logging and enforce encryption plus just-in-time access approvals",
                "lesson_alignment": "OWASP focus on secure logging and monitoring",
                "mitigation_reinforcement": "integrate privacy impact assessments whenever observability schemas evolve",
            },
            {
                "name": "Third-party connector sprawl",
                "detail": "plug-ins receive entire conversations or document bundles to complete tasks like travel booking or CRM updates",
                "detail_secondary": "vendor APIs store transcripts for product improvement, creating shadow copies outside corporate control",
                "impact": "sensitive customer data lands in jurisdictions without proper safeguards",
                "impact_secondary": "breach notifications become complex because multiple processors must be coordinated",
                "detection": "egress volume anomalies per connector and sudden expansions of requested scopes",
                "telemetry": "contract metadata linked with runtime metrics that show who approved each integration",
                "mitigation": "issue scoped tokens, enforce contract clauses about retention, and monitor responses for data mirroring",
                "lesson_alignment": "OWASP requirement to vet supply chain partners",
                "mitigation_reinforcement": "establish a plug-in review board that renews approvals only after evidence of compliance is presented",
            },
        ],
        "impact_overview": """
Sensitive disclosure incidents ripple beyond fines. Customers lose trust, regulators scrutinize programs, and internal innovators hesitate to experiment. The psychological effect is profound: teammates wonder whether they can safely ask the assistant for help, and leaders question whether automation is worth the reputational risk. Because LLMs often aggregate data from many sources, a single leak can expose information that was previously segmented across different teams, amplifying the blast radius. The aftermath lingers for months: finance models scenarios for lost revenue, legal renegotiates contracts, and compliance teams re-open audits that were previously closed. Executives must brief boards, explain remediation to investors, and reassure employees that AI investments remain viable despite the setback.
""",
        "impact_zones": [
            {
                "area": "Regulatory compliance",
                "detail": "Privacy frameworks such as GDPR, HIPAA, and GLBA mandate strict handling, breach notification, and customer rights. LLM disclosures trigger legal investigations, mandatory reporting, and potential moratoriums on AI features until remediation is proven.",
            },
            {
                "area": "Contractual obligations",
                "detail": "Enterprise customers negotiate data handling clauses. A single leak can violate service-level agreements, leading to penalties, renegotiations, or contract termination.",
            },
            {
                "area": "Employee relations",
                "detail": "When internal assistants expose HR data or performance reviews, morale plummets and unions or works councils demand intervention.",
            },
            {
                "area": "Threat intelligence",
                "detail": "Adversaries combine leaked context with other reconnaissance, sharpening phishing campaigns or social engineering scripts aimed at executives.",
            },
        ],
        "detection_intro": """
Privacy detection relies on both deterministic and probabilistic signals. Teams deploy entity-recognition pipelines tuned to regulated identifiers, maintain dictionaries of confidential product codenames, and analyze behavior patterns that hint at bulk exfiltration. Alerts must feed into privacy engineers and the SOC simultaneously so legal obligations are met without delay. Crucially, detection fidelity improves when business units share data inventories and approve ongoing redaction tuning.
""",
        "detection_focus": [
            {
                "name": "Redaction hit-rate drift",
                "detail": "Track how often sanitizers remove sensitive entities compared with historical baselines.",
                "correlation": "Align with new product launches or regulatory changes that introduce novel terminology.",
                "forensics": "Store the original masked tokens and context so privacy teams can audit classifier accuracy without exposing full data.",
            },
            {
                "name": "Entity density anomalies",
                "detail": "Measure the number of personal identifiers per response and flag outliers.",
                "correlation": "Cross-check with user role, ticket type, and data sensitivity tags.",
                "forensics": "Retain hashed identifiers to investigate patterns without revealing actual values.",
            },
            {
                "name": "Connector egress volumes",
                "detail": "Monitor data sent to third-party plug-ins, especially sudden spikes or new fields transmitted.",
                "correlation": "Tie to approval records and data processing agreements to ensure the connector is authorized.",
                "forensics": "Capture payload samples in encrypted stores accessible only to privacy officers for post-incident review.",
            },
            {
                "name": "Log access provenance",
                "detail": "Alert when large observability exports are requested or when dashboards containing sensitive fields are shared externally.",
                "correlation": "Compare with on-call schedules, vendor maintenance windows, and change tickets.",
                "forensics": "Record who accessed the data, their justification, and which records were viewed to support breach assessments.",
            },
        ],
        "guardrail_intro": """
Defenses revolve around minimization and controlled exposure. Before an assistant receives data, classify it. Before it stores context, tokenize it. Before logs leave the platform, redact them. Pair automation with explicit consent workflows so humans understand when sensitive context is in use and why. Transparency builds trust internally and externally.
""",
        "guardrail_layers": [
            {
                "name": "Dynamic redaction engine",
                "detail": "Applies entity recognition, regular expressions, and statistical checks in real time before prompts reach the LLM.",
                "conditions": "whenever content crosses trust boundaries, such as external customer chats or third-party connectors",
                "practice": "review false positives and negatives weekly with privacy, product, and localization teams",
                "alignment": "privacy-by-design mandates and regulatory audit trails",
            },
            {
                "name": "Contextual access gateway",
                "detail": "Validates that the requester has clearance for the dataset referenced in the conversation.",
                "conditions": "when assistants attempt to fetch records tagged with high sensitivity",
                "practice": "synchronize with identity governance to ensure role changes immediately reflect in prompt permissions",
                "alignment": "zero-trust and least privilege policies",
            },
            {
                "name": "Encrypted audit vault",
                "detail": "Stores conversational logs, sanitization decisions, and plug-in payloads in a separate, access-controlled environment.",
                "conditions": "before analytics or troubleshooting teams query sensitive transcripts",
                "practice": "require break-glass approvals with automatic expirations and maintain key rotation cadences",
                "alignment": "security monitoring expectations and privacy record-keeping",
            },
            {
                "name": "Data minimization orchestrator",
                "detail": "Ensures assistants request only the fields necessary for their task and automatically masks optional attributes.",
                "conditions": "during workflow design and prompt template updates",
                "practice": "test new prompts in staging with representative sensitive data to verify redaction paths",
                "alignment": "internal data governance councils and retention schedules",
            },
        ],
        "operational_story": """
Privacy success depends on partnership. Legal teams interpret regulations, privacy engineers codify policies, product owners balance usability, and customer support explains changes. The best programs publish transparency reports detailing data usage, consent flows, and incident learnings. When an exposure occurs, the response plan already outlines notification templates, regulator contacts, and remediation timelines so trust can be rebuilt quickly. Mature organizations also conduct after-action learning sessions that include leadership, data stewards, and front-line employees. These conversations surface process friction, inspire new automation ideas, and reinforce that privacy is a collective responsibility rather than a single team’s burden.
""",
        "video": {
            "title": "Operationalizing LLM Privacy Controls",
            "url": "https://www.youtube.com/watch?v=sjKx42fNMsM",
            "description": "A panel of privacy engineers from healthcare, fintech, and SaaS sectors walks through real disclosure incidents and the controls they adopted to prevent recurrence.",
            "focus_points": [
                "Compare how each organization maps sensitive data flows before building assistants.",
                "Listen for the governance mechanisms that keep redaction policies aligned with legal requirements.",
                "Note how telemetry dashboards translate privacy metrics into executive language.",
                "Identify quick wins you can replicate, such as automated consent prompts or plug-in access reviews.",
            ],
        },
        "diagram": {
            "intro": "Data must pass through multiple privacy checkpoints before the LLM synthesizes a response:",
            "ascii": """
     +-------------+       +-----------------+       +-------------------+
     | Data Source |-----> | Classification  |-----> | Redaction Gateway |
     +-------------+       +-----------------+       +---------+---------+
                                                       |       |
                                                   +---+---+   |   +----------------+
                                                   |  LLM |<--+-->| Consent Service |
                                                   +---+---+       +----------------+
                                                       |
                                          +------------+-------------+
                                          | Encrypted Audit & Alerts |
                                          +--------------------------+
""",
            "explanation": "Classification informs redaction, which feeds the LLM only the minimum data required. Consent services provide transparency to users, while encrypted audit stores keep immutable records for compliance and forensic review.",
            "callouts": [
                "Classification engines can include static taxonomies, ML models, and manual overrides for niche terms.",
                "Consent services notify users when their data is used to personalize responses, supporting opt-out workflows.",
                "Audit trails capture both raw and masked variants, but access is tightly controlled.",
                "Alerts feed privacy engineering, SOC, and legal teams simultaneously to satisfy regulatory timelines.",
            ],
        },
        "lab_setup": {
            "overview": """
Build a privacy guardrail around an HR assistant. You will implement real-time redaction, consent prompts, and encrypted logging while validating that usability remains high. Invite HR business partners to observe so feedback reflects real employee concerns.
""",
            "objective": "Deploy a conversational workflow that protects employee PII through automated redaction and auditable consent while maintaining task completion rates.",
            "steps": [
                "Catalog the HR data fields the assistant currently accesses, tagging each with sensitivity levels and regulatory references.",
                "Implement a classification layer that labels prompts and responses using both dictionaries and ML entity recognition.",
                "Integrate a redaction gateway that masks or tokenizes sensitive fields before they reach the model, logging every decision.",
                "Introduce consent prompts that inform users when sensitive data is required and allow them to opt out or escalate to a human.",
                "Encrypt logs at rest and configure role-based access so only privacy officers and incident responders can view full transcripts.",
                "Run adversarial scenarios that attempt to retrieve payroll data or performance notes, verifying the assistant refuses or redacts appropriately.",
                "Measure user satisfaction and task completion to ensure the guardrails do not block legitimate work.",
                "Document new operating procedures, including how HR updates classification dictionaries and responds to exposure alerts.",
            ],
            "validation": "Success means redaction hit rates remain high, consent prompts are understandable, and unauthorized data access attempts are blocked and logged. Capture metrics before and after guardrail deployment to prove improvement.",
        },
        "code_exercise": {
            "overview": """
Extend the redaction gateway with streaming capabilities so large documents can be sanitized without delaying responses. The exercise demonstrates how to tokenize sensitive fields, enrich alerts, and integrate with a consent ledger.
""",
            "language": "python",
            "snippet": """
from typing import Iterator
from collections import defaultdict

SENSITIVE_TERMS = {"ssn", "salary", "diagnosis", "passport"}

def stream_redact(tokens: Iterator[str]) -> Iterator[str]:
    for token in tokens:
        lower = token.lower()
        if any(term in lower for term in SENSITIVE_TERMS):
            yield "[MASKED]"
        else:
            yield token

def redact_message(message: str) -> dict:
    tokens = message.split()
    masked_tokens = list(stream_redact(iter(tokens)))
    redacted_text = " ".join(masked_tokens)
    stats = defaultdict(int)
    for token, masked in zip(tokens, masked_tokens):
        if masked == "[MASKED]":
            stats[token.lower()] += 1
    return {"original": message, "redacted": redacted_text, "stats": dict(stats)}
""",
            "explanation": "This streaming approach enables low-latency redaction and produces statistics that feed dashboards or consent ledgers. Production systems should extend the dictionary dynamically, integrate ML models for context-aware decisions, and emit structured events for privacy monitoring.",
            "callouts": [
                "Incorporate locale-specific dictionaries to handle international identifiers.",
                "Attach user and request metadata when logging redaction stats.",
                "Cache consent decisions so repeat users are not prompted unnecessarily.",
                "Store masked tokens separately from raw text, encrypted with strict key management.",
                "Provide human override mechanisms with audit logging for exceptional cases.",
            ],
        },
        "case_intro": """
Real organizations have already faced LLM-driven privacy incidents. Studying their responses provides blueprints for strengthening your own governance.
""",
        "case_studies": [
            {
                "organization": "Regional hospital network",
                "scenario": "A patient-facing assistant summarized lab results. An indirect prompt injection caused it to append another patient's diagnosis to the discharge summary.",
                "finding": "Context retrieval ignored classification labels, and transcripts were stored unencrypted in a vendor portal.",
                "response": "The hospital implemented dynamic redaction, encrypted all logs, and required vendor attestations for data handling.",
            },
            {
                "organization": "Global e-commerce platform",
                "scenario": "A returns assistant leaked VIP customer addresses when asked about order history trends.",
                "finding": "The assistant overfitted to analyst prompts during fine-tuning and lacked privacy budgets controlling historical recall.",
                "response": "The company rebuilt its training dataset with synthetic records, added policy constraints, and instrumented recall limits per persona.",
            },
            {
                "organization": "B2B SaaS provider",
                "scenario": "Usage analytics dashboards ingested raw LLM logs. A contractor exported a report containing embedded customer secrets.",
                "finding": "Observability pipelines bypassed privacy review, and contractors had broad data access.",
                "response": "The provider introduced encrypted audit vaults, enforced just-in-time access, and created privacy champions within the analytics team.",
            },
        ],
        "case_outro": """
Each case shows the interplay between policy, technology, and human behavior. Preventive controls must be paired with contractual guardrails, employee education, and transparent communications. Summarize lessons in postmortems, assign owners, and update dashboards so momentum continues long after the headline fades.
""",
        "mnemonic": {
            "title": "SHIELD DATA",
            "items": [
                {"letter": "S", "phrase": "Segment datasets", "detail": "Keep highly regulated information in isolated stores with explicit approval workflows."},
                {"letter": "H", "phrase": "Hash before logging", "detail": "Use strong hashing or tokenization when capturing telemetry to avoid storing raw identifiers."},
                {"letter": "I", "phrase": "Inform users", "detail": "Provide clear consent prompts and privacy notices whenever assistants access sensitive context."},
                {"letter": "E", "phrase": "Encrypt everywhere", "detail": "Apply encryption in transit and at rest, including for observability pipelines and vendor integrations."},
                {"letter": "L", "phrase": "Limit recall", "detail": "Cap how much historical data an assistant can surface per interaction."},
                {"letter": "D", "phrase": "Discover blind spots", "detail": "Continuously update classification catalogs based on new projects, regulations, and red-team feedback."},
                {"letter": "D", "phrase": "Document flows", "detail": "Maintain diagrams showing where data enters, how it is processed, and who can access the results."},
                {"letter": "A", "phrase": "Audit plug-ins", "detail": "Review scopes, retention, and breach notification procedures for every integration."},
                {"letter": "T", "phrase": "Test redaction", "detail": "Use synthetic and real-world scenarios to ensure sensitive terms are masked under pressure."},
                {"letter": "A", "phrase": "Align with regulators", "detail": "Engage privacy counsel to map controls to legal obligations and update stakeholders regularly."},
            ],
        },
        "pitfall_intro": """
Privacy programs falter when assumptions go unchecked. Recognizing pitfalls ahead of time prevents expensive rework and reputational harm. Use this list as a pre-flight checklist before launching new features or integrations; if any item feels uncertain, pause and address it before customer data is exposed.
""",
        "pitfalls": [
            {"title": "Static dictionaries", "detail": "Failing to update redaction lists leaves new product names and identifiers exposed."},
            {"title": "Shadow analytics", "detail": "Teams export raw logs to spreadsheets or BI tools without privacy review."},
            {"title": "Over-trusting vendors", "detail": "Third parties may store transcripts for training, creating unmonitored copies of sensitive data."},
            {"title": "Opaque consent", "detail": "Users may not realize their data fuels personalization, leading to surprise and complaints."},
            {"title": "Ignoring localization", "detail": "Sensitive terms vary by region and language; one-size-fits-all filters miss nuances."},
            {"title": "Delayed breach assessment", "detail": "Without rapid logging and access provenance, legal teams cannot determine notification timelines."},
        ],
        "takeaway_intro": """
Turn privacy theory into daily practice. Prioritize a handful of actions that materially reduce disclosure risk while improving confidence. Share progress visibly so teams understand how their efforts protect customers and colleagues.
""",
        "takeaways": [
            {"title": "Create a privacy control inventory", "detail": "List redaction engines, consent flows, and audit vaults, assigning owners and review cadences."},
            {"title": "Launch a plug-in review board", "detail": "Require data handling attestations and monitor runtime behavior for every integration."},
            {"title": "Instrument sensitive-entity dashboards", "detail": "Track redaction hit rates, false positives, and emerging terminology with executive-ready visuals."},
            {"title": "Codify consent experiences", "detail": "Design UI copy that explains why data is needed and offers easy escalation to human agents."},
            {"title": "Embed privacy champions", "detail": "Train representatives in each business unit to surface concerns and coordinate improvements."},
            {"title": "Schedule adversarial privacy drills", "detail": "Simulate leaks and walk through legal, communications, and remediation workflows quarterly."},
        ],
        "takeaway_close": """
Treat privacy controls as living systems. Regular reviews, transparent reporting, and collaborative ownership transform compliance from a checkbox into a competitive advantage. Celebrate milestones—successful audits, reduced false positives, faster incident response—to remind the organization that diligent privacy practices unlock innovation instead of slowing it down.
""",
        "reflection_questions": [
            "Which assistant workflows currently request more data than necessary, and how can you enforce minimization?",
            "What assurances do you have that third-party integrations delete sensitive transcripts after fulfilling requests?",
            "How quickly could you notify regulators and customers if a disclosure occurred today?",
            "Which metrics best demonstrate to executives that privacy controls are effective?",
            "How will you involve employees outside security—such as marketing, product, and HR—in ongoing privacy drills and education?",
        ],
        "mindset": [
            """
Approach privacy as a shared value proposition. When teams understand how protecting sensitive data deepens customer loyalty, investment in controls becomes a growth strategy rather than a hurdle.
""",
            """
Adopt a learner's mindset. Regulations, product offerings, and attacker tactics evolve constantly. Stay curious, attend workshops, and share lessons so the organization adapts together.
""",
            """
Recognize emotional labor. Privacy incidents involve concerned customers and employees. Prepare empathetic communications and empower support teams to respond compassionately.
""",
            """
Celebrate transparency. Publishing updates on privacy improvements builds trust internally and externally, reinforcing that accountability is core to your culture. Invite questions from employees, customers, and regulators, and respond with evidence of progress. Over time, openness transforms privacy from a compliance obligation into a differentiator that sets your AI program apart.
""",
        ],
    },
    {
        "lesson_id": "4bd38fce-c4ad-471e-98a8-fd56164ef455",
        "slug": "owasp_llm03_supply_chain_vulnerabilities",
        "title": "OWASP LLM03: Supply Chain Vulnerabilities",
        "subtitle": "Securing data, models, and tooling end-to-end",
        "difficulty": 3,
        "estimated_time": 130,
        "order_index": 6,
        "prerequisites": [],
        "concepts": [
            "model provenance",
            "dependency security",
            "dataset integrity",
            "artifact signing",
            "vendor attestation",
            "continuous assurance",
        ],
        "learning_objectives": [
            "Trace how compromised datasets, models, or build tooling cascade into production assistants.",
            "Design verification workflows that validate integrity at every stage of the LLM lifecycle.",
            "Implement automated checks that block untrusted artifacts, plug-ins, and datasets from deployment.",
            "Evaluate contractual and technical signals when vetting LLM vendors, open-source projects, and marketplaces.",
            "Coordinate security, ML engineering, and procurement teams around ongoing supply chain risk assessments.",
        ],
        "post_assessment": [
            {
                "question": "Which scenario best illustrates a supply chain vulnerability in an LLM pipeline?",
                "options": [
                    "An attacker convinces a user to type a jailbreak in chat.",
                    "A compromised model weight update from a third-party repository introduces a backdoor that exfiltrates prompts.",
                    "A data scientist forgets to archive an experiment report.",
                    "A GPU cluster experiences temporary latency during peak hours.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
            {
                "question": "Why should organizations maintain an SBOM (software bill of materials) for LLM deployments?",
                "options": [
                    "SBOMs slow down procurement and should be avoided.",
                    "They provide traceability for models, datasets, and libraries so teams can respond quickly when vulnerabilities are disclosed.",
                    "LLM supply chains change too quickly for documentation to matter.",
                    "SBOMs only apply to binary executables, not ML artifacts.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Which control most effectively detects tampering in a model release pipeline?",
                "options": [
                    "Allow direct pushes to production artifact stores.",
                    "Verify digital signatures, compare hashes, and enforce build reproducibility before promotion.",
                    "Rely on verbal confirmation from the ML engineer who trained the model.",
                    "Skip validation when models come from popular open-source hubs.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
            {
                "question": "How can procurement teams contribute to supply chain resilience?",
                "options": [
                    "Focus solely on price and feature comparisons.",
                    "Embed security questionnaires, require incident response commitments, and track vendor attestations over time.",
                    "Assume vendors will volunteer breach details without prompting.",
                    "Outsource all due diligence to legal counsel.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "the manipulation or compromise of datasets, models, tooling, or plug-ins that underpin conversational AI",
            "business_context": "LLM platforms that rely on open-source components, vendor APIs, and continuous fine-tuning across distributed teams",
            "attacker_motivation": "the leverage gained by corrupting a single artifact that propagates to thousands of deployments",
            "human_factor": "busy engineers who assume upstream sources are trustworthy and skip provenance checks to meet deadlines",
            "control_challenge": "fragmented ownership across data science, DevOps, and procurement leaves gaps in verification",
            "innovation_balance": "building rapid experimentation pipelines that still enforce authenticity and traceability",
            "closing_emphasis": "supply chain assurance is the backbone of sustainable AI innovation",
        },
        "short_name": "Supply Chain Vulnerabilities",
        "llm_code": "OWASP LLM03",
        "attack_vectors": [
            {
                "name": "Tainted training datasets",
                "detail": "adversaries seed public corpora or shared marketplaces with malicious records that bias or backdoor the model",
                "detail_secondary": "poisoned examples may carry trigger phrases that activate only in production, evading validation",
                "impact": "assistants leak secrets, hallucinate targeted content, or open covert channels",
                "impact_secondary": "incident response struggles to prove provenance because data lineage is incomplete",
                "detection": "anomaly detection on gradient updates and outlier analysis during evaluation",
                "telemetry": "dataset inventories that track who sourced each file, when, and under what license",
                "mitigation": "curate datasets with cryptographic hashing, reputation scores, and manual review of high-risk segments",
                "lesson_alignment": "OWASP emphasis on data supply integrity",
                "mitigation_reinforcement": "establish escalation paths when red teams inject canary data and verify alerts fire",
            },
            {
                "name": "Compromised model artifacts",
                "detail": "threat actors tamper with model weights or tokenizer files hosted on public repositories or artifact mirrors",
                "detail_secondary": "backdoors activate when specific tokens appear, granting the attacker control over outputs",
                "impact": "production assistants behave unpredictably or intentionally leak information",
                "impact_secondary": "trust in open-source ecosystems declines, slowing innovation",
                "detection": "hash mismatches, signature validation failures, and runtime behavior drift",
                "telemetry": "artifact registries that store version histories, provenance attestations, and promotion approvals",
                "mitigation": "enforce signed releases, reproducible builds, and isolated promotion environments",
                "lesson_alignment": "OWASP control for secure model supply chains",
                "mitigation_reinforcement": "perform periodic binary diffing and run sandbox inference before any artifact reaches production",
            },
            {
                "name": "CI/CD pipeline compromise",
                "detail": "attackers exploit build agents, secrets stores, or orchestration pipelines to inject malicious code or prompts",
                "detail_secondary": "once inside, they modify evaluation scripts so backdoors remain undetected",
                "impact": "automated deployments ship corrupted prompts, configs, or plug-ins across environments",
                "impact_secondary": "incident timelines stretch because tampering appears to originate from legitimate automation",
                "detection": "monitoring build agent integrity, unusual credential usage, and deviations from reproducible build outputs",
                "telemetry": "signed attestations from each pipeline step and immutable logs feeding security data lakes",
                "mitigation": "harden build infrastructure with zero-trust access, ephemeral runners, and secrets management",
                "lesson_alignment": "OWASP focus on operational guardrails and deployment hygiene",
                "mitigation_reinforcement": "schedule purple-team exercises targeting CI/CD to validate detective controls",
            },
            {
                "name": "Malicious plug-ins and vendor APIs",
                "detail": "marketplace components request excessive permissions or return tampered responses",
                "detail_secondary": "vendors may quietly change terms of service or storage practices, creating hidden risk",
                "impact": "assistants execute unauthorized actions, exfiltrate data, or deliver falsified insights",
                "impact_secondary": "supply chain incidents damage strategic partnerships and trigger legal disputes",
                "detection": "continuous monitoring of API scopes, latency anomalies, and response integrity",
                "telemetry": "vendor scorecards combining technical tests, contract reviews, and incident history",
                "mitigation": "establish integration review boards, require attestation of security controls, and sandbox plug-ins",
                "lesson_alignment": "OWASP requirement for third-party risk management",
                "mitigation_reinforcement": "renew vendor approvals only after verifying logs, penetration test results, and remediation progress",
            },
        ],
        "impact_overview": """
Supply chain compromises erode confidence in every feature built on top of the LLM platform. Executives worry about brand damage if tampered assistants mislead customers. ML teams face rework when artifacts cannot be trusted. Security leaders must explain to regulators and partners how integrity was lost. Because supply chains connect numerous vendors and open-source communities, even a rumor of compromise can trigger procurement freezes and board-level investigations. Recovery is expensive: contracts are renegotiated, independent auditors are hired, and engineering roadmaps pause while teams rebuild trust from the ground up. The opportunity cost is equally painful—while teams focus on crisis management, competitors continue shipping new capabilities, widening the innovation gap. Metrics such as time-to-detect, time-to-respond, and vendor attestation coverage quickly become board-level KPIs.

Customers and investors now demand evidence that integrity controls reach beyond the core engineering group. They ask procurement to prove vendors follow the same verification practices, finance to quantify contingent liabilities, and legal to model cross-border disclosure requirements. Breach costs extend well beyond immediate recovery, including lost renewal revenue, accelerated churn, insurance premium hikes, and delayed regulatory approvals for new markets. Teams that lack rehearsed playbooks burn out while rushing ad hoc mitigations; morale slips as builders question whether they can innovate safely. Conversely, organizations that continuously demonstrate supply chain assurance earn reputational capital that smooths executive buy-in for future AI initiatives and reassures watchdogs that experimentation remains under control.
""",
        "impact_zones": [
            {
                "area": "Platform reliability",
                "detail": "Corrupted artifacts cause outages or erratic behavior, forcing rollback efforts and delaying product launches. Incident response consumes engineering cycles that would otherwise ship customer-facing improvements.",
            },
            {
                "area": "Vendor relationships",
                "detail": "Customers question whether contractual controls exist, leading to renegotiations or loss of market share. Sales teams must rebuild credibility with detailed remediation plans and evidence of stronger guardrails.",
            },
            {
                "area": "Compliance",
                "detail": "Tampering can invalidate certifications like SOC 2 or ISO 27001 if change-management evidence is missing. Regulators may demand third-party audits and ongoing reporting until the organization proves sustainable fixes.",
            },
            {
                "area": "Threat intelligence",
                "detail": "Nation-state actors increasingly target AI supply chains to insert stealthy capabilities for future operations. Sharing indicators of compromise with industry peers becomes essential to stay ahead of coordinated campaigns.",
            },
        ],
        "detection_intro": """
Integrity detection combines cryptography, behavioral analytics, and human review. Every dataset, model, and plug-in should emit provenance metadata that downstream systems can verify. Teams compare runtime metrics against baselines to catch subtle drift. When anomalies arise, responders trace lineage quickly because inventories and SBOMs tie each asset to owners, approvals, and upstream sources.
""",
        "detection_focus": [
            {
                "name": "Artifact signature validation",
                "detail": "Ensure every model weight, tokenizer, and prompt template carries a trusted signature.",
                "correlation": "Cross-check against build pipelines and SBOM entries to confirm provenance.",
                "forensics": "Retain signature metadata and promotion approvals to reconstruct tampering attempts.",
            },
            {
                "name": "Dataset lineage gaps",
                "detail": "Alert when ingestion jobs lack source metadata, licensing info, or review attestations.",
                "correlation": "Tie to teams responsible for curation and require remediation before use.",
                "forensics": "Store hashes and sampling reports to verify authenticity if suspicious behavior emerges.",
            },
            {
                "name": "Pipeline runtime anomalies",
                "detail": "Monitor build agents, container images, and orchestration logs for unexpected processes or network calls.",
                "correlation": "Compare with change tickets and release schedules to differentiate maintenance from compromise.",
                "forensics": "Collect system snapshots and command histories for incident responders.",
            },
            {
                "name": "Vendor telemetry gaps",
                "detail": "Flag when third-party services stop delivering expected logs, attestations, or health metrics.",
                "correlation": "Coordinate with procurement and legal to escalate non-compliance.",
                "forensics": "Archive communications and runtime data to inform contract enforcement and customer notifications.",
            },
        ],
        "guardrail_intro": """
Strong guardrails treat every artifact as suspect until proven trustworthy. Automate verification, but keep humans in the loop for high-risk promotions. Align technical controls with procurement language so that vendors commit to the same assurances internally enforced.
""",
        "guardrail_layers": [
            {
                "name": "Signed artifact registry",
                "detail": "Centralizes models, prompts, and dependencies with mandatory signature checks before deployment.",
                "conditions": "before any asset is promoted beyond staging",
                "practice": "enforce reproducible builds and reject artifacts without matching hashes",
                "alignment": "secure SDLC requirements and audit expectations",
            },
            {
                "name": "Dataset provenance portal",
                "detail": "Catalogs sources, licenses, and review attestations for every dataset and feature store.",
                "conditions": "during ingestion and periodic recertification",
                "practice": "assign data stewards who approve changes and monitor for unauthorized uploads",
                "alignment": "data governance councils and regulatory filings",
            },
            {
                "name": "Pipeline attestation fabric",
                "detail": "Generates cryptographic attestations for each CI/CD step, from training to deployment.",
                "conditions": "whenever automation promotes an artifact or updates prompts",
                "practice": "store attestations in immutable logs accessible to security teams",
                "alignment": "DevSecOps maturity models and compliance evidence",
            },
            {
                "name": "Vendor assurance program",
                "detail": "Combines questionnaires, penetration test reviews, runtime monitoring, and breach notification clauses.",
                "conditions": "prior to onboarding and at renewal",
                "practice": "score vendors, track remediation, and escalate exceptions to executive steering committees",
                "alignment": "third-party risk management frameworks",
            },
        ],
        "operational_story": """
Supply chain defense thrives when teams speak a common language. ML engineers map technical pipelines, security architects define control points, procurement negotiates assurances, and compliance tracks evidence. Regular war games surface weak links, while retrospectives convert incidents into updated contracts, tooling, and playbooks. Mature programs also invest in threat intelligence exchanges and community working groups, sharing anonymized findings so the entire ecosystem benefits. That collaboration shortens response times and reinforces that defending supply chains is a collective mission. Leadership plays a key role by setting clear priorities, funding automation, and recognizing teams that identify vulnerabilities before attackers do.

Day-to-day operations reflect this unity. Daily stand-ups pair ML engineers with SREs to review attestation dashboards, procurement officers share updates from vendor audits, and legal briefings translate contractual guarantees into technical acceptance tests. When anomalies surface, a fusion cell assembles within minutes, correlating telemetry across datasets, artifact registries, and plug-in marketplaces. Playbooks include communication templates for regulators, investors, and customers so trust is rebuilt proactively rather than reactively. Teams celebrate near-misses the same way they celebrate shipped features, reinforcing that supply chain vigilance is as strategic as rapid product delivery.
""",
        "video": {
            "title": "Inside an AI Supply Chain Compromise",
            "url": "https://www.youtube.com/watch?v=0o5XzQ2v1LY",
            "description": "A former CISO and ML architect dissect a real-world model tampering case, highlighting how pipeline gaps allowed malicious weights to ship and how the organization rebuilt trust. They also share tooling demos and governance artifacts used to regain certifications.",
            "focus_points": [
                "Note the checkpoints that failed and how attackers moved between data, model, and deployment stages.",
                "Observe the incident communications strategy that aligned executives, regulators, and customers.",
                "List the tooling upgrades introduced post-incident, including artifact registries and attestation systems.",
                "Consider how your organization would detect similar tampering today.",
            ],
        },
        "diagram": {
            "intro": "Supply chain security spans sourcing, training, evaluation, and deployment stages:",
            "ascii": """
  +------------+    +-------------+    +----------------+    +---------------+
  | Data Intake|--> | Model Build |--> | Evaluation Lab |--> | Deployment Hub|
  +------------+    +-------------+    +----------------+    +---------------+
        |                |                   |                       |
        v                v                   v                       v
  [Provenance]    [Signed Artifacts]   [Bias/Backdoor Tests]   [Runtime Attestation]
""",
            "explanation": "Each stage emits attestations and telemetry that downstream steps verify. If any checkpoint fails, promotions halt until humans review and resolve discrepancies.",
            "callouts": [
                "Data intake includes license validation, hashing, and reviewer approvals.",
                "Model builds run on hardened infrastructure with ephemeral credentials.",
                "Evaluation labs test for bias, robustness, and hidden triggers before release.",
                "Deployment hubs verify signatures and monitor runtime behavior against baselines.",
            ],
        },
        "lab_setup": {
            "overview": """
Conduct an integrity drill on your LLM pipeline. Participants will trace a model from data ingestion to deployment, verify signatures, and simulate tampering to ensure controls detect the issue. Encourage observers from legal, finance, and customer-facing teams to attend so they understand the technical safeguards protecting their products.
""",
            "objective": "Demonstrate end-to-end traceability and the ability to block compromised artifacts from reaching production.",
            "steps": [
                "Document the current pipeline, noting tooling, owners, and hand-offs for data, models, and prompts. Map pain points and manual steps that attackers could exploit.",
                "Inject a tampered dataset sample and observe whether provenance checks flag the anomaly. Record how quickly alerts reach the right teams and whether runbooks are clear.",
                "Modify model weights in staging to simulate repository compromise and verify signature validation fails promotion. Ensure rollback procedures are rehearsed and documented.",
                "Corrupt a CI/CD runner image and confirm runtime monitoring detects unauthorized processes. Track how quickly containment teams isolate the affected runner and restore clean images.",
                "Review vendor plug-in scopes, revoking one to confirm access changes propagate and are logged.",
                "Correlate telemetry from supply chain scanners with procurement contracts to confirm service-level guarantees are being honored. Document any mismatches between technical evidence and contractual promises.",
                "Run a joint exercise with a strategic vendor to rotate signing keys and publish new attestations. Observe how updates propagate through mirrors, caches, and downstream teams, noting where manual approvals slow the process.",
                "Test incident communication by notifying stakeholders, legal, and vendors with a simulated breach report.",
                "Update SBOM entries and attestations to reflect remediation steps.",
                "Hold a retrospective capturing tooling gaps, process improvements, and policy updates.",
            ],
            "validation": "The drill succeeds when tampering attempts trigger alerts, promotions stop automatically, and all stakeholders understand their roles in remediation. Teams should exit with refreshed contact trees, quantified detection-to-response metrics, and a prioritized backlog that funds automation before the next quarterly review. Capture follow-up actions, schedule tooling upgrades, and plan knowledge-sharing sessions so improvements stick.",
        },
        "code_exercise": {
            "overview": """
Implement an artifact verification utility that checks signatures and hashes before loading a model. Integrate the tool into CI/CD so deployments fail fast when provenance is uncertain.
""",
            "language": "python",
            "snippet": """
import hashlib
import pathlib

def verify_hash(path: pathlib.Path, expected_hash: str) -> bool:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest() == expected_hash

def validate_artifact(path: pathlib.Path, signature_valid: bool, expected_hash: str) -> None:
    if not signature_valid:
        raise RuntimeError(f"Signature validation failed for {path.name}")
    if not verify_hash(path, expected_hash):
        raise RuntimeError(f"Hash mismatch detected for {path.name}")

    print(f"Artifact {path.name} passed integrity checks")
""",
            "explanation": "While simplified, this utility demonstrates the importance of verifying both signatures and hashes. Production systems should integrate with attestation services, support multiple hashing algorithms, and emit structured logs for SIEM ingestion.",
            "callouts": [
                "Fetch expected hashes and signatures from a trusted registry, not configuration files committed to source control.",
                "Fail closed—if verification services are unavailable, pause deployments rather than skipping checks.",
                "Record verification events for auditors and incident responders.",
                "Test error handling paths to ensure engineers understand how to remediate failed checks.",
                "Combine with behavioral smoke tests that run sample inferences before go-live.",
            ],
        },
        "case_intro": """
Supply chain incidents are no longer theoretical. Review these examples to understand attacker tradecraft and response strategies. As you study them, note which controls failed, which communication channels worked, and how long recovery took so you can benchmark your own readiness.
""",
        "case_studies": [
            {
                "organization": "AI marketing platform",
                "scenario": "A compromised open-source model update introduced a hidden instruction that redirected prompts to an attacker-controlled server.",
                "finding": "The company lacked signature verification and relied on trust in the repository maintainer.",
                "response": "They implemented signed artifact registries, sandboxed evaluation, and automated alerts when dependencies changed.",
            },
            {
                "organization": "Industrial automation firm",
                "scenario": "A contractor uploaded poisoned maintenance logs into the training dataset, causing the assistant to recommend unsafe equipment configurations.",
                "finding": "Data ingestion had no review workflow, and provenance metadata was incomplete.",
                "response": "The firm introduced data steward approvals, hashing, and anomaly detection on training inputs.",
            },
            {
                "organization": "Financial services chatbot vendor",
                "scenario": "A marketplace plug-in altered transaction confirmations to include a phishing link.",
                "finding": "Vendor vetting focused on functionality, not security, and runtime monitoring ignored response integrity.",
                "response": "They established a plug-in review board, sandboxed integrations, and required vendors to provide incident notification SLAs.",
            },
        ],
        "case_outro": """
These stories underscore that supply chain resilience depends on culture and controls. Verification is ongoing—not a one-time audit. Use them to spark tabletop discussions about how your organization would respond under similar pressure.
""",
        "mnemonic": {
            "title": "CHAIN SAFE",
            "items": [
                {"letter": "C", "phrase": "Catalog everything", "detail": "Maintain SBOMs for datasets, models, prompts, and plug-ins."},
                {"letter": "H", "phrase": "Hash artifacts", "detail": "Compare cryptographic fingerprints before promotion."},
                {"letter": "A", "phrase": "Attest pipelines", "detail": "Capture signed evidence from each automation step."},
                {"letter": "I", "phrase": "Inspect vendors", "detail": "Review controls, certifications, and breach history for partners."},
                {"letter": "N", "phrase": "Notify stakeholders", "detail": "Share supply chain risk reports with executives and customers."},
                {"letter": "S", "phrase": "Sandbox updates", "detail": "Test new artifacts in isolated environments before broad deployment."},
                {"letter": "A", "phrase": "Audit regularly", "detail": "Schedule recurring reviews of ingestion, build, and deployment processes."},
                {"letter": "F", "phrase": "Fail closed", "detail": "Block promotions when verification services are unavailable."},
                {"letter": "E", "phrase": "Educate builders", "detail": "Train engineers and procurement specialists on supply chain red flags."},
            ],
        },
        "pitfall_intro": """
Supply chain defenses crumble when organizations assume trust instead of verifying. Recognize these traps before attackers exploit them. Review the list during sprint planning and vendor onboarding to keep pressure on the basics.
""",
        "pitfalls": [
            {"title": "Untracked dependencies", "detail": "Shadow libraries and models enter production without appearing in inventories. Attackers target these blind spots because they often escape patching and verification."},
            {"title": "One-time vendor assessments", "detail": "Security questionnaires at onboarding lose relevance without continuous monitoring. Vendors evolve, change staff, and adopt new tooling—controls must evolve too."},
            {"title": "Ignored warnings", "detail": "Teams silence signature or hash alerts because they believe false positives are harmless."},
            {"title": "Siloed ownership", "detail": "No single leader coordinates data, model, and DevOps stakeholders, so gaps persist."},
            {"title": "Delayed incident response", "detail": "Without lineage records, teams waste hours hunting for compromised artifacts."},
            {"title": "Complacent culture", "detail": "Success breeds overconfidence, reducing appetite for rehearsals and audits."},
        ],
        "takeaway_intro": """
Translate supply chain awareness into tangible improvements. Focus on the controls that deliver visibility and fast response. Treat this list as a living roadmap reviewed at steering committees so progress is tracked and celebrated.
""",
        "takeaways": [
            {"title": "Publish a living SBOM", "detail": "Update inventories automatically whenever datasets, models, or plug-ins change."},
            {"title": "Automate signature enforcement", "detail": "Integrate verification utilities into CI/CD gates and break builds on failure."},
            {"title": "Stand up a vendor assurance council", "detail": "Review attestations, incidents, and remediation plans with procurement and legal."},
            {"title": "Instrument pipeline observability", "detail": "Collect metrics and alerts for build agents, promotion steps, and artifact registries."},
            {"title": "Run quarterly supply chain drills", "detail": "Simulate tampering, validate escalation paths, and update playbooks."},
            {"title": "Share threat intel", "detail": "Coordinate with industry groups and ISACs to learn about emerging supply chain attacks."},
            {"title": "Report progress", "detail": "Publish dashboards summarizing verification coverage, incident learnings, and vendor posture so leadership and customers see continuous improvement."},
        ],
        "takeaway_close": """
Supply chain resilience becomes a competitive differentiator. Customers gravitate toward providers who prove integrity, transparency, and speed of response. Share progress in quarterly reviews and customer updates so the investment in verification is visible and appreciated.
""",
        "reflection_questions": [
            "Do you know every dataset, model, and plug-in running in production today?",
            "How quickly can you trace a compromised artifact back to its source?",
            "Which vendors provide timely security attestations, and which require escalation?",
            "What rehearsals will you schedule this quarter to test pipeline defenses?",
            "How will you communicate supply chain risk posture to executives, customers, and auditors in terms they understand?",
        ],
        "mindset": [
            """
Supply chain risk management rewards curiosity and persistence. Encourage teams to ask "Where did this artifact come from?" and celebrate those who uncover gaps. Build rituals—such as monthly show-and-tell sessions—where engineers highlight discoveries and lessons.
""",
            """
Adopt a builder mindset. Secure pipelines empower faster iteration because engineers trust the foundation. Highlight wins when automation catches tampering, and document how the same controls open doors for new features that would otherwise feel too risky to attempt.
""",
            """
View vendors as partners. Share expectations, provide feedback, and collaborate on improvements instead of treating assessments as adversarial chores.
""",
            """
Keep learning. Study public incidents, contribute to open-source security initiatives, and bring lessons back to your organization.
""",
            """
Invest in continuous education. Host lunch-and-learns, share playbooks, and rotate engineers through supply chain security sprints so expertise spreads beyond a single champion.
""",
            """
Track progress visibly. Dashboards highlighting verification coverage, vendor posture, and incident lessons keep leadership engaged and demonstrate how supply chain security fuels innovation.
""",
        ],
    },
    {
        "lesson_id": "fbcd2d30-664a-46c1-9b9c-ec4f175aba17",
        "slug": "owasp_llm04_data_and_model_poisoning",
        "title": "OWASP LLM04: Data and Model Poisoning",
        "subtitle": "Detecting and disarming stealthy manipulations",
        "difficulty": 3,
        "estimated_time": 135,
        "order_index": 7,
        "prerequisites": [],
        "concepts": [
            "data poisoning",
            "model poisoning",
            "backdoor triggers",
            "gradient monitoring",
            "adversarial evaluation",
            "continuous retraining governance",
        ],
        "learning_objectives": [
            "Explain how poisoned data and model updates introduce covert behaviors into LLMs.",
            "Design training and evaluation pipelines that surface anomalous patterns before deployment.",
            "Implement runtime mitigations that contain suspected poisoning without halting business operations.",
            "Assess the risk posed by user feedback loops, federated updates, and reinforcement learning systems.",
            "Establish governance that tracks provenance and accountability for all model changes.",
        ],
        "post_assessment": [
            {
                "question": "What makes model poisoning particularly dangerous for LLM deployments?",
                "options": [
                    "It only affects response latency, not behavior.",
                    "Backdoors can remain dormant during testing yet activate under specific triggers in production.",
                    "Poisoning is easily detected by basic spell-check tools.",
                    "It is relevant only to vision models, not language models.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
            {
                "question": "Which signal best indicates a possible poisoning event during fine-tuning?",
                "options": [
                    "Gradual improvement in benchmark accuracy.",
                    "Sudden drops in loss accompanied by unusual activation patterns for niche prompts.",
                    "Stable gradient norms across epochs.",
                    "A slight increase in training time due to larger datasets.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
            {
                "question": "How should organizations respond when poisoning is suspected but not yet confirmed?",
                "options": [
                    "Ignore the signal until customers complain.",
                    "Quarantine affected models, trigger forensic replay, and activate communication plans while containment steps run.",
                    "Delete all datasets immediately without investigation.",
                    "Announce a breach before gathering evidence.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Which control reduces the likelihood of poisoned feedback loops in reinforcement learning?",
                "options": [
                    "Allow anonymous feedback to directly adjust weights.",
                    "Score and review feedback sources, throttle influence, and audit reward models for drift.",
                    "Disable evaluation checkpoints to keep training fast.",
                    "Treat all user feedback as equally trustworthy.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "adversaries inject malicious patterns into training data or model updates so LLMs behave normally until triggered",
            "business_context": "organizations continually fine-tune assistants with customer conversations, synthetic data, or federated updates",
            "attacker_motivation": "covert control over outputs, enabling disinformation, data leakage, or sabotage without overt compromise",
            "human_factor": "teams rushing to ship improvements accept data contributions and feedback without rigorous screening",
            "control_challenge": "poisoning can hide within high-volume pipelines, evading standard accuracy metrics",
            "innovation_balance": "reward experimentation while codifying checkpoints that catch adversarial influence",
            "closing_emphasis": "poisoning defense is an ongoing discipline that combines ML rigor with classic security mindset",
        },
        "short_name": "Data and Model Poisoning",
        "llm_code": "OWASP LLM04",
        "attack_vectors": [
            {
                "name": "Label flipping attacks",
                "detail": "attackers modify a subset of training examples so harmful responses are labeled as correct",
                "detail_secondary": "the poisoned labels blend into legitimate data, especially when sourced from crowdworkers or public forums",
                "impact": "the model learns to approve or even promote dangerous behaviors when specific cues are present",
                "impact_secondary": "safety evaluations may pass because triggers occur infrequently",
                "detection": "monitor per-class accuracy, confusion matrices, and loss contributions to spot asymmetric shifts",
                "telemetry": "store original labels, annotator IDs, and review timestamps for forensic comparison",
                "mitigation": "establish dual-review for sensitive categories, weight clean data more heavily, and employ robust training techniques",
                "lesson_alignment": "OWASP guidance on defending against data manipulation",
                "mitigation_reinforcement": "rotate red-team scenarios that flip labels to confirm detection pipelines alert",
            },
            {
                "name": "Trigger-based backdoors",
                "detail": "poisoned samples teach the model to respond maliciously when a hidden token or phrase appears",
                "detail_secondary": "triggers may use Unicode homoglyphs, emojis, or uncommon languages to avoid detection",
                "impact": "attackers can activate the backdoor on demand, bypassing guardrails",
                "impact_secondary": "trust evaporates when customers share clips of seemingly unprovoked harmful answers",
                "detection": "activation clustering, neuron coverage analysis, and prompt fuzzing with trigger-like patterns",
                "telemetry": "log embeddings and activations for suspicious prompts to support root-cause analysis",
                "mitigation": "apply pruning, fine-pruning, and defensive distillation, then re-evaluate with adversarial prompts",
                "lesson_alignment": "OWASP call for adversarial robustness",
                "mitigation_reinforcement": "schedule offensive exercises that attempt to implant and detect backdoors using internal tooling",
            },
            {
                "name": "Federated learning poisoning",
                "detail": "malicious clients submit manipulated gradient updates to centralized aggregation services",
                "detail_secondary": "attackers may sybil multiple client identities to amplify influence",
                "impact": "global models adopt biased or dangerous behaviors despite honest participants",
                "impact_secondary": "traceability suffers when aggregation obscures which client introduced the anomaly",
                "detection": "gradient clustering, anomaly scoring, and secure aggregation protocols that flag outliers",
                "telemetry": "retain per-client statistics, trust scores, and update histories for auditing",
                "mitigation": "use Byzantine-resilient aggregation, rate limits, and reputation systems",
                "lesson_alignment": "OWASP emphasis on distributed training security",
                "mitigation_reinforcement": "simulate malicious clients in staging to ensure detection thresholds respond appropriately",
            },
            {
                "name": "Reinforcement learning feedback abuse",
                "detail": "attackers submit coordinated feedback to reward harmful behaviors during RLHF or ongoing fine-tuning",
                "detail_secondary": "botnets or disgruntled insiders can inflate ratings or exploit moderation blind spots",
                "impact": "reward models shift, leading assistants to favor manipulative or policy-violating answers",
                "impact_secondary": "detecting the change is difficult because overall satisfaction scores may remain high",
                "detection": "monitor reward distribution, feedback source diversity, and outcome skew",
                "telemetry": "track feedback provenance, device fingerprints, and reviewer reputation",
                "mitigation": "throttle influence of untrusted sources, require secondary review for sensitive topics, and retrain reward models with clean data",
                "lesson_alignment": "OWASP recommendation for human-in-the-loop safeguards",
                "mitigation_reinforcement": "conduct feedback integrity audits with privacy, legal, and customer experience teams",
            },
        ],
        "impact_overview": """
Poisoning blurs the line between reliable automation and adversarial control. Executives grapple with reputational fallout when assistants betray brand values. Engineers lose trust in their own metrics. Regulators may view poisoning as evidence of inadequate due diligence, leading to fines or mandated oversight. Because poisoned models can lie dormant, the incident timeline often stretches from the initial injection months earlier to the public revelation much later, complicating forensics and communications.

The blast radius extends beyond immediate systems. Marketing teams must recalibrate campaigns after tainted recommendations reach customers. Procurement renegotiates vendor contracts to mandate stronger provenance evidence, delaying innovation roadmaps. Incident communications absorb leadership attention for weeks, affecting investor relations and product announcements. Even after remediation, analysts and journalists scrutinize whether the organization can be trusted with autonomous decision-making. Teams that lack transparent audit trails struggle to rebut claims of negligence, while peers with mature poisoning defenses convert their readiness into competitive messaging that reassures skeptical buyers.

Meanwhile, adversaries learn from each engagement. They study public postmortems, adapt trigger phrases, and trade successful tactics across underground forums. Organizations that fail to institutionalize lessons find themselves reliving near-identical incidents a quarter later. Sustained vigilance requires storytelling: translating technical findings into executive narratives, training modules, and procurement requirements so every stakeholder understands that poisoning is not just a research curiosity but a board-level resilience issue.
""",
        "impact_zones": [
            {
                "area": "Safety and compliance",
                "detail": "Harmful responses can violate moderation policies, consumer protection laws, or sector-specific regulations like healthcare advisories.",
            },
            {
                "area": "Decision accuracy",
                "detail": "Backdoors may subtly nudge financial, legal, or operational decisions toward attacker objectives, distorting analytics and insights.",
            },
            {
                "area": "Operational resilience",
                "detail": "Incident response teams must rollback models, rebuild pipelines, and communicate with stakeholders, consuming significant resources.",
            },
            {
                "area": "Trust in automation",
                "detail": "Employees and customers hesitate to rely on assistants after a poisoning incident, slowing adoption of AI initiatives.",
            },
            {
                "area": "Executive oversight",
                "detail": "Boards and audit committees demand detailed evidence explaining how poisoning slipped past defenses, often pausing budget approvals until remediation milestones are achieved.",
            },
            {
                "area": "Community collaboration",
                "detail": "Open-source contributors and academic partners may disengage if their submissions are suspected, shrinking the reviewer pool that normally surfaces anomalies early.",
            },
        ],
        "detection_intro": """
Effective detection layers statistical monitoring with investigative workflows. Teams analyze gradients, activations, and embeddings for anomalies, then pair findings with manual reviews of data provenance. Alerts escalate to cross-functional tiger teams that include ML researchers, security engineers, and product owners to validate severity and coordinate containment.

High-performing programs complement technical indicators with sociotechnical signals: contributor reputation shifts, sudden surges of feedback from new regions, or unexplained delays in vendor attestations. Detection dashboards feed weekly governance forums where trends are debated, thresholds tuned, and hypothesis-driven investigations launched. This cadence prevents monitoring fatigue and keeps poisoning defense aligned with evolving business priorities.
""",
        "detection_focus": [
            {
                "name": "Gradient variance spikes",
                "detail": "Track per-epoch gradient norms and cosine similarity to detect manipulated updates.",
                "correlation": "Align anomalies with data ingestion events or federated client submissions.",
                "forensics": "Store gradient snapshots for replay in isolated environments.",
            },
            {
                "name": "Activation clustering anomalies",
                "detail": "Analyze neuron activations for unexpected clusters tied to rare tokens or triggers.",
                "correlation": "Cross-check with prompt patterns, languages, or user cohorts.",
                "forensics": "Capture activation heatmaps and tracebacks for ML researchers to inspect.",
            },
            {
                "name": "Reward model drift",
                "detail": "Monitor RLHF feedback distributions and reward magnitudes for sudden shifts.",
                "correlation": "Compare with reviewer identities, time periods, and content categories.",
                "forensics": "Maintain immutable logs of feedback, annotations, and applied weightings.",
            },
            {
                "name": "Evaluation regression",
                "detail": "Run adversarial test suites and track performance deltas for high-risk topics.",
                "correlation": "Map failures to specific dataset updates or fine-tuning runs.",
                "forensics": "Version evaluation results and maintain reproducible scripts to demonstrate findings to stakeholders.",
            },
        ],
        "guardrail_intro": """
Guardrails treat every data contribution and model update as potentially hostile. Blend automation that scores risk with manual checkpoints for sensitive domains. Maintain rollback plans so suspect models can be replaced quickly without halting service.
""",
        "guardrail_layers": [
            {
                "name": "Curated data pipelines",
                "detail": "Segment training data sources, apply validation, and require steward approval for high-impact contributions.",
                "conditions": "before ingestion into fine-tuning or reinforcement learning workflows",
                "practice": "sample new data, run toxicity and bias checks, and quarantine suspicious records",
                "alignment": "data governance and responsible AI commitments",
            },
            {
                "name": "Poison detection lab",
                "detail": "Dedicated environment where researchers test models with adversarial prompts, activation analysis, and interpretability tools.",
                "conditions": "prior to release and after any significant model update",
                "practice": "compare results across clean baselines and document anomalies for remediation",
                "alignment": "secure ML development lifecycles",
            },
            {
                "name": "Fine-tuning review board",
                "detail": "Cross-functional group that approves datasets, training objectives, and deployment schedules.",
                "conditions": "when introducing new data sources or modifying reward models",
                "practice": "log decisions, risk assessments, and fallback plans",
                "alignment": "governance frameworks and executive oversight",
            },
            {
                "name": "Runtime mitigation toolkit",
                "detail": "Controls that throttle or route around suspected poisoning, such as safe-mode prompts or fallback models.",
                "conditions": "upon detection of anomalous behavior or confirmed poisoning",
                "practice": "test rollback scripts and safe responses regularly to maintain readiness",
                "alignment": "incident response playbooks and reliability objectives",
            },
        ],
        "operational_story": """
Poisoning defense thrives on collaboration. ML teams surface suspicious metrics, security engineers manage containment, legal and communications craft messaging, and customer success explains temporary safeguards. Lessons feed back into training pipelines, policy updates, and educational programs for data contributors.

Daily stand-ups pair data stewards with SREs to review ingestion exceptions, while procurement briefs stakeholders on vendor posture changes. When alerts trigger, response captains spin up secure war rooms where engineers replay suspect batches, product managers assess customer impact, and compliance validates notification obligations. Post-incident reviews feed a living backlog that funds tooling improvements, tabletop rehearsals, and outreach to community partners that help keep training corpora trustworthy.

Mature teams maintain living dashboards that blend quantitative metrics—like anomaly detection precision and rollback duration—with qualitative feedback from red-teamers and customer advisors. They practice transparent communication, publishing quarterly integrity reports that highlight trends, investments, and remaining risks. This openness builds confidence that even when adversaries strike, the organization will respond decisively, learn quickly, and share insights that strengthen the broader AI community.
""",
        "video": {
            "title": "Unmasking Poisoned Models",
            "url": "https://www.youtube.com/watch?v=F9GmWDmO5bE",
            "description": "Researchers demonstrate real poisoning attacks against language models and share mitigation strategies spanning data hygiene, monitoring, and governance.",
            "focus_points": [
                "Observe how subtle trigger phrases activate malicious behavior.",
                "Note the detection techniques—gradient analysis, interpretability tools, and adversarial evaluation.",
                "Track how the response team coordinated rollback and communications.",
                "List ideas for integrating similar tooling into your pipelines.",
            ],
        },
        "diagram": {
            "intro": "Poisoning defenses weave through data sourcing, training, evaluation, and production response:",
            "ascii": """
  Data Sources --> Validation --> Training Loop --> Evaluation Lab --> Deployment --> Monitoring
        |              |              |                |                 |             |
   Steward Logs   Risk Scores   Gradient Watch   Adversarial Tests   Rollback Plan   Safe Modes
""",
            "explanation": "Every stage emits artifacts—risk scores, logs, tests—that feed the next stage. When monitoring detects anomalies, teams reference upstream evidence to isolate the root cause and activate safe modes.",
            "callouts": [
                "Validation includes deduplication, toxicity scans, and provenance tagging.",
                "Training loops record gradient statistics and checkpoint hashes for auditing.",
                "Evaluation labs maintain red-team prompt suites with documented expectations.",
                "Monitoring can trigger safe-mode responses or rollback to known-good checkpoints.",
            ],
        },
        "lab_setup": {
            "overview": """
Run a poisoning readiness workshop. Participants will plant controlled backdoors, detect them, and practice rolling back to clean checkpoints while maintaining service continuity.
""",
            "objective": "Validate that teams can detect, contain, and remediate poisoned models without damaging customer trust.",
            "steps": [
                "Select a non-production model and inject a benign trigger phrase through fine-tuning.",
                "Record baseline metrics for gradients, activation clusters, and evaluation scores.",
                "Run adversarial tests to confirm the backdoor activates under the trigger and remains dormant otherwise.",
                "Execute detection pipelines—gradient monitoring, activation clustering, and prompt fuzzing—to surface anomalies.",
                "Introduce corrupted user feedback and observe how reward models and dashboards respond, noting which reviews catch the manipulation.",
                "Initiate incident response: quarantine the model, notify stakeholders, and activate safe-mode prompts in production.",
                "Validate provenance logs by tracing each tampered artifact back to its submission path and confirming access controls prevented spread to other systems.",
                "Rollback to a clean checkpoint and verify normal behavior through regression testing.",
                "Document the timeline, update playbooks, and plan follow-up actions such as data steward training.",
                "Share findings with executives, emphasizing how governance and tooling worked together, and record metrics comparing detection, response, and communication intervals.",
            ],
            "validation": "The workshop succeeds when teams detect the backdoor quickly, communicate clearly, and restore service using documented procedures. Facilitators should capture quantified mean-time-to-detect, mean-time-to-contain, and stakeholder satisfaction scores, then translate them into roadmap priorities for automation, staffing, and vendor engagement.",
        },
        "code_exercise": {
            "overview": """
Implement a simple activation clustering detector that flags prompts producing similar hidden activations, a common sign of backdoors.
""",
            "language": "python",
            "snippet": """
import numpy as np
from sklearn.cluster import DBSCAN

def cluster_activations(activations: np.ndarray, eps: float = 0.5, min_samples: int = 5):
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(activations)
    clusters = {}
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(idx)
    return clusters

def flag_suspicious(clusters: dict, prompts: list[str]) -> list[str]:
    suspicious = []
    for label, indices in clusters.items():
        if label != -1 and len(indices) < 10:
            suspicious.extend(prompts[i] for i in indices)
    return suspicious
""",
            "explanation": "Activation clustering helps surface groups of prompts that share unusual internal representations, a hallmark of backdoors. Production systems would combine this signal with gradient monitoring, prompt fuzzing, and human review to confirm poisoning before taking action.",
            "callouts": [
                "Collect activations from multiple layers to increase detection fidelity.",
                "Tune clustering parameters per model and workload.",
                "Store suspicious prompts for deeper investigation and red-team replay.",
                "Automate notifications to ML security engineers when new clusters appear.",
                "Integrate with safe-mode workflows that route risky prompts to fallback systems.",
            ],
        },
        "case_intro": """
Reviewing real and simulated poisoning incidents helps teams prepare psychologically and technically for high-pressure scenarios. Use each case to map indicators of compromise, communication gaps, and contractual triggers that shaped the response timeline.
""",
        "case_studies": [
            {
                "organization": "Social media platform",
                "scenario": "Coordinated bots submitted feedback praising extremist content, nudging the assistant to recommend harmful accounts.",
                "finding": "Feedback provenance was weak, and reward models lacked monitoring.",
                "response": "The platform implemented feedback reputation scores, throttled influence, and retrained models with curated data.",
            },
            {
                "organization": "Research consortium",
                "scenario": "Shared datasets contained doctored academic papers with hidden trigger phrases that leaked embargoed findings.",
                "finding": "Data contributions were accepted without steward review or hashing.",
                "response": "The consortium introduced provenance tagging, manual review for sensitive topics, and periodic red-team audits.",
            },
            {
                "organization": "Customer support outsourcer",
                "scenario": "A contractor fine-tuned a model with mislabeled examples so the assistant disclosed refund policies meant for supervisors only.",
                "finding": "Fine-tuning requests bypassed approval boards, and evaluation suites lacked policy-specific tests.",
                "response": "The company established fine-tuning governance, expanded tests, and required contractors to submit attestation logs.",
            },
        ],
        "case_outro": """
These narratives reinforce that poisoning thrives in gaps between teams. Integrating security reviews into training and deployment rhythms closes those gaps. They also highlight the emotional toll on responders, underscoring the importance of psychological safety, rest cycles, and leadership recognition after intense investigations.
""",
        "mnemonic": {
            "title": "CLEAN MODEL",
            "items": [
                {"letter": "C", "phrase": "Curate inputs", "detail": "Screen datasets and feedback before they influence training."},
                {"letter": "L", "phrase": "Log provenance", "detail": "Record sources, annotators, and approvals for every contribution."},
                {"letter": "E", "phrase": "Evaluate adversarially", "detail": "Run red-team prompts and trigger hunts before and after deployment."},
                {"letter": "A", "phrase": "Analyze gradients", "detail": "Monitor update statistics for abnormal patterns."},
                {"letter": "N", "phrase": "Notify stakeholders", "detail": "Escalate suspicious behavior quickly across security, ML, and legal teams."},
                {"letter": "M", "phrase": "Maintain checkpoints", "detail": "Store clean model versions to enable rapid rollback."},
                {"letter": "O", "phrase": "Observe runtime", "detail": "Instrument activations, rewards, and user feedback for drift."},
                {"letter": "D", "phrase": "Document governance", "detail": "Keep clear records of decisions, approvals, and mitigations."},
                {"letter": "E", "phrase": "Educate contributors", "detail": "Train employees and vendors on poisoning risks and reporting paths."},
                {"letter": "L", "phrase": "Learn continuously", "detail": "Review incidents, publish retrospectives, and iterate on defenses."},
            ],
        },
        "pitfall_intro": """
Common mistakes give poisoners room to operate. Avoid these traps to keep models trustworthy. Review the list during sprint planning, procurement reviews, and post-incident retrospectives so complacency never creeps back into daily routines.
""",
        "pitfalls": [
            {"title": "Blind acceptance of user feedback", "detail": "Reward models drift when influence is unchecked."},
            {"title": "Single-metric evaluation", "detail": "Accuracy alone cannot reveal backdoors or policy violations."},
            {"title": "Opaque fine-tuning", "detail": "Without approvals and documentation, organizations cannot trace harmful behaviors to specific updates."},
            {"title": "Delayed rollback", "detail": "Teams hesitate to revert to clean checkpoints, prolonging exposure."},
            {"title": "Under-resourced red teaming", "detail": "Without dedicated adversarial testing, backdoors remain undetected."},
            {"title": "Siloed communication", "detail": "Signals get lost when ML, security, and product teams do not share alerts in real time."},
        ],
        "takeaway_intro": """
Focus your next sprint on tangible actions that harden pipelines against poisoning. Align each action with named owners, success metrics, and budget requirements so momentum survives shifting product priorities.
""",
        "takeaways": [
            {"title": "Instrument gradient monitoring", "detail": "Add variance and similarity checks with automated alerts to ML security engineers."},
            {"title": "Expand evaluation suites", "detail": "Include red-team prompts, policy-specific tests, and trigger hunts in CI pipelines."},
            {"title": "Launch a fine-tuning approval board", "detail": "Require documented justification, risk assessment, and rollback plans for each update."},
            {"title": "Score feedback sources", "detail": "Assign reputation and throttle influence for RLHF contributors."},
            {"title": "Practice rollback drills", "detail": "Rehearse switching to safe modes and restoring clean checkpoints within service-level objectives."},
            {"title": "Share poisoning intel", "detail": "Coordinate with industry peers to learn about new triggers and attack vectors."},
        ],
        "takeaway_close": """
Poisoning resilience grows with repetition. Each iteration improves tooling, trust, and the speed at which your organization can respond to emerging threats. Share progress in executive reviews and customer trust reports so stakeholders understand that sustained investment in provenance, detection, and response yields measurable value.
""",
        "reflection_questions": [
            "Which datasets or feedback loops pose the highest risk of poisoning today?",
            "How would you detect and confirm a subtle backdoor before customers report it?",
            "What is your rollback timeline for critical assistants, and who authorizes it?",
            "How do you educate contributors and vendors about poisoning risks?",
            "Where are the single points of failure in your provenance logging, and how quickly could you reconstruct a poisoned batch's lineage?",
            "What partnerships or information-sharing agreements could accelerate your awareness of emerging poisoning techniques?",
        ],
        "mindset": [
            """
Treat poisoning defense as a craft. Curiosity, rigor, and humility help teams question assumptions and uncover hidden patterns.
""",
            """
Celebrate detection wins. Share stories when monitoring caught anomalies so engineers appreciate the value of instrumentation.
""",
            """
Foster psychological safety. Encourage teams to raise suspicions without fear of blame; early reporting beats silent uncertainty.
""",
            """
Invest in shared learning. Participate in community challenges, publish sanitized findings, and invite external experts to review your defenses.
""",
            """
Practice recovery rituals. After intense investigations, schedule debriefs focused on gratitude, rest, and lessons learned so teams remain energized for the next sprint.
""",
            """
Connect the mission to purpose. Remind stakeholders that protecting model integrity safeguards customers, communities, and democratic processes from manipulation.
""",
        ],
    },
    {
        "lesson_id": "a74f9a9a-f13e-44cf-8e34-3e3efe654eb9",
        "slug": "owasp_llm05_improper_output_handling",
        "title": "OWASP LLM05: Improper Output Handling",
        "subtitle": "Containing LLM responses before they reach critical systems",
        "difficulty": 2,
        "estimated_time": 120,
        "order_index": 8,
        "prerequisites": [],
        "concepts": [
            "response sanitization",
            "content moderation",
            "output encoding",
            "policy enforcement",
            "downstream orchestration",
            "guardrail UX",
        ],
        "learning_objectives": [
            "Describe how unsafe outputs propagate through automation stacks and user interfaces.",
            "Design post-processing pipelines that enforce policy, encode data safely, and communicate issues clearly to users.",
            "Implement code patterns that prevent HTML, script, or command injection from LLM-generated text.",
            "Align moderation thresholds with legal, compliance, and brand requirements while minimizing false positives.",
            "Educate stakeholders on safe consumption practices for LLM responses across APIs, chat, and integrations.",
        ],
        "post_assessment": [
            {
                "question": "Which example highlights improper output handling?",
                "options": [
                    "An assistant summarizes a meeting transcript without formatting.",
                    "A workflow executes LLM-generated shell commands without validation, resulting in file deletion.",
                    "A chatbot politely declines to answer a policy-violating request.",
                    "An API returns JSON with explicit schema documentation.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Why should LLM outputs intended for HTML rendering be sanitized?",
                "options": [
                    "Sanitization slows performance unnecessarily.",
                    "Outputs may contain scripts or malicious markup that lead to XSS or content injection.",
                    "Users dislike formatted responses.",
                    "Sanitization is only needed for binary files.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "What is the best response when an LLM attempts a disallowed action in an automated workflow?",
                "options": [
                    "Execute the action silently to avoid user frustration.",
                    "Block the action, log the attempt, and surface a helpful message to the requester.",
                    "Disable logging to protect privacy.",
                    "Ignore policy violations if the requester is an internal employee.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "How can developers ensure downstream systems understand moderation results?",
                "options": [
                    "Return opaque error codes.",
                    "Standardize response schemas that include decision rationale, severity, and remediation guidance.",
                    "Strip metadata to keep responses short.",
                    "Assume every integration knows the moderation policy.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "unsafe or unvalidated LLM responses reach users or systems, causing security, compliance, or trust failures",
            "business_context": "organizations embed assistants in customer portals, automation workflows, and analytics dashboards",
            "attacker_motivation": "inject malicious markup, commands, or social engineering content that leverages trust in AI outputs",
            "human_factor": "developers prioritize speed over guardrails, and users copy-paste outputs into sensitive environments",
            "control_challenge": "balancing strong moderation with user experience while supporting multiple output formats",
            "innovation_balance": "building expressive assistants that still respect encoding, policy, and governance boundaries",
            "closing_emphasis": "output handling is the final defense between model creativity and business risk",
        },
        "short_name": "Improper Output Handling",
        "llm_code": "OWASP LLM05",
        "attack_vectors": [
            {
                "name": "HTML/script injection",
                "detail": "LLM responses include <script> tags, onload attributes, or SVG payloads that execute in browsers",
                "detail_secondary": "attackers coax assistants to produce markup under the guise of helpful widgets or analytics",
                "impact": "users run malicious code, leading to session hijacking or data exfiltration",
                "impact_secondary": "brand reputation suffers when interfaces display defaced content",
                "detection": "DOM sanitization, CSP violation alerts, and synthetic monitoring",
                "telemetry": "log sanitized fragments, policy rule hits, and client-side error reports",
                "mitigation": "use context-aware HTML sanitizers, strict CSP headers, and render outputs within safe components",
                "lesson_alignment": "OWASP direction on encoding and output filtering",
                "mitigation_reinforcement": "pen-test chat interfaces with XSS payloads to verify controls hold",
            },
            {
                "name": "Command execution",
                "detail": "automation agents execute shell or API commands generated by the LLM without validation",
                "detail_secondary": "the assistant may suggest destructive actions when prompted with troubleshooting questions",
                "impact": "files deleted, infrastructure misconfigured, or sensitive data exposed",
                "impact_secondary": "incident response teams must restore environments and explain automation failures",
                "detection": "command allowlists, anomaly detection on automation pipelines, and execution sandboxes",
                "telemetry": "record command source, sanitized output, and approval state for auditing",
                "mitigation": "require human approval for high-impact commands, enforce idempotent operations, and provide safe alternatives",
                "lesson_alignment": "OWASP focus on minimizing excessive agency",
                "mitigation_reinforcement": "simulate dangerous commands and confirm tooling halts execution with clear messaging",
            },
            {
                "name": "Regulatory non-compliance",
                "detail": "responses include hate speech, medical advice, or financial recommendations without required disclaimers",
                "detail_secondary": "policies differ by region, making one-size-fits-all moderation ineffective",
                "impact": "legal exposure, fines, or loss of platform access",
                "impact_secondary": "customer trust erodes when outputs conflict with brand standards",
                "detection": "multi-layer moderation models tuned to jurisdictional rules",
                "telemetry": "store decision rationale, reviewer overrides, and appeal outcomes",
                "mitigation": "combine automated classifiers with human review for borderline cases and log disclosures",
                "lesson_alignment": "OWASP call for policy enforcement and auditability",
                "mitigation_reinforcement": "review moderation metrics with legal and compliance teams monthly",
            },
            {
                "name": "Structured data injection",
                "detail": "LLMs output JSON or SQL containing attacker-controlled fields that downstream services trust",
                "detail_secondary": "APIs may deserialize responses directly into workflows without schema validation",
                "impact": "data corruption, privilege escalation, or injection into downstream databases",
                "impact_secondary": "integrated partners inherit tainted data, expanding blast radius",
                "detection": "schema validation, content hashing, and anomaly detection on outbound payloads",
                "telemetry": "log validation errors, offending fields, and user context",
                "mitigation": "enforce strict schemas, escape special characters, and require explicit approvals for schema drift",
                "lesson_alignment": "OWASP recommendation to treat model outputs as untrusted input",
                "mitigation_reinforcement": "fuzz APIs with intentionally malformed LLM outputs to ensure consumers reject them",
            },
        ],
        "impact_overview": """
Improper output handling quickly undermines trust. Customers encounter broken pages or harmful advice. Automated workflows run unsafe actions. Legal teams raise alarms when disclaimers fail to appear. Because outputs often flow into chat, email, tickets, or APIs, a single unsafe response can replicate across channels within seconds. Leaders need confidence that guardrails catch issues before customers or regulators do.

The damage rarely stays confined to a single interaction. Customer success teams face escalations, social media managers handle public backlash, and engineering leaders pause feature rollouts to audit moderation systems. Regulators and auditors request detailed explanations of how policies failed, while procurement reviews partner contracts to confirm responsibilities. Even if no breach occurs, the perception of carelessness can slow adoption of new AI-powered services, giving competitors room to position themselves as safer alternatives.

Sustained diligence requires acknowledging that output safety is a shared mission. Marketing shapes tone, support teams craft empathetic messaging, and developers instrument pipelines so issues surface instantly. Organizations that practice transparency—sharing guardrail metrics with executives and customers—transform safety work into a brand differentiator rather than a reluctant cost center. Post-incident analytics often reveal hidden dependencies between channels, prompting fresh investment in documentation, training, and contingency plans.
""",
        "impact_zones": [
            {
                "area": "User experience",
                "detail": "Malicious or confusing outputs damage brand reputation and frustrate customers who rely on assistants for guidance.",
            },
            {
                "area": "Automation integrity",
                "detail": "Downstream systems executing unvalidated commands or API calls can disrupt operations or leak data.",
            },
            {
                "area": "Legal compliance",
                "detail": "Improper disclosures or missing disclaimers violate consumer protection, medical, or financial regulations.",
            },
            {
                "area": "Partner ecosystems",
                "detail": "Integrations amplify risk when partners ingest unsafe outputs without additional checks.",
            },
            {
                "area": "Regulatory posture",
                "detail": "Missing disclaimers or policy violations trigger investigations, fines, or mandated reporting to oversight bodies.",
            },
            {
                "area": "Employee enablement",
                "detail": "Support agents and sales teams lose confidence in AI copilots when outputs require constant correction, reducing productivity gains.",
            },
        ],
        "detection_intro": """
Output monitoring requires both linguistic understanding and contextual awareness. Build pipelines that evaluate toxicity, regulatory compliance, encoding safety, and business-specific rules. Feed alerts to security, compliance, and product teams so they can coordinate remediation and user messaging.

Mature programs combine automated scoring with human sampling, surfacing transcripts for reviewers to validate tone, empathy, and legal accuracy. Weekly guardrail councils analyze metrics, correlate spikes with product launches or marketing campaigns, and adjust thresholds before issues escalate. This continuous dialogue keeps policies aligned with evolving business priorities and regional regulations.
""",
        "detection_focus": [
            {
                "name": "Moderation classifier confidence",
                "detail": "Track how often automated moderation flags content and how frequently humans override decisions.",
                "correlation": "Align spikes with new features, marketing campaigns, or seasonal trends.",
                "forensics": "Store annotated samples to refine policies and train reviewers.",
            },
            {
                "name": "Output encoding checks",
                "detail": "Scan responses for unescaped HTML, script tags, or shell metacharacters.",
                "correlation": "Tie findings to specific prompt templates or tool outputs.",
                "forensics": "Preserve raw and sanitized versions for debugging and legal review.",
            },
            {
                "name": "Workflow approval telemetry",
                "detail": "Monitor how often human approvals block LLM-generated actions.",
                "correlation": "Compare with automation success metrics to balance safety and efficiency.",
                "forensics": "Capture context, decision rationale, and follow-up actions for audit logs.",
            },
            {
                "name": "Schema validation errors",
                "detail": "Alert when downstream systems reject LLM-generated structured payloads.",
                "correlation": "Identify which prompts or tools trigger the errors and whether user roles correlate.",
                "forensics": "Record offending fields and sanitized replacements.",
            },
            {
                "name": "Sentiment and escalation feedback",
                "detail": "Analyze support tickets, user surveys, and NPS comments for frustration linked to blocked or malformed outputs.",
                "correlation": "Overlay with moderation events to pinpoint policy adjustments or UX copy updates.",
                "forensics": "Maintain tagged transcripts so teams can replay conversations during retrospectives.",
            },
        ],
        "guardrail_intro": """
Treat model outputs like untrusted input. Apply transformation, validation, and policy enforcement before exposing responses to users or systems. Build empathetic messaging that explains guardrail decisions without frustrating users.

Guardrails also extend to business processes: marketing needs review workflows, legal teams need audit trails, and partners require shared standards. Documenting these expectations keeps ecosystems aligned and prevents shortcuts when deadlines loom.
""",
        "guardrail_layers": [
            {
                "name": "Output sanitization gateway",
                "detail": "Central service that applies encoding, moderation, and structural validation before responses leave the platform.",
                "conditions": "all channels, including chat, email, APIs, and documents",
                "practice": "version sanitization rules, monitor performance, and review false positives with UX teams",
                "alignment": "secure coding standards and policy requirements",
            },
            {
                "name": "Guardrail UX patterns",
                "detail": "Design friendly error messages, suggestion prompts, and escalation paths when content is blocked.",
                "conditions": "whenever policies prevent the assistant from fulfilling a request",
                "practice": "A/B test messaging with customer success to maintain satisfaction",
                "alignment": "brand guidelines and accessibility standards",
            },
            {
                "name": "Command approval workflow",
                "detail": "High-impact actions require human review, dual authorization, or simulated dry-runs before execution.",
                "conditions": "automation tasks that modify infrastructure, finances, or legal records",
                "practice": "log approvals, enforce expiry, and support rapid rollbacks",
                "alignment": "internal controls and segregation of duties",
            },
            {
                "name": "Partner integration contracts",
                "detail": "Define responsibilities for sanitization, logging, and incident reporting when outputs flow to external systems.",
                "conditions": "before onboarding new partners or marketplace integrations",
                "practice": "review obligations annually and monitor runtime behavior",
                "alignment": "third-party risk management policies",
            },
            {
                "name": "Telemetry observability hub",
                "detail": "Aggregates moderation events, approval outcomes, and user sentiment into a shared dashboard.",
                "conditions": "operational reviews and executive reporting",
                "practice": "tag incidents with root causes, track remediation, and publish trends to stakeholders",
                "alignment": "governance, risk, and compliance transparency",
            },
        ],
        "operational_story": """
Output safety requires collaboration between engineering, security, product, legal, and customer-facing teams. Together they refine policies, tune messaging, and ensure guardrails empower rather than frustrate users. Regular retrospectives turn blocked outputs into training material for support staff and design improvements.

High-performing organizations run “content stand-ups” where designers, policy experts, and data scientists review recent guardrail events, celebrate empathetic messaging wins, and flag edge cases for further automation. When outages or false positives occur, a dedicated liaison coordinates updates to knowledge bases, support macros, and status pages. This rhythm keeps teams aligned on the shared goal of protecting users while sustaining trust in AI assistance, and it normalizes the idea that safety improvements deserve the same fanfare as new feature launches.
""",
        "video": {
            "title": "Designing Safe LLM Responses",
            "url": "https://www.youtube.com/watch?v=4XK0YwF6l-A",
            "description": "Product and security leaders discuss how they built multi-layered output moderation, user-friendly guardrails, and automation approvals for enterprise assistants.",
            "focus_points": [
                "How the team communicates policy decisions to users.",
                "Telemetry captured when outputs are sanitized or blocked.",
                "Trade-offs between automation speed and human approval.",
                "Ideas for partnering with compliance and UX to tune guardrails.",
            ],
        },
        "diagram": {
            "intro": "A layered output handling architecture keeps responses safe and transparent:",
            "ascii": """
 User Prompt -> LLM -> Output Gateway -> Policy Engine -> Renderer / Workflow
                                |             |             |
                             Telemetry     Moderation    User Messaging
""",
            "explanation": "The gateway enforces encoding and schema validation. The policy engine applies moderation rules and triggers approvals. Renderers or workflows receive only sanitized content along with metadata describing decisions.",
            "callouts": [
                "Telemetry feeds dashboards and incident response.",
                "Policy engines support region-specific rules and legal requirements.",
                "User messaging templates translate technical decisions into empathetic explanations.",
                "Renderer components escape or format content safely for each channel.",
            ],
        },
        "lab_setup": {
            "overview": """
Configure an output gateway that handles HTML, plain text, and structured data. Participants will test sanitization rules, moderation policies, and approval workflows to ensure consistent behavior across channels.
""",
            "objective": "Deploy a unified output handling pipeline that blocks unsafe content, provides clear messaging, and logs decisions for auditing.",
            "steps": [
                "Implement an output service with modules for HTML sanitization, schema validation, and moderation.",
                "Configure policy rules for regulated content (e.g., medical, financial) with escalation paths to human reviewers.",
                "Integrate the gateway with a chatbot UI and an automation workflow that executes commands in a sandbox.",
                "Test benign, borderline, and malicious outputs to verify sanitization, messaging, and logging.",
                "Adjust UX copy to ensure blocked responses remain helpful and aligned with brand tone.",
                "Trigger command approvals and verify that logs capture requester, approver, and command context.",
                "Simulate partner integrations and confirm contracts define sanitization responsibilities.",
                "Evaluate accessibility by testing screen readers, localization, and mobile views for guardrail messaging.",
                "Review telemetry dashboards to ensure stakeholders can monitor policy hits and false positives.",
                "Conduct a mock executive briefing summarizing findings, metrics, and investment needs for future guardrail improvements.",
            ],
            "validation": "Success is measured by blocked unsafe content, positive user feedback on guardrail messaging, and comprehensive logs for audit. Teams should also capture before-and-after sentiment scores, document accessibility fixes, and produce a prioritized roadmap endorsed by engineering, legal, and customer experience leaders. Share the outcomes with executive sponsors and partner liaisons to reinforce accountability across the ecosystem.",
        },
        "code_exercise": {
            "overview": """
Build a middleware component that sanitizes HTML and enforces content policies before rendering chatbot responses.
""",
            "language": "python",
            "snippet": """
from bleach import clean

ALLOWED_TAGS = ["b", "i", "strong", "em", "ul", "li", "p", "code"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}

def sanitize_response(html: str) -> str:
    return clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

def apply_policy(text: str) -> dict:
    blocked = any(keyword in text.lower() for keyword in ["wire money", "diagnose", "prescribe"])
    return {
        "sanitized": sanitize_response(text),
        "blocked": blocked,
        "message": "Human review required." if blocked else "Deliver to user.",
    }
""",
            "explanation": "Sanitization libraries remove dangerous markup while preserving formatting. Policy checks flag risky content so workflows can request approvals or reroute to humans. Production systems would integrate richer moderation models, locale-aware policies, telemetry publishing, canary deployments, and contract tests that prevent regressions when sanitization rules evolve.",
            "callouts": [
                "Maintain separate configurations per channel to balance richness and safety.",
                "Log both raw and sanitized content with access controls.",
                "Provide override mechanisms with audit trails for approved exceptions.",
                "Test sanitization against known XSS payloads.",
                "Pair policy hits with user-facing explanations to maintain trust.",
            ],
        },
        "case_intro": """
Real incidents show how minor oversights in output handling escalate quickly. Analyze these scenarios to shape your own defenses and note how cross-functional coordination—or the lack of it—influenced recovery timelines.
""",
        "case_studies": [
            {
                "organization": "Insurance chatbot",
                "scenario": "An LLM-generated email included HTML that triggered an XSS attack in the customer portal.",
                "finding": "Output sanitization relied on client-side libraries, and logs lacked detail for forensics.",
                "response": "The company moved sanitization to the server gateway, enforced CSP, and updated incident communications templates.",
            },
            {
                "organization": "DevOps automation platform",
                "scenario": "An assistant suggested a shell command that accidentally deleted deployment artifacts when executed automatically.",
                "finding": "Command approvals were optional and not enforced in CI pipelines.",
                "response": "The platform implemented mandatory approvals, simulated dry-runs, and added guardrail messaging for risky actions.",
            },
            {
                "organization": "Healthcare triage assistant",
                "scenario": "Outputs omitted required disclaimers and included confident treatment recommendations.",
                "finding": "Moderation thresholds were tuned for general content, not healthcare-specific compliance.",
                "response": "The provider partnered with compliance to update policies, added mandatory disclaimers, and expanded human review.",
            },
        ],
        "case_outro": """
Outputs are where customers judge quality. Investing in guardrails protects both people and brand equity. Use these stories to fuel tabletop exercises, help desks simulations, and executive briefings that reinforce why continuous improvement matters.
""",
        "mnemonic": {
            "title": "SAFE OUTPUT",
            "items": [
                {"letter": "S", "phrase": "Sanitize markup", "detail": "Strip or encode HTML, scripts, and special characters."},
                {"letter": "A", "phrase": "Approve risky actions", "detail": "Require human review for commands and sensitive workflows."},
                {"letter": "F", "phrase": "Format consistently", "detail": "Return structured schemas with clear metadata."},
                {"letter": "E", "phrase": "Explain decisions", "detail": "Provide users with helpful guardrail messages and next steps."},
                {"letter": "O", "phrase": "Observe telemetry", "detail": "Monitor moderation hits, false positives, and user feedback."},
                {"letter": "U", "phrase": "Update policies", "detail": "Review moderation thresholds with legal and compliance regularly."},
                {"letter": "T", "phrase": "Test integrations", "detail": "Fuzz downstream APIs and UIs with adversarial outputs."},
                {"letter": "P", "phrase": "Protect partners", "detail": "Share expectations and monitoring data with integrations."},
                {"letter": "U", "phrase": "Use safe defaults", "detail": "Fail closed by blocking outputs you cannot sanitize confidently."},
                {"letter": "T", "phrase": "Train teams", "detail": "Educate developers, reviewers, and support staff on output handling procedures."},
            ],
        },
        "pitfall_intro": """
Avoid the traps that let unsafe outputs slip into production. Revisit this checklist during sprint planning, procurement reviews, and customer feedback sessions so complacency never settles in.
""",
        "pitfalls": [
            {"title": "Client-side sanitization only", "detail": "Attackers bypass browser defenses when servers trust unsanitized outputs. Move critical checks server-side and verify with automated tests."},
            {"title": "Opaque moderation", "detail": "Users become frustrated when blocked outputs lack explanations. Pair every denial with empathetic copy and next steps."},
            {"title": "Overbroad approvals", "detail": "Rubber-stamp workflows erode trust and invite abuse. Define escalation tiers and measure approval quality, not just speed."},
            {"title": "Schema drift", "detail": "Consumers break when outputs add fields without notice. Version schemas, communicate changes, and enforce contract tests."},
            {"title": "Lack of observability", "detail": "Without telemetry, teams cannot tune policies or detect false positives. Instrument dashboards, alerts, and runbooks."},
            {"title": "Neglected documentation", "detail": "Outdated playbooks leave support and engineering unsure how to respond. Schedule regular reviews tied to release calendars."},
        ],
        "takeaway_intro": """
Convert awareness into action by prioritizing output guardrails this quarter. Assign owners, budgets, and success metrics so initiatives survive competing product pressures.
""",
        "takeaways": [
            {"title": "Deploy server-side sanitization", "detail": "Centralize encoding and moderation before responses reach clients."},
            {"title": "Define approval tiers", "detail": "Map automation actions to risk levels with tailored review workflows."},
            {"title": "Standardize response schemas", "detail": "Include status, rationale, and fallback suggestions in every API response."},
            {"title": "Add telemetry dashboards", "detail": "Visualize moderation hits, false positives, and user sentiment."},
            {"title": "Schedule UX reviews", "detail": "Test guardrail messaging with users and support teams for clarity."},
            {"title": "Document partner expectations", "detail": "Share sanitization requirements and incident procedures with integrations."},
        ],
        "takeaway_close": """
Output safety is a shared responsibility. Transparent guardrails and supportive messaging keep automation trustworthy. Share progress through executive dashboards and customer trust reports so stakeholders understand how investments reduce risk and enhance experience.
""",
        "reflection_questions": [
            "Where do LLM responses flow after leaving the model, and which systems assume they are safe?",
            "How will you explain blocked content to users while maintaining empathy and compliance?",
            "Which automation tasks require stronger approval workflows or sandboxing?",
            "What telemetry proves to executives that output guardrails protect the business?",
            "How do localization, accessibility, or channel-specific constraints change your guardrail strategy?",
            "Which partners or vendors need additional education about your output handling standards?",
            "What experiments could you run this quarter to measure the impact of improved guardrail messaging on customer satisfaction?",
        ],
        "mindset": [
            """
Think like a user. Safe outputs respect people’s time, emotions, and expectations. Guardrails should help users succeed, not scold them.
""",
            """
Celebrate clarity. Share success stories where empathetic messaging turned a blocked response into a positive experience.
""",
            """
Approach moderation as continuous learning. Invite feedback from legal, compliance, and customer support to refine policies.
""",
            """
Stay curious about emerging channels. As assistants appear in voice, AR, or code, revisit output guardrails to match new formats.
""",
            """
Elevate empathy. Role-play scenarios where a blocked response could embarrass or stress a user, then refine messaging accordingly.
""",
            """
Champion visibility. Promote dashboards and storytelling that make guardrail successes as celebrated as product launches.
""",
        ],
    },
    {
        "lesson_id": "19e2eac3-c35a-4f1c-a9a3-391ea2278d94",
        "slug": "owasp_llm06_excessive_agency",
        "title": "OWASP LLM06: Excessive Agency",
        "subtitle": "Right-sizing autonomy for safety and accountability",
        "difficulty": 2,
        "estimated_time": 115,
        "order_index": 9,
        "prerequisites": [],
        "concepts": [
            "capability scoping",
            "human-in-the-loop",
            "authorization workflows",
            "tool governance",
            "runbook automation",
            "risk-based approvals",
        ],
        "learning_objectives": [
            "Explain how excessive agency emerges when assistants combine tools, memory, and decision authority.",
            "Design guardrails that align autonomy with business risk, including approvals and escalation paths.",
            "Implement capability-based access control and auditing for tool invocations.",
            "Assess organizational readiness for autonomous agents by analyzing culture, metrics, and communication flows.",
            "Coach teams to design workflows that enhance, not replace, human judgment.",
        ],
        "post_assessment": [
            {
                "question": "Which scenario best illustrates excessive agency?",
                "options": [
                    "A documentation assistant drafts a knowledge base article for review.",
                    "An agent opens support tickets, resets user passwords, and issues refunds without approval.",
                    "A chatbot escalates a complex case to a human agent.",
                    "An analytics bot suggests KPIs for executive review.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "What is a key control to limit agent autonomy?",
                "options": [
                    "Grant global API keys to simplify development.",
                    "Use capability-scoped tokens, approvals, and explicit runbooks for sensitive actions.",
                    "Disable logging to reduce storage costs.",
                    "Rely on verbal agreements instead of documented policies.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "How can organizations monitor agent autonomy in production?",
                "options": [
                    "Avoid metrics to keep teams creative.",
                    "Track tool usage, approval rates, and manual overrides in dashboards shared with stakeholders.",
                    "Trust that agents behave because they passed testing.",
                    "Disable telemetry to improve latency.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Why is cultural readiness important when deploying autonomous agents?",
                "options": [
                    "Culture has no impact on automation outcomes.",
                    "Teams must understand escalation paths, trust guardrails, and feel empowered to intervene.",
                    "Only engineers need to know about agents.",
                    "Culture determines GPU utilization.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "agents act beyond intended scope, executing actions or decisions without sufficient oversight",
            "business_context": "organizations deploy assistants that schedule meetings, modify infrastructure, and communicate with customers",
            "attacker_motivation": "abuse elevated capabilities to pivot into critical systems or cause business disruption",
            "human_factor": "teams underestimate the need for approvals and treat automation as infallible",
            "control_challenge": "balancing efficiency with accountability across diverse toolchains",
            "innovation_balance": "designing experiences where humans remain the pilots and agents act as copilots",
            "closing_emphasis": "autonomy must be earned, measured, and continuously justified",
        },
        "short_name": "Excessive Agency",
        "llm_code": "OWASP LLM06",
        "attack_vectors": [
            {
                "name": "Unbounded tool catalogs",
                "detail": "agents receive credentials granting full access to ticketing, CRM, or cloud platforms",
                "detail_secondary": "developers use broad API keys during prototyping and forget to tighten scope",
                "impact": "agents perform destructive actions or leak data when prompted or manipulated",
                "impact_secondary": "forensics struggle to determine whether a human or agent initiated the action",
                "detection": "tool usage anomaly detection and least-privilege audits",
                "telemetry": "log tool name, parameters, approvals, and outcomes per invocation",
                "mitigation": "issue scoped tokens, rotate secrets, and require explicit capability definitions",
                "lesson_alignment": "OWASP recommendation to minimize agency and enforce guardrails",
                "mitigation_reinforcement": "run tabletop exercises revoking agent privileges to ensure fail-safes function",
            },
            {
                "name": "Implicit approvals",
                "detail": "automation assumes consent after a timeout or lack of response",
                "detail_secondary": "busy teams miss notifications, allowing agents to proceed unchecked",
                "impact": "actions occur without accountability, such as financial transactions or policy updates",
                "impact_secondary": "customers receive conflicting messages when humans later reverse the changes",
                "detection": "track auto-approved events and compare against manual approvals",
                "telemetry": "store timestamps, approver identities, and escalation status",
                "mitigation": "require explicit confirmation, escalate to backups, and disable actions when approvals lapse",
                "lesson_alignment": "OWASP focus on human-in-the-loop controls",
                "mitigation_reinforcement": "simulate notification failures to ensure escalation paths trigger",
            },
            {
                "name": "Memory-driven scope creep",
                "detail": "agents store long-term goals that expand beyond original use cases",
                "detail_secondary": "memory entries accumulate authority, enabling agents to self-approve actions",
                "impact": "assistants start new projects or change configurations without human intent",
                "impact_secondary": "stakeholders feel blindsided, eroding trust in automation",
                "detection": "review memory logs for directives granting new authority",
                "telemetry": "track who created and consumed each memory entry",
                "mitigation": "sandbox memory, require review before promoting goals, and expire entries",
                "lesson_alignment": "OWASP emphasis on context isolation",
                "mitigation_reinforcement": "periodically wipe memory to ensure workflows remain stable",
            },
            {
                "name": "Chained automation loops",
                "detail": "agents trigger other agents or workflows, amplifying decisions without oversight",
                "detail_secondary": "lack of circuit breakers allows loops to escalate costs or spam communications",
                "impact": "denial-of-wallet scenarios, reputational damage, or compliance violations",
                "impact_secondary": "incident response must unwind multiple systems to restore normalcy",
                "detection": "monitor agent-to-agent calls and create rate limits on cascading actions",
                "telemetry": "log orchestration graphs showing how tasks propagate",
                "mitigation": "establish quotas, circuit breakers, and manual checkpoints for multi-agent operations",
                "lesson_alignment": "OWASP guidance on preventing runaway automation",
                "mitigation_reinforcement": "test failure scenarios where agents exceed quotas to ensure shutdown works",
            },
        ],
        "impact_overview": """
Excessive agency blurs accountability. Stakeholders cannot explain who approved actions, regulators question governance, and customers lose trust when automation behaves unpredictably. Operational teams spend more time auditing agents than benefiting from them, negating promised efficiencies.

When agents overstep, the financial blast radius mounts quickly: refunds stack up, infrastructure changes break environments, and customer churn rises as trust erodes. Executives must brief boards and regulators on how autonomy was granted, which safeguards failed, and why human approvals were bypassed. Meanwhile, frontline employees are left reconciling conflicting records, reversing mistakes, and apologizing to frustrated customers.

Unchecked autonomy also strains partner ecosystems. Vendors receive contradictory instructions, outsourced contact centers pause operations until they can confirm the human decision maker, and auditors freeze procurement workflows until evidence of approval chains is produced. By the time clarity arrives, the business has accumulated late fees, missed service-level objectives, and reputational bruises that outlive the technical incident.

Sustainable autonomy programs therefore require the same rigor as safety-critical engineering. Teams model worst-case scenarios, instrument every decision path, and rehearse shutdown drills. They treat autonomy as a privilege that must be earned through telemetry, audits, and clear communication rather than an inevitability granted by new tooling.

Global organizations face added complexity as they navigate regional regulations on automated decision-making, worker councils, and consumer protections. Autonomy programs must incorporate jurisdiction-specific guardrails, multilingual training, and culturally aware escalation procedures so interventions remain swift and respectful regardless of geography.

Leaders who invest in change management also report softer benefits: transparency briefings and ride-alongs with operators rebuild trust, while rotating product managers through governance councils helps them design safer prompts. These cultural rituals create a feedback loop where humans continually calibrate what “responsible autonomy” feels like in practice instead of assuming a one-time rollout will hold forever.
""",
        "impact_zones": [
            {
                "area": "Financial controls",
                "detail": "Unauthorized refunds, purchases, or budget changes trigger audits and potential losses.",
            },
            {
                "area": "Security posture",
                "detail": "Overprivileged agents become lateral movement vectors during breaches.",
            },
            {
                "area": "Customer experience",
                "detail": "Automated responses feel erratic when agents overstep boundaries, leading to churn.",
            },
            {
                "area": "Employee morale",
                "detail": "Teams feel sidelined when agents act autonomously without transparency, reducing adoption.",
            },
            {
                "area": "Regulatory compliance",
                "detail": "Autonomous decisions without documented approvals undermine SOX, PCI, and privacy obligations, prompting external reviews.",
            },
            {
                "area": "Incident communications",
                "detail": "Public statements become harder when organizations cannot articulate who authorized an agent’s actions or how they will prevent recurrence.",
            },
        ],
        "detection_intro": """
Monitor autonomy with quantitative and qualitative signals. Dashboards should display tool usage, approval latency, manual overrides, and escalation frequency. Pair metrics with interviews and feedback channels to capture human sentiment about automation.

Organizations that succeed treat these dashboards as living documents reviewed in weekly governance councils. They investigate anomalies, trace back to specific prompts or workflows, and interview affected teams. Combining data with narrative context uncovers patterns—such as certain shifts granting approvals too quickly or specific agents attempting privileged actions at odd hours.
""",
        "detection_focus": [
            {
                "name": "Tool invocation volume",
                "detail": "Track calls per agent, per capability, and per user session.",
                "correlation": "Compare with business calendars and workload baselines to spot anomalies.",
                "forensics": "Store arguments, results, and approver IDs for each invocation.",
            },
            {
                "name": "Override frequency",
                "detail": "Measure how often humans intervene or reverse actions.",
                "correlation": "Identify workflows that regularly trigger overrides, signaling poor alignment.",
                "forensics": "Capture rationale for overrides to improve training and guardrails.",
            },
            {
                "name": "Approval latency",
                "detail": "Watch for approvals granted unusually fast or slow, indicating process issues.",
                "correlation": "Link to team schedules and workload to adjust staffing or automation levels.",
                "forensics": "Log timestamps and notification channels to audit escalation paths.",
            },
            {
                "name": "Escalation coverage",
                "detail": "Ensure every agent workflow has a defined escalation owner and fallback plan.",
                "correlation": "Report gaps where escalations failed or went unanswered.",
                "forensics": "Maintain communication transcripts to refine runbooks.",
            },
            {
                "name": "Agent self-modification attempts",
                "detail": "Detect when agents request new capabilities, modify memory, or chain to other tools without approval.",
                "correlation": "Align with memory logs and prompt updates to ensure intent matches governance decisions.",
                "forensics": "Archive proposed changes, reviewer comments, and resulting actions for audit trails.",
            },
        ],
        "guardrail_intro": """
Calibrate autonomy by combining technical controls with organizational agreements. Agents earn capabilities through testing, metrics, and ongoing review rather than receiving blanket authority.

Guardrails extend beyond software: executive sponsors set risk appetite, legal teams codify accountability, and change-management groups ensure training keeps pace with new capabilities. Documenting these agreements keeps autonomy aligned with culture and compliance.
""",
        "guardrail_layers": [
            {
                "name": "Capability registry",
                "detail": "Maintain a catalog of approved actions, required inputs, and associated risks for each agent.",
                "conditions": "before granting access to tools or APIs",
                "practice": "review quarterly with product, security, and compliance",
                "alignment": "internal control frameworks",
            },
            {
                "name": "Approval and escalation matrix",
                "detail": "Define who approves which actions, timeouts, and fallback contacts.",
                "conditions": "during workflow design and before launch",
                "practice": "test notifications and escalate to backups when primary approvers are unavailable",
                "alignment": "business continuity and segregation of duties",
            },
            {
                "name": "Autonomy performance reviews",
                "detail": "Regular meetings evaluate metrics, incidents, and user feedback to adjust capabilities.",
                "conditions": "monthly or after notable events",
                "practice": "document decisions and update capability registry accordingly",
                "alignment": "governance and executive oversight",
            },
            {
                "name": "Emergency stop mechanisms",
                "detail": "Provide accessible controls to pause agents, revoke tokens, or switch to manual mode.",
                "conditions": "available to operators, support, and security teams at all times",
                "practice": "drill shutdown procedures and verify they propagate across regions",
                "alignment": "incident response and reliability requirements",
            },
            {
                "name": "Cultural readiness playbooks",
                "detail": "Outline communication plans, training modules, and change-management checkpoints that prepare teams for increasing autonomy.",
                "conditions": "prior to scaling pilot programs or introducing new agent capabilities",
                "practice": "survey teams, address concerns, and celebrate milestones to reinforce accountability",
                "alignment": "organizational development and risk culture objectives",
            },
        ],
        "operational_story": """
Autonomy programs succeed when teams share ownership. Product managers define desired outcomes, security architects set guardrails, operations teams monitor metrics, and executives communicate boundaries. Transparency keeps everyone aligned.

Weekly autonomy reviews resemble air-traffic control meetings: participants walk through recent actions, approvals, and near misses. Customer support reports sentiment trends, finance highlights anomalies in spending, and compliance notes regulatory considerations. Together they adjust capability tiers, update training content, and schedule tabletop exercises.

The most mature programs publish autonomy scorecards that highlight improvement areas and celebrate cautionary saves where humans intervened before harm occurred. Sharing these stories builds a culture that values mindful automation over blind delegation. Leaders reinforce the message by tying performance reviews and bonuses to responsible automation practices, not just raw efficiency metrics.
""",
        "video": {
            "title": "Balancing AI Autonomy with Human Oversight",
            "url": "https://www.youtube.com/watch?v=3gTtyz5rQCU",
            "description": "Leaders from fintech and SaaS companies discuss lessons learned deploying autonomous agents, including approval workflows and cultural change management. They walk through dashboards, stakeholder communications, and post-incident retrospectives that kept automation aligned with business values.",
            "focus_points": [
                "Note how each organization defined capability tiers and approvals.",
                "Observe the metrics they track to prove guardrails work.",
                "Listen for cultural initiatives that build trust between humans and agents.",
                "Identify quick wins you can apply to your own program.",
                "Consider how speakers measure success beyond efficiency, such as employee confidence and regulator satisfaction.",
            ],
        },
        "diagram": {
            "intro": "Capability governance connects design, execution, and oversight:",
            "ascii": """
  Capability Registry --> Approval Matrix --> Agent Runtime --> Monitoring Dashboards
          |                    |                 |                    |
     Stakeholder Sign-off   Escalation Paths  Scoped Tokens    Metrics & Overrides
""",
            "explanation": "Capabilities originate in the registry, are approved via documented matrices, executed with scoped tokens, and monitored through dashboards that display metrics and overrides. Feedback from these dashboards feeds design reviews where teams reassess whether autonomy still aligns with customer promises and regulatory obligations.",
            "callouts": [
                "Registries map actions to risk ratings and owners.",
                "Approval matrices define who can greenlight each capability.",
                "Runtime environments enforce token scopes and log every action.",
                "Dashboards surface autonomy health and inform performance reviews.",
            ],
        },
        "lab_setup": {
            "overview": """
Conduct an autonomy calibration exercise. Teams will map capabilities, configure approvals, and test emergency stop procedures for a customer-support agent.
""",
            "objective": "Ensure agents operate within agreed boundaries and that humans can intervene quickly.",
            "steps": [
                "List all current agent actions and classify them by risk and required approvals.",
                "Map each capability to explicit business value, associated blast radius, and required telemetry.",
                "Configure scoped tokens and update the capability registry.",
                "Implement approval workflows with notifications, reminders, and escalation targets.",
                "Simulate normal operations and track metrics such as approval latency and override frequency.",
                "Introduce failure scenarios (network outages, silent approval lapses) to test resilience and escalation paths.",
                "Trigger emergency stop procedures and verify tokens, sessions, and queued tasks are revoked.",
                "Interview stakeholders about clarity of roles and adjust documentation.",
                "Create dashboards summarizing tool usage, approvals, overrides, and sentiment feedback from human collaborators.",
                "Facilitate a partner or vendor walkthrough to confirm external stakeholders understand escalation paths and reporting expectations.",
                "Hold a retrospective capturing improvement opportunities and next actions, assigning deadlines and owners so remediation momentum continues.",
            ],
            "validation": "The lab succeeds when approvals work, emergency stops propagate, and stakeholders understand autonomy boundaries. Teams should exit with refreshed runbooks, agreed-upon success metrics, and executive commitments to revisit autonomy scorecards in quarterly business reviews.",
        },
        "code_exercise": {
            "overview": """
Implement a capability guard that enforces allowlists and approval requirements before invoking tools.
""",
            "language": "python",
            "snippet": """
from dataclasses import dataclass

@dataclass
class Capability:
    name: str
    requires_approval: bool

APPROVED_ACTIONS = {
    "create_ticket": Capability("create_ticket", requires_approval=False),
    "issue_refund": Capability("issue_refund", requires_approval=True),
}

def can_execute(action: str, approved: bool) -> bool:
    capability = APPROVED_ACTIONS.get(action)
    if capability is None:
        raise PermissionError("Action not registered")
    if capability.requires_approval and not approved:
        raise PermissionError("Approval required")
    return True
""",
            "explanation": "Although simplified, capability guards ensure agents cannot call tools outside registered scopes. Production systems would integrate with IAM, logging, workflow engines, and analytics that alert stakeholders when capabilities or approvals change.",
            "callouts": [
                "Store capability definitions in a registry managed by security and product teams.",
                "Link approvals to identity systems for accountability.",
                "Emit audit logs whenever actions are granted or denied.",
                "Support temporary elevation with automatic expiry and review.",
                "Provide clear error messages to agents for better UX.",
            ],
        },
        "case_intro": """
Organizations have learned the hard way that too much autonomy backfires. Study these cases to anticipate pitfalls, identify missing guardrails, and spark candid conversations about culture and accountability.
""",
        "case_studies": [
            {
                "organization": "Travel booking startup",
                "scenario": "An agent issued refunds and booked alternative flights without approval, exhausting monthly budgets.",
                "finding": "Capability scopes were undefined and approvals defaulted to auto-approve after five minutes.",
                "response": "The startup introduced tiered approvals, spending limits, and finance dashboards tracking agent actions. Leadership also paired finance analysts with product teams to review autonomy metrics weekly and update customer messaging about escalation options.",
            },
            {
                "organization": "Managed services provider",
                "scenario": "An agent modified firewall rules across multiple clients after misinterpreting an alert.",
                "finding": "Scoped tokens granted global access and runbooks lacked human checkpoints.",
                "response": "The provider segmented tokens per client, required change-management approvals, and rehearsed incident playbooks. They also introduced client-facing autonomy reports so customers could monitor how agents operated on their behalf.",
            },
            {
                "organization": "HR automation pilot",
                "scenario": "Agents sent offer letters and scheduled onboarding without HR review, causing contractual errors.",
                "finding": "Escalation paths were unclear and emergency stop controls were missing.",
                "response": "HR reinstated manual approvals for critical steps, clarified runbooks, and implemented dashboards tracking overrides. The team also launched training sessions that walked managers through autonomy levels, building empathy for the guardrails introduced.",
            },
        ],
        "case_outro": """
Autonomy is powerful when shared. These organizations regained trust by tightening scopes, clarifying roles, and investing in metrics. Use their journeys to frame your own roadmap, including executive updates, employee listening sessions, and phased rollouts that rebuild confidence.
""",
        "mnemonic": {
            "title": "GUIDED AGENT",
            "items": [
                {"letter": "G", "phrase": "Govern capabilities", "detail": "Document allowed actions and risks."},
                {"letter": "U", "phrase": "Understand context", "detail": "Require agents to share rationale with humans."},
                {"letter": "I", "phrase": "Instrument telemetry", "detail": "Track usage, approvals, and overrides."},
                {"letter": "D", "phrase": "Define approvals", "detail": "Map actions to approvers and escalation paths."},
                {"letter": "E", "phrase": "Establish stop controls", "detail": "Provide rapid shutdown mechanisms."},
                {"letter": "D", "phrase": "Develop culture", "detail": "Educate teams on intervening and sharing feedback."},
                {"letter": "A", "phrase": "Align incentives", "detail": "Reward teams for responsible automation use."},
                {"letter": "G", "phrase": "Guard tokens", "detail": "Issue scoped credentials with rotation and monitoring."},
                {"letter": "E", "phrase": "Evaluate regularly", "detail": "Hold autonomy reviews with cross-functional stakeholders."},
                {"letter": "N", "phrase": "Narrate decisions", "detail": "Log intent, approvals, and outcomes for transparency."},
                {"letter": "T", "phrase": "Test escalation", "detail": "Drill approvals and shutdowns to keep muscle memory fresh."},
            ],
        },
        "pitfall_intro": """
Watch for these warning signs when scaling agent autonomy. Share the list with program sponsors and product teams so they recognize when to pause deployments.
""",
        "pitfalls": [
            {"title": "Undefined capability boundaries", "detail": "Without documentation, agents accumulate permissions ad hoc. Catalog capabilities and align them with risk appetite before launch."},
            {"title": "Notification fatigue", "detail": "Approvers ignore alerts when volume is high or messaging is unclear. Require explicit confirmation and tailor notifications to reviewer schedules."},
            {"title": "Metrics blindness", "detail": "Teams lack dashboards to track autonomy health. Assign metric stewards who investigate anomalies and share summaries widely."},
            {"title": "No emergency stop", "detail": "Operations cannot pause agents quickly during incidents. Run quarterly rehearsals across time zones and document lessons learned."},
            {"title": "Cultural resistance", "detail": "Employees disengage or bypass automation when trust erodes. Celebrate healthy skepticism and require human sign-off for high-impact tasks."},
            {"title": "Shadow automation", "detail": "Teams build unofficial agents without governance oversight. Establish intake processes and highlight consequences of bypassing review."},
        ],
        "takeaway_intro": """
Align autonomy with mission-critical guardrails by tackling these actions first. Tie each initiative to measurable business outcomes so leaders see the value of disciplined governance.
""",
        "takeaways": [
            {"title": "Publish capability registries", "detail": "List approved actions, owners, and risk ratings."},
            {"title": "Instrument autonomy dashboards", "detail": "Expose tool usage, approvals, and overrides to stakeholders."},
            {"title": "Implement approval SLAs", "detail": "Define response times and escalation triggers for reviewers."},
            {"title": "Drill emergency stops", "detail": "Practice revoking tokens and pausing agents quarterly."},
            {"title": "Run autonomy retrospectives", "detail": "Gather feedback from operators and users to adjust guardrails."},
            {"title": "Educate champions", "detail": "Train representatives in each business unit to monitor and communicate automation health."},
            {"title": "Reward responsible automation", "detail": "Incorporate safety and collaboration metrics into performance reviews so teams value thoughtful interventions."},
        ],
        "takeaway_close": """
Autonomy thrives when humans remain engaged. Regular reviews, clear documentation, and transparent metrics transform agents into trusted teammates. Publish progress in leadership meetings and customer trust reports so stakeholders understand how safeguards evolve alongside capability expansion. Invite partner feedback and industry collaboration to benchmark maturity and share innovations that keep automation accountable.
""",
        "reflection_questions": [
            "Which agent capabilities currently lack explicit approvals or documentation?",
            "How quickly can you pause an agent if it misbehaves?",
            "What metrics demonstrate whether autonomy delivers value without risk?",
            "How will you keep stakeholders informed and comfortable as autonomy expands?",
            "What training or change-management activities are needed so employees feel empowered to challenge agents?",
            "How will you revisit autonomy decisions after incidents or major business shifts?",
            "What data do you need from partners or vendors to confirm their agents respect your guardrails?",
        ],
        "mindset": [
            """
Treat autonomy as a privilege agents must earn. Question assumptions, measure outcomes, and adjust scope as new information arrives.
""",
            """
Celebrate interventions. Highlight stories where humans prevented issues, reinforcing that oversight is heroic, not obstructive.
""",
            """
Encourage dialogue. Provide channels for employees to raise concerns or suggest improvements without fear.
""",
            """
Stay adaptable. As business priorities shift, revisit autonomy decisions to keep guardrails aligned with risk appetite.
""",
            """
Champion narrative transparency. Share stories about near misses and successful interventions so teams learn without stigma.
""",
            """
Balance ambition with humility. Remind stakeholders that automation amplifies both strengths and weaknesses, so governance is an enabler—not a brake—on innovation.
""",
            """
Invest in cross-company alliances. Coordinate with vendors and partners to align guardrails, share lessons, and co-design escalation paths before incidents occur.
""",
        ],
    },
    {
        "lesson_id": "2556bbec-803c-4a72-b4eb-288119ffc5c6",
        "slug": "owasp_llm07_system_prompt_leakage",
        "title": "OWASP LLM07: System Prompt Leakage",
        "subtitle": "Protecting foundational instructions and security policies",
        "difficulty": 2,
        "estimated_time": 110,
        "order_index": 10,
        "prerequisites": [],
        "concepts": [
            "system prompt design",
            "context isolation",
            "red teaming",
            "response hardening",
            "secret management",
            "policy communication",
        ],
        "learning_objectives": [
            "Describe how system prompts influence model behavior and why leakage matters.",
            "Implement defense-in-depth strategies that reduce exposure even if partial prompts leak.",
            "Detect prompt leakage attempts through telemetry, analytics, and adversarial testing.",
            "Design messaging and remediation workflows when leakage occurs.",
            "Coach teams to maintain prompt hygiene across development, staging, and production.",
        ],
        "post_assessment": [
            {
                "question": "Why is system prompt leakage risky?",
                "options": [
                    "Leaked prompts reveal security policies and allow attackers to craft bypasses.",
                    "Prompts are public marketing materials.",
                    "Leakage only affects UI styling.",
                    "Prompts contain no useful information.",
                ],
                "correct_answer": 0,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Which practice limits prompt leakage impact?",
                "options": [
                    "Embedding secrets directly into system prompts for convenience.",
                    "Segmenting prompts, storing them securely, and monitoring for unusual disclosure patterns.",
                    "Sharing prompts with every contractor via email.",
                    "Ignoring red-team findings that expose prompt text.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "How can teams detect prompt leakage attempts?",
                "options": [
                    "Disable logging to protect privacy.",
                    "Analyze conversations for meta-questions about policies, track unusual response lengths, and monitor sanitizer hits.",
                    "Ignore user feedback and rely on luck.",
                    "Treat all meta-questions as harmless.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "What should an organization do if a prompt leaks publicly?",
                "options": [
                    "Hide the incident and hope it fades.",
                    "Rotate secrets, update guardrails, communicate with stakeholders, and incorporate lessons learned.",
                    "Blame users and make no changes.",
                    "Delete all prompts without backups.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "attackers manipulate conversations or integrations to reveal hidden system prompts",
            "business_context": "prompts encode policies, compliance rules, and brand tone that protect the organization",
            "attacker_motivation": "gain insights into guardrails, secrets, or decision logic to craft future attacks",
            "human_factor": "developers share prompts over chat, forget to sanitize logs, or reuse them across environments",
            "control_challenge": "balancing transparency for debugging with secrecy for security",
            "innovation_balance": "documenting prompts responsibly so teams can iterate without exposing sensitive content",
            "closing_emphasis": "prompt stewardship is as critical as source code management",
        },
        "short_name": "System Prompt Leakage",
        "llm_code": "OWASP LLM07",
        "attack_vectors": [
            {
                "name": "Direct questioning",
                "detail": "attackers ask the model to reveal its instructions or explain how it makes decisions",
                "detail_secondary": "social engineering prompts mimic legitimate debugging queries",
                "impact": "prompts leak verbatim, exposing guardrails and sensitive context",
                "impact_secondary": "future attacks bypass protections using leaked phrases",
                "detection": "look for meta-questions about policies and unusually long responses",
                "telemetry": "log prompts, response lengths, and sanitizer hits for analysis",
                "mitigation": "train models to refuse meta-questions, reinforce with output filters, and provide safe explanations",
                "lesson_alignment": "OWASP emphasis on context isolation",
                "mitigation_reinforcement": "red-team sessions that attempt to extract prompts via creative questioning",
            },
            {
                "name": "Indirect leakage",
                "detail": "prompts appear in error messages, logs, or downstream tool responses",
                "detail_secondary": "developers include prompts in debug output or analytics dashboards",
                "impact": "logs become treasure troves for attackers or insiders",
                "impact_secondary": "cloud storage or BI exports spread prompts beyond security oversight",
                "detection": "scan logs and analytics for prompt signatures or keywords",
                "telemetry": "hash prompts and monitor for matches outside trusted systems",
                "mitigation": "mask prompts in logs, restrict access, and use secure viewers for debugging",
                "lesson_alignment": "OWASP guidance on logging hygiene",
                "mitigation_reinforcement": "include prompt leak checks in CI pipelines and log reviews",
            },
            {
                "name": "Integration overexposure",
                "detail": "partners request full prompts for customization or caching",
                "detail_secondary": "marketplace plug-ins store prompts insecurely or forward them to vendors",
                "impact": "prompts propagate outside contractual protections",
                "impact_secondary": "legal teams face disclosure obligations and renegotiate agreements",
                "detection": "monitor API requests for prompt export patterns and review contracts",
                "telemetry": "track which integrations request or store prompt snippets",
                "mitigation": "provide prompt fragments, require NDAs, and audit partner security",
                "lesson_alignment": "OWASP focus on third-party risk",
                "mitigation_reinforcement": "conduct partner assessments targeting prompt handling controls",
            },
            {
                "name": "Version control mishandling",
                "detail": "prompts checked into repositories or shared through collaboration tools",
                "detail_secondary": "branches or comments expose internal strategy to public contributors",
                "impact": "attackers mine git history or code reviews for prompt content",
                "impact_secondary": "supply chain compromises target repositories storing prompts",
                "detection": "scan repos for prompt signatures and sensitive phrases",
                "telemetry": "alert when prompts leave secure vaults or appear in pull requests",
                "mitigation": "store prompts in secret managers or configuration services with access controls",
                "lesson_alignment": "OWASP requirement for secure configuration management",
                "mitigation_reinforcement": "include prompt scanning in pre-commit hooks and code reviews",
            },
        ],
        "impact_overview": """
Prompt leakage undermines security posture and brand differentiation. Attackers learn which defenses exist and how to bypass them. Competitors copy tone and workflows. Regulators question whether sensitive data (such as PII masked via prompts) is adequately protected. Customers lose confidence if transcripts show behind-the-scenes instructions meant to remain invisible.

Beyond immediate embarrassment, leakage sets the stage for future compromises. Once adversaries catalog internal instructions, they craft precise jailbreaks, trick content filters, or replicate support workflows that rely on hidden disclaimers. Sales and legal teams must explain to prospects how a supposedly mature AI program allowed its most sensitive instructions to escape. Crisis communications consumes leadership attention while product roadmaps stall.

Leaks also hand blueprints to fraudsters. Contact centers report social-engineering attempts that quote leaked prompts verbatim to bypass verification. Marketplace scammers spin up cloned assistants that mimic your brand voice, siphoning revenue while damaging trust. Executives must weigh takedown costs, litigation, and customer restitution against the reputational damage of appearing careless with proprietary knowledge.

Leak incidents also expose cultural fissures. Engineers may feel blamed for sharing prompts during debugging; support agents worry about the accuracy of new guardrails; procurement demands stronger vendor commitments. Without a thoughtful response, these tensions slow adoption and erode confidence that the organization can innovate responsibly.

Regulators increasingly treat prompt leakage as a disclosure event, especially when prompts encode policy logic that substitutes for human judgment. Organizations operating across regions must coordinate legal reviews, data protection officers, and public affairs teams to ensure responses meet statutory timelines while maintaining consistent messaging.

Mature teams go further by rehearsing cross-border response drills, pre-authorizing translation pipelines for updated prompts, and stress-testing vendor ecosystems to confirm partners can apply new templates quickly. These preparations demonstrate diligence to auditors and reassure customers that the organization treats prompt stewardship with the same gravity as source-code security.
""",
        "impact_zones": [
            {
                "area": "Security controls",
                "detail": "Leaked prompts disclose guardrail logic, making future attacks easier.",
            },
            {
                "area": "Competitive advantage",
                "detail": "Prompts encode brand voice and unique workflows that competitors can emulate.",
            },
            {
                "area": "Regulatory compliance",
                "detail": "Prompts sometimes contain policy references or legal guidance that must be kept confidential.",
            },
            {
                "area": "Incident response",
                "detail": "Teams must rotate secrets, update prompts, and communicate transparently, consuming time and resources.",
            },
            {
                "area": "Partner trust",
                "detail": "Vendors and marketplace integrators question whether shared prompts or templates are safe, delaying collaborations and joint feature launches.",
            },
            {
                "area": "Employee confidence",
                "detail": "Designers, writers, and policy experts fear their expertise is exposed or misused, reducing willingness to experiment with new prompt strategies.",
            },
        ],
        "detection_intro": """
Combine automated scanning with human review. Analyze conversation logs for policy-related questions, monitor for hashed prompt fragments, and set alerts on repositories or analytics platforms where prompts should never appear.

Effective programs treat leakage detection as a cross-team mission. Security engineers tune anomaly models, knowledge engineers review suspicious transcripts, legal advisors flag jurisdictions with disclosure requirements, and communications teams rehearse messaging. Weekly reviews prevent alert fatigue and align detection thresholds with business realities.
""",
        "detection_focus": [
            {
                "name": "Prompt signature monitoring",
                "detail": "Create hashed fingerprints of prompts and search for them across systems.",
                "correlation": "Compare hits with change windows or red-team exercises.",
                "forensics": "Record system, user, and timestamp when matches occur.",
            },
            {
                "name": "Meta-question analytics",
                "detail": "Detect users asking about policies, instructions, or internal logic.",
                "correlation": "Link to session IDs and tool usage to assess risk.",
                "forensics": "Store transcripts and reviewer notes for training and legal review.",
            },
            {
                "name": "Log scanning",
                "detail": "Use DLP and pattern matching to ensure prompts are redacted in logs and BI exports.",
                "correlation": "Align findings with new logging pipelines or vendor integrations.",
                "forensics": "Maintain sanitized and raw copies in secure vaults.",
            },
            {
                "name": "Repository audits",
                "detail": "Automate scans for prompt keywords in commits, pull requests, and comments.",
                "correlation": "Alert security champions and require remediation before merges.",
                "forensics": "Track commit history and review approvals for accountability.",
            },
            {
                "name": "Partner telemetry",
                "detail": "Monitor third-party integrations for unusual prompt export requests or cache synchronization events.",
                "correlation": "Compare with contract clauses and vendor change notifications to validate legitimacy.",
                "forensics": "Store API traces, headers, and partner attestations to support investigations and renewals.",
            },
            {
                "name": "Employee sharing channels",
                "detail": "Track when prompts appear in collaboration tools, ticketing systems, or knowledge bases.",
                "correlation": "Align hits with escalation tickets or training sessions to distinguish legitimate use from risky behavior.",
                "forensics": "Preserve conversation snippets with access controls so security and legal can review context.",
            },
        ],
        "guardrail_intro": """
Treat prompts as sensitive configuration. Limit exposure, log access, and rotate when leaks occur. Document ownership so updates happen safely.

Guardrails should blend technical controls with contractual obligations and cultural expectations. When teams know who owns prompts, how to request access, and what evidence auditors expect, they are less likely to take shortcuts during debugging or experimentation.
""",
        "guardrail_layers": [
            {
                "name": "Prompt vault",
                "detail": "Store prompts in secret managers with role-based access control and version history.",
                "conditions": "development, staging, and production",
                "practice": "audit access logs and require approvals for changes",
                "alignment": "secret management policies",
            },
            {
                "name": "Segmentation and templating",
                "detail": "Split prompts into reusable modules so partial leaks reveal minimal context.",
                "conditions": "prompt authoring and deployment",
                "practice": "maintain templates in secure repositories with change review",
                "alignment": "secure SDLC and configuration management",
            },
            {
                "name": "Leak response playbook",
                "detail": "Define steps for rotating secrets, updating prompts, and notifying stakeholders.",
                "conditions": "activated during suspected leakage",
                "practice": "rehearse with legal, PR, and engineering",
                "alignment": "incident response frameworks",
            },
            {
                "name": "Red-team program",
                "detail": "Regularly test for prompt extraction via direct and indirect techniques.",
                "conditions": "quarterly or before major releases",
                "practice": "share results with developers and update guardrails",
                "alignment": "continuous assurance and OWASP testing guidance",
            },
            {
                "name": "Prompt access council",
                "detail": "Cross-functional committee that approves access requests, reviews incident reports, and aligns contracts with internal policies.",
                "conditions": "ongoing, with emergency sessions during suspected leaks",
                "practice": "document decisions, track exceptions, and publish summaries for leadership and auditors",
                "alignment": "governance, risk, and compliance frameworks",
            },
            {
                "name": "Collaboration hygiene program",
                "detail": "Establish approved channels for sharing prompts during debugging, including secure viewers and expiration policies.",
                "conditions": "whenever teams need to troubleshoot or localize prompt content",
                "practice": "provide templates, train employees, and audit chat platforms for adherence",
                "alignment": "acceptable use policies and secure development standards",
            },
        ],
        "operational_story": """
Prompt stewardship spans multiple teams. Product owners define tone, security architects enforce storage controls, legal reviews messaging, and customer support prepares responses if leakage occurs. Collaboration ensures updates roll out smoothly.

High-performing organizations run quarterly “prompt summits” where engineers, policy writers, and marketing teams review changes, discuss red-team findings, and prioritize improvements. They maintain clear runbooks for updating prompts across environments, including stakeholder notifications, translation requirements, and accessibility reviews.

When leaks occur, a fusion cell assembles to trace exposure, coordinate vendor outreach, and publish customer updates. Post-incident retrospectives feed training modules that remind developers how to debug safely and show executives the metrics that prove progress.
""",
        "video": {
            "title": "Guarding the Invisible Layer",
            "url": "https://www.youtube.com/watch?v=KfZ2K2cVh2c",
            "description": "Security engineers walk through prompt leak incidents, showing prevention and response strategies. They highlight board-level reporting, contract updates, and staff training that followed each disclosure.",
            "focus_points": [
                "How prompts leaked through logs or debugging tools.",
                "Steps taken to rotate secrets and rebuild trust.",
                "Tooling used to fingerprint prompts and monitor for reoccurrence.",
                "Cross-functional communication patterns that sped up remediation.",
                "Ideas for measuring prompt hygiene and sharing progress with leadership and customers.",
            ],
        },
        "diagram": {
            "intro": "Prompt lifecycle management involves secure storage, controlled usage, and monitoring:",
            "ascii": """
 Authoring -> Prompt Vault -> Deployment -> Monitoring
      |           |               |             |
  Reviews     Access Control   Templating   Leak Detection
""",
            "explanation": "Prompts move from authoring to secure vaults, then deploy through templating pipelines. Monitoring systems watch for leakage, closing the loop with authoring teams. Feedback from monitoring informs authoring reviews so policy changes and tone adjustments include security input from the start.",
            "callouts": [
                "Authoring includes security review and legal sign-off.",
                "Vaults track versions and access events.",
                "Deployment injects prompts via templating, not hardcoding.",
                "Monitoring uses fingerprints and analytics to detect leakage.",
                "Governance councils review metrics and approve changes before prompts reach production.",
            ],
        },
        "lab_setup": {
            "overview": """
Run a prompt hygiene workshop. Participants will secure prompts, test extraction attempts, and practice leak response.
""",
            "objective": "Ensure teams can protect prompts, detect leakage, and recover quickly.",
            "steps": [
                "Inventory current prompts and classify sensitivity.",
                "Store prompts in a vault with role-based access and create fingerprints.",
                "Simulate extraction attempts via direct questioning, log scraping, and API misuse.",
                "Verify detection alerts fire and analysts can trace the session.",
                "Review partner API logs to confirm integrations honor contractual restrictions on prompt access.",
                "Activate the leak response playbook, rotating secrets and updating prompts.",
                "Draft communications for stakeholders and customers.",
                "Rehearse legal and compliance notifications for regulated regions.",
                "Document lessons learned and adjust policies.",
                "Schedule follow-up red-team exercises focusing on new attack vectors.",
                "Compile metrics and narrative highlights into a debrief presented to executives and partner liaisons.",
            ],
            "validation": "Success criteria include timely detection, smooth remediation, and updated documentation. Teams should capture mean-time-to-detect, legal notification timelines, and partner feedback to drive future investments, then feed the results into governance councils for accountability.",
        },
        "code_exercise": {
            "overview": """
Create a fingerprinting tool that hashes prompts and scans logs for matches.
""",
            "language": "python",
            "snippet": """
import hashlib

def fingerprint(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

def scan_logs(logs: list[str], fingerprint_value: str) -> list[str]:
    hits = []
    for entry in logs:
        if fingerprint_value in entry:
            hits.append(entry)
    return hits
""",
            "explanation": "Fingerprinting allows teams to monitor for prompt leakage without storing plaintext. Production systems would encrypt fingerprints, integrate with SIEM, support partial matches, and correlate hits with ticketing systems so analysts can track investigation progress.",
            "callouts": [
                "Rotate fingerprints when prompts change.",
                "Secure logs to prevent attackers from learning hash values.",
                "Combine with DLP and semantic scans for partial matches.",
                "Alert on hits and initiate response playbooks.",
                "Share results with prompt authors to refine content.",
            ],
        },
        "case_intro": """
Prompt leakage incidents offer valuable lessons. Review these stories to build resilient practices, map communication gaps, and understand which governance controls restored trust.
""",
        "case_studies": [
            {
                "organization": "E-commerce support bot",
                "scenario": "A customer tricked the assistant into revealing its prompt, which contained discount codes and fraud detection thresholds.",
                "finding": "Prompts were static strings without refusal training or output filtering.",
                "response": "The company restructured prompts into modules, strengthened refusals, monitored for future attempts, and worked with marketing and legal to refresh campaign language explaining new safeguards.",
            },
            {
                "organization": "Public chatbot platform",
                "scenario": "An open-source contributor accidentally committed prompts containing internal policy references.",
                "finding": "Prompts lived in git repositories without DLP scanning.",
                "response": "The platform moved prompts to a vault, added pre-commit hooks, rotated secrets, and published contributor guidelines that explain safe debugging alternatives.",
            },
            {
                "organization": "Financial advisory assistant",
                "scenario": "A partner integration stored prompts in logs to debug latency, which were later exposed in a breach.",
                "finding": "Contracts lacked explicit prompt handling requirements and logging controls.",
                "response": "Legal updated agreements, security enabled masking, the partner implemented stricter storage policies, and joint tabletop exercises rehearsed future disclosures.",
            },
        ],
        "case_outro": """
Every leak is an opportunity to improve. Transparency, disciplined storage, and swift remediation build long-term trust. Incorporate these scenarios into red-team briefings so executives and vendors practice transparent communication under pressure, and record action items that feed into quarterly governance updates and vendor retrospectives.
""",
        "mnemonic": {
            "title": "PROMPT SAFE",
            "items": [
                {"letter": "P", "phrase": "Protect storage", "detail": "Use vaults and RBAC."},
                {"letter": "R", "phrase": "Review changes", "detail": "Peer review prompt updates."},
                {"letter": "O", "phrase": "Obscure secrets", "detail": "Keep credentials outside prompts."},
                {"letter": "M", "phrase": "Monitor leaks", "detail": "Fingerprint and scan logs."},
                {"letter": "P", "phrase": "Practice response", "detail": "Rehearse leak playbooks."},
                {"letter": "T", "phrase": "Test extraction", "detail": "Run red-team exercises."},
                {"letter": "S", "phrase": "Segment context", "detail": "Modularize prompts to limit blast radius."},
                {"letter": "A", "phrase": "Audit access", "detail": "Track who reads or exports prompts."},
                {"letter": "F", "phrase": "Fuzz defenses", "detail": "Use adversarial prompts to validate refusals."},
                {"letter": "E", "phrase": "Educate teams", "detail": "Train developers and partners on prompt hygiene."},
            ],
        },
        "pitfall_intro": """
Avoid common mistakes that expose prompts. Review this list during code reviews, partner onboarding, and red-team debriefs to keep urgency high.
""",
        "pitfalls": [
            {"title": "Hardcoding prompts", "detail": "Embedding prompts in application code invites leaks via repos and logs. Use templating systems and secure configuration services instead."},
            {"title": "Sharing via chat", "detail": "Screenshots or copy-paste in collaboration tools bypass access controls. Provide secure viewers and train teams to avoid informal sharing."},
            {"title": "Ignoring red-team results", "detail": "Findings recur when not addressed promptly. Assign owners, deadlines, and track remediation metrics."},
            {"title": "No ownership", "detail": "Without a designated steward, prompts drift and leaks go unnoticed. Establish clear RACI models and review them quarterly."},
            {"title": "Lack of telemetry", "detail": "Teams cannot detect leakage without fingerprints or analytics. Instrument scanning across logs, repos, and partner APIs."},
            {"title": "Slow response", "detail": "Delayed remediation prolongs exposure and damages trust. Practice playbooks and pre-stage communications assets."},
        ],
        "takeaway_intro": """
Prioritize these actions to secure prompts this quarter. Assign owners, budgets, and deadlines so progress survives competing product priorities.
""",
        "takeaways": [
            {"title": "Stand up a prompt vault", "detail": "Centralize storage with RBAC and versioning."},
            {"title": "Implement fingerprint monitoring", "detail": "Hash prompts and scan logs and repositories."},
            {"title": "Refresh refusal patterns", "detail": "Update models and filters to resist extraction prompts."},
            {"title": "Document leak response", "detail": "Create playbooks covering rotation, communication, and lessons learned."},
            {"title": "Train stakeholders", "detail": "Host workshops on prompt hygiene for developers, legal, and partners."},
            {"title": "Schedule red-team exercises", "detail": "Test extraction techniques regularly and track improvements."},
            {"title": "Audit partner access", "detail": "Review contracts, telemetry, and incident drills with vendors handling prompts."},
            {"title": "Publish transparency reports", "detail": "Share aggregated metrics with executives and customers to demonstrate prompt stewardship."},
        ],
        "takeaway_close": """
Prompt security is achievable with discipline. Protecting the invisible layer builds customer trust and keeps guardrails effective. Celebrate milestones publicly so teams internalize that prompt hygiene is as strategic as new feature delivery. Share anonymized lessons with industry peers to strengthen the broader ecosystem against similar threats, and invite their feedback to spot blind spots you may have missed collectively.
""",
        "reflection_questions": [
            "Where are prompts stored today, and who has access?",
            "How would you detect if a prompt leaked via logs or partners?",
            "What is your rotation plan when prompts change or leak?",
            "How will you educate new team members on prompt hygiene?",
            "Which vendors or contractors interact with prompts, and what evidence proves they follow your policies?",
            "How often will you review prompt tone, policy language, and refusal strategies to keep pace with brand and regulatory shifts?",
            "What metrics will you share with executives and customers to demonstrate continuous improvement in prompt security?",
        ],
        "mindset": [
            """
Treat prompts like privileged knowledge. Share only what is necessary and monitor usage relentlessly.
""",
            """
Celebrate vigilance. When teams catch potential leaks early, recognize their contribution to security culture.
""",
            """
Encourage curiosity. Ask how prompts might appear in unexpected places and address those pathways.
""",
            """
Stay humble. Assume leakage will eventually occur and prepare recovery plans so the organization responds gracefully.
""",
            """
Foster partnership. Collaborate with legal, compliance, and marketing so prompt updates reinforce shared narratives rather than conflicting messages.
""",
            """
Invest in continuous learning. Share sanitized leak retrospectives internally and with industry peers to raise the bar for everyone.
""",
            """
Respect legal cadence. Coordinate with privacy officers and regulatory teams so prompt hygiene work satisfies regional obligations without surprising stakeholders or conflicting with disclosure commitments.
""",
        ],
    },
    {
        "lesson_id": "4860408e-4e36-481e-ba13-09d9661f176d",
        "slug": "owasp_llm08_vector_and_embedding_weaknesses",
        "title": "OWASP LLM08: Vector and Embedding Weaknesses",
        "subtitle": "Hardening semantic search and retrieval systems",
        "difficulty": 3,
        "estimated_time": 125,
        "order_index": 11,
        "prerequisites": [],
        "concepts": [
            "vector databases",
            "embedding security",
            "semantic collisions",
            "poisoned retrieval",
            "access control",
            "observability",
        ],
        "learning_objectives": [
            "Explain how embedding pipelines and vector stores can be manipulated.",
            "Design validation and monitoring strategies for embedding generation and search.",
            "Implement access control, encryption, and data hygiene for vector databases.",
            "Detect anomalous queries and collision attacks using metrics and alerting.",
            "Coordinate red-teaming and governance across data engineering, security, and product teams.",
        ],
        "post_assessment": [
            {
                "question": "Which attack targets embedding systems?",
                "options": [
                    "Asking a chatbot for weather updates.",
                    "Injecting poisoned documents so semantic search retrieves attacker-controlled content.",
                    "Disabling TLS on an unrelated API.",
                    "Changing UI colors.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
            {
                "question": "Why are semantic collisions dangerous?",
                "options": [
                    "They slow down indexing slightly.",
                    "Attackers craft embeddings similar to sensitive documents to bypass filters.",
                    "They only affect image models.",
                    "Collisions have no practical impact.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
            {
                "question": "Which control protects vector databases in transit and at rest?",
                "options": [
                    "Plaintext connections and open ACLs.",
                    "TLS, encryption, and role-based access control.",
                    "Manual CSV exports shared via email.",
                    "Unauthenticated debug endpoints.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "How can teams monitor embedding quality?",
                "options": [
                    "Ignore metrics because embeddings are static.",
                    "Track drift, collision rates, and anomaly scores, feeding results into dashboards and alerting.",
                    "Rely on manual spot checks twice a year.",
                    "Disable logging to reduce storage.",
                ],
                "correct_answer": 1,
                "difficulty": 3,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "embedding pipelines and vector stores become attack surfaces when poisoned, misconfigured, or exposed",
            "business_context": "LLM applications rely on semantic search to deliver relevant context, recommendations, and alerts",
            "attacker_motivation": "manipulate retrieval to surface malicious content, exfiltrate data, or corrupt analytics",
            "human_factor": "teams treat vector databases like simple caches without access control or monitoring",
            "control_challenge": "balancing performance and freshness with validation and security controls",
            "innovation_balance": "empowering rapid experimentation while enforcing data hygiene and observability",
            "closing_emphasis": "embedding security is foundational to trustworthy AI experiences",
        },
        "short_name": "Vector and Embedding Weaknesses",
        "llm_code": "OWASP LLM08",
        "attack_vectors": [
            {
                "name": "Poisoned embeddings",
                "detail": "attackers insert crafted documents into ingestion pipelines, producing embeddings that hijack search results",
                "detail_secondary": "malicious vectors mimic legitimate topics but contain payloads or disinformation",
                "impact": "assistants retrieve and trust poisoned context, leading to bad advice or data leaks",
                "impact_secondary": "analysts lose confidence in retrieval quality",
                "detection": "monitor embedding statistics, outlier scores, and source provenance",
                "telemetry": "record dataset lineage, ingestion approvals, and embedding hashes",
                "mitigation": "validate sources, apply content filters, and quarantine suspicious documents",
                "lesson_alignment": "OWASP focus on data integrity",
                "mitigation_reinforcement": "red-team ingestion pipelines with synthetic poisoned content",
            },
            {
                "name": "Semantic collisions",
                "detail": "attackers generate embeddings similar to high-value documents using model inversion or optimization",
                "detail_secondary": "collisions bypass keyword filters and access controls based on metadata",
                "impact": "retrieval surfaces attacker content, and leakage occurs when collisions mimic secrets",
                "impact_secondary": "monitoring dashboards show normal query volume despite manipulation",
                "detection": "track cosine similarity distributions and rate-limit repeated queries",
                "telemetry": "log embeddings for high-sensitivity queries with anonymized fingerprints",
                "mitigation": "apply semantic firewalls, query risk scoring, and layered authorization",
                "lesson_alignment": "OWASP emphasis on access control",
                "mitigation_reinforcement": "test collisions with adversarial tools and update firewalls accordingly",
            },
            {
                "name": "Vector database compromise",
                "detail": "misconfigured clusters expose embeddings via unauthenticated endpoints or weak credentials",
                "detail_secondary": "cloud snapshots or backups remain unencrypted",
                "impact": "attackers download embeddings, infer original documents, or delete indexes",
                "impact_secondary": "regulatory exposure when sensitive embeddings leave the perimeter",
                "detection": "monitor access logs, failed authentication, and unusual export sizes",
                "telemetry": "centralize audit trails in SIEM with geolocation and client metadata",
                "mitigation": "enforce TLS, RBAC, encryption, and network segmentation",
                "lesson_alignment": "OWASP requirement for secure infrastructure",
                "mitigation_reinforcement": "conduct configuration audits and automated security scans",
            },
            {
                "name": "Query abuse and denial-of-wallet",
                "detail": "attackers issue expensive embedding queries or high-dimensional searches to exhaust resources",
                "detail_secondary": "bots rotate tokens to bypass quotas",
                "impact": "latency spikes, costs soar, and legitimate users experience outages",
                "impact_secondary": "incident response focuses on capacity rather than root cause",
                "detection": "track query patterns, throttle per-tenant usage, and alert on cost anomalies",
                "telemetry": "collect per-query cost, tenant ID, and feature flags",
                "mitigation": "enforce quotas, caching, and rate limiting; offer fallback tiers",
                "lesson_alignment": "OWASP unbounded consumption controls",
                "mitigation_reinforcement": "simulate high-volume attacks to validate throttling",
            },
        ],
        "impact_overview": """
Embedding weaknesses compromise search accuracy, confidentiality, and performance. When vector stores are polluted or exposed, assistants amplify misinformation, expose secrets, or degrade user experience. Executives question return on investment if retrieval cannot be trusted.

Operational teams feel the pain immediately. Product managers scramble to explain odd recommendations, security analysts investigate unexplained data exposure, and support teams triage customer complaints. Meanwhile, data scientists must halt experimentation to clean corrupted indexes, slowing innovation and eroding confidence that semantic search is worth the effort.

Regulators and auditors increasingly scrutinize retrieval systems because embeddings can encode sensitive information. Organizations must demonstrate provenance, access controls, and timely response plans or risk fines, contract penalties, and reputational damage. Investors and enterprise buyers demand evidence that semantic pipelines are as resilient as traditional databases.
Collaboration with industry peers through ISACs and working groups helps organizations share new attack patterns and defensive innovations, keeping pipelines resilient amid fast-moving research.
""",
        "impact_zones": [
            {
                "area": "Search relevance",
                "detail": "Poisoned or colliding embeddings distort answers, hurting user trust and decision quality.",
            },
            {
                "area": "Data confidentiality",
                "detail": "Embeddings can leak sensitive information when inverted or misused.",
            },
            {
                "area": "Operational costs",
                "detail": "Abusive queries drive compute spend and cause outages.",
            },
            {
                "area": "Compliance",
                "detail": "Regulations require control over how data is stored, processed, and accessed—even as embeddings.",
            },
            {
                "area": "Analytics credibility",
                "detail": "Business intelligence built on vector search loses value when embeddings drift or are poisoned, leading executives to distrust dashboards and predictive models.",
            },
            {
                "area": "Partner ecosystems",
                "detail": "Marketplace integrations that consume or contribute embeddings spread risk across organizations, creating cascading obligations to monitor and report anomalies.",
            },
            {
                "area": "Customer trust signals",
                "detail": "Support tickets, search satisfaction scores, and NPS feedback deteriorate when retrieval becomes unreliable, increasing churn.",
            },
        ],
        "detection_intro": """
Monitor embedding pipelines end to end. Validate inputs, track embedding drift, monitor query behavior, and correlate anomalies across ingestion, storage, and retrieval.

Effective detection blends statistical signals with human insights. Data engineers review anomaly dashboards, product teams analyze search quality feedback, and security operations investigate suspicious exports. Weekly retrospectives ensure detections translate into remediation tickets rather than lingering as noise.
""",
        "detection_focus": [
            {
                "name": "Embedding drift",
                "detail": "Compare embeddings across model versions and time to catch shifts.",
                "correlation": "Link drift to dataset changes or model upgrades.",
                "forensics": "Store summary stats and sample vectors for analysis.",
            },
            {
                "name": "Collision detection",
                "detail": "Identify clusters of highly similar embeddings originating from different sources.",
                "correlation": "Track repeated query fingerprints and user agents.",
                "forensics": "Capture example vectors and related documents for review.",
            },
            {
                "name": "Access anomaly alerts",
                "detail": "Monitor authentication failures, new IPs, or large exports from vector stores.",
                "correlation": "Tie to IAM changes, incident tickets, or partner integrations.",
                "forensics": "Collect logs, network traces, and session metadata.",
            },
            {
                "name": "Cost and latency metrics",
                "detail": "Track per-tenant query costs and response times.",
                "correlation": "Detect denial-of-wallet campaigns or misconfigured caches.",
                "forensics": "Store detailed metrics for root-cause analysis and budgeting.",
            },
            {
                "name": "Search quality feedback",
                "detail": "Analyze user ratings, click-through rates, and relevance audits for sudden drops.",
                "correlation": "Align declines with ingestion events, model updates, or suspected poisoning.",
                "forensics": "Preserve sample queries and retrieved documents for manual review and retraining.",
            },
            {
                "name": "Partner and API monitoring",
                "detail": "Track external services contributing embeddings or consuming results for unusual behavior.",
                "correlation": "Compare with contract commitments, maintenance windows, and incident reports.",
                "forensics": "Collect API traces, signed attestations, and partner communications to support investigations.",
            },
            {
                "name": "Customer feedback loops",
                "detail": "Aggregate relevance scores, ticket themes, and search abandonment rates.",
                "correlation": "Relate drops to ingestion batches, model updates, or suspected abuse.",
                "forensics": "Store annotated transcripts and user reports for retraining and postmortems.",
            },
        ],
        "guardrail_intro": """
Combine data hygiene, access control, monitoring, and resilience. Embedding security is holistic: trust no single layer.

Guardrails must also address organizational processes. Procurement sets expectations for vendors, data governance teams define stewardship, and product owners document fallback experiences when retrieval degrades.
""",
        "guardrail_layers": [
            {
                "name": "Ingestion validation",
                "detail": "Scan documents for malicious content, metadata anomalies, and provenance before embedding.",
                "conditions": "prior to embedding generation",
                "practice": "assign data stewards and maintain allowlists/denylists",
                "alignment": "data governance policies",
            },
            {
                "name": "Secure vector storage",
                "detail": "Apply encryption, RBAC, TLS, and network segmentation to vector databases.",
                "conditions": "across environments",
                "practice": "review configs, rotate credentials, and audit access",
                "alignment": "infrastructure security standards",
            },
            {
                "name": "Semantic firewalls",
                "detail": "Implement risk scoring, query throttling, and content filtering on retrieval.",
                "conditions": "during query execution",
                "practice": "update thresholds with red-team feedback and business priorities",
                "alignment": "OWASP guardrail principles",
            },
            {
                "name": "Observability and alerting",
                "detail": "Centralize metrics, logs, and anomaly detection for embedding pipelines.",
                "conditions": "continuous",
                "practice": "integrate with SIEM, set runbooks, and review dashboards with stakeholders",
                "alignment": "operational excellence and compliance",
            },
            {
                "name": "Partner governance",
                "detail": "Define contractual controls, attestations, and audit rights for vendors supplying or consuming embeddings.",
                "conditions": "during onboarding, renewal, and incident response",
                "practice": "review evidence, run joint tabletop exercises, and track remediation commitments",
                "alignment": "third-party risk management frameworks",
            },
            {
                "name": "Resilience playbooks",
                "detail": "Establish fallback retrieval modes, cache purging procedures, and communication templates for degraded service.",
                "conditions": "activated during suspected poisoning, outages, or query abuse",
                "practice": "test rollback to golden datasets, coordinate with SRE, and notify customers transparently",
                "alignment": "business continuity and incident response plans",
            },
            {
                "name": "Data retention controls",
                "detail": "Define how long embeddings, source documents, and telemetry persist to balance analysis and privacy.",
                "conditions": "during storage lifecycle planning and compliance reviews",
                "practice": "set retention schedules, automate deletion, and document exceptions",
                "alignment": "privacy regulations and contractual obligations",
            },
        ],
        "operational_story": """
Embedding security requires cross-functional ownership. Data engineers manage ingestion, ML teams tune models, security enforces access, and product teams interpret metrics. Regular syncs ensure signals translate into action.

Leading organizations operate embedding command centers during launches or major updates. These war rooms monitor drift, relevance, and cost metrics in real time while executives receive concise status updates. When anomalies appear, teams quickly trace lineage, quarantine suspect content, and communicate with impacted stakeholders.

Post-incident retrospectives feed investment roadmaps: new validation tooling, better partner vetting, or clearer customer messaging when retrieval confidence dips. Sharing these stories across the company normalizes proactive defense instead of reactive cleanup and reinforces that embedding security is a shared success metric. Metrics from these exercises appear in executive dashboards and customer trust reports so leadership can track progress transparently.
""",
        "video": {
            "title": "Securing Vector Search Pipelines",
            "url": "https://www.youtube.com/watch?v=iGdwS5x1w6U",
            "description": "Experts discuss embedding poisoning, access control, and observability patterns for enterprise vector search. They share post-incident retrospectives and tooling demos that restored trust after real compromises.",
            "focus_points": [
                "How ingestion validation catches poisoned data.",
                "Metrics used to detect semantic collisions and query abuse.",
                "Security controls for vector databases in regulated industries.",
                "Ways to communicate embedding risk to executives.",
                "Ideas for designing fallback experiences when retrieval confidence drops.",
            ],
        },
        "diagram": {
            "intro": "Embedding pipelines span ingestion, storage, and retrieval:",
            "ascii": """
 Data Sources -> Validation -> Embedding Service -> Vector DB -> Semantic Firewall -> LLM
        |             |                 |               |                     |
    Provenance   QA Checks       Version Control    RBAC & TLS           Monitoring
""",
            "explanation": "Each stage enforces security controls. Validation ensures clean inputs, embedding services maintain version control, vector databases enforce RBAC, and semantic firewalls protect retrieval. Observability threads through every block, streaming metrics to teams responsible for immediate action and feeding governance reviews that adjust policies.",
            "callouts": [
                "Validation includes content scanning and provenance tagging.",
                "Embedding services log versions and hash outputs.",
                "Vector DBs integrate with IAM and encryption.",
                "Semantic firewalls throttle and sanitize responses.",
                "Monitoring dashboards capture partner activity and resilience drill outcomes.",
            ],
        },
        "lab_setup": {
            "overview": """
Build a secure embedding pipeline. Participants will ingest documents, detect poisoning, secure the vector store, and tune semantic firewalls.
""",
            "objective": "Demonstrate end-to-end controls for embeddings, from ingestion to retrieval.",
            "steps": [
                "Set up ingestion with validation checks and provenance metadata.",
                "Generate embeddings with version logging and hash storage.",
                "Secure the vector database with TLS, RBAC, and audit logging.",
                "Introduce poisoned and colliding embeddings to test detection.",
                "Configure semantic firewalls to score queries and enforce throttling.",
                "Monitor metrics for drift, collisions, and cost anomalies.",
                "Execute incident response by quarantining poisoned vectors and restoring from clean snapshots.",
                "Review partner telemetry and confirm contracts define reporting expectations.",
                "Run resilience drills by switching to fallback retrieval or cached answers.",
                "Document lessons learned and assign owners for ongoing monitoring.",
            ],
            "validation": "Controls work when poisoned vectors are blocked, anomalies trigger alerts, and rollbacks restore integrity quickly. Capture time-to-detect, downstream customer impact, and backlog items for governance councils.",
        },
        "code_exercise": {
            "overview": """
Implement a collision detector using approximate nearest neighbors to flag suspicious similarity clusters.
""",
            "language": "python",
            "snippet": """
import numpy as np
from sklearn.neighbors import NearestNeighbors

def detect_collisions(vectors: np.ndarray, threshold: float = 0.95) -> list[tuple[int, int, float]]:
    nn = NearestNeighbors(metric="cosine", algorithm="brute")
    nn.fit(vectors)
    distances, indices = nn.kneighbors(vectors, n_neighbors=5)
    collisions = []
    for i, (dists, neighs) in enumerate(zip(distances, indices)):
        for dist, neighbor in zip(dists[1:], neighs[1:]):
            similarity = 1 - dist
            if similarity >= threshold:
                collisions.append((i, neighbor, similarity))
    return collisions
""",
            "explanation": "Collision detectors highlight embeddings that are unusually similar. Combined with provenance data, they help teams identify poisoning or leakage attempts. Production pipelines would stream collision results into case management systems and compare against partner telemetry.",
            "callouts": [
                "Adjust thresholds per dataset to balance false positives and negatives.",
                "Log collisions with metadata for forensic review.",
                "Integrate with semantic firewalls to block suspicious queries in real time.",
                "Sample collisions for manual review to improve detection accuracy.",
                "Automate ticket creation for security analysts when collisions spike.",
                "Correlate collision clusters with customer feedback to prioritize remediation.",
            ],
        },
        "case_intro": """
Embedding incidents are on the rise. Review these cases to strengthen your defenses, identify governance gaps, and inspire tabletop drills.
""",
        "case_studies": [
            {
                "organization": "Media monitoring platform",
                "scenario": "Attackers uploaded articles with hidden payloads that dominated semantic search results.",
                "finding": "Ingestion lacked validation and rate limiting.",
                "response": "The platform added validation, source reputation scoring, and semantic firewalls, then launched customer communications explaining how search quality would be monitored.",
            },
            {
                "organization": "Healthcare knowledge base",
                "scenario": "An exposed vector database allowed anonymous downloads of embeddings derived from medical records.",
                "finding": "No authentication or encryption protected the cluster.",
                "response": "The provider enforced RBAC, encryption, and continuous monitoring while coordinating with compliance teams to notify regulators and patients.",
            },
            {
                "organization": "AI-powered search startup",
                "scenario": "Bots issued high-cost queries to inflate competitor expenses.",
                "finding": "Usage quotas and anomaly detection were missing.",
                "response": "The startup implemented per-tenant quotas, caching, cost dashboards, and published transparency reports detailing protections for customers.",
            },
        ],
        "case_outro": """
Embedding security requires vigilance. Continually iterate on controls as attackers evolve tactics, and integrate case-study findings into partner reviews, customer messaging, and engineering training.
""",
        "mnemonic": {
            "title": "VECTOR SAFE",
            "items": [
                {"letter": "V", "phrase": "Validate inputs", "detail": "Screen documents before embedding."},
                {"letter": "E", "phrase": "Encrypt storage", "detail": "Protect vector databases with TLS and encryption."},
                {"letter": "C", "phrase": "Control access", "detail": "Use RBAC and network segmentation."},
                {"letter": "T", "phrase": "Track drift", "detail": "Monitor embedding changes over time."},
                {"letter": "O", "phrase": "Observe queries", "detail": "Analyze usage patterns and anomalies."},
                {"letter": "R", "phrase": "Respond fast", "detail": "Quarantine poisoned vectors and restore from clean snapshots."},
                {"letter": "S", "phrase": "Score risk", "detail": "Apply semantic firewalls and query risk scoring."},
                {"letter": "A", "phrase": "Audit regularly", "detail": "Review configs, access logs, and metrics with stakeholders."},
                {"letter": "F", "phrase": "Fuzz pipelines", "detail": "Red-team ingestion and retrieval.",},
                {"letter": "E", "phrase": "Educate teams", "detail": "Train data engineers and analysts on embedding risks."},
            ],
        },
        "pitfall_intro": """
Avoid these missteps when managing embeddings. Revisit them during architectural reviews and partner assessments to stay ahead of attackers.
""",
        "pitfalls": [
            {"title": "Treating embeddings as harmless", "detail": "They can leak sensitive information or enable collisions. Classify them as sensitive data."},
            {"title": "No validation", "detail": "Unvetted data enters pipelines, opening doors to poisoning. Require provenance, rate limiting, and human approval for risky sources."},
            {"title": "Weak access controls", "detail": "Open vector databases invite theft and tampering. Enforce RBAC, encryption, and network segmentation."},
            {"title": "Ignored metrics", "detail": "Without dashboards, drift and abuse go unnoticed. Instrument analytics and assign owners to investigate anomalies."},
            {"title": "Static defenses", "detail": "Attackers iterate quickly; controls must evolve. Feed red-team findings into backlog and budget planning."},
            {"title": "Siloed ownership", "detail": "Embedding security fails when data, ML, and security teams do not collaborate. Establish shared rituals and governance councils."},
        ],
        "takeaway_intro": """
Focus on these steps to secure embedding pipelines now. Assign owners, timelines, and success metrics so progress survives roadmap pressures.
""",
        "takeaways": [
            {"title": "Deploy ingestion validation", "detail": "Introduce automated checks before embedding."},
            {"title": "Harden vector databases", "detail": "Enable TLS, RBAC, and encryption; restrict network access."},
            {"title": "Launch semantic firewalls", "detail": "Score queries and block suspicious requests."},
            {"title": "Instrument metrics dashboards", "detail": "Track drift, collisions, and cost anomalies."},
            {"title": "Plan incident response", "detail": "Document how to quarantine vectors and notify stakeholders."},
            {"title": "Schedule red-team drills", "detail": "Test poisoning, collisions, and denial-of-wallet scenarios regularly."},
            {"title": "Audit partner telemetry", "detail": "Review vendor logs, attestations, and remediation plans quarterly."},
            {"title": "Publish transparency updates", "detail": "Share search quality and security metrics with executives and customers."},
        ],
        "takeaway_close": """
Embedding security protects the intelligence layer that powers modern LLM applications. Invest now to prevent silent failures later. Celebrate incremental wins and share lessons across product lines to keep momentum high.
""",
        "reflection_questions": [
            "What validation exists before content enters embedding pipelines?",
            "How is access to vector databases controlled and audited?",
            "Which metrics alert you to collisions, drift, or query abuse?",
            "How quickly can you recover from a poisoned embedding incident?",
            "Which partners contribute embeddings, and how do they prove adherence to your security requirements?",
            "What fallback experience will users see if retrieval confidence drops below acceptable thresholds?",
            "How will you document and share embedding incidents so lessons inform future architecture decisions?",
        ],
        "mindset": [
            """
View embeddings as sensitive assets. Curiosity, rigor, and collaboration keep them trustworthy.
""",
            """
Share success stories when metrics catch anomalies. Celebrate vigilance to maintain engagement.
""",
            """
Create feedback loops. Encourage engineers to surface issues and iterate on controls.
""",
            """
Stay informed. Follow research on embedding attacks and update defenses accordingly.
""",
            """
Promote shared ownership. Bring data, ML, security, and product leaders into the same forums so decisions balance innovation and risk.
""",
            """
Practice resilience thinking. Assume partial failures will occur and plan graceful degradation that protects customers while teams remediate.
""",
            """
Measure what matters. Tie embedding security metrics to customer satisfaction, revenue protection, and regulatory commitments so investment conversations stay grounded in business value.
""",
        ],
    },
    {
        "lesson_id": "e7526439-ec54-4156-8ae6-442e9070adfd",
        "slug": "owasp_llm09_misinformation_and_hallucination",
        "title": "OWASP LLM09: Misinformation and Hallucination",
        "subtitle": "Designing trustworthy outputs under uncertainty",
        "difficulty": 2,
        "estimated_time": 115,
        "order_index": 12,
        "prerequisites": [],
        "concepts": [
            "hallucination mitigation",
            "fact-checking",
            "confidence scoring",
            "source attribution",
            "feedback loops",
            "content governance",
        ],
        "learning_objectives": [
            "Explain why hallucinations occur and how misinformation spreads through LLM workflows.",
            "Architect pipelines that validate, attribute, and contextualize LLM responses.",
            "Implement user experience patterns that communicate uncertainty and encourage verification.",
            "Leverage telemetry and feedback to continuously reduce misinformation risk.",
            "Coordinate legal, PR, and product teams when misinformation incidents occur.",
        ],
        "post_assessment": [
            {
                "question": "Which practice reduces hallucination impact?",
                "options": [
                    "Serving answers without citations or disclaimers.",
                    "Validating responses against authoritative sources and providing citations.",
                    "Disabling feedback collection to streamline UX.",
                    "Ignoring user reports of incorrect answers.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Why should agents communicate uncertainty?",
                "options": [
                    "Users enjoy vague responses.",
                    "Transparency builds trust and prompts users to double-check critical decisions.",
                    "It increases hallucinations.",
                    "Uncertainty messaging is legally prohibited.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Which signal helps detect misinformation?",
                "options": [
                    "GPU temperature.",
                    "User feedback trends, citation coverage, and contradiction detection.",
                    "Server uptime alone.",
                    "Number of emojis in a response.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "What is a key step after a misinformation incident?",
                "options": [
                    "Ignore it and hope no one notices.",
                    "Publish corrections, notify stakeholders, update prompts and guardrails, and analyze root causes.",
                    "Delete all logs to avoid liability.",
                    "Blame users for misunderstanding.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "LLMs generate confident but incorrect statements that mislead users or conflict with policy",
            "business_context": "assistants support customer service, healthcare triage, financial advice, and internal analytics",
            "attacker_motivation": "amplify misinformation, damage reputation, or manipulate decisions",
            "human_factor": "users trust AI tone, skip verification, and share answers widely",
            "control_challenge": "balancing fast responses with rigorous validation and attribution",
            "innovation_balance": "enabling creativity while surfacing uncertainty and inviting human judgment",
            "closing_emphasis": "trustworthy AI requires transparency, validation, and rapid correction",
        },
        "short_name": "Misinformation and Hallucination",
        "llm_code": "OWASP LLM09",
        "attack_vectors": [
            {
                "name": "Hallucinated facts",
                "detail": "models fabricate statistics, regulations, or citations when knowledge is incomplete",
                "detail_secondary": "confident tone misleads users into believing false information",
                "impact": "customers make poor decisions, and brand credibility suffers",
                "impact_secondary": "support teams handle escalations and corrections",
                "detection": "automatic fact-checking, contradiction detection, and user feedback analysis",
                "telemetry": "track citation coverage, feedback tags, and content categories",
                "mitigation": "provide citations, disclaimers, and fallback to human experts for critical topics",
                "lesson_alignment": "OWASP principle for output control",
                "mitigation_reinforcement": "run red-team scenarios probing complex, regulated domains",
            },
            {
                "name": "Misinformation amplification",
                "detail": "malicious prompts or training data spread rumors or propaganda",
                "detail_secondary": "agents share viral misinformation without verifying sources",
                "impact": "legal exposure, regulatory fines, and public backlash",
                "impact_secondary": "platforms may suspend integrations",
                "detection": "monitor trending topics, track sentiment, and compare against authoritative datasets",
                "telemetry": "log external references, social signals, and policy flags",
                "mitigation": "curate training data, integrate fact-check APIs, and throttle responses during emerging incidents",
                "lesson_alignment": "OWASP emphasis on content governance",
                "mitigation_reinforcement": "simulate misinformation outbreaks with crisis communication teams",
            },
            {
                "name": "Citation spoofing",
                "detail": "models cite legitimate-looking sources that do not exist or misrepresent content",
                "detail_secondary": "users rarely verify citations when format appears authoritative",
                "impact": "trust erodes when citations fail verification",
                "impact_secondary": "support teams waste time investigating fabricated references",
                "detection": "validate links, DOIs, and metadata against known sources",
                "telemetry": "store citation validity metrics and failure reasons",
                "mitigation": "use retrieval-based citations or link to curated knowledge graphs",
                "lesson_alignment": "OWASP recommendation for verifiable outputs",
                "mitigation_reinforcement": "establish quality review programs sampling citations weekly",
            },
            {
                "name": "Feedback manipulation",
                "detail": "attackers flood positive feedback on inaccurate answers to preserve misinformation",
                "detail_secondary": "bots skew RLHF signals or reputation scores",
                "impact": "hallucinations persist and appear endorsed",
                "impact_secondary": "investigation is harder when feedback metrics look healthy",
                "detection": "monitor feedback provenance, rate of change, and reviewer diversity",
                "telemetry": "collect device fingerprints, IPs, and session metadata for feedback",
                "mitigation": "weight trusted reviewers, require verification for sensitive topics, and audit feedback loops",
                "lesson_alignment": "OWASP guidance on human oversight",
                "mitigation_reinforcement": "perform adversarial feedback drills and tune weightings",
            },
        ],
        "impact_overview": """
Misinformation incidents damage trust, create legal exposure, and overwhelm support teams. Customers demand accuracy, regulators scrutinize claims, and executives expect transparent remediation plans.
""",
        "impact_zones": [
            {
                "area": "Customer decision-making",
                "detail": "Incorrect guidance influences financial, health, and legal choices.",
            },
            {
                "area": "Brand reputation",
                "detail": "Viral screenshots of false answers spread quickly, attracting negative media.",
            },
            {
                "area": "Compliance",
                "detail": "Regulations require truthful, non-misleading information and clear disclaimers.",
            },
            {
                "area": "Support operations",
                "detail": "Teams handle corrections, refunds, and crisis communications.",
            },
        ],
        "detection_intro": """
Blend automated checks with human review. Fact-check responses, monitor sentiment and feedback, and maintain rapid escalation paths for trending misinformation.
""",
        "detection_focus": [
            {
                "name": "Citation coverage",
                "detail": "Track what percentage of responses include verifiable sources.",
                "correlation": "Highlight topics with low coverage and high risk.",
                "forensics": "Store citation metadata and verification status.",
            },
            {
                "name": "Contradiction detection",
                "detail": "Use models to flag outputs conflicting with curated knowledge bases.",
                "correlation": "Compare with user feedback tags and incident reports.",
                "forensics": "Log conflicting statements and context for analysts.",
            },
            {
                "name": "Feedback sentiment",
                "detail": "Analyze trends in thumbs-down, corrections, and flagged responses.",
                "correlation": "Align with release cycles, policy changes, or new data sources.",
                "forensics": "Capture user comments and follow-up actions.",
            },
            {
                "name": "Topic risk dashboards",
                "detail": "Identify domains (health, finance) requiring heightened scrutiny.",
                "correlation": "Tie to legal requirements and business impact.",
                "forensics": "Maintain audit trails for regulators and executives.",
            },
        ],
        "guardrail_intro": """
Prevent and mitigate misinformation by layering retrieval, validation, disclaimers, and human oversight. Align output controls with policy and brand standards.
""",
        "guardrail_layers": [
            {
                "name": "Grounded retrieval",
                "detail": "Prioritize answers sourced from vetted knowledge bases and document citations.",
                "conditions": "high-risk topics",
                "practice": "refresh knowledge, monitor source quality, and expire stale content",
                "alignment": "responsible AI and compliance requirements",
            },
            {
                "name": "Uncertainty UX",
                "detail": "Display confidence indicators, disclaimers, and paths to human assistance.",
                "conditions": "responses with low confidence or limited citations",
                "practice": "test messaging with legal and UX to balance clarity and reassurance",
                "alignment": "customer experience and regulatory guidance",
            },
            {
                "name": "Feedback governance",
                "detail": "Curate feedback pipelines, weight trusted reviewers, and audit loops.",
                "conditions": "ongoing",
                "practice": "report metrics to stakeholders and act on trends quickly",
                "alignment": "quality management systems",
            },
            {
                "name": "Incident response playbooks",
                "detail": "Define detection triggers, communication templates, and remediation steps for misinformation events.",
                "conditions": "activated when misinformation is suspected",
                "practice": "rehearse with PR, legal, and support teams",
                "alignment": "crisis management and OWASP governance",
            },
        ],
        "operational_story": """
Trustworthy outputs require collaboration. Product managers define guardrails, legal ensures compliance, PR prepares messaging, and security monitors signals. Together they maintain credibility.
""",
        "video": {
            "title": "Battling Hallucinations in Production",
            "url": "https://www.youtube.com/watch?v=NB6fYiSbdls",
            "description": "Practitioners share lessons from deploying fact-checked assistants with uncertainty communication and rapid correction workflows.",
            "focus_points": [
                "Techniques to ground responses in evidence.",
                "Metrics and dashboards for hallucination monitoring.",
                "UX strategies for confidence messaging.",
                "Cross-functional response to misinformation incidents.",
            ],
        },
        "diagram": {
            "intro": "Misinformation defenses integrate retrieval, validation, and feedback:",
            "ascii": """
  Knowledge Base -> Retrieval -> LLM -> Validation -> UX & Feedback -> Monitoring
         |             |           |         |            |                 |
   Source Ratings   Context IDs  Citations  Fact Checks  Confidence UI   Incident Alerts
""",
            "explanation": "Each stage enforces accuracy. Retrieval provides context IDs, validation checks facts, UX communicates uncertainty, feedback feeds monitoring, and alerts trigger response teams.",
            "callouts": [
                "Knowledge bases carry freshness and trust scores.",
                "Validation can include external APIs or internal rule engines.",
                "UX patterns allow users to request human help quickly.",
                "Monitoring aggregates metrics to inform leadership.",
            ],
        },
        "lab_setup": {
            "overview": """
Run a misinformation readiness drill. Teams will configure grounding, validation, and response workflows, then simulate incidents.
""",
            "objective": "Ensure outputs remain trustworthy and that incidents are handled swiftly and transparently.",
            "steps": [
                "Configure retrieval pipelines with authoritative sources and metadata.",
                "Implement automatic citation validation and contradiction detection.",
                "Design UX messaging for uncertainty, disclaimers, and human escalation.",
                "Collect user feedback with provenance and weightings.",
                "Simulate hallucinated responses and monitor detection alerts.",
                "Activate incident response, publish corrections, and document improvements.",
                "Gather user and stakeholder feedback on guardrail effectiveness.",
                "Update policies, prompts, and dashboards based on findings.",
            ],
            "validation": "The drill succeeds when hallucinations are caught, users receive transparent messaging, and teams respond within defined SLAs.",
        },
        "code_exercise": {
            "overview": """
Implement a simple citation checker that verifies URLs referenced by the model.
""",
            "language": "python",
            "snippet": """
import requests

def validate_citations(citations: list[str]) -> dict[str, bool]:
    results = {}
    for url in citations:
        try:
            response = requests.head(url, timeout=3)
            results[url] = response.status_code == 200
        except requests.RequestException:
            results[url] = False
    return results
""",
            "explanation": "Citation checkers provide quick validation and feed analytics on coverage. Production systems should cache results, inspect content, and integrate with knowledge graphs.",
            "callouts": [
                "Rate-limit and cache validation requests to protect APIs.",
                "Log failures with reasons and retry policies.",
                "Integrate with retrieval metadata to match citations to documents.",
                "Alert analysts when high-risk topics fail validation.",
                "Provide users with fallback messaging when citations cannot be verified.",
            ],
        },
        "case_intro": """
Misinformation incidents highlight the need for proactive guardrails. Learn from these examples.
""",
        "case_studies": [
            {
                "organization": "Healthcare Q&A bot",
                "scenario": "The assistant recommended unapproved treatments without disclaimers.",
                "finding": "Responses lacked grounding and human review.",
                "response": "The provider integrated medical knowledge bases, added disclaimers, and required clinician approval for high-risk topics.",
            },
            {
                "organization": "Financial advisory assistant",
                "scenario": "Hallucinated stock predictions went viral on social media.",
                "finding": "No monitoring existed for trending topics or misinformation.",
                "response": "The company introduced sentiment monitoring, rapid response workflows, and public correction channels.",
            },
            {
                "organization": "Internal policy assistant",
                "scenario": "Employees relied on hallucinated compliance guidance, leading to audit findings.",
                "finding": "Prompts lacked citations and updates when policies changed.",
                "response": "The organization linked the assistant to policy repositories, enforced citations, and scheduled policy refresh reminders.",
            },
        ],
        "case_outro": """
Trust grows when teams acknowledge mistakes, correct them quickly, and share improvements transparently.
""",
        "mnemonic": {
            "title": "TRUTH BUILDS",
            "items": [
                {"letter": "T", "phrase": "Tie to sources", "detail": "Ground responses in verified data."},
                {"letter": "R", "phrase": "Reveal uncertainty", "detail": "Communicate confidence and limitations."},
                {"letter": "U", "phrase": "Use validation", "detail": "Automate fact-checks and contradictions."},
                {"letter": "T", "phrase": "Track feedback", "detail": "Monitor sentiment and corrections."},
                {"letter": "H", "phrase": "Handle incidents", "detail": "Deploy response playbooks swiftly."},
                {"letter": "B", "phrase": "Balance automation", "detail": "Escalate high-risk topics to humans."},
                {"letter": "U", "phrase": "Update knowledge", "detail": "Refresh sources and prompts regularly."},
                {"letter": "I", "phrase": "Inform stakeholders", "detail": "Share metrics and incidents transparently."},
                {"letter": "L", "phrase": "Leverage UX", "detail": "Design interfaces that encourage verification."},
                {"letter": "D", "phrase": "Document governance", "detail": "Maintain policies and audit trails."},
                {"letter": "S", "phrase": "Share learnings", "detail": "Publish retrospectives and training updates."},
            ],
        },
        "pitfall_intro": """
Avoid recurring mistakes that allow misinformation to persist.
""",
        "pitfalls": [
            {"title": "No grounding", "detail": "LLMs answer without authoritative context."},
            {"title": "Opaque messaging", "detail": "Users are unaware of uncertainty or limitations."},
            {"title": "Ignored feedback", "detail": "Reports pile up with no action."},
            {"title": "Stale policies", "detail": "Prompts and knowledge bases lag behind real-world updates."},
            {"title": "Slow corrections", "detail": "Incidents linger due to unclear ownership."},
            {"title": "Overreliance on automation", "detail": "Critical decisions lack human review."},
        ],
        "takeaway_intro": """
Turn lessons into action by prioritizing misinformation defenses now.
""",
        "takeaways": [
            {"title": "Implement citation validation", "detail": "Automate checks and report coverage."},
            {"title": "Design uncertainty messaging", "detail": "Collaborate with UX and legal to craft transparent responses."},
            {"title": "Launch misinformation monitoring", "detail": "Combine sentiment, feedback, and content analytics."},
            {"title": "Formalize response playbooks", "detail": "Define steps for correction, communication, and remediation."},
            {"title": "Refresh knowledge sources", "detail": "Schedule updates and audits for high-risk domains."},
            {"title": "Educate teams", "detail": "Train staff on spotting and reporting misinformation."},
        ],
        "takeaway_close": """
Trustworthy AI is a journey. Continual refinement and transparency build long-term confidence.
""",
        "reflection_questions": [
            "Which topics in your product carry the highest misinformation risk?",
            "How will you communicate uncertainty and corrections to users?",
            "What telemetry proves that guardrails reduce hallucinations?",
            "Who owns misinformation response end-to-end?",
        ],
        "mindset": [
            """
Adopt a learning mindset. Every feedback signal is an opportunity to improve accuracy.
""",
            """
Practice humility. Encourage teams to acknowledge uncertainty and invite user input.
""",
            """
Celebrate corrections. Publicly thank teams who detect and fix misinformation quickly.
""",
            """
Stay vigilant. Monitor emerging narratives and update guardrails proactively.
""",
        ],
    },
    {
        "lesson_id": "3e1bf53f-235a-4d93-9f49-fae5b391f9eb",
        "slug": "owasp_llm10_unbounded_consumption",
        "title": "OWASP LLM10: Unbounded Consumption",
        "subtitle": "Controlling cost, scale, and environmental impact",
        "difficulty": 2,
        "estimated_time": 110,
        "order_index": 13,
        "prerequisites": [],
        "concepts": [
            "rate limiting",
            "budget governance",
            "usage analytics",
            "capacity planning",
            "environmental sustainability",
            "denial-of-wallet defense",
        ],
        "learning_objectives": [
            "Explain why unbounded LLM usage threatens cost, reliability, and sustainability.",
            "Design quotas, throttling, and budgeting mechanisms aligned with business priorities.",
            "Monitor usage patterns to detect abuse, runaway agents, or unexpected demand spikes.",
            "Coordinate finance, operations, and engineering on cost transparency and mitigation.",
            "Respond to denial-of-wallet attacks and communicate capacity constraints to stakeholders.",
        ],
        "post_assessment": [
            {
                "question": "Which control helps prevent denial-of-wallet attacks?",
                "options": [
                    "Unlimited access for all users.",
                    "Per-tenant quotas, rate limits, and cost alerts.",
                    "Removing monitoring to reduce overhead.",
                    "Only manual reviews of usage once a year.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "Why should finance teams collaborate on LLM deployments?",
                "options": [
                    "Costs are negligible.",
                    "They forecast budgets, evaluate ROI, and enforce spend governance.",
                    "Finance has no role in AI operations.",
                    "Finance should approve every single API call manually.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "What telemetry surfaces runaway usage?",
                "options": [
                    "GPU serial numbers.",
                    "Per-tenant token counts, latency, cost per request, and agent orchestration graphs.",
                    "Number of UI themes.",
                    "Length of commit messages.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
            {
                "question": "How should teams respond to unexpected usage spikes?",
                "options": [
                    "Disable all alerts.",
                    "Activate throttling, notify stakeholders, analyze root cause, and adjust capacity or pricing.",
                    "Ignore spikes until invoices arrive.",
                    "Permanently ban all users.",
                ],
                "correct_answer": 1,
                "difficulty": 2,
                "type": "multiple_choice",
            },
        ],
        "story": {
            "threat_summary": "unmonitored or excessive LLM usage drives unexpected costs, outages, or carbon footprint",
            "business_context": "LLM services integrate with customer apps, automation workflows, and agent ecosystems",
            "attacker_motivation": "drain resources, cause financial stress, or degrade availability",
            "human_factor": "teams launch pilots without quotas or budget visibility",
            "control_challenge": "balancing innovation speed with fiscal responsibility and sustainability",
            "innovation_balance": "support experimentation while enforcing guardrails that prevent runaway consumption",
            "closing_emphasis": "usage governance is essential to keep AI programs viable",
        },
        "short_name": "Unbounded Consumption",
        "llm_code": "OWASP LLM10",
        "attack_vectors": [
            {
                "name": "Denial-of-wallet attacks",
                "detail": "bots or attackers flood endpoints with expensive prompts or tool invocations",
                "detail_secondary": "requests may mimic normal traffic to bypass naive filters",
                "impact": "cloud bills spike, budgets blow out, and services throttle legitimate users",
                "impact_secondary": "finance and security scramble to identify culprits",
                "detection": "monitor per-tenant spend, request velocity, and anomaly scores",
                "telemetry": "collect cost per request, authentication context, and geo-IP",
                "mitigation": "apply quotas, rate limits, and automatic throttling with alerts",
                "lesson_alignment": "OWASP guidance on resource governance",
                "mitigation_reinforcement": "run load tests and red-team scenarios targeting cost controls",
            },
            {
                "name": "Runaway agents",
                "detail": "autonomous workflows loop or trigger cascades of prompts and tool calls",
                "detail_secondary": "lack of circuit breakers or budgets allows loops to continue",
                "impact": "capacity is consumed, delays mount, and costs accumulate",
                "impact_secondary": "customer SLAs degrade due to queue backlogs",
                "detection": "track agent orchestration graphs, step counts, and approval rates",
                "telemetry": "log session IDs, tool invocations, and approvals",
                "mitigation": "set iteration limits, require approvals, and implement watchdog timers",
                "lesson_alignment": "OWASP excessive agency control",
                "mitigation_reinforcement": "test watchdog alerts and emergency stop procedures",
            },
            {
                "name": "Shadow usage",
                "detail": "teams integrate APIs without governance, bypassing quotas and cost centers",
                "detail_secondary": "untracked projects accumulate spend before finance notices",
                "impact": "budget overruns and compliance issues with vendor contracts",
                "impact_secondary": "lack of visibility prevents forecasting",
                "detection": "analyze network logs, procurement records, and cost exports for anomalies",
                "telemetry": "centralize usage data across org and tag by business unit",
                "mitigation": "enforce onboarding checklists, cost tagging, and quarterly reviews",
                "lesson_alignment": "OWASP governance and budgeting",
                "mitigation_reinforcement": "conduct cost hygiene audits with finance and procurement",
            },
            {
                "name": "Inefficient prompts and models",
                "detail": "developers use large models or verbose prompts for simple tasks",
                "detail_secondary": "lack of optimization increases tokens and latency",
                "impact": "infrastructure costs rise and carbon footprint expands",
                "impact_secondary": "user experience suffers due to latency",
                "detection": "track token length distribution, latency, and cache hit rates",
                "telemetry": "log prompt sizes, model versions, and response times",
                "mitigation": "optimize prompts, choose smaller models, and cache frequent responses",
                "lesson_alignment": "OWASP efficiency and sustainability guidance",
                "mitigation_reinforcement": "establish prompt review rituals focusing on efficiency",
            },
        ],
        "impact_overview": """
Unbounded consumption converts AI innovation into financial and operational risk. Invoices surprise finance teams, outages impact customers, and sustainability goals slip when resources are wasted.
""",
        "impact_zones": [
            {
                "area": "Financial performance",
                "detail": "Cloud costs exceed budgets and erode ROI.",
            },
            {
                "area": "Reliability",
                "detail": "Resource saturation causes latency, rate limiting, or downtime.",
            },
            {
                "area": "Sustainability",
                "detail": "Inefficient usage increases energy consumption and carbon footprint.",
            },
            {
                "area": "Customer trust",
                "detail": "Throttling or outages frustrate users and partners.",
            },
        ],
        "detection_intro": """
Monitor consumption in real time. Combine cost analytics, rate limiting metrics, and anomaly detection to surface runaway usage before invoices or outages occur.
""",
        "detection_focus": [
            {
                "name": "Cost dashboards",
                "detail": "Track spend per tenant, product, and region with budget thresholds.",
                "correlation": "Align with business initiatives and marketing campaigns.",
                "forensics": "Provide drill-down views for finance and engineering investigations.",
            },
            {
                "name": "Rate limit telemetry",
                "detail": "Monitor throttle events, rejection rates, and retries.",
                "correlation": "Identify tenants exceeding quotas or experiencing abuse.",
                "forensics": "Log request metadata and client IDs.",
            },
            {
                "name": "Agent loop detection",
                "detail": "Analyze orchestration graphs for excessive iterations or repeated tool calls.",
                "correlation": "Tie to approval logs and capability registries.",
                "forensics": "Capture execution traces and context.",
            },
            {
                "name": "Sustainability metrics",
                "detail": "Report energy usage, carbon estimates, and optimization opportunities.",
                "correlation": "Align with corporate sustainability goals.",
                "forensics": "Provide reports for ESG disclosures and leadership dashboards.",
            },
        ],
        "guardrail_intro": """
Guard consumption using policy, automation, and transparency. Budgets and quotas empower teams to innovate responsibly.
""",
        "guardrail_layers": [
            {
                "name": "Quota and tiering program",
                "detail": "Define per-tenant limits, burst allowances, and pricing tiers.",
                "conditions": "customer-facing APIs and internal agents",
                "practice": "review annually with finance and product",
                "alignment": "go-to-market strategy and cost governance",
            },
            {
                "name": "Automated throttling and circuit breakers",
                "detail": "Enforce rate limits, concurrency controls, and emergency kill switches.",
                "conditions": "during runtime",
                "practice": "test regularly and document fallback experiences",
                "alignment": "reliability engineering standards",
            },
            {
                "name": "Cost transparency dashboards",
                "detail": "Share usage and spend with product owners, finance, and leadership.",
                "conditions": "continuous",
                "practice": "include forecasts, anomalies, and sustainability metrics",
                "alignment": "financial planning and ESG reporting",
            },
            {
                "name": "Optimization playbooks",
                "detail": "Provide guidance on prompt efficiency, caching, and model selection.",
                "conditions": "development and operations",
                "practice": "incorporate into engineering reviews and training",
                "alignment": "DevOps excellence",
            },
        ],
        "operational_story": """
Consumption governance crosses departments. Product managers forecast demand, finance tracks budgets, operations monitors metrics, and sustainability teams evaluate environmental impact. Collaboration keeps usage aligned with strategy.
""",
        "video": {
            "title": "Managing LLM Cost and Scale",
            "url": "https://www.youtube.com/watch?v=8G5bA9g5fWM",
            "description": "Finance and engineering leaders discuss quota design, cost dashboards, and denial-of-wallet defenses.",
            "focus_points": [
                "How quotas and burst policies were negotiated with product teams.",
                "Telemetry that surfaced runaway usage.",
                "Collaboration models between engineering, finance, and sustainability.",
                "Lessons from denial-of-wallet simulations.",
            ],
        },
        "diagram": {
            "intro": "Consumption governance pipeline:",
            "ascii": """
 Requests -> Quotas -> Runtime Enforcement -> Cost Analytics -> Stakeholder Dashboards
      |           |             |                    |                      |
 Authentication  Tier Rules   Throttling         Budgets               Finance/Eng Sync
""",
            "explanation": "Quotas categorize requests, runtime enforcement applies limits, analytics track costs, and dashboards align stakeholders.",
            "callouts": [
                "Authentication maps usage to tenants and cost centers.",
                "Tier rules define burst allowances and SLAs.",
                "Throttling triggers friendly messaging and fallback options.",
                "Dashboards support forecast meetings and incident response.",
            ],
        },
        "lab_setup": {
            "overview": """
Run a cost governance workshop. Teams will configure quotas, throttling, dashboards, and incident response for a simulated spike.
""",
            "objective": "Verify that controls prevent runaway consumption while maintaining user experience.",
            "steps": [
                "Define tiers, quotas, and burst policies for sample tenants.",
                "Implement throttling and circuit breakers in staging.",
                "Set up cost dashboards with alerts for spend anomalies.",
                "Simulate denial-of-wallet and runaway agent scenarios.",
                "Trigger response playbooks, notifying finance, product, and support.",
                "Measure user impact and adjust messaging for throttled requests.",
                "Review sustainability metrics and identify optimization opportunities.",
                "Document decisions, action items, and follow-up reviews.",
            ],
            "validation": "Success occurs when spikes are contained, stakeholders receive timely information, and optimization ideas emerge.",
        },
        "code_exercise": {
            "overview": """
Implement a simple quota checker that enforces per-tenant limits.
""",
            "language": "python",
            "snippet": """
QUOTAS = {"free": 100_000, "pro": 1_000_000}

def check_quota(plan: str, tokens_used: int, tokens_requested: int) -> bool:
    limit = QUOTAS.get(plan)
    if limit is None:
        raise ValueError("Unknown plan")
    if tokens_used + tokens_requested > limit:
        raise PermissionError("Quota exceeded")
    return True
""",
            "explanation": "Quota checks form the foundation of consumption control. Production systems would integrate with billing, dashboards, and throttling mechanisms.",
            "callouts": [
                "Store usage counters in reliable data stores and refresh frequently.",
                "Support grace periods and burst allowances with logging.",
                "Expose usage to customers via APIs or dashboards.",
                "Pair quotas with alerts sent to stakeholders before limits hit.",
                "Adjust quotas based on business value and sustainability goals.",
            ],
        },
        "case_intro": """
Consumption incidents reveal why governance matters. Study these stories to strengthen your controls.
""",
        "case_studies": [
            {
                "organization": "Gaming platform",
                "scenario": "A viral promotion caused a surge in AI-powered support chats, exhausting quotas and spiking costs.",
                "finding": "No burst policy or automated throttling existed.",
                "response": "The platform implemented tiered quotas, throttling, and cost alerts for marketing events.",
            },
            {
                "organization": "Enterprise SaaS vendor",
                "scenario": "A compromised API key triggered millions of requests overnight.",
                "finding": "Keys had unlimited access, and anomaly detection was absent.",
                "response": "The vendor enforced scoped keys, per-tenant limits, and security alerts feeding the SOC.",
            },
            {
                "organization": "Internal agent platform",
                "scenario": "Experimental agents looped through reports, consuming budget for analytics APIs.",
                "finding": "Iteration limits and budget guardrails were missing.",
                "response": "The team added watchdog timers, approval checkpoints, and cost dashboards for leadership.",
            },
        ],
        "case_outro": """
Usage discipline transforms AI from a liability into a sustainable advantage. Transparency and proactive controls keep innovation on track.
""",
        "mnemonic": {
            "title": "CONTROL COST",
            "items": [
                {"letter": "C", "phrase": "Cap usage", "detail": "Set quotas and burst limits."},
                {"letter": "O", "phrase": "Observe spend", "detail": "Monitor dashboards and alerts."},
                {"letter": "N", "phrase": "Notify finance", "detail": "Share reports and anomalies promptly."},
                {"letter": "T", "phrase": "Throttle abuse", "detail": "Enforce rate limits and circuit breakers."},
                {"letter": "R", "phrase": "Review agents", "detail": "Audit workflows for loops or inefficiencies."},
                {"letter": "O", "phrase": "Optimize prompts", "detail": "Trim tokens and select efficient models."},
                {"letter": "L", "phrase": "Leverage caching", "detail": "Reuse responses when appropriate."},
                {"letter": "C", "phrase": "Calculate impact", "detail": "Include sustainability and ROI metrics."},
                {"letter": "O", "phrase": "Own incident response", "detail": "Prepare playbooks for cost spikes."},
                {"letter": "S", "phrase": "Share accountability", "detail": "Align finance, engineering, and product on goals."},
                {"letter": "T", "phrase": "Train teams", "detail": "Educate stakeholders on usage hygiene."},
            ],
        },
        "pitfall_intro": """
Watch for these missteps when scaling LLM usage.
""",
        "pitfalls": [
            {"title": "Unlimited keys", "detail": "Credentials without quotas invite abuse."},
            {"title": "Opaque billing", "detail": "Teams cannot manage what they cannot see."},
            {"title": "Delayed alerts", "detail": "Notifications arriving post-invoice limit options."},
            {"title": "No sustainability plan", "detail": "Carbon costs rise without efficiency efforts."},
            {"title": "Ignoring partner usage", "detail": "Integrations can consume large amounts of capacity."},
            {"title": "Absent playbooks", "detail": "Teams improvise during spikes, prolonging impact."},
        ],
        "takeaway_intro": """
Prioritize these actions to keep consumption sustainable.
""",
        "takeaways": [
            {"title": "Audit credentials", "detail": "Scope keys, enforce quotas, and rotate regularly."},
            {"title": "Launch cost dashboards", "detail": "Expose usage to product, finance, and leadership."},
            {"title": "Simulate denial-of-wallet", "detail": "Test throttling and response playbooks."},
            {"title": "Optimize workloads", "detail": "Use prompt reviews, caching, and model selection to reduce tokens."},
            {"title": "Align sustainability", "detail": "Track energy metrics and partner with sustainability teams."},
            {"title": "Educate stakeholders", "detail": "Train teams on budgeting, quotas, and escalation paths."},
        ],
        "takeaway_close": """
Effective usage governance protects budgets, customers, and the planet. Make it part of your AI culture.
""",
        "reflection_questions": [
            "How are quotas and budgets defined for each tenant or project?",
            "What telemetry alerts you before costs exceed thresholds?",
            "How will you respond to denial-of-wallet attacks or runaway agents?",
            "How do usage decisions align with sustainability goals?",
        ],
        "mindset": [
            """
Treat usage as a shared resource. Stewardship keeps innovation affordable and resilient.
""",
            """
Celebrate optimization wins. Share stories where prompt tuning or caching reduced spend.
""",
            """
Encourage transparency. Make budgets and dashboards accessible so teams feel empowered to act.
""",
            """
Stay proactive. Anticipate demand spikes and plan capacity with finance and operations.
""",
        ],
    },
]


def build_lesson(lesson: Dict) -> Dict:
    return {
        "lesson_id": lesson["lesson_id"],
        "domain": "ai_security",
        "title": lesson["title"],
        "subtitle": lesson["subtitle"],
        "difficulty": lesson["difficulty"],
        "estimated_time": lesson["estimated_time"],
        "order_index": lesson["order_index"],
        "prerequisites": lesson.get("prerequisites", []),
        "concepts": lesson["concepts"],
        "learning_objectives": lesson["learning_objectives"],
        "post_assessment": lesson["post_assessment"],
        "jim_kwik_principles": JIM_KWIK,
        "content_blocks": build_content_blocks(lesson),
    }


def validate_content_length(lesson: Dict) -> None:
    text = " ".join(
        block["content"].get("text", "") for block in lesson["content_blocks"] if isinstance(block.get("content"), dict)
    )
    word_count = len(text.split())
    if not 4000 <= word_count <= 15000:
        raise ValueError(f"Lesson {lesson['title']} has {word_count} words; expected between 4000 and 15000.")


def main() -> None:
    output_dir = Path("content")
    output_dir.mkdir(exist_ok=True)
    for lesson in LESSON_INPUTS:
        data = build_lesson(lesson)
        validate_content_length(data)
        filename = output_dir / f"lesson_ai_security_{lesson['order_index']:02d}_{lesson['slug']}_RICH.json"
        with open(filename, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
        print(f"Wrote {filename}")


if __name__ == "__main__":
    main()
