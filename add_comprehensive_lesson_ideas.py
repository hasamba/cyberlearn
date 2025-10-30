"""
Add comprehensive lesson ideas to lesson_ideas.csv
Includes Red Team, Pentest, Malware, AD, Linux, Fundamentals, Blue Team, OSINT, and Emerging Tech
"""
import csv
import os

def add_lesson_ideas():
    csv_file = "lesson_ideas.csv"

    # Check if file exists to determine starting lesson_number
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            last_lesson_number = max(int(row['lesson_number']) for row in rows)
            current_lesson_number = last_lesson_number + 1
    else:
        current_lesson_number = 1

    # New lesson ideas organized by domain
    new_lessons = []

    # RED TEAM ADVANCED OPERATIONS (7 lessons, order_index 57-63)
    red_team_lessons = [
        {
            'order_index': 57,
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Command and Control Infrastructure Setup',
            'module': 'Module 4: C2 Operations',
            'topics': 'C2 framework selection (Covenant, Sliver, Havoc), infrastructure setup, redirectors, listener configuration, OPSEC considerations, egress testing',
            'prerequisites': '[1,2,3,4,5,6]',
            'course_tag': '',
            'notes': 'Focus on modern C2 frameworks post-Cobalt Strike era'
        },
        {
            'order_index': 58,
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Domain Fronting and CDN-Based C2',
            'module': 'Module 4: C2 Operations',
            'topics': 'Domain fronting concepts, CloudFront/Azure CDN abuse, legitimate service abuse (Slack, Discord, OneDrive), traffic profile mimicking, detection challenges',
            'prerequisites': '[57]',
            'course_tag': '',
            'notes': 'Advanced C2 infrastructure techniques'
        },
        {
            'order_index': 59,
            'domain': 'red_team',
            'difficulty': 2,
            'title': 'Living Off the Land Binaries and Scripts',
            'module': 'Module 5: Evasion Techniques',
            'topics': 'LOLBins/LOLBAs concepts, LOLBAS project, legitimate Windows binaries for exploitation, fileless malware, application whitelisting bypass',
            'prerequisites': '[3,4]',
            'course_tag': '',
            'notes': 'Critical for AV/EDR evasion'
        },
        {
            'order_index': 60,
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Advanced Process Injection Techniques',
            'module': 'Module 5: Evasion Techniques',
            'topics': 'Process injection taxonomy, classic DLL injection, APC injection, thread hijacking, process hollowing, atom bombing, reflective DLL injection, detection and defense',
            'prerequisites': '[59]',
            'course_tag': '',
            'notes': 'Deep dive into injection methods'
        },
        {
            'order_index': 61,
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Anti-Forensics and Log Evasion',
            'module': 'Module 5: Evasion Techniques',
            'topics': 'Event log clearing and manipulation, timestomping, disabling logging, ETW patching, Sysmon evasion, covering tracks, anti-forensic tools',
            'prerequisites': '[4,5]',
            'course_tag': '',
            'notes': 'Operational security and cleanup'
        },
        {
            'order_index': 62,
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Red Team Operations Planning and Execution',
            'module': 'Module 6: Operations Management',
            'topics': 'Red team vs pentest differences, CONOPS development, Rules of Engagement (ROE), deconfliction procedures, documentation, final report writing',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'Operational planning and management'
        },
        {
            'order_index': 63,
            'domain': 'red_team',
            'difficulty': 3,
            'title': 'Adversary Simulation and Emulation Frameworks',
            'module': 'Module 6: Operations Management',
            'topics': 'MITRE CALDERA, Atomic Red Team, Purple Team exercises, adversary emulation plans, APT simulation, detection validation',
            'prerequisites': '[62]',
            'course_tag': '',
            'notes': 'Purple team collaboration and testing'
        }
    ]

    # PENTEST WEB APPLICATION SECURITY (6 lessons, order_index 31-36)
    pentest_lessons = [
        {
            'order_index': 31,
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'GraphQL Security Testing',
            'module': 'Module 3: Web Application Testing',
            'topics': 'GraphQL fundamentals, introspection queries, batching attacks, nested query DoS, authorization bypass, information disclosure, GraphQL security tools',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'Modern API technology'
        },
        {
            'order_index': 32,
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'REST API Penetration Testing',
            'module': 'Module 3: Web Application Testing',
            'topics': 'REST API architecture, authentication flaws (API keys, JWT), rate limiting bypass, mass assignment, BOLA/BFLA, excessive data exposure, Postman/Burp for API testing',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'OWASP API Security Top 10'
        },
        {
            'order_index': 33,
            'domain': 'pentest',
            'difficulty': 3,
            'title': 'JWT and OAuth Security Testing',
            'module': 'Module 3: Web Application Testing',
            'topics': 'JWT structure and vulnerabilities, algorithm confusion, none algorithm attack, OAuth 2.0 flows, scope abuse, redirect URI validation, PKCE, token theft',
            'prerequisites': '[32]',
            'course_tag': '',
            'notes': 'Authentication and authorization testing'
        },
        {
            'order_index': 34,
            'domain': 'pentest',
            'difficulty': 2,
            'title': 'Modern JavaScript Framework Security',
            'module': 'Module 3: Web Application Testing',
            'topics': 'React XSS (dangerouslySetInnerHTML), Vue.js security, Angular template injection, client-side routing bypass, JavaScript prototype pollution',
            'prerequisites': '[3]',
            'course_tag': '',
            'notes': 'Frontend framework vulnerabilities'
        },
        {
            'order_index': 35,
            'domain': 'pentest',
            'difficulty': 3,
            'title': 'Serverless Application Security Testing',
            'module': 'Module 4: Cloud Application Testing',
            'topics': 'AWS Lambda security, function injection, event data manipulation, excessive permissions, secrets in environment variables, serverless SSRF, cold start attacks',
            'prerequisites': '[1,2]',
            'course_tag': '',
            'notes': 'Cloud-native application testing'
        },
        {
            'order_index': 36,
            'domain': 'pentest',
            'difficulty': 3,
            'title': 'Container and Kubernetes Penetration Testing',
            'module': 'Module 4: Cloud Application Testing',
            'topics': 'Docker API exposure, container escape, Kubernetes API testing, RBAC misconfigurations, secrets extraction, pod security policies, admission controller bypass',
            'prerequisites': '[1,2]',
            'course_tag': '',
            'notes': 'Container orchestration security'
        }
    ]

    # MALWARE ADVANCED TOPICS (5 lessons, order_index 16-20)
    malware_lessons = [
        {
            'order_index': 16,
            'domain': 'malware',
            'difficulty': 3,
            'title': 'Ransomware Internals and Analysis',
            'module': 'Module 3: Specialized Malware',
            'topics': 'Ransomware kill chain, encryption schemes (AES, RSA), ransom note analysis, RaaS (Ransomware as a Service), LockBit, BlackCat analysis, recovery techniques',
            'prerequisites': '[1,2,3,4,5]',
            'course_tag': '',
            'notes': 'Critical threat landscape topic'
        },
        {
            'order_index': 17,
            'domain': 'malware',
            'difficulty': 3,
            'title': 'APT Malware Case Studies',
            'module': 'Module 3: Specialized Malware',
            'topics': 'Lazarus Group toolsets, APT29 (Cozy Bear), FIN7 malware, state-sponsored malware characteristics, custom C2 protocols, attribution indicators',
            'prerequisites': '[16]',
            'course_tag': '',
            'notes': 'Nation-state threat actors'
        },
        {
            'order_index': 18,
            'domain': 'malware',
            'difficulty': 3,
            'title': 'Mobile Malware Analysis',
            'module': 'Module 3: Specialized Malware',
            'topics': 'Android APK analysis, APK unpacking and decompilation, iOS malware (jailbreak-based), mobile C2, SMS trojans, banking trojans, jadx and MobSF tools',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'Mobile threat analysis'
        },
        {
            'order_index': 19,
            'domain': 'malware',
            'difficulty': 3,
            'title': 'macOS Malware Analysis',
            'module': 'Module 3: Specialized Malware',
            'topics': 'Mach-O file format, macOS malware landscape, XProtect bypass, Gatekeeper bypass, macOS persistence mechanisms, analyzing .dmg and .pkg installers',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'macOS-specific malware'
        },
        {
            'order_index': 20,
            'domain': 'malware',
            'difficulty': 2,
            'title': 'Malware Sandboxing and Automated Analysis',
            'module': 'Module 4: Analysis Automation',
            'topics': 'Cuckoo Sandbox setup and configuration, CAPE Sandbox, Joe Sandbox, automated behavioral analysis, report interpretation, evasion detection, YARA integration',
            'prerequisites': '[1,2]',
            'course_tag': '',
            'notes': 'Automation and scalability'
        }
    ]

    # ACTIVE DIRECTORY ADVANCED (8 lessons, order_index 59-66)
    ad_lessons = [
        {
            'order_index': 59,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'Azure AD and Hybrid Identity Attacks',
            'module': 'Module 4: Cloud AD',
            'topics': 'Azure AD fundamentals, Pass-the-PRT attacks, OAuth token theft, conditional access bypass, Azure AD Connect exploitation, hybrid identity attacks',
            'prerequisites': '[1,2,3,4,5]',
            'course_tag': '',
            'notes': 'Modern cloud-integrated AD attacks'
        },
        {
            'order_index': 60,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'AD CS Template Abuse and ESC Vulnerabilities',
            'module': 'Module 5: Advanced Exploitation',
            'topics': 'Certificate Services exploitation, ESC1-ESC8 vulnerabilities, certificate template abuse, Certipy tool, privilege escalation via certificates',
            'prerequisites': '[8]',
            'course_tag': '',
            'notes': 'Certificate Services attacks'
        },
        {
            'order_index': 61,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'NTLM Relay and Coercion Attacks',
            'module': 'Module 5: Advanced Exploitation',
            'topics': 'NTLM relay fundamentals, PetitPotam, PrinterBug, DFSCoerce, ShadowCoerce, relay to LDAP/SMB/HTTP, mitigation and detection',
            'prerequisites': '[4,5]',
            'course_tag': '',
            'notes': 'Coercion and relay techniques'
        },
        {
            'order_index': 62,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'Shadow Credentials and Key Trust Attacks',
            'module': 'Module 5: Advanced Exploitation',
            'topics': 'Shadow Credentials attack, KeyList attribute abuse, PKINIT authentication, Whisker tool, certificate-based authentication exploitation',
            'prerequisites': '[60]',
            'course_tag': '',
            'notes': 'Advanced certificate attacks'
        },
        {
            'order_index': 63,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'Active Directory Federation Services Attacks',
            'module': 'Module 5: Advanced Exploitation',
            'topics': 'AD FS architecture, Golden SAML attacks, token signing certificate theft, federation trust abuse, Azure AD integration attacks',
            'prerequisites': '[59]',
            'course_tag': '',
            'notes': 'Federation services exploitation'
        },
        {
            'order_index': 64,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'LAPS and Credential Guard Bypass',
            'module': 'Module 5: Advanced Exploitation',
            'topics': 'LAPS architecture and bypass techniques, Credential Guard overview, credential dumping with protections enabled, alternative credential sources',
            'prerequisites': '[4,5]',
            'course_tag': '',
            'notes': 'Bypassing modern defenses'
        },
        {
            'order_index': 65,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'Domain Dominance and Advanced Persistence',
            'module': 'Module 6: Persistence',
            'topics': 'DCShadow for stealthy replication, AdminSDHolder abuse, Skeleton Key malware, DSRM password abuse, SID History injection',
            'prerequisites': '[1,2,3,4,5,6,7]',
            'course_tag': '',
            'notes': 'Advanced persistence mechanisms'
        },
        {
            'order_index': 66,
            'domain': 'active_directory',
            'difficulty': 3,
            'title': 'AD Recovery and Post-Breach Remediation',
            'module': 'Module 6: Persistence',
            'topics': 'Incident response in AD, removing persistence, credential rotation, detecting backdoors, forest recovery, lessons from real breaches',
            'prerequisites': '[65]',
            'course_tag': '',
            'notes': 'Defensive and recovery focus'
        }
    ]

    # LINUX SECURITY AND HARDENING (4 lessons, order_index 13-16)
    linux_lessons = [
        {
            'order_index': 13,
            'domain': 'linux',
            'difficulty': 2,
            'title': 'Linux Security Hardening',
            'module': 'Module 2: Security',
            'topics': 'SELinux policies and enforcement, AppArmor profiles, CIS benchmarks, kernel hardening (sysctl), secure boot, firewall configuration (iptables, nftables)',
            'prerequisites': '[1,2,3,4,5]',
            'course_tag': '',
            'notes': 'Defensive hardening techniques'
        },
        {
            'order_index': 14,
            'domain': 'linux',
            'difficulty': 3,
            'title': 'Docker and Container Security',
            'module': 'Module 3: Containers',
            'topics': 'Docker security best practices, image scanning (Trivy, Clair), runtime security (Falco), seccomp profiles, capability management, rootless containers',
            'prerequisites': '[13]',
            'course_tag': '',
            'notes': 'Container security focus'
        },
        {
            'order_index': 15,
            'domain': 'linux',
            'difficulty': 3,
            'title': 'Kubernetes Security Architecture',
            'module': 'Module 3: Containers',
            'topics': 'Kubernetes RBAC, pod security policies/standards, network policies, admission controllers, secrets management, service mesh security (Istio)',
            'prerequisites': '[14]',
            'course_tag': '',
            'notes': 'K8s security deep dive'
        },
        {
            'order_index': 16,
            'domain': 'linux',
            'difficulty': 3,
            'title': 'Linux Rootkit Detection and Analysis',
            'module': 'Module 4: Threat Detection',
            'topics': 'Kernel module rootkits, LD_PRELOAD rootkits, user-mode rootkits, detection with rkhunter/chkrootkit, memory analysis for rootkits, behavioral indicators',
            'prerequisites': '[1,13]',
            'course_tag': '',
            'notes': 'Advanced threat detection'
        }
    ]

    # FUNDAMENTALS - COMPLIANCE AND GRC (3 lessons, order_index 13-15)
    fundamentals_lessons = [
        {
            'order_index': 13,
            'domain': 'fundamentals',
            'difficulty': 1,
            'title': 'Security Compliance Frameworks Overview',
            'module': 'Module 3: Governance',
            'topics': 'ISO 27001/27002, SOC 2 Type I/II, PCI-DSS, HIPAA, GDPR, NIST frameworks, compliance vs security, audit preparation',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'Foundation for GRC career path'
        },
        {
            'order_index': 14,
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Risk Management and Assessment',
            'module': 'Module 3: Governance',
            'topics': 'Risk identification and analysis, quantitative vs qualitative risk assessment, risk treatment strategies, risk registers, business impact analysis (BIA)',
            'prerequisites': '[13]',
            'course_tag': '',
            'notes': 'Risk management fundamentals'
        },
        {
            'order_index': 15,
            'domain': 'fundamentals',
            'difficulty': 2,
            'title': 'Security Audit and Assessment Methodologies',
            'module': 'Module 3: Governance',
            'topics': 'Vulnerability assessment vs penetration testing, security control testing, evidence collection, audit documentation, remediation tracking',
            'prerequisites': '[13,14]',
            'course_tag': '',
            'notes': 'Audit and assessment skills'
        }
    ]

    # BLUE TEAM - DETECTION ENGINEERING (5 lessons, order_index 52-56)
    blue_team_lessons = [
        {
            'order_index': 52,
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Sigma Rule Development',
            'module': 'Module 4: Detection Engineering',
            'topics': 'Sigma rule format and structure, detection logic, field mappings, rule modifiers, conversion to SIEM queries, rule testing and validation',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'Universal detection rule format'
        },
        {
            'order_index': 53,
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'YARA Rule Creation for Defense',
            'module': 'Module 4: Detection Engineering',
            'topics': 'YARA syntax and rule structure, string patterns, conditions, malware detection rules, memory scanning, performance optimization, false positive reduction',
            'prerequisites': '[52]',
            'course_tag': '',
            'notes': 'Malware and IOC detection'
        },
        {
            'order_index': 54,
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Custom EDR Detection Development',
            'module': 'Module 4: Detection Engineering',
            'topics': 'Behavioral detections, telemetry analysis, EDR query languages, detection logic trees, combining multiple data sources, detection tuning',
            'prerequisites': '[52,6]',
            'course_tag': '',
            'notes': 'Advanced detection creation'
        },
        {
            'order_index': 55,
            'domain': 'blue_team',
            'difficulty': 3,
            'title': 'Detection Engineering Metrics and Testing',
            'module': 'Module 4: Detection Engineering',
            'topics': 'Detection coverage measurement, false positive rate, mean time to detect (MTTD), ATT&CK coverage mapping, A/B testing detections, detection validation',
            'prerequisites': '[54]',
            'course_tag': '',
            'notes': 'Measuring detection effectiveness'
        },
        {
            'order_index': 56,
            'domain': 'blue_team',
            'difficulty': 2,
            'title': 'Threat Intelligence for Detection',
            'module': 'Module 5: Threat Intelligence',
            'topics': 'IOC integration, TIP platforms (MISP, OpenCTI), threat intelligence enrichment, converting CTI to detections, intelligence-driven defense',
            'prerequisites': '[1,52]',
            'course_tag': '',
            'notes': 'CTI and detection integration'
        }
    ]

    # OSINT - THREAT INTEL INTEGRATION (5 lessons, order_index 16-20)
    osint_lessons = [
        {
            'order_index': 16,
            'domain': 'osint',
            'difficulty': 2,
            'title': 'Threat Intelligence Platforms',
            'module': 'Module 3: Threat Intelligence',
            'topics': 'TIP overview, MISP installation and usage, OpenCTI, ThreatConnect, IOC management, intelligence sharing communities, feed integration',
            'prerequisites': '[1,2,3]',
            'course_tag': '',
            'notes': 'TIP fundamentals'
        },
        {
            'order_index': 17,
            'domain': 'osint',
            'difficulty': 2,
            'title': 'STIX TAXII and Intelligence Sharing',
            'module': 'Module 3: Threat Intelligence',
            'topics': 'STIX format (observables, indicators, TTPs), TAXII protocol, intelligence sharing standards, creating STIX bundles, consuming threat feeds',
            'prerequisites': '[16]',
            'course_tag': '',
            'notes': 'Standardized threat intelligence'
        },
        {
            'order_index': 18,
            'domain': 'osint',
            'difficulty': 3,
            'title': 'Adversary Infrastructure Tracking',
            'module': 'Module 3: Threat Intelligence',
            'topics': 'Passive DNS analysis, certificate transparency logs, domain registration tracking, IP reputation, infrastructure pivoting, tools (SecurityTrails, Censys, Shodan)',
            'prerequisites': '[1,7]',
            'course_tag': '',
            'notes': 'Infrastructure intelligence'
        },
        {
            'order_index': 19,
            'domain': 'osint',
            'difficulty': 3,
            'title': 'Malware Intelligence and Campaign Tracking',
            'module': 'Module 3: Threat Intelligence',
            'topics': 'Malware family tracking, campaign attribution, C2 infrastructure mapping, malware configuration extraction, correlating attacks, threat actor profiling',
            'prerequisites': '[18,43]',
            'course_tag': '',
            'notes': 'Malware threat intelligence'
        },
        {
            'order_index': 20,
            'domain': 'osint',
            'difficulty': 3,
            'title': 'OSINT to Detection Pipeline',
            'module': 'Module 3: Threat Intelligence',
            'topics': 'Converting OSINT findings to IOCs, automating intelligence ingestion, enriching alerts with OSINT, intelligence-driven hunting, feedback loops',
            'prerequisites': '[16,17,18,19]',
            'course_tag': '',
            'notes': 'Operationalizing OSINT'
        }
    ]

    # EMERGING TECHNOLOGY TOPICS
    # AI/ML Security (3 lessons)
    ai_lessons = [
        {
            'order_index': 1,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'Machine Learning Security Fundamentals',
            'module': 'Module 1: AI/ML Security',
            'topics': 'ML pipeline security, adversarial ML overview, model poisoning, data poisoning, training data security, model theft',
            'prerequisites': '[]',
            'course_tag': '',
            'notes': 'New domain: AI/ML Security'
        },
        {
            'order_index': 2,
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'AI ML Model Attacks and Defense',
            'module': 'Module 1: AI/ML Security',
            'topics': 'Evasion attacks (FGSM, PGD), adversarial examples, backdoor attacks, model inversion, membership inference, defenses and robustness',
            'prerequisites': '[1]',
            'course_tag': '',
            'notes': 'Attack techniques on ML models'
        },
        {
            'order_index': 3,
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'LLM Security and Prompt Injection',
            'module': 'Module 1: AI/ML Security',
            'topics': 'OWASP LLM Top 10, prompt injection attacks, jailbreaking techniques, indirect prompt injection, data leakage, insecure plugins, supply chain risks',
            'prerequisites': '[1]',
            'course_tag': '',
            'notes': 'Large Language Model security'
        }
    ]

    # IoT and OT Security (4 lessons)
    iot_lessons = [
        {
            'order_index': 1,
            'domain': 'iot_security',
            'difficulty': 2,
            'title': 'IoT Security Fundamentals',
            'module': 'Module 1: IoT Security',
            'topics': 'IoT architecture, protocols (MQTT, CoAP, Zigbee), firmware analysis, hardware hacking basics, UART/JTAG debugging, IoT attack surface',
            'prerequisites': '[]',
            'course_tag': '',
            'notes': 'New domain: IoT/OT Security'
        },
        {
            'order_index': 2,
            'domain': 'iot_security',
            'difficulty': 3,
            'title': 'Industrial Control Systems Security',
            'module': 'Module 2: OT Security',
            'topics': 'ICS/SCADA architecture, Modbus protocol, S7comm (Siemens), DNP3, OT network segmentation, ICS vulnerabilities, Stuxnet case study',
            'prerequisites': '[1]',
            'course_tag': '',
            'notes': 'Critical infrastructure security'
        },
        {
            'order_index': 3,
            'domain': 'iot_security',
            'difficulty': 3,
            'title': 'OT Network Monitoring and Detection',
            'module': 'Module 2: OT Security',
            'topics': 'Zeek for ICS protocol analysis, anomaly detection in OT, passive monitoring, ICS honeypots, detecting unauthorized changes, safety system monitoring',
            'prerequisites': '[2]',
            'course_tag': '',
            'notes': 'Detection in OT environments'
        },
        {
            'order_index': 4,
            'domain': 'iot_security',
            'difficulty': 3,
            'title': 'IoT Penetration Testing',
            'module': 'Module 3: IoT Testing',
            'topics': 'Firmware extraction and analysis, hardware debugging interfaces, RF protocol analysis, mobile app testing, cloud API testing, IoT botnet analysis',
            'prerequisites': '[1]',
            'course_tag': '',
            'notes': 'Comprehensive IoT testing'
        }
    ]

    # Blockchain and Web3 Security (3 lessons)
    web3_lessons = [
        {
            'order_index': 1,
            'domain': 'web3_security',
            'difficulty': 3,
            'title': 'Smart Contract Security',
            'module': 'Module 1: Web3 Security',
            'topics': 'Solidity programming, reentrancy attacks, integer overflow/underflow, flash loan attacks, access control vulnerabilities, tools (Slither, Mythril, Echidna)',
            'prerequisites': '[]',
            'course_tag': '',
            'notes': 'New domain: Web3 Security'
        },
        {
            'order_index': 2,
            'domain': 'web3_security',
            'difficulty': 3,
            'title': 'DeFi Security and Exploit Analysis',
            'module': 'Module 1: Web3 Security',
            'topics': 'DeFi protocols overview, major hack case studies (DAO, Poly Network, Ronin Bridge), oracle manipulation, MEV attacks, rug pulls, security auditing',
            'prerequisites': '[1]',
            'course_tag': '',
            'notes': 'DeFi threat landscape'
        },
        {
            'order_index': 3,
            'domain': 'web3_security',
            'difficulty': 2,
            'title': 'NFT and Crypto Wallet Security',
            'module': 'Module 1: Web3 Security',
            'topics': 'Wallet types (hot vs cold), seed phrase security, phishing attacks, signature verification, hardware wallets, NFT marketplace scams, Web3 social engineering',
            'prerequisites': '[1]',
            'course_tag': '',
            'notes': 'User-facing Web3 security'
        }
    ]

    # Combine all lessons
    all_new_lessons = (
        red_team_lessons +
        pentest_lessons +
        malware_lessons +
        ad_lessons +
        linux_lessons +
        fundamentals_lessons +
        blue_team_lessons +
        osint_lessons +
        ai_lessons +
        iot_lessons +
        web3_lessons
    )

    # Add lesson_number and status to each
    for lesson in all_new_lessons:
        lesson['lesson_number'] = current_lesson_number
        lesson['status'] = 'not_started'
        current_lesson_number += 1

    # Append to CSV
    with open(csv_file, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['lesson_number', 'order_index', 'domain', 'difficulty', 'title',
                      'module', 'topics', 'prerequisites', 'status', 'course_tag', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        for lesson in all_new_lessons:
            writer.writerow(lesson)

    # Print summary
    print(f"[OK] Added {len(all_new_lessons)} new lesson ideas to {csv_file}")
    print("\nSummary by domain:")

    domain_counts = {}
    for lesson in all_new_lessons:
        domain = lesson['domain']
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain}: {count} lessons added")

    print("\nNew domains created:")
    print("  - ai_security (3 lessons)")
    print("  - iot_security (4 lessons)")
    print("  - web3_security (3 lessons)")

if __name__ == "__main__":
    add_lesson_ideas()
