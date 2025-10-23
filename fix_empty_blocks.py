#!/usr/bin/env python3
"""
Fix empty/malformed content blocks identified by validate_lesson_content.py
"""

import json
from pathlib import Path

def fix_empty_blocks():
    """Fix the 4 identified empty/malformed blocks"""

    fixes_applied = 0

    print("=" * 80)
    print("FIXING EMPTY CONTENT BLOCKS")
    print("=" * 80)
    print()

    # Fix 1: lesson_active_directory_01_fundamentals_RICH.json
    filepath = Path('content/lesson_active_directory_01_fundamentals_RICH.json')
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        for block in lesson['content_blocks']:
            if block.get('title') == 'Key Takeaways' and block.get('type') == 'memory_aid':
                if 'summary' in block['content'] and 'text' not in block['content']:
                    # Convert summary list to text
                    summary_items = block['content']['summary']
                    text = "## Key Takeaways\n\n"
                    for item in summary_items:
                        text += f"- **{item}**\n"
                    block['content']['text'] = text
                    print(f"[FIXED] {filepath.name} - Key Takeaways block")
                    fixes_applied += 1

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

    # Fix 2: lesson_blue_team_01_fundamentals_RICH.json
    filepath = Path('content/lesson_blue_team_01_fundamentals_RICH.json')
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        # Find block with title/steps structure
        for idx, block in enumerate(lesson['content_blocks']):
            if block.get('type') == 'explanation' and 'text' not in block.get('content', {}):
                content = block.get('content', {})
                if 'title' in content and 'steps' in content:
                    # Convert steps to text
                    text = f"## {content['title']}\n\n"
                    for step in content['steps']:
                        step_num = step.get('step_number', '')
                        instruction = step.get('instruction', '')
                        explanation = step.get('explanation', '')
                        text += f"### {step_num}. {instruction}\n\n{explanation}\n\n"
                    block['content']['text'] = text
                    print(f"[FIXED] {filepath.name} - Block {idx+1} ({content['title']})")
                    fixes_applied += 1

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

    # Fix 3: lesson_fundamentals_02_authentication_vs_authorization_RICH.json
    filepath = Path('content/lesson_fundamentals_02_authentication_vs_authorization_RICH.json')
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        for block in lesson['content_blocks']:
            if block.get('title') == 'Key Takeaways' and block.get('type') == 'memory_aid':
                if 'summary' in block['content'] and 'text' not in block['content']:
                    # Convert summary list to text
                    summary_items = block['content']['summary']
                    text = "## Key Takeaways\n\n"
                    for item in summary_items:
                        text += f"- **{item}**\n"
                    block['content']['text'] = text
                    print(f"[FIXED] {filepath.name} - Key Takeaways block")
                    fixes_applied += 1

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

    # Fix 4: lesson_red_team_01_fundamentals_RICH.json
    filepath = Path('content/lesson_red_team_01_fundamentals_RICH.json')
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        for block in lesson['content_blocks']:
            if block.get('title') == 'Key Takeaways' and block.get('type') == 'memory_aid':
                if 'summary' in block['content'] and 'text' not in block['content']:
                    # Convert summary list to text
                    summary_items = block['content']['summary']
                    text = "## Key Takeaways\n\n"
                    for item in summary_items:
                        text += f"- **{item}**\n"
                    block['content']['text'] = text
                    print(f"[FIXED] {filepath.name} - Key Takeaways block")
                    fixes_applied += 1

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Fixes applied: {fixes_applied}")

    if fixes_applied > 0:
        print()
        print("[SUCCESS] Empty blocks fixed! Reload lessons with: python load_all_lessons.py")

    print("=" * 80)

if __name__ == '__main__':
    fix_empty_blocks()
