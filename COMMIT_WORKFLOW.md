# Workflow for Committing Database Changes

## The Problem You Just Hit

You tried to commit `cyberlearn.db` but it's in `.gitignore`, so git won't track it. This is intentional and correct!

**Solution: Use a template database instead**

---

## Complete Workflow (Run on Your Dev Machine)

### Step 1: Prepare Your Database

Make sure your local database has all the latest changes:

```bash
# Apply all migrations
python add_ui_preferences.py
python add_difficulty_tags.py
python add_tags_system.py

# Load all lessons
python load_all_lessons.py

# Verify everything is correct
python dev_tools/check_migration_status.py
```

**Expected output from check_migration_status.py:**
```
✓ last_username column: ✅ EXISTS
✓ preferred_tag_filters column: ✅ EXISTS
Total tags: 15
System tags: 13
✅ DATABASE IS READY!
```

### Step 2: Test Your Database

Make sure everything works:

```bash
streamlit run app.py
```

Test checklist:
- [ ] Can create account / login
- [ ] Auto-login works
- [ ] Username persists after refresh
- [ ] Tag filters persist after refresh
- [ ] Can tag lessons with 🏷️ button
- [ ] All 15 tags visible in tag manager

### Step 3: Create Template Database

Copy your working database as a template:

```bash
cp cyberlearn.db cyberlearn_template.db
```

### Step 4: Commit Changes

Commit the template database and new files:

```bash
# Add new files
git add setup_database.py
git add SETUP_GUIDE.md
git add GETTING_STARTED.md
git add DEPLOYMENT_STRATEGY.md
git add COMMIT_WORKFLOW.md

# Add the template database (not the working database!)
git add cyberlearn_template.db

# Commit
git commit -m "Add template database with UI preferences and new tag structure

- UI preferences: last_username, preferred_tag_filters
- Tag system: 15 system tags (3 content, 10 career, 2 package)
- Setup script: setup_database.py to copy template for users
- Documentation: Complete setup and deployment guides"

# Push
git push
```

---

## How Users Will Use This

### On First Install

Users will run:

```bash
git clone <your-repo>
cd cyberlearn
pip install -r requirements.txt
python setup_database.py    # ← Copies template to working database
streamlit run app.py
```

The `setup_database.py` script automatically:
1. Checks if `cyberlearn.db` already exists (skip if yes)
2. Copies `cyberlearn_template.db` → `cyberlearn.db`
3. User gets pre-configured database ready to use!

### On Updates

When you push database changes, users will:

```bash
git pull                    # Gets new cyberlearn_template.db
rm cyberlearn.db            # Delete their working database
python setup_database.py    # Recreate from new template
streamlit run app.py
```

**Note:** This will reset their user accounts! If you want to preserve user data, you need to provide migration scripts instead.

---

## Future Workflow

### When You Make Schema Changes

Example: Adding a new column to users table

**On your dev machine:**

```bash
# 1. Create migration script
vim add_new_feature.py

# 2. Run migration on your database
python add_new_feature.py

# 3. Test it works
streamlit run app.py

# 4. Update template
cp cyberlearn.db cyberlearn_template.db

# 5. Commit both migration script AND template
git add add_new_feature.py cyberlearn_template.db
git commit -m "Add new feature with database migration"
git push
```

**Users will:**

Option A (Fresh start - recommended for development):
```bash
git pull
rm cyberlearn.db
python setup_database.py
streamlit run app.py
```

Option B (Preserve user data):
```bash
git pull
python add_new_feature.py    # Run the migration script
streamlit run app.py
```

---

## When to Update Template

Update the template database (`cyberlearn_template.db`) when:

✅ **Yes - Update Template:**
- Adding/removing system tags
- Adding new lessons to content/
- Changing database schema (new columns, tables)
- Fixing data issues in existing lessons

❌ **No - Don't Update Template:**
- Testing with user accounts (user data is private)
- Experimenting with features
- Any changes you don't want to ship to users

---

## Git Tracking Summary

### These files ARE tracked in git:
- ✅ `cyberlearn_template.db` - Clean template database
- ✅ `setup_database.py` - Script to copy template
- ✅ `add_*.py` - Migration scripts (for option B updates)
- ✅ `load_all_lessons.py` - Content loading script
- ✅ All code files (app.py, models/, utils/, etc.)
- ✅ All documentation (*.md files)
- ✅ Lesson content (content/*.json)

### These files are NOT tracked in git (in .gitignore):
- ❌ `cyberlearn.db` - Working database (contains user data)
- ❌ `__pycache__/` - Python cache
- ❌ `.streamlit/` - Streamlit config
- ❌ `venv/` - Virtual environment
- ❌ User data, backups, logs

---

## Summary

**Your dev workflow:**
```bash
# Make changes
python add_ui_preferences.py
python load_all_lessons.py

# Test
streamlit run app.py

# Update template
cp cyberlearn.db cyberlearn_template.db

# Commit
git add cyberlearn_template.db <other-changed-files>
git commit -m "Description of changes"
git push
```

**User workflow:**
```bash
# First time
git clone <repo>
python setup_database.py
streamlit run app.py

# Updates
git pull
rm cyberlearn.db
python setup_database.py
streamlit run app.py
```

This approach keeps user data private while still shipping a pre-configured database! 🎉
