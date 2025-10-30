"""
Update tag names and remove deprecated tags.

Changes:
- Remove: Advanced, PWK Course, SANS-Aligned, Certification Prep
- Rename: Career path tags (add "Career Path:" prefix)
- Rename: Eric Zimmerman Tools → Package: Eric Zimmerman Tools
- Rename: APT → Package: APT
- Remove: Course: PEN-200 (will be added as specific course tag later)

Usage:
    python update_tag_names.py
"""

import sqlite3
from pathlib import Path

def update_tag_names():
    """Update tag names and remove deprecated tags."""

    # Database is in parent directory (project root)
    db_path = Path(__file__).parent.parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("="*60)
        print("UPDATING TAG SYSTEM")
        print("="*60)

        # Tags to remove
        tags_to_remove = [
            "Advanced",
            "PWK Course",
            "SANS-Aligned",
            "Certification Prep",
            "Course: PEN-200"
        ]

        print("\n1. Removing deprecated tags...")
        for tag_name in tags_to_remove:
            # Check if tag exists
            cursor.execute("SELECT tag_id, name FROM tags WHERE name = ?", (tag_name,))
            tag = cursor.fetchone()

            if tag:
                tag_id, name = tag
                # Count lessons with this tag
                cursor.execute("SELECT COUNT(*) FROM lesson_tags WHERE tag_id = ?", (tag_id,))
                lesson_count = cursor.fetchone()[0]

                # Remove lesson associations
                cursor.execute("DELETE FROM lesson_tags WHERE tag_id = ?", (tag_id,))
                # Remove tag
                cursor.execute("DELETE FROM tags WHERE tag_id = ?", (tag_id,))

                print(f"  ✓ Removed '{name}' (had {lesson_count} lessons tagged)")
            else:
                print(f"  → '{tag_name}' not found (already removed)")

        # Tags to rename
        renames = {
            "SOC Tier 1": "Career Path: SOC Tier 1",
            "SOC Tier 2": "Career Path: SOC Tier 2",
            "Incident Responder": "Career Path: Incident Responder",
            "Threat Hunter": "Career Path: Threat Hunter",
            "Forensic Analyst": "Career Path: Forensic Analyst",
            "Malware Analyst": "Career Path: Malware Analyst",
            "Penetration Tester": "Career Path: Penetration Tester",
            "Red Team Operator": "Career Path: Red Team Operator",
            "Security Engineer": "Career Path: Security Engineer",
            "Cloud Security": "Career Path: Cloud Security",
            "Eric Zimmerman Tools": "Package: Eric Zimmerman Tools",
            "APT": "Package: APT",
            # Difficulty level tags (stars are in icon, not name)
            "Beginner": "Level: Beginner",
            "⭐ Beginner": "Level: Beginner",
            "Level: ⭐ Beginner": "Level: Beginner",
            "Intermediate": "Level: Intermediate",
            "⭐⭐ Intermediate": "Level: Intermediate",
            "Level: ⭐⭐ Intermediate": "Level: Intermediate",
            "Expert": "Level: Expert",
            "⭐⭐⭐ Expert": "Level: Expert",
            "Level: ⭐⭐⭐ Expert": "Level: Expert"
        }

        print("\n2. Renaming tags...")
        for old_name, new_name in renames.items():
            cursor.execute("SELECT tag_id FROM tags WHERE name = ?", (old_name,))
            tag = cursor.fetchone()

            if tag:
                cursor.execute("UPDATE tags SET name = ? WHERE name = ?", (new_name, old_name))
                print(f"  ✓ Renamed '{old_name}' → '{new_name}'")
            else:
                print(f"  → '{old_name}' not found (skipping)")

        conn.commit()

        # Verify results
        print("\n3. Verifying changes...")
        cursor.execute("SELECT COUNT(*) FROM tags")
        total_tags = cursor.fetchone()[0]

        cursor.execute("SELECT name FROM tags WHERE name LIKE 'Career Path:%' ORDER BY name")
        career_tags = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT name FROM tags WHERE name LIKE 'Package:%' ORDER BY name")
        package_tags = [row[0] for row in cursor.fetchall()]

        print("\n" + "="*60)
        print("✅ TAG UPDATE COMPLETED!")
        print("="*60)
        print(f"\nTotal tags: {total_tags}")
        print(f"\nCareer Path tags ({len(career_tags)}):")
        for tag in career_tags:
            print(f"  • {tag}")

        print(f"\nPackage tags ({len(package_tags)}):")
        for tag in package_tags:
            print(f"  • {tag}")

        print("\nRemaining content tags:")
        cursor.execute("""
            SELECT name FROM tags
            WHERE name NOT LIKE 'Career Path:%'
            AND name NOT LIKE 'Package:%'
            AND is_system = 1
            ORDER BY name
        """)
        content_tags = [row[0] for row in cursor.fetchall()]
        for tag in content_tags:
            print(f"  • {tag}")

        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. Restart app: streamlit run app.py")
        print("2. Check Tag Management page to verify changes")
        print("3. Create specific course tags as needed (e.g., 'Course: OSCP')")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during tag update: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    update_tag_names()
