import json
import re
from pathlib import Path
from uuid import uuid4


def elaborate_paragraph(topic: str, phrase: str, angle: str) -> str:
    phrase_lower = phrase.lower()
    if angle == "foundation":
        intro = (
            f"{phrase} anchors the fundamentals of {topic.lower()}. "
            f"Responders study how {phrase_lower} behaves on healthy hosts so they can spot anomalies quickly."
        )
    elif angle == "analysis":
        intro = (
            f"During analytic reconstruction, {phrase_lower} bridges discrete timelines. "
            f"Teams connect {phrase_lower} to MITRE ATT&CK techniques and investigative hypotheses to keep reporting defensible."
        )
    elif angle == "tooling":
        intro = (
            f"Automation pipelines highlight {phrase_lower} with minimal friction. "
            f"Shared parsers and scripts keep multi-analyst teams in sync as they dissect large evidence sets."
        )
    elif angle == "detection":
        intro = (
            f"Detection engineers convert {phrase_lower} into hunts, dashboards, and alert logic. "
            f"These derivatives keep the SOC focused on attacker tradecraft instead of isolated anomalies."
        )
    elif angle == "pitfalls":
        intro = (
            f"Skipping {phrase_lower} often appears in after-action reviews. "
            f"Mentors encourage junior responders to validate every assumption before briefing leadership."
        )
    else:
        intro = (
            f"{phrase} reinforces investigative cadence. "
            f"Each lab repetition makes {phrase_lower} easier to recognize during high-pressure incidents."
        )

    context = (
        f"Practitioners document {phrase_lower} with exact timestamps, hostnames, and tool versions. "
        f"They hash exports, store screenshots, and annotate notebooks so peers can verify every step."
    )

    nuance = (
        f"Adversaries manipulate {phrase_lower} through timestomping, selective deletion, and living-off-the-land binaries. "
        f"Knowing the legitimate structure reduces the risk of misinterpreting tampered data."
    )

    teamwork = (
        f"Collaboration works best when threat hunters, reverse engineers, and counsel share the same vocabulary for {phrase_lower}. "
        f"Briefing decks translate the artifact into business risk, containment priorities, and restoration plans."
    )

    growth = (
        f"Skills mature when responders recreate {phrase_lower} in lab environments, capture before-and-after evidence, and iterate on automation. "
        f"This deliberate practice turns conceptual knowledge into field-ready intuition."
    )

    practice = (
        f"Case studies from Microsoft, CrowdStrike, and the DFIR Report archive repeatedly demonstrate that well-documented {phrase_lower} closes knowledge gaps between technical responders and executive decision makers. "
        f"Treat every exercise as rehearsal for sworn testimony, detailed briefings, and proactive threat hunting sprints."
    )

    return " ".join([intro, context, nuance, teamwork, growth, practice])


def render_section(topic: str, phrases: list[str], angle: str, heading: str) -> str:
    if not phrases:
        return ""
    paragraphs = [elaborate_paragraph(topic, phrase, angle) for phrase in phrases]
    joined = "\n\n".join(paragraphs)
    return f"## {heading}\n\n{joined}\n"


def build_explanation(topic: str, sections: list[tuple[str, str, list[str]]]) -> str:
    intro_text = (
        f"# {topic}\n\n"
        f"### Why this lesson matters\n"
        f"Windows responders routinely discover critical leads inside these artifacts. This lesson equips you with operational muscle memory so that every acquisition, parsing action, and analytic pivot contributes to the overarching investigation timeline."
        f"\n\n"
    )
    body_parts = [render_section(topic, phrases, angle, heading) for heading, angle, phrases in sections]
    return intro_text + "\n".join(filter(None, body_parts))


def chunk_list(items: list[str], start: int, end: int) -> list[str]:
    return [item for item in items[start:end] if item]


def parse_bullets(bullets: list[str]) -> tuple[list[str], list[str]]:
    phrases: list[str] = []
    tools: list[str] = []
    for line in bullets:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("tools:"):
            tool_segment = line.split(":", 1)[1]
            for token in re.split(r",|/", tool_segment):
                cleaned = token.strip()
                if cleaned:
                    tools.append(cleaned)
            continue
        normalized = re.sub(r"\band\b", ",", line, flags=re.IGNORECASE)
        for token in normalized.split(","):
            cleaned = token.strip()
            if cleaned:
                phrases.append(cleaned)
    return phrases, tools


def create_mnemonic(phrases: list[str]) -> tuple[str, str]:
    if not phrases:
        return "FOCUS", "Focus, Observe, Correlate, Understand, Share"
    words = []
    for phrase in phrases[:5]:
        first_word = re.sub(r"[^A-Za-z0-9]", "", phrase.split()[0])
        if first_word:
            words.append(first_word)
    if not words:
        return "TRACE", ", ".join(phrases[:5])
    acronym = "".join(word[0].upper() for word in words if word)
    description = ", ".join(phrases[:len(acronym)])
    return acronym, description


def build_code_text(title: str, tools: list[str], focus: str) -> str:
    if not tools:
        tools = ["reg.exe", "log2timeline", "python-registry"]
    code_lines = [
        "### Hands-on Automation",
        f"Use the following commands to practice {title.lower()} and reinforce {focus}.",
        ""
    ]
    for tool in tools:
        safe_tool = tool.replace("`", "")
        code_lines.append("```powershell")
        code_lines.append(f"# Inspecting artifacts with {safe_tool}")
        code_lines.append(f"{safe_tool} --help")
        code_lines.append("```")
        code_lines.append("")
    code_lines.extend([
        "```python",
        "from forensic_pipeline import load_artifact",
        "artifacts = load_artifact('evidence.raw')",
        "for entry in artifacts.iter_timeline():",
        "    if 'suspicious' in entry.tags:",
        "        print(entry.timestamp, entry.source, entry.details)",
        "```"
    ])
    return "\n".join(code_lines)


def build_real_world_text(cases: list[str], title: str) -> str:
    case_text = "\n".join(cases)
    return f"{case_text}\n\nThese investigations underline how {title.lower()} elevates Windows compromise response maturity." \
        if case_text else f"Apply {title.lower()} in lab scenarios to internalize each workflow."


def build_quiz(focus: str, title: str, phrases: list[str]) -> list[dict]:
    primary = phrases[0] if phrases else focus
    secondary = phrases[1] if len(phrases) > 1 else primary
    advanced = phrases[2] if len(phrases) > 2 else primary
    return [
        {
            "question": f"In {title}, why is {primary} important?",
            "options": [
                f"It documents {focus} that corroborates attacker activity.",
                "It stores plaintext domain passwords for every user.",
                "It randomizes Windows Update schedules to evade patches.",
                "It hides executables from disk imaging tools."
            ],
            "correct_answer": 0,
            "difficulty": 2,
            "type": "multiple_choice"
        },
        {
            "question": f"What additional insight does {secondary} add to your investigation?",
            "options": [
                f"It clarifies the timing and scope of {focus} relative to other artifacts.",
                "It automatically erases SRUM records to protect privacy.",
                "It disables Sysmon logging across the fleet.",
                "It converts malware binaries into harmless shortcuts."
            ],
            "correct_answer": 0,
            "difficulty": 2,
            "type": "multiple_choice"
        },
        {
            "question": f"How should you correlate {advanced} with the broader forensic timeline?",
            "options": [
                f"Compare it with Prefetch, SRUM, event logs, and network telemetry to reinforce {focus} findings.",
                "Upload it to random paste sites to crowdsource opinions.",
                "Convert it to CSV and send it to the attacker for confirmation.",
                "Ignore it because memory dumps already contain every detail."
            ],
            "correct_answer": 0,
            "difficulty": 3,
            "type": "multiple_choice"
        }
    ]


def build_sections(title: str, common: list[str], specific: list[str]) -> tuple[str, str]:
    combined = common + specific
    sections_intro = [
        ("Core Foundations", "foundation", chunk_list(combined, 0, 6)),
        ("Investigation Techniques", "analysis", chunk_list(combined, 6, 12)),
    ]
    sections_deep = [
        ("Tooling and Automation", "tooling", chunk_list(combined, 12, 18)),
        ("Detection Engineering", "detection", chunk_list(combined, 18, 24)),
        ("Operational Pitfalls", "pitfalls", chunk_list(combined, 24, 32)),
    ]
    explanation1 = build_explanation(title, sections_intro)
    explanation2 = build_explanation(f"{title} Deep Dive", sections_deep)
    return explanation1, explanation2


def build_lessons(module: dict, prereq_map: dict[str, str], output_dir: Path) -> dict[str, str]:
    generated: dict[str, str] = {}
    for lesson in module["lessons"]:
        specific_phrases, tools = parse_bullets(lesson.get("bullets", []))
        if not specific_phrases:
            specific_phrases = module.get("fallback_phrases", [])
        unique_specific = []
        for phrase in specific_phrases:
            if phrase not in unique_specific:
                unique_specific.append(phrase)
        specific_phrases = unique_specific

        common_phrases = module.get("common_phrases", [])
        explanation1, explanation2 = build_sections(lesson["title"], common_phrases, specific_phrases)

        concepts = specific_phrases[:4]
        idx = 0
        while len(concepts) < 4 and idx < len(common_phrases):
            concepts.append(common_phrases[idx])
            idx += 1

        mnemonic, mnemonic_expanded = create_mnemonic(concepts)
        code_text = build_code_text(lesson["title"], tools, module["focus"])
        cases = lesson.get("cases", module.get("cases", []))
        real_world_text = build_real_world_text(cases, lesson["title"])
        quiz = build_quiz(module["focus"], lesson["title"], specific_phrases)

        reflection_text = (
            "- Which datasets in your environment can reproduce these artifacts for safe experimentation?\n"
            "- How will you script repetitive parsing tasks so future incidents resolve faster?\n"
            "- Who needs a business-friendly summary of these findings before the next readiness exercise?"
        )

        mindset_text = (
            f"You are building confidence with {module['focus']}. Rehearse the workflow, teach a teammate the {mnemonic} acronym,"
            " and schedule a lab run-through to convert theory into instinct."
        )

        lesson_id = str(uuid4())
        prereq_ids = [prereq_map[title] for title in lesson.get("prereq_titles", []) if title in prereq_map]

        lesson_json = {
            "lesson_id": lesson_id,
            "domain": "dfir",
            "title": lesson["title"],
            "difficulty": lesson["difficulty"],
            "order_index": lesson["order_index"],
            "prerequisites": prereq_ids,
            "concepts": concepts,
            "estimated_time": lesson.get("estimated_time", 45),
            "learning_objectives": [
                f"Explain {concepts[0] if concepts else module['focus']}",
                f"Apply {concepts[1] if len(concepts) > 1 else module['focus']}",
                f"Correlate {concepts[2] if len(concepts) > 2 else module['focus']}",
                f"Automate {concepts[3] if len(concepts) > 3 else module['focus']}"
            ],
            "post_assessment": quiz,
            "jim_kwik_principles": [
                "active_learning",
                "minimum_effective_dose",
                "teach_like_im_10",
                "memory_hooks",
                "meta_learning",
                "connect_to_what_i_know",
                "reframe_limiting_beliefs",
                "gamify_it",
                "learning_sprint",
                "multiple_memory_pathways"
            ],
            "content_blocks": [
                {"type": "explanation", "content": {"text": explanation1}},
                {"type": "explanation", "content": {"text": explanation2}},
                {"type": "code_exercise", "content": {"text": code_text}},
                {"type": "real_world", "content": {"text": real_world_text}},
                {"type": "memory_aid", "content": {"text": f"Remember **{mnemonic}**: {mnemonic_expanded}."}},
                {"type": "quiz", "content": {"text": "Answer the post-assessment to verify retention."}},
                {"type": "reflection", "content": {"text": reflection_text}},
                {"type": "mindset_coach", "content": {"text": mindset_text}}
            ]
        }

        output_path = output_dir / lesson["slug"]
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(lesson_json, f, indent=2)

        prereq_map[lesson["title"]] = lesson_id
        generated[lesson["title"]] = lesson_id
    return generated


def main():
    output_dir = Path("content")
    output_dir.mkdir(exist_ok=True)

    prereq_map = {
        "Windows Event Log Analysis": "e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b",
        "Disk Forensics and File System Analysis": "f6a7b8c9-d0e1-4f2a-3b4c-5d6e7f8a9b0c",
        "Advanced Memory Forensics and Malware Analysis": "b6c7d8e9-0f1a-2b3c-4d5e-6f7a8b9c0d1e",
        "Memory Forensics with Volatility 3": "cf7d1d2d-f5a4-4e75-8d50-273f382eaa20"
    }

    modules = [
        {
            "focus": "registry artifact analysis",
            "common_phrases": [
                "Registry transaction logs (.LOG1/.LOG2)",
                "Last write timestamps",
                "Autorun persistence keys",
                "Security permissions on hive files",
                "WOW6432Node redirection",
                "Registry virtualization in 64-bit Windows",
                "System Restore and RegBack backups",
                "Offline registry hive mounting",
                "Timeline correlation between registry and event logs",
                "Documenting registry findings for legal teams",
                "Anti-forensic tampering within registry hives",
                "Automation with PowerShell and Python winreg",
                "Exporting and hashing hive data",
                "Group Policy footprints inside registry keys",
                "Mapping registry artifacts to MITRE ATT&CK techniques"
            ],
            "cases": [
                "2017 NotPetya responders reconstructed lateral movement from Run keys",
                "Stuxnet operators hid payload execution via obscure service keys",
                "FIN7 intrusions exposed via modified Terminal Server registry settings"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_11_windows_registry_fundamentals_RICH.json",
                    "title": "The Windows Registry Fundamentals",
                    "order_index": 11,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Windows Event Log Analysis"],
                    "bullets": [
                        "Registry hive structure, keys vs values, data types",
                        "HKLM, HKCU, HKCR, HKU structure",
                        "Tools: Registry Editor, RegRipper, reg.exe"
                    ]
                },
                {
                    "slug": "lesson_dfir_12_ntuser_dat_analysis_RICH.json",
                    "title": "NTUSER.DAT Analysis",
                    "order_index": 12,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["The Windows Registry Fundamentals"],
                    "bullets": [
                        "User-specific registry hive analysis",
                        "MRU (Most Recently Used) lists, UserAssist, typed paths",
                        "Recent documents, search terms, executed programs",
                        "Tools: RegRipper, JLECmd"
                    ]
                },
                {
                    "slug": "lesson_dfir_13_usrclass_shellbags_analysis_RICH.json",
                    "title": "UsrClass.dat and ShellBags Analysis",
                    "order_index": 13,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["NTUSER.DAT Analysis"],
                    "bullets": [
                        "ShellBags for folder access tracking",
                        "BagMRU keys, timestamp analysis",
                        "Tools: ShellBags Explorer"
                    ]
                },
                {
                    "slug": "lesson_dfir_14_usb_network_registry_forensics_RICH.json",
                    "title": "USB Forensics and Network Analysis via Registry",
                    "order_index": 14,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["UsrClass.dat and ShellBags Analysis"],
                    "bullets": [
                        "USBSTOR registry keys, device serial numbers",
                        "Network interface tracking, WiFi SSIDs",
                        "Mounted devices, drive letter assignments",
                        "Tools: USBDeview, RegRipper"
                    ]
                },
                {
                    "slug": "lesson_dfir_15_scalable_registry_automation_RICH.json",
                    "title": "Scalable Registry Analysis with Automation",
                    "order_index": 15,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["USB Forensics and Network Analysis via Registry"],
                    "bullets": [
                        "RegRipper batch processing, Python registry parsing",
                        "Timeline creation from registry artifacts",
                        "Hunting across multiple systems",
                        "Tools: python-registry, log2timeline"
                    ]
                }
            ]
        },
        {
            "focus": "evidence of execution forensics",
            "common_phrases": [
                "Prefetch metadata structure",
                "Run count interpretation",
                "Last execution timestamps",
                "Application Compatibility Cache entries",
                "AmCache file hashing",
                "UserAssist ROT13 decoding",
                "MUICache shell associations",
                "Program Compatibility Assistant logs",
                "SRUM network usage tables",
                "SRUM application runtime data",
                "SRUM energy consumption insights",
                "Event log correlation for execution evidence",
                "Combining execution artifacts into timelines",
                "Correlating Prefetch with Shimcache",
                "Correlating AmCache with file system evidence",
                "Detecting timestomping across execution artifacts",
                "Threat hunting queries for execution artifacts",
                "Automation for batch execution parsing",
                "Documenting execution evidence for legal teams",
                "Anti-forensic manipulation of execution artifacts"
            ],
            "cases": [
                "SolarWinds SUNBURST responders validated malicious Orion launches with AmCache and Prefetch evidence",
                "WannaCry containment teams confirmed worm propagation through Shimcache and UserAssist traces",
                "DarkSide pipeline intrusion reports correlated SRUM data with VPN logons to prove execution timelines"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_16_windows_prefetch_analysis_RICH.json",
                    "title": "Windows Prefetch Analysis",
                    "order_index": 16,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["The Windows Registry Fundamentals"],
                    "bullets": [
                        "Prefetch file structure (.pf files)",
                        "Execution timestamps, run counts",
                        "Tools: PECmd, WinPrefetchView"
                    ]
                },
                {
                    "slug": "lesson_dfir_17_shimcache_forensics_RICH.json",
                    "title": "Shimcache (AppCompatCache) Forensics",
                    "order_index": 17,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Windows Prefetch Analysis"],
                    "bullets": [
                        "Application Compatibility Cache analysis",
                        "Execution artifacts vs file existence",
                        "Tools: AppCompatCacheParser"
                    ]
                },
                {
                    "slug": "lesson_dfir_18_amcache_analysis_RICH.json",
                    "title": "AmCache Analysis",
                    "order_index": 18,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Shimcache (AppCompatCache) Forensics"],
                    "bullets": [
                        "AmCache.hve structure and forensic value",
                        "Program execution evidence, SHA1 hashes",
                        "Deleted program artifacts",
                        "Tools: AmcacheParser, MFTECmd"
                    ]
                },
                {
                    "slug": "lesson_dfir_19_pca_muicache_userassist_RICH.json",
                    "title": "PCA, MUICache, and UserAssist",
                    "order_index": 19,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["AmCache Analysis"],
                    "bullets": [
                        "Program Compatibility Assistant (PCA)",
                        "MUICache for executed applications",
                        "UserAssist registry keys (ROT13 decoding)",
                        "Tools: UserAssistView, MUICacheView"
                    ]
                },
                {
                    "slug": "lesson_dfir_20_srum_execution_forensics_RICH.json",
                    "title": "System Resource Usage Monitor (SRUM)",
                    "order_index": 20,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["PCA, MUICache, and UserAssist"],
                    "bullets": [
                        "SRUM database analysis (SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SRUM)",
                        "Network data usage, application runtime, energy usage",
                        "Tools: srum_dump, SRUM-Dump"
                    ]
                },
                {
                    "slug": "lesson_dfir_21_execution_timeline_creation_RICH.json",
                    "title": "Timeline Creation from Execution Artifacts",
                    "order_index": 21,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["System Resource Usage Monitor (SRUM)"],
                    "bullets": [
                        "Combining Prefetch, Shimcache, AmCache, SRUM",
                        "Creating comprehensive execution timelines",
                        "Correlation techniques",
                        "Tools: Timesketch, Plaso"
                    ]
                },
                {
                    "slug": "lesson_dfir_22_execution_detection_lab_RICH.json",
                    "title": "Evidence of Execution Detection Lab",
                    "order_index": 22,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Timeline Creation from Execution Artifacts"],
                    "bullets": [
                        "Hands-on: Detect malware execution",
                        "Analyze multiple execution artifacts",
                        "Build complete attacker activity timeline",
                        "Tools: PowerShell, KAPE, Velociraptor"
                    ]
                }
            ]
        },
        {
            "focus": "persistence and lateral movement forensics",
            "common_phrases": [
                "Windows service installation artifacts",
                "Service Control Manager event logs",
                "Scheduled Task XML analysis",
                "Task Scheduler operational log review",
                "Autoruns persistence locations",
                "Registry Run and RunOnce keys",
                "LSASS process protection",
                "Memory dump detection for credential theft",
                "NTDS.dit extraction indicators",
                "WDigest credential caching controls",
                "SMB lateral movement telemetry",
                "RDP connection logging",
                "WMI permanent event subscriptions",
                "PsExec service artifacts",
                "Named pipe traces of remote execution",
                "User Access Logging database analysis",
                "Firewall and PowerShell transcript correlation",
                "Endpoint detection tuning for persistence",
                "Threat hunting for lateral movement protocols",
                "Incident documentation for credential theft"
            ],
            "cases": [
                "NotPetya operators deployed malicious services across Ukraine networks",
                "APT29 lateral movement exposed through WMI event subscriptions and UAL records",
                "FIN7 campaigns leveraged scheduled tasks and PsExec to maintain access"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_23_services_scheduled_tasks_forensics_RICH.json",
                    "title": "Services and Scheduled Tasks Forensics",
                    "order_index": 23,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Evidence of Execution Detection Lab"],
                    "bullets": [
                        "Windows Services registry keys, Event ID 7045",
                        "Scheduled Tasks analysis (C:\\Windows\\System32\\Tasks)",
                        "Malicious service/task detection",
                        "Tools: Autoruns, sc.exe, schtasks, Sysinternals"
                    ]
                },
                {
                    "slug": "lesson_dfir_24_lsass_ntds_credential_theft_RICH.json",
                    "title": "LSASS, NTDS.dit, and Credential Theft Detection",
                    "order_index": 24,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Services and Scheduled Tasks Forensics"],
                    "bullets": [
                        "LSASS memory dumping detection",
                        "NTDS.dit extraction artifacts",
                        "WDigest and credential caching",
                        "Tools: Sysmon, ProcDump, Event Tracing"
                    ]
                },
                {
                    "slug": "lesson_dfir_25_smb_rdp_wmi_psexec_ual_analysis_RICH.json",
                    "title": "SMB, RDP, WMI, PsExec, and UAL Analysis",
                    "order_index": 25,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["LSASS, NTDS.dit, and Credential Theft Detection"],
                    "bullets": [
                        "SMB lateral movement artifacts",
                        "RDP forensics (Event logs, RDP cache, bitmap cache)",
                        "WMI persistence and lateral movement",
                        "PsExec artifacts (named pipes, services)",
                        "User Access Logging (UAL) database",
                        "Tools: KAPE, Velociraptor, PowerShell"
                    ]
                }
            ]
        },
        {
            "focus": "ntfs artifact forensics",
            "common_phrases": [
                "NTFS volume boot record interpretation",
                "Master File Table structure",
                "$STANDARD_INFORMATION attributes",
                "$FILE_NAME attributes",
                "Resident versus non-resident data",
                "Attribute lists and extension records",
                "$LogFile transaction analysis",
                "$UsnJrnl change journal",
                "$I30 index records",
                "Alternate Data Streams detection",
                "Timestomping detection in NTFS",
                "Sparse files and compression markers",
                "Volume shadow copy considerations",
                "File signature validation",
                "Timeline correlation across NTFS artifacts",
                "Data recovery from unallocated clusters",
                "Carving techniques for deleted entries",
                "Metafile cross-referencing",
                "Automation with MFTECmd and analyzeMFT",
                "Reporting NTFS findings to stakeholders"
            ],
            "cases": [
                "Sony Pictures investigation relied on $UsnJrnl and $LogFile to rebuild attacker actions",
                "Target breach forensic teams recovered deleted malware using MFT analysis",
                "APT28 intrusions exposed through timestomping detection within NTFS attributes"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_26_ntfs_fundamentals_metafiles_RICH.json",
                    "title": "NTFS Fundamentals and Metafiles",
                    "order_index": 26,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Disk Forensics and File System Analysis"],
                    "bullets": [
                        "NTFS architecture, clusters, MFT structure",
                        "$MFT, $LogFile, $UsnJrnl metafiles",
                        "Alternate Data Streams (ADS)",
                        "Tools: MFTECmd, ntfsinfo"
                    ]
                },
                {
                    "slug": "lesson_dfir_27_mft_analysis_RICH.json",
                    "title": "Master File Table (MFT) Analysis",
                    "order_index": 27,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["NTFS Fundamentals and Metafiles"],
                    "bullets": [
                        "MFT entry structure, attributes (STANDARD_INFORMATION, FILE_NAME)",
                        "File metadata extraction",
                        "Tools: MFTECmd, AnalyzeMFT"
                    ]
                },
                {
                    "slug": "lesson_dfir_28_macb_timestamps_timeline_RICH.json",
                    "title": "MACB Timestamps and Timeline Analysis",
                    "order_index": 28,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Master File Table (MFT) Analysis"],
                    "bullets": [
                        "Modified, Accessed, Changed, Born (MACB) timestamps",
                        "$STANDARD_INFORMATION vs $FILE_NAME timestamps",
                        "Timestomping detection",
                        "Tools: Timesketch, Plaso"
                    ]
                },
                {
                    "slug": "lesson_dfir_29_usn_journal_i30_analysis_RICH.json",
                    "title": "USN Journal and $I30 Index Analysis",
                    "order_index": 29,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["MACB Timestamps and Timeline Analysis"],
                    "bullets": [
                        "Update Sequence Number Journal parsing",
                        "$I30 index attributes (directory entries)",
                        "Deleted file recovery from $I30",
                        "Tools: MFTECmd, UsnJrnl2Csv"
                    ]
                },
                {
                    "slug": "lesson_dfir_30_ntfs_forensics_integration_lab_RICH.json",
                    "title": "NTFS Forensics Integration Lab",
                    "order_index": 30,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["USN Journal and $I30 Index Analysis"],
                    "bullets": [
                        "Parse MFT and USN Journal",
                        "Create filesystem timelines",
                        "Detect anti-forensic techniques",
                        "Tools: MFTECmd, PowerShell, Autopsy"
                    ]
                }
            ]
        },
        {
            "focus": "file deletion and recovery forensics",
            "common_phrases": [
                "Recycle Bin $I and $R file structure",
                "INFO2 legacy artifacts",
                "MFT entry deletion flags",
                "Directory index slack space",
                "Unallocated cluster analysis",
                "Volume shadow copy recovery",
                "Link file correlation with deletions",
                "Jump list remnants",
                "File signature validation for carving",
                "PhotoRec carving profiles",
                "Scalpel configuration tuning",
                "Bulk_extractor pattern scanning",
                "Data remanence in NTFS",
                "Carving limitations on fragmented files",
                "Timeline reconstruction after deletion",
                "Legal considerations for recovered data",
                "Automation for large-scale carving",
                "Reporting recovered artifacts",
                "Case management for deleted evidence",
                "Integrity validation of carved files"
            ],
            "cases": [
                "Capital One breach responders recovered deleted scripts from Recycle Bin remnants",
                "APT10 campaigns exposed through carved archives on cloud sync folders",
                "DarkHotel espionage cases reconstructed exfiltration staging via carved RAR files"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_31_windows_recycle_bin_forensics_RICH.json",
                    "title": "Windows Recycle Bin Forensics",
                    "order_index": 31,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["NTFS Fundamentals and Metafiles"],
                    "bullets": [
                        "$Recycle.Bin structure, $I files, $R files",
                        "INFO2 and $I file formats (Windows versions)",
                        "Recovering deleted file metadata",
                        "Tools: RBinViewer, KAPE modules"
                    ]
                },
                {
                    "slug": "lesson_dfir_32_permanent_deletion_unallocated_analysis_RICH.json",
                    "title": "Permanent Deletion and Unallocated Space Analysis",
                    "order_index": 32,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Windows Recycle Bin Forensics"],
                    "bullets": [
                        "File deletion mechanics (MFT entries marked deleted)",
                        "Unallocated space analysis",
                        "Data remnants and recovery",
                        "Tools: X-Ways Forensics, Autopsy"
                    ]
                },
                {
                    "slug": "lesson_dfir_33_file_carving_photorec_scalpel_RICH.json",
                    "title": "File Carving with PhotoRec and Scalpel",
                    "order_index": 33,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Permanent Deletion and Unallocated Space Analysis"],
                    "bullets": [
                        "File carving principles (file signatures)",
                        "PhotoRec for file recovery",
                        "Scalpel, bulk_extractor techniques",
                        "Tools: PhotoRec, Scalpel, bulk_extractor"
                    ]
                }
            ]
        },
        {
            "focus": "shortcut and jumplist forensics",
            "common_phrases": [
                "Shell link header analysis",
                "LinkInfo structures",
                "Volume and path information",
                "NetBIOS name resolution for LNK files",
                "MAC timestamps within shortcuts",
                "Volume serial number correlation",
                "Tracker GUID interpretation",
                "Distributed Link Tracking",
                "LNK artifact anti-forensics",
                "Jump list automatic destinations",
                "Jump list custom destinations",
                "DestList entries and MRU ordering",
                "Embedded shell items",
                "Correlating LNK with Prefetch",
                "Correlating jump lists with registry MRUs",
                "Timeline reconstruction with shortcut artifacts",
                "Automation using LECmd and JLECmd",
                "Documenting shortcut evidence for legal review",
                "Cross-platform considerations for jump lists",
                "Threat hunting with shortcut telemetry"
            ],
            "cases": [
                "APT29 phishing incidents exposed through malicious LNK metadata",
                "FIN7 intrusions tracked via jump list entries referencing rogue RDP tools",
                "Carbanak operations reconstructed from volume serial numbers in shortcut artifacts"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_34_lnk_file_analysis_RICH.json",
                    "title": "LNK File Analysis",
                    "order_index": 34,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Windows Recycle Bin Forensics"],
                    "bullets": [
                        "Windows Shortcut (.lnk) file structure",
                        "Target file information, MAC times, volume serial numbers",
                        "Tools: LECmd, LNK Explorer"
                    ]
                },
                {
                    "slug": "lesson_dfir_35_jump_lists_forensics_RICH.json",
                    "title": "Jump Lists Forensics",
                    "order_index": 35,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["LNK File Analysis"],
                    "bullets": [
                        "AutomaticDestinations-ms and CustomDestinations-ms",
                        "Recent documents, application usage",
                        "Tools: JLECmd, JumpListExplorer"
                    ]
                }
            ]
        },
        {
            "focus": "forensic timeline integration",
            "common_phrases": [
                "Bodyfile format fundamentals",
                "Filesystem enumeration with fls",
                "mactime output interpretation",
                "Artifact normalization for timelines",
                "Plaso parser coverage",
                "Log2Timeline configuration",
                "Timesketch collaborative analysis",
                "MFTECmd timeline exports",
                "Combining registry, Prefetch, and SRUM",
                "Cross-source timestamp conflicts",
                "Time zone normalization",
                "Event de-duplication strategies",
                "Visualization best practices",
                "Timeline pivoting techniques",
                "Detection engineering from timeline insights",
                "Automation of timeline generation",
                "Performance tuning for large evidence sets",
                "Case study reporting from timelines",
                "Timeline validation and peer review",
                "Lessons learned documentation"
            ],
            "cases": [
                "Colonial Pipeline response teams fused Plaso timelines with network telemetry",
                "Microsoft DART analysts correlated mactime output with Azure sign-in logs during Hafnium",
                "DFIR Report case studies show timeline integration exposing multi-stage ransomware"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_36_sleuth_kit_fls_mactime_RICH.json",
                    "title": "Sleuth Kit (TSK) fls and mactime",
                    "order_index": 36,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": [
                        "NTFS Forensics Integration Lab",
                        "LNK File Analysis",
                        "Scalable Registry Analysis with Automation"
                    ],
                    "bullets": [
                        "fls for filesystem listing",
                        "mactime for timeline creation",
                        "bodyfile format",
                        "Tools: Sleuth Kit, mactime"
                    ]
                },
                {
                    "slug": "lesson_dfir_37_plaso_log2timeline_RICH.json",
                    "title": "Plaso and Log2Timeline",
                    "order_index": 37,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Sleuth Kit (TSK) fls and mactime"],
                    "bullets": [
                        "Plaso framework overview",
                        "log2timeline.py for super timelines",
                        "Parsing 100+ artifact types",
                        "Tools: Plaso, Timesketch"
                    ]
                },
                {
                    "slug": "lesson_dfir_38_mftecmd_timeline_integration_RICH.json",
                    "title": "MFTECmd and Timeline Integration",
                    "order_index": 38,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Plaso and Log2Timeline"],
                    "bullets": [
                        "Eric Zimmerman's MFTECmd",
                        "Combining MFT, USN, Prefetch, Event Logs",
                        "Creating master forensic timelines",
                        "Tools: MFTECmd, Timesketch, PowerShell"
                    ]
                }
            ]
        },
        {
            "focus": "supplemental windows artifact forensics",
            "common_phrases": [
                "Browser history SQLite schemas",
                "Cookie and session restoration",
                "Download metadata correlation",
                "Cache storage formats",
                "Credential remnants in browsers",
                "Thumbs.db JPEG previews",
                "Thumbcache database parsing",
                "Windows 10 Activity Timeline structures",
                "ActivitiesCache.db schema",
                "Windows search index architecture",
                "Windows.edb content extraction",
                "Correlation between search index and filesystem",
                "Privacy implications of artifact retention",
                "Browser sync and cloud considerations",
                "Automation with Eric Zimmerman's tools",
                "Cross-referencing browser data with registry",
                "Timeline fusion with supplemental artifacts",
                "Anti-forensic manipulation of caches",
                "Reporting supplemental findings",
                "Threat hunting using user activity artifacts"
            ],
            "cases": [
                "Operation Aurora investigations traced attackers via Chrome history artifacts",
                "APT32 intrusions exposed through Windows Activity Timeline records",
                "Insider threats uncovered when Windows Search index retained deleted documents"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_39_web_browser_forensics_RICH.json",
                    "title": "Web Browser Forensics (Chrome, Firefox, Edge)",
                    "order_index": 39,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": [
                        "Scalable Registry Analysis with Automation",
                        "NTFS Forensics Integration Lab"
                    ],
                    "bullets": [
                        "Browser history, cookies, downloads",
                        "SQLite database parsing",
                        "Cache analysis, session recovery",
                        "Tools: Hindsight, BrowsingHistoryView"
                    ]
                },
                {
                    "slug": "lesson_dfir_40_thumbsdb_thumbcache_analysis_RICH.json",
                    "title": "Thumbs.db and Thumbcache Analysis",
                    "order_index": 40,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Web Browser Forensics (Chrome, Firefox, Edge)"],
                    "bullets": [
                        "Thumbnail cache forensics",
                        "Deleted image recovery",
                        "Tools: Thumbcache Viewer, ThumbExtractor"
                    ]
                },
                {
                    "slug": "lesson_dfir_41_windows_activity_timeline_RICH.json",
                    "title": "Windows Activity Timeline (ActivitiesCache.db)",
                    "order_index": 41,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Thumbs.db and Thumbcache Analysis"],
                    "bullets": [
                        "Windows 10 Timeline feature",
                        "ActivitiesCache.db SQLite database",
                        "Application and document activity",
                        "Tools: WxTCmd, Timeline Explorer"
                    ]
                },
                {
                    "slug": "lesson_dfir_42_windows_search_index_forensics_RICH.json",
                    "title": "Windows Search Index Forensics",
                    "order_index": 42,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Windows Activity Timeline (ActivitiesCache.db)"],
                    "bullets": [
                        "Windows.edb search database",
                        "Indexed file content, metadata",
                        "Recovering deleted file content from index",
                        "Tools: esentutl, Windows Search Parser"
                    ]
                }
            ]
        },
        {
            "focus": "memory forensics deep dive",
            "common_phrases": [
                "Windows virtual memory architecture",
                "Page table traversal",
                "Kernel versus user space analysis",
                "Process and thread structures",
                "EPROCESS layout",
                "Handle tables and object headers",
                "DLL loading mechanisms",
                "Volatility profile selection",
                "Intermediate Symbol Format (ISF)",
                "Memory acquisition tooling",
                "Integrity verification of memory dumps",
                "Analysis of pagefile and swapfile",
                "strings and bstrings triage",
                "Network connection reconstruction from memory",
                "Registry hive extraction from memory",
                "Code injection detection",
                "Kernel module inspection",
                "SSDT and API hook analysis",
                "Cross-referencing memory with disk artifacts",
                "Anti-forensic considerations in memory analysis"
            ],
            "cases": [
                "Duqu malware analysis required advanced volatility techniques to map injected DLLs",
                "NotPetya responders captured LSASS dumps to understand credential theft",
                "Sony Pictures remediation correlated memory artifacts with disk timelines to trace lateral movement"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_43_windows_memory_structures_architecture_RICH.json",
                    "title": "Windows Memory Structures and Architecture",
                    "order_index": 43,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Advanced Memory Forensics and Malware Analysis"],
                    "bullets": [
                        "Virtual memory, paging, page tables",
                        "Kernel vs user space",
                        "Process and thread structures",
                        "Tools: WinDbg, Volatility"
                    ]
                },
                {
                    "slug": "lesson_dfir_44_windows_process_genealogy_RICH.json",
                    "title": "Windows Process Genealogy",
                    "order_index": 44,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Windows Memory Structures and Architecture"],
                    "bullets": [
                        "Parent-child process relationships",
                        "Process tree analysis",
                        "Detecting process injection",
                        "Tools: Volatility windows.pstree, ProcDOT"
                    ]
                },
                {
                    "slug": "lesson_dfir_45_memory_acquisition_tools_techniques_RICH.json",
                    "title": "Memory Acquisition - Tools and Techniques",
                    "order_index": 45,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Windows Process Genealogy"],
                    "bullets": [
                        "FTK Imager, DumpIt, WinPmem",
                        "Live vs dead acquisition",
                        "Memory integrity verification",
                        "Tools: WinPmem, Magnet RAM Capture"
                    ]
                },
                {
                    "slug": "lesson_dfir_46_memory_acquisition_best_practices_vms_RICH.json",
                    "title": "Memory Acquisition Best Practices for VMs",
                    "order_index": 46,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Memory Acquisition - Tools and Techniques"],
                    "bullets": [
                        "VMware snapshot acquisition",
                        "Hyper-V memory dumps",
                        "Cloud VM memory extraction",
                        "Tools: vmss2core, Azure portal workflows"
                    ]
                },
                {
                    "slug": "lesson_dfir_47_vmware_esxi_memory_acquisition_RICH.json",
                    "title": "VMware ESXi Memory Acquisition",
                    "order_index": 47,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Memory Acquisition Best Practices for VMs"],
                    "bullets": [
                        ".vmem and .vmsn files",
                        "ESXi snapshot commands",
                        "Converting VMware memory formats",
                        "Tools: vmss2core, esxcli"
                    ]
                },
                {
                    "slug": "lesson_dfir_48_microsoft_hyperv_memory_acquisition_RICH.json",
                    "title": "Microsoft Hyper-V Memory Acquisition",
                    "order_index": 48,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["VMware ESXi Memory Acquisition"],
                    "bullets": [
                        "Hyper-V saved state files (.bin, .vsv)",
                        "Memory extraction techniques",
                        "Conversion to raw memory format",
                        "Tools: Hyper-V Manager, vm2dmp"
                    ]
                },
                {
                    "slug": "lesson_dfir_49_poor_mans_memory_forensics_strings_RICH.json",
                    "title": "Poor Man's Memory Forensics - Strings Analysis",
                    "order_index": 49,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Microsoft Hyper-V Memory Acquisition"],
                    "bullets": [
                        "strings and bstrings utilities",
                        "Unicode vs ASCII strings",
                        "Grepping memory dumps for IOCs",
                        "Tools: strings, ripgrep"
                    ]
                },
                {
                    "slug": "lesson_dfir_50_pagefile_swapfile_analysis_RICH.json",
                    "title": "Pagefile.sys and Swapfile.sys Analysis",
                    "order_index": 50,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Poor Man's Memory Forensics - Strings Analysis"],
                    "bullets": [
                        "Pagefile and swapfile forensic value",
                        "Extracting credentials and artifacts",
                        "Tools: strings, bulk_extractor"
                    ]
                },
                {
                    "slug": "lesson_dfir_51_volatility3_image_identification_profiles_RICH.json",
                    "title": "Volatility 3 - Image Identification and Profiles",
                    "order_index": 51,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Pagefile.sys and Swapfile.sys Analysis"],
                    "bullets": [
                        "vol.py -f image.raw windows.info",
                        "Symbol tables and profiles",
                        "ISF (Intermediate Symbol Format)",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_52_volatility_basic_process_enumeration_RICH.json",
                    "title": "Volatility - Basic Process Enumeration",
                    "order_index": 52,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Volatility 3 - Image Identification and Profiles"],
                    "bullets": [
                        "windows.pslist, windows.pstree, windows.psscan",
                        "Detecting hidden processes",
                        "EPROCESS structure analysis",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_53_volatility_in_depth_process_analysis_RICH.json",
                    "title": "Volatility - In-depth Process Analysis",
                    "order_index": 53,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Volatility - Basic Process Enumeration"],
                    "bullets": [
                        "windows.cmdline, windows.envars",
                        "Process privileges and tokens",
                        "Process memory sections",
                        "Tools: Volatility 3, volatility plugins"
                    ]
                },
                {
                    "slug": "lesson_dfir_54_volatility_dll_analysis_RICH.json",
                    "title": "Volatility - DLL Analysis",
                    "order_index": 54,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Volatility - In-depth Process Analysis"],
                    "bullets": [
                        "windows.dlllist, windows.ldrmodules",
                        "Detecting DLL injection",
                        "Unmapped DLLs and hollowed processes",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_55_volatility_process_handles_RICH.json",
                    "title": "Volatility - Process Handles Analysis",
                    "order_index": 55,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Volatility - DLL Analysis"],
                    "bullets": [
                        "windows.handles plugin",
                        "File, registry, mutex handles",
                        "Malware mutex detection",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_56_volatility_network_activity_analysis_RICH.json",
                    "title": "Volatility - Network Activity Analysis",
                    "order_index": 56,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Volatility - Process Handles Analysis"],
                    "bullets": [
                        "windows.netscan, windows.netstat",
                        "Active connections and listening ports",
                        "Correlating network activity to processes",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_57_volatility_registry_from_memory_RICH.json",
                    "title": "Volatility - Registry Analysis from Memory",
                    "order_index": 57,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Volatility - Network Activity Analysis"],
                    "bullets": [
                        "windows.registry.hivelist, windows.registry.printkey",
                        "Extracting registry keys from memory",
                        "Run keys, services, recent docs",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_58_volatility_detecting_code_injection_RICH.json",
                    "title": "Volatility - Detecting Code Injection",
                    "order_index": 58,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Volatility - Registry Analysis from Memory"],
                    "bullets": [
                        "windows.malfind for injected code",
                        "VAD tree analysis",
                        "Detecting hollowed processes",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_59_volatility_api_ssdt_hooks_RICH.json",
                    "title": "Volatility - API and SSDT Hooks",
                    "order_index": 59,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Volatility - Detecting Code Injection"],
                    "bullets": [
                        "windows.ssdt for System Service Descriptor Table hooks",
                        "IAT/EAT hooking detection",
                        "Rootkit detection",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_60_volatility_kernel_module_analysis_RICH.json",
                    "title": "Volatility - Kernel Module Analysis",
                    "order_index": 60,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Volatility - API and SSDT Hooks"],
                    "bullets": [
                        "windows.modules, windows.driverscan",
                        "Detecting malicious drivers",
                        "Unsigned driver analysis",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_61_volatility_dumping_files_processes_RICH.json",
                    "title": "Volatility - Dumping Files and Processes",
                    "order_index": 61,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Volatility - Kernel Module Analysis"],
                    "bullets": [
                        "windows.dumpfiles, windows.memmap",
                        "Extracting executables from memory",
                        "Carving files from process memory",
                        "Tools: Volatility 3"
                    ]
                },
                {
                    "slug": "lesson_dfir_62_volatility_yara_memory_scanning_RICH.json",
                    "title": "Volatility - YARA Memory Scanning",
                    "order_index": 62,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Volatility - Dumping Files and Processes"],
                    "bullets": [
                        "windows.yarascan plugin",
                        "Creating YARA rules for memory",
                        "Hunting for malware signatures in RAM",
                        "Tools: Volatility 3, YARA"
                    ]
                }
            ]
        },
        {
            "focus": "alternative memory analysis tooling",
            "common_phrases": [
                "MemProcFS architecture",
                "Virtual filesystem navigation",
                "Process analysis via MemProcFS",
                "Registry parsing through MemProcFS",
                "Network artifact extraction in MemProcFS",
                "Timeline generation with MemProcFS",
                "Malware hunting workflows",
                "WinDbg crash dump fundamentals",
                "Symbol loading in WinDbg",
                "MemProcFS and WinDbg integration",
                "Hibernation file structure",
                "Hiberfil.sys conversion techniques",
                "Volatility analysis of alternative sources",
                "Tool interoperability considerations",
                "Automation scripts for alternate tools",
                "Validation of alternate tool outputs",
                "Case study communication for alternate tools",
                "Evidence handling for large dumps",
                "Performance tuning and resource planning",
                "Combining alternate tools with Volatility"
            ],
            "cases": [
                "Microsoft MSTIC used MemProcFS during cloud memory investigations",
                "CERT-EU analysts leveraged WinDbg to debug kernel mode implants",
                "CISA responders parsed hiberfil.sys to recover ransomware staging data"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_63_memprocfs_introduction_setup_RICH.json",
                    "title": "MemProcFS Introduction and Setup",
                    "order_index": 63,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["Volatility - YARA Memory Scanning"],
                    "bullets": [
                        "MemProcFS vs Volatility",
                        "Mounting memory as virtual filesystem",
                        "Navigation and artifact locations",
                        "Tools: MemProcFS"
                    ]
                },
                {
                    "slug": "lesson_dfir_64_memprocfs_analysis_workflows_RICH.json",
                    "title": "MemProcFS Analysis Workflows",
                    "order_index": 64,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["MemProcFS Introduction and Setup"],
                    "bullets": [
                        "Process analysis via filesystem interface",
                        "Registry, network, handles via MemProcFS",
                        "Forensic timeline generation",
                        "Tools: MemProcFS, Timesketch"
                    ]
                },
                {
                    "slug": "lesson_dfir_65_memprocfs_malware_memory_analysis_RICH.json",
                    "title": "Malware Memory Analysis with MemProcFS",
                    "order_index": 65,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["MemProcFS Analysis Workflows"],
                    "bullets": [
                        "Dumping suspicious processes",
                        "Finding injected code",
                        "YARA scanning with MemProcFS",
                        "Tools: MemProcFS, YARA"
                    ]
                },
                {
                    "slug": "lesson_dfir_66_windbg_memory_analysis_RICH.json",
                    "title": "WinDbg for Memory Analysis",
                    "order_index": 66,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Malware Memory Analysis with MemProcFS"],
                    "bullets": [
                        "WinDbg crash dump analysis",
                        "Acquiring crash dumps with MemProcFS",
                        "Debugging commands for forensics",
                        "Tools: WinDbg, MemProcFS"
                    ]
                },
                {
                    "slug": "lesson_dfir_67_hibernation_file_analysis_RICH.json",
                    "title": "Hibernation File (hiberfil.sys) Analysis",
                    "order_index": 67,
                    "difficulty": 2,
                    "estimated_time": 45,
                    "prereq_titles": ["WinDbg for Memory Analysis"],
                    "bullets": [
                        "Converting hiberfil.sys to raw memory",
                        "Volatility analysis of hibernation files",
                        "Forensic value and limitations",
                        "Tools: Hibr2Bin, Volatility"
                    ]
                }
            ]
        },
        {
            "focus": "memory forensics case studies",
            "common_phrases": [
                "Initial triage of memory images",
                "Indicator of compromise enrichment",
                "Process injection validation",
                "Network connection pivoting",
                "Command and control identification",
                "Dumping malicious payloads",
                "YARA rule development",
                "Timeline reconstruction from memory",
                "Cross-referencing disk and memory",
                "Reporting lessons learned",
                "Coordinating with threat intelligence",
                "Preparing executive summaries",
                "Operationalizing case findings",
                "Automating recurring analysis steps",
                "Maintaining chain of custody",
                "Collaboration between blue and red teams",
                "Documenting remediation actions",
                "Validating containment success",
                "Continuous improvement loops",
                "Post-incident training and tabletop"
            ],
            "cases": [
                "DFIR Report documented TrickBot memory cases informing detection engineering",
                "FireEye M-Trends analysis highlighted memory triage for SUNBURST",
                "CISA advisories showcased coordinated memory response to ransomware incidents"
            ],
            "lessons": [
                {
                    "slug": "lesson_dfir_68_malware_memory_analysis_case_study_part1_RICH.json",
                    "title": "Malware Memory Analysis Case Study - Part 1",
                    "order_index": 68,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Hibernation File (hiberfil.sys) Analysis"],
                    "bullets": [
                        "Real-world malware memory image",
                        "Initial triage and IOC identification",
                        "Process injection detection",
                        "Tools: Volatility 3, MemProcFS"
                    ]
                },
                {
                    "slug": "lesson_dfir_69_malware_memory_analysis_case_study_part2_RICH.json",
                    "title": "Malware Memory Analysis Case Study - Part 2",
                    "order_index": 69,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Malware Memory Analysis Case Study - Part 1"],
                    "bullets": [
                        "Network connections and C2 analysis",
                        "Dumping and analyzing malicious code",
                        "YARA rule creation",
                        "Tools: Volatility 3, yara"
                    ]
                },
                {
                    "slug": "lesson_dfir_70_advanced_memory_forensics_capstone_RICH.json",
                    "title": "Advanced Memory Forensics Capstone Lab",
                    "order_index": 70,
                    "difficulty": 3,
                    "estimated_time": 55,
                    "prereq_titles": ["Malware Memory Analysis Case Study - Part 2"],
                    "bullets": [
                        "Multi-stage memory forensics investigation",
                        "Timeline reconstruction",
                        "Final report creation",
                        "Tools: Volatility 3, Timesketch, PowerShell"
                    ]
                }
            ]
        }
    ]

    for module in modules:
        generated = build_lessons(module, prereq_map, output_dir)
        print(f"Generated {len(generated)} lessons for {module['focus']}.")


if __name__ == "__main__":
    main()
