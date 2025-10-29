#!/usr/bin/env python3
"""
Fix models/user.py to use consistent domain naming with underscores.

Changes:
- redteam → red_team (3 locations)
- blueteam → blue_team (3 locations)

This ensures SkillLevels model matches database domain names.
"""

from pathlib import Path
import shutil
from datetime import datetime

def backup_file():
    """Create timestamped backup of user.py"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    source = Path('models/user.py')
    backup = Path(f'models/user.py.backup_{timestamp}')
    shutil.copy2(source, backup)
    print(f"[OK] Backup created: {backup}")
    return backup

def fix_user_model():
    """Update models/user.py with consistent domain naming"""
    file_path = Path('models/user.py')

    print("\n" + "="*60)
    print("FIXING models/user.py")
    print("="*60)

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Track changes
    changes = []

    # Fix 1: Field definitions (lines 35-36)
    old_redteam_field = "redteam: int = Field(default=0, ge=0, le=100)"
    new_redteam_field = "red_team: int = Field(default=0, ge=0, le=100)"
    if old_redteam_field in content:
        content = content.replace(old_redteam_field, new_redteam_field)
        changes.append("Line 35: redteam → red_team (field definition)")

    old_blueteam_field = "blueteam: int = Field(default=0, ge=0, le=100)"
    new_blueteam_field = "blue_team: int = Field(default=0, ge=0, le=100)"
    if old_blueteam_field in content:
        content = content.replace(old_blueteam_field, new_blueteam_field)
        changes.append("Line 36: blueteam → blue_team (field definition)")

    # Fix 2: get_overall_level method (lines 51-52)
    old_redteam_ref1 = "            self.redteam,"
    new_redteam_ref1 = "            self.red_team,"
    if old_redteam_ref1 in content:
        content = content.replace(old_redteam_ref1, new_redteam_ref1)
        changes.append("Line 51: self.redteam → self.red_team")

    old_blueteam_ref1 = "            self.blueteam,"
    new_blueteam_ref1 = "            self.blue_team,"
    if old_blueteam_ref1 in content:
        content = content.replace(old_blueteam_ref1, new_blueteam_ref1)
        changes.append("Line 52: self.blueteam → self.blue_team")

    # Fix 3: get_weakest_domain method (lines 69-70)
    old_redteam_map = '            self.redteam: "redteam",'
    new_redteam_map = '            self.red_team: "red_team",'
    if old_redteam_map in content:
        content = content.replace(old_redteam_map, new_redteam_map)
        changes.append("Line 69: domain_map redteam → red_team")

    old_blueteam_map = '            self.blueteam: "blueteam",'
    new_blueteam_map = '            self.blue_team: "blue_team",'
    if old_blueteam_map in content:
        content = content.replace(old_blueteam_map, new_blueteam_map)
        changes.append("Line 70: domain_map blueteam → blue_team")

    # Write updated file
    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n[OK] Updated {len(changes)} locations:")
        for change in changes:
            print(f"  ✓ {change}")
    else:
        print("[*] No changes needed (already updated)")

    return len(changes) > 0

def verify_fix():
    """Verify the fix was applied correctly"""
    file_path = Path('models/user.py')

    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for old naming (should NOT exist)
    issues = []
    if 'redteam: int = Field' in content:
        issues.append("[ERROR] Old 'redteam' field definition still exists")
    if 'blueteam: int = Field' in content:
        issues.append("[ERROR] Old 'blueteam' field definition still exists")
    if 'self.redteam,' in content:
        issues.append("[ERROR] Old 'self.redteam' reference still exists")
    if 'self.blueteam,' in content:
        issues.append("[ERROR] Old 'self.blueteam' reference still exists")
    if '"redteam",' in content and 'self.red_team' in content:
        issues.append("[ERROR] Old 'redteam' string in domain_map")
    if '"blueteam",' in content and 'self.blue_team' in content:
        issues.append("[ERROR] Old 'blueteam' string in domain_map")

    # Check for new naming (should exist)
    successes = []
    if 'red_team: int = Field(default=0, ge=0, le=100)' in content:
        successes.append("[OK] 'red_team' field definition")
    if 'blue_team: int = Field(default=0, ge=0, le=100)' in content:
        successes.append("[OK] 'blue_team' field definition")
    if 'self.red_team,' in content:
        successes.append("[OK] 'self.red_team' references")
    if 'self.blue_team,' in content:
        successes.append("[OK] 'self.blue_team' references")
    if '"red_team",' in content:
        successes.append("[OK] 'red_team' in domain_map")
    if '"blue_team",' in content:
        successes.append("[OK] 'blue_team' in domain_map")

    if issues:
        print("\n[!] ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✓ All checks passed!")

    if successes:
        for success in successes:
            print(f"  {success}")

    return len(issues) == 0

def main():
    print("="*60)
    print("USER MODEL DOMAIN NAMING FIX")
    print("="*60)
    print("\nThis script updates models/user.py to use underscore naming:")
    print("  - redteam → red_team")
    print("  - blueteam → blue_team")
    print("\nThis ensures consistency with database domain names.")

    # Step 1: Backup
    backup_path = backup_file()

    # Step 2: Fix model
    updated = fix_user_model()

    # Step 3: Verify
    verified = verify_fix()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    if updated and verified:
        print("[OK] models/user.py updated successfully")
        print(f"[OK] Backup saved: {backup_path}")
        print("\nNext steps:")
        print("  1. Run 'python comprehensive_fix.py' to validate OSINT lessons")
        print("  2. Run 'python load_all_lessons.py' to load OSINT into database")
        print("  3. Restart Streamlit app: 'streamlit run app.py'")
    else:
        print("[!] Issues detected - review output above")
        print(f"[OK] Backup available: {backup_path}")

if __name__ == '__main__':
    main()
