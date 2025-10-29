# Domain Naming Inconsistency Fix

## Issues Identified

### Issue 1: Domain Naming Inconsistency (redteam vs red_team)

**Problem**: Mixed naming convention between Pydantic models and database

**Current State**:
```python
# models/user.py (SkillLevels class)
redteam: int = Field(default=0, ge=0, le=100)    # NO underscore
blueteam: int = Field(default=0, ge=0, le=100)   # NO underscore
```

```sql
-- cyberlearn.db (lessons table)
SELECT DISTINCT domain FROM lessons;
-- Returns:
--   red_team    (WITH underscore)
--   blueteam    (NO underscore)
```

**Impact**:
- ❌ Skill tracking broken for red team lessons (looks for `redteam`, but DB has `red_team`)
- ❌ XP awards won't update correct skill field
- ❌ Adaptive engine recommendations fail
- ❌ Inconsistent naming is confusing for developers

**Root Cause**:
- Original design used `redteam` and `blueteam` (no underscores)
- Later added `red_team` domain to database (with underscore)
- Never updated the model to match

### Issue 2: OSINT Lessons Not in Database

**Problem**: OSINT lessons exist as JSON files but not loaded into database

**Current State**:
```
content/
├── lesson_osint_06_email_username_intelligence_RICH.json     ✓ Created
├── lesson_osint_07_image_geolocation_intelligence_RICH.json  ✓ Created
├── lesson_osint_08_maltego_relationship_mapping_RICH.json    ✓ Created
├── lesson_osint_09_dark_web_paste_monitoring_RICH.json       ✓ Created
└── lesson_osint_10_automation_tool_integration_RICH.json     ✓ Created

cyberlearn.db → No 'osint' domain lessons loaded yet
```

**Impact**:
- ❌ OSINT lessons don't appear in Streamlit app
- ❌ `list_lessons.py` shows no OSINT lessons
- ❌ Users can't access OSINT content

**Root Cause**:
- Lessons created as JSON files
- `load_all_lessons.py` not run yet

---

## Solution: 3-Step Fix Process

### Step 1: Fix Database Domain Naming

**Run**: `python fix_domain_naming.py`

**What it does**:
1. Creates database backup (`cyberlearn.db.backup_TIMESTAMP`)
2. Updates database: `blueteam` → `blue_team` (consistency)
3. Verifies `red_team` is correct (already has underscore)
4. Shows summary of changes

**Expected Output**:
```
[OK] Database backed up to: cyberlearn.db.backup_20251029_153000
[*] Renaming 'blueteam' → 'blue_team' (7 lessons)
[OK] Database updated
[OK] 'red_team' domain has 12 lessons
```

**Result**: Database now has consistent underscore naming:
```
✓ active_directory
✓ blue_team         (fixed)
✓ cloud
✓ dfir
✓ fundamentals
✓ linux
✓ malware
✓ pentest
✓ red_team          (already correct)
✓ system
```

### Step 2: Fix User Model

**Run**: `python fix_user_model.py`

**What it does**:
1. Creates backup (`models/user.py.backup_TIMESTAMP`)
2. Updates 6 locations in `models/user.py`:
   - Line 35: `redteam` → `red_team` (field definition)
   - Line 36: `blueteam` → `blue_team` (field definition)
   - Line 51: `self.redteam` → `self.red_team` (get_overall_level)
   - Line 52: `self.blueteam` → `self.blue_team` (get_overall_level)
   - Line 69: `"redteam"` → `"red_team"` (get_weakest_domain)
   - Line 70: `"blueteam"` → `"blue_team"` (get_weakest_domain)
3. Verifies all changes applied correctly

**Expected Output**:
```
[OK] Backup created: models/user.py.backup_20251029_153015
[OK] Updated 6 locations:
  ✓ Line 35: redteam → red_team (field definition)
  ✓ Line 36: blueteam → blue_team (field definition)
  ✓ Line 51: self.redteam → self.red_team
  ✓ Line 52: self.blueteam → self.blue_team
  ✓ Line 69: domain_map redteam → red_team
  ✓ Line 70: domain_map blueteam → blue_team
✓ All checks passed!
```

**Result**: SkillLevels model now matches database domain names perfectly.

### Step 3: Load OSINT Lessons into Database

**Run**: `python load_all_lessons.py`

**What it does**:
1. Scans `content/` directory for all `*_RICH.json` files
2. Validates each lesson with Pydantic models
3. Loads lessons into database (updates if exists, inserts if new)
4. Reports success/failure for each lesson

**Expected Output**:
```
[OK] Loaded: lesson_osint_06_email_username_intelligence_RICH.json
[OK] Loaded: lesson_osint_07_image_geolocation_intelligence_RICH.json
[OK] Loaded: lesson_osint_08_maltego_relationship_mapping_RICH.json
[OK] Loaded: lesson_osint_09_dark_web_paste_monitoring_RICH.json
[OK] Loaded: lesson_osint_10_automation_tool_integration_RICH.json

Summary:
  Successfully loaded: 5 lessons
  Errors: 0
```

**Result**: OSINT lessons now available in database and Streamlit app.

---

## Verification

### Verify Database Domains

```bash
python -c "import sqlite3; conn = sqlite3.connect('cyberlearn.db'); cursor = conn.cursor(); cursor.execute('SELECT DISTINCT domain FROM lessons ORDER BY domain'); domains = cursor.fetchall(); [print(d[0]) for d in domains]"
```

**Expected Output** (11 domains, all with underscores where applicable):
```
active_directory
blue_team          ← Fixed!
cloud
dfir
fundamentals
linux
malware
osint              ← New!
pentest
red_team
system
```

### Verify OSINT Lessons Loaded

```bash
python list_lessons.py | grep -A 10 "OSINT"
```

**Expected Output**:
```
OSINT (10 lessons)
--------------------------------------------------------------------------------
  1. Social Media Intelligence Gathering         [●] 45min
  2. DNS & Subdomain Reconnaissance               [●] 50min
  3. Search Engine OSINT Techniques               [●] 45min
  4. WHOIS & Domain Intelligence                  [●●] 50min
  5. Shodan & IoT Reconnaissance                  [●●] 55min
  6. Email & Username Intelligence                [●●] 55min
  7. Image & Geolocation Intelligence             [●●] 55min
  8. Maltego & Relationship Mapping               [●●●] 60min
  9. Dark Web & Paste Site Monitoring             [●●●] 60min
 10. OSINT Automation & Tool Integration          [●●●] 60min
```

### Verify Skill Tracking Works

```bash
# Test skill update (run in Python)
from models.user import SkillLevels

skills = SkillLevels()
print("Available skill domains:")
print(dir(skills))

# Should see: red_team, blue_team, osint, etc.
```

### Test in Streamlit App

```bash
streamlit run app.py
```

**Verification checklist**:
- [ ] OSINT appears in domain selection dropdown
- [ ] All 10 OSINT lessons visible
- [ ] Completing a red team lesson updates `red_team` skill (not error)
- [ ] Completing a blue team lesson updates `blue_team` skill (not error)
- [ ] XP awards work correctly for all domains

---

## Complete Fix Workflow

```bash
# Step 1: Fix database domain naming
python fix_domain_naming.py

# Step 2: Fix user model
python fix_user_model.py

# Step 3: Validate OSINT lessons (optional, but recommended)
python comprehensive_fix.py

# Step 4: Load all lessons (including OSINT)
python load_all_lessons.py

# Step 5: Verify database state
python list_lessons.py

# Step 6: Restart Streamlit app
streamlit run app.py
```

**Estimated time**: 5-10 minutes

---

## Technical Details

### Why Underscore Convention?

**Standardize on underscores** because:

1. **Python convention**: `snake_case` for identifiers
2. **Consistency**: Most domains already use underscores
   - `active_directory` ✓
   - `threat_hunting` ✓
3. **Database convention**: SQL/PostgreSQL uses underscores
4. **Readability**: `red_team` is clearer than `redteam`

### Domain Naming Reference

| Domain              | Old Name   | New Name         | Status      |
|---------------------|------------|------------------|-------------|
| Active Directory    | ✓          | `active_directory` | Already correct |
| Blue Team           | `blueteam` | `blue_team`      | **Fixed** |
| Cloud               | ✓          | `cloud`          | Already correct |
| DFIR                | ✓          | `dfir`           | Already correct |
| Fundamentals        | ✓          | `fundamentals`   | Already correct |
| Linux               | ✓          | `linux`          | Already correct |
| Malware             | ✓          | `malware`        | Already correct |
| OSINT               | (missing)  | `osint`          | **Added** |
| Pentest             | ✓          | `pentest`        | Already correct |
| Red Team            | `redteam`  | `red_team`       | **Fixed** |
| System              | ✓          | `system`         | Already correct |
| Threat Hunting      | ✓          | `threat_hunting` | Already correct |

---

## Rollback Instructions

If something goes wrong:

### Rollback Database
```bash
# Find backup file
ls -lt cyberlearn.db.backup_* | head -1

# Restore (replace TIMESTAMP with actual timestamp)
cp cyberlearn.db.backup_TIMESTAMP cyberlearn.db
```

### Rollback User Model
```bash
# Find backup file
ls -lt models/user.py.backup_* | head -1

# Restore (replace TIMESTAMP with actual timestamp)
cp models/user.py.backup_TIMESTAMP models/user.py
```

---

## FAQ

### Q: Will this break existing user progress?

**A**: No. User progress is stored by `lesson_id` (UUID), not domain name. Domain naming only affects:
- Skill level tracking (which domain skill to increment)
- Adaptive engine recommendations
- UI display

Existing user XP, completed lessons, and badges are unaffected.

### Q: Why not change database domains to match the old model naming?

**A**: Because:
1. Most domains already use underscores (`active_directory`, `threat_hunting`)
2. Python convention is `snake_case`
3. Easier to change model (6 lines) than database (potentially hundreds of lessons)
4. Future-proof: All new domains will use underscores

### Q: What happens if I run the fix scripts twice?

**A**: Both scripts are **idempotent**—running them multiple times is safe:
- `fix_domain_naming.py`: Checks if `blueteam` exists before renaming
- `fix_user_model.py`: Checks if old naming exists before replacing

You'll see "No changes needed (already updated)" if run twice.

### Q: Do I need to restart the Streamlit app?

**A**: **Yes**. The app loads models at startup. After changing `models/user.py`, you must restart:
```bash
# Stop app (Ctrl+C)
# Start again
streamlit run app.py
```

---

## Summary

### Before Fix
```
Database:    red_team (underscore), blueteam (no underscore)
Model:       redteam (no underscore), blueteam (no underscore)
Result:      ❌ Skill tracking broken for red team
             ❌ Inconsistent naming
             ❌ OSINT lessons not loaded
```

### After Fix
```
Database:    red_team (underscore), blue_team (underscore)
Model:       red_team (underscore), blue_team (underscore)
Result:      ✓ Skill tracking works for all domains
             ✓ Consistent underscore convention
             ✓ OSINT lessons loaded and accessible
```

---

## Files Modified

1. **cyberlearn.db** - Domain names updated
2. **models/user.py** - SkillLevels fields updated
3. **No breaking changes** - User progress preserved

## Files Created

1. **fix_domain_naming.py** - Database fix script
2. **fix_user_model.py** - Model fix script
3. **DOMAIN_NAMING_FIX.md** - This documentation

## Backups Created

1. **cyberlearn.db.backup_TIMESTAMP** - Database backup
2. **models/user.py.backup_TIMESTAMP** - Model backup

---

**Author**: Claude Code
**Date**: 2025-10-29
**Issue**: Domain naming inconsistency between database and Pydantic models
**Status**: Fix scripts ready, awaiting execution on VM
