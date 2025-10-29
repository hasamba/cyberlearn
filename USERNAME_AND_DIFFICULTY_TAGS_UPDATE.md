# Username Persistence & Difficulty Tags Update

## What Changed

### 1. Username Persistence
Users no longer need to re-enter their username after each logout. The username is now saved in session state and persists across login/logout cycles.

**Files Modified:**
- `app.py` - Login form, create account form, and logout button

**Changes:**
- Login form pre-fills with last username used
- Create account saves username for next login
- Logout preserves username for convenience

### 2. Difficulty Level Tags
Added three new system tags for lesson difficulty levels:
- ⭐ **Beginner** (Green) - Difficulty 1 lessons
- ⭐⭐ **Intermediate** (Orange) - Difficulty 2 lessons
- ⭐⭐⭐ **Expert** (Red) - Difficulty 3 lessons

All existing lessons are automatically tagged with their difficulty level.

**Files Created:**
- `add_difficulty_tags.py` - Migration script to add difficulty tags

**Files Modified:**
- `ui/pages/lesson_viewer.py` - Tag filter now saves user preferences and defaults to "Beginner" for new users

### 3. Tag Filter Persistence
Tag filter selections now persist across sessions per user:
- New users see "Beginner" tag selected by default
- Returning users see their last tag selection
- Selections are saved per user (using `user_id`)

---

## Commands to Run on VM

### Step 1: Add Difficulty Tags to Database

```bash
cd /path/to/cyberlearn
python add_difficulty_tags.py
```

**Expected Output:**
```
Adding difficulty level tags...
  ✓ Added tag: ⭐ Beginner
  ✓ Added tag: ⭐⭐ Intermediate
  ✓ Added tag: ⭐⭐⭐ Expert

Auto-tagging lessons by difficulty...
  ✓ Tagged 45 lessons as Beginner
  ✓ Tagged 52 lessons as Intermediate
  ✓ Tagged 43 lessons as Expert

============================================================
✅ Difficulty tag migration completed successfully!
============================================================
Difficulty tags added: 3

Tag Details:
  ⭐ Beginner (Green) - Difficulty 1 lessons
  ⭐⭐ Intermediate (Orange) - Difficulty 2 lessons
  ⭐⭐⭐ Expert (Red) - Difficulty 3 lessons

Next steps:
1. Difficulty tags are now available for filtering
2. New users will see Beginner tag selected by default
3. Tag preferences persist across sessions
```

### Step 2: Restart Streamlit App

```bash
# Stop current app (Ctrl+C if running)
# Then restart:
streamlit run app.py
```

---

## Testing the New Features

### Test 1: Username Persistence

1. **Login with existing user**
   - Navigate to sidebar
   - Username field should be pre-filled if you logged in before
   - Click "Login"

2. **Logout and login again**
   - Click "🚪 Logout" button
   - Username should still be visible in login form
   - Click "Login" again without re-typing

3. **Create new account**
   - Enter new username in "Create Account" form
   - Click "Create Account"
   - Logout and login again
   - Username should be pre-filled

**Expected Behavior:**
- ✅ Username persists after logout
- ✅ Username persists across page refreshes (within same browser session)
- ✅ No need to re-type username each time

### Test 2: Difficulty Tags

1. **Go to Tag Management**
   - Click "🏷️ Manage Tags" in sidebar
   - Verify new tags exist:
     - ⭐ Beginner (Green)
     - ⭐⭐ Intermediate (Orange)
     - ⭐⭐⭐ Expert (Red)

2. **Check Tag Statistics**
   - Go to "Tag Statistics" tab
   - Verify all lessons are tagged with difficulty levels
   - Counts should match lesson difficulties in database

3. **Filter by Difficulty**
   - Go to "📚 My Learning"
   - Verify "Beginner" tag is selected by default (for new users)
   - Try selecting "Intermediate" and "Expert" tags
   - Verify lessons are filtered correctly

**Expected Behavior:**
- ✅ New difficulty tags visible in tag management
- ✅ All lessons auto-tagged with correct difficulty
- ✅ Filter works for all difficulty levels
- ✅ New users see "Beginner" selected by default

### Test 3: Tag Filter Persistence

1. **Select tags as User 1**
   - Login as first user
   - Go to "📚 My Learning"
   - Select multiple tags (e.g., "Beginner" + "PWK Course")
   - Note the selection

2. **Logout and login as different user**
   - Logout
   - Create or login as second user
   - Go to "📚 My Learning"
   - Second user should see their own saved selection (default: "Beginner")

3. **Return to User 1**
   - Logout from second user
   - Login as first user again
   - Go to "📚 My Learning"
   - First user's selection should be restored (e.g., "Beginner" + "PWK Course")

**Expected Behavior:**
- ✅ Each user has their own saved tag filter
- ✅ Filters persist across sessions
- ✅ New users default to "Beginner" only

---

## Current Tag System Overview

After running the migration, you'll have **21 total system tags**:

### Content & Source Tags (8)
- 🔵 Built-In
- 🟣 Advanced (high difficulty content, different from "Expert" difficulty level)
- 🔴 PWK Course
- 🟠 Eric Zimmerman Tools
- 🟢 SANS-Aligned
- ⚪ User Content
- 🩷 Community
- 🏆 Certification Prep

### Career Path Tags (10)
- 🛡️ SOC Tier 1
- 🛡️ SOC Tier 2
- 🚨 Incident Responder
- 🎯 Threat Hunter
- 🔬 Forensic Analyst
- 🦠 Malware Analyst
- 🔓 Penetration Tester
- ⚔️ Red Team Operator
- 🔧 Security Engineer
- ☁️ Cloud Security

### Difficulty Level Tags (3) - NEW!
- ⭐ Beginner (difficulty 1)
- ⭐⭐ Intermediate (difficulty 2)
- ⭐⭐⭐ Expert (difficulty 3)

---

## Technical Details

### Username Storage
- Stored in: `st.session_state.last_username`
- Persists: Within browser session (clears on browser close)
- Not actual cookies: Uses Streamlit session state
- Cleared on: Browser close or cache clear

### Tag Filter Storage
- Stored in: `st.session_state[f"tag_filter_{user.user_id}"]`
- Persists: Within browser session, per user
- Default: `["Beginner"]` for new users
- Cleared on: Browser close or cache clear

### Difficulty Tag Auto-Tagging
- Reads `difficulty` field from `lessons` table
- Maps: `1 → Beginner`, `2 → Intermediate`, `3 → Expert`
- Applied to: All existing lessons during migration
- Future lessons: Should be tagged manually or via automated tagging script

---

## Notes

### Difference Between "Advanced" and "Expert"
- **"Advanced" tag** (🟣 Purple) - High difficulty content, advanced topics
- **"Expert" difficulty tag** (⭐⭐⭐ Red) - Difficulty level 3

These are **separate concepts**:
- A lesson can be "Advanced" content (complex topics) but have difficulty 1 (Beginner)
- A lesson can be "Expert" difficulty but not tagged as "Advanced" content

**Example:**
- "Windows Registry Forensics" - Advanced content (🟣) + Expert difficulty (⭐⭐⭐)
- "Introduction to Cryptography" - Not "Advanced" content, but can be difficulty 2 (⭐⭐)

### Browser Session vs Database
- Username and tag filter preferences use **session state** (in-memory)
- Data clears when browser closes
- For persistent storage across browser sessions, would need database fields:
  - `users.last_username_used`
  - `users.preferred_tag_filters`

---

## Troubleshooting

### Issue: Username not persisting
**Cause**: Browser session cleared or cache cleared
**Fix**: This is expected behavior. Session state only persists within browser session.

### Issue: "Beginner" tag not showing
**Cause**: Migration script not run
**Fix**: Run `python add_difficulty_tags.py` on VM

### Issue: Tag filter always resets to Beginner
**Cause**: Session state key collision or user_id issue
**Fix**: Check that `user.user_id` is valid and consistent

### Issue: Lessons not tagged with difficulty
**Cause**: Migration ran before lessons loaded
**Fix**: Re-run migration after loading lessons: `python add_difficulty_tags.py`

---

## Summary

**Run on VM:**
```bash
# 1. Add difficulty tags
python add_difficulty_tags.py

# 2. Restart app
streamlit run app.py
```

**Features Added:**
1. ✅ Username persistence across login/logout
2. ✅ Three new difficulty level tags
3. ✅ Auto-tagging of all lessons by difficulty
4. ✅ Tag filter persistence per user
5. ✅ Default "Beginner" filter for new users

**User Experience Improvements:**
- No more re-entering username on each test
- Easier to filter by difficulty level
- Personalized tag filter defaults
- Consistent experience across sessions
