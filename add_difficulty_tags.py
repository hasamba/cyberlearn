"""
Database migration script to add difficulty level tags.

This script adds:
- Beginner (difficulty 1) tag
- Intermediate (difficulty 2) tag
- Advanced (difficulty 3) tag

Then auto-tags all existing lessons based on their difficulty field.

Usage:
    python add_difficulty_tags.py
"""

import sqlite3
from pathlib import Path
import uuid
from datetime import datetime

def add_difficulty_tags():
    """Add difficulty level tags and auto-tag existing lessons."""

    db_path = Path(__file__).parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Adding difficulty level tags...")

        difficulty_tags = [
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Beginner",
                "color": "#22C55E",  # Green
                "icon": "⭐",
                "description": "Beginner-friendly lessons (difficulty 1)",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Intermediate",
                "color": "#F59E0B",  # Orange
                "icon": "⭐⭐",
                "description": "Intermediate difficulty lessons (difficulty 2)",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Expert",
                "color": "#EF4444",  # Red
                "icon": "⭐⭐⭐",
                "description": "Advanced/Expert difficulty lessons (difficulty 3)",
                "is_system": 1
            }
        ]

        now = datetime.utcnow().isoformat()

        # Insert difficulty tags
        for tag in difficulty_tags:
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

        # Auto-tag lessons based on difficulty field
        print("\nAuto-tagging lessons by difficulty...")

        # Get tag IDs
        cursor.execute("SELECT tag_id FROM tags WHERE name = 'Beginner'")
        beginner_tag = cursor.fetchone()
        cursor.execute("SELECT tag_id FROM tags WHERE name = 'Intermediate'")
        intermediate_tag = cursor.fetchone()
        cursor.execute("SELECT tag_id FROM tags WHERE name = 'Expert'")
        expert_tag = cursor.fetchone()

        if beginner_tag and intermediate_tag and expert_tag:
            beginner_tag_id = beginner_tag[0]
            intermediate_tag_id = intermediate_tag[0]
            expert_tag_id = expert_tag[0]

            # Get all lessons with their difficulty
            cursor.execute("SELECT lesson_id, difficulty FROM lessons")
            lessons = cursor.fetchall()

            beginner_count = 0
            intermediate_count = 0
            expert_count = 0

            for lesson_id, difficulty in lessons:
                # Determine which tag to apply
                if difficulty == 1:
                    tag_id = beginner_tag_id
                    beginner_count += 1
                elif difficulty == 2:
                    tag_id = intermediate_tag_id
                    intermediate_count += 1
                elif difficulty == 3:
                    tag_id = expert_tag_id
                    expert_count += 1
                else:
                    continue

                try:
                    cursor.execute("""
                        INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                        VALUES (?, ?, ?)
                    """, (lesson_id, tag_id, now))
                except sqlite3.IntegrityError:
                    pass  # Already tagged

            print(f"  ✓ Tagged {beginner_count} lessons as Beginner")
            print(f"  ✓ Tagged {intermediate_count} lessons as Intermediate")
            print(f"  ✓ Tagged {expert_count} lessons as Expert")

        conn.commit()

        # Verify
        cursor.execute("SELECT COUNT(*) FROM tags WHERE name IN ('Beginner', 'Intermediate', 'Expert')")
        difficulty_tag_count = cursor.fetchone()[0]

        print("\n" + "="*60)
        print("✅ Difficulty tag migration completed successfully!")
        print("="*60)
        print(f"Difficulty tags added: {difficulty_tag_count}")
        print("\nTag Details:")
        print("  ⭐ Beginner (Green) - Difficulty 1 lessons")
        print("  ⭐⭐ Intermediate (Orange) - Difficulty 2 lessons")
        print("  ⭐⭐⭐ Expert (Red) - Difficulty 3 lessons")
        print("\nNext steps:")
        print("1. Difficulty tags are now available for filtering")
        print("2. New users will see Beginner tag selected by default")
        print("3. Tag preferences persist across sessions")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_difficulty_tags()
