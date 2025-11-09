#!/usr/bin/env python3
"""
Add SANS LDR553: Cyber Incident Management lessons to lesson_ideas.csv

Course Focus: Leadership and coordination of major cyber incidents
Sections:
- Section 1: Understanding the Incident, Building the Team With GenAI, Scoping & Tracking
- Section 2: Communications, Planning and Executing Remediations
- Section 3: Training, Leveraging CTI, Bug Bounties
- Section 4: Cloud Incidents, BEC, Credential Theft, Metrics
- Section 5: AI for Incidents, Attacker Extortion, Ransomware, Capstone

Domain Distribution: Primarily blue_team (IM leadership), with some dfir, fundamentals
Difficulty: Mix of intermediate (core IM skills) and advanced (complex scenarios)
"""

import csv
from pathlib import Path

def add_ldr553_lessons():
    csv_path = Path("lesson_ideas.csv")

    # Read existing lessons
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Get next lesson number
    last_lesson_num = max(int(row['lesson_number']) for row in rows)
    next_lesson_num = last_lesson_num + 1

    print(f"Starting from lesson_number: {next_lesson_num}")

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

    # Define LDR553 lessons
    ldr553_lessons = [
        # Section 1: Understanding the Incident, Building the Team With GenAI (8 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Cyber Incident Management Fundamentals',
            'module': 'LDR553 Section 1',
            'topics': 'Initial information gathering, common language, defining objectives, incident categorization, IR frameworks, NIST, OODA loops',
            'prerequisites': '[]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S1 - Foundation of incident management'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Cyber Incident Management Tool Kit (CIMTK): The Grid',
            'module': 'LDR553 Section 1',
            'topics': 'CIMTK framework, The Grid questions, AIM-RADAR tracking, task identification, concurrent activities, incident tracking',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S1 - Core IM tool for task tracking'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Setting Objectives and Commander\'s Intent in Incident Management',
            'module': 'LDR553 Section 1',
            'topics': 'Defining objectives, Commander\'s Intent, focus retention, team briefing, short/medium-term goals, information overload combat',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S1 - Leadership communication technique'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Building Incident Management Teams',
            'module': 'LDR553 Section 1',
            'topics': 'Team composition, skills needed, team size, location, roles (IR, IT, HR, Legal), unique contributions, team assessment',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S1 - Team building and composition'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Leveraging GenAI for Incident Management',
            'module': 'LDR553 Section 1',
            'topics': 'GenAI team support, ChatGPT for IM, building custom GPTs, OpenAI integration, GenAI augmentation, prompt engineering',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: AI Security',
            'notes': 'LDR553 S1 - GenAI as team member'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Incident Management Platforms and Safe Operations',
            'module': 'LDR553 Section 1',
            'topics': 'IM platform requirements, safe operations, attacker access prevention, evidence management, task tracking, work tracking',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S1 - Platform selection and security'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Mapping Attacks to Business Impacts',
            'module': 'LDR553 Section 1',
            'topics': 'Business impact analysis, attack mapping, stakeholder communication, damage assessment, priority determination',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S1 - Business impact assessment'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Building Communications Plans for Incidents',
            'module': 'LDR553 Section 1',
            'topics': 'Communications planning, exec comms, team comms, third-party comms, battle rhythm, team welfare, stress management',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S1 - Communications strategy'
        },

        # Section 2: Communications, Planning and Executing Remediations (9 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Crisis Communications: Briefing Executives',
            'module': 'LDR553 Section 2',
            'topics': 'Executive briefing structure, Three What\'s approach, modality, frequency, incident scope, objectives, forward plans',
            'prerequisites': '["Building Communications Plans for Incidents"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S2 - Executive communication'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Crisis Communications: Engaging with Threat Actors',
            'module': 'LDR553 Section 2',
            'topics': 'Attacker engagement, dialogue strategies, buying time, preventing data leaks, communication medium, proxies, trusted third parties, attacker reputation',
            'prerequisites': '["Building Communications Plans for Incidents"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S2 - Attacker communications (controversial)'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Crisis Communications: Public Statements and Media',
            'module': 'LDR553 Section 2',
            'topics': 'Public statement drafting, media handling, narrative control, customer communications, disclosure timing, reputation management',
            'prerequisites': '["Building Communications Plans for Incidents"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S2 - Public/media communications'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Network and Data Remediation Planning',
            'module': 'LDR553 Section 2',
            'topics': 'Categorizing damage, system remediation, data remediation, remediation tracking, Counter Compromise activities, exposed assets',
            'prerequisites': '["Cyber Incident Management Tool Kit (CIMTK): The Grid"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S2 - Remediation strategy'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Managing Secrets in Compromised Systems',
            'module': 'LDR553 Section 2',
            'topics': 'Secret exposure, stolen data secrets, compromised system secrets, future operation implications, secret rotation, credential management',
            'prerequisites': '["Network and Data Remediation Planning"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S2 - Often-overlooked remediation aspect'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Incident Management Reporting and Documentation',
            'module': 'LDR553 Section 2',
            'topics': 'IM report outputs, IR report adaptation, report types, graphics, stakeholder input, consensus building, report control and access',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S2 - Documentation and reporting'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Root Cause Analysis (RCA) Methods',
            'module': 'LDR553 Section 2',
            'topics': 'RCA planning (PALPATE), Five Whys method, RCA meeting facilitation, lessons learned, reflection sessions, avoiding flawed RCA',
            'prerequisites': '["Incident Management Reporting and Documentation"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S2 - Post-incident analysis'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Incident Closure and Transition to BAU',
            'module': 'LDR553 Section 2',
            'topics': 'Incident closure planning, Business-as-Usual (BAU) transition, project handoff, IM team dissolution, ongoing initiatives',
            'prerequisites': '["Incident Management Reporting and Documentation"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S2 - Closing incidents properly'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'GenAI for Brief Generation and Text Parsing',
            'module': 'LDR553 Section 2',
            'topics': 'Automated brief generation, text formatting, unstructured text parsing, communication validation, cross-checking outputs, GenAI limitations',
            'prerequisites': '["Leveraging GenAI for Incident Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: AI Security',
            'notes': 'LDR553 S2 - GenAI applications in comms'
        },

        # Section 3: Training, Leveraging CTI, Bug Bounties (10 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Training the Organization for Cyber Incidents',
            'module': 'LDR553 Section 3',
            'topics': 'Enterprise-wide training, organizational maturity, training needs analysis, non-IR personnel onboarding, training program development',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S3 - Organization-wide preparation'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Developing SOC/IR/IM Teams Through Training',
            'module': 'LDR553 Section 3',
            'topics': 'Team development, long-term training strategies, tactical exercises, addressing gaps, practical experience, beyond compliance training',
            'prerequisites': '["Building Incident Management Teams"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: SOC Analyst',
            'notes': 'LDR553 S3 - Team capability building'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Cyber Incident Exercises and Table-Tops',
            'module': 'LDR553 Section 3',
            'topics': 'Exercise types, maturity levels, exercise planning, hotseat exercises, external group inclusion, non-IM specialist exercises',
            'prerequisites': '["Training the Organization for Cyber Incidents"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S3 - Practical exercise design'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Integrating Cyber Threat Intelligence into Incident Management',
            'module': 'LDR553 Section 3',
            'topics': 'CTI integration, strategic/operational/tactical products, CTI for IM, CTI availability during incidents, CTI requirements development',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Threat Hunter',
            'notes': 'LDR553 S3 - Leveraging CTI effectively'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Request For Intelligence (RFI) and PIR Development',
            'module': 'LDR553 Section 3',
            'topics': 'RFI generation, Priority Intelligence Requirements (PIR), avoiding common mistakes, intelligence feedback loops, optimizing CTI team',
            'prerequisites': '["Integrating Cyber Threat Intelligence into Incident Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Threat Hunter',
            'notes': 'LDR553 S3 - Intelligence requests'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Third-Party Supply Chain Compromise Management',
            'module': 'LDR553 Section 3',
            'topics': 'Supply chain attacks, notification routes, exposure analysis, data void planning, third-party RFI, third-party meeting planning',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S3 - Complex third-party incidents'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Managing Limitations in Third-Party Incidents',
            'module': 'LDR553 Section 3',
            'topics': 'Third-party incident limitations, scope assessment, impact analysis, investigative actions, closing third-party incidents',
            'prerequisites': '["Third-Party Supply Chain Compromise Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S3 - Working with constraints'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'GenAI for Idea Validation and Information Parsing',
            'module': 'LDR553 Section 3',
            'topics': 'Validating IC ideas, external information parsing, simplifying complex info, unburdening leaders, bespoke GPT creation',
            'prerequisites': '["Leveraging GenAI for Incident Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: AI Security',
            'notes': 'LDR553 S3 - GenAI as decision support'
        },
        {
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Cyber Incident Exercise Design and Facilitation',
            'module': 'LDR553 Section 3',
            'topics': 'Exercise design, facilitation techniques, participant engagement, scenario development, learning objectives, post-exercise debrief',
            'prerequisites': '["Cyber Incident Exercises and Table-Tops"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S3 - Running effective exercises'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Submarine Studios Case Study: Third-Party Compromise',
            'module': 'LDR553 Section 3',
            'topics': 'Case study analysis, scope understanding, impact assessment, immediate remediation, required information unavailability',
            'prerequisites': '["Third-Party Supply Chain Compromise Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S3 - Hands-on third-party scenario'
        },

        # Section 4: Cloud Incidents, BEC, Credential Theft, Metrics (11 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Incident Timelines for Visualization',
            'module': 'LDR553 Section 4',
            'topics': 'Timeline scoping, audience consideration, detail levels, timeline styles, comprehensive view visualization, case studies',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'LDR553 S4 - Timeline creation'
        },
        {
            'domain': 'cloud',
            'difficulty': 2,
            'title': 'Defining and Scoping Cloud Attacks',
            'module': 'LDR553 Section 4',
            'topics': 'Cloud attack definition, shared responsibility models, MITRE for Cloud, attack focuses, cloud vs on-prem differences',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Cloud Security',
            'notes': 'LDR553 S4 - Cloud incident fundamentals'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Credential Theft Attack Management',
            'module': 'LDR553 Section 4',
            'topics': 'Credential theft vectors, attacker objectives, MITRE framework, Initial Access Brokers, underground marketplaces, MFA fatigue, illicit consent',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S4 - Credential attack management'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'CIMTK: Credential Loss Immediate Actions (CLIA)',
            'module': 'LDR553 Section 4',
            'topics': 'Immediate credential loss response, CLIA framework, credential harvesting, password manager attacks, malicious browser extensions, BYOD vectors',
            'prerequisites': '["Credential Theft Attack Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S4 - Rapid credential response'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Business Email Compromise (BEC) Incident Management',
            'module': 'LDR553 Section 4',
            'topics': 'BEC stages, 6+ BEC types, attacker position, impacted parties, legal support, liability determination, MITRE O365 reference',
            'prerequisites': '["Credential Theft Attack Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'LDR553 S4 - Complex BEC management'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'BEC Investigation and Forensics Direction',
            'module': 'LDR553 Section 4',
            'topics': 'Inbox investigations, multi-site/multi-vendor compromises, BECIA framework, supporting legal arguments, directing IR for forensics',
            'prerequisites': '["Business Email Compromise (BEC) Incident Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'LDR553 S4 - BEC investigation leadership'
        },
        {
            'domain': 'cloud',
            'difficulty': 3,
            'title': 'Cloud IaaS Host Compromise Management',
            'module': 'LDR553 Section 4',
            'topics': 'IaaS compromise vectors, impact assessment, investigation requirements, forensics on cloud VMs, policy holes, network gaps',
            'prerequisites': '["Defining and Scoping Cloud Attacks"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Cloud Security',
            'notes': 'LDR553 S4 - Cloud asset incidents'
        },
        {
            'domain': 'cloud',
            'difficulty': 3,
            'title': 'Cloud Management Console Attack Response',
            'module': 'LDR553 Section 4',
            'topics': 'Management console compromise, attacker goals, policy checks, leveraging auditors, console access vectors, cloud-focused RCA',
            'prerequisites': '["Defining and Scoping Cloud Attacks"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Cloud Security',
            'notes': 'LDR553 S4 - Management console incidents'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Incident Management Metrics and KPIs',
            'module': 'LDR553 Section 4',
            'topics': 'Metrics vs KPIs, message behind metrics, what metrics show/hide, people vs tools, improving IR/IM',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S4 - Measuring IM effectiveness'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Policies, Playbooks and Runbooks for IM',
            'module': 'LDR553 Section 4',
            'topics': 'Policy development, playbook creation, runbook maintenance, leveraging outside groups, disaster recovery integration, relationship management',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S4 - Documentation and processes'
        },
        {
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Integrating Incident Management with Disaster Recovery',
            'module': 'LDR553 Section 4',
            'topics': 'DR integration, cross-team collaboration, DR processes, DR exercises, smoother operations, relationship approaches',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S4 - IM and DR alignment'
        },

        # Section 5: AI for Incidents, Ransomware, Capstone (10 lessons)
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Understanding AI Categories for Incident Management',
            'module': 'LDR553 Section 5',
            'topics': 'AI definition, NLP, neural networks, GenAI, machine learning, robotics, LLMs, ChatGPT, AI applications in IM',
            'prerequisites': '["Leveraging GenAI for Incident Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: AI Security',
            'notes': 'LDR553 S5 - AI fundamentals for IM'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'AI Risks and Hallucinations in Incident Management',
            'module': 'LDR553 Section 5',
            'topics': 'AI risks, hallucination problem, minimizing hallucination impact, responsible AI use, when/where/how to apply AI',
            'prerequisites': '["Understanding AI Categories for Incident Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: AI Security',
            'notes': 'LDR553 S5 - AI limitations and risks'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Investigating Compromised AI Chatbots',
            'module': 'LDR553 Section 5',
            'topics': 'Chatbot compromise investigation, behavior assessment, indicators of compromise, vulnerability identification, LLM security',
            'prerequisites': '["Understanding AI Categories for Incident Management"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: AI Security',
            'notes': 'LDR553 S5 - Hands-on compromised chatbot analysis'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Ransomware: History and Evolution',
            'module': 'LDR553 Section 5',
            'topics': 'Ransomware history, early attacks, modern operations, ransomware stages, evolution of tactics, "how the dirty get dirtier"',
            'prerequisites': '["Cyber Incident Management Fundamentals"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'LDR553 S5 - Ransomware background'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Ransomware Detection and Alert Analysis',
            'module': 'LDR553 Section 5',
            'topics': 'Ransomware alerts, attack stage mapping, instant checks, automation opportunities, early warning, adversary preparation phase detection',
            'prerequisites': '["Ransomware: History and Evolution"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: SOC Analyst',
            'notes': 'LDR553 S5 - Detecting ransomware early'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Ransomware Incident Management and Executive Decision Support',
            'module': 'LDR553 Section 5',
            'topics': 'Key questions, executive needs, no-regret options, "going dark" implications, clear communication, decision documentation',
            'prerequisites': '["Ransomware: History and Evolution"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S5 - Leading ransomware response'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'CIMTK: Ransomware Initial Actions (RIA)',
            'module': 'LDR553 Section 5',
            'topics': 'Ransomware immediate actions, RIA framework, planning to meet threat, exercising for ransomware, DR options, impact documentation',
            'prerequisites': '["Ransomware Incident Management and Executive Decision Support"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S5 - Rapid ransomware response'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Ransomware Negotiation and Attacker Engagement',
            'module': 'LDR553 Section 5',
            'topics': 'Ransom negotiation planning, negotiation execution, attacker engagement, payment considerations, buying time, parallel investigation',
            'prerequisites': '["Ransomware Incident Management and Executive Decision Support"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S5 - Negotiation strategy (controversial)'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Ransomware Recovery and Network Rebuilding',
            'module': 'LDR553 Section 5',
            'topics': 'Network rebuilding, preventing repeat compromise, technical requirements, procedural requirements, records and evidence, decision documentation',
            'prerequisites': '["Ransomware Incident Management and Executive Decision Support"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'LDR553 S5 - Recovery and rebuilding'
        },
        {
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'LDR553 Capstone: Multi-Stage Time-Sensitive Incident',
            'module': 'LDR553 Section 5',
            'topics': 'Capstone exercise, report analysis, policy/procedure review, plan creation, leadership briefing, end-of-day summary',
            'prerequisites': '["Ransomware Incident Management and Executive Decision Support", "Business Email Compromise (BEC) Incident Management", "Cloud Management Console Attack Response"]',
            'tags': 'Course: SANS-LDR553, Career Path: Blue Teamer',
            'notes': 'LDR553 S5 - Final comprehensive exercise'
        },
    ]

    print(f"Adding {len(ldr553_lessons)} SANS LDR553 lessons...\n")

    # Add new lessons
    added_count = 0
    domain_counts = {}
    difficulty_counts = {1: 0, 2: 0, 3: 0}

    for lesson in ldr553_lessons:
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

    print(f"\n[SUCCESS] Added {added_count} SANS LDR553 lessons")
    print(f"Total lessons in CSV: {len(rows)}")
    print(f"\nSANS LDR553 Course Coverage:")
    print(f"  Section 1: 8 lessons - Understanding, Building Team, GenAI")
    print(f"  Section 2: 9 lessons - Communications, Remediations")
    print(f"  Section 3: 10 lessons - Training, CTI, Third-Party")
    print(f"  Section 4: 11 lessons - Cloud, BEC, Credentials, Metrics")
    print(f"  Section 5: 10 lessons - AI, Ransomware, Capstone")
    print(f"\nDifficulty Distribution:")
    print(f"  Beginner: {difficulty_counts[1]}")
    print(f"  Intermediate: {difficulty_counts[2]}")
    print(f"  Advanced: {difficulty_counts[3]}")
    print(f"\nDomains Covered:")
    for domain in sorted(domain_counts.keys()):
        print(f"  {domain}: {domain_counts[domain]} lessons")

if __name__ == '__main__':
    add_ldr553_lessons()
