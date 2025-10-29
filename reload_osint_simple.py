#!/usr/bin/env python3
"""
Simple script to reload OSINT lessons.
Deletes OSINT lessons from database then runs load_all_lessons.py
"""

import sqlite3
import subprocess
import sys

def delete_osint_from_db():
    """Delete OSINT lessons directly from database"""
    try:
        conn = sqlite3.connect('cyberlearn.db')
        cursor = conn.cursor()

        # Count current OSINT lessons
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain='osint'")
        count = cursor.fetchone()[0]

        print("="*60)
        print("Removing existing OSINT lessons from database")
        print("="*60)
        print(f"Found {count} existing OSINT lessons")

        if count > 0:
            # Delete them
            cursor.execute("DELETE FROM lessons WHERE domain='osint'")
            conn.commit()
            print(f"Deleted {count} OSINT lessons")
        else:
            print("No OSINT lessons to delete")

        conn.close()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def run_load_all_lessons():
    """Run the standard load_all_lessons.py script"""
    print("\n" + "="*60)
    print("Running load_all_lessons.py to load OSINT lessons")
    print("="*60 + "\n")

    try:
        result = subprocess.run(
            [sys.executable, 'load_all_lessons.py'],
            capture_output=True,
            text=True
        )

        # Print output
        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"Error running load_all_lessons.py: {e}")
        return False

def verify_osint():
    """Verify OSINT lessons loaded"""
    try:
        conn = sqlite3.connect('cyberlearn.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT lesson_id, title, difficulty, order_index
            FROM lessons
            WHERE domain='osint'
            ORDER BY order_index
        """)

        lessons = cursor.fetchall()

        print("\n" + "="*60)
        print(f"Verification: OSINT Lessons in Database")
        print("="*60)

        if lessons:
            print(f"\nFound {len(lessons)} OSINT lessons:")
            for lesson_id, title, difficulty, order_index in lessons:
                print(f"  {order_index}. {title} (difficulty: {difficulty})")
        else:
            print("\n⚠️  No OSINT lessons found in database")
            print("    Check the errors above from load_all_lessons.py")

        conn.close()
        return len(lessons)

    except Exception as e:
        print(f"Error verifying: {e}")
        return 0

def main():
    print("\n" + "="*60)
    print("OSINT Lessons Reload")
    print("="*60 + "\n")

    # Step 1: Delete existing OSINT lessons
    if not delete_osint_from_db():
        print("\n❌ Failed to delete OSINT lessons")
        return 1

    # Step 2: Run load_all_lessons.py
    if not run_load_all_lessons():
        print("\n⚠️  load_all_lessons.py had errors")
        # Continue to verification anyway

    # Step 3: Verify
    count = verify_osint()

    if count > 0:
        print(f"\n✅ Success! {count} OSINT lessons loaded")
        print("\nNext steps:")
        print("  1. Restart Streamlit: streamlit run app.py")
        print("  2. Go to My Learning → OSINT tab")
        print("  3. Verify all lessons appear")
        return 0
    else:
        print("\n❌ No OSINT lessons were loaded")
        print("   Check validation errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
