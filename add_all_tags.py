"""
Add all system tags to database - Unicode-safe version
"""

import sqlite3
from pathlib import Path
import uuid
from datetime import datetime

def add_all_tags():
    """Add all system tags to the database"""

    db_path = Path(__file__).parent / "cyberlearn.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Create tags table if not exists
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

        # Create lesson_tags junction table
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

        # Create indices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lesson_tags_lesson
            ON lesson_tags(lesson_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lesson_tags_tag
            ON lesson_tags(tag_id)
        """)

        print("=" * 60)
        print("ADDING ALL SYSTEM TAGS")
        print("=" * 60)

        # Define all tags
        default_tags = [
            # Content Tags
            {
                "name": "Built-In",
                "color": "#3B82F6",
                "icon": "[BI]",
                "description": "Core platform lessons included by default",
                "is_system": 1
            },
            {
                "name": "User Content",
                "color": "#6B7280",
                "icon": "[UC]",
                "description": "User-created or imported lessons",
                "is_system": 0
            },
            {
                "name": "Community",
                "color": "#EC4899",
                "icon": "[CM]",
                "description": "Community-contributed lessons",
                "is_system": 0
            },
            # Career Path Tags
            {
                "name": "Career Path: SOC Tier 1",
                "color": "#06B6D4",
                "icon": "[S1]",
                "description": "Security Operations Center Tier 1 Analyst career path",
                "is_system": 1
            },
            {
                "name": "Career Path: SOC Tier 2",
                "color": "#0891B2",
                "icon": "[S2]",
                "description": "Security Operations Center Tier 2 Analyst career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Incident Responder",
                "color": "#DC2626",
                "icon": "[IR]",
                "description": "Incident Response Specialist career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Threat Hunter",
                "color": "#7C3AED",
                "icon": "[TH]",
                "description": "Threat Hunting Specialist career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Forensic Analyst",
                "color": "#059669",
                "icon": "[FA]",
                "description": "Digital Forensics Analyst career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Malware Analyst",
                "color": "#B91C1C",
                "icon": "[MA]",
                "description": "Malware Reverse Engineering Analyst career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Penetration Tester",
                "color": "#CA8A04",
                "icon": "[PT]",
                "description": "Penetration Testing / Ethical Hacking career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Red Team Operator",
                "color": "#BE123C",
                "icon": "[RT]",
                "description": "Red Team Operations career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Security Engineer",
                "color": "#4F46E5",
                "icon": "[SE]",
                "description": "Security Engineering career path",
                "is_system": 1
            },
            {
                "name": "Career Path: Cloud Security",
                "color": "#0D9488",
                "icon": "[CS]",
                "description": "Cloud Security Specialist career path",
                "is_system": 1
            },
            # Package Tags
            {
                "name": "Package: Eric Zimmerman Tools",
                "color": "#F59E0B",
                "icon": "[EZ]",
                "description": "Lessons focused on Eric Zimmerman's forensic tool suite",
                "is_system": 1
            },
            {
                "name": "Package: APT",
                "color": "#7C2D12",
                "icon": "[APT]",
                "description": "Advanced Persistent Threat campaigns and techniques",
                "is_system": 1
            }
        ]

        now = datetime.utcnow().isoformat()
        added_count = 0
        skipped_count = 0

        for tag in default_tags:
            try:
                cursor.execute("""
                    INSERT INTO tags (tag_id, name, color, icon, description, created_at, is_system)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    tag["name"],
                    tag["color"],
                    tag["icon"],
                    tag["description"],
                    now,
                    tag["is_system"]
                ))
                print(f"  [OK] Added: {tag['icon']} {tag['name']}")
                added_count += 1
            except sqlite3.IntegrityError:
                print(f"  [SKIP] Exists: {tag['name']}")
                skipped_count += 1

        conn.commit()

        # Count total tags
        cursor.execute("SELECT COUNT(*) FROM tags")
        total_tags = cursor.fetchone()[0]

        print("\n" + "=" * 60)
        print("[SUCCESS] TAG SYSTEM READY")
        print("=" * 60)
        print(f"Added: {added_count} tags")
        print(f"Skipped: {skipped_count} tags")
        print(f"Total: {total_tags} tags in database")
        print("\nTag Categories:")
        print("  - Content Tags: 3")
        print("  - Career Paths: 10")
        print("  - Package Tags: 2")

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_all_tags()
