# CyberLearn Setup Guide

**Simple installation guide for end users**

---

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/hasamba/cyberlearn.git
cd cyberlearn
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python setup_database.py
```

This creates your database from the template with:
- ✅ 82 lessons across 9 domains
- ✅ 15 system tags (career paths, packages, content)
- ✅ All migrations applied

### 5. Run the App
```bash
streamlit run app.py
```

That's it! The app will open in your browser.

---

## Updating the App

### Get Latest Changes
```bash
git pull
streamlit run app.py
```

The database and content are already updated in the repository.

---

## Optional: Adding Custom Lessons

If you want to add your own lessons:

### 1. Create Lesson JSON File
Place your lesson file in `content/` directory:
```json
{
  "lesson_id": "...",
  "title": "Your Lesson Title",
  "domain": "fundamentals",
  ...
}
```

### 2. Load Into Database
```bash
python load_all_lessons.py
```

This scans `content/` and loads any new lessons.

---

## Troubleshooting

### Database Issues
If you encounter database errors:

```bash
# Backup your database first
cp cyberlearn.db cyberlearn.db.backup

# Pull fresh database from repo
git checkout cyberlearn.db

# Restart app
streamlit run app.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

---

## User Workflows

### Normal Usage
```bash
# Update code
git pull

# Start app
streamlit run app.py

# That's it!
```

### Adding Custom Content
```bash
# 1. Add lesson JSON to content/
# 2. Load lessons
python load_all_lessons.py

# 3. Restart app
streamlit run app.py
```

### Managing Tags (via UI)
- Click "🏷️ Manage Tags" in sidebar
- Create/edit/delete custom tags
- Tag lessons using 🏷️ button on lesson cards

---

## What NOT to Do

❌ **Don't run scripts in dev_tools/** - These are for developers only

❌ **Don't modify the database manually** - Use the app UI or load_all_lessons.py

❌ **Don't run migration scripts** - Already applied in the repo

---

## File Structure (User Perspective)

```
cyberlearn/
├── app.py                     # Main app - RUN THIS
├── load_all_lessons.py        # Optional: Load custom lessons
├── cyberlearn.db              # Database (pre-configured)
├── content/                   # Lessons (add custom ones here)
│   ├── lesson_*.json
│   └── lesson_*_RICH.json
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

**Ignore everything else** - It's code and config files you don't need to touch.

---

## Support

### Documentation
- [README.md](README.md) - Project overview
- [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md) - Create lessons
- [TAGGING_GUIDE.md](TAGGING_GUIDE.md) - Tag system reference

### Common Questions

**Q: Do I need to run migrations?**
A: No, they're already applied in the database.

**Q: How do I update the app?**
A: `git pull` and restart.

**Q: Can I add my own lessons?**
A: Yes! Add JSON to `content/` and run `load_all_lessons.py`.

**Q: What if something breaks?**
A: `git checkout cyberlearn.db` to restore database.

---

## Summary

### Regular User
```bash
git pull               # Update
streamlit run app.py   # Run
```

### Content Creator
```bash
# Add lesson JSON to content/
python load_all_lessons.py
streamlit run app.py
```

**That's all you need to know!** 🎉
