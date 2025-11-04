"""
Fix post_assessment fields that are incorrectly wrapped in {"text": "..."} dicts.
Post-assessment question and explanation fields must be plain strings, not dicts.
"""

import json
from pathlib import Path

def fix_post_assessment_wrapping(lesson_data):
    """Unwrap post_assessment question/explanation fields from {"text": "..."} dicts."""
    modified = False

    if "post_assessment" in lesson_data and isinstance(lesson_data["post_assessment"], list):
        for assessment in lesson_data["post_assessment"]:
            # Fix question field
            if "question" in assessment and isinstance(assessment["question"], dict):
                if "text" in assessment["question"]:
                    assessment["question"] = assessment["question"]["text"]
                    modified = True

            # Fix explanation field
            if "explanation" in assessment and isinstance(assessment["explanation"], dict):
                if "text" in assessment["explanation"]:
                    assessment["explanation"] = assessment["explanation"]["text"]
                    modified = True

    return modified

def main():
    content_dir = Path("content")
    fixed_count = 0

    # Process all JSON files
    for lesson_file in sorted(content_dir.glob("lesson_*.json")):
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Fix post_assessment wrapping
            if fix_post_assessment_wrapping(data):
                # Save the fixed file
                with open(lesson_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"[FIXED] {lesson_file.name}")
                fixed_count += 1

        except Exception as e:
            print(f"[ERROR] {lesson_file.name}: {e}")

    print(f"\n[COMPLETE] Fixed {fixed_count} lesson files")

if __name__ == "__main__":
    main()
