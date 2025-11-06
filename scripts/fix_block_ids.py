#!/usr/bin/env python3
"""
Fix invalid block_ids in lesson JSON files by converting them to valid UUIDs
"""

import json
import uuid
from pathlib import Path

def fix_lesson_block_ids(lesson_path: Path) -> bool:
    """
    Fix block_ids in a lesson file by generating valid UUIDs

    Args:
        lesson_path: Path to lesson JSON file

    Returns:
        True if file was modified, False otherwise
    """
    print(f"\nProcessing: {lesson_path.name}")

    # Read lesson
    with open(lesson_path, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    modified = False

    # Fix content_blocks block_ids
    if 'content_blocks' in lesson:
        for block in lesson['content_blocks']:
            if 'block_id' in block:
                block_id = block['block_id']
                # Check if it's a valid UUID
                try:
                    uuid.UUID(block_id)
                except (ValueError, AttributeError):
                    # Not a valid UUID, replace with new one
                    new_id = str(uuid.uuid4())
                    print(f"  Replacing block_id: {block_id} -> {new_id}")
                    block['block_id'] = new_id
                    modified = True

    # Save if modified
    if modified:
        with open(lesson_path, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)
        print(f"  [FIXED] Saved: {lesson_path.name}")
        return True
    else:
        print(f"  No changes needed")
        return False

def main():
    """Fix all lessons with invalid block_ids"""
    content_dir = Path(__file__).parent / "content"

    # Find all JSON files
    lesson_files = list(content_dir.glob("lesson_*.json"))
    print(f"Found {len(lesson_files)} lesson files")

    fixed_count = 0

    for lesson_path in lesson_files:
        if fix_lesson_block_ids(lesson_path):
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"Summary: Fixed {fixed_count} lesson files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
