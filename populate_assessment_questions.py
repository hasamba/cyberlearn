#!/usr/bin/env python3
"""
Populate assessment questions for all 15 domains.

This script creates diagnostic assessment questions covering:
- 15 domains (fundamentals, osint, dfir, malware, active_directory, system, linux, cloud, pentest, red_team, blue_team, threat_hunting, ai_security, iot_security, web3_security)
- 3 difficulty levels per domain (beginner, intermediate, advanced)
- Multiple choice format
- Total: 93 questions (6-7 per domain)
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4
import json

# Assessment questions database
ASSESSMENT_QUESTIONS = {
    "fundamentals": [
        {
            "question": "What is the CIA Triad in information security?",
            "options": [
                "Confidentiality, Integrity, Availability",
                "Control, Investigation, Assessment",
                "Certification, Implementation, Authorization",
                "Configuration, Installation, Administration"
            ],
            "correct": 0,
            "difficulty": 1,
            "explanation": "The CIA Triad consists of Confidentiality (keeping data private), Integrity (keeping data accurate), and Availability (keeping systems accessible)."
        },
        {
            "question": "What is the purpose of encryption?",
            "options": [
                "To compress data to save space",
                "To protect data confidentiality by making it unreadable without a key",
                "To speed up network transmission",
                "To create backups of important files"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "Encryption transforms data into an unreadable format that can only be decrypted with the proper key, ensuring confidentiality."
        },
        {
            "question": "What is multi-factor authentication (MFA)?",
            "options": [
                "Using multiple passwords for one account",
                "Requiring two or more different types of credentials to authenticate",
                "Having multiple user accounts",
                "Using fingerprint only for login"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "MFA requires multiple independent credentials from different categories: something you know (password), something you have (token), or something you are (biometric)."
        },
        {
            "question": "Which security principle states that users should have only the minimum access necessary?",
            "options": [
                "Defense in Depth",
                "Need to Know",
                "Least Privilege",
                "Separation of Duties"
            ],
            "correct": 2,
            "difficulty": 2,
            "explanation": "The Principle of Least Privilege ensures users only have the minimum permissions required to perform their job functions."
        },
        {
            "question": "What is a zero-day vulnerability?",
            "options": [
                "A vulnerability that takes zero days to exploit",
                "A vulnerability discovered and exploited before the vendor releases a patch",
                "A vulnerability that was fixed yesterday",
                "A vulnerability with zero impact on security"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "A zero-day vulnerability is unknown to the software vendor and has no available patch, giving attackers an advantage before detection."
        },
        {
            "question": "What is the difference between a vulnerability, threat, and risk?",
            "options": [
                "They are all the same thing",
                "Vulnerability is a weakness, threat is a potential danger, risk is the likelihood and impact combined",
                "Vulnerability is external, threat is internal, risk is hypothetical",
                "Vulnerability is software-only, threat is hardware-only, risk is network-only"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Vulnerability is a weakness, threat is a potential danger that could exploit the vulnerability, and risk is the probability and impact of a threat exploiting a vulnerability."
        }
    ],
    "osint": [
        {
            "question": "What does OSINT stand for?",
            "options": [
                "Operating System Intelligence",
                "Open Source Intelligence",
                "Organized Security Intelligence Network",
                "Online Security Integration Tools"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "OSINT stands for Open Source Intelligence - gathering information from publicly available sources."
        },
        {
            "question": "Which tool is commonly used for DNS reconnaissance?",
            "options": [
                "Wireshark",
                "Nmap",
                "dig",
                "Metasploit"
            ],
            "correct": 2,
            "difficulty": 1,
            "explanation": "The 'dig' command is a DNS lookup utility used for querying DNS servers and gathering domain information."
        },
        {
            "question": "What is passive reconnaissance?",
            "options": [
                "Scanning a target's network ports",
                "Gathering information without directly interacting with the target",
                "Using social engineering to gather information",
                "Physically accessing a target location"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Passive reconnaissance involves gathering information from public sources without directly engaging the target, leaving no traces."
        },
        {
            "question": "What is Google dorking?",
            "options": [
                "A type of phishing attack",
                "Using advanced search operators to find specific information on Google",
                "Hacking Google's search algorithm",
                "Blocking Google from indexing your site"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Google dorking uses advanced search operators (like site:, filetype:, inurl:) to find specific information that might be sensitive or hidden."
        },
        {
            "question": "What is shodan.io used for?",
            "options": [
                "Social media monitoring",
                "Searching for internet-connected devices and systems",
                "Email verification",
                "Domain registration"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Shodan is a search engine for internet-connected devices, allowing users to find specific types of servers, IoT devices, and exposed systems."
        },
        {
            "question": "What information can WHOIS lookups provide?",
            "options": [
                "Website visitor statistics",
                "Domain registration details, registrant contact info, and nameservers",
                "Network bandwidth usage",
                "Server uptime statistics"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "WHOIS provides domain registration information including registrant details, registration/expiration dates, and nameserver information."
        }
    ],
    "dfir": [
        {
            "question": "What does DFIR stand for?",
            "options": [
                "Data Forensics and Incident Response",
                "Digital Forensics and Incident Response",
                "Disk Forensics Investigation Report",
                "Defense Forensics Intelligence Research"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "DFIR stands for Digital Forensics and Incident Response - the practice of investigating and responding to cybersecurity incidents."
        },
        {
            "question": "What is the order of volatility in digital forensics?",
            "options": [
                "Disk, memory, network, logs",
                "CPU registers, RAM, disk, backups",
                "Logs, RAM, disk, backups",
                "Network traffic, RAM, logs, disk"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "The order of volatility (most to least) is: CPU registers/cache, RAM, network connections, running processes, disk, remote logging, backups. Collect volatile data first."
        },
        {
            "question": "What is a write blocker used for?",
            "options": [
                "Preventing malware from executing",
                "Preventing writes to evidence drives to maintain integrity",
                "Blocking unauthorized network access",
                "Preventing users from saving files"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "A write blocker prevents any writes to a storage device, ensuring the original evidence remains unmodified during forensic acquisition."
        },
        {
            "question": "What is the purpose of creating a forensic image?",
            "options": [
                "To compress files for storage",
                "To create a bit-by-bit copy of storage media for analysis",
                "To take screenshots of evidence",
                "To create backups of important files"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "A forensic image is an exact bit-by-bit copy of storage media, allowing analysis without modifying the original evidence."
        },
        {
            "question": "What is the SANS FOR500 course focused on?",
            "options": [
                "Network penetration testing",
                "Windows forensics and incident response",
                "Malware analysis",
                "Cloud security"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "SANS FOR500 focuses on Windows forensics and incident response techniques."
        },
        {
            "question": "What is timeline analysis in DFIR?",
            "options": [
                "Tracking project deadlines",
                "Reconstructing event sequence from artifacts to understand attack progression",
                "Measuring response time to incidents",
                "Scheduling forensic investigations"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Timeline analysis involves creating a chronological sequence of events from various artifacts to reconstruct what happened during an incident."
        },
        {
            "question": "What is the difference between live forensics and dead forensics?",
            "options": [
                "Live forensics is faster than dead forensics",
                "Live forensics analyzes running systems, dead forensics analyzes powered-off systems",
                "Live forensics is for recent incidents, dead forensics is for old cases",
                "Live forensics uses different tools than dead forensics"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Live forensics captures data from a running system (volatile data), while dead forensics analyzes powered-off systems or forensic images (non-volatile data)."
        }
    ],
    "malware": [
        {
            "question": "What is malware?",
            "options": [
                "Any software with bugs",
                "Malicious software designed to harm or exploit systems",
                "Software that runs slowly",
                "Outdated software"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "Malware is any software intentionally designed to cause damage, steal data, or gain unauthorized access to systems."
        },
        {
            "question": "What is the difference between a virus and a worm?",
            "options": [
                "Viruses are worse than worms",
                "Viruses require a host program, worms self-replicate independently",
                "Viruses spread via email, worms spread via USB",
                "There is no difference"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "A virus attaches to a host program and requires user action to spread, while a worm is self-replicating and spreads automatically across networks."
        },
        {
            "question": "What is a trojan horse?",
            "options": [
                "A type of firewall",
                "Malware disguised as legitimate software",
                "A network scanning tool",
                "An encryption method"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "A trojan horse appears to be legitimate software but contains hidden malicious functionality."
        },
        {
            "question": "What is ransomware?",
            "options": [
                "Software that encrypts files and demands payment for decryption",
                "Software that steals passwords",
                "Software that spies on users",
                "Software that displays unwanted ads"
            ],
            "correct": 0,
            "difficulty": 1,
            "explanation": "Ransomware encrypts victim's files and demands payment (usually in cryptocurrency) to provide the decryption key."
        },
        {
            "question": "What is a Command and Control (C2) server?",
            "options": [
                "A server that hosts websites",
                "A server used by attackers to control compromised systems",
                "A server that stores backups",
                "A server that runs antivirus scans"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "A C2 server is used by attackers to send commands to and receive data from compromised systems in their botnet."
        },
        {
            "question": "What is polymorphic malware?",
            "options": [
                "Malware that infects multiple file types",
                "Malware that changes its code signature to evade detection",
                "Malware that targets multiple operating systems",
                "Malware with multiple payloads"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Polymorphic malware mutates its code with each infection while maintaining the same functionality, making signature-based detection difficult."
        },
        {
            "question": "What is the purpose of sandboxing in malware analysis?",
            "options": [
                "To speed up malware execution",
                "To safely execute and observe malware behavior in an isolated environment",
                "To permanently delete malware",
                "To encrypt malware samples"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Sandboxing runs malware in an isolated, monitored environment to observe its behavior without risking the host system."
        }
    ],
    "active_directory": [
        {
            "question": "What is Active Directory (AD)?",
            "options": [
                "A type of firewall",
                "Microsoft's directory service for Windows domain networks",
                "An antivirus program",
                "A backup solution"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "Active Directory is Microsoft's directory service that manages users, computers, and resources in Windows domain networks."
        },
        {
            "question": "What is a domain controller?",
            "options": [
                "A network switch",
                "A server that responds to authentication requests in a Windows domain",
                "A firewall appliance",
                "A backup server"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "A domain controller authenticates users, stores directory data, and enforces security policies for a Windows domain."
        },
        {
            "question": "What is Kerberos?",
            "options": [
                "A malware type",
                "An authentication protocol used by Active Directory",
                "A firewall technology",
                "A backup system"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Kerberos is a network authentication protocol that uses tickets to allow secure authentication over non-secure networks."
        },
        {
            "question": "What is a Golden Ticket attack?",
            "options": [
                "Stealing admin passwords",
                "Forging Kerberos TGT tickets to gain domain admin access",
                "Phishing domain users",
                "Brute forcing passwords"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "A Golden Ticket attack forges a Kerberos Ticket Granting Ticket (TGT) using the KRBTGT account hash, granting unlimited domain access."
        },
        {
            "question": "What is Pass-the-Hash (PtH)?",
            "options": [
                "Cracking password hashes offline",
                "Using captured NTLM hashes to authenticate without knowing the plaintext password",
                "Sharing passwords between users",
                "Encrypting passwords before storage"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Pass-the-Hash allows an attacker to authenticate using a captured NTLM hash without needing to crack it to obtain the plaintext password."
        },
        {
            "question": "What is the purpose of Group Policy Objects (GPOs)?",
            "options": [
                "To backup Active Directory",
                "To centrally manage and configure operating systems, applications, and user settings",
                "To encrypt domain communications",
                "To monitor network traffic"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "GPOs allow administrators to centrally configure and enforce settings across users and computers in an Active Directory domain."
        }
    ],
    "system": [
        {
            "question": "What is a registry in Windows?",
            "options": [
                "A database of installed software",
                "A hierarchical database storing system and application configuration settings",
                "A list of running processes",
                "A backup location for files"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "The Windows Registry is a hierarchical database that stores configuration settings for the operating system, drivers, and applications."
        },
        {
            "question": "What is the Windows Event Log used for?",
            "options": [
                "To track user browsing history",
                "To record system, security, and application events",
                "To store temporary files",
                "To manage network connections"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "Windows Event Logs record important events including system errors, security events, and application issues for troubleshooting and auditing."
        },
        {
            "question": "What is the Master File Table (MFT) in NTFS?",
            "options": [
                "A list of installed programs",
                "A database containing information about every file and directory on an NTFS volume",
                "A network routing table",
                "A list of active processes"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "The MFT is a critical NTFS structure that stores metadata for every file and directory, including timestamps, attributes, and data locations."
        },
        {
            "question": "What is the purpose of prefetch files in Windows?",
            "options": [
                "To store deleted files",
                "To speed up application loading by caching frequently accessed data",
                "To encrypt system files",
                "To compress large files"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Prefetch files contain information about application execution to optimize loading times and are valuable forensic artifacts showing program execution history."
        },
        {
            "question": "What is the Windows Alternate Data Stream (ADS)?",
            "options": [
                "A backup storage location",
                "A feature of NTFS allowing files to contain multiple data streams",
                "A network protocol",
                "A type of encryption"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "ADS is an NTFS feature allowing files to contain multiple data streams. Attackers can hide malicious code in alternate streams."
        },
        {
            "question": "What is the difference between kernel mode and user mode?",
            "options": [
                "Kernel mode is faster than user mode",
                "Kernel mode has full hardware access, user mode has restricted access",
                "Kernel mode is for servers, user mode is for desktops",
                "There is no difference"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Kernel mode code has unrestricted access to hardware and memory, while user mode code runs in a protected environment with limited privileges."
        }
    ],
    "linux": [
        {
            "question": "What is the purpose of the /etc/passwd file in Linux?",
            "options": [
                "To store encrypted passwords",
                "To store user account information",
                "To store system logs",
                "To store network configuration"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "/etc/passwd contains user account information including username, UID, GID, home directory, and default shell. Passwords are stored in /etc/shadow."
        },
        {
            "question": "What does the chmod command do?",
            "options": [
                "Changes file ownership",
                "Changes file permissions",
                "Moves files",
                "Compresses files"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "chmod (change mode) modifies file permissions, controlling who can read, write, or execute files."
        },
        {
            "question": "What is sudo used for?",
            "options": [
                "To switch users",
                "To execute commands with elevated (root) privileges",
                "To shutdown the system",
                "To list files"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "sudo allows authorized users to execute commands as the superuser (root) or another user with elevated privileges."
        },
        {
            "question": "What is the purpose of the /var/log directory?",
            "options": [
                "To store user documents",
                "To store system and application log files",
                "To store temporary files",
                "To store program binaries"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "/var/log contains system and application log files used for troubleshooting, auditing, and forensic investigations."
        },
        {
            "question": "What is a cron job?",
            "options": [
                "A running process",
                "A scheduled task that runs automatically at specified times",
                "A system service",
                "A type of script"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "A cron job is a scheduled task configured in crontab that executes commands or scripts automatically at specified intervals."
        },
        {
            "question": "What is the difference between hard links and soft links (symlinks)?",
            "options": [
                "Hard links are faster than soft links",
                "Hard links point to inode data, soft links point to file paths",
                "Hard links work across filesystems, soft links don't",
                "There is no difference"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Hard links point directly to the inode (file data), while soft links (symlinks) point to the file path. Hard links can't cross filesystems."
        },
        {
            "question": "What information can you find in the bash history file?",
            "options": [
                "System boot times",
                "Previously executed commands by the user",
                "Network connections",
                "Installed packages"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "The .bash_history file (usually in home directory) records commands previously executed by the user in the bash shell."
        }
    ],
    "cloud": [
        {
            "question": "What is the cloud computing shared responsibility model?",
            "options": [
                "Cloud provider and customer share costs equally",
                "Security and compliance responsibilities are divided between provider and customer",
                "Multiple customers share the same servers",
                "Customers share their data with the provider"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "The shared responsibility model defines which security controls are managed by the cloud provider (infrastructure) versus the customer (data, applications, access)."
        },
        {
            "question": "What is an S3 bucket in AWS?",
            "options": [
                "A compute instance",
                "An object storage container",
                "A database service",
                "A networking component"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "S3 (Simple Storage Service) buckets are containers for storing objects (files) in AWS cloud storage."
        },
        {
            "question": "What is IAM in AWS?",
            "options": [
                "Internet Access Management",
                "Identity and Access Management",
                "Infrastructure Automation Manager",
                "Internal Application Monitor"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "IAM (Identity and Access Management) controls user access and permissions to AWS resources and services."
        },
        {
            "question": "What is CloudTrail in AWS?",
            "options": [
                "A CDN service",
                "A logging service that records AWS API calls and account activity",
                "A backup service",
                "A monitoring dashboard"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "CloudTrail logs all API calls and account activity in AWS, providing an audit trail for security analysis and compliance."
        },
        {
            "question": "What is a security group in AWS?",
            "options": [
                "A group of IAM users",
                "A virtual firewall controlling inbound and outbound traffic for resources",
                "A collection of S3 buckets",
                "A monitoring alert group"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Security groups act as virtual firewalls for EC2 instances and other resources, controlling inbound and outbound network traffic."
        },
        {
            "question": "What is the principle of least privilege in cloud IAM?",
            "options": [
                "Granting minimum necessary permissions to users",
                "Using the smallest instance sizes",
                "Minimizing cloud costs",
                "Reducing network latency"
            ],
            "correct": 0,
            "difficulty": 2,
            "explanation": "Least privilege means granting users and services only the minimum permissions necessary to perform their required tasks."
        },
        {
            "question": "What is serverless computing?",
            "options": [
                "Computing without internet connection",
                "Running applications without managing underlying infrastructure",
                "Using peer-to-peer networks",
                "Cloud computing without costs"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Serverless computing (like AWS Lambda) allows running code without provisioning or managing servers, with automatic scaling and pay-per-execution pricing."
        }
    ],
    "pentest": [
        {
            "question": "What is penetration testing?",
            "options": [
                "Testing network speed",
                "Authorized simulated cyberattack to test security defenses",
                "Installing security patches",
                "Monitoring network traffic"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "Penetration testing is an authorized simulated attack on systems to identify vulnerabilities and assess security posture."
        },
        {
            "question": "What is the difference between white box, gray box, and black box testing?",
            "options": [
                "Different testing tools",
                "Different levels of prior knowledge about the target",
                "Different attack techniques",
                "Different report formats"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "White box has full knowledge, gray box has partial knowledge, and black box has no prior knowledge of the target system."
        },
        {
            "question": "What is Nmap used for?",
            "options": [
                "Password cracking",
                "Network scanning and port discovery",
                "Malware analysis",
                "Log analysis"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "Nmap (Network Mapper) is a network scanning tool used to discover hosts, open ports, services, and operating systems."
        },
        {
            "question": "What is Metasploit Framework?",
            "options": [
                "An antivirus program",
                "A penetration testing framework with exploit modules",
                "A firewall configuration tool",
                "A backup solution"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Metasploit is a comprehensive penetration testing framework containing exploit modules, payloads, and auxiliary tools."
        },
        {
            "question": "What is SQL injection?",
            "options": [
                "Installing SQL databases",
                "Injecting malicious SQL code to manipulate database queries",
                "Backing up SQL databases",
                "Encrypting SQL data"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "SQL injection exploits vulnerabilities in web applications by inserting malicious SQL statements to manipulate or extract database data."
        },
        {
            "question": "What is a reverse shell?",
            "options": [
                "A backup shell session",
                "A shell connection initiated from the target back to the attacker",
                "A shell with reversed commands",
                "An encrypted shell session"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "A reverse shell connects from the compromised target back to the attacker's system, bypassing firewalls that block inbound connections."
        },
        {
            "question": "What is privilege escalation?",
            "options": [
                "Increasing network bandwidth",
                "Gaining higher access privileges than initially obtained",
                "Adding more user accounts",
                "Upgrading software versions"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Privilege escalation involves exploiting vulnerabilities to gain higher access levels, often from standard user to administrator/root."
        }
    ],
    "red_team": [
        {
            "question": "What is the difference between penetration testing and red teaming?",
            "options": [
                "They are the same thing",
                "Red teaming simulates real adversaries with broader objectives, pentesting focuses on finding vulnerabilities",
                "Red teaming is easier than pentesting",
                "Pentesting is for networks, red teaming is for applications"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Red teaming simulates sophisticated adversaries with strategic objectives, while penetration testing focuses on identifying specific vulnerabilities."
        },
        {
            "question": "What is OPSEC in red teaming?",
            "options": [
                "Operations Security - protecting information about activities",
                "Open Source Security",
                "Operational Systems Engineering",
                "Offensive Penetration Security"
            ],
            "correct": 0,
            "difficulty": 2,
            "explanation": "OPSEC (Operations Security) involves protecting information about red team activities to avoid detection and maintain operational effectiveness."
        },
        {
            "question": "What is a Command and Control (C2) framework?",
            "options": [
                "A network management tool",
                "Infrastructure used to maintain control over compromised systems",
                "A firewall configuration",
                "A backup system"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "C2 frameworks (like Cobalt Strike) allow red teamers to maintain control over compromised systems and execute post-exploitation activities."
        },
        {
            "question": "What is lateral movement?",
            "options": [
                "Moving files between folders",
                "Moving through a network after initial compromise to access additional systems",
                "Changing user accounts",
                "Network load balancing"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Lateral movement involves moving from one compromised system to other systems within the network to access high-value targets."
        },
        {
            "question": "What is persistence in red teaming?",
            "options": [
                "Continuing the engagement for a long time",
                "Maintaining access to a compromised system across reboots and credential changes",
                "Repeatedly attacking the same target",
                "Keeping detailed documentation"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Persistence mechanisms ensure continued access to compromised systems even after reboots, allowing long-term operations."
        },
        {
            "question": "What is living off the land (LOL) in red teaming?",
            "options": [
                "Conducting physical operations",
                "Using legitimate system tools and features for malicious purposes",
                "Working without internet connection",
                "Using open-source tools only"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Living off the land uses legitimate system binaries and features (LOLbins) for malicious purposes, making detection harder."
        }
    ],
    "blue_team": [
        {
            "question": "What is the primary goal of a blue team?",
            "options": [
                "To attack systems",
                "To defend against and detect attacks",
                "To develop software",
                "To manage networks"
            ],
            "correct": 1,
            "difficulty": 1,
            "explanation": "Blue teams focus on defending systems, detecting threats, and responding to security incidents."
        },
        {
            "question": "What is a SIEM system?",
            "options": [
                "A firewall",
                "Security Information and Event Management - centralized log collection and analysis",
                "A backup solution",
                "An antivirus program"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "SIEM systems collect, correlate, and analyze security logs from multiple sources to detect threats and support incident response."
        },
        {
            "question": "What is an Intrusion Detection System (IDS)?",
            "options": [
                "A firewall that blocks attacks",
                "A system that monitors and alerts on suspicious network activity",
                "An antivirus scanner",
                "A password manager"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "An IDS monitors network traffic or system activity for suspicious behavior and generates alerts but doesn't block traffic."
        },
        {
            "question": "What is the difference between IDS and IPS?",
            "options": [
                "IDS detects and alerts, IPS detects and blocks",
                "IDS is faster than IPS",
                "IDS is for networks, IPS is for hosts",
                "There is no difference"
            ],
            "correct": 0,
            "difficulty": 2,
            "explanation": "IDS (Intrusion Detection System) only alerts on threats, while IPS (Intrusion Prevention System) actively blocks detected threats."
        },
        {
            "question": "What is endpoint detection and response (EDR)?",
            "options": [
                "Network monitoring software",
                "Security solution that monitors endpoints for threats and enables response",
                "Firewall software",
                "Backup software"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "EDR solutions monitor endpoint devices (workstations, servers) for threats, providing visibility, detection, and response capabilities."
        },
        {
            "question": "What is a false positive in security monitoring?",
            "options": [
                "A real attack that was detected",
                "An alert triggered by benign activity incorrectly flagged as malicious",
                "A missed attack",
                "An encrypted connection"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "A false positive occurs when security tools incorrectly flag legitimate activity as malicious, generating unnecessary alerts."
        },
        {
            "question": "What is defense in depth?",
            "options": [
                "Using one very strong security control",
                "Implementing multiple layers of security controls",
                "Deeply analyzing threats",
                "Having a large security team"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Defense in depth uses multiple overlapping layers of security controls so that if one fails, others still provide protection."
        }
    ],
    "threat_hunting": [
        {
            "question": "What is threat hunting?",
            "options": [
                "Waiting for alerts from security tools",
                "Proactively searching for threats that evaded existing security controls",
                "Scanning for vulnerabilities",
                "Installing antivirus software"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Threat hunting is the proactive practice of searching through networks and systems to detect threats that evaded automated detection tools."
        },
        {
            "question": "What is a hypothesis-driven threat hunt?",
            "options": [
                "Randomly searching for threats",
                "Starting with a theory about potential threats and testing it",
                "Waiting for alerts",
                "Following a checklist"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Hypothesis-driven hunting starts with a specific theory about potential threats based on intelligence or environmental knowledge."
        },
        {
            "question": "What is an Indicator of Compromise (IOC)?",
            "options": [
                "A security policy",
                "Evidence that a security breach has occurred",
                "A type of malware",
                "A firewall rule"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "IOCs are forensic artifacts (like file hashes, IPs, domains) that indicate a system has been compromised or attacked."
        },
        {
            "question": "What is the MITRE ATT&CK framework?",
            "options": [
                "A penetration testing methodology",
                "A knowledge base of adversary tactics and techniques based on real-world observations",
                "A compliance framework",
                "A programming language"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "MITRE ATT&CK is a comprehensive framework documenting adversary tactics, techniques, and procedures (TTPs) used in cyberattacks."
        },
        {
            "question": "What is a threat intelligence feed?",
            "options": [
                "A news website about cybersecurity",
                "A stream of IOCs and threat information from external sources",
                "A social media account",
                "An email newsletter"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Threat intelligence feeds provide real-time information about known threats, IOCs, and adversary behaviors from various sources."
        },
        {
            "question": "What is behavioral analysis in threat hunting?",
            "options": [
                "Analyzing user personalities",
                "Identifying anomalous patterns and behaviors that may indicate threats",
                "Studying attacker psychology",
                "Monitoring employee productivity"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Behavioral analysis identifies deviations from normal patterns that may indicate malicious activity, focusing on actions rather than signatures."
        }
    ],
    "ai_security": [
        {
            "question": "What is the OWASP LLM Top 10?",
            "options": [
                "A list of AI programming languages",
                "A list of the most critical security risks for Large Language Model applications",
                "A ranking of AI companies",
                "A machine learning algorithm"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "OWASP LLM Top 10 identifies the most critical security vulnerabilities and risks specific to applications using Large Language Models."
        },
        {
            "question": "What is prompt injection in AI security?",
            "options": [
                "Optimizing AI prompts",
                "Manipulating AI input to cause unintended behavior or bypass restrictions",
                "Training AI models faster",
                "Creating better AI responses"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Prompt injection attacks manipulate LLM inputs to make the model ignore instructions, leak data, or perform unintended actions."
        },
        {
            "question": "What is model poisoning?",
            "options": [
                "Deleting AI models",
                "Injecting malicious data into training sets to corrupt AI model behavior",
                "Slowing down AI models",
                "Encrypting AI models"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Model poisoning corrupts AI training data or fine-tuning processes to manipulate model behavior or introduce backdoors."
        },
        {
            "question": "What is adversarial ML?",
            "options": [
                "Using AI for attacks",
                "Techniques to fool machine learning models with crafted inputs",
                "Competing AI models",
                "AI-powered firewalls"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Adversarial ML involves creating specially crafted inputs designed to cause machine learning models to make incorrect predictions."
        },
        {
            "question": "What is sensitive data exposure in LLMs?",
            "options": [
                "Sharing AI model architecture",
                "LLMs inadvertently revealing training data or sensitive information in responses",
                "Publishing AI research",
                "Open-sourcing AI models"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "LLMs may leak sensitive information from training data or context through their responses, requiring careful data handling and output filtering."
        },
        {
            "question": "What is AI hallucination?",
            "options": [
                "AI models getting confused",
                "AI generating false or fabricated information presented as fact",
                "AI models crashing",
                "AI being too slow"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "AI hallucination occurs when models generate plausible-sounding but false or fabricated information, which can be a security risk in critical applications."
        }
    ],
    "iot_security": [
        {
            "question": "What does IoT stand for?",
            "options": [
                "Internet of Things",
                "Internet over TCP",
                "Integrated Online Technology",
                "Internal Operations Technology"
            ],
            "correct": 0,
            "difficulty": 1,
            "explanation": "IoT (Internet of Things) refers to physical devices connected to the internet, collecting and exchanging data."
        },
        {
            "question": "What is a common security challenge with IoT devices?",
            "options": [
                "They are too expensive",
                "Many lack basic security features and use default credentials",
                "They are too complex to use",
                "They are too large"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "IoT devices often lack security features, use default passwords, rarely receive updates, and have limited computing resources for security controls."
        },
        {
            "question": "What is firmware in IoT devices?",
            "options": [
                "The physical case",
                "Low-level software that provides device control and functionality",
                "The network connection",
                "The power supply"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Firmware is the low-level software embedded in IoT devices that controls hardware functionality. Vulnerable firmware is a major security concern."
        },
        {
            "question": "What is the Mirai botnet?",
            "options": [
                "An IoT security tool",
                "A malware that infected IoT devices to create a massive DDoS botnet",
                "An IoT protocol",
                "An encryption standard"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Mirai is malware that infected thousands of IoT devices (cameras, routers) using default credentials to create a powerful DDoS botnet."
        },
        {
            "question": "What is MQTT in IoT?",
            "options": [
                "A security protocol",
                "A lightweight messaging protocol commonly used by IoT devices",
                "An encryption algorithm",
                "A hardware interface"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "MQTT (Message Queuing Telemetry Transport) is a lightweight publish-subscribe messaging protocol commonly used in IoT applications."
        }
    ],
    "web3_security": [
        {
            "question": "What is Web3?",
            "options": [
                "The third version of HTML",
                "Decentralized internet based on blockchain technology",
                "A web browser",
                "A programming language"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Web3 refers to a decentralized internet built on blockchain technology, featuring cryptocurrencies, smart contracts, and distributed applications."
        },
        {
            "question": "What is a smart contract?",
            "options": [
                "A digital legal document",
                "Self-executing code on a blockchain that automatically enforces agreement terms",
                "An AI-powered contract analyzer",
                "A secure email protocol"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "Smart contracts are programs stored on blockchain that automatically execute when predefined conditions are met, without intermediaries."
        },
        {
            "question": "What is a reentrancy attack in smart contracts?",
            "options": [
                "Deploying the same contract twice",
                "Exploiting a contract by recursively calling it before state updates complete",
                "Viewing contract source code",
                "Testing contracts multiple times"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "Reentrancy attacks exploit vulnerable smart contracts by recursively calling functions before previous invocations complete, potentially draining funds."
        },
        {
            "question": "What is a cryptocurrency wallet private key?",
            "options": [
                "A password for exchanges",
                "A secret cryptographic key that controls access to cryptocurrency",
                "A public address",
                "A transaction ID"
            ],
            "correct": 1,
            "difficulty": 2,
            "explanation": "A private key is a secret cryptographic key that provides ownership and control over cryptocurrency. If compromised, funds can be stolen."
        },
        {
            "question": "What is a 51% attack on blockchain?",
            "options": [
                "Stealing 51% of cryptocurrency",
                "Controlling majority of network hash power to manipulate transactions",
                "A tax on cryptocurrency",
                "A blockchain upgrade"
            ],
            "correct": 1,
            "difficulty": 3,
            "explanation": "A 51% attack occurs when an entity controls over 50% of a blockchain's mining/validation power, allowing transaction manipulation and double-spending."
        }
    ]
}


def populate_assessment_questions():
    """Populate assessment questions table"""
    db_path = Path("cyberlearn.db")

    if not db_path.exists():
        print("ERROR Database not found at cyberlearn.db")
        print("Please run the app first to create the database.")
        return False

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Check if assessment_questions table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assessment_questions'")
    if not cursor.fetchone():
        print("ERROR assessment_questions table does not exist!")
        print("Please ensure the database schema is up to date.")
        conn.close()
        return False

    # Check if questions already exist
    cursor.execute("SELECT COUNT(*) FROM assessment_questions")
    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        print(f"Found {existing_count} existing assessment questions.")
        response = input("Delete existing questions and repopulate? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            conn.close()
            return False

        cursor.execute("DELETE FROM assessment_questions")
        print("Deleted existing questions.")

    print("\n" + "=" * 60)
    print("POPULATING ASSESSMENT QUESTIONS")
    print("=" * 60)

    total_questions = 0

    for domain, questions in ASSESSMENT_QUESTIONS.items():
        print(f"\n{domain.replace('_', ' ').title()}: Adding {len(questions)} questions")

        for question_data in questions:
            question_id = str(uuid4())

            cursor.execute("""
                INSERT INTO assessment_questions (
                    question_id, domain, question_text, options,
                    correct_answer, difficulty, explanation, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question_id,
                domain,
                question_data["question"],
                json.dumps(question_data["options"]),
                question_data["correct"],
                question_data["difficulty"],
                question_data["explanation"],
                datetime.now(timezone.utc).isoformat()
            ))

            total_questions += 1

        print(f"  OK Added {len(questions)} questions")

    conn.commit()

    # Verify counts
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    cursor.execute("SELECT domain, COUNT(*) FROM assessment_questions GROUP BY domain ORDER BY domain")
    for row in cursor.fetchall():
        print(f"  {row[0].replace('_', ' ').title()}: {row[1]} questions")

    print("\n" + "=" * 60)
    print("SUCCESS ASSESSMENT QUESTIONS POPULATED!")
    print("=" * 60)
    print(f"\nTotal questions created: {total_questions}")
    print(f"Domains covered: {len(ASSESSMENT_QUESTIONS)}")
    print("\nUsers can now take the skill assessment in the app.")

    conn.close()
    return True


if __name__ == "__main__":
    import sys
    success = populate_assessment_questions()
    sys.exit(0 if success else 1)
