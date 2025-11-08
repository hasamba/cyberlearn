#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update SANS course tag descriptions with proper course names.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import sqlite3
from datetime import datetime

# SANS course names mapping
SANS_COURSES = {
    "Course: SANS-FOR500": "Windows Forensic Analysis",
    "Course: SANS-FOR508": "Advanced Incident Response",
    "Course: SANS-FOR509": "Enterprise Cloud Forensics and Incident Response",
    "Course: SANS-FOR518": "Mac and iOS Forensic Analysis and Incident Response",
    "Course: SANS-FOR528": "Ransomware for Incident Responders",
    "Course: SANS-FOR572": "Advanced Network Forensics",
    "Course: SANS-FOR589": "Cybercrime Intelligence and Investigations",
    "Course: SANS-FOR608": "Enterprise-Class Incident Response & Threat Hunting",
    "Course: SANS-FOR610": "Reverse-Engineering Malware",
    "Course: SANS-SEC504": "Hacker Tools, Techniques, and Incident Handling",
}

def update_sans_descriptions():
    """Update SANS course tag descriptions"""

    conn = sqlite3.connect('cyberlearn.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=" * 70)
    print("Updating SANS Course Tag Descriptions")
    print("=" * 70)

    # Get all SANS course tags
    cursor.execute("""
        SELECT id, name, description
        FROM tags
        WHERE name LIKE 'Course: SANS-%'
        ORDER BY name
    """)

    tags = cursor.fetchall()

    if not tags:
        print("\n❌ No SANS course tags found")
        return

    print(f"\nFound {len(tags)} SANS course tag(s):\n")

    updated_count = 0

    for tag in tags:
        tag_id = tag['id']
        tag_name = tag['name']
        old_description = tag['description']

        if tag_name in SANS_COURSES:
            new_description = SANS_COURSES[tag_name]

            # Update the tag
            cursor.execute("""
                UPDATE tags
                SET description = ?
                WHERE id = ?
            """, (new_description, tag_id))

            print(f"✅ {tag_name}")
            print(f"   Old: {old_description}")
            print(f"   New: {new_description}\n")

            updated_count += 1
        else:
            print(f"⚠️  {tag_name} - No mapping found (skipped)")

    conn.commit()
    conn.close()

    print("=" * 70)
    print(f"✅ Updated {updated_count} tag description(s)")
    print("=" * 70)

if __name__ == "__main__":
    update_sans_descriptions()
