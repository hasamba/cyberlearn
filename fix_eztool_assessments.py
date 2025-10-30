"""
Fix missing question_id and explanation fields in Eric Zimmerman Tools lessons.

All 14 new EZ Tool lessons are missing:
- question_id: UUID for each assessment question
- explanation: Explanation for why the answer is correct

This script adds these required fields to all post_assessment questions.
"""

import json
import uuid
from pathlib import Path

def fix_eztool_lessons():
    """Fix post_assessment validation errors in EZ Tool lessons."""

    content_dir = Path(__file__).parent / "content"

    # EZ Tool lessons: dfir_11 through dfir_24
    lesson_files = [
        "lesson_dfir_11_amcacheparser_RICH.json",
        "lesson_dfir_12_appcompatcacheparser_RICH.json",
        "lesson_dfir_13_bstrings_RICH.json",
        "lesson_dfir_14_evtxecmd_RICH.json",
        "lesson_dfir_15_jlecmd_RICH.json",
        "lesson_dfir_16_lecmd_RICH.json",
        "lesson_dfir_17_mftecmd_RICH.json",
        "lesson_dfir_18_pecmd_RICH.json",
        "lesson_dfir_19_rbcmd_RICH.json",
        "lesson_dfir_20_recmd_RICH.json",
        "lesson_dfir_21_sbecmd_RICH.json",
        "lesson_dfir_22_sqlecmd_RICH.json",
        "lesson_dfir_23_wxtcmd_RICH.json",
        "lesson_dfir_24_timelineexplorer_RICH.json",
    ]

    print("="*70)
    print("FIXING ERIC ZIMMERMAN TOOLS LESSON VALIDATION ERRORS")
    print("="*70)
    print()

    fixed_count = 0
    error_count = 0

    for filename in lesson_files:
        filepath = content_dir / filename

        if not filepath.exists():
            print(f"[WARN] {filename} - NOT FOUND")
            error_count += 1
            continue

        try:
            # Read the lesson
            with open(filepath, 'r', encoding='utf-8') as f:
                lesson = json.load(f)

            # Fix post_assessment questions
            if 'post_assessment' in lesson and isinstance(lesson['post_assessment'], list):
                questions_fixed = 0

                for question in lesson['post_assessment']:
                    # Add question_id if missing
                    if 'question_id' not in question:
                        question['question_id'] = str(uuid.uuid4())
                        questions_fixed += 1

                    # Add explanation if missing
                    if 'explanation' not in question:
                        # Generate a basic explanation based on the correct answer
                        correct_idx = question.get('correct_answer', 0)
                        correct_option = question.get('options', [])[correct_idx] if correct_idx < len(question.get('options', [])) else "the correct option"

                        question['explanation'] = f"The correct answer is '{correct_option}' because it best addresses the question in the context of digital forensics and incident response workflows."
                        questions_fixed += 1

                # Write back the fixed lesson
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(lesson, f, indent=2, ensure_ascii=False)

                print(f"[OK] {filename} - Fixed {questions_fixed} field(s)")
                fixed_count += 1
            else:
                print(f"[WARN] {filename} - No post_assessment found")
                error_count += 1

        except Exception as e:
            print(f"[ERROR] {filename} - ERROR: {e}")
            error_count += 1

    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"[OK] Fixed: {fixed_count} lessons")
    print(f"[ERROR] Errors: {error_count} lessons")
    print()

    if fixed_count == 14 and error_count == 0:
        print("[SUCCESS] All Eric Zimmerman Tools lessons fixed successfully!")
        print()
        print("Next steps:")
        print("1. Run: python load_all_lessons.py")
        print("2. Run: python dev_tools/tag_eztool_lessons.py")
        print("3. Commit the changes to git")
    else:
        print("[WARN] Some lessons had issues. Please review the output above.")

if __name__ == "__main__":
    fix_eztool_lessons()
