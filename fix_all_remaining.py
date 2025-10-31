#!/usr/bin/env python3
"""
Fix all remaining placeholder text in non-compliant lessons with targeted technical content
"""

import json
from pathlib import Path

CONTENT_DIR = Path("content")

# Specific lessons and their issues from validation
FIXES = {
    "lesson_blue_team_08_siem_detection_engineering_RICH.json": {
        2: {  # Block index
            "type": "explanation",
            "find": "TODO",
            "content": """**SIEM Detection Engineering: Advanced Techniques**

Detection engineering is the process of creating, tuning, and maintaining detection logic that identifies security threats in your environment. Unlike traditional signature-based detection, modern detection engineering focuses on behavioral analytics and threat hunting hypotheses.

**Core Detection Engineering Principles:**

1. **Detection-as-Code Philosophy**
   - Version control all detection rules (Git)
   - Automated testing and validation
   - CI/CD pipelines for detection deployment
   - Peer review process for new detections

2. **MITRE ATT&CK Mapping**
   - Map every detection to specific TTPs
   - Track coverage across the ATT&CK matrix
   - Identify gaps in detection capabilities
   - Prioritize based on threat intelligence

3. **False Positive Management**
   - Baseline normal behavior first
   - Context-aware thresholds
   - Whitelist legitimate activity
   - Continuous tuning based on feedback

**Detection Rule Anatomy:**

Every SIEM detection rule should include:
- **Rule Name**: Clear, descriptive (e.g., "Brute Force Authentication - External IPs")
- **MITRE Technique**: T1110.001 (Password Guessing)
- **Data Sources**: Windows Security Event ID 4625, Syslog auth failures
- **Logic**: The actual detection query (SPL, KQL, etc.)
- **Threshold**: When to trigger (e.g., >10 failures in 5 minutes)
- **Context**: Additional enrichment (GeoIP, user risk score, asset criticality)
- **Action**: Alert severity, SOAR playbook trigger
- **Tuning History**: Track changes over time

**Advanced Detection Techniques:**

**1. Statistical Anomaly Detection**
Instead of static thresholds, use standard deviation:
```spl
index=authentication action=failure
| bucket _time span=1h
| stats count by _time, src_ip
| eventstats avg(count) as avg_count, stdev(count) as stdev_count
| eval threshold=avg_count + (2*stdev_count)
| where count > threshold
```

**2. Chain Detection (Correlation)**
Detect multi-stage attacks by correlating events:
```spl
index=windows EventCode=4624 Logon_Type=3
| transaction src_ip, dest_ip maxspan=5m
| where eventcount > 5
| table src_ip, dest_ip, eventcount, duration
```

**3. Threat Intelligence Enrichment**
Automatically check IPs against threat feeds:
```spl
index=proxy
| lookup threatfeed_ip.csv ip as src_ip OUTPUT threat_score, threat_category
| where threat_score > 80
```

**4. User/Entity Behavior Analytics (UEBA)**
Build user baselines and detect deviations:
```spl
index=authentication action=success
| stats dc(src_ip) as unique_ips, dc(dest_host) as unique_hosts by user
| eventstats avg(unique_ips) as avg_ips, stdev(unique_ips) as stdev_ips by user
| eval z_score=(unique_ips - avg_ips) / stdev_ips
| where z_score > 3
```

**Detection Gaps Analysis:**

Use this methodology to identify where you lack visibility:
1. Map MITRE ATT&CK techniques to your environment
2. For each technique, document:
   - Do we have the required logs?
   - Do we have detection rules?
   - Have we tested them against real attacks?
   - What's our detection rate?
3. Prioritize gaps based on:
   - Threat intelligence (what attackers use)
   - Asset criticality (protect crown jewels first)
   - Detection difficulty (quick wins vs. hard problems)

**Common Detection Engineering Pitfalls:**

1. **Alert Fatigue**: Too many low-fidelity alerts
   - Fix: Implement tiered alerting (P1-P4)
   - Fix: Require minimum confidence scores
   - Fix: Aggregate similar alerts

2. **Detection Drift**: Rules stop working over time
   - Fix: Monitor "days since last fire" metric
   - Fix: Schedule monthly rule validation
   - Fix: Test against Purple Team exercises

3. **Blind Spots**: Missing critical data sources
   - Fix: Inventory all security tools
   - Fix: Ensure SIEM ingests all relevant logs
   - Fix: Monitor data source health

**Metrics for Detection Engineering:**

Track these KPIs:
- **Coverage**: % of MITRE ATT&CK techniques detected
- **Precision**: True Positives / (True Positives + False Positives)
- **Recall**: True Positives / (True Positives + False Negatives)
- **MTTD**: Mean Time To Detect (goal: <1 hour)
- **MTTR**: Mean Time To Respond (goal: <4 hours)
- **Detection Effectiveness**: Validated through Purple Team

This detection engineering approach ensures your SIEM evolves with the threat landscape, maintaining high-fidelity alerts while minimizing analyst burnout."""
        }
    },

    "lesson_cloud_02_azure_security_RICH.json": {
        0: {
            "type": "explanation",
            "find": "XXX",
            "content": """**Azure Security Fundamentals: Building a Secure Cloud Foundation**

Microsoft Azure is the world's second-largest cloud provider, powering critical infrastructure for Fortune 500 companies, government agencies, and healthcare organizations. Understanding Azure security is essential for any cybersecurity professional working in hybrid or multi-cloud environments.

**The Azure Security Shared Responsibility Model:**

```
┌─────────────────────────────────────────────────────────┐
│  Security Responsibility Distribution                     │
├─────────────────────────────────────────────────────────┤
│  Layer            │ On-Prem │ IaaS │ PaaS │ SaaS       │
├─────────────────────────────────────────────────────────┤
│  Data & Access    │   YOU   │ YOU  │ YOU  │ YOU        │
│  Applications     │   YOU   │ YOU  │ YOU  │ MICROSOFT  │
│  Runtime          │   YOU   │ YOU  │ MSFT │ MICROSOFT  │
│  OS               │   YOU   │ YOU  │ MSFT │ MICROSOFT  │
│  Network          │   YOU   │ BOTH │ MSFT │ MICROSOFT  │
│  Physical         │   YOU   │ MSFT │ MSFT │ MICROSOFT  │
└─────────────────────────────────────────────────────────┘
```

**Key Insight**: Even in the cloud, YOU are always responsible for securing your data and controlling access. Never assume Microsoft handles security for you.

**Common Azure Security Misconceptions:**

❌ **Myth 1**: "It's in the cloud, so it's automatically secure"
✅ **Reality**: Misconfigured Azure resources are the #1 cause of breaches

❌ **Myth 2**: "Microsoft secures everything"
✅ **Reality**: Microsoft secures the infrastructure, you secure YOUR workloads

❌ **Myth 3**: "Azure handles compliance for me"
✅ **Reality**: You must configure Azure to meet YOUR compliance requirements (HIPAA, PCI-DSS, etc.)

**Why Azure Security Matters:**

- **95% of Fortune 500** companies use Azure
- **53 Azure regions** worldwide (more than AWS)
- **Government cloud** (Azure Government) for sensitive workloads
- **Healthcare adoption**: HIPAA-compliant by default if configured correctly

**AWS vs Azure: Security Translation Guide**

If you know AWS, here's how Azure maps:

| Concept | AWS | Azure |
|---------|-----|-------|
| Identity | IAM | Azure AD / Entra ID |
| Access Control | IAM Policies | RBAC (Role-Based Access Control) |
| Secrets | Secrets Manager | Key Vault |
| Security Hub | Security Hub | Microsoft Defender for Cloud |
| Storage | S3 | Blob Storage |
| Network ACL | Security Groups | Network Security Groups (NSGs) |
| Audit Logs | CloudTrail | Activity Log + Azure Monitor |
| Firewall | WAF | Azure Firewall + Application Gateway |

**Azure Active Directory (Now Microsoft Entra ID):**

Azure AD is not "Active Directory in the cloud" - it's a completely different product:

**Traditional AD vs Azure AD:**
- Traditional AD: On-premises, Kerberos, NTLM, LDAP
- Azure AD: Cloud-native, OAuth, SAML, OpenID Connect

**Core Concepts:**

1. **Tenants**: Your organization's dedicated Azure AD instance
   - Each tenant has a unique domain: yourcompany.onmicrosoft.com
   - Can link to custom domains: yourcompany.com

2. **Users**: Individual identities
   - Cloud-only users (created in Azure AD)
   - Synchronized users (synced from on-prem AD via Azure AD Connect)
   - Guest users (B2B collaboration from other tenants)

3. **Groups**: Collections of users
   - Security groups (for access control)
   - Microsoft 365 groups (for collaboration)
   - Dynamic groups (membership based on rules)

4. **Service Principals**: Application identities
   - Think of them as "service accounts" for apps
   - Used for automation and API access

5. **Managed Identities**: Azure resource identities
   - System-assigned: Tied to resource lifecycle
   - User-assigned: Independent, reusable across resources
   - **Best Practice**: Use managed identities instead of storing credentials

This foundation ensures you understand the Azure security landscape before diving into specific controls and configurations."""
        }
    },
}

def load_lesson(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_lesson(filepath, lesson):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] {filepath.name}")

def fix_lesson(filename, fixes_dict):
    """Fix specific blocks in a lesson"""
    filepath = CONTENT_DIR / filename

    if not filepath.exists():
        print(f"[SKIP] Not found: {filename}")
        return False

    try:
        lesson = load_lesson(filepath)
        modified = False

        for block_idx, fix_info in fixes_dict.items():
            if block_idx >= len(lesson['content_blocks']):
                print(f"[WARN] {filename}: Block {block_idx} doesn't exist")
                continue

            block = lesson['content_blocks'][block_idx]

            if 'content' in block and 'text' in block['content']:
                text = block['content']['text']

                # Check if placeholder exists
                if fix_info['find'] in text:
                    # Replace the entire text with new content
                    block['content']['text'] = fix_info['content']
                    modified = True
                    print(f"[FIXED] {filename}: Block {block_idx} ({fix_info['type']})")
                else:
                    print(f"[INFO] {filename}: Block {block_idx} - placeholder '{fix_info['find']}' not found")

        if modified:
            save_lesson(filepath, lesson)
            return True

    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        return False

    return False

def main():
    print("=== Fixing Remaining Non-Compliant Lessons ===\n")

    fixed_count = 0
    for filename, fixes_dict in FIXES.items():
        print(f"\nProcessing {filename}...")
        if fix_lesson(filename, fixes_dict):
            fixed_count += 1

    print(f"\n=== Summary ===")
    print(f"Lessons fixed: {fixed_count}/{len(FIXES)}")

if __name__ == "__main__":
    main()
