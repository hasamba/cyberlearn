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
- **`domain_content_library.py`** - Domain-specific content library and templates
- **`generate_lessons_from_csv.py`** - Generate lessons from CSV curriculum file
- **`generate_owasp_llm_lessons.py`** - Generate OWASP LLM Top 10 lessons
- **`generate_windows_forensics_lessons.py`** - Generate Windows forensics lessons
- **`rebuild_lessons_to_prompt.py`** - Rebuild lessons from prompts

### Content Validation & Fixing
- **`validate_lesson_compliance.py`** - Validate all lessons against compliance requirements
- **`validate_lesson_content.py`** - Validate lesson content structure and types
- **`verify_prompt_compliance.py`** - Verify lessons meet prompt requirements
- **`comprehensive_fix.py`** - Fix common validation issues (UUIDs, order_index, etc.)

### Content Enhancement
- **`add_memory_aids.py`** - Add memory aids to lessons
- **`add_mindset_coaching.py`** - Add mindset coaching sections to lessons

## Tag Management

- **`check_tags.py`** - Verify tag assignments
- **`tag_builtin_lessons.py`** - Tag lessons as built-in content
- **`tag_lessons_from_csv.py`** - Apply tags from CSV mapping file
- **`restore_all_system_tags.py`** - Restore all system tags to database
- **`restore_content_tags.py`** - Restore content category tags
- **`restore_package_tags.py`** - Restore package tags

## Utility Scripts

### Listing & Inspection
- **`list_lessons.py`** - List all lessons with metadata
- **`list_users_simple.py`** - Simple user list
- **`reload_lesson.py`** - Reload a specific lesson
- **`test_hide_functionality.py`** - Test lesson hide/unhide functionality

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

### Bulk Lesson Generation
```bash
# Generate lessons from CSV
python scripts/generate_lessons_from_csv.py

# Or generate specific lesson sets
python scripts/generate_windows_forensics_lessons.py
python scripts/generate_owasp_llm_lessons.py

# Load generated lessons
python scripts/load_all_lessons.py

# Apply tags
python scripts/tag_lessons_from_csv.py
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

# Verify tags
python scripts/check_tags.py
```

### Tag Management Workflow
```bash
# Restore system tags
python scripts/restore_all_system_tags.py

# Tag built-in lessons
python scripts/tag_builtin_lessons.py

# Apply course tags from CSV
python scripts/tag_lessons_from_csv.py

# Verify tags applied correctly
python scripts/check_tags.py
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

5. **Tag restoration**: If tags get corrupted, use the restore scripts to rebuild from scratch

## Script Categories

- **Core** (run regularly): `load_all_lessons.py`, `update_outdated_lessons.py`, `update_template_database.py`
- **Maintenance** (run as needed): `validate_lesson_compliance.py`, `compare_lessons_to_db.py`, `check_database.py`
- **Content creation** (one-time): `create_rich_lesson.py`, `generate_lessons_from_csv.py`
- **Content enhancement** (batch operations): `add_memory_aids.py`, `add_mindset_coaching.py`
- **Tag management** (as needed): `tag_builtin_lessons.py`, `tag_lessons_from_csv.py`, `restore_all_system_tags.py`
- **Utilities** (helper scripts): `list_lessons.py`, `check_tags.py`, `test_hide_functionality.py`

## Script Dependencies

Some scripts have dependencies and should be run in order:

1. **Database Setup**: `setup_database.py` → `load_all_lessons.py`
2. **Tag System**: `restore_all_system_tags.py` → `tag_builtin_lessons.py` → `tag_lessons_from_csv.py`
3. **Content Generation**: `generate_*_lessons.py` → `load_all_lessons.py` → `tag_lessons_from_csv.py`

---

**Last Updated**: 2025-11-06
**Total Scripts**: 33
