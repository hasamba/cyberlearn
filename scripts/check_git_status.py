#!/usr/bin/env python3
import subprocess
import sys

try:
    result = subprocess.run(
        ['git', 'status', '--short'],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    if result.stdout.strip():
        print("\n=== UNCOMMITTED CHANGES FOUND ===")
        sys.exit(1)
    else:
        print("=== NO UNCOMMITTED CHANGES ===")
        sys.exit(0)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    print(f"stderr: {e.stderr}")
    sys.exit(1)
