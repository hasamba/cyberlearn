"""
Generate comprehensive cybersecurity lessons
"""

import json
from uuid import uuid4
from datetime import datetime

# Lesson curriculum structure
LESSON_CURRICULUM = {
    "fundamentals": [
        {
            "title": "Authentication vs Authorization",
            "subtitle": "Understanding the difference between identity and access",
            "difficulty": 1,
            "order": 2,
            "concepts": ["Authentication", "Authorization", "AAA model", "Access Control"],
            "quiz": [
                {
                    "q": "What is authentication?",
                    "opts": ["Verifying identity", "Granting access", "Encrypting data", "Logging events"],
                    "correct": 0,
                    "explanation": "Authentication is the process of verifying WHO you are (identity), not what you can do."
                },
                {
                    "q": "Which is an example of authorization?",
                    "opts": ["Entering password", "File permissions", "Fingerprint scan", "Security questions"],
                    "correct": 1,
                    "explanation": "File permissions determine WHAT you can do (authorization), not WHO you are."
                }
            ]
        },
        {
            "title": "Encryption Fundamentals",
            "subtitle": "Protecting data confidentiality through cryptography",
            "difficulty": 2,
            "order": 3,
            "concepts": ["Symmetric encryption", "Asymmetric encryption", "Hashing", "Keys"],
            "quiz": [
                {
                    "q": "What is symmetric encryption?",
                    "opts": ["Same key for encrypt/decrypt", "Different keys", "No key needed", "One-way only"],
                    "correct": 0,
                    "explanation": "Symmetric encryption uses the SAME key to encrypt and decrypt data (like AES)."
                }
            ]
        },
        {
            "title": "Network Security Basics",
            "subtitle": "Protecting data in transit",
            "difficulty": 2,
            "order": 4,
            "concepts": ["Firewalls", "VPNs", "SSL/TLS", "Network segmentation"],
            "quiz": [
                {
                    "q": "What does a firewall do?",
                    "opts": ["Encrypts files", "Filters network traffic", "Scans for viruses", "Backs up data"],
                    "correct": 1,
                    "explanation": "Firewalls filter network traffic based on rules, blocking unauthorized connections."
                }
            ]
        },
        {
            "title": "Threat Landscape Overview",
            "subtitle": "Understanding cyber threats and attackers",
            "difficulty": 2,
            "order": 5,
            "concepts": ["Threat actors", "Attack vectors", "Threat intelligence", "APTs"],
            "quiz": [
                {
                    "q": "What is an APT?",
                    "opts": ["Antivirus Program", "Advanced Persistent Threat", "Automated Patch Tool", "Application Protocol"],
                    "correct": 1,
                    "explanation": "APT = Advanced Persistent Threat: sophisticated, long-term targeted attacks."
                }
            ]
        }
    ],
    "dfir": [
        {
            "title": "Introduction to Digital Forensics",
            "subtitle": "Collecting and analyzing digital evidence",
            "difficulty": 1,
            "order": 1,
            "concepts": ["Digital evidence", "Forensic process", "Evidence handling", "Court admissibility"],
            "quiz": [
                {
                    "q": "What is digital forensics?",
                    "opts": ["Hacking systems", "Analyzing digital evidence", "Installing software", "Network monitoring"],
                    "correct": 1,
                    "explanation": "Digital forensics involves collecting, preserving, and analyzing digital evidence."
                }
            ]
        },
        {
            "title": "Chain of Custody",
            "subtitle": "Maintaining evidence integrity",
            "difficulty": 2,
            "order": 2,
            "concepts": ["Evidence tracking", "Documentation", "Legal requirements", "Integrity"],
            "quiz": [
                {
                    "q": "Why is chain of custody critical?",
                    "opts": ["Faster analysis", "Legal admissibility", "Better tools", "More storage"],
                    "correct": 1,
                    "explanation": "Chain of custody ensures evidence is legally admissible by proving it wasn't tampered with."
                }
            ]
        },
        {
            "title": "Incident Response Process",
            "subtitle": "Structured approach to security incidents",
            "difficulty": 2,
            "order": 3,
            "concepts": ["IR lifecycle", "Preparation", "Detection", "Containment", "Eradication", "Recovery"],
            "quiz": [
                {
                    "q": "What is the first phase of incident response?",
                    "opts": ["Eradication", "Recovery", "Preparation", "Lessons learned"],
                    "correct": 2,
                    "explanation": "Preparation comes first - having plans, tools, and training BEFORE incidents occur."
                }
            ]
        }
    ],
    "malware": [
        {
            "title": "Malware Types and Classifications",
            "subtitle": "Understanding different types of malicious software",
            "difficulty": 1,
            "order": 1,
            "concepts": ["Viruses", "Worms", "Trojans", "Ransomware", "Spyware"],
            "quiz": [
                {
                    "q": "What distinguishes a worm from a virus?",
                    "opts": ["Worms need user action", "Worms self-replicate", "Worms are less dangerous", "Worms only affect Windows"],
                    "correct": 1,
                    "explanation": "Worms self-replicate across networks without needing a host file or user action."
                }
            ]
        },
        {
            "title": "Static Malware Analysis",
            "subtitle": "Analyzing malware without execution",
            "difficulty": 2,
            "order": 2,
            "concepts": ["File analysis", "Strings extraction", "PE headers", "Hashing"],
            "quiz": [
                {
                    "q": "What is static analysis?",
                    "opts": ["Running malware in sandbox", "Examining code without execution", "Network monitoring", "Memory dumping"],
                    "correct": 1,
                    "explanation": "Static analysis examines malware code, strings, and structure WITHOUT executing it."
                }
            ]
        },
        {
            "title": "Dynamic Malware Analysis",
            "subtitle": "Observing malware behavior in controlled environment",
            "difficulty": 3,
            "order": 3,
            "concepts": ["Sandboxing", "Behavioral analysis", "Network capture", "System monitoring"],
            "quiz": [
                {
                    "q": "What is a sandbox in malware analysis?",
                    "opts": ["A type of malware", "Isolated environment for safe execution", "Antivirus software", "Network firewall"],
                    "correct": 1,
                    "explanation": "A sandbox is an isolated environment where malware can be safely executed and observed."
                }
            ]
        }
    ],
    "active_directory": [
        {
            "title": "Active Directory Fundamentals",
            "subtitle": "Understanding Microsoft's directory service",
            "difficulty": 1,
            "order": 1,
            "concepts": ["Domain", "Domain Controller", "Organizational Units", "Objects"],
            "quiz": [
                {
                    "q": "What is Active Directory primarily used for?",
                    "opts": ["Web hosting", "Identity and access management", "Antivirus", "File storage"],
                    "correct": 1,
                    "explanation": "Active Directory is Microsoft's directory service for managing identities and access in Windows environments."
                }
            ]
        },
        {
            "title": "Group Policy Essentials",
            "subtitle": "Centralized configuration management",
            "difficulty": 2,
            "order": 2,
            "concepts": ["GPO", "Policy inheritance", "Security settings", "User/Computer policies"],
            "quiz": [
                {
                    "q": "What does Group Policy allow?",
                    "opts": ["Create user groups", "Centrally manage Windows settings", "Share files", "Install antivirus"],
                    "correct": 1,
                    "explanation": "Group Policy enables centralized management of Windows settings across the domain."
                }
            ]
        },
        {
            "title": "Kerberos Authentication",
            "subtitle": "Understanding AD's authentication protocol",
            "difficulty": 3,
            "order": 3,
            "concepts": ["Tickets", "TGT", "Service tickets", "KDC"],
            "quiz": [
                {
                    "q": "What is Kerberos?",
                    "opts": ["A password manager", "Ticket-based authentication protocol", "A firewall", "An antivirus"],
                    "correct": 1,
                    "explanation": "Kerberos is a ticket-based authentication protocol used by Active Directory."
                }
            ]
        }
    ],
    "pentest": [
        {
            "title": "Penetration Testing Methodology",
            "subtitle": "Systematic approach to security testing",
            "difficulty": 1,
            "order": 1,
            "concepts": ["Reconnaissance", "Scanning", "Exploitation", "Post-exploitation", "Reporting"],
            "quiz": [
                {
                    "q": "What is the goal of penetration testing?",
                    "opts": ["Break systems permanently", "Identify and report vulnerabilities", "Install backdoors", "Steal data"],
                    "correct": 1,
                    "explanation": "Penetration testing aims to find and report vulnerabilities so they can be fixed."
                }
            ]
        },
        {
            "title": "Reconnaissance Techniques",
            "subtitle": "Gathering information about targets",
            "difficulty": 2,
            "order": 2,
            "concepts": ["OSINT", "Passive recon", "Active recon", "Footprinting"],
            "quiz": [
                {
                    "q": "What is OSINT?",
                    "opts": ["A hacking tool", "Open Source Intelligence gathering", "Operating system", "Antivirus"],
                    "correct": 1,
                    "explanation": "OSINT = Open Source Intelligence: gathering info from publicly available sources."
                }
            ]
        },
        {
            "title": "Exploitation Fundamentals",
            "subtitle": "Understanding vulnerability exploitation",
            "difficulty": 3,
            "order": 3,
            "concepts": ["Exploits", "Payloads", "Shells", "Privilege escalation"],
            "quiz": [
                {
                    "q": "What is privilege escalation?",
                    "opts": ["Adding users", "Gaining higher-level access", "Faster authentication", "Password reset"],
                    "correct": 1,
                    "explanation": "Privilege escalation means gaining higher-level access rights than initially obtained."
                }
            ]
        }
    ]
}

def generate_lesson_json(domain, lesson_data, lesson_num):
    """Generate a complete lesson JSON structure"""

    lesson_id = str(uuid4())
    block_id = str(uuid4())

    return {
        "lesson_id": lesson_id,
        "domain": domain,
        "title": lesson_data["title"],
        "subtitle": lesson_data["subtitle"],
        "difficulty": lesson_data["difficulty"],
        "estimated_time": 25,
        "order_index": lesson_data["order"],
        "prerequisites": [],
        "learning_objectives": [
            f"Understand {concept}" for concept in lesson_data["concepts"][:3]
        ],
        "content_blocks": [
            {
                "block_id": block_id,
                "type": "explanation",
                "title": lesson_data["title"],
                "content": {
                    "text": f"This lesson covers {', '.join(lesson_data['concepts'])}. You'll learn the fundamentals and practical applications."
                },
                "simplified_explanation": f"Think of this like {lesson_data['concepts'][0]} in everyday life...",
                "memory_aids": [
                    f"Remember: {lesson_data['concepts'][0]}",
                    f"Tip: {lesson_data['concepts'][1] if len(lesson_data['concepts']) > 1 else 'Key concept'}"
                ],
                "real_world_connection": f"In real-world scenarios, {lesson_data['concepts'][0]} is used daily by security professionals.",
                "reflection_prompt": "What questions do you have about this topic?",
                "is_interactive": False,
                "xp_reward": 0
            }
        ],
        "pre_assessment": None,
        "post_assessment": [
            {
                "question_id": f"q{i+1}",
                "type": "multiple_choice",
                "question": q["q"],
                "options": q["opts"],
                "correct_answer": q["correct"],
                "explanation": q["explanation"],
                "difficulty": lesson_data["difficulty"],
                "memory_aid": f"Remember: {lesson_data['concepts'][0]}",
                "points": 10
            }
            for i, q in enumerate(lesson_data["quiz"])
        ],
        "mastery_threshold": 80,
        "jim_kwik_principles": [
            "active_learning",
            "teach_like_im_10",
            "memory_hooks",
            "connect_to_what_i_know"
        ],
        "base_xp_reward": 100 * lesson_data["difficulty"],
        "badge_unlock": None,
        "is_core_concept": lesson_data["difficulty"] <= 2,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "author": "CyberLearn Curriculum Team",
        "version": "1.0"
    }


def generate_all_lessons():
    """Generate all lesson files"""

    print("=" * 60)
    print("Generating CyberLearn Lessons")
    print("=" * 60)

    total = 0

    for domain, lessons in LESSON_CURRICULUM.items():
        print(f"\n📁 {domain.upper()}: {len(lessons)} lessons")

        for idx, lesson_data in enumerate(lessons, 1):
            lesson_json = generate_lesson_json(domain, lesson_data, idx)

            filename = f"content/lesson_{domain}_{idx:02d}_{lesson_data['title'].replace(' ', '_').lower()}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(lesson_json, f, indent=2)

            print(f"  ✅ {lesson_data['title']}")
            total += 1

    print("\n" + "=" * 60)
    print(f"✅ Generated {total} lessons")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python load_all_lessons.py")
    print("2. Run: streamlit run app.py")
    print("3. Login and see all lessons!")


if __name__ == "__main__":
    generate_all_lessons()
