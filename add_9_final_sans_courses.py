#!/usr/bin/env python3
"""
Add 9 final SANS courses - 90 key lessons covering:
SEC588, SEC617, SEC599, SEC598, SEC660, SEC670, SEC699, FOR578, FOR610
"""

import csv
from pathlib import Path

csv_path = Path("lesson_ideas.csv")

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

last_lesson_num = max(int(row['lesson_number']) for row in rows)
next_lesson_num = last_lesson_num + 1

print(f"Starting from lesson {next_lesson_num}")

domain_order = {}
for row in rows:
    domain = row['domain']
    order_idx = int(row['order_index'])
    domain_order[domain] = max(domain_order.get(domain, 0), order_idx)

for d in domain_order:
    domain_order[d] += 1

all_lessons = []

# SEC588: Cloud Pentesting (10 lessons)
all_lessons.extend([
    {'domain': 'cloud', 'difficulty': 3, 'title': 'Cloud Penetration Testing Methodology', 'module': 'SEC588 S1', 'topics': 'Cloud pentesting approach, scoping cloud tests, architecture assessment, attack surface mapping', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security, Career Path: Pentester', 'notes': 'SEC588 S1'},
    {'domain': 'cloud', 'difficulty': 2, 'title': 'External Cloud Attack Surface Discovery', 'module': 'SEC588 S1', 'topics': 'Asset discovery pipeline, cloud enumeration, reconnaissance at scale, shadow IT discovery', 'prerequisites': '["Cloud Penetration Testing Methodology"]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security', 'notes': 'SEC588 S1'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'Attacking Microsoft Entra ID', 'module': 'SEC588 S2', 'topics': 'Entra ID attacks, authentication bypass, malicious app consents, Microsoft Graph exploitation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security, Career Path: Pentester', 'notes': 'SEC588 S2'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'AWS IAM Privilege Escalation', 'module': 'SEC588 S3', 'topics': 'AWS privilege escalation, IAM exploitation, AssumeRole attacks, confused deputy', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security', 'notes': 'SEC588 S3'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'Azure Compute Exploitation', 'module': 'SEC588 S3', 'topics': 'Azure VM attacks, code execution, managed VM abuse, Azure compute security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security', 'notes': 'SEC588 S3'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'Attacking Cloud-Native Applications', 'module': 'SEC588 S4', 'topics': 'Cloud app security, API attacks, serverless exploitation, web vulnerabilities in cloud', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security, Career Path: Pentester', 'notes': 'SEC588 S4'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'CI/CD Pipeline Attacks', 'module': 'SEC588 S4', 'topics': 'CI/CD hijacking, Terraform attacks, pipeline security, IaC exploitation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security', 'notes': 'SEC588 S4'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'Container Breakout Techniques', 'module': 'SEC588 S5', 'topics': 'Docker breakout, container escape, container vulnerabilities, runtime exploitation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security', 'notes': 'SEC588 S5'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'Kubernetes Penetration Testing', 'module': 'SEC588 S5', 'topics': 'K8s assessment, pod security, RBAC bypass, K8s privilege escalation, persistence', 'prerequisites': '["Container Breakout Techniques"]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security', 'notes': 'SEC588 S5'},
    {'domain': 'cloud', 'difficulty': 3, 'title': 'Red Team Operations in Cloud', 'module': 'SEC588 S5', 'topics': 'Cloud red teaming, C2 in cloud, persistence, lateral movement, backdooring workloads', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC588, Career Path: Cloud Security, Career Path: Red Teamer', 'notes': 'SEC588 S5'},
])

# SEC617: Wireless Pentesting (10 lessons)
all_lessons.extend([
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Wi-Fi Protocol Analysis and Packet Capture', 'module': 'SEC617 S1', 'topics': '802.11 analysis, packet capture, monitor mode, Kismet, RF mapping', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S1'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Rogue Access Point Detection', 'module': 'SEC617 S1', 'topics': 'Rogue AP identification, wireless threat assessment, unauthorized networks', 'prerequisites': '["Wi-Fi Protocol Analysis and Packet Capture"]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S1'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Client-Side Wi-Fi Attacks', 'module': 'SEC617 S2', 'topics': 'Client exploitation, evil twin, hotspot attacks, Wi-Fi DoS, fuzzing', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S2'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Attacking WEP Networks', 'module': 'SEC617 S2', 'topics': 'WEP vulnerabilities, WEP cracking, legacy wireless security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S2'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'WPA2/WPA3 Enterprise Network Attacks', 'module': 'SEC617 S3', 'topics': 'WPA2 enterprise bypass, WPA3 attacks, EAP vulnerabilities, authentication bypass', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S3'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Bluetooth Classic and BLE Exploitation', 'module': 'SEC617 S4', 'topics': 'Bluetooth attacks, BLE vulnerabilities, pairing bypass, service exploitation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S4'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Software Defined Radio (SDR) Attacks', 'module': 'SEC617 S4', 'topics': 'SDR techniques, RF analysis, proprietary protocol decoding, signal analysis', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S4'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'RFID and NFC Hacking', 'module': 'SEC617 S5', 'topics': 'RFID exploitation, NFC attacks, smart card reconnaissance, contactless security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S5'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Low/High-Frequency RFID Attacks', 'module': 'SEC617 S5', 'topics': 'LF/HF RFID, tag cloning, decoding, analysis, badge attacks', 'prerequisites': '["RFID and NFC Hacking"]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S5'},
    {'domain': 'pentest', 'difficulty': 2, 'title': 'Privacy Attacks: AirTag Spoofing', 'module': 'SEC617 S5', 'topics': 'Privacy attacks, tracking, AirTag spoofing, detection, Bluetooth tracking', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC617, Career Path: Pentester', 'notes': 'SEC617 S5'},
])

# SEC599: Defeating Advanced Adversaries (10 lessons)
all_lessons.extend([
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Extended Kill Chain and MITRE ATT&CK Integration', 'module': 'SEC599 S1', 'topics': 'Kill chain methodology, MITRE ATT&CK, purple team concepts, attack analysis', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer, Career Path: Threat Hunter', 'notes': 'SEC599 S1'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Attack Surface Mapping with BBOT', 'module': 'SEC599 S1', 'topics': 'Attack surface management, BBOT tool, surface mapping, vulnerability identification', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer', 'notes': 'SEC599 S1'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Blocking Phishing Payload Execution', 'module': 'SEC599 S2', 'topics': 'Phishing prevention, payload blocking, execution control, email security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer', 'notes': 'SEC599 S2'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Stopping NTLMv2 Relay Attacks', 'module': 'SEC599 S2', 'topics': 'NTLM relay prevention, authentication hardening, network security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer', 'notes': 'SEC599 S2'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Exploit Mitigation Using Compile-Time Controls', 'module': 'SEC599 S3', 'topics': 'Compile-time security, exploit mitigation, secure development, Exploit Guard', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer, Career Path: Security Engineer', 'notes': 'SEC599 S3'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Catching Persistence with Autoruns and Osquery', 'module': 'SEC599 S3', 'topics': 'Persistence detection, Autoruns, Osquery, endpoint monitoring', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer', 'notes': 'SEC599 S3'},
    {'domain': 'active_directory', 'difficulty': 2, 'title': 'Implementing LAPS for Credential Protection', 'module': 'SEC599 S4', 'topics': 'LAPS implementation, local admin passwords, credential protection, AD security', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer, Career Path: Security Engineer', 'notes': 'SEC599 S4'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Hardening Windows Against Credential Compromise', 'module': 'SEC599 S4', 'topics': 'Credential theft prevention, Windows hardening, LSA protection, Credential Guard', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer', 'notes': 'SEC599 S4'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Defending Against Ransomware', 'module': 'SEC599 S5', 'topics': 'Ransomware defense, detection, prevention, recovery, mitigation strategies', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Blue Teamer', 'notes': 'SEC599 S5'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Hunting with Velociraptor', 'module': 'SEC599 S5', 'topics': 'Velociraptor, endpoint hunting, artifact collection, at-scale hunting', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC599, Career Path: Threat Hunter', 'notes': 'SEC599 S5'},
])

# SEC598: AI Security Automation (10 lessons)
all_lessons.extend([
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Detection-as-Code with LLMs', 'module': 'SEC598 S1', 'topics': 'Detection engineering, LLM-assisted detection, GenAI for security, detection pipelines', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Blue Teamer, Career Path: AI Security', 'notes': 'SEC598 S1'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Security Automation with Ansible', 'module': 'SEC598 S1-2', 'topics': 'Ansible automation, OS hardening, configuration management, policy-as-code', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Blue Teamer, Career Path: Security Engineer', 'notes': 'SEC598 S1'},
    {'domain': 'cloud', 'difficulty': 2, 'title': 'Infrastructure as Code Security with Terraform', 'module': 'SEC598 S2', 'topics': 'Terraform automation, IaC security, cloud management, automated firing ranges', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Cloud Security, Career Path: Security Engineer', 'notes': 'SEC598 S2'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'SOAR Playbook Automation with Tines', 'module': 'SEC598 S2', 'topics': 'Tines SOAR, playbook automation, workflow orchestration, response automation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Blue Teamer, Career Path: SOC Analyst', 'notes': 'SEC598 S2'},
    {'domain': 'cloud', 'difficulty': 2, 'title': 'Cloud-Native Incident Response Automation', 'module': 'SEC598 S3', 'topics': 'Azure/AWS IR, automated response, cloud security automation, policy enforcement', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Cloud Security', 'notes': 'SEC598 S3'},
    {'domain': 'ai_security', 'difficulty': 3, 'title': 'Offensive AI Agents with CrewAI', 'module': 'SEC598 S4', 'topics': 'Red team AI agents, CrewAI, autonomous adversaries, agentic attacks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Red Teamer, Career Path: AI Security', 'notes': 'SEC598 S4'},
    {'domain': 'red_team', 'difficulty': 2, 'title': 'Adversary Emulation with Caldera', 'module': 'SEC598 S4', 'topics': 'Caldera framework, breach exercises, automated adversary emulation, ATT&CK', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Red Teamer', 'notes': 'SEC598 S4'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'AI-Augmented Incident Response Playbooks', 'module': 'SEC598 S5', 'topics': 'AI-infused IR, modular playbooks, LLM-powered response, automated triage', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Blue Teamer, Career Path: AI Security', 'notes': 'SEC598 S5'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Automated Triage with Velociraptor and Timesketch', 'module': 'SEC598 S5', 'topics': 'Automated analysis, Velociraptor, Timesketch, timeline analysis, artifact collection', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Blue Teamer', 'notes': 'SEC598 S5'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Continuous Purple Teaming with Automation', 'module': 'SEC598 All', 'topics': 'Purple team automation, continuous testing, detection validation, adversary emulation as code', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC598, Career Path: Blue Teamer, Career Path: Red Teamer', 'notes': 'SEC598'},
])

# SEC660: Advanced Pentesting (6 lessons)
all_lessons.extend([
    {'domain': 'pentest', 'difficulty': 3, 'title': 'Network Access Control Evasion', 'module': 'SEC660 S1', 'topics': 'NAC bypass, 802.1X evasion, captive portal bypass, network access', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC660, Career Path: Pentester', 'notes': 'SEC660 S1'},
    {'domain': 'pentest', 'difficulty': 3, 'title': 'Advanced IPv6 Attacks', 'module': 'SEC660 S1', 'topics': 'IPv6 exploitation, dual-stack attacks, IPv6 security implications, router attacks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC660, Career Path: Pentester', 'notes': 'SEC660 S1'},
    {'domain': 'pentest', 'difficulty': 3, 'title': 'Cryptographic Implementation Testing', 'module': 'SEC660 S2', 'topics': 'Crypto exploitation, CBC bitflipping, hash extension, implementation flaws', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC660, Career Path: Pentester', 'notes': 'SEC660 S2'},
    {'domain': 'pentest', 'difficulty': 3, 'title': 'Protocol Fuzzing and Code Coverage', 'module': 'SEC660 S3', 'topics': 'Fuzzing techniques, AFL++, protocol state manipulation, code coverage, binary instrumentation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC660, Career Path: Pentester', 'notes': 'SEC660 S3'},
    {'domain': 'pentest', 'difficulty': 3, 'title': 'Linux Buffer Overflow Exploitation', 'module': 'SEC660 S4', 'topics': 'Stack exploitation, return-to-libc, ROP, ASLR bypass, 64-bit exploitation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC660, Career Path: Pentester', 'notes': 'SEC660 S4'},
    {'domain': 'pentest', 'difficulty': 3, 'title': 'Windows Exploit Development', 'module': 'SEC660 S5', 'topics': 'Windows exploitation, SafeSEH bypass, ROP chains, DEP mitigation, shellcode', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC660, Career Path: Pentester', 'notes': 'SEC660 S5'},
])

# SEC670: Red Team Tools (8 lessons)
all_lessons.extend([
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Windows Offensive Tool Development', 'module': 'SEC670 S1', 'topics': 'Windows internals, tool development, Win32 API, offensive programming', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S1'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'PE Format and Custom Win32 API', 'module': 'SEC670 S3', 'topics': 'PE headers, Win32 API creation, process injection, DLL injection', 'prerequisites': '["Windows Offensive Tool Development"]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S3'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Advanced Process Injection Techniques', 'module': 'SEC670 S3', 'topics': 'Process injection, thread injection, reflective DLL, code injection', 'prerequisites': '["PE Format and Custom Win32 API"]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S3'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Token Stealing and Privilege Escalation', 'module': 'SEC670 S3', 'topics': 'Token manipulation, privilege escalation, impersonation, access tokens', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S3'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Binary Patching for Persistence', 'module': 'SEC670 S4', 'topics': 'Binary patching, in-memory execution, registry persistence, service manipulation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S4'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Shellcode Execution and Injection', 'module': 'SEC670 S5', 'topics': 'Shellcode generation, local/remote execution, payload injection, position-independent code', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S5'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Antivirus Bypass Techniques', 'module': 'SEC670 S5', 'topics': 'AV evasion, signature bypass, behavioral bypass, obfuscation', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S5'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Building Custom C2 Communication', 'module': 'SEC670 S5', 'topics': 'C2 development, command execution, hook manipulation, covert channels', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC670, Career Path: Red Teamer', 'notes': 'SEC670 S5'},
])

# SEC699: Purple Teaming (8 lessons)
all_lessons.extend([
    {'domain': 'blue_team', 'difficulty': 3, 'title': 'Purple Team Infrastructure with VECTR', 'module': 'SEC699 S1', 'topics': 'VECTR platform, purple team tooling, Elastic/SIGMA stack, Prelude Operator', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Blue Teamer, Career Path: Red Teamer', 'notes': 'SEC699 S1'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'VBA Stomping and AMSI Bypasses', 'module': 'SEC699 S2', 'topics': 'VBA stomping, AMSI bypass, endpoint evasion, macro attacks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Red Teamer', 'notes': 'SEC699 S2'},
    {'domain': 'blue_team', 'difficulty': 2, 'title': 'Attack Surface Reduction and ASR Bypass', 'module': 'SEC699 S2', 'topics': 'ASR rules, ASR bypass, attack surface reduction, endpoint protection', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Blue Teamer', 'notes': 'SEC699 S2'},
    {'domain': 'active_directory', 'difficulty': 3, 'title': 'Active Directory Certificate Services (ADCS) Attacks', 'module': 'SEC699 S3', 'topics': 'ADCS exploitation, certificate abuse, ESC attacks, certificate-based attacks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Red Teamer, Career Path: Pentester', 'notes': 'SEC699 S3'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'NTLMv1 Downgrade Attacks', 'module': 'SEC699 S3', 'topics': 'NTLM downgrade, authentication attacks, relay attacks, credential theft', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Red Teamer', 'notes': 'SEC699 S3'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'COM Object Hijacking for Persistence', 'module': 'SEC699 S4', 'topics': 'COM hijacking, WMI persistence, advanced persistence, stealthy access', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Red Teamer', 'notes': 'SEC699 S4'},
    {'domain': 'red_team', 'difficulty': 3, 'title': 'Cross-Domain and Forest Pivoting', 'module': 'SEC699 S4', 'topics': 'Domain pivoting, forest pivoting, AD trust abuse, cross-boundary attacks', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Red Teamer', 'notes': 'SEC699 S4'},
    {'domain': 'blue_team', 'difficulty': 3, 'title': 'Threat Actor Emulation Plans', 'module': 'SEC699 S5', 'topics': 'APT emulation, threat actor techniques, emulation planning, purple team exercises', 'prerequisites': '[]', 'tags': 'Course: SANS-SEC699, Career Path: Blue Teamer, Career Path: Red Teamer', 'notes': 'SEC699 S5'},
])

# FOR578: Cyber Threat Intelligence (8 lessons)
all_lessons.extend([
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Intelligence Cycle and Analytical Techniques', 'module': 'FOR578 S1', 'topics': 'Intelligence cycle, tradecraft, structured analysis, analytical techniques', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter, Career Path: Blue Teamer', 'notes': 'FOR578 S1'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Threat Modeling and Risk Assessment', 'module': 'FOR578 S1', 'topics': 'Strategic threat modeling, risk assessment, threat actors, threat intelligence levels', 'prerequisites': '["Intelligence Cycle and Analytical Techniques"]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter', 'notes': 'FOR578 S1'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Intrusion Analysis and Kill Chain', 'module': 'FOR578 S2', 'topics': 'Multi-phase intrusions, kill chain analysis, pivoting techniques, indicator collection', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter, Career Path: DFIR Specialist', 'notes': 'FOR578 S2'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Domain Intelligence and Pivoting', 'module': 'FOR578 S3', 'topics': 'Domain analysis, OSINT pivoting, DomainTools, Maltego, malware analysis for CTI', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter, Career Path: OSINT', 'notes': 'FOR578 S3'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Storing Threat Data in MISP', 'module': 'FOR578 S4', 'topics': 'MISP platform, threat data structuring, information sharing, CTI platforms', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter', 'notes': 'FOR578 S4'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'Analysis of Competing Hypotheses', 'module': 'FOR578 S4', 'topics': 'ACH methodology, cognitive biases, logical fallacies, analytical rigor', 'prerequisites': '["Intelligence Cycle and Analytical Techniques"]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter', 'notes': 'FOR578 S4'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'YARA Rules for Tactical Intelligence', 'module': 'FOR578 S5', 'topics': 'YARA development, IOC generation, signature creation, tactical dissemination', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter, Career Path: Malware Analyst', 'notes': 'FOR578 S5'},
    {'domain': 'threat_hunting', 'difficulty': 2, 'title': 'STIX and Campaign Attribution', 'module': 'FOR578 S5', 'topics': 'STIX format, threat intelligence sharing, campaign analysis, attribution techniques', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR578, Career Path: Threat Hunter', 'notes': 'FOR578 S5'},
])

# FOR610: Malware RE (6 lessons)
all_lessons.extend([
    {'domain': 'malware', 'difficulty': 2, 'title': 'Malware Behavioral Analysis', 'module': 'FOR610 S1', 'topics': 'Behavioral analysis, dynamic analysis, sandbox analysis, malware execution monitoring', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR610, Career Path: Malware Analyst', 'notes': 'FOR610 S1'},
    {'domain': 'malware', 'difficulty': 3, 'title': 'x86/x64 Assembly for Malware Analysis', 'module': 'FOR610 S2', 'topics': 'Assembly concepts, disassembly, control flow, API analysis, Ghidra', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR610, Career Path: Malware Analyst', 'notes': 'FOR610 S2'},
    {'domain': 'malware', 'difficulty': 2, 'title': 'Malicious Document Analysis', 'module': 'FOR610 S3', 'topics': 'PDF analysis, VBA macros, RTF files, shellcode, JavaScript deobfuscation', 'prerequisites': '[]', 'tags': 'Course: SANS-FOR610, Career Path: Malware Analyst', 'notes': 'FOR610 S3'},
    {'domain': 'malware', 'difficulty': 3, 'title': 'Unpacking Malware', 'module': 'FOR610 S4', 'topics': 'Packed malware, unpacking techniques, memory dumping, .NET analysis', 'prerequisites': '["x86/x64 Assembly for Malware Analysis"]', 'tags': 'Course: SANS-FOR610, Career Path: Malware Analyst', 'notes': 'FOR610 S4'},
    {'domain': 'malware', 'difficulty': 3, 'title': 'Anti-Analysis Techniques', 'module': 'FOR610 S5', 'topics': 'Debugger detection, sandbox evasion, obfuscation, anti-forensics', 'prerequisites': '["Unpacking Malware"]', 'tags': 'Course: SANS-FOR610, Career Path: Malware Analyst', 'notes': 'FOR610 S5'},
    {'domain': 'malware', 'difficulty': 3, 'title': 'Bypassing Anti-Analysis Measures', 'module': 'FOR610 S5', 'topics': 'Patching malware, string deobfuscation, defeating protection, analysis evasion bypass', 'prerequisites': '["Anti-Analysis Techniques"]', 'tags': 'Course: SANS-FOR610, Career Path: Malware Analyst', 'notes': 'FOR610 S5'},
])

# Write all lessons
added_count = 0
domain_counts = {}
difficulty_counts = {1: 0, 2: 0, 3: 0}

for lesson in all_lessons:
    domain = lesson['domain']
    difficulty = lesson['difficulty']

    if domain not in domain_order:
        domain_order[domain] = 1
    order_idx = domain_order[domain]
    domain_order[domain] += 1

    domain_counts[domain] = domain_counts.get(domain, 0) + 1
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

# Write CSV
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['lesson_number', 'order_index', 'domain', 'difficulty', 'title',
                 'module', 'topics', 'prerequisites', 'status', 'tags', 'notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\n{'=' * 80}")
print(f"SUCCESS - Added {added_count} lessons from 9 SANS courses")
print(f"Total lessons: {len(rows)}")
print(f"{'=' * 80}\n")

print("Difficulty Distribution:")
for diff, count in difficulty_counts.items():
    print(f"  {['Beginner', 'Intermediate', 'Advanced'][diff-1]}: {count}")

print(f"\nDomains:")
for domain in sorted(domain_counts.keys()):
    print(f"  {domain}: {domain_counts[domain]} lessons")
