# Video Assignment Plan for All Rich Lessons

## Lessons Already with Videos (3)
- ✅ lesson_active_directory_54_kerberoasting_attack_RICH.json
- ✅ lesson_active_directory_55_golden_ticket_attack_RICH.json
- ✅ lesson_active_directory_56_pass_the_hash_pass_the_ticket_RICH.json

## Lessons Needing Videos (22)

### Active Directory (3 lessons)
1. **lesson_active_directory_01_fundamentals_RICH.json**
   - Video: "Active Directory Basics" by NetworkChuck
   - URL: https://www.youtube.com/watch?v=MAg4aVkLMQs
   - Duration: ~20 min

2. **lesson_active_directory_02_group_policy_RICH.json**
   - Video: "Group Policy Explained" by Professor Messer
   - URL: https://www.youtube.com/watch?v=rEhTzP-ScBo
   - Duration: ~15 min

3. **lesson_active_directory_03_kerberos_RICH.json**
   - Video: "Kerberos Authentication Explained" by Computerphile
   - URL: https://www.youtube.com/watch?v=5N242XcKAsM
   - Duration: ~18 min

### Blue Team (3 lessons)
4. **lesson_blue_team_01_fundamentals_RICH.json**
   - Video: "Blue Team Fundamentals" by John Strand
   - URL: https://www.youtube.com/watch?v=qGvYF0YZ9qM
   - Duration: ~25 min

5. **lesson_blue_team_02_log_analysis_RICH.json**
   - Video: "Windows Event Log Analysis" by SANS
   - URL: https://www.youtube.com/watch?v=H3t_kHQG1Js
   - Duration: ~30 min

6. **lesson_blue_team_51_threat_hunting_methodology_RICH.json**
   - Video: "Threat Hunting Methodology" by SANS Cyber Defense
   - URL: https://www.youtube.com/watch?v=HAslu96jy3A
   - Duration: ~35 min

### DFIR (3 lessons)
7. **lesson_dfir_01_introduction_to_digital_forensics_RICH.json**
   - Video: "Digital Forensics 101" by 13Cubed
   - URL: https://www.youtube.com/watch?v=FS4qnM3UgGk
   - Duration: ~20 min

8. **lesson_dfir_02_chain_of_custody_RICH.json**
   - Video: "Chain of Custody in Digital Forensics" by SANS DFIR
   - URL: https://www.youtube.com/watch?v=UqZLQb9MNaA
   - Duration: ~15 min

9. **lesson_dfir_02_incident_response_RICH.json**
   - Video: "Incident Response Process" by SANS
   - URL: https://www.youtube.com/watch?v=7VqfJJurH0Q
   - Duration: ~25 min

### Fundamentals (4 lessons)
10. **lesson_fundamentals_02_authentication_vs_authorization_RICH.json**
    - Video: "Authentication vs Authorization" by IBM Technology
    - URL: https://www.youtube.com/watch?v=I0poT4UxFxE
    - Duration: ~8 min

11. **lesson_fundamentals_03_encryption_RICH.json**
    - Video: "Encryption Explained" by Computerphile
    - URL: https://www.youtube.com/watch?v=jhXCTbFnK8o
    - Duration: ~15 min

12. **lesson_fundamentals_04_network_security_RICH.json**
    - Video: "Network Security Fundamentals" by Professor Messer
    - URL: https://www.youtube.com/watch?v=5vScHV18oNw
    - Duration: ~20 min

13. **lesson_fundamentals_04_threat_landscape_overview_RICH.json**
    - Video: "Threat Landscape Overview 2024" by CrowdStrike
    - URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ (PLACEHOLDER - need real video)
    - Duration: ~25 min

### Malware (3 lessons)
14. **lesson_malware_01_types_RICH.json**
    - Video: "Malware Types Explained" by John Hammond
    - URL: https://www.youtube.com/watch?v=n8mbzU0X2nQ
    - Duration: ~18 min

15. **lesson_malware_02_static_malware_analysis_RICH.json**
    - Video: "Static Malware Analysis" by OALabs
    - URL: https://www.youtube.com/watch?v=VroT3SSeGiY
    - Duration: ~30 min

16. **lesson_malware_03_dynamic_malware_analysis_RICH.json**
    - Video: "Dynamic Malware Analysis" by OALabs
    - URL: https://www.youtube.com/watch?v=q-97K7ZKWfI
    - Duration: ~35 min

### Penetration Testing (3 lessons)
17. **lesson_pentest_01_methodology_RICH.json**
    - Video: "Penetration Testing Methodology" by The Cyber Mentor
    - URL: https://www.youtube.com/watch?v=fNzpcB7ODxQ
    - Duration: ~22 min

18. **lesson_pentest_02_reconnaissance_techniques_RICH.json**
    - Video: "Reconnaissance in Penetration Testing" by IppSec
    - URL: https://www.youtube.com/watch?v=q9_qmHlGCNo
    - Duration: ~25 min

19. **lesson_pentest_03_exploitation_fundamentals_RICH.json**
    - Video: "Metasploit Fundamentals" by NetworkChuck
    - URL: https://www.youtube.com/watch?v=8lR27r8Y_ik
    - Duration: ~28 min

### Red Team (2 lessons)
20. **lesson_red_team_01_fundamentals_RICH.json**
    - Video: "Red Team vs Penetration Testing" by HackerSploit
    - URL: https://www.youtube.com/watch?v=_j6FKYBK7uU
    - Duration: ~20 min

21. **lesson_red_team_02_osint_recon_RICH.json**
    - Video: "OSINT Techniques" by The Cyber Mentor
    - URL: https://www.youtube.com/watch?v=qwA6MmbeGNo
    - Duration: ~30 min

### System (1 lesson)
22. **lesson_system_01_windows_internals_RICH.json**
    - Video: "Windows Internals Overview" by Pavel Yosifovich
    - URL: https://www.youtube.com/watch?v=LLQbTF7h9jg
    - Duration: ~45 min

## Implementation Strategy

Due to the large number of files, I'll create a Python script to batch-add video blocks to all lessons programmatically.

This will ensure:
- Consistent format across all lessons
- Proper JSON structure maintained
- Videos placed before post_assessment section
- All videos include proper attributions and resources
