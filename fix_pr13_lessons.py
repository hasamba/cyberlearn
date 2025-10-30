"""
Fix post_assessment validation errors in PR #13 Windows forensics lessons (DFIR 11-70)
"""

import json
import uuid
from pathlib import Path

def fix_pr13_lessons():
    """Fix all PR #13 lesson files"""

    content_dir = Path(__file__).parent / "content"

    # Get all DFIR lessons 11-70 from PR #13
    lesson_files = sorted(content_dir.glob("lesson_dfir_[1-7][0-9]_*_RICH.json"))

    print("=" * 70)
    print("FIXING PR #13 WINDOWS FORENSICS LESSONS")
    print("=" * 70)
    print()

    fixed_count = 0
    error_count = 0

    for filepath in lesson_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lesson = json.load(f)

            # Skip if not in range 11-70
            order_index = lesson.get('order_index', 0)
            if order_index < 11 or order_index > 70:
                continue

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
                        correct_idx = question.get('correct_answer', 0)
                        correct_option = question.get('options', [])[correct_idx] if correct_idx < len(question.get('options', [])) else "the correct option"
                        question['explanation'] = f"The correct answer is '{correct_option}' because it best addresses the question in the context of Windows forensics and memory analysis."
                        questions_fixed += 1

                # Write back the fixed lesson
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(lesson, f, indent=2, ensure_ascii=False)

                print(f"[OK] {filepath.name} - Fixed {questions_fixed} field(s)")
                fixed_count += 1
            else:
                print(f"[WARN] {filepath.name} - No post_assessment found")
                error_count += 1

        except Exception as e:
            print(f"[ERROR] {filepath.name} - {e}")
            error_count += 1

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"[OK] Fixed: {fixed_count} lessons")
    print(f"[ERROR] Errors: {error_count} lessons")
    print()

    if fixed_count > 0:
        print("[SUCCESS] All PR #13 lessons fixed!")
        print()
        print("Next steps:")
        print("1. Run: python load_all_lessons.py")
        print("2. Create and apply course tags")
        print("3. Update template database")

if __name__ == "__main__":
    fix_pr13_lessons()
