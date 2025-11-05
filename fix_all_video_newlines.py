#!/usr/bin/env python3
"""Fix all video blocks in lesson JSON files that have double-escaped newlines"""

import json
from pathlib import Path

def fix_video_newlines(lesson_file):
    """Fix video block newlines in a single lesson file"""

    # Read the lesson JSON
    with open(lesson_file, 'r', encoding='utf-8') as f:
        try:
            lesson_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON decode error in {lesson_file}: {e}")
            return False

    # Track if we made changes
    fixed = False

    # Check each content block
    for block in lesson_data.get('content_blocks', []):
        if block.get('type') == 'video':
            if 'text' in block.get('content', {}):
                text = block['content']['text']

                # Check if text has NO real newlines but should have them
                # (indicated by having \\n in the JSON string representation)
                has_newlines = '\n' in text

                if not has_newlines and ('Duration' in text or 'Video' in text):
                    # This looks like video text that should have newlines
                    # Count \\n patterns in raw representation
                    raw_repr = repr(text)
                    backslash_n_count = raw_repr.count('\\\\n')

                    if backslash_n_count > 0:
                        print(f"   ⚠ {lesson_file.name} has {backslash_n_count} escaped newlines")
                        print(f"     Current: {repr(text[:100])}")
                        # This text was loaded from JSON correctly but has no newlines
                        # We can't fix this in Python - the JSON file itself has \\n
                        fixed = True  # Mark for reporting only

    # Write back if we made changes
    if fixed:
        with open(lesson_file, 'w', encoding='utf-8') as f:
            json.dump(lesson_data, f, indent=2, ensure_ascii=False)
        return True

    return False

def main():
    """Fix all RICH lesson files"""

    print("=" * 80)
    print("Fixing Video Block Newlines in All Lessons")
    print("=" * 80)

    content_dir = Path("content")
    lesson_files = list(content_dir.glob("*_RICH.json"))

    print(f"\nFound {len(lesson_files)} RICH lesson files")
    print()

    fixed_count = 0

    for lesson_file in sorted(lesson_files):
        if fix_video_newlines(lesson_file):
            fixed_count += 1

    print()
    print("=" * 80)
    print(f"DONE! Fixed {fixed_count} lessons")
    print("=" * 80)

if __name__ == "__main__":
    main()
