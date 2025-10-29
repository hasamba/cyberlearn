#!/usr/bin/env python3
"""
Fix domain naming inconsistencies between models and database.

Issue:
- SkillLevels model has 'redteam' (no underscore)
- Database lessons have 'red_team' (with underscore)
- This breaks skill tracking and XP awards

Solution:
1. Standardize on UNDERSCORE format (matches most domains: active_directory, threat_hunting)
2. Update SkillLevels model to use 'red_team', 'blue_team'
3. Update database 'blueteam' → 'blue_team' for consistency
"""

import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

def backup_database():
    """Create timestamped backup"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(f'cyberlearn.db.backup_{timestamp}')
    shutil.copy2('cyberlearn.db', backup_path)
    print(f"[OK] Database backed up to: {backup_path}")
    return backup_path

def check_current_state():
    """Show current domain naming"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    cursor.execute('SELECT domain, COUNT(*) FROM lessons GROUP BY domain ORDER BY domain')
    domains = cursor.fetchall()

    print("\n" + "="*60)
    print("CURRENT DATABASE STATE")
    print("="*60)
    for domain, count in domains:
        print(f"  {domain:<20} ({count} lessons)")

    conn.close()
    return domains

def fix_database_domains():
    """Rename blueteam → blue_team in database"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("FIXING DATABASE DOMAIN NAMES")
    print("="*60)

    # Check if blueteam exists
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'blueteam'")
    blueteam_count = cursor.fetchone()[0]

    if blueteam_count > 0:
        print(f"[*] Renaming 'blueteam' → 'blue_team' ({blueteam_count} lessons)")
        cursor.execute("UPDATE lessons SET domain = 'blue_team' WHERE domain = 'blueteam'")
        conn.commit()
        print("[OK] Database updated")
    else:
        print("[*] No 'blueteam' domain found (may already be 'blue_team')")

    # Verify red_team is correct
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'red_team'")
    redteam_count = cursor.fetchone()[0]
    print(f"[OK] 'red_team' domain has {redteam_count} lessons")

    conn.close()

def show_model_fix_instructions():
    """Show what needs to be updated in models/user.py"""
    print("\n" + "="*60)
    print("NEXT STEP: UPDATE models/user.py")
    print("="*60)
    print("\nYou need to update models/user.py manually:")
    print("\n  OLD (lines 35-36):")
    print("    redteam: int = Field(default=0, ge=0, le=100)")
    print("    blueteam: int = Field(default=0, ge=0, le=100)")
    print("\n  NEW (lines 35-36):")
    print("    red_team: int = Field(default=0, ge=0, le=100)")
    print("    blue_team: int = Field(default=0, ge=0, le=100)")
    print("\n  Also update lines 51-52, 69-70 (references in methods)")
    print("\n[!] This requires manual editing - shall I create the updated file? (see below)")

def verify_final_state():
    """Show final domain state"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    cursor.execute('SELECT domain, COUNT(*) FROM lessons GROUP BY domain ORDER BY domain')
    domains = cursor.fetchall()

    print("\n" + "="*60)
    print("FINAL DATABASE STATE")
    print("="*60)
    for domain, count in domains:
        indicator = "[OK]" if "_" in domain or domain in ["fundamentals", "dfir", "malware", "pentest", "cloud", "linux", "system"] else "[FIX]"
        print(f"  {indicator} {domain:<20} ({count} lessons)")

    conn.close()

def main():
    print("="*60)
    print("DOMAIN NAMING CONSISTENCY FIX")
    print("="*60)
    print("\nThis script fixes domain naming inconsistencies:")
    print("  - Standardizes on underscore format (red_team, blue_team)")
    print("  - Updates database: blueteam → blue_team")
    print("  - Shows required model changes")

    # Step 1: Backup
    backup_path = backup_database()

    # Step 2: Show current state
    check_current_state()

    # Step 3: Fix database
    fix_database_domains()

    # Step 4: Show model fix instructions
    show_model_fix_instructions()

    # Step 5: Verify
    verify_final_state()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("[OK] Database fixed: blueteam → blue_team")
    print("[TODO] Update models/user.py (run fix_user_model.py)")
    print(f"[OK] Backup saved: {backup_path}")
    print("\nNext: Run 'python fix_user_model.py' to update the model")

if __name__ == '__main__':
    main()
