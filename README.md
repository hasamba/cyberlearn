# CyberLearn - Adaptive Cybersecurity Learning Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An intelligent, gamified cybersecurity training system integrating Jim Kwik's accelerated learning principles to transform beginners into security professionals through adaptive, engaging daily lessons.

---

## 🎯 What is CyberLearn?

CyberLearn is a **complete adaptive learning platform** that delivers professional-level cybersecurity training through:

- **🧠 Adaptive Intelligence**: AI-powered engine that personalizes difficulty, content format, and pacing to your skill level
- **🎮 Gamification**: Earn XP, unlock badges, maintain streaks, and level up from Apprentice to Grandmaster
- **⚡ Accelerated Learning**: Every lesson implements all 10 Jim Kwik learning principles for faster, deeper mastery
- **📊 Spaced Repetition**: Smart review scheduling ensures long-term retention using cognitive science
- **🎯 15 Domains**: 12 core domains + 3 emerging tech (AI Security, IoT, Web3)
- **⏱️ 30-60 Minute Sessions**: Focused learning designed to fit busy schedules

**Current Status**: 591 professional lessons (2.4+ million words) covering all 15 domains, with 100% compliance validation

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.10 or higher
- Git

### Installation & Setup

**Linux/Mac**:

```bash
git clone https://github.com/hasamba/cyberlearn.git
cd cyberlearn
chmod +x setup.sh start.sh
./setup.sh    # One-time setup: creates venv, installs deps, loads lessons
./start.sh    # Start the application

# Access at: http://localhost:8501
```

**Windows**:

```batch
git clone https://github.com/hasamba/cyberlearn.git
cd cyberlearn
setup.bat     # One-time setup: creates venv, installs deps, loads lessons
start.bat     # Start the application

# Access at: http://localhost:8501
```

**🎉 That's it!** Create an account and start learning!

---

## 📚 Complete Documentation

| Document | Description |
|----------|-------------|
| **[CLAUDE.md](CLAUDE.md)** | **Complete project guide** - Structure, domains, lesson standards, troubleshooting |
| **[HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md)** | **Step-by-step guide** for creating lessons (manual & AI-assisted) |
| **[NEXT_LESSONS_PLAN.md](NEXT_LESSONS_PLAN.md)** | **Content roadmap** - What lessons to create next, priorities |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design, technology stack, algorithms |

---

## 🔄 Keeping Your Platform Updated

### Pull Latest Lessons

```bash
# On your VM, run:
cd cyberlearn
git pull  # Pull latest changes from GitHub

# If new lessons were added:
python validate_lesson_compliance.py  # Validate all lessons
python load_all_lessons.py            # Load new lessons into database

# Restart app:
streamlit run app.py
```

### Check for Updates in Dashboard

The dashboard automatically shows:
- ✅ **Last Update**: When you last ran `git pull`
- ⚠️ **Update Available**: If new commits exist on GitHub
- 📊 **Lesson Count**: Total lessons loaded

---

## 📝 Creating New Lessons

### Method 1: AI-Assisted (Recommended - Fastest)

**Using Any LLM** (ChatGPT, Claude, Gemini, etc.):

```bash
# 1. Copy the universal lesson prompt
cat UNIVERSAL_LESSON_PROMPT.md

# 2. Paste the entire prompt into your LLM (ChatGPT, Claude, Gemini, etc.)

# 3. Add ONE LINE with your topic:
Topic: SQL Injection Attacks

# 4. LLM automatically infers domain, difficulty, order_index, prerequisites
#    and generates complete JSON lesson (4,000-5,500 words)

# 5. Save output to content/lesson_<domain>_<number>_<topic>_RICH.json

# 6. Validate the lesson
python validate_lesson_compliance.py

# 7. Load lesson into database
python load_all_lessons.py

# 8. Verify it loaded
python list_lessons.py | grep -i "sql injection"
```

**That's it!** Just ONE LINE ("Topic: XYZ") and the LLM generates a complete, production-ready lesson following all CyberLearn standards. The AI intelligently determines domain, difficulty, order, and prerequisites from your topic.

**Time Estimate**: 1-2 minutes per lesson (vs 4-6 hours manual)

### Method 2: Template-Based (Manual)

```bash
# 1. Create lesson template
python create_lesson_template.py

# 2. Fill in content manually following rich lesson standards
# Edit the generated JSON file in content/

# 3. Fix and load
python comprehensive_fix.py
python load_all_lessons.py
```

### Method 3: Interactive Creator

```bash
# Interactive CLI lesson creator
python create_rich_lesson.py --interactive
```

### Lesson Requirements

**All lessons MUST have**:
- Valid UUID (use `uuid.uuid4()`)
- Domain from: fundamentals, osint, dfir, malware, active_directory, system, linux, cloud, pentest, red_team, blue_team, threat_hunting, ai_security, iot_security, web3_security
- Difficulty: 1 (beginner), 2 (intermediate), 3 (advanced)
- `estimated_time`: 30-60 minutes
- `prerequisites`: List of lesson_id UUIDs (empty if none)
- **Valid content block types only**: explanation, video, diagram, quiz, simulation, reflection, memory_aid, real_world, code_exercise, mindset_coach

**Rich Lesson Standards** (4,000-5,500 words):
- Deep technical content (not surface-level)
- Real-world examples (companies, attacks, case studies)
- Code snippets (commands, scripts, configurations)
- Memory aids (mnemonics, acronyms)
- Common pitfalls and warnings
- Actionable takeaways
- ASCII art diagrams where helpful

**See [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md) for complete guide with examples.**

---

## 🛠️ Scripts & Tools Reference

### 📚 Core Application Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `app.py` | Main Streamlit application | `streamlit run app.py` |
| `database.py` | Database setup and models | Imported by other scripts |
| `config.py` | Configuration management | Imported by other scripts |
| `setup_database.py` | Initialize database schema | `python setup_database.py` |

### 📖 Lesson Management

| Script | Description | Usage |
|--------|-------------|-------|
| `load_all_lessons.py` | Load all lessons from content/ into database | `python load_all_lessons.py` |
| `reload_lesson.py` | Reload a specific lesson by ID | `python reload_lesson.py <lesson_id>` |
| `list_lessons.py` | List all loaded lessons by domain | `python list_lessons.py` |
| `validate_lesson_compliance.py` | Validate all lessons against standards | `python validate_lesson_compliance.py` |
| `validate_lesson_content.py` | Validate lesson content structure | `python validate_lesson_content.py` |
| `comprehensive_fix.py` | Auto-fix common validation errors | `python comprehensive_fix.py` |

### ✍️ Lesson Creation Tools

| Script | Description | Usage |
|--------|-------------|-------|
| `create_rich_lesson.py` | Interactive lesson creator with CLI | `python create_rich_lesson.py --interactive` |
| `create_lesson_template.py` | Generate lesson JSON template | `python create_lesson_template.py` |

### 🏷️ Tagging System

| Script | Description | Usage |
|--------|-------------|-------|
| `tag_lessons_from_csv.py` | Tag lessons based on lesson_ideas.csv | `python tag_lessons_from_csv.py` |
| `check_tags.py` | Verify tag assignments | `python check_tags.py` |

### 🗄️ Database Operations

| Script | Description | Usage |
|--------|-------------|-------|
| `rebuild_database.py` | Rebuild database from scratch | `python rebuild_database.py` |
| `sync_database.py` | Sync database with content files | `python sync_database.py` |
| `check_database.py` | Check database state and contents | `python check_database.py` |
| `sync_lessons.py` | Sync lessons: remove orphaned, reload modified | `python sync_lessons.py --confirm` |
| `test_hide_functionality.py` | Test lesson hide/unhide feature | `python test_hide_functionality.py` |

### 📝 Documentation Files

| File | Description |
|------|-------------|
| `README.md` | Main project documentation (this file) |
| `CLAUDE.md` | Complete project guide for development |
| `ARCHITECTURE.md` | System architecture and design |
| `FEATURES.md` | Feature tracking and roadmap |
| `HOW_TO_ADD_NEW_LESSONS.md` | Complete lesson creation guide |
| `UNIVERSAL_LESSON_PROMPT.md` | AI lesson generation template |
| `TAGGING_GUIDE.md` | Tagging system documentation |
| `RUN_ON_VM.md` | VM deployment instructions |
| `SYNC_DATABASE_TO_VM.md` | Database sync guide for VM |

### 📊 Planning & Tracking

| File | Description |
|------|-------------|
| `lesson_ideas.csv` | Lesson curriculum planning (231 lessons tracked) |
| `requirements.txt` | Python dependencies |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                      │
│  (Dashboard, Lessons, Diagnostic, Profile, Achievements)   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Core Business Logic                       │
│  ┌────────────────────┐  ┌────────────────────────────┐   │
│  │  Adaptive Engine   │  │  Gamification Engine       │   │
│  │  - Skill profiling │  │  - XP calculation          │   │
│  │  - Lesson routing  │  │  - Badge system            │   │
│  │  - Difficulty adj  │  │  - Streak tracking         │   │
│  │  │  - Spaced review   │  │  - Level progression       │   │
│  └────────────────────┘  └────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Data Layer (SQLite)                       │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Users  │  │ Lessons  │  │ Progress │  │   Domain   │  │
│  │         │  │          │  │          │  │  Progress  │  │
│  └─────────┘  └──────────┘  └──────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Tech Stack:**
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Pydantic V2
- **Frontend**: Streamlit (interactive UI), Plotly (visualizations)
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Content**: JSON-based modular lessons
- **Deployment**: Docker, VM, or Streamlit Cloud

---

## 📊 Domain Structure (15 Domains)

### Core Domains (12)

| Domain | Lessons | Prerequisites | Description |
|--------|---------|---------------|-------------|
| **fundamentals** | 17 | None | Security basics, CIA Triad, Authentication, GRC |
| **osint** | 37 | fundamentals | OSINT, cybercrime intelligence (SANS FOR589) |
| **dfir** | 237 | fundamentals | Digital forensics, IR (SANS FOR500/508/528/572, 13Cubed) |
| **malware** | 21 | fundamentals | Malware analysis & reverse engineering |
| **active_directory** | 24 | fundamentals | AD security, attacks, defense |
| **system** | 22 | fundamentals | Windows/Linux internals |
| **linux** | 22 | fundamentals | Linux security & administration |
| **cloud** | 45 | fundamentals + system | AWS, Azure, GCP, Kubernetes (SANS FOR509) |
| **pentest** | 62 | fundamentals + AD | Penetration testing (SANS SEC504) |
| **red_team** | 26 | pentest + malware | Red team operations & TTPs |
| **blue_team** | 28 | dfir + malware | Blue team defense, SIEM (SANS FOR608) |
| **threat_hunting** | 30 | blue_team | Threat hunting & enterprise IR (SANS FOR608) |

### Emerging Technology Domains (3)

| Domain | Lessons | Prerequisites | Description |
|--------|---------|---------------|-------------|
| **ai_security** | 13 | fundamentals | AI/ML security, OWASP LLM Top 10 |
| **iot_security** | 4 | fundamentals + system | IoT device security, embedded systems |
| **web3_security** | 3 | fundamentals | Blockchain, smart contract security |

**Total**: 591 professional lessons (2.4+ million words)

---

## 🧠 Jim Kwik Learning Principles Integration

Every lesson implements all 10 accelerated learning principles:

| Principle | Implementation |
|-----------|----------------|
| 🎮 **Active Learning** | Interactive simulations, hands-on labs, scenario analysis |
| 🎯 **Minimum Effective Dose** | Focus on 20% core concepts that deliver 80% results |
| 🎈 **Teach Like I'm 10** | Simplified explanations, plain language, progressive complexity |
| 💡 **Memory Hooks** | Mnemonics, metaphors, storytelling, visual imagery |
| 🤔 **Meta-Learning** | Reflective prompts: "What question should I be asking?" |
| 🌍 **Connect to What I Know** | Real-world analogies, everyday examples, industry scenarios |
| 💪 **Reframe Limiting Beliefs** | Mindset coaching, growth mindset reinforcement |
| 🏆 **Gamify It** | XP, badges, levels, streaks, leaderboards |
| ⏱️ **Learning Sprint** | Focused 30-min sessions, weekend crash courses |
| 📊 **Multiple Memory Pathways** | Visual diagrams, text, interactive exercises, emotional stories |

---

## ✨ Key Features

### 🎓 For Learners

- **Diagnostic Assessment**: Initial skill profiling across all 12 domains
- **Personalized Path**: Adaptive recommendations based on performance
- **Interactive Lessons**: Mix of text, visuals, simulations, and quizzes
- **Progress Tracking**: Real-time skill levels, completion rates, mastery metrics
- **Gamification**: 40+ badges, 6 levels, daily streaks, XP multipliers
- **Spaced Repetition**: Automatic review scheduling for long-term retention
- **Mobile-Friendly**: Responsive design works on any device

### 📖 For Content Creators

- **JSON-Based Authoring**: Easy lesson creation with structured templates
- **Multi-Format Support**: Text, video, diagrams, code, quizzes, simulations
- **AI-Assisted Generation**: Use ChatGPT/Claude to generate lessons quickly
- **Validation Tools**: `comprehensive_fix.py` auto-corrects common errors
- **Version Control**: Git-friendly content management
- **Rapid Deployment**: Add lessons without code changes

### 🏢 For Organizations

- **Self-Hosted**: Deploy on your infrastructure for data sovereignty
- **Scalable**: SQLite for small teams, PostgreSQL for enterprise
- **Customizable**: White-label branding, custom domains
- **Analytics**: Track team progress, identify knowledge gaps
- **Compliance**: GDPR-ready, audit logs, data export

---

## 🛠️ Troubleshooting

### Validation Errors

**Error**: `Field required` or `Input should be 'explanation', 'video'...`

```bash
# Validate lessons first
python validate_lesson_compliance.py

# If validation fails, check specific errors
# Fix manually or use comprehensive_fix.py for auto-correction
python comprehensive_fix.py

# This auto-fixes:
# - Invalid UUIDs
# - Missing fields
# - Wrong content block types
# - Invalid jim_kwik_principles
# - Format issues
```

### Lessons Not Appearing

```bash
# Check what's loaded
python list_lessons.py

# Force reload all lessons
python load_all_lessons.py

# Check for errors in output
```

### Database Issues

```bash
# Check database state
python check_database.py

# Reset database (WARNING: Deletes all user progress)
rm cyberlearn.db
python load_all_lessons.py
```

### Unicode Errors (Windows)

Fixed in latest version. If you see encoding errors:

```bash
# Pull latest updates
git pull origin main
```

**More help**: See [CLAUDE.md](CLAUDE.md) - "Validation Error Troubleshooting" section

---

## 🗺️ Learning Pathways

### Path 1: Complete Beginner → Security Analyst
**Duration**: 6-8 months | **Lessons**: 80+ | **Domains**: All

```
Months 1-2:  Fundamentals + OSINT (23 lessons)
Months 3-4:  DFIR + Malware Basics (33 lessons)
Months 5-6:  Active Directory + System (31 lessons)
Months 7-8:  Specialization (Blue Team, Threat Hunting)
```

### Path 2: IT Pro → Penetration Tester
**Duration**: 3-4 months | **Lessons**: 50+ | **Focus**: Pentest, Red Team

```
Month 1:  Security Fundamentals + OSINT (23 lessons)
Month 2-3: Penetration Testing (35 lessons)
Month 4:  Red Team Operations (18 lessons)
```

### Path 3: Analyst → Threat Hunter
**Duration**: 2-3 months | **Lessons**: 40+ | **Focus**: DFIR, Blue Team, Threat Hunting

```
Month 1:  DFIR Deep Dive (17 lessons)
Month 2:  Blue Team Defense (15 lessons)
Month 3:  Threat Hunting Mastery (10 lessons)
```

---

## 🎯 Content Roadmap

### ✅ Complete (591 lessons - TARGET EXCEEDED)
**Core Domains (12)**:
- Fundamentals (17), OSINT (37), DFIR (237), Malware (21)
- Active Directory (24), System (22), Linux (22), Cloud (45)
- Pentest (62), Red Team (26), Blue Team (28), Threat Hunting (30)

**Emerging Tech Domains (3)**:
- AI Security (13), IoT Security (4), Web3 Security (3)

**Course-Based Content**:
- 13Cubed Linux Forensics: 41 lessons
- SANS FOR500 (Windows Forensics): 19 lessons
- SANS FOR508 (Advanced IR): 18 lessons
- SANS FOR509 (Cloud Forensics): 25 lessons
- SANS FOR528 (Ransomware): 16 lessons
- SANS FOR572 (Network Forensics): 25 lessons
- SANS FOR589 (Cybercrime): 22 lessons
- SANS FOR608 (Enterprise IR): 27 lessons
- SANS SEC504 (Hacker Tools): 28 lessons
- OWASP LLM Top 10: 10 lessons

### 🚧 Future Expansion
- Expand AI Security: Adversarial ML, model security
- Expand IoT Security: Industrial IoT, firmware analysis
- Expand Web3 Security: DeFi, smart contract auditing
- Mobile security (iOS, Android)
- DevSecOps and CI/CD security

**See [lesson_ideas.csv](lesson_ideas.csv) for detailed lesson pipeline**

---

## 🤝 Contributing

Contributions welcome! Here's how you can help:

### 🎓 Content Creators
- Write new lessons following standards in [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md)
- Ensure all Jim Kwik principles are represented
- Submit via pull request with lesson JSON files

### 💻 Developers
- Fix bugs or add features
- Improve UI/UX
- Optimize performance
- Add tests

### 📚 Educators
- Test lessons with learners
- Provide feedback on effectiveness
- Suggest improvements to pedagogy

**Before contributing**: Read [CLAUDE.md](CLAUDE.md) for project structure and standards

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

**Commercial Use**: Encouraged! Build your training business with this platform.

---

## 🙏 Acknowledgments

**Inspired by:**
- Jim Kwik's *Limitless* accelerated learning framework
- Dr. Barbara Oakley's *Learning How to Learn* principles
- Bloom's Taxonomy for learning objectives
- Spaced repetition research (Ebbinghaus, Leitner)

**Built with:**
- Streamlit team for amazing framework
- Open-source cybersecurity community
- Educational psychology research

---

## 📞 Support & Contact

- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Complete guides in repository
- **Community**: Share lessons and best practices

---

## 🎓 About

**Mission**: Democratize cybersecurity education through adaptive, engaging, and scientifically-grounded learning experiences.

**Vision**: Empower 1 million learners to transition into cybersecurity careers by 2030.

**Values**:
- **Accessibility**: Learning should be available to everyone
- **Effectiveness**: Leverage cognitive science for better outcomes
- **Engagement**: Make learning enjoyable, not just informative
- **Empowerment**: Build confidence alongside competence

---

**Ready to accelerate your cybersecurity mastery? Let's begin! 🛡️🚀**
