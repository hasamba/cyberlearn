---
name: prerequisite-checker
description: Validate prerequisite chains and detect dependency issues
version: 1.0
auto_invoke: true
---

# Prerequisite Checker Skill

Validate lesson prerequisite chains and detect issues.

## When to Use

- After batch lesson generation
- User asks to "check prerequisites"
- Before committing lessons
- When debugging lesson sequence issues

## Validation Checks

### 1. UUID Existence
Verify all prerequisite UUIDs actually exist:
```python
for lesson in lessons:
    for prereq_uuid in lesson.prerequisites:
        if not uuid_exists(prereq_uuid):
            ERROR: "Lesson {lesson.order} references non-existent UUID {prereq_uuid}"
```

### 2. Order Index Validation
Prerequisites must have lower order_index:
```
Lesson 78 (order_index=78) → prerequisite Lesson 77 (order_index=77) ✓
Lesson 78 (order_index=78) → prerequisite Lesson 79 (order_index=79) ✗ INVALID!
```

### 3. Circular Dependency Detection
```
Lesson A → Lesson B → Lesson C → Lesson A  ✗ CIRCULAR!
```

### 4. Domain Consistency
Check if prerequisites are from appropriate domains:
- Same domain (preferred)
- Fundamentals domain (always valid)
- Cross-domain with justification

### 5. Missing Prerequisites
Identify lessons that should have prerequisites but don't:
```
Lesson 78 (Module 2, Advanced) has no prerequisites?
Expected: Should reference Lesson 77 (end of Module 1)
```

## Output Format

```
🔍 PREREQUISITE VALIDATION

Checking 282 lessons...

✅ Valid Prerequisites: 275 lessons
⚠️  Warnings: 5 lessons
❌ Errors: 2 lessons

ERRORS:
1. Lesson 85 (order_index=85)
   - References non-existent UUID: abc123...
   - Fix: Update to valid UUID or remove

2. Lesson 92 (order_index=92)
   - Prerequisite Lesson 95 (order_index=95) has HIGHER order
   - Fix: Should reference lesson with lower order

WARNINGS:
1. Lesson 81 (order_index=81)
   - No prerequisites (expected to follow Lesson 80)
   - Recommendation: Add Lesson 80 as prerequisite

Prerequisite Chain Visualization:
71 → 72 → 73 → 74 → 75 → 76 → 77 → 78 → 79 → 80 ✓
81 ⚠️ (broken chain)
82 → 83 → 84 ✓
```

## Auto-Fix Suggestions

For common issues:
1. **Non-existent UUID** → Find intended lesson by order_index, use its UUID
2. **Broken chain** → Suggest previous lesson as prerequisite
3. **Circular dependency** → Suggest breaking at logical point
4. **Wrong order** → Suggest reordering or fixing reference

## Integration

- Used by **batch-lesson-generator** after generation
- Works with **lesson-validator** for comprehensive validation
- Integrates with **lesson-analytics** for dependency visualization
