"""
Test script to verify username is being saved correctly.
"""

import sqlite3
from pathlib import Path
from utils.database import Database
import sys

db_path = Path(__file__).parent.parent / "cyberlearn.db"

if not db_path.exists():
    print(f"❌ Database not found at {db_path}")
    exit(1)

# Get username from command line
if len(sys.argv) < 2:
    print("Usage: python test_username_save.py <username>")
    print("Example: python test_username_save.py alice")
    exit(1)

username = sys.argv[1]

print("="*60)
print(f"Testing username save for: {username}")
print("="*60)

# Initialize database
db = Database(db_path)

# Get user
print(f"\n1. Loading user '{username}' from database...")
user = db.get_user_by_username(username)

if not user:
    print(f"❌ User '{username}' not found!")
    exit(1)

print(f"✓ User found: {user.username}")
print(f"  Current last_username in object: {user.last_username}")

# Set username
print(f"\n2. Setting last_username to '{username}'...")
user.last_username = username
print(f"  Object last_username now: {user.last_username}")

# Save to database
print(f"\n3. Saving to database...")
result = db.update_user(user)
print(f"  Update result: {result}")

# Verify by reading directly from database
print(f"\n4. Verifying database value...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT last_username FROM users WHERE username = ?", (username,))
row = cursor.fetchone()

if row:
    db_value = row[0]
    print(f"  Database last_username: {db_value}")

    if db_value == username:
        print("\n" + "="*60)
        print("✅ SUCCESS! Username saved correctly!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print(f"❌ MISMATCH! Expected '{username}', got '{db_value}'")
        print("="*60)
else:
    print(f"❌ Could not read from database")

conn.close()

# Test loading again
print(f"\n5. Re-loading user to verify...")
user2 = db.get_user_by_username(username)
print(f"  Loaded last_username: {user2.last_username}")

if user2.last_username == username:
    print("\n✅ FULL VERIFICATION PASSED!")
else:
    print(f"\n❌ Verification failed: expected '{username}', got '{user2.last_username}'")
