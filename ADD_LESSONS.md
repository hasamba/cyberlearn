# Adding Lessons to CyberLearn

## 🚀 Quick Start: Load 18 Lessons

Run these commands on your VM to add 18 comprehensive lessons:

```bash
# 1. Generate lesson files
python generate_lessons.py

# 2. Load lessons into database
python load_all_lessons.py

# 3. Check what's loaded
python check_database.py

# 4. Reset your user to see new lessons
python check_database.py reset yourusername

# 5. Restart app
streamlit run app.py
```

---

## 📚 Lessons Created

### Fundamentals (4 lessons)
1. ✅ CIA Triad (already exists)
2. Authentication vs Authorization
3. Encryption Fundamentals
4. Network Security Basics
5. Threat Landscape Overview

### DFIR (3 lessons)
1. Introduction to Digital Forensics
2. Chain of Custody
3. Incident Response Process

### Malware Analysis (3 lessons)
1. Malware Types and Classifications
2. Static Malware Analysis
3. Dynamic Malware Analysis

### Active Directory (3 lessons)
1. Active Directory Fundamentals
2. Group Policy Essentials
3. Kerberos Authentication

### Penetration Testing (3 lessons)
1. Penetration Testing Methodology
2. Reconnaissance Techniques
3. Exploitation Fundamentals

**Total: 18 lessons across 5 domains**

---

## 🎯 After Loading

You'll have:
- Beginner lessons (difficulty 1)
- Intermediate lessons (difficulty 2)
- Advanced lessons (difficulty 3)
- Full learning progression

The adaptive engine will:
- Recommend lessons based on your skill level
- Show appropriate difficulty
- Track your progress
- Award XP and badges

---

## ✏️ Creating Your Own Lessons

### Option 1: Use the Generator

Edit `generate_lessons.py` and add to `LESSON_CURRICULUM`:

```python
"your_domain": [
    {
        "title": "Your Lesson Title",
        "subtitle": "Brief description",
        "difficulty": 2,  # 1-4
        "order": 1,
        "concepts": ["Concept1", "Concept2"],
        "quiz": [
            {
                "q": "Question text?",
                "opts": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 1,  # Index of correct answer
                "explanation": "Why this is correct"
            }
        ]
    }
]
```

Then run: `python generate_lessons.py`

### Option 2: Manual JSON

Copy `content/sample_lesson_cia_triad.json` as template and edit.

Key requirements:
- Unique `lesson_id` (UUID)
- At least 1 learning objective
- At least 1 content block
- At least 1 quiz question in `post_assessment`
- All 10 Jim Kwik principles (or at least 4)

---

## 🔄 Push to GitHub

After generating and loading lessons:

```bash
git add generate_lessons.py load_all_lessons.py check_database.py ADD_LESSONS.md content/lesson_*.json

git commit -m "Add lesson generation system and 18 initial lessons

- Created generate_lessons.py to auto-generate lesson JSON
- Added load_all_lessons.py to batch load lessons
- Generated 18 lessons across 5 domains
- Fundamentals, DFIR, Malware, Active Directory, Pentest
- Mix of difficulty levels 1-3
- All lessons include quizzes and Jim Kwik principles"

git push origin main
```

---

## 📊 Verify Lessons Loaded

```bash
python check_database.py
```

Should show:
```
📚 Lessons: 18
   - The CIA Triad: Foundation of Cybersecurity (Domain: fundamentals, Difficulty: 1)
   - Authentication vs Authorization (Domain: fundamentals, Difficulty: 1)
   - Encryption Fundamentals (Domain: fundamentals, Difficulty: 2)
   ... (15 more)
```

---

## 🎓 Test the Learning Experience

1. Login to app
2. Take diagnostic (get skill levels 0-50)
3. Dashboard shows recommended lessons
4. Complete lessons in each domain
5. Watch skills increase
6. Earn XP and badges
7. Level up!

---

## 🚀 Next Steps

Want more lessons? You can:

1. **Expand existing domains** - Add more intermediate/advanced lessons
2. **Add Red Team & Blue Team** - Complete all 7 domains
3. **Create hands-on labs** - Add interactive Docker simulations
4. **Import external content** - Link to TryHackMe, HackTheBox rooms
5. **Community contributions** - Accept lesson submissions via GitHub

The framework is complete - it's all about content now! 🎉
