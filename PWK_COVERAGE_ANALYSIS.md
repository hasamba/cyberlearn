# PWK (PEN-200) Syllabus Coverage Analysis

## Summary

Based on the OffSec PEN-200 (PWK) syllabus and your current CyberLearn lessons, here's a comprehensive analysis of what's covered and what's missing.

**Total PWK Topics**: ~90 learning units across 20 modules
**Currently Covered**: ~40% (well covered in some areas, gaps in others)
**Recommended New Lessons**: 25-30 lessons

---

## Coverage by PWK Module

### ✅ WELL COVERED (80-100%)

#### 1. Introduction to Cybersecurity (100% covered)
**Your lessons**:
- Fundamentals: CIA Triad, Threat Landscape, Security Principles
- Already have: Threats and Threat Actors, Security Principles, Laws/Regulations

**PWK Topics**: Practice of Cybersecurity, Threats, CIA Triad, Security Principles, Laws
**Status**: ✅ Complete - No new lessons needed

#### 2. Active Directory (95% covered)
**Your lessons**:
- Active Directory Fundamentals, Kerberos, BloodHound
- Kerberoasting, Golden Ticket, Pass-the-Hash, DCSync
- AD CS Exploitation, Group Policy

**PWK Topics**: AD Enumeration, Authentication, Attacks, Lateral Movement, Persistence
**Status**: ✅ Nearly complete - Maybe add 1-2 advanced AD lessons

#### 3. Windows/Linux Privilege Escalation (90% covered)
**Your lessons**:
- Windows Privilege Escalation for Red Teams
- Linux has full coverage (13 lessons)
- System internals well covered

**PWK Topics**: Enumeration, Service Hijacking, Scheduled Tasks, SUID, Sudo abuse
**Status**: ✅ Well covered

---

### ⚠️ PARTIALLY COVERED (40-70%)

#### 4. Information Gathering (60% covered)
**Your lessons**:
- Reconnaissance Techniques (general)
- Active Information Gathering (pentest)
- OSINT basics exist

**PWK Topics Missing**:
- Passive vs Active Information Gathering (detailed comparison)
- DNS, SMB, SMTP, SNMP Enumeration (protocol-specific)
- Living off the Land reconnaissance
- Netcat and Nmap port scanning (detailed)

**Recommended New Lessons**: 3-4 lessons

#### 5. Web Application Assessment (65% covered)
**Your lessons**:
- Web Application Penetration Testing Fundamentals
- SQL Injection comprehensive
- XSS, File Upload, Command Injection
- OWASP Top 10

**PWK Topics Missing**:
- **Web Application Assessment Methodology** (specific PWK approach)
- **Burp Suite Deep Dive** (practical usage)
- **Web Application Enumeration** (headers, cookies, API testing)
- **Directory Traversal** (dedicated lesson)
- **File Inclusion Vulnerabilities** (LFI/RFI dedicated lesson)

**Recommended New Lessons**: 4-5 lessons

#### 6. Password Attacks (50% covered)
**Your lessons**:
- General password attacks mentioned in various lessons

**PWK Topics Missing**:
- **Attacking Network Service Logins** (SSH, RDP, HTTP POST)
- **Password Cracking Fundamentals** (methodology, wordlist mutation)
- **Working with Password Hashes** (NTLM, Net-NTLMv2, relay attacks)
- **Password Manager Key Files**
- **SSH Private Key Passphrase Cracking**

**Recommended New Lessons**: 3-4 lessons

#### 7. Metasploit Framework (40% covered)
**Your lessons**:
- Some Metasploit mentioned in existing lessons

**PWK Topics Missing**:
- **Getting Familiar with Metasploit** (setup, navigation, auxiliary modules)
- **Using Metasploit Payloads** (staged vs non-staged, Meterpreter)
- **Metasploit Post-Exploitation** (core features, modules, pivoting)
- **Automating Metasploit** (resource scripts)

**Recommended New Lessons**: 4 lessons

---

### ❌ MAJOR GAPS (0-30% coverage)

#### 8. Report Writing for Penetration Testers (10% covered)
**Your lessons**:
- None dedicated to pentest reporting

**PWK Topics Missing**:
- **Understanding Note-Taking** (deliverables, portability, structure)
- **Choosing Note-Taking Tools** (CherryTree, Obsidian, Joplin)
- **Taking Screenshots Effectively**
- **Writing Technical Reports** (structure, executive summary, technical findings)
- **Report Templates and Examples**

**Recommended New Lessons**: 2-3 lessons

#### 9. Effective Learning Strategies (5% covered)
**Your lessons**:
- Cybersecurity Orientation & Learning Gameplan (partial)

**PWK Topics Missing**:
- **Learning Theory** (memory mechanisms, dual encoding, forgetting curve)
- **Unique Challenges to Learning Technical Skills**
- **OffSec Methodology** (Demonstrative Methodology, Try Harder)
- **Tactics and Common Methods** (Retrieval Practice, Spaced Practice, SQ3R, PQ4R, Feynman, Leitner)
- **Exam Strategies** (dealing with stress, readiness, practical approach)
- **Practical Steps** (long-term strategy, time management, community)

**Recommended New Lessons**: 3-4 lessons (OPTIONAL - meta-learning)

#### 10. Vulnerability Scanning (20% covered)
**Your lessons**:
- Nessus and Nmap NSE mentioned briefly

**PWK Topics Missing**:
- **Vulnerability Scanning Theory** (types of scans, authenticated vs unauthenticated)
- **Vulnerability Scanning with Nessus** (installation, configuration, interpreting results, plugins)
- **Vulnerability Scanning with Nmap NSE** (NSE basics, custom scripts, lightweight scanning)

**Recommended New Lessons**: 2 lessons

#### 11. Client-Side Attacks (25% covered)
**Your lessons**:
- Client-Side Attacks & Social Engineering (general)

**PWK Topics Missing**:
- **Target Reconnaissance for Client-Side Attacks** (client fingerprinting)
- **Exploiting Microsoft Office** (macros, DDE, PPSX)
- **Abusing Windows Library Files** (.library-ms files)
- **Windows Shortcuts for Code Execution** (.lnk files)

**Recommended New Lessons**: 2-3 lessons

#### 12. Locating Public Exploits (30% covered)
**Your lessons**:
- Public Exploits: Finding, Fixing & Executing (partial)

**PWK Topics Missing**:
- **Online Exploit Resources** (ExploitDB, GitHub, Google dorking for exploits)
- **Offline Exploit Resources** (SearchSploit, Nmap NSE, exploit frameworks)
- **Analyzing Exploit Code** (understanding risk, reading code)
- **Complete Exploitation Workflow** (enumerate → find exploit → modify → execute)

**Recommended New Lessons**: 1-2 lessons

#### 13. Fixing Exploits (20% covered)
**Your lessons**:
- Mentioned in "Public Exploits" lesson

**PWK Topics Missing**:
- **Fixing Memory Corruption Exploits** (buffer overflow theory, cross-compilation)
- **Fixing Web Exploits** (common issues, troubleshooting)

**Recommended New Lessons**: 1-2 lessons

#### 14. Antivirus Evasion (10% covered)
**Your lessons**:
- Some mention in red team lessons

**PWK Topics Missing**:
- **AV Evasion Theory** (known vs unknown threats, AV components, detection engines)
- **AV Evasion in Practice** (manual evasion, automated tools, testing methodology)

**Recommended New Lessons**: 1-2 lessons

#### 15. Port Redirection and SSH Tunneling (15% covered)
**Your lessons**:
- Mentioned in red team/pentest lessons

**PWK Topics Missing**:
- **Port Forwarding with Linux Tools** (Socat, SSH local/dynamic/remote)
- **Port Forwarding with Windows Tools** (ssh.exe, Plink, Netsh)
- **SSH Tunneling Deep Dive** (all types: local, remote, dynamic)

**Recommended New Lessons**: 2 lessons

#### 16. Advanced Tunneling (5% covered)
**Your lessons**:
- Minimal coverage

**PWK Topics Missing**:
- **HTTP Tunneling** (Chisel)
- **DNS Tunneling** (dnscat2)
- **Tunneling Through Deep Packet Inspection**

**Recommended New Lessons**: 1 lesson

#### 17. Assembling the Pieces (0% covered)
**Your lessons**:
- None (this is PWK's capstone section)

**PWK Topics Missing**:
- **Public Network Enumeration Lab**
- **Attacking WEBSRV1** (WordPress exploitation)
- **Gaining Access to Internal Network** (phishing, validation)
- **Internal Network Enumeration**
- **Attacking INTERNALSRV1** (Kerberoasting, WordPress relay)
- **Gaining Access to Domain Controller**

**Recommended New Lessons**: 0 (these are lab scenarios, not lessons)

---

## Recommended New Lessons (Priority Order)

### 🔴 HIGH PRIORITY (Core PWK Skills)

#### Pentest Domain (add 10-12 lessons):

**1. Penetration Testing Report Writing**
- **Difficulty**: 2
- **Content**: Note-taking tools, screenshot tools, report structure, executive summary, technical findings, templates
- **Why**: Critical professional skill, PWK emphasizes this

**2. Burp Suite Deep Dive for Web Application Testing**
- **Difficulty**: 2
- **Content**: Proxy setup, intercepting requests, Repeater, Intruder, Scanner (Community), extensions, workflows
- **Why**: Essential web testing tool, heavily used in PWK

**3. Web Application Enumeration & Inspection**
- **Difficulty**: 2
- **Content**: Headers, cookies, source code inspection, API testing, debugging web apps
- **Why**: PWK has dedicated section, foundational for web testing

**4. Directory Traversal Exploitation Playbook**
- **Difficulty**: 2
- **Content**: Absolute/relative paths, encoding special characters, exploitation techniques, chaining with other vulns
- **Why**: Distinct from file inclusion, PWK has dedicated unit

**5. File Inclusion Vulnerabilities: LFI and RFI**
- **Difficulty**: 2-3
- **Content**: LFI vs directory traversal, code execution via LFI, PHP wrappers, RFI attacks, log poisoning
- **Why**: Critical web vuln, PWK dedicates significant content

**6. File Upload Vulnerabilities: Complete Exploitation**
- **Difficulty**: 2
- **Content**: Identifying uploads, bypassing restrictions (client/server), content-type manipulation, polyglot files, execution chains
- **Why**: Common vuln with many bypass techniques

**7. Vulnerability Scanning with Nessus**
- **Difficulty**: 1-2
- **Content**: Installation, scan types, configuration, authenticated scans, interpreting results, plugins, prioritization
- **Why**: Industry standard tool, PWK has dedicated section

**8. Nmap Scripting Engine (NSE) for Vulnerability Detection**
- **Difficulty**: 2
- **Content**: NSE basics, vuln category scripts, custom NSE scripts, lightweight scanning, NSE vs Nessus
- **Why**: Powerful Nmap feature, PWK covers extensively

**9. Password Attacks: Network Services & Hash Cracking**
- **Difficulty**: 2
- **Content**: SSH/RDP brute force, HTTP POST attacks, Hydra, Medusa, password cracking fundamentals, wordlist mutation, Hashcat/John
- **Why**: Essential pentest skill, PWK has full module

**10. Working with Password Hashes: NTLM, Net-NTLMv2, and Relay Attacks**
- **Difficulty**: 3
- **Content**: Obtaining hashes, cracking NTLM, Pass-the-Hash, Net-NTLMv2 capture, NTLM relay, Responder, ntlmrelayx
- **Why**: Critical for Windows pentesting, PWK covers in detail

**11. Client-Side Attacks: Microsoft Office & Windows Library Files**
- **Difficulty**: 2
- **Content**: Word macros, DDE, .library-ms abuse, .lnk shortcuts, HTA files, target reconnaissance
- **Why**: Real-world initial access, PWK dedicates module

**12. Antivirus Evasion Techniques**
- **Difficulty**: 2-3
- **Content**: AV components, detection engines, manual evasion, obfuscation, automated tools (Veil, Shellter), AMSI bypass
- **Why**: Essential for modern pentesting, PWK full section

#### Metasploit Domain (add 4 lessons - consider new domain or add to pentest):

**13. Metasploit Fundamentals & Workspace Setup**
- **Difficulty**: 1-2
- **Content**: MSF architecture, navigation, workspaces, databases, auxiliary modules, exploit modules
- **Why**: Essential framework, PWK dedicates full module

**14. Metasploit Payload Engineering**
- **Difficulty**: 2
- **Content**: Staged vs non-staged, Meterpreter deep dive, payload encoders, creating executables, payload handlers
- **Why**: Core Metasploit skill

**15. Metasploit Post-Exploitation Operations**
- **Difficulty**: 2
- **Content**: Meterpreter commands, post-exploitation modules, credential harvesting, screenshot/keylogger, hashdump, pivoting
- **Why**: Post-exploitation is half of pentesting

**16. Automating Metasploit Engagements**
- **Difficulty**: 2-3
- **Content**: Resource scripts, AutoRunScript, custom RC files, batch exploitation, automated post-exploitation
- **Why**: Efficiency in repetitive tasks

#### Networking/Tunneling Domain (add 3 lessons):

**17. Port Forwarding and Pivoting with Linux Tools**
- **Difficulty**: 2-3
- **Content**: Socat port forwarding, SSH local/remote/dynamic port forwarding, ProxyChains, pivoting concepts
- **Why**: Essential for internal network pentesting, PWK covers extensively

**18. Port Forwarding and Pivoting with Windows Tools**
- **Difficulty**: 2-3
- **Content**: ssh.exe, Plink, Netsh port forwarding, Windows-specific tunneling challenges
- **Why**: Windows environments are common, PWK dedicates section

**19. Advanced Tunneling: HTTP and DNS**
- **Difficulty**: 3
- **Content**: HTTP tunneling (Chisel), DNS tunneling (dnscat2), tunneling through DPI, choosing the right tunnel
- **Why**: Bypassing network restrictions, advanced technique

---

### 🟡 MEDIUM PRIORITY (Enhance Existing Coverage)

#### Information Gathering (add 3-4 lessons):

**20. Passive Information Gathering & OSINT Techniques**
- **Difficulty**: 1-2
- **Content**: Passive vs active, web server enumeration, DNS passive reconnaissance, WHOIS, certificate transparency, Shodan
- **Why**: PWK distinguishes this clearly, expand existing OSINT

**21. Active Information Gathering: Protocol Enumeration**
- **Difficulty**: 2
- **Content**: DNS enumeration (zone transfers, brute force), SMB enumeration (enum4linux, smbclient), SMTP/SNMP enum, Netcat scanning
- **Why**: PWK covers each protocol, current lesson is too general

**22. Living off the Land: Reconnaissance with Native Tools**
- **Difficulty**: 2
- **Content**: Windows built-in tools (net, whoami, systeminfo, ipconfig), Linux reconnaissance, avoiding detection
- **Why**: PWK emphasizes LOTL, critical for modern pentesting

#### Exploit Development Basics (add 2 lessons):

**23. Public Exploits: Discovery, Analysis, and Execution**
- **Difficulty**: 2
- **Content**: ExploitDB, SearchSploit, GitHub, Google dorking, reading exploit code, understanding risks, complete workflow
- **Why**: Expand existing lesson with PWK's structured approach

**24. Fixing and Troubleshooting Exploits**
- **Difficulty**: 2-3
- **Content**: Memory corruption exploits (cross-compilation, architecture), web exploit troubleshooting, dependency issues, debugging
- **Why**: Real-world exploits often need modification

---

### 🟢 LOW PRIORITY (Optional Meta-Content)

#### Learning Strategies (add 2-3 lessons - OPTIONAL):

**25. Effective Learning Strategies for Technical Skills**
- **Difficulty**: 1
- **Content**: Learning theory, memory mechanisms, forgetting curve, cognitive load, dual encoding
- **Why**: PWK emphasizes meta-learning, valuable for all students

**26. OffSec Try Harder Methodology**
- **Difficulty**: 1
- **Content**: Demonstrative methodology, dealing with uncertainty, retrieval practice, spaced practice, Feynman technique, Leitner system
- **Why**: Unique PWK approach, helps with mindset

**27. OSCP Exam Preparation & Strategies**
- **Difficulty**: 1
- **Content**: Exam format, time management, dealing with stress, when you're ready, documentation during exam
- **Why**: Helps students preparing for certification

---

## Suggested Lesson Creation Order

### Phase 1: Core Pentest Skills (Weeks 1-3)
Create lessons 1-12 (Report Writing, Web App Testing, Password Attacks, AV Evasion)
**Impact**: Covers most critical PWK gaps

### Phase 2: Metasploit Mastery (Week 4)
Create lessons 13-16 (Metasploit fundamentals through automation)
**Impact**: Addresses major framework gap

### Phase 3: Networking & Pivoting (Week 5)
Create lessons 17-19 (Port forwarding, SSH tunneling, advanced tunneling)
**Impact**: Essential for internal network pentesting

### Phase 4: Enhanced Reconnaissance (Week 6)
Create lessons 20-22 (Passive OSINT, Active enumeration, LOTL)
**Impact**: Improves existing coverage

### Phase 5: Exploit Skills (Week 7)
Create lessons 23-24 (Public exploits, fixing exploits)
**Impact**: Practical exploit usage

### Phase 6: Meta-Learning (Optional)
Create lessons 25-27 (Learning strategies, Try Harder methodology, exam prep)
**Impact**: Student mindset and success

---

## Domains That Need New Lessons

Based on this analysis, here are the domain distributions:

### Suggested New Domain: **"Advanced Pentest"**
- Metasploit 4 lessons
- Tunneling/Pivoting 3 lessons
- Advanced exploitation 2-3 lessons
- Total: 9-10 lessons

### Expand Existing **Pentest Domain** (currently 9 lessons):
- Add 10-12 lessons (web testing, password attacks, client-side, AV evasion, vuln scanning, reporting)
- New total: 19-21 lessons

### Optionally Create **"Learning & Career"** Domain:
- Meta-learning 2-3 lessons
- Pentest reporting 2 lessons
- Career development 1-2 lessons
- Total: 5-7 lessons

---

## Summary Statistics

**PWK Syllabus Topics**: ~90 learning units
**Currently Well Covered**: ~35-40 topics (40%)
**Partially Covered**: ~20-25 topics (25%)
**Major Gaps**: ~30-35 topics (35%)

**Recommended New Lessons**: 25-30 lessons
**Time Estimate**: 100-150 hours of content creation
**Priority Breakdown**:
- High Priority: 16 lessons (core PWK skills)
- Medium Priority: 6-7 lessons (enhanced coverage)
- Low Priority: 3-4 lessons (optional meta-learning)

**After adding these lessons**:
- PWK coverage: ~85-90%
- Total CyberLearn lessons: 130-140
- Complete alignment with industry-standard pentest training

---

## Next Steps

1. **Review this analysis** - Decide which lessons to prioritize
2. **Use CHATGPT_LESSON_PROMPT.md** - Generate lessons with ChatGPT
3. **Create in batches** - Do 3-5 lessons at a time for consistency
4. **Start with High Priority** - Maximum impact on PWK coverage
5. **Test on VM** - Load and verify each batch

**Estimated Timeline**:
- High Priority (16 lessons): 4-5 weeks
- Medium Priority (7 lessons): 2 weeks
- Low Priority (4 lessons): 1 week
- **Total**: 7-8 weeks for complete PWK coverage

---

Would you like me to create detailed lesson outlines for any of these suggested lessons?
