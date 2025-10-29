# Database-Backed UI Preferences Implementation

## Overview

This implementation adds **persistent storage** for username and tag filter preferences directly in the database. Unlike session-based storage, these preferences **survive browser refreshes** and **persist across sessions**.

---

## What Changed

### 1. Database Schema Updates

**New Columns in `users` Table:**
- `last_username` (TEXT) - Stores the last username entered for login convenience
- `preferred_tag_filters` (TEXT/JSON) - Stores array of preferred tag filter names

### 2. Model Updates

**File:** `models/user.py`

Added new fields to `UserProfile` class:
```python
# UI Preferences (persistent across sessions)
last_username: Optional[str] = None  # For login form convenience
preferred_tag_filters: List[str] = Field(default_factory=list)  # List of tag names
```

### 3. Database Layer Updates

**File:** `utils/database.py`

**Updated Methods:**
- `update_user()` - Now saves `last_username` and `preferred_tag_filters` to database
- `_row_to_user()` - Now loads these fields when fetching user from database

### 4. Login Logic Updates

**File:** `app.py`

**Changes:**
- Login form queries database for most recently used username
- Saves username to user's database record on successful login
- Create account sets default `preferred_tag_filters = ["Beginner"]`
- Username persists **across browser sessions** (stored in DB, not session state)

### 5. Tag Filter Updates

**File:** `ui/pages/lesson_viewer.py`

**Changes:**
- Loads tag preferences from user's database record (not session state)
- Saves tag selection changes immediately to database
- Tag preferences persist **across browser refreshes** (stored in DB)

---

## Migration Required

### Step 1: Run Migration Script

```bash
python add_ui_preferences.py
```

**What it does:**
- Adds `last_username` column to `users` table
- Adds `preferred_tag_filters` column to `users` table
- Initializes all existing users with default `["Beginner"]` tag preference

**Expected Output:**
```
Adding UI preference columns to users table...
  ✓ Added column: last_username
  ✓ Added column: preferred_tag_filters

Initializing default tag preferences for existing users...
  ✓ Set 'Beginner' as default for X users

============================================================
✅ UI preferences migration completed successfully!
============================================================
```

### Step 2: Restart Application

```bash
streamlit run app.py
```

---

## How It Works

### Username Persistence

**Before (Session State Only):**
1. User logs in with "alice"
2. Username stored in `st.session_state.last_username`
3. Browser refresh → **Username lost**
4. User must re-enter "alice"

**After (Database-Backed):**
1. User logs in with "alice"
2. Username stored in:
   - `st.session_state.last_username` (for current session)
   - `user.last_username` → Database (persistent)
3. Browser refresh → **Username loaded from database**
4. Login form pre-fills with "alice"

**Implementation:**
```python
# Load from database on app start
cursor.execute("""
    SELECT last_username
    FROM users
    WHERE last_username IS NOT NULL
    ORDER BY last_login DESC
    LIMIT 1
""")

# Save to database on login
user.last_username = username
db.update_user(user)
```

### Tag Filter Persistence

**Before (Session State Only):**
1. User selects tags: ["Beginner", "PWK Course"]
2. Stored in `st.session_state[f"tag_filter_{user.user_id}"]`
3. Browser refresh → **Selection lost**
4. Resets to default ["Beginner"]

**After (Database-Backed):**
1. User selects tags: ["Beginner", "PWK Course"]
2. Stored in:
   - `st.session_state[f"tag_filter_{user.user_id}"]` (for current session)
   - `user.preferred_tag_filters` → Database (persistent)
3. Browser refresh → **Selection loaded from database**
4. Filter shows ["Beginner", "PWK Course"]

**Implementation:**
```python
# Load from database on page render
if user.preferred_tag_filters:
    st.session_state[tag_pref_key] = user.preferred_tag_filters

# Save to database on change
if selected_tag_names != st.session_state[tag_pref_key]:
    user.preferred_tag_filters = selected_tag_names
    db.update_user(user)
```

---

## Testing

### Test 1: Username Persistence Across Browser Refresh

**Steps:**
1. Open app in browser
2. Login as "alice"
3. Note: Username shows "alice" in login form
4. **Close browser completely** (not just tab)
5. Reopen browser, navigate to app
6. Check login form

**Expected Result:**
- ✅ Username field pre-filled with "alice"
- ✅ No need to re-type username

### Test 2: Username Persistence Across Different Users

**Steps:**
1. Login as "alice"
2. Logout
3. Create new account "bob"
4. Logout
5. Check login form

**Expected Result:**
- ✅ Username field shows "bob" (most recent user)
- ✅ Can still type "alice" to login as alice
- ✅ After logging in as alice, username switches back to "alice"

### Test 3: Tag Filter Persistence Across Browser Refresh

**Steps:**
1. Login as "alice"
2. Go to "📚 My Learning"
3. Select tags: ["Intermediate", "PWK Course"]
4. Navigate to dashboard, then back to learning
5. Tags still selected? **YES** (session state works)
6. **Refresh browser (F5)**
7. Login as "alice" again
8. Go to "📚 My Learning"

**Expected Result:**
- ✅ Tag filters show ["Intermediate", "PWK Course"]
- ✅ Preferences loaded from database

### Test 4: Tag Filter Per-User Isolation

**Steps:**
1. Login as "alice"
2. Select tags: ["Beginner", "PWK Course"]
3. Logout
4. Login as "bob"
5. Check tag selection

**Expected Result:**
- ✅ Bob sees his own preferences (default: ["Beginner"])
- ✅ Alice's preferences not shown to bob
6. Logout bob, login alice again
7. ✅ Alice sees ["Beginner", "PWK Course"] (her preferences)

---

## Benefits

### Before (Session State)
- ❌ Username lost on browser refresh
- ❌ Tag filters lost on browser refresh
- ❌ Frustrating user experience during testing/development
- ✅ Fast (no database writes)

### After (Database-Backed)
- ✅ Username persists across browser refreshes
- ✅ Tag filters persist across browser refreshes
- ✅ Better user experience (settings remembered)
- ✅ Per-user preferences (isolated)
- ⚠️ Slightly slower (database writes on every tag change)

---

## Performance Considerations

**Database Writes:**
- Username: Updated only on login (infrequent)
- Tag filters: Updated on every tag selection change (frequent)

**Optimization Applied:**
- Only write to database when selection **actually changes**
- Session state used for current session (fast reads)
- Database only written on change detection

**Code:**
```python
# Only write if changed
if selected_tag_names != st.session_state[tag_pref_key]:
    st.session_state[tag_pref_key] = selected_tag_names
    user.preferred_tag_filters = selected_tag_names
    db.update_user(user)  # Only called when changed
```

---

## Architecture Comparison

### Session State Only (Old)
```
User Login
    ↓
st.session_state.last_username = "alice"
    ↓
(Browser Refresh)
    ↓
st.session_state cleared
    ↓
Username lost ❌
```

### Database-Backed (New)
```
User Login
    ↓
st.session_state.last_username = "alice" (fast access)
user.last_username = "alice" → Database (persistent)
    ↓
(Browser Refresh)
    ↓
st.session_state cleared
    ↓
Load from database: user.last_username
    ↓
Username restored ✅
```

---

## Files Modified

| File | Changes |
|------|---------|
| `models/user.py` | Added `last_username` and `preferred_tag_filters` fields |
| `utils/database.py` | Updated `update_user()` and `_row_to_user()` to handle new fields |
| `app.py` | Updated login/create account to save username to database |
| `ui/pages/lesson_viewer.py` | Updated tag filter to load/save from database |
| `add_ui_preferences.py` | **NEW** - Migration script to add database columns |
| `add_difficulty_tags.py` | (No changes, works with new system) |

---

## Rollback Instructions

If you need to rollback this change:

### Option 1: Remove Columns (Destructive)
```sql
-- Not recommended, SQLite doesn't support DROP COLUMN easily
-- Would need to recreate table
```

### Option 2: Keep Columns, Revert Code
```bash
git revert <commit-hash>
```
- Columns remain in database (unused, harmless)
- App reverts to session-state-only behavior

### Option 3: Set Fields to NULL
```sql
UPDATE users SET last_username = NULL, preferred_tag_filters = '[]';
```
- Clears all saved preferences
- App will use session state defaults

---

## Future Enhancements

### Possible Improvements:

1. **Batch Database Writes**
   - Debounce tag filter changes (write after 2 seconds of inactivity)
   - Reduces database writes for rapid tag selections

2. **User Preferences Page**
   - Dedicated page to manage all UI preferences
   - "Reset to defaults" button
   - "Clear saved username" option

3. **More UI Preferences**
   - Last viewed lesson
   - Preferred domain filter
   - Lesson sort order preference
   - Dark/light mode preference

4. **Cross-Device Sync**
   - Already works! (database is shared)
   - User logs in on different computer → preferences follow them

---

## Summary

**Run on VM:**
```bash
# 1. Add database columns
python add_ui_preferences.py

# 2. Restart app
streamlit run app.py
```

**New Features:**
- ✅ Username persists across browser refreshes
- ✅ Tag filters persist across browser refreshes
- ✅ Per-user isolated preferences
- ✅ Cross-device sync (database-backed)
- ✅ New users default to "Beginner" tag filter

**User Experience:**
- No more re-entering username on each test
- Tag selections remembered across sessions
- Seamless experience across browser refreshes
- Professional, polished application behavior
