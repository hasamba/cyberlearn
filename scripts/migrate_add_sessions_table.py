"""
Database migration: Add user_sessions table for cookie-based authentication
"""

import sqlite3
from pathlib import Path

def migrate_database(db_path="cyberlearn.db"):
    """Add user_sessions table if it doesn't exist"""
    print(f"Migrating database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table already exists
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='user_sessions'
    """)

    if cursor.fetchone():
        print("✓ user_sessions table already exists")
        conn.close()
        return

    # Create user_sessions table
    print("Creating user_sessions table...")
    cursor.execute("""
        CREATE TABLE user_sessions (
            session_token TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            last_accessed TEXT NOT NULL,
            user_agent TEXT,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # Create index for user_id lookup
    cursor.execute("""
        CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id)
    """)

    # Create index for expires_at for cleanup queries
    cursor.execute("""
        CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at)
    """)

    conn.commit()
    print("✓ user_sessions table created successfully")

    # Verify table structure
    cursor.execute("PRAGMA table_info(user_sessions)")
    columns = cursor.fetchall()
    print("\nTable structure:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

    conn.close()
    print("\nMigration complete!")

if __name__ == "__main__":
    # Migrate working database
    if Path("cyberlearn.db").exists():
        migrate_database("cyberlearn.db")
    else:
        print("⚠ cyberlearn.db not found")

    # Migrate template database
    if Path("cyberlearn_template.db").exists():
        print("\n" + "=" * 50)
        migrate_database("cyberlearn_template.db")
    else:
        print("\n⚠ cyberlearn_template.db not found")
