#!/usr/bin/env python3
"""
Renumber lesson files to eliminate duplicates and ensure sequential numbering.
Also updates order_index inside the JSON files to match new numbers.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import shutil

def extract_lesson_info(filename):
    """Extract domain and number from filename like lesson_dfir_23_..."""
    match = re.match(r'lesson_([a-z_]+)_(\d+)_(.+_RICH\.json)', filename)
    if match:
        domain = match.group(1)
        number = int(match.group(2))
        rest = match.group(3)
        return domain, number, rest
    return None, None, None

def create_new_filename(domain, new_number, rest):
    """Create new filename with updated number"""
    return f"lesson_{domain}_{new_number:02d}_{rest}"

def update_order_index_in_file(file_path, new_order_index):
    """Update the order_index field inside the JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lesson_data = json.load(f)

    lesson_data['order_index'] = new_order_index

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(lesson_data, f, indent=2, ensure_ascii=False)

def main():
    content_dir = Path("content")
    lesson_files = sorted(content_dir.glob("lesson_*_RICH.json"))

    # Group lessons by domain
    domain_lessons = defaultdict(list)

    for file_path in lesson_files:
        domain, number, rest = extract_lesson_info(file_path.name)
        if domain and number and rest:
            domain_lessons[domain].append({
                'file': file_path,
                'number': number,
                'rest': rest,
                'filename': file_path.name
            })

    print("=" * 80)
    print("RENUMBERING LESSONS")
    print("=" * 80)

    all_renames = []

    for domain in sorted(domain_lessons.keys()):
        lessons = sorted(domain_lessons[domain], key=lambda x: (x['number'], x['filename']))

        # Create renumbering plan
        renumber_map = {}
        next_number = 1

        for lesson in lessons:
            old_number = lesson['number']
            old_file = lesson['file']
            old_filename = lesson['filename']
            rest = lesson['rest']

            new_number = next_number
            next_number += 1

            if old_number != new_number:
                new_filename = create_new_filename(domain, new_number, rest)
                renumber_map[old_file] = {
                    'old_filename': old_filename,
                    'new_filename': new_filename,
                    'old_number': old_number,
                    'new_number': new_number,
                    'file': old_file
                }
                all_renames.append((domain, old_file, old_filename, new_filename, old_number, new_number))

    if not all_renames:
        print("\nNo renumbering needed! All lessons are correctly numbered.")
        return

    print(f"\nTotal lessons to renumber: {len(all_renames)}")
    print("\nRenaming files...")

    renamed_count = 0

    # Use a two-phase rename to avoid conflicts:
    # Phase 1: Rename all to temp names
    # Phase 2: Rename temp names to final names

    temp_renames = []

    # Phase 1: Rename to temp files
    for domain, old_file, old_filename, new_filename, old_num, new_num in all_renames:
        temp_filename = f"TEMP_{renamed_count}_{new_filename}"
        temp_file = old_file.parent / temp_filename

        print(f"  [{renamed_count+1}/{len(all_renames)}] {domain}: {old_filename} -> {temp_filename}")

        shutil.move(str(old_file), str(temp_file))
        temp_renames.append((temp_file, old_file.parent / new_filename, new_num))
        renamed_count += 1

    # Phase 2: Rename temp files to final names and update order_index
    for temp_file, final_file, new_order_index in temp_renames:
        shutil.move(str(temp_file), str(final_file))

        # Update order_index inside the JSON
        update_order_index_in_file(final_file, new_order_index)

        print(f"  Finalized: {final_file.name} (order_index = {new_order_index})")

    print(f"\n[✓] Successfully renumbered {renamed_count} lessons!")
    print("\nNext steps:")
    print("  1. Run: python load_all_lessons.py")
    print("  2. Test the application to verify all lessons load correctly")

if __name__ == "__main__":
    main()
