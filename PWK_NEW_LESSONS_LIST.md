# PWK Coverage - New Lessons Needed (Quick Reference)

## 25 New Lessons to Cover PWK Syllabus Gaps

### HIGH PRIORITY - Pentest Domain (12 lessons)

1. **Penetration Testing Report Writing**
   - Domain: pentest | Difficulty: 2 | Time: 45min

2. **Burp Suite Deep Dive for Web Application Testing**
   - Domain: pentest | Difficulty: 2 | Time: 60min

3. **Web Application Enumeration & Inspection**
   - Domain: pentest | Difficulty: 2 | Time: 50min

4. **Directory Traversal Exploitation Playbook**
   - Domain: pentest | Difficulty: 2 | Time: 45min

5. **File Inclusion Vulnerabilities: LFI and RFI**
   - Domain: pentest | Difficulty: 2-3 | Time: 60min

6. **File Upload Vulnerabilities: Complete Exploitation**
   - Domain: pentest | Difficulty: 2 | Time: 55min

7. **Vulnerability Scanning with Nessus**
   - Domain: pentest | Difficulty: 1-2 | Time: 50min

8. **Nmap Scripting Engine (NSE) for Vulnerability Detection**
   - Domain: pentest | Difficulty: 2 | Time: 55min

9. **Password Attacks: Network Services & Hash Cracking**
   - Domain: pentest | Difficulty: 2 | Time: 60min

10. **Working with Password Hashes: NTLM, Net-NTLMv2, and Relay Attacks**
    - Domain: pentest | Difficulty: 3 | Time: 60min

11. **Client-Side Attacks: Microsoft Office & Windows Library Files**
    - Domain: pentest | Difficulty: 2 | Time: 55min

12. **Antivirus Evasion Techniques**
    - Domain: pentest | Difficulty: 2-3 | Time: 60min

### HIGH PRIORITY - Metasploit (4 lessons)

13. **Metasploit Fundamentals & Workspace Setup**
    - Domain: pentest (or new "advanced_pentest") | Difficulty: 1-2 | Time: 50min

14. **Metasploit Payload Engineering**
    - Domain: pentest | Difficulty: 2 | Time: 55min

15. **Metasploit Post-Exploitation Operations**
    - Domain: pentest | Difficulty: 2 | Time: 60min

16. **Automating Metasploit Engagements**
    - Domain: pentest | Difficulty: 2-3 | Time: 50min

### HIGH PRIORITY - Networking/Tunneling (3 lessons)

17. **Port Forwarding and Pivoting with Linux Tools**
    - Domain: pentest | Difficulty: 2-3 | Time: 60min

18. **Port Forwarding and Pivoting with Windows Tools**
    - Domain: pentest | Difficulty: 2-3 | Time: 60min

19. **Advanced Tunneling: HTTP and DNS**
    - Domain: pentest | Difficulty: 3 | Time: 60min

### MEDIUM PRIORITY - Information Gathering (3 lessons)

20. **Passive Information Gathering & OSINT Techniques**
    - Domain: osint (expand existing) | Difficulty: 1-2 | Time: 50min

21. **Active Information Gathering: Protocol Enumeration**
    - Domain: pentest | Difficulty: 2 | Time: 55min

22. **Living off the Land: Reconnaissance with Native Tools**
    - Domain: pentest | Difficulty: 2 | Time: 50min

### MEDIUM PRIORITY - Exploit Development (2 lessons)

23. **Public Exploits: Discovery, Analysis, and Execution**
    - Domain: pentest | Difficulty: 2 | Time: 55min

24. **Fixing and Troubleshooting Exploits**
    - Domain: pentest | Difficulty: 2-3 | Time: 50min

### LOW PRIORITY - Learning Strategies (3 lessons - OPTIONAL)

25. **Effective Learning Strategies for Technical Skills**
    - Domain: fundamentals | Difficulty: 1 | Time: 40min

26. **OffSec Try Harder Methodology**
    - Domain: fundamentals | Difficulty: 1 | Time: 35min

27. **OSCP Exam Preparation & Strategies**
    - Domain: fundamentals | Difficulty: 1 | Time: 30min

---

## Domain Summary After Adding These Lessons

| Domain | Current | Add | New Total |
|--------|---------|-----|-----------|
| **pentest** | 9 | +19 | 28 lessons |
| **osint** | 5 | +1 | 6 lessons |
| **fundamentals** | 11 | +3 | 14 lessons |
| **TOTAL** | 108 | +23-27 | 131-135 lessons |

---

## Creation Priority

### Week 1-2: Core Web Testing (Lessons 1-6)
Focus on web application testing fundamentals that PWK emphasizes heavily.

### Week 3: Vulnerability Scanning & Password Attacks (Lessons 7-10)
Essential pentest skills with industry-standard tools.

### Week 4: Client-Side & AV Evasion (Lessons 11-12)
Modern initial access techniques.

### Week 5: Metasploit Mastery (Lessons 13-16)
Complete Metasploit module from PWK.

### Week 6: Networking & Pivoting (Lessons 17-19)
Advanced techniques for internal network pentesting.

### Week 7: Enhanced Reconnaissance (Lessons 20-22)
Improve existing coverage with PWK-specific techniques.

### Week 8: Exploit Skills (Lessons 23-24)
Practical exploit usage and troubleshooting.

### Optional: Learning Meta-Content (Lessons 25-27)
If you want to include OffSec's learning philosophy.

---

## Quick Start: Top 5 Most Critical Gaps

If you can only create 5 lessons immediately, start with these:

1. **Burp Suite Deep Dive** (Lesson 2) - Essential tool
2. **File Inclusion Vulnerabilities** (Lesson 5) - Major web vuln
3. **Password Attacks & Hash Cracking** (Lessons 9-10) - Critical skill
4. **Metasploit Fundamentals** (Lesson 13) - Framework basics
5. **Port Forwarding with Linux Tools** (Lesson 17) - Pivoting essential

These 5 lessons would immediately improve your PWK alignment by ~20%.

---

## File Naming Convention

Use this pattern:
```
lesson_pentest_[XX]_[topic_snake_case]_RICH.json
```

Examples:
- `lesson_pentest_10_burp_suite_deep_dive_RICH.json`
- `lesson_pentest_11_file_inclusion_lfi_rfi_RICH.json`
- `lesson_pentest_12_password_attacks_hash_cracking_RICH.json`

---

## Next Action

1. Choose which lessons to create first (recommend starting with High Priority)
2. Use CHATGPT_LESSON_PROMPT.md for each lesson
3. Generate 3-5 lessons at a time for consistency
4. Run comprehensive_fix.py after each batch
5. Load and test on VM

**Ready to start? Pick your first batch of 3-5 lessons!**
