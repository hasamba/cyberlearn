"""
Add relevant memory aid blocks to lessons missing them.

This script adds contextually appropriate mnemonics and memory techniques based on:
- Lesson domain and specific topic
- Key concepts that need memorization
- Professional acronyms and industry standards
"""

import json
import os
from pathlib import Path

# Memory aid content tailored to specific lessons
MEMORY_AIDS = {
    "lesson_active_directory_02_group_policy_RICH.json": {
        "text": """**Memory Aid: Group Policy Processing Order - LSDOU**

To remember the order that Group Policy Objects (GPOs) are applied:

**L**ocal → **S**ite → **D**omain → **O**U

**Mnemonic: "**L**ocal **S**ecurity **D**epartment **O**rders **U**pdates"

**Key Points to Remember:**
- **Last applied = Highest priority** (OU policies override Domain policies)
- **LSDOU = Processing order from lowest to highest priority**
- **Block inheritance** stops LSDOU chain at that OU
- **Enforce** makes a GPO override all lower-level policies

**Visual Memory Aid:**
```
Priority (Low → High):
┌─────────────┐
│   Local     │  (Computer-level policies)
├─────────────┤
│    Site     │  (Physical network location)
├─────────────┤
│   Domain    │  (Active Directory domain-wide)
├─────────────┤
│     OU      │  (Organizational Unit - HIGHEST PRIORITY)
└─────────────┘
```

**Memory Hook for GPO Conflicts:**
"**OU**r policies **O**verride **U**nder-level settings" (OU = highest priority)

**Quick Recall Test:**
If you have conflicting settings in Domain GPO (password length: 10) and OU GPO (password length: 14), which wins?
Answer: OU GPO (14 characters) - last applied wins!"""
    },

    "lesson_active_directory_03_kerberos_RICH.json": {
        "text": """**Memory Aid: Kerberos Authentication Flow - "Three-Headed Dog"**

Kerberos is named after Cerberus, the three-headed dog guarding the underworld. Remember the three main components:

**The Three Heads of Kerberos:**
1. **C**lient (the user requesting access)
2. **KDC** (Key Distribution Center - the authentication authority)
3. **S**ervice (the resource being accessed)

**Mnemonic for the Ticket Flow: "Can't Keep Secrets From TGT Services"**
- **C**lient authenticates → **K**DC
- **K**DC issues → **TGT** (Ticket Granting Ticket)
- **TGT** used to request → **Service Ticket**

**The Two-Ticket System:**
- **TGT** = "Golden Ticket" = Your authentication proof (like a passport)
- **Service Ticket** = "Silver Ticket" = Access to specific resource (like a visa)

**Port Number Memory Hook:**
Kerberos uses port **88** → "**88** keys on a piano, Kerberos is the KEY to authentication"

**Visual Flow (Remember: AS → TGS → Service):**
```
Client → [AS-REQ] → KDC (Authentication Service)
       ← [AS-REP with TGT] ←

Client → [TGS-REQ with TGT] → KDC (Ticket Granting Service)
       ← [TGS-REP with Service Ticket] ←

Client → [AP-REQ with Service Ticket] → Service
       ← [AP-REP access granted] ←
```

**Attack Mnemonic: "Golden Pass, Silver Service, Roasted Credentials"**
- **Golden** Ticket attack = Forged TGT (full domain access)
- **Silver** Ticket attack = Forged Service Ticket (specific service access)
- **Kerberoasting** = Roast the service ticket to crack password

**Quick Recall:** What's the difference between Golden and Silver tickets?
- Golden = TGT (authenticate to KDC, get any service ticket)
- Silver = Service ticket (access specific service, no KDC involved)"""
    },

    "lesson_blue_team_01_fundamentals_RICH.json": {
        "text": """**Memory Aid: Blue Team Core Functions - "DIRTCAR"**

Remember the seven core Blue Team functions with **DIRTCAR**:

**D**etection - Identify security events and anomalies
**I**ncident Response - Handle security breaches
**R**ecovery - Restore systems after attacks
**T**hreat Intelligence - Understand adversary TTPs
**C**ompliance - Meet regulatory requirements
**A**nalysis - Investigate logs and artifacts
**R**esponse - Take action to contain and remediate

**Visual Memory Aid - The Blue Team Cycle:**
```
    ┌──────────────┐
    │   Monitor    │ ← Detection & Analysis
    └──────┬───────┘
           ↓
    ┌──────────────┐
    │    Detect    │ ← Threat Intelligence
    └──────┬───────┘
           ↓
    ┌──────────────┐
    │   Respond    │ ← Incident Response
    └──────┬───────┘
           ↓
    ┌──────────────┐
    │   Recover    │ ← Recovery & Compliance
    └──────────────┘
```

**Blue vs Red Team - Color Code Memory:**
- **Blue** = Defense = "**B**lock **L**ogs **U**nderstand **E**vents"
- **Red** = Offense = "**R**econnoiter **E**xploit **D**eploy"
- **Purple** = Collaboration (Blue + Red = Purple team exercises)

**Essential Blue Team Tools - "SPLASHEM"**
**S**IEM (Splunk, ELK)
**P**acket capture (Wireshark)
**L**og analysis (Kibana)
**A**ntivirus/EDR (CrowdStrike)
**S**ecurity monitoring (Nagios)
**H**oneypots (deception)
**E**vent correlation (QRadar)
**M**alware analysis (Cuckoo)

**Quick Recall:** What's the first thing Blue Team does when an alert fires?
Answer: **DIRT** → **D**etect (confirm it's real), **I**nvestigate (gather context), **R**espond (contain), **T**rack (document for threat intel)"""
    },

    "lesson_blue_team_02_log_analysis_RICH.json": {
        "text": """**Memory Aid: Critical Windows Event IDs - "The Security Big 5"**

**For Login Activity - "45 is Alive, 40 is Dead":**
- **4624** = Successful login (user is **alive** in system)
- **4625** = Failed login (access attempt **dead**/denied)
- **4634/4647** = Logoff (session is **dead**)

**For Account Changes - "The 72x Series":**
- **4720** = Account created
- **4722** = Account enabled
- **4724** = Password reset attempt
- **4725** = Account disabled
- **4726** = Account deleted

**For Privilege Escalation - "The 67x Series":**
- **4672** = Special privileges assigned (Administrator login)
- **4673** = Privileged service called
- **4674** = Operation attempted on privileged object

**Mnemonic for the Big 5 Security Events:**
"**46** **24/7** Login Monitoring Prevents **49** Problems"
- **4624** = Successful login
- **4625** = Failed login
- **4648** = Explicit credentials (RunAs)
- **4672** = Admin login
- **4720** = New account created

**Linux Log Location Memory - "/var/log/SAMBA":**
**S**yslog = /var/log/syslog
**A**uth = /var/log/auth.log
**M**essages = /var/log/messages
**B**oot = /var/log/boot.log
**A**pache = /var/log/apache2/

**Process Events - "The 4688 Rule":**
- **4688** = New process created
- **4689** = Process terminated
- **Remember:** "**88** keys on piano, **4688** creates new process"

**Quick Recall Test:**
User successfully logs in with admin rights. Which two events fire?
Answer: **4624** (successful login) + **4672** (special privileges assigned)"""
    },

    "lesson_cloud_12_aws_control_tower_security_automation_RICH.json": {
        "text": """**Memory Aid: AWS Control Tower Core Concepts - "LOGS"**

Remember the four pillars of AWS Control Tower with **LOGS**:

**L**anding Zone - Multi-account foundation
**O**rganizational Units - Account structure
**G**uardrails - Security and compliance controls
**S**ervice Control Policies - Permission boundaries

**Landing Zone Components - "CASSH":**
**C**loudFormation StackSets
**A**WS Organizations
**S**ingle Sign-On (SSO)
**S**ervice Catalog
**H**ome Region

**Guardrail Types - "MPD":**
**M**andatory = Cannot be disabled (e.g., "Disallow public write access to S3")
**P**reventive = Block actions before they happen (SCPs)
**D**etective = Alert after actions occur (AWS Config rules)

**OU Structure Memory - "SALI":**
**S**ecurity OU - Security and compliance accounts
**A**udit OU - Log Archive and Audit accounts
**L**og Archive OU - Centralized logging
**I**nfrastructure OU - Shared services (optional custom)

**Baseline Accounts - "The Three Pillars":**
1. **Management** account - Control Tower operations
2. **Log Archive** account - Centralized logs
3. **Audit** account - Security and compliance monitoring

**Visual Memory Aid:**
```
Control Tower
    │
    ├─ Management Account (The Boss)
    │
    ├─ Security OU
    │   ├─ Log Archive (Record Everything)
    │   └─ Audit (Check Everything)
    │
    └─ Production OU
        └─ Workload Accounts (Guardrails Applied)
```

**Guardrail Enforcement - "Red Light, Yellow Light":**
- **Preventive** guardrails = **Red light** (STOP before action)
- **Detective** guardrails = **Yellow light** (Alert AFTER action)

**Quick Recall:** What's the difference between preventive and detective guardrails?
- Preventive = Uses SCPs to **block** actions (e.g., can't delete CloudTrail logs)
- Detective = Uses Config rules to **detect** violations (e.g., alerts if MFA disabled)"""
    },

    "lesson_dfir_02_incident_response_process_RICH.json": {
        "text": """**Memory Aid: Incident Response Process - "PICERL"**

Remember the six phases of incident response with **PICERL** (pronounced "pickle"):

**P**reparation - Set up tools, processes, and team before incidents
**I**dentification - Detect and confirm security incidents
**C**ontainment - Limit damage and prevent spread
**E**radication - Remove threat from environment
**R**ecovery - Restore systems to normal operations
**L**essons Learned - Post-incident analysis and improvement

**Detailed Mnemonic: "Please Investigate Carefully, Eradicate Rapidly, Learn"**

**Containment Types - "SSH":**
**S**hort-term containment - Quick isolation (network isolation, account disable)
**S**ystem backup - Preserve evidence before eradication
**H**ard containment - Long-term isolation (rebuild systems, patch vulnerabilities)

**Order of Volatility (Data Collection) - "RAM CRASHD":**
**R**egisters & Cache
**A**ctive network connections
**M**emory (RAM)
**C**ommand history
**R**unning processes
**A**rtifacts (event logs, registry)
**S**wap/page files
**H**ard drive/Disk
**D**ata backups

**Severity Levels - "CLIMT":**
**C**ritical - Immediate threat to business operations
**L**ow - Minimal impact
**I**nformation - FYI, no action needed
**M**edium - Moderate impact
**T**ime-sensitive - High impact

**Communication During IR - "SWAT Team":**
**S**takeholders - Keep leadership informed
**W**orkforce - Internal communication
**A**uthorities - Law enforcement if needed
**T**echnical team - Coordinate response actions

**Visual Memory Aid:**
```
INCIDENT OCCURS
      ↓
[P] Preparation ← (Done before incident)
      ↓
[I] Identification ← "What happened?"
      ↓
[C] Containment ← "Stop the bleeding"
      ↓
[E] Eradication ← "Remove the threat"
      ↓
[R] Recovery ← "Back to normal"
      ↓
[L] Lessons Learned ← "How do we prevent this?"
```

**Quick Recall:** You detect ransomware encrypting files. What's your PICERL action order?
- **I**dentify: Confirm ransomware variant
- **C**ontain: Isolate infected systems from network
- **E**radicate: Remove malware, check for persistence
- **R**ecover: Restore from clean backups
- **L**earn: Review how ransomware entered, improve defenses"""
    },

    "lesson_dfir_03_windows_event_log_analysis_RICH.json": {
        "text": """**Memory Aid: Critical Windows Event Logs - "SAPS"**

Remember the four most critical Windows Event Logs with **SAPS**:

**S**ecurity - Authentication, privilege use, policy changes
**A**pplication - Software events and errors
**P**owerShell - Script execution and commands
**S**ystem - Service status, drivers, system events

**Security Log Event Categories - "ALPHA":**
**A**ccount logon/logoff (4624, 4625, 4634)
**L**ogon events (4648, 4672)
**P**rivilege use (4673, 4674)
**H**istorical changes (4720-4726 account management)
**A**udit policy changes (4719)

**PowerShell Event IDs - "The 4100 Series":**
- **4103** = Module logging (commands executed)
- **4104** = Script block logging (full script content)
- **4105** = Script execution start
- **4106** = Script execution stop

**Mnemonic: "**4104** captures **FULL** script blocks"** (Both have 4 letters)

**Sysmon Event IDs - "Process Power 3":**
- **Event 1** = Process creation (new executable started)
- **Event 3** = Network connection (outbound connections)
- **Event 11** = File creation (files written to disk)

**Remember:** "**1** process, **3** connections, **11** files" (Ascending numbers for common events)

**Log Locations - Windows Path Memory:**
```
%SystemRoot%\System32\winevt\Logs\
    ├─ Security.evtx (The Big One)
    ├─ System.evtx
    ├─ Application.evtx
    └─ Microsoft-Windows-PowerShell%4Operational.evtx
```

**Event ID Ranges by Category:**
- **4xxx** = Security events (auditing)
- **1xxx** = Application events
- **7xxx** = Service Control Manager events
- **10xx** = System events

**Lateral Movement Detection - "The 4648 Clue":**
Event **4648** = Explicit credentials used (RunAs, PsExec, RDP)
**Memory hook:** "**48** hours to detect lateral movement = look for **4648**"

**Visual - Timeline Analysis:**
```
Attack Timeline Using Event IDs:
4624 (Login) → 4688 (Process: mimikatz.exe) → 4648 (RunAs to DC) → 4672 (Admin rights) → 4720 (New account)
```

**Quick Recall:** Attacker uses mimikatz to dump credentials, then laterally moves to Domain Controller. Which 3 events would you search for?
Answer: **4688** (process creation: mimikatz), **4648** (explicit credentials for lateral movement), **4672** (special privileges assigned on DC)"""
    },

    "lesson_dfir_04_disk_forensics_RICH.json": {
        "text": """**Memory Aid: Order of Volatility - "RAM CRASHD"**

When collecting forensic evidence, remember the order from most to least volatile with **RAM CRASHD**:

**R**egisters & CPU Cache
**A**ctive network connections & ARP cache
**M**emory (RAM)
**C**ommand history (bash_history, PowerShell history)
**R**unning processes & loaded modules
**A**rtifacts (event logs, registry, temp files)
**S**wap/Page files
**H**ard drive / Disk
**D**ata backups & archives

**Mnemonic:** "**R**acing **A**gainst **M**emory loss, **C**ollect **R**apidly **A**ll **S**ystem **H**istory **D**ata"

**NTFS Forensic Artifacts - "MUFT":**
**M**FT ($MFT) - Master File Table (all file metadata)
**U**SN Journal ($UsnJrnl) - File system change log
**F**ile names ($I30) - Directory indexes
**T**imestamps (MACB) - Modified, Accessed, Changed, Birth

**MACB Timestamps Memory - "Make A Change, Baby":**
**M**odified (M) - File content changed
**A**ccessed (A) - File was read
**C**hanged (C) - Metadata changed (rename, permissions)
**B**irth (B) - File created (Born)

**File Signature Memory - Magic Bytes:**
- **PDF** = `%PDF` (25 50 44 46)
- **ZIP** = `PK` (50 4B)
- **JPEG** = `FF D8 FF`
- **PNG** = `89 50 4E 47`
- **EXE** = `MZ` (4D 5A)

**Remember:** "**P**lease **K**eep **M**agic **Z**ips" for common signatures

**Alternate Data Streams (ADS) - The Hidden Files:**
- Normal file: `file.txt`
- Hidden stream: `file.txt:hidden.exe`
- **Memory hook:** "**ADS** = **A**lternate **D**ata = **S**ecret data hidden"

**Slack Space Types - "FR":**
**F**ile slack - Unused space between end of file and end of cluster
**R**AM slack - Unused space between end of file and end of sector

**Visual Memory Aid - Disk Structure:**
```
┌─────────────────────────────────────┐
│  MBR (Master Boot Record)           │ ← Sector 0
├─────────────────────────────────────┤
│  Partition Table                    │
├─────────────────────────────────────┤
│  Boot Sector (VBR)                  │
├─────────────────────────────────────┤
│  $MFT (Master File Table)           │ ← File metadata
├─────────────────────────────────────┤
│  File System Data                   │
│  (Your files and folders)           │
└─────────────────────────────────────┘
```

**Forensic Tool Memory - "FASTE":**
**F**TK (Forensic Toolkit)
**A**utopsy (Open source)
**S**leuth Kit (Command line)
**T**SK (The Sleuth Kit utilities)
**E**nCase (Commercial)

**Quick Recall:** You find a suspicious file named `document.pdf:malware.exe`. What forensic concept is this?
Answer: **Alternate Data Stream (ADS)** - hiding malware in ADS of PDF file"""
    },

    "lesson_fundamentals_03_encryption_RICH.json": {
        "text": """**Memory Aid: Encryption Types - "SASH"**

Remember the four main encryption categories with **SASH**:

**S**ymmetric - Same key encrypts and decrypts (fast, shared secret)
**A**symmetric - Public/private key pairs (slow, secure key exchange)
**S**treaming - Encrypts data bit-by-bit (XOR with keystream)
**H**ashing - One-way function (cannot decrypt, verify integrity)

**Symmetric Encryption Algorithms - "3-ABC":**
**3**DES - Triple DES (legacy, 168-bit)
**A**ES - Advanced Encryption Standard (current standard: 128, 192, 256-bit)
**B**lowfish - Fast, variable key (32-448 bit)
**C**hacha20 - Modern stream cipher

**Mnemonic:** "**3** **A**lgorithms **B**efore **C**hacha" (Evolution of symmetric encryption)

**Asymmetric Algorithms - "RED":**
**R**SA - Rivest-Shamir-Adleman (most common, 2048-4096 bit)
**E**CC - Elliptic Curve Cryptography (smaller keys, mobile-friendly)
**D**iffie-Hellman - Key exchange protocol

**Hash Functions - "SMASH":**
**S**HA-2 (SHA-256, SHA-512) - Current standard
**M**D5 - Broken, **do not use** (128-bit)
**A**rgon2 - Password hashing (winner of Password Hashing Competition)
**S**HA-1 - Deprecated, **avoid** (160-bit, collision attacks)
**H**MAC - Hash-based Message Authentication Code

**Mnemonic for Hash Strength:** "**SHA-2** is **2**wice as strong as SHA-1"

**AES Key Sizes - "The Three Strengths":**
- **AES-128** = 128-bit key = Standard security
- **AES-192** = 192-bit key = High security
- **AES-256** = 256-bit key = Top secret (government use)
- **Memory hook:** "**128** protects your **house**, **256** protects the **W**hite **H**ouse"

**Encryption Modes - "ECB is Evil, CBC is Better":**
**E**CB (Electronic Codebook) - **Avoid!** (patterns visible)
**C**BC (Cipher Block Chaining) - Standard mode
**G**CM (Galois/Counter Mode) - Modern, authenticated encryption
**C**TR (Counter Mode) - Parallelizable

**RSA Key Size Timeline:**
- **1024-bit** = Deprecated (broken in 2010)
- **2048-bit** = Minimum today
- **4096-bit** = High security

**Hashing vs Encryption - The Directional Rule:**
```
Encryption:  Plaintext → [Key] → Ciphertext → [Key] → Plaintext (TWO-WAY)
Hashing:     Plaintext → [Hash Function] → Hash (ONE-WAY, cannot reverse)
```

**SSL/TLS Handshake - "Asymmetric starts, Symmetric continues":**
1. Asymmetric (RSA/ECDH) used to exchange session key (slow, secure)
2. Symmetric (AES) used for bulk data encryption (fast)

**Quick Recall Questions:**
Q: You need to encrypt 1GB of data. Symmetric or Asymmetric?
A: **Symmetric** (AES) - asymmetric too slow for bulk data

Q: You need to verify file integrity. Encryption or hashing?
A: **Hashing** (SHA-256) - one-way, fixed output for verification

Q: Should you use MD5 for password hashing?
A: **No!** Use Argon2, bcrypt, or scrypt (MD5 is broken)"""
    },

    "lesson_fundamentals_05_network_security_RICH.json": {
        "text": """**Memory Aid: OSI Model - "Please Do Not Throw Sausage Pizza Away"**

Remember the 7 layers of the OSI model from Layer 1 to Layer 7:

**P**hysical (Layer 1) - Cables, electrical signals, bits
**D**ata Link (Layer 2) - MAC addresses, switches, frames
**N**etwork (Layer 3) - IP addresses, routers, packets
**T**ransport (Layer 4) - TCP/UDP, ports, segments
**S**ession (Layer 5) - Session management, connections
**P**resentation (Layer 6) - Data formatting, encryption
**A**pplication (Layer 7) - HTTP, FTP, SMTP, user applications

**Layer Device Memory - "HSwitch, Rout-3, Fire-3-7":**
- **Hub** operates at Layer **1** (Physical)
- **Switch** operates at Layer **2** (Data Link)
- **Router** operates at Layer **3** (Network)
- **Firewall** operates at Layer **3-7** (Network to Application)

**TCP vs UDP - "Reliable vs Rapid":**

**TCP (Transmission Control Protocol)** = **"The Careful Protocol"**
- **C**onnection-oriented
- **A**cknowledgments required
- **R**eliable delivery
- **E**rror checking
- **S**low but sure

**UDP (User Datagram Protocol)** = **"The Uncaring Deliverer Protocol"**
- **U**nreliable (no guarantees)
- **D**atagram (fire and forget)
- **P**erformance over reliability (fast!)

**When to use:**
- **TCP** = Email, file transfer, web (HTTPS) - "**C**an't **L**ose **D**ata"
- **UDP** = Streaming, gaming, DNS - "**S**peed **O**ver **R**eliability"

**Common Port Numbers - "The Essential Dozen":**
```
20/21   FTP     "**2** ports for **FTP**"
22      SSH     "**2**wo **2**wos = **22** SSH"
23      Telnet  "**23** = Old and insecure"
25      SMTP    "**25** sends mail"
53      DNS     "**5**3 = DNS (Domain Name **S**ystem)"
80      HTTP    "**80** = **8**0s internet (plain web)"
110     POP3    "**110** = **P**ick up mail (P = 110)"
143     IMAP    "**143** = **I** **M**anage email (**I**MAP)"
443     HTTPS   "**443** = **4** letters (HTTP) + **S** = secure web"
3389    RDP     "**3389** = **3** + **8** + **9** = **20** (Remote **20**20 vision - Desktop)"
```

**Firewall Rule Order - "FILO":**
**F**irst **I**n, **L**ast **O**ut
- Rules processed **top to bottom**
- **First matching rule wins**
- **Default deny** at bottom

**Network Security Devices - "FINDS":**
**F**irewall - Blocks/allows based on rules
**I**DS/IPS - Detects/prevents intrusions
**N**AC - Network Access Control
**D**LP - Data Loss Prevention
**S**IEM - Security Information and Event Management

**Three-Way Handshake (TCP) - "SYN, SYN-ACK, ACK":**
```
Client → [SYN] → Server          "Let's talk?"
Client ← [SYN-ACK] ← Server      "Sure, ready!"
Client → [ACK] → Server          "Great, here's data"
```

**Mnemonic:** "**S**ome **Y**oung **N**erd **S**ent **Y**ou **N**ew **A**wesome **C**ode **K**ind **A**cknowledgment, **C**ool **K**eepsake"

**Visual Memory Aid - Where Attacks Happen:**
```
Layer 7 (Application) ← SQL Injection, XSS, CSRF
Layer 4 (Transport)   ← SYN Flood, Port Scanning
Layer 3 (Network)     ← IP Spoofing, ICMP Flood
Layer 2 (Data Link)   ← ARP Poisoning, MAC Flooding
Layer 1 (Physical)    ← Cable cutting, Jamming
```

**Quick Recall Test:**
Q: Attacker performs ARP poisoning. Which OSI layer?
A: **Layer 2 (Data Link)** - ARP operates at MAC address level

Q: You need reliable file transfer. TCP or UDP?
A: **TCP** - file transfer requires guaranteed delivery"""
    },

    "lesson_fundamentals_06_cia_triad_RICH.json": {
        "text": """**Memory Aid: CIA Triad - "Confidential Integrity Available"**

The three pillars of information security:

**C**onfidentiality - Keep data private (only authorized access)
**I**ntegrity - Keep data accurate (prevent unauthorized modification)
**A**vailability - Keep data accessible (systems up and running)

**Mnemonic:** "**C**an **I**nformation be **A**ccessed correctly and safely?"

**Confidentiality Controls - "EACL":**
**E**ncryption (AES, RSA)
**A**ccess controls (RBAC, ACLs)
**C**lassification (Top Secret, Confidential, Public)
**L**east privilege (minimum necessary access)

**Integrity Controls - "HAVOC":**
**H**ashing (SHA-256 verify data hasn't changed)
**A**ccess controls (prevent unauthorized modification)
**V**ersioning (track changes, rollback if needed)
**O**peration logging (audit trails)
**C**hecksums (detect corruption)

**Availability Controls - "RBFD":**
**R**edundancy (backup systems)
**B**ackups (regular data backups)
**F**ailover (automatic switchover to backup)
**D**DOS protection (prevent availability attacks)

**Visual Memory Aid - The Security Triangle:**
```
           Confidentiality
                 △
                ╱ ╲
               ╱   ╲
              ╱  CIA ╲
             ╱ Triad  ╲
            ╱─────────╲
    Integrity         Availability
```

**Attack Type by CIA Impact:**
- **Confidentiality** breach = Data leak, eavesdropping, theft
  - Example: Password database stolen
- **Integrity** breach = Data tampering, unauthorized modification
  - Example: Malware modifying system files
- **Availability** breach = DoS, ransomware, system destruction
  - Example: DDoS takes website offline

**Related Concepts - "CIA's Friends: AAA":**
**A**uthentication - Verify identity ("Who are you?")
**A**uthorization - Grant permissions ("What can you do?")
**A**ccounting - Track actions ("What did you do?")

**Confidentiality vs Privacy:**
- **Confidentiality** = Protecting **data** from unauthorized access
- **Privacy** = Protecting **personal information** rights
- **Remember:** "Confidentiality is technical, Privacy is legal"

**Real-World Examples:**
```
Healthcare:
  C = Patient medical records encrypted
  I = Medical records cannot be altered without authorization
  A = Doctors can access records 24/7

Banking:
  C = Account balances kept secret from other customers
  I = Transaction records protected from tampering
  A = ATMs and online banking available 24/7

Military:
  C = Classified information protected (Top Secret clearance)
  I = Orders and intelligence cannot be forged
  A = Command and control systems always operational
```

**Quick Recall Test:**
Q: Ransomware encrypts all company files. Which CIA principle is violated?
A: **Availability** - data exists but cannot be accessed

Q: Attacker intercepts and reads email traffic. Which CIA principle is violated?
A: **Confidentiality** - unauthorized access to private data

Q: Attacker modifies DNS records to redirect traffic. Which CIA principle is violated?
A: **Integrity** - data has been tampered with"""
    },

    "lesson_dfir_02_incident_response_RICH.json": {
        "text": """**Memory Aid: Incident Response Process - "PICERL"**

Remember the six phases of incident response with **PICERL** (pronounced "pickle"):

**P**reparation - Set up tools, processes, and team before incidents
**I**dentification - Detect and confirm security incidents
**C**ontainment - Limit damage and prevent spread
**E**radication - Remove threat from environment
**R**ecovery - Restore systems to normal operations
**L**essons Learned - Post-incident analysis and improvement

**Detailed Mnemonic: "Please Investigate Carefully, Eradicate Rapidly, Learn"**

**Containment Types - "SSH":**
**S**hort-term containment - Quick isolation (network isolation, account disable)
**S**ystem backup - Preserve evidence before eradication
**H**ard containment - Long-term isolation (rebuild systems, patch vulnerabilities)

**Order of Volatility (Data Collection) - "RAM CRASHD":**
**R**egisters & Cache
**A**ctive network connections
**M**emory (RAM)
**C**ommand history
**R**unning processes
**A**rtifacts (event logs, registry)
**S**wap/page files
**H**ard drive/Disk
**D**ata backups

**Severity Levels - "CLIMT":**
**C**ritical - Immediate threat to business operations
**L**ow - Minimal impact
**I**nformation - FYI, no action needed
**M**edium - Moderate impact
**T**ime-sensitive - High impact

**Communication During IR - "SWAT Team":**
**S**takeholders - Keep leadership informed
**W**orkforce - Internal communication
**A**uthorities - Law enforcement if needed
**T**echnical team - Coordinate response actions

**Visual Memory Aid:**
```
INCIDENT OCCURS
      ↓
[P] Preparation ← (Done before incident)
      ↓
[I] Identification ← "What happened?"
      ↓
[C] Containment ← "Stop the bleeding"
      ↓
[E] Eradication ← "Remove the threat"
      ↓
[R] Recovery ← "Back to normal"
      ↓
[L] Lessons Learned ← "How do we prevent this?"
```

**Quick Recall:** You detect ransomware encrypting files. What's your PICERL action order?
- **I**dentify: Confirm ransomware variant
- **C**ontain: Isolate infected systems from network
- **E**radicate: Remove malware, check for persistence
- **R**ecover: Restore from clean backups
- **L**earn: Review how ransomware entered, improve defenses"""
    },

    "lesson_dfir_04_disk_forensics_file_systems_RICH.json": {
        "text": """**Memory Aid: Order of Volatility - "RAM CRASHD"**

When collecting forensic evidence, remember the order from most to least volatile with **RAM CRASHD**:

**R**egisters & CPU Cache
**A**ctive network connections & ARP cache
**M**emory (RAM)
**C**ommand history (bash_history, PowerShell history)
**R**unning processes & loaded modules
**A**rtifacts (event logs, registry, temp files)
**S**wap/Page files
**H**ard drive / Disk
**D**ata backups & archives

**Mnemonic:** "**R**acing **A**gainst **M**emory loss, **C**ollect **R**apidly **A**ll **S**ystem **H**istory **D**ata"

**NTFS Forensic Artifacts - "MUFT":**
**M**FT ($MFT) - Master File Table (all file metadata)
**U**SN Journal ($UsnJrnl) - File system change log
**F**ile names ($I30) - Directory indexes
**T**imestamps (MACB) - Modified, Accessed, Changed, Birth

**MACB Timestamps Memory - "Make A Change, Baby":**
**M**odified (M) - File content changed
**A**ccessed (A) - File was read
**C**hanged (C) - Metadata changed (rename, permissions)
**B**irth (B) - File created (Born)

**File Signature Memory - Magic Bytes:**
- **PDF** = `%PDF` (25 50 44 46)
- **ZIP** = `PK` (50 4B)
- **JPEG** = `FF D8 FF`
- **PNG** = `89 50 4E 47`
- **EXE** = `MZ` (4D 5A)

**Remember:** "**P**lease **K**eep **M**agic **Z**ips" for common signatures

**Alternate Data Streams (ADS) - The Hidden Files:**
- Normal file: `file.txt`
- Hidden stream: `file.txt:hidden.exe`
- **Memory hook:** "**ADS** = **A**lternate **D**ata = **S**ecret data hidden"

**Slack Space Types - "FR":**
**F**ile slack - Unused space between end of file and end of cluster
**R**AM slack - Unused space between end of file and end of sector

**Visual Memory Aid - Disk Structure:**
```
┌─────────────────────────────────────┐
│  MBR (Master Boot Record)           │ ← Sector 0
├─────────────────────────────────────┤
│  Partition Table                    │
├─────────────────────────────────────┤
│  Boot Sector (VBR)                  │
├─────────────────────────────────────┤
│  $MFT (Master File Table)           │ ← File metadata
├─────────────────────────────────────┤
│  File System Data                   │
│  (Your files and folders)           │
└─────────────────────────────────────┘
```

**Forensic Tool Memory - "FASTE":**
**F**TK (Forensic Toolkit)
**A**utopsy (Open source)
**S**leuth Kit (Command line)
**T**SK (The Sleuth Kit utilities)
**E**nCase (Commercial)

**Quick Recall:** You find a suspicious file named `document.pdf:malware.exe`. What forensic concept is this?
Answer: **Alternate Data Stream (ADS)** - hiding malware in ADS of PDF file"""
    },

    "lesson_fundamentals_04_network_security_RICH.json": {
        "text": """**Memory Aid: OSI Model - "Please Do Not Throw Sausage Pizza Away"**

Remember the 7 layers of the OSI model from Layer 1 to Layer 7:

**P**hysical (Layer 1) - Cables, electrical signals, bits
**D**ata Link (Layer 2) - MAC addresses, switches, frames
**N**etwork (Layer 3) - IP addresses, routers, packets
**T**ransport (Layer 4) - TCP/UDP, ports, segments
**S**ession (Layer 5) - Session management, connections
**P**resentation (Layer 6) - Data formatting, encryption
**A**pplication (Layer 7) - HTTP, FTP, SMTP, user applications

**Layer Device Memory - "HSwitch, Rout-3, Fire-3-7":**
- **Hub** operates at Layer **1** (Physical)
- **Switch** operates at Layer **2** (Data Link)
- **Router** operates at Layer **3** (Network)
- **Firewall** operates at Layer **3-7** (Network to Application)

**TCP vs UDP - "Reliable vs Rapid":**

**TCP (Transmission Control Protocol)** = **"The Careful Protocol"**
- **C**onnection-oriented
- **A**cknowledgments required
- **R**eliable delivery
- **E**rror checking
- **S**low but sure

**UDP (User Datagram Protocol)** = **"The Uncaring Deliverer Protocol"**
- **U**nreliable (no guarantees)
- **D**atagram (fire and forget)
- **P**erformance over reliability (fast!)

**Common Port Numbers - "The Essential Dozen":**
```
20/21   FTP     "2 ports for FTP"
22      SSH     "Two 2wos = 22 SSH"
23      Telnet  "23 = Old and insecure"
25      SMTP    "25 sends mail"
53      DNS     "53 = DNS (Domain Name System)"
80      HTTP    "80 = 80s internet (plain web)"
110     POP3    "110 = Pick up mail (P = 110)"
143     IMAP    "143 = I Manage email (IMAP)"
443     HTTPS   "443 = 4 letters (HTTP) + S = secure web"
3389    RDP     "3389 = 3 + 8 + 9 = 20 (Remote 2020 vision - Desktop)"
```

**Three-Way Handshake (TCP) - "SYN, SYN-ACK, ACK":**
```
Client → [SYN] → Server          "Let's talk?"
Client ← [SYN-ACK] ← Server      "Sure, ready!"
Client → [ACK] → Server          "Great, here's data"
```

**Visual Memory Aid - Where Attacks Happen:**
```
Layer 7 (Application) ← SQL Injection, XSS, CSRF
Layer 4 (Transport)   ← SYN Flood, Port Scanning
Layer 3 (Network)     ← IP Spoofing, ICMP Flood
Layer 2 (Data Link)   ← ARP Poisoning, MAC Flooding
Layer 1 (Physical)    ← Cable cutting, Jamming
```

**Quick Recall Test:**
Q: Attacker performs ARP poisoning. Which OSI layer?
A: **Layer 2 (Data Link)** - ARP operates at MAC address level

Q: You need reliable file transfer. TCP or UDP?
A: **TCP** - file transfer requires guaranteed delivery"""
    },

    "lesson_fundamentals_05_cia_triad_security_principles_RICH.json": {
        "text": """**Memory Aid: CIA Triad - "Confidential Integrity Available"**

The three pillars of information security:

**C**onfidentiality - Keep data private (only authorized access)
**I**ntegrity - Keep data accurate (prevent unauthorized modification)
**A**vailability - Keep data accessible (systems up and running)

**Mnemonic:** "**C**an **I**nformation be **A**ccessed correctly and safely?"

**Confidentiality Controls - "EACL":**
**E**ncryption (AES, RSA)
**A**ccess controls (RBAC, ACLs)
**C**lassification (Top Secret, Confidential, Public)
**L**east privilege (minimum necessary access)

**Integrity Controls - "HAVOC":**
**H**ashing (SHA-256 verify data hasn't changed)
**A**ccess controls (prevent unauthorized modification)
**V**ersioning (track changes, rollback if needed)
**O**peration logging (audit trails)
**C**hecksums (detect corruption)

**Availability Controls - "RBFD":**
**R**edundancy (backup systems)
**B**ackups (regular data backups)
**F**ailover (automatic switchover to backup)
**D**DOS protection (prevent availability attacks)

**Visual Memory Aid - The Security Triangle:**
```
           Confidentiality
                 △
                ╱ ╲
               ╱   ╲
              ╱  CIA ╲
             ╱ Triad  ╲
            ╱─────────╲
    Integrity         Availability
```

**Attack Type by CIA Impact:**
- **Confidentiality** breach = Data leak, eavesdropping, theft
  - Example: Password database stolen
- **Integrity** breach = Data tampering, unauthorized modification
  - Example: Malware modifying system files
- **Availability** breach = DoS, ransomware, system destruction
  - Example: DDoS takes website offline

**Related Concepts - "CIA's Friends: AAA":**
**A**uthentication - Verify identity ("Who are you?")
**A**uthorization - Grant permissions ("What can you do?")
**A**ccounting - Track actions ("What did you do?")

**Quick Recall Test:**
Q: Ransomware encrypts all company files. Which CIA principle is violated?
A: **Availability** - data exists but cannot be accessed

Q: Attacker intercepts and reads email traffic. Which CIA principle is violated?
A: **Confidentiality** - unauthorized access to private data

Q: Attacker modifies DNS records to redirect traffic. Which CIA principle is violated?
A: **Integrity** - data has been tampered with"""
    },

    "lesson_fundamentals_06_common_vulnerabilities_owasp_top_10_RICH.json": {
        "text": """**Memory Aid: OWASP Top 10 (2021) - "BAC IS SLICK SS"**

Remember the OWASP Top 10 web vulnerabilities with this mnemonic:

**B**roken Access Control (A01)
**A**uthentication Failures (A02 - Cryptographic failures)
**C**ryptographic Failures (A02)
**I**njection (A03 - SQL, XSS, Command)
**S**ecurity Misconfiguration (A05)

**S**oftware/Data Integrity Failures (A08)
**L**ogging & Monitoring Failures (A09)
**I**nsecure Design (A04)
**C**omponent Vulnerabilities (A06 - Vulnerable components)
**K**nown Vulnerable Components (A06)

**S**SRF (A10 - Server-Side Request Forgery)
**S**oftware Supply Chain (A08)

**The Critical Three - "ISS":**
1. **I**njection (SQL, XSS, Command) - #3
2. **S**ecurity Misconfiguration - #5
3. **S**ensitive Data Exposure (Crypto failures) - #2

**SQL Injection Memory - "OR 1=1":**
Classic SQLi: `' OR '1'='1`
**Mnemonic:** "**O**ne **R**eally dumb vulnerability equals **1** = **1** (always true)"

**Impact:** Database bypass, data theft, database destruction

**XSS Types - "SRD":**
**S**tored XSS - Malicious script stored in database (most dangerous)
**R**eflected XSS - Malicious script in URL, reflected back
**D**OM XSS - Client-side JavaScript manipulation

**Remember:** "**S**tored is **S**evere, **R**eflected is **R**epeated, **D**OM is **D**angerous"

**CSRF Attack - "Sea-Surf":**
**C**ross-**S**ite **R**equest **F**orgery
- Tricks user's browser into making unauthorized requests
- **Defense:** CSRF tokens (random value per session)

**Authentication Failures - "WWPS":**
**W**eak passwords allowed
**W**eak credential recovery
**P**lain text password storage
**S**ession fixation vulnerabilities

**Access Control Failures - "PIED":**
**P**ath traversal (../../etc/passwd)
**I**nsecure Direct Object References (IDOR)
**E**levation of privilege
**D**efault credentials not changed

**Visual - SQL Injection:**
```
Normal query:  SELECT * FROM users WHERE id = $id
Malicious:     SELECT * FROM users WHERE id = 1 OR 1=1; DROP TABLE users;--

Result: Returns all users, then deletes users table
```

**Defense Mnemonic - "VALIDATE":**
**V**alidate all input
**A**uthenticate properly
**L**imit privileges (least privilege)
**I**mage/file type checking
**D**isable unnecessary features
**A**pply security patches
**T**est for vulnerabilities
**E**ncrypt sensitive data

**CVE Scoring (CVSS) - "LMH-C":**
- **L**ow (0.1-3.9) - Minimal risk
- **M**edium (4.0-6.9) - Moderate risk
- **H**igh (7.0-8.9) - Serious risk
- **C**ritical (9.0-10.0) - Emergency patching required

**Quick Recall:**
Q: Attacker submits `'; DROP TABLE users;--` in login form. What vulnerability?
A: **SQL Injection** (A03)

Q: Website allows users to view any file by changing URL parameter from `file=invoice.pdf` to `file=../../etc/passwd`. What vulnerability?
A: **Broken Access Control** (A01) - specifically Path Traversal"""
    }
}

def add_memory_aid_block(lesson_data, filename):
    """Add relevant memory aid block to a lesson."""

    if filename not in MEMORY_AIDS:
        return False, "No memory aid content defined for this lesson"

    # Check if memory aid already exists
    for block in lesson_data.get("content_blocks", []):
        if block.get("type") == "memory_aid":
            return False, "Lesson already has memory aid block"

    # Get the memory aid content
    memory_aid_content = MEMORY_AIDS[filename]

    # Create the memory aid block
    memory_aid_block = {
        "type": "memory_aid",
        "content": memory_aid_content
    }

    # Insert before reflection block or at end
    content_blocks = lesson_data.get("content_blocks", [])
    insert_index = len(content_blocks)

    for i, block in enumerate(content_blocks):
        if block.get("type") == "reflection":
            insert_index = i
            break

    content_blocks.insert(insert_index, memory_aid_block)
    lesson_data["content_blocks"] = content_blocks

    return True, f"Added memory aid block at position {insert_index + 1}"

def main():
    content_dir = Path("content")
    modified_count = 0
    skipped_count = 0

    print("=" * 80)
    print("ADD MEMORY AIDS TO LESSONS")
    print("=" * 80)
    print()

    for filename in MEMORY_AIDS.keys():
        filepath = content_dir / filename

        if not filepath.exists():
            print(f"[SKIP] {filename}: File not found")
            skipped_count += 1
            continue

        # Load lesson
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)

        # Add memory aid
        success, message = add_memory_aid_block(lesson_data, filename)

        if success:
            # Save updated lesson
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lesson_data, f, indent=2, ensure_ascii=False)

            print(f"[OK] {filename}")
            print(f"     Title: {lesson_data.get('title', 'Unknown')}")
            print(f"     {message}")
            print()
            modified_count += 1
        else:
            print(f"[SKIP] {filename}: {message}")
            skipped_count += 1

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Lessons modified: {modified_count}")
    print(f"Lessons skipped: {skipped_count}")
    print()

    if modified_count > 0:
        print("Next steps:")
        print("1. python -m scripts.update_outdated_lessons    # Update database")
        print("2. python -m scripts.validate_lesson_compliance  # Verify changes")
        print("3. python -m scripts.update_template_database    # Sync template")

if __name__ == "__main__":
    main()
