"""
Fix database and reload all lessons after prerequisite type change
"""

import os
import sys

print("=" * 60)
print("Fixing Database and Reloading Lessons")
print("=" * 60)

# Step 1: Backup database
print("\n1️⃣ Backing up database...")
if os.path.exists("cyberlearn.db"):
    import shutil
    shutil.copy("cyberlearn.db", "cyberlearn.db.backup")
    print("   ✅ Database backed up to cyberlearn.db.backup")
else:
    print("   ℹ️  No existing database found - will create fresh")

# Step 2: Delete existing database to rebuild with new schema
print("\n2️⃣ Removing old database...")
if os.path.exists("cyberlearn.db"):
    os.remove("cyberlearn.db")
    print("   ✅ Old database removed")

# Step 3: Initialize new database
print("\n3️⃣ Initializing new database...")
from utils.database import Database

db = Database()
print("   ✅ New database initialized with updated schema")

# Step 4: Generate all lessons (basic + advanced)
print("\n4️⃣ Generating basic lessons...")
os.system("python generate_lessons.py")

print("\n5️⃣ Generating advanced lessons...")
os.system("python generate_advanced_lessons.py")

# Step 5: Load all lessons
print("\n6️⃣ Loading all lessons into database...")
os.system("python load_all_lessons.py")

print("\n" + "=" * 60)
print("✅ Database fixed and lessons reloaded!")
print("=" * 60)
print("\nNext steps:")
print("1. Run: python check_database.py")
print("2. If you have a user, reset: python check_database.py reset yourusername")
print("3. Run: streamlit run app.py")
