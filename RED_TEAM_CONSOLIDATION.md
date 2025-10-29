# Red Team Domain Consolidation - Complete Guide

## Problem Statement

The CyberLearn database currently has TWO separate red team domains:
- `red_team` - 5 lessons
- `redteam` - 7 lessons

This creates confusion and inconsistency with the naming convention used by other domains (e.g., `active_directory`, `blue_team`, `threat_hunting`).

## Solution: Consolidate into Single Domain

Merge both domains into a single `red_team` domain (with underscore) containing all 12 lessons.

## Why `red_team` (with underscore)?

1. **Consistency**: Matches existing domain naming convention
   - `active_directory` ✓
   - `blue_team` ✓
   - `threat_hunting` ✓
   - `red_team` ✓ (should be this)
   - ~~`redteam`~~ ✗ (inconsistent)

2. **Readability**: More readable with underscore separator

3. **Python-friendly**: Can be used as valid Python variable name

4. **Industry standard**: Most tools use snake_case for multi-word identifiers

## Current State Analysis

### red_team domain (5 lessons):
1. Red Team Initial Access Tradecraft
2. Payload Development & Execution Frameworks
3. Command & Control (C2) Infrastructure
4. Living Off The Land (LOLBins & LOLBAs)
5. Red Team Adversary Emulation

### redteam domain (7 lessons):
1. Red Team Fundamentals
2. OSINT and Reconnaissance
3. Phishing and Social Engineering
4. Web Application Attacks
5. Post-Exploitation and Lateral Movement
6. Persistence Mechanisms
7. Lazarus Group Operations and Tactics

### Consolidated red_team (12 lessons total):
All 12 lessons will be merged into single domain with order_index 1-12.

## Tools Created

### 1. consolidate_redteam_domains.py (Analysis Script)

**Purpose**: Analyze the current state before making changes

**What it shows**:
- Current lessons in each domain (red_team vs redteam)
- Lesson files and their domain fields
- Proposed consolidated order (1-12)
- Consolidation strategy and recommendations

**Usage**:
```bash
python consolidate_redteam_domains.py
```

**Output**:
- Domain analysis (lessons per domain)
- File analysis (which JSON files use which domain)
- Proposed mapping (final order after consolidation)
- Consolidation strategy

### 2. consolidate_redteam_execute.py (Execution Script)

**Purpose**: Perform the actual consolidation

**What it does**:
1. **Creates database backup** (`cyberlearn.db.backup`)
2. **Updates database**: Changes all `domain='redteam'` to `domain='red_team'`
3. **Renames lesson files**: `lesson_redteam_*.json` -> `lesson_red_team_*.json`
4. **Updates JSON files**: Changes `"domain": "redteam"` to `"domain": "red_team"`
5. **Resequences order_index**: Assigns values 1-12 (no conflicts)
6. **Verifies consolidation**: Checks database and files for success

**Usage**:
```bash
python consolidate_redteam_execute.py
```

**Safety Features**:
- Creates database backup before any changes
- Prompts for confirmation before proceeding
- Provides detailed status output for each step
- Verifies success at the end
- Tells you how to restore from backup if something fails

## Execution Plan

### Step 1: Review Current State (ANALYSIS)

Run the analysis script to see what will change:

```bash
python consolidate_redteam_domains.py
```

This shows:
- Current lesson distribution (5 vs 7)
- Which files need renaming
- Proposed consolidated order
- No data will be modified

### Step 2: Execute Consolidation (AUTOMATED)

Run the execution script to perform consolidation:

```bash
python consolidate_redteam_execute.py
```

**Interactive prompts**:
- Asks for confirmation before starting
- Creates backup automatically
- Shows progress for each step
- Reports success or warnings

**Expected output**:
```
======================================================================
RED TEAM DOMAIN CONSOLIDATION - EXECUTION
======================================================================

This script will consolidate 'redteam' and 'red_team' domains.
All 'redteam' lessons will become 'red_team' lessons.

A database backup will be created: cyberlearn.db.backup

Continue with consolidation? (yes/no): yes

======================================================================
Step 1: Creating database backup
======================================================================
[OK] Database backed up to: cyberlearn.db.backup

======================================================================
Step 2: Updating database - redteam -> red_team
======================================================================
Found 7 lessons with domain='redteam'
[OK] Updated 7 lessons to domain='red_team'

======================================================================
Step 3: Renaming lesson files
======================================================================
Found 7 files to rename:
  lesson_redteam_01_fundamentals.json -> lesson_red_team_01_fundamentals.json
  lesson_redteam_02_osint.json -> lesson_red_team_02_osint.json
  ...
[OK] Renamed 7 files

======================================================================
Step 4: Updating JSON domain fields
======================================================================
  [UPDATED] lesson_red_team_01_fundamentals.json: domain='redteam' -> 'red_team'
  ...
[OK] Updated 7 JSON files

======================================================================
Step 5: Resequencing order_index (1-12)
======================================================================
Resequencing 12 lessons:
   1. Red Team Initial Access Tradecraft                  [no change]
   2. Payload Development & Execution Frameworks          [no change]
   ...
  12. Lazarus Group Operations and Tactics                (was 7)

[OK] Resequenced 12 lessons

======================================================================
Step 6: Verification
======================================================================

Database status:
  domain='redteam': 0 lessons
  domain='red_team': 12 lessons

File status:
  lesson_redteam_*.json: 0 files
  lesson_red_team_*.json: 12 files

======================================================================
[SUCCESS] Consolidation complete!
======================================================================

Next steps:
1. Test the app: streamlit run app.py
2. Verify lessons load correctly
3. Commit changes: git add -A && git commit -m 'Consolidate red_team and redteam domains'
```

### Step 3: Verify Result

Check that consolidation was successful:

```bash
python list_lessons.py
```

**Expected output**:
```
RED_TEAM (12 lessons)
--------------------------------------------------------------------------------
   1. Red Team Initial Access Tradecraft                      [●●○] 50min
   2. Payload Development & Execution Frameworks              [●●○] 55min
   3. Command & Control (C2) Infrastructure                    [●●●] 60min
   4. Living Off The Land (LOLBins & LOLBAs)                  [●●●] 60min
   5. Red Team Adversary Emulation                            [●●●] 60min
   6. Red Team Fundamentals                                   [●○○] 45min
   7. OSINT and Reconnaissance                                [●●○] 50min
   8. Phishing and Social Engineering                         [●●○] 55min
   9. Web Application Attacks                                 [●●○] 60min
  10. Post-Exploitation and Lateral Movement                  [●●●] 60min
  11. Persistence Mechanisms                                  [●●●] 60min
  12. Lazarus Group Operations and Tactics                    [●●●] 60min
```

**No more separate `redteam` domain!**

### Step 4: Commit Changes

Once verified, commit to git:

```bash
git add -A
git commit -m "Consolidate red_team and redteam domains into single red_team domain

- Merged 5 red_team + 7 redteam lessons into single domain
- Renamed all lesson_redteam_* files to lesson_red_team_*
- Updated all JSON domain fields to 'red_team'
- Resequenced order_index 1-12 for consolidated domain
- Result: 12 lessons in unified red_team domain

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push
```

## Rollback Plan

If something goes wrong, restore from backup:

```bash
# On Linux/Mac:
cp cyberlearn.db.backup cyberlearn.db

# On Windows:
copy cyberlearn.db.backup cyberlearn.db

# Then reload lessons:
python load_all_lessons.py
```

## Benefits After Consolidation

1. **Consistent naming**: All domains follow snake_case convention
2. **Single source of truth**: Only one red_team domain
3. **Proper sequencing**: Clear progression from lesson 1-12
4. **Meets target**: 12 lessons (within 8-12 range)
5. **No duplicate content**: All 12 lessons are unique
6. **Better user experience**: No confusion about which domain to choose

## Domain Status After Consolidation

| Domain | Lessons | Status |
|--------|---------|--------|
| active_directory | 11 | ✅ Complete |
| blueteam | 11 | ✅ Complete |
| cloud | 10 | ✅ Complete |
| dfir | 11 | ✅ Complete |
| fundamentals | 11 | ✅ Complete |
| linux | 13 | ✅ Complete+ |
| malware | 10 | ✅ Complete |
| osint | 5 (loading) | ⚠️ Needs 3-7 more |
| pentest | 9 | ✅ Complete |
| **red_team** | **12** | ✅ **Complete** (after consolidation) |
| system | 10 | ✅ Complete |
| threat_hunting | 0 | ❌ Not created |

**Total**: 108 lessons (after OSINT loaded, before consolidation)
**After consolidation**: Still 108 lessons (no duplicates, just unified domain)

## Frequently Asked Questions

### Q: Will any lessons be deleted?
**A**: No, all 12 lessons will be preserved. We're only changing the domain name and organization.

### Q: Will this affect user progress?
**A**: User progress is stored by lesson_id (UUID), which doesn't change. Progress is preserved.

### Q: Can I undo the consolidation?
**A**: Yes, restore from the automatic backup (`cyberlearn.db.backup`) and manually rename files back.

### Q: Do I need to reload lessons after consolidation?
**A**: No, the consolidation script updates the database directly. Lessons remain loaded.

### Q: What if I have unsaved changes?
**A**: Commit or stash changes before running consolidation scripts.

### Q: Why not consolidate into 'redteam' instead?
**A**: Consistency with other domains. All multi-word domains use underscores (active_directory, blue_team, threat_hunting).

## Technical Details

### Database Changes

**SQL executed**:
```sql
UPDATE lessons
SET domain = 'red_team'
WHERE domain = 'redteam';
```

### File Changes

**Files renamed** (example):
```
Before: content/lesson_redteam_01_fundamentals.json
After:  content/lesson_red_team_01_fundamentals.json
```

**JSON updated** (example):
```json
{
  "lesson_id": "abc123...",
  "domain": "red_team",  // Changed from "redteam"
  "title": "Red Team Fundamentals",
  ...
}
```

### Order Index Resequencing

The script ensures no conflicts by resequencing all lessons 1-12:

```python
for new_index, (lesson_id, title, old_index) in enumerate(lessons, 1):
    cursor.execute("""
        UPDATE lessons
        SET order_index = ?
        WHERE lesson_id = ?
    """, (new_index, lesson_id))
```

## Summary

- **Problem**: Two separate red team domains (red_team, redteam)
- **Solution**: Consolidate into single red_team domain
- **Tools**: Analysis script + Execution script (automated)
- **Result**: 12 lessons in unified red_team domain
- **Safety**: Automatic backup + verification
- **Status**: ✅ Ready to execute

---

**To execute**: Run on your VM:
```bash
python consolidate_redteam_domains.py    # Review first
python consolidate_redteam_execute.py     # Then execute
python list_lessons.py                    # Verify result
```
