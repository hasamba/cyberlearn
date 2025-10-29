# ChatGPT Prompt: Batch 1 - Web Application Testing (5 lessons)

Copy and paste this entire prompt into ChatGPT to generate 5 web application testing lessons.

---

# LESSON CREATION REQUEST: Web Application Testing (5 Lessons)

You are creating **5 comprehensive cybersecurity lessons** for the CyberLearn adaptive learning platform. These lessons cover web application penetration testing with Burp Suite, enumeration, and common web vulnerabilities.

## CRITICAL REQUIREMENTS

### Lesson Structure (MUST FOLLOW EXACTLY)

Each lesson MUST have this exact JSON structure:

```json
{
  "lesson_id": "[Generate new UUID v4]",
  "domain": "pentest",
  "title": "[Lesson Title]",
  "difficulty": [1-3],
  "order_index": [10-14],
  "prerequisites": [],
  "concepts": [
    "[Concept 1]",
    "[Concept 2]",
    ... (5-8 concepts)
  ],
  "estimated_time": [45-60],
  "learning_objectives": [
    "[Objective 1]",
    "[Objective 2]",
    ... (4-6 objectives)
  ],
  "content_blocks": [
    {
      "type": "mindset_coach",
      "content": {
        "text": "[300-500 words of encouragement and mindset coaching]"
      }
    },
    {
      "type": "explanation",
      "content": {
        "text": "[800-1200 words of deep technical content with markdown formatting]"
      }
    },
    {
      "type": "video",
      "content": {
        "text": "[Video URL with context and key takeaways, 50-100 words]"
      }
    },
    {
      "type": "explanation",
      "content": {
        "text": "[600-1000 words covering additional concepts]"
      }
    },
    {
      "type": "code_exercise",
      "content": {
        "text": "[800-1200 words hands-on lab with commands and expected output]"
      }
    },
    {
      "type": "real_world",
      "content": {
        "text": "[600-900 words real case study with company names and metrics]"
      }
    },
    {
      "type": "memory_aid",
      "content": {
        "text": "[400-600 words with mnemonics and quick reference]"
      }
    },
    {
      "type": "reflection",
      "content": {
        "text": "[300-500 words with reflection questions and career connections]"
      }
    }
  ],
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
      "explanation": "[200-300 word explanation]",
      "difficulty": [1-3]
    },
    {
      "question_id": "[Generate UUID]",
      "type": "multiple_choice",
      "question": "[Another scenario-based question]",
      "options": ["[A]", "[B]", "[C]", "[D]"],
      "correct_answer": [0-3],
      "explanation": "[200-300 words]",
      "difficulty": [1-3]
    }
  ],
  "jim_kwik_principles": [
    "active_learning",
    "meta_learning",
    "memory_hooks",
    "teach_like_im_10",
    "connect_to_what_i_know"
  ]
}
```

### VALID CONTENT BLOCK TYPES (ONLY USE THESE):
- `explanation`, `video`, `diagram`, `quiz`, `simulation`, `reflection`, `memory_aid`, `real_world`, `code_exercise`, `mindset_coach`

### VALID JIM KWIK PRINCIPLES (ONLY USE THESE):
- `active_learning`, `meta_learning`, `memory_hooks`, `minimum_effective_dose`, `teach_like_im_10`, `connect_to_what_i_know`, `reframe_limiting_beliefs`, `gamify_it`, `learning_sprint`, `multiple_memory_pathways`

### CONTENT QUALITY REQUIREMENTS

**Each lesson MUST include**:
- ✅ 4,000-5,500 words total content
- ✅ Real company names and case studies
- ✅ Actual attack examples with dates
- ✅ Code snippets with syntax highlighting (markdown code blocks)
- ✅ Commands for testing tools
- ✅ ASCII diagrams for attack flow
- ✅ Memory aids and mnemonics
- ✅ Common mistakes and how to avoid them
- ✅ Actionable takeaways
- ✅ YouTube video embed (find real relevant video)
- ✅ Hands-on exercises with expected output
- ✅ Markdown formatting (##, ###, bullet points, code blocks)

---

## LESSONS TO CREATE (5 Total)

### Lesson 10: Burp Suite Deep Dive for Web Application Testing
**Domain**: pentest
**Difficulty**: 2
**Order Index**: 10
**Estimated Time**: 60 minutes
**Prerequisites**: []

**Concepts** (include these):
- Burp Suite architecture and components (Proxy, Intruder, Repeater, Scanner)
- Intercepting and modifying HTTP/HTTPS requests
- Burp Intruder for automated fuzzing and brute force attacks
- Burp Repeater for manual request testing
- Burp Decoder, Comparer, and utility tabs
- Browser configuration and proxy setup
- Scope configuration and target mapping
- Extensions and BApp Store plugins

**Content Focus**:
- Complete Burp Suite workflow from setup to exploitation
- Hands-on labs: Intercept login, modify parameters, fuzz inputs
- Real-world: How bug bounty hunters use Burp Suite (HackerOne stats)
- Common Burp Suite workflows (SQLi testing, XSS detection, auth bypass)
- Integration with other tools (ffuf, sqlmap)
- Memory aid: "PIRDS" mnemonic (Proxy, Intruder, Repeater, Decoder, Scanner)

**File name**: `lesson_pentest_10_burp_suite_deep_dive_RICH.json`

---

### Lesson 11: Web Application Enumeration & Inspection
**Domain**: pentest
**Difficulty**: 2
**Order Index**: 11
**Estimated Time**: 50 minutes
**Prerequisites**: []

**Concepts** (include these):
- Browser Developer Tools mastery (Network, Console, Debugger tabs)
- Web application architecture analysis (frontend vs backend)
- Client-side vs server-side validation identification
- JavaScript analysis and deobfuscation techniques
- API endpoint discovery (hidden endpoints, GraphQL introspection)
- Hidden parameter enumeration (HTTP headers, cookies, local storage)
- Technology stack fingerprinting (Wappalyzer, BuiltWith, Whatweb)
- Sitemap generation and web crawling (Burp Spider, OWASP ZAP)

**Content Focus**:
- Systematic enumeration methodology before exploitation
- Hands-on: Analyze a modern web app (identify techs, find endpoints)
- Real-world: Enumeration that led to critical bug bounty findings
- Common mistakes: Skipping enumeration, missing hidden functionality
- Tools: Browser DevTools, Burp Suite, Wappalyzer, Whatweb
- Memory aid: "JATSE" mnemonic (JavaScript, APIs, Tech stack, Sitemap, Endpoints)

**File name**: `lesson_pentest_11_web_enumeration_inspection_RICH.json`

---

### Lesson 12: Directory Traversal Exploitation Playbook
**Domain**: pentest
**Difficulty**: 2
**Order Index**: 12
**Estimated Time**: 45 minutes
**Prerequisites**: ["pentest_10"]

**Concepts** (include these):
- Path traversal fundamentals (`../`, `..\\`, absolute paths)
- OS-specific path separators (Windows vs Linux)
- Filter bypass techniques (encoding, double encoding, null bytes, Unicode)
- Directory traversal in web apps vs REST APIs
- Common vulnerable parameters (file, path, page, template)
- Escalating directory traversal to RCE (log poisoning, session files)
- Automated scanning tools (dotdotpwn, OWASP ZAP)
- Real-world exploitation scenarios and payloads

**Content Focus**:
- Complete attack methodology from detection to exploitation
- Hands-on: Exploit path traversal to read `/etc/passwd`, `C:\Windows\win.ini`
- Bypass filters: URL encoding, double encoding, path normalization bypasses
- Real-world: CVEs involving directory traversal (with company names)
- Escalation: From file read to RCE via log poisoning
- Memory aid: "DECODE" mnemonic (Detect, Encode bypass, OS paths, Double encode, Escalate)

**File name**: `lesson_pentest_12_directory_traversal_RICH.json`

---

### Lesson 13: File Inclusion Vulnerabilities: LFI and RFI
**Domain**: pentest
**Difficulty**: 3
**Order Index**: 13
**Estimated Time**: 60 minutes
**Prerequisites**: ["pentest_10", "pentest_12"]

**Concepts** (include these):
- Local File Inclusion (LFI) fundamentals and exploitation
- Remote File Inclusion (RFI) attack chains
- PHP wrappers exploitation (php://filter, php://input, data://, expect://, phar://)
- Log poisoning for RCE (Apache, Nginx, SSH logs)
- Session file inclusion and manipulation
- Filter bypass techniques (null bytes, encoding, path truncation)
- LFI to RCE escalation paths (multiple techniques)
- Automated exploitation tools (Burp, LFISuite)

**Content Focus**:
- Advanced file inclusion exploitation with multiple RCE paths
- Hands-on: LFI → read source code with php://filter, RCE via log poisoning
- PHP wrapper abuse: Complete exploitation examples
- Real-world: LFI/RFI CVEs that led to major breaches
- Detection and exploitation workflow
- Memory aid: "PWLER" (PHP wrappers, Wrappers, Logs, Escalate, RFI)

**File name**: `lesson_pentest_13_file_inclusion_lfi_rfi_RICH.json`

---

### Lesson 14: File Upload Vulnerabilities: Complete Exploitation
**Domain**: pentest
**Difficulty**: 2
**Order Index**: 14
**Estimated Time**: 55 minutes
**Prerequisites**: ["pentest_10"]

**Concepts** (include these):
- Unrestricted file upload exploitation fundamentals
- MIME type validation bypass (Content-Type header manipulation)
- Extension filter bypass techniques (.php5, .phtml, .phar, .phps, case manipulation)
- Content validation bypass (magic bytes, polyglot files)
- Magic byte manipulation for file type spoofing
- Double extension attacks (.jpg.php, .php.jpg)
- Path traversal in file upload functionality
- Webshell deployment, obfuscation, and access

**Content Focus**:
- Systematic approach to bypassing upload restrictions
- Hands-on: Upload PHP webshell bypassing multiple protections
- Bypass techniques: MIME type, extensions, content filters, size limits
- Real-world: File upload vulnerabilities that led to full compromise
- Webshell deployment strategies and post-exploitation
- Memory aid: "MECDP" (MIME, Extensions, Content, Double extension, Path)

**File name**: `lesson_pentest_14_file_upload_vulnerabilities_RICH.json`

---

## OUTPUT FORMAT

For each of the 5 lessons above, generate:

1. **Complete valid JSON file** following the exact structure
2. **4,000-5,500 words** of technical content per lesson
3. **All required content blocks** (mindset_coach, explanation, video, code_exercise, real_world, memory_aid, reflection)
4. **Real-world case studies** with specific company names, CVE numbers, dates
5. **Hands-on exercises** with complete commands and expected output
6. **YouTube video URLs** (real, relevant videos - search for Burp Suite tutorials, LFI exploitation, etc.)
7. **Memory aids and mnemonics**
8. **Two challenging post-assessment questions** per lesson

**IMPORTANT**:
- Generate NEW UUID v4 for each lesson_id and question_id
- Use ONLY the valid content types listed above
- Use ONLY the valid jim_kwik_principles listed above
- Ensure estimated_time is between 45-60 minutes
- Include proper markdown formatting (headers, code blocks, tables)
- Content must be in "text" key inside "content" object
- Prerequisites can be empty array or reference earlier pentest lessons

---

**START GENERATING NOW**: Please create all 5 complete lesson JSON files following the specifications above. Output each lesson as a complete, valid JSON file.
