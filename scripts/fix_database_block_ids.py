#!/usr/bin/env python3
"""
Fix invalid block_ids directly in the database
"""

import sqlite3
import json
import uuid
import sys

def fix_block_ids_in_database(db_path="cyberlearn.db"):
    """Fix all invalid block_ids in the database"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Fixing block_ids in database: {db_path}\n")

    # Get all lessons with their content_blocks
    cursor.execute("SELECT lesson_id, title, content_blocks FROM lessons")
    lessons = cursor.fetchall()

    fixed_count = 0

    for lesson_id, title, content_blocks_json in lessons:
        if not content_blocks_json:
            continue

        try:
            content_blocks = json.loads(content_blocks_json)
            modified = False

            for block in content_blocks:
                if 'block_id' in block:
                    block_id = block['block_id']
                    # Try to validate UUID
                    try:
                        uuid.UUID(block_id)
                    except (ValueError, AttributeError):
                        # Not a valid UUID, replace it
                        new_id = str(uuid.uuid4())
                        print(f"  Lesson: {title}")
                        print(f"    Replacing: {block_id} -> {new_id}")
                        block['block_id'] = new_id
                        modified = True

            # Update lesson if modified
            if modified:
                updated_json = json.dumps(content_blocks, ensure_ascii=False)
                cursor.execute(
                    "UPDATE lessons SET content_blocks = ? WHERE lesson_id = ?",
                    (updated_json, lesson_id)
                )
                fixed_count += 1
                print(f"    [FIXED] Updated in database\n")

        except json.JSONDecodeError:
            print(f"  ERROR: Could not parse content_blocks for lesson: {title}")
            continue

    conn.commit()
    conn.close()

    print(f"{'='*60}")
    print(f"Summary: Fixed {fixed_count} lessons in database")
    print(f"{'='*60}")

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "cyberlearn.db"
    fix_block_ids_in_database(db_path)
