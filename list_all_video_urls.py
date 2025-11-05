#!/usr/bin/env python3
"""
List all YouTube video URLs from lessons with their context.
This helps identify which videos need to be checked/replaced.
"""

import json
import re
from pathlib import Path

def extract_video_info(lesson_file):
    """Extract video information from a lesson file"""
    with open(lesson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    videos = []
    for i, block in enumerate(data.get('content_blocks', [])):
        if block.get('type') == 'video':
            text = block.get('content', {}).get('text', '')

            # Extract YouTube URLs and video titles
            youtube_pattern = r'https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
            title_pattern = r'\*\*Video:\s*([^\*\n]+)\*\*'

            matches = re.findall(youtube_pattern, text)
            title_matches = re.findall(title_pattern, text)

            for video_id in matches:
                url = f'https://www.youtube.com/watch?v={video_id}'
                video_title = title_matches[0].strip() if title_matches else 'Unknown'

                videos.append({
                    'url': url,
                    'video_id': video_id,
                    'video_title': video_title,
                    'block_index': i
                })

    return data, videos

def main():
    """List all video URLs"""

    print("=" * 80)
    print("All YouTube Video URLs in Lessons")
    print("=" * 80)
    print()

    content_dir = Path("content")
    lesson_files = sorted(content_dir.glob("*_RICH.json"))

    all_videos = []

    for lesson_file in lesson_files:
        try:
            data, videos = extract_video_info(lesson_file)

            if not videos:
                continue

            for video in videos:
                all_videos.append({
                    'lesson_title': data['title'],
                    'lesson_file': lesson_file.name,
                    'lesson_id': data['lesson_id'],
                    'domain': data['domain'],
                    'video_title': video['video_title'],
                    'url': video['url'],
                    'video_id': video['video_id'],
                    'block_index': video['block_index']
                })

        except Exception as e:
            print(f"ERROR processing {lesson_file.name}: {e}")

    # Group by domain
    videos_by_domain = {}
    for v in all_videos:
        domain = v['domain']
        if domain not in videos_by_domain:
            videos_by_domain[domain] = []
        videos_by_domain[domain].append(v)

    # Print grouped by domain
    for domain in sorted(videos_by_domain.keys()):
        videos = videos_by_domain[domain]
        print(f"\n{'='*80}")
        print(f"DOMAIN: {domain.upper()} ({len(videos)} videos)")
        print(f"{'='*80}\n")

        for v in videos:
            print(f"Lesson: {v['lesson_title']}")
            print(f"Video: {v['video_title']}")
            print(f"URL: {v['url']}")
            print(f"File: {v['lesson_file']}")
            print()

    # Save to CSV for easy editing
    with open('all_video_urls.csv', 'w', encoding='utf-8') as f:
        f.write('Domain,Lesson Title,Video Title,Video URL,Video ID,Lesson File,Status,Replacement URL\n')
        for v in all_videos:
            f.write(f'"{v["domain"]}","{v["lesson_title"]}","{v["video_title"]}","{v["url"]}","{v["video_id"]}","{v["lesson_file"]}","",""\n')

    print(f"\n{'='*80}")
    print(f"Total videos: {len(all_videos)}")
    print(f"Saved to: all_video_urls.csv")
    print(f"{'='*80}")
    print()
    print("Next steps:")
    print("1. Open all_video_urls.csv in Excel/Google Sheets")
    print("2. Manually check each video URL (click to test)")
    print("3. Mark broken videos in 'Status' column as 'BROKEN'")
    print("4. Find replacement videos and add to 'Replacement URL' column")
    print("5. Run replace_broken_videos.py to update lesson files")

if __name__ == "__main__":
    main()
