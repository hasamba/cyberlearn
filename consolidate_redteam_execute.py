#!/usr/bin/env python3
"""
Execute red_team domain consolidation.

WHAT THIS SCRIPT DOES:
1. Updates database: Changes domain 'redteam' -> 'red_team'
2. Renames lesson files: lesson_redteam_* -> lesson_red_team_*
3. Updates JSON files: Changes domain field to 'red_team'
4. Resequences order_index values 1-12
5. Reloads lessons into database

PREREQUISITE: Run consolidate_redteam_domains.py first to see the analysis
"""

import sqlite3
import json
import shutil
from pathlib import Path

def backup_database():
    """Create backup of database before changes"""
    print("\n" + "="*70)
    print("Step 1: Creating database backup")
    print("="*70)

    backup_path = Path('cyberlearn.db.backup')
    shutil.copy2('cyberlearn.db', backup_path)
    print(f"[OK] Database backed up to: {backup_path}")

def update_database():
    """Update all 'redteam' domain entries to 'red_team'"""
    print("\n" + "="*70)
    print("Step 2: Updating database - redteam -> red_team")
    print("="*70)

    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Count affected lessons
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'redteam'")
    count = cursor.fetchone()[0]

    if count == 0:
        print("[SKIP] No 'redteam' lessons found in database")
        conn.close()
        return

    print(f"Found {count} lessons with domain='redteam'")

    # Update domain field
    cursor.execute("UPDATE lessons SET domain = 'red_team' WHERE domain = 'redteam'")
    conn.commit()
    conn.close()

    print(f"[OK] Updated {count} lessons to domain='red_team'")

def rename_lesson_files():
    """Rename lesson files from lesson_redteam_* to lesson_red_team_*"""
    print("\n" + "="*70)
    print("Step 3: Renaming lesson files")
    print("="*70)

    content_dir = Path('content')
    redteam_files = sorted(content_dir.glob('lesson_redteam_*.json'))

    if not redteam_files:
        print("[SKIP] No lesson_redteam_* files found")
        return

    print(f"Found {len(redteam_files)} files to rename:")

    for old_path in redteam_files:
        # Generate new filename
        new_filename = old_path.name.replace('lesson_redteam_', 'lesson_red_team_')
        new_path = content_dir / new_filename

        print(f"  {old_path.name} -> {new_filename}")

        # Rename file
        old_path.rename(new_path)

    print(f"[OK] Renamed {len(redteam_files)} files")

def update_json_domain_field():
    """Update domain field in all red team lesson JSON files"""
    print("\n" + "="*70)
    print("Step 4: Updating JSON domain fields")
    print("="*70)

    content_dir = Path('content')
    red_team_files = sorted(content_dir.glob('lesson_red_team_*.json'))

    if not red_team_files:
        print("[SKIP] No lesson_red_team_* files found")
        return

    updated_count = 0

    for filepath in red_team_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check current domain
            current_domain = data.get('domain')

            if current_domain == 'redteam':
                # Update to red_team
                data['domain'] = 'red_team'

                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"  [UPDATED] {filepath.name}: domain='redteam' -> 'red_team'")
                updated_count += 1
            elif current_domain == 'red_team':
                print(f"  [OK] {filepath.name}: already domain='red_team'")
            else:
                print(f"  [WARNING] {filepath.name}: unexpected domain='{current_domain}'")

        except Exception as e:
            print(f"  [ERROR] {filepath.name}: {e}")

    if updated_count > 0:
        print(f"\n[OK] Updated {updated_count} JSON files")
    else:
        print("\n[OK] All JSON files already have domain='red_team'")

def resequence_order_index():
    """Resequence order_index values 1-12 for consolidated red_team domain"""
    print("\n" + "="*70)
    print("Step 5: Resequencing order_index (1-12)")
    print("="*70)

    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Get all red_team lessons sorted by current order
    cursor.execute("""
        SELECT lesson_id, title, order_index
        FROM lessons
        WHERE domain = 'red_team'
        ORDER BY order_index
    """)

    lessons = cursor.fetchall()

    if not lessons:
        print("[SKIP] No red_team lessons found")
        conn.close()
        return

    print(f"Resequencing {len(lessons)} lessons:")

    for new_index, (lesson_id, title, old_index) in enumerate(lessons, 1):
        if old_index != new_index:
            cursor.execute("""
                UPDATE lessons
                SET order_index = ?
                WHERE lesson_id = ?
            """, (new_index, lesson_id))
            print(f"  {new_index:2d}. {title[:50]:<50} (was {old_index})")
        else:
            print(f"  {new_index:2d}. {title[:50]:<50} [no change]")

    conn.commit()
    conn.close()

    print(f"\n[OK] Resequenced {len(lessons)} lessons")

def verify_consolidation():
    """Verify the consolidation was successful"""
    print("\n" + "="*70)
    print("Step 6: Verification")
    print("="*70)

    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Check for any remaining 'redteam' entries
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'redteam'")
    redteam_count = cursor.fetchone()[0]

    # Check red_team count
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain = 'red_team'")
    red_team_count = cursor.fetchone()[0]

    conn.close()

    print(f"\nDatabase status:")
    print(f"  domain='redteam': {redteam_count} lessons")
    print(f"  domain='red_team': {red_team_count} lessons")

    # Check files
    content_dir = Path('content')
    redteam_files = list(content_dir.glob('lesson_redteam_*.json'))
    red_team_files = list(content_dir.glob('lesson_red_team_*.json'))

    print(f"\nFile status:")
    print(f"  lesson_redteam_*.json: {len(redteam_files)} files")
    print(f"  lesson_red_team_*.json: {len(red_team_files)} files")

    # Determine success
    success = (redteam_count == 0 and red_team_count == 12 and
               len(redteam_files) == 0 and len(red_team_files) == 12)

    if success:
        print("\n" + "="*70)
        print("[SUCCESS] Consolidation complete!")
        print("="*70)
        print("\nNext steps:")
        print("1. Test the app: streamlit run app.py")
        print("2. Verify lessons load correctly")
        print("3. Commit changes: git add -A && git commit -m 'Consolidate red_team and redteam domains'")
    else:
        print("\n" + "="*70)
        print("[WARNING] Consolidation may be incomplete")
        print("="*70)
        print("\nPlease review the status above and:")
        print("1. Check for any remaining 'redteam' entries")
        print("2. Verify all files were renamed")
        print("3. Run python list_lessons.py to see current state")

def main():
    print("="*70)
    print("RED TEAM DOMAIN CONSOLIDATION - EXECUTION")
    print("="*70)
    print("\nThis script will consolidate 'redteam' and 'red_team' domains.")
    print("All 'redteam' lessons will become 'red_team' lessons.")
    print("\nA database backup will be created: cyberlearn.db.backup")

    response = input("\nContinue with consolidation? (yes/no): ")

    if response.lower() not in ['yes', 'y']:
        print("\n[ABORTED] No changes made")
        return

    try:
        backup_database()
        update_database()
        rename_lesson_files()
        update_json_domain_field()
        resequence_order_index()
        verify_consolidation()

    except Exception as e:
        print(f"\n[ERROR] Consolidation failed: {e}")
        print("\nTo restore from backup:")
        print("  cp cyberlearn.db.backup cyberlearn.db")

if __name__ == "__main__":
    main()
