"""
Populate assessment_questions table with diagnostic questions for all 15 domains

Question Distribution:
- Fundamentals: 7 questions (3 beginner, 2 intermediate, 2 advanced)
- DFIR: 7 questions (3 beginner, 2 intermediate, 2 advanced)
- Malware: 7 questions (2 beginner, 3 intermediate, 2 advanced)
- Active Directory: 7 questions (2 beginner, 3 intermediate, 2 advanced)
- System: 7 questions (2 beginner, 3 intermediate, 2 advanced)
- Cloud: 7 questions (2 beginner, 3 intermediate, 2 advanced)
- Pentest: 7 questions (2 beginner, 3 intermediate, 2 advanced)
- Red Team: 7 questions (1 beginner, 3 intermediate, 3 advanced)
- Blue Team: 7 questions (2 beginner, 3 intermediate, 2 advanced)
- OSINT: 5 questions (2 beginner, 2 intermediate, 1 advanced)
- Threat Hunting: 5 questions (1 beginner, 2 intermediate, 2 advanced)
- Linux: 5 questions (2 beginner, 2 intermediate, 1 advanced)
- AI Security: 5 questions (2 beginner, 2 intermediate, 1 advanced)
- IoT Security: 5 questions (2 beginner, 2 intermediate, 1 advanced)
- Web3 Security: 5 questions (2 beginner, 2 intermediate, 1 advanced)

Total: 90 questions
"""

import sqlite3
import json
import uuid
from datetime import datetime

# Assessment questions database
QUESTIONS = [
    # FUNDAMENTALS (7 questions)
    {
        "domain": "fundamentals",
        "difficulty": 1,
        "question_text": "What is the primary difference between symmetric and asymmetric encryption?",
        "options": [
            "Symmetric uses one key, asymmetric uses two keys (public and private)",
            "Symmetric is faster but less secure than asymmetric",
            "Symmetric is used for authentication, asymmetric for confidentiality",
            "There is no difference, they are interchangeable terms"
        ],
        "correct_answer": 0,
        "explanation": "Symmetric encryption uses a single shared key for both encryption and decryption, while asymmetric encryption uses a key pair: a public key for encryption and a private key for decryption."
    },
    {
        "domain": "fundamentals",
        "difficulty": 1,
        "question_text": "Which of the following is NOT part of the CIA triad in information security?",
        "options": [
            "Confidentiality",
            "Integrity",
            "Authenticity",
            "Availability"
        ],
        "correct_answer": 2,
        "explanation": "The CIA triad consists of Confidentiality, Integrity, and Availability. Authenticity is a related but separate security principle."
    },
    {
        "domain": "fundamentals",
        "difficulty": 1,
        "question_text": "What port does HTTPS typically use?",
        "options": [
            "80",
            "443",
            "8080",
            "22"
        ],
        "correct_answer": 1,
        "explanation": "HTTPS uses port 443 by default. Port 80 is for HTTP, 22 for SSH, and 8080 is an alternative HTTP port."
    },
    {
        "domain": "fundamentals",
        "difficulty": 2,
        "question_text": "In the context of authentication, what does MFA stand for and why is it important?",
        "options": [
            "Multi-Factor Authentication - combines something you know, have, and are for stronger security",
            "Main Frame Access - controls access to mainframe systems",
            "Managed File Access - secures file sharing",
            "Multiple Firewall Architecture - layers firewalls for defense"
        ],
        "correct_answer": 0,
        "explanation": "MFA (Multi-Factor Authentication) requires multiple forms of verification (knowledge, possession, inherence) to significantly improve security beyond passwords alone."
    },
    {
        "domain": "fundamentals",
        "difficulty": 2,
        "question_text": "What is the purpose of a Security Operations Center (SOC)?",
        "options": [
            "To develop new security products",
            "To monitor, detect, analyze, and respond to security incidents 24/7",
            "To conduct penetration tests on customer systems",
            "To manage physical security of data centers"
        ],
        "correct_answer": 1,
        "explanation": "A SOC is responsible for continuous monitoring and response to security threats, providing detection, analysis, and incident response capabilities."
    },
    {
        "domain": "fundamentals",
        "difficulty": 3,
        "question_text": "In a PKI (Public Key Infrastructure), what is the role of a Certificate Revocation List (CRL)?",
        "options": [
            "It lists all valid certificates currently in use",
            "It contains certificates that have been revoked before their expiration date",
            "It stores private keys for certificate authorities",
            "It defines which encryption algorithms are allowed"
        ],
        "correct_answer": 1,
        "explanation": "A CRL is published by a Certificate Authority and lists certificates that have been revoked (due to compromise, change of use, etc.) before their scheduled expiration."
    },
    {
        "domain": "fundamentals",
        "difficulty": 3,
        "question_text": "Which MITRE ATT&CK tactic describes adversaries trying to avoid being detected?",
        "options": [
            "Persistence",
            "Defense Evasion",
            "Privilege Escalation",
            "Command and Control"
        ],
        "correct_answer": 1,
        "explanation": "Defense Evasion is the tactic where adversaries use techniques to avoid detection and evade defensive measures like AV, EDR, and logging systems."
    },

    # DFIR (7 questions)
    {
        "domain": "dfir",
        "difficulty": 1,
        "question_text": "What is the primary purpose of maintaining chain of custody in digital forensics?",
        "options": [
            "To ensure evidence is admissible in court by documenting its handling",
            "To track the cost of forensic investigations",
            "To measure the performance of forensic analysts",
            "To encrypt evidence for secure storage"
        ],
        "correct_answer": 0,
        "explanation": "Chain of custody documents who handled evidence, when, and how, ensuring its integrity and admissibility in legal proceedings."
    },
    {
        "domain": "dfir",
        "difficulty": 1,
        "question_text": "Which Windows artifact stores recently accessed file and application shortcuts?",
        "options": [
            "Prefetch files",
            "Jump Lists",
            "Registry hives",
            "Event logs"
        ],
        "correct_answer": 1,
        "explanation": "Jump Lists (AutomaticDestinations and CustomDestinations) store recently accessed files and applications, useful for tracking user activity."
    },
    {
        "domain": "dfir",
        "difficulty": 1,
        "question_text": "What tool is commonly used for disk imaging in forensics?",
        "options": [
            "Wireshark",
            "FTK Imager",
            "Metasploit",
            "Burp Suite"
        ],
        "correct_answer": 1,
        "explanation": "FTK Imager is a popular forensic imaging tool that creates bit-for-bit copies of storage media while maintaining evidence integrity."
    },
    {
        "domain": "dfir",
        "difficulty": 2,
        "question_text": "Which Volatility plugin would you use to analyze network connections in a memory dump?",
        "options": [
            "pslist",
            "netscan",
            "malfind",
            "filescan"
        ],
        "correct_answer": 1,
        "explanation": "The netscan plugin in Volatility scans for network artifacts including TCP/UDP connections, listening sockets, and related information in memory dumps."
    },
    {
        "domain": "dfir",
        "difficulty": 2,
        "question_text": "What is the $MFT in NTFS forensics?",
        "options": [
            "A backup of deleted files",
            "The Master File Table containing metadata for all files and directories",
            "A hidden malware storage location",
            "A network traffic log"
        ],
        "correct_answer": 1,
        "explanation": "The Master File Table ($MFT) is the heart of NTFS, containing entries for every file and folder with metadata like timestamps, size, and location."
    },
    {
        "domain": "dfir",
        "difficulty": 3,
        "question_text": "In timeline analysis, what does the 'MACB' acronym represent?",
        "options": [
            "Modified, Accessed, Created, Born",
            "Malware Analysis Control Board",
            "Master Access Control Base",
            "Memory Artifact Collection Buffer"
        ],
        "correct_answer": 0,
        "explanation": "MACB timestamps represent Modified, Accessed, Changed (MFT), and Born (creation) times, critical for establishing file activity timelines in forensics."
    },
    {
        "domain": "dfir",
        "difficulty": 3,
        "question_text": "What forensic technique would you use to detect timestomping?",
        "options": [
            "Compare $STANDARD_INFORMATION with $FILE_NAME timestamps",
            "Check file hash against VirusTotal",
            "Analyze registry run keys",
            "Scan network traffic for anomalies"
        ],
        "correct_answer": 0,
        "explanation": "Timestomping can be detected by comparing $STANDARD_INFORMATION timestamps (easily modified) with $FILE_NAME timestamps (harder to modify) in NTFS."
    },

    # MALWARE (7 questions)
    {
        "domain": "malware",
        "difficulty": 1,
        "question_text": "What is the primary purpose of packing malware?",
        "options": [
            "To compress files to save storage space",
            "To obfuscate code and evade signature-based detection",
            "To improve malware performance",
            "To encrypt communications with C2 servers"
        ],
        "correct_answer": 1,
        "explanation": "Packing obfuscates malware code to evade antivirus signatures and make reverse engineering more difficult."
    },
    {
        "domain": "malware",
        "difficulty": 1,
        "question_text": "What is the difference between static and dynamic malware analysis?",
        "options": [
            "Static analysis runs malware in a sandbox, dynamic analysis examines code without execution",
            "Static analysis examines malware without execution, dynamic analysis runs it in a controlled environment",
            "Static analysis is for Windows malware, dynamic analysis is for Linux malware",
            "There is no difference, they are the same technique"
        ],
        "correct_answer": 1,
        "explanation": "Static analysis examines malware's code, strings, and structure without running it. Dynamic analysis executes malware in a safe environment to observe behavior."
    },
    {
        "domain": "malware",
        "difficulty": 2,
        "question_text": "Which tool is commonly used for interactive disassembly and debugging of malware?",
        "options": [
            "Wireshark",
            "IDA Pro / Ghidra",
            "Nmap",
            "Metasploit"
        ],
        "correct_answer": 1,
        "explanation": "IDA Pro and Ghidra are powerful disassemblers/debuggers used for reverse engineering malware and understanding its functionality."
    },
    {
        "domain": "malware",
        "difficulty": 2,
        "question_text": "What is a 'dropper' in malware terminology?",
        "options": [
            "A technique to delete log files",
            "Malware that delivers and installs additional malicious payloads",
            "A tool for removing malware infections",
            "A method to drop network connections"
        ],
        "correct_answer": 1,
        "explanation": "A dropper is malware designed to install (drop) additional malicious payloads onto a compromised system, often to evade detection."
    },
    {
        "domain": "malware",
        "difficulty": 2,
        "question_text": "What does API hooking allow malware to do?",
        "options": [
            "Intercept and modify system or application function calls",
            "Connect to the internet faster",
            "Bypass firewalls automatically",
            "Encrypt files for ransomware"
        ],
        "correct_answer": 0,
        "explanation": "API hooking lets malware intercept function calls to steal data, hide processes, or alter program behavior by redirecting API calls."
    },
    {
        "domain": "malware",
        "difficulty": 3,
        "question_text": "What technique do advanced malware families use to detect sandbox environments?",
        "options": [
            "Checking for specific VM artifacts like drivers, registry keys, or hardware identifiers",
            "Measuring internet connection speed",
            "Analyzing the color scheme of the operating system",
            "Counting the number of running processes"
        ],
        "correct_answer": 0,
        "explanation": "Malware detects sandboxes by looking for VM artifacts (VMware Tools, VirtualBox drivers, specific registry keys, limited RAM/CPU) and alters behavior to evade analysis."
    },
    {
        "domain": "malware",
        "difficulty": 3,
        "question_text": "What is process hollowing in the context of malware techniques?",
        "options": [
            "Injecting code into a suspended legitimate process to hide malicious execution",
            "Deleting system processes to crash the OS",
            "Creating empty processes to confuse analysts",
            "Extracting data from process memory"
        ],
        "correct_answer": 0,
        "explanation": "Process hollowing replaces the memory of a legitimate process with malicious code, making detection harder as the process appears legitimate."
    },

    # ACTIVE DIRECTORY (7 questions)
    {
        "domain": "active_directory",
        "difficulty": 1,
        "question_text": "What is the primary authentication protocol used in Active Directory?",
        "options": [
            "NTLM",
            "Kerberos",
            "OAuth",
            "SAML"
        ],
        "correct_answer": 1,
        "explanation": "Kerberos is the default authentication protocol in Active Directory, providing ticket-based authentication for secure network access."
    },
    {
        "domain": "active_directory",
        "difficulty": 1,
        "question_text": "What is a Domain Controller's primary role?",
        "options": [
            "Managing network routing and firewalls",
            "Storing user accounts and authenticating users in the domain",
            "Hosting web applications",
            "Monitoring network traffic"
        ],
        "correct_answer": 1,
        "explanation": "A Domain Controller authenticates users, manages Active Directory objects (users, groups, computers), and enforces security policies across the domain."
    },
    {
        "domain": "active_directory",
        "difficulty": 2,
        "question_text": "What authentication protocol does Kerberoasting exploit?",
        "options": [
            "NTLM",
            "Kerberos",
            "LDAP",
            "SMB"
        ],
        "correct_answer": 1,
        "explanation": "Kerberoasting exploits Kerberos by requesting service tickets (TGS) for service accounts, then cracking their encrypted hashes offline."
    },
    {
        "domain": "active_directory",
        "difficulty": 2,
        "question_text": "What is the purpose of Group Policy Objects (GPOs)?",
        "options": [
            "To manage user passwords",
            "To centrally configure and enforce settings across domain computers and users",
            "To backup Active Directory data",
            "To monitor network traffic"
        ],
        "correct_answer": 1,
        "explanation": "GPOs allow administrators to centrally manage and enforce configuration settings, security policies, and software deployment across AD domains."
    },
    {
        "domain": "active_directory",
        "difficulty": 2,
        "question_text": "What is a Golden Ticket attack in Active Directory?",
        "options": [
            "Stealing valid user credentials through phishing",
            "Forging a Kerberos TGT using the KRBTGT account hash to impersonate any user",
            "Brute-forcing domain admin passwords",
            "Exploiting a vulnerability in domain controllers"
        ],
        "correct_answer": 1,
        "explanation": "A Golden Ticket attack forges a Kerberos Ticket Granting Ticket (TGT) using the KRBTGT hash, allowing an attacker to impersonate any user with persistence."
    },
    {
        "domain": "active_directory",
        "difficulty": 3,
        "question_text": "What is DCSync and what permissions does it require?",
        "options": [
            "A tool to synchronize time across domain controllers, requires admin rights",
            "An attack that replicates AD data using Directory Replication permissions to extract credentials",
            "A method to backup domain controller data, requires backup operator rights",
            "A technique to crash domain controllers, requires no special permissions"
        ],
        "correct_answer": 1,
        "explanation": "DCSync abuses Directory Replication (DS-Replication-Get-Changes) rights to extract password hashes from domain controllers without running code on them."
    },
    {
        "domain": "active_directory",
        "difficulty": 3,
        "question_text": "How does NTLM relay attack work and why is it dangerous?",
        "options": [
            "It captures NTLM hashes from network traffic and relays them to authenticate to other services without cracking",
            "It brute-forces NTLM passwords locally",
            "It exploits a vulnerability in the NTLM protocol to gain admin access",
            "It converts NTLM hashes to Kerberos tickets"
        ],
        "correct_answer": 0,
        "explanation": "NTLM relay intercepts authentication attempts and forwards them to target systems, authenticating as the victim without knowing their password."
    },

    # SYSTEM (7 questions)
    {
        "domain": "system",
        "difficulty": 1,
        "question_text": "What is the Windows Registry?",
        "options": [
            "A backup system for files",
            "A hierarchical database storing system and application configuration data",
            "A list of installed software",
            "A network protocol"
        ],
        "correct_answer": 1,
        "explanation": "The Windows Registry is a centralized hierarchical database storing configuration settings, hardware information, and system state."
    },
    {
        "domain": "system",
        "difficulty": 1,
        "question_text": "In Linux, what directory contains system configuration files?",
        "options": [
            "/home",
            "/etc",
            "/var",
            "/bin"
        ],
        "correct_answer": 1,
        "explanation": "/etc contains system-wide configuration files in Linux. /home stores user data, /var stores variable data, /bin stores binaries."
    },
    {
        "domain": "system",
        "difficulty": 2,
        "question_text": "What is DLL hijacking?",
        "options": [
            "Stealing DLL files from the system",
            "Placing a malicious DLL in a location where an application will load it instead of the legitimate one",
            "Disabling DLL loading to prevent malware",
            "Encrypting DLL files for ransomware"
        ],
        "correct_answer": 1,
        "explanation": "DLL hijacking exploits the Windows DLL search order to load malicious DLLs by placing them in directories checked before the legitimate DLL location."
    },
    {
        "domain": "system",
        "difficulty": 2,
        "question_text": "What Windows feature allows applications to run with elevated privileges?",
        "options": [
            "User Account Control (UAC)",
            "Windows Defender",
            "Task Scheduler",
            "Event Viewer"
        ],
        "correct_answer": 0,
        "explanation": "UAC prompts users for elevation, allowing applications to run with administrative privileges while normally running with standard user rights."
    },
    {
        "domain": "system",
        "difficulty": 2,
        "question_text": "In Linux, what command shows which processes are listening on which ports?",
        "options": [
            "ps aux",
            "netstat -tulpn or ss -tulpn",
            "ls -la",
            "top"
        ],
        "correct_answer": 1,
        "explanation": "netstat -tulpn and ss -tulpn display listening ports with the associated process IDs and names, useful for security auditing."
    },
    {
        "domain": "system",
        "difficulty": 3,
        "question_text": "What is the purpose of Windows Alternate Data Streams (ADS)?",
        "options": [
            "A backup mechanism for files",
            "NTFS feature allowing multiple data streams per file, potentially used to hide data",
            "A network streaming protocol",
            "A method to compress files"
        ],
        "correct_answer": 1,
        "explanation": "ADS is an NTFS feature that allows additional data streams to be associated with files, which can be used to hide malicious code or data."
    },
    {
        "domain": "system",
        "difficulty": 3,
        "question_text": "What kernel-level technique allows malware to hide processes and files from system tools?",
        "options": [
            "Process hollowing",
            "Rootkit",
            "DLL injection",
            "API hooking"
        ],
        "correct_answer": 1,
        "explanation": "Rootkits operate at kernel level to hide malicious processes, files, network connections, and registry keys by hooking system calls."
    },

    # CLOUD (7 questions)
    {
        "domain": "cloud",
        "difficulty": 1,
        "question_text": "What does IAM stand for in cloud security?",
        "options": [
            "Internet Access Management",
            "Identity and Access Management",
            "Infrastructure Asset Monitoring",
            "Incident Analysis Method"
        ],
        "correct_answer": 1,
        "explanation": "IAM (Identity and Access Management) controls who can access what resources in cloud environments, managing users, roles, and permissions."
    },
    {
        "domain": "cloud",
        "difficulty": 1,
        "question_text": "Which AWS service is used for object storage?",
        "options": [
            "EC2",
            "S3",
            "Lambda",
            "RDS"
        ],
        "correct_answer": 1,
        "explanation": "Amazon S3 (Simple Storage Service) provides scalable object storage for files, backups, and static website content."
    },
    {
        "domain": "cloud",
        "difficulty": 2,
        "question_text": "What is the primary security concern with misconfigured S3 buckets?",
        "options": [
            "Slow performance",
            "High costs",
            "Public exposure of sensitive data",
            "Incompatibility with other services"
        ],
        "correct_answer": 2,
        "explanation": "Misconfigured S3 buckets with public read/write access have led to major data breaches, exposing sensitive data to the internet."
    },
    {
        "domain": "cloud",
        "difficulty": 2,
        "question_text": "What is the shared responsibility model in cloud security?",
        "options": [
            "Cloud provider and customer share the costs equally",
            "Cloud provider secures the infrastructure, customer secures their data and applications",
            "Only the cloud provider is responsible for all security",
            "Customers must implement all security controls themselves"
        ],
        "correct_answer": 1,
        "explanation": "In the shared responsibility model, cloud providers secure infrastructure (hardware, network), while customers secure their data, applications, and configurations."
    },
    {
        "domain": "cloud",
        "difficulty": 2,
        "question_text": "What is a VPC in cloud networking?",
        "options": [
            "Virtual Private Cloud - an isolated network environment within the cloud",
            "Verified Provider Certificate - for authenticating cloud services",
            "Volume Protection Control - for encrypting storage",
            "Virtual Processing Center - for managing compute resources"
        ],
        "correct_answer": 0,
        "explanation": "A VPC (Virtual Private Cloud) provides an isolated virtual network where you can launch cloud resources with custom IP ranges, subnets, and routing."
    },
    {
        "domain": "cloud",
        "difficulty": 3,
        "question_text": "What is privilege escalation via cloud metadata services?",
        "options": [
            "Exploiting misconfigured Instance Metadata Service (IMDS) to access IAM credentials from within an instance",
            "Hacking cloud admin accounts through phishing",
            "Brute-forcing cloud API keys",
            "Exploiting vulnerabilities in cloud control panels"
        ],
        "correct_answer": 0,
        "explanation": "IMDS privilege escalation occurs when attackers access cloud instance metadata (169.254.169.254) to steal IAM role credentials and escalate privileges."
    },
    {
        "domain": "cloud",
        "difficulty": 3,
        "question_text": "What is the security risk of serverless function over-privileging?",
        "options": [
            "Functions run too slowly",
            "Lambda/Cloud Functions with excessive IAM permissions can be exploited to access unintended resources",
            "Functions cost too much",
            "Functions cannot scale properly"
        ],
        "correct_answer": 1,
        "explanation": "Serverless functions should follow least privilege. Over-privileged functions can be exploited (via injection, misconfiguration) to access databases, storage, or other services."
    },

    # PENTEST (7 questions)
    {
        "domain": "pentest",
        "difficulty": 1,
        "question_text": "What is the first phase of a penetration test?",
        "options": [
            "Exploitation",
            "Reconnaissance",
            "Reporting",
            "Privilege escalation"
        ],
        "correct_answer": 1,
        "explanation": "Reconnaissance (information gathering) is the first phase where pentesters collect data about the target through passive and active methods."
    },
    {
        "domain": "pentest",
        "difficulty": 1,
        "question_text": "Which tool is commonly used for network scanning and service enumeration?",
        "options": [
            "Metasploit",
            "Nmap",
            "Burp Suite",
            "Wireshark"
        ],
        "correct_answer": 1,
        "explanation": "Nmap is the industry-standard tool for network discovery, port scanning, version detection, and OS fingerprinting during reconnaissance."
    },
    {
        "domain": "pentest",
        "difficulty": 2,
        "question_text": "What does OWASP stand for and what is it known for?",
        "options": [
            "Online Web Application Security Protocol - creates security standards",
            "Open Web Application Security Project - maintains Top 10 web vulnerabilities list",
            "Operational Wireless Access Security Platform - secures WiFi networks",
            "Official Web API Security Protocol - defines API security rules"
        ],
        "correct_answer": 1,
        "explanation": "OWASP (Open Web Application Security Project) maintains the OWASP Top 10, a widely-recognized list of critical web application security risks."
    },
    {
        "domain": "pentest",
        "difficulty": 2,
        "question_text": "What is the difference between authenticated and unauthenticated scanning?",
        "options": [
            "Authenticated scanning requires a valid certificate, unauthenticated does not",
            "Authenticated scanning uses provided credentials to scan from inside the system, revealing more vulnerabilities",
            "Authenticated scanning is slower than unauthenticated",
            "There is no difference in results"
        ],
        "correct_answer": 1,
        "explanation": "Authenticated scanning uses valid credentials to scan systems from an insider perspective, detecting more vulnerabilities like missing patches and misconfigurations."
    },
    {
        "domain": "pentest",
        "difficulty": 2,
        "question_text": "What is the purpose of the Metasploit Framework?",
        "options": [
            "To detect malware infections",
            "To develop, test, and execute exploits against target systems",
            "To monitor network traffic",
            "To create secure applications"
        ],
        "correct_answer": 1,
        "explanation": "Metasploit is an exploitation framework providing tools to develop, test, and execute exploits, used by both attackers and penetration testers."
    },
    {
        "domain": "pentest",
        "difficulty": 3,
        "question_text": "What is a buffer overflow and how is it exploited?",
        "options": [
            "Writing more data to a buffer than it can hold, potentially overwriting adjacent memory to inject malicious code",
            "Filling a network buffer to cause denial of service",
            "Overloading a server with too many requests",
            "Accessing files outside of intended directories"
        ],
        "correct_answer": 0,
        "explanation": "Buffer overflow vulnerabilities occur when more data is written to a buffer than allocated, allowing attackers to overwrite memory and potentially execute arbitrary code."
    },
    {
        "domain": "pentest",
        "difficulty": 3,
        "question_text": "What is pivoting in the context of penetration testing?",
        "options": [
            "Changing attack techniques when one fails",
            "Using a compromised system as a stepping stone to attack other systems on the internal network",
            "Rotating between different vulnerability scanners",
            "Switching between different exploit frameworks"
        ],
        "correct_answer": 1,
        "explanation": "Pivoting uses a compromised host as a proxy to access and attack other systems on the internal network that aren't directly accessible from the outside."
    },

    # RED TEAM (7 questions)
    {
        "domain": "red_team",
        "difficulty": 1,
        "question_text": "What is the primary goal of a red team engagement?",
        "options": [
            "To find as many vulnerabilities as possible",
            "To simulate real-world adversaries and test detection and response capabilities",
            "To conduct compliance audits",
            "To provide security awareness training"
        ],
        "correct_answer": 1,
        "explanation": "Red teams simulate sophisticated adversary tactics to test an organization's detection, response, and defense capabilities in realistic attack scenarios."
    },
    {
        "domain": "red_team",
        "difficulty": 2,
        "question_text": "What does C2 stand for in red team operations?",
        "options": [
            "Cloud Computing",
            "Command and Control",
            "Code Compliance",
            "Credential Capture"
        ],
        "correct_answer": 1,
        "explanation": "C2 (Command and Control) refers to infrastructure and communication channels used to control compromised systems and exfiltrate data."
    },
    {
        "domain": "red_team",
        "difficulty": 2,
        "question_text": "What is the main advantage of using domain fronting for C2 communication?",
        "options": [
            "It's faster than other methods",
            "It makes C2 traffic appear to come from legitimate high-reputation domains, evading detection",
            "It encrypts all traffic automatically",
            "It requires no infrastructure setup"
        ],
        "correct_answer": 1,
        "explanation": "Domain fronting disguises C2 traffic as connections to legitimate services (like CDNs), making it harder for security tools to block or detect malicious communications."
    },
    {
        "domain": "red_team",
        "difficulty": 2,
        "question_text": "What is OPSEC in red team operations?",
        "options": [
            "Operational Security - protecting sensitive operation details and tactics from being discovered by defenders",
            "Open Source Security - using public tools only",
            "Optional Security - security measures that can be skipped",
            "Operating System Security - hardening the OS"
        ],
        "correct_answer": 0,
        "explanation": "OPSEC (Operational Security) involves protecting operation details, TTPs, and indicators to avoid attribution and maintain stealth during engagements."
    },
    {
        "domain": "red_team",
        "difficulty": 3,
        "question_text": "What technique involves embedding malicious code in legitimate-looking documents?",
        "options": [
            "Process injection",
            "Macro-enabled phishing",
            "DLL hijacking",
            "API hooking"
        ],
        "correct_answer": 1,
        "explanation": "Macro-enabled phishing uses malicious VBA macros in Office documents that execute when victims enable macros, a common initial access technique."
    },
    {
        "domain": "red_team",
        "difficulty": 3,
        "question_text": "What is living off the land (LOLBins) in red team tactics?",
        "options": [
            "Using only physical access to compromise systems",
            "Using legitimate system tools (PowerShell, WMI, etc.) for malicious purposes to evade detection",
            "Conducting operations without network connectivity",
            "Using only open-source tools"
        ],
        "correct_answer": 1,
        "explanation": "Living off the land means using legitimate system binaries and tools for malicious actions, making detection harder as the tools are already trusted and whitelisted."
    },
    {
        "domain": "red_team",
        "difficulty": 3,
        "question_text": "What is credential stuffing and why is it effective?",
        "options": [
            "Brute-forcing passwords with random guesses",
            "Using stolen username/password pairs from breaches to access accounts across services where users reuse credentials",
            "Phishing users for their credentials",
            "Exploiting password reset mechanisms"
        ],
        "correct_answer": 1,
        "explanation": "Credential stuffing leverages password reuse by testing stolen credentials from one breach against other services, often achieving high success rates."
    },

    # BLUE TEAM (7 questions)
    {
        "domain": "blue_team",
        "difficulty": 1,
        "question_text": "What is the primary function of a SIEM (Security Information and Event Management) system?",
        "options": [
            "To block malware infections",
            "To aggregate, correlate, and analyze security logs from multiple sources to detect threats",
            "To encrypt sensitive data",
            "To manage user passwords"
        ],
        "correct_answer": 1,
        "explanation": "SIEM systems collect logs from various sources, correlate events, and provide real-time analysis and alerting for security incidents."
    },
    {
        "domain": "blue_team",
        "difficulty": 1,
        "question_text": "What does EDR stand for in cybersecurity?",
        "options": [
            "Endpoint Detection and Response",
            "External Data Repository",
            "Event Detection Record",
            "Encrypted Data Recovery"
        ],
        "correct_answer": 0,
        "explanation": "EDR (Endpoint Detection and Response) monitors endpoints for suspicious activity, provides detection capabilities, and enables rapid incident response."
    },
    {
        "domain": "blue_team",
        "difficulty": 2,
        "question_text": "What is the purpose of threat hunting?",
        "options": [
            "To wait for alerts from security tools",
            "To proactively search for threats that evaded existing detection mechanisms",
            "To conduct penetration tests",
            "To develop new security products"
        ],
        "correct_answer": 1,
        "explanation": "Threat hunting is proactive searching for adversaries who have bypassed automated defenses, using hypotheses and threat intelligence."
    },
    {
        "domain": "blue_team",
        "difficulty": 2,
        "question_text": "What is a false positive in security detection?",
        "options": [
            "An alert for malicious activity that is actually benign or legitimate behavior",
            "Missing a real attack completely",
            "An incorrect password entry",
            "A system misconfiguration"
        ],
        "correct_answer": 0,
        "explanation": "False positives are security alerts triggered by legitimate activity, creating alert fatigue and wasting analyst time if too frequent."
    },
    {
        "domain": "blue_team",
        "difficulty": 2,
        "question_text": "What is the Pyramid of Pain in threat intelligence?",
        "options": [
            "A ranking of security vulnerabilities by severity",
            "A model showing how difficult it is for adversaries when defenders block different indicator types",
            "The organizational structure of SOC teams",
            "A method for prioritizing incident response"
        ],
        "correct_answer": 1,
        "explanation": "The Pyramid of Pain ranks indicators (hash values, IPs, domains, TTPs) by how much pain/cost it causes adversaries when defenders detect and block them."
    },
    {
        "domain": "blue_team",
        "difficulty": 3,
        "question_text": "What is defense evasion and how do attackers achieve it?",
        "options": [
            "Bypassing physical security controls",
            "Using techniques like obfuscation, code signing, disabling logging to avoid detection by security tools",
            "Attacking from different countries",
            "Using encrypted communications only"
        ],
        "correct_answer": 1,
        "explanation": "Defense evasion uses various techniques (process injection, disabling AV/logs, obfuscation, living off the land) to avoid detection by security controls."
    },
    {
        "domain": "blue_team",
        "difficulty": 3,
        "question_text": "What is the difference between IOCs and TTPs in threat intelligence?",
        "options": [
            "IOCs are indicators of compromise (IPs, hashes, domains); TTPs are tactics, techniques, and procedures describing adversary behavior",
            "IOCs are used for attack, TTPs are used for defense",
            "IOCs relate to network security, TTPs relate to endpoint security",
            "There is no difference, they mean the same thing"
        ],
        "correct_answer": 0,
        "explanation": "IOCs are specific artifacts (IP addresses, file hashes); TTPs describe how adversaries operate. TTPs are harder for attackers to change, making them more valuable for detection."
    },

    # OSINT (5 questions)
    {
        "domain": "osint",
        "difficulty": 1,
        "question_text": "What does OSINT stand for?",
        "options": [
            "Online Security Intelligence Network",
            "Open Source Intelligence",
            "Operational System Integration",
            "Open System Information Network"
        ],
        "correct_answer": 1,
        "explanation": "OSINT (Open Source Intelligence) refers to collecting and analyzing publicly available information from various sources for intelligence purposes."
    },
    {
        "domain": "osint",
        "difficulty": 1,
        "question_text": "Which of these is a legitimate OSINT source?",
        "options": [
            "Social media profiles",
            "Hacked databases",
            "Stolen documents",
            "Intercepted private communications"
        ],
        "correct_answer": 0,
        "explanation": "OSINT uses only publicly available sources like social media, websites, public records, and news articles. Hacked or stolen data is not OSINT."
    },
    {
        "domain": "osint",
        "difficulty": 2,
        "question_text": "What is Google dorking?",
        "options": [
            "Using advanced Google search operators to find specific information or vulnerabilities",
            "A type of social engineering attack via Google",
            "Google's internal security scanning tool",
            "A method to hack Google accounts"
        ],
        "correct_answer": 0,
        "explanation": "Google dorking uses advanced search operators (site:, filetype:, inurl:) to find sensitive information, exposed files, or vulnerable systems indexed by Google."
    },
    {
        "domain": "osint",
        "difficulty": 2,
        "question_text": "What tool is commonly used for reverse image searches in OSINT?",
        "options": [
            "Shodan",
            "Maltego",
            "TinEye / Google Images",
            "Recon-ng"
        ],
        "correct_answer": 2,
        "explanation": "TinEye and Google Reverse Image Search help trace image origins, find similar images, and identify people or locations from photos."
    },
    {
        "domain": "osint",
        "difficulty": 3,
        "question_text": "What is Shodan and how is it used in OSINT?",
        "options": [
            "A social media monitoring tool",
            "A search engine for internet-connected devices, revealing exposed services and vulnerabilities",
            "An email intelligence platform",
            "A dark web search engine"
        ],
        "correct_answer": 1,
        "explanation": "Shodan indexes internet-connected devices (IoT, servers, cameras), allowing OSINT practitioners to find exposed systems, services, and potential vulnerabilities."
    },

    # THREAT HUNTING (5 questions)
    {
        "domain": "threat_hunting",
        "difficulty": 1,
        "question_text": "What is the primary difference between threat hunting and traditional security monitoring?",
        "options": [
            "Threat hunting is reactive, monitoring is proactive",
            "Threat hunting is proactive hypothesis-driven searching, monitoring relies on automated alerts",
            "Threat hunting only looks at network traffic",
            "There is no difference"
        ],
        "correct_answer": 1,
        "explanation": "Threat hunting proactively searches for threats using hypotheses and threat intelligence, while traditional monitoring waits for automated alerts."
    },
    {
        "domain": "threat_hunting",
        "difficulty": 2,
        "question_text": "What is a threat hunting hypothesis?",
        "options": [
            "A random guess about security issues",
            "An educated assumption about how adversaries might operate in your environment",
            "A proven fact about attacker behavior",
            "A list of known malware signatures"
        ],
        "correct_answer": 1,
        "explanation": "A hunting hypothesis is an educated assumption based on threat intelligence, environmental knowledge, and attacker TTPs that guides proactive searching."
    },
    {
        "domain": "threat_hunting",
        "difficulty": 2,
        "question_text": "What is the role of MITRE ATT&CK in threat hunting?",
        "options": [
            "It's an antivirus engine",
            "It provides a framework of adversary tactics and techniques to guide hunting hypotheses",
            "It's a vulnerability scanner",
            "It's a log management tool"
        ],
        "correct_answer": 1,
        "explanation": "MITRE ATT&CK is a knowledge base of adversary tactics and techniques, providing structured guidance for developing threat hunting hypotheses and detection strategies."
    },
    {
        "domain": "threat_hunting",
        "difficulty": 3,
        "question_text": "What is behavioral analysis in threat hunting?",
        "options": [
            "Analyzing user psychology",
            "Looking for deviations from normal system and user behavior patterns to identify potential threats",
            "Studying malware source code",
            "Testing employee security awareness"
        ],
        "correct_answer": 1,
        "explanation": "Behavioral analysis establishes baselines of normal activity and hunts for anomalies that might indicate compromise, like unusual process executions or data transfers."
    },
    {
        "domain": "threat_hunting",
        "difficulty": 3,
        "question_text": "What is the difference between stack counting and frequency analysis in threat hunting?",
        "options": [
            "Stack counting groups similar events, frequency analysis looks at occurrence rates over time",
            "They are the same technique",
            "Stack counting is for network traffic, frequency is for logs",
            "Stack counting detects malware, frequency detects intrusions"
        ],
        "correct_answer": 0,
        "explanation": "Stack counting groups and counts similar events to find outliers. Frequency analysis examines how often events occur over time to spot anomalies."
    },

    # LINUX (5 questions)
    {
        "domain": "linux",
        "difficulty": 1,
        "question_text": "What Linux command is used to change file permissions?",
        "options": [
            "chown",
            "chmod",
            "chgrp",
            "chroot"
        ],
        "correct_answer": 1,
        "explanation": "chmod (change mode) modifies file permissions. chown changes ownership, chgrp changes group, chroot changes root directory."
    },
    {
        "domain": "linux",
        "difficulty": 1,
        "question_text": "Which directory contains user home directories in Linux?",
        "options": [
            "/usr",
            "/var",
            "/home",
            "/etc"
        ],
        "correct_answer": 2,
        "explanation": "/home contains user home directories. /usr has user programs, /var has variable data, /etc has configuration files."
    },
    {
        "domain": "linux",
        "difficulty": 2,
        "question_text": "What is the purpose of the sudo command?",
        "options": [
            "To shut down the system",
            "To execute commands with elevated (root) privileges",
            "To switch between users",
            "To schedule tasks"
        ],
        "correct_answer": 1,
        "explanation": "sudo (superuser do) allows permitted users to execute commands as root or another user with elevated privileges."
    },
    {
        "domain": "linux",
        "difficulty": 2,
        "question_text": "Where are system logs typically stored in Linux?",
        "options": [
            "/etc/logs",
            "/home/logs",
            "/var/log",
            "/usr/logs"
        ],
        "correct_answer": 2,
        "explanation": "/var/log stores system and application log files, critical for troubleshooting and security monitoring."
    },
    {
        "domain": "linux",
        "difficulty": 3,
        "question_text": "What is a Linux rootkit and how does it hide itself?",
        "options": [
            "A tool to repair root filesystem damage",
            "Malicious software that operates at kernel level to hide processes, files, and connections by hooking system calls",
            "A root password cracking tool",
            "A backup utility for root directories"
        ],
        "correct_answer": 1,
        "explanation": "A rootkit hides malicious presence by intercepting system calls at kernel level, making processes, files, and network connections invisible to detection tools."
    },

    # AI SECURITY (5 questions)
    {
        "domain": "ai_security",
        "difficulty": 1,
        "question_text": "What is prompt injection in the context of LLM security?",
        "options": [
            "Injecting malicious code into AI training data",
            "Crafting inputs to make an LLM bypass safety controls or produce unintended outputs",
            "Hacking AI model parameters",
            "Stealing AI model weights"
        ],
        "correct_answer": 1,
        "explanation": "Prompt injection manipulates LLM inputs to override instructions, bypass filters, or cause the model to generate harmful content or leak sensitive data."
    },
    {
        "domain": "ai_security",
        "difficulty": 1,
        "question_text": "What is model poisoning in machine learning?",
        "options": [
            "Corrupting AI model files",
            "Injecting malicious data into training datasets to compromise model behavior",
            "Overloading models with too much data",
            "Encrypting AI models for ransomware"
        ],
        "correct_answer": 1,
        "explanation": "Model poisoning injects malicious or biased data into training sets to make the model produce incorrect or harmful outputs during inference."
    },
    {
        "domain": "ai_security",
        "difficulty": 2,
        "question_text": "What is the OWASP LLM Top 10?",
        "options": [
            "A list of the best LLM models",
            "A ranking of critical security risks specific to Large Language Model applications",
            "Top 10 LLM providers by security",
            "A list of LLM training datasets"
        ],
        "correct_answer": 1,
        "explanation": "OWASP LLM Top 10 identifies the most critical security risks for LLM applications, including prompt injection, insecure output handling, and model theft."
    },
    {
        "domain": "ai_security",
        "difficulty": 2,
        "question_text": "What is an adversarial example in AI/ML security?",
        "options": [
            "A competing AI model",
            "Specially crafted inputs designed to fool machine learning models into making incorrect predictions",
            "A malicious training dataset",
            "An AI model trained by attackers"
        ],
        "correct_answer": 1,
        "explanation": "Adversarial examples are inputs with imperceptible modifications that cause ML models to misclassify (e.g., stop sign seen as speed limit sign)."
    },
    {
        "domain": "ai_security",
        "difficulty": 3,
        "question_text": "What is model extraction/stealing and why is it concerning?",
        "options": [
            "Copying AI model files from servers",
            "Querying a model to reverse-engineer and replicate it, stealing IP and enabling adversarial attacks",
            "Extracting features from training data",
            "Removing AI models from production"
        ],
        "correct_answer": 1,
        "explanation": "Model extraction uses API queries to reverse-engineer proprietary models, stealing intellectual property and enabling attackers to craft better adversarial attacks."
    },

    # IOT SECURITY (5 questions)
    {
        "domain": "iot_security",
        "difficulty": 1,
        "question_text": "What does IoT stand for?",
        "options": [
            "Internet of Things",
            "Integration of Technology",
            "Internal Operating Terminal",
            "International Online Transmission"
        ],
        "correct_answer": 0,
        "explanation": "IoT (Internet of Things) refers to interconnected physical devices (sensors, cameras, appliances) that communicate over networks."
    },
    {
        "domain": "iot_security",
        "difficulty": 1,
        "question_text": "What is a common security issue with IoT devices?",
        "options": [
            "Too much encryption",
            "Hardcoded default credentials that users don't change",
            "Too many security updates",
            "Overly complex authentication"
        ],
        "correct_answer": 1,
        "explanation": "Many IoT devices ship with default credentials (admin/admin) that users never change, making them easily compromisable."
    },
    {
        "domain": "iot_security",
        "difficulty": 2,
        "question_text": "What is firmware analysis in IoT security?",
        "options": [
            "Testing network connectivity",
            "Examining IoT device firmware for vulnerabilities, hardcoded secrets, and backdoors",
            "Updating device software",
            "Monitoring device performance"
        ],
        "correct_answer": 1,
        "explanation": "Firmware analysis involves extracting and examining IoT firmware to find security flaws, hardcoded credentials, backdoors, and vulnerable components."
    },
    {
        "domain": "iot_security",
        "difficulty": 2,
        "question_text": "What protocol is commonly used for IoT device communication?",
        "options": [
            "HTTP only",
            "MQTT (Message Queuing Telemetry Transport)",
            "FTP",
            "SMTP"
        ],
        "correct_answer": 1,
        "explanation": "MQTT is a lightweight publish-subscribe protocol widely used for IoT device communication, especially in constrained environments."
    },
    {
        "domain": "iot_security",
        "difficulty": 3,
        "question_text": "What is a botnet in the context of IoT security?",
        "options": [
            "A network of legitimate IoT devices working together",
            "A network of compromised IoT devices controlled by attackers for DDoS or other attacks",
            "An IoT device management platform",
            "A protocol for IoT communication"
        ],
        "correct_answer": 1,
        "explanation": "IoT botnets (like Mirai) consist of compromised devices controlled by attackers to launch massive DDoS attacks, often exploiting weak credentials."
    },

    # WEB3 SECURITY (5 questions)
    {
        "domain": "web3_security",
        "difficulty": 1,
        "question_text": "What is a smart contract in blockchain technology?",
        "options": [
            "A legal document stored on blockchain",
            "Self-executing code that runs on blockchain when conditions are met",
            "A type of cryptocurrency wallet",
            "A blockchain mining algorithm"
        ],
        "correct_answer": 1,
        "explanation": "Smart contracts are programs that automatically execute on blockchain when predefined conditions are met, enabling decentralized applications."
    },
    {
        "domain": "web3_security",
        "difficulty": 1,
        "question_text": "What is a cryptocurrency wallet's private key?",
        "options": [
            "Your wallet's public address",
            "The secret key that controls access to your cryptocurrency assets",
            "Your password for cryptocurrency exchanges",
            "A backup code for recovery"
        ],
        "correct_answer": 1,
        "explanation": "A private key is the cryptographic secret that proves ownership of cryptocurrency. Losing it means losing access; exposing it means theft."
    },
    {
        "domain": "web3_security",
        "difficulty": 2,
        "question_text": "What is a reentrancy attack in smart contract security?",
        "options": [
            "Attempting to log into a wallet multiple times",
            "Exploiting a smart contract by recursively calling a function before the previous execution completes, draining funds",
            "Replaying old transactions",
            "Trying different private keys to access wallets"
        ],
        "correct_answer": 1,
        "explanation": "Reentrancy attacks exploit smart contracts by making recursive calls to withdraw functions, allowing attackers to drain funds before balances update."
    },
    {
        "domain": "web3_security",
        "difficulty": 2,
        "question_text": "What is a rug pull in DeFi (Decentralized Finance)?",
        "options": [
            "A legitimate liquidation of positions",
            "A scam where developers abandon a project and steal investor funds",
            "A security feature to protect users",
            "A method to improve blockchain performance"
        ],
        "correct_answer": 1,
        "explanation": "A rug pull is a scam where developers create a token/project, attract investment, then drain liquidity or sell holdings, leaving investors with worthless tokens."
    },
    {
        "domain": "web3_security",
        "difficulty": 3,
        "question_text": "What is a 51% attack on blockchain networks?",
        "options": [
            "Stealing 51% of a network's cryptocurrency",
            "Controlling majority of network's mining/validation power to manipulate transactions or double-spend",
            "Hacking 51% of wallet addresses",
            "A type of phishing targeting half of users"
        ],
        "correct_answer": 1,
        "explanation": "A 51% attack occurs when an entity controls majority of a blockchain's computing power, enabling transaction reversal, double-spending, and network manipulation."
    },
]

def populate_questions(db_path: str = "cyberlearn.db"):
    """Populate assessment_questions table"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("POPULATING ASSESSMENT QUESTIONS")
    print("=" * 60)

    added_count = 0

    for q in QUESTIONS:
        question_id = str(uuid.uuid4())

        # Convert options list to JSON string
        options_json = json.dumps(q["options"]) if "options" in q else None

        cursor.execute('''
            INSERT INTO assessment_questions (
                question_id, domain, difficulty, question_text,
                question_type, options, correct_answer, explanation, skill_weight
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            question_id,
            q["domain"],
            q["difficulty"],
            q["question_text"],
            "multiple_choice",
            options_json,
            q["correct_answer"],
            q["explanation"],
            1  # Default weight
        ))

        added_count += 1

    conn.commit()

    # Print summary
    cursor.execute('''
        SELECT domain, COUNT(*) as count
        FROM assessment_questions
        GROUP BY domain
        ORDER BY domain
    ''')

    print(f"\n[OK] Added {added_count} questions\n")
    print("Questions by domain:")
    for row in cursor.fetchall():
        domain, count = row
        cursor.execute('''
            SELECT difficulty, COUNT(*) as count
            FROM assessment_questions
            WHERE domain = ?
            GROUP BY difficulty
            ORDER BY difficulty
        ''', (domain,))

        difficulty_dist = cursor.fetchall()
        beginner = next((c for d, c in difficulty_dist if d == 1), 0)
        intermediate = next((c for d, c in difficulty_dist if d == 2), 0)
        advanced = next((c for d, c in difficulty_dist if d == 3), 0)

        print(f"  {domain:20s}: {count:2d} (B:{beginner} I:{intermediate} A:{advanced})")

    print("\n" + "=" * 60)
    print("[SUCCESS] Assessment questions populated")
    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    populate_questions()
