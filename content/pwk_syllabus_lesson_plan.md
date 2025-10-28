# PWK Syllabus Lesson Plan (Filtered)

This plan maps the PEN-200 / PWK syllabus to new lesson content that is **not** already covered by existing CyberLearn lessons. Topics already addressed by current lessons were filtered out to avoid duplication.

## Summary of Existing Coverage (Filtered Out)

These syllabus topics map directly to existing CyberLearn lessons and were therefore omitted from the new plan:

- **CIA Triad** → "CIA Triad and Core Security Principles".
- **Penetration Testing Lifecycle** → "Penetration Testing Methodology".
- **Passive / Active Information Gathering** → "Passive OSINT & Target Profiling" and "Active Information Gathering".
- **Vulnerability Scanning Theory** → "Vulnerability Scanning Strategy & Analysis".
- **Web Application Methodology, Enumeration, and Common XSS/File Upload/Command Injection Attacks** → "Web Application Penetration Testing Fundamentals" and "Advanced Web Attacks: XSS, File Upload & Command Injection".
- **SQL Injection (manual/automated) and Public Exploits** → "SQL Injection: From Manual Exploitation to Automated Mastery" and "Public Exploits: Finding, Fixing & Executing".
- **Antivirus Evasion and Password / Privilege Escalation Basics** → "Antivirus and EDR Evasion Techniques", "Password Attacks and Credential Operations", "Windows Privilege Escalation Field Guide", and "Linux Privilege Escalation Playbook".
- **Port Forwarding & Advanced Tunneling** → "Port Forwarding & Pivoting Techniques".
- **Active Directory Enumeration, Attacks, and Persistence** → Active Directory lesson suite (Fundamentals through AD CS Exploitation).

## New Lesson Plan

### 1. Penetration Testing with Kali Linux: General Course Introduction
- **PWK Course Onboarding & Lab Setup** — Inventory course materials, build the Kali attacking VM, connect to PWK VPN, and walkthrough of module exercise workflows.
- **PWK Learning Strategy & Mindset** — Applying uncertainty-based learning models, understanding PEN-200 learning components, and strategies for deliberate practice.
- **PWK Module Roadmap Overview** — High-level briefing of each PWK learning module and how they connect throughout the course.

### 2. Introduction to Cybersecurity
- **The Practice of Cybersecurity Mindsets** — Challenges unique to information security, offensive vs. defensive parity, and cultivating resilient mindsets.
- **Threats and Threat Actor Landscape** — Taxonomy of threat actors, recent attack case studies, and differentiating risks, threats, vulnerabilities, and exploits.
- **Security Principles, Controls, and Strategies** — Defense-in-depth design, threat intelligence programs, least privilege enforcement, and security policy frameworks.
- **Cybersecurity Laws, Regulations, and Frameworks** — Overview of major regulations (GDPR, HIPAA, etc.), industry frameworks (NIST CSF, ISO 27001), and compliance considerations.
- **Career Pathways in Cybersecurity** — Survey of offensive, defensive, and governance career tracks plus skill development roadmaps.

### 3. Effective Learning Strategies
- **Learning Science for Technical Mastery** — Memory models, dual encoding, cognitive load, and retention challenges specific to cybersecurity.
- **Overcoming Technical Learning Obstacles** — Digital learning advantages, preparing for unknown scenarios, and strategies for remote/asynchronous study.
- **OffSec Demonstrative Methodology Deep Dive** — Applying OffSec’s demonstrative methodology to prepare for novel offensive tasks.
- **Case Study: chmod -x chmod** — Guided expansion of the sample exercise, troubleshooting workflow, and meta-learning reflections.
- **High-Impact Study Tactics** — Retrieval and spaced practice, SQ3R/PQ4R, Feynman Technique, Leitner systems, and combining tactics effectively.
- **PWK Exam Mindset & Stress Strategies** — Recognizing exam readiness signals, stress management, and execution playbooks for practical exams.
- **PWK Practical Planning & Time Management** — Long-term strategy building, time allotment frameworks, focus sprints, and community-based learning practices.

### 4. Report Writing for Penetration Testers
- **Penetration Testing Note-Taking Systems** — Deliverables overview, portable note workflows, tooling selection, and screenshot capture discipline.
- **Authoring Penetration Testing Reports** — Executive and technical summaries, environment scoping, documenting findings with remediation, and appendices best practices.

### 5. Vulnerability Scanning
- **Nessus Vulnerability Scanning Operations** — Installation, component overview, credentialed scanning workflows, parsing results, and plugin management.
- **Nmap Scripting Engine for Vulnerability Detection** — NSE fundamentals, building lightweight scan profiles, and customizing scripts for exploit validation.

### 6. Common Web Application Attacks
- **Directory Traversal Exploitation Playbook** — Recognizing path traversal patterns, crafting payloads, encoding bypasses, and post-exploitation steps.
- **File Inclusion Exploitation Techniques** — LFI/RFI distinctions, leveraging wrappers, chaining to code execution, and defensive detection notes.

### 7. Client-Side Attacks
- **Client-Side Reconnaissance & Fingerprinting** — Information gathering for client targets, fingerprinting strategies, and tailoring payload delivery.
- **Microsoft Office Exploitation Workbench** — Installing lab environments, macro abuse techniques, and bypassing common mitigations.
- **Windows Library File Abuse for Execution** — Crafting weaponized library files, shortcut abuse, and execution flow control.

### 8. Fixing & Improving Exploits
- **Repairing Memory Corruption Exploits** — Buffer overflow fundamentals, cross-compiling binaries, and patching exploit code for reliability.
- **Troubleshooting Web Exploits** — Debugging common web exploit failures, adapting payloads, and ensuring post-exploitation stability.

### 9. The Metasploit Framework
- **Metasploit Fundamentals & Workspace Setup** — Console navigation, environment configuration, and using auxiliary modules for reconnaissance.
- **Metasploit Payload Engineering** — Differences between staged vs. non-staged payloads, Meterpreter exploration, and crafting custom executables.
- **Metasploit Post-Exploitation Operations** — Core Meterpreter features, post modules, and pivoting techniques inside Metasploit.
- **Automating Metasploit Engagements** — Building and executing resource scripts, parameterizing runs, and integrating with workflows.

### 10. Assembling the Pieces (Scenario Labs)
- **Public Network Enumeration Lab** — Mapping exposed services, gathering artifacts for later attacks, and prioritizing targets.
- **WEBSRV1 Exploitation Scenario** — Exploiting WordPress plugin vulnerabilities, cracking SSH key passphrases, and privilege escalation via sudo.
- **Internal Access via Phishing Campaigns** — Validating credentials off-domain, phishing playbooks, and transitioning to internal footholds.
- **Internal Network Reconnaissance Lab** — Enumerating hosts, sessions, and attack paths within the internal network.
- **INTERNALSRV1 Web Application Attack Lab** — Kerberoasting workflow, plugin abuse for relay attacks, and maintaining access.
- **Domain Controller Compromise Simulation** — Client-side reconnaissance, fingerprinting, and executing domain takeover sequences.

### 11. Trying Harder: The Labs & Exam
- **PWK Challenge Lab Overview** — Survey of challenge lab types, scenario expectations, and alignment with OSCP objectives.
- **Navigating Challenge Lab Dependencies** — Understanding scenario dependencies, decoys, routing considerations, and password attack strategy.
- **OSCP Exam Orientation** — Structuring exam preparation, managing credentials, and interpreting exam-day logistics and rules.
