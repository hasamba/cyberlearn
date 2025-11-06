#!/usr/bin/env python3
"""
Apply the lesson renumbering fix and reload the database.
This script sets up the Python path correctly and runs all necessary steps.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_script(script_path, description):
    """Run a Python script with proper path setup"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}\n")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=project_root,
        env={**dict(os.environ), 'PYTHONPATH': str(project_root)}
    )

    if result.returncode != 0:
        print(f"\n[ERROR] {description} failed with exit code {result.returncode}")
        return False

    print(f"\n[✓] {description} completed successfully")
    return True

def main():
    print("=" * 80)
    print("APPLYING LESSON RENUMBERING FIX")
    print("=" * 80)

    scripts = [
        (project_root / "renumber_lessons.py", "Step 1/3: Renumbering lesson files"),
        (project_root / "rebuild_all_lessons.py", "Step 2/3: Rebuilding database with all lessons"),
        (project_root / "scripts" / "update_template_database.py", "Step 3/3: Updating template database"),
    ]

    for script_path, description in scripts:
        if not script_path.exists():
            print(f"\n[ERROR] Script not found: {script_path}")
            sys.exit(1)

        if not run_script(script_path, description):
            print(f"\n[FAILED] Process stopped due to error")
            sys.exit(1)

    print("\n" + "=" * 80)
    print("[✓] ALL STEPS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Run: git add content/ cyberlearn_template.db models/lesson.py ui/pages/lesson_viewer.py")
    print("  2. Run: git commit -m 'Fix duplicate lesson numbers and add short lesson IDs'")
    print("  3. Run: git push")
    print("  4. On VM: bash update_vm.sh")

if __name__ == "__main__":
    main()
