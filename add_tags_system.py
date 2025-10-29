"""
Database migration script to add tag-based lesson organization system.

This script adds:
1. tags table - stores tag definitions (name, color, icon, description)
2. lesson_tags table - many-to-many junction table linking lessons to tags

Usage:
    python add_tags_system.py

After running, lessons can have multiple colored tags for organization.
"""

import sqlite3
from pathlib import Path
import uuid
from datetime import datetime

def add_tags_system():
    """Add tags and lesson_tags tables to the database."""

    db_path = Path(__file__).parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Create tags table
        print("Creating tags table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                tag_id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                color TEXT NOT NULL,
                icon TEXT,
                description TEXT,
                created_at TEXT NOT NULL,
                is_system INTEGER DEFAULT 0
            )
        """)

        # Create lesson_tags junction table (many-to-many)
        print("Creating lesson_tags table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lesson_tags (
                lesson_id TEXT NOT NULL,
                tag_id TEXT NOT NULL,
                added_at TEXT NOT NULL,
                PRIMARY KEY (lesson_id, tag_id),
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
            )
        """)

        # Create indices for performance
        print("Creating indices...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lesson_tags_lesson
            ON lesson_tags(lesson_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lesson_tags_tag
            ON lesson_tags(tag_id)
        """)

        # Insert default system tags
        print("Adding default system tags...")
        default_tags = [
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Built-In",
                "color": "#3B82F6",  # Blue
                "icon": "🔵",
                "description": "Core platform lessons included by default",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Advanced",
                "color": "#8B5CF6",  # Purple
                "icon": "🟣",
                "description": "Advanced difficulty lessons for experienced users",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "PWK Course",
                "color": "#EF4444",  # Red
                "icon": "🔴",
                "description": "Offensive Security PWK/OSCP course aligned lessons",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Eric Zimmerman Tools",
                "color": "#F59E0B",  # Orange
                "icon": "🟠",
                "description": "Lessons focused on Eric Zimmerman's forensic tool suite",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "SANS-Aligned",
                "color": "#10B981",  # Green
                "icon": "🟢",
                "description": "Lessons aligned with SANS course content and methodology",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "User Content",
                "color": "#6B7280",  # Gray
                "icon": "⚪",
                "description": "User-created or imported lessons",
                "is_system": 0
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Community",
                "color": "#EC4899",  # Pink
                "icon": "🩷",
                "description": "Community-contributed lessons",
                "is_system": 0
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Certification Prep",
                "color": "#14B8A6",  # Teal
                "icon": "🏆",
                "description": "Lessons aligned with industry certifications",
                "is_system": 1
            },
            # Career Path Tags
            {
                "tag_id": str(uuid.uuid4()),
                "name": "SOC Tier 1",
                "color": "#06B6D4",  # Cyan
                "icon": "🛡️",
                "description": "Security Operations Center Tier 1 Analyst career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "SOC Tier 2",
                "color": "#0891B2",  # Darker Cyan
                "icon": "🛡️",
                "description": "Security Operations Center Tier 2 Analyst career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Incident Responder",
                "color": "#DC2626",  # Dark Red
                "icon": "🚨",
                "description": "Incident Response Specialist career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Threat Hunter",
                "color": "#7C3AED",  # Violet
                "icon": "🎯",
                "description": "Threat Hunting Specialist career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Forensic Analyst",
                "color": "#059669",  # Emerald
                "icon": "🔬",
                "description": "Digital Forensics Analyst career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Malware Analyst",
                "color": "#B91C1C",  # Crimson
                "icon": "🦠",
                "description": "Malware Reverse Engineering Analyst career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Penetration Tester",
                "color": "#CA8A04",  # Gold
                "icon": "🔓",
                "description": "Penetration Testing / Ethical Hacking career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Red Team Operator",
                "color": "#BE123C",  # Rose
                "icon": "⚔️",
                "description": "Red Team Operations career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Security Engineer",
                "color": "#4F46E5",  # Indigo
                "icon": "🔧",
                "description": "Security Engineering career path",
                "is_system": 1
            },
            {
                "tag_id": str(uuid.uuid4()),
                "name": "Cloud Security",
                "color": "#0D9488",  # Teal
                "icon": "☁️",
                "description": "Cloud Security Specialist career path",
                "is_system": 1
            }
        ]

        now = datetime.utcnow().isoformat()

        for tag in default_tags:
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

        # Auto-tag existing lessons as "Built-In"
        print("\nAuto-tagging existing lessons as 'Built-In'...")
        cursor.execute("SELECT tag_id FROM tags WHERE name = 'Built-In'")
        builtin_tag = cursor.fetchone()

        if builtin_tag:
            builtin_tag_id = builtin_tag[0]
            cursor.execute("SELECT lesson_id FROM lessons")
            lessons = cursor.fetchall()

            for (lesson_id,) in lessons:
                try:
                    cursor.execute("""
                        INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                        VALUES (?, ?, ?)
                    """, (lesson_id, builtin_tag_id, now))
                except sqlite3.IntegrityError:
                    pass  # Already tagged

            print(f"  ✓ Tagged {len(lessons)} existing lessons as 'Built-In'")

        conn.commit()

        # Verify tables created
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND (name='tags' OR name='lesson_tags')
        """)
        tables = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM tags")
        tag_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lesson_tags")
        lesson_tag_count = cursor.fetchone()[0]

        print("\n" + "="*60)
        print("✅ Tag system migration completed successfully!")
        print("="*60)
        print(f"Tables created: {[t[0] for t in tables]}")
        print(f"System tags: {tag_count}")
        print(f"Lesson-tag associations: {lesson_tag_count}")
        print("\nTag Categories:")
        print("  • Content Tags: Built-In, Advanced, PWK Course, Eric Zimmerman Tools, SANS-Aligned")
        print("  • Source Tags: User Content, Community, Certification Prep")
        print("  • Career Paths: SOC Tier 1, SOC Tier 2, Incident Responder, Threat Hunter,")
        print("                  Forensic Analyst, Malware Analyst, Penetration Tester,")
        print("                  Red Team Operator, Security Engineer, Cloud Security")
        print("\nNext steps:")
        print("1. Run the app: streamlit run app.py")
        print("2. Use tag filters to organize lesson view")
        print("3. Manage tags via the new Tag Management page")
        print("4. Tag lessons with career paths for role-based learning")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_tags_system()
