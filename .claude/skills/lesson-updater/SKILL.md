---
name: lesson-updater
description: Safely update existing CyberLearn lessons while preserving critical fields
version: 1.0
auto_invoke: true
---

# Lesson Updater Skill

Safely modify existing lessons without breaking validation or prerequisite chains.

## When to Use

Automatically invoke when:
- User asks to "update lesson X"
- User wants to add content to existing lesson
- User needs to fix or enhance a lesson
- User wants to change specific fields

## Critical Rules - NEVER CHANGE

When updating an existing lesson, **NEVER modify**:
- `lesson_id` (breaks references)
- `order_index` (breaks sequence)
- `domain` (breaks organization)
- `prerequisites` (unless explicitly requested)

**ALWAYS preserve** the existing values for these fields!

## Update Process

1. **Read existing lesson**:
   ```bash
   content/lesson_<domain>_<order>_<slug>_RICH.json
   ```

2. **Parse and backup**:
   - Load JSON
   - Store critical fields (lesson_id, order_index, domain, prerequisites)
   - Create backup: `lesson_<order>_BACKUP_<timestamp>.json`

3. **Apply updates**:
   - Modify requested fields only
   - Restore critical fields if accidentally changed
   - Ensure all required fields still present
   - Validate updated content

4. **Show diff**:
   ```
   Changes to lesson_dfir_74:
   + Added 2 new code_exercise blocks
   + Enhanced real_world content (+1,200 words)
   ~ Updated 3 assessment questions
   ✓ Preserved lesson_id, order_index, prerequisites
   ```

5. **Validate** using lesson-validator skill

6. **Save** with confirmation

## Common Update Scenarios

### Add Content Blocks

**User**: "Add more code exercises to lesson 74"

**Process**:
1. Read lesson 74
2. Identify existing code_exercise blocks
3. Generate new code_exercise content
4. Insert appropriately in content_blocks array
5. Validate
6. Show preview
7. Save if confirmed

### Enhance Assessment Questions

**User**: "Improve assessment questions for lesson 78"

**Process**:
1. Read existing post_assessment
2. Analyze quality (difficulty distribution, explanations)
3. Generate improved questions
4. Ensure all required fields present
5. Show before/after comparison
6. Save if confirmed

### Update Tags

**User**: "Add SANS-FOR508 tag to lessons 50-60"

**Process**:
1. Read each lesson
2. Append new tag to existing tags array
3. Preserve all other fields
4. Batch update all lessons
5. Report summary

### Fix Validation Errors

**User**: "Fix validation errors in lesson 73"

**Process**:
1. Run lesson-validator
2. Identify specific errors
3. Apply minimal fixes
4. Preserve all valid content
5. Re-validate
6. Report fixes applied

## Safety Checks

Before any update:
- ✅ Backup original file
- ✅ Verify lesson exists
- ✅ Parse JSON successfully
- ✅ Preserve critical fields
- ✅ Validate after changes
- ✅ Show diff before saving

## Update Commands

### Syntax Examples

```
"Update lesson 74 to add code exercises"
"Add memory aids to lesson 78"
"Enhance real-world content in lesson 72"
"Fix assessment questions in lesson 71"
"Add tag 'Course: SANS-FOR500' to lesson 80"
"Increase difficulty of lesson 75 to 3"
```

## Output Format

```
📝 UPDATING: lesson_dfir_74_users_groups_authentication_RICH.json

Original:
- 7 content blocks
- 5 assessment questions
- 16,000 words

Changes Requested:
- Add 2 code_exercise blocks

Changes Applied:
+ content_blocks[7]: code_exercise "Advanced UID/GID Analysis"
+ content_blocks[8]: code_exercise "Sudo Log Correlation"
+ Updated estimated_time: 55 → 60 minutes

Preserved (unchanged):
✓ lesson_id: d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a
✓ order_index: 74
✓ domain: dfir
✓ prerequisites: [c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f]

New Stats:
- 9 content blocks
- 5 assessment questions
- 18,200 words

✅ Validation: PASSED
💾 Backup saved: lesson_74_BACKUP_20250131_143022.json

Ready to save? (yes/no)
```

## Integration with Other Skills

- Uses **lesson-validator** to validate after updates
- Works with **lesson-generator** for content generation
- Works with **git-commit-helper** for committing updates
- Uses **content-enhancer** for adding missing content types

## Error Handling

If update would break validation:
1. Show preview of issues
2. Suggest fixes
3. Ask for confirmation
4. Apply fixes with comprehensive_fix.py
5. Re-validate
6. Save only if valid

Never save a lesson that fails validation!
