"""
Fix JLECmd lesson - remove leading spaces and fix markdown formatting
"""

import json
from pathlib import Path

lesson_file = Path(__file__).parent / 'content' / 'lesson_dfir_15_jlecmd_RICH.json'

with open(lesson_file, 'r', encoding='utf-8') as f:
    lesson = json.load(f)

# Find and fix the code_exercise block
for i, block in enumerate(lesson['content_blocks']):
    if block.get('type') == 'code_exercise':
        text = block['content'].get('text', '')

        if 'Lab: Mastering JLECmd Syntax' in text:
            print(f'Found block at index {i}')

            # Remove leading spaces from each line
            lines = text.split('\n')
            cleaned_lines = []
            for line in lines:
                # Remove leading whitespace but preserve relative indentation
                cleaned_lines.append(line.lstrip())

            # Join back together
            cleaned_text = '\n'.join(cleaned_lines)

            # Fix specific issues
            cleaned_text = cleaned_text.replace('##Scanario', '## Scenario')
            cleaned_text = cleaned_text.replace('\n```\n    $', '\n```bash\n$')

            # Update
            block['content']['text'] = cleaned_text
            print('[OK] Fixed formatting')
            break

# Save
with open(lesson_file, 'w', encoding='utf-8') as f:
    json.dump(lesson, f, indent=2, ensure_ascii=False)

print(f'\n[OK] Saved to {lesson_file.name}')
print('Next: python reload_lesson.py content/lesson_dfir_15_jlecmd_RICH.json')
