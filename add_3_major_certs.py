#!/usr/bin/env python3
"""
Add lessons from 3 major certification courses to lesson_ideas.csv:
- OffSec PEN-300 (OSEP): Advanced penetration testing and evasion
- ISC2 CISSP: Enterprise security management across 8 domains
- CompTIA Security+: Foundational to intermediate security concepts
"""

import csv
from pathlib import Path

# Path to CSV file
csv_path = Path(__file__).parent / "lesson_ideas.csv"

def main():
    # Read existing CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Get the next lesson number
    last_lesson_num = max(int(row['lesson_number']) for row in rows)
    next_lesson_num = last_lesson_num + 1

    # Track order_index per domain
    domain_order = {}
    for row in rows:
        domain = row['domain']
        order_idx = int(row['order_index'])
        domain_order[domain] = max(domain_order.get(domain, 0), order_idx)

    # New lessons to add
    new_lessons = []

    # ========================================
    # OFFSEC PEN-300 (OSEP) - 15 lessons
    # Advanced Windows exploitation and evasion
    # ========================================
    pen300_lessons = [
        # Client-Side Code Execution
        {'domain': 'red_team', 'difficulty': 3, 'title': 'Advanced Client-Side Attacks', 'module': 'PEN300 M1', 'topics': 'HTML smuggling, VBA macros, HTA attacks, browser exploitation, staged payloads', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 1'},
        {'domain': 'red_team', 'difficulty': 3, 'title': 'Application Whitelisting Bypass Techniques', 'module': 'PEN300 M2', 'topics': 'AppLocker bypass, InstallUtil, regsvr32, mshta, LOLBAS techniques, trusted binaries', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 2'},
        {'domain': 'red_team', 'difficulty': 3, 'title': 'PowerShell Empire and C2 Frameworks', 'module': 'PEN300 M3', 'topics': 'Empire agents, C2 channels, post-exploitation, persistence, credential dumping', 'prerequisites': '["Advanced Client-Side Attacks"]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 3'},

        # Code Execution and Process Injection
        {'domain': 'red_team', 'difficulty': 3, 'title': 'Advanced Process Injection and Migration', 'module': 'PEN300 M4', 'topics': 'DLL injection, reflective DLL injection, process hollowing, thread hijacking, APC injection', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 4'},
        {'domain': 'red_team', 'difficulty': 3, 'title': 'In-Memory Payload Execution', 'module': 'PEN300 M5', 'topics': 'Reflective PE loading, in-memory .NET execution, fileless malware, memory-only payloads', 'prerequisites': '["Advanced Process Injection and Migration"]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 5'},

        # Antivirus Evasion
        {'domain': 'red_team', 'difficulty': 3, 'title': 'Signature-Based AV Evasion', 'module': 'PEN300 M6', 'topics': 'Static signature evasion, encoding, encryption, string obfuscation, binary modification', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 6'},
        {'domain': 'red_team', 'difficulty': 3, 'title': 'Behavior-Based AV Evasion', 'module': 'PEN300 M7', 'topics': 'API hashing, syscalls, AMSI bypass, ETW patching, sandbox evasion', 'prerequisites': '["Signature-Based AV Evasion"]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 7'},

        # Active Directory Attacks
        {'domain': 'active_directory', 'difficulty': 3, 'title': 'Kerberos Abuse and Golden Tickets', 'module': 'PEN300 M8', 'topics': 'Kerberoasting, AS-REP roasting, golden tickets, silver tickets, ticket manipulation', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'PEN300 Module 8'},
        {'domain': 'active_directory', 'difficulty': 3, 'title': 'Advanced Active Directory Enumeration', 'module': 'PEN300 M9', 'topics': 'BloodHound analysis, ACL abuse, GPO enumeration, trust relationships, delegation attacks', 'prerequisites': '["Kerberos Abuse and Golden Tickets"]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'PEN300 Module 9'},
        {'domain': 'active_directory', 'difficulty': 3, 'title': 'Lateral Movement and Persistence in AD', 'module': 'PEN300 M10', 'topics': 'DCOM, WMI, PsExec alternatives, skeleton key, DCShadow, AdminSDHolder abuse', 'prerequisites': '["Advanced Active Directory Enumeration"]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'PEN300 Module 10'},

        # Linux Attacks
        {'domain': 'linux', 'difficulty': 3, 'title': 'Linux Post-Exploitation and Privilege Escalation', 'module': 'PEN300 M11', 'topics': 'SUID binaries, capabilities, kernel exploits, container escape, cron abuse', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'PEN300 Module 11'},

        # Network and Web Attacks
        {'domain': 'pentest', 'difficulty': 3, 'title': 'Advanced Web Application Exploitation', 'module': 'PEN300 M12', 'topics': 'Blind SQL injection, second-order injection, XXE, SSRF, deserialization attacks', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Pentester', 'notes': 'PEN300 Module 12'},
        {'domain': 'pentest', 'difficulty': 3, 'title': 'Network Pivoting and Tunneling', 'module': 'PEN300 M13', 'topics': 'SSH tunneling, SOCKS proxies, Chisel, ligolo, dynamic port forwarding, double pivoting', 'prerequisites': '[]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'PEN300 Module 13'},

        # Custom Tool Development
        {'domain': 'red_team', 'difficulty': 3, 'title': 'Custom C2 Development Fundamentals', 'module': 'PEN300 M14', 'topics': 'C2 architecture, HTTP/HTTPS channels, encryption, beaconing, agent design', 'prerequisites': '["PowerShell Empire and C2 Frameworks"]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 14'},
        {'domain': 'red_team', 'difficulty': 3, 'title': 'Offensive Tool Development in C#', 'module': 'PEN300 M15', 'topics': '.NET internals, P/Invoke, Win32 API, custom tooling, exploit development', 'prerequisites': '["Custom C2 Development Fundamentals"]', 'tags': 'Course: OffSec-PEN300, Career Path: Red Teamer', 'notes': 'PEN300 Module 15'},
    ]

    # ========================================
    # ISC2 CISSP - 40 lessons (5 per domain)
    # Enterprise security management
    # ========================================
    cissp_lessons = [
        # Domain 1: Security and Risk Management (16%)
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'CIA Triad and Security Principles', 'module': 'CISSP D1', 'topics': 'Confidentiality, integrity, availability, authenticity, nonrepudiation, security concepts', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'CISSP Domain 1.1'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Security Governance and Compliance', 'module': 'CISSP D1', 'topics': 'Governance frameworks, organizational policies, regulatory compliance, legal requirements', 'prerequisites': '["CIA Triad and Security Principles"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'CISSP Domain 1.2'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Risk Management Frameworks', 'module': 'CISSP D1', 'topics': 'Risk assessment, risk treatment, NIST RMF, ISO 27005, threat modeling, supply chain risk', 'prerequisites': '["Security Governance and Compliance"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'CISSP Domain 1.3'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Business Continuity and Disaster Recovery', 'module': 'CISSP D1', 'topics': 'BCP/DRP planning, RTO/RPO, business impact analysis, continuity strategies', 'prerequisites': '["Risk Management Frameworks"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'CISSP Domain 1.4'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Security Awareness and Training Programs', 'module': 'CISSP D1', 'topics': 'Personnel security, security awareness training, role-based training, metrics', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'CISSP Domain 1.5'},

        # Domain 2: Asset Security (10%)
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Information and Asset Classification', 'module': 'CISSP D2', 'topics': 'Data classification, asset inventory, labeling, handling requirements, ownership', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'CISSP Domain 2.1'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Data Lifecycle Management', 'module': 'CISSP D2', 'topics': 'Data collection, storage, use, sharing, archiving, destruction, retention policies', 'prerequisites': '["Information and Asset Classification"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 2.2'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Data Protection Controls', 'module': 'CISSP D2', 'topics': 'Data at rest protection, data in transit, data in use, DLP, encryption controls', 'prerequisites': '["Data Lifecycle Management"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 2.3'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Privacy and Data Protection', 'module': 'CISSP D2', 'topics': 'GDPR, CCPA, privacy principles, PII protection, data subject rights', 'prerequisites': '["Data Protection Controls"]', 'tags': 'Course: ISC2-CISSP, Career Path: GRC Analyst', 'notes': 'CISSP Domain 2.4'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Asset Provisioning and Deprovisioning', 'module': 'CISSP D2', 'topics': 'Secure provisioning, asset tracking, disposal, sanitization, destruction methods', 'prerequisites': '["Data Lifecycle Management"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 2.5'},

        # Domain 3: Security Architecture and Engineering (13%)
        {'domain': 'system', 'difficulty': 2, 'title': 'Secure Design Principles', 'module': 'CISSP D3', 'topics': 'Defense in depth, least privilege, separation of duties, fail secure, zero trust', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 3.1'},
        {'domain': 'system', 'difficulty': 2, 'title': 'Security Models and Frameworks', 'module': 'CISSP D3', 'topics': 'Bell-LaPadula, Biba, Clark-Wilson, reference monitor, security kernel', 'prerequisites': '["Secure Design Principles"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 3.2'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Cryptography Fundamentals', 'module': 'CISSP D3', 'topics': 'Symmetric encryption, asymmetric encryption, hashing, digital signatures, PKI basics', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 3.3'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Cryptographic Implementations and PKI', 'module': 'CISSP D3', 'topics': 'PKI architecture, certificate management, key management, HSM, cryptanalytic attacks', 'prerequisites': '["Cryptography Fundamentals"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 3.4'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud and Virtualization Security', 'module': 'CISSP D3', 'topics': 'Cloud service models, virtualization security, container security, serverless security', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Cloud Security, Career Path: Security Engineer', 'notes': 'CISSP Domain 3.5'},
        {'domain': 'iot_security', 'difficulty': 2, 'title': 'IoT and Embedded Systems Security', 'module': 'CISSP D3', 'topics': 'IoT architecture, embedded security, OT/ICS security, SCADA, physical security', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 3.6'},
        {'domain': 'system', 'difficulty': 2, 'title': 'Facility Security Design and Controls', 'module': 'CISSP D3', 'topics': 'Physical access controls, environmental controls, fire suppression, CPTED', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 3.7'},

        # Domain 4: Communication and Network Security (13%)
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Network Architecture and Design', 'module': 'CISSP D4', 'topics': 'OSI model, TCP/IP model, network topologies, defense in depth networking', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 4.1'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Secure Network Protocols', 'module': 'CISSP D4', 'topics': 'TLS/SSL, IPSec, SSH, DNSSEC, secure email protocols, VPN technologies', 'prerequisites': '["Network Architecture and Design"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 4.2'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Network Segmentation and Isolation', 'module': 'CISSP D4', 'topics': 'VLANs, DMZ, micro-segmentation, zero trust networking, network zoning', 'prerequisites': '["Network Architecture and Design"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 4.3'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Wireless and Mobile Security', 'module': 'CISSP D4', 'topics': 'Wi-Fi security, WPA2/WPA3, cellular security, mobile device management, BYOD', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 4.4'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Network Monitoring and Management', 'module': 'CISSP D4', 'topics': 'SIEM, NetFlow, packet capture, IDS/IPS, network visibility, SDN security', 'prerequisites': '["Network Architecture and Design"]', 'tags': 'Course: ISC2-CISSP, Career Path: SOC Analyst, Career Path: Security Engineer', 'notes': 'CISSP Domain 4.5'},

        # Domain 5: Identity and Access Management (13%)
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Identity and Access Management Concepts', 'module': 'CISSP D5', 'topics': 'Identification, authentication, authorization, accounting, identity lifecycle', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 5.1'},
        {'domain': 'active_directory', 'difficulty': 2, 'title': 'Access Control Models', 'module': 'CISSP D5', 'topics': 'RBAC, ABAC, MAC, DAC, rule-based access control, access control matrix', 'prerequisites': '["Identity and Access Management Concepts"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 5.2'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Authentication Methods and MFA', 'module': 'CISSP D5', 'topics': 'Password policies, biometrics, tokens, MFA, passwordless, FIDO2', 'prerequisites': '["Identity and Access Management Concepts"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 5.3'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Federated Identity and SSO', 'module': 'CISSP D5', 'topics': 'SAML, OAuth, OIDC, federation, SSO, identity providers, trust relationships', 'prerequisites': '["Authentication Methods and MFA"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 5.4'},
        {'domain': 'active_directory', 'difficulty': 2, 'title': 'Privileged Access Management', 'module': 'CISSP D5', 'topics': 'PAM, privileged accounts, JIT access, session monitoring, credential vaulting', 'prerequisites': '["Identity and Access Management Concepts"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 5.5'},

        # Domain 6: Security Assessment and Testing (12%)
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Security Assessment Strategy', 'module': 'CISSP D6', 'topics': 'Assessment planning, scope definition, risk-based testing, compliance testing', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'CISSP Domain 6.1'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Vulnerability Assessment and Scanning', 'module': 'CISSP D6', 'topics': 'Vulnerability scanners, scan types, remediation prioritization, false positives', 'prerequisites': '["Security Assessment Strategy"]', 'tags': 'Course: ISC2-CISSP, Career Path: Pentester, Career Path: Security Engineer', 'notes': 'CISSP Domain 6.2'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Penetration Testing Methodologies', 'module': 'CISSP D6', 'topics': 'Pentest phases, white/grey/black box, attack simulation, reporting', 'prerequisites': '["Vulnerability Assessment and Scanning"]', 'tags': 'Course: ISC2-CISSP, Career Path: Pentester', 'notes': 'CISSP Domain 6.3'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Security Control Testing', 'module': 'CISSP D6', 'topics': 'Control validation, effectiveness testing, SOC 2, ISO audits, compliance testing', 'prerequisites': '["Security Assessment Strategy"]', 'tags': 'Course: ISC2-CISSP, Career Path: GRC Analyst, Career Path: Security Engineer', 'notes': 'CISSP Domain 6.4'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Log Review and Security Analytics', 'module': 'CISSP D6', 'topics': 'Log analysis, SIEM analytics, baseline establishment, anomaly detection', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: SOC Analyst, Career Path: Security Engineer', 'notes': 'CISSP Domain 6.5'},

        # Domain 7: Security Operations (13%)
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Security Operations Center (SOC) Operations', 'module': 'CISSP D7', 'topics': 'SOC structure, monitoring, alerting, triage, escalation, runbooks', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: SOC Analyst, Career Path: Blue Teamer', 'notes': 'CISSP Domain 7.1'},
        {'domain': 'dfir', 'difficulty': 2, 'title': 'Incident Response Lifecycle', 'module': 'CISSP D7', 'topics': 'Preparation, detection, containment, eradication, recovery, lessons learned', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: DFIR Specialist, Career Path: Blue Teamer', 'notes': 'CISSP Domain 7.2'},
        {'domain': 'dfir', 'difficulty': 2, 'title': 'Digital Forensics and Investigations', 'module': 'CISSP D7', 'topics': 'Evidence collection, chain of custody, forensic tools, analysis, reporting', 'prerequisites': '["Incident Response Lifecycle"]', 'tags': 'Course: ISC2-CISSP, Career Path: DFIR Specialist', 'notes': 'CISSP Domain 7.3'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Patch and Vulnerability Management', 'module': 'CISSP D7', 'topics': 'Patch management, vulnerability remediation, change management, risk prioritization', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 7.4'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Configuration and Change Management', 'module': 'CISSP D7', 'topics': 'Configuration baselines, change control, version control, asset management', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 7.5'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Disaster Recovery Operations', 'module': 'CISSP D7', 'topics': 'Backup strategies, recovery procedures, testing DR plans, failover, restoration', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 7.6'},

        # Domain 8: Software Development Security (10%)
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Secure Software Development Lifecycle (SDLC)', 'module': 'CISSP D8', 'topics': 'SDLC phases, security integration, Agile security, DevSecOps principles', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 8.1'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Secure Coding Practices', 'module': 'CISSP D8', 'topics': 'OWASP Top 10, input validation, output encoding, secure APIs, code review', 'prerequisites': '["Secure Software Development Lifecycle (SDLC)"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 8.2'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Application Security Testing', 'module': 'CISSP D8', 'topics': 'SAST, DAST, IAST, SCA, dependency scanning, security testing automation', 'prerequisites': '["Secure Coding Practices"]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 8.3'},
        {'domain': 'fundamentals', 'difficulty': 2, 'title': 'Database Security', 'module': 'CISSP D8', 'topics': 'Database access controls, encryption, SQL injection prevention, auditing', 'prerequisites': '[]', 'tags': 'Course: ISC2-CISSP, Career Path: Security Engineer', 'notes': 'CISSP Domain 8.4'},
    ]

    # ========================================
    # COMPTIA SECURITY+ - 25 lessons (5 per domain)
    # Foundational to intermediate security
    # ========================================
    secplus_lessons = [
        # Domain 1: General Security Concepts (12%)
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Security Controls and Types', 'module': 'Sec+ D1', 'topics': 'Preventive, detective, corrective, deterrent, compensating, physical, technical', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst, Career Path: Security Engineer', 'notes': 'Security+ Domain 1.1'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Zero Trust Architecture Fundamentals', 'module': 'Sec+ D1', 'topics': 'Zero trust principles, control plane, data plane, never trust always verify', 'prerequisites': '["Security Controls and Types"]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 1.2'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'AAA: Authentication, Authorization, Accounting', 'module': 'Sec+ D1', 'topics': 'Authentication factors, authorization models, accounting, auditing', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst, Career Path: Security Engineer', 'notes': 'Security+ Domain 1.3'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Public Key Infrastructure (PKI) Basics', 'module': 'Sec+ D1', 'topics': 'Certificates, CA hierarchy, certificate lifecycle, trust chains, revocation', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 1.4'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Cryptographic Solutions', 'module': 'Sec+ D1', 'topics': 'Encryption, hashing, digital signatures, obfuscation, blockchain basics', 'prerequisites': '["Public Key Infrastructure (PKI) Basics"]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 1.5'},

        # Domain 2: Threats, Vulnerabilities, and Mitigations (22%)
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Threat Actors and Motivations', 'module': 'Sec+ D2', 'topics': 'Nation-states, hacktivists, organized crime, insiders, threat actor attributes', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst, Career Path: Threat Hunter', 'notes': 'Security+ Domain 2.1'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Attack Vectors and Techniques', 'module': 'Sec+ D2', 'topics': 'Phishing, malware, social engineering, supply chain, physical attacks', 'prerequisites': '["Threat Actors and Motivations"]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst', 'notes': 'Security+ Domain 2.2'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Common Vulnerabilities', 'module': 'Sec+ D2', 'topics': 'Software flaws, misconfigurations, weak authentication, unpatched systems', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst, Career Path: Security Engineer', 'notes': 'Security+ Domain 2.3'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Malware Types and Indicators', 'module': 'Sec+ D2', 'topics': 'Viruses, worms, trojans, ransomware, spyware, rootkits, malware analysis', 'prerequisites': '["Attack Vectors and Techniques"]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst, Career Path: Malware Analyst', 'notes': 'Security+ Domain 2.4'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Password and Credential Attacks', 'module': 'Sec+ D2', 'topics': 'Brute force, dictionary attacks, password spraying, credential stuffing, hash cracking', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst', 'notes': 'Security+ Domain 2.5'},
        {'domain': 'blue_team', 'difficulty': 1, 'title': 'Mitigation Techniques and Hardening', 'module': 'Sec+ D2', 'topics': 'Segmentation, access control, configuration management, patching, isolation', 'prerequisites': '["Common Vulnerabilities"]', 'tags': 'Course: CompTIA-Security+, Career Path: Blue Teamer, Career Path: Security Engineer', 'notes': 'Security+ Domain 2.6'},

        # Domain 3: Security Architecture (18%)
        {'domain': 'cloud', 'difficulty': 1, 'title': 'Cloud Service Models and Security', 'module': 'Sec+ D3', 'topics': 'IaaS, PaaS, SaaS, cloud deployment models, shared responsibility', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Cloud Security', 'notes': 'Security+ Domain 3.1'},
        {'domain': 'cloud', 'difficulty': 1, 'title': 'Cloud Security Controls and Best Practices', 'module': 'Sec+ D3', 'topics': 'CASB, CSPM, cloud access controls, data protection, misconfigurations', 'prerequisites': '["Cloud Service Models and Security"]', 'tags': 'Course: CompTIA-Security+, Career Path: Cloud Security', 'notes': 'Security+ Domain 3.2'},
        {'domain': 'system', 'difficulty': 1, 'title': 'Enterprise Infrastructure Security', 'module': 'Sec+ D3', 'topics': 'Network design, segmentation, DMZ, VPN, secure protocols, jump servers', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 3.3'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Data Protection and Classification', 'module': 'Sec+ D3', 'topics': 'Data states, classification levels, DLP, tokenization, masking, data sovereignty', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer, Career Path: GRC Analyst', 'notes': 'Security+ Domain 3.4'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Business Continuity and Resilience', 'module': 'Sec+ D3', 'topics': 'High availability, redundancy, backup strategies, BCP, DRP, resilience', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 3.5'},

        # Domain 4: Security Operations (28%)
        {'domain': 'blue_team', 'difficulty': 1, 'title': 'Security Baselines and Configuration Management', 'module': 'Sec+ D4', 'topics': 'Hardening guides, CIS benchmarks, secure configurations, baseline monitoring', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Blue Teamer, Career Path: Security Engineer', 'notes': 'Security+ Domain 4.1'},
        {'domain': 'blue_team', 'difficulty': 1, 'title': 'Asset and Vulnerability Management', 'module': 'Sec+ D4', 'topics': 'Asset inventory, vulnerability scanning, patch management, remediation tracking', 'prerequisites': '["Security Baselines and Configuration Management"]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 4.2'},
        {'domain': 'blue_team', 'difficulty': 1, 'title': 'Security Monitoring Tools and Techniques', 'module': 'Sec+ D4', 'topics': 'SIEM, log aggregation, alerting, dashboards, security metrics, KPIs', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst', 'notes': 'Security+ Domain 4.3'},
        {'domain': 'blue_team', 'difficulty': 1, 'title': 'Network Security Devices and Technologies', 'module': 'Sec+ D4', 'topics': 'Firewalls, IDS/IPS, proxies, WAF, NAC, security appliances', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: SOC Analyst, Career Path: Security Engineer', 'notes': 'Security+ Domain 4.4'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Identity and Access Management Solutions', 'module': 'Sec+ D4', 'topics': 'SSO, MFA, PAM, directory services, LDAP, authentication protocols', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 4.5'},
        {'domain': 'dfir', 'difficulty': 1, 'title': 'Incident Response Process', 'module': 'Sec+ D4', 'topics': 'IR phases, NIST framework, detection, analysis, containment, recovery', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: DFIR Specialist, Career Path: SOC Analyst', 'notes': 'Security+ Domain 4.6'},
        {'domain': 'dfir', 'difficulty': 1, 'title': 'Digital Forensics Fundamentals', 'module': 'Sec+ D4', 'topics': 'Evidence handling, chain of custody, forensic tools, acquisition, analysis', 'prerequisites': '["Incident Response Process"]', 'tags': 'Course: CompTIA-Security+, Career Path: DFIR Specialist', 'notes': 'Security+ Domain 4.7'},

        # Domain 5: Security Program Management and Oversight (20%)
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Security Governance Frameworks', 'module': 'Sec+ D5', 'topics': 'NIST CSF, ISO 27001, CIS Controls, COBIT, governance structure', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: GRC Analyst, Career Path: Security Engineer', 'notes': 'Security+ Domain 5.1'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Risk Management Processes', 'module': 'Sec+ D5', 'topics': 'Risk identification, analysis, treatment, monitoring, risk registers', 'prerequisites': '["Security Governance Frameworks"]', 'tags': 'Course: CompTIA-Security+, Career Path: GRC Analyst', 'notes': 'Security+ Domain 5.2'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Third-Party and Vendor Risk Management', 'module': 'Sec+ D5', 'topics': 'Vendor assessment, SLAs, due diligence, supply chain risk, contracts', 'prerequisites': '["Risk Management Processes"]', 'tags': 'Course: CompTIA-Security+, Career Path: GRC Analyst', 'notes': 'Security+ Domain 5.3'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Compliance and Regulatory Requirements', 'module': 'Sec+ D5', 'topics': 'PCI DSS, HIPAA, GDPR, SOX, compliance audits, regulatory frameworks', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: GRC Analyst', 'notes': 'Security+ Domain 5.4'},
        {'domain': 'fundamentals', 'difficulty': 1, 'title': 'Security Awareness and Training', 'module': 'Sec+ D5', 'topics': 'Training programs, phishing simulations, security culture, user education', 'prerequisites': '[]', 'tags': 'Course: CompTIA-Security+, Career Path: Security Engineer', 'notes': 'Security+ Domain 5.5'},
    ]

    # Combine all lessons
    all_new_lessons = pen300_lessons + cissp_lessons + secplus_lessons

    # Process each lesson
    for lesson in all_new_lessons:
        domain = lesson['domain']
        domain_order[domain] = domain_order.get(domain, 0) + 1
        order_idx = domain_order[domain]

        new_row = {
            'lesson_number': next_lesson_num,
            'order_index': order_idx,
            'domain': domain,
            'difficulty': lesson['difficulty'],
            'title': lesson['title'],
            'module': lesson['module'],
            'topics': lesson['topics'],
            'prerequisites': lesson['prerequisites'],
            'status': 'idea',
            'tags': lesson['tags'],
            'notes': lesson['notes']
        }

        new_lessons.append(new_row)
        print(f"Added #{next_lesson_num} [{domain}:{order_idx}]: {lesson['title']} ({'Beginner' if lesson['difficulty']==1 else 'Intermediate' if lesson['difficulty']==2 else 'Advanced'})")
        next_lesson_num += 1

    # Append to CSV
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['lesson_number', 'order_index', 'domain', 'difficulty', 'title', 'module', 'topics', 'prerequisites', 'status', 'tags', 'notes'])
        writer.writerows(new_lessons)

    print("\n" + "="*80)
    print(f"SUCCESS - Added {len(new_lessons)} lessons from 3 major certification courses")
    print(f"Total lessons: {next_lesson_num - 1}")
    print("="*80)

    # Statistics
    difficulty_counts = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0}
    domain_counts = {}

    for lesson in all_new_lessons:
        diff_name = 'Beginner' if lesson['difficulty']==1 else 'Intermediate' if lesson['difficulty']==2 else 'Advanced'
        difficulty_counts[diff_name] += 1
        domain_counts[lesson['domain']] = domain_counts.get(lesson['domain'], 0) + 1

    print("\nDifficulty Distribution:")
    for diff, count in difficulty_counts.items():
        print(f"  {diff}: {count}")

    print("\nDomains:")
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain}: {count} lessons")

if __name__ == "__main__":
    main()
