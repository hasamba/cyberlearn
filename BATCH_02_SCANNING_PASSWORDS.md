# ChatGPT Prompt: Batch 2 - Vulnerability Scanning & Password Attacks (4 lessons)

Copy this entire prompt into ChatGPT to generate 4 lessons on vulnerability scanning and password attacks.

---

# LESSON CREATION REQUEST: Vulnerability Scanning & Password Attacks (4 Lessons)

Generate 4 pentest lessons following the exact structure from BATCH_01_WEB_TESTING.md.

## Lessons to Create:

### Lesson 15: Vulnerability Scanning with Nessus
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 15 | **Time**: 50min
**Prerequisites**: []

**Concepts**: Nessus architecture, credentialed vs non-credentialed scans, scan policy configuration, vulnerability prioritization (CVSS scoring), false positive identification, integration with other tools, custom scan policies, compliance scanning

**Content Focus**: Professional vulnerability scanning, interpreting scan results, prioritizing findings, reducing false positives, integrating into pentest workflow. Real-world: Enterprise vulnerability management program.

**File name**: `lesson_pentest_15_nessus_vulnerability_scanning_RICH.json`

---

### Lesson 16: Nmap Scripting Engine (NSE) for Vulnerability Detection
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 16 | **Time**: 55min
**Prerequisites**: []

**Concepts**: NSE script categories (vuln, exploit, discovery, auth, brute), common vulnerability detection scripts, custom NSE script development basics, authentication bypass scripts, service-specific enumeration, script optimization, chaining multiple scripts, output parsing

**Content Focus**: Advanced Nmap NSE for vulnerability detection, writing custom scripts, automating enumeration. Hands-on: Run vuln scripts, create custom NSE script. Real-world: NSE scripts that discovered critical vulnerabilities.

**File name**: `lesson_pentest_16_nmap_nse_vulnerability_detection_RICH.json`

---

### Lesson 17: Password Attacks: Network Services & Hash Cracking
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 17 | **Time**: 60min
**Prerequisites**: []

**Concepts**: Network service brute forcing (SSH, RDP, SMB, FTP), Hydra/Medusa/Ncrack usage, wordlist generation (CeWL, crunch, maskprocessor), rule-based attacks with Hashcat, hash identification (hash-identifier, hashid), GPU-accelerated cracking, password spray attacks, rate limiting and detection avoidance

**Content Focus**: Comprehensive password attack methodology covering network services, hash cracking with Hashcat, wordlist generation, rule-based attacks. Hands-on: Crack NTLM hashes, brute force SSH. Real-world: Time to crack different hash types.

**File name**: `lesson_pentest_17_password_attacks_hash_cracking_RICH.json`

---

### Lesson 18: Working with Password Hashes: NTLM, Net-NTLMv2, and Relay Attacks
**Domain**: pentest | **Difficulty**: 3 | **Order Index**: 18 | **Time**: 60min
**Prerequisites**: ["pentest_17"]

**Concepts**: NTLM vs Net-NTLMv2 authentication, hash extraction from Windows (Mimikatz, secretsdump), Pass-the-Hash attacks, NTLM relay attacks with Responder + ntlmrelayx, SMB relay attack chains, LDAP and HTTP relay, relay mitigation and detection, cracking vs passing hashes

**Content Focus**: Deep dive into NTLM authentication weaknesses, hash extraction, pass-the-hash, relay attacks, complete attack chains for domain compromise. Hands-on: Capture and relay NTLM hashes. Real-world: NTLM relay attacks in APT campaigns.

**File name**: `lesson_pentest_18_ntlm_hashes_relay_attacks_RICH.json`

---

## Requirements (Same as Batch 1):
- 4,000-5,500 words per lesson
- All content blocks: mindset_coach, explanation, video, code_exercise, real_world, memory_aid, reflection
- 2 post-assessment questions per lesson
- Valid content types and Jim Kwik principles only
- New UUIDs for all lesson_id and question_id fields
- Real company names, CVE numbers, specific tools and commands
- YouTube video URLs for each lesson

**START GENERATING**: Create all 4 lessons as complete JSON files.
