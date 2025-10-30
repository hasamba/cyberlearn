"""
Database migration script to add Course: PEN-200 and APT tags.

This script adds:
- "Course: PEN-200" tag - For Offensive Security PEN-200 aligned lessons
- "APT" tag - For Advanced Persistent Threat lessons

Usage:
    python add_course_apt_tags.py
"""

import sqlite3
from pathlib import Path
import uuid
from datetime import datetime

def add_course_apt_tags():
    """Add Course: PEN-200 and APT tags to the database."""

    db_path = Path(__file__).parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Adding Course: PEN-200 and APT tags...")

        new_tags = [
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Course: PEN-200",
                "color": "#DC2626",  # Dark Red
                "icon": "🎓",
                "description": "Offensive Security PEN-200 (OSCP) course aligned lessons",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "APT",
                "color": "#7C2D12",  # Darker Red/Brown
                "icon": "🎯",
                "description": "Advanced Persistent Threat campaigns and techniques",
                "is_system": 1
            }
        ]

        now = datetime.utcnow().isoformat()

        # Insert tags
        for tag in new_tags:
            try:
                cursor.execute("""
                    INSERT INTO tags (tag_id, name, color, icon, description, created_at, is_system)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    tag["tag_id"],
                    tag["name"],
                    tag["color"],
                    tag["icon"],
                    tag["description"],
                    now,
                    tag["is_system"]
                ))
                print(f"  ✓ Added tag: {tag['icon']} {tag['name']}")
            except sqlite3.IntegrityError:
                print(f"  → Tag '{tag['name']}' already exists, skipping")

        conn.commit()

        # Verify tags exist
        cursor.execute("SELECT COUNT(*) FROM tags WHERE name IN ('Course: PEN-200', 'APT')")
        count = cursor.fetchone()[0]

        print("\n" + "="*60)
        print("✅ Course and APT tags migration completed!")
        print("="*60)
        print(f"Tags available: {count}/2")
        print("\nNew Tags:")
        print("  🎓 Course: PEN-200 (Dark Red)")
        print("     → For Offensive Security PEN-200/OSCP lessons")
        print("  🎯 APT (Darker Red)")
        print("     → For Advanced Persistent Threat lessons")
        print("\nNext steps:")
        print("1. Run bulk tagging: python bulk_tag_lessons.py")
        print("   - Tags pentest lessons 11-30 with 'Course: PEN-200'")
        print("   - Tags red_team lessons 52-56 with 'APT'")
        print("2. Refresh app to see new tags")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_course_apt_tags()
