#!/usr/bin/env python3
"""
Fix broken video links in lesson files.
Replaces unavailable YouTube links with working alternatives.
"""

import json
from pathlib import Path

def fix_video_links():
    """Fix broken video links in all lesson files"""

    content_dir = Path('content')

    # Map of broken links to working alternatives
    video_replacements = {
        'https://www.youtube.com/watch?v=7VqfJJurH0Q': 'https://www.youtube.com/watch?v=FS4qnM3UgGk',
        # Add more as needed
    }

    fixed_count = 0
    files_processed = 0

    print("=" * 80)
    print("FIXING VIDEO LINKS")
    print("=" * 80)
    print()

    for filepath in sorted(content_dir.glob('lesson_*_RICH.json')):
        files_processed += 1
        modified = False

        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        # Check all content blocks
        for block in lesson.get('content_blocks', []):
            if block.get('type') == 'video':
                content = block.get('content', {})

                # Check for video URLs in various fields
                for field in ['url', 'video_url', 'text', 'resources', 'description']:
                    if field in content:
                        text = content[field]
                        if isinstance(text, str):
                            for old_link, new_link in video_replacements.items():
                                if old_link in text:
                                    content[field] = text.replace(old_link, new_link)
                                    modified = True
                                    print(f"[FIXED] {filepath.name}")
                                    print(f"  Block: {block.get('title', 'Untitled')}")
                                    print(f"  Old: {old_link}")
                                    print(f"  New: {new_link}")
                                    print()
                                    fixed_count += 1

        # Save if modified
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files processed: {files_processed}")
    print(f"Video links fixed: {fixed_count}")

    if fixed_count > 0:
        print()
        print("[SUCCESS] Video links fixed! Reload lessons with: python load_all_lessons.py")
    else:
        print()
        print("[INFO] No broken video links found")

    print("=" * 80)

if __name__ == '__main__':
    fix_video_links()
