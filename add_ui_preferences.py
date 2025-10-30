"""
Add UI preferences columns to users table
- last_username: Last logged in username for auto-login
- preferred_tag_filters: JSON array of preferred tag filter selections
"""

import sqlite3
from pathlib import Path

def add_ui_preferences(db_path: str = "cyberlearn.db"):
    """Add last_username and preferred_tag_filters columns to users table"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("ADDING UI PREFERENCES TO DATABASE")
    print("=" * 60)

    try:
        # Check which columns exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]

        columns_to_add = []

        # Check last_username column
        if 'last_username' not in columns:
            columns_to_add.append(('last_username', 'TEXT'))

        # Check preferred_tag_filters column
        if 'preferred_tag_filters' not in columns:
            columns_to_add.append(('preferred_tag_filters', 'TEXT'))

        if not columns_to_add:
            print("\n[OK] All UI preference columns already exist")
            print("  - last_username: EXISTS")
            print("  - preferred_tag_filters: EXISTS")
            conn.close()
            return True

        # Add missing columns
        for column_name, column_type in columns_to_add:
            print(f"\nAdding column: {column_name}")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
            print(f"  [OK] Added {column_name}")

        conn.commit()

        print("\n" + "=" * 60)
        print("[SUCCESS] UI preferences columns added successfully")
        print("=" * 60)
        print("\nThe following columns are now available:")
        print("  - last_username: Stores last logged in username")
        print("  - preferred_tag_filters: Stores user's tag filter preferences")
        print()

        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to add columns: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    success = add_ui_preferences()
    sys.exit(0 if success else 1)
