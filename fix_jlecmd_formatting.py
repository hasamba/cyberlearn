"""
Fix JLECmd lesson formatting - convert markdown code blocks to proper structure
"""

import json
from pathlib import Path

lesson_file = Path(__file__).parent / 'content' / 'lesson_dfir_15_jlecmd_RICH.json'

with open(lesson_file, 'r', encoding='utf-8') as f:
    lesson = json.load(f)

# Find the code_exercise block with the issue (should be around index 4)
for i, block in enumerate(lesson['content_blocks']):
    if block.get('type') == 'code_exercise':
        text = block['content'].get('text', '')

        # Check if this is the problematic block
        if 'Lab: Mastering JLECmd Syntax' in text:
            print(f"Found problematic block at index {i}")
            print(f"Block type: {block['type']}")

            # Restructure the content
            # Extract the main text without code blocks
            new_text = """# Lab: Mastering JLECmd Syntax

## Scenario Setup

You acquired a disk image from an endpoint suspected of staging ransomware. Mount the image read-only, copy the relevant windows automaticdestinations and customdestinations jump lists files into `D:/Evidence/jlecmd`, and verify hashes.

## Step-by-Step Commands

Run these JLECmd commands to parse jump list artifacts:

**Command 1: Parse single artifact**
```bash
JLECmd.exe -f path_to_artifact -d output_folder
```

**Command 2: Recurse entire directory**
```bash
JLECmd.exe -d evidence_directory --csv --json
```

**Command 3: Explore optional switches**
```bash
JLECmd.exe -f evidence_item -o optional
```

### Execution Steps:

1. Run the first command to parse a single artifact. Inspect the CSV to identify recent documents and executables accessed by jump list-enabled apps.
2. Execute the second command to recurse an entire directory. Note how JLECmd handles subfolders and aggregates results.
3. Apply the third command to explore optional switches like `-o` or advanced flags such as `--ns`.

## Analysis Tasks

- Tag three entries that correlate with suspicious activity (for example, binaries signed by unknown publishers or paths referencing network shares).
- Cross-reference hostnames, SIDs, or device identifiers with Active Directory or asset inventories.
- Use `jq`, `pandas`, or Excel to filter on hash values, execution counts, or timestamps.

## Automation Challenge

Write a Python snippet that ingests the CSV and surfaces top anomalies:

```python
import csv
from collections import Counter

with open('output/jlecmd.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

by_path = Counter(row['Path'] for row in rows)
print('Most referenced paths:')
for path, count in by_path.most_common(5):
    print(f"{path}: {count}")
```

## PowerShell Automation

```powershell
# PowerShell wrapper for enterprise triage
$targets = Get-Content .\\hosts.txt
foreach ($target in $targets) {
    Invoke-Command -ComputerName $target -ScriptBlock {
        & "C:\\Tools\\JLECmd.exe" -o "C:\\Temp\\EZ" -d "C:\\Evidence"
    }
}
```

## Extended Analysis Sprint

- Export the CSV into a Jupyter notebook and craft three pandas queries: one that surfaces the rarest paths, one that highlights unsigned binaries, and one that groups entries by user or device.
- Feed the JSON output into your SIEM and build a dashboard tile summarizing execution counts by day. Capture a screenshot to include in the incident report.
- Create a Sigma or KQL rule based on the artifact fields so your detection team can alert on similar behavior the next time it appears.

## Verification Steps

After parsing, revisit the evidence source to double-check integrity. Recalculate hashes of the original hive or directory, compare them with acquisition logs, and note any mismatches. Run the tool with `--nl` or verbosity toggles to confirm lookup lists are behaving as expected.

## Advanced Filtering Ideas

- Pivot on `JLECmd` output to identify binaries executed from network shares, temporary directories, or user profiles.
- Cross-reference hashes with VirusTotal, MISP, or your private threat intelligence platform.
- Normalize timestamps to UTC and align them with authentication logs to spot lateral movement corridors.

Document your findings in a short report: artifact summary, commands used, anomalies discovered, and recommended containment actions. Share it with your blue team to reinforce collaborative learning.

## Scaling to the Enterprise

- Incorporate this command sequence into a KAPE target so responders can collect and parse the artifact in one sweep.
- Embed the utility into a Velociraptor artifact or SOAR playbook to trigger parsing when new hosts enroll in containment VLANs.
- Schedule periodic hunts that compare the latest outputs with historical baselines to catch first-time executions.

## Post-Incident Review Checklist

- Did JLECmd reveal any process gaps (missing detection rules, delayed containment)? Capture them in your lessons-learned tracker.
- Update training decks with screenshots of notable rows so future responders recognize red flags instantly.
- Coordinate with threat intel to feed extracted hashes, paths, and device IDs into watchlists.
"""

            # Update the block
            block['content']['text'] = new_text
            print("[OK] Fixed block content")
            break

# Save the updated lesson
with open(lesson_file, 'w', encoding='utf-8') as f:
    json.dump(lesson, f, indent=2, ensure_ascii=False)

print(f"\n[OK] Saved updated lesson to {lesson_file.name}")
print("\nRun: python load_all_lessons.py to reload the lesson into database")
