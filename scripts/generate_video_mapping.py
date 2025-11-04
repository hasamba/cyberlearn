"""
Generate a mapping file of lessons that need video content blocks

This script:
1. Parses lesson_compliance_report_20251104_111645.txt
2. Identifies all lessons with "No video content block found" warning
3. Creates a CSV file with lesson details for video selection
4. User can fill in YouTube URLs manually or in bulk

Output: lessons_needing_videos.csv

Usage:
    python generate_video_mapping.py
"""

import json
import re
from pathlib import Path
import csv

CONTENT_DIR = Path("content")
REPORT_FILE = Path("lesson_compliance_report_20251104_111645.txt")
OUTPUT_CSV = Path("lessons_needing_videos.csv")


def extract_lessons_needing_videos(report_path: Path) -> list:
    """Parse compliance report and extract lessons needing videos"""
    lessons = []

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all lessons with "No video content block found" warning
    pattern = r'(lesson_[^.]+\.json).*?\n.*?No video content block found'
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        lesson_filename = match.group(1)
        lessons.append(lesson_filename)

    return lessons


def load_lesson_metadata(lesson_filename: str) -> dict:
    """Load lesson to extract title, domain, difficulty"""
    lesson_path = CONTENT_DIR / lesson_filename

    if not lesson_path.exists():
        return None

    with open(lesson_path, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    return {
        'filename': lesson_filename,
        'lesson_id': lesson.get('lesson_id', ''),
        'domain': lesson.get('domain', ''),
        'title': lesson.get('title', ''),
        'difficulty': lesson.get('difficulty', 0),
        'concepts': ', '.join(lesson.get('concepts', [])[:3]),  # First 3 concepts
        'youtube_url': '',  # To be filled by user
        'video_title': '',  # To be filled by user
        'video_duration': '',  # To be filled by user (format: MM:SS or HH:MM:SS)
        'notes': ''  # Optional notes
    }


def main():
    """Main logic"""
    print("=" * 80)
    print("GENERATE VIDEO MAPPING")
    print("=" * 80)
    print()

    print("[SCAN] Parsing compliance report...")
    lessons_needing_videos = extract_lessons_needing_videos(REPORT_FILE)

    print(f"[FOUND] {len(lessons_needing_videos)} lessons need video content blocks")
    print()

    print("[EXTRACT] Loading lesson metadata...")
    lesson_data = []

    for lesson_filename in lessons_needing_videos:
        metadata = load_lesson_metadata(lesson_filename)
        if metadata:
            lesson_data.append(metadata)

    print(f"[LOADED] {len(lesson_data)} lesson metadata entries")
    print()

    # Write to CSV
    print(f"[WRITE] Creating {OUTPUT_CSV}...")

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'filename', 'lesson_id', 'domain', 'title', 'difficulty',
            'concepts', 'youtube_url', 'video_title', 'video_duration', 'notes'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in lesson_data:
            writer.writerow(row)

    print(f"[DONE] Created {OUTPUT_CSV} with {len(lesson_data)} entries")
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print(f"1. Open {OUTPUT_CSV} in Excel/Google Sheets")
    print("2. Fill in columns:")
    print("   - youtube_url: Full YouTube URL (e.g., https://www.youtube.com/watch?v=...)")
    print("   - video_title: Title of the video")
    print("   - video_duration: Duration (e.g., 10:35 or 1:15:20)")
    print("   - notes: Optional notes about video relevance")
    print("3. Save the CSV file")
    print("4. Run: python add_videos_to_lessons.py")
    print()


if __name__ == "__main__":
    main()
