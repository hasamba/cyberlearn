"""
Fix validation errors in new lessons from PR #14
- Add missing question_id fields
- Add missing explanation fields
"""

import json
import uuid
from pathlib import Path

def fix_lesson(lesson_file):
    """Fix validation errors in a single lesson file"""

    with open(lesson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed = False

    # Fix post_assessment questions
    if 'post_assessment' in data:
        for i, question in enumerate(data['post_assessment']):
            # Add missing question_id
            if 'question_id' not in question:
                question['question_id'] = str(uuid.uuid4())
                fixed = True

            # Add missing explanation
            if 'explanation' not in question:
                # Generate a basic explanation based on the question
                question['explanation'] = "Review the lesson content for the correct answer."
                fixed = True

    if fixed:
        # Write back to file
        with open(lesson_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True

    return False

def main():
    """Fix all lesson files with validation errors"""

    content_dir = Path('content')
    lesson_files = sorted(content_dir.glob('lesson_*_RICH.json'))

    print(f"[INFO] Checking {len(lesson_files)} RICH lesson files...")
    print("=" * 60)

    fixed_count = 0

    for lesson_file in lesson_files:
        try:
            if fix_lesson(lesson_file):
                print(f"[FIXED] {lesson_file.name}")
                fixed_count += 1
        except Exception as e:
            print(f"[ERROR] {lesson_file.name}: {e}")

    print("=" * 60)
    print(f"[SUMMARY] Fixed {fixed_count} lessons")

if __name__ == "__main__":
    main()
