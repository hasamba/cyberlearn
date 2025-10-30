# CyberLearn Platform - Claude Instructions

## Project Context

CyberLearn is an adaptive cybersecurity learning platform built with:
- **Backend**: FastAPI + SQLAlchemy + Pydantic V2
- **Frontend**: Streamlit
- **Database**: SQLite (cyberlearn.db)
- **Content**: Rich JSON lesson files with 4,000-5,500 words each

## General Guidelines

- Always save new or changed code in files in the project folder
- Don't run commands - this is just a host machine, tell me what to run on my VMs
- Write files only in the project folder, not anywhere else

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
- **Length**: 4,000-5,500 words
- **Mindset coaching**: Jim Kwik principles, encouragement
- **Deep technical content**: Not surface-level explanations
- **Real-world examples**: Actual attacks, case studies, company examples
- **Code snippets**: Commands, scripts, configurations (where applicable)
- **Memory aids**: Mnemonics, acronyms, visual associations
- **Common pitfalls**: Warnings about mistakes
- **Actionable takeaways**: Clear next steps
- **ASCII art**: Diagrams where helpful (network topology, attack flow)

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

## Current Status (Latest Update: 2025-10-30)

- ✅ **275 total lessons** in database
- ✅ **12 active domains** (9 core + 3 specialized)
- ✅ **17 system tags** implemented (Career Path, Course, Package)
- ✅ **Tagging system** with many-to-many relationships
- ✅ **Linux Forensics course** (41 lessons, 13Cubed)
- ✅ **124 lesson ideas** planned in lesson_ideas.csv
- ✅ **5 planned features** in FEATURES.md

### Lessons by Domain (Database):
- **DFIR**: 93 lessons (includes 70 Windows + 41 Linux forensics from 13Cubed courses)
- **Pentest**: 36 lessons
- **Red Team**: 19 lessons
- **Active Directory**: 16 lessons
- **Blue Team**: 16 lessons
- **Linux**: 16 lessons
- **Malware**: 16 lessons
- **Cloud**: 15 lessons
- **System**: 15 lessons
- **Fundamentals**: 13 lessons
- **OSINT**: 10 lessons
- **Threat Hunting**: 10 lessons

### Tagging System:
- **17 system tags** across 3 categories:
  - **Career Path** (10 tags): SOC Analyst, Pentester, Red Teamer, Blue Teamer, DFIR Specialist, Malware Analyst, Cloud Security, Threat Hunter, GRC Analyst, Security Engineer
  - **Course** (5 tags): 13Cubed courses (Windows Memory, Windows Endpoints, Linux Forensics), Eric Zimmerman Tools, Log2Timeline/Plaso
  - **Package** (2 tags): Eric Zimmerman Tools, User Content
- **Auto-tagging**: Lessons automatically tagged based on order_index ranges
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
1. **Single/Multiple JSON Lesson Upload** - High priority
2. **Lesson Package Import/Export (ZIP)** - High priority
3. **Add AI Security Domain** - High priority
4. **Global Lesson Search** - High priority
5. **Hide/Unhide Lessons** - Medium priority

### Completion Status:
- **Target**: 325+ lessons for comprehensive coverage (8-12 per domain)
- **Current**: 275 lessons in database
- **Completion**: 84% of target
- **Next Priority**: Implement planned features, add AI/IoT/Web3 domains

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
- **Current**: 275 lessons (84% of target)
- **Architecture**: FastAPI + Streamlit + SQLite + Pydantic V2

### Development Workflow
When working on this project:
1. **Check FEATURES.md** for planned work and priorities
2. **Review lesson_ideas.csv** for curriculum gaps
3. **Follow validation requirements** strictly (use comprehensive_fix.py)
4. **Test thoroughly** before considering complete:
   - Run `python load_all_lessons.py`
   - Test in Streamlit app
   - Verify tags, XP, prerequisites
5. **Document all changes** in appropriate files (FEATURES.md, CLAUDE.md, session docs)
6. **Prioritize quality over quantity** - rich, technical content with real-world examples

### Feature Implementation Priority
1. **High Priority**: Search, JSON upload, AI domain, package import/export
2. **Medium Priority**: Hide/unhide lessons
3. **Future**: See FEATURES.md Future Ideas section

### Recent Major Updates (2025-10-30)
- ✅ Merged PR #11, #12, #13 (Linux forensics, 75 lessons)
- ✅ Implemented tagging system (17 tags, many-to-many)
- ✅ Created FEATURES.md master features list
- ✅ Added 124 lesson ideas to lesson_ideas.csv
- ✅ Fixed domain naming consistency (blue_team, red_team)

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
