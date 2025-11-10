#!/usr/bin/env python3
"""
Add 6 SANS courses to lesson_ideas.csv:
1. SEC411: AI Security Principles and Practices (14 hours, 3 labs)
2. SEC450: SOC Analyst Training (36 hours, 22 labs)
3. SEC467: Social Engineering Security (12 hours, 8 labs)
4. SEC497: Practical OSINT (36 hours, 29 labs)
5. SEC501: Advanced Security Essentials - Enterprise Defender (38 hours, 25 labs)
6. SEC502: Cloud Security Tactical Defense (36 hours, 41 labs)

Total: 172 hours, 128 labs across 6 courses
"""

import csv
from pathlib import Path

def add_all_sans_courses():
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
    # SEC411: AI Security Principles and Practices (ai_security domain)
    # ============================================================================
    print("=" * 80)
    print("SEC411: AI Security Principles and Practices")
    print("=" * 80)

    sec411_lessons = [
        # Note: We already have some SEC411 lessons, so these are ADDITIONAL/updated ones
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'AI Threat Landscape and Attack Surfaces',
            'module': 'SEC411 Section 1 - KNOW',
            'topics': 'AI attack surfaces, LLM vulnerabilities, OWASP Top 10 for LLMs, AI-specific threats, threat modeling for AI systems',
            'prerequisites': '["AI Security 101: Understanding AI Threats"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security, Career Path: Security Engineer',
            'notes': 'SEC411 S1 - Understanding AI threats'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'Tokenization Security in LLMs',
            'module': 'SEC411 Section 1 - KNOW',
            'topics': 'Tokenization process, token-level attacks, security implications, bypass techniques, tokenization vulnerabilities',
            'prerequisites': '["LLM Architecture and Security Fundamentals"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security',
            'notes': 'SEC411 S1 - Token-level security'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'MITRE ATLAS Framework for AI Threats',
            'module': 'SEC411 Section 1 - KNOW',
            'topics': 'MITRE ATLAS framework, AI-specific tactics, techniques, procedures, mapping AI threats, adversarial ML techniques',
            'prerequisites': '["AI Threat Landscape and Attack Surfaces"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security, Career Path: Security Engineer',
            'notes': 'SEC411 S1 - AI threat framework'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'Securing AI Training Pipelines',
            'module': 'SEC411 Section 2 - DEFEND',
            'topics': 'Training pipeline security, data poisoning prevention, model integrity, supply chain security, secure model training',
            'prerequisites': '["AI Threat Landscape and Attack Surfaces"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security, Career Path: Security Engineer',
            'notes': 'SEC411 S2 - Training security'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'Inference Environment Security',
            'module': 'SEC411 Section 2 - DEFEND',
            'topics': 'Inference protection, runtime security, model serving security, inference attacks, deployment hardening',
            'prerequisites': '["Securing AI Training Pipelines"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security',
            'notes': 'SEC411 S2 - Inference security'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'RAG System Security and Controls',
            'module': 'SEC411 Section 2 - DEFEND',
            'topics': 'RAG architecture security, retrieval attacks, context injection, RAG-specific controls, vector database security',
            'prerequisites': '["Retrieval-Augmented Generation (RAG) Security"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security',
            'notes': 'SEC411 S2 - RAG security controls'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'Input/Output Filtering for LLMs',
            'module': 'SEC411 Section 2 - DEFEND',
            'topics': 'Input validation, output filtering, content moderation, toxic output prevention, filtering strategies',
            'prerequisites': '["Prompt Injection Defense Strategies"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security',
            'notes': 'SEC411 S2 - I/O filtering'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'AI Guardrail Implementation',
            'module': 'SEC411 Section 2 - DEFEND',
            'topics': 'Guardrail design, policy enforcement, safety mechanisms, behavioral constraints, guardrail testing',
            'prerequisites': '["Input/Output Filtering for LLMs"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security',
            'notes': 'SEC411 S2 - Implementing guardrails'
        },
        {
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'Secure LLM Application Deployment',
            'module': 'SEC411 Section 3 - DEPLOY',
            'topics': 'Production deployment security, application integration, secure configuration, deployment best practices',
            'prerequisites': '["AI Guardrail Implementation"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security, Career Path: Security Engineer',
            'notes': 'SEC411 S3 - Production deployment'
        },
        {
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'LLM API Security',
            'module': 'SEC411 Section 3 - DEPLOY',
            'topics': 'API security for LLMs, authentication, authorization, rate limiting, API abuse prevention, secure API design',
            'prerequisites': '["Secure LLM Application Deployment"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security',
            'notes': 'SEC411 S3 - API security'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'Integrating LLMs into SOC Workflows',
            'module': 'SEC411 Section 3 - DEPLOY',
            'topics': 'SOC integration, workflow automation, AI-assisted analysis, security operations enhancement, practical use cases',
            'prerequisites': '["Secure LLM Application Deployment"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security, Career Path: SOC Analyst',
            'notes': 'SEC411 S3 - SOC integration'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'AI Monitoring and Observability',
            'module': 'SEC411 Section 3 - DEPLOY',
            'topics': 'AI system monitoring, behavioral analysis, anomaly detection, observability strategies, performance tracking',
            'prerequisites': '["Secure LLM Application Deployment"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security, Career Path: Blue Teamer',
            'notes': 'SEC411 S3 - Monitoring AI systems'
        },
        {
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'Defending Agentic AI Systems',
            'module': 'SEC411 Section 3 - DEPLOY',
            'topics': 'Agentic system security, autonomous agents, reasoning model security, advanced AI threats, emerging defenses',
            'prerequisites': '["AI Monitoring and Observability"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security',
            'notes': 'SEC411 S3 - Advanced agentic systems'
        },
        {
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'NIST AI Risk Management Framework',
            'module': 'SEC411 All Sections',
            'topics': 'NIST AI RMF, risk assessment, AI governance, compliance, framework implementation, risk mitigation',
            'prerequisites': '["AI Threat Landscape and Attack Surfaces"]',
            'tags': 'Course: SANS-SEC411, Career Path: AI Security, Career Path: GRC Analyst',
            'notes': 'SEC411 - AI risk management'
        },
    ]
    all_lessons.extend(sec411_lessons)

    # ============================================================================
    # SEC450: SOC Analyst Training (blue_team, dfir domains)
    # ============================================================================
    print("=" * 80)
    print("SEC450: SOC Analyst Training - Applied Skills for Cyber Defense Operations")
    print("=" * 80)

    sec450_lessons = [
        # Section 1: Blue Team Tools and Operations (5 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Foundations of Security Operations',
            'module': 'SEC450 Section 1',
            'topics': 'SOC fundamentals, security operations principles, SOC roles, responsibilities, operational workflows, SOC maturity',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S1 - SOC foundations'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Cyber Threat Intelligence for SOC Analysts',
            'module': 'SEC450 Section 1',
            'topics': 'CTI fundamentals, threat-informed defense, TIPs (Threat Intelligence Platforms), intelligence consumption, IOC management',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S1 - CTI for SOC'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'SOC Data Sources and SIEM',
            'module': 'SEC450 Section 1',
            'topics': 'SOC data sources, SIEM fundamentals, log analysis, search queries, correlation rules, SIEM workflow',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S1 - SIEM basics'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Case Management Systems and Playbooks',
            'module': 'SEC450 Section 1',
            'topics': 'Case management, playbook design, workflow automation, incident tracking, SOC orchestration, SOAR concepts',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S1 - Case management'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'AI-Powered SOC: LLMs for Investigation and Coding',
            'module': 'SEC450 Section 1',
            'topics': 'GenAI for SOC, LLM prompting, AI-assisted investigation, automated coding, ChatGPT for analysts, practical AI use',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: AI Security',
            'notes': 'SEC450 S1 - AI in SOC'
        },

        # Section 2: Understanding Your Network (7 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Network Visibility and Traffic Analysis',
            'module': 'SEC450 Section 2',
            'topics': 'Network monitoring, traffic analysis, packet capture, network telemetry, visibility strategies, traffic baseline',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S2 - Network visibility'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'DNS Monitoring and Threat Detection',
            'module': 'SEC450 Section 2',
            'topics': 'DNS monitoring, malicious DNS detection, DNS tunneling, DGA detection, DNS-based threats, analysis techniques',
            'prerequisites': '["Network Visibility and Traffic Analysis"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S2 - DNS analysis'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'HTTP Traffic Dissection and Analysis',
            'module': 'SEC450 Section 2',
            'topics': 'HTTP protocol analysis, Wireshark workflow, HTTP threats, web attack detection, traffic dissection techniques',
            'prerequisites': '["Network Visibility and Traffic Analysis"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: DFIR Specialist',
            'notes': 'SEC450 S2 - HTTP analysis'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Modern HTTP (HTTP/2 and HTTP/3) Analysis',
            'module': 'SEC450 Section 2',
            'topics': 'HTTP/2 protocol, HTTP/3/QUIC, modern web protocols, decoding techniques, analyzing encrypted protocols',
            'prerequisites': '["HTTP Traffic Dissection and Analysis"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst',
            'notes': 'SEC450 S2 - Modern HTTP'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'TLS Traffic Analysis without Decryption',
            'module': 'SEC450 Section 2',
            'topics': 'Encrypted traffic analysis, TLS fingerprinting, JA3/JA3S, metadata analysis, threat detection in encryption',
            'prerequisites': '["Network Visibility and Traffic Analysis"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S2 - Encrypted traffic'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Post-Exploitation Protocol Analysis',
            'module': 'SEC450 Section 2',
            'topics': 'C2 traffic detection, post-exploitation indicators, lateral movement detection, protocol abuse, beacon analysis',
            'prerequisites': '["Network Visibility and Traffic Analysis"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S2 - C2 detection'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Wireshark for SOC Analysts',
            'module': 'SEC450 Section 2',
            'topics': 'Wireshark fundamentals, display filters, protocol analysis, capture filters, pcap analysis workflow, troubleshooting',
            'prerequisites': '["Network Visibility and Traffic Analysis"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: DFIR Specialist',
            'notes': 'SEC450 S2 - Wireshark skills'
        },

        # Section 3: Endpoints, Logs, and Files (6 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Advanced SIEM for Threat Detection',
            'module': 'SEC450 Section 3',
            'topics': 'Advanced SIEM queries, correlation rules, threat hunting with SIEM, building visualizations, dashboards, analytics',
            'prerequisites': '["SOC Data Sources and SIEM"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S3 - Advanced SIEM'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Windows and Linux Logging for Detection',
            'module': 'SEC450 Section 3',
            'topics': 'Windows Event Logs, Sysmon, Linux logging (syslog, auditd), key log sources, logging configuration, log enrichment',
            'prerequisites': '["SOC Data Sources and SIEM"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S3 - OS logging'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Key Log Events for Threat Detection',
            'module': 'SEC450 Section 3',
            'topics': 'Critical event IDs, log interpretation, attack indicators, authentication logs, process creation, lateral movement logs',
            'prerequisites': '["Windows and Linux Logging for Detection"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S3 - Key events'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Logging for SOC Analysts',
            'module': 'SEC450 Section 3',
            'topics': 'Cloud logging (AWS CloudTrail, Azure Monitor, GCP Cloud Logging), cloud attack detection, cloud log analysis',
            'prerequisites': '["SOC Data Sources and SIEM"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Cloud Security',
            'notes': 'SEC450 S3 - Cloud logs'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Malware Analysis Fundamentals for SOC',
            'module': 'SEC450 Section 3',
            'topics': 'Suspicious file triage, static analysis, malware sandboxes, behavioral analysis, file analysis workflow',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Malware Analyst',
            'notes': 'SEC450 S3 - File analysis'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Reverse Engineering Common Malware File Types',
            'module': 'SEC450 Section 3',
            'topics': 'Office macros, PowerShell scripts, JavaScript, reverse engineering basics, deobfuscation, file format analysis',
            'prerequisites': '["Malware Analysis Fundamentals for SOC"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Malware Analyst',
            'notes': 'SEC450 S3 - Malware RE basics'
        },

        # Section 4: Triage and Analysis (5 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Phishing Prevention and Detection',
            'module': 'SEC450 Section 4',
            'topics': 'Phishing techniques, email security, phishing detection, user training, technical controls, phishing analysis',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S4 - Phishing defense'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Investigating Phishing: Headers and Spoofing',
            'module': 'SEC450 Section 4',
            'topics': 'Email header analysis, spoofing detection, SPF/DKIM/DMARC, email authentication, phishing investigation techniques',
            'prerequisites': '["Phishing Prevention and Detection"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: DFIR Specialist',
            'notes': 'SEC450 S4 - Email forensics'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Analyzing Malicious Email Attachments',
            'module': 'SEC450 Section 4',
            'topics': 'Modern attachment threats, macro analysis, malicious documents, attachment sandboxing, file detonation',
            'prerequisites': '["Investigating Phishing: Headers and Spoofing"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Malware Analyst',
            'notes': 'SEC450 S4 - Malicious attachments'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Alert Triage and Prioritization',
            'module': 'SEC450 Section 4',
            'topics': 'Triage process, alert prioritization, severity assessment, CVSS, risk-based triage, queue management',
            'prerequisites': '["Foundations of Security Operations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S4 - Alert triage'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Structured Analysis Techniques for Investigations',
            'module': 'SEC450 Section 4',
            'topics': 'Structured analysis, analytical frameworks, hypothesis testing, avoiding cognitive bias, investigation methodology',
            'prerequisites': '["Alert Triage and Prioritization"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S4 - Analytical rigor'
        },

        # Section 5: Continuous Improvement (7 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Detection Engineering Fundamentals',
            'module': 'SEC450 Section 5',
            'topics': 'Detection engineering, creating detections, testing detections, detection lifecycle, coverage assessment',
            'prerequisites': '["Advanced SIEM for Threat Detection"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S5 - Detection engineering'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'File-Based Detection with YARA-X',
            'module': 'SEC450 Section 5',
            'topics': 'YARA rules, YARA-X, file-based detection, signature creation, pattern matching, malware hunting',
            'prerequisites': '["Detection Engineering Fundamentals"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Malware Analyst',
            'notes': 'SEC450 S5 - YARA detection'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Log-Based Detection with Sigma',
            'module': 'SEC450 Section 5',
            'topics': 'Sigma rules, log-based detection, SIEM-agnostic rules, Sigma syntax, community rules, rule development',
            'prerequisites': '["Detection Engineering Fundamentals"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Threat Hunter',
            'notes': 'SEC450 S5 - Sigma rules'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Alert Tuning and False Positive Reduction',
            'module': 'SEC450 Section 5',
            'topics': 'Alert tuning, false positive analysis, baselining, detection refinement, noise reduction, tuning strategies',
            'prerequisites': '["Detection Engineering Fundamentals"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S5 - Alert tuning'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'SOC Automation and Orchestration',
            'module': 'SEC450 Section 5',
            'topics': 'SOAR platforms, automation playbooks, orchestration workflows, response automation, integrating tools',
            'prerequisites': '["Case Management Systems and Playbooks"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: Blue Teamer',
            'notes': 'SEC450 S5 - Automation'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Integrating GenAI into SOC Automation',
            'module': 'SEC450 Section 5',
            'topics': 'AI automation, LLM-powered SOAR, intelligent response, GenAI workflows, AI-assisted orchestration',
            'prerequisites': '["SOC Automation and Orchestration", "AI-Powered SOC: LLMs for Investigation and Coding"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst, Career Path: AI Security',
            'notes': 'SEC450 S5 - AI automation'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Investigation Quality and Burnout Prevention',
            'module': 'SEC450 Section 5',
            'topics': 'Investigation quality, incident documentation, burnout prevention, analyst wellness, team sustainability, career growth',
            'prerequisites': '["Structured Analysis Techniques for Investigations"]',
            'tags': 'Course: SANS-SEC450, Career Path: SOC Analyst',
            'notes': 'SEC450 S5 - Sustainability'
        },
    ]
    all_lessons.extend(sec450_lessons)

    # ============================================================================
    # SEC467: Social Engineering Security (pentest, fundamentals domains)
    # ============================================================================
    print("=" * 80)
    print("SEC467: Social Engineering for Security Professionals")
    print("=" * 80)

    sec467_lessons = [
        # Section 1: Fundamentals, Recon, Phishing (6 lessons)
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Psychology of Social Engineering',
            'module': 'SEC467 Section 1',
            'topics': 'Psychological principles, influence tactics, persuasion techniques, cognitive biases, human vulnerabilities',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC467 S1 - Psychology fundamentals'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Social Engineering Targeting and Reconnaissance',
            'module': 'SEC467 Section 1',
            'topics': 'Target profiling, OSINT for social engineering, information gathering, recon techniques, victim selection',
            'prerequisites': '["Psychology of Social Engineering"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester, Career Path: OSINT',
            'notes': 'SEC467 S1 - Recon and profiling'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Secure and Convincing Phishing Campaigns',
            'module': 'SEC467 Section 1',
            'topics': 'Phishing methodology, convincing pretext creation, email crafting, domain setup, secure infrastructure, OpSec',
            'prerequisites': '["Social Engineering Targeting and Reconnaissance"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC467 S1 - Phishing campaigns'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Phishing Click Tracking and Analytics',
            'module': 'SEC467 Section 1',
            'topics': 'Click tracking, campaign metrics, tracking pixels, analytics, measuring success, data collection',
            'prerequisites': '["Secure and Convincing Phishing Campaigns"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester',
            'notes': 'SEC467 S1 - Tracking clicks'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Social Engineering Toolkit (SET) and Site Cloning',
            'module': 'SEC467 Section 1',
            'topics': 'SET framework, site cloning, credential harvesting, fake login pages, cloning techniques',
            'prerequisites': '["Secure and Convincing Phishing Campaigns"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC467 S1 - SET and cloning'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Secure Phishing Forms and Data Logging',
            'module': 'SEC467 Section 1',
            'topics': 'Form creation, secure data collection, credential logging, data handling, phishing infrastructure',
            'prerequisites': '["Social Engineering Toolkit (SET) and Site Cloning"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester',
            'notes': 'SEC467 S1 - Data logging'
        },

        # Section 2: Advanced Attacks and Physical (6 lessons)
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'USB and Media Drop Attacks',
            'module': 'SEC467 Section 2',
            'topics': 'USB attacks, malicious USB creation, media drop campaigns, BadUSB, rubber ducky, physical drops',
            'prerequisites': '["Psychology of Social Engineering"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC467 S2 - USB attacks'
        },
        {
            'domain': 'red_team',
            'difficulty': 2,
            'title': 'Building PowerShell Payloads',
            'module': 'SEC467 Section 2',
            'topics': 'PowerShell payloads, obfuscation, evasion techniques, payload delivery, encoded commands',
            'prerequisites': '["USB and Media Drop Attacks"]',
            'tags': 'Course: SANS-SEC467, Career Path: Red Teamer, Career Path: Pentester',
            'notes': 'SEC467 S2 - PowerShell payloads'
        },
        {
            'domain': 'red_team',
            'difficulty': 2,
            'title': 'Custom Payload Development',
            'module': 'SEC467 Section 2',
            'topics': 'Payload creation, custom malware, payload obfuscation, evasion, AV bypass, payload delivery mechanisms',
            'prerequisites': '["Building PowerShell Payloads"]',
            'tags': 'Course: SANS-SEC467, Career Path: Red Teamer, Career Path: Pentester',
            'notes': 'SEC467 S2 - Roll your own payload'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Weaponized Document Creation',
            'module': 'SEC467 Section 2',
            'topics': 'Malicious documents, macro payloads, document weaponization, pretty payloads, template injection',
            'prerequisites': '["Custom Payload Development"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC467 S2 - Pretty payloads'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Successful Pretexting Techniques',
            'module': 'SEC467 Section 2',
            'topics': 'Pretexting methodology, building pretexts, impersonation, vishing, phone-based attacks, pretext scenarios',
            'prerequisites': '["Psychology of Social Engineering"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester',
            'notes': 'SEC467 S2 - Pretexting'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Physical Security: Tailgating and Access',
            'module': 'SEC467 Section 2',
            'topics': 'Tailgating, physical access testing, badge cloning, lock picking basics, physical security testing',
            'prerequisites': '["Successful Pretexting Techniques"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC467 S2 - Physical access'
        },

        # Additional lessons
        {
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Social Engineering Ethics and ROE',
            'module': 'SEC467 All Sections',
            'topics': 'Ethical considerations, rules of engagement, scope definition, legal boundaries, responsible testing',
            'prerequisites': '["Psychology of Social Engineering"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester',
            'notes': 'SEC467 - Ethics and legal'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Social Engineering Assessment Reporting',
            'module': 'SEC467 Section 2',
            'topics': 'Report writing, metrics, success measurement, recommendations, user awareness findings, executive summaries',
            'prerequisites': '["Secure and Convincing Phishing Campaigns"]',
            'tags': 'Course: SANS-SEC467, Career Path: Pentester',
            'notes': 'SEC467 S2 - Reporting'
        },
    ]
    all_lessons.extend(sec467_lessons)

    # ============================================================================
    # SEC497: Practical OSINT (osint domain)
    # ============================================================================
    print("=" * 80)
    print("SEC497: Practical Open-Source Intelligence")
    print("=" * 80)

    sec497_lessons = [
        # Section 1: OSINT and OPSEC Fundamentals (5 lessons)
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'The OSINT Process and Methodology',
            'module': 'SEC497 Section 1',
            'topics': 'OSINT lifecycle, intelligence cycle, collection planning, processing, analysis, dissemination, feedback',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Threat Hunter',
            'notes': 'SEC497 S1 - OSINT fundamentals'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'OPSEC for OSINT Investigators',
            'module': 'SEC497 Section 1',
            'topics': 'Operational security, attribution management, sock puppet accounts, OPSEC principles, investigator safety',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S1 - OPSEC'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Canary Tokens for OSINT',
            'module': 'SEC497 Section 1',
            'topics': 'Canary tokens, tracking, tripwires, detection mechanisms, honeytokens, defensive OSINT',
            'prerequisites': '["OPSEC for OSINT Investigators"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Blue Teamer',
            'notes': 'SEC497 S1 - Canary tokens'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'OSINT Tools: Hunchly and Obsidian',
            'module': 'SEC497 Section 1',
            'topics': 'Hunchly web capture, Obsidian note-taking, evidence preservation, investigation documentation, tool workflow',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S1 - Investigation tools'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'OSINT Note Taking and Report Writing',
            'module': 'SEC497 Section 1',
            'topics': 'Effective note-taking, report structure, professional reporting, intelligence products, communication',
            'prerequisites': '["OSINT Tools: Hunchly and Obsidian"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S1 - Documentation'
        },

        # Section 2: Essential OSINT Skills (7 lessons)
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'OSINT Link Collections and Bookmarks',
            'module': 'SEC497 Section 2',
            'topics': 'OSINT resource management, bookmark organization, curated link lists, resource discovery, tool catalogs',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S2 - Resource management'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Web Data Collection and Processing',
            'module': 'SEC497 Section 2',
            'topics': 'Web scraping, Instant Data Scraper, automated collection, data extraction, processing techniques',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S2 - Data scraping'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Metadata Analysis for OSINT',
            'module': 'SEC497 Section 2',
            'topics': 'Metadata extraction, EXIF data, document metadata, file properties, metadata tools, privacy implications',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: DFIR Specialist',
            'notes': 'SEC497 S2 - Metadata'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Geolocation and Mapping',
            'module': 'SEC497 Section 2',
            'topics': 'Geolocation techniques, mapping tools, GPS coordinates, location analysis, visual geolocation',
            'prerequisites': '["Metadata Analysis for OSINT"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S2 - Geolocation'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Image Analysis and Reverse Image Search',
            'module': 'SEC497 Section 2',
            'topics': 'Image OSINT, reverse image search, Google Images, TinEye, Yandex, image analysis techniques',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S2 - Image OSINT'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Facial Recognition and Translations',
            'module': 'SEC497 Section 2',
            'topics': 'Facial recognition tools, PimEyes, translation services, multilingual OSINT, cross-language investigation',
            'prerequisites': '["Image Analysis and Reverse Image Search"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S2 - Facial recognition'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'OSINT Malware Handling',
            'module': 'SEC497 Section 1',
            'topics': 'Safe malware handling, virtual machines, sandboxing, OSINT on malicious sites, investigator safety',
            'prerequisites': '["OPSEC for OSINT Investigators"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S1 - Malware safety'
        },

        # Section 3: Investigating People (7 lessons)
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Privacy Considerations in OSINT',
            'module': 'SEC497 Section 3',
            'topics': 'Privacy ethics, legal considerations, responsible OSINT, data protection, ethical boundaries',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S3 - Privacy and ethics'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Username and Contact Information Research',
            'module': 'SEC497 Section 3',
            'topics': 'Username enumeration, contact info discovery, Keybase, email investigation, phone number OSINT',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S3 - Username research'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Breach Data and Credential Analysis',
            'module': 'SEC497 Section 3',
            'topics': 'Data breach research, HaveIBeenPwned, credential databases, password analysis, breach aggregation',
            'prerequisites': '["Username and Contact Information Research"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Threat Hunter',
            'notes': 'SEC497 S3 - Breach data'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Social Media Analysis and Investigation',
            'module': 'SEC497 Section 3',
            'topics': 'Twitter/X OSINT, Facebook, LinkedIn, Instagram, social media scraping, deleted content recovery, timelines',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S3 - Social media'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Advanced Geolocation Techniques',
            'module': 'SEC497 Section 3',
            'topics': 'Advanced geolocation, landmark identification, visual analysis, environmental clues, location verification',
            'prerequisites': '["Geolocation and Mapping"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S3 - Advanced geolocation'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Bot Detection and AI Content Analysis',
            'module': 'SEC497 Section 3',
            'topics': 'Bot detection, sentiment analysis, trend analysis, AI-generated content detection, deepfakes, synthetic media',
            'prerequisites': '["Social Media Analysis and Investigation"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: AI Security',
            'notes': 'SEC497 S3 - Detecting AI/bots'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Recovering Deleted Social Media Content',
            'module': 'SEC497 Section 3',
            'topics': 'Deleted content recovery, web archives, cached pages, Wayback Machine, timeline reconstruction',
            'prerequisites': '["Social Media Analysis and Investigation"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S3 - Deleted content'
        },

        # Section 4: Websites and Infrastructure (7 lessons)
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'IP Address Research and Analysis',
            'module': 'SEC497 Section 4',
            'topics': 'IP address OSINT, geolocation, ownership, ASN research, IP reputation, common ports',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Threat Hunter',
            'notes': 'SEC497 S4 - IP research'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'WHOIS and DNS Investigation',
            'module': 'SEC497 Section 4',
            'topics': 'WHOIS lookups, DNS records, domain registration, historical DNS, passive DNS, domain relationships',
            'prerequisites': '["IP Address Research and Analysis"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Threat Hunter',
            'notes': 'SEC497 S4 - WHOIS and DNS'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Email Header Analysis',
            'module': 'SEC497 Section 4',
            'topics': 'Email headers, SPF/DKIM/DMARC, email routing, spoofing detection, email forensics',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: DFIR Specialist',
            'notes': 'SEC497 S4 - Email headers'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Subdomain Discovery with Amass',
            'module': 'SEC497 Section 4',
            'topics': 'Subdomain enumeration, Amass tool, DNS reconnaissance, Eyewitness, screenshot automation',
            'prerequisites': '["WHOIS and DNS Investigation"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Pentester',
            'notes': 'SEC497 S4 - Subdomain discovery'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Technology-Focused Search: Censys and Shodan',
            'module': 'SEC497 Section 4',
            'topics': 'Censys, Shodan, internet-wide scanning, exposed services, device discovery, banner grabbing',
            'prerequisites': '["IP Address Research and Analysis"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Threat Hunter',
            'notes': 'SEC497 S4 - Censys and Shodan'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Cloud Storage Bucket Discovery',
            'module': 'SEC497 Section 4',
            'topics': 'S3 buckets, Azure blobs, GCP storage, exposed cloud storage, bucket enumeration, data leakage',
            'prerequisites': '["Technology-Focused Search: Censys and Shodan"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Cloud Security',
            'notes': 'SEC497 S4 - Buckets of fun'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Cyber Threat Intelligence with OSINT',
            'module': 'SEC497 Section 4',
            'topics': 'CTI collection, threat actor research, IOC discovery, malware analysis via OSINT, threat hunting',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Threat Hunter',
            'notes': 'SEC497 S4 - CTI'
        },

        # Section 5: Automation, Dark Web, Large Data (6 lessons)
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Business and Corporate OSINT',
            'module': 'SEC497 Section 5',
            'topics': 'Company research, corporate filings, business records, organizational structure, supply chain OSINT',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S5 - Business OSINT'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Wireless Network OSINT',
            'module': 'SEC497 Section 5',
            'topics': 'WiFi OSINT, Wigle, wireless geolocation, BSSID/SSID research, wireless mapping',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S5 - Wireless OSINT'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'AI for OSINT Automation',
            'module': 'SEC497 Section 5',
            'topics': 'AI-powered OSINT, LLM automation, intelligent analysis, AI tools, GPT for investigation',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: AI Security',
            'notes': 'SEC497 S5 - AI for OSINT'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Large Dataset Triage and Analysis',
            'module': 'SEC497 Section 5',
            'topics': 'Bulk data processing, dataset triage, data analysis tools, pattern recognition, large-scale OSINT',
            'prerequisites': '["Web Data Collection and Processing"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT',
            'notes': 'SEC497 S5 - Bulk data'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Dark Web and Tor Investigation',
            'module': 'SEC497 Section 5',
            'topics': 'Tor network, dark web investigation, onion services, PGP encryption, anonymous communication',
            'prerequisites': '["OPSEC for OSINT Investigators"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: Threat Hunter',
            'notes': 'SEC497 S5 - Dark web'
        },
        {
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Cryptocurrency OSINT',
            'module': 'SEC497 Section 5',
            'topics': 'Bitcoin tracking, blockchain analysis, crypto wallets, transaction tracing, cryptocurrency forensics',
            'prerequisites': '["The OSINT Process and Methodology"]',
            'tags': 'Course: SANS-SEC497, Career Path: OSINT, Career Path: DFIR Specialist',
            'notes': 'SEC497 S5 - Cryptocurrency'
        },
    ]
    all_lessons.extend(sec497_lessons)

    # ============================================================================
    # SEC501: Advanced Security Essentials - Enterprise Defender (multiple domains)
    # ============================================================================
    print("=" * 80)
    print("SEC501: Advanced Security Essentials - Enterprise Defender")
    print("=" * 80)

    sec501_lessons = [
        # Section 1: Defensive Network Architecture (4 lessons)
        {
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Security Standards and Audit Frameworks',
            'module': 'SEC501 Section 1',
            'topics': 'CIS benchmarks, compliance frameworks, regulatory requirements, audit processes, security baselines',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: Security Engineer, Career Path: GRC Analyst',
            'notes': 'SEC501 S1 - Standards and audit'
        },
        {
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Authentication, Authorization, and Accounting (AAA)',
            'module': 'SEC501 Section 1',
            'topics': 'AAA principles, RADIUS, TACACS+, authentication mechanisms, authorization models, accounting/auditing',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: Security Engineer, Career Path: Blue Teamer',
            'notes': 'SEC501 S1 - AAA fundamentals'
        },
        {
            'domain': 'system',
            'difficulty': 2,
            'title': 'Defending Network Infrastructure Devices',
            'module': 'SEC501 Section 1',
            'topics': 'Router security, switch hardening, network device security, redundancy protocol security, infrastructure defense',
            'prerequisites': '["Authentication, Authorization, and Accounting (AAA)"]',
            'tags': 'Course: SANS-SEC501, Career Path: Security Engineer, Career Path: Blue Teamer',
            'notes': 'SEC501 S1 - Network device security'
        },
        {
            'domain': 'system',
            'difficulty': 2,
            'title': 'Securing Network Redundancy Protocols',
            'module': 'SEC501 Section 1',
            'topics': 'HSRP, VRRP, STP security, redundancy protocol attacks, protocol hardening, high availability security',
            'prerequisites': '["Defending Network Infrastructure Devices"]',
            'tags': 'Course: SANS-SEC501, Career Path: Security Engineer',
            'notes': 'SEC501 S1 - Redundancy security'
        },

        # Section 2: Penetration Testing (5 lessons)
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Penetration Testing Scoping and ROE',
            'module': 'SEC501 Section 2',
            'topics': 'Scope definition, rules of engagement, legal considerations, testing boundaries, authorization, contracts',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: Pentester, Career Path: Security Engineer',
            'notes': 'SEC501 S2 - Pentest scoping'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'OSINT for Penetration Testing',
            'module': 'SEC501 Section 2',
            'topics': 'Reconnaissance, passive information gathering, target enumeration, OSINT tools, intelligence collection',
            'prerequisites': '["Penetration Testing Scoping and ROE"]',
            'tags': 'Course: SANS-SEC501, Career Path: Pentester, Career Path: OSINT',
            'notes': 'SEC501 S2 - Pentest OSINT'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Network Scanning Fundamentals (Nmap)',
            'module': 'SEC501 Section 2',
            'topics': 'Nmap, port scanning, service enumeration, OS fingerprinting, scan techniques, evasion',
            'prerequisites': '["OSINT for Penetration Testing"]',
            'tags': 'Course: SANS-SEC501, Career Path: Pentester, Career Path: Security Engineer',
            'notes': 'SEC501 S2 - Network scanning'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Vulnerability Scanning with Nessus',
            'module': 'SEC501 Section 2',
            'topics': 'Nessus scanner, vulnerability assessment, scan configuration, result analysis, remediation planning',
            'prerequisites': '["Network Scanning Fundamentals (Nmap)"]',
            'tags': 'Course: SANS-SEC501, Career Path: Pentester, Career Path: Security Engineer',
            'notes': 'SEC501 S2 - Vulnerability scanning'
        },
        {
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Exploitation and Metasploit Basics',
            'module': 'SEC501 Section 2',
            'topics': 'Metasploit framework, exploitation techniques, payloads, post-exploitation, msfconsole, MSFvenom',
            'prerequisites': '["Vulnerability Scanning with Nessus"]',
            'tags': 'Course: SANS-SEC501, Career Path: Pentester, Career Path: Red Teamer',
            'notes': 'SEC501 S2 - Metasploit basics'
        },

        # Section 3: Security Operations (4 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Network Security Monitoring Fundamentals',
            'module': 'SEC501 Section 3',
            'topics': 'NSM principles, monitoring strategies, detection methodologies, network telemetry, visibility',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: Blue Teamer, Career Path: SOC Analyst',
            'notes': 'SEC501 S3 - NSM fundamentals'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Advanced Packet Analysis with tcpdump',
            'module': 'SEC501 Section 3',
            'topics': 'tcpdump, BPF filters, packet capture, PCAP analysis, command-line analysis, capture optimization',
            'prerequisites': '["Network Security Monitoring Fundamentals"]',
            'tags': 'Course: SANS-SEC501, Career Path: DFIR Specialist, Career Path: Blue Teamer',
            'notes': 'SEC501 S3 - tcpdump analysis'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Attack Analysis with Wireshark',
            'module': 'SEC501 Section 3',
            'topics': 'Wireshark advanced features, attack pattern recognition, protocol dissection, traffic reconstruction',
            'prerequisites': '["Advanced Packet Analysis with tcpdump"]',
            'tags': 'Course: SANS-SEC501, Career Path: DFIR Specialist, Career Path: SOC Analyst',
            'notes': 'SEC501 S3 - Wireshark attack analysis'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Snort IDS/IPS Fundamentals',
            'module': 'SEC501 Section 3',
            'topics': 'Snort architecture, rule writing, signature-based detection, IDS/IPS configuration, alert analysis',
            'prerequisites': '["Network Security Monitoring Fundamentals"]',
            'tags': 'Course: SANS-SEC501, Career Path: Blue Teamer, Career Path: SOC Analyst',
            'notes': 'SEC501 S3 - Snort basics'
        },

        # Section 4: DFIR (4 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Active Defense and Honeypots',
            'module': 'SEC501 Section 4',
            'topics': 'Active defense strategies, honeypots, deception technology, attacker engagement, early warning systems',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: Blue Teamer, Career Path: Threat Hunter',
            'notes': 'SEC501 S4 - Active defense'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Digital Forensics Core Concepts',
            'module': 'SEC501 Section 4',
            'topics': 'DFIR fundamentals, forensic methodology, evidence handling, chain of custody, forensic principles',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: DFIR Specialist, Career Path: Blue Teamer',
            'notes': 'SEC501 S4 - DFIR core concepts'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Data Recovery with FTK Imager and Photorec',
            'module': 'SEC501 Section 4',
            'topics': 'Data recovery, FTK Imager, Photorec, deleted file recovery, file carving, forensic imaging',
            'prerequisites': '["Digital Forensics Core Concepts"]',
            'tags': 'Course: SANS-SEC501, Career Path: DFIR Specialist',
            'notes': 'SEC501 S4 - Data recovery'
        },
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Discovering Forensic Artifacts',
            'module': 'SEC501 Section 4',
            'topics': 'Artifact analysis, registry forensics, log analysis, browser artifacts, persistence mechanisms',
            'prerequisites': '["Digital Forensics Core Concepts"]',
            'tags': 'Course: SANS-SEC501, Career Path: DFIR Specialist',
            'notes': 'SEC501 S4 - Artifact discovery'
        },

        # Section 5: Malware Analysis (3 lessons)
        {
            'domain': 'malware',
            'difficulty': 2,
            'title': 'Introduction to Malware Analysis',
            'module': 'SEC501 Section 5',
            'topics': 'Malware types, analysis methodology, analysis phases, malware behavior, analysis environment setup',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: Malware Analyst, Career Path: DFIR Specialist',
            'notes': 'SEC501 S5 - Malware intro'
        },
        {
            'domain': 'malware',
            'difficulty': 2,
            'title': 'Static Properties Analysis of Ransomware',
            'module': 'SEC501 Section 5',
            'topics': 'Static analysis, file properties, strings analysis, PE structure, indicators, ransomware characteristics',
            'prerequisites': '["Introduction to Malware Analysis"]',
            'tags': 'Course: SANS-SEC501, Career Path: Malware Analyst',
            'notes': 'SEC501 S5 - Static analysis'
        },
        {
            'domain': 'malware',
            'difficulty': 2,
            'title': 'Interactive Behavior Analysis of Ransomware',
            'module': 'SEC501 Section 5',
            'topics': 'Behavioral analysis, sandboxing, dynamic analysis, process monitoring, network activity, file system changes',
            'prerequisites': '["Static Properties Analysis of Ransomware"]',
            'tags': 'Course: SANS-SEC501, Career Path: Malware Analyst',
            'notes': 'SEC501 S5 - Behavioral analysis'
        },

        # Additional lessons
        {
            'domain': 'dfir',
            'difficulty': 2,
            'title': 'Incident Response Scaling and Scoping',
            'module': 'SEC501 Section 4',
            'topics': 'IR scope definition, scaling response, resource allocation, prioritization, enterprise IR',
            'prerequisites': '["Digital Forensics Core Concepts"]',
            'tags': 'Course: SANS-SEC501, Career Path: DFIR Specialist, Career Path: Blue Teamer',
            'notes': 'SEC501 S4 - IR scoping'
        },
        {
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Attacker Tactics and Risk Reduction',
            'module': 'SEC501 All Sections',
            'topics': 'Attacker TTPs, MITRE ATT&CK, threat modeling, risk assessment, defense strategies, security controls',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC501, Career Path: Security Engineer, Career Path: Threat Hunter',
            'notes': 'SEC501 - Attacker tactics'
        },
    ]
    all_lessons.extend(sec501_lessons)

    # ============================================================================
    # SEC502: Cloud Security Tactical Defense (cloud domain)
    # ============================================================================
    print("=" * 80)
    print("SEC502: Cloud Security Tactical Defense")
    print("=" * 80)

    sec502_lessons = [
        # Section 1: IAM (5 lessons)
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Identity and Access Management Fundamentals',
            'module': 'SEC502 Section 1',
            'topics': 'Cloud IAM, identity types, access control, IAM best practices, Zero Trust, least privilege',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: Security Engineer',
            'notes': 'SEC502 S1 - IAM fundamentals'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Account Separation and Workload Isolation',
            'module': 'SEC502 Section 1',
            'topics': 'Account structure, workload separation, multi-account strategy, organizational units, guardrails',
            'prerequisites': '["Cloud Identity and Access Management Fundamentals"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S1 - Account separation'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Least Privilege and IAM Policy Design',
            'module': 'SEC502 Section 1',
            'topics': 'Least privilege implementation, IAM policies, permission boundaries, policy evaluation, access advisor',
            'prerequisites': '["Cloud Identity and Access Management Fundamentals"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S1 - Least privilege'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Application Credentials and Secret Management',
            'module': 'SEC502 Section 1',
            'topics': 'Temporary credentials, secrets management, credential rotation, service accounts, managed identities',
            'prerequisites': '["Cloud Identity and Access Management Fundamentals"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: Security Engineer',
            'notes': 'SEC502 S1 - Secrets management'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Metadata Services Security',
            'module': 'SEC502 Section 1',
            'topics': 'Instance metadata, IMDS attacks, metadata service hardening, IMDSv2, credential theft prevention',
            'prerequisites': '["Cloud Application Credentials and Secret Management"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S1 - Metadata security'
        },

        # Section 2: Compute and Configuration (5 lessons)
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Shared Responsibility Model',
            'module': 'SEC502 Section 2',
            'topics': 'Shared responsibility, IaaS/PaaS/SaaS security, CSP vs customer responsibilities, security boundaries',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: Security Engineer',
            'notes': 'SEC502 S2 - Shared responsibility'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Secure Cloud VM and Host Configuration',
            'module': 'SEC502 Section 2',
            'topics': 'VM security, hardening, image management, secure deployment, configuration baselines, host security',
            'prerequisites': '["Cloud Shared Responsibility Model"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S2 - VM security'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Application Security and Threat Modeling',
            'module': 'SEC502 Section 2',
            'topics': 'Application security, threat modeling, STRIDE, secure architecture, cloud-native apps, AppSec',
            'prerequisites': '["Cloud Shared Responsibility Model"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: Security Engineer',
            'notes': 'SEC502 S2 - App security'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Container Security and Deployment',
            'module': 'SEC502 Section 2',
            'topics': 'Container security, Docker, Kubernetes, image scanning, runtime security, container best practices',
            'prerequisites': '["Secure Cloud VM and Host Configuration"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S2 - Container security'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Infrastructure as Code (IaC) Security Analysis',
            'module': 'SEC502 Section 2',
            'topics': 'IaC security, Terraform, CloudFormation, IaC scanning, misconfigurations, policy as code',
            'prerequisites': '["Cloud Shared Responsibility Model"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: Security Engineer',
            'notes': 'SEC502 S2 - IaC security'
        },

        # Section 3: Data Protection (5 lessons)
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Data Protection and Legal Requirements',
            'module': 'SEC502 Section 3',
            'topics': 'Data protection, GDPR, data residency, legal requirements, compliance, data sovereignty',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: GRC Analyst',
            'notes': 'SEC502 S3 - Data protection legal'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Securing Cloud Storage (S3, Azure Blob, GCS)',
            'module': 'SEC502 Section 3',
            'topics': 'Cloud storage security, S3 buckets, public exposure prevention, bucket policies, encryption, access controls',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S3 - Storage security'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Sensitive Data Discovery',
            'module': 'SEC502 Section 3',
            'topics': 'Data discovery, sensitive data identification, DLP, data classification, scanning tools',
            'prerequisites': '["Securing Cloud Storage (S3, Azure Blob, GCS)"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S3 - Data discovery'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Data Encryption (At Rest and In Transit)',
            'module': 'SEC502 Section 3',
            'topics': 'Encryption at rest, encryption in transit, KMS, key management, TLS, certificate management',
            'prerequisites': '["Securing Cloud Storage (S3, Azure Blob, GCS)"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S3 - Encryption'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Data Lifecycle Management',
            'module': 'SEC502 Section 3',
            'topics': 'Data lifecycle, retention policies, data deletion, backups, disaster recovery, resilience',
            'prerequisites': '["Securing Cloud Storage (S3, Azure Blob, GCS)"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S3 - Data lifecycle'
        },

        # Section 4: Networking and Detection (5 lessons)
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Networking vs On-Premises',
            'module': 'SEC502 Section 4',
            'topics': 'Cloud networking, VPC, subnets, security groups, NACLs, network architecture, differences from on-prem',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: Security Engineer',
            'notes': 'SEC502 S4 - Cloud networking'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Securing Remote Cloud Management',
            'module': 'SEC502 Section 4',
            'topics': 'Remote management security, bastion hosts, jump servers, SSM, SSH hardening, access control',
            'prerequisites': '["Cloud Networking vs On-Premises"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S4 - Remote management'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Network Segmentation',
            'module': 'SEC502 Section 4',
            'topics': 'Network segmentation, micro-segmentation, isolation, security zones, network architecture, defense in depth',
            'prerequisites': '["Cloud Networking vs On-Premises"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S4 - Segmentation'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Web Application Firewalls (WAF)',
            'module': 'SEC502 Section 4',
            'topics': 'WAF deployment, rule configuration, OWASP Top 10 protection, managed rules, custom rules, WAF tuning',
            'prerequisites': '["Cloud Networking vs On-Premises"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S4 - WAF'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Logging and Threat Detection',
            'module': 'SEC502 Section 4',
            'topics': 'CloudTrail, flow logs, cloud-native detection, GuardDuty, Security Hub, log aggregation, SIEM integration',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: SOC Analyst',
            'notes': 'SEC502 S4 - Logging and detection'
        },

        # Section 5: Compliance, IR, Pentesting (6 lessons)
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Asset Inventory and Risk Management',
            'module': 'SEC502 Section 5',
            'topics': 'Asset inventory, tagging, CMDB, resource discovery, risk assessment, cloud governance',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: GRC Analyst',
            'notes': 'SEC502 S5 - Asset management'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'AI and Serverless for Cloud Defense',
            'module': 'SEC502 Section 5',
            'topics': 'Serverless security, Lambda/Functions, AI-powered defense, automated remediation, event-driven security',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: AI Security',
            'notes': 'SEC502 S5 - AI and serverless'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Security Posture Management (CSPM)',
            'module': 'SEC502 Section 5',
            'topics': 'CSPM tools, CASB, CWPP, misconfiguration detection, compliance monitoring, Cloud Custodian',
            'prerequisites': '["Cloud Asset Inventory and Risk Management"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S5 - CSPM'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Cloud Vulnerability Assessment',
            'module': 'SEC502 Section 5',
            'topics': 'Cloud-native vulnerability scanning, Inspector, Qualys, Tenable, vulnerability management, patching',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security',
            'notes': 'SEC502 S5 - Vulnerability assessment'
        },
        {
            'domain': 'cloud',
            'difficulty': 3,
            'title': 'Cloud Penetration Testing',
            'module': 'SEC502 Section 5',
            'topics': 'Cloud pentest methodology, rules of engagement, cloud-specific attacks, testing limitations, tooling',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: Pentester',
            'notes': 'SEC502 S5 - Cloud pentesting'
        },
        {
            'domain': 'cloud',
            'difficulty': 3,
            'title': 'Cloud Incident Detection and Containment',
            'module': 'SEC502 Section 5',
            'topics': 'Cloud IR, tripwires, early detection, breach containment, forensics in cloud, incident response',
            'prerequisites': '["Cloud Logging and Threat Detection"]',
            'tags': 'Course: SANS-SEC502, Career Path: Cloud Security, Career Path: DFIR Specialist',
            'notes': 'SEC502 S5 - Cloud IR'
        },
    ]
    all_lessons.extend(sec502_lessons)

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
        'SEC411': 0,
        'SEC450': 0,
        'SEC467': 0,
        'SEC497': 0,
        'SEC501': 0,
        'SEC502': 0
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
    print(f"SUCCESS - Added {added_count} lessons from 6 SANS courses")
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
    add_all_sans_courses()
