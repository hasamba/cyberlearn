"""
Quick script to check if UI preferences migration has been applied.
"""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "cyberlearn.db"

if not db_path.exists():
    print(f"❌ Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check columns
cursor.execute("PRAGMA table_info(users)")
columns = {row[1]: row[2] for row in cursor.fetchall()}

print("="*60)
print("Database Migration Status Check")
print("="*60)

has_last_username = 'last_username' in columns
has_preferred_tags = 'preferred_tag_filters' in columns

print(f"\n✓ last_username column: {'✅ EXISTS' if has_last_username else '❌ MISSING'}")
print(f"✓ preferred_tag_filters column: {'✅ EXISTS' if has_preferred_tags else '❌ MISSING'}")

if has_last_username and has_preferred_tags:
    print("\n" + "="*60)
    print("✅ MIGRATION COMPLETED - Persistence is enabled!")
    print("="*60)

    # Check if any users have saved preferences
    cursor.execute("SELECT COUNT(*) FROM users WHERE last_username IS NOT NULL")
    users_with_username = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE preferred_tag_filters != '[]'")
    users_with_tags = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    print(f"\nTotal users: {total_users}")
    print(f"Users with saved username: {users_with_username}")
    print(f"Users with tag preferences: {users_with_tags}")

    print("\nUsername and tag preferences WILL persist across browser refreshes.")
else:
    print("\n" + "="*60)
    print("❌ MIGRATION NOT COMPLETE")
    print("="*60)
    print("\nRun: python add_ui_preferences.py")

conn.close()
