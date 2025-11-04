#!/usr/bin/env python3
"""Quick script to check tag names in database"""
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "cyberlearn.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*60)
print("CURRENT TAGS IN DATABASE")
print("="*60)

# Check for Career Path tags
cursor.execute("SELECT name FROM tags WHERE name LIKE 'Career Path:%' ORDER BY name")
career_tags = [row[0] for row in cursor.fetchall()]

print(f"\nCareer Path tags ({len(career_tags)}):")
if career_tags:
    for tag in career_tags:
        print(f"  ✓ {tag}")
else:
    print("  ❌ NO Career Path tags found")

# Check for Package tags
cursor.execute("SELECT name FROM tags WHERE name LIKE 'Package:%' ORDER BY name")
package_tags = [row[0] for row in cursor.fetchall()]

print(f"\nPackage tags ({len(package_tags)}):")
if package_tags:
    for tag in package_tags:
        print(f"  ✓ {tag}")
else:
    print("  ❌ NO Package tags found")

# Check for old-style tags (without prefix)
cursor.execute("""
    SELECT name FROM tags
    WHERE name IN (
        'SOC Tier 1', 'SOC Tier 2', 'Incident Responder', 'Threat Hunter',
        'Forensic Analyst', 'Malware Analyst', 'Penetration Tester',
        'Red Team Operator', 'Security Engineer', 'Cloud Security',
        'Eric Zimmerman Tools', 'APT'
    )
    ORDER BY name
""")
old_tags = [row[0] for row in cursor.fetchall()]

print(f"\nOld-style tags (should be 0):")
if old_tags:
    print("  ❌ Found old tags that need to be renamed:")
    for tag in old_tags:
        print(f"    • {tag}")
else:
    print("  ✓ No old-style tags found")

# Show all tags
cursor.execute("SELECT name FROM tags ORDER BY name")
all_tags = [row[0] for row in cursor.fetchall()]

print(f"\nAll tags ({len(all_tags)}):")
for tag in all_tags:
    print(f"  • {tag}")

conn.close()

print("\n" + "="*60)
if len(career_tags) >= 10 and len(package_tags) >= 2 and len(old_tags) == 0:
    print("✅ TAGS ARE CORRECTLY RENAMED!")
else:
    print("❌ TAGS NEED TO BE RENAMED - Run: python dev_tools/update_tag_names.py")
print("="*60)
