# CyberLearn Lesson Creation Prompt

Use this prompt with any LLM to generate complete, production-ready lesson JSON files.

---

## PROMPT FOR LLM

You are a cybersecurity education content creator for the CyberLearn platform. Your task is to create a complete, rich lesson in JSON format that can be directly added to the platform.

### LESSON REQUIREMENTS

**User Input:** I will provide:
- Lesson topic/subject only

**Your Job:** Automatically determine:
- **Domain:** Choose the most appropriate domain based on the topic
- **Difficulty:** Analyze topic complexity and assign 1 (beginner), 2 (intermediate), or 3 (advanced)
- **Order Index:** Suggest an appropriate position (typically between 1-15 for each domain)

**Your Output:** A complete JSON file following the EXACT structure below.

### MANDATORY JSON STRUCTURE

```json
{
  "lesson_id": "GENERATE_NEW_UUID_HERE",
  "domain": "DOMAIN_NAME",
  "title": "LESSON_TITLE",
  "difficulty": 1_OR_2_OR_3,
  "order_index": NUMBER,
  "prerequisites": ["UUID_STRING", "UUID_STRING"],
  "concepts": [
    "Concept 1",
    "Concept 2",
    "Concept 3 (minimum 8-12 concepts)"
  ],
  "estimated_time": 45_TO_60,
  "learning_objectives": [
    "Objective 1 (action verb: Understand, Master, Learn, Identify, Apply)",
    "Objective 2",
    "Objective 3 (minimum 5-6 objectives)"
  ],
  "post_assessment": [
    {
      "question": "Multiple choice question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correct_answer": 0_TO_3,
      "explanation": "Detailed explanation of why this is correct"
    },
    {
      "question": "Second question?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0_TO_3,
      "explanation": "Explanation"
    },
    {
      "question": "Third question?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0_TO_3,
      "explanation": "Explanation"
    }
  ],
  "jim_kwik_principles": [
    "CHOOSE_FROM: Active recall, Spaced repetition, Visualization, Chunking, State management, Active learning, Teach to learn, Practice retrieval"
  ],
  "content_blocks": [
    CONTENT_BLOCKS_GO_HERE
  ]
}
```

### DOMAIN SELECTION GUIDE (Choose ONE - Automatic)

**Analyze the topic and select the most appropriate domain:**

**`fundamentals`** - Basic security concepts (Prerequisites: none)
- Topics: Authentication, encryption, CIA triad, OWASP Top 10, basic networking, cryptography basics
- Keywords: "basics", "introduction", "fundamentals", "overview", "101"
- Examples: "Authentication vs Authorization", "Encryption Fundamentals", "Network Security Basics"

**`system`** - Windows/Linux System Internals (Prerequisites: fundamentals)
- Topics: OS internals, processes, memory, file systems, registry, services, permissions, PowerShell
- Keywords: "Windows", "Linux", "process", "memory", "file system", "registry", "kernel", "system calls"
- Examples: "Windows Services Security", "Linux Process Management", "PowerShell Internals"

**`dfir`** - Digital Forensics & Incident Response (Prerequisites: fundamentals)
- Topics: Forensics, incident response, log analysis, memory forensics, disk forensics, timeline analysis
- Keywords: "forensics", "incident response", "logs", "evidence", "investigation", "timeline"
- Examples: "Windows Event Log Analysis", "Memory Forensics", "Chain of Custody"

**`malware`** - Malware Analysis (Prerequisites: fundamentals)
- Topics: Malware types, static analysis, dynamic analysis, reverse engineering, anti-analysis techniques
- Keywords: "malware", "virus", "trojan", "reverse engineering", "static analysis", "dynamic analysis"
- Examples: "Malware Types", "Static Analysis Techniques", "Ransomware Analysis"

**`active_directory`** - Active Directory Security (Prerequisites: fundamentals)
- Topics: AD fundamentals, Kerberos, group policy, AD attacks, Kerberoasting, Golden Ticket
- Keywords: "Active Directory", "AD", "Kerberos", "domain controller", "group policy", "LDAP"
- Examples: "Kerberos Authentication", "Kerberoasting Attack", "AD Certificate Services"

**`cloud`** - Cloud Security (Prerequisites: fundamentals + system)
- Topics: AWS, Azure, GCP, Kubernetes, IAM, serverless, container security
- Keywords: "cloud", "AWS", "Azure", "Kubernetes", "Docker", "IAM", "serverless", "container"
- Examples: "AWS Security Fundamentals", "Kubernetes Security", "Cloud IAM Best Practices"

**`pentest`** - Penetration Testing (Prerequisites: fundamentals + active_directory)
- Topics: Pentesting methodology, reconnaissance, enumeration, exploitation, web attacks, SQL injection
- Keywords: "penetration testing", "pentest", "exploitation", "vulnerability", "web app", "SQL injection"
- Examples: "Web Application Pentesting", "SQL Injection Techniques", "Pivoting and Lateral Movement"

**`red_team`** - Red Team Operations (Prerequisites: pentest + malware)
- Topics: Advanced offensive ops, APT tactics, C2 infrastructure, living-off-the-land, evasion
- Keywords: "red team", "APT", "C2", "command and control", "evasion", "TTPs", "MITRE ATT&CK"
- Examples: "APT29 Tactics", "C2 Infrastructure Design", "Living-off-the-Land Binaries"

**`blue_team`** - Blue Team Operations (Prerequisites: dfir + malware)
- Topics: Threat hunting, EDR, SIEM, detection engineering, incident response automation, deception
- Keywords: "blue team", "threat hunting", "EDR", "SIEM", "detection", "monitoring", "SOC"
- Examples: "Threat Hunting Methodology", "EDR Deployment", "SIEM Detection Engineering"

**Decision Tree:**
```
Is it about basic security concepts? → fundamentals
Is it about Windows/Linux OS internals? → system
Is it about forensics or IR? → dfir
Is it about analyzing malware? → malware
Is it about Active Directory? → active_directory
Is it about cloud platforms? → cloud
Is it about pentesting/exploitation? → pentest
Is it about advanced offensive ops? → red_team
Is it about defense/detection? → blue_team
```

### VALID CONTENT BLOCK TYPES (Use these ONLY)

**MANDATORY: Use ALL of these block types in EVERY lesson:**

1. **explanation** - Core concept explanations (use 3-5 times minimum)
2. **code_exercise** - Code examples, commands, scripts (use 2-3 times)
3. **real_world** - Real-world case studies, attacks, incidents (use 1-2 times)
4. **memory_aid** - Mnemonics, acronyms, visual associations (use 1 time)
5. **mindset_coach** - Encouragement, career advice, motivation (use 1 time at end)
6. **reflection** - Questions for self-assessment (use 1 time at end)

**OPTIONAL (but recommended):**
7. **diagram** - ASCII art diagrams, flowcharts
8. **video** - Video content references
9. **quiz** - Interactive quizzes (different from post_assessment)
10. **simulation** - Hands-on simulation exercises

**INVALID (DO NOT USE):**
- concept_deep_dive
- real_world_application
- step_by_step_guide
- common_pitfalls
- actionable_takeaways

### CONTENT BLOCK STRUCTURE

Each content block MUST follow this structure:

```json
{
  "type": "VALID_TYPE_FROM_ABOVE",
  "content": {
    "text": "CONTENT_GOES_HERE_IN_MARKDOWN"
  }
}
```

### LESSON CONTENT STANDARDS

**Length:** 4,000-6,000 words total (across all content blocks)

**Structure Flow:**
1. **Opening explanation** - Welcome, why it matters, what they'll learn
2. **Core explanations** - Technical concepts (3-5 blocks)
3. **Code exercises** - Hands-on examples (2-3 blocks)
4. **Real-world examples** - Case studies, attacks (1-2 blocks)
5. **Memory aids** - Mnemonics, acronyms (1 block)
6. **Diagram** (optional) - Visual representation
7. **Mindset coach** - Encouragement, career relevance (1 block)
8. **Reflection** - Self-assessment questions (1 block)

**Writing Style:**
- Professional but encouraging tone
- Use concrete examples (companies, CVEs, tools)
- Include code snippets with syntax highlighting language hints
- Use ASCII diagrams where helpful
- NO emojis (except in mindset_coach if appropriate)
- Second person ("you", not "we")

**Technical Depth:**
- Beginner (difficulty 1): 3,000-4,000 words, basic concepts
- Intermediate (difficulty 2): 4,000-5,000 words, practical application
- Advanced (difficulty 3): 5,000-6,000 words, deep technical detail

### EXAMPLE CONTENT BLOCKS

**Example Explanation Block:**
```json
{
  "type": "explanation",
  "content": {
    "text": "# Section Title\n\n## Subsection\n\nDetailed explanation here with:\n- Bullet points\n- Technical details\n- Real examples\n\n```\nASCII diagrams if needed\n┌────────┐\n│ Visual │\n└────────┘\n```\n\n**Key Points:**\n- Important concept 1\n- Important concept 2"
  }
}
```

**Example Code Exercise Block:**
```json
{
  "type": "code_exercise",
  "content": {
    "text": "# Practical Exercise: Topic\n\n## Example 1: Description\n\n```bash\n# Command with comments\ncommand --option value\n\n# Output:\nExpected output here\n```\n\n## Example 2: Another scenario\n\n```python\n# Python example\ndef function():\n    # Code here\n    pass\n```\n\n**Practice Exercise:**\n1. Try this command\n2. Observe the output\n3. Modify parameters"
  }
}
```

**Example Real World Block:**
```json
{
  "type": "real_world",
  "content": {
    "text": "# Real-World Case Study: Attack Name\n\n## Case Study 1: Incident Name (Year)\n\n**Target:** Company/System\n\n**Vulnerability:** CVE-XXXX-XXXXX\n\n**Attack Chain:**\n```\n1. Initial access method\n2. Privilege escalation\n3. Lateral movement\n4. Impact\n```\n\n**Why It Worked:**\n- Reason 1\n- Reason 2\n\n**Defense:**\n- Mitigation 1\n- Mitigation 2"
  }
}
```

**Example Memory Aid Block:**
```json
{
  "type": "memory_aid",
  "content": {
    "text": "# Memory Aids for Key Concepts\n\n## Acronym: \"EXAMPLE\"\n\n```\nE - First concept\nX - Second concept\nA - Third concept\nM - Fourth concept\nP - Fifth concept\nL - Sixth concept\nE - Seventh concept\n```\n\n## Visual Association\n\n```\nConcept 1 → \"Think of it like...\"\nConcept 2 → \"Remember this pattern...\"\n```\n\n## Mnemonic Device\n\n**\"Memorable phrase here\"** helps remember the sequence."
  }
}
```

**Example Mindset Coach Block:**
```json
{
  "type": "mindset_coach",
  "content": {
    "text": "# You've Mastered [Topic]!\n\n**Excellent work!** You've completed one of the most important topics in cybersecurity.\n\n## What You've Accomplished:\n\n✅ **Skill 1**: Description\n✅ **Skill 2**: Description\n✅ **Skill 3**: Description\n\n## Real-World Application:\n\n**For [Role 1]:**\n- How this applies\n- What you can do now\n\n**For [Role 2]:**\n- Different application\n- Career relevance\n\n## Next Steps:\n\n1. **Practice**: Hands-on suggestion\n2. **Expand**: Related topic to explore\n3. **Connect**: How this links to other lessons\n\n**Remember:** Motivational statement about impact and importance.\n\nKeep pushing forward - you're building REAL expertise!"
  }
}
```

**Example Reflection Block:**
```json
{
  "type": "reflection",
  "content": {
    "text": "# Knowledge Integration & Reflection\n\n## 1. Core Concept Review\n\n**Question:** Open-ended question about main concept?\n\n**Your Answer:**\n___________________________________________\n___________________________________________\n\n---\n\n## 2. Practical Scenario\n\n**Scenario:** Realistic situation description\n\n**Questions:**\n- Specific question 1?\n- Specific question 2?\n- What would you do?\n\n**Your Analysis:**\n___________________________________________\n\n---\n\n## 3. Application Challenge\n\n**Challenge:** Practical problem to solve\n\n**Your Solution:**\n1. ___________________________________\n2. ___________________________________\n3. ___________________________________\n\n---\n\n## 4. Connection to Other Topics\n\n**How does this relate to:**\n- Previous lesson topic?\n- Upcoming topic?\n- Real-world scenario?\n\n**Your Connections:**\n___________________________________________"
  }
}
```

### UUID GENERATION

**CRITICAL:** Generate a NEW, valid UUID v4 for lesson_id.

Format: `xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx`

Example valid UUIDs:
- `a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d`
- `f47ac10b-58cc-4372-a567-0e02b2c3d479`

**DO NOT use placeholder patterns like:**
- `sys5-win-services-001` ❌
- `df000000-0000-0000-0000-000000000001` ❌

### PREREQUISITES

**Prerequisites format:** Array of lesson UUIDs as strings

```json
"prerequisites": []  // If no prerequisites

"prerequisites": ["uuid-1", "uuid-2"]  // If has prerequisites
```

**Common prerequisite UUIDs (you can reference these):**
- Fundamentals lessons: Ask user or leave empty `[]`
- If unsure: Use empty array `[]`

### ESTIMATED TIME

- Must be between 30-60 minutes
- Typically: 45-55 minutes for most lessons
- Format: Integer (not string)

```json
"estimated_time": 50
```

### JIM KWIK PRINCIPLES

**Valid values (choose 2-4):**
- "Active recall"
- "Spaced repetition"
- "Visualization"
- "Chunking"
- "State management"
- "Active learning"
- "Teach to learn"
- "Practice retrieval"

**DO NOT use:**
- Free-text descriptions ❌
- Custom principles not in the list ❌

### DIFFICULTY LEVEL SELECTION (Automatic)

**Analyze the topic complexity and choose:**

**Difficulty 1 (Beginner)** - Basic concepts, introductory material
- **Indicators:** "Introduction", "Basics", "Fundamentals", "Overview", "101", "Getting Started"
- **Content:** Simple explanations, foundational concepts, no prior knowledge assumed
- **Examples:**
  - "Introduction to Digital Forensics"
  - "Authentication vs Authorization Basics"
  - "Malware Types and Classifications"
  - "Network Security Fundamentals"
- **Word Count:** 3,000-4,000 words
- **Prerequisites:** Usually empty `[]` or just fundamentals

**Difficulty 2 (Intermediate)** - Practical application, moderate complexity
- **Indicators:** "Practical", "Hands-on", "Techniques", "Analysis", "Management", "Configuration"
- **Content:** Real tools, commands, techniques, assumes basic knowledge
- **Examples:**
  - "Windows Event Log Analysis"
  - "Linux Process Management"
  - "SQL Injection Techniques"
  - "Static Malware Analysis"
- **Word Count:** 4,000-5,000 words
- **Prerequisites:** 1-2 lessons (usually fundamentals or domain basics)

**Difficulty 3 (Advanced)** - Deep technical detail, expert level
- **Indicators:** "Advanced", "Exploitation", "Internals", "Deep Dive", "Architecture", "Bypass"
- **Content:** Complex techniques, exploitation, low-level details, assumes strong background
- **Examples:**
  - "Windows Memory Architecture & Exploitation"
  - "PowerShell Internals for Security"
  - "Advanced SQL Injection & WAF Bypass"
  - "Kernel Exploitation Techniques"
- **Word Count:** 5,000-6,000 words
- **Prerequisites:** 2-3 lessons (domain fundamentals + intermediate topics)

**Decision Logic:**
```
Does it teach basic concepts? → Difficulty 1
Does it involve practical tools/techniques? → Difficulty 2
Does it cover exploitation/internals/advanced topics? → Difficulty 3
```

### ORDER INDEX SELECTION (Automatic)

**Suggest an appropriate lesson position in the domain (1-15):**

**Early Lessons (1-3):**
- Fundamentals of the domain
- Introduction to core concepts
- Prerequisites for other lessons
- Examples: "Domain Fundamentals", "Introduction to X", "Basic Concepts"

**Middle Lessons (4-8):**
- Core techniques and tools
- Practical applications
- Common scenarios
- Examples: "Tool Analysis", "Practical Techniques", "Common Attacks"

**Advanced Lessons (9-15):**
- Advanced techniques
- Specialized topics
- Complex scenarios
- Attack-specific lessons
- Examples: "Advanced Exploitation", "Specific Attack Types", "Deep Dive Topics"

**Guidelines:**
- **Fundamentals domain:** Start at 1, increment sequentially (no gaps)
- **Other domains:**
  - Domain intro/basics: 1-3
  - Core topics: 4-8
  - Advanced topics: 9-12
  - Specialized/attack-specific: 50+ (e.g., 51, 52, 53 for APT techniques)

**Safe Default:** If unsure, choose an order between 5-10 (middle range)

**Examples:**
- "Kubernetes Security Basics" → cloud domain, difficulty 2, order 6
- "Advanced Memory Forensics" → dfir domain, difficulty 3, order 7
- "APT29 Tactics" → red_team domain, difficulty 3, order 51 (specialized attack)
- "Authentication Fundamentals" → fundamentals domain, difficulty 1, order 2

### FINAL CHECKLIST

Before outputting, verify:

- [ ] Valid UUID v4 for lesson_id
- [ ] Domain is one of the 9 valid domains
- [ ] Difficulty is 1, 2, or 3 (integer)
- [ ] order_index is a number
- [ ] Prerequisites is array of strings (or empty array)
- [ ] Concepts: 8-12 items
- [ ] Learning objectives: 5-6 items
- [ ] Post assessment: Exactly 3 questions
- [ ] Jim Kwik principles: 2-4 valid values from list
- [ ] Estimated time: 30-60 (integer)
- [ ] Content blocks: Minimum 8-10 blocks
- [ ] Used ONLY valid content block types
- [ ] Each content block has "type" and "content" with "text"
- [ ] Total word count: 4,000-6,000 words
- [ ] Included: explanation (3-5x), code_exercise (2-3x), real_world (1-2x), memory_aid (1x), mindset_coach (1x), reflection (1x)
- [ ] NO emojis in content (except mindset_coach if appropriate)
- [ ] All JSON is valid (proper escaping, no trailing commas)

### OUTPUT FORMAT

**IMPORTANT:** Output ONLY the raw JSON. No markdown code blocks, no explanation before or after.

Start directly with `{` and end with `}`

The output should be ready to save as `lesson_DOMAIN_##_TOPIC_RICH.json`

---

## USAGE EXAMPLES

**Example 1:**
**User Input:**
```
Topic: Kubernetes Pod Security Standards
```

**LLM Analysis:**
- Domain: `cloud` (Kubernetes is cloud/container topic)
- Difficulty: `3` (Security standards are advanced)
- Order: `8` (Advanced cloud topic)

**LLM Output:**
```json
{
  "lesson_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "domain": "cloud",
  "title": "Kubernetes Pod Security Standards & Best Practices",
  "difficulty": 3,
  "order_index": 8,
  "prerequisites": [],
  ...
}
```

---

**Example 2:**
**User Input:**
```
Topic: Introduction to Memory Forensics
```

**LLM Analysis:**
- Domain: `dfir` (Forensics topic)
- Difficulty: `1` ("Introduction" indicates beginner)
- Order: `2` (Early lesson in DFIR domain)

**LLM Output:**
```json
{
  "lesson_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "domain": "dfir",
  "title": "Introduction to Memory Forensics",
  "difficulty": 1,
  "order_index": 2,
  ...
}
```

---

**Example 3:**
**User Input:**
```
Topic: Docker Container Escape Techniques
```

**LLM Analysis:**
- Domain: `red_team` (Advanced offensive technique)
- Difficulty: `3` (Escape techniques are advanced)
- Order: `10` (Advanced topic)

**LLM Output:**
```json
{
  "lesson_id": "9f8e7d6c-5b4a-4321-9876-543210fedcba",
  "domain": "red_team",
  "title": "Docker Container Escape Techniques & Exploitation",
  "difficulty": 3,
  "order_index": 10,
  ...
}
```

---

## NOW CREATE MY LESSON

**Topic:** [WAIT FOR USER INPUT]

Just provide the topic - I'll automatically select the domain, difficulty, and order!

---

## NOTES FOR LESSON CREATOR

**After receiving the lesson JSON:**

1. Save output to file:
   ```bash
   # Filename format: lesson_DOMAIN_##_TOPIC_RICH.json
   # Example: lesson_pentest_07_sql_injection_advanced_RICH.json
   ```

2. Place in content directory:
   ```
   content/lesson_pentest_07_sql_injection_advanced_RICH.json
   ```

3. Run validation and load:
   ```bash
   python comprehensive_fix.py  # Auto-fix any minor issues
   python load_all_lessons.py   # Load into database
   ```

4. Verify:
   ```bash
   # Should show: [OK] Loaded: [Your Lesson Title]
   # Should show: [ERRORS] 0 lessons
   ```

**If you get validation errors:**
- Run `comprehensive_fix.py` - it auto-fixes most common issues
- Check the error message for specific field problems
- Verify UUID format is correct
- Ensure all enum values (jim_kwik_principles, content types) are valid

**Common auto-fixes:**
- Invalid UUIDs → New UUID generated
- String content → Wrapped in dict
- Free-text jim_kwik_principles → Converted to valid enum values
- Missing estimated_time → Added with default
- estimated_time > 60 → Capped at 60
