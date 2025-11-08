"""
Add 'Teach Me Like I'm 10' section to all PR#50 lessons.

This script adds a dedicated content block that explains the lesson's core concepts
in simple terms suitable for a 10-year-old. The section is inserted as the second
content block (right after the opening explanation).
"""

import json
import os
import glob
import uuid
from typing import Dict, List

# List of all 53 PR#50 lesson files (from PR50_VALIDATION_REPORT.md)
PR50_LESSONS = [
    # AI Security (3 lessons)
    "lesson_ai_security_14_llm_prompt_injection_attacks_RICH.json",
    "lesson_ai_security_15_ai_model_poisoning_and_backdoors_RICH.json",
    "lesson_ai_security_16_adversarial_machine_learning_RICH.json",

    # Fundamentals (5 lessons)
    "lesson_fundamentals_21_cryptography_basics_for_cybersecurity_RICH.json",
    "lesson_fundamentals_22_security_frameworks_overview_nist_csf_and_iso_27001_RICH.json",
    "lesson_fundamentals_23_vulnerability_management_lifecycle_RICH.json",
    "lesson_fundamentals_24_zero_trust_architecture_principles_RICH.json",
    "lesson_fundamentals_25_secure_software_development_lifecycle_ssdlc_RICH.json",

    # Malware (10 lessons)
    "lesson_malware_22_static_malware_analysis_with_ida_pro_RICH.json",
    "lesson_malware_23_dynamic_malware_analysis_sandbox_setup_RICH.json",
    "lesson_malware_24_malware_persistence_mechanisms_RICH.json",
    "lesson_malware_25_ransomware_analysis_and_decryption_RICH.json",
    "lesson_malware_26_fileless_malware_and_living_off_the_land_RICH.json",
    "lesson_malware_27_mobile_malware_analysis_android_RICH.json",
    "lesson_malware_28_macos_malware_analysis_RICH.json",
    "lesson_malware_29_malware_c2_communication_analysis_RICH.json",
    "lesson_malware_30_behavioral_analysis_with_procmon_and_api_monitor_RICH.json",
    "lesson_malware_31_yara_rules_for_malware_detection_RICH.json",

    # Pentest (7 lessons)
    "lesson_pentest_63_web_application_firewall_waf_bypass_techniques_RICH.json",
    "lesson_pentest_64_graphql_api_security_testing_RICH.json",
    "lesson_pentest_65_server_side_request_forgery_ssrf_exploitation_RICH.json",
    "lesson_pentest_66_xml_external_entity_xxe_attacks_RICH.json",
    "lesson_pentest_67_insecure_deserialization_exploits_RICH.json",
    "lesson_pentest_68_oauth_2_0_and_oidc_security_testing_RICH.json",
    "lesson_pentest_69_saml_authentication_bypass_RICH.json",

    # Red Team (8 lessons)
    "lesson_red_team_27_c2_framework_comparison_cobalt_strike_vs_sliver_vs_havoc_RICH.json",
    "lesson_red_team_28_red_team_infrastructure_setup_RICH.json",
    "lesson_red_team_29_opsec_for_red_teams_RICH.json",
    "lesson_red_team_30_physical_security_assessment_RICH.json",
    "lesson_red_team_31_wi_fi_penetration_testing_RICH.json",
    "lesson_red_team_32_phishing_campaign_development_RICH.json",
    "lesson_red_team_33_adversary_emulation_with_caldera_RICH.json",
    "lesson_red_team_34_red_team_reporting_and_deconfliction_RICH.json",

    # System (15 lessons)
    "lesson_system_23_windows_services_security_RICH.json",
    "lesson_system_24_windows_scheduled_tasks_security_RICH.json",
    "lesson_system_25_windows_authentication_protocols_deep_dive_RICH.json",
    "lesson_system_26_powershell_for_system_administration_RICH.json",
    "lesson_system_27_bash_scripting_for_security_automation_RICH.json",
    "lesson_system_28_windows_internals_process_and_thread_management_RICH.json",
    "lesson_system_29_linux_kernel_security_RICH.json",
    "lesson_system_30_hardware_security_and_tpm_RICH.json",
    "lesson_system_31_firmware_analysis_and_security_RICH.json",
    "lesson_system_32_windows_access_control_lists_acls_RICH.json",
    "lesson_system_33_linux_process_management_and_forensics_RICH.json",
    "lesson_system_34_windows_driver_security_RICH.json",
    "lesson_system_35_container_security_docker_containerd_RICH.json",
    "lesson_system_36_windows_wmi_security_RICH.json",
    "lesson_system_37_systemd_security_on_linux_RICH.json",

    # Threat Hunting (5 lessons)
    "lesson_threat_hunting_31_hunting_for_lateral_movement_RICH.json",
    "lesson_threat_hunting_32_hunting_for_data_exfiltration_RICH.json",
    "lesson_threat_hunting_33_hunting_for_persistence_mechanisms_RICH.json",
    "lesson_threat_hunting_34_hunting_with_sysmon_RICH.json",
    "lesson_threat_hunting_35_mitre_att_ck_navigator_for_threat_hunting_RICH.json",
]


def create_teach_like_im_10_block(lesson_title: str, concepts: List[str]) -> Dict:
    """
    Create a 'Teach Me Like I'm 10' content block with simple explanations.

    This generates age-appropriate analogies and explanations for the lesson topic.
    """

    # Topic-specific simple explanations
    topic_explanations = {
        # AI Security
        "llm prompt injection": "Imagine you have a really smart robot assistant that follows instructions. Prompt injection is like tricking the robot by sneaking secret instructions into your regular questions - kind of like when you ask your parents 'Can I have ice cream?' but you already put ice cream in your backpack! The robot gets confused and does things it's not supposed to do.",

        "ai model poisoning": "Think of teaching a dog tricks. If someone sneaks in and teaches your dog the WRONG tricks when you're not looking, the dog will do the wrong things forever! AI model poisoning is when bad guys sneak bad lessons into an AI's training, so it learns the wrong way to do things.",

        "adversarial machine learning": "You know how optical illusions trick your eyes? Adversarial machine learning is like creating optical illusions for computers. You add tiny changes to a picture that you can't see, but they make the computer see something totally different - like making it think a stop sign is a speed limit sign!",

        # Fundamentals
        "cryptography": "Cryptography is like having a secret code with your best friend. You write messages that look like gibberish to everyone else, but your friend knows the secret decoder ring to read them. It keeps your secrets safe even if someone steals your note!",

        "security frameworks": "A security framework is like a recipe book for keeping things safe. Just like a cookbook tells you step-by-step how to make cookies, these frameworks tell companies step-by-step how to protect their computers and data from bad guys.",

        "vulnerability management": "Think of your house having broken locks and windows. Vulnerability management is like having a handyman who checks your house every week, makes a list of everything broken, and fixes the most dangerous problems first - like that back door that won't lock!",

        "zero trust": "Usually, once you're inside a building, you can go anywhere. Zero Trust is like a building where you need to show your ID badge at EVERY door, even inside! You can't just walk around freely - you have to prove who you are at each step.",

        "secure software development": "Imagine building a treehouse. Normally you build it first, THEN check if it's safe. Secure development is like checking for safety at EVERY step - making sure each board is strong BEFORE nailing it in, not after the treehouse is built!",

        # Malware
        "static malware analysis": "It's like being a detective who figures out what a suspicious package does WITHOUT opening it. You look at the outside, weigh it, X-ray it, and read any labels - all without touching what's inside!",

        "dynamic malware analysis": "This is like opening that suspicious package, but doing it inside a super-safe bomb disposal box. You can see what it does when it opens, but it can't hurt anything because it's trapped in a special container.",

        "malware persistence": "Imagine a really annoying fly that keeps coming back no matter how many times you swat it away. Malware persistence is when bad programs hide little copies of themselves all over your computer, so even if you delete them, they pop back up!",

        "ransomware": "Ransomware is like a bully who sneaks into your room, puts all your toys in a locked safe, and says 'Give me your lunch money or you'll never see your toys again!' It locks all your files and demands money to unlock them.",

        "fileless malware": "Most malware is like hiding toys under your bed - someone can find them if they look. Fileless malware is like juggling - the balls are always in the air, never touching the ground, so no one can catch them! It hides in your computer's memory instead of files.",

        "mobile malware": "Your phone is like a mini-computer in your pocket. Mobile malware is like bad apps that pretend to be games but secretly read your messages, listen to your calls, or steal your photos. Like a fake toy that's actually a spy device!",

        "macos malware": "Mac computers are like houses with really good locks. Mac malware is created by burglars who figured out how to pick those special locks. Just because Macs are safer doesn't mean they're impossible to break into!",

        "c2 communication": "C2 is like a walkie-talkie between a bad guy and his robot helpers hiding in your computer. The bad guy sends secret messages through the walkie-talkie telling the robots what to do - steal files, spy on you, or attack others.",

        "behavioral analysis": "Instead of looking at what a program looks like, we watch what it DOES - like watching if someone sneaks around, tries doors, and takes things that aren't theirs. Their behavior shows they're a burglar even if they look normal!",

        "yara rules": "YARA rules are like 'Wanted' posters for bad software. They say 'If you see a program that looks like THIS, does THAT, and has THESE words in it - that's a bad guy!' It helps computers recognize malware automatically.",

        # Pentest
        "waf bypass": "A WAF is like a security guard checking what you bring into a building. WAF bypass is figuring out clever ways to sneak things past the guard - like hiding stuff in a cake or putting it in a fancy box the guard doesn't check!",

        "graphql": "GraphQL is like ordering at a restaurant where you can ask for EXACTLY what you want, not a set meal. Security testing it is like finding if you can order secret menu items or peek into the kitchen by asking in special ways.",

        "ssrf": "SSRF is like tricking a waiter into going to the kitchen and bringing back secret recipes for you. You're not allowed in the kitchen, but if you trick the waiter (the server), they'll fetch things for you!",

        "xxe attacks": "XXE is like putting a secret note inside a book that says 'go read my diary and tell this person what it says.' When someone opens the book (XML file), it follows the secret instruction and reveals things it shouldn't!",

        "insecure deserialization": "Imagine you receive a LEGO set. Deserialization is building it. Insecure deserialization is when someone swaps the instructions so instead of building a house, you accidentally build a trap! The pieces look normal but build something dangerous.",

        "oauth": "OAuth is like giving a valet your car key that ONLY works for parking - it can't open the trunk or glove box. We test if hackers can trick the valet key into doing more than it should, like opening everything!",

        "saml": "SAML is like a special backstage pass that works at multiple concerts. It proves you're allowed backstage without needing a different pass for each venue. We test if fake passes can get through or if stolen passes still work.",

        # Red Team
        "c2 framework": "A C2 framework is like a remote control for hacking tools. Just like you use a remote to control a toy car, hackers use C2 frameworks to control their hacking programs from far away. We test which remote is best!",

        "red team infrastructure": "This is like setting up a secret hideout before a game of spies and seekers. You need walkie-talkies that can't be tracked, disguises, and safe places to hide - all set up BEFORE you start the mission!",

        "opsec": "OPSEC is like making sure you don't leave clues when playing hide-and-seek. Don't leave footprints, don't make noise, don't leave your jacket behind - don't do ANYTHING that tells people where you are or what you're doing!",

        "physical security": "This is about testing if you can sneak into a building like a spy movie! Can you tailgate behind someone? Can you pick locks? Can you trick the receptionist? We find weaknesses in real-world security, not just computer security!",

        "wi-fi pentesting": "WiFi is invisible internet waves around you. WiFi pentesting is like trying to listen to your neighbor's conversations through the wall, or sneaking onto their WiFi without the password, to show them their WiFi isn't safe!",

        "phishing campaign": "Phishing is like sending fake letters that look like they're from your school or parents, trying to trick people into giving away secrets or clicking on traps. We create fake ones to teach people how to spot the real bad ones!",

        "adversary emulation": "This is like playing pretend where you act EXACTLY like a real burglar to test your home's security. You use the same tools, same tricks, and same sneaky methods real bad guys use, so you can find the holes in security!",

        "red team reporting": "After playing security tester (ethical hacker), you need to write a report card explaining what you found - what worked, what didn't, and how to fix problems. It's like showing your work in math class!",

        # System
        "windows services": "Windows services are like invisible robot helpers that start working when your computer turns on - even before you log in! Some are good (like security guards), but bad guys try to sneak in bad robot helpers!",

        "scheduled tasks": "Scheduled tasks are like setting an alarm clock for your computer. 'Every day at 3pm, do THIS.' We make sure bad guys haven't set secret alarms that tell the computer to do bad things!",

        "windows authentication": "Authentication is proving you're really you. Windows has different ways to check - like showing your ID, fingerprint, or secret password. We learn about all the different proof methods and how to keep them safe!",

        "powershell": "PowerShell is like magic words that control Windows computers. Instead of clicking buttons, you type commands that make the computer do powerful things. It's like having admin superpowers through typing!",

        "bash scripting": "Bash is like PowerShell but for Linux computers. It's a special language where you write instructions for the computer to follow automatically, like giving a robot a to-do list!",

        "windows internals": "This is like learning how the inside of a car engine works. Most people just drive the car, but mechanics know about pistons, timing belts, and oil. Windows internals is knowing the 'engine' of Windows!",

        "linux kernel": "The kernel is like the brain of Linux. It controls EVERYTHING - memory, programs, devices. Kernel security is making sure the brain can't be tricked or taken over, because if the brain is hacked, everything is hacked!",

        "hardware security": "Most security is software (programs). Hardware security is about the physical chips and parts. TPM is like a safe built into your computer's motherboard that stores secrets even hackers with screwdrivers can't steal!",

        "firmware": "Firmware is like the computer's DNA - instructions permanently written into chips. It runs BEFORE Windows or Linux starts. Firmware analysis is checking if hackers hid bad instructions in the computer's DNA!",

        "acls": "ACLs are like permission slips for computer files. They say 'Alice can read this, Bob can edit it, Charlie can't touch it.' We make sure the permission slips are written correctly and can't be forged!",

        "linux process management": "A process is a program that's running. Process management is like being a conductor of an orchestra - starting programs, stopping them, seeing what each one is doing, and catching any that are acting suspicious!",

        "windows driver": "Drivers are like translators between Windows and your devices. Your printer driver translates 'print this' into language your printer understands. Bad drivers can be like evil translators that lie to both sides!",

        "container security": "Containers are like putting each app in its own playpen. Even if one app is bad, it can't escape the playpen to hurt other apps. We check if the playpens have holes or weak spots!",

        "wmi": "WMI is like Windows' control panel for admins. It lets you manage and monitor everything. But hackers LOVE it because if they get WMI access, they can control everything too - like stealing the TV remote!",

        "systemd": "Systemd is like Linux's manager that starts all the programs when the computer boots up. It's like a conductor saying 'First start this, then start that, if this crashes restart it.' We secure the conductor!",

        # Threat Hunting
        "lateral movement": "Once a bad guy sneaks into one computer in a network, lateral movement is when they jump from computer to computer like hopscotch, looking for the computer with the best stuff to steal!",

        "data exfiltration": "Exfiltration is a fancy word for sneaking data OUT. Like a spy stealing secret documents by hiding them in their briefcase, hackers find clever ways to steal data without triggering alarms!",

        "persistence mechanisms": "Persistence is how bad guys make sure they can come back even after you kick them out. It's like a burglar who hides a key under your doormat so they can sneak back in anytime!",

        "sysmon": "Sysmon is like a security camera system for Windows that records EVERYTHING happening on the computer. It helps us find bad guys by watching what programs do, what files they touch, and where they connect!",

        "mitre att&ck": "MITRE ATT&CK is like a huge encyclopedia of every trick hackers use. It lists hundreds of techniques from 'how to break in' to 'how to steal data.' We use it like a checklist to hunt for each type of attack!",
    }

    # Generate a simple explanation based on lesson title and concepts
    simple_text = ""

    # Try to find a matching explanation
    title_lower = lesson_title.lower()
    matched = False

    for keyword, explanation in topic_explanations.items():
        if keyword in title_lower:
            simple_text = explanation
            matched = True
            break

    # If no match found, create a generic but concept-specific explanation
    if not matched and concepts:
        first_concept = concepts[0].lower()
        simple_text = f"Imagine you're learning about {first_concept}. "

        if "attack" in first_concept or "exploit" in first_concept:
            simple_text += "This is like learning about how bad guys try to break into computers, so we can learn how to stop them. Think of it as studying how burglars work so you can build better locks!"
        elif "analysis" in first_concept:
            simple_text += "Analysis means carefully studying something to understand how it works. It's like being a detective who examines clues to solve a mystery!"
        elif "security" in first_concept or "protect" in first_concept:
            simple_text += "Security is about keeping things safe from bad guys. It's like having locks on your doors, alarm systems, and security cameras to protect your home!"
        elif "test" in first_concept or "hunting" in first_concept:
            simple_text += "This is about actively looking for problems before bad guys find them. Like checking if your bike lock works BEFORE someone tries to steal your bike!"
        else:
            simple_text += "We'll learn how this works in a simple, clear way that anyone can understand. Think of it as learning the basics first, then building up to the complicated stuff!"

    # Add a closing that ties to the actual lesson
    simple_text += f"\n\nIn this lesson, we'll learn about {lesson_title.lower()} in a way that makes sense. We'll start simple, use real examples, and build your understanding step by step. By the end, you'll understand the core ideas and why they matter!"

    # Create the content block
    block = {
        "block_id": str(uuid.uuid4()),
        "type": "explanation",
        "title": "Teach Me Like I'm 10",
        "content": {
            "text": simple_text
        }
    }

    return block


def add_teach_like_im_10_to_lesson(lesson_file: str) -> bool:
    """
    Add a 'Teach Me Like I'm 10' section to a single lesson.

    Returns True if successful, False otherwise.
    """
    try:
        # Read lesson file
        with open(lesson_file, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        # Check if already has a "Teach Me Like I'm 10" block
        for block in lesson.get('content_blocks', []):
            if block.get('title') == "Teach Me Like I'm 10":
                print(f"  [SKIP] Already has 'Teach Me Like I'm 10' section")
                return True

        # Create the new block
        new_block = create_teach_like_im_10_block(
            lesson.get('title', ''),
            lesson.get('concepts', [])
        )

        # Insert as second block (index 1)
        content_blocks = lesson.get('content_blocks', [])
        content_blocks.insert(1, new_block)
        lesson['content_blocks'] = content_blocks

        # Write back to file
        with open(lesson_file, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

        print(f"  [SUCCESS] Added 'Teach Me Like I'm 10' section")
        return True

    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        return False


def main():
    """Add 'Teach Me Like I'm 10' sections to all PR#50 lessons."""
    print("="*80)
    print("ADDING 'TEACH ME LIKE I'M 10' SECTIONS TO PR#50 LESSONS")
    print("="*80)
    print(f"\nProcessing {len(PR50_LESSONS)} lessons...\n")

    content_dir = "content"
    success_count = 0
    skip_count = 0
    error_count = 0

    for lesson_filename in PR50_LESSONS:
        lesson_path = os.path.join(content_dir, lesson_filename)

        print(f"\n{lesson_filename}")

        if not os.path.exists(lesson_path):
            print(f"  [ERROR] File not found")
            error_count += 1
            continue

        result = add_teach_like_im_10_to_lesson(lesson_path)

        if result:
            # Check if it was skipped or successful
            with open(lesson_path, 'r', encoding='utf-8') as f:
                lesson = json.load(f)
                # Count blocks - if it already had it, we skipped
                if len([b for b in lesson['content_blocks'] if b.get('title') == "Teach Me Like I'm 10"]) > 1:
                    skip_count += 1
                else:
                    success_count += 1
        else:
            error_count += 1

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nTotal Lessons: {len(PR50_LESSONS)}")
    print(f"Successfully Updated: {success_count}")
    print(f"Already Had Section: {skip_count}")
    print(f"Errors: {error_count}")

    if success_count > 0:
        print(f"\n[SUCCESS] Added 'Teach Me Like I'm 10' sections to {success_count} lessons!")
        print("\nNext steps:")
        print("1. Run validation: python validate_content_quality.py")
        print("2. Load lessons: python load_all_lessons.py")
        print("3. Test in app: streamlit run app.py")

    if error_count > 0:
        print(f"\n[WARNING] {error_count} lessons had errors. Review output above.")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())
