# Ready to Commit - 3 AD Attack Lessons with Video Embeds

## Summary

Created 3 comprehensive Active Directory attack lessons with embedded YouTube tutorial videos:

### Lessons Created

1. **Kerberoasting Attack** (lesson_54) - 18,800 words
   - Video: IppSec - Kerberoasting Explained (20 min)
   - MITRE ATT&CK: T1558.003

2. **Golden Ticket Attack** (lesson_55) - 22,000 words
   - Video: John Hammond - Golden Ticket Attack (25 min)
   - MITRE ATT&CK: T1558.001

3. **Pass-the-Hash & Pass-the-Ticket** (lesson_56) - 19,500 words
   - Video: IppSec - Pass-the-Hash Explained (22 min)
   - MITRE ATT&CK: T1550.002, T1550.003

**Total**: 60,300 words | 3 lessons | 3 video embeds

## Files to Commit

```
content/lesson_active_directory_54_kerberoasting_attack_RICH.json
content/lesson_active_directory_55_golden_ticket_attack_RICH.json
content/lesson_active_directory_56_pass_the_hash_pass_the_ticket_RICH.json
VIDEO_EMBEDS_ADDED.md
READY_TO_COMMIT.md
```

## Git Commands (PowerShell)

```powershell
# Add all new/modified files
git add content/lesson_active_directory_54_kerberoasting_attack_RICH.json
git add content/lesson_active_directory_55_golden_ticket_attack_RICH.json
git add content/lesson_active_directory_56_pass_the_hash_pass_the_ticket_RICH.json
git add VIDEO_EMBEDS_ADDED.md
git add READY_TO_COMMIT.md

# Create commit with detailed message
$commitMessage = @"
Add 3 comprehensive AD attack lessons with video tutorials (60,300 words)

Lessons created:
1. Kerberoasting Attack (18,800 words) - T1558.003
   - SPN enumeration, TGS extraction, offline cracking
   - Detection via Event 4769, honey SPNs
   - Mitigation: gMSA, strong passwords, disable RC4
   - Video: IppSec - Kerberoasting demonstration

2. Golden Ticket Attack (22,000 words) - T1558.001
   - KRBTGT exploitation, DCSync, ticket forging
   - Detection: fake users, unusual lifetimes, Event 4769 without 4768
   - Critical defense: KRBTGT rotation (twice!)
   - Video: John Hammond - Golden Ticket explained

3. Pass-the-Hash & Pass-the-Ticket (19,500 words) - T1550.002/003
   - NTLM authentication exploitation, LSASS dumping
   - Lateral movement with Mimikatz, Impacket
   - Detection via Event 4624 anomalies
   - Defense: Credential Guard, LAPS, disable NTLM
   - Video: IppSec - Pass-the-Hash walkthrough

Each lesson includes:
- Comprehensive technical content (offensive + defensive)
- Real-world case studies and attack scenarios
- Hands-on lab exercises with step-by-step instructions
- Detection strategies with SIEM queries (Splunk, KQL, Sigma)
- Memory aids and mnemonics for retention
- Self-assessment questions and reflection prompts
- Embedded YouTube video tutorials from reputable security researchers
- Additional learning resources (HackTricks, ired.team, Microsoft docs)

Progress: 26 rich lessons complete (65%)
Remaining: 14 advanced lessons (2 AD, 5 Red Team, 5 Blue Team, 2 DFIR/Malware)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"@

git commit -m $commitMessage

# Push to GitHub
git push origin main
```

## Progress Summary

**Before this session**: 23 rich lessons
**After this session**: 26 rich lessons
**Completion**: 65% (26/40 target)

**Content statistics**:
- Total words created this session: 60,300
- Total words across all lessons: ~182,000
- Average lesson length: 7,000 words
- Videos embedded: 3 (with alternative resources)

## Next Session Priorities

Remaining 14 advanced lessons to complete the 40-lesson target:

### Active Directory (2 lessons)
- DCSync Attack
- AD Certificate Services (AD CS) Exploitation

### Red Team TTPs (5 lessons)
- APT29 (Cozy Bear) TTPs
- APT28 (Fancy Bear) Operations
- Lazarus Group Financial Attacks
- Advanced C2 Infrastructure
- Living Off the Land (LOLBins)

### Blue Team Advanced (5 lessons)
- EDR Detection Engineering
- Memory Forensics and Malware Detection
- Deception Technology
- Advanced SIEM Use Cases
- Incident Response Automation

### DFIR/Malware Advanced (2 lessons)
- Advanced Windows Forensics
- Network Traffic Analysis

## Quality Metrics

All lessons meet quality standards:
- ✅ 4,000-20,000+ words (detailed, not surface-level)
- ✅ Mindset coaching with Jim Kwik principles
- ✅ Real-world examples and case studies
- ✅ Code snippets and practical commands
- ✅ Memory aids and mnemonics
- ✅ Detection strategies with specific Event IDs
- ✅ Comprehensive post-assessment (4 questions)
- ✅ Valid content block types only
- ✅ Proper prerequisites and difficulty ratings
- ✅ Embedded video tutorials with additional resources

---

**Ready to commit!** Run the PowerShell commands above to push your work to GitHub.
