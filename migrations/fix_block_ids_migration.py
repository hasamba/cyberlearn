"""
Migration: Fix invalid block IDs in lessons.
Converts string block_ids to valid UUIDs.

Run this on VM after pulling latest code.
"""

import sqlite3
import json
import uuid
import sys
from pathlib import Path

def fix_block_ids():
    """Fix invalid block IDs in the database."""

    # Try to find the database
    db_path = Path('cyberlearn.db')
    if not db_path.exists():
        db_path = Path('/opt/cyberlearn/cyberlearn.db')
    if not db_path.exists():
        print("ERROR: Could not find cyberlearn.db")
        sys.exit(1)

    print(f"Using database: {db_path}")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find lessons with invalid block IDs
    cursor.execute("SELECT lesson_id, title, domain, content_blocks FROM lessons")

    fixed_count = 0
    total_blocks_fixed = 0

    for row in cursor.fetchall():
        lesson_id = row['lesson_id']
        title = row['title']
        domain = row['domain']
        content_blocks_json = row['content_blocks']

        try:
            content_blocks = json.loads(content_blocks_json)
        except:
            print(f"[ERROR] Could not parse JSON for lesson: {title}")
            continue

        changed = False
        blocks_fixed = 0

        for block in content_blocks:
            if 'block_id' in block:
                block_id = block['block_id']
                try:
                    # Try to validate as UUID
                    uuid.UUID(block_id)
                except (ValueError, AttributeError):
                    # Invalid UUID, generate a new one
                    old_id = block_id
                    new_id = str(uuid.uuid4())
                    block['block_id'] = new_id
                    changed = True
                    blocks_fixed += 1

        if changed:
            # Update the database
            new_json = json.dumps(content_blocks, ensure_ascii=False)
            cursor.execute(
                "UPDATE lessons SET content_blocks = ? WHERE lesson_id = ?",
                (new_json, lesson_id)
            )
            fixed_count += 1
            total_blocks_fixed += blocks_fixed
            print(f"[FIXED] {domain} - {title} ({blocks_fixed} blocks)")

    conn.commit()
    conn.close()

    print("\n" + "=" * 80)
    print(f"Migration complete!")
    print(f"  - Fixed {fixed_count} lessons")
    print(f"  - Fixed {total_blocks_fixed} content blocks")
    print("=" * 80)

if __name__ == "__main__":
    print("=" * 80)
    print("MIGRATION: Fix Invalid Block IDs")
    print("=" * 80)
    print()

    fix_block_ids()
