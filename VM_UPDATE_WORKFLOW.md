# VM Update Workflow

This document explains how `update_vm.sh` works and the two update strategies available.

## Quick Start

On your VM, run:
```bash
bash update_vm.sh
```

You'll be presented with two options for handling the database.

## Update Strategy 1: Full Reset (Recommended for new deployments)

**Best for:**
- Fresh VM deployments
- Major schema changes (new tables, columns)
- Starting from scratch

**What happens:**
1. Pulls latest code from GitHub
2. **Deletes existing database** (all user progress, notes, XP lost)
3. Creates fresh database from `cyberlearn_template.db`
4. All 594 lessons with latest content

**Workflow:**
```bash
bash update_vm.sh
# Answer 'y' when prompted: "Delete and recreate database?"
```

**User impact:**
- ❌ All user progress lost
- ❌ All notes deleted
- ❌ XP and achievements reset
- ✅ Latest lesson content (including 190 new videos)
- ✅ Latest schema and tags

## Update Strategy 2: Incremental Update (Preserves User Data)

**Best for:**
- Production systems with active users
- Lesson content updates only
- Preserving user progress

**What happens:**
1. Pulls latest code from GitHub
2. **Keeps existing database** (user progress preserved)
3. Checks for outdated lessons (compares JSON files to database)
4. Updates only changed lessons

**Workflow:**
```bash
bash update_vm.sh
# Answer 'n' when prompted: "Delete and recreate database?"
# Answer 'y' when prompted: "Check for lesson content updates?"
```

**User impact:**
- ✅ All user progress preserved
- ✅ Notes kept
- ✅ XP and achievements maintained
- ✅ Latest lesson content applied (190 video additions)
- ⚠️ Tags may be outdated (if new tags were added)

## Interactive Prompts

### Prompt 1: Delete Database?
```
Delete and recreate database? This will remove all user data (y/n):
```

- **'y'**: Full reset (Strategy 1)
- **'n'**: Keep database, proceed to Prompt 2

### Prompt 2: Update Lessons? (Only if 'n' to Prompt 1)
```
Check for lesson content updates? This preserves user data (y/n):
```

- **'y'**: Run `update_outdated_lessons.py` (Strategy 2)
- **'n'**: Skip updates, keep everything as-is

## What Gets Updated in Each Strategy

| Feature | Strategy 1: Full Reset | Strategy 2: Incremental |
|---------|------------------------|-------------------------|
| Code (Python, Streamlit) | ✅ Updated | ✅ Updated |
| Lesson JSON files | ✅ Updated | ✅ Updated |
| Database schema | ✅ Latest | ⚠️ Unchanged |
| Lesson content in DB | ✅ All 594 lessons | ✅ Only changed lessons |
| System tags | ✅ Latest | ⚠️ Unchanged |
| User progress | ❌ Lost | ✅ Preserved |
| User notes | ❌ Lost | ✅ Preserved |
| XP and achievements | ❌ Lost | ✅ Preserved |

## Behind the Scenes: update_outdated_lessons.py

This script compares lesson JSON files to the database:

1. **Loads all JSON files** from `content/` directory
2. **Queries database** for corresponding lessons
3. **Compares content** (content_blocks, concepts, jim_kwik_principles, etc.)
4. **Updates only changed fields** in database
5. **Reports results** (X lessons updated, Y lessons skipped)

**Example output:**
```
================================================================================
UPDATE OUTDATED LESSONS IN DATABASE
================================================================================

[FILES] Loading lesson files from content/...
        Found 594 lesson files

[DB]    Connecting to database...
[CHECK] Checking for outdated lessons...
        Found 190 outdated lessons

[UPDATE] Updating outdated lessons...

[UPDATE] lesson_dfir_20_srum_execution_forensics_RICH.json
         Title: System Resource Usage Monitor (SRUM) Forensics
         Changed fields: content_blocks
         Status: SUCCESS

... (188 more lessons)

[SUCCESS] Database updated successfully!
          Updated: 190 lessons
          Skipped: 404 lessons (already current)
```

## When to Use Each Strategy

### Use Strategy 1 (Full Reset) When:
- ✅ This is a new VM deployment
- ✅ Schema migrations were applied on dev machine
- ✅ New tables or columns were added
- ✅ You don't care about user data (testing/demo environment)
- ✅ There are database corruption issues

### Use Strategy 2 (Incremental Update) When:
- ✅ This is a production system with active users
- ✅ Only lesson content changed (no schema changes)
- ✅ You want to preserve user progress
- ✅ This is a minor content update (like adding videos)

## Example Scenarios

### Scenario 1: Adding Videos to Lessons (Current Situation)

**Dev machine:**
```bash
python add_videos_to_lessons.py        # Add videos to 190 lessons
python load_all_lessons.py             # Load into database
python update_outdated_lessons.py      # Update database
python update_template_database.py     # Sync template
git add cyberlearn_template.db content/
git commit -m "Add videos to 190 lessons"
git push
```

**VM (Production with users):**
```bash
bash update_vm.sh
# Prompt 1: Delete database? → 'n' (preserve user data)
# Prompt 2: Check for updates? → 'y' (get new videos)
# Result: 190 lessons updated, user progress preserved
```

**VM (Demo/Testing):**
```bash
bash update_vm.sh
# Prompt 1: Delete database? → 'y' (fresh start)
# Result: All 594 lessons with videos, clean database
```

### Scenario 2: Adding New Domain (Schema Change)

**Dev machine:**
```bash
python add_new_domain_migration.py     # Add new skill column
python load_all_lessons.py             # Load lessons
python update_template_database.py     # Sync template
git add cyberlearn_template.db migrations/
git commit -m "Add new domain: web3_security"
git push
```

**VM:**
```bash
bash update_vm.sh
# Prompt 1: Delete database? → 'y' (REQUIRED for schema changes)
# Result: Fresh database with new domain column
```

**Why Strategy 1 required:** Schema changes (new columns) can't be applied incrementally. You need a fresh database from template.

### Scenario 3: Fixing Typos in Lessons

**Dev machine:**
```bash
# Edit lesson JSON files manually
python update_outdated_lessons.py      # Update database
python update_template_database.py     # Sync template
git add cyberlearn_template.db content/
git commit -m "Fix typos in 5 lessons"
git push
```

**VM:**
```bash
bash update_vm.sh
# Prompt 1: Delete database? → 'n' (preserve user data)
# Prompt 2: Check for updates? → 'y' (get typo fixes)
# Result: 5 lessons updated, user progress preserved
```

## Manual Update Commands

If you want to update lessons manually without running `update_vm.sh`:

```bash
# Update lessons only (preserves user data)
python scripts/update_outdated_lessons.py

# Full reset (loses user data)
rm cyberlearn.db
python setup_database.py

# Check what would be updated (dry run)
# (Not implemented yet, but could be added with --dry-run flag)
```

## Troubleshooting

### Issue: "No outdated lessons found" but I added videos
**Cause:** Database already has the latest content
**Solution:** This is normal if you ran `update_outdated_lessons.py` multiple times

### Issue: Videos not showing in app after incremental update
**Cause:** Database update failed or didn't run
**Solution:**
```bash
python scripts/update_outdated_lessons.py
# Check output for errors
```

### Issue: User data lost after incremental update
**Cause:** You chose 'y' to delete database by mistake
**Solution:** No recovery possible unless you have a database backup

### Issue: Schema errors after incremental update
**Cause:** Schema changed but you used incremental update
**Solution:** Use Strategy 1 (full reset):
```bash
rm cyberlearn.db
python setup_database.py
```

## Best Practices

1. **Always backup user database before major updates:**
   ```bash
   cp cyberlearn.db cyberlearn.db.backup_$(date +%Y%m%d)
   ```

2. **Test updates on demo VM first:**
   - Apply update on demo VM
   - Verify lessons display correctly
   - Then apply to production VM

3. **Communicate with users before full resets:**
   - If using Strategy 1, warn users their progress will be reset
   - Consider scheduled maintenance window

4. **Use incremental updates for content-only changes:**
   - Video additions
   - Typo fixes
   - Content improvements

5. **Use full resets for structural changes:**
   - Schema migrations
   - New tables/columns
   - Tag system changes

## Summary

The updated `update_vm.sh` gives you flexibility:

- **Fresh deployments**: Full reset (Strategy 1)
- **Production updates**: Incremental update (Strategy 2)
- **User data**: Preserved with Strategy 2, lost with Strategy 1
- **Automation**: Both strategies automated, just answer prompts

For the current video addition update, **Strategy 2 is recommended** for production VMs to preserve user progress while getting the new video content.

---

**Created**: 2025-11-04
**Last Updated**: 2025-11-04
**Related Files**: `update_vm.sh`, `update_outdated_lessons.py`, `setup_database.py`
