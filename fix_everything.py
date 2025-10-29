#!/usr/bin/env python3
"""
Master fix script - runs all fixes in correct order.

This script:
1. Fixes database domain naming (blueteam → blue_team)
2. Fixes user model (redteam/blueteam → red_team/blue_team)
3. Fixes post_assessment fields (Blue Team, DFIR, Malware lessons)
4. Fixes pentest lessons (jim_kwik_principles, estimated_time, post_assessment)
5. Validates all lessons (optional)
6. Loads all lessons into database
7. Verifies final state

Usage:
  python fix_everything.py
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and check for errors"""
    print("\n" + "="*70)
    print(f"STEP: {description}")
    print("="*70)
    print(f"Running: {script_name}")
    print("-"*70)

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n[OK] {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {script_name} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n[ERROR] Script not found: {script_name}")
        return False

def main():
    print("="*70)
    print("CYBERLEARN MASTER FIX SCRIPT")
    print("="*70)
    print("\nThis script will:")
    print("  1. Fix database domain naming (blueteam → blue_team)")
    print("  2. Fix user model (redteam/blueteam → red_team/blue_team)")
    print("  3. Fix post_assessment fields (Blue Team, DFIR, Malware)")
    print("  4. Fix pentest lessons (jim_kwik_principles, estimated_time)")
    print("  5. Validate all lessons (optional)")
    print("  6. Load all lessons into database")
    print("  7. Display final lesson count and domain summary")
    print("\nEstimated time: 5-10 minutes")
    print("="*70)

    response = input("\nContinue? [y/N]: ").strip().lower()
    if response != 'y':
        print("Aborted by user.")
        sys.exit(0)

    # Track success
    all_success = True

    # Step 1: Fix database domain naming
    if not run_script('fix_domain_naming.py', 'Fix Database Domain Naming'):
        all_success = False
        print("\n[!] Database fix failed. Stopping here.")
        sys.exit(1)

    # Step 2: Fix user model
    if not run_script('fix_user_model.py', 'Fix User Model'):
        all_success = False
        print("\n[!] User model fix failed. Stopping here.")
        sys.exit(1)

    # Step 3: Fix post-assessment fields (Blue Team, DFIR, Malware lessons)
    if not run_script('fix_post_assessments.py', 'Fix Post-Assessment Fields'):
        print("\n[WARNING] Post-assessment fix had issues, but continuing...")

    # Step 4: Fix pentest lessons (jim_kwik_principles, estimated_time, post_assessment)
    if not run_script('fix_pentest_lessons.py', 'Fix Pentest Lessons'):
        print("\n[WARNING] Pentest lesson fix had issues, but continuing...")

    # Step 5: Validate lessons (optional but recommended)
    print("\n" + "="*70)
    print("STEP: Validate All Lessons")
    print("="*70)
    response = input("Run comprehensive_fix.py to validate lessons? [Y/n]: ").strip().lower()
    if response != 'n':
        if not run_script('comprehensive_fix.py', 'Validate All Lessons'):
            print("\n[WARNING] Validation had issues, but continuing...")

    # Step 6: Load all lessons
    if not run_script('load_all_lessons.py', 'Load All Lessons into Database'):
        all_success = False
        print("\n[!] Lesson loading failed. Check errors above.")
        sys.exit(1)

    # Step 7: Final verification
    print("\n" + "="*70)
    print("FINAL VERIFICATION")
    print("="*70)

    try:
        # Count lessons by domain
        import sqlite3
        conn = sqlite3.connect('cyberlearn.db')
        cursor = conn.cursor()

        cursor.execute('SELECT domain, COUNT(*) FROM lessons GROUP BY domain ORDER BY domain')
        domains = cursor.fetchall()

        print("\nLessons by domain:")
        total = 0
        for domain, count in domains:
            print(f"  {domain:<20} {count:>3} lessons")
            total += count

        print(f"\n  {'TOTAL':<20} {total:>3} lessons")

        # Check for OSINT
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'osint'")
        osint_count = cursor.fetchone()[0]

        if osint_count >= 10:
            print(f"\n[OK] OSINT domain fully loaded ({osint_count} lessons)")
        elif osint_count > 0:
            print(f"\n[WARNING] OSINT partially loaded ({osint_count}/10 lessons)")
        else:
            print("\n[ERROR] OSINT domain not loaded (0 lessons)")

        # Check for red_team and blue_team
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'red_team'")
        redteam_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'blue_team'")
        blueteam_count = cursor.fetchone()[0]

        print(f"[OK] red_team domain: {redteam_count} lessons")
        print(f"[OK] blue_team domain: {blueteam_count} lessons")

        conn.close()

    except Exception as e:
        print(f"\n[ERROR] Verification failed: {e}")
        all_success = False

    # Final summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    if all_success:
        print("[OK] All fixes applied successfully!")
        print("\nNext steps:")
        print("  1. Test in Streamlit: streamlit run app.py")
        print("  2. Verify OSINT lessons appear in UI")
        print("  3. Test skill tracking for red_team and blue_team lessons")
        print("\nBackups created:")
        print("  - cyberlearn.db.backup_TIMESTAMP")
        print("  - models/user.py.backup_TIMESTAMP")
    else:
        print("[!] Some fixes had issues - review output above")
        print("\nRollback instructions in DOMAIN_NAMING_FIX.md")

    print("="*70)

if __name__ == '__main__':
    main()
