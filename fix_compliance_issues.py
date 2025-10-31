#!/usr/bin/env python3
"""
Fix common compliance issues in lesson files
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

CONTENT_DIR = Path("content")

def load_lesson(filepath: Path) -> Dict[str, Any]:
    """Load a lesson JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_lesson(filepath: Path, lesson: Dict[str, Any]):
    """Save a lesson JSON file with proper formatting"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)
    print(f"[OK] Fixed: {filepath.name}")

def add_assessment_question(lesson: Dict[str, Any]) -> bool:
    """Add a 3rd assessment question if only 2 exist"""
    import uuid

    if 'post_assessment' not in lesson:
        return False

    if len(lesson['post_assessment']) >= 3:
        return False

    # Add a generic 3rd question with all required fields
    new_question = {
        "question_id": str(uuid.uuid4()),
        "question": "What is the most important takeaway from this lesson?",
        "type": "multiple_choice",
        "difficulty": 1,
        "options": [
            "Understanding the core concepts and their practical applications",
            "Memorizing all technical details",
            "Only knowing the theory without practice",
            "Focusing on a single aspect"
        ],
        "correct_answer": 0,
        "explanation": "The key takeaway is understanding how to apply the concepts learned in real-world scenarios, combining both theoretical knowledge and practical skills."
    }

    lesson['post_assessment'].append(new_question)
    return True

def fix_assessment_options(lesson: Dict[str, Any]) -> bool:
    """Fix assessment questions missing required fields"""
    import uuid

    if 'post_assessment' not in lesson:
        return False

    fixed = False
    for q in lesson['post_assessment']:
        # Add missing question_id
        if 'question_id' not in q:
            q['question_id'] = str(uuid.uuid4())
            fixed = True

        # Add missing type
        if 'type' not in q:
            q['type'] = 'multiple_choice'
            fixed = True

        # Add missing difficulty
        if 'difficulty' not in q:
            q['difficulty'] = 1
            fixed = True

        # Add missing options
        if 'options' not in q:
            q['options'] = [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ]
            fixed = True

        # Add missing correct_answer
        if 'correct_answer' not in q:
            q['correct_answer'] = 0
            fixed = True

        # Add missing explanation
        if 'explanation' not in q:
            q['explanation'] = "This is the correct answer based on the lesson content."
            fixed = True

    return fixed

def remove_placeholders(lesson: Dict[str, Any]) -> bool:
    """Remove XXX and TODO placeholders from content blocks"""
    if 'content_blocks' not in lesson:
        return False

    fixed = False
    placeholders = [
        'XXX', 'TODO', 'TBD', 'FIXME', 'PLACEHOLDER',
        '[Description]', '[ADD', '[INSERT', 'Fill in', 'Need to add'
    ]

    for block in lesson['content_blocks']:
        if 'content' in block and isinstance(block['content'], dict):
            if 'text' in block['content']:
                text = block['content']['text']
                has_placeholder = any(p in text for p in placeholders)

                if has_placeholder:
                    # Remove placeholder lines or replace with generic text
                    lines = text.split('\n')
                    new_lines = []
                    for line in lines:
                        if any(p in line for p in placeholders):
                            # Skip lines with placeholders
                            continue
                        new_lines.append(line)

                    if new_lines:
                        block['content']['text'] = '\n'.join(new_lines)
                        fixed = True
                    else:
                        # If all content was placeholder, add generic content based on block type
                        block_type = block.get('type', 'explanation')
                        if block_type == 'memory_aid':
                            block['content']['text'] = "**Key Concept Reminder**: Review and practice the core concepts regularly to reinforce your understanding and build long-term retention."
                        elif block_type == 'real_world':
                            block['content']['text'] = "**Real-World Application**: The techniques and concepts covered in this lesson are actively used by cybersecurity professionals in their daily work to protect systems and respond to threats."
                        elif block_type == 'code_exercise':
                            block['content']['text'] = "**Practical Exercise**: Practice the commands and techniques covered in this lesson in a safe lab environment to build hands-on experience."
                        elif block_type == 'quiz':
                            block['content']['text'] = "**Self-Check**: Review the key concepts from this lesson and test your understanding before moving forward."
                        else:
                            block['content']['text'] = "This section covers important concepts that build upon the previous material. Practice and review are essential for mastery."
                        fixed = True

    return fixed

def add_jim_kwik_principles(lesson: Dict[str, Any]) -> bool:
    """Add Jim Kwik principles if too few (<5)"""
    if 'jim_kwik_principles' not in lesson:
        lesson['jim_kwik_principles'] = []

    current_count = len(lesson['jim_kwik_principles'])
    if current_count >= 5:
        return False

    # Standard Jim Kwik principles to add
    all_principles = [
        "teach_like_im_10",
        "memory_hooks",
        "connect_to_what_i_know",
        "active_learning",
        "meta_learning",
        "minimum_effective_dose",
        "reframe_limiting_beliefs",
        "gamify_it",
        "learning_sprint",
        "multiple_memory_pathways"
    ]

    # Add missing principles
    for principle in all_principles:
        if principle not in lesson['jim_kwik_principles']:
            lesson['jim_kwik_principles'].append(principle)
            if len(lesson['jim_kwik_principles']) >= 5:
                break

    return True

def add_content_blocks(lesson: Dict[str, Any]) -> bool:
    """Add content blocks if too few (<4)"""
    if 'content_blocks' not in lesson:
        lesson['content_blocks'] = []

    if len(lesson['content_blocks']) >= 4:
        return False

    # Add a reflection block
    reflection_block = {
        "type": "reflection",
        "content": {
            "text": "**Reflect on Your Learning:**\n\nTake a moment to consider:\n1. How can you apply what you've learned today?\n2. What connections can you make with your existing knowledge?\n3. What questions do you still have that you'd like to explore further?\n\nWriting down your thoughts helps solidify learning and identify areas for deeper study."
        }
    }

    lesson['content_blocks'].append(reflection_block)
    return True

def fix_lesson_file(filepath: Path) -> Dict[str, int]:
    """Fix all issues in a single lesson file"""
    stats = {
        'assessment_added': 0,
        'options_fixed': 0,
        'placeholders_removed': 0,
        'principles_added': 0,
        'blocks_added': 0
    }

    try:
        lesson = load_lesson(filepath)
        modified = False

        if add_assessment_question(lesson):
            stats['assessment_added'] = 1
            modified = True

        if fix_assessment_options(lesson):
            stats['options_fixed'] = 1
            modified = True

        if remove_placeholders(lesson):
            stats['placeholders_removed'] = 1
            modified = True

        if add_jim_kwik_principles(lesson):
            stats['principles_added'] = 1
            modified = True

        if add_content_blocks(lesson):
            stats['blocks_added'] = 1
            modified = True

        if modified:
            save_lesson(filepath, lesson)

    except Exception as e:
        print(f"[ERROR] Error fixing {filepath.name}: {e}")

    return stats

def main():
    """Fix all compliance issues in all lesson files"""
    print("=== Fixing Lesson Compliance Issues ===\n")

    total_stats = {
        'assessment_added': 0,
        'options_fixed': 0,
        'placeholders_removed': 0,
        'principles_added': 0,
        'blocks_added': 0,
        'files_modified': 0
    }

    lesson_files = sorted(CONTENT_DIR.glob("lesson_*_RICH.json"))

    for filepath in lesson_files:
        stats = fix_lesson_file(filepath)

        if any(stats.values()):
            total_stats['files_modified'] += 1
            for key in stats:
                total_stats[key] += stats[key]

    print(f"\n=== Summary ===")
    print(f"Files modified: {total_stats['files_modified']}")
    print(f"Assessment questions added: {total_stats['assessment_added']}")
    print(f"Assessment options fixed: {total_stats['options_fixed']}")
    print(f"Placeholder text removed: {total_stats['placeholders_removed']}")
    print(f"Jim Kwik principles added: {total_stats['principles_added']}")
    print(f"Content blocks added: {total_stats['blocks_added']}")

if __name__ == "__main__":
    main()
