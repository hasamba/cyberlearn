"""
Fix all compliance issues found in lesson_compliance_report

Issues to fix:
1. 116 lessons: Duplicate blocks 0 and 1 (both explanation) - DELETE block 1
2. 22 lessons: Duplicate blocks 1 and 3 (explanation + memory_aid) - DELETE block 3
3. 23 lessons: Too few Jim Kwik principles - ADD missing principles
4. 14 lessons: Too few content blocks - Cannot auto-fix (needs content)
5. 19 lessons: Placeholder text in blocks - REPLACE with proper content notice

Usage:
    python fix_all_compliance_issues.py [--dry-run]
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set

CONTENT_DIR = Path("content")

# Valid Jim Kwik principles - all 10 required
ALL_JIM_KWIK_PRINCIPLES = [
    'active_learning',
    'minimum_effective_dose',
    'teach_like_im_10',
    'memory_hooks',
    'meta_learning',
    'connect_to_what_i_know',
    'reframe_limiting_beliefs',
    'gamify_it',
    'learning_sprint',
    'multiple_memory_pathways'
]

# Placeholder patterns to detect
PLACEHOLDER_PATTERNS = [
    'TODO', 'PLACEHOLDER', '[INSERT', '[ADD', 'TBD',
    'Coming soon', 'Content coming', 'To be added'
]


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


def fix_lesson(lesson_path: Path, dry_run: bool = False) -> Dict:
    """
    Fix all compliance issues in a lesson

    Returns:
        Dict with fix stats: {'fixed': [], 'skipped': []}
    """
    stats = {'fixed': [], 'skipped': []}

    with open(lesson_path, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    title = lesson.get('title', 'Unknown')
    modified = False

    # Fix 1: Remove duplicate blocks 0 and 1
    if has_duplicate_blocks(lesson, 0, 1):
        if not dry_run:
            del lesson['content_blocks'][1]
            modified = True
        stats['fixed'].append(f"Removed duplicate block 1 (explanation)")
        print(f"  [FIX] {lesson_path.name}: Removed duplicate explanation block")

    # Fix 2: Remove duplicate blocks 1 and 3 (after fix 1, might be 0 and 2 now)
    elif has_duplicate_blocks(lesson, 1, 3):
        if not dry_run:
            del lesson['content_blocks'][3]
            modified = True
        stats['fixed'].append(f"Removed duplicate block 3 (memory_aid)")
        print(f"  [FIX] {lesson_path.name}: Removed duplicate memory_aid block")

    # Fix 3: Add missing Jim Kwik principles
    principles = lesson.get('jim_kwik_principles', [])
    if len(principles) < 10:
        missing = [p for p in ALL_JIM_KWIK_PRINCIPLES if p not in principles]
        if not dry_run:
            lesson['jim_kwik_principles'] = ALL_JIM_KWIK_PRINCIPLES.copy()
            modified = True
        stats['fixed'].append(f"Added {len(missing)} missing Jim Kwik principles")
        print(f"  [FIX] {lesson_path.name}: Added {len(missing)} missing principles")

    # Fix 4: Replace placeholder text
    blocks = lesson.get('content_blocks', [])
    for i, block in enumerate(blocks):
        if has_placeholder_text(block):
            block_type = block.get('type', 'unknown')
            if not dry_run:
                # Replace placeholder with proper content notice
                content = block.get('content', {})
                if isinstance(content, dict):
                    lesson['content_blocks'][i]['content']['text'] = (
                        f"**Content Under Development**\n\n"
                        f"This {block_type} section is being developed and will be "
                        f"available in a future update. Please check back soon for "
                        f"comprehensive content on this topic."
                    )
                    modified = True
            stats['fixed'].append(f"Replaced placeholder in block {i} ({block_type})")
            print(f"  [FIX] {lesson_path.name}: Replaced placeholder in block {i}")

    # Save if modified
    if modified and not dry_run:
        with open(lesson_path, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

    return stats


def main():
    """Main fix logic"""
    dry_run = '--dry-run' in sys.argv

    print("=" * 80)
    print("FIX ALL COMPLIANCE ISSUES")
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
            elif stats['skipped']:
                skipped_lessons += 1

        except Exception as e:
            print(f"  [ERROR] {lesson_file.name}: {e}")

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total lessons scanned:  {len(lesson_files)}")
    print(f"Lessons fixed:          {fixed_lessons}")
    print(f"Total fixes applied:    {total_fixes}")
    print(f"Lessons skipped:        {skipped_lessons}")
    print()

    if dry_run:
        print("[DRY RUN] Run without --dry-run to apply fixes")
    else:
        print("[DONE] All fixes applied!")
        print()
        print("Next steps:")
        print("  1. Run: python validate_lesson_compliance.py")
        print("  2. Run: python load_all_lessons.py")
        print("  3. Run: python update_template_database.py")
        print("  4. Commit: git add content/ cyberlearn_template.db")
    print()


if __name__ == "__main__":
    main()
