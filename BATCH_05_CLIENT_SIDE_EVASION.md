# ChatGPT Prompt: Batch 5 - Client-Side Attacks & AV Evasion (2 lessons)

Copy this entire prompt into ChatGPT to generate 2 lessons on client-side attacks and antivirus evasion.

---

# LESSON CREATION REQUEST: Client-Side Attacks & Evasion (2 Lessons)

Generate 2 pentest lessons following the exact structure from BATCH_01_WEB_TESTING.md.

## Lessons to Create:

### Lesson 19: Client-Side Attacks: Microsoft Office & Windows Library Files
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 19 | **Time**: 55min
**Prerequisites**: []

**Concepts**: Malicious Office macros (VBA), DDE and DDEAUTO exploitation, OLE objects and embedded files, Windows Library Files (.library-ms), Shortcut file (.lnk) attacks, HTML Application (HTA) payloads, social engineering integration, delivery methods (email, USB, file shares), detection and mitigation

**Content Focus**: Modern client-side attack vectors focusing on Office documents, Windows library files, and other user-initiated payloads. Includes social engineering context and evasion techniques. Hands-on: Create malicious macro document, library file attack. Real-world: Client-side attacks in APT campaigns (APT29 using LNK files).

**File name**: `lesson_pentest_19_client_side_attacks_RICH.json`

---

### Lesson 20: Antivirus Evasion Techniques
**Domain**: pentest | **Difficulty**: 3 | **Order Index**: 20 | **Time**: 60min
**Prerequisites**: ["pentest_03"]

**Concepts**: AV detection mechanisms (signature, heuristic, behavioral, cloud-based), code obfuscation techniques, payload encoding and encryption, process injection methods (CreateRemoteThread, Process Hollowing, Reflective DLL Injection), AMSI bypass techniques, in-memory execution (PowerShell, C#), custom shellcode loaders (C, C++, Rust), testing payloads without burning them (private sandboxes)

**Content Focus**: Advanced AV evasion covering multiple detection bypass techniques, AMSI bypass, in-memory execution, custom shellcode loaders, operational testing without burning payloads. Hands-on: Create custom shellcode loader, bypass AMSI, test with Defender. Real-world: Evolution of AV evasion (from simple encoding to modern in-memory techniques).

**File name**: `lesson_pentest_20_antivirus_evasion_RICH.json`

---

## Requirements (Same as Batch 1):
- 4,000-5,500 words per lesson
- All content blocks: mindset_coach, explanation, video, code_exercise, real_world, memory_aid, reflection
- 2 post-assessment questions per lesson
- Valid content types and Jim Kwik principles only
- New UUIDs for all lesson_id and question_id fields
- Real attack examples, tools, and code snippets
- YouTube video URLs for relevant tutorials

**START GENERATING**: Create both lessons as complete JSON files.
