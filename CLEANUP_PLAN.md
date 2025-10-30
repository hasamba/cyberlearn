# Project Cleanup Plan

## Files to Remove (One-Time Use Scripts)

### Migration Scripts (Already Executed)
These were one-time migrations already applied to the template database:
- `add_emerging_tech_domains.py` - Added AI/IoT/Web3 domains (DONE - in template)
- `add_owasp_ai_lessons.py` - Added OWASP lessons to CSV (DONE)
- `add_lesson_ideas.py` - Old lesson idea importer (replaced by CSV)
- `add_comprehensive_lesson_ideas.py` - One-time CSV population (DONE)

### Fix Scripts (Issues Already Fixed)
- `fix_duplicate_lesson_ids.py` - Fixed duplicate IDs (DONE)
- `fix_new_lessons_validation.py` - Fixed validation errors (DONE)

### Debug Scripts (Temporary)
- `debug_issues.py` - One-time debugging (likely obsolete)
- `debug_recommendation.py` - One-time debugging (likely obsolete)

### Old Generation Scripts
- `__generate_lessons.py` - Old lesson generator (replaced by better tools)
- `lesson_ideas.json` - Replaced by lesson_ideas.csv

## Files to Keep

### Essential Utilities
- `debug_tags.py` - KEEP - Useful for verifying tag system on VM
- `create_rich_lesson.py` - KEEP - Active tool for creating lessons
- `setup_database.py` - KEEP - Critical for VM updates
- `update_vm.sh` - KEEP - Critical for VM updates
- `load_all_lessons.py` - KEEP - Used to reload lessons
- `validate_lesson_compliance.py` - KEEP - QA tool

### Essential Documentation
- `CLAUDE.md` - KEEP - Project instructions
- `README.md` - KEEP - Main readme
- `HOW_TO_ADD_NEW_LESSONS.md` - KEEP - Important guide
- `RUN_ON_VM.md` - KEEP - VM instructions
- `SYNC_DATABASE_TO_VM.md` - KEEP - Recently added, useful
- `TAGGING_GUIDE.md` - KEEP - Tag system guide
- `ARCHITECTURE.md` - KEEP - System design
- `FEATURES.md` - KEEP - Feature tracking

### Potentially Redundant Documentation (Review)
- `ADD_NEW_DOMAINS.md` - May be redundant with CLAUDE.md
- `COMMIT_WORKFLOW.md` - May be redundant
- `CONTRIBUTING.md` - May be redundant for solo project
- `DEBUG.md` - May be outdated
- `DEVELOPER_NOTES.md` - May be redundant with CLAUDE.md
- `GETTING_STARTED.md` - May overlap with README/QUICK_START
- `GITHUB_SETUP.md` - One-time setup, may be archived
- `INDEX.md` - May be redundant
- `INSTALL.md` - May overlap with SETUP_GUIDE
- `PROJECT_SUMMARY.md` - May be redundant with README
- `QUICK_START.md` - May overlap with README
- `SETUP_GUIDE.md` - May overlap with INSTALL
- `UNIVERSAL_LESSON_PROMPT.md` - May be incorporated into CLAUDE.md
- `USER_FLOWS.md` - May be incorporated into ARCHITECTURE.md

## Recommended Action

1. **Immediate Removal**: Migration and fix scripts that are obsolete
2. **Review**: Consolidate redundant documentation
3. **Keep**: Active utilities and essential docs
