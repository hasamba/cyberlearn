#!/usr/bin/env python3
"""
Add SANS FOR577 (Linux Incident Response and Threat Hunting) lessons to lesson_ideas.csv
Based on the official course syllabus
"""

import csv

# SANS FOR577 course lessons - organized by sections
for577_lessons = [
    # SECTION 1: Linux Incident Response and Analysis

    # Beginner lessons
    {
        'domain': 'dfir',
        'difficulty': 1,
        'title': 'Linux Incident Response Fundamentals',
        'topics': 'Why IR is needed in Linux, Current state of Linux intrusions, SANS six-step IR methodology, Linux-specific IR challenges, Building IR capabilities',
        'prerequisites': '["Digital Forensics 101: Your First Investigation"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 1 - Foundation for Linux IR'
    },
    {
        'domain': 'linux',
        'difficulty': 1,
        'title': 'Linux Command Line for DFIR',
        'topics': 'Essential Linux commands for DFIR, Command line basics, DFIR techniques with CLI, Navigating Linux filesystems, Working with files and directories',
        'prerequisites': '["Linux Security Basics for Beginners"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 1 Lab - Introduction to Linux commands in DFIR'
    },

    # Intermediate lessons
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Package Management Investigations',
        'topics': 'Package management differences across distros, Debian package analysis, Red Hat package analysis, Investigating software installations, Package-based IOCs',
        'prerequisites': '["Linux Command Line for DFIR"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 1 Lab - Reviewing package management evidence'
    },
    {
        'domain': 'threat_hunting',
        'difficulty': 2,
        'title': 'Endpoint Threat Hunting on Linux',
        'topics': 'Hunting vs reactive response, Intelligence-driven IR, Building continuous threat hunting capability, Forensic analysis across Linux endpoints, Threat hunt team roles',
        'prerequisites': '["Threat Hunting 101: What is Threat Hunting?"]',
        'tags': 'Course: SANS-FOR577, Career Path: Threat Hunter, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 1 Lab - Threat intelligence and threat hunting'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Cyber Attacks and the Unified Kill Chain',
        'topics': 'Unified Kill Chain framework, Linux-specific attack techniques, Attack patterns in Linux, Adversary tactics on Linux systems, Kill chain analysis',
        'prerequisites': '["Linux Incident Response Fundamentals"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 1 - Cyber attacks and Linux'
    },

    # SECTION 2: Disk Analysis and Evidence Collection

    # Intermediate lessons
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'The Sleuth Kit for Linux Forensics',
        'topics': 'TSK layers model, Filesystem layer tools, Filename layer tools, Metadata layer tools, Data units layer tools, Application layer tools',
        'prerequisites': '["Linux Command Line for DFIR"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 2 Lab - Introduction to the Sleuth Kit'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux File Systems Forensics',
        'topics': 'Ext2/3/4 filesystem structures, XFS filesystem analysis, Btrfs filesystem forensics, Superblocks and inodes, Manually extracting filesystem data',
        'prerequisites': '["The Sleuth Kit for Linux Forensics"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 2 Lab - Reviewing filesystem data'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Disk Evidence Collection',
        'topics': 'Physical vs virtual system imaging, dd and dcfldd commands, dc3dd and ewfacquire, Image mounting techniques, RAW and E01 format files',
        'prerequisites': '["Linux File Systems Forensics"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 2 Lab - Disk evidence collection'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Operating System File Structures',
        'topics': 'Filesystem hierarchy standard, Boot and binary locations, Configuration file locations, Devices and drivers, Shared libraries, User profiles, Temporary files',
        'prerequisites': '["Linux File Systems Forensics"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 2 - OS file structures and artifacts'
    },

    # SECTION 3: Linux Logging and Log Analysis

    # Intermediate lessons
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Device Profiling for Incident Response',
        'topics': 'Evidence management, Confirming device identity, Timezone validation, Distro identification, System profiling techniques',
        'prerequisites': '["Linux Incident Response Fundamentals"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 3 Lab - System and log profiling'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux System Logs Analysis',
        'topics': 'Linux logging basics, Syslog and logrotate, Kernel and boot logs, System message analysis, Background service logs, UTC vs local timestamps',
        'prerequisites': '["Linux Device Profiling for Incident Response"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 3 Lab - Reviewing system logs'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Authentication Log Analysis',
        'topics': 'Authentication log formats, Privilege use analysis, Binary vs plain text logs, Login event analysis, SSH authentication forensics',
        'prerequisites': '["Linux System Logs Analysis"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 3 Lab - Analyzing authentication logs'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Application Logs Forensics',
        'topics': 'Webserver log analysis (Apache, Nginx), Database log forensics, File sharing logs, Firewall log analysis, Application-specific logging',
        'prerequisites': '["Linux System Logs Analysis"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 3 Lab - Reviewing webserver and database logs'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Auditd for Security Monitoring',
        'topics': 'Auditd introduction and configuration, Log file format analysis, Audit rules creation, Analysis techniques, Incident investigation with Auditd',
        'prerequisites': '["Linux System Logs Analysis"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist, Career Path: SOC Analyst',
        'notes': 'FOR577 Section 3 Lab - AuditD logs and the Journal'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Systemd Journal Analysis',
        'topics': 'Systemd Journal introduction, How journald works, Journal log structure, What gets logged, Analysis techniques with journalctl',
        'prerequisites': '["Linux System Logs Analysis"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 3 - Operating System Journal'
    },

    # SECTION 4: Live Response and Volatile Data

    # Intermediate lessons
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Enterprise-Scale Linux Incident Response',
        'topics': 'Scaling IR for large enterprises, Enterprise IR problems and solutions, Tools for enterprise response, Coordination and communication, Response automation',
        'prerequisites': '["Linux Incident Response Fundamentals"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 4 - Enterprise response'
    },
    {
        'domain': 'blue_team',
        'difficulty': 2,
        'title': 'Linux EDR: OSSEC Deployment and Use',
        'topics': 'Linux EDR challenges, OSSEC architecture, OSSEC deployment strategies, Configuration and tuning, Alert analysis and response, OSSEC as cost-effective EDR',
        'prerequisites': '["Enterprise-Scale Linux Incident Response"]',
        'tags': 'Course: SANS-FOR577, Career Path: SOC Analyst, Career Path: Blue Team Operator',
        'notes': 'FOR577 Section 4 Lab - OSSEC deployment and use'
    },
    {
        'domain': 'blue_team',
        'difficulty': 2,
        'title': 'Linux EDR: Velociraptor Deployment and Use',
        'topics': 'Velociraptor architecture, Deployment for Linux endpoints, VQL query language, Artifact collection, Hunting with Velociraptor, Offline collectors',
        'prerequisites': '["Enterprise-Scale Linux Incident Response"]',
        'tags': 'Course: SANS-FOR577, Career Path: SOC Analyst, Career Path: Blue Team Operator, Career Path: Threat Hunter',
        'notes': 'FOR577 Section 4 Lab - Velociraptor deployment and use'
    },

    # Advanced lessons
    {
        'domain': 'dfir',
        'difficulty': 3,
        'title': 'Linux Memory Forensics and Analysis',
        'topics': 'Why memory matters in Linux, Memory acquisition with AVML, Memory structures on Linux, /proc filesystem analysis, Volatile data collection',
        'prerequisites': '["Linux Incident Response Fundamentals"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 4 Lab - Capturing RAM and live memory analysis'
    },
    {
        'domain': 'dfir',
        'difficulty': 3,
        'title': 'Linux Live Response Techniques',
        'topics': 'Live response workflow, Reviewing /proc filesystem, Process analysis on live systems, Network connection analysis, Live memory investigation techniques',
        'prerequisites': '["Linux Memory Forensics and Analysis"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 4 - Live memory analysis and response'
    },

    # SECTION 5: Advanced Incident Response Techniques

    # Intermediate lessons
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Triage and Rapid Assessment',
        'topics': 'Triage concepts and workflow, Collecting triage data, Open-source triage tools (CyLR, GRR), UAC for Linux, Building custom triage scripts',
        'prerequisites': '["Linux Incident Response Fundamentals"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 5 Lab - Running triage tools and assessment'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Velociraptor Offline Collectors for Linux',
        'topics': 'Offline collector concepts, Creating collectors, Deploying offline collectors, Analyzing collected data, Triage with offline collectors',
        'prerequisites': '["Linux EDR: Velociraptor Deployment and Use"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 5 - Velociraptor offline collectors'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Linux Filesystem Timeline Analysis',
        'topics': 'Timeline types and concepts, Filesystem timeline creation, Timeline analysis techniques, Identifying suspicious activity, Temporal analysis strategies',
        'prerequisites': '["Linux File Systems Forensics"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 5 Lab - Filesystem timelines'
    },

    # Advanced lessons
    {
        'domain': 'dfir',
        'difficulty': 3,
        'title': 'Linux Super Timeline Creation and Analysis',
        'topics': 'Super timeline concepts, Plaso and log2timeline, Creating comprehensive timelines, Super timeline analysis with Timesketch, Targeted timeline creation',
        'prerequisites': '["Linux Filesystem Timeline Analysis"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 5 Lab - Super timeline creation and analysis'
    },
    {
        'domain': 'dfir',
        'difficulty': 3,
        'title': 'Linux Anti-Forensics Detection and Mitigation',
        'topics': 'Common anti-forensic techniques on Linux, Timestamp manipulation detection, Recovering deleted files, File hiding techniques, Minimizing anti-forensic impact',
        'prerequisites': '["Linux Super Timeline Creation and Analysis"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 5 - Anti-forensics'
    },
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Improving Linux Incident Response Workflows',
        'topics': 'IR workflow optimization, Environment hardening for better forensics, Logging best practices, Tool integration, Lessons learned implementation',
        'prerequisites': '["Linux Incident Response Fundamentals"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 5 - Improving incident response'
    },

    # Additional specialized topics from FOR577
    {
        'domain': 'dfir',
        'difficulty': 2,
        'title': 'Dissect Framework for Linux Forensics',
        'topics': 'Introduction to Dissect, Dissect for Linux analysis, Automated artifact extraction, Timeline generation with Dissect, Integration with existing workflows',
        'prerequisites': '["Linux Triage and Rapid Assessment"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 5 - Dissect triage tool'
    },
    {
        'domain': 'linux',
        'difficulty': 2,
        'title': 'SIFT Workstation for Linux DFIR',
        'topics': 'SIFT Workstation introduction, Essential SIFT tools, DFIR workflow with SIFT, Tool integration, Customizing SIFT for your environment',
        'prerequisites': '["Linux Command Line for DFIR"]',
        'tags': 'Course: SANS-FOR577, Career Path: DFIR Specialist',
        'notes': 'FOR577 Section 1 Lab - SIFT Workstation orientation'
    },
]

def main():
    """Add SANS FOR577 lessons to lesson_ideas.csv"""

    # Read existing CSV
    with open('lesson_ideas.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)
        fieldnames = reader.fieldnames

    # Get max lesson_number and domain-specific order_index
    max_lesson_number = max(int(row['lesson_number']) for row in existing_rows)

    # Get max order_index per domain
    domain_max_order = {}
    for row in existing_rows:
        domain = row['domain']
        order_idx = int(row['order_index'])
        if domain not in domain_max_order or order_idx > domain_max_order[domain]:
            domain_max_order[domain] = order_idx

    print(f"Starting from lesson_number: {max_lesson_number + 1}")
    print(f"Adding {len(for577_lessons)} SANS FOR577 lessons...")
    print()

    # Add lessons
    current_lesson_number = max_lesson_number + 1

    for lesson in for577_lessons:
        domain = lesson['domain']

        # Increment order_index for this domain
        if domain not in domain_max_order:
            domain_max_order[domain] = 0
        domain_max_order[domain] += 1

        lesson_row = {
            'lesson_number': current_lesson_number,
            'order_index': domain_max_order[domain],
            'domain': domain,
            'difficulty': lesson['difficulty'],
            'title': lesson['title'],
            'module': '',
            'topics': lesson['topics'],
            'prerequisites': lesson['prerequisites'],
            'status': 'planned',
            'tags': lesson['tags'],
            'notes': lesson['notes']
        }

        existing_rows.append(lesson_row)

        diff_label = ['', 'Beginner', 'Intermediate', 'Advanced'][lesson['difficulty']]
        print(f"Added #{current_lesson_number} [{domain}:{domain_max_order[domain]}]: {lesson['title']} ({diff_label})")

        current_lesson_number += 1

    # Write updated CSV
    with open('lesson_ideas.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)

    print()
    print(f"[SUCCESS] Added {len(for577_lessons)} SANS FOR577 lessons")
    print(f"Total lessons in CSV: {len(existing_rows)}")
    print()
    print("SANS FOR577 Course Coverage:")
    print("  Section 1: 5 lessons - Linux IR and Analysis")
    print("  Section 2: 4 lessons - Disk Analysis and Evidence Collection")
    print("  Section 3: 6 lessons - Linux Logging and Log Analysis")
    print("  Section 4: 5 lessons - Live Response and Volatile Data")
    print("  Section 5: 9 lessons - Advanced IR Techniques")
    print()
    print("Difficulty Distribution:")
    beginner = sum(1 for l in for577_lessons if l['difficulty'] == 1)
    intermediate = sum(1 for l in for577_lessons if l['difficulty'] == 2)
    advanced = sum(1 for l in for577_lessons if l['difficulty'] == 3)
    print(f"  Beginner: {beginner}")
    print(f"  Intermediate: {intermediate}")
    print(f"  Advanced: {advanced}")
    print()
    print("Domains Covered:")
    domains_count = {}
    for l in for577_lessons:
        domains_count[l['domain']] = domains_count.get(l['domain'], 0) + 1
    for domain in sorted(domains_count.keys()):
        print(f"  {domain}: {domains_count[domain]} lessons")

if __name__ == '__main__':
    main()
