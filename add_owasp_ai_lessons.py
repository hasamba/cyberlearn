"""
Add OWASP AI Security Top 10 lessons to lesson_ideas.csv

OWASP LLM Top 10 (2025):
1. LLM01: Prompt Injection
2. LLM02: Sensitive Information Disclosure
3. LLM03: Supply Chain Vulnerabilities
4. LLM04: Data and Model Poisoning
5. LLM05: Improper Output Handling
6. LLM06: Excessive Agency
7. LLM07: System Prompt Leakage
8. LLM08: Vector and Embedding Weaknesses
9. LLM09: Misinformation
10. LLM10: Unbounded Consumption
"""

import csv
from pathlib import Path

def add_owasp_ai_lessons():
    """Add OWASP AI Security Top 10 lessons to lesson_ideas.csv"""

    csv_file = Path('lesson_ideas.csv')

    # OWASP AI Top 10 lessons
    owasp_lessons = [
        {
            'lesson_number': '',  # Will be auto-numbered
            'order_index': 4,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM01: Prompt Injection Attacks and Defenses',
            'module': 'OWASP AI Top 10',
            'topics': 'Direct prompt injection, indirect prompt injection, jailbreaking, prompt injection detection, input validation, output filtering, defense-in-depth',
            'prerequisites': '[1,2,3]',  # Assumes first 3 AI lessons exist
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'Critical vulnerability - manipulating LLM behavior through crafted inputs'
        },
        {
            'lesson_number': '',
            'order_index': 5,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM02: Sensitive Information Disclosure',
            'module': 'OWASP AI Top 10',
            'topics': 'Training data leakage, PII exposure, model inversion attacks, membership inference, data sanitization, differential privacy',
            'prerequisites': '[1,2,3]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'LLMs may leak sensitive data from training sets or user inputs'
        },
        {
            'lesson_number': '',
            'order_index': 6,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM03: Supply Chain Vulnerabilities',
            'module': 'OWASP AI Top 10',
            'topics': 'Third-party model risks, plugin security, data poisoning via supply chain, model provenance, dependency management, SBOM for AI',
            'prerequisites': '[1,2,3]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'Risks from third-party models, datasets, and plugins'
        },
        {
            'lesson_number': '',
            'order_index': 7,
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'OWASP LLM04: Data and Model Poisoning',
            'module': 'OWASP AI Top 10',
            'topics': 'Training data poisoning, backdoor attacks, adversarial examples, federated learning attacks, data validation, robust training',
            'prerequisites': '[1,2,3,4]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'Manipulating training data or fine-tuning to compromise model behavior'
        },
        {
            'lesson_number': '',
            'order_index': 8,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM05: Improper Output Handling',
            'module': 'OWASP AI Top 10',
            'topics': 'XSS via LLM output, injection attacks, unsafe code execution, output validation, sandboxing, content security policy',
            'prerequisites': '[1,2,3]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'LLM outputs used without proper validation can lead to injection attacks'
        },
        {
            'lesson_number': '',
            'order_index': 9,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM06: Excessive Agency',
            'module': 'OWASP AI Top 10',
            'topics': 'Over-permissioned LLMs, plugin abuse, unintended actions, principle of least privilege, action validation, human-in-the-loop',
            'prerequisites': '[1,2,3]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'LLM-based systems granted too much autonomy or dangerous capabilities'
        },
        {
            'lesson_number': '',
            'order_index': 10,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM07: System Prompt Leakage',
            'module': 'OWASP AI Top 10',
            'topics': 'System prompt extraction, role revelation, instruction leakage, prompt protection techniques, obfuscation, detection',
            'prerequisites': '[1,2,3,4]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'Attackers extract system prompts to understand and exploit LLM behavior'
        },
        {
            'lesson_number': '',
            'order_index': 11,
            'domain': 'ai_security',
            'difficulty': 3,
            'title': 'OWASP LLM08: Vector and Embedding Weaknesses',
            'module': 'OWASP AI Top 10',
            'topics': 'RAG poisoning, vector database attacks, embedding manipulation, semantic search bypass, vector store security',
            'prerequisites': '[1,2,3]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'Attacks targeting vector databases and RAG systems'
        },
        {
            'lesson_number': '',
            'order_index': 12,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM09: Misinformation and Hallucination',
            'module': 'OWASP AI Top 10',
            'topics': 'LLM hallucinations, factual incorrectness, confidence calibration, source attribution, fact-checking, adversarial misinformation',
            'prerequisites': '[1,2,3]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'LLMs generating false or misleading information with confidence'
        },
        {
            'lesson_number': '',
            'order_index': 13,
            'domain': 'ai_security',
            'difficulty': 2,
            'title': 'OWASP LLM10: Unbounded Consumption',
            'module': 'OWASP AI Top 10',
            'topics': 'Denial of service via LLM, resource exhaustion, cost attacks, rate limiting, quotas, circuit breakers, monitoring',
            'prerequisites': '[1,2,3]',
            'status': 'planned',
            'course_tag': 'Course: OWASP LLM Top 10',
            'notes': 'Resource exhaustion through excessive LLM usage or complex queries'
        }
    ]

    # Read existing CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_lessons = list(reader)
        fieldnames = reader.fieldnames

    # Add new lessons
    print(f"Adding {len(owasp_lessons)} OWASP AI Security Top 10 lessons...\n")

    for i, lesson in enumerate(owasp_lessons, 1):
        existing_lessons.append(lesson)
        print(f"[{i:2d}] {lesson['title']}")

    # Write back to CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_lessons)

    print(f"\n✓ Successfully added {len(owasp_lessons)} lessons to lesson_ideas.csv")
    print(f"  Total lessons in file: {len(existing_lessons)}")
    print(f"\nCourse tag: 'Course: OWASP LLM Top 10'")
    print(f"Domain: ai_security")
    print(f"Order indices: 4-13 (assumes lessons 1-3 are AI fundamentals)")


if __name__ == "__main__":
    print("=== Adding OWASP AI Security Top 10 Lessons ===\n")
    add_owasp_ai_lessons()
    print("\n=== Complete ===")
