# Rich Lesson Content Generator - Complete Guide

## What Is This?

A tool that helps you create professional, educational cybersecurity lessons automatically. It generates structured lesson templates that you can fill with rich content, or use as a starting point for AI-enhanced content generation.

## Quick Start

### Option 1: Interactive Mode (Easiest)

```bash
python create_rich_lesson.py --interactive

# You'll be prompted for:
# - Domain (red_team, blue_team, etc.)
# - Title
# - Difficulty (1-4)
# - Key concepts
# - Lesson type
```

### Option 2: Command Line

```bash
python create_rich_lesson.py \\
  --title "Kerberoasting Attack" \\
  --domain active_directory \\
  --difficulty 4 \\
  --concepts "SPN enumeration,TGS extraction,Offline cracking,Mitigation" \\
  --order 4
```

### Option 3: Batch Generation

```bash
# Generate 10 lessons at once
python create_rich_lesson.py --batch generate_all_rich_lessons.json
```

## Features

### 1. Structured Template Generation

Creates properly formatted lesson JSON with:
- ✅ All required fields (Pydantic-validated structure)
- ✅ Content blocks for different sections
- ✅ Quiz questions with explanations
- ✅ Memory aids and analogies placeholders
- ✅ Jim Kwik learning principles integration

### 2. Content Quality Guidelines

Each generated lesson includes:
- **Minimum word counts** based on difficulty
- **ELI10 analogy templates** (not placeholders like "Think of X as X")
- **Memory aid frameworks** (mnemonics, acronyms, visual associations)
- **Quiz question templates** with detailed explanation structure
- **Real-world connection prompts**

### 3. Lesson Types

Different templates for different content types:

#### Fundamentals (Difficulty 1-2)
- **Word count**: 2000+
- **Focus**: Clear explanations, build from basics
- **Example**: "What is Active Directory?"

#### Technique (Difficulty 2-4)
- **Word count**: 2500+
- **Focus**: Step-by-step procedures, tools, detection
- **Example**: "Kerberoasting Attack"

#### Tool (Difficulty 2-3)
- **Word count**: 1500+
- **Focus**: Installation, usage, practical examples
- **Example**: "Using Wireshark for Network Analysis"

#### Advanced (Difficulty 3-4)
- **Word count**: 3000+
- **Focus**: Deep technical details, attack chains
- **Example**: "APT29 Attack Simulation"

### 4. Content Generation Workflow

```
1. Run Generator
   ↓
2. Structured Template Created
   (with [CONTENT TO BE GENERATED] markers)
   ↓
3. Fill in Rich Content
   (manually or with AI assistance)
   ↓
4. Validate JSON
   ↓
5. Load into Database
   ↓
6. Lesson Available in App
```

## Detailed Usage

### Interactive Mode Example

```bash
$ python create_rich_lesson.py --interactive

============================================================
Rich Lesson Content Generator - Interactive Mode
============================================================

📚 Lesson Details:
  Domain: red_team
  Lesson Title: Social Engineering Advanced
  Difficulty (1-4): 3
  Key Concepts (comma-separated): Pretexting, Vishing, Baiting, Tailgating
  Order Index: 4

📝 Lesson Type:
  1. Fundamentals (foundational concepts)
  2. Technique (attack/defense procedures)
  3. Tool (how to use specific tool)
  4. Advanced (expert-level deep dive)
  Choose type (1-4): 2

🔧 Generating lesson structure...
✅ Created: content/lesson_red_team_04_social_engineering_advanced.json

📄 Content Template Generated
============================================================

NEXT STEPS:

1. EDIT THE CONTENT:
   Open: content/lesson_red_team_04_social_engineering_advanced.json
   Replace [CONTENT TO BE GENERATED] sections with real content

2. CONTENT REQUIREMENTS:
   - 2500+ words minimum
   - Real analogies (not 'like X in everyday life')
   - Specific examples and case studies
   - Memory techniques that actually work

3. USE THE GUIDE:
   Content guide saved to: content/lesson_red_team_04_social_engineering_advanced_PROMPT.txt
   Use this as reference when writing content

4. LOAD INTO DATABASE:
   python load_all_lessons.py
```

### Batch Generation Example

**Step 1**: Create batch file (`my_lessons.json`):

```json
[
  {
    "title": "SQL Injection Basics",
    "domain": "pentest",
    "difficulty": 2,
    "order_index": 5,
    "concepts": ["SQL queries", "Union attacks", "Blind SQLi", "Prevention"]
  },
  {
    "title": "Cross-Site Scripting (XSS)",
    "domain": "pentest",
    "difficulty": 2,
    "order_index": 6,
    "concepts": ["Reflected XSS", "Stored XSS", "DOM XSS", "CSP"]
  }
]
```

**Step 2**: Generate:

```bash
python create_rich_lesson.py --batch my_lessons.json

============================================================
Batch Lesson Generation
============================================================

📝 Generating: SQL Injection Basics
   ✅ Created: content/lesson_pentest_05_sql_injection_basics.json

📝 Generating: Cross-Site Scripting (XSS)
   ✅ Created: content/lesson_pentest_06_cross-site_scripting_xss.json

============================================================
✅ Generated 2 lessons
============================================================
```

## Content Quality Standards

### ❌ BAD Content (What to Avoid)

```json
{
  "content": {
    "text": "This lesson covers Kerberoasting. You'll learn the fundamentals."
  },
  "simplified_explanation": "Think of Kerberoasting like Kerberoasting in everyday life...",
  "memory_aids": ["Remember: Kerberoasting"]
}
```

**Problems:**
- No actual information
- Circular analogy (X like X)
- Useless memory aid

### ✅ GOOD Content (What to Create)

```json
{
  "content": {
    "text": "Kerberoasting exploits a weakness in how Windows Active Directory handles service accounts. When a service (like SQL Server) runs under a specific account, that account is assigned a Service Principal Name (SPN). Any authenticated user can request a Kerberos service ticket (TGS) for that SPN. The TGS is encrypted with the service account's password hash - and here's the vulnerability: you can extract that encrypted ticket and crack it OFFLINE.

Step-by-step attack:
1. Enumerate SPNs: setspn -T domain.com -Q */*
2. Request TGS tickets: Invoke-Kerberoast
3. Extract tickets to hashcat format
4. Crack offline with wordlists
5. Use compromised credentials

Why this works:
- Service accounts often have weak passwords
- TGS uses RC4 encryption (weak) by default
- Requesting TGS is legitimate - looks normal
- Cracking happens offline - undetectable

Defense:
- Use 25+ character passwords for service accounts
- Enable AES encryption
- Use Managed Service Accounts (gMSA)
- Monitor Event ID 4769 for unusual TGS requests"
  },
  "simplified_explanation": "Imagine service accounts are like spare keys hidden under doormats. Kerberoasting is finding those hiding spots, taking pictures of the keys, and going home to make copies at your leisure. The building doesn't know you took photos - you just walked by looking normal!",
  "memory_aids": [
    "Kerberoasting = Kerber-ROASTING (cooking/cracking passwords)",
    "SPN = Service Principal Name = Service's 'phone number' in AD",
    "Remember: Request TGS → Extract → Crack offline"
  ]
}
```

**Good because:**
- 250+ words of real technical content
- Actual analogy that teaches the concept
- Step-by-step procedures
- Tools and commands included
- Attack AND defense perspectives
- Real memory techniques

## Using with AI Assistants

Each generated lesson includes a `_PROMPT.txt` file with detailed instructions for AI content generation.

### With Claude/ChatGPT:

```
1. Open the generated _PROMPT.txt file
2. Copy the entire prompt
3. Paste into Claude/ChatGPT
4. Ask: "Generate the content blocks as specified"
5. AI generates rich, detailed content
6. Copy the generated content into your lesson JSON
7. Review and refine
```

### Example AI Prompt Usage:

```
You: [Paste content from lesson_kerberoasting_PROMPT.txt]

Claude: [Generates 2500+ words of detailed Kerberoasting content with:
- Technical explanations
- Step-by-step attack procedures
- Real-world analogies
- Memory aids
- Quiz questions
- Defense strategies]

You: [Copy generated content into lesson JSON]
```

## Batch Generation of All Remaining Lessons

To generate rich templates for all 42 remaining lessons:

```bash
# This creates templates for the top 10 most important lessons
python create_rich_lesson.py --batch generate_all_rich_lessons.json

# Creates 10 structured lesson templates in content/ directory
# Each with [CONTENT TO BE GENERATED] markers
# Each with a _PROMPT.txt guide for AI assistance
```

Then fill in content:
- **Option A**: Manually write content (30-60 min per lesson)
- **Option B**: Use AI with the generated prompts (5-10 min per lesson)
- **Option C**: Hybrid - AI generates, you refine (10-15 min per lesson)

## File Structure

After generation:

```
content/
├── lesson_red_team_04_social_engineering_advanced.json
├── lesson_red_team_04_social_engineering_advanced_PROMPT.txt
├── lesson_pentest_05_sql_injection_basics.json
├── lesson_pentest_05_sql_injection_basics_PROMPT.txt
└── ... (more lessons)
```

### Lesson JSON Structure

```json
{
  "lesson_id": "uuid",
  "domain": "red_team",
  "title": "Social Engineering Advanced",
  "difficulty": 3,
  "content_blocks": [
    {
      "block_id": "uuid",
      "type": "mindset_coach",
      "title": "Why This Matters",
      "content": { "text": "..." },
      "simplified_explanation": "...",
      "memory_aids": ["..."],
      "real_world_connection": "..."
    },
    {
      "block_id": "uuid",
      "type": "explanation",
      "title": "Concept Name",
      "content": { "text": "[CONTENT TO BE GENERATED]" },
      ...
    }
  ],
  "post_assessment": [
    {
      "question_id": "q1",
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 1,
      "explanation": "..."
    }
  ]
}
```

## Tips for Writing Rich Content

### 1. Start with "Why"
Begin each lesson explaining why this topic matters. Motivation drives learning.

### 2. Use the "Explain to a Friend" Test
If you can't explain it to a non-technical friend, your analogy isn't good enough.

### 3. Include Specific Examples
Not: "Attackers use social engineering"
But: "In 2016, attackers called a help desk pretending to be the CEO, reset the CEO's password using social engineering, and gained access to 10 million customer records"

### 4. Show, Don't Just Tell
Include:
- Commands and syntax
- Step-by-step procedures
- Screenshots or ASCII diagrams
- Real tool output

### 5. Balance Offensive and Defensive
For attack lessons, always include:
- How to perform the attack
- How to detect it
- How to prevent it
- Why defenders struggle with it

### 6. Test Your Memory Aids
Show the mnemonic to someone else. Do they remember it 5 minutes later? If not, improve it.

## Loading Lessons into Database

After creating rich content:

```bash
# Load all lessons (including new ones)
python load_all_lessons.py

# Check what's loaded
python check_database.py

# Reset user to see new lessons
python check_database.py reset yourusername

# Launch app
streamlit run app.py
```

## Troubleshooting

### Issue: "JSON validation error"
**Solution**: Check your JSON syntax with `python -m json.tool lesson.json`

### Issue: "Lesson not appearing in app"
**Solution**:
1. Check lesson was loaded: `python check_database.py`
2. Check user's skill level matches lesson difficulty
3. Reset user: `python check_database.py reset yourusername`

### Issue: "Content blocks missing"
**Solution**: Ensure all [CONTENT TO BE GENERATED] markers are replaced with real content

## Advanced: Custom Lesson Types

You can extend the tool with custom lesson types:

```python
# In create_rich_lesson.py, add to LESSON_TEMPLATES:

"case_study": {
    "description": "Real-world breach analysis",
    "word_count": 2000,
    "focus": "Timeline, attack chain, lessons learned, prevention"
},

"hands_on_lab": {
    "description": "Practical lab exercise",
    "word_count": 1000,
    "focus": "Setup instructions, step-by-step tasks, verification"
}
```

## Next Steps

1. **Generate templates** for your priority lessons
2. **Fill in rich content** (manually or with AI)
3. **Load into database** and test
4. **Get user feedback** on content quality
5. **Iterate and improve** based on feedback

## Questions?

- **How long to create one lesson?** 5-60 minutes depending on method (AI vs manual)
- **Can I edit generated lessons?** Yes! They're just JSON files
- **Can I create lessons in other languages?** Yes, just translate the content
- **Can I add custom fields?** Yes, but update Pydantic models too

---

**You now have a professional content generation system!** 🎉

Create unlimited high-quality lessons for your cybersecurity training platform.
