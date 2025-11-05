#!/usr/bin/env python3
"""Debug script to check how video text is being loaded"""
import json

# Read the lesson file
with open('content/lesson_dfir_17_shimcache_forensics_RICH.json', 'r', encoding='utf-8') as f:
    lesson_data = json.load(f)

# Find the video block
for block in lesson_data['content_blocks']:
    if block['type'] == 'video':
        text = block['content']['text']

        print("=" * 80)
        print("RAW TEXT (repr):")
        print("=" * 80)
        print(repr(text[:200]))  # First 200 chars
        print()

        print("=" * 80)
        print("TEXT WITH VISIBLE SPECIAL CHARS:")
        print("=" * 80)
        # Show newlines explicitly
        visible_text = text[:200].replace('\n', '[NEWLINE]').replace('\r', '[CR]')
        print(visible_text)
        print()

        print("=" * 80)
        print("AFTER REPLACING \\n WITH <br>:")
        print("=" * 80)
        formatted = text[:200].replace('\n', '<br>')
        print(formatted)
        print()

        print("=" * 80)
        print("CHARACTER ANALYSIS OF FIRST 50 CHARS:")
        print("=" * 80)
        for i, char in enumerate(text[:50]):
            print(f"  [{i:2d}] {repr(char):6s} ASCII:{ord(char):3d}")

        break
