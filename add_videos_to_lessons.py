"""
Add YouTube video embeds to lessons that don't have them.
Maps lesson topics to relevant educational YouTube videos.
"""

import json
import os
from pathlib import Path

# Mapping of lesson topics/keywords to relevant YouTube video IDs
# These are educational cybersecurity videos from reputable channels
VIDEO_MAPPINGS = {
    # Active Directory
    'active_directory': 'lFwJTKmXUbE',  # What is Active Directory?
    'kerberos': 'qW361k3-BtU',  # Kerberos explained
    'bloodhound': '0r2TQTL9IuA',  # BloodHound tutorial
    'group_policy': '5uA9p6hLCpM',  # Group Policy basics

    # Blue Team / DFIR
    'blue_team': 'h4rdSZ3AYFo',  # Introduction to Blue Team
    'siem': 'qxmPBWVWuZg',  # SIEM explained
    'elk': 'QXEd9l7u3CE',  # ELK Stack tutorial
    'splunk': 'InT3CesJSfY',  # Splunk tutorial
    'forensics': 'Vh_h6NfLkAg',  # Digital Forensics intro
    'memory_forensics': 'cP2QGRZ8j8M',  # Memory forensics
    'incident_response': 'cHj7z5Y9qbM',  # Incident Response

    # Cloud Security
    'aws': 'sQo5HJkgz7I',  # AWS Security
    'azure': 'LdaW8R6RwYA',  # Azure Security
    'kubernetes': 'PH-2FfFD2PU',  # Kubernetes Security
    'cloud': '3hLmDS179YE',  # Cloud Security intro
    'iam': 'SXSqhTn2DuE',  # IAM explained

    # Fundamentals
    'encryption': 'AQDCe585Lnc',  # Encryption explained
    'authentication': 'j5zB1jn_4tc',  # Authentication vs Authorization
    'networking': 'qiQR5rTSshw',  # Networking basics
    'cia_triad': 'AJTJN4wDBM8',  # CIA Triad
    'owasp': 'avPpCKLPPfk',  # OWASP Top 10

    # Linux
    'linux': '6OHVjVtjQVw',  # Linux for hackers
    'selinux': 'cNoVgDqqJmM',  # SELinux explained
    'kernel': 'mycVSMyShk8',  # Linux kernel
    'auditd': '8o0pNc2aDXk',  # Linux auditd

    # Malware Analysis
    'malware': 'YOAc7R9zXxk',  # Malware analysis intro
    'reverse_engineering': 'OsqZdMqNPMM',  # Reverse engineering
    'ransomware': 'WqD-ATqw3ao',  # Ransomware explained
    'rootkit': 'ZBsu1RYWlrg',  # Rootkits explained

    # Penetration Testing
    'pentest': 'fNzpcB7ODxQ',  # Penetration Testing intro
    'reconnaissance': 'Sk8V1vHJnbU',  # Recon techniques
    'exploitation': 'kQc2K2oqmjU',  # Exploitation basics
    'sql_injection': 'ciNHn38EyRc',  # SQL Injection
    'xss': 'L7v5F4m-5SU',  # XSS explained

    # Red Team
    'red_team': 'dTXRu4w5q7w',  # Red Team intro
    'c2': 'IlW4P8vvPj4',  # Command and Control
    'phishing': 'S2bQ06NiRRo',  # Phishing techniques
    'privilege_escalation': 'FXs3mvNxR8s',  # Privilege escalation
    'lateral_movement': 'jmjR7LMFbNE',  # Lateral movement

    # System Internals
    'windows_internals': 'REexhR84Vj8',  # Windows internals
    'registry': 'V5xwzqhSSW0',  # Windows Registry
    'processes': 'DXYkqtfI3uE',  # Windows processes
    'powershell': 'zN5-pOsGILA',  # PowerShell for security
}

def find_relevant_video(lesson_data):
    """Find most relevant video based on lesson content."""
    title = lesson_data.get('title', '').lower()
    concepts = [c.lower() for c in lesson_data.get('concepts', [])]
    domain = lesson_data.get('domain', '').lower()

    # Check title and concepts for keyword matches
    all_text = f"{title} {' '.join(concepts)} {domain}"

    # Try exact matches first
    for keyword, video_id in VIDEO_MAPPINGS.items():
        if keyword in all_text:
            return video_id

    # Fallback to domain-based video
    if 'active_directory' in domain or 'active' in domain:
        return VIDEO_MAPPINGS.get('active_directory')
    elif 'blue' in domain:
        return VIDEO_MAPPINGS.get('blue_team')
    elif 'cloud' in domain:
        return VIDEO_MAPPINGS.get('cloud')
    elif 'dfir' in domain:
        return VIDEO_MAPPINGS.get('forensics')
    elif 'fundamentals' in domain:
        return VIDEO_MAPPINGS.get('cia_triad')
    elif 'linux' in domain:
        return VIDEO_MAPPINGS.get('linux')
    elif 'malware' in domain:
        return VIDEO_MAPPINGS.get('malware')
    elif 'pentest' in domain:
        return VIDEO_MAPPINGS.get('pentest')
    elif 'red' in domain or 'redteam' in domain:
        return VIDEO_MAPPINGS.get('red_team')
    elif 'system' in domain:
        return VIDEO_MAPPINGS.get('windows_internals')

    # Ultimate fallback - general cybersecurity video
    return 'inWWhr5tnEA'  # "What is Cybersecurity?"

def add_video_to_lesson(filepath):
    """Add video block to lesson if missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if video already exists
    has_video = any(block.get('type') == 'video' for block in data.get('content_blocks', []))

    if has_video:
        return False  # Already has video

    # Find relevant video
    video_id = find_relevant_video(data)

    # Create video block
    video_block = {
        "type": "video",
        "content": {
            "title": f"Video: {data.get('title', 'Lesson')} Overview",
            "url": f"https://www.youtube.com/embed/{video_id}",
            "description": "Watch this video for a visual introduction to the concepts covered in this lesson."
        }
    }

    # Insert video block after first explanation or at position 1
    content_blocks = data.get('content_blocks', [])
    insert_position = 1  # After mindset_coach (position 0)

    # Find first explanation block
    for i, block in enumerate(content_blocks):
        if block.get('type') == 'explanation':
            insert_position = i + 1
            break

    content_blocks.insert(insert_position, video_block)
    data['content_blocks'] = content_blocks

    # Save updated lesson
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True  # Video added

def main():
    """Process all RICH lessons."""
    content_dir = Path('content')
    lessons_processed = 0
    videos_added = 0

    for filepath in sorted(content_dir.glob('*_RICH.json')):
        lessons_processed += 1
        if add_video_to_lesson(filepath):
            videos_added += 1
            print(f"[ADDED] {filepath.name}")
        else:
            print(f"[SKIP] {filepath.name} (already has video)")

    print(f"\n{'='*60}")
    print(f"[COMPLETE] Processed {lessons_processed} lessons")
    print(f"[ADDED] {videos_added} video blocks")
    print(f"[TOTAL] {lessons_processed - videos_added} lessons already had videos")

if __name__ == '__main__':
    main()
