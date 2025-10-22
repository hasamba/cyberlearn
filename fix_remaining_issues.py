"""
Fix remaining UUID issues in rich lessons
- Convert prerequisite UUIDs to strings
- Fix malformed lesson_id UUIDs
"""

import json
import os
import glob
import uuid

def fix_lesson_file(filepath):
    """Fix remaining UUID issues in a lesson file"""
    filename = os.path.basename(filepath)
    print(f"\nFixing: {filename}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse JSON
    lesson = json.loads(content)

    changes = []

    # Fix prerequisites - convert to strings
    if 'prerequisites' in lesson and lesson['prerequisites']:
        fixed_prereqs = []
        for prereq in lesson['prerequisites']:
            # If it's a dict with UUID info, extract the UUID string
            if isinstance(prereq, dict):
                # Try different UUID dict formats
                if 'uuid' in prereq:
                    prereq_str = str(prereq['uuid'])
                elif '$uuid' in prereq:
                    prereq_str = str(prereq['$uuid'])
                else:
                    # Just convert the whole dict to string
                    prereq_str = str(prereq)
                fixed_prereqs.append(prereq_str)
                changes.append(f"  [FIXED] prerequisite: {prereq} -> {prereq_str}")
            elif not isinstance(prereq, str):
                prereq_str = str(prereq)
                fixed_prereqs.append(prereq_str)
                changes.append(f"  [FIXED] prerequisite: {prereq} -> {prereq_str}")
            else:
                fixed_prereqs.append(prereq)

        lesson['prerequisites'] = fixed_prereqs

    # Check if lesson_id is valid UUID format
    if 'lesson_id' in lesson:
        lesson_id = str(lesson['lesson_id'])

        # Check if it's a malformed UUID (too many zeros, wrong format)
        try:
            # Try to parse as UUID
            uuid.UUID(lesson_id)
        except (ValueError, AttributeError):
            # Invalid UUID - generate new one
            new_uuid = str(uuid.uuid4())
            lesson['lesson_id'] = new_uuid
            changes.append(f"  [FIXED] lesson_id: {lesson_id} -> {new_uuid}")

    # Save fixed lesson
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)

    if changes:
        for change in changes:
            print(change)
        print("  [SAVED] Fixed version")
        return True
    else:
        print("  [OK] No changes needed")
        return False

def main():
    """Fix all problematic lesson files"""
    print("=" * 60)
    print("Fixing Remaining UUID Issues")
    print("=" * 60)
    print()

    # Target the files that had errors
    problem_files = [
        'lesson_active_directory_02_group_policy_RICH.json',
        'lesson_active_directory_03_kerberos_RICH.json',
        'lesson_blue_team_02_log_analysis_RICH.json',
        'lesson_fundamentals_03_encryption_RICH.json',
        'lesson_fundamentals_04_network_security_RICH.json',
        'lesson_red_team_02_osint_recon_RICH.json'
    ]

    fixed_count = 0
    error_count = 0

    for filename in problem_files:
        filepath = os.path.join('content', filename)
        if not os.path.exists(filepath):
            print(f"\n[SKIP] {filename} not found")
            continue

        try:
            if fix_lesson_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            error_count += 1

    print()
    print("=" * 60)
    if error_count == 0:
        print(f"[SUCCESS] Fixed {fixed_count} lesson files!")
    else:
        print(f"[WARNING] Fixed {fixed_count} files, {error_count} errors")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python load_all_lessons.py")
    print("2. Run: streamlit run app.py")

if __name__ == "__main__":
    main()
