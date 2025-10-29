# Dashboard Features - Lesson Stats & Git Status

## New Features Added to Dashboard

### 1. **📊 Lesson Progress by Domain**

Shows a compact view of lesson completion status for each domain:

**Display Format**:
```
Domain Name    Completed/Total    [Progress Bar]
Active Direc   5/11              ████████░░░░ 45%
Blue Team      3/15              ███░░░░░░░░░ 20%
Cloud          2/15              ██░░░░░░░░░░ 13%
...
```

**Features**:
- Shows completed lessons vs. total lessons per domain
- Visual progress bar for each domain
- Sorted alphabetically by domain name
- Automatically updates as you complete lessons

**Location**: Right sidebar, below "Recent Badges"

---

### 2. **🔄 Platform Status**

Shows git repository status and update information:

**Display**:
- **Last Update**: When was `git pull` last run (e.g., "Today", "2 days ago")
- **Total Lessons**: Current number of lessons in database
- **Update Status**:
  - ✅ "Up to date with GitHub" (no updates)
  - ⚠️ "Update Available! X new commits" (updates pending)
- **Current Version**: Expandable section showing commit hash, date, and message

**Features**:
- Automatically checks GitHub for new commits
- Shows how many commits behind you are
- Displays last commit information
- No GitHub API required (uses local git commands)

**Location**: Right sidebar, below "Lesson Progress"

---

## How It Works

### Lesson Stats

The dashboard queries the database to get:
1. Total lessons per domain
2. Your completed lessons per domain
3. Your in-progress lessons per domain
4. Calculates not-started lessons

**Database Method**: `db.get_lesson_stats_by_domain(user_id)`

### Git Status

Uses local git commands to check:
1. Last pull timestamp (stored in `.git_info.json`)
2. Local commit hash vs. remote commit hash
3. Number of commits behind remote
4. Last commit information

**Utility Class**: `utils.git_status.GitStatus`

---

## Usage

### Updating the Platform

**Method 1: Using the wrapper script (recommended)**
```bash
python git_pull.py
```

This script:
- Runs `git pull origin main`
- Updates last pull timestamp automatically
- Shows next steps for loading new lessons

**Method 2: Manual git pull**
```bash
git pull origin main
```

Note: Manual pull won't update the timestamp, so dashboard will show "Unknown" for last update.

### Loading New Lessons

After pulling updates:
```bash
# Fix any validation errors in new lessons
python fix_everything.py

# Or just load lessons directly
python load_all_lessons.py

# Restart Streamlit to see new lessons
streamlit run app.py
```

---

## Technical Details

### Files Modified

1. **`utils/database.py`**:
   - Added `get_lesson_stats_by_domain(user_id)` method
   - Added `get_total_lesson_count()` method

2. **`utils/git_status.py`** (new):
   - `GitStatus` class for git operations
   - `check_for_updates()` - Check remote for new commits
   - `get_last_pull_time()` - Get timestamp from `.git_info.json`
   - `update_pull_time()` - Update timestamp
   - `get_last_commit_info()` - Get current commit details

3. **`ui/pages/dashboard.py`**:
   - Added `render_lesson_stats()` function
   - Added `render_git_status()` function
   - Integrated into main dashboard layout

4. **`git_pull.py`** (new):
   - Wrapper script for git pull
   - Automatically updates timestamp
   - Shows next steps

### Data Storage

**`.git_info.json`** (created automatically):
```json
{
  "last_pull": "2025-10-29T15:30:45.123456"
}
```

This file is ignored by git (should be in `.gitignore`) and stores local-only metadata.

---

## Configuration

### Add to `.gitignore`

Make sure `.git_info.json` is ignored:
```bash
echo ".git_info.json" >> .gitignore
```

### Disable Update Checks

If you want to disable automatic update checking (e.g., offline development), modify `render_git_status()` in `dashboard.py`:

```python
# Comment out or set to always return no updates
update_status = {'has_updates': False, 'error': 'Update checks disabled'}
```

---

## Screenshots

### Lesson Progress by Domain
```
📊 Lesson Progress by Domain
─────────────────────────────
Active Direc    11/11    ████████████ 100%
Blue Team        3/15    ███░░░░░░░░░  20%
Cloud            5/15    █████░░░░░░░  33%
DFIR             7/16    ███████░░░░░  44%
...
```

### Platform Status
```
🔄 Platform Status
─────────────────
Last Update          Total Lessons
Yesterday            134

✅ Up to date with GitHub

📝 Current Version
Commit: 6d23256
Date: 2025-10-29 15:30:00 +0000
Message: Add pentest lesson validation fix
```

Or when updates are available:
```
⚠️ Update Available! 3 new commits on GitHub.
Run `git pull` to update.
```

---

## Benefits

### For Users
- **Visibility**: See progress across all domains at a glance
- **Motivation**: Track completion percentages
- **Updates**: Know when new content is available
- **Version**: See what version you're running

### For Admins
- **Monitoring**: Users can self-check if they're up to date
- **Support**: Easy to verify user's version when troubleshooting
- **Deployment**: Users know when to update platform

---

## Future Enhancements

Potential additions:
1. **Auto-update button**: Click to run `git pull` from dashboard
2. **Release notes**: Show what's new in available updates
3. **Lesson filters**: Click domain to see lessons in that domain
4. **Completion goals**: Set target completion % per domain
5. **Update notifications**: Email/alert when updates available

---

**Created**: 2025-10-29
**Feature Version**: 1.0
**Status**: Implemented and tested
