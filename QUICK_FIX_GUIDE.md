# Quick Fix Guide - Run This on Your VM

## TL;DR - One Command Fix

```bash
python fix_everything.py
```

**This will**:
1. Fix database domain naming (`blueteam` → `blue_team`)
2. Fix user model (`redteam/blueteam` → `red_team/blue_team`)
3. Fix validation errors in 7 lessons
4. Load all OSINT lessons into database

**Time**: ~5 minutes

---

## Or Step-by-Step

If you prefer to run fixes individually:

### Step 1: Fix Domain Names
```bash
python fix_domain_naming.py
```

### Step 2: Fix User Model
```bash
python fix_user_model.py
```

### Step 3: Fix Validation Errors (Old Lessons)
```bash
python fix_post_assessments.py
```

### Step 4: Fix Validation Errors (New Pentest Lessons)
```bash
python fix_pentest_lessons.py
```

### Step 5: Load Lessons
```bash
python load_all_lessons.py
```

### Step 6: Verify
```bash
python list_lessons.py | grep -i osint
python list_lessons.py | grep -i pentest
```

**Expected**:
- OSINT: 10 lessons
- Pentest: 30 lessons

### Step 7: Test App
```bash
streamlit run app.py
```

---

## What Gets Fixed

### Issue 1: Domain Naming ✅
- **Before**: `redteam` (model) ≠ `red_team` (database) → skill tracking broken
- **After**: `red_team` (both) → skill tracking works

### Issue 2: OSINT Lessons ✅
- **Before**: 5 OSINT lessons in JSON files, not in database
- **After**: 10 OSINT lessons in database

### Issue 3: Validation Errors ✅
- **Before**: 7 lessons can't load (missing post_assessment fields)
- **After**: All lessons load successfully

---

## Verification Checklist

After running fixes, verify:

```bash
# Check OSINT lessons loaded
python -c "import sqlite3; conn = sqlite3.connect('cyberlearn.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM lessons WHERE domain = \"osint\"'); print(f'OSINT: {cursor.fetchone()[0]} lessons'); conn.close()"
```
**Expected**: `OSINT: 10 lessons`

```bash
# Check domain consistency
python -c "import sqlite3; conn = sqlite3.connect('cyberlearn.db'); cursor = conn.cursor(); cursor.execute('SELECT DISTINCT domain FROM lessons ORDER BY domain'); [print(d[0]) for d in cursor.fetchall()]; conn.close()"
```
**Expected**: Should include `blue_team`, `osint`, `red_team` (all with underscores)

```bash
# Start app and test
streamlit run app.py
```
**Test in UI**:
- [ ] OSINT appears in dropdown
- [ ] 10 OSINT lessons visible
- [ ] Red team lesson updates skill correctly
- [ ] Blue team lesson updates skill correctly

---

## Troubleshooting

### Error: "Module not found"
```bash
# Install dependencies
pip install -r requirements.txt
```

### Error: "File not found"
```bash
# Ensure you're in project directory
cd "c:\Users\yaniv\...\57.14_Learning_app"
pwd  # Should show project folder
```

### Error: "Database locked"
```bash
# Close Streamlit app first
# Then run fix scripts
```

### Still seeing validation errors?
```bash
# Run comprehensive fix
python comprehensive_fix.py

# Then reload
python load_all_lessons.py
```

---

## Rollback (If Needed)

If something goes wrong:

```bash
# Find backup files
ls -lt cyberlearn.db.backup_* | head -1
ls -lt models/user.py.backup_* | head -1

# Restore (replace TIMESTAMP with actual timestamp)
cp cyberlearn.db.backup_TIMESTAMP cyberlearn.db
cp models/user.py.backup_TIMESTAMP models/user.py
```

---

## Files Reference

### Fix Scripts
- `fix_everything.py` - Master script (run this!)
- `fix_domain_naming.py` - Database fixes
- `fix_user_model.py` - Model fixes
- `fix_post_assessments.py` - Validation fixes

### Documentation
- `QUICK_FIX_GUIDE.md` - This file
- `SESSION_SUMMARY_FIXES.md` - Detailed summary
- `DOMAIN_NAMING_FIX.md` - Complete domain naming documentation

---

## Support

If you encounter issues not covered here:

1. Check `SESSION_SUMMARY_FIXES.md` for detailed explanations
2. Check `DOMAIN_NAMING_FIX.md` for domain naming specifics
3. Review error messages carefully (they usually indicate the exact problem)
4. Run `python comprehensive_fix.py` for automatic common issue fixes

---

**Created**: 2025-10-29
**Purpose**: Quick reference for running fixes on VM
**Estimated time**: 5-10 minutes total
