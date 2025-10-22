# Adding "System" and "Cloud" Domains

## Overview

Adding two new domains to CyberLearn:
- **system**: Operating systems security (Windows, Linux internals, hardening, privilege escalation)
- **cloud**: Cloud security (AWS, Azure, GCP, containers, serverless, cloud-native security)

## Files That Need Updates

### 1. models/user.py

**Location**: Lines 24-58 in `SkillLevels` class

**Current code**:
```python
class SkillLevels(BaseModel):
    """Skill proficiency across cybersecurity domains (0-100 scale)"""
    fundamentals: int = Field(default=0, ge=0, le=100)
    dfir: int = Field(default=0, ge=0, le=100)
    malware: int = Field(default=0, ge=0, le=100)
    active_directory: int = Field(default=0, ge=0, le=100)
    pentest: int = Field(default=0, ge=0, le=100)
    redteam: int = Field(default=0, ge=0, le=100)
    blueteam: int = Field(default=0, ge=0, le=100)
```

**Add these lines**:
```python
    system: int = Field(default=0, ge=0, le=100)
    cloud: int = Field(default=0, ge=0, le=100)
```

**Update `get_overall_level()` method** (lines 34-45):
```python
def get_overall_level(self) -> int:
    """Calculate overall skill level across all domains"""
    skills = [
        self.fundamentals,
        self.dfir,
        self.malware,
        self.active_directory,
        self.pentest,
        self.redteam,
        self.blueteam,
        self.system,      # ADD THIS
        self.cloud        # ADD THIS
    ]
    return sum(skills) // len(skills)
```

**Update `get_weakest_domain()` method** (lines 47-58):
```python
def get_weakest_domain(self) -> str:
    """Identify domain needing most attention"""
    domain_map = {
        self.fundamentals: "fundamentals",
        self.dfir: "dfir",
        self.malware: "malware",
        self.active_directory: "active_directory",
        self.pentest: "pentest",
        self.redteam: "redteam",
        self.blueteam: "blueteam",
        self.system: "system",      # ADD THIS
        self.cloud: "cloud"          # ADD THIS
    }
    return domain_map[min(domain_map.keys())]
```

### 2. core/adaptive_engine.py

**Location**: Lines 23-31 in `__init__` method

**Current code**:
```python
self.domain_prerequisites = {
    "fundamentals": [],
    "dfir": ["fundamentals"],
    "malware": ["fundamentals"],
    "active_directory": ["fundamentals"],
    "pentest": ["fundamentals", "active_directory"],
    "redteam": ["pentest", "malware"],
    "blueteam": ["dfir", "malware"],
}
```

**Update to**:
```python
self.domain_prerequisites = {
    "fundamentals": [],
    "dfir": ["fundamentals"],
    "malware": ["fundamentals"],
    "active_directory": ["fundamentals"],
    "system": ["fundamentals"],                    # ADD THIS
    "cloud": ["fundamentals", "system"],           # ADD THIS (cloud needs system basics)
    "pentest": ["fundamentals", "active_directory"],
    "redteam": ["pentest", "malware"],
    "blueteam": ["dfir", "malware"],
}
```

**Location**: Lines 100-106 in `_select_optimal_domain` method

**Current code**:
```python
domains = [
    "fundamentals",
    "dfir",
    "malware",
    "active_directory",
    "pentest",
```

**Add to list**:
```python
domains = [
    "fundamentals",
    "dfir",
    "malware",
    "active_directory",
    "system",      # ADD THIS
    "cloud",       # ADD THIS
    "pentest",
```

**Location**: Around line 235 in `generate_diagnostic_questions` method

**Add diagnostic questions for new domains**:
```python
"system": [
    {
        "question_id": "sys_q1",
        "type": "multiple_choice",
        "question": "What is the purpose of privilege escalation in system security?",
        "options": [
            "To gain higher-level permissions on a system",
            "To reduce user access rights",
            "To encrypt system files",
            "To monitor network traffic"
        ],
        "correct_answer": 0,
        "explanation": "Privilege escalation is the act of exploiting vulnerabilities to gain elevated access to resources.",
        "difficulty": 2
    },
    {
        "question_id": "sys_q2",
        "type": "multiple_choice",
        "question": "Which Linux file controls sudo permissions?",
        "options": ["/etc/passwd", "/etc/sudoers", "/etc/shadow", "/etc/hosts"],
        "correct_answer": 1,
        "explanation": "/etc/sudoers defines which users can run commands with elevated privileges.",
        "difficulty": 2
    },
    {
        "question_id": "sys_q3",
        "type": "multiple_choice",
        "question": "What does UAC (User Account Control) do in Windows?",
        "options": [
            "Prevents all administrative actions",
            "Prompts for permission before privileged operations",
            "Encrypts user files",
            "Monitors network connections"
        ],
        "correct_answer": 1,
        "explanation": "UAC prompts users for permission or credentials before allowing privileged operations.",
        "difficulty": 2
    }
],
"cloud": [
    {
        "question_id": "cloud_q1",
        "type": "multiple_choice",
        "question": "What is the shared responsibility model in cloud security?",
        "options": [
            "Cloud provider responsible for everything",
            "Customer responsible for everything",
            "Responsibilities split between provider and customer",
            "Third-party manages all security"
        ],
        "correct_answer": 2,
        "explanation": "In cloud security, provider secures infrastructure, customer secures their data and configurations.",
        "difficulty": 2
    },
    {
        "question_id": "cloud_q2",
        "type": "multiple_choice",
        "question": "What does IAM stand for in cloud security?",
        "options": [
            "Internet Access Management",
            "Identity and Access Management",
            "Infrastructure Administration Module",
            "Integrated Alert Monitoring"
        ],
        "correct_answer": 1,
        "explanation": "IAM (Identity and Access Management) controls who can access cloud resources and what they can do.",
        "difficulty": 1
    },
    {
        "question_id": "cloud_q3",
        "type": "multiple_choice",
        "question": "What is a common security risk of misconfigured S3 buckets?",
        "options": [
            "Too much encryption",
            "Public exposure of sensitive data",
            "Excessive monitoring",
            "Too many backups"
        ],
        "correct_answer": 1,
        "explanation": "Misconfigured S3 buckets often result in unintentional public access to sensitive data.",
        "difficulty": 2
    }
],
```

### 3. Database Migration

**The database needs to be updated** to add the two new skill fields to existing users.

Create file: `migrations/add_system_cloud_domains.py`

```python
"""
Migration: Add system and cloud domains to user skill levels
"""

import sqlite3
import sys

def migrate():
    """Add system and cloud skill columns to users table"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]

        # Add system skill if not exists
        if 'skill_system' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN skill_system INTEGER DEFAULT 0")
            print("✅ Added skill_system column")
        else:
            print("ℹ️  skill_system column already exists")

        # Add cloud skill if not exists
        if 'skill_cloud' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN skill_cloud INTEGER DEFAULT 0")
            print("✅ Added skill_cloud column")
        else:
            print("ℹ️  skill_cloud column already exists")

        conn.commit()
        print("\n✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
```

### 4. UI Updates (Optional but Recommended)

Check these files for domain references that may need updating:
- `ui/pages/dashboard.py` - Domain skill display
- `ui/pages/diagnostic.py` - Diagnostic test UI
- `app.py` - Main app navigation

These likely auto-discover domains from the data, but verify.

## Lesson Content for New Domains

### System Domain - Suggested Lessons

**Beginner (Difficulty 1)**:
1. Windows System Internals Fundamentals
2. Linux System Fundamentals
3. File System Permissions (Windows & Linux)

**Intermediate (Difficulty 2)**:
4. Windows Registry Deep Dive
5. Linux Process Management
6. System Logging and Auditing
7. User and Group Management

**Advanced (Difficulty 3)**:
8. Windows Privilege Escalation Techniques
9. Linux Privilege Escalation Techniques
10. Kernel Security and Hardening
11. System Call Monitoring

**Expert (Difficulty 4)**:
12. Rootkit Detection and Analysis
13. Advanced Process Injection Techniques
14. Custom Security Module Development

### Cloud Domain - Suggested Lessons

**Beginner (Difficulty 1)**:
1. Cloud Security Fundamentals
2. Shared Responsibility Model
3. IAM Basics (Users, Roles, Policies)

**Intermediate (Difficulty 2)**:
4. AWS Security Essentials
5. Azure Security Fundamentals
6. Storage Security (S3, Blob Storage)
7. Network Security in the Cloud (VPC, NSG)
8. Cloud Logging and Monitoring

**Advanced (Difficulty 3)**:
9. Container Security (Docker, Kubernetes)
10. Serverless Security (Lambda, Functions)
11. Cloud Penetration Testing
12. Infrastructure as Code Security (Terraform, CloudFormation)

**Expert (Difficulty 4)**:
13. Advanced Threat Detection in Cloud
14. Cloud-Native Security Architecture
15. Multi-Cloud Security Strategy
16. Cloud Security Incident Response

## Implementation Steps

### Step 1: Update Models
```bash
# Edit models/user.py
# Add system and cloud fields to SkillLevels class
# Update get_overall_level() and get_weakest_domain() methods
```

### Step 2: Update Adaptive Engine
```bash
# Edit core/adaptive_engine.py
# Add domains to domain_prerequisites
# Add domains to domain lists
# Add diagnostic questions for new domains
```

### Step 3: Database Migration
```bash
# Create and run migration
python migrations/add_system_cloud_domains.py
```

### Step 4: Create Initial Lessons
```bash
# Use the content generator tool
python create_rich_lesson.py --interactive

# Or create batch config for system domain
# Then create lessons for cloud domain
```

### Step 5: Test
```bash
# Load lessons
python load_all_lessons.py

# Reset user to see new domains
python check_database.py reset yourusername

# Run app
streamlit run app.py

# Verify:
# - Diagnostic test includes system and cloud questions
# - Dashboard shows system and cloud skills (at 0)
# - Can complete lessons in new domains
# - Skills update correctly
```

## Domain Prerequisite Logic

Based on the structure:

```
fundamentals (no prerequisites)
    ├─> dfir
    ├─> malware
    ├─> active_directory
    ├─> system (NEW)
    │     └─> cloud (NEW - requires system knowledge)
    └─> pentest (requires active_directory too)
          ├─> redteam (requires malware too)
          └─> blueteam (requires dfir and malware)
```

**Rationale**:
- **system** requires **fundamentals**: Need basic security concepts before diving into OS internals
- **cloud** requires **fundamentals** + **system**: Cloud builds on system knowledge (VMs, containers, OS security)

## Naming Conventions

**Domain names** (lowercase, underscore for multi-word):
- `system` (not `systems` or `operating_systems`)
- `cloud` (not `cloud_security`)

**Keep it short and clear** - matches existing pattern (fundamentals, dfir, malware, pentest)

## Summary Checklist

- [ ] Update `models/user.py` - Add skill fields
- [ ] Update `core/adaptive_engine.py` - Add domain prerequisites and diagnostic questions
- [ ] Create database migration script
- [ ] Run migration on database
- [ ] Create initial lessons for system domain (3-5 lessons)
- [ ] Create initial lessons for cloud domain (3-5 lessons)
- [ ] Load lessons into database
- [ ] Test diagnostic includes new domains
- [ ] Test skill tracking works for new domains
- [ ] Test lesson recommendations work
- [ ] Update documentation

---

**Ready to implement?** The changes are straightforward and follow the existing pattern. Once code is updated and migration run, you can start creating lessons for the new domains!
