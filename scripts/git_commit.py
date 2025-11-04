#!/usr/bin/env python3
import subprocess
import sys

def run_git_command(args):
    """Run a git command and return output"""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)

# Add all changes
print("Adding all changes...")
run_git_command(['add', '-A'])

# Check status
print("\nGit status:")
status = run_git_command(['status', '--short'])
print(status if status else "No changes to commit")

if not status.strip():
    print("Nothing to commit, working tree clean")
    sys.exit(0)

# Commit
commit_message = """Fix sync_lessons.py column name error

- Changed 'lesson_content' to proper column names in UPDATE query
- Now updates all lesson fields: title, subtitle, difficulty, etc.
- Fixes "no such column: lesson_content" error
- Properly serializes JSON fields (prerequisites, content_blocks, etc.)"""

print(f"\nCommitting with message:\n{commit_message}\n")
run_git_command(['commit', '-m', commit_message])

# Push
print("\nPushing to remote...")
output = run_git_command(['push'])
print(output)

print("\nSuccess! All changes committed and pushed.")
