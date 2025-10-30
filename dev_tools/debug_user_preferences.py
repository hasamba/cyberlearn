"""
Debug script to show actual user preference values in database.
"""

import sqlite3
from pathlib import Path
import json

db_path = Path(__file__).parent / "cyberlearn.db"

if not db_path.exists():
    print(f"❌ Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if columns exist
cursor.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cursor.fetchall()]

if 'last_username' not in columns or 'preferred_tag_filters' not in columns:
    print("❌ Migration not run - columns don't exist")
    print("Run: python add_ui_preferences.py")
    conn.close()
    exit(1)

# Get all users with their preferences
cursor.execute("""
    SELECT
        username,
        last_username,
        preferred_tag_filters,
        last_login
    FROM users
    ORDER BY last_login DESC
""")

users = cursor.fetchall()

print("="*80)
print("USER PREFERENCES DEBUG")
print("="*80)

for username, last_username, preferred_tag_filters, last_login in users:
    print(f"\n👤 User: {username}")
    print(f"   Last Login: {last_login}")
    print(f"   Saved Username: {last_username if last_username else '(none)'}")

    try:
        tags = json.loads(preferred_tag_filters) if preferred_tag_filters else []
        print(f"   Preferred Tags: {tags if tags else '(none)'}")
    except:
        print(f"   Preferred Tags: {preferred_tag_filters}")

print("\n" + "="*80)
print("EXPECTED BEHAVIOR:")
print("="*80)
print("• last_username should be set after user logs in")
print("• preferred_tag_filters should be set when user selects tags")
print("• If all are '(none)', user hasn't logged in/selected tags yet")
print("\nTo test:")
print("1. Login as a user")
print("2. Select some tags in 'My Learning'")
print("3. Run this script again to see values saved")

conn.close()
