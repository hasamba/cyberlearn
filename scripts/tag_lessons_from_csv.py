#!/usr/bin/env python3
"""
Tag lessons according to lesson_ideas.csv

Matches lessons by domain and order_index, then adds course_tag as a tag.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict

CONTENT_DIR = Path(__file__).parent / 'content'

def load_lesson_ideas():
    """Load lesson ideas CSV and create mapping by domain/order_index"""
    mapping = defaultdict(dict)  # domain -> order_index -> course_tag

    with open('lesson_ideas.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                domain = row['domain'].strip()
                order_index = int(row['order_index'])
                course_tag = row.get('course_tag', '').strip()

                if course_tag:
                    mapping[domain][order_index] = course_tag
            except (ValueError, KeyError) as e:
                print(f"[WARNING] Skipping row: {e}")
                continue

    return mapping

def tag_lessons(mapping):
    """Tag all lessons based on CSV mapping"""
    tagged_count = 0
    skipped_count = 0

    # Get all lesson files
    lesson_files = sorted(CONTENT_DIR.glob('lesson_*.json'))

    for filepath in lesson_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        domain = lesson.get('domain')
        order_index = lesson.get('order_index')

        # Check if this lesson has a course tag in CSV
        if domain in mapping and order_index in mapping[domain]:
            course_tag = mapping[domain][order_index]

            # Add tag if not already present
            if 'tags' not in lesson:
                lesson['tags'] = []

            if course_tag not in lesson['tags']:
                lesson['tags'].append(course_tag)

                # Save lesson
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(lesson, f, indent=2, ensure_ascii=False)

                print(f"[OK] {filepath.name}: Added tag '{course_tag}'")
                tagged_count += 1
            else:
                print(f"[SKIP] {filepath.name}: Already has tag '{course_tag}'")
                skipped_count += 1
        else:
            # No tag for this lesson
            skipped_count += 1

    return tagged_count, skipped_count

def main():
    print("Loading lesson_ideas.csv...")
    mapping = load_lesson_ideas()

    print(f"\nFound course tags for {sum(len(v) for v in mapping.values())} lessons across {len(mapping)} domains")
    print("\nTagging lessons...")

    tagged, skipped = tag_lessons(mapping)

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Tagged: {tagged} lessons")
    print(f"  Skipped: {skipped} lessons (already tagged or no course tag)")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
