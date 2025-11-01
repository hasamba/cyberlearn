#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore Content tags from v1.4 (Built-In, User Content, Community)
"""

import sqlite3
import sys
import uuid
from pathlib import Path
from datetime import datetime

# Fix unicode output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = Path(__file__).parent / "cyberlearn.db"


def restore_content_tags():
    """Restore Content tags from v1.4"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("RESTORING CONTENT TAGS FROM V1.4")
    print("=" * 60)
    print(f"Database: {DB_PATH}\n")

    # Define Content tags from v1.4
    content_tags = [
        {
            "name": "Built-In",
            "category": "Content",
            "color": "#3B82F6",
            "icon": "🔵",
            "description": "Core platform lessons included by default",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "User Content",
            "category": "Content",
            "color": "#6B7280",
            "icon": "⚪",
            "description": "User-created or imported lessons",
            "is_system": 0,
            "user_id": None
        },
        {
            "name": "Community",
            "category": "Content",
            "color": "#EC4899",
            "icon": "🩷",
            "description": "Community-contributed lessons",
            "is_system": 0,
            "user_id": None
        }
    ]

    now = datetime.utcnow().isoformat()
    added_count = 0
    skipped_count = 0

    for tag in content_tags:
        try:
            # Check if tag already exists
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag["name"],))
            existing = cursor.fetchone()

            if existing:
                print(f"  ✓ {tag['icon']} {tag['name']} - Already exists")
                skipped_count += 1
            else:
                cursor.execute("""
                    INSERT INTO tags (id, name, category, color, icon, description, created_at, is_system, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    tag["name"],
                    tag["category"],
                    tag["color"],
                    tag["icon"],
                    tag["description"],
                    now,
                    tag["is_system"],
                    tag["user_id"]
                ))
                print(f"  ✅ {tag['icon']} {tag['name']} - Added")
                added_count += 1

        except Exception as e:
            print(f"  ❌ Error adding {tag['name']}: {e}")

    conn.commit()

    # Show summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Added: {added_count}")
    print(f"Skipped: {skipped_count}")

    # Verify all tags in database
    cursor.execute("SELECT category, COUNT(*) FROM tags GROUP BY category ORDER BY category")
    print("\nAll tags in database:")
    total = 0
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} tags")
        total += row[1]
    print(f"\nTotal: {total} tags")

    conn.close()

    if added_count > 0:
        print("\n✅ Content tags restored successfully!")
        print("\nNext steps:")
        print("  1. Update template database: python update_template_database.py")
        print("  2. Commit and push changes")
    else:
        print("\n✅ All content tags already present!")


if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        exit(1)

    restore_content_tags()
