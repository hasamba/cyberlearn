# ChatGPT Prompt: Batch 3 - Metasploit Framework Mastery (4 lessons)

Copy this entire prompt into ChatGPT to generate 4 comprehensive Metasploit lessons.

---

# LESSON CREATION REQUEST: Metasploit Framework (4 Lessons)

Generate 4 pentest lessons following the exact structure from BATCH_01_WEB_TESTING.md.

## Lessons to Create:

### Lesson 21: Metasploit Fundamentals & Workspace Setup
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 21 | **Time**: 50min
**Prerequisites**: []

**Concepts**: Metasploit architecture (msfconsole, modules, handlers), workspace management, database integration (PostgreSQL), module types (exploit, auxiliary, post, payload, encoder, evasion), search and module selection, global and module-specific options, session management, basic exploitation workflow

**Content Focus**: Complete introduction to Metasploit Framework, architecture understanding, workspace organization, database integration, systematic exploitation workflow. Hands-on: Set up workspace, run exploit, manage sessions. Real-world: Metasploit in red team engagements.

**File name**: `lesson_pentest_21_metasploit_fundamentals_RICH.json`

---

### Lesson 22: Metasploit Payload Engineering
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 22 | **Time**: 55min
**Prerequisites**: ["pentest_21"]

**Concepts**: Payload types (singles, stagers, stages), Meterpreter vs shell payloads, multi-handler configuration, payload generation with msfvenom, custom payload templates, encoding and obfuscation (shikata_ga_nai), payload delivery mechanisms, handler management and session juggling

**Content Focus**: Deep dive into Metasploit payloads, msfvenom generation, encoding, delivery, handler setup, managing multiple sessions. Hands-on: Generate encoded payloads, set up handlers, manage sessions. Real-world: Payload detection rates and evasion.

**File name**: `lesson_pentest_22_metasploit_payload_engineering_RICH.json`

---

### Lesson 23: Metasploit Post-Exploitation Operations
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 23 | **Time**: 60min
**Prerequisites**: ["pentest_21", "pentest_22"]

**Concepts**: Meterpreter post-exploitation modules, credential harvesting (hashdump, mimikatz module), privilege escalation modules, persistence installation (registry, service, scheduled tasks), lateral movement through sessions, pivoting and port forwarding, evidence collection and exfiltration, session upgrade and migration

**Content Focus**: Comprehensive post-exploitation using Metasploit modules, Meterpreter commands, privilege escalation, persistence, lateral movement, pivoting. Hands-on: Full post-exploitation workflow from shell to domain admin. Real-world: APT groups using Metasploit.

**File name**: `lesson_pentest_23_metasploit_post_exploitation_RICH.json`

---

### Lesson 24: Automating Metasploit Engagements
**Domain**: pentest | **Difficulty**: 3 | **Order Index**: 24 | **Time**: 50min
**Prerequisites**: ["pentest_21", "pentest_22", "pentest_23"]

**Concepts**: Resource scripts (.rc files), automated exploitation chains, RPC API integration, Ruby scripting for custom modules, mass exploitation scenarios, automated post-exploitation, reporting automation, CI/CD integration for security testing

**Content Focus**: Advanced Metasploit automation using resource scripts, RPC API, custom Ruby modules, automated exploitation workflows for large-scale engagements. Hands-on: Create resource script, use RPC API. Real-world: Automated vulnerability validation in DevSecOps.

**File name**: `lesson_pentest_24_automating_metasploit_RICH.json`

---

## Requirements (Same as Batch 1):
- 4,000-5,500 words per lesson
- All content blocks: mindset_coach, explanation, video, code_exercise, real_world, memory_aid, reflection
- 2 post-assessment questions per lesson
- Valid content types and Jim Kwik principles only
- New UUIDs for all lesson_id and question_id fields
- Real tools, commands, and Metasploit module names
- YouTube video URLs for Metasploit tutorials

**START GENERATING**: Create all 4 lessons as complete JSON files.
