# CyberLearn - Next Lessons Plan

## Current Status (Based on Local Database)

**Total Lessons**: 108 lessons across 11 domains

### Lessons by Domain:

| Domain | Current Count | Target (8-12) | Status |
|--------|--------------|---------------|--------|
| **active_directory** | 11 | ✅ 8-12 | Complete |
| **blueteam** | 11 | ✅ 8-12 | Complete |
| **cloud** | 10 | ✅ 8-12 | Complete |
| **dfir** | 11 | ✅ 8-12 | Complete |
| **fundamentals** | 11 | ✅ 8-12 | Complete |
| **linux** | 13 | ✅ 8-12 | Complete+ |
| **malware** | 10 | ✅ 8-12 | Complete |
| **pentest** | 9 | ✅ 8-12 | Complete |
| **red_team** | 5 | ⚠️ 8-12 | **NEEDS 3-7 MORE** |
| **redteam** | 7 | ⚠️ 8-12 | **NEEDS 1-5 MORE** |
| **system** | 10 | ✅ 8-12 | Complete |
| **osint** | 0 (5 ready) | ❌ 8-12 | **NOT LOADED + NEEDS 3-7 MORE** |
| **threat_hunting** | 0 | ❌ 8-12 | **NOT CREATED - NEEDS 8-12** |

### Issues to Address:

1. **red_team vs redteam** - Two separate domains with same content (should consolidate)
2. **OSINT lessons not loaded** - 5 lessons created but not in database
3. **Threat Hunting domain** - Infrastructure exists but NO lessons created yet

---

## Priority 1: Fix OSINT Domain (IMMEDIATE)

**Status**: 5 lessons created with unique UUIDs, not yet loaded into database

### Action Required:

On your VM, run:
```bash
python reload_osint_simple.py
```

This will add 5 OSINT lessons:
1. OSINT Fundamentals & Ethics
2. Google Dorking & Search Mastery
3. Social Media Intelligence (SOCMINT)
4. DNS & Infrastructure OSINT
5. Shodan & IoT Search

**After loading, OSINT will have 5/8-12 lessons (needs 3-7 more)**

---

## Priority 2: Create Remaining OSINT Lessons (5 more)

### Suggested OSINT Lessons 6-10:

**6. Email & Username Intelligence (OSINT 6)**
- **Difficulty**: 2 (Intermediate)
- **Content**:
  - Email format enumeration (Hunter.io, RocketReach)
  - Username OSINT (Sherlock, WhatsMyName, Namechk)
  - Have I Been Pwned integration
  - Email header analysis and tracking
  - Disposable email detection
  - Professional email intelligence (LinkedIn Sales Navigator)
- **Real-world**: Phishing campaign reconnaissance case study
- **Estimated Time**: 50 min

**7. Image & Geolocation Intelligence (OSINT 7)**
- **Difficulty**: 2 (Intermediate)
- **Content**:
  - EXIF metadata extraction (ExifTool)
  - Reverse image search (Google, TinEye, Yandex)
  - Geolocation from photos (GPS coordinates, landmarks)
  - Google Earth Pro for OSINT
  - Shadow analysis and sun position
  - Social media geolocation (Instagram, Twitter)
  - SunCalc and other geolocation tools
- **Real-world**: Bellingcat geolocation investigations
- **Estimated Time**: 55 min

**8. Maltego & Relationship Mapping (OSINT 8)**
- **Difficulty**: 3 (Advanced)
- **Content**:
  - Maltego fundamentals and transforms
  - Entity relationship mapping
  - Infrastructure correlation (domains, IPs, emails)
  - Social network analysis
  - Custom transform development
  - Graph analysis techniques
  - Export and reporting
- **Real-world**: APT infrastructure mapping
- **Hands-on**: Complete infrastructure investigation lab
- **Estimated Time**: 60 min

**9. Dark Web & Paste Site Monitoring (OSINT 9)**
- **Difficulty**: 3 (Advanced)
- **Content**:
  - Tor Browser setup and safety
  - Dark web search engines (Ahmia, Torch)
  - Underground forums and markets (research only)
  - Paste site monitoring (Pastebin, GitHub Gists)
  - Breach monitoring and data leak detection
  - OPSEC for dark web research
  - Legal and ethical boundaries
- **Real-world**: Credential leak detection case study
- **Estimated Time**: 60 min

**10. OSINT Automation & Tool Integration (OSINT 10)**
- **Difficulty**: 3 (Advanced)
- **Content**:
  - Recon-ng framework
  - SpiderFoot automation
  - TheHarvester for email/subdomain enumeration
  - OSINT Framework overview
  - Custom Python OSINT scripts
  - API integration (Shodan, Hunter.io, VirusTotal)
  - CI/CD for continuous OSINT monitoring
  - Building an OSINT dashboard
- **Real-world**: Automated threat intelligence pipeline
- **Hands-on**: Build custom OSINT workflow
- **Estimated Time**: 60 min

---

## Priority 3: Create Threat Hunting Domain (10 lessons)

**Status**: Domain infrastructure exists (adaptive_engine.py, user.py, UI tabs), but NO lessons created

### Suggested Threat Hunting Lessons 1-10:

**1. Threat Hunting Fundamentals (TH 1)**
- **Difficulty**: 1 (Beginner)
- **Content**:
  - Threat hunting vs detection engineering
  - Hypothesis-driven hunting
  - MITRE ATT&CK framework for hunters
  - Hunt metrics and ROI
  - Building a threat hunting program
  - Hunt team structure and responsibilities
- **Estimated Time**: 45 min

**2. Threat Hunting Methodologies (TH 2)**
- **Difficulty**: 2 (Intermediate)
- **Content**:
  - Crown Jewels Analysis
  - TTP-based hunting (Tactics, Techniques, Procedures)
  - Indicator-based hunting vs behavior-based hunting
  - Hunt loop: Hypothesis → Data → Analysis → Detection
  - Structured vs unstructured hunting
  - Hunt documentation and playbooks
- **Real-world**: Ransomware hunt playbook
- **Estimated Time**: 50 min

**3. Windows Event Log Analysis for Hunters (TH 3)**
- **Difficulty**: 2 (Intermediate)
- **Content**:
  - Critical Windows Event IDs (4624, 4625, 4688, 4720, etc.)
  - Sysmon configuration and event analysis
  - PowerShell logging (Module, ScriptBlock, Transcription)
  - Lateral movement detection in logs
  - Credential dumping indicators
  - Parsing logs with PowerShell and Python
- **Real-world**: Detecting Mimikatz via event logs
- **Hands-on**: Hunt lab with simulated attacks
- **Estimated Time**: 60 min

**4. Network Traffic Analysis for Threat Hunting (TH 4)**
- **Difficulty**: 2 (Intermediate)
- **Content**:
  - Zeek (Bro) log analysis
  - C2 beacon detection
  - DNS tunneling and exfiltration detection
  - TLS/SSL certificate anomalies
  - Network flow analysis (NetFlow, IPFIX)
  - Cobalt Strike and Metasploit C2 patterns
- **Real-world**: APT29 C2 detection
- **Estimated Time**: 60 min

**5. Memory Forensics for Threat Hunting (TH 5)**
- **Difficulty**: 3 (Advanced)
- **Content**:
  - Volatility 3 for live hunting
  - In-memory malware detection
  - Process injection hunting
  - Fileless malware indicators
  - Hunting persistence mechanisms
  - Memory dump acquisition from live systems
- **Real-world**: Fileless ransomware hunt
- **Estimated Time**: 60 min

**6. Endpoint Detection & Response (EDR) for Hunters (TH 6)**
- **Difficulty**: 2 (Intermediate)
- **Content**:
  - EDR platforms overview (CrowdStrike, Carbon Black, Defender ATP)
  - Writing custom detection rules
  - Behavioral analysis with EDR
  - Process tree analysis
  - EDR query languages (KQL, Splunk SPL)
  - Hunting at scale with EDR
- **Real-world**: Living-off-the-land (LOLBin) detection
- **Hands-on**: Hunt lab with EDR platform
- **Estimated Time**: 55 min

**7. Threat Intelligence for Hunting (TH 7)**
- **Difficulty**: 2 (Intermediate)
- **Content**:
  - Integrating IOCs into hunts
  - TIP (Threat Intelligence Platform) usage
  - STIX/TAXII feeds
  - Automated IOC enrichment
  - Threat actor profiling for hunters
  - Creating custom threat intel from hunts
- **Real-world**: APT attribution via TTP analysis
- **Estimated Time**: 50 min

**8. Advanced Persistent Threat (APT) Hunting (TH 8)**
- **Difficulty**: 3 (Advanced)
- **Content**:
  - APT lifecycle and dwell time reduction
  - Long-term persistence detection
  - Lateral movement paths
  - Data staging and exfiltration detection
  - APT case studies (APT29, APT28, Lazarus)
  - Hunt cadence for APT detection
- **Real-world**: SolarWinds supply chain attack hunt
- **Estimated Time**: 60 min

**9. SIEM & Data Lake Hunting (TH 9)**
- **Difficulty**: 3 (Advanced)
- **Content**:
  - Splunk hunting queries (SPL)
  - ELK Stack hunting (Elasticsearch queries)
  - Sigma rule creation for hunters
  - Statistical anomaly detection
  - Machine learning for hunting
  - Hunt dashboards and visualizations
- **Real-world**: Building a hunt analytics platform
- **Hands-on**: Create custom hunt dashboard
- **Estimated Time**: 60 min

**10. Purple Team Threat Hunting Exercises (TH 10)**
- **Difficulty**: 3 (Advanced)
- **Content**:
  - Purple team methodology
  - Adversary emulation for hunt validation
  - Detection gap analysis
  - Hunt maturity model
  - Measuring hunt effectiveness
  - Building a continuous hunt program
  - Red team feedback loop
- **Real-world**: Full purple team exercise
- **Hands-on**: Simulated APT hunt with red team
- **Estimated Time**: 60 min

---

## Priority 4: Consolidate Red Team Domains

**Issue**: Two separate domains exist:
- `red_team` (5 lessons)
- `redteam` (7 lessons)

### Recommended Action:

1. **Decide on single naming convention**: `red_team` (with underscore) to match other domains
2. **Merge lessons** into single domain
3. **Update database** to consolidate
4. **Add 1-5 more lessons** to reach 8-12 target

### Suggested Additional Red Team Lessons:

**Red Team 11: Cloud Red Teaming**
- AWS/Azure/GCP attack paths
- Cloud misconfigurations exploitation
- Serverless exploitation
- Container escape techniques

**Red Team 12: Active Directory Red Teaming**
- Kerberoasting at scale
- DCSync attacks
- AD CS exploitation
- Trust relationship abuse

---

## Priority 5: Expand Smaller Domains (Optional)

While most domains meet the 8-12 lesson target, you could expand:

### Pentest Domain (currently 9, could add 1-3 more):
- **API Penetration Testing Advanced**
- **Mobile Application Penetration Testing**
- **IoT Penetration Testing**

### System Domain (currently 10, could add 1-2 more):
- **macOS Internals for Security**
- **Container Security Deep Dive**

---

## Recommended Execution Order

### Phase 1: Fix Immediate Issues (Week 1)
1. ✅ **Load OSINT lessons** (run `reload_osint_simple.py`) - DONE
2. Create **OSINT lessons 6-10** (5 more lessons)
3. **Result**: OSINT domain complete with 10 lessons

### Phase 2: Create Threat Hunting Domain (Week 2-3)
1. Create **Threat Hunting lessons 1-5** (fundamentals through memory forensics)
2. Create **Threat Hunting lessons 6-10** (EDR through purple team)
3. **Result**: Threat Hunting domain complete with 10 lessons

### Phase 3: Consolidate Red Team (Week 4)
1. Audit red_team vs redteam lessons
2. Merge into single `red_team` domain
3. Create 1-5 additional lessons to reach 12 total
4. **Result**: Unified Red Team domain with 12 lessons

### Phase 4: Polish & Expand (Ongoing)
1. Review all lessons for consistency
2. Add video embeds where missing
3. Enhance hands-on labs
4. Expand domains that need 1-2 more lessons

---

## Total Work Estimate

| Task | Lessons | Estimated Time |
|------|---------|---------------|
| OSINT 6-10 | 5 lessons | 20-25 hours |
| Threat Hunting 1-10 | 10 lessons | 40-50 hours |
| Red Team consolidation + new | 3-5 lessons | 12-20 hours |
| **TOTAL** | **18-20 lessons** | **72-95 hours** |

---

## Final Target State

After completing all priorities:

| Domain | Lessons | Status |
|--------|---------|--------|
| active_directory | 11 | ✅ |
| blueteam | 11 | ✅ |
| cloud | 10 | ✅ |
| dfir | 11 | ✅ |
| fundamentals | 11 | ✅ |
| linux | 13 | ✅ |
| malware | 10 | ✅ |
| **osint** | **10** | ✅ Complete |
| pentest | 9-12 | ✅ |
| **red_team** | **12** | ✅ Consolidated |
| system | 10-12 | ✅ |
| **threat_hunting** | **10** | ✅ Complete |

**Total**: ~130-140 lessons across 12 domains

---

## Next Steps

1. **Run on VM**: `python reload_osint_simple.py` to load the 5 existing OSINT lessons
2. **Verify**: `python list_lessons.py` to confirm OSINT shows 5 lessons
3. **Decide priority**: Which domain to work on next?
   - OSINT (5 more lessons to complete)
   - Threat Hunting (10 lessons from scratch)
   - Red Team consolidation (3-5 lessons)

Let me know which you'd like to tackle first!
