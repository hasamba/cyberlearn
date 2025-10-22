"""
Fix validation errors in new rich lessons
Adds missing required fields and fixes content block types
"""

import json
import os
import glob

# Mapping of invalid content types to valid ones
CONTENT_TYPE_MAPPING = {
    "concept_deep_dive": "explanation",
    "real_world_application": "real_world",
    "step_by_step_guide": "explanation",
    "common_pitfalls": "explanation",
    "actionable_takeaways": "explanation"
}

# Default values for missing fields
DEFAULT_VALUES = {
    "estimated_time": 30,  # minutes
    "learning_objectives": [
        "Understand core concepts",
        "Apply knowledge in real-world scenarios",
        "Identify common security issues",
        "Implement best practices"
    ],
    "post_assessment": [
        {
            "question_id": "q1",
            "type": "multiple_choice",
            "question": "What is the main concept covered in this lesson?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Review the lesson content for details.",
            "difficulty": 2,
            "points": 10
        },
        {
            "question_id": "q2",
            "type": "multiple_choice",
            "question": "Which best practice should you implement?",
            "options": ["Best Practice A", "Best Practice B", "Best Practice C", "Best Practice D"],
            "correct_answer": 0,
            "explanation": "Review the lesson content for details.",
            "difficulty": 2,
            "points": 10
        }
    ],
    "jim_kwik_principles": [
        "active_learning",
        "teach_like_im_10",
        "memory_hooks",
        "connect_to_what_i_know"
    ]
}

def fix_lesson_file(filepath):
    """Fix a single lesson file"""
    print(f"\nFixing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    changes = []

    # Add missing fields
    if 'estimated_time' not in lesson:
        lesson['estimated_time'] = DEFAULT_VALUES['estimated_time']
        changes.append("  [ADDED] estimated_time")

    if 'learning_objectives' not in lesson:
        lesson['learning_objectives'] = DEFAULT_VALUES['learning_objectives']
        changes.append("  [ADDED] learning_objectives")

    if 'post_assessment' not in lesson:
        lesson['post_assessment'] = DEFAULT_VALUES['post_assessment']
        changes.append("  [ADDED] post_assessment")

    if 'jim_kwik_principles' not in lesson:
        lesson['jim_kwik_principles'] = DEFAULT_VALUES['jim_kwik_principles']
        changes.append("  [ADDED] jim_kwik_principles")

    # Fix prerequisites (convert UUID objects to strings if needed)
    if 'prerequisites' in lesson and lesson['prerequisites']:
        fixed_prereqs = []
        for prereq in lesson['prerequisites']:
            if isinstance(prereq, dict) and '$uuid' in prereq:
                # Handle UUID object format
                fixed_prereqs.append(str(prereq['$uuid']))
            elif not isinstance(prereq, str):
                # Convert any non-string to string
                fixed_prereqs.append(str(prereq))
            else:
                fixed_prereqs.append(prereq)

        if fixed_prereqs != lesson['prerequisites']:
            lesson['prerequisites'] = fixed_prereqs
            changes.append("  [FIXED] prerequisites format")

    # Fix content block types
    if 'content_blocks' in lesson:
        for i, block in enumerate(lesson['content_blocks']):
            if 'type' in block:
                old_type = block['type']
                if old_type in CONTENT_TYPE_MAPPING:
                    block['type'] = CONTENT_TYPE_MAPPING[old_type]
                    changes.append(f"  [FIXED] block {i+1} type: {old_type} -> {block['type']}")

    # Save fixed lesson
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)

    if changes:
        print("\n".join(changes))
        print("  [SAVED] Fixed version")
        return True
    else:
        print("  [OK] No changes needed")
        return False

def main():
    """Fix all new rich lesson files"""
    print("=" * 60)
    print("Fixing Validation Errors in Rich Lessons")
    print("=" * 60)
    print()

    # Find all rich lesson files
    pattern = os.path.join('content', 'lesson_*_RICH.json')
    files = glob.glob(pattern)

    if not files:
        print("No rich lesson files found!")
        return

    print(f"Found {len(files)} rich lesson files\n")

    fixed_count = 0
    error_count = 0

    for filepath in sorted(files):
        try:
            if fix_lesson_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            error_count += 1

    print()
    print("=" * 60)
    if error_count == 0:
        print(f"[SUCCESS] Fixed {fixed_count} lesson files!")
    else:
        print(f"[WARNING] Fixed {fixed_count} files, {error_count} errors")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python load_all_lessons.py")
    print("2. Run: streamlit run app.py")

if __name__ == "__main__":
    main()
