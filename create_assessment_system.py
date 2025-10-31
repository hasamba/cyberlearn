"""
Create skill assessment system database tables and populate with questions

Database Schema:
1. assessment_questions - Diagnostic questions for each domain
2. user_assessments - Historical assessment results
3. assessment_responses - Individual question responses
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

def create_assessment_tables(db_path: str = "cyberlearn.db"):
    """Create assessment system tables"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("CREATING ASSESSMENT SYSTEM")
    print("=" * 60)

    # Table 1: Assessment Questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessment_questions (
            question_id TEXT PRIMARY KEY,
            domain TEXT NOT NULL,
            difficulty INTEGER NOT NULL,  -- 1=beginner, 2=intermediate, 3=advanced
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL,  -- multiple_choice, self_assessment, scenario
            options TEXT,  -- JSON array of options for multiple_choice
            correct_answer INTEGER,  -- Index of correct option (0-based)
            explanation TEXT,
            skill_weight INTEGER DEFAULT 1,  -- How much this question affects skill score
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("\n[OK] Created assessment_questions table")

    # Table 2: User Assessments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_assessments (
            assessment_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            assessment_date TEXT NOT NULL,
            total_questions INTEGER,
            total_correct INTEGER,
            domain_scores TEXT,  -- JSON: {"domain": score}
            skill_levels TEXT,  -- JSON: {"domain": 0-100}
            recommended_lessons TEXT,  -- JSON: [lesson_ids]
            completed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    print("[OK] Created user_assessments table")

    # Table 3: Assessment Responses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessment_responses (
            response_id TEXT PRIMARY KEY,
            assessment_id TEXT NOT NULL,
            question_id TEXT NOT NULL,
            user_answer INTEGER,  -- Index of selected option or self-assessment score
            is_correct BOOLEAN,
            time_taken INTEGER,  -- Seconds spent on question
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assessment_id) REFERENCES user_assessments(assessment_id),
            FOREIGN KEY (question_id) REFERENCES assessment_questions(question_id)
        )
    ''')
    print("[OK] Created assessment_responses table")

    conn.commit()

    print("\n" + "=" * 60)
    print("[SUCCESS] Assessment system tables created")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run populate_assessment_questions.py to add questions")
    print("  2. Test assessment flow in UI")
    print()

    conn.close()

if __name__ == "__main__":
    create_assessment_tables()
