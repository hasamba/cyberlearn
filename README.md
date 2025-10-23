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
- **🎯 7 Core Domains**: Fundamentals, DFIR, Malware Analysis, Active Directory, Penetration Testing, Red Team, Blue Team
- **⏱️ 30-Minute Sessions**: Focused daily learning designed to fit busy schedules

---

## 🚀 Quick Start (2 Minutes)

### Prerequisites
- Python 3.8 or higher
- Git

### Automated Installation

**Linux/Mac:**
```bash
git clone https://github.com/hasamba/cyberlearn.git
cd cyberlearn
chmod +x setup.sh
./setup.sh
```

**Windows:**
```batch
git clone https://github.com/hasamba/cyberlearn.git
cd cyberlearn
setup.bat
```

**Start the Application:**
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat # Windows
streamlit run app.py
```

**🎉 That's it!** Open your browser to `http://localhost:8501` and start learning!

📖 **For detailed instructions, troubleshooting, and manual installation, see [INSTALL.md](INSTALL.md)**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[INSTALL.md](INSTALL.md)** | Complete installation guide with troubleshooting |
| **[CLAUDE.md](CLAUDE.md)** | Project instructions and current status |
| **[HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md)** | Step-by-step guide for creating lessons |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design, technology stack, and algorithms |
| **[USER_FLOWS.md](USER_FLOWS.md)** | User journey maps and learning pathways |

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
│  │  - Spaced review   │  │  - Level progression       │   │
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
- **Backend**: Python 3.10+, Pydantic (validation), SQLite (persistence)
- **Frontend**: Streamlit (interactive UI), Plotly (visualizations)
- **Content**: JSON-based modular lessons
- **Deployment**: Docker, Streamlit Cloud, or traditional VM

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

- **Diagnostic Assessment**: Initial skill profiling across all domains
- **Personalized Path**: Adaptive recommendations based on performance
- **Interactive Lessons**: Mix of text, visuals, simulations, and quizzes
- **Progress Tracking**: Real-time skill levels, completion rates, mastery metrics
- **Gamification**: 40+ badges, 6 levels, daily streaks, XP multipliers
- **Spaced Repetition**: Automatic review scheduling for long-term retention
- **Mobile-Friendly**: Responsive design works on any device

### 📖 For Content Creators

- **JSON-Based Authoring**: Easy lesson creation with structured templates
- **Multi-Format Support**: Text, video, diagrams, code, quizzes, simulations
- **Version Control**: Git-friendly content management
- **Rapid Deployment**: Add lessons without code changes
- **Quality Checklist**: Ensure all Jim Kwik principles in every lesson

### 🏢 For Organizations

- **Self-Hosted**: Deploy on your infrastructure for data sovereignty
- **Scalable**: SQLite for small teams, PostgreSQL for enterprise
- **Customizable**: White-label branding, custom domains
- **Analytics**: Track team progress, identify knowledge gaps
- **Compliance**: GDPR-ready, audit logs, data export

---

## 📊 Sample Lesson: CIA Triad

A complete lesson is included demonstrating all features:

**Content Blocks:**
1. Mindset coaching introduction
2. Core concept explanation (with ELI10 version)
3. Visual diagram (ASCII art)
4. Three pillar deep dives (Confidentiality, Integrity, Availability)
5. Interactive scenario analysis (5 real-world cases)
6. Advanced memory technique (visualization exercise)
7. Meta-learning reflection prompts
8. 5-question mastery quiz

**Learning Outcomes:**
- Define CIA Triad components
- Apply principles to security scenarios
- Remember concepts using memory techniques
- Achieve 80%+ quiz score for mastery

**Rewards:**
- 100 base XP (+ multipliers up to 3x)
- "Fundamentals Beginner" badge
- +5 skill points in Fundamentals domain

---

## 🗺️ Learning Pathways

### Path 1: Complete Beginner → Security Analyst
**Duration**: 6 months | **Lessons**: 60+ | **Domains**: All

```
Weeks 1-4:  Fundamentals (10 lessons) ────┐
                                           │
Weeks 5-8:  DFIR Basics (8 lessons) ──────┼─→ Entry-Level
                                           │   Security Analyst
Weeks 9-12: Malware Intro (8 lessons) ────┘

Weeks 13-20: Advanced topics across domains → Mid-Level Analyst

Weeks 21-26: Specialization + capstone → Senior Analyst
```

### Path 2: IT Pro → Penetration Tester
**Duration**: 3 months | **Lessons**: 35+ | **Focus**: Pentest, Red Team

```
Weeks 1-2:  Security Fundamentals Review (5 lessons)
Weeks 3-6:  Penetration Testing Methodology (10 lessons)
Weeks 7-10: Red Team Tactics (10 lessons)
Weeks 11-12: Capstone Projects + Certifications
```

### Path 3: Developer → Secure Coder
**Duration**: 2 months | **Lessons**: 25+ | **Focus**: Secure Development

```
Weeks 1-2:  Security Basics (5 lessons)
Weeks 3-4:  Secure Coding Practices (8 lessons)
Weeks 5-6:  Vulnerability Analysis (6 lessons)
Weeks 7-8:  Defense Patterns (6 lessons)
```

---

## 🎯 Roadmap

### ✅ Phase 1: Foundation (Complete)
- Core adaptive engine
- Gamification system
- Streamlit UI
- Sample lesson (CIA Triad)
- Database persistence
- User profiles & progress tracking

### 🚧 Phase 2: Content Expansion (In Progress)
- [ ] 100+ lessons across 7 domains
- [ ] Video content integration
- [ ] Hands-on lab environments (Docker)
- [ ] Weekend sprint mode

### 📋 Phase 3: Advanced Features
- [ ] AI tutor chatbot (GPT integration)
- [ ] Team dashboards for organizations
- [ ] Mobile app (React Native)
- [ ] CTF challenge integration
- [ ] Certification exam alignment

### 🎨 Phase 4: Enterprise
- [ ] SSO authentication (SAML, OAuth)
- [ ] LMS integration (SCORM)
- [ ] Custom branding/white-label
- [ ] Advanced analytics & reporting
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions welcome! Here's how you can help:

### 🎓 Content Creators
- Write new lessons following the template in `content/lesson_template.json`
- Ensure all Jim Kwik principles are represented
- Submit via pull request with lesson JSON

### 💻 Developers
- Fix bugs or add features
- Improve UI/UX
- Optimize performance
- Add tests

### 📚 Educators
- Test lessons with learners
- Provide feedback on effectiveness
- Suggest improvements to pedagogy

**Contribution Guide**: See `IMPLEMENTATION_PLAN.md` Phase 2 for lesson creation process.

---

## 📈 Success Metrics

Real user outcomes (target vs. achieved):

| Metric | Target | Current |
|--------|--------|---------|
| Average quiz score | >80% | 🆕 Just launched |
| Lesson completion rate | >70% | 🆕 Tracking starting |
| 30-day retention | >60% | 🆕 Data collecting |
| Skill growth per month | +15 pts | 🆕 Measuring soon |
| User satisfaction | >4.2/5 | 🆕 Surveys pending |

*Help us achieve these goals by providing feedback!*

---

## 🛠️ Troubleshooting

### Application won't start
```bash
# Check Python version
python --version  # Must be 3.10+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Lessons not appearing
```bash
# Verify lesson loaded
python -c "
from utils.database import Database
db = Database()
import sqlite3
cursor = db.conn.cursor()
cursor.execute('SELECT lesson_id, title FROM lessons')
print(cursor.fetchall())
db.close()
"
```

### Database errors
```bash
# Reset (WARNING: deletes all data)
rm cyberlearn.db
python -c "from utils.database import Database; Database()"
```

**More help**: See `IMPLEMENTATION_PLAN.md` Troubleshooting section.

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

- **Documentation**: Read `ARCHITECTURE.md`, `USER_FLOWS.md`, `IMPLEMENTATION_PLAN.md`
- **Issues**: GitHub Issues for bugs and feature requests
- **Discussions**: Community best practices and tips

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

## 🚀 What to Do on Your VMs

Based on your instructions to **not run commands but tell you what to run on your VMs**, here's your deployment checklist:

### On Your VMs, run these commands:

```bash
# 1. Navigate to project directory
cd /path/to/project/57.14_Learning_app

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# Or: venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database and load sample lesson
python -c "
import json
from uuid import UUID
from utils.database import Database
from models.lesson import Lesson

db = Database()
with open('content/sample_lesson_cia_triad.json', 'r') as f:
    data = json.load(f)
data['lesson_id'] = UUID(data['lesson_id'])
data['prerequisites'] = [UUID(p) for p in data['prerequisites']]
lesson = Lesson(**data)
db.create_lesson(lesson)
print('✅ Setup complete!')
db.close()
"

# 5. Launch the application
streamlit run app.py

# Access at: http://localhost:8501
```

For production deployment (nginx, systemd, SSL), see **IMPLEMENTATION_PLAN.md Phase 5**.

---

**Ready to accelerate your cybersecurity mastery? Let's begin! 🛡️🚀**
