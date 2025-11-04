#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore Package tags that were accidentally deleted.

Package tags:
1. Package: Eric Zimmerman Tools - Lessons focused on Eric Zimmerman's forensic tool suite
2. Package: APT - Advanced Persistent Threat campaigns and techniques
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


def restore_package_tags():
    """Restore Package system tags"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("RESTORING PACKAGE TAGS")
    print("=" * 60)
    print(f"Database: {DB_PATH}\n")

    # Define Package tags
    package_tags = [
        {
            "name": "Package: Eric Zimmerman Tools",
            "category": "Package",
            "color": "#F59E0B",
            "icon": "🛠️",
            "description": "Lessons focused on Eric Zimmerman's forensic tool suite",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Package: APT",
            "category": "Package",
            "color": "#7C2D12",
            "icon": "🎯",
            "description": "Advanced Persistent Threat campaigns and techniques",
            "is_system": 1,
            "user_id": None
        }
    ]

    now = datetime.utcnow().isoformat()
    added_count = 0
    skipped_count = 0

    for tag in package_tags:
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

    # Verify tags in database
    cursor.execute("SELECT COUNT(*) FROM tags WHERE category = 'Package' AND is_system = 1")
    package_count = cursor.fetchone()[0]
    print(f"\nTotal Package tags in database: {package_count}")

    # Show all Package tags
    print("\nPackage tags:")
    cursor.execute("SELECT name, icon FROM tags WHERE category = 'Package' AND is_system = 1")
    for row in cursor.fetchall():
        print(f"  {row[1]} {row[0]}")

    conn.close()

    if added_count > 0:
        print("\n✅ Package tags restored successfully!")
        print("\nNext steps:")
        print("  1. Update template database: python update_template_database.py")
        print("  2. Commit changes: git add cyberlearn.db cyberlearn_template.db")
        print("  3. User runs on VM: bash update_vm.sh")
    else:
        print("\n✅ All Package tags already present!")


if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        exit(1)

    restore_package_tags()
