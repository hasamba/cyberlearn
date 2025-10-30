# Database Deployment Strategy

## Current Situation

The database (`cyberlearn.db`) is in `.gitignore`, which prevents it from being committed to git. This is standard practice because:
- Databases contain user data (privacy concerns)
- They change frequently (git conflicts)
- They can be large (repo bloat)

However, you want to ship a pre-configured database with:
- UI preferences columns ready (`last_username`, `preferred_tag_filters`)
- All 15 system tags pre-populated
- All lessons pre-loaded

---

## Recommended Solution: Template Database

### Setup (One-Time)

1. **Prepare a clean template database on your dev machine:**

```bash
# Apply all migrations
python add_ui_preferences.py
python add_difficulty_tags.py
python add_tags_system.py

# Load all lessons
python load_all_lessons.py

# Verify state
python dev_tools/check_migration_status.py
```

2. **Copy the configured database as a template:**

```bash
cp cyberlearn.db cyberlearn_template.db
```

3. **Track the template in git:**

```bash
# Remove cyberlearn_template.db from .gitignore if needed
git add cyberlearn_template.db
git add SETUP_GUIDE.md GETTING_STARTED.md
git commit -m "Add template database with all migrations and tags"
git push
```

### User Setup (First Run)

Users run a simple setup script that copies the template:

**setup_database.py** (create this):
```python
#!/usr/bin/env python3
"""
One-time database setup for new installations.
Copies the template database to create the working database.
"""
from pathlib import Path
import shutil

template_db = Path(__file__).parent / "cyberlearn_template.db"
working_db = Path(__file__).parent / "cyberlearn.db"

if working_db.exists():
    print(f"✓ Database already exists at {working_db}")
    print("  No action needed. Delete cyberlearn.db to start fresh.")
else:
    if not template_db.exists():
        print(f"❌ Template database not found at {template_db}")
        print("  Please run migrations manually:")
        print("    python add_ui_preferences.py")
        print("    python add_difficulty_tags.py")
        print("    python add_tags_system.py")
        print("    python load_all_lessons.py")
        exit(1)

    print(f"Creating database from template...")
    shutil.copy2(template_db, working_db)
    print(f"✅ Database created at {working_db}")
    print(f"✓ Ready to use! Run: streamlit run app.py")
```

### Updated User Instructions

**SETUP_GUIDE.md:**
```markdown
# Setup Guide

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Setup database: `python setup_database.py`
4. Run the app: `streamlit run app.py`

That's it! The database comes pre-configured with:
- ✅ All migrations applied
- ✅ All system tags created
- ✅ All lessons loaded
```

---

## Alternative: Track Database with Force

If you REALLY want to track the live database (not recommended):

```bash
# Override .gitignore for this specific file
git add -f cyberlearn.db
git commit -m "Add configured database"
git push
```

**Downsides:**
- User data gets committed (privacy issue)
- Frequent conflicts on VM pulls
- Large commit history
- Not standard practice

---

## Recommended Workflow

**Your Dev Machine:**
```bash
# 1. Make changes to migrations/lessons
vim add_ui_preferences.py  # or whatever

# 2. Test locally
python add_ui_preferences.py
python load_all_lessons.py
streamlit run app.py

# 3. Update template database
cp cyberlearn.db cyberlearn_template.db

# 4. Commit changes
git add cyberlearn_template.db add_ui_preferences.py
git commit -m "Update database schema and template"
git push
```

**Your Test VM:**
```bash
# 1. Pull changes
git pull

# 2. Recreate database from new template
rm cyberlearn.db
python setup_database.py

# 3. Test
streamlit run app.py
```

---

## Summary

✅ **Use template database approach** - Standard, clean, maintainable
❌ **Track live database** - Creates problems with user data and conflicts

The template database gives you the best of both worlds:
- Users get pre-configured setup
- You maintain version control
- No user data in git
- Clean separation of template vs working data
