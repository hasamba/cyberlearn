#!/usr/bin/env python3
"""
Rebuild database from scratch - use when domain names or structure changes
"""

import os
import sys

def main():
    db_path = "cyberlearn.db"

    if os.path.exists(db_path):
        print(f"[DELETE] Removing existing database: {db_path}")
        os.remove(db_path)
        print(f"[OK] Database deleted")
    else:
        print(f"[INFO] No existing database found at {db_path}")

    print("\n[REBUILD] Creating fresh database...")
    print("[INFO] Import database to trigger creation...")

    # Import will create tables
    from database import Base, engine
    Base.metadata.create_all(bind=engine)

    print("[OK] Database tables created")
    print("\n[NEXT] Run: python load_all_lessons.py")

if __name__ == "__main__":
    main()
