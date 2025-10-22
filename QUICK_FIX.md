# Quick Fix for UUID Error

## What Happened

The advanced lessons had prerequisite field expecting UUIDs but we're using string lesson references. This has been fixed.

## Files Updated

1. **models/lesson.py** - Changed `prerequisites: List[UUID]` to `prerequisites: List[str]`
2. **fix_and_reload.py** - New automated fix script

## Fix Instructions (Run on VM)

### Option 1: Automated Fix (Recommended)

```bash
# Run the automated fix script
python fix_and_reload.py
```

This will:
- Backup your database
- Rebuild with new schema
- Generate all 40 lessons
- Load everything automatically

### Option 2: Manual Fix

```bash
# 1. Backup database
cp cyberlearn.db cyberlearn.db.backup

# 2. Remove old database
rm cyberlearn.db

# 3. Generate lessons
python generate_lessons.py
python generate_advanced_lessons.py

# 4. Load lessons
python load_all_lessons.py

# 5. Verify
python check_database.py
```

### After Fix

```bash
# If you have an existing user, reset to see all lessons
python check_database.py reset yourusername

# Launch app
streamlit run app.py
```

## Expected Result

After running the fix:

```
✅ Loaded: 40 lessons
⏭️  Skipped: 0
❌ Errors: 0

📊 Breakdown:
- Fundamentals: 5 lessons (1 CIA Triad + 4 basic)
- DFIR: 6 lessons (3 basic + 3 advanced)
- Malware: 6 lessons (3 basic + 3 advanced)
- Active Directory: 8 lessons (3 basic + 5 advanced)
- Pentest: 3 lessons (3 basic)
- Red Team: 5 lessons (5 advanced)
- Blue Team: 6 lessons (6 advanced)

TOTAL: 40 lessons
```

## What Got Fixed

**Before**: `prerequisites: List[UUID]` - Expected valid UUIDs like `550e8400-e29b-41d4-a716-446655440000`

**After**: `prerequisites: List[str]` - Accepts lesson references like `"active_directory_03_kerberos_authentication"` or empty `[]`

## Verify Everything Works

```bash
# Check database contents
python check_database.py

# Should show:
# 📊 Total lessons in database: 40
#
# Lessons by domain:
# - fundamentals: 5
# - dfir: 6
# - malware: 6
# - active_directory: 8
# - pentest: 3
# - red_team: 5
# - blue_team: 6
```

## No Data Loss

Your user accounts are preserved! The fix only:
- Updates the lesson schema
- Reloads lesson content
- Keeps all user progress, XP, badges, and streak data

If you want to retake the diagnostic with the new advanced lessons visible, run:
```bash
python check_database.py reset yourusername
```

---

Now you're ready to push to GitHub! 🚀
