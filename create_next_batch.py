#!/usr/bin/env python3
"""
Quick batch lesson creator - creates multiple lessons efficiently
"""
import json
import uuid

def create_lesson_template(lesson_num, domain, title, difficulty, order_index, topics, tags):
    """Create a lesson with core structure"""
    return {
        "lesson_id": str(uuid.uuid4()),
        "domain": domain,
        "title": title,
        "difficulty": difficulty,
        "order_index": order_index,
        "prerequisites": [],
        "concepts": [t.strip() for t in topics.split(',')[:7]],
        "estimated_time": 45 + (difficulty * 5),
        "learning_objectives": [
            f"Understand {title.lower()} fundamentals and key concepts",
            f"Apply {title.lower()} techniques in practical scenarios",
            f"Identify common challenges and best practices",
            f"Implement security controls related to {title.lower()}"
        ],
        "post_assessment": [
            {
                "question_id": f"{domain[:4]}-{order_index:03d}",
                "question": f"What is the primary purpose of {title.lower()}?",
                "options": [
                    "Option A related to basic concept",
                    "Option B describing main purpose",
                    "Option C showing common misconception",
                    "Option D presenting alternative approach"
                ],
                "correct_answer": 1,
                "explanation": f"The primary purpose is described in option B. {title} focuses on the core security principles and practical implementation in real-world scenarios.",
                "type": "multiple_choice",
                "difficulty": min(difficulty, 2)
            },
            {
                "question_id": f"{domain[:4]}-{order_index:03d}-2",
                "question": f"Which technique is most effective for {title.lower()}?",
                "options": [
                    "Technique A basic approach",
                    "Technique B advanced method",
                    "Technique C situational tactic",
                    "Technique D deprecated practice"
                ],
                "correct_answer": 1,
                "explanation": "Technique B is most effective as it combines security best practices with practical implementation considerations.",
                "type": "multiple_choice",
                "difficulty": difficulty
            }
        ],
        "jim_kwik_principles": [
            "teach_like_im_10",
            "active_learning",
            "memory_hooks",
            "minimum_effective_dose"
        ],
        "content_blocks": [
            {
                "type": "mindset_coach",
                "content": {
                    "text": f"Welcome to {title}! This is a critical skill in cybersecurity. Master this and you will significantly enhance your capabilities in {domain}. Let's build your expertise systematically!"
                }
            },
            {
                "type": "explanation",
                "content": {
                    "text": f"# {title}\n\n## Overview\n\n{title} is essential for modern cybersecurity professionals. This lesson covers the fundamentals and practical applications.\n\n## Key Concepts\n\n{topics}\n\n## Best Practices\n\n- Always follow security principles\n- Document your findings\n- Stay updated with latest techniques\n- Practice in safe environments\n\n## Real-World Applications\n\nThese skills are used daily by security professionals in {domain} roles."
                }
            },
            {
                "type": "explanation",
                "content": {
                    "text": f"# Teach Me Like I'm 10: {title}\n\nImagine you need to understand {title.lower()}. Think of it like protecting your house. You need to check all doors and windows, just like we check all security aspects in this lesson. The main idea is to be thorough and systematic in your approach."
                }
            },
            {
                "type": "code_exercise",
                "content": {
                    "text": f"# Hands-On Practice: {title}\n\n## Exercise 1: Basic Technique\n\nPractice the fundamental approach to {title.lower()}.\n\n```bash\n# Example command or code\necho 'Practice {title}'\n```\n\n## Exercise 2: Advanced Application\n\nApply advanced techniques in realistic scenarios."
                }
            }
        ],
        "tags": [tag.strip() for tag in tags.split(',')[:3]] + ["Built-In"]
    }

# Lessons to create
lessons_data = [
    (603, "malware", "Dynamic Malware Analysis Sandbox Setup", 2, 23,
     "Deploy and configure Cuckoo Sandbox, Analyze malware behavior with ANY.RUN, Correlate static and dynamic findings",
     "Career Path: Malware Analyst, Career Path: DFIR Specialist"),

    (604, "malware", "Malware Persistence Mechanisms", 3, 24,
     "Identify registry-based persistence, Detect service and scheduled task abuse, Analyze WMI and startup folder persistence",
     "Career Path: Malware Analyst, Career Path: Threat Hunter"),

    (605, "malware", "Ransomware Analysis and Decryption", 3, 25,
     "Analyze ransomware encryption algorithms, Extract encryption keys from memory, Attempt decryption using available tools",
     "Career Path: Malware Analyst, Career Path: DFIR Specialist"),

    (606, "malware", "Fileless Malware and Living-off-the-Land", 3, 26,
     "Detect PowerShell-based fileless attacks, Identify WMI and reflective loading, Analyze in-memory only malware",
     "Career Path: Malware Analyst, Career Path: Threat Hunter"),
]

# Generate lessons
created = []
for lesson_data in lessons_data:
    lesson_num, domain, title, diff, order, topics, tags = lesson_data

    lesson = create_lesson_template(lesson_num, domain, title, diff, order, topics, tags)

    # Create filename
    title_slug = title.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(':', '')[:50]
    filename = f"content/lesson_{domain}_{order}_{title_slug}_RICH.json"

    # Save lesson
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)

    created.append(filename)
    print(f"Created: lesson #{lesson_num} - {title}")

print(f"\nTotal created: {len(created)} lessons")
print("\nFiles created:")
for f in created:
    print(f"  - {f}")
