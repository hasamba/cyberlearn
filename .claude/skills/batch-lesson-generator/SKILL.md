---
name: batch-lesson-generator
description: Generate multiple related lessons in sequence with proper prerequisite chains
version: 1.0
auto_invoke: true
---

# Batch Lesson Generator Skill

Generate multiple lessons efficiently while maintaining prerequisite chains and consistency.

## When to Use

Automatically invoke when:
- User asks to "generate Module X"
- User requests multiple lessons (e.g., "create lessons 78-80")
- User wants to batch-generate from lesson_ideas.csv
- User needs to fill gaps in lesson sequence

## Batch Generation Process

1. **Read lesson_ideas.csv or lesson_ideas.json**
   - Identify lessons to generate
   - Extract metadata (title, difficulty, topics, prerequisites)
   - Verify order sequence

2. **Generate lessons in order**:
   - Start with lowest order_index
   - Generate each lesson using lesson-generator skill
   - Maintain prerequisite chain (each lesson references previous)
   - Validate each lesson before proceeding to next

3. **Update tracking files**:
   - Mark status as "completed" in lesson_ideas.csv
   - Update lesson_ideas.json status
   - Track progress for user

4. **Validate batch**:
   - Run load_all_lessons.py
   - Check for errors
   - Fix any issues with comprehensive_fix.py
   - Verify prerequisite chain integrity

5. **Report summary**:
   - Lessons generated
   - Word counts
   - Validation status
   - Next steps

## Batch Strategies

### Strategy 1: Module-Based

**User**: "Generate Module 2 (lessons 78-80)"

**Process**:
```
Module 2: Advanced Logging
├── Lesson 78: Linux auditd Framework (order 78, prereq: 77)
├── Lesson 79: Sysmon for Linux (order 79, prereq: 78)
└── Lesson 80: VMware ESXi Logging (order 80, prereq: 79)
```

Generate in sequence:
1. Lesson 78 → prerequisite: [lesson_77_UUID]
2. Lesson 79 → prerequisite: [lesson_78_UUID]
3. Lesson 80 → prerequisite: [lesson_79_UUID]

### Strategy 2: Range-Based

**User**: "Generate lessons 85-90"

**Process**:
1. Read lesson_ideas.csv for orders 85-90
2. Extract metadata for each
3. Generate in sequence
4. Chain prerequisites
5. Validate batch

### Strategy 3: Domain-Based

**User**: "Generate all remaining OSINT lessons"

**Process**:
1. Query lesson_ideas.csv for domain=osint, status=not_started
2. Sort by order_index
3. Generate in sequence
4. Update status
5. Report completion

## Prerequisite Chain Management

**Critical**: Each lesson in a batch must reference the previous lesson's UUID.

```python
# Pseudo-code
lesson_78_uuid = generate_lesson_78()
lesson_79 = generate_lesson_79(prerequisites=[lesson_78_uuid])
lesson_80 = generate_lesson_80(prerequisites=[lesson_79.uuid])
```

After generation:
- Verify chain integrity with prerequisite-checker skill
- Ensure no circular dependencies
- Validate UUIDs are valid format

## Progress Tracking

During batch generation, show real-time progress:

```
📦 BATCH GENERATION: Module 2 (Lessons 78-80)

[1/3] Generating lesson 78: Linux auditd Framework
      ⏳ Generating content... (8,500 words)
      ✅ Generated
      ✅ Validated
      💾 Saved: content/lesson_dfir_78_auditd_RICH.json

[2/3] Generating lesson 79: Sysmon for Linux
      ⏳ Generating content... (7,200 words)
      ✅ Generated
      ✅ Validated
      💾 Saved: content/lesson_dfir_79_sysmon_linux_RICH.json

[3/3] Generating lesson 80: VMware ESXi Logging
      ⏳ Generating content... (9,100 words)
      ✅ Generated
      ✅ Validated
      💾 Saved: content/lesson_dfir_80_vmware_esxi_logging_RICH.json

✅ BATCH COMPLETE

Summary:
- 3 lessons generated
- Total: 24,800 words
- All validations passed
- Prerequisite chain: 78 → 79 → 80 ✓
- Status updated in lesson_ideas.csv

Next steps:
1. Test: python load_all_lessons.py
2. Commit: git add content/lesson_dfir_7*.json lesson_ideas.csv
3. Push: git commit && git push
```

## Error Handling

If validation fails during batch:
1. Stop generation
2. Show which lesson failed
3. Display errors
4. Ask user:
   - Fix and continue?
   - Skip and continue?
   - Abort batch?

## Batch Size Recommendations

- **Small batch**: 3-5 lessons (one module)
- **Medium batch**: 6-10 lessons (multiple modules)
- **Large batch**: 10+ lessons (entire course section)

**Token management**:
- Generate in chunks to avoid context limits
- Pause between lessons if needed
- Save progress after each lesson

## Output Files

For each lesson generated:
```
content/lesson_<domain>_<order>_<slug>_RICH.json
```

Updated tracking:
```
lesson_ideas.csv - status changed to "completed"
lesson_ideas.json - status changed to "completed"
```

## Integration with Other Skills

- Uses **lesson-generator** for each individual lesson
- Uses **lesson-validator** to validate each lesson
- Uses **prerequisite-checker** to verify chain
- Works with **git-commit-helper** for batch commits

## Example Commands

```
"Generate Module 2"
"Create lessons 78-80"
"Generate all remaining Linux lessons"
"Batch generate OSINT domain lessons"
"Fill lesson gaps in DFIR domain"
```

## Optimization Features

1. **Parallel content block generation** (where applicable)
2. **Template reuse** for similar lessons
3. **Batch validation** instead of one-by-one
4. **Smart prerequisite resolution** from UUIDs
5. **Auto-tagging** based on course_tag in lesson_ideas

## Post-Generation Checklist

After batch generation:
- [ ] All files created
- [ ] All validations passed
- [ ] Prerequisites chain correctly
- [ ] lesson_ideas.csv updated
- [ ] lesson_ideas.json updated
- [ ] Ready to commit

User is prompted to commit batch when complete.
