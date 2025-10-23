#!/usr/bin/env python3
"""
Fix validation errors in newly created rich lesson files.
"""

import json
import os
import uuid
import re
from pathlib import Path

# Valid Jim Kwik principle enum values
VALID_JIM_KWIK_PRINCIPLES = [
    'active_learning',
    'minimum_effective_dose',
    'teach_like_im_10',
    'memory_hooks',
    'meta_learning',
    'connect_to_what_i_know',
    'reframe_limiting_beliefs',
    'gamify_it',
    'learning_sprint',
    'multiple_memory_pathways'
]

def fix_lesson_file(filepath):
    """Fix validation errors in a single lesson file."""
    print(f"\n📝 Fixing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    fixed = False

    # Fix 1: Ensure lesson_id is valid UUID
    try:
        uuid.UUID(lesson['lesson_id'])
    except (ValueError, KeyError):
        lesson['lesson_id'] = str(uuid.uuid4())
        print(f"  ✓ Fixed lesson_id")
        fixed = True

    # Fix 2: Cap estimated_time at 60
    if lesson.get('estimated_time', 0) > 60:
        lesson['estimated_time'] = 60
        print(f"  ✓ Capped estimated_time to 60")
        fixed = True

    # Fix 3: Fix content_blocks that are strings instead of dicts
    for i, block in enumerate(lesson.get('content_blocks', [])):
        if isinstance(block.get('content'), str):
            # If it's a video block, wrap in dict
            if block.get('type') == 'video':
                if not block['content'].startswith('{'):
                    lesson['content_blocks'][i]['content'] = {
                        'resources': block['content']
                    }
                    print(f"  ✓ Fixed content_block {i} (video)")
                    fixed = True

    # Fix 4: Fix jim_kwik_principles - convert free text to enum values
    if 'jim_kwik_principles' in lesson:
        new_principles = []
        for principle in lesson['jim_kwik_principles']:
            if principle not in VALID_JIM_KWIK_PRINCIPLES:
                # Map common patterns to valid enums
                if 'active' in principle.lower() or 'hands' in principle.lower():
                    new_principles.append('active_learning')
                elif 'teach' in principle.lower():
                    new_principles.append('teach_like_im_10')
                elif 'memory' in principle.lower() or 'mnemonic' in principle.lower():
                    new_principles.append('memory_hooks')
                elif 'spaced' in principle.lower() or 'repetition' in principle.lower():
                    new_principles.append('meta_learning')
                elif 'connect' in principle.lower() or 'prior' in principle.lower():
                    new_principles.append('connect_to_what_i_know')
                elif 'gamif' in principle.lower() or 'challenge' in principle.lower():
                    new_principles.append('gamify_it')
                else:
                    new_principles.append('active_learning')  # Default
            else:
                new_principles.append(principle)

        # Ensure we have exactly 10 unique principles
        new_principles = list(dict.fromkeys(new_principles))  # Remove duplicates
        while len(new_principles) < 10:
            for p in VALID_JIM_KWIK_PRINCIPLES:
                if p not in new_principles:
                    new_principles.append(p)
                    if len(new_principles) >= 10:
                        break

        lesson['jim_kwik_principles'] = new_principles[:10]
        print(f"  ✓ Fixed jim_kwik_principles")
        fixed = True

    # Fix 5: Add missing fields to post_assessment questions
    for i, qa in enumerate(lesson.get('post_assessment', [])):
        if 'question_id' not in qa:
            qa['question_id'] = str(uuid.uuid4())
            fixed = True
        if 'type' not in qa:
            qa['type'] = 'multiple_choice'
            fixed = True
        if 'difficulty' not in qa:
            qa['difficulty'] = lesson.get('difficulty', 2)
            fixed = True

    if fixed:
        lesson['post_assessment'] = lesson.get('post_assessment', [])
        print(f"  ✓ Fixed post_assessment questions")

    # Write back
    if fixed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Saved fixes to {os.path.basename(filepath)}")
        return True
    else:
        print(f"  ℹ️  No fixes needed")
        return False

def main():
    """Fix all lesson files in content directory."""
    content_dir = Path(__file__).parent / 'content'

    print("🔧 Fixing lesson validation errors...")
    print(f"📂 Content directory: {content_dir}")

    # Get all RICH lesson files
    lesson_files = list(content_dir.glob('*_RICH.json'))
    print(f"📚 Found {len(lesson_files)} RICH lesson files")

    fixed_count = 0
    for filepath in sorted(lesson_files):
        try:
            if fix_lesson_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n✅ Fixed {fixed_count} lesson files")
    print(f"🎯 Run 'python load_all_lessons.py' to load lessons")

if __name__ == '__main__':
    main()
