"""
Check for code block formatting issues in lesson JSON files
"""

import json
from pathlib import Path

content_dir = Path(__file__).parent / 'content'
issues = []

for lesson_file in sorted(content_dir.glob('*.json')):
    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        lesson_title = lesson.get('title', 'Unknown')

        for i, block in enumerate(lesson.get('content_blocks', [])):
            content = block.get('content', {})
            if isinstance(content, dict):
                text = content.get('text', '')

                # Check for broken code blocks
                if '```' in text:
                    # Count backticks
                    triple_count = text.count('```')
                    if triple_count % 2 != 0:
                        issues.append({
                            'file': lesson_file.name,
                            'title': lesson_title,
                            'block': i,
                            'issue': f'Unmatched backticks ({triple_count} found - should be even)',
                            'severity': 'ERROR'
                        })

                    # Check for missing language specifier after opening ```
                    lines = text.split('\n')
                    for line_num, line in enumerate(lines):
                        if line.strip().startswith('```') and not line.strip().endswith('```'):
                            # This is an opening code block
                            lang_spec = line.strip()[3:].strip()
                            if not lang_spec:
                                issues.append({
                                    'file': lesson_file.name,
                                    'title': lesson_title,
                                    'block': i,
                                    'issue': f'Code block on line {line_num} missing language specifier',
                                    'severity': 'WARNING'
                                })

    except Exception as e:
        print(f'Error reading {lesson_file.name}: {e}')

# Print results
if issues:
    print(f'\n[FOUND {len(issues)} CODE BLOCK ISSUES]\n')
    print('=' * 80)

    errors = [i for i in issues if i['severity'] == 'ERROR']
    warnings = [i for i in issues if i['severity'] == 'WARNING']

    if errors:
        print(f'\nERRORS ({len(errors)}):')
        print('-' * 80)
        for issue in errors:
            print(f'\nFile: {issue["file"]}')
            print(f'Lesson: {issue["title"]}')
            print(f'Block: {issue["block"]}')
            print(f'Issue: {issue["issue"]}')

    if warnings:
        print(f'\nWARNINGS ({len(warnings)}):')
        print('-' * 80)
        for issue in warnings[:10]:  # Show first 10 warnings
            print(f'\nFile: {issue["file"]}')
            print(f'Lesson: {issue["title"]}')
            print(f'Block: {issue["block"]}')
            print(f'Issue: {issue["issue"]}')

        if len(warnings) > 10:
            print(f'\n... and {len(warnings) - 10} more warnings')

    print('\n' + '=' * 80)
else:
    print('\n[OK] No code block issues found')
