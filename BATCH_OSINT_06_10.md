# ChatGPT Prompt: OSINT Lessons 6-10 (5 lessons)

Copy and paste this entire prompt into ChatGPT to generate 5 OSINT lessons completing the domain.

---

# LESSON CREATION REQUEST: OSINT Domain Completion (5 Lessons)

You are creating **5 comprehensive OSINT lessons** for the CyberLearn adaptive learning platform. These lessons complete the OSINT domain, covering email intelligence, geolocation, relationship mapping, dark web monitoring, and automation.

## CRITICAL REQUIREMENTS

### Lesson Structure (MUST FOLLOW EXACTLY)

Each lesson MUST have this exact JSON structure:

```json
{
  "lesson_id": "[Generate new UUID v4]",
  "domain": "osint",
  "title": "[Lesson Title]",
  "difficulty": [2-3],
  "order_index": [6-10],
  "prerequisites": ["84542765-253e-4b68-b230-3abfb6d16f54"],
  "concepts": [
    "[Concept 1]",
    "[Concept 2]",
    ... (5-8 concepts)
  ],
  "estimated_time": [50-60],
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
      "difficulty": [2-3]
    },
    {
      "question_id": "[Generate UUID]",
      "type": "multiple_choice",
      "question": "[Another scenario-based question]",
      "options": ["[A]", "[B]", "[C]", "[D]"],
      "correct_answer": [0-3],
      "explanation": "[200-300 words]",
      "difficulty": [2-3]
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
- ✅ Real company names and case studies (Bellingcat, APT investigations, etc.)
- ✅ Actual OSINT examples with dates and specific incidents
- ✅ Tool commands and examples (bash, Python scripts)
- ✅ Screenshots descriptions or ASCII art for workflows
- ✅ Memory aids and mnemonics
- ✅ Common mistakes OSINT practitioners make
- ✅ Actionable takeaways and workflows
- ✅ YouTube video embed (real OSINT tutorials)
- ✅ Hands-on exercises with step-by-step instructions
- ✅ Legal and ethical considerations
- ✅ Markdown formatting (##, ###, bullet points, code blocks)

---

## LESSONS TO CREATE (5 Total)

### Lesson 6: Email & Username Intelligence
**Domain**: osint
**Difficulty**: 2
**Order Index**: 6
**Estimated Time**: 50 minutes
**Prerequisites**: ["84542765-253e-4b68-b230-3abfb6d16f54"]

**Concepts** (include these):
- Email format enumeration and validation
- Username OSINT across multiple platforms
- Have I Been Pwned (HIBP) integration
- Email header analysis for tracking
- Disposable email detection
- Professional email intelligence gathering
- Email permutation and guessing
- Data breach correlation

**Content Focus**:
- Complete email OSINT methodology from discovery to verification
- Tools: Hunter.io, RocketReach, Sherlock, WhatsMyName, Namechk, holehe
- Hands-on: Find all email addresses for a target organization
- Email header analysis: tracking email origins and routes
- Real-world: Phishing campaign reconnaissance case study (with company names)
- Username correlation across platforms (Instagram, Twitter, GitHub, LinkedIn)
- Memory aid: "HEUS" mnemonic (Hunter, Email headers, Username search, Sherlock)
- Ethical considerations: Privacy boundaries and legal frameworks

**File name**: `lesson_osint_06_email_username_intelligence_RICH.json`

---

### Lesson 7: Image & Geolocation Intelligence
**Domain**: osint
**Difficulty**: 2
**Order Index**: 7
**Estimated Time**: 55 minutes
**Prerequisites**: ["84542765-253e-4b68-b230-3abfb6d16f54"]

**Concepts** (include these):
- EXIF metadata extraction and analysis
- Reverse image search techniques
- Geolocation from photographs
- Google Earth Pro for OSINT
- Shadow analysis and sun position calculation
- Social media geolocation
- Landmark and terrain identification
- Image forensics and manipulation detection

**Content Focus**:
- Comprehensive image intelligence gathering methodology
- Tools: ExifTool, Google Lens, TinEye, Yandex Images, InVID, FotoForensics
- Hands-on: Geolocate a photograph using multiple techniques
- Shadow analysis: Using SunCalc and shadow direction to determine time/location
- Real-world: Bellingcat geolocation investigations (MH17, Syria conflict analysis)
- Social media image intelligence (Instagram geotags, Twitter media)
- Detecting image manipulation and deepfakes
- Memory aid: "GIRL" mnemonic (Google reverse search, Image metadata, Reverse search engines, Landmarks)

**File name**: `lesson_osint_07_image_geolocation_intelligence_RICH.json`

---

### Lesson 8: Maltego & Relationship Mapping
**Domain**: osint
**Difficulty**: 3
**Order Index**: 8
**Estimated Time**: 60 minutes
**Prerequisites**: ["84542765-253e-4b68-b230-3abfb6d16f54"]

**Concepts** (include these):
- Maltego fundamentals and interface
- Entity types and transforms
- Infrastructure relationship mapping
- Domain and IP correlation
- Social network analysis
- Custom transform development
- Graph analysis techniques
- Data visualization for OSINT
- Export and reporting workflows

**Content Focus**:
- Complete Maltego workflow from setup to advanced analysis
- Entity relationships: Domains → IPs → Emails → People → Organizations
- Built-in transforms: DNS, WHOIS, social media, email
- Hands-on: Complete infrastructure investigation lab (map entire organization)
- Real-world: APT infrastructure mapping (Lazarus Group, APT29 infrastructure)
- Custom transform creation for specific OSINT needs
- Alternative tools: Spiderfoot, Recon-ng comparison
- Memory aid: "MAGIC" mnemonic (Map entities, Analyze transforms, Graph relationships, Investigate correlations, Correlate findings)

**File name**: `lesson_osint_08_maltego_relationship_mapping_RICH.json`

---

### Lesson 9: Dark Web & Paste Site Monitoring
**Domain**: osint
**Difficulty**: 3
**Order Index**: 9
**Estimated Time**: 60 minutes
**Prerequisites**: ["84542765-253e-4b68-b230-3abfb6d16f54"]

**Concepts** (include these):
- Tor Browser setup and safety protocols
- Dark web search engines
- Underground forum research
- Paste site monitoring
- Breach monitoring and data leak detection
- OPSEC for dark web research
- Legal and ethical boundaries
- Threat intelligence from dark web
- Credential leak detection

**Content Focus**:
- Safe dark web research methodology with strong OPSEC
- Tools: Tor Browser, Ahmia, Torch, OnionScan, PasteBin monitors
- Dark web search engines and .onion services
- Hands-on: Monitor paste sites for organizational leaks
- Real-world: Credential leak detection case studies (major breaches discovered via dark web)
- Underground forums: Research-only approach (no engagement)
- Legal framework: What's legal vs illegal in dark web research
- Automated monitoring: Scripts for paste site and breach monitoring
- Memory aid: "DROPS" mnemonic (Dark web, Research safely, OPSEC always, Paste sites, Safety first)

**File name**: `lesson_osint_09_dark_web_paste_monitoring_RICH.json`

---

### Lesson 10: OSINT Automation & Tool Integration
**Domain**: osint
**Difficulty**: 3
**Order Index**: 10
**Estimated Time**: 60 minutes
**Prerequisites**: ["84542765-253e-4b68-b230-3abfb6d16f54"]

**Concepts** (include these):
- Recon-ng framework mastery
- SpiderFoot automation platform
- TheHarvester for enumeration
- OSINT Framework overview
- Custom Python OSINT scripts
- API integration (Shodan, Hunter.io, VirusTotal, Censys)
- CI/CD for continuous OSINT monitoring
- Building OSINT dashboards
- Workflow automation and orchestration

**Content Focus**:
- Complete OSINT automation workflow from manual to fully automated
- Tools: Recon-ng, SpiderFoot, TheHarvester, OSINT Framework
- Hands-on: Build custom OSINT automation workflow with Python
- API integration: Shodan, VirusTotal, Hunter.io, Censys, URLScan.io
- Real-world: Automated threat intelligence pipeline (Fortune 500 company example)
- Custom Python OSINT scripts: Email enumeration, subdomain discovery
- Building dashboards: ELK Stack or Kibana for OSINT visualization
- Continuous monitoring: Scheduled scans and alerting
- Memory aid: "RAPID" mnemonic (Recon-ng, APIs, Python scripts, Integrate tools, Dashboards)

**File name**: `lesson_osint_10_automation_tool_integration_RICH.json`

---

## OUTPUT FORMAT

For each of the 5 lessons above, generate:

1. **Complete valid JSON file** following the exact structure
2. **4,000-5,500 words** of technical content per lesson
3. **All required content blocks** (mindset_coach, explanation, video, code_exercise, real_world, memory_aid, reflection)
4. **Real-world case studies** with specific organizations (Bellingcat, investigative journalism examples)
5. **Hands-on exercises** with complete commands and expected output
6. **YouTube video URLs** (real OSINT tutorials - Bellingcat, SANS, OSINT Curious)
7. **Memory aids and mnemonics**
8. **Two challenging post-assessment questions** per lesson
9. **Legal and ethical considerations** in each lesson

**IMPORTANT**:
- Generate NEW UUID v4 for each lesson_id and question_id
- Use ONLY the valid content types listed above
- Use ONLY the valid jim_kwik_principles listed above
- Ensure estimated_time is between 50-60 minutes
- Include proper markdown formatting (headers, code blocks, tables)
- Content must be in "text" key inside "content" object
- Prerequisites: Use ["84542765-253e-4b68-b230-3abfb6d16f54"] (OSINT lesson 1)
- Include ethical and legal considerations in every lesson

**ETHICAL FOCUS**:
All OSINT lessons must emphasize:
- Legal boundaries (CFAA, GDPR, privacy laws)
- Ethical research practices
- No unauthorized access or social engineering
- Responsible disclosure
- Privacy considerations

---

**START GENERATING NOW**: Please create all 5 complete lesson JSON files following the specifications above. Output each lesson as a complete, valid JSON file.
