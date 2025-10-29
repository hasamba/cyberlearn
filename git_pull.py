#!/usr/bin/env python3
"""
Git pull wrapper that updates last pull timestamp.

Usage:
  python git_pull.py

This script:
1. Runs 'git pull origin main'
2. Updates .git_info.json with timestamp
3. Shows what was pulled
"""

import subprocess
import sys
from utils.git_status import GitStatus


def main():
    print("="*70)
    print("GIT PULL - Updating CyberLearn Platform")
    print("="*70)

    # Run git pull
    print("\n[*] Pulling from origin/main...\n")

    try:
        result = subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            capture_output=False,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("\n[OK] Git pull successful!")

            # Update timestamp
            git = GitStatus()
            git.update_pull_time()
            print("[OK] Updated last pull timestamp")

            print("\n" + "="*70)
            print("NEXT STEPS")
            print("="*70)
            print("If new lessons were added, run:")
            print("  python fix_everything.py    # Fix any validation errors")
            print("  python load_all_lessons.py  # Load new lessons into database")
            print("\nThen restart Streamlit app:")
            print("  streamlit run app.py")

        else:
            print("\n[ERROR] Git pull failed!")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print("\n[ERROR] Git pull timeout (> 60 seconds)")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
