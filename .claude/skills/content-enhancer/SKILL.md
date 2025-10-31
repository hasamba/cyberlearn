---
name: content-enhancer
description: Add missing content types and enhance existing lessons
version: 1.0
auto_invoke: true
---

# Content Enhancer Skill

Automatically enhance lessons by adding missing content block types and improving quality.

## When to Use

- User asks to "enhance lesson X"
- Lesson is missing key content types
- Lesson word count is too low
- User wants to add specific content types

## Enhancement Strategies

### 1. Add Missing Content Types

Minimum required: 4 different content block types
Optimal: 7+ types

**Check for missing**:
- ✅ mindset_coach (opening/closing)
- ✅ explanation (main content)
- ✅ code_exercise (hands-on)
- ✅ real_world (case studies)
- ✅ memory_aid (mnemonics)
- ✅ reflection (critical thinking)

**Auto-generate missing types**:
```
Lesson 85 has only: explanation, code_exercise
Missing: mindset_coach, real_world, memory_aid, reflection

Adding:
+ mindset_coach (opening): Motivation and context
+ real_world: Case study from actual breach
+ memory_aid: Mnemonics for key concepts
+ reflection: 5 critical thinking questions
+ mindset_coach (closing): Celebration and next steps
```

### 2. Enhance Word Count

If lesson < 4,000 words:
- Expand explanation sections
- Add more examples
- Include additional case studies
- Add troubleshooting guides
- Expand code exercises

### 3. Add Real-World Examples

Every lesson should have at least one real-world case study:
- Actual company breaches (Target, SolarWinds, etc.)
- Specific CVEs
- Timeline reconstructions
- Lessons learned

### 4. Improve Memory Aids

Add memorable mnemonics:
- Acronyms (e.g., "FUDGE" for forensic checks)
- Visual associations
- Stories/analogies
- Rhymes or patterns

### 5. Enhance Code Exercises

Make exercises more comprehensive:
- Add expected outputs
- Include troubleshooting tips
- Provide variations
- Add difficulty levels

## Enhancement Process

1. **Analyze existing content**:
   - Word count
   - Content block types present
   - Quality assessment
   - Gaps identification

2. **Generate missing content**:
   - Use lesson-generator skill patterns
   - Match lesson's domain and difficulty
   - Maintain consistent voice
   - Reference existing content

3. **Integrate new content**:
   - Insert appropriately in content_blocks
   - Maintain logical flow
   - Update estimated_time if needed

4. **Validate**:
   - Check all requirements met
   - Validate with lesson-validator
   - Verify word count increased
   - Ensure quality maintained

## Example Output

```
📈 ENHANCING: lesson_dfir_85_timestomping_RICH.json

Current State:
- 3,200 words (below 4,000 minimum)
- 4 content blocks (minimum met)
- Missing: memory_aid, reflection

Enhancements Applied:
+ memory_aid: "MACB" mnemonic for timestamps
+ reflection: 5 critical thinking questions
+ real_world: Enhanced with Colonial Pipeline case study
+ explanation: Expanded detection techniques (+800 words)
+ code_exercise: Added 2 new hands-on exercises

Updated State:
- 5,100 words ✓
- 6 content blocks (7 types) ✓
- All content types balanced ✓

✅ Enhanced successfully
💾 Ready to save
```

## Integration

- Uses **lesson-generator** patterns for new content
- Works with **lesson-updater** for safe modifications
- Validates with **lesson-validator**
- Used by **batch-lesson-generator** for comprehensive lessons
