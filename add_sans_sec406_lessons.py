#!/usr/bin/env python3
"""
Add SANS SEC406: Linux Security for InfoSec Professionals lessons to lesson_ideas.csv

Course Focus: Fundamental Linux security knowledge and system hardening
Sections:
- Section 1: Linux Command Line
- Section 2: Shell Syntax and Account Management
- Section 3: File and User Access Control
- Section 4: Process and Log Management
- Section 5: Package, SSH, and Network Management

Domain Distribution: Primarily linux (fundamentals), with some system (hardening), blue_team (logging)
Difficulty: Mix of beginner (command line basics) and intermediate (hardening, SELinux)
"""

import csv
from pathlib import Path

def add_sec406_lessons():
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

    # Define SEC406 lessons
    sec406_lessons = [
        # Section 1: Linux Command Line (5 lessons - beginner)
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Linux Kernel, Operating System, and Distributions',
            'module': 'SEC406 Section 1',
            'topics': 'Kernel architecture, OS components, Linux distributions, distro selection, kernel vs userland',
            'prerequisites': '[]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S1 - Foundation of Linux understanding'
        },
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Linux Terminals and Manual Pages',
            'module': 'SEC406 Section 1',
            'topics': 'Terminal usage, shell basics, man pages, help systems, command documentation, navigation tips',
            'prerequisites': '["Linux Kernel, Operating System, and Distributions"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S1 - Essential command line skills'
        },
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Linux Command History and Navigation',
            'module': 'SEC406 Section 1',
            'topics': 'Command history, history expansion, directory navigation, path concepts, filesystem hierarchy',
            'prerequisites': '["Linux Terminals and Manual Pages"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S1 - Efficient shell navigation'
        },
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Linux File Management Commands',
            'module': 'SEC406 Section 1',
            'topics': 'File operations (cp, mv, rm, mkdir, rmdir), file attributes, directory management, wildcards, glob patterns',
            'prerequisites': '["Linux Command History and Navigation"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S1 - Core file operations'
        },
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Linux Visual Editors (vi/vim)',
            'module': 'SEC406 Section 1',
            'topics': 'vi/vim basics, modes (normal, insert, command), editing commands, search/replace, configuration',
            'prerequisites': '["Linux File Management Commands"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S1 - Essential text editing'
        },

        # Section 2: Shell Syntax and Account Management (7 lessons - beginner/intermediate)
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Searching the Linux Filesystem (find, locate)',
            'module': 'SEC406 Section 2',
            'topics': 'find command, locate/updatedb, search criteria, file attributes search, time-based search, complex queries',
            'prerequisites': '["Linux File Management Commands"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'SEC406 S2 - Finding files efficiently'
        },
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Grep and Text Search Techniques',
            'module': 'SEC406 Section 2',
            'topics': 'grep, egrep, fgrep, regular expressions, grep options, piping, text filtering, pattern matching',
            'prerequisites': '["Linux File Management Commands"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'SEC406 S2 - Text search mastery'
        },
        {
            'domain': 'linux',
            'difficulty': 1,
            'title': 'Linux Environment Variables and Aliases',
            'module': 'SEC406 Section 2',
            'topics': 'Environment variables, PATH, shell configuration, aliases, shell functions, .bashrc/.bash_profile',
            'prerequisites': '["Linux Terminals and Manual Pages"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S2 - Shell customization'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Redirection and Piping',
            'module': 'SEC406 Section 2',
            'topics': 'stdin/stdout/stderr, redirection operators, piping, command chaining, input/output control, process substitution',
            'prerequisites': '["Grep and Text Search Techniques"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S2 - I/O manipulation'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Account Management',
            'module': 'SEC406 Section 2',
            'topics': 'User creation (useradd, adduser), user modification, user deletion, password management (passwd), su/sudo, switching users',
            'prerequisites': '["Linux Kernel, Operating System, and Distributions"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S2 - User management'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Group Management',
            'module': 'SEC406 Section 2',
            'topics': 'Group creation (groupadd), group membership, primary/secondary groups, group modification, /etc/group',
            'prerequisites': '["Linux Account Management"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S2 - Group administration'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux File Ownership (chown, chgrp)',
            'module': 'SEC406 Section 2',
            'topics': 'File ownership concepts, chown, chgrp, ownership changes, recursive changes, security implications',
            'prerequisites': '["Linux Group Management"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S2 - Ownership management'
        },

        # Section 3: File and User Access Control (7 lessons - intermediate)
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux File Permissions (chmod)',
            'module': 'SEC406 Section 3',
            'topics': 'Permission model (rwx), chmod numeric/symbolic, permission calculation, umask, default permissions, permission strategies',
            'prerequisites': '["Linux File Ownership (chown, chgrp)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S3 - Core permission system'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Special Permissions (SUID, SGID, Sticky Bit)',
            'module': 'SEC406 Section 3',
            'topics': 'SUID/SGID concepts, sticky bit, security implications, finding special permissions, attack vectors, mitigation',
            'prerequisites': '["Linux File Permissions (chmod)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer, Career Path: Pentester',
            'notes': 'SEC406 S3 - Advanced permissions and security'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Permission Practical Security',
            'module': 'SEC406 Section 3',
            'topics': 'Permission security best practices, common misconfigurations, privilege escalation risks, permission auditing, security hardening',
            'prerequisites': '["Linux Special Permissions (SUID, SGID, Sticky Bit)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S3 - Practical permission security'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Sudo and Sudoers Configuration',
            'module': 'SEC406 Section 3',
            'topics': 'sudo concepts, /etc/sudoers, visudo, sudo policies, NOPASSWD, command restrictions, sudo logging, best practices',
            'prerequisites': '["Linux Account Management"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S3 - Privilege delegation'
        },
        {
            'domain': 'system',
            'difficulty': 2,
            'title': 'SELinux (Security-Enhanced Linux) Fundamentals',
            'module': 'SEC406 Section 3',
            'topics': 'SELinux architecture, mandatory access control (MAC), contexts, policies, modes (enforcing/permissive/disabled), troubleshooting',
            'prerequisites': '["Linux File Permissions (chmod)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S3 - Advanced access control'
        },
        {
            'domain': 'system',
            'difficulty': 2,
            'title': 'AppArmor Security Framework',
            'module': 'SEC406 Section 3',
            'topics': 'AppArmor architecture, profiles, enforce/complain modes, profile creation, vs SELinux comparison, Ubuntu/Debian usage',
            'prerequisites': '["SELinux (Security-Enhanced Linux) Fundamentals"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S3 - Alternative MAC framework'
        },
        {
            'domain': 'system',
            'difficulty': 2,
            'title': 'Linux System Hardening Best Practices',
            'module': 'SEC406 Section 3',
            'topics': 'Hardening checklist, CIS benchmarks, attack surface reduction, unnecessary services, kernel hardening, security configurations',
            'prerequisites': '["SELinux (Security-Enhanced Linux) Fundamentals", "AppArmor Security Framework"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S3 - Comprehensive hardening'
        },

        # Section 4: Process and Log Management (6 lessons - intermediate)
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Resource Limits (ulimit)',
            'module': 'SEC406 Section 4',
            'topics': 'Resource limits, ulimit, /etc/security/limits.conf, soft/hard limits, process constraints, DoS prevention',
            'prerequisites': '["Linux Kernel, Operating System, and Distributions"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S4 - Resource control'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Process Management (ps, top, kill)',
            'module': 'SEC406 Section 4',
            'topics': 'Process viewing (ps, top, htop), process signals, kill/killall, process priorities (nice/renice), process states',
            'prerequisites': '["Linux Resource Limits (ulimit)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'SEC406 S4 - Managing processes'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Job Scheduling (cron, at)',
            'module': 'SEC406 Section 4',
            'topics': 'cron/crontab, cron syntax, at/batch, anacron, scheduled tasks, persistence mechanisms, security implications',
            'prerequisites': '["Linux Process Management (ps, top, kill)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'SEC406 S4 - Task scheduling'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Services and Systemd',
            'module': 'SEC406 Section 4',
            'topics': 'systemd architecture, systemctl, service management, unit files, targets, init systems (systemd vs sysvinit), service hardening',
            'prerequisites': '["Linux Process Management (ps, top, kill)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S4 - Service management'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Linux Logging and Log Rotation',
            'module': 'SEC406 Section 4',
            'topics': 'syslog/rsyslog, log locations (/var/log), logrotate, log management, log analysis, centralized logging',
            'prerequisites': '["Linux Services and Systemd"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'SEC406 S4 - Log management'
        },
        {
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Linux Auditd Framework',
            'module': 'SEC406 Section 4',
            'topics': 'auditd architecture, audit rules, aureport/ausearch, file/system call auditing, compliance logging, SIEM integration',
            'prerequisites': '["Linux Logging and Log Rotation"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: DFIR Specialist',
            'notes': 'SEC406 S4 - Advanced auditing (duplicate check with FOR577)'
        },

        # Section 5: Package, SSH, and Network Management (8 lessons - intermediate)
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Python Package Management on Linux (pip, venv)',
            'module': 'SEC406 Section 5',
            'topics': 'pip, virtual environments, venv, pipenv, poetry, dependency management, requirements.txt, security considerations',
            'prerequisites': '["Linux Kernel, Operating System, and Distributions"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S5 - Python package management'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Package Management (apt, yum, dnf)',
            'module': 'SEC406 Section 5',
            'topics': 'Package managers (apt, yum, dnf, zypper), repositories, package installation, updates, security patches, dependency resolution',
            'prerequisites': '["Linux Kernel, Operating System, and Distributions"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S5 - System package management'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Installing Open-Source Software from Source',
            'module': 'SEC406 Section 5',
            'topics': 'Source compilation, ./configure, make, make install, build dependencies, compilation troubleshooting, security risks',
            'prerequisites': '["Linux Package Management (apt, yum, dnf)"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer',
            'notes': 'SEC406 S5 - Building from source'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'SSH Fundamentals and Configuration',
            'module': 'SEC406 Section 5',
            'topics': 'SSH protocol, ssh client, sshd server, /etc/ssh/sshd_config, client config (~/.ssh/config), security best practices',
            'prerequisites': '["Linux Kernel, Operating System, and Distributions"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S5 - Secure remote access'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'SSH Key Management and Authentication',
            'module': 'SEC406 Section 5',
            'topics': 'SSH key generation (ssh-keygen), public/private keys, authorized_keys, key-based auth, passphrase management, key rotation',
            'prerequisites': '["SSH Fundamentals and Configuration"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S5 - SSH key authentication'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'SSH Agent and Key Forwarding',
            'module': 'SEC406 Section 5',
            'topics': 'ssh-agent, agent forwarding, ForwardAgent, security implications, key management, bastion/jump hosts',
            'prerequisites': '["SSH Key Management and Authentication"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S5 - Advanced SSH usage'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'SSH Tunneling and Port Forwarding',
            'module': 'SEC406 Section 5',
            'topics': 'Local/remote/dynamic port forwarding, SSH tunnels, SOCKS proxy, post-quantum cryptography, secure tunneling use cases',
            'prerequisites': '["SSH Fundamentals and Configuration"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Pentester',
            'notes': 'SEC406 S5 - SSH tunneling and PQC'
        },
        {
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Networking and Firewalls (iptables, firewalld)',
            'module': 'SEC406 Section 5',
            'topics': 'Network configuration, iptables, firewalld, ufw, nftables, firewall rules, network security, traffic filtering',
            'prerequisites': '["Linux Kernel, Operating System, and Distributions"]',
            'tags': 'Course: SANS-SEC406, Career Path: Blue Teamer, Career Path: Security Engineer',
            'notes': 'SEC406 S5 - Network security'
        },
    ]

    print(f"Adding {len(sec406_lessons)} SANS SEC406 lessons...\n")

    # Add new lessons
    added_count = 0
    domain_counts = {}
    difficulty_counts = {1: 0, 2: 0, 3: 0}

    for lesson in sec406_lessons:
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

    print(f"\n[SUCCESS] Added {added_count} SANS SEC406 lessons")
    print(f"Total lessons in CSV: {len(rows)}")
    print(f"\nSANS SEC406 Course Coverage:")
    print(f"  Section 1: 5 lessons - Linux Command Line")
    print(f"  Section 2: 7 lessons - Shell Syntax and Account Management")
    print(f"  Section 3: 7 lessons - File and User Access Control")
    print(f"  Section 4: 6 lessons - Process and Log Management")
    print(f"  Section 5: 8 lessons - Package, SSH, and Network Management")
    print(f"\nDifficulty Distribution:")
    print(f"  Beginner: {difficulty_counts[1]}")
    print(f"  Intermediate: {difficulty_counts[2]}")
    print(f"  Advanced: {difficulty_counts[3]}")
    print(f"\nDomains Covered:")
    for domain in sorted(domain_counts.keys()):
        print(f"  {domain}: {domain_counts[domain]} lessons")

if __name__ == '__main__':
    add_sec406_lessons()
