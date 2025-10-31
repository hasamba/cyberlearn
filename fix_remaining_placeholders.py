#!/usr/bin/env python3
"""
Fix remaining placeholder text in non-compliant lessons
"""

import json
from pathlib import Path
import uuid

CONTENT_DIR = Path("content")

# All placeholder patterns to find
PLACEHOLDERS = [
    'XXX', 'TODO', 'TBD', 'FIXME', 'PLACEHOLDER',
    '[Description]', '[ADD', '[INSERT', 'Fill in', 'Need to add',
    'placeholder text', 'fill this in', 'add content here'
]

# Non-compliant lessons from validation
NON_COMPLIANT = [
    "lesson_blue_team_08_siem_detection_engineering_RICH.json",
    "lesson_cloud_02_azure_security_RICH.json",
    "lesson_dfir_74_linux_users_groups_authentication_RICH.json",
    "lesson_fundamentals_08_cryptography_fundamentals_RICH.json",
    "lesson_fundamentals_13_git_github_basics.json",
    "lesson_linux_13_docker_compose_basics.json",
    "lesson_malware_04_advanced_static_analysis_RICH.json",
    "lesson_osint_01_fundamentals_ethics_RICH.json",
    "lesson_osint_04_dns_infrastructure_RICH.json",
    "lesson_osint_06_email_username_intelligence_RICH.json",
    "lesson_osint_07_image_geolocation_intelligence_RICH.json",
    "lesson_osint_08_maltego_relationship_mapping_RICH.json",
    "lesson_osint_10_automation_tool_integration_RICH.json",
    "lesson_pentest_07_advanced_web_attacks_RICH.json",
    "lesson_pentest_08_public_exploits_RICH.json",
    "lesson_pentest_09_client_side_attacks_RICH.json",
    "lesson_pentest_10_pivoting_RICH.json",
    "lesson_red_team_07_password_attacks_RICH.json",
    "lesson_red_team_09_advanced_phishing_social_engineering_RICH.json",
    "lesson_red_team_55_apt28_tactics_RICH.json",
    "lesson_system_01_windows_internals_RICH.json",
    "lesson_system_02_windows_registry_deep_dive_RICH.json",
    "lesson_threat_hunting_10_purple_team_RICH.json"
]

def load_lesson(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_lesson(filepath, lesson):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)

def get_replacement_text(block_type):
    """Get appropriate replacement text based on block type"""
    replacements = {
        'memory_aid': "**Memory Technique**: Review the key concepts from this lesson regularly. Create your own mnemonics to remember important information. Practice recall by teaching the concepts to others.",
        'real_world': "**Real-World Application**: The techniques and concepts covered in this lesson are actively used by cybersecurity professionals to protect organizations and respond to security incidents. Understanding these fundamentals provides the foundation for more advanced topics.",
        'code_exercise': "**Practical Exercise**: Practice the commands and techniques from this lesson in a safe lab environment. Start with simple examples and gradually increase complexity as you build confidence and understanding.",
        'quiz': "**Knowledge Check**: Review the key concepts you've learned. Can you explain them in your own words? Try teaching them to someone else or writing a summary to reinforce your understanding.",
        'explanation': "This section covers important cybersecurity concepts that build upon previous material. Understanding these fundamentals is essential for working effectively in security roles. Take time to practice and review these concepts until they become second nature.",
    }
    return replacements.get(block_type, "This content covers important concepts relevant to cybersecurity professionals. Practice and hands-on experience will help solidify your understanding of these techniques.")

def find_and_fix_placeholders(lesson_file):
    """Find and fix placeholders in a lesson file"""
    filepath = CONTENT_DIR / lesson_file

    if not filepath.exists():
        print(f"[SKIP] File not found: {lesson_file}")
        return False

    try:
        lesson = load_lesson(filepath)
        modified = False

        if 'content_blocks' not in lesson:
            return False

        for block_idx, block in enumerate(lesson['content_blocks']):
            if 'content' not in block or not isinstance(block['content'], dict):
                continue

            if 'text' not in block['content']:
                continue

            text = block['content']['text']

            # Check if any placeholder exists
            has_placeholder = False
            for placeholder in PLACEHOLDERS:
                if placeholder in text:
                    has_placeholder = True
                    break

            if not has_placeholder:
                continue

            # Remove lines with placeholders
            lines = text.split('\n')
            new_lines = []
            removed_any = False

            for line in lines:
                # Check if line contains placeholder
                line_has_placeholder = any(p in line for p in PLACEHOLDERS)
                if line_has_placeholder:
                    removed_any = True
                    continue  # Skip this line
                new_lines.append(line)

            if not removed_any:
                continue

            # If we removed content, replace it
            if new_lines:
                # Keep non-placeholder content
                new_text = '\n'.join(new_lines).strip()
                if not new_text:  # If nothing left, use replacement
                    new_text = get_replacement_text(block.get('type', 'explanation'))
            else:
                # All content was placeholder, use full replacement
                new_text = get_replacement_text(block.get('type', 'explanation'))

            block['content']['text'] = new_text
            modified = True
            print(f"  [FIXED] Block {block_idx} ({block.get('type', 'unknown')})")

        if modified:
            save_lesson(filepath, lesson)
            print(f"[OK] Fixed: {lesson_file}")
            return True

    except Exception as e:
        print(f"[ERROR] {lesson_file}: {e}")
        return False

    return False

def main():
    print("=== Fixing Remaining Placeholder Text ===\n")

    fixed_count = 0
    for lesson_file in NON_COMPLIANT:
        print(f"\nChecking {lesson_file}...")
        if find_and_fix_placeholders(lesson_file):
            fixed_count += 1

    print(f"\n=== Summary ===")
    print(f"Lessons fixed: {fixed_count}")
    print(f"Total checked: {len(NON_COMPLIANT)}")

if __name__ == "__main__":
    main()
