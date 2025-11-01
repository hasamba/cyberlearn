#!/usr/bin/env python3
"""
Add assessment_questions and user_assessments tables to existing database.

This migration script adds the assessment system tables to databases
that don't have them yet.
"""

import sqlite3
from pathlib import Path


def add_assessment_tables():
    """Add assessment tables to existing database"""
    db_path = Path("cyberlearn.db")

    if not db_path.exists():
        print("ERROR Database not found at cyberlearn.db")
        print("Please run the app first to create the database.")
        return False

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    print("=" * 60)
    print("ADDING ASSESSMENT TABLES")
    print("=" * 60)

    # Check if assessment_questions table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assessment_questions'")
    has_questions_table = cursor.fetchone() is not None

    # Check if user_assessments table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_assessments'")
    has_assessments_table = cursor.fetchone() is not None

    if has_questions_table and has_assessments_table:
        print("\nOK Assessment tables already exist.")
        print("  - assessment_questions: EXISTS")
        print("  - user_assessments: EXISTS")
        print("\nNo migration needed.")
        conn.close()
        return True

    # Create assessment_questions table
    if not has_questions_table:
        print("\nCreating assessment_questions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessment_questions (
                question_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                question_text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer INTEGER NOT NULL,
                difficulty INTEGER NOT NULL,
                explanation TEXT,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_assessment_questions_domain
            ON assessment_questions(domain)
        """)

        print("  OK assessment_questions table created")
    else:
        print("\n  SKIP assessment_questions table already exists")

    # Create user_assessments table
    if not has_assessments_table:
        print("\nCreating user_assessments table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_assessments (
                assessment_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                assessment_date TEXT NOT NULL,
                domain_scores TEXT NOT NULL,
                total_score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_assessments_user
            ON user_assessments(user_id)
        """)

        print("  OK user_assessments table created")
    else:
        print("\n  SKIP user_assessments table already exists")

    conn.commit()

    print("\n" + "=" * 60)
    print("SUCCESS ASSESSMENT TABLES ADDED!")
    print("=" * 60)
    print("\nNext step: Run populate_assessment_questions.py to add questions")
    print("  python populate_assessment_questions.py")

    conn.close()
    return True


if __name__ == "__main__":
    import sys
    success = add_assessment_tables()
    sys.exit(0 if success else 1)
