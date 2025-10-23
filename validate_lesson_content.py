#!/usr/bin/env python3
"""
Validate that all lesson content blocks have renderable content.
Checks for empty or malformed content blocks.
"""

import json
from pathlib import Path
from collections import defaultdict

def validate_content_blocks():
    """Validate all content blocks have proper content"""

    content_dir = Path('content')

    issues = defaultdict(list)
    total_blocks = 0
    empty_blocks = 0

    print("=" * 80)
    print("VALIDATING LESSON CONTENT BLOCKS")
    print("=" * 80)
    print()

    for filepath in sorted(content_dir.glob('lesson_*_RICH.json')):
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        lesson_title = lesson.get('title', 'Unknown')

        for idx, block in enumerate(lesson.get('content_blocks', [])):
            total_blocks += 1
            block_type = block.get('type', 'unknown')
            block_title = block.get('title', f'Block {idx+1}')
            content = block.get('content', {})

            # Check if content is empty or missing required keys
            is_empty = False

            if not content:
                is_empty = True
                issues[filepath.name].append({
                    'block': block_title,
                    'type': block_type,
                    'issue': 'Empty content dict'
                })

            elif block_type == 'mindset_coach':
                if not content.get('text') and not content.get('message'):
                    is_empty = True
                    issues[filepath.name].append({
                        'block': block_title,
                        'type': block_type,
                        'issue': 'Missing text/message key'
                    })

            elif block_type == 'explanation':
                if not content.get('text'):
                    is_empty = True
                    issues[filepath.name].append({
                        'block': block_title,
                        'type': block_type,
                        'issue': 'Missing text key'
                    })

            elif block_type == 'memory_aid':
                if not content.get('text') and not content.get('technique') and not content.get('visualization'):
                    is_empty = True
                    issues[filepath.name].append({
                        'block': block_title,
                        'type': block_type,
                        'issue': 'Missing text/technique/visualization keys'
                    })

            elif block_type == 'video':
                if not content.get('text') and not content.get('resources') and not content.get('description'):
                    is_empty = True
                    issues[filepath.name].append({
                        'block': block_title,
                        'type': block_type,
                        'issue': 'Missing text/resources/description keys'
                    })

            elif block_type == 'real_world':
                if not content.get('text') and not content.get('description'):
                    is_empty = True
                    issues[filepath.name].append({
                        'block': block_title,
                        'type': block_type,
                        'issue': 'Missing text/description keys'
                    })

            elif block_type == 'code_exercise':
                if not content.get('text'):
                    is_empty = True
                    issues[filepath.name].append({
                        'block': block_title,
                        'type': block_type,
                        'issue': 'Missing text key'
                    })

            if is_empty:
                empty_blocks += 1

    # Print results
    if issues:
        print(f"[WARNING] Found {empty_blocks} empty/malformed content blocks in {len(issues)} lessons")
        print()

        for filename, file_issues in issues.items():
            print(f"📄 {filename}")
            for issue in file_issues:
                print(f"  ❌ {issue['block']} ({issue['type']})")
                print(f"     Issue: {issue['issue']}")
            print()
    else:
        print(f"[SUCCESS] All {total_blocks} content blocks validated successfully!")
        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total content blocks checked: {total_blocks}")
    print(f"Empty/malformed blocks: {empty_blocks}")
    print(f"Lessons with issues: {len(issues)}")
    print(f"Pass rate: {((total_blocks - empty_blocks) / total_blocks * 100):.1f}%")
    print("=" * 80)

if __name__ == '__main__':
    validate_content_blocks()
