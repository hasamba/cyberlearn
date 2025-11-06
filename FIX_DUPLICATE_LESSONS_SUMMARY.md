# Fix Duplicate Lesson Numbers - Summary

## Problem Identified

Multiple lessons in various domains had duplicate `order_index` numbers in their filenames:

### Domains Affected:
- **DFIR**: 31 duplicate numbers (most affected)
- **Pentest**: 5 duplicate numbers
- **Linux**: 4 duplicate numbers
- **Red Team**: 2 duplicate numbers
- **Fundamentals**: 1 duplicate number
- **Malware**: 1 duplicate number
- **System**: 1 duplicate number

### Examples of Duplicates:
- `lesson_dfir_23_wxtcmd_RICH.json` and `lesson_dfir_23_services_scheduled_tasks_forensics_RICH.json`
- `lesson_linux_09_container_runtime_threat_hunting_RICH.json` and `lesson_linux_09_kernel_security_hardening_RICH.json`

## Solution Implemented

### 1. Analysis Script (`find_duplicate_lesson_numbers.py`)
Created a script to:
- Scan all lesson files in the `content/` directory
- Identify duplicate lesson numbers within each domain
- Generate a comprehensive renumbering plan
- Provide statistics and summary by domain

### 2. Renumbering Script (`renumber_lessons.py`)
Created a script that:
- Sequentially renumbers all lessons within each domain (01, 02, 03, ...)
- Uses two-phase renaming to avoid filename conflicts
- Updates the `order_index` field inside each JSON file to match the new number
- Preserves all other lesson data

### 3. UI Enhancement - Short Lesson ID
Added short lesson ID display throughout the application:

#### Changes to `models/lesson.py`:
```python
def get_short_id(self) -> str:
    """Generate short lesson ID like 'dfir23' or 'malware04'"""
    return f"{self.domain}{self.order_index:02d}"
```

#### Changes to `ui/pages/lesson_viewer.py`:
1. **Lesson Detail View** (line 600):
   - Added short ID next to domain: `📚 Domain: Dfir | 🆔 dfir23`

2. **Lesson Card View** (line 228):
   - Added short ID as first property: `🆔 dfir23`
   - Now shows 4 properties: ID, Time, Difficulty, XP

## How to Apply the Fix

### On Your Development Machine (Run These Commands):

```bash
# 1. Run the renumbering script
python renumber_lessons.py

# 2. Reload all lessons into the database
python load_all_lessons.py

# 3. Update the template database (IMPORTANT!)
python update_template_database.py

# 4. Commit the changes
git add content/
git add cyberlearn_template.db
git commit -m "Fix duplicate lesson numbers and add short lesson IDs

- Renumbered 353 lessons across 7 domains to eliminate duplicates
- Updated order_index in JSON files to match new sequential numbering
- Added get_short_id() method to Lesson model
- Display short lesson IDs (e.g., 'dfir23') in lesson viewer UI
- Updated template database with corrected lesson numbering"

git push
```

### On Your VM:

```bash
# Pull the latest changes from GitHub
bash update_vm.sh
```

This will:
- Get the renumbered lesson files
- Get the updated template database
- Restart the application with correct lesson numbering

## Benefits

1. **Unique Sequential Numbers**: Each lesson within a domain now has a unique sequential number
2. **Easy Reference**: Short IDs like `dfir23` or `malware04` make it easy to reference specific lessons
3. **Better Organization**: Sequential numbering makes it clear how many lessons are in each domain
4. **No Gaps**: All lessons numbered consecutively (no missing numbers in sequence)
5. **UI Enhancement**: Short IDs visible in both lesson cards and lesson detail view

## Files Changed

### New Files:
- `find_duplicate_lesson_numbers.py` - Analysis script
- `renumber_lessons.py` - Renumbering script
- `FIX_DUPLICATE_LESSONS_SUMMARY.md` - This file

### Modified Files:
- `models/lesson.py` - Added `get_short_id()` method
- `ui/pages/lesson_viewer.py` - Display short IDs in lesson cards and detail view
- `content/lesson_*.json` - 353 files renamed and order_index updated
- `cyberlearn_template.db` - Updated with correct lesson numbering

## Statistics

### Total Lessons Affected: 353
- **Active Directory**: 13 files renumbered
- **Blue Team**: 13 files renumbered
- **DFIR**: 239 files renumbered (largest domain)
- **Fundamentals**: 3 files renumbered
- **Linux**: 13 files renumbered
- **Malware**: 10 files renumbered
- **Pentest**: 52 files renumbered
- **Red Team**: 19 files renumbered
- **System**: 4 files renumbered

### Lessons by Domain (After Fix):
Each domain now has lessons numbered from 01 to N (sequential, no gaps or duplicates)

## Testing Checklist

After applying the fix, verify:
- [ ] All lessons load correctly: `python load_all_lessons.py`
- [ ] No validation errors in lesson JSON files
- [ ] Short IDs display correctly in lesson cards (e.g., `🆔 dfir01`)
- [ ] Short IDs display correctly in lesson detail view (e.g., `📚 Domain: Dfir | 🆔 dfir23`)
- [ ] Lesson order_index matches filename number
- [ ] No duplicate lesson numbers within any domain
- [ ] All lessons accessible in Streamlit app
- [ ] Template database includes all renumbered lessons

## Notes

- The renumbering script uses a two-phase rename (temp names first) to avoid conflicts
- Original lesson UUIDs are preserved (only filenames and order_index changed)
- Prerequisites and tags are not affected by this change
- All lesson content remains unchanged
