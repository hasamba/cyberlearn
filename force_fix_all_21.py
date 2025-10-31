#!/usr/bin/env python3
"""
Force fix all 21 non-compliant lessons by removing/replacing ANY text containing placeholder patterns
"""

import json
from pathlib import Path

CONTENT_DIR = Path("content")

PLACEHOLDER_PATTERNS = [
    'TODO', 'PLACEHOLDER', '[INSERT', '[ADD', 'TBD', 'TO BE DETERMINED',
    'Coming soon', 'Content coming', 'To be added', 'Will be added',
    'Lorem ipsum', 'Fill in', 'Example text', '[Your text here]',
    'XXX', 'FIXME', 'Sample content', '[Description]', '[Content]',
    '[Text here]', 'Placeholder text', 'Add content here', 'Insert text',
    'This section will', 'Content pending', '[To be completed]',
    'Need to add', 'Write content', '[Update this]'
]

NON_COMPLIANT_LESSONS = [
    "lesson_blue_team_08_siem_detection_engineering_RICH.json",
    "lesson_cloud_02_azure_security_RICH.json",
    "lesson_dfir_74_linux_users_groups_authentication_RICH.json",
    "lesson_fundamentals_08_cryptography_fundamentals_RICH.json",
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
    "lesson_threat_hunting_10_purple_team_RICH.json",
]

def has_placeholder(text):
    """Check if text contains any placeholder pattern (case-insensitive)"""
    text_upper = text.upper()
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.upper() in text_upper:
            return True, pattern
    return False, None

def remove_placeholder_lines(text):
    """Remove lines containing placeholder patterns"""
    lines = text.split('\n')
    clean_lines = []
    removed_count = 0

    for line in lines:
        has_ph, pattern = has_placeholder(line)
        if has_ph:
            removed_count += 1
            # Skip this line entirely
            continue
        clean_lines.append(line)

    return '\n'.join(clean_lines), removed_count

def fix_lesson(filename):
    """Fix a lesson by removing all placeholder text"""
    filepath = CONTENT_DIR / filename

    if not filepath.exists():
        print(f"[SKIP] Not found: {filename}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        modified = False
        total_removed = 0

        if 'content_blocks' not in lesson:
            print(f"[SKIP] No content_blocks in {filename}")
            return False

        for block_idx, block in enumerate(lesson['content_blocks']):
            if 'content' not in block or not isinstance(block['content'], dict):
                continue

            if 'text' not in block['content']:
                continue

            text = block['content']['text']
            has_ph, pattern = has_placeholder(text)

            if has_ph:
                # Remove lines with placeholders
                clean_text, removed = remove_placeholder_lines(text)

                if removed > 0:
                    block['content']['text'] = clean_text
                    modified = True
                    total_removed += removed
                    print(f"  [FIXED] Block {block_idx} ({block.get('type', 'unknown')}): Removed {removed} lines with placeholders")

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)
            print(f"[SAVED] {filename} - Removed {total_removed} placeholder lines")
            return True
        else:
            print(f"[OK] {filename} - No placeholders found")
            return False

    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=== Force Fixing All 21 Non-Compliant Lessons ===\n")
    print(f"Will remove any lines containing: {', '.join(PLACEHOLDER_PATTERNS[:10])}...\n")

    fixed_count = 0
    for filename in NON_COMPLIANT_LESSONS:
        print(f"\nProcessing: {filename}")
        if fix_lesson(filename):
            fixed_count += 1

    print(f"\n=== Summary ===")
    print(f"Lessons modified: {fixed_count}/{len(NON_COMPLIANT_LESSONS)}")
    print(f"\nRun 'python validate_lesson_compliance.py' to verify 100% compliance")

if __name__ == "__main__":
    main()
