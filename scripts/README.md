# Scripts Directory

This directory contains utility scripts for database management, lesson maintenance, and content validation.

## Database Management

### Core Scripts
- **`setup_database.py`** - Initial database setup and schema creation
- **`load_all_lessons.py`** - Load all lesson JSON files from content/ into database
- **`update_outdated_lessons.py`** - Update only changed lessons in database (preserves user data)
- **`update_template_database.py`** - Sync working database to template database
- **`compare_lessons_to_db.py`** - Verify database sync status
- **`rebuild_database.py`** - Rebuild entire database from scratch
- **`check_database.py`** - Verify database integrity and statistics
- **`sync_database.py`** - Synchronize database with latest schema
- **`sync_lessons.py`** - Sync lesson data between database and files

## Lesson Management

### Content Creation
- **`create_rich_lesson.py`** - Interactive rich lesson generator

### Content Validation & Fixing
- **`validate_lesson_compliance.py`** - Validate all lessons against compliance requirements
- **`validate_lesson_content.py`** - Validate lesson content structure and types
- **`verify_prompt_compliance.py`** - Verify lessons meet prompt requirements
- **`comprehensive_fix.py`** - Fix common validation issues (UUIDs, order_index, etc.)

## Utility Scripts

### Listing & Inspection
- **`list_lessons.py`** - List all lessons with metadata
- **`list_users_simple.py`** - Simple user list
- **`reload_lesson.py`** - Reload a specific lesson

### Git Operations
- **`git_commit.py`** - Automated git commit helper
- **`check_git_status.py`** - Check git status

## Usage Patterns

### Fresh Deployment
```bash
# 1. Setup database schema
python scripts/setup_database.py

# 2. Load all lessons
python scripts/load_all_lessons.py

# 3. Update template database
python scripts/update_template_database.py
```

### Content Updates (Preserving User Data)
```bash
# 1. Update lesson JSON files manually or via scripts

# 2. Update database with changes only
python scripts/update_outdated_lessons.py

# 3. Sync template database
python scripts/update_template_database.py
```

### Content Creation
```bash
# Create a new rich lesson interactively
python scripts/create_rich_lesson.py

# Load new lessons into database
python scripts/load_all_lessons.py
```

### Validation & Compliance
```bash
# Validate all lessons
python scripts/validate_lesson_compliance.py

# Save report to file
python scripts/validate_lesson_compliance.py --save-report

# Fix common issues
python scripts/comprehensive_fix.py
```

### Database Verification
```bash
# Check database integrity
python scripts/check_database.py

# Compare files to database
python scripts/compare_lessons_to_db.py

# List all lessons
python scripts/list_lessons.py
```

## Important Notes

1. **Always run from project root**: All scripts expect to be run from the project root directory
   ```bash
   # Correct
   python scripts/load_all_lessons.py

   # Incorrect (don't cd into scripts/)
   cd scripts && python load_all_lessons.py
   ```

2. **Template database workflow**: After any database changes, always update the template:
   ```bash
   python scripts/update_template_database.py
   git add cyberlearn_template.db
   git commit -m "Update template database"
   ```

3. **User data preservation**: Use `update_outdated_lessons.py` for content-only changes to preserve user progress

4. **Validation before deployment**: Always run `validate_lesson_compliance.py` before pushing changes

## Script Categories

- **Core** (run regularly): `load_all_lessons.py`, `update_outdated_lessons.py`, `update_template_database.py`
- **Maintenance** (run as needed): `validate_lesson_compliance.py`, `compare_lessons_to_db.py`, `check_database.py`, `sync_database.py`
- **Content creation**: `create_rich_lesson.py`
- **Validation & fixing**: `validate_lesson_content.py`, `verify_prompt_compliance.py`, `comprehensive_fix.py`
- **Utilities**: `list_lessons.py`, `list_users_simple.py`, `reload_lesson.py`, `git_commit.py`, `check_git_status.py`

## Script Dependencies

Some scripts have dependencies and should be run in order:

1. **Database Setup**: `setup_database.py` → `load_all_lessons.py`
2. **Content Creation**: `create_rich_lesson.py` → `load_all_lessons.py` → `update_template_database.py`
3. **Database Rebuild**: `rebuild_database.py` → `load_all_lessons.py` → `update_template_database.py`

---

**Last Updated**: 2025-11-06
**Total Scripts**: 19
