#!/usr/bin/env python3
"""Reload the ShimCache lesson to update the video text in the database"""
import json
import sqlite3
from pathlib import Path

# Database path
db_path = Path("cyberlearn.db")

# Lesson file
lesson_file = Path("content/lesson_dfir_17_shimcache_forensics_RICH.json")

print("=" * 80)
print("Reloading ShimCache Lesson")
print("=" * 80)

# Read the lesson JSON
print(f"\n1. Reading lesson from: {lesson_file}")
with open(lesson_file, 'r', encoding='utf-8') as f:
    lesson_data = json.load(f)

lesson_id = lesson_data['lesson_id']
print(f"   Lesson ID: {lesson_id}")
print(f"   Title: {lesson_data['title']}")

# Connect to database
print(f"\n2. Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if lesson exists
cursor.execute("SELECT lesson_id, title FROM lessons WHERE lesson_id = ?", (lesson_id,))
existing = cursor.fetchone()

if existing:
    print(f"   Found existing lesson: {existing[1]}")
    print(f"   Updating lesson content...")

    # Update the lesson
    cursor.execute("""
        UPDATE lessons
        SET content_blocks = ?
        WHERE lesson_id = ?
    """, (json.dumps(lesson_data['content_blocks']), lesson_id))

    conn.commit()
    print(f"   ✓ Updated successfully!")
else:
    print(f"   Lesson not found in database!")
    print(f"   Loading lesson for the first time...")

    # Insert the lesson
    cursor.execute("""
        INSERT INTO lessons (
            lesson_id, domain, title, difficulty, order_index,
            prerequisites, concepts, estimated_time, learning_objectives,
            content_blocks, post_assessment, jim_kwik_principles
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lesson_id,
        lesson_data['domain'],
        lesson_data['title'],
        lesson_data['difficulty'],
        lesson_data['order_index'],
        json.dumps(lesson_data['prerequisites']),
        json.dumps(lesson_data['concepts']),
        lesson_data['estimated_time'],
        json.dumps(lesson_data['learning_objectives']),
        json.dumps(lesson_data['content_blocks']),
        json.dumps(lesson_data['post_assessment']),
        json.dumps(lesson_data['jim_kwik_principles'])
    ))

    conn.commit()
    print(f"   ✓ Loaded successfully!")

# Verify the update
cursor.execute("SELECT content_blocks FROM lessons WHERE lesson_id = ?", (lesson_id,))
result = cursor.fetchone()
if result:
    content_blocks = json.loads(result[0])

    # Find video block
    for block in content_blocks:
        if block['type'] == 'video':
            text = block['content']['text']
            print(f"\n3. Verification:")
            print(f"   Video text first 100 chars: {text[:100]}")
            print(f"   Contains newlines: {chr(10) in text}")
            print(f"   Newline count: {text.count(chr(10))}")
            break

conn.close()

print("\n" + "=" * 80)
print("DONE! Please restart Streamlit to see the changes.")
print("=" * 80)
