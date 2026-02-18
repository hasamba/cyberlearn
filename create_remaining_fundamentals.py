import json
import uuid

# Generate lesson #600: Zero Trust Architecture
lesson_600 = {
  "lesson_id": str(uuid.uuid4()),
  "domain": "fundamentals",
  "title": "Zero Trust Architecture Principles",
  "difficulty": 2,
  "order_index": 24,
  "prerequisites": [],
  "concepts": [
    "Zero Trust philosophy never trust always verify",
    "Microsegmentation and network isolation",
    "Identity-centric security model",
    "Least privilege access control",
    "Continuous verification"
  ],
  "estimated_time": 50,
  "learning_objectives": [
    "Understand zero trust philosophy and core principles",
    "Implement never trust always verify security controls",
    "Design microsegmentation strategies",
    "Apply identity-centric security with continuous verification"
  ],
  "post_assessment": [
    {
      "question_id": "zt-001",
      "question": "What is the core principle of Zero Trust Architecture?",
      "options": [
        "Trust internal networks verify external",
        "Never trust always verify regardless of location",
        "Use stronger perimeter firewalls",
        "Trust authenticated users automatically"
      ],
      "correct_answer": 1,
      "explanation": "Zero Trust core principle is never trust always verify treating every access request as potentially hostile regardless of location. Traditional perimeter security assumes internal traffic is safe which fails against insider threats and lateral movement.",
      "type": "multiple_choice",
      "difficulty": 1
    }
  ],
  "jim_kwik_principles": ["teach_like_im_10", "active_learning", "memory_hooks"],
  "content_blocks": [
    {
      "type": "mindset_coach",
      "content": {
        "text": "Welcome to Zero Trust! Traditional castle and moat security assumes everything inside the network is trustworthy. But attackers who breach the perimeter move laterally freely. Zero Trust fixes this: never trust always verify every user device and request. This reshapes enterprise security!"
      }
    }
  ],
  "tags": ["Career Path: Security Engineer", "Career Path: Cloud Security", "Built-In"]
}

# Generate lesson #601: Secure SDLC
lesson_601 = {
  "lesson_id": str(uuid.uuid4()),
  "domain": "fundamentals",
  "title": "Secure Software Development Lifecycle (SSDLC)",
  "difficulty": 2,
  "order_index": 25,
  "prerequisites": [],
  "concepts": [
    "SDLC phases and security integration",
    "Shift-left security approach",
    "Threat modeling and security requirements",
    "Secure coding practices",
    "SAST and DAST testing"
  ],
  "estimated_time": 50,
  "learning_objectives": [
    "Integrate security into each SDLC phase",
    "Apply shift-left security principles",
    "Conduct threat modeling",
    "Implement secure coding practices",
    "Use SAST and DAST in CI/CD pipelines"
  ],
  "post_assessment": [
    {
      "question_id": "ssdlc-001",
      "question": "What does shift-left mean in secure software development?",
      "options": [
        "Move security testing to earlier phases",
        "Shift security responsibilities to developers",
        "Move security teams to the left side",
        "Use left-handed programming"
      ],
      "correct_answer": 0,
      "explanation": "Shift-left means moving security testing earlier in the development lifecycle. Instead of finding vulnerabilities in production catch them during design and coding. This is 10-100x less expensive and more effective.",
      "type": "multiple_choice",
      "difficulty": 1
    }
  ],
  "jim_kwik_principles": ["teach_like_im_10", "active_learning", "memory_hooks"],
  "content_blocks": [
    {
      "type": "mindset_coach",
      "content": {
        "text": "Welcome to Secure SDLC! Fixing security bugs costs 100x more in production than during design. Most vulnerabilities are introduced during development yet testing happens at the end. SSDLC integrates security throughout preventing vulnerabilities before production!"
      }
    }
  ],
  "tags": ["Career Path: Security Engineer", "Career Path: Application Security", "Built-In"]
}

# Save both lessons
with open('content/lesson_fundamentals_24_zero_trust_architecture_RICH.json', 'w', encoding='utf-8') as f:
    json.dump(lesson_600, f, indent=2, ensure_ascii=False)

with open('content/lesson_fundamentals_25_secure_sdlc_RICH.json', 'w', encoding='utf-8') as f:
    json.dump(lesson_601, f, indent=2, ensure_ascii=False)

print("Created lesson #600: Zero Trust Architecture Principles")
print("Created lesson #601: Secure Software Development Lifecycle")
print("\nFundamentals domain complete: 5 lessons")
