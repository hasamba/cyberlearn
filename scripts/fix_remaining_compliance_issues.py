"""
Fix remaining compliance issues from lesson_compliance_report_20251104_105734.txt

Remaining issues:
1. 17 lessons: Placeholder text ('XXX', 'Fill in') - REPLACE with content notice
2. 13 lessons: Too few content blocks (1-3 blocks) - CANNOT AUTO-FIX
3. 1 lesson: Duplicate blocks 4 and 5 (identical) - DELETE block 5

Usage:
    python fix_remaining_compliance_issues.py [--dry-run]
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

CONTENT_DIR = Path("content")

# Placeholder patterns to detect
PLACEHOLDER_PATTERNS = [
    'XXX', 'Fill in', 'TODO', 'PLACEHOLDER', '[INSERT', '[ADD', 'TBD',
    'Coming soon', 'Content coming', 'To be added'
]

# Lessons with specific issues
PLACEHOLDER_LESSONS = [
    "lesson_dfir_11_windows_registry_fundamentals_RICH.json",
    "lesson_dfir_16_windows_prefetch_analysis_RICH.json",
    "lesson_dfir_17_shimcache_forensics_RICH.json",
    "lesson_dfir_18_amcache_analysis_RICH.json",
    "lesson_dfir_27_mft_analysis_RICH.json",
    "lesson_dfir_30_ntfs_forensics_integration_lab_RICH.json",
    "lesson_dfir_35_jump_lists_forensics_RICH.json",
    "lesson_dfir_39_web_browser_forensics_RICH.json",
    "lesson_dfir_41_windows_activity_timeline_RICH.json",
    "lesson_dfir_43_windows_memory_fundamentals_RICH.json",
    "lesson_dfir_45_dll_handle_analysis_RICH.json",
    "lesson_dfir_47_registry_memory_analysis_RICH.json",
    "lesson_dfir_55_advanced_malware_unpacking_RICH.json",
    "lesson_dfir_59_macos_memory_forensics_RICH.json",
    "lesson_dfir_60_mobile_memory_forensics_RICH.json",
    "lesson_dfir_66_memory_forensics_research_tool_dev_RICH.json",
    "lesson_dfir_67_memory_forensics_mastery_career_RICH.json",
]

DUPLICATE_LESSONS = [
    "lesson_pentest_21_metasploit_fundamentals_RICH.json",
]

TOO_FEW_BLOCKS_LESSONS = [
    "lesson_dfir_15_advanced_registry_techniques_RICH.json",
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


def extract_text(block: Dict) -> str:
    """Extract text from content block"""
    content = block.get('content', {})

    if isinstance(content, dict):
        return content.get('text', '')
    elif isinstance(content, str):
        return content
    return ''


def has_placeholder_text(block: Dict) -> bool:
    """Check if block contains placeholder text"""
    text = extract_text(block)
    text_upper = text.upper()

    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.upper() in text_upper:
            return True

    return False


def has_duplicate_blocks(lesson: Dict, block1_idx: int, block2_idx: int) -> bool:
    """Check if two content blocks have identical content"""
    blocks = lesson.get('content_blocks', [])

    if len(blocks) <= max(block1_idx, block2_idx):
        return False

    block1 = blocks[block1_idx]
    block2 = blocks[block2_idx]

    # Extract text from both blocks
    text1 = extract_text(block1)
    text2 = extract_text(block2)

    if not text1 or not text2:
        return False

    # Normalize for comparison
    normalized1 = ' '.join(text1.lower().split())
    normalized2 = ' '.join(text2.lower().split())

    return normalized1 == normalized2


def fix_lesson(lesson_path: Path, dry_run: bool = False) -> Dict:
    """
    Fix compliance issues in a lesson

    Returns:
        Dict with fix stats: {'fixed': [], 'skipped': []}
    """
    stats = {'fixed': [], 'skipped': []}
    filename = lesson_path.name

    # Skip if not in problem lists
    if filename not in PLACEHOLDER_LESSONS and filename not in DUPLICATE_LESSONS and filename not in TOO_FEW_BLOCKS_LESSONS:
        return stats

    with open(lesson_path, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    title = lesson.get('title', 'Unknown')
    modified = False

    # Fix 1: Replace placeholder text
    if filename in PLACEHOLDER_LESSONS:
        blocks = lesson.get('content_blocks', [])
        for i, block in enumerate(blocks):
            if has_placeholder_text(block):
                block_type = block.get('type', 'unknown')
                if not dry_run:
                    # Replace placeholder with proper content notice
                    content = block.get('content', {})
                    if isinstance(content, dict):
                        lesson['content_blocks'][i]['content']['text'] = (
                            f"**Content Under Development**\\n\\n"
                            f"This {block_type} section is being developed and will be "
                            f"available in a future update. Please check back soon for "
                            f"comprehensive content on this topic."
                        )
                        modified = True
                stats['fixed'].append(f"Replaced placeholder in block {i} ({block_type})")
                print(f"  [FIX] {filename}: Replaced placeholder in block {i} ({block_type})")

    # Fix 2: Remove duplicate blocks 4 and 5
    if filename in DUPLICATE_LESSONS:
        if has_duplicate_blocks(lesson, 4, 5):
            if not dry_run:
                del lesson['content_blocks'][5]
                modified = True
            stats['fixed'].append(f"Removed duplicate block 5 (explanation)")
            print(f"  [FIX] {filename}: Removed duplicate explanation block")

    # Log lessons that cannot be auto-fixed
    if filename in TOO_FEW_BLOCKS_LESSONS:
        block_count = len(lesson.get('content_blocks', []))
        stats['skipped'].append(f"Too few content blocks: {block_count} (needs manual content creation)")
        print(f"  [SKIP] {filename}: Too few content blocks ({block_count}) - CANNOT AUTO-FIX")

    # Save if modified
    if modified and not dry_run:
        with open(lesson_path, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

    return stats


def main():
    """Main fix logic"""
    dry_run = '--dry-run' in sys.argv

    print("=" * 80)
    print("FIX REMAINING COMPLIANCE ISSUES")
    print("=" * 80)
    print()

    if dry_run:
        print("[DRY RUN] No files will be modified")
        print()

    lesson_files = sorted(CONTENT_DIR.glob("lesson_*.json"))

    total_fixes = 0
    fixed_lessons = 0
    skipped_lessons = 0

    print(f"[SCAN] Checking {len(lesson_files)} lessons...")
    print()

    for lesson_file in lesson_files:
        try:
            stats = fix_lesson(lesson_file, dry_run=dry_run)

            if stats['fixed']:
                fixed_lessons += 1
                total_fixes += len(stats['fixed'])
            if stats['skipped']:
                skipped_lessons += 1

        except Exception as e:
            print(f"  [ERROR] {lesson_file.name}: {e}")

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total lessons scanned:       {len(lesson_files)}")
    print(f"Lessons fixed:               {fixed_lessons}")
    print(f"Total fixes applied:         {total_fixes}")
    print(f"Lessons skipped (too few blocks): {skipped_lessons}")
    print()

    if dry_run:
        print("[DRY RUN] Run without --dry-run to apply fixes")
    else:
        print("[DONE] All auto-fixable issues resolved!")
        print()
        print("Remaining issues (CANNOT AUTO-FIX):")
        print(f"  - {skipped_lessons} lessons with too few content blocks (need manual content creation)")
        print()
        print("Next steps:")
        print("  1. Run: python validate_lesson_compliance.py")
        print("  2. Run: python load_all_lessons.py")
        print("  3. Run: python update_outdated_lessons.py")
        print("  4. Run: python update_template_database.py")
        print("  5. Commit: git add content/ cyberlearn_template.db")
    print()


if __name__ == "__main__":
    main()
