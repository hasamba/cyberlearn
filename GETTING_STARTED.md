# Getting Started - Dev Machine Setup

**Run these commands on your dev machine to get the database in the correct state**

---

## Step 1: Apply UI Preferences Migration

This adds the columns needed for username and tag persistence:

```bash
python add_ui_preferences.py
```

**Expected output:**
```
============================================================
ADDING UI PREFERENCES TO DATABASE
============================================================
✓ last_username column: ✅ Added successfully
✓ preferred_tag_filters column: ✅ Added successfully
✅ UI PREFERENCES MIGRATION COMPLETED!
```

---

## Step 2: Reset Tag System

Your database currently has only 5 tags instead of 15. Run this to populate with the new tag structure:

```bash
python add_tags_system.py
```

This will create all 15 system tags:
- 3 Content Tags (Built-In, User Content, Community)
- 10 Career Path Tags (with "Career Path:" prefix)
- 2 Package Tags (with "Package:" prefix)

---

## Step 3: Verify Database State

Run the check script to confirm everything is correct:

```bash
python dev_tools/check_migration_status.py
```

**Expected output:**
```
============================================================
DATABASE MIGRATION STATUS
============================================================

Database: c:\Users\yaniv\...\cyberlearn.db

✓ users table exists
✓ last_username column: ✅ EXISTS
✓ preferred_tag_filters column: ✅ EXISTS
✓ tags table exists
✓ lesson_tags table exists

Total tags: 15
System tags: 13
Custom tags: 2

Career Path Tags (10):
  - Career Path: SOC Tier 1
  - Career Path: SOC Tier 2
  ...

============================================================
✅ DATABASE IS READY!
============================================================
```

---

## Step 4: Test Username and Tag Persistence

Test that the persistence features work:

```bash
python dev_tools/test_username_save.py
```

This will verify that username and tag preferences are being saved to the database correctly.

---

## Step 5: Test the App

Start the app and test the features:

```bash
streamlit run app.py
```

**Test checklist:**
- [ ] Auto-login works (logs in with last user automatically)
- [ ] Logout button works (requires "Quick Login" to log back in)
- [ ] Username persists across browser refreshes
- [ ] Tag filters persist across browser refreshes
- [ ] Tag management button (🏷️) works on lesson cards
- [ ] Can add/remove tags from lessons

---

## Step 6: Commit to Repo

Once everything works on your dev machine, commit the database:

```bash
git add cyberlearn.db
git commit -m "Update database: UI preferences migration and new tag structure"
git push
```

---

## Step 7: Test on VM

On your test VM, just pull and run:

```bash
git pull
streamlit run app.py
```

**The VM should:**
- ✅ Have all 15 tags pre-configured
- ✅ Have UI preferences columns ready
- ✅ Auto-login with last user
- ✅ Persist username and tag selections
- ✅ NOT need to run any migration scripts

---

## Notes on Bulk Tagging

The bulk tagging script (`bulk_tag_lessons.py`) currently references "Course: PEN-200" which was removed during tag refactoring.

**Two options:**

### Option A: Don't use Course: PEN-200 tag
Just skip the bulk tagging for now. The script is a developer tool for your convenience.

### Option B: Create Course: PEN-200 tag
If you want to tag pentest lessons 11-30 with this tag:

```bash
python dev_tools/add_course_apt_tags.py  # Creates the tag
python dev_tools/bulk_tag_lessons.py     # Applies tags to lessons
```

---

## Summary

**On Dev Machine (Your PC):**
```bash
# 1. Apply migrations and populate tags
python add_ui_preferences.py
python add_tags_system.py

# 2. Verify state
python dev_tools/check_migration_status.py
python dev_tools/test_username_save.py

# 3. Test app
streamlit run app.py

# 4. Commit changes
git add cyberlearn.db
git commit -m "Database ready: UI preferences + new tag structure"
git push
```

**On Test VM:**
```bash
# Just pull and run
git pull
streamlit run app.py
```

That's it! The database is now shipped pre-configured with all features ready to use.
