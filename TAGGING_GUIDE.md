# Lesson Tagging Guide

## Overview

The CyberLearn platform now includes **20 system tags** for organizing lessons by content type, career path, and course alignment.

---

## System Tags (20 Total)

### Content & Source Tags (8)
| Tag | Color | Icon | Description |
|-----|-------|------|-------------|
| Built-In | Blue (#3B82F6) | 🔵 | Core platform lessons |
| Advanced | Purple (#8B5CF6) | 🟣 | Advanced difficulty content |
| PWK Course | Red (#EF4444) | 🔴 | Offensive Security PWK/OSCP |
| Eric Zimmerman Tools | Orange (#F59E0B) | 🟠 | Eric Zimmerman's forensic tools |
| SANS-Aligned | Green (#10B981) | 🟢 | SANS course methodology |
| User Content | Gray (#6B7280) | ⚪ | User-created lessons |
| Community | Pink (#EC4899) | 🩷 | Community-contributed |
| Certification Prep | Teal (#14B8A6) | 🏆 | Industry certifications |

### Career Path Tags (10)
| Tag | Color | Icon | Description |
|-----|-------|------|-------------|
| SOC Tier 1 | Cyan (#06B6D4) | 🛡️ | SOC Tier 1 Analyst |
| SOC Tier 2 | Dark Cyan (#0891B2) | 🛡️ | SOC Tier 2 Analyst |
| Incident Responder | Dark Red (#DC2626) | 🚨 | Incident Response |
| Threat Hunter | Violet (#7C3AED) | 🎯 | Threat Hunting |
| Forensic Analyst | Emerald (#059669) | 🔬 | Digital Forensics |
| Malware Analyst | Crimson (#B91C1C) | 🦠 | Malware Analysis |
| Penetration Tester | Gold (#CA8A04) | 🔓 | Penetration Testing |
| Red Team Operator | Rose (#BE123C) | ⚔️ | Red Team Operations |
| Security Engineer | Indigo (#4F46E5) | 🔧 | Security Engineering |
| Cloud Security | Teal (#0D9488) | ☁️ | Cloud Security |

### Course Tags (2) - **NEW**
| Tag | Color | Icon | Description |
|-----|-------|------|-------------|
| Course: PEN-200 | Dark Red (#DC2626) | 🎓 | Offensive Security PEN-200/OSCP |
| APT | Darker Red (#7C2D12) | 🎯 | Advanced Persistent Threats |

---

## Installation

### New Installations
Tags are automatically included when running:
```bash
python add_tags_system.py
```

### Existing Installations
Add new course tags to existing database:
```bash
python add_course_apt_tags.py
```

---

## Bulk Tagging Lessons

### Automatic Tagging Script

Use `bulk_tag_lessons.py` to tag multiple lessons at once:

```bash
python bulk_tag_lessons.py
```

**What it does:**
- Tags pentest lessons (order_index 11-30) with "Course: PEN-200"
- Tags red_team lessons (order_index 52-56) with "APT"
- Skips already-tagged lessons
- Shows progress for each lesson

**Output Example:**
```
============================================================
BULK TAGGING LESSONS
============================================================

1. Finding pentest lessons (order_index 11-30)...
   Found 20 pentest lessons

2. Finding red_team lessons (order_index 52-56)...
   Found 5 red_team lessons

3. Tagging pentest lessons with 'Course: PEN-200'...
   ✓ Lesson 11: Introduction to Penetration Testing
   ✓ Lesson 12: Reconnaissance Techniques
   ...
   Tagged: 20, Skipped: 0

4. Tagging red_team lessons with 'APT'...
   ✓ Lesson 52: APT29 (Cozy Bear) Campaign
   ✓ Lesson 53: APT28 (Fancy Bear) Techniques
   ...
   Tagged: 5, Skipped: 0

============================================================
✅ BULK TAGGING COMPLETED!
============================================================
```

---

## Manual Tagging via UI

### Tag a Single Lesson

1. Go to **"📚 My Learning"**
2. Find the lesson you want to tag
3. Click the **🏷️** icon next to the lesson
4. Tag editor appears
5. Click emoji icons to add tags
6. Click **✕** to remove tags

### Tag Multiple Lessons

1. Go to **"🏷️ Manage Tags"** in sidebar
2. View all lessons with each tag
3. Click lesson cards to add/remove tags

---

## Tag Management

### View All Tags
1. Click **"🏷️ Manage Tags"** in sidebar
2. See all system and custom tags
3. View tag statistics

### Create Custom Tags
1. Go to **"🏷️ Manage Tags"**
2. Click **"Create New Tag"**
3. Fill in:
   - Name
   - Color (hex code, e.g., #FF0000)
   - Icon (emoji)
   - Description
   - System tag checkbox
4. Click **"Create Tag"**

### Edit/Delete Custom Tags
- **System tags** (🔒): Cannot be edited or deleted
- **Custom tags** (✏️): Can be edited or deleted

---

## Tag Filtering

### Filter Lessons by Tags

1. Go to **"📚 My Learning"**
2. Use tag multiselect dropdown
3. Select one or more tags
4. Choose match mode:
   - **Match ANY**: Show lessons with at least one selected tag
   - **Match ALL**: Show lessons with all selected tags

### Tag Preferences

Your tag filter selections are **saved to the database** and persist across:
- Browser refreshes
- Different devices
- Multiple sessions

New users default to **"Beginner"** tag selected.

---

## Use Cases

### Use Case 1: Study for OSCP Exam
1. Filter by: **"Course: PEN-200"**
2. Also select: **"Penetration Tester"** career path
3. Study all pentest lessons 11-30

### Use Case 2: Learn APT Techniques
1. Filter by: **"APT"**
2. Also select: **"Red Team Operator"** or **"Threat Hunter"**
3. Study red_team lessons 52-56

### Use Case 3: SOC Analyst Career Path
1. Filter by: **"SOC Tier 1"**
2. Progress to: **"SOC Tier 2"**
3. Then: **"Incident Responder"** or **"Threat Hunter"**

### Use Case 4: Forensics Specialization
1. Filter by: **"Forensic Analyst"**
2. Also select: **"Eric Zimmerman Tools"**
3. Focus on DFIR domain lessons

---

## Database Schema

### tags Table
```sql
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    color TEXT NOT NULL,
    icon TEXT,
    description TEXT,
    created_at TEXT NOT NULL,
    is_system INTEGER DEFAULT 0
)
```

### lesson_tags Table (Junction)
```sql
CREATE TABLE lesson_tags (
    lesson_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    added_at TEXT NOT NULL,
    PRIMARY KEY (lesson_id, tag_id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
)
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `add_tags_system.py` | Initial tag system setup (20 tags) |
| `add_course_apt_tags.py` | Add course tags to existing DB |
| `bulk_tag_lessons.py` | Tag specific lesson ranges |
| `add_difficulty_tags.py` | Add difficulty level tags |

---

## Tag Naming Conventions

### Good Tag Names
- ✅ "Course: PEN-200" (specific course)
- ✅ "APT" (clear acronym)
- ✅ "SOC Tier 1" (specific level)
- ✅ "Eric Zimmerman Tools" (specific toolset)

### Avoid
- ❌ Generic names ("Good", "Important")
- ❌ Vague descriptions ("Stuff", "Misc")
- ❌ Duplicate meanings (multiple "Advanced" tags)

---

## Summary

**Total System Tags: 20**
- 8 Content/Source tags
- 10 Career path tags
- 2 Course tags

**Features:**
- ✅ Persistent tag filters (database-backed)
- ✅ On-the-fly tagging (🏷️ button)
- ✅ Bulk tagging scripts
- ✅ Tag management UI
- ✅ Match ANY/ALL filtering

**Commands:**
```bash
# Setup (new installations)
python add_tags_system.py

# Add course tags (existing installations)
python add_course_apt_tags.py

# Bulk tag lessons
python bulk_tag_lessons.py

# Start app
streamlit run app.py
```
