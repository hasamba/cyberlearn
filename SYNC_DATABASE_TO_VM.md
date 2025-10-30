# Sync Database to VM

## Problem
The dev host database has all tags and new domains, but the VM database doesn't.

## Solution: Copy Database from Dev Host to VM

### Step 1: On Dev Host (Windows)
```bash
# The database is already up-to-date with:
# - 17 tags
# - 401 lessons (all tagged)
# - 3 new domain columns (ai_security, iot_security, web3_security)

# Location: c:\Users\yaniv\10Root Dropbox\Yaniv Radunsky\Documents\50-59 Projects\57 ClaudeCode\57.14_Learning_app\cyberlearn.db
```

### Step 2: Copy to VM
Use one of these methods:

**Method A: Using SCP/SFTP**
```bash
# From dev host (Windows PowerShell or Git Bash):
scp "c:\Users\yaniv\10Root Dropbox\Yaniv Radunsky\Documents\50-59 Projects\57 ClaudeCode\57.14_Learning_app\cyberlearn.db" user@vm:/path/to/cyberlearn/

# Replace 'user@vm' with your actual VM user and hostname
# Replace '/path/to/cyberlearn/' with actual path on VM
```

**Method B: Using Git (if database is in .gitignore, won't work)**
Database files are typically in .gitignore, so this won't work. Use Method A or C.

**Method C: Manual Copy**
1. Download `cyberlearn.db` from dev host to your local machine
2. Upload to VM using your preferred file transfer method
3. Place in the cyberlearn project directory

### Step 3: Verify on VM
```bash
# On VM:
cd /path/to/cyberlearn
python debug_tags.py

# Should show:
# - Total tags: 17
# - Lessons with tags: 401/401 (100%)
# - New domain columns: All [OK] EXISTS
```

### Step 4: Restart Streamlit on VM
```bash
# On VM:
# Stop current Streamlit process (Ctrl+C)
streamlit run app.py
```

## Expected Result
After syncing and restarting:
- ✅ All 15 domains visible in tabs (including AI Security, IoT Security, Web3 Security)
- ✅ All lessons show tags next to the 🏷️ button
- ✅ Tag filter dropdown shows all 17 tags
- ✅ Dashboard radar chart shows all 15 domains

## Alternative: Run Migration Scripts on VM (Not Recommended)

If you prefer to run scripts instead of copying the database:

```bash
# On VM:
git pull  # Get latest code

# Run these in order:
python add_emerging_tech_domains.py  # Add new domain columns
python tag_builtin_lessons.py        # Tag all untagged lessons

# Verify:
python debug_tags.py
```

**Note**: This assumes the VM already has the tag system tables created. If not, you'll need to run the tag system migration first.

## Why This Happened
- The dev host ran all migration and tagging scripts automatically
- The VM has an older version of the database
- Database files are not synced via git (typically in .gitignore)
- Need to manually sync database or run migrations on VM

## Prevention
Going forward, after running database migrations on dev host:
1. Always sync the database to VM, OR
2. Run the same migration scripts on VM
