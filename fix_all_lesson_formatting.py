"""
Fix formatting issues in ALL lesson JSON files:
1. Remove leading spaces/indentation from text blocks
2. Fix markdown headers without spaces (##Header → ## Header)
3. Add language specifiers to code blocks (``` → ```bash/python/etc)
"""

import json
import re
from pathlib import Path

content_dir = Path(__file__).parent / 'content'
fixed_count = 0
error_count = 0

def clean_text_formatting(text: str) -> tuple[str, list]:
    """Clean text formatting and return cleaned text + list of fixes applied"""
    fixes = []

    # Remove leading spaces from all lines
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip())

    cleaned_text = '\n'.join(cleaned_lines)

    # Check if leading spaces were removed
    if text != cleaned_text:
        fixes.append('Removed leading spaces')

    # Fix markdown headers without spaces: ##Header → ## Header
    header_pattern = r'^(#{1,6})([^\s#])'
    cleaned_text_before = cleaned_text
    cleaned_text = re.sub(header_pattern, r'\1 \2', cleaned_text, flags=re.MULTILINE)
    if cleaned_text != cleaned_text_before:
        fixes.append('Fixed markdown headers')

    # Fix code blocks without language specifiers
    # Match: ```\n (opening code block without language)
    if re.search(r'```\n\s*[\$#]', cleaned_text):
        # This looks like bash/shell code
        cleaned_text = re.sub(r'```\n(\s*[\$#])', r'```bash\n\1', cleaned_text)
        fixes.append('Added bash language to code blocks')

    return cleaned_text, fixes

print('Scanning all lesson files for formatting issues...\n')

for lesson_file in sorted(content_dir.glob('*_RICH.json')):
    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        lesson_title = lesson.get('title', 'Unknown')
        lesson_fixes = []
        modified = False

        # Check all content blocks
        for i, block in enumerate(lesson.get('content_blocks', [])):
            content = block.get('content', {})
            if isinstance(content, dict):
                text = content.get('text', '')

                if text:
                    cleaned_text, fixes = clean_text_formatting(text)

                    if fixes:
                        block['content']['text'] = cleaned_text
                        lesson_fixes.extend([f'Block {i}: {fix}' for fix in fixes])
                        modified = True

        if modified:
            # Save the fixed lesson
            with open(lesson_file, 'w', encoding='utf-8') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)

            print(f'[FIXED] {lesson_file.name}')
            print(f'  Title: {lesson_title}')
            for fix in lesson_fixes[:5]:  # Show first 5 fixes
                print(f'    - {fix}')
            if len(lesson_fixes) > 5:
                print(f'    ... and {len(lesson_fixes) - 5} more fixes')
            print()
            fixed_count += 1

    except Exception as e:
        print(f'[ERROR] {lesson_file.name}: {e}')
        error_count += 1

print('=' * 60)
print(f'Summary:')
print(f'  Fixed: {fixed_count} lessons')
print(f'  Errors: {error_count} lessons')
print(f'\nNext steps:')
print(f'  1. Review changes: git diff content/')
print(f'  2. Reload all lessons: python load_all_lessons.py (delete DB first)')
print(f'  3. Update template: cp cyberlearn.db cyberlearn_template.db')
print(f'  4. Commit: git add content/ cyberlearn_template.db && git commit')
