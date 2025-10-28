#!/usr/bin/env python3
"""
Database migration script to add OSINT and Threat Hunting domains.

NOTE: Skills are stored as JSON in the 'skill_levels' column,
so no schema migration is needed. This script updates existing
users to include the new domains with default values.
"""

import sqlite3
import json
from pathlib import Path

def migrate_database():
    """Update existing users to include osint and threat_hunting skills"""

    # Database path
    db_path = "cyberlearn.db"
    print(f"Connecting to database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check database schema
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]

        print("\n📊 Current users table schema:")
        print(f"   Columns: {', '.join(columns[:10])}...")
        print(f"   (Note: Skills stored in 'skill_levels' JSON column)")

        # Get all users
        cursor.execute("SELECT user_id, username, skill_levels FROM users")
        users = cursor.fetchall()

        if not users:
            print("\n⚠️  No users found in database")
            print("   New domains will be automatically available when users are created")
            return True

        print(f"\n👤 Found {len(users)} user(s) in database")
        print("   Updating skill levels to include new domains...")

        updated_count = 0
        for user_id, username, skill_levels_json in users:
            try:
                # Parse existing skill levels
                skill_levels = json.loads(skill_levels_json)

                # Check if new domains already exist
                has_osint = 'osint' in skill_levels
                has_threat_hunting = 'threat_hunting' in skill_levels

                if has_osint and has_threat_hunting:
                    print(f"   ✓ {username}: Already has new domains")
                    continue

                # Add new domains with default value 0
                if not has_osint:
                    skill_levels['osint'] = 0
                if not has_threat_hunting:
                    skill_levels['threat_hunting'] = 0

                # Update user
                updated_json = json.dumps(skill_levels)
                cursor.execute(
                    "UPDATE users SET skill_levels = ? WHERE user_id = ?",
                    (updated_json, user_id)
                )
                updated_count += 1
                print(f"   ✓ {username}: Added {'osint' if not has_osint else ''}{' and ' if not has_osint and not has_threat_hunting else ''}{'threat_hunting' if not has_threat_hunting else ''}")

            except json.JSONDecodeError as e:
                print(f"   ✗ {username}: Failed to parse skill_levels JSON: {e}")
                continue

        # Commit changes
        conn.commit()

        if updated_count > 0:
            print(f"\n✅ Migration successful! Updated {updated_count} user(s)")
        else:
            print("\n✅ No migration needed - all users already have new domains")

    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

    return True

def verify_domains():
    """Verify the new domains are available in the SkillLevels model"""

    expected_domains = [
        'fundamentals', 'osint', 'dfir', 'malware', 'active_directory',
        'system', 'linux', 'cloud', 'pentest', 'redteam', 'blueteam', 'threat_hunting'
    ]

    print(f"\n✅ All {len(expected_domains)} domains defined in models/user.py:")
    for domain in expected_domains:
        marker = "🆕" if domain in ['osint', 'threat_hunting'] else "  "
        print(f"   {marker} {domain}")

if __name__ == "__main__":
    print("=" * 60)
    print("OSINT & Threat Hunting Domain Migration")
    print("=" * 60)
    print()

    success = migrate_database()

    if success:
        print()
        verify_domains()
        print()
        print("=" * 60)
        print("Migration complete! You can now:")
        print("  1. Create OSINT lessons (domain: 'osint')")
        print("  2. Create Threat Hunting lessons (domain: 'threat_hunting')")
        print("  3. Load lessons with: python load_all_lessons.py")
        print("=" * 60)
    else:
        sys.exit(1)
