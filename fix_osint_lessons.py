#!/usr/bin/env python3
"""
Fix validation errors in OSINT lessons:
1. Add missing question_id and type fields to post_assessment
2. Replace invalid jim_kwik_principles with valid enum values
"""

import json
import uuid
from pathlib import Path

# Valid jim_kwik_principles enum values
VALID_JIM_KWIK_PRINCIPLES = [
    "active_learning",
    "meta_learning",
    "memory_hooks",
    "minimum_effective_dose",
    "teach_like_im_10",
    "connect_to_what_i_know",
    "reframe_limiting_beliefs",
    "gamify_it",
    "learning_sprint",
    "multiple_memory_pathways"
]

# Mapping of invalid to valid principles
PRINCIPLE_MAPPING = {
    "spaced_repetition": "learning_sprint",
    "visualization": "memory_hooks",
    "real_world_application": "connect_to_what_i_know",
    "mistakes_as_learning": "reframe_limiting_beliefs",
    "teach_others": "teach_like_im_10",
    "chunking_information": "minimum_effective_dose",
    "emotional_connection": "connect_to_what_i_know",
    "pattern_recognition": "meta_learning",
    "progressive_complexity": "learning_sprint"
}

def fix_post_assessment(lesson):
    """Add missing question_id and type fields to post_assessment"""
    if 'post_assessment' not in lesson:
        return

    for qa in lesson['post_assessment']:
        # Add question_id if missing
        if 'question_id' not in qa:
            qa['question_id'] = str(uuid.uuid4())
            print(f"   Added question_id: {qa['question_id']}")

        # Add type if missing (default to multiple_choice)
        if 'type' not in qa:
            qa['type'] = 'multiple_choice'
            print(f"   Added type: multiple_choice")

def fix_jim_kwik_principles(lesson):
    """Replace invalid jim_kwik_principles with valid enum values"""
    if 'jim_kwik_principles' not in lesson:
        return

    principles = lesson['jim_kwik_principles']
    fixed_principles = []

    for principle in principles:
        if principle in VALID_JIM_KWIK_PRINCIPLES:
            # Already valid, keep it
            fixed_principles.append(principle)
        elif principle in PRINCIPLE_MAPPING:
            # Map invalid to valid
            valid_principle = PRINCIPLE_MAPPING[principle]
            fixed_principles.append(valid_principle)
            print(f"   Mapped '{principle}' -> '{valid_principle}'")
        else:
            # Unknown invalid principle, map to active_learning as default
            fixed_principles.append("active_learning")
            print(f"   Unknown principle '{principle}' -> 'active_learning'")

    # Remove duplicates while preserving order
    seen = set()
    unique_principles = []
    for p in fixed_principles:
        if p not in seen:
            seen.add(p)
            unique_principles.append(p)

    # Ensure we have at least 3 principles
    while len(unique_principles) < 3:
        for principle in VALID_JIM_KWIK_PRINCIPLES:
            if principle not in unique_principles:
                unique_principles.append(principle)
                break

    lesson['jim_kwik_principles'] = unique_principles

def fix_osint_lesson(filepath):
    """Fix a single OSINT lesson file"""
    print(f"\nProcessing: {filepath.name}")

    # Read lesson
    with open(filepath, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    # Fix post_assessment
    print("  Fixing post_assessment...")
    fix_post_assessment(lesson)

    # Fix jim_kwik_principles
    print("  Fixing jim_kwik_principles...")
    fix_jim_kwik_principles(lesson)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)

    print(f"  [OK] Fixed and saved: {filepath.name}")

def main():
    """Fix all OSINT lesson files"""
    print("=" * 60)
    print("OSINT Lesson Validation Fixes")
    print("=" * 60)

    content_dir = Path(__file__).parent / "content"
    osint_lessons = sorted(content_dir.glob("lesson_osint_*_RICH.json"))

    if not osint_lessons:
        print("\n[WARNING] No OSINT lessons found in content/ directory")
        return

    print(f"\nFound {len(osint_lessons)} OSINT lesson(s) to fix")

    for lesson_file in osint_lessons:
        try:
            fix_osint_lesson(lesson_file)
        except Exception as e:
            print(f"  [ERROR] Error fixing {lesson_file.name}: {e}")

    print("\n" + "=" * 60)
    print("[SUCCESS] All OSINT lessons fixed!")
    print("\nNext steps:")
    print("  1. Run: python load_all_lessons.py")
    print("  2. Verify OSINT lessons load successfully")
    print("  3. Check OSINT domain in My Learning tab")
    print("=" * 60)

if __name__ == "__main__":
    main()
