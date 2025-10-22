# Advanced Cybersecurity Lessons

## Overview

This document describes the **advanced curriculum** for CyberLearn - covering real-world threat actor techniques, APT simulations, and advanced defensive operations.

⚠️ **IMPORTANT**: These lessons contain advanced offensive and defensive techniques used in real-world cyberattacks and defense operations. **Use this knowledge ethically and only on authorized systems.**

## Prerequisites

Before accessing advanced lessons, complete:
- All fundamentals lessons (skill level 25+)
- Basic lessons in your chosen domain (skill level 50+)
- Diagnostic assessment

## Advanced Curriculum (22 Lessons)

### Active Directory Security (5 Lessons)

**Difficulty 4 | Prerequisites: AD Fundamentals & Kerberos**

1. **Kerberoasting Attack**
   - SPN enumeration and TGS extraction
   - Offline credential cracking
   - Detection and mitigation strategies
   - Tools: Rubeus, Invoke-Kerberoast, Hashcat

2. **Golden Ticket Attack**
   - KRBTGT hash extraction
   - Forging Kerberos TGTs
   - Domain persistence techniques
   - Detection via anomalous ticket properties

3. **Pass-the-Hash and Pass-the-Ticket**
   - NTLM hash reuse for authentication
   - Kerberos ticket reuse techniques
   - Lateral movement strategies
   - Credential theft prevention

4. **DCSync Attack**
   - Directory replication abuse
   - Credential dumping from domain controllers
   - Detection via replication monitoring
   - Tools: mimikatz, BloodHound

5. **AD Certificate Services Exploitation**
   - ESC1-ESC8 vulnerability classes
   - Certificate template misconfiguration
   - Persistent authentication via certificates
   - PKI hardening strategies

### Red Team Operations (5 Lessons)

**Difficulty 4 | Prerequisites: Pentest Fundamentals**

1. **APT29 (Cozy Bear) TTPs**
   - Russian state-sponsored threat actor simulation
   - Spear phishing initial access
   - Living-off-the-land techniques
   - PowerShell-based C2 infrastructure
   - MITRE ATT&CK mapping
   - Detection opportunities at each stage

2. **APT28 (Fancy Bear) Operations**
   - GRU-linked aggressive operations
   - X-Agent/Sofacy malware family
   - Supply chain targeting
   - Watering hole attacks
   - Information operations

3. **Lazarus Group Financial Attacks**
   - North Korean cybercrime operations
   - SWIFT banking system targeting
   - Cryptocurrency theft techniques
   - WannaCry ransomware campaign
   - Financial sector defenses

4. **Advanced C2 Infrastructure**
   - Domain fronting techniques
   - Multi-channel C2 resilience
   - Anonymization strategies
   - Infrastructure detection and takedown

5. **Living Off The Land (LOLBins)**
   - Using legitimate Windows tools maliciously
   - certutil, bitsadmin, PowerShell abuse
   - Bypassing application whitelisting
   - Fileless attack techniques
   - Detection via behavioral analytics

### Blue Team Defense (6 Lessons)

**Difficulty 4 | Prerequisites: DFIR & Incident Response**

1. **Threat Hunting Methodology**
   - Hypothesis-driven hunting
   - IOC development and validation
   - Behavioral analysis techniques
   - Threat intelligence integration
   - **HANDS-ON**: Kerberoasting hunt playbook with detection logic

2. **EDR Detection Engineering**
   - Custom detection rule development
   - False positive reduction strategies
   - SIEM correlation logic
   - Behavioral analytics implementation
   - Detection rule testing

3. **Memory Forensics and Malware Detection**
   - Volatility framework usage
   - Rootkit detection in memory
   - Process injection identification
   - Fileless malware analysis
   - Memory artifact interpretation

4. **Deception Technology**
   - Honeypot deployment strategies
   - Honeytoken creation and monitoring
   - Canary file systems
   - High-fidelity alert generation
   - Attacker behavior analysis

5. **Advanced SIEM Use Cases**
   - Multi-source log correlation
   - Complex attack pattern detection
   - Alert tuning and prioritization
   - Threat-informed use case development
   - Dashboard and reporting

6. **Incident Response Automation**
   - SOAR platform implementation
   - Playbook development
   - Automated enrichment and containment
   - Orchestration workflows
   - Human-in-the-loop decision points

### DFIR Advanced (3 Lessons)

**Difficulty 4 | Prerequisites: DFIR Basics**

1. **Advanced Windows Forensics**
   - Prefetch analysis for execution tracking
   - ShimCache and Amcache artifacts
   - SRUM (System Resource Usage Monitor)
   - Registry forensics deep dive
   - Timeline reconstruction

2. **Network Traffic Analysis**
   - PCAP analysis with Wireshark
   - C2 beaconing detection
   - Data exfiltration patterns
   - Protocol anomaly identification
   - Encrypted traffic analysis

3. **Timeline Analysis**
   - Super timeline creation with Plaso
   - Log2timeline usage
   - Event correlation across sources
   - Attack sequence reconstruction
   - Evidence presentation

### Malware Analysis Advanced (3 Lessons)

**Difficulty 4 | Prerequisites: Static & Dynamic Analysis**

1. **Reverse Engineering Fundamentals**
   - Assembly language basics (x86/x64)
   - IDA Pro and Ghidra usage
   - Control flow analysis
   - Function identification
   - String and API analysis

2. **Anti-Analysis Techniques**
   - Packing and obfuscation
   - Anti-debugging tricks
   - VM and sandbox detection
   - Code encryption and polymorphism
   - Bypassing anti-analysis

3. **Ransomware Analysis**
   - Encryption algorithm identification
   - Ransom note analysis
   - Payment mechanism tracking
   - Double extortion tactics
   - Decryption possibilities

## APT Attack Path Simulations

Advanced Red Team lessons include full APT attack simulations:

### APT29 (Cozy Bear) Attack Chain
```
Phase 1: Initial Compromise
├── Spear phishing with malicious Office macro
├── WellMess/WellMail dropper deployment
└── MITRE: T1566.001 (Phishing: Spearphishing Attachment)

Phase 2: Establish Foothold
├── PowerShell Empire or Cobalt Strike
├── Registry persistence mechanisms
├── Scheduled task creation
└── MITRE: T1053.005, T1059.001

Phase 3: Credential Access
├── mimikatz LSASS dumping
├── Pass-the-hash lateral movement
├── Kerberoasting service accounts
└── MITRE: T1003.001, T1558.003

Phase 4: Lateral Movement
├── PsExec or WMI execution
├── RDP with stolen credentials
└── MITRE: T1021.001, T1021.002

Phase 5: Data Collection & Exfiltration
├── Archive sensitive files
├── OneDrive staging
├── HTTPS exfiltration to legitimate services
└── MITRE: T1560, T1567.002

Detection Opportunities:
• Email gateway: Macro detection
• EDR: LSASS access alerts
• Network: Unusual cloud uploads
• Behavioral: Anomalous PowerShell usage
```

### APT28 (Fancy Bear) Attack Chain
```
Phase 1: Reconnaissance
├── Extensive OSINT collection
├── LinkedIn target profiling
└── Infrastructure mapping

Phase 2: Initial Access
├── Spear phishing with exploits
├── Watering hole attacks
└── USB drop operations

Phase 3: Malware Deployment
├── X-Agent modular backdoor
├── Sedkit exploit kit
└── Credential harvesting modules
```

## Threat Hunting Playbook Example

### Hunt: Kerberoasting Activity

**Hypothesis**: "Adversaries may be extracting service account TGS tickets for offline password cracking"

**Data Sources**:
- Windows Event Logs (Security: Event ID 4769)
- EDR telemetry
- Network traffic captures
- Authentication logs

**Hunt Steps**:
1. Establish baseline: Normal TGS request patterns
2. Search for Event ID 4769 with RC4 encryption (downgrade indicator)
3. Correlate multiple TGS requests from single account in short timeframe
4. Check for requests to high-value service accounts
5. Investigate anomalous requesting accounts

**Detection Logic**:
```
IF: >10 TGS requests in 5 minutes
FROM: single user account
THEN: Alert "Potential Kerberoasting"

IF: TGS request
WITH: RC4 encryption type
FOR: service account with SPN
THEN: Alert "Encryption Downgrade - Kerberoasting"

IF: TGS requests
FOR: admin-level service accounts
FROM: low-privilege user
THEN: Alert "Privilege Mismatch - Kerberoasting"
```

**Response Actions**:
1. Isolate suspicious user account
2. Rotate compromised service account passwords (25+ character complexity)
3. Review authentication logs for successful compromise
4. Create permanent detection rule
5. Enable AES-only Kerberos encryption

## Learning Objectives

After completing advanced lessons, you will be able to:

### Red Team Skills
- Simulate real APT attack chains (APT29, APT28, Lazarus)
- Exploit Active Directory vulnerabilities (Kerberoasting, Golden Ticket, DCSync)
- Build resilient C2 infrastructure
- Use living-off-the-land techniques
- Map activities to MITRE ATT&CK framework

### Blue Team Skills
- Conduct hypothesis-driven threat hunting
- Build custom EDR detection rules
- Analyze memory dumps for malware
- Deploy deception technology
- Develop SOAR playbooks for automated response
- Create advanced SIEM correlation rules

### DFIR Skills
- Perform advanced Windows forensics (Prefetch, ShimCache, SRUM)
- Analyze network traffic for C2 and exfiltration
- Create super timelines with Plaso
- Reconstruct attack sequences
- Identify evidence across multiple sources

### Malware Analysis Skills
- Reverse engineer binaries with IDA/Ghidra
- Identify and bypass anti-analysis techniques
- Analyze ransomware encryption and payment flows
- Detect packing and obfuscation
- Extract IOCs and behavioral signatures

## Ethical Use Policy

**CRITICAL**: These lessons teach powerful offensive and defensive techniques.

✅ **AUTHORIZED USE**:
- Penetration testing with written authorization
- Security research in controlled environments
- Red team exercises on company-owned systems
- CTF competitions
- Educational labs and practice environments
- Defensive blue team operations

❌ **PROHIBITED USE**:
- Unauthorized access to systems
- Attacks on systems without explicit permission
- Malicious intent or criminal activity
- Testing on production systems without approval
- Reconnaissance of targets you don't own

**Legal Notice**: Unauthorized computer access is illegal under CFAA (US), Computer Misuse Act (UK), and similar laws globally. Always obtain written authorization before security testing.

## Tools Referenced

Advanced lessons reference industry-standard tools:

**Red Team**:
- Cobalt Strike, PowerShell Empire (C2)
- Rubeus, Invoke-Kerberoast (AD exploitation)
- mimikatz (credential access)
- BloodHound (AD enumeration)
- Metasploit Framework

**Blue Team**:
- Splunk, Elastic SIEM (log analysis)
- Velociraptor, OSQuery (EDR)
- Volatility (memory forensics)
- Suricata, Zeek (network monitoring)
- TheHive, Cortex (SOAR)

**DFIR**:
- Plaso/log2timeline (timeline analysis)
- FTK Imager, X-Ways (disk forensics)
- Wireshark (network analysis)
- Autopsy (case management)

**Malware Analysis**:
- IDA Pro, Ghidra (disassembly)
- x64dbg, WinDbg (debugging)
- PE Studio, PEiD (static analysis)
- Remnux, FLARE VM (analysis environments)

## Difficulty Progression

**Difficulty 1-2** (Beginner/Intermediate): Basic lessons
- Concepts and fundamentals
- Theory and simple practice
- Guided exercises

**Difficulty 3** (Advanced): Intermediate lessons
- Practical application
- Multi-step procedures
- Real-world scenarios

**Difficulty 4** (Expert): Advanced lessons
- Complex attack chains
- Multi-stage operations
- Advanced detection and analysis
- Requires strong fundamentals

## XP and Rewards

Advanced lessons provide higher rewards:
- **Base XP**: 150 × difficulty level (600 XP for difficulty 4)
- **Quiz points**: 15 per question (vs 10 for basic)
- **Simulation XP**: 50 XP for interactive attack/hunt simulations
- **Badge unlocks**: "APT Hunter", "AD Dominator", "Memory Forensics Expert"

## Running Advanced Lesson Generator

On your VM, run:

```bash
# Generate 22 advanced lessons
python generate_advanced_lessons.py

# Load all lessons (basic + advanced)
python load_all_lessons.py

# Check database
python check_database.py

# Launch app
streamlit run app.py
```

## Lesson File Structure

Advanced lessons include:
- **Mindset coaching**: Ethical use reminders
- **Technical content**: Deep technical explanations
- **Attack simulations**: Step-by-step attack paths with MITRE mapping
- **Threat hunting playbooks**: Detection logic and data sources
- **MITRE ATT&CK mapping**: Industry-standard technique IDs
- **Detection opportunities**: Blue team perspective on each attack
- **Advanced quizzes**: Higher difficulty questions

## Total Curriculum

After generating all lessons:

**Basic Lessons (18)**:
- Fundamentals: 4 lessons
- DFIR: 3 lessons
- Malware: 3 lessons
- Active Directory: 3 lessons
- Pentest: 3 lessons
- Red Team: 0 (covered in advanced)
- Blue Team: 0 (covered in advanced)
- **CIA Triad**: 1 existing lesson

**Advanced Lessons (22)**:
- Active Directory: 5 lessons
- Red Team: 5 lessons
- Blue Team: 6 lessons
- DFIR: 3 lessons
- Malware: 3 lessons

**TOTAL: 40 comprehensive lessons** covering beginner to expert level

## Questions?

The advanced curriculum provides:
- Real-world APT simulations (APT29, APT28, Lazarus)
- Active Directory attack techniques (Kerberoasting, Golden Ticket, DCSync, Pass-the-Hash, AD CS)
- Advanced detection engineering
- Threat hunting methodologies
- Memory forensics
- Malware reverse engineering
- Incident response automation

This is a **professional-grade curriculum** used in real SOC, Red Team, and DFIR operations.

---

**Remember**: With great power comes great responsibility. Use these skills to make cyberspace safer. 🛡️
