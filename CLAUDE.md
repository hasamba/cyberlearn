# CyberLearn Platform - Claude Instructions

## Project Context

CyberLearn is an adaptive cybersecurity learning platform built with:
- **Backend**: FastAPI + SQLAlchemy + Pydantic V2
- **Frontend**: Streamlit
- **Database**: SQLite (cyberlearn.db)
- **Content**: Rich JSON lesson files with 4,000-5,500 words each

## General Guidelines

- Always save new or changed code in files in the project folder
- Write files only in the project folder, not anywhere else

## CRITICAL: Template Database Workflow

**IMPORTANT: After ANY database schema changes (migrations, new tables, etc.), ALWAYS update the template database:**

```bash
# 1. Update template database on dev machine
python update_template_database.py

# 2. Commit the updated template
git add cyberlearn_template.db
git commit -m "Update template database with [describe changes]"
git push

# 3. User runs on VM to get updated database
bash update_vm.sh
```

**Why this matters**: The template database (`cyberlearn_template.db`) is copied to VMs when running `update_vm.sh`. If you don't update it after schema changes, VMs will get an outdated database and crash with "no such table" or "no such column" errors.

**Template database should always include**:
- All tables (lessons, users, progress, tags, lesson_tags, notes, etc.)
- All system tags (Course tags, Career Path tags, etc.)
- All lessons loaded and tagged
- All migrations applied

## CRITICAL: Development Environment Rules

**THIS IS A DEVELOPMENT HOST MACHINE**

- ✅ **DO**: Run Python scripts on THIS dev host (where Claude is)
- ✅ **DO**: Execute database migrations, validation scripts, data processing
- ✅ **DO**: Create files, edit code, commit to git, push to GitHub
- ✅ **DO**: Run the Streamlit app locally for testing (`streamlit run app.py`)
- ✅ **DO**: Use Playwright MCP to test the application automatically
- ✅ **DO**: Test all changes with Playwright BEFORE creating PRs (unless impossible)
- ❌ **DON'T**: Tell user to run Python scripts - just run them here!
- ❌ **DON'T**: Ask user to test manually - use Playwright to test automatically
- ❌ **DON'T**: Create PRs without testing when testing is possible

**If a Python script needs to run, RUN IT HERE IMMEDIATELY. Do NOT ask the user to run it.**

**If a feature needs testing, USE PLAYWRIGHT MCP TO TEST IT. Do NOT ask the user to test it.**

## Testing Requirements

**CRITICAL: Always test changes before creating PRs**

1. **For UI changes**: Use Playwright MCP (`mcp__playwright_*` tools) to:
   - Navigate to the affected page
   - Take screenshots before/after
   - Verify the fix works
   - Test edge cases

2. **For backend/database changes**: Run validation scripts and verify data integrity

3. **When to skip testing**: Only if Playwright cannot access the feature (auth walls, complex state) or user explicitly says to skip testing

**Testing workflow:**
```bash
# 1. Run Streamlit app in background
streamlit run app.py &

# 2. Use Playwright MCP to test
# (Use mcp__playwright_navigate, mcp__playwright_click, mcp__playwright_screenshot, etc.)

# 3. Verify fix works

# 4. Create PR with test results
```

## Project Structure

```
c:\Users\yaniv\...\57.14_Learning_app\
├── api/                    # FastAPI backend
│   ├── routes.py          # API endpoints
│   └── __init__.py
├── content/               # Lesson JSON files
│   ├── lesson_*_RICH.json  # Rich lessons (4,000-5,500 words)
│   └── lesson_*.json       # Placeholder lessons
├── core/                  # Core business logic
│   ├── adaptive_engine.py  # Lesson recommendations
│   └── lesson_generator.py # Content generation
├── models/                # Pydantic models
│   ├── user.py            # User and SkillLevels
│   └── lesson.py          # Lesson model
├── tools/                 # Content creation tools
│   ├── create_lesson_template.py
│   └── fill_lesson_with_ai.py
├── app.py                 # Streamlit frontend
├── database.py            # Database setup
└── cyberlearn.db          # SQLite database
```

## Domain Structure (15 Domains)

### Core Domains (12)
1. **fundamentals** - Prerequisites: none
2. **dfir** - Prerequisites: fundamentals
3. **malware** - Prerequisites: fundamentals
4. **active_directory** - Prerequisites: fundamentals
5. **system** - Prerequisites: fundamentals (Windows/Linux internals)
6. **cloud** - Prerequisites: fundamentals + system (AWS, Azure, GCP)
7. **pentest** - Prerequisites: fundamentals + active_directory
8. **red_team** - Prerequisites: pentest + malware
9. **blue_team** - Prerequisites: dfir + malware
10. **osint** - Prerequisites: fundamentals
11. **threat_hunting** - Prerequisites: blue_team
12. **linux** - Prerequisites: fundamentals

### Emerging Technology Domains (3)
13. **ai_security** - Prerequisites: fundamentals (Planned - see FEATURES.md)
14. **iot_security** - Prerequisites: fundamentals + system (Planned)
15. **web3_security** - Prerequisites: fundamentals (Planned)

**Important Notes:**
- Keep pentest and red_team separate (different career paths and skill progressions)
- Domain naming: Use underscores (e.g., `blue_team` not `blueteam`) for consistency
- Emerging domains are in planning phase - see [lesson_ideas.csv](lesson_ideas.csv) and [FEATURES.md](FEATURES.md)

## Working with Lessons

### Lesson Format Requirements

All lessons MUST have:
- `lesson_id`: Valid UUID (use uuid.uuid4())
- `domain`: One of the 9 domains
- `title`: Clear, descriptive title
- `difficulty`: 1-3 (beginner, intermediate, advanced)
- `order_index`: Position in domain sequence
- `prerequisites`: List[str] of lesson_id UUIDs (empty array if none)
- `concepts`: List of key concepts covered
- `estimated_time`: Minutes to complete
- `learning_objectives`: List of learning goals
- `post_assessment`: List of assessment questions
- `jim_kwik_principles`: List of learning principles applied
- `content_blocks`: List of content sections

### Valid Content Block Types

Only use these content block types (ContentType enum):
- `explanation` - Core concept explanations
- `video` - Video content (URL or embedded)
- `diagram` - Visual diagrams
- `quiz` - Interactive quizzes
- `simulation` - Hands-on simulations
- `reflection` - Reflection questions
- `memory_aid` - Mnemonics and memory techniques
- `real_world` - Real-world applications
- `code_exercise` - Code examples and exercises
- `mindset_coach` - Motivational coaching sections

**Do NOT use**: concept_deep_dive, real_world_application, step_by_step_guide, common_pitfalls, actionable_takeaways (these are invalid and will cause validation errors)

### Rich Lesson Standards

Rich lessons should include:
- **Length**: 4,000-15,000 words (extended for complex topics)
- **Mindset coaching**: All 10 Jim Kwik principles applied, encouragement throughout
- **Deep technical content**: Not surface-level explanations
- **Real-world examples**: Actual attacks, case studies, company examples
- **Code snippets**: Commands, scripts, configurations (where applicable)
- **Memory aids**: Mnemonics, acronyms, visual associations
- **Common pitfalls**: Warnings about mistakes
- **Actionable takeaways**: Clear next steps
- **ASCII art**: Diagrams where helpful (network topology, attack flow)
- **Video content**: At least one video block (recommended)
- **Content variety**: Minimum 4 different content block types
- **Post-assessment**: Minimum 3 assessment questions

**Jim Kwik Principles (All 10 Required):**

**CRITICAL:** The `jim_kwik_principles` array is a metadata tag indicating which learning science principles are **actually implemented** in the lesson content, NOT just listed. Each principle must be evident in the content itself.

---

## 🚨 MOST IMPORTANT: teach_like_im_10 (MANDATORY FOR EVERY LESSON)

**This is the foundation of all effective teaching. Every lesson MUST implement this principle.**

**IMPORTANT:** This does NOT mean the entire lesson is written for 10-year-olds. It means there must be a dedicated section called "Teach Me Like I'm 10" that explains the core concepts simply.

1. **`teach_like_im_10`** - Include a dedicated "Teach Me Like I'm 10" section ⭐ **MANDATORY - HIGHEST PRIORITY**
   - ✅ **REQUIRED:** A content block with title "Teach Me Like I'm 10"
   - ✅ **REQUIRED:** This block explains the lesson's core concepts in simple, everyday language
   - ✅ **REQUIRED:** Use analogies a 10-year-old can understand ("like a hotel check-in", "like a locked safe", "like a security guard")
   - ✅ **REQUIRED:** Typically 200-400 words
   - ✅ **REQUIRED:** Should be one of the early content blocks (usually block 2 or 3)
   - ✅ The REST of the lesson can and should contain technical depth appropriate to the difficulty level
   - ❌ This is ONE dedicated section, not a requirement for the entire lesson to be written in simple language

   **Validation:** Every lesson will be checked for the presence of a "Teach Me Like I'm 10" section. Lessons without this dedicated section will FAIL validation.

---

## Other Required Principles (All Important)

2. **`memory_hooks`** - Create memorable associations
   - ✅ Include `memory_aid` content blocks with mnemonics
   - ✅ Create acronyms (e.g., "AAA = Authentication, Authorization, Accounting")
   - ✅ Visual associations ("Think: 'Triple-A' like AAA batteries")
   - ❌ Do NOT just list the principle without actual mnemonics

3. **`connect_to_what_i_know`** - Link to existing knowledge
   - ✅ Reference prior lessons ("Remember from lesson X...")
   - ✅ Use `prerequisites` array to link related lessons
   - ✅ Connect to familiar concepts ("Similar to how you...")
   - ✅ Build on established knowledge

4. **`active_learning`** - Hands-on practice and exercises
   - ✅ Include `code_exercise` blocks with hands-on tasks
   - ✅ Include `simulation` blocks with practice scenarios
   - ✅ Include `quiz` blocks with interactive questions
   - ✅ Minimum 2 active learning blocks per lesson

5. **`meta_learning`** - Learn how to learn
   - ✅ Include `reflection` blocks about the learning process
   - ✅ Ask "How did you learn this?" questions
   - ✅ Prompt students to monitor their own progress
   - ✅ Encourage awareness of learning strategies

6. **`minimum_effective_dose`** - Focus on essential concepts
   - ✅ Limit to 6-8 key concepts per lesson
   - ✅ Keep content blocks to 12-15 maximum
   - ✅ Avoid information overload
   - ✅ Focus on what matters most

7. **`reframe_limiting_beliefs`** - Overcome mental blocks
   - ✅ Include `mindset_coach` blocks with encouragement
   - ✅ Address common fears ("This may seem complex, but...")
   - ✅ Build confidence with positive framing
   - ✅ Celebrate progress and learning

8. **`gamify_it`** - Make learning engaging
   - ✅ Include challenges and practice tasks
   - ✅ Use engaging language ("mission", "challenge", "level up")
   - ✅ Include `quiz` blocks as mini-challenges
   - ✅ Post-assessment as final challenge

9. **`learning_sprint`** - Build momentum
   - ✅ Structure: Explanation → Practice → Reflection
   - ✅ Clear progression through content blocks
   - ✅ Sprint-sized: 30-60 minutes (estimated_time)
   - ✅ Focused flow with clear beginning, middle, end

10. **`multiple_memory_pathways`** - Visual, auditory, kinesthetic learning
    - ✅ Visual: `diagram` blocks with ASCII art or visual aids
    - ✅ Auditory: `video` blocks with video content
    - ✅ Kinesthetic: `code_exercise` and `simulation` blocks
    - ✅ Minimum 2 pathways per lesson (ideally all 3)

**Quality Check:** Use `validate_content_quality.py` to verify that principles are ACTUALLY implemented in content, not just listed in metadata.

### Creating New Lessons

**Option 1: Manual Creation**
1. Use `create_lesson_template.py` to generate JSON structure
2. Fill in content manually following rich lesson standards

**Option 2: AI-Assisted Creation**
1. Create template with `create_lesson_template.py`
2. Use `fill_lesson_with_ai.py` to generate content
3. Review and enhance generated content

**Option 3: Direct Creation**
- Create JSON file following [lesson_*_RICH.json](content/) examples
- Ensure all required fields present
- Use valid content block types only

## Common Scripts

### Loading Lessons
```bash
python load_all_lessons.py  # Load all lessons from content/ into database
```

### Fixing Validation Errors
```bash
python comprehensive_fix.py          # MAIN FIX SCRIPT - Run this first!
python fix_rich_uuids.py              # (Legacy) Fix invalid UUIDs
python fix_new_rich_lessons.py        # (Legacy) Add missing fields, fix content types
python fix_placeholder_prerequisites.py  # Remove invalid prerequisites
```

**comprehensive_fix.py** automatically handles:
- ✅ Invalid UUIDs → Generates new valid UUIDs
- ✅ Missing order_index → Extracts from filename
- ✅ estimated_time > 60 → Caps at 60 minutes
- ✅ String content → Wraps in dict with 'text' key
- ✅ Free-text jim_kwik_principles → Converts to enum values
- ✅ Missing post_assessment fields → Adds with defaults

### Database Migration
```bash
python add_system_cloud_domains.py    # Add system and cloud domains
```

### Tagging Scripts
```bash
python add_all_tags.py                # Add all 17 system tags to database
python add_13cubed_tags.py            # Add 13Cubed course tags and auto-tag lessons
python verify_tags.py                 # Verify all lessons are correctly tagged
```

### Content Generation
```bash
python create_lesson_template.py      # Create lesson JSON template
python fill_lesson_with_ai.py         # AI-assisted content filling
python create_rich_lesson.py --interactive  # Interactive lesson creator
python add_lesson_ideas.py            # Add lesson ideas to lesson_ideas.csv
python add_comprehensive_lesson_ideas.py  # Add 53 comprehensive lesson ideas
```

## Validation Error Troubleshooting

### Error: "Field required"
**Cause**: Missing required field (estimated_time, learning_objectives, etc.)
**Fix**: Run `fix_new_rich_lessons.py` or add missing fields manually

### Error: "Input should be 'explanation', 'video'..."
**Cause**: Invalid content block type
**Fix**: Use only valid ContentType enum values listed above

### Error: "Input should be a valid string [input_value=UUID(...)]"
**Cause**: Prerequisites stored as UUID objects instead of strings
**Fix**: Already fixed in load_all_lessons.py line 40

### Error: "invalid literal for int() with base 16"
**Cause**: Malformed UUID (wrong format or length)
**Fix**: Run `comprehensive_fix.py` to generate new valid UUIDs

### Error: "Input should be a valid dictionary"
**Cause**: Content block has string content instead of dict structure
**Fix**: Run `comprehensive_fix.py` to automatically wrap all string content in dicts

## Adding New Domains

When adding a new domain:
1. Update [models/user.py](models/user.py) - Add skill field to SkillLevels class
2. Update [core/adaptive_engine.py](core/adaptive_engine.py) - Add prerequisites and diagnostic questions
3. Create database migration script to add skill column
4. Create first lesson for domain (order_index 1, difficulty 1)
5. Update documentation

See [ADD_NEW_DOMAINS.md](ADD_NEW_DOMAINS.md) for detailed guide.

## Content Creation Workflow

### For New Rich Lessons:

1. **Plan**: Decide domain, difficulty, order_index, prerequisites
2. **Research**: Gather technical content, real-world examples, code snippets
3. **Write**: Create comprehensive content following rich lesson standards
4. **Structure**: Organize into proper content blocks with valid types
5. **Validate**: Ensure all required fields present
6. **Fix**: Run `python comprehensive_fix.py` to auto-correct validation issues
7. **Test Load**: Run `python load_all_lessons.py` to validate
8. **Review**: Test in Streamlit app, verify XP awards, skill updates

**See [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md) for complete step-by-step guide with examples.**

### For Domain Expansion:

1. **Identify gaps**: Which domains have < 8 lessons?
2. **Create batch config**: Use `generate_all_rich_lessons.json` format
3. **Generate lessons**: One at a time with proper prerequisites
4. **Maintain progression**: Easy (1) → Medium (2) → Hard (3)
5. **Link prerequisites**: Each lesson builds on previous concepts

## Current Status (Latest Update: 2025-10-31)

- ✅ **591 total lessons** in database (115% increase from 275)
- ✅ **15 active domains** (12 core + 3 emerging tech)
- ✅ **17 system tags** implemented (Career Path, Course, Package)
- ✅ **10 course tags** applied (13Cubed, SANS courses, OWASP)
- ✅ **Tagging system** with many-to-many relationships
- ✅ **100% lesson compliance** (all 591 lessons validated)
- ✅ **Notes system** with image support
- ✅ **Hide/unhide lessons** functionality
- ✅ **Assessment system** integrated

### Lessons by Domain (Database):
- **DFIR**: 237 lessons (156% increase - includes SANS FOR500/508/528/572, 13Cubed courses)
- **Pentest**: 62 lessons (72% increase - includes SANS SEC504)
- **Cloud**: 45 lessons (200% increase - includes SANS FOR509)
- **OSINT**: 37 lessons (270% increase - includes SANS FOR589)
- **Threat Hunting**: 30 lessons (200% increase - includes SANS FOR608)
- **Blue Team**: 28 lessons (75% increase)
- **Red Team**: 26 lessons (37% increase)
- **Active Directory**: 24 lessons (50% increase)
- **Linux**: 22 lessons (38% increase)
- **System**: 22 lessons (47% increase)
- **Malware**: 21 lessons (31% increase)
- **Fundamentals**: 17 lessons (31% increase)
- **AI Security**: 13 lessons (NEW - includes OWASP LLM Top 10)
- **IoT Security**: 4 lessons (NEW)
- **Web3 Security**: 3 lessons (NEW)

### Tagging System:
- **17 system tags** across 3 categories:
  - **Career Path** (10 tags): SOC Analyst, Pentester, Red Teamer, Blue Teamer, DFIR Specialist, Malware Analyst, Cloud Security, Threat Hunter, GRC Analyst, Security Engineer
  - **Course** (5 tags): 13Cubed courses (Windows Memory, Windows Endpoints, Linux Forensics), Eric Zimmerman Tools, Log2Timeline/Plaso
  - **Package** (2 tags): Eric Zimmerman Tools, User Content
- **10 course tags** applied to 226 lessons:
  - **Course: 13Cubed-Investigating Linux Devices**: 41 lessons
  - **Course: OWASP LLM Top 10**: 10 lessons
  - **Course: SANS-FOR500**: 19 lessons (Windows Forensics)
  - **Course: SANS-FOR508**: 18 lessons (Advanced IR)
  - **Course: SANS-FOR509**: 25 lessons (Cloud Forensics)
  - **Course: SANS-FOR528**: 16 lessons (Ransomware)
  - **Course: SANS-FOR572**: 25 lessons (Network Forensics)
  - **Course: SANS-FOR589**: 22 lessons (Cybercrime Intelligence)
  - **Course: SANS-FOR608**: 27 lessons (Enterprise IR)
  - **Course: SANS-SEC504**: 28 lessons (Hacker Tools)
- **Auto-tagging**: Course tags assigned via lesson_ideas.csv mapping
- **Template database**: Ships with all tags pre-populated

### Lesson Ideas Pipeline (lesson_ideas.csv):
- **124 lesson ideas** planned across 15 domains
- **53 new ideas** added 2025-10-30:
  - Red Team Advanced Operations (7 lessons)
  - Pentest Web App Security (6 lessons)
  - Malware Advanced Topics (5 lessons)
  - Active Directory Advanced (8 lessons)
  - Linux Security & Hardening (4 lessons)
  - Fundamentals GRC (3 lessons)
  - Blue Team Detection Engineering (5 lessons)
  - OSINT Threat Intel (5 lessons)
  - AI Security (3 lessons)
  - IoT Security (4 lessons)
  - Web3 Security (3 lessons)

### Planned Features (FEATURES.md):
1. **Single/Multiple JSON Lesson Upload** - High priority ✅ COMPLETED (PR#4)
2. **Lesson Package Import/Export (ZIP)** - High priority
3. **Global Lesson Search** - High priority ✅ COMPLETED (PR#5)
4. **Hide/Unhide Lessons** - Medium priority ✅ COMPLETED (PR#8)
5. **Notes System** - ✅ COMPLETED (PR#10, V1.3)
6. **Assessment System** - ✅ COMPLETED

### Completion Status:
- **Target**: 325+ lessons for comprehensive coverage (8-12 per domain)
- **Current**: 591 lessons in database
- **Completion**: 182% of target (EXCEEDED)
- **Achievement**: All 15 domains now have substantial content (13-237 lessons each)
- **Next Priority**: Expand emerging tech domains (AI Security, IoT, Web3)

## Important Notes

### Prerequisites
- Store as List[str] (lesson_id UUIDs as strings)
- Empty array `[]` if no prerequisites
- Don't reference placeholder lessons (bt000000-*, fn000000-*, etc.)

### Lesson IDs
- Always use valid UUIDs: `str(uuid.uuid4())`
- Format: `xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx`
- No placeholder IDs in production lessons

### Content Quality
- Professional tone with encouragement
- Technical depth appropriate for difficulty level
- Real-world relevance (actual tools, attacks, companies)
- Learning science principles (Jim Kwik methods)
- 4,000-15,000 words for rich lessons (adjusted for complexity)

### Testing
- Always test lesson loading: `python load_all_lessons.py`
- Verify in Streamlit app: XP awards, skill updates, prerequisites
- Check adaptive recommendations: Does engine suggest appropriate lessons?

## Planning & Documentation Files

### Primary Planning
- **[FEATURES.md](FEATURES.md)** - Master features list (5 planned, 2 completed)
- **[lesson_ideas.csv](lesson_ideas.csv)** - 124 lesson ideas across 15 domains
- **[lesson_ideas.json](lesson_ideas.json)** - Linux Forensics course specification (41 lessons)
- **[UNIVERSAL_LESSON_PROMPT.md](UNIVERSAL_LESSON_PROMPT.md)** - Template for AI lesson generation

### Implementation Guides
- **[HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md)** - Complete guide with examples and commands
- **[ADD_NEW_DOMAINS.md](ADD_NEW_DOMAINS.md)** - Domain creation guide
- **[FINAL_FIXES_READY.md](FINAL_FIXES_READY.md)** - Deployment instructions

### Recent Work
- **[SESSION_ACCOMPLISHMENTS.md](SESSION_ACCOMPLISHMENTS.md)** - Recent work summary
- **[DOMAINS_ADDED_SUMMARY.md](DOMAINS_ADDED_SUMMARY.md)** - System/cloud domains

### Key Differences to Understand
- **lesson_ideas.csv** vs **lesson_ideas.json**:
  - CSV = Master curriculum planning for ALL domains (124 lessons)
  - JSON = Detailed specification for Linux Forensics course only (41 lessons)
- **lesson_ideas.csv** vs **content/lesson_*.json**:
  - CSV = Planning/roadmap (lightweight metadata)
  - JSON = Production content (4,000-5,500 words, full teaching material)

## Contact & Development

- **Platform**: Adaptive cybersecurity learning with gamification (XP, levels, achievements)
- **Goal**: Comprehensive cybersecurity education across 15 domains
- **Target**: 325+ lessons (8-12 per domain)
- **Current**: 591 lessons (182% of target - EXCEEDED)
- **Architecture**: FastAPI + Streamlit + SQLite + Pydantic V2

### Development Workflow
When working on this project:
1. **Check FEATURES.md** for planned work and priorities
2. **Review lesson_ideas.csv** for curriculum gaps
3. **Follow validation requirements** strictly (use validate_lesson_compliance.py)
4. **Test thoroughly** before considering complete:
   - Run `python load_all_lessons.py`
   - Run `python validate_lesson_compliance.py`
   - Test in Streamlit app
   - Verify tags, XP, prerequisites
5. **Document all changes** in appropriate files (FEATURES.md, CLAUDE.md)
6. **Prioritize quality over quantity** - rich, technical content with real-world examples

### Feature Implementation Priority
1. **High Priority**: Lesson Package Import/Export (ZIP)
2. **Medium Priority**: Expand emerging tech domains (AI, IoT, Web3)
3. **Completed**: ✅ Search, ✅ JSON upload, ✅ Hide/unhide, ✅ Notes, ✅ Assessments

### Recent Major Updates (2025-10-31)
- ✅ Merged PR #16 (180 SANS-based lessons across multiple domains)
- ✅ Tagged 226 lessons with 10 course tags (SANS, 13Cubed, OWASP)
- ✅ Updated lesson_ideas.csv status (all created lessons marked completed)
- ✅ Achieved 100% lesson compliance (591/591 lessons pass validation)
- ✅ Cleaned up 30 temporary/obsolete scripts and files
- ✅ Added 3 emerging tech domains: AI Security, IoT Security, Web3 Security
- ✅ Total lesson count: 591 (115% increase from 275)

## Quick Start for Adding Lessons

```bash
# 1. Create your lesson JSON file in content/
# 2. Fix validation issues
python comprehensive_fix.py

# 3. Load into database
python load_all_lessons.py

# 4. Test in app
streamlit run app.py
```

**For detailed instructions, see [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md)**
