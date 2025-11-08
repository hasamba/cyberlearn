# Quick Start: Create a CyberLearn Lesson in 5 Minutes

## The Fastest Way to Create a Complete Lesson

### Step 1: Copy the Universal Prompt (30 seconds)

Open **[UNIVERSAL_RICH_LESSON_PROMPT.md](UNIVERSAL_RICH_LESSON_PROMPT.md)** and copy the entire file.

### Step 2: Customize Topic (30 seconds)

Replace these placeholders:
- `[LESSON_TOPIC]` → Your actual topic (e.g., "SQL Injection Attacks")
- `[DOMAIN]` → One of: fundamentals, dfir, malware, active_directory, system, cloud, pentest, red_team, blue_team, osint, threat_hunting, linux, ai_security, iot_security, web3_security
- `[DIFFICULTY]` → 1 (Beginner), 2 (Intermediate), or 3 (Advanced)
- `[ORDER_INDEX]` → Lesson number in sequence

**Example:**
```
Topic: SQL Injection Attacks
Domain: pentest
Difficulty: 2
Order Index: 42
```

### Step 3: Paste into AI (10 seconds)

Paste the customized prompt into:
- **Claude** → https://claude.ai
- **ChatGPT** → https://chat.openai.com (GPT-4 recommended)
- **Gemini** → https://gemini.google.com

### Step 4: Get Complete JSON (2-3 minutes)

The AI will generate a complete lesson JSON with:
- ✅ 4,000-15,000 words
- ✅ All 10 Jim Kwik principles implemented
- ✅ 12-15 content blocks
- ✅ Memory aids with mnemonics
- ✅ Hands-on exercises
- ✅ Assessment questions
- ✅ No placeholders

### Step 5: Save and Validate (1 minute)

```bash
# Save the JSON
# File: content/lesson_pentest_42_sql_injection_RICH.json

# Validate
python scripts/validate_lesson_compliance.py

# Check quality
python validate_content_quality.py
```

---

## What You Get

### Complete Lesson Structure
```json
{
  "lesson_id": "[Valid UUID v4]",
  "domain": "pentest",
  "title": "SQL Injection Attacks",
  "difficulty": 2,
  "estimated_time": 45,
  "order_index": 42,
  "prerequisites": ["uuid1", "uuid2"],
  "concepts": ["SQL injection", "Input validation", ...],
  "learning_objectives": [...],
  "post_assessment": [3-6 questions],
  "jim_kwik_principles": [All 10],
  "content_blocks": [12-15 blocks]
}
```

### 13 Content Blocks

1. **Opening Explanation** - Simple introduction with analogies
2. **Video Content** - Relevant YouTube link
3. **Technical Deep Dive** - 800-1500 words of detailed content
4. **Diagram** - ASCII art visualization
5. **Memory Aid** - Mnemonics and acronyms
6. **Hands-On Exercise** - Real commands and practice
7. **Real-World Case Study** - Actual incident/company
8. **Interactive Quiz** - Knowledge check questions
9. **Advanced Simulation** - Scenario-based lab
10. **Connection to Prior Knowledge** - Building on previous lessons
11. **Reflection** - Meta-learning prompts
12. **Mindset Coaching** - Encouragement and confidence building
13. **Next Steps Preview** - What's coming next

### All 10 Jim Kwik Principles

- ✅ `teach_like_im_10` - Simple analogies, no jargon
- ✅ `memory_hooks` - Mnemonics in memory_aid block
- ✅ `connect_to_what_i_know` - References prior lessons
- ✅ `active_learning` - code_exercise + simulation blocks
- ✅ `meta_learning` - reflection block
- ✅ `minimum_effective_dose` - 6-8 focused concepts
- ✅ `reframe_limiting_beliefs` - mindset_coach block
- ✅ `gamify_it` - Challenges and progression
- ✅ `learning_sprint` - 30-60 minute flow
- ✅ `multiple_memory_pathways` - Video + diagram + exercises

---

## Quality Checklist

After generating, verify:

- [ ] 4,000+ words total
- [ ] All 10 Jim Kwik principles listed
- [ ] Memory_aid block has actual mnemonic (not placeholder)
- [ ] Code_exercise has real commands
- [ ] No "[INSERT X]" or "TODO" placeholders
- [ ] Simple language with analogies
- [ ] Real-world examples with specific details
- [ ] Valid JSON syntax
- [ ] 3+ post-assessment questions

---

## Validation Commands

```bash
# Full validation
python scripts/validate_lesson_compliance.py

# Content quality check
python validate_content_quality.py

# Load into database
python load_all_lessons.py

# Test in app
streamlit run app.py
```

---

## Common Adjustments

### If Lesson is Too Short
Ask AI: "Expand each content block to 300-500 words"

### If Missing Required Block
Ask AI: "Add a memory_aid block with actual mnemonics"

### If Too Much Jargon
Ask AI: "Simplify language - teach like I'm 10. Add more analogies"

### If Needs More Examples
Ask AI: "Add 2-3 more real-world examples with company names"

---

## Example Topics by Domain

### Fundamentals
- "Authentication vs Authorization"
- "Cryptography Basics"
- "Zero Trust Architecture"

### DFIR
- "Memory Forensics with Volatility"
- "Timeline Analysis"
- "Network Packet Analysis"

### Malware
- "Static Analysis with IDA Pro"
- "Dynamic Analysis in Sandbox"
- "Ransomware Detection"

### Pentest
- "SQL Injection Attacks"
- "Cross-Site Scripting (XSS)"
- "API Security Testing"

### Red Team
- "C2 Framework Setup"
- "Phishing Campaign Development"
- "Physical Security Assessment"

### Blue Team
- "SIEM Configuration"
- "Incident Response Procedures"
- "Threat Hunting Techniques"

---

## Why This Method Works

**Speed:** 5 minutes vs. hours of manual writing

**Quality:** AI follows exact standards and requirements

**Completeness:** No placeholders - everything filled out

**Consistency:** Same structure every time

**Validation:** Passes all checks automatically

---

## Files You Need

1. **[UNIVERSAL_RICH_LESSON_PROMPT.md](UNIVERSAL_RICH_LESSON_PROMPT.md)** - Copy this
2. **[CLAUDE.md](CLAUDE.md)** - Reference for standards
3. **[JIM_KWIK_IMPLEMENTATION_GUIDE.md](JIM_KWIK_IMPLEMENTATION_GUIDE.md)** - Implementation checklist
4. **[HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md)** - Full guide

---

## Next Steps

1. **Create your first lesson** using this quick start
2. **Validate it** with the provided scripts
3. **Load it** into the database
4. **Test it** in the Streamlit app
5. **Iterate** based on feedback

---

**That's it!** You now have a complete, production-ready lesson in 5 minutes.

For more details, see [HOW_TO_ADD_NEW_LESSONS.md](HOW_TO_ADD_NEW_LESSONS.md).
