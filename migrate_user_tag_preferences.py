#!/usr/bin/env python3
"""
Migrate user tag preferences to match renamed tags.

This script updates users' preferred_tag_filters to use the new tag names:
- Beginner → Level: Beginner
- Intermediate → Level: Intermediate
- Expert → Level: Expert
- ⭐ Beginner → Level: Beginner
- etc.

Run this after renaming tags to fix user preferences.
"""

import sqlite3
import json
from pathlib import Path

def migrate_tag_preferences():
    """Update user tag preferences to match new tag names"""

    db_path = Path(__file__).parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("=" * 60)
        print("MIGRATING USER TAG PREFERENCES")
        print("=" * 60)

        # Mapping of old tag names to new tag names
        tag_mapping = {
            # Difficulty tags
            "Beginner": "Level: Beginner",
            "⭐ Beginner": "Level: Beginner",
            "Level: ⭐ Beginner": "Level: Beginner",
            "Intermediate": "Level: Intermediate",
            "⭐⭐ Intermediate": "Level: Intermediate",
            "Level: ⭐⭐ Intermediate": "Level: Intermediate",
            "Expert": "Level: Expert",
            "⭐⭐⭐ Expert": "Level: Expert",
            "Level: ⭐⭐⭐ Expert": "Level: Expert",
            # Career path tags (in case some users had old names)
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
            # Package tags
            "Eric Zimmerman Tools": "Package: Eric Zimmerman Tools",
            "APT": "Package: APT"
        }

        # Get all users with tag preferences
        cursor.execute("""
            SELECT user_id, username, preferred_tag_filters
            FROM users
            WHERE preferred_tag_filters IS NOT NULL
            AND preferred_tag_filters != '[]'
        """)
        users = cursor.fetchall()

        if not users:
            print("\nNo users with tag preferences found.")
            print("✓ Nothing to migrate")
            return True

        print(f"\nFound {len(users)} users with tag preferences")
        print("\nMigrating tag preferences...")

        updated_count = 0
        for user_id, username, tag_filters_json in users:
            try:
                # Parse JSON
                tag_filters = json.loads(tag_filters_json)

                if not tag_filters:
                    continue

                # Update tag names
                updated_filters = []
                changed = False

                for tag_name in tag_filters:
                    if tag_name in tag_mapping:
                        new_name = tag_mapping[tag_name]
                        updated_filters.append(new_name)
                        changed = True
                        print(f"  User '{username}': '{tag_name}' → '{new_name}'")
                    else:
                        # Keep unchanged if not in mapping
                        updated_filters.append(tag_name)

                # Update database if changed
                if changed:
                    new_json = json.dumps(updated_filters)
                    cursor.execute("""
                        UPDATE users
                        SET preferred_tag_filters = ?
                        WHERE user_id = ?
                    """, (new_json, user_id))
                    updated_count += 1

            except json.JSONDecodeError:
                print(f"  ⚠ Warning: Invalid JSON for user {username}, skipping")
                continue

        conn.commit()

        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETED!")
        print("=" * 60)
        print(f"\nUsers checked: {len(users)}")
        print(f"Users updated: {updated_count}")
        print(f"Users unchanged: {len(users) - updated_count}")

        print("\nNext steps:")
        print("  1. Test app: streamlit run app.py")
        print("  2. Tag filters should now work without errors")

        return True

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    success = migrate_tag_preferences()
    sys.exit(0 if success else 1)
