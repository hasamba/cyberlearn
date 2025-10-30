# Development Tools

**⚠️ FOR DEVELOPERS ONLY - NOT FOR END USERS**

This directory contains scripts for maintaining and developing the CyberLearn platform. These scripts should **NOT** be shipped with the application or run by end users.

---

## Directory Purpose

- **User-facing scripts**: Root directory (setup, migrations)
- **Developer scripts**: This directory (maintenance, testing, bulk operations)

---

## Scripts in This Directory

### Tag Management
| Script | Purpose |
|--------|---------|
| `update_tag_names.py` | Update existing tag names in database |
| `bulk_tag_lessons.py` | Bulk tag specific lesson ranges |
| `add_course_apt_tags.py` | Add course/APT tags to existing DB |

### Testing & Debugging
| Script | Purpose |
|--------|---------|
| `test_username_save.py` | Test username persistence functionality |
| `debug_user_preferences.py` | Show user preference values in DB |
| `check_migration_status.py` | Verify migration status |

---

## When to Use These Scripts

### During Development (Your PC)
Run these scripts to:
- Update tag structure across all lessons
- Test new features
- Debug database issues
- Bulk operations on content

### Before Release
1. Run maintenance scripts to prepare database
2. Run migrations to update schema
3. Commit changes to repo
4. Tag release version

### User Installation
Users should **NEVER** run these scripts. They only run:
- `setup.py` (initial setup)
- `add_tags_system.py` (if setting up from scratch)
- `add_ui_preferences.py` (migration)
- `add_difficulty_tags.py` (migration)
- `load_all_lessons.py` (if adding custom lessons)

---

## Example Workflows

### Workflow 1: Update Tag Names (Developer)
**Location: Your PC**
```bash
# 1. Update tag names
python dev_tools/update_tag_names.py

# 2. Verify in app
streamlit run app.py

# 3. Commit changes
git add cyberlearn.db
git commit -m "Update tag names"
git push
```

**Location: User VM**
```bash
# User just pulls and restarts
git pull
streamlit run app.py
```

### Workflow 2: Bulk Tag Lessons (Developer)
**Location: Your PC**
```bash
# 1. Bulk tag lessons
python dev_tools/bulk_tag_lessons.py

# 2. Verify tags applied
python dev_tools/check_migration_status.py

# 3. Commit database with new tags
git add cyberlearn.db
git commit -m "Tag pentest/redteam lessons"
git push
```

**Location: User VM**
```bash
# User just pulls (database already updated)
git pull
streamlit run app.py
```

### Workflow 3: Add New Migration (Developer)
**Location: Your PC**
```bash
# 1. Create migration in root
# add_new_feature.py

# 2. Test migration
python add_new_feature.py

# 3. Document in README
# Update user-facing docs

# 4. Commit migration script (in root, not dev_tools)
git add add_new_feature.py README.md
git commit -m "Add new feature migration"
git push
```

**Location: User VM**
```bash
# User runs the migration
git pull
python add_new_feature.py
streamlit run app.py
```

---

## File Organization

```
cyberlearn/
├── app.py                          # Main app (USER)
├── setup.py                        # Initial setup (USER)
├── load_all_lessons.py             # Load lessons (USER)
├── add_tags_system.py              # Initial tag setup (USER)
├── add_ui_preferences.py           # Migration (USER)
├── add_difficulty_tags.py          # Migration (USER)
├── README.md                       # User documentation
├── SETUP_GUIDE.md                  # User installation guide
│
├── dev_tools/                      # DEVELOPER ONLY
│   ├── README.md                   # This file
│   ├── update_tag_names.py         # Dev maintenance
│   ├── bulk_tag_lessons.py         # Dev maintenance
│   ├── add_course_apt_tags.py      # Dev maintenance
│   ├── test_username_save.py       # Dev testing
│   ├── debug_user_preferences.py   # Dev debugging
│   └── check_migration_status.py   # Dev debugging
│
├── content/                        # Lesson files (SHIPPED)
├── models/                         # Code (SHIPPED)
├── core/                           # Code (SHIPPED)
└── cyberlearn.db                   # Database (SHIPPED WITH CONTENT)
```

---

## Key Principle

**Users should never touch dev_tools/**

Users only interact with:
- Root-level setup/migration scripts
- The app itself (`streamlit run app.py`)
- Their own custom content (if adding lessons)

All maintenance, bulk operations, and development tasks happen on your dev machine using scripts in `dev_tools/`.

---

## Adding New Dev Tools

When creating new maintenance scripts:

1. **Put them in dev_tools/**
2. **Add entry to this README**
3. **Do NOT include in user docs**
4. **Run them on your PC, commit results**

When creating new user-facing scripts:

1. **Put them in root directory**
2. **Add to main README.md**
3. **Add to SETUP_GUIDE.md**
4. **Document clearly for end users**

---

## Summary

| What | Where | Who |
|------|-------|-----|
| Maintenance scripts | `dev_tools/` | Developer only |
| Setup/migration scripts | Root | User runs once |
| Application code | Root | User never touches |
| Content management | Root | User via app UI |
| Database updates | Root | Developer commits, user pulls |

**Golden Rule:** If a user shouldn't run it, put it in `dev_tools/`.
