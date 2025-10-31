---
name: course-tag-manager
description: Manage course tags across lessons systematically
version: 1.0
auto_invoke: true
---

# Course Tag Manager Skill

Systematically manage and apply course tags to lessons.

## When to Use

- User asks to "tag lessons with X"
- User wants to add/remove course tags
- User needs to see which lessons have which tags
- User wants tag statistics

## Available Course Tags

```
Course: 13Cubed-Investigating Linux Devices
Course: 13Cubed-Windows Memory Forensics
Course: 13Cubed-Windows Endpoints
Course: SANS-FOR500 (Windows Forensics)
Course: SANS-FOR508 (Advanced IR)
Course: SANS-FOR509 (Cloud Forensics)
Course: SANS-FOR528 (Ransomware)
Course: SANS-FOR572 (Network Forensics)
Course: SANS-FOR589 (Cybercrime Intelligence)
Course: SANS-FOR608 (Enterprise IR)
Course: SANS-SEC504 (Hacker Tools)
Course: OWASP LLM Top 10
Package: Eric Zimmerman Tools
Package: User Content
```

## Operations

### Add Tags

**Command**: "Tag lessons 78-80 with Course: 13Cubed-Investigating Linux Devices"

**Process**:
1. Read each lesson file
2. Append tag to tags array (avoid duplicates)
3. Save lesson
4. Update lesson_ideas.csv course_tag column
5. Report summary

### Remove Tags

**Command**: "Remove SANS-FOR500 tag from lessons 10-20"

**Process**:
1. Read each lesson
2. Filter out specified tag
3. Save lesson
4. Report summary

### List Tagged Lessons

**Command**: "Show me all lessons tagged with SANS-FOR508"

**Process**:
1. Scan all lesson files
2. Filter by tag
3. Display list with order, title, domain

### Tag Statistics

**Command**: "Show tag statistics"

**Output**:
```
Course Tag Distribution:
- 13Cubed-Investigating Linux Devices: 41 lessons
- SANS-FOR500: 19 lessons
- SANS-FOR508: 18 lessons
- OWASP LLM Top 10: 10 lessons
- Untagged: 3 lessons
```

## Batch Tagging

From lesson_ideas.csv:
- Read course_tag column
- Apply to corresponding lessons automatically
- Update all lessons in batch
- Report completion

## Integration

- Works with **lesson-updater** for safe tag updates
- Works with **batch-lesson-generator** for auto-tagging new lessons
- Works with **lesson-analytics** for tag statistics
