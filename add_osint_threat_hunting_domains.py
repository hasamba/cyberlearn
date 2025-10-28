#!/usr/bin/env python3
"""
Database migration script to add OSINT and Threat Hunting domains.
Adds skill columns to users table for the new domains.
"""

import sqlite3
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.database import get_db_path

def migrate_database():
    """Add osint and threat_hunting columns to users table"""

    db_path = get_db_path()
    print(f"Connecting to database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]

        migrations_applied = []

        # Add osint column if it doesn't exist
        if 'osint' not in columns:
            print("Adding 'osint' column to users table...")
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN osint INTEGER DEFAULT 0 CHECK(osint >= 0 AND osint <= 100)
            """)
            migrations_applied.append("osint")
        else:
            print("'osint' column already exists")

        # Add threat_hunting column if it doesn't exist
        if 'threat_hunting' not in columns:
            print("Adding 'threat_hunting' column to users table...")
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN threat_hunting INTEGER DEFAULT 0 CHECK(threat_hunting >= 0 AND threat_hunting <= 100)
            """)
            migrations_applied.append("threat_hunting")
        else:
            print("'threat_hunting' column already exists")

        # Commit changes
        if migrations_applied:
            conn.commit()
            print(f"\n✅ Migration successful! Added columns: {', '.join(migrations_applied)}")
        else:
            print("\n✅ No migration needed - all columns already exist")

        # Verify columns
        cursor.execute("PRAGMA table_info(users)")
        all_columns = [col[1] for col in cursor.fetchall()]

        print("\n📊 Current user table schema:")
        domain_columns = [col for col in all_columns if col in [
            'fundamentals', 'osint', 'dfir', 'malware', 'active_directory',
            'system', 'linux', 'cloud', 'pentest', 'redteam', 'blueteam', 'threat_hunting'
        ]]
        for col in domain_columns:
            print(f"  - {col}")

        # Check if any users exist
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"\n👤 Total users in database: {user_count}")

        if user_count > 0 and migrations_applied:
            print(f"   Note: Existing users now have {', '.join(migrations_applied)} skills initialized to 0")

    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

    return True

def verify_domains():
    """Verify all 11 domains are in the database schema"""

    expected_domains = [
        'fundamentals', 'osint', 'dfir', 'malware', 'active_directory',
        'system', 'linux', 'cloud', 'pentest', 'redteam', 'blueteam', 'threat_hunting'
    ]

    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()

    missing_domains = [d for d in expected_domains if d not in columns]

    if missing_domains:
        print(f"\n⚠️  Missing domain columns: {', '.join(missing_domains)}")
        return False
    else:
        print(f"\n✅ All {len(expected_domains)} domains present in database schema!")
        return True

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
