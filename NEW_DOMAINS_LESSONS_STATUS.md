# New Domains Lessons - Creation Status

## Completed Lessons (1 of 6)

### ✅ System Domain
1. **Windows System Internals Fundamentals** (lesson_system_01_windows_internals_RICH.json) - ✅ COMPLETE
   - 5,000+ words of professional content
   - Covers: Processes, Services, Registry, File System, Privileges, User Accounts
   - Real-world examples: PrintNightmare, persistence hunting
   - Attack vectors and defense strategies
   - PowerShell commands and hardening checklist

## Lessons to Create (5 remaining)

### System Domain (2 more lessons needed)

**2. Linux System Fundamentals** (Priority: HIGH)
- File system hierarchy (/etc, /var, /home, /root)
- Users and groups (/etc/passwd, /etc/shadow, /etc/group)
- Permissions (chmod, chown, umask)
- Processes (ps, top, kill, systemd)
- Services (systemctl, systemd units)
- Package management (apt, yum, dnf)
- Logs (/var/log/*, journalctl)
- SSH and remote access
- sudo and privilege management
- Common attack vectors and hardening

**3. Privilege Escalation Fundamentals** (Priority: MEDIUM)
- Windows privilege escalation techniques
- Linux privilege escalation techniques
- SUID/SGID binaries
- Weak service permissions
- Unquoted service paths
- DLL hijacking
- Kernel exploits
- Sudo misconfigurations
- Credential harvesting
- Detection and prevention

### Cloud Domain (3 lessons needed)

**4. Cloud Security Fundamentals** (Priority: HIGH)
- Cloud computing models (IaaS, PaaS, SaaS)
- Shared responsibility model
- Cloud vs on-prem security differences
- Major cloud providers (AWS, Azure, GCP)
- Common cloud security risks
- Cloud-native security controls
- Compliance in the cloud
- Cloud security best practices

**5. IAM Basics - Identity and Access Management** (Priority: HIGH)
- IAM fundamentals
- Users, groups, roles
- Policies and permissions
- Least privilege in cloud
- MFA and conditional access
- Service accounts vs user accounts
- IAM best practices
- Common misconfigurations
- AWS IAM, Azure AD, GCP IAM
- Attack vectors and defense

**6. AWS Security Essentials** (Priority: MEDIUM)
- AWS security services (GuardDuty, Security Hub, IAM)
- VPC and network security (security groups, NACLs)
- S3 bucket security (common misconfigurations)
- EC2 instance security
- CloudTrail for logging
- AWS Config for compliance
- Secrets Manager
- Key Management Service (KMS)
- Common AWS attacks
- Security best practices

## Quick Creation Guide

### Using the Content Generator

```bash
# For each lesson above:
python create_rich_lesson.py --interactive

# When prompted, use the information from this file:
# - Title: [As listed above]
# - Domain: system or cloud
# - Difficulty: 1 for fundamentals, 2 for intermediate
# - Concepts: [Listed in each lesson description]
```

### Alternative: Batch Generation

Create file: `generate_new_domain_lessons.json`

```json
[
  {
    "title": "Linux System Fundamentals",
    "domain": "system",
    "difficulty": 1,
    "order_index": 2,
    "concepts": ["File system", "Users", "Permissions", "Processes", "Services"]
  },
  {
    "title": "Privilege Escalation Fundamentals",
    "domain": "system",
    "difficulty": 2,
    "order_index": 3,
    "concepts": ["Windows privesc", "Linux privesc", "SUID", "Weak permissions"]
  },
  {
    "title": "Cloud Security Fundamentals",
    "domain": "cloud",
    "difficulty": 1,
    "order_index": 1,
    "concepts": ["Cloud models", "Shared responsibility", "Cloud providers"]
  },
  {
    "title": "IAM Basics",
    "domain": "cloud",
    "difficulty": 1,
    "order_index": 2,
    "concepts": ["Users", "Roles", "Policies", "Permissions", "MFA"]
  },
  {
    "title": "AWS Security Essentials",
    "domain": "cloud",
    "difficulty": 2,
    "order_index": 3,
    "concepts": ["VPC", "S3", "IAM", "CloudTrail", "Security services"]
  }
]
```

Then run:
```bash
python create_rich_lesson.py --batch generate_new_domain_lessons.json
```

## What to Do Next

### Option 1: I Create Remaining Lessons
In a new conversation (to avoid token limits), ask me to create the remaining 5 lessons with the same quality as Windows Internals.

### Option 2: You Use Content Generator + AI
1. Run `create_rich_lesson.py` to generate lesson templates
2. Use the `enhance_with_ai.py` tool to get detailed prompts
3. Fill content using Claude or ChatGPT
4. Load lessons into database

### Option 3: Hybrid Approach
- I create 2-3 more high-priority lessons (Linux, Cloud Fundamentals, IAM)
- You create the remaining lessons using the generator tools

## Current Domain Status

### Complete Domains (Good Coverage):
- ✅ **Fundamentals**: 4 rich lessons
- ✅ **Active Directory**: 3 rich lessons
- ✅ **Red Team**: 2 rich lessons
- ✅ **Blue Team**: 2 rich lessons
- ✅ **Pentest**: 1 rich lesson
- ✅ **Malware**: 1 rich lesson
- ✅ **DFIR**: 1 rich lesson

### New Domains (Minimal Coverage):
- ⚠️ **System**: 1 lesson (need 2-3 more)
- ⚠️ **Cloud**: 0 lessons (need 3-4)

## Recommended Priority

1. **Cloud Security Fundamentals** - Entry point for cloud domain
2. **Linux System Fundamentals** - Balance with Windows content
3. **IAM Basics** - Critical cloud security skill
4. **AWS Security Essentials** - Most popular cloud platform
5. **Privilege Escalation** - Advanced system security

## Testing After Creation

```bash
# Fix UUIDs
python fix_rich_uuids.py

# Load all lessons
python load_all_lessons.py

# Check database
python check_database.py

# Run app
streamlit run app.py

# Verify:
# - System domain shows 1 lesson (Windows Internals)
# - Can complete Windows Internals lesson
# - Skill level updates for system domain
# - After fundamentals complete, system lessons are recommended
# - After system complete, cloud lessons are recommended (when created)
```

## Summary

**Completed**: 1 lesson (Windows System Internals - 5,000 words)
**Remaining**: 5 lessons across system and cloud domains
**Tools Ready**: Content generator, AI enhancement, batch processing
**Status**: System domain has entry point, cloud domain needs initial content

The foundation is laid with one excellent lesson. The remaining lessons can be created using the same pattern and the tools we've built.
