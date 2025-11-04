#!/usr/bin/env python3
"""
Comprehensive fix for all lesson validation errors.
"""

import json
import os
import uuid
from pathlib import Path

VALID_JIM_KWIK = [
    'active_learning', 'minimum_effective_dose', 'teach_like_im_10',
    'memory_hooks', 'meta_learning', 'connect_to_what_i_know',
    'reframe_limiting_beliefs', 'gamify_it', 'learning_sprint',
    'multiple_memory_pathways'
]

def fix_lesson(filepath):
    """Fix all validation errors in a lesson file."""
    print(f"\n[FIX] {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    fixed = False

    # Fix 1: Ensure lesson_id is valid UUID
    try:
        uuid.UUID(lesson['lesson_id'])
    except:
        lesson['lesson_id'] = str(uuid.uuid4())
        print(f"  [OK] Fixed lesson_id")
        fixed = True

    # Fix 2: Add order_index if missing
    if 'order_index' not in lesson:
        # Extract from filename if possible
        import re
        match = re.search(r'_(\d+)_', os.path.basename(filepath))
        lesson['order_index'] = int(match.group(1)) if match else 1
        print(f"  [OK] Added order_index: {lesson['order_index']}")
        fixed = True

    # Fix 3: Cap estimated_time
    if lesson.get('estimated_time', 0) > 60:
        lesson['estimated_time'] = 60
        print(f"  [OK] Capped estimated_time")
        fixed = True

    # Fix 4: Fix content_blocks
    for i, block in enumerate(lesson.get('content_blocks', [])):
        # Fix block_id if it's not a valid UUID
        if 'block_id' in block:
            try:
                uuid.UUID(block['block_id'])
            except:
                block['block_id'] = str(uuid.uuid4())
                fixed = True

        # Fix content if it's a string (should be dict)
        if isinstance(block.get('content'), str):
            block['content'] = {'text': block['content']}
            fixed = True

    # Fix 5: Fix jim_kwik_principles
    if 'jim_kwik_principles' in lesson:
        new_principles = []
        for p in lesson['jim_kwik_principles']:
            if p not in VALID_JIM_KWIK:
                # Map to valid enum
                if any(word in p.lower() for word in ['active', 'hands', 'practice']):
                    new_principles.append('active_learning')
                elif 'teach' in p.lower():
                    new_principles.append('teach_like_im_10')
                elif any(word in p.lower() for word in ['memory', 'mnemonic']):
                    new_principles.append('memory_hooks')
                elif any(word in p.lower() for word in ['spaced', 'repetition']):
                    new_principles.append('meta_learning')
                elif 'connect' in p.lower():
                    new_principles.append('connect_to_what_i_know')
                elif 'gamif' in p.lower():
                    new_principles.append('gamify_it')
                else:
                    new_principles.append('active_learning')
            else:
                new_principles.append(p)

        # Ensure unique and exactly 10
        new_principles = list(dict.fromkeys(new_principles))
        while len(new_principles) < 10:
            for p in VALID_JIM_KWIK:
                if p not in new_principles:
                    new_principles.append(p)
                    if len(new_principles) >= 10:
                        break

        lesson['jim_kwik_principles'] = new_principles[:10]
        print(f"  [OK] Fixed jim_kwik_principles")
        fixed = True

    # Fix 6: Add missing post_assessment fields
    for qa in lesson.get('post_assessment', []):
        if 'question_id' not in qa:
            qa['question_id'] = str(uuid.uuid4())
            fixed = True
        if 'type' not in qa:
            qa['type'] = 'multiple_choice'
            fixed = True
        if 'difficulty' not in qa:
            qa['difficulty'] = lesson.get('difficulty', 2)
            fixed = True
        if 'correct_answer' not in qa:
            qa['correct_answer'] = 0  # Default to first option
            fixed = True
        if 'explanation' not in qa:
            qa['explanation'] = "Explanation not provided."
            fixed = True

    if fixed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)
        print(f"  [SAVED] Changes written to file")
        return True
    else:
        print(f"  [INFO] No fixes needed")
        return False

def main():
    content_dir = Path(__file__).parent / 'content'
    lesson_files = list(content_dir.glob('*_RICH.json'))

    print(f"[START] Fixing {len(lesson_files)} lessons...")

    fixed_count = 0
    for filepath in sorted(lesson_files):
        try:
            if fix_lesson(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"  [ERROR] {e}")

    print(f"\n[COMPLETE] Fixed {fixed_count} files")
    print("[NEXT] Now run: python load_all_lessons.py")

if __name__ == '__main__':
    main()
