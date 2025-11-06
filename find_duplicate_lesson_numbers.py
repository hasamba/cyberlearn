#!/usr/bin/env python3
"""
Find duplicate lesson numbers within each domain and suggest renumbering.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def extract_lesson_number(filename):
    """Extract domain and number from filename like lesson_dfir_23_..."""
    match = re.match(r'lesson_([a-z_]+)_(\d+)_', filename)
    if match:
        domain = match.group(1)
        number = int(match.group(2))
        return domain, number
    return None, None

def main():
    content_dir = Path("content")
    lesson_files = sorted(content_dir.glob("lesson_*_RICH.json"))

    # Group lessons by domain
    domain_lessons = defaultdict(list)

    for file_path in lesson_files:
        domain, number = extract_lesson_number(file_path.name)
        if domain and number:
            domain_lessons[domain].append({
                'file': file_path,
                'number': number,
                'filename': file_path.name
            })

    # Find duplicates and suggest renumbering
    print("=" * 80)
    print("DUPLICATE LESSON NUMBER ANALYSIS")
    print("=" * 80)

    all_duplicates = []

    for domain in sorted(domain_lessons.keys()):
        lessons = sorted(domain_lessons[domain], key=lambda x: x['number'])

        # Find duplicates
        number_count = defaultdict(list)
        for lesson in lessons:
            number_count[lesson['number']].append(lesson['filename'])

        duplicates = {num: files for num, files in number_count.items() if len(files) > 1}

        if duplicates:
            print(f"\n{domain.upper()}: Found {len(duplicates)} duplicate number(s)")
            for num, files in sorted(duplicates.items()):
                print(f"  Number {num:02d}: {len(files)} lessons")
                for f in files:
                    print(f"    - {f}")
                all_duplicates.append((domain, num, files))

    if not all_duplicates:
        print("\n✓ No duplicates found!")
        return

    # Suggest renumbering plan
    print("\n" + "=" * 80)
    print("SUGGESTED RENUMBERING PLAN")
    print("=" * 80)

    renumber_plan = []

    for domain in sorted(domain_lessons.keys()):
        lessons = sorted(domain_lessons[domain], key=lambda x: (x['number'], x['filename']))

        # Assign sequential numbers
        suggested_numbers = {}
        next_number = 1

        for lesson in lessons:
            suggested_numbers[lesson['filename']] = next_number
            next_number += 1

        # Check if any changes needed
        changes_needed = []
        for lesson in lessons:
            old_num = lesson['number']
            new_num = suggested_numbers[lesson['filename']]
            if old_num != new_num:
                changes_needed.append((lesson['filename'], old_num, new_num))

        if changes_needed:
            print(f"\n{domain.upper()}: {len(changes_needed)} file(s) need renumbering")
            for filename, old_num, new_num in changes_needed:
                print(f"  {filename}")
                print(f"    {old_num:02d} -> {new_num:02d}")
                renumber_plan.append({
                    'domain': domain,
                    'old_filename': filename,
                    'old_number': old_num,
                    'new_number': new_num
                })

    # Save renumbering plan
    plan_file = Path("renumber_plan.json")
    with open(plan_file, 'w') as f:
        json.dump(renumber_plan, f, indent=2)

    print(f"\n✓ Renumbering plan saved to: {plan_file}")
    print(f"  Total files to rename: {len(renumber_plan)}")

    # Show summary by domain
    print("\n" + "=" * 80)
    print("SUMMARY BY DOMAIN")
    print("=" * 80)

    for domain in sorted(domain_lessons.keys()):
        lessons = domain_lessons[domain]
        numbers = sorted([l['number'] for l in lessons])
        duplicates = len(numbers) - len(set(numbers))
        gaps = []

        for i in range(1, max(numbers)):
            if i not in numbers:
                gaps.append(i)

        print(f"\n{domain.upper()}:")
        print(f"  Total lessons: {len(lessons)}")
        print(f"  Number range: {min(numbers)}-{max(numbers)}")
        print(f"  Duplicates: {duplicates}")
        if gaps:
            print(f"  Gaps: {gaps[:5]}{'...' if len(gaps) > 5 else ''}")

if __name__ == "__main__":
    main()
