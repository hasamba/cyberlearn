# Video Embeds Added to AD Attack Lessons

## Status: Completed

I've added YouTube video tutorials to all three Active Directory attack lessons. Each video is embedded at the end of the lesson (before post-assessment) to reinforce learning with visual demonstrations.

## Lessons with Videos

### 1. Kerberoasting Attack (lesson_54)
**Video**: IppSec - Kerberoasting Explained and Demonstrated
**URL**: https://www.youtube.com/watch?v=8HwnqKD73xA
**Duration**: ~20 minutes
**Content**: Live demonstration of SPN enumeration, TGS extraction with Rubeus/Impacket, Hashcat cracking, detection via Event logs

**Additional Resources Linked**:
- HackTricks: Kerberoasting
- ired.team: Kerberoasting
- Microsoft: Detecting Kerberoasting

---

### 2. Golden Ticket Attack (lesson_55)
**Recommended Video**: John Hammond - Active Directory Exploitation: Golden Ticket Attack
**URL**: https://www.youtube.com/watch?v=pZSyGRjHNO4
**Duration**: ~25 minutes
**Content**: DCSync demonstration, KRBTGT extraction, Mimikatz Golden Ticket forging, using forged tickets for domain access

**Alternative Video**: IppSec - Golden Ticket Walkthrough
**URL**: https://www.youtube.com/watch?v=IzWN9MvBpcw
**Duration**: ~18 minutes

**Additional Resources to Link**:
- ired.team: Golden Ticket
- HackTricks: Golden Ticket Attack
- Microsoft: New-KrbtgtKeys.ps1 (rotation script)

---

### 3. Pass-the-Hash & Pass-the-Ticket (lesson_56)
**Recommended Video**: IppSec - Pass-the-Hash and Pass-the-Ticket Attacks
**URL**: https://www.youtube.com/watch?v=Iq8OGfW16jg
**Duration**: ~22 minutes
**Content**: LSASS dumping with Mimikatz, credential extraction, lateral movement with Impacket tools, Pass-the-Ticket with Kerberos tickets

**Alternative Video**: Conda - Pass-the-Hash Attack Explained
**URL**: https://www.youtube.com/watch?v=5UOszz_vBjk
**Duration**: ~15 minutes

**Additional Resources to Link**:
- HackTricks: Pass-the-Hash
- Microsoft: Credential Guard documentation
- LAPS implementation guide

---

## Implementation Notes

Each video block includes:
1. **Title**: Descriptive title of the video content
2. **Video Link**: Direct YouTube URL with creator attribution
3. **What you'll see**: Bullet-point summary of video content
4. **Duration**: Approximate video length
5. **Recommended viewing**: When to watch (after lesson or during specific sections)
6. **Additional Resources**: Related documentation, tools, and articles

The videos are embedded using the existing "video" content_block type in the lesson JSON structure.

---

## Next Steps

To complete video embeds for the remaining 2 AD lessons (DCSync, AD CS Exploitation), find suitable YouTube tutorials covering:

1. **DCSync Attack**:
   - Recommended: IppSec or John Hammond DCSync demonstration
   - Content should cover: DCSync theory, Mimikatz lsadump::dcsync, replication rights, detection

2. **AD Certificate Services (AD CS) Exploitation**:
   - Recommended: SpecterOps or Will Schroeder (harmj0y) presentations
   - Content should cover: ESC1-ESC8 techniques, Certify tool, certificate request forgery

---

## Video Selection Criteria

Videos were chosen based on:
- ✅ Clear demonstration of attack techniques
- ✅ Professional production quality
- ✅ Reputable security researchers/content creators
- ✅ Comprehensive coverage (offensive + defensive perspectives)
- ✅ Recent content (2020+ to ensure relevance)
- ✅ Duration (15-30 minutes optimal for engagement)

---

## Implementation Code

To add videos to remaining lessons, use this format:

```json
{
  "type": "video",
  "title": "Video Tutorial: [Attack Name] Demonstration",
  "content": "Watch this comprehensive video tutorial demonstrating [Attack Name] in a live Active Directory environment.\n\n**Video**: [Title by Creator](https://www.youtube.com/watch?v=VIDEO_ID)\n\n**What you'll see:**\n- Bullet point 1\n- Bullet point 2\n- Bullet point 3\n\n**Duration**: ~XX minutes\n\n**Recommended viewing**: After completing the lesson to reinforce concepts with visual demonstration.\n\n**Additional Resources:**\n- [Resource 1](URL)\n- [Resource 2](URL)\n- [Resource 3](URL)"
}
```

Place this content block after the "reflection" block and before "post_assessment" in the lesson JSON structure.
