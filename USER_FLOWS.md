# CyberLearn - User Flow & Learning Journey Documentation

## User Flow Architecture

### Flow 1: First-Time User Onboarding

```
START
  |
  v
Welcome Page
  - View platform features
  - Read about learning approach
  - Choose: Login or Create Account
  |
  v
Create Account
  - Enter username
  - Optional email
  - Account created instantly
  |
  v
Diagnostic Assessment Introduction
  - Explain purpose (skill profiling)
  - Explain benefit (personalized path)
  - Reframe limiting belief: "Not about being right, about starting right"
  |
  v
20-Question Diagnostic Quiz
  - Questions across all 7 domains
  - Mixed difficulty (1-3)
  - 10 minutes estimated
  - Progress bar visible
  |
  v
Skill Profile Results
  - Visual radar chart of skills
  - Domain-by-domain breakdown
  - Identify strongest/weakest areas
  - Encouragement message
  |
  v
Personalized Dashboard
  - Welcome message with streak info
  - Recommended first lesson (adaptive)
  - Domain progress overview
  - Next milestone display
  |
  v
First Lesson Experience
  (See Flow 3: Lesson Completion Journey)
```

### Flow 2: Returning User Experience

```
START (Login)
  |
  v
Login Page
  - Enter username
  - System loads user profile
  |
  v
Streak Update Logic
  |
  +-- Same day login → Streak unchanged
  |
  +-- Next day login → Streak +1
  |       |
  |       v
  |   🔥 Streak Maintained Message
  |   "X days strong! Consistency builds mastery."
  |
  +-- Missed day(s) → Streak reset to 1
          |
          v
      Reframe Message
      "Streaks are numbers. Your knowledge remains.
       Let's rebuild momentum today!"
  |
  v
Personalized Dashboard
  - Stats: Level, XP, Lessons, Badges
  - Recommended Next Lesson (adaptive)
      |
      +-- Lesson due for review? → Review lesson
      |
      +-- Core concept remaining? → Core lesson
      |
      +-- Normal progression → Next in sequence
  |
  - Skill radar chart
  - Next milestone progress
  - Recent badges
  |
  v
USER CHOOSES:
  |
  +-- Start Recommended Lesson → Flow 3
  |
  +-- Browse All Lessons → Flow 4
  |
  +-- View Profile/Achievements → Flow 5
  |
  +-- Continue In-Progress Lesson → Flow 3 (resume)
```

### Flow 3: Lesson Completion Journey

```
Lesson Start
  |
  v
Lesson Header
  - Title, subtitle, domain
  - Difficulty, estimated time, XP reward
  - Learning objectives
  - Progress bar (blocks completed)
  |
  v
Content Block 1: Mindset Coach
  - Reframe limiting beliefs
  - "You've got this" message
  - Set positive expectations
  - JIM KWIK: Reframe Limiting Beliefs ✓
  |
  v
Content Block 2: Explanation
  - Core concept introduction
  - Professional explanation
  - JIM KWIK: Teach Like I'm 10 ✓
      |
      v
  [Expandable: Simplified Explanation]
  - Plain language version
  - Real-world analogy
  - JIM KWIK: Connect to What I Know ✓
  |
  v
Content Block 3: Diagram/Visual
  - ASCII art or visual representation
  - Key points highlighted
  - JIM KWIK: Multiple Memory Pathways (visual) ✓
  |
  v
Content Block 4: Detailed Explanations
  - For each sub-concept (e.g., CIA pillars)
  - Protection methods
  - Common violations
  - JIM KWIK: Minimum Effective Dose (core info only) ✓
  |
  [Each block includes:]
  - Memory Aids (expandable)
      - Mnemonics, metaphors
      - JIM KWIK: Memory Hooks ✓
  |
  - Real-World Connection (expandable)
      - Practical examples
      - Industry scenarios
      - JIM KWIK: Connect to What I Know ✓
  |
  - Reflection Prompt (expandable)
      - "What question should I ask?"
      - JIM KWIK: Meta-Learning ✓
  |
  v
Content Block 5: Interactive Simulation
  - Hands-on scenario analysis
  - Immediate feedback on answers
  - Explanation after each attempt
  - JIM KWIK: Active Learning ✓
  - XP awarded for completion (50 XP)
  |
  v
Content Block 6: Memory Aid Deep Dive
  - Advanced memory technique
  - Visualization exercise
  - Emotional anchoring
  - JIM KWIK: Memory Hooks + Multiple Pathways ✓
  |
  v
Content Block 7: Meta-Learning Reflection
  - Open-ended reflection prompts
  - Text area for learner thoughts
  - JIM KWIK: Meta-Learning ✓
  - Bonus XP for submission (25 XP)
  |
  v
Final Assessment Quiz
  - 5 questions (varied difficulty)
  - Mix of types: MC, scenario-based
  - 80% mastery threshold
  - Timer running in background
  |
  v
Quiz Submission
  |
  v
Scoring Logic
  - Calculate % correct
  - Measure time vs. estimated
  - Check if first attempt
  |
  v
XP Calculation
  Base XP: 100 (difficulty 1 lesson)
  |
  Multipliers Applied:
  +-- Score ≥ 100% → 1.5x
  +-- Score ≥ 90% → 1.2x
  +-- Score ≥ 80% → 1.1x
  +-- Under estimated time → 1.2x
  +-- First attempt success → 1.2x
  +-- Streak bonus → 1.0x to 2.0x (based on streak)
  +-- Difficulty multiplier → 1.0x to 1.4x
  |
  Total XP = Base * All Multipliers
  |
  v
Skill Level Update
  - Domain skill increases based on score & difficulty
  - Diminishing returns at higher levels
  |
  v
Badge Check
  - Check all badge criteria
  - Domain completion badges
  - Performance badges (perfect score, speed, etc.)
  - Milestone badges (50 lessons, etc.)
  - Jim Kwik principle badges
  |
  v
Results Display
  |
  +-- Score Display
  |
  +-- XP Breakdown
  |   - Base XP
  |   - Each multiplier listed
  |   - Total XP earned
  |
  +-- Level Up? (if applicable)
  |   🎊 "LEVEL UP! You're now Level X - [Name]"
  |   🎈 Balloons animation
  |
  +-- New Badges? (if any)
  |   🏅 Badge icon + name + description
  |
  +-- Encouragement Message
      - Context-aware (perfect score, level up, streak, etc.)
      - Growth mindset reinforcement
      - JIM KWIK: Reframe Limiting Beliefs ✓
  |
  v
Next Review Scheduled
  - Spaced repetition algorithm
  - Next review in 1, 3, 7, 14, 30, 60, or 90 days
  - Based on performance
  |
  v
Return to Dashboard
  - Updated stats visible
  - New recommended lesson
  - JIM KWIK: All 10 Principles Integrated ✓
```

### Flow 4: Lesson Browser & Selection

```
My Learning Page
  |
  v
Domain Tabs
  [Fundamentals] [DFIR] [Malware] [AD] [Pentest] [RedTeam] [BlueTeam]
  |
  v
Selected Domain View
  |
  - Domain Skill Level (0-100) with progress bar
  |
  - List of Lessons:
      |
      For Each Lesson:
      |
      +-- Status Icon
      |   - 📘 Not Started
      |   - 🔄 In Progress
      |   - ✅ Completed
      |   - ⭐ Mastered
      |
      +-- Lesson Title
      |
      +-- Metadata
      |   - ⏱️ Time estimate
      |   - 🎯 Difficulty
      |   - ⚡ XP reward
      |   - 🔥 Core Concept flag (if applicable)
      |
      +-- Action Button
          - "Start" (new)
          - "Continue" (in progress)
          - "Review" (due for spaced repetition)
  |
  v
User Clicks Lesson
  |
  v
Lesson Start (Flow 3)
```

### Flow 5: Profile & Achievement Management

```
Profile Page
  |
  +-- User Information Section
  |   - Edit username, email
  |   - View account stats
  |
  +-- Learning Preferences
  |   - Pace: slow, normal, fast
  |   - Session duration: 15-60 min slider
  |   - Learning style weights:
  |       * Visual weight
  |       * Kinesthetic (hands-on) weight
  |       * Auditory weight (auto-calculated)
  |   - Save button
  |
  +-- Statistics Display
      - Lessons completed
      - Total study time
      - Streak stats
      - Overall skill level

Achievements Page
  |
  +-- Summary Stats
  |   - Total XP, Level, Badges, Streak
  |
  +-- Badge Gallery (by category)
  |   |
  |   +-- Domain Badges
  |   +-- Mastery Badges
  |   +-- Streak Badges
  |   +-- Performance Badges
  |   +-- Milestone Badges
  |   +-- Jim Kwik Principle Badges
  |   |
  |   Each Badge Shows:
  |   - Icon (emoji)
  |   - Name
  |   - Description
  |   - Earned ✅ or Locked 🔒
  |   - Visual style: Gold gradient if earned, grayscale if locked
  |
  +-- Next Milestone
  |   - Description
  |   - Progress bar
  |   - Encouragement based on % complete
  |
  +-- Level Progression
      - All 6 levels listed
      - ✅ Achieved levels
      - ⏳ Next level with XP remaining
      - 🔒 Future levels
```

## Learning Journey Map

### Beginner Path (0-25 Skill)

```
Day 1-7: Fundamentals Foundation
  ├─ Day 1: CIA Triad (sample lesson provided)
  ├─ Day 2: Security Principles
  ├─ Day 3: Threat Landscape
  ├─ Day 4: Risk Management
  ├─ Day 5: Authentication & Authorization
  ├─ Day 6: Encryption Basics
  └─ Day 7: Network Security Fundamentals

Day 8-14: Introduction to DFIR
  ├─ Day 8: Digital Forensics Overview
  ├─ Day 9: Chain of Custody
  ├─ Day 10: Evidence Collection
  └─ ...

MILESTONE: "Week Warrior" badge (7-day streak)
```

### Intermediate Path (26-50 Skill)

```
Week 3-8: Domain Deep Dives
  ├─ Advanced Fundamentals
  ├─ DFIR Techniques
  ├─ Malware Analysis Basics
  └─ Active Directory Fundamentals

MILESTONE: "Monthly Master" badge (30-day streak)
MILESTONE: "Persistent Learner" badge (50 lessons)
```

### Advanced Path (51-75 Skill)

```
Week 9-16: Specialized Skills
  ├─ Penetration Testing Methodology
  ├─ Red Team Tactics
  ├─ Blue Team Defense
  ├─ Advanced Malware Analysis
  └─ AD Attack & Defense

MILESTONE: Domain Mastery Badges
MILESTONE: "Dedicated Scholar" badge (100 lessons)
```

### Expert Path (76-100 Skill)

```
Week 17+: Mastery & Advanced Operations
  ├─ Expert-level challenges
  ├─ Integrated scenarios
  ├─ Capstone projects
  └─ Real-world simulations

MILESTONE: "Century Scholar" badge (100-day streak)
MILESTONE: "Grandmaster" level (30,000+ XP)
```

## Adaptive Pathways

### Scenario 1: Complete Beginner
```
Diagnostic Score: All domains < 15
Recommended Path: Linear fundamentals → DFIR → Malware
Content Style: Heavy on ELI10, metaphors, real-world connections
Pace: Slow (1 lesson per 2 days)
```

### Scenario 2: Some IT Experience
```
Diagnostic Score: Fundamentals 40, others < 20
Recommended Path: Skip basic fundamentals, focus on security specifics
Content Style: Balanced technical + practical
Pace: Normal (1 lesson per day)
```

### Scenario 3: Security Professional
```
Diagnostic Score: Multiple domains 50-70
Recommended Path: Advanced content, interleaved domains
Content Style: Technical depth, minimal simplification
Pace: Fast (1-2 lessons per day)
```

### Scenario 4: Uneven Skills
```
Diagnostic Score: Strong in Pentest (70), weak in DFIR (20)
Recommended Path: Adaptive balancing—strengthen weak areas while challenging strong
Content Style: Domain-specific adaptation
Pace: Normal with domain-specific focus
```

## Spaced Repetition Schedule

```
Lesson Completed
  |
  v
Review 1: +1 day
  (Quick retention check: 5 questions)
  |
  +-- Score ≥ 90% → Review 2: +3 days
  |
  +-- Score 80-89% → Review 2: +2 days
  |
  +-- Score < 80% → Review 2: +1 day (needs reinforcement)
  |
  v
Review 2: +3 days (if 90%+)
  |
  +-- Score ≥ 90% → Review 3: +7 days
  +-- Score < 90% → Review 3: +3 days
  |
  v
Review 3: +7 days
  |
  v
Review 4: +14 days
  |
  v
Review 5: +30 days
  |
  v
Review 6: +60 days
  |
  v
MASTERED (90+ days retention)
```

## Jim Kwik Principle Integration Map

| Principle | Implementation Points | UI Elements |
|-----------|----------------------|-------------|
| **Active Learning** | Interactive simulations in every lesson | 🎮 Simulation blocks, hands-on exercises |
| **Minimum Effective Dose** | Core concepts flagged, 20% focus | 🔥 "Core Concept" badges |
| **Teach Like I'm 10** | Expandable simplified explanations | 🎈 "Simplified Explanation" expanders |
| **Memory Hooks** | Mnemonics, metaphors in every lesson | 💡 "Memory Aids" sections |
| **Meta-Learning** | Reflection prompts throughout | 🤔 Reflection text areas |
| **Connect to What I Know** | Real-world scenarios and analogies | 🌍 "Real-World Connection" expanders |
| **Reframe Limiting Beliefs** | Mindset coaching messages | 💪 Encouragement after scores, mindset blocks |
| **Gamify It** | XP, badges, levels, streaks | 🏆 Entire gamification system |
| **Learning Sprint** | 30-min sessions, weekend modes | ⏱️ Session timers, sprint mode (future) |
| **Multiple Memory Pathways** | Visual, text, interactive, emotional | 📊 Diagrams, simulations, stories |

## Key UX Principles

1. **Immediate Feedback**: Every interaction gets instant response
2. **Progress Visibility**: Always show where learner is in journey
3. **Positive Reinforcement**: Celebrate small wins frequently
4. **Low Friction**: One-click lesson start, auto-save progress
5. **Contextual Help**: Expandable aids don't interrupt flow
6. **Mobile-First Design**: Works on any device (Streamlit responsive)
7. **Accessibility**: Clear contrast, readable fonts, screen-reader friendly
8. **Psychological Safety**: "Wrong answers help learning" messaging
