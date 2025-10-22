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

## Domain Structure (9 Domains)

1. **fundamentals** - Prerequisites: none
2. **dfir** - Prerequisites: fundamentals
3. **malware** - Prerequisites: fundamentals
4. **active_directory** - Prerequisites: fundamentals
5. **system** - Prerequisites: fundamentals (Windows/Linux internals)
6. **cloud** - Prerequisites: fundamentals + system (AWS, Azure, GCP)
7. **pentest** - Prerequisites: fundamentals + active_directory
8. **redteam** - Prerequisites: pentest + malware
9. **blueteam** - Prerequisites: dfir + malware

**Important**: Keep pentest and redteam separate (different career paths and skill progressions)

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
python fix_rich_uuids.py              # Fix invalid UUIDs
python fix_new_rich_lessons.py        # Add missing fields, fix content types
python fix_placeholder_prerequisites.py  # Remove invalid prerequisites
```

### Database Migration
```bash
python add_system_cloud_domains.py    # Add system and cloud domains
```

### Content Generation
```bash
python create_lesson_template.py      # Create lesson JSON template
python fill_lesson_with_ai.py         # AI-assisted content filling
python create_rich_lesson.py --interactive  # Interactive lesson creator
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
**Fix**: Run `fix_rich_uuids.py` to generate new valid UUIDs

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
6. **Test Load**: Run `python load_all_lessons.py` to validate
7. **Review**: Test in Streamlit app, verify XP awards, skill updates

### For Domain Expansion:

1. **Identify gaps**: Which domains have < 8 lessons?
2. **Create batch config**: Use `generate_all_rich_lessons.json` format
3. **Generate lessons**: One at a time with proper prerequisites
4. **Maintain progression**: Easy (1) → Medium (2) → Hard (3)
5. **Link prerequisites**: Each lesson builds on previous concepts

## Current Status (After Recent Session)

- ✅ 14 rich lessons created (46,700+ words)
- ✅ 9 domains defined with prerequisites
- ✅ Database migration ready for system + cloud domains
- ✅ All validation errors fixed
- ✅ Load scripts updated for Pydantic V2

### Domains with Content:
- **Active Directory**: 3 lessons (Fundamentals, Group Policy, Kerberos)
- **Blue Team**: 2 lessons (Fundamentals, Log Analysis)
- **DFIR**: 1 lesson (Incident Response)
- **Fundamentals**: 4 lessons (Auth, Encryption, Network Security, etc.)
- **Malware**: 1 lesson (Malware Types)
- **Pentest**: 1 lesson (Methodology)
- **Red Team**: 2 lessons (Fundamentals, OSINT)
- **System**: 1 lesson (Windows Internals)
- **Cloud**: 0 lessons (needs content)

### Priority Work:
1. Create first lessons for Blue Team, Red Team (order_index 1)
2. Create 5-6 cloud domain lessons
3. Expand all domains to 8-12 lessons each

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
- 4,000-5,500 words for rich lessons

### Testing
- Always test lesson loading: `python load_all_lessons.py`
- Verify in Streamlit app: XP awards, skill updates, prerequisites
- Check adaptive recommendations: Does engine suggest appropriate lessons?

## Resources

- [FINAL_FIXES_READY.md](FINAL_FIXES_READY.md) - Deployment instructions
- [SESSION_ACCOMPLISHMENTS.md](SESSION_ACCOMPLISHMENTS.md) - Recent work summary
- [ADD_NEW_DOMAINS.md](ADD_NEW_DOMAINS.md) - Domain creation guide
- [DOMAINS_ADDED_SUMMARY.md](DOMAINS_ADDED_SUMMARY.md) - System/cloud domains

## Contact & Development

- **Platform**: Adaptive learning with gamification (XP, levels, achievements)
- **Goal**: Comprehensive cybersecurity education across 9 domains
- **Target**: 80-100 rich lessons (8-12 per domain)
- **Current**: 14 rich lessons (17% of target)

When working on this project:
- Prioritize content quality over quantity
- Maintain consistent lesson structure
- Follow validation requirements strictly
- Test thoroughly before considering complete
- Document all changes and decisions
