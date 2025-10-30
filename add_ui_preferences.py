"""
Database migration script to add UI preference fields to users table.

This script adds:
- last_username: VARCHAR - Last username entered (for login convenience)
- preferred_tag_filters: TEXT - JSON array of preferred tag names

These fields enable persistence of UI preferences across browser sessions.

Usage:
    python add_ui_preferences.py
"""

import sqlite3
from pathlib import Path
import json

def add_ui_preferences():
    """Add UI preference columns to users table."""

    db_path = Path(__file__).parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Adding UI preference columns to users table...")

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]

        # Add last_username column if it doesn't exist
        if 'last_username' not in columns:
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN last_username TEXT
            """)
            print("  ✓ Added column: last_username")
        else:
            print("  → Column 'last_username' already exists")

        # Add preferred_tag_filters column if it doesn't exist
        if 'preferred_tag_filters' not in columns:
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN preferred_tag_filters TEXT DEFAULT '[]'
            """)
            print("  ✓ Added column: preferred_tag_filters")

            # Initialize all existing users with default Beginner tag preference
            print("\nInitializing default tag preferences for existing users...")

            # Check if Beginner tag exists (try both old and new names)
            cursor.execute("SELECT name FROM tags WHERE name IN ('Beginner', 'Level: ⭐ Beginner') LIMIT 1")
            beginner_tag = cursor.fetchone()

            if beginner_tag:
                default_filters = json.dumps([beginner_tag[0]])
                cursor.execute("""
                    UPDATE users
                    SET preferred_tag_filters = ?
                    WHERE preferred_tag_filters IS NULL OR preferred_tag_filters = '[]'
                """, (default_filters,))
                updated_count = cursor.rowcount
                print(f"  ✓ Set 'Beginner' as default for {updated_count} users")
            else:
                print("  → No 'Beginner' tag found, users will have empty preferences")
        else:
            print("  → Column 'preferred_tag_filters' already exists")

        conn.commit()

        # Verify columns added
        cursor.execute("PRAGMA table_info(users)")
        columns_after = [row[1] for row in cursor.fetchall()]

        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        print("\n" + "="*60)
        print("✅ UI preferences migration completed successfully!")
        print("="*60)
        print(f"Columns in users table: {len(columns_after)}")
        print(f"Total users: {user_count}")
        print("\nNew Features:")
        print("  • last_username - Login form pre-fill (convenience)")
        print("  • preferred_tag_filters - Tag selection persistence")
        print("\nBehavior:")
        print("  • Username remembered across browser sessions")
        print("  • Tag filters persist across browser refreshes")
        print("  • New users default to 'Beginner' tag filter")
        print("\nNext steps:")
        print("1. Restart the app: streamlit run app.py")
        print("2. Login - username will be remembered")
        print("3. Select tags - preferences will persist")
        print("4. Refresh browser - settings remain!")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_ui_preferences()
