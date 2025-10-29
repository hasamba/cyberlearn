# Tag System Implementation Guide

## Overview

The CyberLearn platform now includes a **comprehensive tag-based lesson organization system** that allows lessons to have multiple colored tags for flexible categorization and filtering.

### Key Features

- **Many-to-Many Relationship**: Lessons can have multiple tags
- **Colored Tag Badges**: Visual distinction with customizable colors and emojis
- **Flexible Filtering**: Filter by ANY tag or ALL tags
- **System & Custom Tags**: Pre-defined system tags + user-created custom tags
- **Tag Management UI**: Full CRUD interface for creating and managing tags
- **Lesson Browser**: Enhanced lesson viewing with tag-based filtering

---

## Architecture

### Database Schema

**Tags Table:**
```sql
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    color TEXT NOT NULL,           -- Hex color code (e.g., #3B82F6)
    icon TEXT,                      -- Emoji icon (e.g., 🔵)
    description TEXT,
    created_at TEXT NOT NULL,
    is_system INTEGER DEFAULT 0    -- System-managed tags cannot be deleted
)
```

**Lesson-Tags Junction Table (Many-to-Many):**
```sql
CREATE TABLE lesson_tags (
    lesson_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    added_at TEXT NOT NULL,
    PRIMARY KEY (lesson_id, tag_id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
)
```

### Default System Tags

The migration script automatically creates these default tags:

| Tag Name | Color | Icon | Description |
|----------|-------|------|-------------|
| **Built-In** | Blue (#3B82F6) | 🔵 | Core platform lessons included by default |
| **Advanced** | Purple (#8B5CF6) | 🟣 | Advanced difficulty lessons |
| **PWK Course** | Red (#EF4444) | 🔴 | Offensive Security PWK/OSCP aligned |
| **Eric Zimmerman Tools** | Orange (#F59E0B) | 🟠 | Lessons focused on Eric Zimmerman's forensic tools |
| **SANS-Aligned** | Green (#10B981) | 🟢 | SANS course aligned lessons |
| **User Content** | Gray (#6B7280) | ⚪ | User-created or imported lessons |
| **Community** | Pink (#EC4899) | 🩷 | Community-contributed lessons |
| **Certification Prep** | Teal (#14B8A6) | 🏆 | Industry certification preparation |

**All existing lessons** are automatically tagged as "Built-In" during migration.

---

## Installation & Setup

### Step 1: Run the Migration Script

On your VM, run the database migration to add the tag system:

```bash
cd /path/to/cyberlearn
python add_tags_system.py
```

**Expected Output:**
```
Creating tags table...
Creating lesson_tags table...
Creating indices...
Adding default system tags...
  ✓ Added tag: 🔵 Built-In
  ✓ Added tag: 🟣 Advanced
  ✓ Added tag: 🔴 PWK Course
  ✓ Added tag: 🟠 Eric Zimmerman Tools
  ✓ Added tag: 🟢 SANS-Aligned
  ✓ Added tag: ⚪ User Content
  ✓ Added tag: 🩷 Community
  ✓ Added tag: 🏆 Certification Prep

Auto-tagging existing lessons as 'Built-In'...
  ✓ Tagged 140 existing lessons as 'Built-In'

============================================================
✅ Tag system migration completed successfully!
============================================================
Tables created: ['tags', 'lesson_tags']
System tags: 8
Lesson-tag associations: 140

Next steps:
1. Run the app: streamlit run app.py
2. Use tag filters to organize lesson view
3. Manage tags via the new Tag Management page
```

### Step 2: Verify Installation

```bash
python -c "from utils.database import Database; db = Database(); print(f'Tags: {len(db.get_all_tags())}')"
```

Should output: `Tags: 8`

---

## Using the Tag System

### 1. Tag Management Page

**Access**: Click **🏷️ Manage Tags** in the sidebar navigation.

**Features:**
- **View Tags Tab**: See all tags with colored badges, edit/delete custom tags
- **Create Tag Tab**: Create new custom tags with colors and icons
- **Tag Statistics Tab**: View tag usage across lessons (bar chart + detailed breakdown)

**Creating a Custom Tag:**
1. Navigate to **🏷️ Manage Tags** → **Create Tag** tab
2. Fill in:
   - **Tag Name** (required): e.g., "HTB Challenges", "My Course"
   - **Color** (required): Pick a color using the color picker
   - **Icon** (optional): Enter an emoji like 🎯, 🔥, ⚡
   - **Description** (optional): What the tag represents
3. Click **Create Tag**

**Editing a Tag:**
1. Go to **View Tags** tab
2. Find a custom tag (not a system tag)
3. Click **Edit**
4. Modify fields and click **Save Changes**

**Deleting a Tag:**
1. Go to **View Tags** tab
2. Find a custom tag
3. Click **Delete** twice to confirm
4. **Note**: System tags (🔒) cannot be deleted

### 2. Lesson Browser with Tag Filtering

**Access**: Click **📚 My Learning** → Switch to **🏷️ By Tags** view mode

**Filtering Lessons:**
1. Use the multi-select dropdown to choose tags
2. Toggle **Match ALL tags** checkbox:
   - **OFF (default)**: Shows lessons with ANY selected tag
   - **ON**: Shows only lessons with ALL selected tags
3. Lessons are grouped by domain
4. Each lesson card displays its colored tag badges

**Example Use Cases:**
- View only "PWK Course" lessons for OSCP prep
- Filter "Advanced" + "DFIR" for advanced forensics
- Browse "Eric Zimmerman Tools" for tool-specific training
- See all "Built-In" lessons (default view)

### 3. Programmatic Tag Operations

**Adding Tags to Lessons:**
```python
from utils.database import Database

db = Database()

# Get tag ID
tag = db.get_tag_by_name("PWK Course")

# Add tag to lesson
lesson_id = "your-lesson-uuid"
db.add_tag_to_lesson(lesson_id, tag.tag_id)

db.close()
```

**Removing Tags:**
```python
db.remove_tag_from_lesson(lesson_id, tag_id)
```

**Getting Lesson Tags:**
```python
tags = db.get_lesson_tags(lesson_id)
for tag in tags:
    print(f"{tag.icon} {tag.name} - {tag.color}")
```

**Filtering Lessons by Tags:**
```python
from models.tag import TagFilter

# Get PWK Course lessons
pwk_tag = db.get_tag_by_name("PWK Course")
tag_filter = TagFilter(tag_ids=[pwk_tag.tag_id], match_all=False)
lessons = db.get_lessons_by_tags(tag_filter)

# Get lessons that are BOTH advanced AND SANS-aligned
advanced_tag = db.get_tag_by_name("Advanced")
sans_tag = db.get_tag_by_name("SANS-Aligned")
tag_filter = TagFilter(
    tag_ids=[advanced_tag.tag_id, sans_tag.tag_id],
    match_all=True  # Must have BOTH tags
)
lessons = db.get_lessons_by_tags(tag_filter)
```

---

## Merging Pull Requests with Tag Assignment

When merging PRs with new lessons (e.g., PR #13 with 60 DFIR lessons), tag them appropriately:

### Option 1: Manual Tagging via UI
1. Merge the PR
2. Run `python load_all_lessons.py` to load lessons into database
3. Open Tag Management page
4. For each new lesson domain, add appropriate tags

### Option 2: Batch Tagging Script

Create a helper script `tag_new_lessons.py`:

```python
from utils.database import Database
from uuid import UUID

db = Database()

# Get Eric Zimmerman Tools tag
ez_tag = db.get_tag_by_name("Eric Zimmerman Tools")
advanced_tag = db.get_tag_by_name("Advanced")

# Get all DFIR lessons from PR #13 (lessons 11-70)
all_lessons = db.get_all_lessons_metadata()

for lesson in all_lessons:
    if lesson.domain == "dfir" and lesson.order_index >= 11:
        # Add Advanced tag to difficulty 3 lessons
        if lesson.difficulty == 3:
            db.add_tag_to_lesson(str(lesson.lesson_id), advanced_tag.tag_id)

        # Tag Eric Zimmerman tool lessons (check title)
        lesson_full = db.get_lesson(lesson.lesson_id)
        if any(tool in lesson_full.title.lower() for tool in
               ["amcache", "prefetch", "shimcache", "mft", "recycle bin", "registry"]):
            db.add_tag_to_lesson(str(lesson.lesson_id), ez_tag.tag_id)

print("✅ Tagging complete!")
db.close()
```

### Option 3: Tag on Lesson Creation

When creating lessons via scripts, include tags in JSON:

```json
{
  "lesson_id": "uuid-here",
  "domain": "dfir",
  "title": "Eric Zimmerman's MFTECmd Deep Dive",
  "tags": ["tag-id-1", "tag-id-2"],  // Tag IDs
  ...
}
```

---

## Tag Best Practices

### Naming Conventions
- **Be specific**: "PWK Course" instead of "PWK"
- **Use title case**: "Eric Zimmerman Tools" not "eric zimmerman tools"
- **Avoid redundancy**: Don't create "DFIR-Advanced" when you can use both "DFIR" domain filter + "Advanced" tag

### Color Selection
- **Use distinct colors**: Make tags easily distinguishable at a glance
- **Color meaning**:
  - Blue/Green: Standard/built-in content
  - Red/Orange: Certification/course-aligned
  - Purple: Advanced difficulty
  - Gray: User/community content
  - Pink/Teal: Special categories

### Tag Organization Strategy

**Use tags for:**
- ✅ Cross-domain course alignment (PWK, SANS, HTB)
- ✅ Tool-specific training (Eric Zimmerman, Volatility, Metasploit)
- ✅ Difficulty modifiers (Advanced, Expert)
- ✅ Content source (Built-In, User Content, Community)
- ✅ Certification prep (OSCP, GCFE, GPEN)

**Don't use tags for:**
- ❌ Domain classification (use existing domain field)
- ❌ Difficulty levels 1-3 (use existing difficulty field)
- ❌ Lesson order/sequence (use order_index field)

---

## API Reference

### Database Methods

**Tag CRUD:**
```python
db.create_tag(tag: Tag) -> bool
db.get_tag(tag_id: str) -> Optional[Tag]
db.get_tag_by_name(name: str) -> Optional[Tag]
db.get_all_tags() -> List[Tag]
db.update_tag(tag_id: str, update: TagUpdate) -> bool
db.delete_tag(tag_id: str) -> bool  # Raises ValueError if system tag
```

**Lesson-Tag Association:**
```python
db.add_tag_to_lesson(lesson_id: str, tag_id: str) -> bool
db.remove_tag_from_lesson(lesson_id: str, tag_id: str) -> bool
db.get_lesson_tags(lesson_id: str) -> List[Tag]
```

**Filtering & Stats:**
```python
db.get_lessons_by_tags(tag_filter: TagFilter) -> List[LessonMetadata]
db.get_tag_stats() -> Dict[str, int]  # {tag_name: lesson_count}
```

### Pydantic Models

**Tag:**
```python
from models.tag import Tag

tag = Tag(
    tag_id="uuid",
    name="My Tag",
    color="#FF0000",  # Hex color
    icon="🔥",         # Optional emoji
    description="Description",
    created_at=datetime.utcnow(),
    is_system=False
)
```

**TagFilter:**
```python
from models.tag import TagFilter

# Match ANY tag
filter1 = TagFilter(tag_ids=["tag1", "tag2"], match_all=False)

# Match ALL tags
filter2 = TagFilter(tag_ids=["tag1", "tag2"], match_all=True)
```

---

## Troubleshooting

### Issue: Migration fails with "table already exists"
**Solution**: Tables already created. Safe to ignore or drop tables first:
```bash
sqlite3 cyberlearn.db "DROP TABLE IF EXISTS lesson_tags; DROP TABLE IF EXISTS tags;"
python add_tags_system.py
```

### Issue: No lessons appear when filtering by tags
**Solution**: Check if lessons have the selected tags:
```python
db = Database()
lesson = db.get_lesson("lesson-uuid")
tags = db.get_lesson_tags(str(lesson.lesson_id))
print(f"Lesson tags: {[t.name for t in tags]}")
```

### Issue: Cannot delete a tag
**Solution**: Only custom tags can be deleted. System tags (is_system=True) are protected:
```python
tag = db.get_tag_by_name("Built-In")
print(f"Is system tag: {tag.is_system}")  # True = cannot delete
```

### Issue: Tag colors not displaying
**Solution**: Ensure color is valid hex format:
```python
# Valid
color = "#3B82F6"

# Invalid
color = "blue"  # Must use hex code
```

---

## Future Enhancements

### Planned Features
- **Tag Import/Export**: Export lessons with tags as ZIP packages
- **Tag Hierarchies**: Parent-child tag relationships (e.g., "Forensics" → "Registry Forensics")
- **Smart Tag Suggestions**: Auto-suggest tags based on lesson content
- **Tag Analytics**: Most popular tags, tag usage trends over time
- **Tag-Based Achievements**: Earn badges for completing all lessons with a specific tag

### Extension Ideas
- **Tag Permissions**: User vs admin-created tags
- **Tag Subscriptions**: Follow specific tags for notifications
- **Tag-Based Learning Paths**: Curated sequences by tag
- **Tag Cloud Visualization**: Interactive tag cloud on dashboard

---

## Summary

The tag system provides **flexible, multi-dimensional lesson organization** beyond the fixed domain structure. It enables:

1. **Course Alignment**: Group lessons for specific certifications (PWK, SANS)
2. **Tool-Specific Training**: Focus on particular toolsets (Eric Zimmerman, Volatility)
3. **Custom Collections**: Create personal learning paths
4. **Content Source Tracking**: Distinguish built-in, user, and community content
5. **Advanced Filtering**: Find exactly the lessons you need

**Get Started:**
```bash
# 1. Run migration
python add_tags_system.py

# 2. Launch app
streamlit run app.py

# 3. Go to 🏷️ Manage Tags to create custom tags
# 4. Browse lessons using 📚 My Learning → 🏷️ By Tags
```

---

## Questions & Support

**File Structure:**
- `models/tag.py` - Tag Pydantic models
- `utils/database.py` - Database methods (lines 627-907)
- `add_tags_system.py` - Migration script
- `ui/pages/tag_management.py` - Tag management UI
- `ui/components/lesson_browser.py` - Tag-based lesson browser
- `ui/pages/lesson_viewer.py` - Updated with tag view mode

**Need help?** Check the inline documentation in each file or review the database schema at the top of this guide.
