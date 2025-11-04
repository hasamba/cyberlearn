# Scripts Directory

This directory contains utility scripts for database management, lesson maintenance, and content validation.

## Database Management

### Core Scripts
- **`load_all_lessons.py`** - Load all lesson JSON files from content/ into database
- **`update_outdated_lessons.py`** - Update only changed lessons in database (preserves user data)
- **`update_template_database.py`** - Sync working database to template database
- **`compare_lessons_to_db.py`** - Verify database sync status
- **`rebuild_database.py`** - Rebuild entire database from scratch
- **`check_database.py`** - Verify database integrity and statistics

### Migration Scripts
- **`add_assessment_tables.py`** - Add assessment tables (questions, user_answers)
- **`add_hidden_column.py`** - Add hidden column to lessons table
- **`add_lesson_notes_table.py`** - Add notes table for user annotations
- **`add_user_id_to_tags.py`** - Add user_id to lesson_tags for multi-user support
- **`add_user_preferences_columns.py`** - Add UI preferences columns
- **`migrate_tags_to_database.py`** - Migrate tags from JSON to database
- **`migrate_tags_to_database_v2.py`** - Updated tag migration
- **`fix_tag_system_flags.py`** - Fix tag system flags in database

## Lesson Management

### Content Creation
- **`create_rich_lesson.py`** - Interactive rich lesson generator

### Content Validation & Fixing
- **`validate_lesson_compliance.py`** - Validate all lessons against compliance requirements
- **`comprehensive_fix.py`** - Fix common validation issues (UUIDs, order_index, etc.)
- **`fix_all_compliance_issues.py`** - Round 1 fixes (duplicates, Jim Kwik principles)
- **`fix_remaining_compliance_issues.py`** - Round 2 fixes (placeholder text)
- **`fix_post_assessment_wrapping.py`** - Fix assessment question wrapping
- **`restructure_minimal_lessons.py`** - Round 3 fixes (restructure lessons with too few blocks)

### Video Content Addition
- **`generate_video_mapping.py`** - Identify lessons needing videos
- **`auto_suggest_videos.py`** - Auto-suggest YouTube videos based on lesson topics
- **`add_videos_to_lessons.py`** - Add video blocks to lessons

### Assessment Management
- **`populate_assessment_questions.py`** - Populate assessment questions in database

## Utility Scripts

### Listing & Inspection
- **`list_lessons.py`** - List all lessons with metadata
- **`list_users.py`** - List all users
- **`list_users_simple.py`** - Simple user list
- **`check_tags.py`** - Verify tag assignments
- **`reload_lesson.py`** - Reload a specific lesson

### Git Operations
- **`git_commit.py`** - Automated git commit helper
- **`check_git_status.py`** - Check git status

## Usage Patterns

### Fresh Deployment
```bash
# 1. Run migrations (if needed)
python scripts/add_assessment_tables.py

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

### Adding Videos to Lessons
```bash
# 1. Generate video mapping
python scripts/generate_video_mapping.py

# 2. Auto-suggest videos
python scripts/auto_suggest_videos.py

# 3. Apply videos to lessons
python scripts/add_videos_to_lessons.py

# 4. Update databases
python scripts/update_outdated_lessons.py
python scripts/update_template_database.py
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
- **Maintenance** (run as needed): `validate_lesson_compliance.py`, `compare_lessons_to_db.py`, `check_database.py`
- **Content creation** (one-time): `create_rich_lesson.py`, `add_videos_to_lessons.py`
- **Migrations** (run once): `add_assessment_tables.py`, `add_hidden_column.py`, etc.
- **Utilities** (helper scripts): `list_lessons.py`, `check_tags.py`, etc.

---

**Last Updated**: 2025-11-04
**Total Scripts**: 32
