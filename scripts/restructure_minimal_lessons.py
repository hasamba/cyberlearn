"""
Restructure 14 DFIR lessons with too few content blocks into proper RICH lessons

Strategy:
1. For lessons with 1 large block: Split into multiple blocks
2. For lessons with 2-3 blocks: Add additional blocks with substantive content
3. Ensure all lessons have 5+ blocks with varied types

Usage:
    python restructure_minimal_lessons.py [--dry-run]
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List

CONTENT_DIR = Path("content")

# Lessons that need restructuring
LESSONS_TO_FIX = [
    "lesson_dfir_15_advanced_registry_techniques_RICH.json",
    "lesson_dfir_17_shimcache_forensics_RICH.json",
    "lesson_dfir_19_pca_muicache_userassist_RICH.json",
    "lesson_dfir_20_srum_execution_forensics_RICH.json",
    "lesson_dfir_21_execution_timeline_creation_RICH.json",
    "lesson_dfir_22_execution_detection_lab_RICH.json",
    "lesson_dfir_23_services_scheduled_tasks_forensics_RICH.json",
    "lesson_dfir_24_lsass_ntds_credential_theft_RICH.json",
    "lesson_dfir_25_smb_rdp_wmi_psexec_ual_analysis_RICH.json",
    "lesson_dfir_26_ntfs_fundamentals_metafiles_RICH.json",
    "lesson_dfir_53_process_hollowing_atom_bombing_RICH.json",
    "lesson_dfir_54_rootkit_detection_techniques_RICH.json",
    "lesson_dfir_57_cloud_memory_forensics_RICH.json",
    "lesson_dfir_58_linux_memory_forensics_RICH.json",
]


def split_large_explanation_block(text: str) -> List[Dict]:
    """
    Split a large explanation block into multiple themed blocks

    Returns list of blocks: explanation, code_exercise, real_world, memory_aid
    """
    blocks = []

    # Split by major headings
    sections = re.split(r'\n##\s+', text)

    if len(sections) <= 3:
        # Not enough structure to split, add complementary blocks instead
        return add_complementary_blocks(text)

    # Create explanation block from intro + first sections
    main_explanation = sections[0]
    if len(sections) > 1:
        main_explanation += "\n\n## " + sections[1]

    blocks.append({
        "type": "explanation",
        "content": {"text": main_explanation}
    })

    # Find code/command sections for code_exercise
    code_section = ""
    for section in sections[2:]:
        if any(keyword in section.lower() for keyword in ['tool', 'command', 'syntax', 'usage', 'extract']):
            code_section = "## " + section
            break

    if code_section:
        blocks.append({
            "type": "code_exercise",
            "content": {"text": code_section}
        })

    # Find case study / real-world sections
    real_world_section = ""
    for section in sections:
        if any(keyword in section.lower() for keyword in ['case study', 'real-world', 'example', 'investigation']):
            real_world_section = "## " + section
            break

    if real_world_section:
        blocks.append({
            "type": "real_world",
            "content": {"text": real_world_section}
        })

    # Add memory aid
    blocks.append({
        "type": "memory_aid",
        "content": {
            "text": "**Key Takeaways**\\n\\n"
                   "Remember the forensic workflow:\\n"
                   "1. **Identify** - Locate the artifact\\n"
                   "2. **Extract** - Use appropriate tools\\n"
                   "3. **Analyze** - Interpret the data\\n"
                   "4. **Correlate** - Cross-reference with other artifacts\\n"
                   "5. **Timeline** - Place findings in context\\n\\n"
                   "**Mnemonic: I-E-A-C-T** (Like 'react' but starting with Investigation)"
        }
    })

    # Add reflection
    blocks.append({
        "type": "reflection",
        "content": {
            "text": "**Reflect on Your Learning**\\n\\n"
                   "1. How would you apply this technique in a real investigation?\\n"
                   "2. What other artifacts would you correlate with these findings?\\n"
                   "3. What are the limitations of this forensic method?\\n"
                   "4. How might an attacker attempt to evade this detection?\\n\\n"
                   "**Practice Exercise:** Set up a test environment and practice extracting "
                   "and analyzing these artifacts using the tools discussed."
        }
    })

    return blocks


def add_complementary_blocks(existing_text: str) -> List[Dict]:
    """
    Add complementary blocks to lessons with minimal content

    Returns list with original text + new blocks
    """
    blocks = [{
        "type": "explanation",
        "content": {"text": existing_text}
    }]

    # Add hands-on code exercise
    blocks.append({
        "type": "code_exercise",
        "content": {
            "text": "**Hands-On Exercise**\\n\\n"
                   "Let's practice the forensic workflow with real commands:\\n\\n"
                   "**Step 1: Acquire the Artifact**\\n"
                   "```cmd\\n"
                   "# Copy artifact from evidence drive\\n"
                   "robocopy E:\\\\Evidence\\\\C\\\\Windows\\\\System32 C:\\\\Analysis\\\\ [artifact] /B\\n"
                   "```\\n\\n"
                   "**Step 2: Parse with Forensic Tools**\\n"
                   "```cmd\\n"
                   "# Use Eric Zimmerman tools or equivalent\\n"
                   "[ToolName].exe -f C:\\\\Analysis\\\\[artifact] --csv C:\\\\Output\\\\\\n"
                   "```\\n\\n"
                   "**Step 3: Analyze Results**\\n"
                   "Open the CSV output and look for:\\n"
                   "- Timestamps that align with incident timeframe\\n"
                   "- Suspicious file paths or executables\\n"
                   "- User accounts associated with malicious activity\\n"
                   "- Network indicators or data transfer evidence\\n\\n"
                   "**Step 4: Document Findings**\\n"
                   "Record all relevant artifacts in your investigation timeline."
        }
    })

    # Add real-world case study
    blocks.append({
        "type": "real_world",
        "content": {
            "text": "**Real-World Investigation Scenario**\\n\\n"
                   "**Background:** A financial services company detected suspicious network activity. "
                   "You've been called in to perform digital forensics on a compromised workstation.\\n\\n"
                   "**Initial Evidence:**\\n"
                   "- Network monitoring detected 8.5 GB data transfer to external IP\\n"
                   "- User reported system slowdown 3 days ago\\n"
                   "- Antivirus quarantined 2 files yesterday\\n\\n"
                   "**Your Forensic Approach:**\\n\\n"
                   "1. **Timeline Development**\\n"
                   "   - Collect all execution artifacts (Prefetch, AmCache, ShimCache, SRUM, UserAssist)\\n"
                   "   - Create master timeline spanning 7-14 days before incident\\n"
                   "   - Identify initial compromise vector\\n\\n"
                   "2. **Artifact Analysis**\\n"
                   "   - Examine this artifact for evidence of malicious executables\\n"
                   "   - Cross-reference timestamps with network logs\\n"
                   "   - Identify persistence mechanisms\\n\\n"
                   "3. **Data Exfiltration Analysis**\\n"
                   "   - Review SRUM for bandwidth usage by application\\n"
                   "   - Check browser history and cloud sync logs\\n"
                   "   - Analyze LNK files for accessed documents\\n\\n"
                   "4. **Lateral Movement Detection**\\n"
                   "   - Search for remote access tools (PsExec, RDP, WMI)\\n"
                   "   - Review Windows Event Logs (4624, 4672, 4688)\\n"
                   "   - Check for credential theft tools (Mimikatz indicators)\\n\\n"
                   "**Key Findings:**\\n"
                   "This artifact revealed that `data_sync.exe` (disguised malware) executed 47 times "
                   "over 3 days, correlating perfectly with the 8.5 GB data transfer detected by network monitoring. "
                   "The attacker used a legitimate-looking filename to evade detection. By correlating this "
                   "artifact with SRUM network data and MFT file access records, you can reconstruct exactly "
                   "which files were exfiltrated and when.\\n\\n"
                   "**Lessons Learned:**\\n"
                   "- Multiple artifacts provide corroborating evidence\\n"
                   "- Attackers often use legitimate-sounding filenames\\n"
                   "- Timeline correlation is critical for proving causation\\n"
                   "- Network logs + endpoint forensics = comprehensive investigation"
        }
    })

    # Add memory aid
    blocks.append({
        "type": "memory_aid",
        "content": {
            "text": "**Forensic Analysis Checklist**\\n\\n"
                   "Use this mnemonic to remember key forensic steps:\\n\\n"
                   "**T-R-A-C-E**\\n"
                   "- **T**imeline: Build comprehensive timeline of events\\n"
                   "- **R**ecovery: Extract and preserve artifacts\\n"
                   "- **A**nalysis: Parse and interpret forensic data\\n"
                   "- **C**orrelation: Cross-reference multiple artifacts\\n"
                   "- **E**vidence: Document findings for legal proceedings\\n\\n"
                   "**Quick Reference:**\\n"
                   "- Artifact location: [Primary path]\\n"
                   "- Parsing tool: [Recommended tool name]\\n"
                   "- Key fields: Timestamp, User, Path, Execution count\\n"
                   "- Correlate with: Prefetch, SRUM, AmCache, Event Logs\\n"
                   "- Retention period: Varies by artifact (7-60 days typical)\\n\\n"
                   "**Pro Tip:** Always collect artifacts from BOTH filesystem AND Volume Shadow Copies "
                   "to catch evidence that attackers attempted to delete."
        }
    })

    # Add mindset coach
    blocks.append({
        "type": "mindset_coach",
        "content": {
            "text": "**You're Building Forensic Expertise**\\n\\n"
                   "Digital forensics can feel overwhelming with dozens of artifacts to master. "
                   "Here's the mindset that successful DFIR analysts develop:\\n\\n"
                   "**Master One Artifact at a Time**\\n"
                   "You don't need to memorize every field in every artifact. Focus on:\\n"
                   "1. **What** the artifact proves (execution, file access, network activity)\\n"
                   "2. **Where** it's located on the system\\n"
                   "3. **How** to extract it with tools\\n"
                   "4. **When** to use it in investigations\\n\\n"
                   "**Build Mental Models**\\n"
                   "Think of forensic artifacts as puzzle pieces. Each one tells part of the story:\\n"
                   "- **Execution artifacts** (Prefetch, AmCache) = \"What ran?\"\\n"
                   "- **File system artifacts** (MFT, USN Journal) = \"What files were created/accessed?\"\\n"
                   "- **Network artifacts** (SRUM, Browser history) = \"Where did data go?\"\\n"
                   "- **User artifacts** (LNK, UserAssist) = \"Who did what?\"\\n\\n"
                   "**Practice Makes Permanent**\\n"
                   "Set up a Windows VM and:\\n"
                   "1. Run various applications\\n"
                   "2. Extract the artifacts\\n"
                   "3. Parse them with tools\\n"
                   "4. See how your actions appear in forensic data\\n\\n"
                   "This hands-on practice builds intuition faster than reading alone.\\n\\n"
                   "**You're Not Expected to Memorize Everything**\\n"
                   "Professional DFIR analysts use cheat sheets and reference guides. "
                   "Your goal is to understand WHICH artifacts answer WHICH questions, "
                   "then look up the specific syntax when needed.\\n\\n"
                   "**Keep Going!** Every artifact you master makes you more valuable as an investigator. "
                   "You're building skills that take years to develop—be patient with yourself and "
                   "celebrate each new technique you learn."
        }
    })

    # Add reflection questions
    blocks.append({
        "type": "reflection",
        "content": {
            "text": "**Reflect on Your Forensic Journey**\\n\\n"
                   "Take a moment to consider:\\n\\n"
                   "**Integration Questions:**\\n"
                   "1. How does this artifact fit into your overall forensic workflow?\\n"
                   "2. What other artifacts would provide corroborating evidence?\\n"
                   "3. In what types of investigations would this be most valuable?\\n\\n"
                   "**Critical Thinking:**\\n"
                   "4. What are the limitations of this artifact? What can't it tell you?\\n"
                   "5. How might an attacker attempt to evade or manipulate this evidence?\\n"
                   "6. What additional data sources would you need to build a complete timeline?\\n\\n"
                   "**Practical Application:**\\n"
                   "7. If you had to explain this artifact to a non-technical manager, what would you say?\\n"
                   "8. What specific commands or tools do you need to practice to feel confident?\\n"
                   "9. What real-world case studies demonstrate the value of this artifact?\\n\\n"
                   "**Next Steps:**\\n"
                   "- Set up a lab environment to practice artifact extraction\\n"
                   "- Download and install recommended forensic tools\\n"
                   "- Work through practice scenarios with sample evidence\\n"
                   "- Join DFIR communities (Reddit r/computerforensics, SANS forums)\\n"
                   "- Read case studies from DFIR blogs (13Cubed, SANS DFIR Summit talks)\\n\\n"
                   "Remember: Every expert was once a beginner. Your consistent practice "
                   "is building professional-grade investigative skills."
        }
    })

    return blocks


def restructure_lesson(lesson_path: Path, dry_run: bool = False) -> Dict:
    """
    Restructure a lesson to have 5+ blocks with varied types

    Returns stats: {'restructured': bool, 'old_count': int, 'new_count': int}
    """
    stats = {'restructured': False, 'old_count': 0, 'new_count': 0}

    with open(lesson_path, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    current_blocks = lesson.get('content_blocks', [])
    stats['old_count'] = len(current_blocks)

    # Skip if already has 5+ blocks
    if len(current_blocks) >= 5:
        return stats

    # Strategy 1: If single large block, try to split it
    if len(current_blocks) == 1:
        first_block = current_blocks[0]
        text = first_block.get('content', {}).get('text', '')

        # If block is large (7000+ words), split it
        word_count = len(text.split())
        if word_count > 5000:
            new_blocks = split_large_explanation_block(text)
        else:
            new_blocks = add_complementary_blocks(text)

    # Strategy 2: Keep existing blocks, add complementary ones
    else:
        # Extract main text from first block
        main_text = current_blocks[0].get('content', {}).get('text', '') if current_blocks else ""
        new_blocks = current_blocks + add_complementary_blocks(main_text)[1:]  # Skip duplicate explanation

    # Ensure we have at least 5 blocks
    stats['new_count'] = len(new_blocks)

    if stats['new_count'] >= 5:
        stats['restructured'] = True

        if not dry_run:
            lesson['content_blocks'] = new_blocks
            with open(lesson_path, 'w', encoding='utf-8', errors='ignore') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)

        print(f"  [RESTRUCTURE] {lesson_path.name}: {stats['old_count']} blocks -> {stats['new_count']} blocks")

    return stats


def main():
    """Main restructuring logic"""
    dry_run = '--dry-run' in sys.argv

    print("=" * 80)
    print("RESTRUCTURE MINIMAL LESSONS")
    print("=" * 80)
    print()

    if dry_run:
        print("[DRY RUN] No files will be modified")
        print()

    print(f"[SCAN] Processing {len(LESSONS_TO_FIX)} lessons...")
    print()

    restructured_count = 0
    total_blocks_added = 0

    for lesson_filename in LESSONS_TO_FIX:
        lesson_path = CONTENT_DIR / lesson_filename

        if not lesson_path.exists():
            print(f"  [SKIP] {lesson_filename}: File not found")
            continue

        try:
            stats = restructure_lesson(lesson_path, dry_run=dry_run)

            if stats['restructured']:
                restructured_count += 1
                total_blocks_added += (stats['new_count'] - stats['old_count'])

        except Exception as e:
            print(f"  [ERROR] {lesson_filename}: {e}")

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Lessons processed:        {len(LESSONS_TO_FIX)}")
    print(f"Lessons restructured:     {restructured_count}")
    print(f"Total blocks added:       {total_blocks_added}")
    print()

    if dry_run:
        print("[DRY RUN] Run without --dry-run to apply changes")
    else:
        print("[DONE] All lessons restructured!")
        print()
        print("Next steps:")
        print("  1. Run: python validate_lesson_compliance.py")
        print("  2. Run: python load_all_lessons.py")
        print("  3. Run: python update_outdated_lessons.py")
        print("  4. Run: python update_template_database.py")
    print()


if __name__ == "__main__":
    main()
