#!/usr/bin/env python3
"""
Tag all lessons that don't have Course or Package tags with the Built-In tag.
Also applies career path tags based on domain.
"""

import sqlite3
from datetime import datetime, timezone

# Domain to Career Path mapping
DOMAIN_CAREER_PATHS = {
    'dfir': ['Career Path: DFIR Specialist', 'Career Path: Forensic Analyst', 'Career Path: Incident Responder'],
    'malware': ['Career Path: Malware Analyst', 'Career Path: DFIR Specialist'],
    'blue_team': ['Career Path: SOC Analyst', 'Career Path: SOC Tier 2', 'Career Path: Security Engineer'],
    'red_team': ['Career Path: Red Team Operator', 'Career Path: Penetration Tester'],
    'pentest': ['Career Path: Penetration Tester'],
    'threat_hunting': ['Career Path: Threat Hunter', 'Career Path: SOC Tier 2'],
    'cloud': ['Career Path: Cloud Security', 'Career Path: Security Engineer'],
    'osint': ['Career Path: Threat Hunter', 'Career Path: SOC Analyst'],
    'active_directory': ['Career Path: Red Team Operator', 'Career Path: Penetration Tester', 'Career Path: DFIR Specialist'],
    'system': ['Career Path: Security Engineer', 'Career Path: DFIR Specialist'],
    'linux': ['Career Path: DFIR Specialist', 'Career Path: Security Engineer'],
    'fundamentals': ['Career Path: SOC Tier 1', 'Career Path: SOC Analyst'],
    'ai_security': ['Career Path: Security Engineer'],
    'iot_security': ['Career Path: Security Engineer'],
    'web3_security': ['Career Path: Security Engineer', 'Career Path: Penetration Tester']
}

def get_tag_id(cursor, tag_name):
    """Get tag_id for a tag name"""
    cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def tag_has_lesson(cursor, lesson_id, tag_id):
    """Check if lesson already has this tag"""
    cursor.execute(
        "SELECT 1 FROM lesson_tags WHERE lesson_id = ? AND tag_id = ?",
        (lesson_id, tag_id)
    )
    return cursor.fetchone() is not None

def add_tag_to_lesson(cursor, lesson_id, tag_id):
    """Add tag to lesson"""
    if not tag_has_lesson(cursor, lesson_id, tag_id):
        cursor.execute(
            "INSERT INTO lesson_tags (lesson_id, tag_id, added_at) VALUES (?, ?, ?)",
            (lesson_id, tag_id, datetime.now(timezone.utc).isoformat())
        )
        return True
    return False

def main():
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("TAGGING BUILT-IN LESSONS AND CAREER PATHS")
    print("=" * 80)

    # Get Built-In tag ID
    builtin_tag_id = get_tag_id(cursor, "Built-In")
    if not builtin_tag_id:
        print("\n[ERROR] Built-In tag not found in database")
        print("Please run scripts/restore_all_system_tags.py first")
        conn.close()
        return

    # Get all lessons
    cursor.execute("""
        SELECT l.lesson_id, l.domain, l.title,
               GROUP_CONCAT(t.name) as tags
        FROM lessons l
        LEFT JOIN lesson_tags lt ON l.lesson_id = lt.lesson_id
        LEFT JOIN tags t ON lt.tag_id = t.id
        GROUP BY l.lesson_id
    """)

    lessons = cursor.fetchall()
    print(f"\nFound {len(lessons)} lessons in database\n")

    builtin_tagged = 0
    career_path_tagged = 0
    skipped = 0

    for lesson_id, domain, title, tags_str in lessons:
        tags = set(tags_str.split(',') if tags_str else [])
        modified = False

        # Check if lesson has Course or Package tags
        has_course_or_package = any(
            tag.startswith('Course:') or tag.startswith('Package:')
            for tag in tags
        )

        # Add Built-In tag if no Course/Package tags
        if not has_course_or_package and 'Built-In' not in tags:
            if add_tag_to_lesson(cursor, lesson_id, builtin_tag_id):
                print(f"[Built-In] {domain}: {title}")
                builtin_tagged += 1
                modified = True

        # Add career path tags based on domain
        if domain in DOMAIN_CAREER_PATHS:
            for career_path in DOMAIN_CAREER_PATHS[domain]:
                if career_path not in tags:
                    career_tag_id = get_tag_id(cursor, career_path)
                    if career_tag_id and add_tag_to_lesson(cursor, lesson_id, career_tag_id):
                        if not modified:  # Only print lesson title once
                            print(f"[Career] {domain}: {title}")
                            modified = True
                        career_path_tagged += 1

        if not modified:
            skipped += 1

    conn.commit()
    conn.close()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Built-In tags added: {builtin_tagged}")
    print(f"Career path tags added: {career_path_tagged}")
    print(f"Lessons skipped (already tagged): {skipped}")
    print(f"Total lessons processed: {len(lessons)}")

if __name__ == '__main__':
    main()
