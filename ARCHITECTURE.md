# CyberLearn Adaptive Learning System - Architecture Specification

## Executive Summary

CyberLearn is an adaptive, gamified cybersecurity learning platform that integrates Jim Kwik's accelerated learning principles to deliver professional-level mastery through daily 30-minute sessions. The system progresses learners from beginner to expert across 7 core domains: Cybersecurity Fundamentals, DFIR, Malware Analysis, Active Directory Security, Penetration Testing, Red Team Operations, and Blue Team Defense.

## System Architecture

### Technology Stack

**Backend**
- Python 3.10+
- SQLite (data persistence)
- Pydantic (data validation)
- JSON (content storage)

**Frontend**
- Streamlit (interactive web UI)
- Plotly (data visualization)
- Pillow (image processing)
- Mermaid (diagrams)

**Content Delivery**
- Multi-format lesson modules (text, images, videos, interactive simulations)
- Markdown-based content authoring
- Embedded media support

### Architectural Patterns

**1. Modular Domain-Driven Design**
```
├── core/                      # Core business logic
│   ├── adaptive_engine.py     # Adaptive learning algorithm
│   ├── gamification.py        # XP, badges, streaks
│   └── assessment.py          # Quiz & diagnostic logic
├── models/                    # Data models
│   ├── user.py
│   ├── lesson.py
│   └── progress.py
├── content/                   # Lesson content (JSON)
│   ├── fundamentals/
│   ├── dfir/
│   ├── malware/
│   ├── active_directory/
│   ├── pentest/
│   ├── redteam/
│   └── blueteam/
├── ui/                        # Streamlit pages
│   ├── dashboard.py
│   ├── lesson_viewer.py
│   └── assessment.py
└── utils/                     # Utilities
    ├── database.py
    └── content_loader.py
```

**2. Adaptive Learning Engine**

The engine implements a multi-dimensional assessment model:

```
User Skill Level = f(
    diagnostic_score,
    lesson_completion_rate,
    quiz_accuracy,
    time_to_mastery,
    retention_rate
)
```

**Difficulty Levels:**
- Level 1: Beginner (0-25% mastery)
- Level 2: Intermediate (26-50% mastery)
- Level 3: Advanced (51-75% mastery)
- Level 4: Expert (76-100% mastery)

**Adaptive Mechanisms:**
- Dynamic content difficulty adjustment
- Personalized lesson sequencing
- Intelligent review scheduling (spaced repetition)
- Prerequisite gating

**3. Jim Kwik Principle Integration**

| Principle | Implementation | System Components |
|-----------|----------------|-------------------|
| **Active Learning** | Every lesson includes hands-on lab, code exercise, or scenario simulation | `InteractiveComponent` class, sandboxed environments |
| **Minimum Effective Dose** | Content curated to 20% concepts delivering 80% results; flagged as "Core Concept" | Content metadata: `is_core: true` |
| **Teach Like I'm 10** | Analogies, simple language, progressive complexity unlocking | `SimplifiedExplanation` content blocks |
| **Memory Hooks** | Mnemonics, stories, visual metaphors embedded in lessons | `MemoryAid` component type |
| **Meta-Learning** | Reflective prompts after each section: "What deeper question should I ask?" | `ReflectionPrompt` component |
| **Connect to What I Know** | Real-world scenarios, analogies to everyday experiences | `RealWorldConnection` sections |
| **Reframe Limiting Beliefs** | Mindset coaching messages, growth mindset reinforcements | `MindsetCoach` popups, affirmations |
| **Gamify It** | XP, badges, levels, streaks, leaderboards | `GamificationEngine` |
| **Learning Sprint** | 30-min daily sessions, weekend crash courses | Session timer, sprint mode |
| **Multiple Memory Pathways** | Visual diagrams, audio narration, kinesthetic sims, emotional stories | Multi-format content delivery |

### Data Model

**User Profile**
```python
{
    "user_id": UUID,
    "username": str,
    "created_at": datetime,
    "skill_levels": {
        "fundamentals": int (0-100),
        "dfir": int,
        "malware": int,
        "active_directory": int,
        "pentest": int,
        "redteam": int,
        "blueteam": int
    },
    "total_xp": int,
    "level": int,
    "streak_days": int,
    "last_login": datetime,
    "badges": [str],
    "learning_preferences": {
        "visual_weight": float,
        "hands_on_weight": float,
        "pace": str ("slow" | "normal" | "fast")
    }
}
```

**Lesson Structure**
```python
{
    "lesson_id": UUID,
    "domain": str,
    "title": str,
    "difficulty": int (1-4),
    "estimated_time": int (minutes),
    "prerequisites": [UUID],
    "learning_objectives": [str],
    "jim_kwik_principles": [str],
    "content_blocks": [
        {
            "type": "explanation" | "video" | "diagram" | "quiz" | "simulation" | "reflection",
            "content": {...},
            "memory_aids": [str],
            "real_world_connection": str
        }
    ],
    "assessments": [...],
    "xp_reward": int,
    "badge_unlock": str (optional)
}
```

**Progress Tracking**
```python
{
    "progress_id": UUID,
    "user_id": UUID,
    "lesson_id": UUID,
    "status": "not_started" | "in_progress" | "completed" | "mastered",
    "attempts": int,
    "quiz_scores": [int],
    "time_spent": int (seconds),
    "completed_at": datetime,
    "retention_checks": [
        {
            "checked_at": datetime,
            "score": int
        }
    ]
}
```

### Adaptive Learning Algorithm

**Diagnostic Assessment Flow:**
```
1. User starts → Initial diagnostic quiz (20 questions, mixed difficulty)
2. Scoring algorithm analyzes:
   - Correct answers by domain
   - Question difficulty distribution
   - Time per question
3. Generate skill profile matrix
4. Recommend starting point in curriculum
```

**Content Adaptation Logic:**
```python
def get_next_lesson(user_profile, domain):
    current_skill = user_profile.skill_levels[domain]

    if current_skill < 25:
        difficulty_filter = [1, 2]
        format_preference = "simplified_explanation"
    elif current_skill < 50:
        difficulty_filter = [2, 3]
        format_preference = "mixed"
    elif current_skill < 75:
        difficulty_filter = [3, 4]
        format_preference = "technical"
    else:
        difficulty_filter = [4]
        format_preference = "expert_challenge"

    # Get lessons matching criteria with prerequisites met
    available_lessons = query_lessons(
        domain=domain,
        difficulty__in=difficulty_filter,
        prerequisites_met=True
    )

    # Apply learning science: interleaving & spacing
    if should_review(user_profile, domain):
        return get_spaced_review_lesson(user_profile, domain)

    return available_lessons[0]  # Next in sequence
```

### Gamification System

**XP Calculation:**
```
Base XP = lesson_difficulty * 100
Bonus Multipliers:
- First attempt perfect score: 1.5x
- Streak bonus: 1.1x per consecutive day (max 2x)
- Speed bonus: 1.2x if completed under estimated time
- Teaching bonus: 1.3x if user explains concept in reflection

Total XP = Base XP * Multipliers
```

**Badge System:**
- Domain Badges: Complete all lessons in domain
- Mastery Badges: Achieve 90%+ in domain
- Streak Badges: 7, 30, 100, 365-day streaks
- Speed Badges: Complete lessons under target time
- Teaching Badges: High-quality reflections
- Jim Kwik Badges: Demonstrate each learning principle

**Level System:**
```
Level 1: 0-1,000 XP (Apprentice)
Level 2: 1,001-3,000 XP (Practitioner)
Level 3: 3,001-7,000 XP (Specialist)
Level 4: 7,001-15,000 XP (Expert)
Level 5: 15,001-30,000 XP (Master)
Level 6: 30,001+ XP (Grandmaster)
```

### Safety & Sandboxing

**Simulation Environment:**
- Docker containers for hands-on labs
- Network isolation
- Resource limits
- Automatic cleanup
- No real-world target interaction
- Pre-configured vulnerable VMs (DVWA, Metasploitable, etc.)

**Content Safety:**
- All exploits are educational demonstrations
- Clear ethical guidelines
- Legal disclaimer acknowledgment
- Focus on defensive applications

### Scalability Considerations

**Content Expansion:**
- JSON-based content allows easy authoring
- Template system for rapid lesson creation
- Community contribution workflow
- Version control for content updates

**Performance:**
- Lazy loading of media assets
- Caching of frequently accessed lessons
- Database indexing on user_id, lesson_id
- Asynchronous content loading

**Multi-tenancy:**
- User isolation in database
- Separate progress tracking
- Optional team/organization support

### User Flow Architecture

**First-Time User Journey:**
```
1. Welcome → Mindset Primer (Jim Kwik introduction)
2. Diagnostic Assessment → Skill profiling
3. Personalized Dashboard → Recommended path
4. First Lesson (adaptive difficulty)
5. Post-lesson reflection + XP reward
6. Next lesson recommendation
```

**Returning User Journey:**
```
1. Login → Streak acknowledgment
2. Dashboard → Progress visualization
3. Daily lesson recommendation (personalized)
4. Optional: Sprint mode or Review mode
5. Lesson completion → Gamification feedback
6. Meta-learning reflection
```

**Learning Sprint Mode:**
```
Weekend Crash Course:
- 6x 30-min sessions over 2 days
- Focus on single domain
- Accelerated progression
- Bonus XP multiplier
- Certificate upon completion
```

### Assessment & Feedback System

**Question Types:**
- Multiple choice (knowledge checks)
- Scenario-based (application)
- Code review (find the vulnerability)
- Hands-on labs (perform task)
- Reflection (meta-learning)

**Feedback Mechanisms:**
- Immediate answer validation
- Explanation of correct/incorrect
- Memory aids reinforcement
- Related concept suggestions
- Encouragement messaging

### Integration Points

**Future Extensibility:**
- API for external content providers
- LMS integration (SCORM)
- Certification exam alignment
- CTF competition integration
- Real-world lab environments (TryHackMe, HackTheBox)

## Technology Justification

**Why Streamlit:**
- Rapid prototyping and deployment
- Built-in interactivity (perfect for quizzes, simulations)
- Python-native (leverages ecosystem)
- Easy to extend with custom components
- Low barrier for maintenance

**Why SQLite:**
- Zero-configuration
- Embedded database (easy deployment)
- ACID compliance
- Sufficient for single-user or small team
- Easy migration path to PostgreSQL if needed

**Why JSON for Content:**
- Human-readable
- Version control friendly
- Easy to author and edit
- Supports rich nested structures
- No schema migrations for content updates

## Deployment Architecture

**Local Development:**
```bash
python -m streamlit run app.py
```

**Production Options:**
1. Streamlit Cloud (easiest)
2. Docker container on cloud VM
3. Heroku/Railway deployment
4. Self-hosted on internal network

## Success Metrics

**Learning Effectiveness:**
- Skill level progression rate
- Lesson completion rate
- Quiz score trends
- Retention rate (spaced repetition results)
- Time to domain mastery

**Engagement Metrics:**
- Daily active users
- Streak maintenance
- Session duration
- Lesson replay rate
- Reflection quality scores

**Jim Kwik Principle Adoption:**
- Active learning completion rate
- Memory aid utilization
- Meta-learning reflection depth
- Real-world connection engagement

## Next Steps

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed build and deployment instructions.
