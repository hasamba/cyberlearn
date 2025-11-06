#!/usr/bin/env python3
"""
Rebuild the template database with all lessons properly tagged.
This ensures the template includes all lesson-tag associations.
"""

import sys
import subprocess
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_script(script_name, description):
    """Run a script and report results"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}\n")

    result = subprocess.run(
        [sys.executable, script_name],
        cwd=project_root
    )

    if result.returncode != 0:
        print(f"\n[ERROR] {description} failed!")
        return False

    print(f"\n[✓] {description} completed")
    return True

def main():
    print("=" * 80)
    print("REBUILD TEMPLATE DATABASE WITH TAGS")
    print("=" * 80)
    print("\nThis will:")
    print("  1. Delete and rebuild cyberlearn.db")
    print("  2. Load all 591 lessons")
    print("  3. Apply all lesson tags from lesson_ideas.csv")
    print("  4. Copy to cyberlearn_template.db")

    response = input("\nProceed? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Cancelled.")
        return

    # Step 1: Rebuild database with all lessons
    if not run_script("rebuild_all_lessons.py", "Step 1/3: Rebuilding database with all lessons"):
        return

    # Step 2: Tag lessons from CSV
    if not run_script("scripts/tag_lessons_from_csv.py", "Step 2/3: Tagging lessons from lesson_ideas.csv"):
        return

    # Step 3: Update template database
    if not run_script("scripts/update_template_database.py", "Step 3/3: Updating template database"):
        return

    print("\n" + "=" * 80)
    print("[✓] TEMPLATE DATABASE REBUILT SUCCESSFULLY!")
    print("=" * 80)
    print("\nThe template now includes:")
    print("  ✓ All 591 lessons")
    print("  ✓ All lesson-tag associations")
    print("  ✓ All 17 system tags")
    print("\nNext steps:")
    print("  1. git add cyberlearn_template.db")
    print("  2. git commit -m 'Update template database with lesson tags'")
    print("  3. git push")
    print("  4. On VM: ./update_vm.sh")

if __name__ == "__main__":
    main()
