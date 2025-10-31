---
name: lesson-analytics
description: Analyze lesson statistics, coverage, and generate reports
version: 1.0
auto_invoke: true
---

# Lesson Analytics Skill

Generate comprehensive analytics and reports on lesson content.

## When to Use

- User asks for lesson statistics
- User wants to see domain coverage
- User requests progress reports
- User needs gap analysis

## Analytics Reports

### 1. Lesson Statistics

```
📊 LESSON STATISTICS

Total Lessons: 282
Completed: 77 (27%)
In Progress: 0
Not Started: 205 (73%)

By Domain:
- DFIR: 77 lessons (27% of total)
- Malware: 21 lessons
- Active Directory: 24 lessons
- Cloud: 45 lessons
- [... all 15 domains]

By Difficulty:
- Beginner (1): 45 lessons (16%)
- Intermediate (2): 180 lessons (64%)
- Advanced (3): 57 lessons (20%)

Word Count Distribution:
- < 4,000 words: 12 lessons ⚠️
- 4,000-8,000: 145 lessons
- 8,000-12,000: 98 lessons
- > 12,000: 27 lessons
- Average: 7,200 words
```

### 2. Domain Coverage

```
🎯 DOMAIN COVERAGE ANALYSIS

DFIR Domain:
- Total planned: 111 lessons
- Completed: 77 lessons (69%)
- Gap: 34 lessons remaining
- Next: Lessons 78-111 (Modules 2-9)

Coverage by Topic:
✅ Linux Foundations (7/7) - 100%
⏳ Advanced Logging (0/3) - 0%
⏳ File Systems (0/7) - 0%
[... all topics]

Completion Timeline:
- Module 1: ✅ Complete (7 lessons)
- Module 2: 📋 Ready (3 lessons planned)
- Module 3: 📋 Ready (7 lessons planned)
```

### 3. Quality Metrics

```
📈 QUALITY METRICS

Content Block Distribution:
- mindset_coach: 98% of lessons ✓
- explanation: 100% of lessons ✓
- code_exercise: 85% of lessons
- real_world: 78% of lessons
- memory_aid: 65% of lessons ⚠️
- reflection: 72% of lessons

Assessment Questions:
- Average per lesson: 4.2 questions
- Lessons with < 3 questions: 5 ⚠️
- Difficulty distribution:
  - Easy: 35%
  - Medium: 50%
  - Hard: 15%

Jim Kwik Principles Usage:
- active_learning: 95%
- minimum_effective_dose: 92%
- teach_like_im_10: 88%
[... all 10 principles]
```

### 4. Prerequisite Chain Analysis

```
🔗 PREREQUISITE ANALYSIS

Chain Completeness:
- Valid chains: 275 lessons (98%)
- Broken chains: 7 lessons ⚠️
- No prerequisites: 15 lessons (expected for starting lessons)

Average Chain Length:
- DFIR: 6.2 lessons per chain
- Malware: 4.5 lessons per chain
- [... per domain]

Dependency Graph:
  71 → 72 → 73 → 74 → 75 → 76 → 77 ✓
       ↓
      78 → 79 → 80 (Module 2)
```

### 5. Course Tag Distribution

```
🏷️  COURSE TAG ANALYSIS

Tagged Lessons: 226 (80%)
Untagged: 56 (20%) ⚠️

By Course:
- 13Cubed-Investigating Linux Devices: 41 lessons
- SANS-FOR500: 19 lessons
- SANS-FOR508: 18 lessons
- SANS-FOR509: 25 lessons
[... all tags]

Recommendations:
- Tag lessons 50-60 (currently untagged)
- Consider adding SANS-FOR572 tag to network lessons
```

### 6. Gap Analysis

```
🔍 GAP ANALYSIS

Missing Content Types:
- 35 lessons missing memory_aid
- 28 lessons missing reflection
- 15 lessons below 4,000 words

Domain Gaps (not_started):
- DFIR: 34 lessons (orders 78-111)
- IoT Security: 4 lessons
- Web3 Security: 3 lessons

Difficulty Gaps:
- DFIR needs more beginner lessons
- Cloud needs more advanced lessons
- OSINTneeds intermediate lessons

Recommendations:
1. Enhance lessons missing memory_aids
2. Complete DFIR domain (high priority)
3. Balance difficulty distribution
```

## Custom Queries

Support flexible queries:
```
"Show me all DFIR lessons with < 5,000 words"
"List lessons missing memory_aids"
"Which domains have the most advanced lessons?"
"Show prerequisite chain for lesson 85"
"Word count distribution for Blue Team domain"
```

## Visualization

Generate ASCII art visualizations:
```
Lesson Progress by Domain:

DFIR     ████████████████████░░░░░░░░░░ 77/111 (69%)
Malware  ███████████████░░░░░░░░░░░░░░░ 21/35  (60%)
Cloud    ███████████████████████░░░░░░░ 45/60  (75%)
...
```

## Export Formats

- Markdown reports
- CSV exports
- JSON data dumps
- Terminal-friendly summaries

## Integration

- Works with **prerequisite-checker** for chain analysis
- Uses **course-tag-manager** for tag statistics
- Integrates with **lesson-validator** for quality metrics
- Helps **batch-lesson-generator** prioritize gaps
