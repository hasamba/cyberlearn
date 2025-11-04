# Database Sync Workflow

## Overview

This document explains the correct workflow for syncing lesson files with databases.

## Key Databases

- **`cyberlearn.db`** - Working database on dev machine (used by Streamlit app)
- **`cyberlearn_template.db`** - Template database deployed to VMs via `update_vm.sh`

## Scripts

### 1. `compare_lessons_to_db.py`
Compares lesson files with database to find:
- Missing lessons (in files but not DB)
- Extra lessons (in DB but no file)
- Outdated lessons (content mismatch)

**Configuration**: Change `DB_PATH` variable to check either database

### 2. `update_outdated_lessons.py`
Updates outdated lessons in the database from lesson files.

**Important**: This modifies `cyberlearn.db` (working database), NOT the template!

### 3. `update_template_database.py`
Copies `cyberlearn.db` → `cyberlearn_template.db`

## Correct Workflow

### When lesson files change:

```bash
# 1. Check working database for outdated lessons
python compare_lessons_to_db.py

# 2. Update outdated lessons in working database
python update_outdated_lessons.py

# 3. Verify working database is in sync
python compare_lessons_to_db.py

# 4. Copy working database to template
python update_template_database.py

# 5. (Optional) Verify template database
# Edit compare_lessons_to_db.py: DB_PATH = "cyberlearn_template.db"
python compare_lessons_to_db.py

# 6. Commit updated template
git add cyberlearn_template.db
git commit -m "Update template database with latest lesson content"
git push
```

## Common Mistakes

### ❌ WRONG: Modifying template directly

```bash
# DON'T DO THIS:
# 1. update_outdated_lessons.py modifies cyberlearn_template.db
# 2. update_template_database.py overwrites it with cyberlearn.db
# Result: Your changes are lost!
```

### ✅ CORRECT: Modify working DB, then copy to template

```bash
# Always follow this order:
# 1. Modify cyberlearn.db (working database)
# 2. Copy cyberlearn.db → cyberlearn_template.db (template)
```

## Script Configuration

### `compare_lessons_to_db.py`
```python
# Check working database:
DB_PATH = "cyberlearn.db"

# OR check template database:
DB_PATH = "cyberlearn_template.db"
```

### `update_outdated_lessons.py`
```python
# Always use working database:
DB_PATH = "cyberlearn.db"
```

## Why This Matters

The template database (`cyberlearn_template.db`) is deployed to VMs when users run:
```bash
bash update_vm.sh
```

If the template is out of sync with lesson files:
- VMs get outdated content
- Users see old lessons
- Inconsistent learning experience

## Verification Checklist

Before committing template database:

- [ ] `cyberlearn.db` has all 594 lessons
- [ ] All lessons in `cyberlearn.db` match their JSON files
- [ ] Template database copied from working database
- [ ] Template database verified with comparison script
- [ ] All checks pass (0 outdated, 0 missing, 0 extra)

## Troubleshooting

### "4 lessons outdated after running update_template_database.py"

**Cause**: You modified the template database directly, then `update_template_database.py` overwrote it with the old working database.

**Fix**:
```bash
# 1. Change scripts to use working database
# In update_outdated_lessons.py: DB_PATH = "cyberlearn.db"

# 2. Run update on working database
python update_outdated_lessons.py

# 3. Copy working → template
python update_template_database.py
```

### "No such file: cyberlearn.db"

**Cause**: Working database doesn't exist yet.

**Fix**:
```bash
# Run the app to create working database
streamlit run app.py

# OR load lessons from scratch
python load_all_lessons.py
```

## Reference

See also:
- [CLAUDE.md](CLAUDE.md) - Main project instructions
- [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md) - Lesson creation guide
- [FINAL_FIXES_READY.md](FINAL_FIXES_READY.md) - Deployment instructions
