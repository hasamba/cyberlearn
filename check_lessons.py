#!/usr/bin/env python3
"""
Check all lessons for completeness:
- Required fields
- Video content blocks
- Proper structure
"""

import json
from pathlib import Path
from collections import defaultdict

def check_lesson(filepath):
    """Check a single lesson for completeness"""
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)
    except Exception as e:
        return [f"ERROR: Cannot parse JSON - {e}"]

    # Check required top-level fields
    required_fields = [
        'lesson_id', 'domain', 'title', 'difficulty', 'order_index',
        'estimated_time', 'prerequisites', 'learning_objectives',
        'concepts', 'content_blocks', 'post_assessment', 'jim_kwik_principles'
    ]

    for field in required_fields:
        if field not in lesson:
            issues.append(f"MISSING FIELD: {field}")

    # Check content blocks
    content_blocks = lesson.get('content_blocks', [])
    if not content_blocks:
        issues.append("NO CONTENT BLOCKS")
    else:
        # Check for video block
        has_video = False
        block_types = []

        for i, block in enumerate(content_blocks):
            block_type = block.get('type', 'UNKNOWN')
            block_types.append(block_type)

            if block_type == 'video':
                has_video = True
                # Check if video block has content
                content = block.get('content', {})
                if not content:
                    issues.append(f"VIDEO BLOCK #{i} HAS NO CONTENT")
                elif isinstance(content, dict):
                    # Check for text/resources/description
                    has_text = bool(content.get('text') or content.get('resources') or content.get('description'))
                    if not has_text:
                        issues.append(f"VIDEO BLOCK #{i} HAS EMPTY CONTENT")

            # Check if content exists
            if 'content' not in block:
                issues.append(f"BLOCK #{i} ({block_type}) HAS NO CONTENT FIELD")
            elif isinstance(block['content'], dict):
                if not any(block['content'].values()):
                    issues.append(f"BLOCK #{i} ({block_type}) HAS EMPTY CONTENT DICT")

        if not has_video:
            issues.append(f"NO VIDEO BLOCK (has: {', '.join(set(block_types))})")

    # Check post_assessment
    post_assessment = lesson.get('post_assessment', [])
    if not post_assessment:
        issues.append("NO POST ASSESSMENT QUESTIONS")
    else:
        for i, qa in enumerate(post_assessment):
            if 'question' not in qa:
                issues.append(f"QUESTION #{i} MISSING 'question' FIELD")
            if 'correct_answer' not in qa:
                issues.append(f"QUESTION #{i} MISSING 'correct_answer' FIELD")

    # Check jim_kwik_principles
    principles = lesson.get('jim_kwik_principles', [])
    if not principles:
        issues.append("NO JIM KWIK PRINCIPLES")

    return issues

def main():
    """Check all lessons in content directory"""
    content_dir = Path('content')
    lesson_files = sorted(content_dir.glob('lesson_*_RICH.json'))

    print("=" * 80)
    print(f"Checking {len(lesson_files)} RICH lessons for completeness")
    print("=" * 80)
    print()

    # Statistics
    stats = {
        'total': len(lesson_files),
        'perfect': 0,
        'issues': 0,
        'by_domain': defaultdict(lambda: {'total': 0, 'perfect': 0, 'issues': 0})
    }

    all_issues = {}

    for filepath in lesson_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        domain = lesson.get('domain', 'unknown')
        title = lesson.get('title', filepath.name)

        issues = check_lesson(filepath)

        stats['by_domain'][domain]['total'] += 1

        if issues:
            stats['issues'] += 1
            stats['by_domain'][domain]['issues'] += 1
            all_issues[filepath.name] = {'title': title, 'domain': domain, 'issues': issues}

            print(f"[ISSUES] {filepath.name}")
            print(f"  Title: {title}")
            print(f"  Domain: {domain}")
            for issue in issues:
                print(f"    - {issue}")
            print()
        else:
            stats['perfect'] += 1
            stats['by_domain'][domain]['perfect'] += 1
            print(f"[OK] {filepath.name} - {title}")

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total lessons checked: {stats['total']}")
    print(f"Perfect lessons: {stats['perfect']} ({stats['perfect']/stats['total']*100:.1f}%)")
    print(f"Lessons with issues: {stats['issues']} ({stats['issues']/stats['total']*100:.1f}%)")
    print()

    print("By Domain:")
    print("-" * 80)
    for domain in sorted(stats['by_domain'].keys()):
        d = stats['by_domain'][domain]
        print(f"  {domain:20s}: {d['perfect']:2d}/{d['total']:2d} perfect ({d['perfect']/d['total']*100:.0f}%)")
    print()

    # Issue breakdown
    if all_issues:
        print("=" * 80)
        print("ISSUE BREAKDOWN")
        print("=" * 80)

        issue_counts = defaultdict(int)
        for lesson_issues in all_issues.values():
            for issue in lesson_issues['issues']:
                # Extract issue type
                if ':' in issue:
                    issue_type = issue.split(':')[0]
                else:
                    issue_type = issue
                issue_counts[issue_type] += 1

        print("Most common issues:")
        for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {count:3d}x  {issue_type}")
        print()

    # List lessons needing video
    lessons_need_video = [name for name, data in all_issues.items()
                          if any('NO VIDEO BLOCK' in issue for issue in data['issues'])]

    if lessons_need_video:
        print("=" * 80)
        print(f"LESSONS NEEDING VIDEO BLOCKS ({len(lessons_need_video)})")
        print("=" * 80)
        for name in sorted(lessons_need_video):
            print(f"  - {name}: {all_issues[name]['title']}")
        print()

    print("=" * 80)
    if stats['issues'] == 0:
        print("SUCCESS: All lessons are complete!")
    else:
        print(f"ACTION NEEDED: {stats['issues']} lessons need attention")
    print("=" * 80)

if __name__ == '__main__':
    main()
