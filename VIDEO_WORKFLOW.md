# Video Content Addition Workflow

This document explains the automated workflow for adding YouTube videos to lessons.

## Quick Start (3 Steps)

```bash
# Step 1: Analyze which lessons need videos
python scripts/generate_video_mapping.py

# Step 2: Auto-suggest relevant videos based on lesson topics
python scripts/auto_suggest_videos.py

# Step 3: Add videos to all lessons
python scripts/add_videos_to_lessons.py
```

## Detailed Workflow

### Step 1: Analysis (generate_video_mapping.py)

**Purpose**: Identify which lessons are missing video blocks

**Input**: `lesson_compliance_report_20251104_111645.txt`

**Process**:
1. Parses compliance report
2. Finds all lessons with "No video content block found" warning
3. Loads lesson metadata (title, domain, concepts)

**Output**: `lessons_needing_videos.csv`

**Sample output**:
```csv
filename,lesson_id,domain,title,difficulty,concepts,youtube_url,video_title,video_duration,notes
lesson_dfir_11_windows_registry_fundamentals_RICH.json,uuid,dfir,Windows Registry Fundamentals,1,"Active Directory, Domain Controllers",,,,,
```

### Step 2: Auto-Suggestion (auto_suggest_videos.py)

**Purpose**: Match lessons to relevant YouTube videos automatically

**Input**: `lessons_needing_videos.csv`

**Process**:
1. Loads curated video database (50+ cybersecurity videos)
2. Extracts keywords from lesson title and concepts
3. Matches lessons to videos based on:
   - Direct keyword matches (e.g., "registry" → "Windows Registry Forensics - 13Cubed")
   - Partial keyword matches (e.g., "forensics" → relevant forensics video)
   - Domain defaults (e.g., dfir → incident response video)
4. Fills in video URL, title, duration, and notes

**Output**: `lessons_with_suggested_videos.csv`

**Sample output**:
```csv
filename,lesson_id,domain,title,difficulty,concepts,youtube_url,video_title,video_duration,notes
lesson_dfir_11_windows_registry_fundamentals_RICH.json,uuid,dfir,Windows Registry Fundamentals,1,"Active Directory, Domain Controllers",https://www.youtube.com/watch?v=2Kn0TDbKqYw,Windows Registry Forensics - 13Cubed,15:24,Auto-suggested based on lesson topic
```

### Step 3: Application (add_videos_to_lessons.py)

**Purpose**: Add video content blocks to lesson JSON files

**Input**: `lessons_with_suggested_videos.csv`

**Process**:
1. Reads CSV file with video URLs
2. For each lesson:
   - Checks if video block already exists (skip if so)
   - Creates video content block with:
     - Video title and duration
     - Direct YouTube link
     - Embedded iframe code
     - Learning tips
   - Inserts as 2nd block (after explanation)
3. Updates lesson JSON files
4. Reports results

**Output**: Updated lesson JSON files

**Video block structure**:
```json
{
  "type": "video",
  "content": {
    "text": "**Video: Windows Registry Forensics - 13Cubed**\n\n**Duration**: 15:24\n\nThis video provides...\n\n**Learning Tips**:\n- Watch the video first...",
    "url": "https://www.youtube.com/watch?v=2Kn0TDbKqYw",
    "title": "Windows Registry Forensics - 13Cubed",
    "duration": "15:24"
  }
}
```

### Step 4: Database Update (standard workflow)

After adding videos, update databases:

```bash
# Load updated lessons into database
python scripts/load_all_lessons.py

# Verify compliance
python scripts/validate_lesson_compliance.py

# Update database with changes
python scripts/update_outdated_lessons.py

# Sync template database
python scripts/update_template_database.py
```

## Manual Workflow (Alternative)

If you want to manually select videos:

```bash
# Step 1: Generate CSV template
python scripts/generate_video_mapping.py

# Step 2: Manually edit lessons_needing_videos.csv in Excel/Google Sheets
# Fill in youtube_url, video_title, video_duration columns

# Step 3: Skip auto-suggest, go directly to application
# Update scripts/add_videos_to_lessons.py to read from lessons_needing_videos.csv instead
python scripts/add_videos_to_lessons.py
```

## Dry Run Mode

Test before applying changes:

```bash
# Preview which videos will be added without modifying files
python scripts/add_videos_to_lessons.py --dry-run
```

## Video Database Curation

The `auto_suggest_videos.py` script uses a curated database of 50+ videos.

**To add more videos**, edit the `VIDEO_DATABASE` dictionary in `auto_suggest_videos.py`:

```python
VIDEO_DATABASE = {
    "new_topic": {
        "url": "https://www.youtube.com/watch?v=...",
        "title": "Video Title - Creator",
        "duration": "MM:SS"
    },
    # ... more videos
}
```

**Keyword matching**:
- Use underscores for multi-word topics: `"windows_registry"`
- Keywords are matched against lesson titles and concepts
- Domain defaults ensure every lesson gets a relevant video

## Results Summary

### Run on 2025-11-04

**Input**: 208 lessons missing videos

**Process**:
- Generated mapping: 208 lessons identified
- Auto-suggested videos: 208 matches found
- Applied videos: 190 added (18 already had videos)

**Output**:
- 190 lessons enhanced with YouTube videos
- 359 → 169 warnings (53% reduction)
- 100% lesson compliance maintained

## Troubleshooting

### Issue: CSV file not found
```bash
Error: lessons_needing_videos.csv not found
Solution: Run python generate_video_mapping.py first
```

### Issue: No videos suggested
```bash
Warning: No video URLs found in CSV file
Solution: Run python auto_suggest_videos.py to fill in videos
```

### Issue: Video already exists
```bash
[SKIP] lesson_xxx.json: Already has video block
Solution: This is normal - script skips lessons that already have videos
```

### Issue: Compliance report outdated
```bash
Solution: Generate new compliance report first:
python validate_lesson_compliance.py --save-report
```

## Best Practices

1. **Always dry-run first**
   ```bash
   python add_videos_to_lessons.py --dry-run
   ```

2. **Verify video relevance**
   - Review `lessons_with_suggested_videos.csv` before applying
   - Adjust auto-suggested videos if needed

3. **Test with small batch**
   - Edit CSV to include only 5-10 lessons
   - Run application script
   - Verify results before full run

4. **Keep video database updated**
   - Add new high-quality videos as you find them
   - Update video URLs if links break
   - Maintain duration accuracy

5. **Run validation after**
   ```bash
   python validate_lesson_compliance.py
   ```

## Files Overview

| File | Purpose | Type |
|------|---------|------|
| `generate_video_mapping.py` | Identify lessons needing videos | Script |
| `auto_suggest_videos.py` | Match lessons to videos | Script |
| `add_videos_to_lessons.py` | Add video blocks to lessons | Script |
| `lessons_needing_videos.csv` | Initial analysis | Data |
| `lessons_with_suggested_videos.csv` | Video suggestions | Data |
| `VIDEO_ADDITIONS_SUMMARY.md` | Full documentation | Docs |
| `VIDEO_WORKFLOW.md` | This file - workflow guide | Docs |

## Future Enhancements

1. **YouTube API Integration**
   - Automatically search YouTube for relevant videos
   - Fetch video metadata (duration, views, rating)
   - Validate video availability

2. **Video Quality Scoring**
   - Rank videos by views, likes, recency
   - Prioritize trusted channels (13Cubed, SANS, etc.)
   - Filter by video length (prefer 10-30 minute videos)

3. **Multi-Video Support**
   - Add multiple video blocks per lesson
   - Beginner vs advanced videos
   - Multiple perspectives on same topic

4. **Playlist Integration**
   - Create domain-specific playlists
   - Link related videos across lessons
   - Progressive learning paths

---

**Created**: 2025-11-04
**Status**: Production Ready
**Maintenance**: Update VIDEO_DATABASE in auto_suggest_videos.py as new videos are discovered
