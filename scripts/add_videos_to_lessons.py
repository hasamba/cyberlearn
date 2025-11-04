"""
Add video content blocks to lessons based on lessons_needing_videos.csv

This script:
1. Reads lessons_needing_videos.csv (filled with YouTube URLs)
2. Adds video content blocks to each lesson
3. Places video block as 2nd block (after explanation)
4. Updates lesson files

Usage:
    python add_videos_to_lessons.py [--dry-run]
"""

import json
import sys
import csv
from pathlib import Path
from typing import Dict, List

CONTENT_DIR = Path("content")
INPUT_CSV = Path("lessons_with_suggested_videos.csv")


def create_video_block(youtube_url: str, video_title: str, video_duration: str, lesson_title: str) -> Dict:
    """Create a video content block"""

    # Extract video ID from URL
    video_id = ""
    if "youtube.com" in youtube_url or "youtu.be" in youtube_url:
        if "watch?v=" in youtube_url:
            video_id = youtube_url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[1].split("?")[0]

    # Create comprehensive video block text
    block_text = f"**Video: {video_title}**\\n\\n"

    if video_duration:
        block_text += f"**Duration**: {video_duration}\\n\\n"

    block_text += f"This video provides a visual demonstration of the concepts covered in this lesson. "
    block_text += f"Watch to see practical examples and deepen your understanding of {lesson_title}.\\n\\n"

    block_text += f"**Video Link**: [{video_title}]({youtube_url})\\n\\n"

    if video_id:
        block_text += f"**Embedded Video**:\\n\\n"
        block_text += f"<iframe width=\"560\" height=\"315\" "
        block_text += f"src=\"https://www.youtube.com/embed/{video_id}\" "
        block_text += f"frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; "
        block_text += f"encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>\\n\\n"

    block_text += f"**Learning Tips**:\\n"
    block_text += f"- Watch the video first to get an overview\\n"
    block_text += f"- Pause and take notes on key concepts\\n"
    block_text += f"- Replay sections that cover complex topics\\n"
    block_text += f"- Try to practice along with the video demonstrations\\n"
    block_text += f"- Return to the video as needed while working through exercises"

    return {
        "type": "video",
        "content": {
            "text": block_text,
            "url": youtube_url,
            "title": video_title,
            "duration": video_duration if video_duration else "N/A"
        }
    }


def add_video_to_lesson(lesson_path: Path, video_data: Dict, dry_run: bool = False) -> bool:
    """Add video block to a lesson (insert as 2nd block after explanation)"""

    with open(lesson_path, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    # Check if lesson already has a video block
    content_blocks = lesson.get('content_blocks', [])
    has_video = any(block.get('type') == 'video' for block in content_blocks)

    if has_video:
        print(f"  [SKIP] {lesson_path.name}: Already has video block")
        return False

    # Create video block
    video_block = create_video_block(
        youtube_url=video_data['youtube_url'],
        video_title=video_data['video_title'],
        video_duration=video_data['video_duration'],
        lesson_title=lesson.get('title', '')
    )

    # Insert as 2nd block (index 1) - right after explanation block
    lesson['content_blocks'].insert(1, video_block)

    if not dry_run:
        with open(lesson_path, 'w', encoding='utf-8', errors='ignore') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

    print(f"  [ADD] {lesson_path.name}: Added video block ({video_data['video_title']})")
    return True


def load_video_mapping(csv_path: Path) -> Dict[str, Dict]:
    """Load CSV file with video mapping"""
    video_mapping = {}

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Only include rows with YouTube URL filled in
            if row['youtube_url'].strip():
                video_mapping[row['filename']] = {
                    'youtube_url': row['youtube_url'].strip(),
                    'video_title': row['video_title'].strip() or 'Related Video',
                    'video_duration': row['video_duration'].strip(),
                    'lesson_title': row['title']
                }

    return video_mapping


def main():
    """Main logic"""
    dry_run = '--dry-run' in sys.argv

    print("=" * 80)
    print("ADD VIDEOS TO LESSONS")
    print("=" * 80)
    print()

    if dry_run:
        print("[DRY RUN] No files will be modified")
        print()

    # Check if CSV exists
    if not INPUT_CSV.exists():
        print(f"[ERROR] {INPUT_CSV} not found!")
        print()
        print("Please run: python generate_video_mapping.py")
        return

    print(f"[LOAD] Reading video mapping from {INPUT_CSV}...")
    video_mapping = load_video_mapping(INPUT_CSV)

    print(f"[FOUND] {len(video_mapping)} lessons with video URLs specified")
    print()

    if len(video_mapping) == 0:
        print("[WARNING] No video URLs found in CSV file!")
        print()
        print("Please fill in the 'youtube_url' column in lessons_needing_videos.csv")
        return

    print("[PROCESS] Adding video blocks to lessons...")
    print()

    added_count = 0
    skipped_count = 0

    for lesson_filename, video_data in video_mapping.items():
        lesson_path = CONTENT_DIR / lesson_filename

        if not lesson_path.exists():
            print(f"  [ERROR] {lesson_filename}: File not found")
            skipped_count += 1
            continue

        try:
            if add_video_to_lesson(lesson_path, video_data, dry_run=dry_run):
                added_count += 1
            else:
                skipped_count += 1

        except Exception as e:
            print(f"  [ERROR] {lesson_filename}: {e}")
            skipped_count += 1

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total lessons processed:     {len(video_mapping)}")
    print(f"Video blocks added:          {added_count}")
    print(f"Lessons skipped:             {skipped_count}")
    print()

    if dry_run:
        print("[DRY RUN] Run without --dry-run to apply changes")
    else:
        print("[DONE] All video blocks added!")
        print()
        print("Next steps:")
        print("  1. Run: python load_all_lessons.py")
        print("  2. Run: python validate_lesson_compliance.py")
        print("  3. Run: python update_outdated_lessons.py")
        print("  4. Run: python update_template_database.py")
    print()


if __name__ == "__main__":
    main()
