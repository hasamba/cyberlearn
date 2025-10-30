# Developer Notes

**For developers maintaining the CyberLearn platform**

---

## Project Structure

### User-Facing (Shipped)
```
cyberlearn/
├── app.py                          # Main application
├── load_all_lessons.py             # User can load custom lessons
├── add_tags_system.py              # Initial setup (rarely needed)
├── add_ui_preferences.py           # Migration (already applied)
├── add_difficulty_tags.py          # Migration (already applied)
├── cyberlearn.db                   # Pre-configured database
├── content/                        # Lesson files
├── models/                         # Pydantic models
├── core/                           # Business logic
├── ui/                             # Streamlit UI components
├── utils/                          # Helper functions
├── README.md                       # Main documentation
└── SETUP_GUIDE.md                  # User installation guide
```

### Developer Only (NOT Shipped)
```
dev_tools/
├── README.md                       # Dev tools documentation
├── update_tag_names.py             # Bulk update tag names
├── bulk_tag_lessons.py             # Tag specific lesson ranges
├── add_course_apt_tags.py          # Add specific tags
├── test_username_save.py           # Test persistence
├── debug_user_preferences.py       # Debug user data
└── check_migration_status.py       # Verify migrations
```

---

## Development Workflow

### Making Changes to Content/Tags

#### On Your Dev Machine:
```bash
# 1. Make changes using dev tools
python dev_tools/update_tag_names.py
python dev_tools/bulk_tag_lessons.py

# 2. Verify in app
streamlit run app.py

# 3. Commit database with changes
git add cyberlearn.db
git commit -m "Update tags and lesson associations"
git push
```

#### On User VM (Testing):
```bash
# User just pulls - database already updated
git pull
streamlit run app.py
```

### Adding New Migrations

#### Creating a Migration:
1. Create script in **root directory** (user-facing)
2. Name clearly: `add_feature_name.py`
3. Make idempotent (safe to run multiple times)
4. Document in SETUP_GUIDE.md

#### Example:
```python
# add_new_feature.py (in root directory)
def add_new_feature():
    """Add new feature to database."""
    # Check if already applied
    # Apply changes
    # Show success message
```

### Adding Dev Tools

#### Creating a Dev Tool:
1. Create script in **dev_tools/** directory
2. Add entry to `dev_tools/README.md`
3. Run on dev machine only
4. Commit results to repo

---

## Key Principles

### 1. Separation of Concerns
- **Users**: Run app, optionally load custom content
- **Developers**: Maintain content, update schema, bulk operations

### 2. Database is Shipped
- Database included in repo with all content
- Users never rebuild from scratch
- Dev changes committed to repo

### 3. Migrations vs Maintenance
- **Migrations** (root): Schema changes, user runs once
- **Maintenance** (dev_tools): Content updates, dev runs often

### 4. One-Time vs Repeatable
- **One-time**: Migrations in root
- **Repeatable**: Dev tools for ongoing maintenance

---

## Common Tasks

### Update Tag Names Across Platform
```bash
# Dev machine
python dev_tools/update_tag_names.py
git add cyberlearn.db
git commit -m "Rename tags"
git push

# User machine
git pull  # Gets updated database
```

### Bulk Tag Lessons
```bash
# Dev machine
python dev_tools/bulk_tag_lessons.py
git add cyberlearn.db
git commit -m "Tag pentest lessons"
git push

# User machine
git pull  # Gets updated tags
```

### Add New Content Category
```bash
# Dev machine
python dev_tools/add_new_tags.py  # If creating new dev tool
# OR
python add_new_category.py  # If user-facing migration

git add cyberlearn.db add_new_category.py
git commit -m "Add new category"
git push

# User machine
git pull
python add_new_category.py  # Only if user-facing
```

---

## Testing Flow

### Dev Machine (Your PC):
1. Make changes using dev tools
2. Test in local app
3. Verify database state
4. Commit changes
5. Push to repo

### Test VM:
1. Pull changes
2. Run app
3. Verify functionality
4. Confirm user experience

### Production:
- Users pull and run
- Database already updated
- No manual steps needed

---

## Release Process

### Before Release:
1. Run all maintenance scripts to finalize content
2. Verify all migrations in root directory
3. Test on fresh VM
4. Update documentation
5. Tag release version

### Creating Release:
```bash
# Finalize database
python dev_tools/update_tag_names.py
python dev_tools/bulk_tag_lessons.py

# Verify
python dev_tools/check_migration_status.py

# Commit
git add .
git commit -m "Release v1.0: Final content and tags"
git tag v1.0
git push origin main --tags
```

---

## Documentation Standards

### User Documentation (Root):
- **README.md**: Project overview
- **SETUP_GUIDE.md**: Installation instructions
- **HOW_TO_ADD_NEW_LESSONS.md**: Content creation
- **TAGGING_GUIDE.md**: Tag system reference

### Developer Documentation:
- **DEVELOPER_NOTES.md**: This file
- **dev_tools/README.md**: Dev tools reference

### Keep Separate:
- User docs: Simple, action-oriented
- Dev docs: Technical, workflow-focused

---

## Summary

### Users Should:
- ✅ Clone repo and run app
- ✅ Pull updates regularly
- ✅ Optionally add custom lessons
- ❌ Never touch dev_tools/
- ❌ Never run maintenance scripts

### Developers Should:
- ✅ Use dev_tools for maintenance
- ✅ Commit database changes to repo
- ✅ Keep user docs simple
- ✅ Test on VM before pushing
- ❌ Never tell users to run dev_tools scripts

### The Golden Rule:
**If users need to run it, put it in root.**
**If only you need to run it, put it in dev_tools.**

---

## Quick Reference

| Task | Location | Who | Shipped? |
|------|----------|-----|----------|
| Update tags | dev_tools/ | Dev | Results only |
| Bulk operations | dev_tools/ | Dev | Results only |
| Testing | dev_tools/ | Dev | No |
| Migrations | root/ | User | Yes |
| App code | root/ | N/A | Yes |
| Content | content/ | Both | Yes |
| Database | root/ | N/A | Yes (with updates) |

---

This structure keeps things clean, organized, and user-friendly! 🎯
