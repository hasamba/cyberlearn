# ChatGPT Prompt: Batch 4 - Network Pivoting & Reconnaissance (6 lessons)

Copy this entire prompt into ChatGPT to generate 6 lessons on pivoting, tunneling, and reconnaissance.

---

# LESSON CREATION REQUEST: Pivoting & Reconnaissance (6 Lessons)

Generate 6 pentest lessons following the exact structure from BATCH_01_WEB_TESTING.md.

## Lessons to Create:

### Lesson 25: Port Forwarding and Pivoting with Linux Tools
**Domain**: pentest | **Difficulty**: 3 | **Order Index**: 25 | **Time**: 60min
**Prerequisites**: ["pentest_03"]

**Concepts**: SSH local port forwarding (-L), SSH remote port forwarding (-R), SSH dynamic port forwarding (SOCKS proxy -D), ProxyChains configuration and usage, Socat for port redirection, Chisel for HTTP tunneling, Ligolo-ng for network pivoting, multi-hop pivoting scenarios, troubleshooting pivot connections

**Content Focus**: Comprehensive network pivoting using Linux tools, SSH tunneling techniques, SOCKS proxies, modern tools like Chisel and Ligolo-ng, multi-hop pivot scenarios. Hands-on: Set up multi-hop SSH tunnel, use ProxyChains. Real-world: Pivoting through DMZ networks.

**File name**: `lesson_pentest_25_pivoting_linux_tools_RICH.json`

---

### Lesson 26: Port Forwarding and Pivoting with Windows Tools
**Domain**: pentest | **Difficulty**: 3 | **Order Index**: 26 | **Time**: 60min
**Prerequisites**: ["pentest_03"]

**Concepts**: Windows netsh port forwarding, PowerShell remoting for pivoting, Plink (PuTTY Link) for SSH tunnels, Netcat and PowerCat relays, built-in Windows SOCKS proxies, WMI and DCOM for pivoting, RDP tunneling, troubleshooting Windows pivots

**Content Focus**: Windows-specific pivoting techniques using native tools and PowerShell, netsh, plink, and Windows-specific lateral movement for pivot establishment. Hands-on: netsh portproxy, PowerShell remoting pivot. Real-world: Pivoting in enterprise Windows networks.

**File name**: `lesson_pentest_26_pivoting_windows_tools_RICH.json`

---

### Lesson 27: Advanced Tunneling: HTTP and DNS
**Domain**: pentest | **Difficulty**: 3 | **Order Index**: 27 | **Time**: 60min
**Prerequisites**: ["pentest_25", "pentest_26"]

**Concepts**: HTTP tunneling fundamentals, DNS tunneling techniques, Iodine for DNS tunnels, dnscat2 for C2 over DNS, HTTP tunneling with reGeorg and ABPTTS, ICMP tunneling, protocol-specific evasion, detecting and defending against tunneling

**Content Focus**: Advanced covert tunneling using DNS and HTTP protocols, circumventing egress filtering, C2 over DNS, detection evasion for restricted network environments. Hands-on: Set up DNS tunnel with dnscat2. Real-world: APT groups using DNS tunneling.

**File name**: `lesson_pentest_27_advanced_tunneling_http_dns_RICH.json`

---

### Lesson 28: Active Information Gathering: Protocol Enumeration
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 28 | **Time**: 55min
**Prerequisites**: []

**Concepts**: Service-specific enumeration (SMB, SNMP, SMTP, DNS, LDAP), banner grabbing techniques, version detection and vulnerability correlation, protocol-specific exploitation, automated enumeration scripts (enum4linux, snmpwalk, ldapsearch), NetBIOS and LDAP enumeration, manual vs automated approaches, enumeration opsec

**Content Focus**: Protocol-level enumeration for common network services, manual and automated approaches, information extraction, correlating findings with vulnerabilities. Hands-on: Enumerate SMB shares, SNMP community strings. Real-world: Information disclosure leading to compromise.

**File name**: `lesson_pentest_28_protocol_enumeration_RICH.json`

---

### Lesson 29: Living off the Land: Reconnaissance with Native Tools
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 29 | **Time**: 50min
**Prerequisites**: []

**Concepts**: Windows native reconnaissance (net commands, wmic, tasklist, query), Linux/Unix native tools (ps, netstat, who, w, ss), PowerShell reconnaissance cmdlets (Get-Process, Get-Service), LOLBAS and GTFOBins for reconnaissance, domain reconnaissance without custom tools, network mapping with native tools, avoiding detection with LOLBins, operational security considerations

**Content Focus**: Stealthy reconnaissance using only native operating system tools, living-off-the-land techniques, domain enumeration without custom tools, detection avoidance. Hands-on: Complete recon using only native Windows/Linux tools. Real-world: APT groups using LOLBins.

**File name**: `lesson_pentest_29_living_off_land_recon_RICH.json`

---

### Lesson 30: Public Exploits: Discovery, Analysis, and Execution
**Domain**: pentest | **Difficulty**: 2 | **Order Index**: 30 | **Time**: 55min
**Prerequisites**: []

**Concepts**: Exploit database navigation (Exploit-DB, GitHub, Packet Storm), CVE research and correlation, exploit code analysis and safety review, dependency resolution, exploit customization and adaptation, compiling exploits (C, Python, Java, Go), exploit reliability testing, documenting exploit usage

**Content Focus**: Finding, analyzing, and safely executing public exploits, understanding exploit code, customizing for target environments, troubleshooting exploit failures. Hands-on: Find exploit for specific CVE, analyze code, modify and execute. Real-world: Public exploits used in major breaches.

**File name**: `lesson_pentest_30_public_exploits_RICH.json`

---

## Requirements (Same as Batch 1):
- 4,000-5,500 words per lesson
- All content blocks: mindset_coach, explanation, video, code_exercise, real_world, memory_aid, reflection
- 2 post-assessment questions per lesson
- Valid content types and Jim Kwik principles only
- New UUIDs for all lesson_id and question_id fields
- Real tools, commands, and techniques
- YouTube video URLs for relevant tutorials

**START GENERATING**: Create all 6 lessons as complete JSON files.
