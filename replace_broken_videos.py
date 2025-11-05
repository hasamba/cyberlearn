#!/usr/bin/env python3
"""
Replace broken video URLs in lesson JSON files based on a mapping.
Reads from broken_videos_mapping.json which contains old_url -> new_url mappings.
"""

import json
import re
from pathlib import Path

def replace_video_url_in_text(text, old_video_id, new_video_id, new_video_title=None):
    """Replace video URL and embed in text content"""

    # Replace watch URLs
    text = text.replace(
        f'https://www.youtube.com/watch?v={old_video_id}',
        f'https://www.youtube.com/watch?v={new_video_id}'
    )

    # Replace embed URLs
    text = text.replace(
        f'https://www.youtube.com/embed/{old_video_id}',
        f'https://www.youtube.com/embed/{new_video_id}'
    )

    # Update video title if provided
    if new_video_title:
        # Find and replace video title
        title_pattern = r'\*\*Video:\s*([^\*\n]+)\*\*'
        text = re.sub(title_pattern, f'**Video: {new_video_title}**', text, count=1)

    return text

def replace_videos_in_lesson(lesson_file, replacements):
    """Replace broken videos in a lesson file"""

    with open(lesson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified = False

    for block in data.get('content_blocks', []):
        if block.get('type') == 'video':
            text = block.get('content', {}).get('text', '')

            # Check if this block has any broken videos
            for old_id, replacement in replacements.items():
                if old_id in text:
                    new_id = replacement['new_video_id']
                    new_title = replacement.get('new_video_title')

                    # Replace in text
                    new_text = replace_video_url_in_text(text, old_id, new_id, new_title)
                    block['content']['text'] = new_text
                    modified = True

                    print(f"  Replaced {old_id} with {new_id}")

                    # Also update url field if present
                    if 'url' in block['content']:
                        old_url = f'https://www.youtube.com/watch?v={old_id}'
                        new_url = f'https://www.youtube.com/watch?v={new_id}'
                        if block['content']['url'] == old_url:
                            block['content']['url'] = new_url

    # Save if modified
    if modified:
        with open(lesson_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True

    return False

def main():
    """Replace all broken videos based on mapping file"""

    print("=" * 80)
    print("Replacing Broken YouTube Videos")
    print("=" * 80)
    print()

    # Load mapping file
    mapping_file = Path('broken_videos_mapping.json')
    if not mapping_file.exists():
        print("ERROR: broken_videos_mapping.json not found!")
        print()
        print("Create this file with format:")
        print('{')
        print('  "OLD_VIDEO_ID": {')
        print('    "new_video_id": "NEW_VIDEO_ID",')
        print('    "new_video_title": "New Video Title (optional)"')
        print('  }')
        print('}')
        print()
        print("Example:")
        print('{')
        print('  "fSD4GJzqr2w": {')
        print('    "new_video_id": "BMFCdAGxVN4",')
        print('    "new_video_title": "ShimCache Forensics - 13Cubed"')
        print('  }')
        print('}')
        return

    with open(mapping_file, 'r', encoding='utf-8') as f:
        replacements = json.load(f)

    print(f"Loaded {len(replacements)} video replacements")
    print()

    content_dir = Path("content")
    lesson_files = sorted(content_dir.glob("*_RICH.json"))

    updated_count = 0

    for lesson_file in lesson_files:
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if this file contains any broken video IDs
            needs_update = any(old_id in content for old_id in replacements.keys())

            if needs_update:
                print(f"Updating: {lesson_file.name}")
                if replace_videos_in_lesson(lesson_file, replacements):
                    updated_count += 1

        except Exception as e:
            print(f"ERROR processing {lesson_file.name}: {e}")

    print()
    print("=" * 80)
    print(f"Updated {updated_count} lesson files")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review the updated files")
    print("2. Run: python load_all_lessons.py")
    print("3. Test in Streamlit app")

if __name__ == "__main__":
    main()
