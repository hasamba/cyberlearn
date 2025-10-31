# Lesson Generator Quick Reference

## Quick Copy-Paste Templates

### Valid Domains (15 total)
```
dfir, malware, active_directory, system, cloud, pentest, red_team, blue_team,
osint, threat_hunting, linux, fundamentals, ai_security, iot_security, web3_security
```

### Valid Jim Kwik Principles
```json
[
  "active_learning",
  "minimum_effective_dose",
  "teach_like_im_10",
  "memory_hooks",
  "meta_learning",
  "connect_to_what_i_know",
  "reframe_limiting_beliefs",
  "gamify_it",
  "learning_sprint",
  "multiple_memory_pathways"
]
```

### Valid Content Block Types
```
explanation, video, diagram, quiz, simulation, reflection,
memory_aid, real_world, code_exercise, mindset_coach
```

### Post-Assessment Question Template
```json
{
  "question_id": "topic-001",
  "question": "Your question here?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_answer": 1,
  "explanation": "Detailed explanation of why this is correct.",
  "type": "multiple_choice",
  "difficulty": 2
}
```

### Content Block Template
```json
{
  "type": "explanation",
  "content": {
    "text": "Your markdown content here..."
  }
}
```

### UUID Generation
Use online tool or Python:
```python
import uuid
str(uuid.uuid4())  # e.g., "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
```

## Validation Errors - Quick Fixes

| Error | Fix |
|-------|-----|
| Missing `question_id` | Add unique ID to each question |
| Missing `type` | Add `"type": "multiple_choice"` |
| Missing `difficulty` | Add `"difficulty": 1/2/3` |
| Invalid jim_kwik_principle | Use ONLY the 10 valid enum values |
| Invalid content type | Use ONLY the 10 valid content block types |
| Content not dict | Wrap in `{"text": "..."}` |

## Typical Lesson Structure (7 content blocks)

1. **mindset_coach** - Opening motivation
2. **explanation** - Main technical content (4000+ words)
3. **code_exercise** - Hands-on commands/scripts
4. **real_world** - Case study from actual breach
5. **memory_aid** - Mnemonics/acronyms
6. **reflection** - Critical thinking questions
7. **mindset_coach** - Closing celebration

## Word Count Guidelines

- **Beginner (difficulty 1)**: 4,000-6,000 words
- **Intermediate (difficulty 2)**: 6,000-10,000 words
- **Advanced (difficulty 3)**: 10,000-15,000 words

## Testing Your Lesson

```bash
# Load into database
python load_all_lessons.py

# Check for errors
grep "ERROR" <output>

# If errors, run comprehensive fix
python comprehensive_fix.py
```

## Common Course Tags

```json
"tags": ["Course: 13Cubed-Investigating Linux Devices"]
"tags": ["Course: SANS-FOR500"]
"tags": ["Course: SANS-FOR508"]
"tags": ["Course: OWASP LLM Top 10"]
```
