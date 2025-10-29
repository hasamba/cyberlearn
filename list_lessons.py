#!/usr/bin/env python3
"""
List all lessons in the database organized by domain.
"""

import sqlite3

def list_lessons():
    """List all lessons organized by domain"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Get all domains with lesson counts
    cursor.execute("""
        SELECT domain, COUNT(*) as count
        FROM lessons
        GROUP BY domain
        ORDER BY domain
    """)

    domains = cursor.fetchall()

    print("="*80)
    print("CYBERLEARN LESSONS DATABASE")
    print("="*80)

    total_lessons = 0

    for domain, count in domains:
        total_lessons += count

        # Get lessons for this domain
        cursor.execute("""
            SELECT order_index, title, difficulty, estimated_time
            FROM lessons
            WHERE domain = ?
            ORDER BY order_index
        """, (domain,))

        lessons = cursor.fetchall()

        print(f"\n{domain.upper()} ({count} lessons)")
        print("-" * 80)

        for order_idx, title, difficulty, est_time in lessons:
            # Use ASCII characters for Windows compatibility
            diff_icon = "*" * difficulty + "-" * (3 - difficulty)
            print(f"  {order_idx:2d}. {title[:60]:<60} [{diff_icon}] {est_time}min")

    print("\n" + "="*80)
    print(f"TOTAL: {total_lessons} lessons across {len(domains)} domains")
    print("="*80)

    # Show domains summary
    print("\nDomains Summary:")
    for domain, count in domains:
        # Use ASCII characters for Windows compatibility
        bar = "#" * (count // 2)
        print(f"  {domain:20s} {count:3d} {bar}")

    conn.close()

if __name__ == "__main__":
    list_lessons()
