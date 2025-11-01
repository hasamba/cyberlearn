#!/usr/bin/env python3
"""
Migrate tags from lesson JSON files to database (FIXED VERSION).

This script handles both old and new database schemas by:
1. Checking if tags table exists
2. If it exists with old schema (tag_id column), drops and recreates with new schema
3. Extracts all unique tags from lesson JSON files
4. Creates tag records in the database
5. Creates lesson_tags associations

This ensures compatibility with existing databases.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

# Tag categories and default colors
TAG_CONFIG = {
    "Course:": {
        "category": "Course",
        "color": "#3B82F6",  # Blue
        "icon": "📚"
    },
    "Career Path:": {
        "category": "Career Path",
        "color": "#10B981",  # Green
        "icon": "💼"
    },
    "Package:": {
        "category": "Package",
        "color": "#8B5CF6",  # Purple
        "icon": "📦"
    },
    "Level:": {
        "category": "Level",
        "color": "#F59E0B",  # Orange
        "icon": "⭐"
    }
}

def get_tag_config(tag_name: str) -> dict:
    """Get tag configuration based on tag name prefix"""
    for prefix, config in TAG_CONFIG.items():
        if tag_name.startswith(prefix):
            return config

    # Default for tags without prefix
    return {
        "category": "Custom",
        "color": "#6B7280",  # Gray
        "icon": "🏷️"
    }

def check_and_recreate_tags_table(conn: sqlite3.Connection) -> bool:
    """Check tags table schema and recreate if needed"""
    cursor = conn.cursor()

    # Check if tags table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tags'")
    table_exists = cursor.fetchone() is not None

    if table_exists:
        # Check if it has the old schema (tag_id column) or new schema (id column)
        cursor.execute("PRAGMA table_info(tags)")
        columns = {row[1] for row in cursor.fetchall()}

        if 'tag_id' in columns and 'id' not in columns:
            print("⚠️  Old tags table schema detected (has 'tag_id' column)")
            print("   Dropping old tables and recreating with new schema...")

            # Drop old tables
            cursor.execute("DROP TABLE IF EXISTS lesson_tags")
            cursor.execute("DROP TABLE IF EXISTS tags")
            conn.commit()
            table_exists = False
        elif 'id' in columns:
            print("✅ Tags table already has correct schema")
            return True

    if not table_exists:
        print("Creating tags table with new schema...")

        # Tags table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tags (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                color TEXT NOT NULL,
                icon TEXT,
                is_system INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        # Lesson tags junction table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lesson_tags (
                lesson_id TEXT NOT NULL,
                tag_id TEXT NOT NULL,
                added_at TEXT NOT NULL,
                PRIMARY KEY (lesson_id, tag_id),
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
            """
        )

        # Indexes
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_lesson_tags_lesson ON lesson_tags(lesson_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_lesson_tags_tag ON lesson_tags(tag_id)"
        )

        conn.commit()
        print("✅ Tags tables created successfully")
        return False

    return True

def collect_tags_from_lessons() -> dict:
    """Collect all unique tags from lesson JSON files"""
    content_dir = Path("content")
    tag_to_lessons = {}  # tag_name -> set of lesson_ids

    lesson_files = sorted(content_dir.glob("lesson_*.json"))

    print(f"Scanning {len(lesson_files)} lesson files...")

    for filepath in lesson_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lesson = json.load(f)

            lesson_id = lesson.get("lesson_id")
            tags = lesson.get("tags", [])

            if not lesson_id:
                print(f"[WARNING] {filepath.name}: No lesson_id found, skipping")
                continue

            for tag in tags:
                if tag not in tag_to_lessons:
                    tag_to_lessons[tag] = set()
                tag_to_lessons[tag].add(lesson_id)

        except Exception as e:
            print(f"[ERROR] {filepath.name}: {e}")

    return tag_to_lessons

def create_tags_in_database(conn: sqlite3.Connection, tag_to_lessons: dict) -> dict:
    """Create tag records in database and return tag_name -> tag_id mapping"""
    cursor = conn.cursor()
    tag_id_map = {}
    created_count = 0

    print(f"\nCreating {len(tag_to_lessons)} tags in database...")

    for tag_name in sorted(tag_to_lessons.keys()):
        # Check if tag already exists
        cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
        existing = cursor.fetchone()

        if existing:
            tag_id_map[tag_name] = existing[0]
            print(f"[SKIP] {tag_name}: Already exists")
            continue

        # Get tag configuration
        config = get_tag_config(tag_name)

        # Create tag
        tag_id = str(uuid4())
        tag_id_map[tag_name] = tag_id

        cursor.execute(
            """
            INSERT INTO tags (id, name, category, color, icon, is_system, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tag_id,
                tag_name,
                config["category"],
                config["color"],
                config["icon"],
                1,  # is_system = True for all migrated tags
                datetime.now(timezone.utc).isoformat()
            )
        )
        conn.commit()

        created_count += 1
        lesson_count = len(tag_to_lessons[tag_name])
        print(f"[OK] {tag_name}: Created ({lesson_count} lessons)")

    print(f"\nCreated {created_count} new tags (skipped {len(tag_to_lessons) - created_count} existing)")
    return tag_id_map

def create_lesson_tag_associations(conn: sqlite3.Connection, tag_to_lessons: dict, tag_id_map: dict):
    """Create lesson_tags associations in database"""
    total_associations = sum(len(lessons) for lessons in tag_to_lessons.values())
    created_count = 0
    skipped_count = 0

    print(f"\nCreating {total_associations} lesson-tag associations...")

    cursor = conn.cursor()

    for tag_name, lesson_ids in tag_to_lessons.items():
        tag_id = tag_id_map[tag_name]

        for lesson_id in lesson_ids:
            # Check if association already exists
            cursor.execute(
                "SELECT 1 FROM lesson_tags WHERE lesson_id = ? AND tag_id = ?",
                (lesson_id, tag_id)
            )

            if cursor.fetchone():
                skipped_count += 1
                continue

            # Create association
            cursor.execute(
                """
                INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                VALUES (?, ?, ?)
                """,
                (lesson_id, tag_id, datetime.now(timezone.utc).isoformat())
            )
            created_count += 1

    conn.commit()

    print(f"Created {created_count} new associations (skipped {skipped_count} existing)")

def main():
    print("="*60)
    print("MIGRATING TAGS TO DATABASE (V2 - FIXED)")
    print("="*60)

    # Connect to database
    db_path = Path("cyberlearn.db")
    if not db_path.exists():
        print(f"\nError: Database not found at {db_path}")
        print("Please run 'streamlit run app.py' first to create the database")
        return

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # Check and recreate tags table if needed
    had_correct_schema = check_and_recreate_tags_table(conn)

    # Collect tags from lessons
    tag_to_lessons = collect_tags_from_lessons()

    if not tag_to_lessons:
        print("\n❌ No tags found in lesson files!")
        conn.close()
        return

    # Create tags in database
    tag_id_map = create_tags_in_database(conn, tag_to_lessons)

    # Create lesson-tag associations
    create_lesson_tag_associations(conn, tag_to_lessons, tag_id_map)

    # Summary
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Total tags: {len(tag_to_lessons)}")
    print(f"Total associations: {sum(len(lessons) for lessons in tag_to_lessons.values())}")

    # Show tag breakdown by category
    print("\nTags by category:")
    category_counts = {}
    for tag_name in tag_to_lessons.keys():
        config = get_tag_config(tag_name)
        category = config["category"]
        category_counts[category] = category_counts.get(category, 0) + 1

    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} tags")

    print("\n✅ Tags are now visible in the UI!")
    print("="*60)

    conn.close()

if __name__ == "__main__":
    main()
