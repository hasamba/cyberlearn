# CyberLearn Installation Guide

Complete installation instructions for setting up CyberLearn on a new machine.

---

## Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads/)
- **Internet connection** - To download dependencies

---

## Quick Installation (Recommended)

### Linux/Mac

```bash
# 1. Clone the repository
git clone https://github.com/hasamba/cyberlearn.git

# 2. Navigate to project directory
cd cyberlearn

# 3. Run setup script (this does everything!)
chmod +x setup.sh
./setup.sh

# 4. Start the application
source venv/bin/activate
streamlit run app.py
```

### Windows

```batch
REM 1. Clone the repository
git clone https://github.com/hasamba/cyberlearn.git

REM 2. Navigate to project directory
cd cyberlearn

REM 3. Run setup script (this does everything!)
setup.bat

REM 4. Start the application
venv\Scripts\activate.bat
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

---

## Manual Installation (Alternative)

If the automated script doesn't work, follow these manual steps:

### Step 1: Clone Repository

```bash
git clone https://github.com/hasamba/cyberlearn.git
cd cyberlearn
```

### Step 2: Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Load Lessons into Database

```bash
python load_all_lessons.py
```

You should see output like:
```
[FOUND] 82 lesson files
============================================================
[OK] Loaded: Active Directory Fundamentals
[OK] Loaded: Group Policy Essentials
...
[LOADED] 82 lessons
[TOTAL] 82 lessons in database
```

### Step 5: Start the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`

---

## Verification

After installation, verify everything works:

1. **Open the application** - Browser should show CyberLearn welcome page
2. **Create an account** - Click "Create Account" tab, enter a username
3. **Take diagnostic** - Complete the diagnostic assessment
4. **Start learning** - You should see lesson recommendations on the dashboard

---

## Troubleshooting

### Error: "No lessons found"

**Cause**: Lessons not loaded into database

**Solution**: Run the lesson loader:
```bash
python load_all_lessons.py
```

---

### Error: "badly formed hexadecimal UUID string"

**Cause**: Database corruption or old database format

**Solution**: Delete the database and reload lessons:

**Linux/Mac:**
```bash
rm cyberlearn.db
python load_all_lessons.py
```

**Windows:**
```batch
del cyberlearn.db
python load_all_lessons.py
```

---

### Error: "Module not found"

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:

1. Activate virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate.bat`

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### Error: "Port 8501 already in use"

**Cause**: Another Streamlit instance is running

**Solution**:

1. Kill existing process or restart your machine
2. Or use a different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

### Database Issues

If you encounter any database-related errors:

```bash
# 1. Stop the application (Ctrl+C)

# 2. Delete old database
rm cyberlearn.db  # Linux/Mac
del cyberlearn.db  # Windows

# 3. Reload all lessons
python load_all_lessons.py

# 4. Restart application
streamlit run app.py
```

---

## Updating the Application

To get the latest updates:

```bash
# 1. Stop the application (Ctrl+C)

# 2. Pull latest changes
git pull origin main

# 3. Update dependencies
pip install --upgrade -r requirements.txt

# 4. Reload lessons (to get new content)
python load_all_lessons.py

# 5. Restart application
streamlit run app.py
```

---

## Running on a Server

To run CyberLearn on a server accessible from other machines:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then access from other machines using: `http://<server-ip>:8501`

---

## System Requirements

- **OS**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 500MB for application and database
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

---

## First Time Usage

1. **Create Account**: Enter a username (min 3 characters)
2. **Take Diagnostic**: Answer 20-30 questions to assess your skill level
3. **Start Learning**: Follow the recommended lessons on your dashboard
4. **Track Progress**: View your XP, level, and skill progress
5. **Earn Badges**: Complete lessons to unlock achievements

---

## Default File Locations

- **Database**: `cyberlearn.db` (SQLite database)
- **Lessons**: `content/` directory (JSON files)
- **Virtual Environment**: `venv/` directory
- **Logs**: Streamlit creates logs in `~/.streamlit/`

---

## Uninstallation

To completely remove CyberLearn:

```bash
# 1. Navigate to project directory
cd /path/to/cyberlearn

# 2. Deactivate virtual environment (if active)
deactivate

# 3. Remove entire project directory
cd ..
rm -rf cyberlearn  # Linux/Mac
rmdir /s /q cyberlearn  # Windows
```

---

## Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/hasamba/cyberlearn/issues)
2. Review [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md) for content-related questions
3. Check [CLAUDE.md](CLAUDE.md) for project documentation
4. Create a new issue on GitHub with:
   - Your operating system
   - Python version (`python --version`)
   - Full error message
   - Steps to reproduce

---

## Quick Reference

### Start Application (After Initial Setup)

**Option 1 - Using Start Script (Recommended):**

Linux/Mac:
```bash
cd cyberlearn
chmod +x start.sh  # Only needed first time
./start.sh
```

Windows:
```batch
cd cyberlearn
start.bat
```

**Option 2 - Manual Start:**

Linux/Mac:
```bash
cd cyberlearn
source venv/bin/activate
streamlit run app.py
```

Windows:
```batch
cd cyberlearn
venv\Scripts\activate.bat
streamlit run app.py
```

### Stop Application

Press `Ctrl+C` in the terminal where Streamlit is running

---

**Last Updated**: 2025-10-23
**Version**: 1.0
