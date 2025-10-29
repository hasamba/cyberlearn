#!/usr/bin/env python3
"""
Fix missing post_assessment fields in lessons.

Issue: Several lessons have incomplete post_assessment questions missing:
- question_id
- type
- difficulty

This script adds these fields with appropriate values.
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List

# Lessons that need fixing (from load_all_lessons.py output)
LESSONS_TO_FIX = [
    "lesson_blue_team_11_misp_threat_intelligence_RICH.json",
    "lesson_blue_team_12_opencti_threat_intelligence_RICH.json",
    "lesson_blue_team_13_sigma_detection_rules_RICH.json",
    "lesson_blue_team_14_snort_ids_ips_RICH.json",
    "lesson_blue_team_15_security_onion_nsm_RICH.json",
    "lesson_dfir_10_timesketch_timeline_analysis_RICH.json",
    "lesson_malware_11_yara_rules_RICH.json"
]

def fix_post_assessment_question(question: Dict, index: int) -> Dict:
    """Add missing fields to a post_assessment question"""
    # Add question_id if missing
    if 'question_id' not in question:
        question['question_id'] = str(uuid.uuid4())
        print(f"    Added question_id: {question['question_id']}")

    # Add type if missing (default to multiple_choice)
    if 'type' not in question:
        question['type'] = 'multiple_choice'
        print(f"    Added type: multiple_choice")

    # Add difficulty if missing (infer from question complexity or default to 2)
    if 'difficulty' not in question:
        # Default to difficulty 2 (medium)
        question['difficulty'] = 2
        print(f"    Added difficulty: 2")

    return question

def fix_lesson_file(filepath: Path) -> bool:
    """Fix post_assessment in a single lesson file"""
    print(f"\n[*] Processing: {filepath.name}")

    try:
        # Read JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        # Check if post_assessment needs fixing
        if 'post_assessment' not in lesson:
            print("  [SKIP] No post_assessment field")
            return True

        post_assessment = lesson['post_assessment']
        if not isinstance(post_assessment, list):
            print("  [ERROR] post_assessment is not a list")
            return False

        # Fix each question
        fixed_count = 0
        for i, question in enumerate(post_assessment):
            print(f"  Question {i+1}:")

            # Check if fixes needed
            needs_fix = (
                'question_id' not in question or
                'type' not in question or
                'difficulty' not in question
            )

            if needs_fix:
                fix_post_assessment_question(question, i)
                fixed_count += 1
            else:
                print("    [OK] All fields present")

        if fixed_count > 0:
            # Write back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)
            print(f"  [OK] Fixed {fixed_count} questions, saved to file")
        else:
            print("  [OK] No fixes needed")

        return True

    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON parse error: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def main():
    print("="*70)
    print("POST-ASSESSMENT FIELD FIX SCRIPT")
    print("="*70)
    print("\nThis script adds missing fields to post_assessment questions:")
    print("  - question_id (UUID)")
    print("  - type (multiple_choice)")
    print("  - difficulty (2 by default)")
    print("\nLessons to fix:")
    for lesson in LESSONS_TO_FIX:
        print(f"  - {lesson}")

    content_dir = Path('content')
    if not content_dir.exists():
        print("\n[ERROR] content/ directory not found")
        return

    # Process each lesson
    results = {'success': 0, 'failed': 0}

    for lesson_file in LESSONS_TO_FIX:
        filepath = content_dir / lesson_file

        if not filepath.exists():
            print(f"\n[WARNING] File not found: {lesson_file}")
            continue

        if fix_lesson_file(filepath):
            results['success'] += 1
        else:
            results['failed'] += 1

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Successfully fixed: {results['success']} files")
    print(f"Failed: {results['failed']} files")

    if results['failed'] == 0:
        print("\n[OK] All files fixed successfully!")
        print("\nNext step: Run 'python load_all_lessons.py' to load fixed lessons")
    else:
        print("\n[!] Some files had errors - review output above")

if __name__ == '__main__':
    main()
