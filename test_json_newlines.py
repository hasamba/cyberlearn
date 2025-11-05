#!/usr/bin/env python3
"""Test if JSON newlines are being parsed correctly"""
import json

# Read the lesson file
with open('content/lesson_dfir_17_shimcache_forensics_RICH.json', 'r', encoding='utf-8') as f:
    lesson_data = json.load(f)

# Find the video block
for block in lesson_data['content_blocks']:
    if block['type'] == 'video':
        text = block['content']['text']
        print("=" * 80)
        print("RAW TEXT FROM JSON:")
        print("=" * 80)
        print(repr(text))  # Show with escape sequences
        print("\n" + "=" * 80)
        print("RENDERED TEXT:")
        print("=" * 80)
        print(text)  # Show how it will appear
        print("\n" + "=" * 80)
        print("ANALYSIS:")
        print("=" * 80)
        print(f"Contains actual newlines: {'\\n' in text}")
        print(f"Contains literal backslash-n: {chr(92)+'n' in text}")
        print(f"Number of newlines: {text.count(chr(10))}")
        break
