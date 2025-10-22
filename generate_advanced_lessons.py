"""
Generate ADVANCED cybersecurity lessons
Focuses on: AD vulnerabilities, APT simulations, advanced Red/Blue Team operations
"""

import json
from uuid import uuid4
from datetime import datetime

# Advanced lesson curriculum
ADVANCED_CURRICULUM = {
    "active_directory": [
        {
            "title": "Kerberoasting Attack",
            "subtitle": "Exploiting service account credentials",
            "difficulty": 4,
            "order": 4,
            "concepts": ["SPN enumeration", "TGS extraction", "Offline cracking", "Mitigation strategies"],
            "quiz": [
                {
                    "q": "What does Kerberoasting target?",
                    "opts": ["User passwords", "Service account TGS tickets", "Domain controller files", "DNS records"],
                    "correct": 1,
                    "explanation": "Kerberoasting extracts TGS tickets for service accounts, which can be cracked offline to reveal passwords."
                },
                {
                    "q": "How can you mitigate Kerberoasting?",
                    "opts": ["Disable Kerberos", "Use long complex passwords for service accounts", "Remove all SPNs", "Disable TGS"],
                    "correct": 1,
                    "explanation": "Long, complex passwords (25+ characters) for service accounts make offline cracking impractical."
                },
                {
                    "q": "What tool is commonly used for Kerberoasting?",
                    "opts": ["mimikatz", "Rubeus/Invoke-Kerberoast", "nmap", "Wireshark"],
                    "correct": 1,
                    "explanation": "Rubeus and Invoke-Kerberoast are PowerShell tools specifically designed for Kerberoasting attacks."
                }
            ],
            "attack_simulation": {
                "scenario": "You've gained initial access to a Windows domain. Now you need to escalate privileges.",
                "steps": [
                    "Enumerate SPNs using setspn -T domain -Q */*",
                    "Request TGS tickets for service accounts",
                    "Extract tickets using Rubeus or Invoke-Kerberoast",
                    "Crack tickets offline with Hashcat",
                    "Use compromised service account credentials"
                ],
                "detection": [
                    "Monitor for unusual TGS requests (Event ID 4769)",
                    "Alert on encryption type downgrades (RC4 vs AES)",
                    "Track service account authentication patterns"
                ]
            }
        },
        {
            "title": "Golden Ticket Attack",
            "subtitle": "Forging Kerberos TGTs for domain persistence",
            "difficulty": 4,
            "order": 5,
            "concepts": ["KRBTGT hash", "Ticket forging", "Domain persistence", "Detection methods"],
            "quiz": [
                {
                    "q": "What is required to create a Golden Ticket?",
                    "opts": ["User password", "KRBTGT account hash", "Domain admin token", "DNS records"],
                    "correct": 1,
                    "explanation": "The KRBTGT account hash is used to forge TGTs, creating a Golden Ticket with domain admin privileges."
                },
                {
                    "q": "Why are Golden Tickets dangerous?",
                    "opts": ["They're loud and easily detected", "They provide persistent domain access", "They only work once", "They require constant C2 connection"],
                    "correct": 1,
                    "explanation": "Golden Tickets provide persistent domain access and survive password resets (except KRBTGT rotation)."
                },
                {
                    "q": "How do you remediate a Golden Ticket attack?",
                    "opts": ["Reset user passwords", "Rotate KRBTGT password twice", "Reboot domain controllers", "Disable Kerberos"],
                    "correct": 1,
                    "explanation": "KRBTGT must be rotated TWICE (maintains two password versions) to invalidate all Golden Tickets."
                }
            ],
            "attack_simulation": {
                "scenario": "You've compromised a domain controller and extracted credentials. Time for persistence.",
                "steps": [
                    "Extract KRBTGT hash using mimikatz",
                    "Gather domain SID and domain name",
                    "Forge TGT with desired privileges (Domain Admin)",
                    "Inject ticket into memory",
                    "Access any resource in the domain"
                ],
                "detection": [
                    "Monitor for tickets with unusual lifetimes (10 years)",
                    "Track tickets created outside normal KDC processes",
                    "Alert on tickets for disabled accounts",
                    "Monitor KRBTGT password changes"
                ]
            }
        },
        {
            "title": "Pass-the-Hash and Pass-the-Ticket",
            "subtitle": "Lateral movement without passwords",
            "difficulty": 4,
            "order": 6,
            "concepts": ["NTLM hash reuse", "Ticket reuse", "Lateral movement", "Credential theft"],
            "quiz": [
                {
                    "q": "What is Pass-the-Hash?",
                    "opts": ["Cracking password hashes", "Authenticating with hash instead of password", "Hashing passwords", "Deleting hash files"],
                    "correct": 1,
                    "explanation": "Pass-the-Hash uses the NTLM hash directly for authentication without knowing the plaintext password."
                },
                {
                    "q": "How does Pass-the-Ticket differ from Pass-the-Hash?",
                    "opts": ["It's the same thing", "PtT uses Kerberos tickets instead of NTLM hashes", "PtT is slower", "PtT requires passwords"],
                    "correct": 1,
                    "explanation": "Pass-the-Ticket reuses Kerberos tickets for authentication, while PtH uses NTLM hashes."
                }
            ]
        },
        {
            "title": "DCSync Attack",
            "subtitle": "Replicating Active Directory credentials",
            "difficulty": 4,
            "order": 7,
            "concepts": ["Directory replication", "Credential dumping", "Domain compromise", "Detection"],
            "quiz": [
                {
                    "q": "What does DCSync abuse?",
                    "opts": ["DNS protocols", "Domain replication rights", "File sharing", "Remote desktop"],
                    "correct": 1,
                    "explanation": "DCSync abuses directory replication (DS-Replication-Get-Changes) to extract credentials from domain controllers."
                },
                {
                    "q": "What permissions are needed for DCSync?",
                    "opts": ["Read-only domain user", "DS-Replication-Get-Changes rights", "Physical DC access", "DNS admin"],
                    "correct": 1,
                    "explanation": "DCSync requires replication rights: DS-Replication-Get-Changes and DS-Replication-Get-Changes-All."
                }
            ],
            "attack_simulation": {
                "scenario": "You've compromised an account with replication rights. Extract all domain credentials.",
                "steps": [
                    "Verify replication permissions",
                    "Use mimikatz: lsadump::dcsync /domain:example.com /all",
                    "Extract KRBTGT, admin, and user hashes",
                    "Store credentials for future use"
                ],
                "detection": [
                    "Monitor replication requests from non-DC systems",
                    "Alert on Event ID 4662 with replication GUIDs",
                    "Track accounts with replication rights"
                ]
            }
        },
        {
            "title": "AD Certificate Services Exploitation",
            "subtitle": "ESC1-ESC8 certificate abuse techniques",
            "difficulty": 4,
            "order": 8,
            "concepts": ["PKI vulnerabilities", "Certificate templates", "ESC attacks", "Persistence"],
            "quiz": [
                {
                    "q": "What is ESC1 vulnerability?",
                    "opts": ["Weak encryption", "Misconfigured certificate template allowing SAN", "SQL injection", "Buffer overflow"],
                    "correct": 1,
                    "explanation": "ESC1 allows requesting certificates with arbitrary Subject Alternative Names, enabling impersonation."
                },
                {
                    "q": "Why are AD CS attacks powerful?",
                    "opts": ["Easy to execute", "Certificates provide long-term authentication", "Require no privileges", "Can't be detected"],
                    "correct": 1,
                    "explanation": "Certificates can be used for authentication even after password changes, providing persistent access."
                }
            ]
        }
    ],
    "red_team": [
        {
            "title": "APT29 (Cozy Bear) TTPs",
            "subtitle": "Simulating Russian state-sponsored threat actor",
            "difficulty": 4,
            "order": 1,
            "concepts": ["Initial access", "Persistence", "Stealth", "Data exfiltration"],
            "quiz": [
                {
                    "q": "What is APT29 known for?",
                    "opts": ["Ransomware", "State-sponsored espionage", "Cryptomining", "DDoS attacks"],
                    "correct": 1,
                    "explanation": "APT29 (Cozy Bear) is a Russian state-sponsored APT focused on intelligence gathering and long-term espionage."
                },
                {
                    "q": "Which initial access vector is commonly used by APT29?",
                    "opts": ["SQL injection", "Spear phishing", "Physical access", "Brute force"],
                    "correct": 1,
                    "explanation": "APT29 frequently uses highly targeted spear phishing campaigns with malicious attachments or links."
                },
                {
                    "q": "What makes APT29 particularly stealthy?",
                    "opts": ["No malware used", "Living-off-the-land techniques and legitimate tools", "Very fast attacks", "DDoS as distraction"],
                    "correct": 1,
                    "explanation": "APT29 uses legitimate tools (PowerShell, WMI, legitimate admin tools) to blend in with normal activity."
                }
            ],
            "attack_path": {
                "scenario": "Simulate APT29 attack chain against corporate environment",
                "phases": [
                    {
                        "name": "Initial Compromise",
                        "techniques": [
                            "Spear phishing with malicious Office document",
                            "Macro-based dropper",
                            "WellMess or WellMail malware deployment"
                        ],
                        "mitre_tactics": ["Initial Access: T1566.001"]
                    },
                    {
                        "name": "Establish Foothold",
                        "techniques": [
                            "PowerShell Empire or Cobalt Strike",
                            "Registry persistence",
                            "Scheduled tasks"
                        ],
                        "mitre_tactics": ["Persistence: T1053.005", "Execution: T1059.001"]
                    },
                    {
                        "name": "Credential Access",
                        "techniques": [
                            "mimikatz for LSASS dumping",
                            "Pass-the-hash",
                            "Kerberoasting"
                        ],
                        "mitre_tactics": ["Credential Access: T1003.001", "T1558.003"]
                    },
                    {
                        "name": "Lateral Movement",
                        "techniques": [
                            "PsExec or WMI",
                            "Remote Desktop Protocol",
                            "Stolen credentials"
                        ],
                        "mitre_tactics": ["Lateral Movement: T1021.001", "T1021.002"]
                    },
                    {
                        "name": "Data Collection & Exfiltration",
                        "techniques": [
                            "Archive sensitive files",
                            "OneDrive/cloud storage for staging",
                            "HTTPS exfiltration to legitimate services"
                        ],
                        "mitre_tactics": ["Collection: T1560", "Exfiltration: T1567.002"]
                    }
                ],
                "detection_opportunities": [
                    "Email gateway detecting malicious macros",
                    "EDR detecting LSASS access",
                    "Network monitoring for unusual cloud uploads",
                    "Behavioral analytics for anomalous PowerShell usage"
                ]
            }
        },
        {
            "title": "APT28 (Fancy Bear) Operations",
            "subtitle": "Simulating GRU-linked threat actor",
            "difficulty": 4,
            "order": 2,
            "concepts": ["Credential harvesting", "Supply chain attacks", "Infrastructure"],
            "quiz": [
                {
                    "q": "What differentiates APT28 from APT29?",
                    "opts": ["APT28 is more stealthy", "APT28 is more aggressive and destructive", "APT28 only targets military", "APT28 uses only open-source tools"],
                    "correct": 1,
                    "explanation": "APT28 (GRU-linked) tends to be more aggressive, including destructive attacks and information operations."
                },
                {
                    "q": "Which APT28 malware family is notable?",
                    "opts": ["WannaCry", "X-Agent/Sofacy", "Emotet", "Zeus"],
                    "correct": 1,
                    "explanation": "X-Agent (Sofacy) is APT28's primary modular backdoor with extensive capabilities."
                }
            ],
            "attack_path": {
                "scenario": "Simulate APT28 attack targeting government/military",
                "phases": [
                    {
                        "name": "Reconnaissance",
                        "techniques": [
                            "Extensive OSINT on targets",
                            "LinkedIn profiling",
                            "Infrastructure mapping"
                        ],
                        "mitre_tactics": ["Reconnaissance: T1589", "T1591"]
                    },
                    {
                        "name": "Initial Access",
                        "techniques": [
                            "Spear phishing with exploits",
                            "Watering hole attacks",
                            "USB drop attacks"
                        ],
                        "mitre_tactics": ["Initial Access: T1566", "T1189", "T1091"]
                    },
                    {
                        "name": "Malware Deployment",
                        "techniques": [
                            "X-Agent implant",
                            "Sedkit exploit kit",
                            "Credential harvesting modules"
                        ],
                        "mitre_tactics": ["Execution: T1204", "Command and Control: T1071"]
                    }
                ]
            }
        },
        {
            "title": "Lazarus Group Financial Attacks",
            "subtitle": "Simulating North Korean cybercrime operations",
            "difficulty": 4,
            "order": 3,
            "concepts": ["Financial targeting", "SWIFT attacks", "Cryptocurrency theft", "Destructive attacks"],
            "quiz": [
                {
                    "q": "What is Lazarus Group primarily motivated by?",
                    "opts": ["Espionage only", "Financial gain for DPRK", "Hacktivism", "Ransomware distribution"],
                    "correct": 1,
                    "explanation": "Lazarus Group conducts financially motivated attacks to generate revenue for North Korea."
                },
                {
                    "q": "Which Lazarus attack is most infamous?",
                    "opts": ["Stuxnet", "WannaCry ransomware", "Heartbleed", "Shellshock"],
                    "correct": 1,
                    "explanation": "WannaCry (2017) was attributed to Lazarus, causing global disruption and financial losses."
                }
            ]
        },
        {
            "title": "Advanced C2 Infrastructure",
            "subtitle": "Building resilient command and control",
            "difficulty": 4,
            "order": 4,
            "concepts": ["Domain fronting", "C2 channels", "Anonymization", "Resilience"],
            "quiz": [
                {
                    "q": "What is domain fronting?",
                    "opts": ["DNS hijacking", "Using CDN to hide true C2 destination", "Port forwarding", "VPN tunneling"],
                    "correct": 1,
                    "explanation": "Domain fronting uses CDNs (CloudFront, Azure CDN) to disguise C2 traffic as legitimate HTTPS connections."
                },
                {
                    "q": "Why use multiple C2 channels?",
                    "opts": ["Faster speed", "Redundancy and resilience against takedowns", "Better encryption", "Cheaper infrastructure"],
                    "correct": 1,
                    "explanation": "Multiple C2 channels provide fallback options if primary infrastructure is blocked or taken down."
                }
            ]
        },
        {
            "title": "Living Off The Land (LOLBins)",
            "subtitle": "Using legitimate tools for malicious purposes",
            "difficulty": 4,
            "order": 5,
            "concepts": ["Native Windows tools", "Detection evasion", "Fileless attacks", "Application whitelisting bypass"],
            "quiz": [
                {
                    "q": "What is a LOLBin?",
                    "opts": ["Linux malware", "Legitimate tool used maliciously", "Ransomware type", "Firewall rule"],
                    "correct": 1,
                    "explanation": "LOLBin = Living Off The Land Binary: legitimate OS tools (like PowerShell, certutil, bitsadmin) used for attacks."
                },
                {
                    "q": "Why are LOLBins effective?",
                    "opts": ["They're faster", "They bypass many security controls designed to block unknown executables", "They're easier to code", "They require no privileges"],
                    "correct": 1,
                    "explanation": "LOLBins are signed, trusted binaries that bypass application whitelisting and raise fewer alerts."
                },
                {
                    "q": "Which is an example of LOLBin abuse?",
                    "opts": ["SQL injection", "Using certutil.exe to download malware", "Buffer overflow", "XSS attack"],
                    "correct": 1,
                    "explanation": "certutil.exe (certificate utility) can download files, making it useful for malware deployment."
                }
            ]
        }
    ],
    "blue_team": [
        {
            "title": "Threat Hunting Methodology",
            "subtitle": "Proactive adversary detection",
            "difficulty": 4,
            "order": 1,
            "concepts": ["Hypothesis-driven hunting", "IOC development", "Behavioral analysis", "Threat intelligence"],
            "quiz": [
                {
                    "q": "What is threat hunting?",
                    "opts": ["Reactive incident response", "Proactive search for hidden threats", "Installing antivirus", "Patching systems"],
                    "correct": 1,
                    "explanation": "Threat hunting is proactively searching for threats that evaded automated detection systems."
                },
                {
                    "q": "What's the first step in threat hunting?",
                    "opts": ["Block all traffic", "Form a hypothesis based on threat intel", "Reimage all systems", "Update signatures"],
                    "correct": 1,
                    "explanation": "Effective threat hunting starts with a hypothesis (e.g., 'Are we vulnerable to Kerberoasting?')."
                },
                {
                    "q": "What differentiates hunting from monitoring?",
                    "opts": ["Hunting is automated", "Hunting is hypothesis-driven and iterative", "Hunting is slower", "Hunting requires no tools"],
                    "correct": 1,
                    "explanation": "Hunting is an active, hypothesis-driven process, while monitoring is passive alert-based detection."
                }
            ],
            "hunting_playbook": {
                "scenario": "Hunt for Kerberoasting activity in enterprise environment",
                "hypothesis": "Adversaries may be extracting service account TGS tickets for offline cracking",
                "data_sources": [
                    "Windows Event Logs (Security, System)",
                    "EDR telemetry",
                    "Network traffic captures",
                    "Authentication logs"
                ],
                "hunt_steps": [
                    "Identify baseline: normal TGS request patterns",
                    "Search for Event ID 4769 with RC4 encryption (downgrade)",
                    "Correlate multiple TGS requests from single account",
                    "Check for requests to high-value service accounts",
                    "Investigate anomalous requesting accounts"
                ],
                "detection_logic": [
                    "IF: >10 TGS requests in 5 minutes FROM: single account",
                    "IF: TGS request WITH: RC4 encryption (weak) FOR: service account",
                    "IF: TGS requests FOR: admin service accounts FROM: low-privilege user"
                ],
                "response_actions": [
                    "Isolate suspicious account",
                    "Rotate service account passwords",
                    "Review authentication logs for compromise",
                    "Create detection rule for future prevention"
                ]
            }
        },
        {
            "title": "EDR Detection Engineering",
            "subtitle": "Building custom detection rules",
            "difficulty": 4,
            "order": 2,
            "concepts": ["Detection logic", "False positive reduction", "SIEM rules", "Behavioral analytics"],
            "quiz": [
                {
                    "q": "What is detection engineering?",
                    "opts": ["Installing EDR", "Creating custom rules to detect specific threats", "Updating antivirus", "Network segmentation"],
                    "correct": 1,
                    "explanation": "Detection engineering involves creating custom detection logic tailored to your environment and threats."
                },
                {
                    "q": "What's the main challenge in detection engineering?",
                    "opts": ["Lack of tools", "Balancing detection coverage with false positive rates", "High cost", "Slow response"],
                    "correct": 1,
                    "explanation": "The key challenge is detecting real threats without overwhelming analysts with false positives."
                }
            ]
        },
        {
            "title": "Memory Forensics and Malware Detection",
            "subtitle": "Analyzing system memory for threats",
            "difficulty": 4,
            "order": 3,
            "concepts": ["Volatility framework", "Memory artifacts", "Rootkit detection", "Process analysis"],
            "quiz": [
                {
                    "q": "Why is memory forensics important?",
                    "opts": ["It's faster than disk analysis", "Malware often operates in memory only (fileless)", "It requires no tools", "It's easier than log analysis"],
                    "correct": 1,
                    "explanation": "Many advanced malware strains operate entirely in memory, leaving minimal disk artifacts."
                },
                {
                    "q": "What is Volatility?",
                    "opts": ["A malware strain", "Memory forensics framework", "Network scanner", "Log analyzer"],
                    "correct": 1,
                    "explanation": "Volatility is the leading open-source framework for analyzing memory dumps."
                }
            ]
        },
        {
            "title": "Deception Technology",
            "subtitle": "Using honeypots and deception for detection",
            "difficulty": 4,
            "order": 4,
            "concepts": ["Honeypots", "Honeytokens", "Canary files", "Deception strategy"],
            "quiz": [
                {
                    "q": "What is a honeypot?",
                    "opts": ["Antivirus software", "Decoy system to attract and detect attackers", "Firewall rule", "Backup system"],
                    "correct": 1,
                    "explanation": "A honeypot is a deliberately vulnerable system designed to detect and analyze attacker behavior."
                },
                {
                    "q": "What is a honeytoken?",
                    "opts": ["Authentication method", "Fake credential that alerts when used", "Encryption key", "Network protocol"],
                    "correct": 1,
                    "explanation": "Honeytokens are fake credentials that trigger alerts when used, indicating compromise."
                },
                {
                    "q": "Why use deception technology?",
                    "opts": ["It's cheaper than EDR", "It provides high-fidelity alerts with low false positives", "It requires no maintenance", "It blocks all attacks"],
                    "correct": 1,
                    "explanation": "Deception generates very high-fidelity alerts because legitimate users shouldn't trigger honeypots."
                }
            ]
        },
        {
            "title": "Advanced SIEM Use Cases",
            "subtitle": "Building correlation rules and dashboards",
            "difficulty": 4,
            "order": 5,
            "concepts": ["Log correlation", "Use case development", "Alert tuning", "Threat detection"],
            "quiz": [
                {
                    "q": "What is SIEM correlation?",
                    "opts": ["Log storage", "Combining multiple events to detect complex attacks", "Password management", "Network routing"],
                    "correct": 1,
                    "explanation": "Correlation combines events from multiple sources to detect attack patterns that single events wouldn't reveal."
                },
                {
                    "q": "What makes a good SIEM use case?",
                    "opts": ["Generates many alerts", "Detects real threats with low false positives", "Uses all data sources", "Runs very fast"],
                    "correct": 1,
                    "explanation": "Good use cases balance threat coverage with manageable false positive rates."
                }
            ]
        },
        {
            "title": "Incident Response Automation",
            "subtitle": "SOAR and playbook development",
            "difficulty": 4,
            "order": 6,
            "concepts": ["SOAR platforms", "Playbooks", "Automated response", "Orchestration"],
            "quiz": [
                {
                    "q": "What is SOAR?",
                    "opts": ["Antivirus software", "Security Orchestration, Automation, and Response", "Firewall type", "Log aggregator"],
                    "correct": 1,
                    "explanation": "SOAR platforms automate incident response tasks and orchestrate security tool workflows."
                },
                {
                    "q": "What should be automated in IR?",
                    "opts": ["All decisions", "Repetitive, time-consuming tasks like enrichment and containment", "Nothing - manual only", "Only alerting"],
                    "correct": 1,
                    "explanation": "Automate repetitive tasks (enrichment, initial containment) while keeping critical decisions manual."
                }
            ]
        }
    ],
    "dfir": [
        {
            "title": "Advanced Windows Forensics",
            "subtitle": "Deep dive into Windows artifacts",
            "difficulty": 4,
            "order": 4,
            "concepts": ["Registry forensics", "Prefetch analysis", "ShimCache", "Amcache", "SRUM"],
            "quiz": [
                {
                    "q": "What forensic artifact shows program execution?",
                    "opts": ["Event logs only", "Prefetch, ShimCache, and Amcache", "Registry only", "Network logs"],
                    "correct": 1,
                    "explanation": "Multiple artifacts track execution: Prefetch (last 128 runs), ShimCache (compatibility), Amcache (installation)."
                },
                {
                    "q": "What is SRUM?",
                    "opts": ["Malware type", "System Resource Usage Monitor - tracks app resource usage", "Firewall log", "Authentication protocol"],
                    "correct": 1,
                    "explanation": "SRUM tracks application resource usage including network activity over time."
                }
            ]
        },
        {
            "title": "Network Traffic Analysis",
            "subtitle": "Detecting threats in packet captures",
            "difficulty": 4,
            "order": 5,
            "concepts": ["Wireshark", "Protocol analysis", "C2 detection", "Exfiltration patterns"],
            "quiz": [
                {
                    "q": "What indicates potential C2 traffic?",
                    "opts": ["High bandwidth usage", "Regular beaconing patterns to external IPs", "HTTPS traffic only", "DNS queries"],
                    "correct": 1,
                    "explanation": "C2 traffic often shows regular beaconing patterns (periodic connections) to maintain communication."
                },
                {
                    "q": "How can you detect data exfiltration in PCAP?",
                    "opts": ["All HTTPS is suspicious", "Large outbound transfers to unusual destinations", "Any DNS queries", "ICMP traffic"],
                    "correct": 1,
                    "explanation": "Look for large outbound data transfers to unusual external destinations, especially outside business hours."
                }
            ]
        },
        {
            "title": "Timeline Analysis",
            "subtitle": "Reconstructing attack sequences",
            "difficulty": 4,
            "order": 6,
            "concepts": ["Super timeline", "Plaso", "Log2timeline", "Event correlation"],
            "quiz": [
                {
                    "q": "What is a super timeline?",
                    "opts": ["Fast analysis tool", "Comprehensive timeline from all available artifacts", "Network diagram", "Malware family"],
                    "correct": 1,
                    "explanation": "A super timeline combines ALL forensic artifacts (filesystem, registry, logs, etc.) into one chronological view."
                },
                {
                    "q": "Which tool creates super timelines?",
                    "opts": ["Wireshark", "Plaso/log2timeline", "nmap", "Burp Suite"],
                    "correct": 1,
                    "explanation": "Plaso (log2timeline) is the primary tool for creating comprehensive forensic timelines."
                }
            ]
        }
    ],
    "malware": [
        {
            "title": "Reverse Engineering Fundamentals",
            "subtitle": "Understanding malware through disassembly",
            "difficulty": 4,
            "order": 4,
            "concepts": ["Assembly language", "IDA Pro", "Ghidra", "Control flow analysis"],
            "quiz": [
                {
                    "q": "What is reverse engineering?",
                    "opts": ["Creating malware", "Analyzing compiled code to understand functionality", "Network scanning", "Password cracking"],
                    "correct": 1,
                    "explanation": "Reverse engineering involves analyzing compiled binaries to understand their behavior and logic."
                },
                {
                    "q": "Which tool is commonly used for disassembly?",
                    "opts": ["Wireshark", "IDA Pro or Ghidra", "Metasploit", "Burp Suite"],
                    "correct": 1,
                    "explanation": "IDA Pro and Ghidra are industry-standard disassemblers for reverse engineering."
                }
            ]
        },
        {
            "title": "Anti-Analysis Techniques",
            "subtitle": "How malware evades detection and analysis",
            "difficulty": 4,
            "order": 5,
            "concepts": ["Packing", "Obfuscation", "Anti-debugging", "VM detection"],
            "quiz": [
                {
                    "q": "What is packing?",
                    "opts": ["Compressing files", "Encrypting/compressing malware to hide code", "Archive creation", "Data backup"],
                    "correct": 1,
                    "explanation": "Packing encrypts or compresses malware code, which is decrypted at runtime to evade static analysis."
                },
                {
                    "q": "How does malware detect sandboxes?",
                    "opts": ["It can't", "Checks for VM artifacts, debugger presence, timing anomalies", "DNS queries", "File permissions"],
                    "correct": 1,
                    "explanation": "Malware checks for VM artifacts (VMware tools), debuggers, unusual timing, or common sandbox filenames."
                }
            ]
        },
        {
            "title": "Ransomware Analysis",
            "subtitle": "Understanding encryption-based extortion",
            "difficulty": 4,
            "order": 6,
            "concepts": ["Encryption methods", "Ransom notes", "Payment mechanisms", "Decryption possibilities"],
            "quiz": [
                {
                    "q": "How does modern ransomware typically work?",
                    "opts": ["Deletes files", "Encrypts files and demands payment", "Changes passwords only", "Floods network"],
                    "correct": 1,
                    "explanation": "Ransomware encrypts files using strong cryptography and demands payment (usually cryptocurrency) for decryption."
                },
                {
                    "q": "What is double extortion ransomware?",
                    "opts": ["Encrypts twice", "Encrypts AND threatens to leak stolen data", "Two payments required", "Targets two networks"],
                    "correct": 1,
                    "explanation": "Double extortion: encrypt data AND steal it, threatening public release if ransom isn't paid."
                }
            ]
        }
    ]
}


def generate_advanced_lesson_json(domain, lesson_data, lesson_num):
    """Generate complete advanced lesson JSON"""

    lesson_id = str(uuid4())

    content_blocks = []

    # Block 1: Mindset coach
    content_blocks.append({
        "block_id": str(uuid4()),
        "type": "explanation",
        "title": "Advanced Topic Ahead",
        "content": {
            "text": f"You're about to learn {lesson_data['title']}, an advanced technique used by real-world threat actors and security professionals. This knowledge is powerful and must be used ethically."
        },
        "simplified_explanation": "Think of this like learning advanced martial arts - powerful, but requires responsibility.",
        "memory_aids": [
            "🎯 Advanced level - requires prerequisite knowledge",
            "⚖️ Use ethically - authorized testing only"
        ],
        "real_world_connection": "This technique is actively used in real-world attacks and defenses.",
        "reflection_prompt": "How would you use this knowledge to improve security?",
        "is_interactive": False,
        "xp_reward": 0
    })

    # Block 2: Technical explanation
    content_blocks.append({
        "block_id": str(uuid4()),
        "type": "explanation",
        "title": lesson_data["title"],
        "content": {
            "text": f"This lesson covers: {', '.join(lesson_data['concepts'])}. These are advanced techniques requiring solid fundamentals."
        },
        "simplified_explanation": f"Core concept: {lesson_data['concepts'][0]} enables attackers (or defenders) to {lesson_data['subtitle'].lower()}.",
        "memory_aids": [
            f"💡 Key: {concept}" for concept in lesson_data['concepts'][:3]
        ],
        "real_world_connection": f"Real threat actors use {lesson_data['title']} daily in active campaigns.",
        "reflection_prompt": "What security controls could prevent or detect this technique?",
        "is_interactive": False,
        "xp_reward": 0
    })

    # Block 3: Attack simulation or hunting playbook (if present)
    if "attack_simulation" in lesson_data:
        sim = lesson_data["attack_simulation"]
        content_blocks.append({
            "block_id": str(uuid4()),
            "type": "simulation",
            "title": "Attack Simulation",
            "content": {
                "scenario": sim["scenario"],
                "steps": sim["steps"],
                "detection": sim.get("detection", [])
            },
            "simplified_explanation": "Follow this attack path step-by-step to understand the adversary perspective.",
            "memory_aids": [
                "🔴 Red Team: Offensive simulation",
                "🔵 Blue Team: Detection opportunities"
            ],
            "real_world_connection": "This exact attack path has been observed in real breaches.",
            "reflection_prompt": "How would you detect each step of this attack?",
            "is_interactive": True,
            "xp_reward": 50
        })

    if "attack_path" in lesson_data:
        path = lesson_data["attack_path"]
        content_blocks.append({
            "block_id": str(uuid4()),
            "type": "simulation",
            "title": "APT Attack Path",
            "content": {
                "scenario": path["scenario"],
                "phases": path["phases"],
                "detection": path.get("detection_opportunities", [])
            },
            "simplified_explanation": "Understand how advanced threat actors conduct multi-stage operations.",
            "memory_aids": [
                "🎯 APT = Advanced Persistent Threat",
                "📊 Multi-stage attack chain",
                "🔍 Detection at each stage"
            ],
            "real_world_connection": f"This attack pattern is documented in real {lesson_data['title']} operations.",
            "reflection_prompt": "Where are the best opportunities to disrupt this attack chain?",
            "is_interactive": True,
            "xp_reward": 50
        })

    if "hunting_playbook" in lesson_data:
        hunt = lesson_data["hunting_playbook"]
        content_blocks.append({
            "block_id": str(uuid4()),
            "type": "simulation",
            "title": "Threat Hunting Playbook",
            "content": {
                "hypothesis": hunt["hypothesis"],
                "data_sources": hunt["data_sources"],
                "hunt_steps": hunt["hunt_steps"],
                "detection_logic": hunt.get("detection_logic", []),
                "response_actions": hunt.get("response_actions", [])
            },
            "simplified_explanation": "Use this structured approach to hunt for threats in your environment.",
            "memory_aids": [
                "🔍 Start with hypothesis",
                "📊 Query data sources",
                "✅ Validate findings",
                "🚨 Create detection rules"
            ],
            "real_world_connection": "SOC analysts use these exact hunting techniques daily.",
            "reflection_prompt": "What additional data sources would improve this hunt?",
            "is_interactive": True,
            "xp_reward": 50
        })

    # Block 4: MITRE ATT&CK mapping (if applicable)
    if "attack_path" in lesson_data and "phases" in lesson_data["attack_path"]:
        mitre_techniques = []
        for phase in lesson_data["attack_path"]["phases"]:
            if "mitre_tactics" in phase:
                mitre_techniques.extend(phase["mitre_tactics"])

        if mitre_techniques:
            content_blocks.append({
                "block_id": str(uuid4()),
                "type": "explanation",
                "title": "MITRE ATT&CK Mapping",
                "content": {
                    "text": f"This attack uses the following MITRE ATT&CK techniques: {', '.join(mitre_techniques)}"
                },
                "simplified_explanation": "MITRE ATT&CK provides a common language for describing adversary behavior.",
                "memory_aids": [
                    "🎯 MITRE ATT&CK = Adversary tactics and techniques",
                    "📚 Industry standard framework"
                ],
                "real_world_connection": "Security teams use ATT&CK to map detections and prioritize defenses.",
                "reflection_prompt": "Which of these techniques does your organization currently detect?",
                "is_interactive": False,
                "xp_reward": 0
            })

    return {
        "lesson_id": lesson_id,
        "domain": domain,
        "title": lesson_data["title"],
        "subtitle": lesson_data["subtitle"],
        "difficulty": lesson_data["difficulty"],
        "estimated_time": 30,
        "order_index": lesson_data["order"],
        "prerequisites": [],  # Empty for now - prerequisites handled by skill level system
        "learning_objectives": [
            f"Understand {concept}" for concept in lesson_data["concepts"][:4]
        ],
        "content_blocks": content_blocks,
        "pre_assessment": None,
        "post_assessment": [
            {
                "question_id": f"q{i+1}",
                "type": "multiple_choice",
                "question": q["q"],
                "options": q["opts"],
                "correct_answer": q["correct"],
                "explanation": q["explanation"],
                "difficulty": lesson_data["difficulty"],
                "memory_aid": f"Remember: {lesson_data['concepts'][0]}",
                "points": 15
            }
            for i, q in enumerate(lesson_data["quiz"])
        ],
        "mastery_threshold": 80,
        "jim_kwik_principles": [
            "active_learning",
            "teach_like_im_10",
            "memory_hooks",
            "connect_to_what_i_know",
            "meta_learning"
        ],
        "base_xp_reward": 150 * lesson_data["difficulty"],
        "badge_unlock": None,
        "is_core_concept": False,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "author": "CyberLearn Advanced Curriculum Team",
        "version": "1.0"
    }


def generate_all_advanced_lessons():
    """Generate all advanced lesson files"""

    print("=" * 70)
    print("Generating ADVANCED CyberLearn Lessons")
    print("=" * 70)
    print("⚠️  ADVANCED CONTENT - Requires prerequisite knowledge")
    print("⚖️  USE ETHICALLY - Authorized testing only")
    print("=" * 70)

    total = 0

    for domain, lessons in ADVANCED_CURRICULUM.items():
        print(f"\n📁 {domain.upper()}: {len(lessons)} advanced lessons")

        for idx, lesson_data in enumerate(lessons, 1):
            lesson_json = generate_advanced_lesson_json(domain, lesson_data, idx)

            # Use high order numbers to sort after basic lessons
            order_num = lesson_data["order"] + 50

            filename = f"content/lesson_{domain}_{order_num:02d}_{lesson_data['title'].replace(' ', '_').replace('(', '').replace(')', '').lower()}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(lesson_json, f, indent=2)

            print(f"  ✅ {lesson_data['title']} (Difficulty {lesson_data['difficulty']})")
            total += 1

    print("\n" + "=" * 70)
    print(f"✅ Generated {total} ADVANCED lessons")
    print("=" * 70)
    print("\n📊 Breakdown:")
    print(f"  • Active Directory: 5 advanced lessons (Kerberoasting, Golden Ticket, etc.)")
    print(f"  • Red Team: 5 lessons (APT29, APT28, Lazarus, C2, LOLBins)")
    print(f"  • Blue Team: 6 lessons (Threat Hunting, EDR, Memory Forensics, etc.)")
    print(f"  • DFIR: 3 advanced lessons (Windows artifacts, Network analysis, Timeline)")
    print(f"  • Malware: 3 lessons (Reverse engineering, Anti-analysis, Ransomware)")
    print(f"\n  TOTAL: {total} advanced lessons")
    print("\nNext steps:")
    print("1. Run: python load_all_lessons.py")
    print("2. Run: streamlit run app.py")
    print("3. Complete basic lessons to unlock advanced content!")
    print("\n⚠️  Remember: Use this knowledge ethically and only on authorized systems!")


if __name__ == "__main__":
    generate_all_advanced_lessons()
