#!/usr/bin/env python3
"""
Find all broken YouTube video links in lesson JSON files.
Checks if videos are available and reports broken ones.
"""

import json
import re
import requests
from pathlib import Path
from time import sleep

def extract_video_urls(lesson_file):
    """Extract all YouTube URLs from a lesson file"""
    with open(lesson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    urls = []
    for block in data.get('content_blocks', []):
        if block.get('type') == 'video':
            text = block.get('content', {}).get('text', '')

            # Extract YouTube URLs
            youtube_pattern = r'https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
            matches = re.findall(youtube_pattern, text)

            for video_id in matches:
                url = f'https://www.youtube.com/watch?v={video_id}'
                urls.append({
                    'url': url,
                    'video_id': video_id,
                    'block': block
                })

    return data, urls

def check_video_availability(video_id):
    """Check if a YouTube video is available"""
    try:
        # Use YouTube oEmbed API to check if video exists
        url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return True, response.json().get('title', 'Unknown')
        else:
            return False, None
    except Exception as e:
        return False, str(e)

def main():
    """Find all broken video links"""

    print("=" * 80)
    print("Finding Broken YouTube Video Links")
    print("=" * 80)
    print()

    content_dir = Path("content")
    lesson_files = sorted(content_dir.glob("*_RICH.json"))

    broken_videos = []
    working_videos = []

    print(f"Checking {len(lesson_files)} lesson files...")
    print()

    for i, lesson_file in enumerate(lesson_files, 1):
        try:
            data, urls = extract_video_urls(lesson_file)

            if not urls:
                continue

            lesson_title = data['title']

            for video_info in urls:
                video_id = video_info['video_id']
                url = video_info['url']

                # Check availability
                is_available, title = check_video_availability(video_id)

                if is_available:
                    working_videos.append({
                        'lesson': lesson_title,
                        'file': lesson_file.name,
                        'url': url,
                        'video_id': video_id,
                        'video_title': title
                    })
                else:
                    broken_videos.append({
                        'lesson': lesson_title,
                        'file': lesson_file.name,
                        'url': url,
                        'video_id': video_id,
                        'error': title
                    })
                    print(f"❌ BROKEN: {lesson_title}")
                    print(f"   File: {lesson_file.name}")
                    print(f"   URL: {url}")
                    print()

                # Rate limit: don't spam YouTube API
                sleep(0.5)

            if i % 20 == 0:
                print(f"Checked {i}/{len(lesson_files)} lessons...")

        except Exception as e:
            print(f"ERROR processing {lesson_file.name}: {e}")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total videos checked: {len(working_videos) + len(broken_videos)}")
    print(f"Working videos: {len(working_videos)}")
    print(f"Broken videos: {len(broken_videos)}")
    print()

    if broken_videos:
        print("=" * 80)
        print("BROKEN VIDEOS")
        print("=" * 80)
        for v in broken_videos:
            print(f"\nLesson: {v['lesson']}")
            print(f"File: {v['file']}")
            print(f"URL: {v['url']}")
            print(f"Error: {v['error']}")

        # Save to file for reference
        with open('broken_videos.json', 'w', encoding='utf-8') as f:
            json.dump(broken_videos, f, indent=2, ensure_ascii=False)
        print()
        print(f"Saved broken videos list to: broken_videos.json")

if __name__ == "__main__":
    main()
