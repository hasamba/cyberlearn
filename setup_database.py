#!/usr/bin/env python3
"""
One-time database setup for new installations.
Copies the template database to create the working database.

This ensures users get a pre-configured database with:
- All migrations applied (UI preferences, difficulty tags, tag system)
- All system tags created
- All lessons loaded
"""
from pathlib import Path
import shutil

def setup_database():
    """Copy template database to working database if it doesn't exist"""
    template_db = Path(__file__).parent / "cyberlearn_template.db"
    working_db = Path(__file__).parent / "cyberlearn.db"

    print("=" * 60)
    print("CYBERLEARN DATABASE SETUP")
    print("=" * 60)

    if working_db.exists():
        print(f"\n✓ Database already exists at:")
        print(f"  {working_db}")
        print("\n  No action needed.")
        print("\n  To start fresh, delete cyberlearn.db and run this script again.")
        return True

    if not template_db.exists():
        print(f"\n❌ Template database not found at:")
        print(f"  {template_db}")
        print("\n  Please run migrations manually:")
        print("    python add_ui_preferences.py")
        print("    python add_difficulty_tags.py")
        print("    python add_tags_system.py")
        print("    python load_all_lessons.py")
        print("\n  Then copy the database:")
        print("    cp cyberlearn.db cyberlearn_template.db")
        return False

    print(f"\nCreating database from template...")
    print(f"  Template: {template_db}")
    print(f"  Working:  {working_db}")

    try:
        shutil.copy2(template_db, working_db)
        print("\n✅ Database created successfully!")
        print("\nThe database includes:")
        print("  ✓ All migrations applied")
        print("  ✓ All system tags (15 tags)")
        print("  ✓ All lessons loaded")
        print("  ✓ Ready for user accounts")
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETE!")
        print("=" * 60)
        print("\nNext step: Run the app")
        print("  streamlit run app.py")
        print()
        return True
    except Exception as e:
        print(f"\n❌ Error copying database: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = setup_database()
    sys.exit(0 if success else 1)
