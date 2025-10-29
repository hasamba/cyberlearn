#!/usr/bin/env python3
"""
Consolidate red_team and redteam domains into single domain.

Current situation:
- red_team: 5 lessons
- redteam: 7 lessons

Goal: Merge into single 'red_team' domain (with underscore to match other domains)
"""

import sqlite3
import json
from pathlib import Path

def analyze_domains():
    """Analyze current red team domain situation"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    print("="*70)
    print("Red Team Domain Analysis")
    print("="*70)

    for domain in ['red_team', 'redteam']:
        cursor.execute("""
            SELECT lesson_id, order_index, title, difficulty
            FROM lessons
            WHERE domain = ?
            ORDER BY order_index
        """, (domain,))

        lessons = cursor.fetchall()

        print(f"\n{domain.upper()} ({len(lessons)} lessons):")
        print("-"*70)
        for lesson_id, order_idx, title, difficulty in lessons:
            print(f"  {order_idx:2d}. {title[:50]:<50} [D{difficulty}] {lesson_id[:8]}...")

    conn.close()

def check_lesson_files():
    """Check which domain lesson files use"""
    content_dir = Path('content')

    print("\n" + "="*70)
    print("Red Team Lesson Files")
    print("="*70)

    for pattern in ['lesson_red_team_*.json', 'lesson_redteam_*.json']:
        files = sorted(content_dir.glob(pattern))
        if files:
            print(f"\n{pattern}:")
            for f in files:
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        domain = data.get('domain')
                        title = data.get('title', 'Unknown')
                        print(f"  {f.name[:45]:<45} domain='{domain}' - {title[:30]}")
                except Exception as e:
                    print(f"  {f.name}: Error - {e}")

def suggest_consolidation():
    """Suggest consolidation strategy"""
    print("\n" + "="*70)
    print("Consolidation Strategy")
    print("="*70)

    print("""
RECOMMENDATION: Consolidate into 'red_team' (with underscore)

Why 'red_team' with underscore:
- Matches existing domain naming (active_directory, blue_team, threat_hunting)
- More readable and consistent
- Python-friendly (can use as variable name)

Steps:
1. Update database: Change all 'redteam' to 'red_team'
2. Rename lesson files: lesson_redteam_* becomes lesson_red_team_*
3. Update JSON content: domain field 'redteam' becomes 'red_team'
4. Resequence order_index to avoid conflicts
5. Reload lessons into database

IMPORTANT: This script will only show analysis.
To perform consolidation, run: python consolidate_redteam_execute.py
    """)

def show_proposed_mapping():
    """Show how lessons would be renumbered after consolidation"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Get all red team lessons from both domains
    cursor.execute("""
        SELECT domain, order_index, title, lesson_id
        FROM lessons
        WHERE domain IN ('red_team', 'redteam')
        ORDER BY
            CASE WHEN domain = 'red_team' THEN 1 ELSE 2 END,
            order_index
    """)

    all_lessons = cursor.fetchall()

    print("\n" + "="*70)
    print("Proposed Consolidated Order (red_team)")
    print("="*70)

    for i, (domain, old_order, title, lesson_id) in enumerate(all_lessons, 1):
        status = "[OK]" if domain == 'red_team' else "[RENAME]"
        print(f"{i:2d}. {title[:55]:<55} {status}")

    print(f"\nTotal: {len(all_lessons)} lessons in consolidated red_team domain")

    # Check for title duplicates
    titles = [lesson[2] for lesson in all_lessons]
    duplicates = [t for t in titles if titles.count(t) > 1]
    if duplicates:
        print(f"\n[WARNING] Found duplicate titles:")
        for dup in set(duplicates):
            print(f"   - {dup}")

    conn.close()

def main():
    analyze_domains()
    check_lesson_files()
    show_proposed_mapping()
    suggest_consolidation()

if __name__ == "__main__":
    main()
