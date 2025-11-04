#!/usr/bin/env python3
"""
Migrate tags from lesson JSON files to database.

This script:
1. Creates the tags table (if not exists)
2. Extracts all unique tags from lesson JSON files
3. Creates tag records in the database
4. Creates lesson_tags associations
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from utils.database import Database

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

def collect_tags_from_lessons() -> dict[str, set[str]]:
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

def create_tags_in_database(db: Database, tag_to_lessons: dict[str, set[str]]) -> dict[str, str]:
    """Create tag records in database and return tag_name -> tag_id mapping"""
    tag_id_map = {}
    created_count = 0

    print(f"\nCreating {len(tag_to_lessons)} tags in database...")

    for tag_name in sorted(tag_to_lessons.keys()):
        # Check if tag already exists
        existing_tag = db.get_tag_by_name(tag_name)
        if existing_tag:
            tag_id_map[tag_name] = existing_tag.tag_id
            print(f"[SKIP] {tag_name}: Already exists")
            continue

        # Get tag configuration
        config = get_tag_config(tag_name)

        # Create tag
        tag_id = str(uuid4())
        tag_id_map[tag_name] = tag_id

        cursor = db.conn.cursor()
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
                datetime.utcnow().isoformat()
            )
        )
        db.conn.commit()

        created_count += 1
        lesson_count = len(tag_to_lessons[tag_name])
        print(f"[OK] {tag_name}: Created ({lesson_count} lessons)")

    print(f"\nCreated {created_count} new tags (skipped {len(tag_to_lessons) - created_count} existing)")
    return tag_id_map

def create_lesson_tag_associations(db: Database, tag_to_lessons: dict[str, set[str]], tag_id_map: dict[str, str]):
    """Create lesson_tags associations in database"""
    total_associations = sum(len(lessons) for lessons in tag_to_lessons.values())
    created_count = 0
    skipped_count = 0

    print(f"\nCreating {total_associations} lesson-tag associations...")

    cursor = db.conn.cursor()

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
                (lesson_id, tag_id, datetime.utcnow().isoformat())
            )
            created_count += 1

    db.conn.commit()

    print(f"Created {created_count} new associations (skipped {skipped_count} existing)")

def main():
    print("="*60)
    print("MIGRATING TAGS TO DATABASE")
    print("="*60)

    # Initialize database (creates tags table if not exists)
    db = Database()

    # Collect tags from lessons
    tag_to_lessons = collect_tags_from_lessons()

    if not tag_to_lessons:
        print("\n❌ No tags found in lesson files!")
        return

    # Create tags in database
    tag_id_map = create_tags_in_database(db, tag_to_lessons)

    # Create lesson-tag associations
    create_lesson_tag_associations(db, tag_to_lessons, tag_id_map)

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

if __name__ == "__main__":
    main()
