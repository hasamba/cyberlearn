#!/usr/bin/env python3
"""
Verification script for URL persistence fix
This script checks that all necessary code changes are in place
"""

import os
import re

def check_file_contains(filepath, patterns, description):
    """Check if file contains all required patterns"""
    print(f"\nChecking: {description}")
    print(f"File: {filepath}")

    if not os.path.exists(filepath):
        print(f"  ❌ File not found!")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    all_found = True
    for pattern in patterns:
        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            print(f"  [OK] Found: {pattern[:50]}...")
        else:
            print(f"  [MISSING] Missing: {pattern[:50]}...")
            all_found = False

    return all_found

def main():
    """Run verification checks"""
    print("=" * 80)
    print("URL Persistence Fix - Verification Script")
    print("=" * 80)

    base_path = os.path.dirname(__file__)

    # Check 1: app.py - Read block_index from URL
    app_py_path = os.path.join(base_path, "app.py")
    app_read_patterns = [
        r'if\s+"block_index"\s+in\s+params.*lesson',
        r'block_index\s*=\s*int\(params\["block_index"\]\)',
        r'st\.session_state\.current_block_index\s*=\s*block_index',
    ]
    check1 = check_file_contains(app_py_path, app_read_patterns,
                                  "app.py - Read block_index from URL")

    # Check 2: app.py - Write block_index to URL
    app_write_patterns = [
        r'if\s+"current_block_index"\s+in\s+st\.session_state',
        r'params\["block_index"\]\s*=\s*str\(st\.session_state\.current_block_index\)',
    ]
    check2 = check_file_contains(app_py_path, app_write_patterns,
                                  "app.py - Write block_index to URL")

    # Check 3: lesson_viewer.py - Initialize on start
    lesson_viewer_path = os.path.join(base_path, "ui", "pages", "lesson_viewer.py")
    init_patterns = [
        r'st\.session_state\.current_block_index\s*=\s*0.*Start from beginning',
        r'"block_index":\s*"0"',
    ]
    check3 = check_file_contains(lesson_viewer_path, init_patterns,
                                  "lesson_viewer.py - Initialize block_index")

    # Check 4: lesson_viewer.py - Update URL on navigation
    nav_patterns = [
        r'Prev.*block_index.*str\(st\.session_state\.current_block_index\)',
        r'Next.*block_index.*str\(st\.session_state\.current_block_index\)',
        r'Quiz.*block_index.*str\(st\.session_state\.current_block_index\)',
    ]
    check4 = check_file_contains(lesson_viewer_path, nav_patterns,
                                  "lesson_viewer.py - Update URL on navigation")

    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)

    checks = [
        ("app.py - Read from URL", check1),
        ("app.py - Write to URL", check2),
        ("lesson_viewer.py - Initialize", check3),
        ("lesson_viewer.py - Navigation", check4),
    ]

    all_passed = all(result for _, result in checks)

    for check_name, result in checks:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {check_name}")

    print("=" * 80)
    if all_passed:
        print("[SUCCESS] ALL CHECKS PASSED - Fix is ready for testing!")
        print("\nNext steps:")
        print("1. Run the Streamlit app on your VM: streamlit run app.py")
        print("2. Follow test cases in test_url_persistence.md")
        print("3. Verify URL updates as you navigate through lessons")
        print("4. Test refresh behavior (F5) - should stay on same section")
        return 0
    else:
        print("[ERROR] SOME CHECKS FAILED - Review the code changes")
        return 1

if __name__ == "__main__":
    exit(main())
