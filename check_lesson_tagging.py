"""
Check which lessons from lesson_ideas.csv need to be tagged in the database
"""

import csv
import sqlite3
from collections import defaultdict

def check_tagging():
    """Check lesson tagging against lesson_ideas.csv"""

    # Read lesson_ideas.csv
    lesson_ideas = []
    with open('lesson_ideas.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] == 'completed' and row['course_tag']:
                lesson_ideas.append({
                    'domain': row['domain'],
                    'order_index': int(row['order_index']),
                    'title': row['title'],
                    'course_tag': row['course_tag']
                })

    print(f"Found {len(lesson_ideas)} completed lessons with course tags in lesson_ideas.csv")

    # Connect to database
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Get all tags
    cursor.execute("SELECT tag_id, name FROM tags")
    tags = {name: tag_id for tag_id, name in cursor.fetchall()}

    print(f"Found {len(tags)} tags in database")
    print(f"\nAvailable tags:")
    for tag_name in sorted(tags.keys()):
        print(f"  - {tag_name}")

    # Check tagging for each lesson
    print(f"\n=== Checking lesson tagging ===\n")

    tagged_count = 0
    untagged_count = 0
    missing_lessons = []
    missing_tags = set()

    for idea in lesson_ideas:
        # Find lesson by domain and order_index
        cursor.execute('''
            SELECT lesson_id, title
            FROM lessons
            WHERE domain = ? AND order_index = ?
        ''', (idea['domain'], idea['order_index']))

        result = cursor.fetchone()

        if not result:
            missing_lessons.append(idea)
            continue

        lesson_id, db_title = result

        # Check if tag exists
        tag_name = idea['course_tag']
        if tag_name not in tags:
            missing_tags.add(tag_name)
            untagged_count += 1
            continue

        tag_id = tags[tag_name]

        # Check if lesson is tagged
        cursor.execute('''
            SELECT 1 FROM lesson_tags
            WHERE lesson_id = ? AND tag_id = ?
        ''', (lesson_id, tag_id))

        if cursor.fetchone():
            tagged_count += 1
        else:
            print(f"[UNTAGGED] {idea['domain']:15s} [{idea['order_index']:3d}]: {idea['title']}")
            print(f"            Tag: {tag_name}")
            untagged_count += 1

    conn.close()

    print(f"\n=== Summary ===")
    print(f"Lessons with tags in lesson_ideas.csv: {len(lesson_ideas)}")
    print(f"Already tagged in database: {tagged_count}")
    print(f"Need tagging: {untagged_count}")
    print(f"Missing from database: {len(missing_lessons)}")

    if missing_tags:
        print(f"\n=== Missing tags (need to be created) ===")
        for tag in sorted(missing_tags):
            print(f"  - {tag}")

    if missing_lessons:
        print(f"\n=== Lessons in CSV but not in database ===")
        for idea in missing_lessons[:10]:  # Show first 10
            print(f"  {idea['domain']:15s} [{idea['order_index']:3d}]: {idea['title']}")

if __name__ == "__main__":
    check_tagging()
