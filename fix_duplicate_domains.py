#!/usr/bin/env python3
"""
Fix duplicate domain entries in database.
Consolidates old naming (blueteam, redteam) to new naming (blue_team, red_team).
"""

import sqlite3
from pathlib import Path

def fix_duplicate_domains():
    """Update all lessons with old domain names to new naming convention"""

    db_path = Path("cyberlearn.db")
    if not db_path.exists():
        print("ERROR: cyberlearn.db not found!")
        return False

    print("="*70)
    print("FIXING DUPLICATE DOMAIN ENTRIES")
    print("="*70)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check current state
    print("\n[*] Current domain distribution:")
    cursor.execute("""
        SELECT domain, COUNT(*) as count
        FROM lessons
        GROUP BY domain
        ORDER BY domain
    """)

    for row in cursor.fetchall():
        print(f"    {row['domain']:<20} {row['count']:>3} lessons")

    # Update blueteam -> blue_team
    print("\n[*] Updating 'blueteam' to 'blue_team'...")
    cursor.execute("""
        UPDATE lessons
        SET domain = 'blue_team'
        WHERE domain = 'blueteam'
    """)
    blueteam_updated = cursor.rowcount
    print(f"    Updated {blueteam_updated} lessons")

    # Update redteam -> red_team
    print("\n[*] Updating 'redteam' to 'red_team'...")
    cursor.execute("""
        UPDATE lessons
        SET domain = 'red_team'
        WHERE domain = 'redteam'
    """)
    redteam_updated = cursor.rowcount
    print(f"    Updated {redteam_updated} lessons")

    # Commit changes
    conn.commit()

    # Verify changes
    print("\n[*] New domain distribution:")
    cursor.execute("""
        SELECT domain, COUNT(*) as count
        FROM lessons
        GROUP BY domain
        ORDER BY domain
    """)

    for row in cursor.fetchall():
        print(f"    {row['domain']:<20} {row['count']:>3} lessons")

    conn.close()

    print("\n" + "="*70)
    print(f"SUCCESS! Updated {blueteam_updated + redteam_updated} lessons")
    print("="*70)

    return True

if __name__ == '__main__':
    fix_duplicate_domains()
