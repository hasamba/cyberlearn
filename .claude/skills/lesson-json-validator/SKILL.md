---
name: lesson-json-validator
description: Validate CyberLearn lesson JSON files and suggest fixes for validation errors
version: 1.0
auto_invoke: true
---

# Lesson JSON Validator Skill

Automatically validate lesson JSON files and provide actionable fix suggestions.

## When to Use

Automatically invoke when:
- User creates or modifies a lesson file
- User asks to "validate lesson X"
- User runs into validation errors
- Before committing lesson files to git

## Validation Process

1. **Read the lesson JSON file**
   ```bash
   content/lesson_<domain>_<order>_<slug>_RICH.json
   ```

2. **Check all required fields**:
   - `lesson_id` (valid UUID format)
   - `domain` (one of 15 valid domains)
   - `title` (non-empty string)
   - `difficulty` (1, 2, or 3)
   - `order_index` (positive integer)
   - `prerequisites` (array of UUID strings)
   - `concepts` (array of strings)
   - `estimated_time` (30-60 minutes)
   - `learning_objectives` (array of strings)
   - `post_assessment` (array with ≥3 questions)
   - `jim_kwik_principles` (array with valid enum values)
   - `content_blocks` (array with ≥4 blocks)
   - `tags` (array of strings)

3. **Validate post_assessment questions**:
   Each question MUST have:
   - `question_id` (string, unique)
   - `question` (string)
   - `options` (array of strings)
   - `correct_answer` (integer, 0-based index)
   - `explanation` (string)
   - `type` (always "multiple_choice")
   - `difficulty` (1, 2, or 3)

4. **Validate jim_kwik_principles**:
   Only these values allowed:
   - active_learning
   - minimum_effective_dose
   - teach_like_im_10
   - memory_hooks
   - meta_learning
   - connect_to_what_i_know
   - reframe_limiting_beliefs
   - gamify_it
   - learning_sprint
   - multiple_memory_pathways

5. **Validate content_blocks**:
   Only these types allowed:
   - explanation
   - video
   - diagram
   - quiz
   - simulation
   - reflection
   - memory_aid
   - real_world
   - code_exercise
   - mindset_coach

6. **Check for content duplication**:
   - Detect identical content across blocks (exact duplicates)
   - Detect very similar content (>90% overlap)
   - Flag as critical issue (likely copy-paste error)
   - Common issue: Same content repeated in multiple sections

7. **Run comprehensive_fix.py** if errors found:
   ```bash
   python comprehensive_fix.py
   ```

8. **Test loading**:
   ```bash
   python load_all_lessons.py 2>&1 | grep -A 5 "lesson_<domain>_<order>"
   ```

## Output Format

Provide clear, actionable report:

```
✅ VALIDATION PASSED: lesson_dfir_78_auditd_RICH.json

Summary:
- All required fields present
- 5 assessment questions (all valid)
- 7 content blocks (6 types)
- jim_kwik_principles: valid
- Word count: ~8,500 words
- Status: Ready to commit
```

Or if errors:

```
❌ VALIDATION FAILED: lesson_dfir_78_auditd_RICH.json

Errors found:
1. post_assessment[2] missing "difficulty" field
2. jim_kwik_principles contains invalid value: "real_world_application"
3. content_blocks[5] has invalid type: "concept_deep_dive"
4. Content blocks 3 (explanation) and 7 (real_world) contain identical content

🔧 FIXES APPLIED:
- Added difficulty=2 to question 3
- Replaced "real_world_application" with "active_learning"
- Changed "concept_deep_dive" to "explanation"

✅ Running comprehensive_fix.py...
✅ Fixed! Re-validating...
✅ VALIDATION PASSED

Status: Ready to commit
```

## Auto-Fix Common Issues

1. **Missing question fields** → Add with defaults
2. **Invalid enum values** → Replace with valid alternatives
3. **String content** → Wrap in {"text": "..."}
4. **Invalid UUIDs** → Generate new valid UUIDs
5. **estimated_time > 60** → Cap at 60

## Example Usage

**User**: "Validate lesson 78"

**You**:
1. Read `content/lesson_dfir_78_*.json`
2. Check all validation rules
3. Run comprehensive_fix.py if needed
4. Report status clearly
5. Provide next steps

## Integration with Other Skills

- Works with **lesson-generator** to validate generated lessons
- Works with **batch-lesson-generator** to validate batches
- Works with **git-commit-helper** before committing
- Complements **validate_lesson_compliance.py** script for automated validation
