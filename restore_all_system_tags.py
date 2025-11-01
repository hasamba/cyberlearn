#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore all system tags (Career Path + Package) that were accidentally deleted.

System tags:
- 10 Career Path tags (SOC Tier 1/2, Incident Responder, Threat Hunter, etc.)
- 2 Package tags (Eric Zimmerman Tools, APT)
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


def restore_system_tags():
    """Restore all Career Path and Package system tags"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("RESTORING SYSTEM TAGS")
    print("=" * 60)
    print(f"Database: {DB_PATH}\n")

    # Define all system tags
    system_tags = [
        # Career Path Tags (10)
        {
            "name": "Career Path: SOC Tier 1",
            "category": "Career Path",
            "color": "#06B6D4",
            "icon": "🛡️",
            "description": "Security Operations Center Tier 1 Analyst career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: SOC Tier 2",
            "category": "Career Path",
            "color": "#0891B2",
            "icon": "🛡️",
            "description": "Security Operations Center Tier 2 Analyst career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Incident Responder",
            "category": "Career Path",
            "color": "#DC2626",
            "icon": "🚨",
            "description": "Incident Response Specialist career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Threat Hunter",
            "category": "Career Path",
            "color": "#7C3AED",
            "icon": "🔍",
            "description": "Threat Hunting Specialist career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Forensic Analyst",
            "category": "Career Path",
            "color": "#059669",
            "icon": "🔬",
            "description": "Digital Forensics Analyst career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Malware Analyst",
            "category": "Career Path",
            "color": "#B91C1C",
            "icon": "🦠",
            "description": "Malware Reverse Engineering Analyst career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Penetration Tester",
            "category": "Career Path",
            "color": "#CA8A04",
            "icon": "⚔️",
            "description": "Penetration Testing / Ethical Hacking career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Red Team Operator",
            "category": "Career Path",
            "color": "#BE123C",
            "icon": "🔴",
            "description": "Red Team Operations career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Security Engineer",
            "category": "Career Path",
            "color": "#4F46E5",
            "icon": "🔧",
            "description": "Security Engineering career path",
            "is_system": 1,
            "user_id": None
        },
        {
            "name": "Career Path: Cloud Security",
            "category": "Career Path",
            "color": "#0D9488",
            "icon": "☁️",
            "description": "Cloud Security Specialist career path",
            "is_system": 1,
            "user_id": None
        },
        # Package Tags (2)
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

    for tag in system_tags:
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
    cursor.execute("SELECT category, COUNT(*) FROM tags WHERE is_system = 1 GROUP BY category ORDER BY category")
    print("\nSystem tags in database:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} tags")

    # Show all Career Path tags
    cursor.execute("SELECT name, icon FROM tags WHERE category = 'Career Path' ORDER BY name")
    career_tags = cursor.fetchall()
    if career_tags:
        print("\nCareer Path tags:")
        for row in career_tags:
            print(f"  {row[1]} {row[0]}")

    # Show all Package tags
    cursor.execute("SELECT name, icon FROM tags WHERE category = 'Package' ORDER BY name")
    package_tags = cursor.fetchall()
    if package_tags:
        print("\nPackage tags:")
        for row in package_tags:
            print(f"  {row[1]} {row[0]}")

    conn.close()

    if added_count > 0:
        print("\n✅ System tags restored successfully!")
        print("\nNext steps:")
        print("  1. Re-tag Eric Zimmerman Tools lessons (28 lessons)")
        print("  2. Update template database: python update_template_database.py")
        print("  3. Commit changes and push to GitHub")
    else:
        print("\n✅ All system tags already present!")


if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        exit(1)

    restore_system_tags()
