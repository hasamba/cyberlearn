# ChatGPT Prompt for Creating CyberLearn Lessons

Use this prompt template when asking ChatGPT to create new lessons for the CyberLearn platform.

---

## Full Prompt Template

Copy and paste this entire prompt into ChatGPT, filling in the [BRACKETED] sections:

```
You are creating a comprehensive cybersecurity lesson for the CyberLearn adaptive learning platform.

## LESSON SPECIFICATIONS

**Domain**: [DOMAIN] (e.g., osint, threat_hunting, pentest, malware, etc.)
**Lesson Number**: [NUMBER]
**Title**: [LESSON TITLE]
**Difficulty**: [1-3] (1=Beginner, 2=Intermediate, 3=Advanced)
**Order Index**: [NUMBER] (sequence in domain)
**Prerequisites**: [List lesson IDs or "none"]
**Estimated Time**: [30-60] minutes
**Concepts to Cover**: [List 5-8 key concepts]

## REQUIRED LESSON STRUCTURE

Create a complete JSON lesson file with the following structure:

### 1. METADATA
```json
{
  "lesson_id": "[Generate new UUID v4]",
  "domain": "[domain]",
  "title": "[Lesson Title]",
  "difficulty": [1-3],
  "order_index": [number],
  "prerequisites": [],
  "concepts": [
    "[Concept 1]",
    "[Concept 2]",
    ... (5-8 concepts)
  ],
  "estimated_time": [30-60],
  "learning_objectives": [
    "[Objective 1]",
    "[Objective 2]",
    ... (4-6 objectives)
  ]
}
```

### 2. CONTENT BLOCKS (8-12 blocks total)

**MUST INCLUDE IN THIS ORDER:**

**Block 1 - Mindset Coach** (type: "mindset_coach")
- 300-500 words of encouragement and mindset coaching
- Reference Jim Kwik learning principles
- Explain why this topic matters
- Build confidence and curiosity
- Connect to career goals

**Block 2-3 - Core Explanations** (type: "explanation")
- 800-1200 words each
- Deep technical content
- Use markdown formatting (##, ###, bullet points, tables)
- Include ASCII diagrams where helpful
- Real-world examples
- Code snippets where applicable

**Block 4 - Video** (type: "video")
- Embed relevant YouTube video URL
- Provide context: what to watch for
- Include key takeaways from video
- 50-100 words

**Block 5-7 - Additional Explanations** (type: "explanation")
- 600-1000 words each
- Cover remaining concepts
- Include comparisons, contrasts, tables
- Common pitfalls and mistakes
- Best practices

**Block 8 - Code Exercise** (type: "code_exercise")
- 800-1200 words
- Hands-on lab or exercise
- Step-by-step commands
- Expected output
- Troubleshooting tips
- Windows/Linux/Mac commands as appropriate

**Block 9 - Real World Case Study** (type: "real_world")
- 600-900 words
- Real company, real incident, real numbers
- Timeline of events
- What went wrong / what went right
- Lessons learned
- Metrics and impact ($$$, time, scale)

**Block 10 - Memory Aids** (type: "memory_aid")
- 400-600 words
- Mnemonics for key concepts
- Acronyms and frameworks
- Quick reference guide
- Cheat sheet format
- Visual associations

**Block 11 - Quiz** (type: "quiz")
- 2-3 scenario-based questions
- Each with explanation
- Test understanding, not memorization

**Block 12 - Reflection** (type: "reflection")
- 300-500 words
- Reflection questions
- How to apply learning
- Next steps
- Connection to career

### 3. POST-ASSESSMENT (2 questions)

```json
"post_assessment": [
  {
    "question_id": "[Generate UUID]",
    "type": "multiple_choice",
    "question": "[Challenging scenario-based question]",
    "options": [
      "[Option A]",
      "[Option B]",
      "[Option C]",
      "[Option D]"
    ],
    "correct_answer": [0-3],
    "explanation": "[Detailed 200-300 word explanation of why answer is correct and others are wrong]",
    "difficulty": [1-3]
  },
  ... (2 questions total)
]
```

### 4. JIM KWIK PRINCIPLES

```json
"jim_kwik_principles": [
  "active_learning",
  "meta_learning",
  "memory_hooks",
  "connect_to_what_i_know",
  "teach_like_im_10"
]
```

**ONLY USE THESE VALID VALUES:**
- active_learning
- meta_learning
- memory_hooks
- minimum_effective_dose
- teach_like_im_10
- connect_to_what_i_know
- reframe_limiting_beliefs
- gamify_it
- learning_sprint
- multiple_memory_pathways

### 5. MITRE ATT&CK TAGS (if applicable)

```json
"mitre_attack_tags": [
  "T1595 - Active Scanning",
  "T1592 - Gather Victim Host Information"
]
```

## CONTENT QUALITY REQUIREMENTS

### Length Target: 4,000-5,500 words total

### Must Include:
- ✅ Professional but encouraging tone
- ✅ Real company names and case studies
- ✅ Actual attack examples with dates
- ✅ Code snippets with syntax highlighting
- ✅ Commands for Windows, Linux, or Mac
- ✅ ASCII diagrams for network topology or process flow
- ✅ Dollar amounts ($) for business impact
- ✅ Time savings or attack timelines
- ✅ Memory aids and mnemonics
- ✅ Common mistakes and how to avoid them
- ✅ Actionable takeaways
- ✅ YouTube video embed (find real relevant video)
- ✅ Hands-on exercises with expected output
- ✅ Tables comparing technologies or approaches
- ✅ Markdown formatting (headers, bullets, code blocks)

### Content Block Structure:
```json
{
  "type": "explanation",
  "content": {
    "text": "Full markdown content here..."
  }
}
```

## EXAMPLE SNIPPET

Here's an example of the mindset_coach block:

```json
{
  "type": "mindset_coach",
  "content": {
    "text": "Welcome to [Topic Name]! You're about to learn one of the most powerful skills in [domain].\n\nHere's why this matters: [3-4 sentences on real-world impact]\n\nYou might be thinking: 'This looks complicated.' That's normal! As Jim Kwik teaches, the key to mastering complex topics is to break them into smaller chunks and connect them to what you already know.\n\nBy the end of this lesson, you'll be able to [specific achievement]. This skill has helped security professionals [real example: detect APT28, save $2M, reduce incident response time by 75%].\n\nLet's dive in with curiosity and confidence. Remember: every expert was once a beginner who decided to keep learning."
  }
}
```

## OUTPUT FORMAT

Generate a complete, valid JSON lesson file that:
1. Follows the exact structure above
2. Contains 4,000-5,500 words of technical content
3. Includes all required blocks
4. Has properly formatted JSON (no trailing commas)
5. Uses valid enum values for content types and Jim Kwik principles
6. Includes real case studies with company names
7. Provides hands-on exercises with commands
8. Contains challenging post-assessment questions

Generate the complete JSON now.
```

---

## Quick Examples for Different Domains

### Example 1: OSINT Lesson

```
**Domain**: osint
**Lesson Number**: 6
**Title**: Email & Username Intelligence
**Difficulty**: 2
**Order Index**: 6
**Prerequisites**: ["osint_01", "osint_02"]
**Estimated Time**: 50 minutes
**Concepts to Cover**:
- Email format enumeration
- Username OSINT across platforms
- Have I Been Pwned integration
- Email header analysis
- Professional email intelligence
- Disposable email detection
```

### Example 2: Threat Hunting Lesson

```
**Domain**: threat_hunting
**Lesson Number**: 3
**Title**: Windows Event Log Analysis for Hunters
**Difficulty**: 2
**Order Index**: 3
**Prerequisites**: ["threat_hunting_01", "threat_hunting_02"]
**Estimated Time**: 60 minutes
**Concepts to Cover**:
- Critical Windows Event IDs
- Sysmon event analysis
- PowerShell logging
- Lateral movement detection
- Credential dumping indicators
- Log parsing with PowerShell
```

### Example 3: Red Team Lesson

```
**Domain**: red_team
**Lesson Number**: 11
**Title**: Cloud Red Teaming - AWS Attack Paths
**Difficulty**: 3
**Order Index**: 11
**Prerequisites**: ["red_team_01", "fundamentals_cloud"]
**Estimated Time**: 60 minutes
**Concepts to Cover**:
- AWS enumeration techniques
- IAM privilege escalation
- S3 bucket exploitation
- Lambda backdoors
- CloudTrail evasion
- Cross-account pivoting
```

---

## After ChatGPT Generates the Lesson

### Step 1: Save the JSON

Save ChatGPT's output to:
```
content/lesson_[domain]_[number]_[title_snake_case]_RICH.json
```

Example:
```
content/lesson_osint_06_email_username_intelligence_RICH.json
```

### Step 2: Validate Locally (on Windows)

```bash
cd "C:\Users\yaniv\...\57.14_Learning_app"
python comprehensive_fix.py
```

This will:
- Fix any invalid UUIDs
- Fix any validation errors
- Add missing fields

### Step 3: Commit and Push

```bash
git add content/
git commit -m "Add [lesson title]"
git push
```

### Step 4: Load on VM

```bash
git pull
python load_all_lessons.py
```

Or for force reload:
```bash
python force_load_domain.py [domain]
```

---

## Tips for Best Results with ChatGPT

1. **Be specific**: Give exact domain, difficulty, and concepts
2. **Request real examples**: Ask for "real company case studies with dates and dollar amounts"
3. **Emphasize length**: Remind it "4,000-5,500 words total"
4. **Request hands-on**: "Include a complete hands-on lab with commands and expected output"
5. **Check JSON validity**: Ask ChatGPT to "validate the JSON has no syntax errors"

## Common Fixes Needed After Generation

ChatGPT might make these mistakes:

### Fix 1: Invalid Jim Kwik Principles
❌ Bad: `"spaced_repetition"`, `"visualization"`
✅ Good: `"learning_sprint"`, `"memory_hooks"`

### Fix 2: Missing Fields
Add if missing:
- `question_id` (UUID)
- `type` field in post_assessment
- `difficulty` in post_assessment

### Fix 3: Invalid Content Types
❌ Bad: `"concept_deep_dive"`, `"step_by_step_guide"`
✅ Good: `"explanation"`, `"code_exercise"`

### Fix 4: Estimated Time
Must be ≤ 60 minutes

---

## Batch Creation Strategy

Create lessons in batches of 3-5:

1. **Plan the batch**: Decide on 3-5 related lessons
2. **Generate sequentially**: Create lesson 1, review, then lesson 2, etc.
3. **Validate batch**: Run `comprehensive_fix.py` on all
4. **Test load**: Load on VM with `force_load_domain.py`
5. **Commit batch**: Single commit with all 3-5 lessons

This approach ensures consistency and makes review easier.

---

## Need Help?

- Review existing rich lessons in `content/` for examples
- Check [CLAUDE.md](CLAUDE.md) for all lesson requirements
- Run `python comprehensive_fix.py` to auto-fix validation errors
- Use `diagnose_osint.py` to check for UUID conflicts

---

**Save this file and reference it each time you create lessons with ChatGPT!**
