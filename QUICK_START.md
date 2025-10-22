# CyberLearn - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (on your VM)

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed streamlit-1.28.0 pydantic-2.5.0 plotly-5.17.0 python-dateutil-2.8.2
```

---

### Step 2: Initialize System (on your VM)

Create a file called `setup.py` with this content:

```python
import json
from uuid import UUID
from utils.database import Database
from models.lesson import Lesson

# Initialize database
print("📊 Initializing database...")
db = Database()
print("✅ Database created: cyberlearn.db")

# Load sample lesson
print("📚 Loading sample CIA Triad lesson...")
with open('content/sample_lesson_cia_triad.json', 'r') as f:
    data = json.load(f)

data['lesson_id'] = UUID(data['lesson_id'])
data['prerequisites'] = [UUID(p) for p in data['prerequisites']]

lesson = Lesson(**data)

if db.create_lesson(lesson):
    print(f"✅ Lesson '{lesson.title}' loaded successfully!")
else:
    print("ℹ️ Lesson already exists in database")

db.close()
print("\n🎉 Setup complete! Run: streamlit run app.py")
```

Then run it on your VM:

```bash
python setup.py
```

---

### Step 3: Launch Application (on your VM)

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

### Step 4: Test the System

**In your browser**, go to `http://localhost:8501` (or your VM's IP:8501)

#### Test Checklist:

1. **Create Account**
   - Click "Create Account" tab
   - Enter username: `testuser`
   - Click "Create Account"
   - ✅ Should see welcome message

2. **Complete Diagnostic**
   - Click "Start Diagnostic" button
   - Answer 20 questions (click any option)
   - Click "Complete Assessment"
   - ✅ Should see skill profile radar chart

3. **View Dashboard**
   - ✅ Should see:
     - Level 1 - Apprentice
     - 0 XP
     - Recommended lesson: "CIA Triad"
     - Skill radar chart

4. **Start Lesson**
   - Click "Start Lesson" on CIA Triad
   - ✅ Should see lesson content
   - Navigate through all blocks (click Next)
   - ✅ Memory aids, real-world connections visible

5. **Complete Quiz**
   - Answer all 5 questions
   - Click "Submit Quiz"
   - ✅ Should see:
     - XP earned (with multipliers)
     - Score percentage
     - Encouragement message
     - Balloons animation

6. **Check Progress**
   - Go to Dashboard
   - ✅ Should show:
     - Updated XP (100-300 depending on score)
     - 1 lesson completed
     - Skill in Fundamentals increased

7. **View Achievements**
   - Click "Achievements" in sidebar
   - ✅ Should see badge gallery
   - Some badges earned (if criteria met)

8. **View Profile**
   - Click "Profile" in sidebar
   - ✅ Should see user stats
   - Can edit preferences

9. **Test Logout/Login**
   - Click "Logout"
   - Login with same username
   - ✅ Streak updated, progress preserved

---

## 🎯 What You Should See

### Welcome Page
```
🛡️ CyberLearn
Accelerated Cybersecurity Mastery with Adaptive Learning

Features:
- Adaptive Learning Engine
- Gamified Experience
- Jim Kwik Principles
...

[Login] [Create Account]
```

### Dashboard (After Login)
```
🏠 Dashboard

🔥 1 day streak maintained! Keep it up!

[Level 1]  [150 XP]  [1 Lesson]  [1 Badge]

📚 Recommended for You
🎯 The CIA Triad: Foundation of Cybersecurity
[Start Lesson]

📊 Your Skill Levels
[Radar chart showing domains]
```

### Lesson Page
```
The CIA Triad: Foundation of Cybersecurity
Understanding Confidentiality, Integrity, and Availability

Section 1 of 8
[Progress bar]

💪 Welcome to Your Cybersecurity Journey
You're about to learn the foundation...

[Next →]
```

### Completion Screen
```
🎉 Lesson Completed! Score: 100%
🎈 [Balloons animation]

🏆 Rewards
XP Earned: 180 XP
- Base XP: 100
- Perfect Score: 1.5x
- First Try Success: 1.2x
Total: 180 XP

🏅 New Badges Unlocked!
Fundamentals Beginner - Complete first fundamentals lesson

[Back to Dashboard]
```

---

## 🔧 Common Issues & Fixes

### Issue: `ModuleNotFoundError: No module named 'streamlit'`

**Fix (run on VM):**
```bash
pip install streamlit pydantic plotly python-dateutil
```

---

### Issue: `FileNotFoundError: content/sample_lesson_cia_triad.json`

**Fix (run on VM):**
```bash
# Make sure you're in the project root directory
ls content/sample_lesson_cia_triad.json
# Should show the file. If not, check your current directory:
pwd
```

---

### Issue: Database errors or "table already exists"

**Fix (run on VM):**
```bash
# Remove and reinitialize database
rm cyberlearn.db
python setup.py
```

---

### Issue: Port 8501 already in use

**Fix (run on VM):**
```bash
# Use different port
streamlit run app.py --server.port=8502

# Or find and kill process using 8501
lsof -i :8501  # Note the PID
kill <PID>
```

---

### Issue: Application loads but lesson doesn't appear

**Check database (run on VM):**
```bash
sqlite3 cyberlearn.db "SELECT lesson_id, title FROM lessons;"
# Should show: 00000000-0000-0000-0000-000000000001|The CIA Triad...

# If empty, reload lesson:
python setup.py
```

---

## 📱 Accessing from Other Devices

### From Another Computer on Same Network

On your VM, find the IP address:
```bash
hostname -I  # Linux
ipconfig     # Windows
```

Then on other device, go to: `http://YOUR_VM_IP:8501`

Example: `http://192.168.1.100:8501`

---

### From Internet (Production Deployment)

See `IMPLEMENTATION_PLAN.md` Phase 5 for:
- Nginx reverse proxy setup
- SSL certificate (Let's Encrypt)
- Domain configuration
- Firewall rules

---

## 🎓 Next Steps

After successful setup:

1. **Create More Lessons**
   - Copy `content/lesson_template.json`
   - Follow guide in `IMPLEMENTATION_PLAN.md` Phase 2

2. **Customize Branding**
   - Edit `app.py` CSS section
   - Change colors, logo, title

3. **Add Users**
   - Share URL with learners
   - Each creates their own account

4. **Monitor Progress**
   - Check SQLite database for analytics
   - Export user progress data

5. **Scale Up**
   - Deploy to Streamlit Cloud (free)
   - Or use Docker for production
   - See `IMPLEMENTATION_PLAN.md` Phase 5

---

## 📊 System Status Checks

### Check Database Health (run on VM)

```bash
sqlite3 cyberlearn.db << EOF
SELECT 'Users:', COUNT(*) FROM users;
SELECT 'Lessons:', COUNT(*) FROM lessons;
SELECT 'Progress:', COUNT(*) FROM progress;
EOF
```

### Check Application Files (run on VM)

```bash
# Verify all required files exist
ls -R | grep -E "\.(py|json|md|txt)$"
```

### Test Database Connection (run on VM)

```python
python << EOF
from utils.database import Database
db = Database()
print("✅ Database connection successful")
lessons = db.get_all_lessons_metadata()
print(f"📚 Lessons in database: {len(lessons)}")
db.close()
EOF
```

---

## 💡 Pro Tips

1. **Open in Incognito**: Test multi-user by opening different browser sessions
2. **Use Browser DevTools**: Check console for errors if issues occur
3. **Keep Logs**: Run `streamlit run app.py > app.log 2>&1` to save logs
4. **Backup Database**: Copy `cyberlearn.db` regularly before testing
5. **Test on Mobile**: Check responsive design on phone/tablet

---

## ✅ Success Criteria

You're ready to go when:

- ✅ Application loads without errors
- ✅ Can create account and login
- ✅ Diagnostic assessment works
- ✅ Can complete CIA Triad lesson
- ✅ XP and badges awarded correctly
- ✅ Dashboard shows updated stats
- ✅ Can logout and login (data persists)

---

## 🆘 Still Having Issues?

1. Check `IMPLEMENTATION_PLAN.md` Troubleshooting section
2. Review Python version: `python --version` (need 3.10+)
3. Verify all files in place: `ls -R`
4. Check logs for detailed errors
5. Re-run setup: `rm cyberlearn.db && python setup.py`

---

## 🎉 You're All Set!

The system is now running on your VM. Commands to remember:

```bash
# Start application
streamlit run app.py

# Stop application
Ctrl+C

# Restart after changes
streamlit run app.py --server.runOnSave=true
```

**Ready to learn? Go to your browser and start your cybersecurity journey! 🛡️🚀**
