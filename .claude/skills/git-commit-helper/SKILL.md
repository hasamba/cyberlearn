---
name: git-commit-helper
description: Automate git commits for lesson files with proper commit messages
version: 1.0
auto_invoke: true
---

# Git Commit Helper Skill

Automatically create proper git commits for CyberLearn lesson files and related updates.

## When to Use

Automatically invoke when:
- User completes lesson generation
- User asks to "commit" or "push" changes
- Batch lesson generation completes
- Lesson updates are saved
- Tracking files are modified

## Commit Message Standards

### For Single Lesson
```
Add lesson <order>: <title>

- Domain: <domain>
- Difficulty: <difficulty>
- Prerequisites: <list>
- Word count: ~<count> words
- Course tag: <tag>
```

**Example**:
```
Add lesson 78: Linux auditd Framework for Forensics

- Domain: dfir
- Difficulty: 2
- Prerequisites: lesson 77
- Word count: ~8,500 words
- Course tag: 13Cubed-Investigating Linux Devices
```

### For Batch Lessons
```
Add lessons <start>-<end>: <module-name>

Module <number>: <module-title>
- Lesson <order>: <title>
- Lesson <order>: <title>
- Lesson <order>: <title>

Total: <count> lessons, ~<word-count> words
All validations passed
```

**Example**:
```
Add lessons 78-80: Advanced Logging Module

Module 2: Advanced Logging
- Lesson 78: Linux auditd Framework for Forensics
- Lesson 79: Sysmon for Linux
- Lesson 80: VMware ESXi Logging

Total: 3 lessons, ~24,800 words
All validations passed
```

### For Lesson Updates
```
Update lesson <order>: <what-changed>

Changes:
- Added <feature>
- Enhanced <section>
- Fixed <issue>

Validation: PASSED
```

### For Tracking File Updates
```
Update lesson status: <description>

Updated lesson_ideas.csv:
- Lessons <range>: not_started → completed

Updated lesson_ideas.json:
- Module <number>: <count> lessons completed
```

### For Skill Creation
```
Add Claude Code skills for lesson management

Skills created:
- lesson-generator: Generate lessons following validation rules
- lesson-validator: Validate and fix lesson JSON
- batch-lesson-generator: Generate multiple lessons in sequence
[... list all skills]

Total: <count> skills
All auto-invoke enabled
```

## Git Workflow

1. **Check git status**:
   ```bash
   git status
   ```

2. **Stage files**:
   ```bash
   # For lesson files
   git add content/lesson_*.json

   # For tracking files
   git add lesson_ideas.csv lesson_ideas.json

   # For skills
   git add .claude/skills/

   # For specific lesson
   git add content/lesson_dfir_78_*.json
   ```

3. **Commit with message**:
   ```bash
   git commit -m "$(cat <<'EOF'
   Add lesson 78: Linux auditd Framework for Forensics

   - Domain: dfir
   - Difficulty: 2
   - Prerequisites: lesson 77
   - Word count: ~8,500 words
   - Course tag: 13Cubed-Investigating Linux Devices
   EOF
   )"
   ```

4. **Push to remote**:
   ```bash
   git push
   ```

5. **Report results**:
   ```
   ✅ COMMITTED: lesson_dfir_78_auditd_RICH.json

   Commit: a1b2c3d
   Files: 1 changed, 850 insertions(+)

   ✅ PUSHED to origin/main

   Status: Lesson 78 deployed successfully
   ```

## File Grouping Strategy

### Strategy 1: Commit Each Lesson Separately
**When**: Generating lessons manually one-by-one

**Process**:
1. Generate lesson X
2. Validate lesson X
3. Commit lesson X immediately
4. Continue to lesson X+1

**Advantage**: Clean git history, easy to revert individual lessons

### Strategy 2: Commit Module Batches
**When**: Batch-generating entire modules

**Process**:
1. Generate all lessons in module
2. Validate all lessons
3. Commit entire module at once
4. Update tracking files
5. Commit tracking file updates separately

**Advantage**: Logical grouping, fewer commits

### Strategy 3: Commit by File Type
**When**: Making systematic updates across many lessons

**Process**:
1. Commit 1: All lesson content files
2. Commit 2: All tracking file updates (CSV/JSON)
3. Commit 3: Documentation updates

**Advantage**: Clear separation of concerns

## Pre-Commit Checklist

Before committing, verify:
- ✅ All lessons pass validation (`python load_all_lessons.py`)
- ✅ No validation errors in output
- ✅ Tracking files updated (lesson_ideas.csv, lesson_ideas.json)
- ✅ File naming convention correct: `lesson_<domain>_<order>_<slug>_RICH.json`
- ✅ Prerequisites chain properly
- ✅ Course tags applied correctly
- ✅ UUIDs are valid format

## Error Handling

### If validation fails:
```
❌ VALIDATION FAILED - COMMIT ABORTED

Errors in lesson_dfir_78:
- Missing question_id in post_assessment[2]
- Invalid jim_kwik_principles value

🔧 Running comprehensive_fix.py...
✅ Fixed! Re-validating...
✅ VALIDATION PASSED

Ready to commit? (yes/no)
```

### If git push fails:
```
❌ PUSH FAILED

Error: Updates were rejected because the remote contains work

Solution:
1. Pull latest changes: git pull --rebase
2. Resolve any conflicts
3. Push again: git push

Would you like me to pull and retry? (yes/no)
```

## Integration with Other Skills

- Uses **lesson-validator** before committing
- Works with **batch-lesson-generator** for module commits
- Coordinates with **lesson-updater** for update commits
- Integrates with **lesson-analytics** for commit summaries

## Automatic Commit Scenarios

### After lesson generation:
```
📝 Lesson 78 generated and validated

Ready to commit? (auto-commit enabled)

✅ COMMITTED: Add lesson 78: Linux auditd Framework
✅ PUSHED to origin/main

Next: Continue to lesson 79? (yes/no)
```

### After batch generation:
```
📦 Module 2 complete (3 lessons)

Auto-committing batch...

✅ COMMITTED: Add lessons 78-80: Advanced Logging Module
✅ COMMITTED: Update lesson status: Mark Module 2 as completed
✅ PUSHED to origin/main (2 commits)

Next: Generate Module 3? (yes/no)
```

## Commit Best Practices

1. **One logical change per commit**
   - Single lesson = single commit
   - Module batch = single commit
   - Tracking updates = separate commit

2. **Descriptive commit messages**
   - Include lesson number and title
   - List key metadata (domain, difficulty, word count)
   - Note validation status

3. **Atomic commits**
   - Don't mix lesson content with unrelated changes
   - Keep tracking file updates separate
   - Skills go in separate commits

4. **Validation before commit**
   - Always run load_all_lessons.py first
   - Fix any errors with comprehensive_fix.py
   - Verify no regressions

5. **Push frequently**
   - Push after each module completion
   - Don't accumulate many unpushed commits
   - Ensure remote backup of work

## Example Workflow

**User**: "Generate lesson 78"

**Git Commit Helper**:
1. ✅ Lesson generated: lesson_dfir_78_auditd_RICH.json
2. ✅ Validation: PASSED
3. 📝 Staging file: `git add content/lesson_dfir_78_auditd_RICH.json`
4. 💾 Committing: "Add lesson 78: Linux auditd Framework for Forensics"
5. 🚀 Pushing: `git push`
6. ✅ Complete: Commit a1b2c3d pushed to origin/main

**User**: "Generate Module 2 (lessons 78-80)"

**Git Commit Helper**:
1. ✅ 3 lessons generated and validated
2. 📝 Staging: `git add content/lesson_dfir_7*.json`
3. 💾 Commit 1: "Add lessons 78-80: Advanced Logging Module"
4. 📝 Staging: `git add lesson_ideas.csv lesson_ideas.json`
5. 💾 Commit 2: "Update lesson status: Mark Module 2 as completed"
6. 🚀 Pushing: `git push`
7. ✅ Complete: 2 commits pushed to origin/main

## Configuration Options

Users can configure:
- **Auto-commit**: Automatically commit after validation (default: ask)
- **Auto-push**: Automatically push after commit (default: ask)
- **Batch strategy**: Commit individually or as batches
- **Message template**: Custom commit message format

## Safety Features

- ✅ Always validate before commit
- ✅ Show diff before committing
- ✅ Confirm before pushing
- ✅ Check for unpushed commits
- ✅ Warn about large commits (>10 files)
- ✅ Prevent committing broken lessons

Never commit lessons that fail validation!
