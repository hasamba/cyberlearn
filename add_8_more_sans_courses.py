#!/usr/bin/env python3
"""
Add 8 additional SANS courses to lesson_ideas.csv:
1. SEC504: Hacker Tools, Techniques, and Incident Handling (38 hours, 44 labs)
2. SEC510: Cloud Security Engineering and Controls (38 hours, 52 labs)
3. SEC511: Cybersecurity Engineering - Advanced Threat Detection (46 hours, 18+ labs)
4. SEC535: Offensive AI - Attack Tools and Techniques (18 hours, 14 labs)
5. SEC541: Cloud Security Threat Detection (30 hours, 22 labs)
6. SEC542: Web App Penetration Testing (36 hours, 30 labs)
7. SEC560: Enterprise Penetration Testing (36 hours, 30 labs)
8. SEC587: Advanced OSINT (36 hours, 28+ labs)

Total: 278 hours, 238+ labs across 8 courses
"""

import csv
from pathlib import Path

def add_8_more_sans_courses():
    csv_path = Path("lesson_ideas.csv")

    # Read existing lessons
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Get next lesson number
    last_lesson_num = max(int(row['lesson_number']) for row in rows)
    next_lesson_num = last_lesson_num + 1

    print(f"Starting from lesson_number: {next_lesson_num}\n")

    # Track order_index per domain
    domain_order = {}
    for row in rows:
        domain = row['domain']
        order_idx = int(row['order_index'])
        if domain not in domain_order:
            domain_order[domain] = order_idx
        else:
            domain_order[domain] = max(domain_order[domain], order_idx)

    # Increment for new lessons
    for domain in domain_order:
        domain_order[domain] += 1

    # Define all course lessons
    all_lessons = []

    # ============================================================================
    # SEC504: Hacker Tools, Techniques, and Incident Handling
    # ============================================================================
    print("=" * 80)
    print("SEC504: Hacker Tools, Techniques, and Incident Handling")
    print("=" * 80)

    sec504_lessons = [
        # Section 1: IR and Investigations (6 lessons)
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Dynamic Approach to Incident Response (DAIR)',
            'module': 'SEC504 Section 1',
            'topics': 'DAIR methodology, incident response process, IR workflows, response phases, decision-making frameworks',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist, Career Path: Blue Teamer',
            'notes': 'SEC504 S1 - IR methodology'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Live Windows Investigation Techniques',
            'module': 'SEC504 Section 1',
            'topics': 'Live examination, volatile data collection, memory acquisition, running process analysis, network connections',
            'prerequisites': '["Dynamic Approach to Incident Response (DAIR)"]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist',
            'notes': 'SEC504 S1 - Live investigation'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Network Investigation with NDR',
            'module': 'SEC504 Section 1',
            'topics': 'Network detection and response, traffic analysis, NDR platforms, network forensics, packet analysis',
            'prerequisites': '["Dynamic Approach to Incident Response (DAIR)"]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist, Career Path: Threat Hunter',
            'notes': 'SEC504 S1 - Network investigation'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Malware Analysis for Incident Response',
            'module': 'SEC504 Section 1',
            'topics': 'Malware triage, behavioral analysis, indicators extraction, malware families, analysis workflow',
            'prerequisites': '["Dynamic Approach to Incident Response (DAIR)"]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist, Career Path: Malware Analyst',
            'notes': 'SEC504 S1 - Malware investigation'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Writing IR Playbooks with AI',
            'module': 'SEC504 Section 1',
            'topics': 'AI-assisted playbook creation, automated response procedures, GenAI for IR, playbook templates, response automation',
            'prerequisites': '["Dynamic Approach to Incident Response (DAIR)"]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist, Career Path: AI Security',
            'notes': 'SEC504 S1 - AI for IR playbooks'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Web Application Log Assessment',
            'module': 'SEC504 Section 1',
            'topics': 'Web server logs, WordPress forensics, application log analysis, attack pattern recognition, log correlation',
            'prerequisites': '["Dynamic Approach to Incident Response (DAIR)"]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist',
            'notes': 'SEC504 S1 - Web log analysis'
        },

        # Section 2: Scanning and Enumeration (6 lessons)
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Network and Host Scanning with Nmap',
            'module': 'SEC504 Section 2',
            'topics': 'Nmap techniques, host discovery, port scanning, service enumeration, OS detection, NSE scripts',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester, Career Path: Security Engineer',
            'notes': 'SEC504 S2 - Nmap mastery'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Asset Discovery with Masscan',
            'module': 'SEC504 Section 2',
            'topics': 'Shadow cloud discovery, Masscan, cloud asset enumeration, unauthorized cloud resources, rapid scanning',
            'prerequisites': '["Network and Host Scanning with Nmap"]',
            'tags': 'Course: SANS-SEC504, Career Path: Cloud Security, Career Path: Pentester',
            'notes': 'SEC504 S2 - Cloud scanning'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Windows SMB Security Investigation',
            'module': 'SEC504 Section 2',
            'topics': 'SMB protocol security, SMB vulnerabilities, lateral movement via SMB, SMB relay attacks, SMB hardening',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist, Career Path: Blue Teamer',
            'notes': 'SEC504 S2 - SMB security'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Hayabusa and Sigma Rules for Detection',
            'module': 'SEC504 Section 2',
            'topics': 'Hayabusa tool, Sigma rule implementation, Windows event log analysis, detection rules, threat hunting',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Blue Teamer, Career Path: Threat Hunter',
            'notes': 'SEC504 S2 - Hayabusa and Sigma'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Detecting Password Spray Attacks',
            'module': 'SEC504 Section 2',
            'topics': 'Password spray detection, authentication monitoring, failed login analysis, detection strategies, attack patterns',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Blue Teamer, Career Path: SOC Analyst',
            'notes': 'SEC504 S2 - Password spray detection'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Netcat for Network Manipulation',
            'module': 'SEC504 Section 2',
            'topics': 'Netcat usage, network testing, port listening, banner grabbing, reverse shells, network troubleshooting',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester',
            'notes': 'SEC504 S2 - Netcat uses'
        },

        # Section 3: Password Attacks (7 lessons)
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Password Attack Methodologies',
            'module': 'SEC504 Section 3',
            'topics': 'Password guessing, brute force, dictionary attacks, password spray, credential stuffing, attack strategies',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC504 S3 - Password attacks'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Password Guessing with Legba',
            'module': 'SEC504 Section 3',
            'topics': 'Legba tool, targeted guessing, credential testing, service authentication, attack automation',
            'prerequisites': '["Password Attack Methodologies"]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester',
            'notes': 'SEC504 S3 - Legba tool'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Microsoft 365 Authentication Attacks',
            'module': 'SEC504 Section 3',
            'topics': 'M365 attacks, bypassing MFA, conditional access bypass, Azure AD authentication, cloud auth weaknesses',
            'prerequisites': '["Password Attack Methodologies"]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester, Career Path: Cloud Security',
            'notes': 'SEC504 S3 - M365 attacks'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Understanding Windows Password Hashes',
            'module': 'SEC504 Section 3',
            'topics': 'NTLM hashes, NTLMv2, Kerberos tickets, hash extraction, hash storage, Windows authentication',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester, Career Path: DFIR Specialist',
            'notes': 'SEC504 S3 - Password hashes'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Password Cracking with Hashcat',
            'module': 'SEC504 Section 3',
            'topics': 'Hashcat, GPU cracking, rule-based attacks, wordlist generation, hybrid attacks, cracking strategies',
            'prerequisites': '["Understanding Windows Password Hashes"]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC504 S3 - Hashcat cracking'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Metasploit Framework Exploitation',
            'module': 'SEC504 Section 3',
            'topics': 'Metasploit usage, exploit modules, payloads, post-exploitation, meterpreter, framework architecture',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC504 S3 - Metasploit'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'Offensive AI for Password Attacks',
            'module': 'SEC504 Section 3',
            'topics': 'AI-powered attacks, GenAI for password generation, intelligent wordlist creation, ML-assisted cracking',
            'prerequisites': '["Password Cracking with Hashcat"]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester, Career Path: AI Security',
            'notes': 'SEC504 S3 - AI for attacks'
        },

        # Section 4: Web Application Attacks (5 lessons)
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Forced Browsing and IDOR Attacks',
            'module': 'SEC504 Section 4',
            'topics': 'Forced browsing, IDOR vulnerabilities, access control bypass, direct object references, enumeration',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester',
            'notes': 'SEC504 S4 - Forced browsing'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Command Injection Exploitation',
            'module': 'SEC504 Section 4',
            'topics': 'Command injection, OS command execution, blind command injection, injection vectors, prevention',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester',
            'notes': 'SEC504 S4 - Command injection'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Cross-Site Scripting (XSS) Attacks',
            'module': 'SEC504 Section 4',
            'topics': 'XSS types (reflected, stored, DOM), XSS payloads, filter bypass, XSS exploitation, BeEF integration',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester',
            'notes': 'SEC504 S4 - XSS attacks'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'SQL Injection Exploitation',
            'module': 'SEC504 Section 4',
            'topics': 'SQL injection types, blind SQLi, time-based SQLi, union-based attacks, sqlmap, database extraction',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester',
            'notes': 'SEC504 S4 - SQL injection'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'API Security Testing and Exploitation',
            'module': 'SEC504 Section 4',
            'topics': 'API vulnerabilities, REST API testing, authentication bypass, parameter tampering, API fuzzing',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Pentester',
            'notes': 'SEC504 S4 - API attacks'
        },

        # Section 5: Post-Exploitation (6 lessons)
        {
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Endpoint Security Bypass Techniques',
            'module': 'SEC504 Section 5',
            'topics': 'EDR evasion, application allow list bypass, defense evasion, AV bypass, security control circumvention',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Red Teamer, Career Path: Pentester',
            'notes': 'SEC504 S5 - Endpoint bypass'
        },
        {
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Pivoting and Lateral Movement with C2',
            'module': 'SEC504 Section 5',
            'topics': 'C2 frameworks, pivoting techniques, network tunneling, lateral movement, command and control infrastructure',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Red Teamer, Career Path: Pentester',
            'notes': 'SEC504 S5 - Pivoting and C2'
        },
        {
            'domain': 'red_team',
            'difficulty': 2,
            'title': 'Windows Network Hijacking with Responder',
            'module': 'SEC504 Section 5',
            'topics': 'Responder tool, LLMNR poisoning, NBT-NS spoofing, credential capture, man-in-the-middle attacks',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: Red Teamer, Career Path: Pentester',
            'notes': 'SEC504 S5 - Responder attacks'
        },
        {
            'domain': 'red_team',
            'difficulty': 2,
            'title': 'Establishing Persistence with Metasploit',
            'module': 'SEC504 Section 5',
            'topics': 'Persistence mechanisms, backdoors, scheduled tasks, registry modifications, startup persistence',
            'prerequisites': '["Metasploit Framework Exploitation"]',
            'tags': 'Course: SANS-SEC504, Career Path: Red Teamer, Career Path: Pentester',
            'notes': 'SEC504 S5 - Persistence'
        },
        {
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'AI Prompt Injection Attacks',
            'module': 'SEC504 Section 5',
            'topics': 'Prompt injection, jailbreaking LLMs, bypassing guardrails, indirect prompt injection, AI system exploitation',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC504, Career Path: AI Security, Career Path: Pentester',
            'notes': 'SEC504 S5 - AI attacks'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Detecting Post-Exploitation Activity',
            'module': 'SEC504 Section 5',
            'topics': 'Post-exploitation detection, lateral movement indicators, persistence detection, C2 communications, forensic artifacts',
            'prerequisites': '["Dynamic Approach to Incident Response (DAIR)"]',
            'tags': 'Course: SANS-SEC504, Career Path: DFIR Specialist, Career Path: Threat Hunter',
            'notes': 'SEC504 S5 - Detecting post-exploit'
        },
    ]
    all_lessons.extend(sec504_lessons)

    # Continue with remaining courses...
    # For brevity, I'll add key lessons from each remaining course

    # SEC510: Cloud Security Engineering (cloud domain) - 15 lessons
    sec510_lessons = [
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud IAM Fundamentals and Best Practices', 'module': 'SEC510 Section 1', 'topics': 'Cloud IAM, identity management, access control, least privilege, IAM policy design, role-based access', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S1 - IAM fundamentals'},
        {'domain': 'cloud', 'difficulty': 3, 'title': 'Virtual Machine Credential Exposure', 'module': 'SEC510 Section 1', 'topics': 'VM credential attacks, metadata exploitation, instance identity, credential theft, managed identity abuse', 'prerequisites': '["Cloud IAM Fundamentals and Best Practices"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S1 - VM credential exposure'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Broken Access Control and IAM Policy Analysis', 'module': 'SEC510 Section 1', 'topics': 'Policy analysis, misconfiguration detection, access analyzer, policy simulation, privilege boundaries', 'prerequisites': '["Cloud IAM Fundamentals and Best Practices"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S1 - Policy analysis'},
        {'domain': 'cloud', 'difficulty': 3, 'title': 'IAM Privilege Escalation Techniques', 'module': 'SEC510 Section 1', 'topics': 'Privilege escalation paths, IAM exploitation, permission abuse, role assumption, escalation vectors', 'prerequisites': '["Broken Access Control and IAM Policy Analysis"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S1 - Privilege escalation'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Virtual Network Security', 'module': 'SEC510 Section 2', 'topics': 'VPC/VNet security, network isolation, security groups, NACLs, network architecture, ingress/egress control', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S2 - Network security'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Protecting Public Virtual Machines', 'module': 'SEC510 Section 2', 'topics': 'VM hardening, exposure minimization, network controls, bastion hosts, SSH security, public VM risks', 'prerequisites': '["Cloud Virtual Network Security"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S2 - Public VM protection'},
        {'domain': 'cloud', 'difficulty': 3, 'title': 'Private Endpoint Security and Abuse', 'module': 'SEC510 Section 2', 'topics': 'Private endpoints, VPC endpoints, PrivateLink, data exfiltration, service endpoints, endpoint abuse', 'prerequisites': '["Cloud Virtual Network Security"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S2 - Private endpoints'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Traffic Monitoring with Flow Logs', 'module': 'SEC510 Section 2', 'topics': 'Flow logs, VPC flow logs, traffic analysis, network forensics, anomaly detection, log analysis', 'prerequisites': '["Cloud Virtual Network Security"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S2 - Flow logs'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Cryptographic Key Management', 'module': 'SEC510 Section 3', 'topics': 'KMS, key management, key rotation, HSM, envelope encryption, key policies, CMK/CSE', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S3 - Key management'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Ransomware Recovery', 'module': 'SEC510 Section 3', 'topics': 'Ransomware mitigation, versioning, object lock, backup strategies, recovery procedures, immutable storage', 'prerequisites': '["Cloud Cryptographic Key Management"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S3 - Ransomware recovery'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'GenAI-Driven Security Mitigations', 'module': 'SEC510 Section 3', 'topics': 'AI for cloud security, automated remediation, GenAI security tools, intelligent threat response', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security, Career Path: AI Security', 'notes': 'SEC510 S3 - GenAI mitigations'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Securing Cloud GenAI Infrastructure', 'module': 'SEC510 Section 3', 'topics': 'AI infrastructure security, model security, SageMaker/Vertex AI security, AI workload protection', 'prerequisites': '["GenAI-Driven Security Mitigations"]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security, Career Path: AI Security', 'notes': 'SEC510 S3 - GenAI infrastructure'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Serverless Function Security', 'module': 'SEC510 Section 4', 'topics': 'Lambda/Functions security, serverless risks, function hardening, runtime protection, event-driven security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S4 - Serverless security'},
        {'domain': 'cloud', 'difficulty': 3, 'title': 'Cloud Customer IAM Exploitation', 'module': 'SEC510 Section 4', 'topics': 'Cognito attacks, Auth0 abuse, CIAM vulnerabilities, account takeover, authentication bypass', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S4 - CIAM exploitation'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Multicloud Security and Workload Identity Federation', 'module': 'SEC510 Section 5', 'topics': 'Multicloud IAM, cross-cloud access, workload identity, federated authentication, cloud interoperability', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC510, Career Path: Cloud Security', 'notes': 'SEC510 S5 - Multicloud security'},
    ]
    all_lessons.extend(sec510_lessons)

    # SEC511: Cybersecurity Engineering (blue_team, threat_hunting) - 12 lessons
    sec511_lessons = [
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Adversary Tactics and Threat Informed Defense', 'module': 'SEC511 Section 1', 'topics': 'Adversary TTPs, threat informed defense, MITRE ATT&CK, cyber defense principles, security frameworks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer, Career Path: Threat Hunter', 'notes': 'SEC511 S1 - Threat informed defense'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Security Onion for Network Security Monitoring', 'module': 'SEC511 Section 1', 'topics': 'Security Onion 2.x, NSM platform, Zeek, Suricata, integrated monitoring, security analytics', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer, Career Path: SOC Analyst', 'notes': 'SEC511 S1 - Security Onion'},
        {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Threat Hunting Fundamentals', 'module': 'SEC511 Section 1', 'topics': 'Threat hunting methodology, hypothesis-driven hunting, hunt missions, hunting maturity, hunt frameworks', 'prerequisites': '["Adversary Tactics and Threat Informed Defense"]', 'tags': 'Course: SANS-SEC511, Career Path: Threat Hunter', 'notes': 'SEC511 S1 - Threat hunting'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'GenAI/LLM for Cybersecurity Engineering', 'module': 'SEC511 Section 1', 'topics': 'LLM for security, AI-assisted analysis, GenAI in SOC, automated investigation, AI tools', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer, Career Path: AI Security', 'notes': 'SEC511 S1 - GenAI for security'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Web Application Firewalls with ModSecurity', 'module': 'SEC511 Section 2', 'topics': 'ModSecurity, WAF rules, OWASP CRS, web attack prevention, rule tuning, application protection', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer', 'notes': 'SEC511 S2 - ModSecurity WAF'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'TLS Decryption for Network Analysis', 'module': 'SEC511 Section 2', 'topics': 'TLS decryption, SSL inspection, encrypted traffic analysis, Wireshark decryption, certificate management', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer, Career Path: DFIR Specialist', 'notes': 'SEC511 S2 - TLS decryption'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Intrusion Detection Honeypots', 'module': 'SEC511 Section 2', 'topics': 'Honeypot deployment, deception technology, attacker interaction, threat intelligence, early warning', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer, Career Path: Threat Hunter', 'notes': 'SEC511 S2 - Honeypots'},
        {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Network Threat Hunting with Zeek', 'module': 'SEC511 Section 3', 'topics': 'Zeek (Bro), protocol analysis, network hunting, pcap analysis, file carving, script customization', 'prerequisites': '["Threat Hunting Fundamentals"]', 'tags': 'Course: SANS-SEC511, Career Path: Threat Hunter', 'notes': 'SEC511 S3 - Zeek hunting'},
        {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Detecting TLS Certificate and User-Agent Anomalies', 'module': 'SEC511 Section 3', 'topics': 'TLS fingerprinting, certificate anomalies, user-agent analysis, JA3/JA3S, behavioral detection', 'prerequisites': '["Network Threat Hunting with Zeek"]', 'tags': 'Course: SANS-SEC511, Career Path: Threat Hunter', 'notes': 'SEC511 S3 - TLS anomalies'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Sysmon for Endpoint Visibility', 'module': 'SEC511 Section 4', 'topics': 'Sysmon deployment, configuration, event types, process monitoring, network connections, file creation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer, Career Path: DFIR Specialist', 'notes': 'SEC511 S4 - Sysmon'},
        {'domain': 'blue_team', 'difficulty': 2, 'title': 'Application Control with AppLocker', 'module': 'SEC511 Section 4', 'topics': 'AppLocker, application allow listing, executable control, DLL control, script control, bypass prevention', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: Blue Teamer', 'notes': 'SEC511 S4 - AppLocker'},
        {'domain': 'ai_security', 'difficulty': 2, 'title': 'Defending AI/LLM Applications', 'module': 'SEC511 Section 5', 'topics': 'LLM application defense, AI security controls, prompt injection defense, model security, AI workload protection', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC511, Career Path: AI Security, Career Path: Blue Teamer', 'notes': 'SEC511 S5 - AI/LLM defense'},
    ]
    all_lessons.extend(sec511_lessons)

    # SEC535: Offensive AI - Already have some, add new ones (10 lessons)
    sec535_lessons = [
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'AI-Powered Penetration Testing Reconnaissance', 'module': 'SEC535 Section 1', 'topics': 'AI for OSINT, automated recon, LLM-assisted enumeration, intelligent target profiling, AI recon tools', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC535, Career Path: Pentester, Career Path: AI Security', 'notes': 'SEC535 S1 - AI recon'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'Automated Vulnerability Exploitation with AI', 'module': 'SEC535 Section 1', 'topics': 'AI exploit generation, automated exploitation, Metasploit with AI, vulnerability chaining, intelligent payloads', 'prerequisites': '["AI-Powered Penetration Testing Reconnaissance"]', 'tags': 'Course: SANS-SEC535, Career Path: Pentester, Career Path: AI Security', 'notes': 'SEC535 S1 - AI exploitation'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'AI for SQL Injection (AInjection)', 'module': 'SEC535 Section 1', 'topics': 'AI-assisted SQLi, automated injection, intelligent payloads, bypass generation, LLM for web exploits', 'prerequisites': '["Automated Vulnerability Exploitation with AI"]', 'tags': 'Course: SANS-SEC535, Career Path: Pentester, Career Path: AI Security', 'notes': 'SEC535 S1 - AI SQLi'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'Building AI-Powered Phishing (PhishGPT)', 'module': 'SEC535 Section 2', 'topics': 'PhishGPT, AI phishing generation, personalized lures, social engineering automation, spear phishing', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC535, Career Path: Pentester, Career Path: AI Security', 'notes': 'SEC535 S2 - PhishGPT'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'Audio Deepfakes and Voice Cloning', 'module': 'SEC535 Section 2', 'topics': 'Voice cloning, ElevenLabs, audio deepfakes, vishing attacks, AI voice generation, speaker impersonation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC535, Career Path: Pentester, Career Path: AI Security', 'notes': 'SEC535 S2 - Voice cloning'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'Image and Video Deepfakes', 'module': 'SEC535 Section 2', 'topics': 'Video deepfakes, image manipulation, face swapping, synthetic media, deepfake generation, detection evasion', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC535, Career Path: Pentester, Career Path: AI Security', 'notes': 'SEC535 S2 - Video deepfakes'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'AI-Assisted Patch Diffing', 'module': 'SEC535 Section 2', 'topics': 'Patch analysis, vulnerability discovery, diff analysis, 0-day hunting, AI code analysis, exploit development', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC535, Career Path: Pentester, Career Path: AI Security', 'notes': 'SEC535 S2 - Patch diffing'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'Writing Malware with AI', 'module': 'SEC535 Section 3', 'topics': 'AI malware generation, code obfuscation, polymorphic malware, evasion techniques, automated coding', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC535, Career Path: Red Teamer, Career Path: AI Security', 'notes': 'SEC535 S3 - AI malware'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'Agentic Malware Development', 'module': 'SEC535 Section 3', 'topics': 'Autonomous malware, agentic systems, self-modifying code, intelligent persistence, adaptive attacks', 'prerequisites': '["Writing Malware with AI"]', 'tags': 'Course: SANS-SEC535, Career Path: Red Teamer, Career Path: AI Security', 'notes': 'SEC535 S3 - Agentic malware'},
        {'domain': 'ai_security', 'difficulty': 3, 'title': 'Bypassing Security Controls with AI', 'module': 'SEC535 Section 3', 'topics': 'AI evasion, AV bypass, EDR evasion, intelligent obfuscation, defense circumvention, AI-powered attacks', 'prerequisites': '["Writing Malware with AI"]', 'tags': 'Course: SANS-SEC535, Career Path: Red Teamer, Career Path: AI Security', 'notes': 'SEC535 S3 - AI bypass'},
    ]
    all_lessons.extend(sec535_lessons)

    # SEC541: Cloud Security Threat Detection (cloud, blue_team) - 12 lessons
    sec541_lessons = [
        {'domain': 'cloud', 'difficulty': 3, 'title': 'Cloud Attack Analysis Methodology', 'module': 'SEC541 Section 1', 'topics': 'Cloud attack patterns, TTPs, kill chain, attack analysis, threat modeling, cloud security incidents', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security, Career Path: Threat Hunter', 'notes': 'SEC541 S1 - Attack analysis'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Detection Engineering for Cloud', 'module': 'SEC541 Section 1', 'topics': 'Cloud detection engineering, rule creation, alert development, detection testing, cloud-specific detections', 'prerequisites': '["Cloud Attack Analysis Methodology"]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security, Career Path: Blue Teamer', 'notes': 'SEC541 S1 - Detection engineering'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'JSON Log Parsing for Cloud Security', 'module': 'SEC541 Section 1', 'topics': 'CloudTrail logs, JSON parsing, log analysis, JMESPath, structured logging, cloud forensics', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S1 - JSON parsing'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Network Traffic Analysis', 'module': 'SEC541 Section 1', 'topics': 'VPC traffic analysis, packet capture, network forensics, traffic mirroring, cloud network monitoring', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S1 - Network analysis'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Kubernetes Command and Control Detection', 'module': 'SEC541 Section 2', 'topics': 'K8s security, container C2, pod monitoring, Kubernetes logs, container threat detection', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S2 - K8s C2 detection'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Cryptojacking Detection', 'module': 'SEC541 Section 2', 'topics': 'Cryptomining detection, resource abuse, unauthorized compute, billing anomalies, cryptojacking indicators', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S2 - Cryptojacking'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Storage Ransomware Detection', 'module': 'SEC541 Section 2', 'topics': 'Ransomware in cloud, S3 encryption attacks, mass deletion detection, version tampering, data hostage', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S2 - Cloud ransomware'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'eBPF for Cloud Threat Detection', 'module': 'SEC541 Section 2', 'topics': 'eBPF, kernel-level monitoring, syscall tracking, advanced visibility, custom detections', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S2 - eBPF'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Microsoft 365 Attack Investigation', 'module': 'SEC541 Section 4', 'topics': 'M365 forensics, email investigation, Teams security, SharePoint incidents, O365 logs', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S4 - M365 investigation'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Azure Sentinel and Advanced KQL', 'module': 'SEC541 Section 4', 'topics': 'Sentinel SIEM, KQL query language, hunting queries, workbooks, analytics rules, automation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S4 - Sentinel KQL'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Incident Response Automation', 'module': 'SEC541 Section 5', 'topics': 'IR automation, SOAR in cloud, automated remediation, runbooks, orchestration, response playbooks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security', 'notes': 'SEC541 S5 - IR automation'},
        {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud Forensic Workflow Implementation', 'module': 'SEC541 Section 5', 'topics': 'Cloud forensics, evidence collection, disk imaging, memory acquisition, forensic tools, chain of custody', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC541, Career Path: Cloud Security, Career Path: DFIR Specialist', 'notes': 'SEC541 S5 - Forensics'},
    ]
    all_lessons.extend(sec541_lessons)

    # SEC542: Web App Pentesting (pentest) - 12 lessons
    sec542_lessons = [
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Web Application Assessment Methodologies', 'module': 'SEC542 Section 1', 'topics': 'Web app testing methodology, OWASP testing guide, assessment phases, planning, execution', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S1 - Assessment methodology'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Burp Suite Professional for Web Testing', 'module': 'SEC542 Section 1', 'topics': 'Burp Suite, interception proxy, scanner, repeater, intruder, extensions, workflow', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S1 - Burp Suite'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Web Application Fuzzing Techniques', 'module': 'SEC542 Section 2', 'topics': 'Fuzzing, ffuf, directory brute force, parameter discovery, content discovery, wordlists', 'prerequisites': '["Web Application Assessment Methodologies"]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S2 - Fuzzing'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Username Enumeration Techniques', 'module': 'SEC542 Section 2', 'topics': 'User enumeration, timing attacks, error messages, response differences, account discovery', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S2 - User enumeration'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Authentication and Authorization Bypass', 'module': 'SEC542 Section 3', 'topics': 'Auth bypass techniques, session manipulation, privilege escalation, access control flaws, broken auth', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S3 - Auth bypass'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Directory Traversal and Path Manipulation', 'module': 'SEC542 Section 3', 'topics': 'Path traversal, LFI, file inclusion, directory attacks, path manipulation, file access', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S3 - Directory traversal'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Advanced SQL Injection with sqlmap', 'module': 'SEC542 Section 3', 'topics': 'sqlmap usage, automated SQLi, database dumping, WAF bypass, advanced techniques, blind SQLi', 'prerequisites': '["SQL Injection Exploitation"]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S3 - sqlmap'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Browser Exploitation Framework (BeEF)', 'module': 'SEC542 Section 4', 'topics': 'BeEF framework, browser hooking, XSS exploitation, browser attacks, post-exploitation', 'prerequisites': '["Cross-Site Scripting (XSS) Attacks"]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S4 - BeEF'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Server-Side Request Forgery (SSRF) Exploitation', 'module': 'SEC542 Section 4', 'topics': 'SSRF attacks, internal network access, cloud metadata abuse, SSRF chains, exploitation techniques', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S4 - SSRF'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'XML External Entities (XXE) Attacks', 'module': 'SEC542 Section 4', 'topics': 'XXE vulnerabilities, XML parsing, data exfiltration, file disclosure, SSRF via XXE, exploitation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S4 - XXE'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Cross-Site Request Forgery (CSRF) Exploitation', 'module': 'SEC542 Section 5', 'topics': 'CSRF attacks, token bypass, same-site cookies, CSRF exploitation, state-changing operations', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S5 - CSRF'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Nuclei Vulnerability Scanner', 'module': 'SEC542 Section 5', 'topics': 'Nuclei scanner, template-based scanning, custom templates, automation, vulnerability discovery', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC542, Career Path: Pentester', 'notes': 'SEC542 S5 - Nuclei'},
    ]
    all_lessons.extend(sec542_lessons)

    # SEC560: Enterprise Pentesting (pentest, red_team, active_directory) - 15 lessons
    sec560_lessons = [
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Building World-Class Pentest Infrastructure', 'module': 'SEC560 Section 1', 'topics': 'Pentest lab setup, infrastructure design, VM configuration, tooling, kali Linux, attack platform', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Pentester', 'notes': 'SEC560 S1 - Infrastructure'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Credential Stuffing to Exploit Breaches', 'module': 'SEC560 Section 1', 'topics': 'Credential stuffing, breach data usage, password reuse, account compromise, credential databases', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Pentester', 'notes': 'SEC560 S1 - Credential stuffing'},
        {'domain': 'pentest', 'difficulty': 2, 'title': 'Password Spraying with Hydra', 'module': 'SEC560 Section 2', 'topics': 'Hydra tool, password spraying, targeted attacks, service authentication, spray techniques', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Pentester', 'notes': 'SEC560 S2 - Hydra spraying'},
        {'domain': 'red_team', 'difficulty': 2, 'title': 'Command and Control with Sliver', 'module': 'SEC560 Section 2', 'topics': 'Sliver C2, implant deployment, C2 infrastructure, command execution, post-exploitation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S2 - Sliver C2'},
        {'domain': 'red_team', 'difficulty': 2, 'title': 'Command and Control with Empire', 'module': 'SEC560 Section 2', 'topics': 'PowerShell Empire, agent deployment, modules, persistence, lateral movement, C2 operations', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S2 - Empire C2'},
        {'domain': 'red_team', 'difficulty': 2, 'title': 'Situational Awareness with Seatbelt', 'module': 'SEC560 Section 2', 'topics': 'Seatbelt tool, GhostPack, host enumeration, security posture, privilege context, recon', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S2 - Seatbelt'},
        {'domain': 'active_directory', 'difficulty': 3, 'title': 'Domain Mapping with BloodHound', 'module': 'SEC560 Section 3', 'topics': 'BloodHound, AD enumeration, attack paths, graph analysis, privilege escalation paths, SharpHound', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Pentester, Career Path: Red Teamer', 'notes': 'SEC560 S3 - BloodHound'},
        {'domain': 'red_team', 'difficulty': 2, 'title': 'Credential Harvesting with Mimikatz', 'module': 'SEC560 Section 3', 'topics': 'Mimikatz, credential extraction, LSASS dumping, Kerberos tickets, password hashes, sekurlsa', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S3 - Mimikatz'},
        {'domain': 'red_team', 'difficulty': 2, 'title': 'Lateral Movement with Impacket', 'module': 'SEC560 Section 4', 'topics': 'Impacket suite, psexec, smbexec, wmiexec, lateral movement automation, network protocols', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S4 - Impacket'},
        {'domain': 'red_team', 'difficulty': 2, 'title': 'Pass-the-Hash Attacks', 'module': 'SEC560 Section 4', 'topics': 'PTH attacks, hash authentication, NTLM relay, hash exploitation, lateral movement', 'prerequisites': '["Credential Harvesting with Mimikatz"]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S4 - Pass-the-hash'},
        {'domain': 'red_team', 'difficulty': 2, 'title': 'Bypassing Application Control with MSBuild', 'module': 'SEC560 Section 4', 'topics': 'MSBuild abuse, AppLocker bypass, application allow list evasion, LOLBins, defense bypass', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S4 - MSBuild bypass'},
        {'domain': 'active_directory', 'difficulty': 3, 'title': 'Kerberoasting for Privilege Escalation', 'module': 'SEC560 Section 5', 'topics': 'Kerberoasting, SPN enumeration, TGS extraction, service account cracking, AD attacks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Pentester, Career Path: Red Teamer', 'notes': 'SEC560 S5 - Kerberoasting'},
        {'domain': 'active_directory', 'difficulty': 3, 'title': 'Extracting Domain Hashes from NTDS.dit', 'module': 'SEC560 Section 5', 'topics': 'NTDS.dit extraction, domain controller compromise, DCSync, hash dumping, domain admin', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC560 S5 - NTDS extraction'},
        {'domain': 'active_directory', 'difficulty': 3, 'title': 'Golden and Silver Ticket Attacks', 'module': 'SEC560 Section 5', 'topics': 'Golden ticket, silver ticket, Kerberos forging, TGT/TGS crafting, persistence, domain dominance', 'prerequisites': '["Extracting Domain Hashes from NTDS.dit"]', 'tags': 'Course: SANS-SEC560, Career Path: Red Teamer', 'notes': 'SEC560 S5 - Ticket attacks'},
        {'domain': 'cloud', 'difficulty': 3, 'title': 'Azure Penetration Testing', 'module': 'SEC560 Section 5', 'topics': 'Azure pentesting, Entra ID, password spray, privilege escalation, cloud lateral movement, Azure attacks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC560, Career Path: Pentester, Career Path: Cloud Security', 'notes': 'SEC560 S5 - Azure pentesting'},
    ]
    all_lessons.extend(sec560_lessons)

    # SEC587: Advanced OSINT (osint) - 15 lessons
    sec587_lessons = [
        {'domain': 'osint', 'difficulty': 3, 'title': 'Disinformation Detection and Analysis', 'module': 'SEC587 Section 1', 'topics': 'Disinformation, reliability models, NATO analysis, CRAAP test, fake content detection, verification', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S1 - Disinformation'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'Russian OSINT Techniques', 'module': 'SEC587 Section 1', 'topics': 'Russian facial recognition, Russian search engines, Cyrillic OSINT, Russian social media, Yandex', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S1 - Russian OSINT'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'Chinese OSINT and Access Challenges', 'module': 'SEC587 Section 1', 'topics': 'Chinese websites, Great Firewall, Chinese social media, Mandarin OSINT, Baidu, WeChat', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S1 - Chinese OSINT'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'Python for OSINT Automation', 'module': 'SEC587 Section 2', 'topics': 'Python scripting, web scraping, API interaction, automation, BeautifulSoup, requests, selenium', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S2 - Python OSINT'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'Building Automated Intelligence Dashboards', 'module': 'SEC587 Section 2', 'topics': 'Dashboard creation, data visualization, intelligence products, reporting automation, analytics', 'prerequisites': '["Python for OSINT Automation"]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S2 - Dashboards'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'Advanced Image and Video Verification', 'module': 'SEC587 Section 3', 'topics': 'Image forensics, video verification, deepfake detection, manipulation analysis, authenticity verification', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S3 - Image verification'},
        {'domain': 'osint', 'difficulty': 2, 'title': 'Steganography Detection', 'module': 'SEC587 Section 3', 'topics': 'Steganography, hidden data, steganalysis, image forensics, covert communication detection', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S3 - Steganography'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'AI Audio Analysis and Speaker Identification', 'module': 'SEC587 Section 3', 'topics': 'Speaker diarization, voice analysis, audio forensics, speech recognition, speaker identification', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT, Career Path: AI Security', 'notes': 'SEC587 S3 - Audio analysis'},
        {'domain': 'osint', 'difficulty': 2, 'title': 'Gaming Platform OSINT', 'module': 'SEC587 Section 3', 'topics': 'Gaming OSINT, Discord, Twitch, Steam, gamer profiles, in-game intelligence, gaming communities', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S3 - Gaming OSINT'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'Creating False Personas with OPSEC', 'module': 'SEC587 Section 4', 'topics': 'Sock puppets, false identities, OPSEC, attribution management, persona creation, operational security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S4 - Sock puppets'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'Dark Web De-Anonymization Techniques', 'module': 'SEC587 Section 4', 'topics': 'De-anonymization, Tor analysis, hidden service discovery, dark web forensics, attribution', 'prerequisites': '["Dark Web and Tor Investigation"]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S4 - De-anonymization'},
        {'domain': 'osint', 'difficulty': 2, 'title': 'Cryptocurrency Transaction Tracking', 'module': 'SEC587 Section 4', 'topics': 'Blockchain analysis, transaction tracing, wallet clustering, crypto forensics, sanctioned entities', 'prerequisites': '["Cryptocurrency OSINT"]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S4 - Crypto tracking'},
        {'domain': 'osint', 'difficulty': 2, 'title': 'Detecting Modern Drones', 'module': 'SEC587 Section 4', 'topics': 'Drone detection, UAV identification, wireless signals, drone OSINT, aerial surveillance', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S4 - Drone detection'},
        {'domain': 'osint', 'difficulty': 3, 'title': 'OSINT Workflow Automation with N8n', 'module': 'SEC587 Section 5', 'topics': 'N8n workflow automation, OSINT pipelines, automated collection, integration, orchestration', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S5 - N8n automation'},
        {'domain': 'osint', 'difficulty': 2, 'title': 'Aviation and Maritime OSINT', 'module': 'SEC587 Section 5', 'topics': 'Flight tracking, vessel tracking, ADS-B, AIS, FlightAware, MarineTraffic, transportation intelligence', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC587, Career Path: OSINT', 'notes': 'SEC587 S5 - Aviation/maritime'},
    ]
    all_lessons.extend(sec587_lessons)

    # ============================================================================
    # Now add all lessons to CSV
    # ============================================================================

    print("\n" + "=" * 80)
    print("ADDING ALL LESSONS TO CSV")
    print("=" * 80 + "\n")

    added_count = 0
    domain_counts = {}
    difficulty_counts = {1: 0, 2: 0, 3: 0}
    course_counts = {
        'SEC504': 0,
        'SEC510': 0,
        'SEC511': 0,
        'SEC535': 0,
        'SEC541': 0,
        'SEC542': 0,
        'SEC560': 0,
        'SEC587': 0
    }

    for lesson in all_lessons:
        domain = lesson['domain']
        difficulty = lesson['difficulty']

        # Get order_index for this domain
        if domain not in domain_order:
            domain_order[domain] = 1
        order_idx = domain_order[domain]
        domain_order[domain] += 1

        # Count by domain
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

        # Count by difficulty
        difficulty_counts[difficulty] += 1

        # Count by course
        for course_code in course_counts.keys():
            if course_code in lesson['tags']:
                course_counts[course_code] += 1

        new_row = {
            'lesson_number': str(next_lesson_num),
            'order_index': str(order_idx),
            'domain': domain,
            'difficulty': str(difficulty),
            'title': lesson['title'],
            'module': lesson['module'],
            'topics': lesson['topics'],
            'prerequisites': lesson['prerequisites'],
            'status': 'idea',
            'tags': lesson['tags'],
            'notes': lesson['notes']
        }

        rows.append(new_row)

        difficulty_name = {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}[difficulty]
        print(f"Added #{next_lesson_num} [{domain}:{order_idx}]: {lesson['title']} ({difficulty_name})")

        next_lesson_num += 1
        added_count += 1

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['lesson_number', 'order_index', 'domain', 'difficulty', 'title',
                     'module', 'topics', 'prerequisites', 'status', 'tags', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{'=' * 80}")
    print(f"SUCCESS - Added {added_count} lessons from 8 SANS courses")
    print(f"Total lessons in CSV: {len(rows)}")
    print(f"{'=' * 80}\n")

    print("Course Breakdown:")
    for course, count in course_counts.items():
        print(f"  {course}: {count} lessons")

    print(f"\nDifficulty Distribution:")
    print(f"  Beginner: {difficulty_counts[1]}")
    print(f"  Intermediate: {difficulty_counts[2]}")
    print(f"  Advanced: {difficulty_counts[3]}")

    print(f"\nDomains Covered:")
    for domain in sorted(domain_counts.keys()):
        print(f"  {domain}: {domain_counts[domain]} lessons")

if __name__ == '__main__':
    add_8_more_sans_courses()
