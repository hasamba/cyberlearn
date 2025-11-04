"""
Add relevant mindset coaching blocks to lessons missing them.

This script adds contextually appropriate mindset coaching based on:
- Lesson domain and difficulty
- Specific topic and challenges
- Professional context and career relevance
"""

import json
import os
from pathlib import Path

# Mindset coaching content tailored to specific lessons
MINDSET_COACHING = {
    "lesson_active_directory_57_dcsync_attack_RICH.json": {
        "text": """**Mindset: Master the Attacker's Perspective to Defend Better**

Learning DCSync attacks isn't about becoming a malicious actor—it's about understanding how adversaries think and operate. As a defender, this knowledge is your superpower.

**Why This Matters:**
- Red teamers who understand DCSync can test organizational defenses realistically
- Blue teamers who know this attack can detect it before damage occurs
- Every DFIR analyst needs to recognize DCSync in memory dumps and event logs

**Overcoming the Learning Curve:**
DCSync feels intimidating because it touches Active Directory's core replication mechanism. That's exactly why mastering it sets you apart. Break it down:
1. Understand the legitimate replication process first
2. See how Mimikatz abuses that same process
3. Practice detection in a lab environment

**Career Impact:**
Organizations desperately need security professionals who understand privilege escalation attacks like DCSync. This knowledge directly translates to:
- Penetration testing certifications (OSCP, PNPT)
- Red team positions at top security firms
- SOC analyst roles focused on detecting credential theft

Remember: Every expert was once a beginner who refused to give up. You're building expertise that protects organizations from real threats."""
    },

    "lesson_active_directory_58_ad_cs_exploitation_RICH.json": {
        "text": """**Mindset: Certificate Services Exploitation is Your Competitive Advantage**

AD CS vulnerabilities (ESC1-ESC8) are among the most powerful attack vectors discovered in recent years, yet many security professionals haven't studied them deeply. This is your opportunity to stand out.

**Why This Complexity is Worth It:**
- ESC vulnerabilities were presented at Black Hat 2021 and changed AD security forever
- Most organizations haven't patched these attack vectors
- Knowing ESC attacks makes you invaluable to both red and blue teams

**Breaking Down the Challenge:**
Certificate-based attacks feel abstract at first because they combine cryptography, Active Directory, and PKI concepts. Use this approach:
1. Understand what certificates are used for in AD (authentication, encryption)
2. Learn why misconfigured certificate templates are dangerous
3. Practice one ESC technique at a time in your lab

**Real-World Relevance:**
When SpecterOps researchers discovered these vulnerabilities, organizations worldwide scrambled to find defenders who understood certificate services. That demand still exists.

**Career Insight:**
- ESC knowledge is explicitly listed in advanced red team job descriptions
- Purple team exercises specifically test for AD CS misconfigurations
- This expertise commands premium consulting rates ($200+/hour)

You're not just learning an attack—you're mastering a critical gap in enterprise security that few professionals understand. That makes you exceptionally valuable."""
    },

    "lesson_active_directory_59_azure_ad_and_hybrid_identity_attacks_RICH.json": {
        "text": """**Mindset: Cloud + On-Prem = Modern Security Career Essential**

Hybrid identity attacks represent the future of cybersecurity. As organizations move to cloud, understanding the bridge between Azure AD and on-premises AD is no longer optional—it's career-critical.

**Why This Matters Now:**
- 95% of Fortune 500 companies use Azure AD + on-prem hybrid setups
- Attackers specifically target sync accounts (MSOL_, AZUREADSSOACC$)
- Most security teams lack hybrid identity expertise

**Embracing the Learning Curve:**
Hybrid environments feel overwhelming because you're juggling two identity systems simultaneously. That's exactly why this skill is so valuable—it's hard, so fewer people master it.

**Your Learning Strategy:**
1. Solidify on-prem AD fundamentals first
2. Learn Azure AD concepts separately
3. Then tackle the hybrid sync mechanisms (Azure AD Connect)
4. Finally, study attack paths that cross boundaries

**Market Demand:**
Cloud security roles (especially Azure-focused) are growing 40% year-over-year. Adding hybrid identity attack knowledge to your resume makes you stand out for:
- Cloud security engineer positions
- Azure red team specialists
- Hybrid environment penetration testers

**Mindset Shift:**
Don't think "this is too complex." Think "this complexity is my moat." While others avoid hybrid identity security, you're becoming the expert organizations desperately need.

The future of cybersecurity is hybrid. You're preparing for that future right now."""
    },

    "lesson_blue_team_05_edr_deployment_RICH.json": {
        "text": """**Mindset: EDR Mastery Equals Job Security**

EDR deployment and tuning is one of the most in-demand blue team skills today. Organizations are drowning in alerts, and they need professionals who can deploy EDR effectively without creating alert fatigue.

**Why This Skill Matters:**
- Every modern SOC relies on EDR (CrowdStrike, SentinelOne, Microsoft Defender)
- Poorly deployed EDR creates more problems than it solves
- Organizations will pay premium salaries for EDR expertise

**Overcoming Implementation Anxiety:**
EDR feels overwhelming because you're balancing security coverage with operational impact. Too aggressive = alert fatigue. Too permissive = missed threats. This is a learned skill, not an innate talent.

**Your Path to Mastery:**
1. Start with a small pilot group (IT team, security team)
2. Fine-tune detection policies based on actual environment behavior
3. Gradually roll out to production systems
4. Learn from each deployment phase

**Career Accelerator:**
- SOC analyst roles explicitly require EDR experience
- Security operations engineers focus heavily on EDR tuning
- Incident responders rely on EDR telemetry daily

**Real Talk:**
Every EDR deployment has challenges. You'll create false positives. You'll miss some threats initially. That's normal and expected. The difference between junior and senior analysts is persistence through these learning moments.

You're not just deploying software—you're building enterprise-grade detection capabilities that protect real people and real data."""
    },

    "lesson_blue_team_06_memory_forensics_RICH.json": {
        "text": """**Mindset: Memory Forensics Reveals What Others Miss**

Memory forensics is where elite DFIR analysts separate themselves from the rest. While others rely on disk artifacts, you'll be extracting malware, credentials, and network connections from RAM—uncovering evidence attackers thought they erased.

**Why This Expertise is Powerful:**
- Memory contains artifacts that never touch disk (fileless malware, injected code)
- Sophisticated attackers specifically avoid disk to evade detection
- Memory analysis is explicitly tested in GIAC GCFA and GCFE certifications

**Embracing the Complexity:**
Memory forensics feels intimidating because you're working with raw binary data, OS internals, and complex data structures. But here's the truth: every memory forensics expert started exactly where you are now.

**Breaking It Down:**
1. Start with basic memory acquisition (creating memory dumps)
2. Learn Volatility framework one plugin at a time (pslist, netscan, malfind)
3. Practice on known malware samples in a lab
4. Gradually tackle more complex analysis scenarios

**Career Differentiator:**
Organizations pay significantly more for DFIR analysts with memory forensics skills:
- Incident response consultants: $150-250/hour
- Malware analysts: $120k-180k salary range
- Digital forensics examiners: Premium billing rates

**Mindset Shift:**
Memory forensics isn't about memorizing every Volatility plugin. It's about understanding what processes, connections, and artifacts live in RAM, then using tools to extract that evidence. You're developing investigative thinking, not just technical skills.

Remember: The most advanced threats hide in memory. By mastering memory forensics, you're learning to catch what others miss."""
    },

    "lesson_blue_team_07_deception_technology_RICH.json": {
        "text": """**Mindset: Deception Technology is the Future of Proactive Defense**

Most organizations play defense reactively—waiting for alerts after attackers strike. Deception technology flips the script: you're actively creating traps that detect attackers the moment they move laterally.

**Why This Approach is Revolutionary:**
- Honeypots and deception create high-fidelity alerts (almost zero false positives)
- Attackers can't distinguish fake credentials from real ones
- This is active defense without legal/ethical risks of "hack back"

**Overcoming Implementation Doubts:**
You might think "won't sophisticated attackers detect honeypots?" Here's the reality: even nation-state APT groups fall for well-designed deception. Why? Because they're operating in YOUR environment, where you control the narrative.

**Your Deployment Strategy:**
1. Start small: Deploy 3-5 honeypot VMs in your network
2. Plant fake credentials in obvious locations (SMB shares, scripts)
3. Monitor for any interaction with these decoys
4. Gradually expand your deception infrastructure

**Career Advantage:**
Deception technology experience makes you stand out for:
- Threat hunting roles (proactive detection mindset)
- Security architecture positions (designing defensive layers)
- Purple team exercises (you understand attacker TTP at a deep level)

**Real-World Impact:**
Organizations using deception technology detect lateral movement in minutes instead of months. You're learning to give defenders the advantage for once.

**Mindset Shift:**
Traditional defense is exhausting—you're constantly reacting. Deception technology lets you take control of the battlefield. You're not just defending; you're setting traps that turn attackers' own techniques against them.

This is the mindset of elite defenders: proactive, creative, and relentlessly focused on early detection."""
    },

    "lesson_blue_team_09_incident_response_automation_RICH.json": {
        "text": """**Mindset: Automation Multiplies Your Impact**

As an incident responder, you'll face moments where 10 alerts fire simultaneously, and you can't be in 10 places at once. That's where SOAR (Security Orchestration, Automation, and Response) transforms you from a single responder into an entire response team.

**Why Automation Matters:**
- Organizations face 1,000+ security alerts per day on average
- Manual response takes 30-60 minutes per incident
- Automated playbooks respond in seconds

**Overcoming Automation Anxiety:**
You might worry: "What if I automate the wrong response and cause an outage?" This fear is normal and actually shows good security thinking. The solution isn't to avoid automation—it's to start small and test thoroughly.

**Your Automation Journey:**
1. Start with read-only automation (gather data, create tickets)
2. Progress to semi-automated responses (prompt analyst for approval)
3. Eventually deploy full automation for known-good scenarios (block IOCs, quarantine files)
4. Always maintain human oversight for critical actions

**Career Multiplier:**
SOAR expertise is exploding in demand:
- Security automation engineer roles: $130k-190k
- SOC managers prioritize hiring analysts who can build playbooks
- Consulting firms bill premium rates for SOAR implementations

**Real-World Impact:**
A single well-designed playbook can:
- Reduce mean time to respond (MTTR) from 1 hour to 5 minutes
- Free analysts to focus on complex threats instead of repetitive tasks
- Enable 24/7 response even with limited staff

**Mindset Shift:**
Automation isn't about replacing security analysts—it's about amplifying your effectiveness. Think of SOAR as your force multiplier: you design the response logic once, and it executes consistently every time.

You're not just responding to incidents; you're building an automated defense system that scales your expertise across hundreds of scenarios simultaneously."""
    },

    "lesson_cloud_03_kubernetes_security_RICH.json": {
        "text": """**Mindset: Kubernetes Security is Your Cloud Career Accelerator**

Kubernetes runs production workloads at virtually every tech company—Google, Netflix, Spotify, Airbnb. Understanding K8s security isn't just valuable; it's becoming mandatory for cloud security roles.

**Why This Investment Pays Off:**
- 94% of organizations use containers in production (CNCF survey)
- Kubernetes security roles command $140k-200k+ salaries
- Most security professionals avoid K8s due to complexity—your opportunity

**Embracing the Learning Curve:**
Kubernetes feels overwhelming because it's a distributed system with many moving parts: pods, services, ingress, RBAC, network policies, admission controllers. But here's the secret: you don't need to master everything at once.

**Your Learning Path:**
1. Understand basic K8s architecture (control plane, worker nodes)
2. Learn how pods are created and managed
3. Focus on security primitives (RBAC, network policies, pod security policies)
4. Practice attacks and defenses in a local cluster (kind, minikube)

**Real-World Demand:**
Organizations are desperately seeking security professionals who understand:
- Kubernetes RBAC misconfigurations (excessive permissions)
- Container escape techniques (protecting the host)
- Supply chain attacks (malicious container images)

**Career Insight:**
Adding "Kubernetes security" to your resume unlocks:
- Cloud security engineer positions at Fortune 500 companies
- DevSecOps roles where you embed security into CI/CD pipelines
- Consulting opportunities at premium rates

**Mindset Shift:**
Don't think "Kubernetes is too complex for me." The engineers who built K8s aren't smarter than you—they just invested the time. You're making that same investment now.

Every container orchestration platform has complexity. Kubernetes won the market. By mastering K8s security, you're positioning yourself for the next decade of cloud security careers.

Start small, practice consistently, and watch this skill transform your opportunities."""
    },

    "lesson_cloud_04_iam_cloud_identity_RICH.json": {
        "text": """**Mindset: IAM is Where Cloud Breaches Begin and End**

95% of cloud security incidents involve identity and access management misconfigurations. Master IAM, and you're mastering the root cause of most cloud breaches.

**Why IAM Expertise is Critical:**
- IAM controls who can access what resources across your entire cloud environment
- A single misconfigured IAM role can expose your entire AWS/Azure/GCP infrastructure
- Organizations desperately need professionals who understand least privilege at cloud scale

**Overcoming IAM Complexity:**
IAM feels overwhelming because it's:
- Abstract (policies, roles, permissions—not tangible like servers)
- Deeply nested (policies inherit from groups, roles assume other roles)
- Cloud-specific (AWS IAM ≠ Azure RBAC ≠ GCP IAM)

Here's how to tackle it: Focus on one cloud provider's IAM model first (AWS is most common). Once you understand the concepts—policies, principals, actions, resources—the other clouds make sense.

**Your Mastery Path:**
1. Learn to read IAM policies (JSON for AWS, RBAC for Azure)
2. Practice principle of least privilege in a lab
3. Study common misconfigurations (overly permissive policies)
4. Learn to audit and remediate IAM at scale

**Career Game-Changer:**
IAM expertise unlocks premium roles:
- Cloud security architect: $150k-220k
- Cloud IAM engineer: $130k-180k
- GRC analyst (cloud focus): $100k-150k

**Real-World Impact:**
The Capital One breach (2019) happened because of IAM misconfigurations. The SolarWinds attack leveraged cloud IAM. Uber, Twilio, Mailchimp breaches—all involved IAM issues.

By mastering IAM, you're learning to prevent the types of breaches making headlines.

**Mindset Shift:**
IAM isn't "boring identity stuff." It's the control plane for your entire cloud infrastructure. If attackers control IAM, they control everything. If you master IAM, you control security posture.

This is where cloud security careers are built."""
    },

    "lesson_cloud_05_serverless_security_RICH.json": {
        "text": """**Mindset: Serverless is the Future—Secure it Now**

Serverless computing (Lambda, Azure Functions, Cloud Functions) is revolutionizing how applications are built. As organizations rush to adopt serverless, they're creating new security blind spots. Your serverless security expertise makes you indispensable.

**Why Serverless Security Matters:**
- Serverless adoption growing 50% year-over-year
- Traditional security tools don't work for ephemeral functions
- Most developers don't understand serverless security implications

**New Paradigm, New Challenges:**
Serverless security feels different because:
- No persistent servers to patch and monitor
- Functions execute for milliseconds then disappear
- Attack surface shifts to function permissions, event triggers, and dependencies

This isn't harder than traditional security—it's just different. And "different" creates opportunity for those who learn it early.

**Your Learning Strategy:**
1. Understand serverless architecture (event-driven, stateless functions)
2. Learn function permission models (Lambda execution roles)
3. Study serverless-specific attacks (event injection, over-privileged functions)
4. Practice securing a serverless application end-to-end

**Career Positioning:**
Serverless security expertise positions you for:
- Cloud-native application security roles
- DevSecOps positions in modern tech companies
- Security consulting for organizations migrating to serverless

**Market Reality:**
Organizations are deploying thousands of Lambda functions without security reviews. They need professionals who can:
- Audit function permissions at scale
- Secure API Gateway and event sources
- Implement least privilege for serverless applications

**Mindset Shift:**
Don't see serverless as "one more thing to learn." See it as early positioning in the next wave of cloud computing. You're building expertise in technology that will dominate enterprise computing for the next decade.

The security professionals who master serverless now will lead cloud security teams in 5 years.

Start learning serverless security while it's still early. Your future self will thank you."""
    },

    "lesson_cloud_12_aws_control_tower_security_automation_RICH.json": {
        "text": """**Mindset: Governance at Scale Separates Good from Great Cloud Engineers**

AWS Control Tower automates the governance and security baseline for entire organizations with dozens or hundreds of AWS accounts. This isn't entry-level cloud security—this is enterprise-grade, multi-account orchestration. You're learning skills that large organizations desperately need.

**Why Control Tower Expertise is Valuable:**
- Enterprise organizations manage 50-500+ AWS accounts
- Manual governance doesn't scale beyond 10 accounts
- Control Tower architects command premium salaries ($160k-230k)

**Embracing Enterprise Complexity:**
Control Tower feels intimidating because it orchestrates multiple AWS services simultaneously:
- AWS Organizations (account structure)
- Service Control Policies (permissions guardrails)
- AWS Config (compliance monitoring)
- CloudFormation StackSets (deployment automation)

Here's the reality: Large organizations need this complexity managed, and very few professionals can do it. That's your opportunity.

**Breaking It Down:**
1. Understand multi-account AWS architecture (why organizations use many accounts)
2. Learn AWS Organizations and OUs (organizational units)
3. Study Service Control Policies (preventive controls)
4. Finally, see how Control Tower automates all of this

**Career Acceleration:**
Control Tower expertise unlocks:
- Cloud security architect roles at enterprise companies
- Cloud governance consultant positions
- Multi-cloud security management opportunities

**Real-World Impact:**
Without Control Tower, security teams manually configure:
- Logging and monitoring for each account
- Network security for every VPC
- IAM policies across hundreds of resources

With Control Tower, you define governance once and enforce it automatically across the entire organization.

**Mindset Shift:**
Don't think "this is too advanced for me right now." Enterprise organizations need engineers who understand multi-account governance TODAY. By learning Control Tower now, you're positioning yourself for senior cloud security roles.

This is the difference between managing cloud security for small projects versus architecting security for entire enterprises. You're choosing the enterprise path—that's ambitious and exactly the right move for your career."""
    },

    "lesson_dfir_08_forensic_timeline_hunt_evil_RICH.json": {
        "text": """**Mindset: Timeline Analysis is How You Tell the Complete Story**

When an incident occurs, executives will ask: "What happened, when did it start, and how far did they get?" Timeline analysis is how you answer those questions with confidence and evidence.

**Why Timeline Mastery Matters:**
- Timelines reveal the full attack narrative (reconnaissance → exploitation → lateral movement → exfiltration)
- Courts and executives demand chronological evidence
- Timeline analysis is explicitly tested in SANS FOR500 and FOR508

**Overcoming Analysis Paralysis:**
Looking at 50,000 timestamp entries feels overwhelming. Where do you even start? Elite forensic analysts use a structured approach:

1. Start with known-bad indicators (malware execution time, C2 connection timestamp)
2. Work backward (what happened before?) and forward (what happened after?)
3. Correlate across multiple artifact sources (registry, prefetch, event logs, browser history)
4. Build the narrative piece by piece

**The Learning Curve:**
You won't master timelines in one lesson or even one case. Each investigation teaches you:
- Which artifacts matter most for specific attack types
- How to spot timeline anomalies (gaps that indicate anti-forensics)
- What normal vs. suspicious activity looks like

**Career Differentiator:**
DFIR analysts who excel at timeline analysis:
- Close investigations faster (efficient root cause identification)
- Testify effectively in court (clear chronological narratives)
- Get promoted to lead investigator roles

**Real-World Validation:**
Major breach reports (Verizon DBIR, Mandiant M-Trends) emphasize that understanding the attack timeline is critical for:
- Determining breach scope
- Identifying all compromised systems
- Preventing recurrence

**Mindset Shift:**
Timeline analysis isn't about finding every single timestamp. It's about constructing a defensible narrative of what happened. Think like a detective assembling clues, not a computer processing data.

You're learning to turn raw forensic artifacts into courtroom-ready evidence. That's the core skill of elite DFIR professionals."""
    },

    "lesson_dfir_157_password_hash_collection_and_analysis_RICH.json": {
        "text": """**Mindset: Understanding Password Attacks Protects Organizations**

Learning to extract and analyze password hashes isn't about cracking your employer's passwords—it's about understanding how attackers escalate privileges so you can defend against these techniques.

**Why This Knowledge is Essential:**
- Password hash extraction is step 1 in almost every privilege escalation attack
- DFIR analysts must recognize hash dumping in memory and on disk
- Red teamers need to test whether organizations can detect credential theft

**Ethical Clarity:**
You might feel uncomfortable learning these techniques. That discomfort shows you have good security ethics. Channel that into:
- Only practicing in authorized environments (your lab, sanctioned penetration tests)
- Understanding that defenders MUST know attacker techniques
- Using this knowledge to improve organizational security posture

**The Technical Journey:**
Password hash analysis combines multiple domains:
- Windows internals (how LSASS stores credentials)
- Cryptography (NTLM, Kerberos, bcrypt hashing)
- Tool proficiency (Mimikatz, Impacket, Hashcat)

Break it into phases:
1. Learn where hashes are stored (SAM, NTDS.dit, LSASS memory)
2. Practice extraction in your lab
3. Understand hash formats (NTLM, NTLMv2, Kerberos tickets)
4. Learn detection and prevention techniques

**Career Applications:**
This expertise directly applies to:
- Penetration testing (credential access phase of attacks)
- Incident response (identifying credential compromise)
- Threat hunting (detecting hash dumping tools like Mimikatz)
- Security architecture (preventing credential exposure)

**Detection Mindset:**
As you learn offensive techniques, simultaneously think:
- What event logs does this generate?
- What memory artifacts does this leave?
- How would I detect this as a defender?

**Mindset Shift:**
Elite security professionals understand both offense and defense. You're not "going to the dark side" by learning credential attacks—you're becoming a complete security professional who understands the full threat landscape.

Organizations need people who can think like attackers to defend effectively. That's what you're becoming."""
    },

    "lesson_fundamentals_08_security_frameworks_compliance_RICH.json": {
        "text": """**Mindset: Frameworks Create Career Opportunities**

Security frameworks (NIST, ISO 27001, CIS Controls) might seem like "boring compliance stuff" compared to hacking and forensics. But here's the reality: Every security program is built on frameworks, and professionals who understand them unlock management and architect roles.

**Why Framework Knowledge Matters:**
- Every organization must comply with at least one framework (industry requirement)
- Security managers must map controls to NIST CSF, ISO 27001, SOC 2
- Framework expertise bridges technical skills with business value

**Overcoming the "Boring" Perception:**
Frameworks feel abstract because they're not hands-on like penetration testing. But consider:
- CISOs need analysts who understand compliance requirements
- Consultants bill $200+/hour for framework assessments
- Cloud security architects map technical controls to framework requirements daily

**Your Learning Strategy:**
1. Start with one framework (NIST CSF is most universal)
2. Understand the core categories (Identify, Protect, Detect, Respond, Recover)
3. Map technical security controls you know (firewalls, SIEM, EDR) to framework requirements
4. Practice articulating security value in business terms

**Career Acceleration:**
Framework expertise unlocks:
- GRC analyst roles: $85k-130k (entry to mid-level)
- Security architect positions: $140k-200k (requires framework knowledge)
- CISO track (executives must understand compliance frameworks)

**Real-World Application:**
When executives ask "Are we secure?", the answer isn't technical—it's:
- "We're 85% compliant with NIST CSF"
- "We've implemented all critical CIS Controls"
- "Our ISO 27001 audit found zero non-conformities"

**Mindset Shift:**
Technical skills get you hired. Framework knowledge gets you promoted.

You're not abandoning hands-on security work. You're adding a skill layer that:
- Translates technical security into business value
- Opens management career paths
- Makes you valuable beyond just technical execution

Think of frameworks as the language of security leadership. You're learning to speak that language now."""
    }
}

def add_mindset_coaching_block(lesson_data, filename):
    """Add relevant mindset coaching block to a lesson."""

    if filename not in MINDSET_COACHING:
        return False, "No mindset coaching content defined for this lesson"

    # Check if mindset coaching already exists
    for block in lesson_data.get("content_blocks", []):
        if block.get("type") == "mindset_coach":
            return False, "Lesson already has mindset coaching block"

    # Get the coaching content
    coaching_content = MINDSET_COACHING[filename]

    # Create the mindset coaching block
    mindset_block = {
        "type": "mindset_coach",
        "content": coaching_content
    }

    # Insert as second-to-last block (before reflection, which is typically last)
    content_blocks = lesson_data.get("content_blocks", [])

    # Find the best insertion point (before reflection or at the end)
    insert_index = len(content_blocks)
    for i, block in enumerate(content_blocks):
        if block.get("type") == "reflection":
            insert_index = i
            break

    content_blocks.insert(insert_index, mindset_block)
    lesson_data["content_blocks"] = content_blocks

    return True, f"Added mindset coaching block at position {insert_index + 1}"

def main():
    content_dir = Path("content")
    modified_count = 0
    skipped_count = 0

    print("=" * 80)
    print("ADD MINDSET COACHING TO LESSONS")
    print("=" * 80)
    print()

    for filename in MINDSET_COACHING.keys():
        filepath = content_dir / filename

        if not filepath.exists():
            print(f"[SKIP] {filename}: File not found")
            skipped_count += 1
            continue

        # Load lesson
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)

        # Add mindset coaching
        success, message = add_mindset_coaching_block(lesson_data, filename)

        if success:
            # Save updated lesson
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lesson_data, f, indent=2, ensure_ascii=False)

            print(f"[OK] {filename}")
            print(f"     Title: {lesson_data.get('title', 'Unknown')}")
            print(f"     {message}")
            print()
            modified_count += 1
        else:
            print(f"[SKIP] {filename}: {message}")
            skipped_count += 1

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Lessons modified: {modified_count}")
    print(f"Lessons skipped: {skipped_count}")
    print()

    if modified_count > 0:
        print("Next steps:")
        print("1. python scripts/load_all_lessons.py         # Load into database")
        print("2. python scripts/validate_lesson_compliance.py  # Verify changes")
        print("3. python scripts/update_template_database.py   # Sync template")

if __name__ == "__main__":
    main()
