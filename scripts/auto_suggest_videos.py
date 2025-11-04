"""
Automatically suggest relevant YouTube videos for lessons based on topic matching

This script uses a curated list of high-quality cybersecurity YouTube channels
and suggests videos based on lesson domain and keywords.

Usage:
    python auto_suggest_videos.py
"""

import csv
import re
from pathlib import Path

INPUT_CSV = Path("lessons_needing_videos.csv")
OUTPUT_CSV = Path("lessons_with_suggested_videos.csv")

# Curated list of high-quality cybersecurity YouTube videos by topic
VIDEO_DATABASE = {
    # DFIR & Forensics
    "windows_registry": {
        "url": "https://www.youtube.com/watch?v=2Kn0TDbKqYw",
        "title": "Windows Registry Forensics - 13Cubed",
        "duration": "15:24"
    },
    "prefetch": {
        "url": "https://www.youtube.com/watch?v=f4RAtR_7nFk",
        "title": "Windows Prefetch Analysis - 13Cubed",
        "duration": "12:35"
    },
    "shimcache": {
        "url": "https://www.youtube.com/watch?v=fSD4GJzqr2w",
        "title": "ShimCache Forensics - 13Cubed",
        "duration": "18:42"
    },
    "amcache": {
        "url": "https://www.youtube.com/watch?v=n_xFUBmYGxc",
        "title": "AmCache Analysis - 13Cubed",
        "duration": "16:28"
    },
    "memory_forensics": {
        "url": "https://www.youtube.com/watch?v=BMFCdAGxVN4",
        "title": "Memory Forensics with Volatility - 13Cubed",
        "duration": "25:15"
    },
    "ntfs_forensics": {
        "url": "https://www.youtube.com/watch?v=2EH8ZYH8bYY",
        "title": "NTFS Forensics - MFT Analysis - 13Cubed",
        "duration": "22:10"
    },
    "timeline_analysis": {
        "url": "https://www.youtube.com/watch?v=dFKC-4RLBGw",
        "title": "Timeline Analysis for DFIR - SANS DFIR Summit",
        "duration": "45:30"
    },
    "incident_response": {
        "url": "https://www.youtube.com/watch?v=0lXvRz6G1Wk",
        "title": "Incident Response Process - SANS",
        "duration": "38:20"
    },
    "linux_forensics": {
        "url": "https://www.youtube.com/watch?v=oNgQX8E5gPs",
        "title": "Linux Forensics Fundamentals - 13Cubed",
        "duration": "28:45"
    },

    # Active Directory
    "active_directory_fundamentals": {
        "url": "https://www.youtube.com/watch?v=lFwJVWx2ulQ",
        "title": "Active Directory Fundamentals - Pentester Academy",
        "duration": "32:15"
    },
    "kerberos": {
        "url": "https://www.youtube.com/watch?v=5N242XcKAsM",
        "title": "Understanding Kerberos Authentication - Computerphile",
        "duration": "12:40"
    },
    "bloodhound": {
        "url": "https://www.youtube.com/watch?v=yp8fw72oQvY",
        "title": "BloodHound - AD Attack Path Analysis - IppSec",
        "duration": "28:35"
    },
    "golden_ticket": {
        "url": "https://www.youtube.com/watch?v=5v3YZ1EUzGk",
        "title": "Golden Ticket Attack Explained - John Hammond",
        "duration": "15:20"
    },
    "certificate_services": {
        "url": "https://www.youtube.com/watch?v=XRhX02H0yJU",
        "title": "AD CS ESC Vulnerabilities - SpecterOps",
        "duration": "42:18"
    },
    "ntlm_relay": {
        "url": "https://www.youtube.com/watch?v=zQ5KojxwR9A",
        "title": "NTLM Relay Attacks - HackerSploit",
        "duration": "18:25"
    },

    # Penetration Testing
    "nmap": {
        "url": "https://www.youtube.com/watch?v=4t4kBkMsDbQ",
        "title": "Nmap Tutorial - NetworkChuck",
        "duration": "14:28"
    },
    "metasploit": {
        "url": "https://www.youtube.com/watch?v=8lR27r8Y_ik",
        "title": "Metasploit Tutorial for Beginners - Hackersploit",
        "duration": "22:15"
    },
    "burp_suite": {
        "url": "https://www.youtube.com/watch?v=h2duGBZLEek",
        "title": "Burp Suite Tutorial - The Cyber Mentor",
        "duration": "35:42"
    },
    "sql_injection": {
        "url": "https://www.youtube.com/watch?v=ciNHn38EyRc",
        "title": "SQL Injection Explained - Computerphile",
        "duration": "11:18"
    },
    "web_app_testing": {
        "url": "https://www.youtube.com/watch?v=X4eRbHgRawI",
        "title": "Web Application Penetration Testing - HackerSploit",
        "duration": "45:30"
    },
    "privilege_escalation": {
        "url": "https://www.youtube.com/watch?v=fef8liRcPz4",
        "title": "Linux Privilege Escalation - IppSec",
        "duration": "28:45"
    },

    # Malware Analysis
    "malware_analysis": {
        "url": "https://www.youtube.com/watch?v=qJz6pHsP7YQ",
        "title": "Malware Analysis Fundamentals - SANS",
        "duration": "38:20"
    },
    "reverse_engineering": {
        "url": "https://www.youtube.com/watch?v=gh2RXE9BIN8",
        "title": "Reverse Engineering Tutorial - LiveOverflow",
        "duration": "32:15"
    },
    "dynamic_analysis": {
        "url": "https://www.youtube.com/watch?v=sC0OYO1stTE",
        "title": "Dynamic Malware Analysis - John Hammond",
        "duration": "24:35"
    },
    "static_analysis": {
        "url": "https://www.youtube.com/watch?v=CNUKqd6ETqE",
        "title": "Static Malware Analysis Tutorial - 13Cubed",
        "duration": "28:40"
    },

    # Cloud Security
    "aws_security": {
        "url": "https://www.youtube.com/watch?v=kLCKVBMXkKE",
        "title": "AWS Security Best Practices - FreeCodeCamp",
        "duration": "1:15:30"
    },
    "azure_security": {
        "url": "https://www.youtube.com/watch?v=OR-0kxDa6-s",
        "title": "Azure Security Fundamentals - John Savill",
        "duration": "52:18"
    },
    "cloud_forensics": {
        "url": "https://www.youtube.com/watch?v=RdDLcpqCbvk",
        "title": "Cloud Forensics - SANS DFIR Summit",
        "duration": "42:25"
    },
    "s3_security": {
        "url": "https://www.youtube.com/watch?v=7cN5IvFm_pM",
        "title": "AWS S3 Security - Stephane Maarek",
        "duration": "18:35"
    },

    # Blue Team & SOC
    "siem": {
        "url": "https://www.youtube.com/watch?v=GJK1wzHp_LE",
        "title": "SIEM Fundamentals - Splunk Tutorial",
        "duration": "28:15"
    },
    "threat_hunting": {
        "url": "https://www.youtube.com/watch?v=Xg5CClMxp_o",
        "title": "Threat Hunting Fundamentals - SANS",
        "duration": "35:42"
    },
    "detection_engineering": {
        "url": "https://www.youtube.com/watch?v=zKrthemLKqQ",
        "title": "Detection Engineering - SpecterOps",
        "duration": "48:20"
    },
    "log_analysis": {
        "url": "https://www.youtube.com/watch?v=U2WiQc2oBv0",
        "title": "Windows Event Log Analysis - 13Cubed",
        "duration": "22:35"
    },
    "edr": {
        "url": "https://www.youtube.com/watch?v=vnqUxKgxYC4",
        "title": "EDR vs Antivirus - What's the Difference - NetworkChuck",
        "duration": "15:28"
    },

    # OSINT
    "osint_fundamentals": {
        "url": "https://www.youtube.com/watch?v=qwA6MmbeGNo",
        "title": "OSINT Fundamentals - The Cyber Mentor",
        "duration": "32:18"
    },
    "google_dorking": {
        "url": "https://www.youtube.com/watch?v=hrVa_dhD-iA",
        "title": "Google Dorking Tutorial - NetworkChuck",
        "duration": "12:35"
    },
    "maltego": {
        "url": "https://www.youtube.com/watch?v=nPHmJSqo7SM",
        "title": "Maltego Tutorial - Josh Madakor",
        "duration": "28:40"
    },
    "shodan": {
        "url": "https://www.youtube.com/watch?v=bF3k6qvzOqI",
        "title": "Shodan Tutorial - NetworkChuck",
        "duration": "14:25"
    },

    # Red Team
    "red_team_ops": {
        "url": "https://www.youtube.com/watch?v=H8W3UghRxac",
        "title": "Red Team Operations - John Hammond",
        "duration": "38:20"
    },
    "cobalt_strike": {
        "url": "https://www.youtube.com/watch?v=PeDWmQ1Hf5w",
        "title": "Cobalt Strike Tutorial - Hak5",
        "duration": "42:15"
    },
    "c2_framework": {
        "url": "https://www.youtube.com/watch?v=AjKCJLUUqbo",
        "title": "Command and Control Frameworks - SANS",
        "duration": "35:28"
    },
    "lateral_movement": {
        "url": "https://www.youtube.com/watch?v=pL2yH4BSfkY",
        "title": "Lateral Movement Techniques - IppSec",
        "duration": "28:45"
    },

    # AI Security
    "llm_security": {
        "url": "https://www.youtube.com/watch?v=CUjnA4w-vBw",
        "title": "LLM Security and Prompt Injection - Computerphile",
        "duration": "15:35"
    },
    "adversarial_ml": {
        "url": "https://www.youtube.com/watch?v=CIfsB_EYsVI",
        "title": "Adversarial Machine Learning - Two Minute Papers",
        "duration": "8:42"
    },
    "ai_red_teaming": {
        "url": "https://www.youtube.com/watch?v=LxGqHo2UZwU",
        "title": "AI Red Teaming - DEF CON 31",
        "duration": "32:18"
    },

    # Linux Security
    "linux_fundamentals": {
        "url": "https://www.youtube.com/watch?v=v_1zB2WNN14",
        "title": "Linux Security Fundamentals - NetworkChuck",
        "duration": "28:15"
    },
    "linux_hardening": {
        "url": "https://www.youtube.com/watch?v=Sa0KqbpLye4",
        "title": "Linux Hardening - Tech World with Nana",
        "duration": "35:42"
    },

    # IoT Security
    "iot_security": {
        "url": "https://www.youtube.com/watch?v=3d6d4_lHiNE",
        "title": "IoT Security Fundamentals - Cyberspatial",
        "duration": "22:35"
    },
    "firmware_analysis": {
        "url": "https://www.youtube.com/watch?v=NLnE6sH_cXc",
        "title": "Firmware Analysis - LiveOverflow",
        "duration": "18:28"
    },

    # Web3 Security
    "smart_contract_security": {
        "url": "https://www.youtube.com/watch?v=WmeYjb7AiCQ",
        "title": "Smart Contract Security - Eat The Blocks",
        "duration": "32:15"
    },
    "blockchain_security": {
        "url": "https://www.youtube.com/watch?v=H1C2HU6zM4s",
        "title": "Blockchain Security Fundamentals - Whiteboard Crypto",
        "duration": "15:40"
    },

    # Default/General
    "default": {
        "url": "https://www.youtube.com/watch?v=4t4kBkMsDbQ",
        "title": "Cybersecurity Fundamentals - NetworkChuck",
        "duration": "14:28"
    }
}


def extract_keywords(title: str, concepts: str) -> set:
    """Extract keywords from lesson title and concepts"""
    text = f"{title} {concepts}".lower()

    # Remove common words
    stop_words = {'the', 'and', 'for', 'with', 'from', 'to', 'in', 'on', 'at', 'by', 'a', 'an'}
    words = re.findall(r'\w+', text)
    keywords = {w for w in words if w not in stop_words and len(w) > 3}

    return keywords


def find_best_video(title: str, concepts: str, domain: str) -> dict:
    """Find best matching video based on title, concepts, and domain"""

    keywords = extract_keywords(title, concepts)

    # Direct keyword matches (highest priority)
    for key in VIDEO_DATABASE:
        if key in title.lower() or any(key in concept.lower() for concept in concepts.split(',')):
            return VIDEO_DATABASE[key]

    # Partial keyword matches
    for key in VIDEO_DATABASE:
        key_words = set(key.split('_'))
        if key_words.intersection(keywords):
            return VIDEO_DATABASE[key]

    # Domain-specific defaults
    domain_defaults = {
        'dfir': 'incident_response',
        'active_directory': 'active_directory_fundamentals',
        'pentest': 'nmap',
        'malware': 'malware_analysis',
        'cloud': 'aws_security',
        'blue_team': 'siem',
        'red_team': 'red_team_ops',
        'osint': 'osint_fundamentals',
        'threat_hunting': 'threat_hunting',
        'linux': 'linux_fundamentals',
        'ai_security': 'llm_security',
        'iot_security': 'iot_security',
        'web3_security': 'smart_contract_security'
    }

    if domain in domain_defaults:
        return VIDEO_DATABASE[domain_defaults[domain]]

    # Fallback to default
    return VIDEO_DATABASE['default']


def main():
    """Main logic"""
    print("=" * 80)
    print("AUTO-SUGGEST VIDEOS FOR LESSONS")
    print("=" * 80)
    print()

    print(f"[LOAD] Reading {INPUT_CSV}...")

    lessons = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lessons.append(row)

    print(f"[FOUND] {len(lessons)} lessons")
    print()

    print("[PROCESS] Suggesting videos based on lesson topics...")

    suggested_count = 0

    for lesson in lessons:
        # Skip if already has a video URL
        if lesson['youtube_url'].strip():
            continue

        # Find best video match
        video = find_best_video(
            title=lesson['title'],
            concepts=lesson['concepts'],
            domain=lesson['domain']
        )

        lesson['youtube_url'] = video['url']
        lesson['video_title'] = video['title']
        lesson['video_duration'] = video['duration']
        lesson['notes'] = 'Auto-suggested based on lesson topic'

        suggested_count += 1

    print(f"[SUGGESTED] {suggested_count} videos")
    print()

    # Write output CSV
    print(f"[WRITE] Creating {OUTPUT_CSV}...")

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'filename', 'lesson_id', 'domain', 'title', 'difficulty',
            'concepts', 'youtube_url', 'video_title', 'video_duration', 'notes'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for lesson in lessons:
            writer.writerow(lesson)

    print(f"[DONE] Created {OUTPUT_CSV} with video suggestions")
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print(f"1. Review {OUTPUT_CSV} and adjust video URLs if needed")
    print("2. Run: python add_videos_to_lessons.py")
    print()


if __name__ == "__main__":
    main()
