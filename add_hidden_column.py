"""
Add 'hidden' column to lessons table for hide/unhide functionality
"""

import sqlite3

def add_hidden_column(db_path: str = "cyberlearn.db"):
    """Add hidden boolean column to lessons table"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("ADDING HIDDEN COLUMN TO LESSONS")
    print("=" * 60)

    # Check if column exists
    cursor.execute("PRAGMA table_info(lessons)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'hidden' in columns:
        print("\n[OK] 'hidden' column already exists")
        conn.close()
        return True

    # Add hidden column
    cursor.execute("ALTER TABLE lessons ADD COLUMN hidden BOOLEAN DEFAULT 0")
    conn.commit()

    print("\n[OK] Added 'hidden' column to lessons table")
    print("  - Default value: FALSE (0)")
    print("  - Type: BOOLEAN")

    # Verify
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE hidden = 1")
    hidden_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM lessons")
    total_count = cursor.fetchone()[0]

    print(f"\nCurrent status:")
    print(f"  Hidden lessons: {hidden_count}")
    print(f"  Visible lessons: {total_count - hidden_count}")
    print(f"  Total lessons: {total_count}")

    print("\n" + "=" * 60)
    print("[SUCCESS] Hidden column added")
    print("=" * 60)

    conn.close()
    return True

if __name__ == "__main__":
    add_hidden_column()
