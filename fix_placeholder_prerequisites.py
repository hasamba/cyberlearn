"""
Fix prerequisite references to placeholder lessons.

Some lessons reference placeholder lesson IDs that don't exist.
This script removes those invalid prerequisites.
"""

import json
from pathlib import Path

def is_placeholder_id(uuid_str):
    """Check if UUID is a placeholder (has pattern like bt000000-0000-0000-0000-000000000001)"""
    # Placeholder patterns: bt000000, fn000000, rt000000, etc.
    placeholder_patterns = [
        'bt000000-0000-0000-0000-',
        'fn000000-0000-0000-0000-',
        'rt000000-0000-0000-0000-',
        'pt000000-0000-0000-0000-',
        'ad000000-0000-0000-0000-',
        'df000000-0000-0000-0000-',
        'mw000000-0000-0000-0000-'
    ]
    return any(uuid_str.startswith(pattern) for pattern in placeholder_patterns)

def fix_prerequisites():
    """Remove placeholder prerequisites from all lessons"""

    content_dir = Path("content")
    rich_lessons = list(content_dir.glob("lesson_*_RICH.json"))

    if not rich_lessons:
        print("No RICH lesson files found")
        return

    fixed_count = 0

    for lesson_file in rich_lessons:
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check prerequisites
            original_prereqs = data.get('prerequisites', [])

            # Filter out placeholder IDs
            valid_prereqs = [p for p in original_prereqs if not is_placeholder_id(p)]

            if len(valid_prereqs) != len(original_prereqs):
                # Found placeholder prerequisites - remove them
                data['prerequisites'] = valid_prereqs

                # Save updated file
                with open(lesson_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                removed = len(original_prereqs) - len(valid_prereqs)
                print(f"✓ {lesson_file.name}: Removed {removed} placeholder prerequisite(s)")
                fixed_count += 1

        except Exception as e:
            print(f"✗ Error processing {lesson_file.name}: {e}")

    print()
    if fixed_count > 0:
        print(f"Fixed {fixed_count} lesson file(s)!")
        print()
        print("Next step: Run 'python load_all_lessons.py' to load lessons into database")
    else:
        print("No placeholder prerequisites found - all lessons are ready!")

if __name__ == "__main__":
    fix_prerequisites()
