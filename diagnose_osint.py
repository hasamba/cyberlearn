#!/usr/bin/env python3
"""
Diagnose OSINT lesson database issues.
"""

import json
import sqlite3
from pathlib import Path

def check_database():
    """Check what's actually in the database"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    print("="*60)
    print("Database Diagnostics")
    print("="*60)

    # Check total lessons
    cursor.execute("SELECT COUNT(*) FROM lessons")
    total = cursor.fetchone()[0]
    print(f"\nTotal lessons in database: {total}")

    # Check lessons by domain
    print("\nLessons by domain:")
    cursor.execute("SELECT domain, COUNT(*) FROM lessons GROUP BY domain ORDER BY domain")
    for domain, count in cursor.fetchall():
        print(f"  {domain}: {count}")

    # Check if OSINT lessons exist with different domain name
    print("\nSearching for OSINT-related lessons by title:")
    cursor.execute("SELECT lesson_id, domain, title FROM lessons WHERE title LIKE '%OSINT%' OR title LIKE '%osint%'")
    osint_lessons = cursor.fetchall()

    if osint_lessons:
        print(f"Found {len(osint_lessons)} OSINT-related lessons:")
        for lesson_id, domain, title in osint_lessons:
            print(f"  - {title}")
            print(f"    Domain: '{domain}' (type: {type(domain)})")
            print(f"    ID: {lesson_id}")
    else:
        print("  No OSINT lessons found by title search")

    # Check exact IDs from JSON files
    print("\n" + "="*60)
    print("Checking JSON file lesson_ids against database:")
    print("="*60)

    content_dir = Path('content')
    osint_files = sorted(content_dir.glob("lesson_osint_*_RICH.json"))

    for filepath in osint_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        lesson_id = data['lesson_id']
        title = data['title']
        domain = data['domain']

        print(f"\n{filepath.name}:")
        print(f"  Title: {title}")
        print(f"  Domain in JSON: '{domain}'")
        print(f"  Lesson ID: {lesson_id}")

        # Check if this ID exists in database
        cursor.execute("SELECT domain, title FROM lessons WHERE lesson_id = ?", (lesson_id,))
        result = cursor.fetchone()

        if result:
            db_domain, db_title = result
            print(f"  ✓ Found in database!")
            print(f"    DB Domain: '{db_domain}'")
            print(f"    DB Title: {db_title}")
            if db_domain != domain:
                print(f"    ⚠️ DOMAIN MISMATCH! JSON='{domain}' vs DB='{db_domain}'")
        else:
            print(f"  ✗ NOT in database")

    conn.close()

def suggest_fix():
    """Suggest the fix based on diagnostics"""
    print("\n" + "="*60)
    print("Suggested Fix:")
    print("="*60)

    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Check if lessons exist with wrong domain
    cursor.execute("""
        SELECT lesson_id, domain, title
        FROM lessons
        WHERE (title LIKE '%OSINT%' OR title LIKE '%osint%')
        AND domain != 'osint'
    """)

    wrong_domain = cursor.fetchall()

    if wrong_domain:
        print(f"\nFound {len(wrong_domain)} OSINT lessons with wrong domain:")
        for lesson_id, domain, title in wrong_domain:
            print(f"  - {title}: domain='{domain}' (should be 'osint')")

        print("\nTo fix, run:")
        print("  python fix_osint_domain.py")
    else:
        print("\nNo domain mismatch found.")
        print("The lessons might be loaded but domain value is correct.")
        print("Check if there are any special characters or whitespace in domain field.")

    conn.close()

def main():
    check_database()
    suggest_fix()

if __name__ == "__main__":
    main()
