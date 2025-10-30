"""
Fix duplicate lesson IDs by generating new UUIDs
"""

import json
import uuid
from pathlib import Path
from collections import defaultdict

def fix_duplicates():
    """Find and fix duplicate lesson IDs"""

    # Find duplicate lesson IDs
    lesson_ids = defaultdict(list)
    content_dir = Path('content')

    for lesson_file in content_dir.glob('lesson_*.json'):
        with open(lesson_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            lesson_ids[data['lesson_id']].append((lesson_file, data))

    # Find duplicates
    duplicates = {lid: files_data for lid, files_data in lesson_ids.items() if len(files_data) > 1}

    if not duplicates:
        print("No duplicate lesson IDs found")
        return

    print(f"=== Found {len(duplicates)} duplicate lesson IDs ===\n")

    fixed_count = 0

    for lesson_id, files_data in duplicates.items():
        print(f"Duplicate lesson ID: {lesson_id}")

        # Keep the first file, fix the rest
        for i, (lesson_file, data) in enumerate(files_data):
            if i == 0:
                print(f"  [KEEP] {lesson_file.name}")
            else:
                # Generate new UUID
                new_id = str(uuid.uuid4())
                data['lesson_id'] = new_id

                # Write back to file
                with open(lesson_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"  [FIX] {lesson_file.name} -> {new_id}")
                fixed_count += 1
        print()

    print(f"[SUMMARY] Fixed {fixed_count} lessons with duplicate IDs")

if __name__ == "__main__":
    fix_duplicates()
