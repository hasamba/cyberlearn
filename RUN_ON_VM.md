# Commands to Run on VM

## Tag System Setup

### 1. Run Database Migration (Required)

```bash
cd /path/to/cyberlearn
python add_tags_system.py
```

**What this does:**
- Creates `tags` table
- Creates `lesson_tags` junction table
- Adds 8 default system tags
- Auto-tags all existing lessons as "Built-In"

**Expected output:**
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
```

### 2. Launch Application

```bash
streamlit run app.py
```

### 3. Verify Installation

```bash
# Check tag count
python -c "from utils.database import Database; db = Database(); print(f'Tags: {len(db.get_all_tags())}'); db.close()"

# Expected output: Tags: 8
```

---

## Using the Tag System

### Access Tag Management
1. Login to CyberLearn
2. Click **🏷️ Manage Tags** in sidebar
3. Create/edit/view tags

### Browse Lessons by Tags
1. Click **📚 My Learning**
2. Toggle to **🏷️ By Tags** view
3. Select tags from dropdown
4. Browse filtered lessons

---

## After Merging PR #13 (60 DFIR Lessons)

### Tag Eric Zimmerman Tool Lessons

Create `tag_pr13_lessons.py`:

```python
from utils.database import Database

db = Database()

# Get tags
ez_tag = db.get_tag_by_name("Eric Zimmerman Tools")
advanced_tag = db.get_tag_by_name("Advanced")
sans_tag = db.get_tag_by_name("SANS-Aligned")

# Get DFIR lessons from PR #13 (order_index >= 11)
all_lessons = db.get_all_lessons_metadata()

for lesson_meta in all_lessons:
    if lesson_meta.domain == "dfir" and lesson_meta.order_index >= 11:
        lesson = db.get_lesson(lesson_meta.lesson_id)

        # Tag Eric Zimmerman tool lessons
        ez_tools = ["amcache", "prefetch", "shimcache", "mft", "recycle bin",
                    "registry", "shellbags", "jump list", "lnk"]

        if any(tool in lesson.title.lower() for tool in ez_tools):
            db.add_tag_to_lesson(str(lesson.lesson_id), ez_tag.tag_id)
            print(f"✓ Eric Z Tools: {lesson.title}")

        # Tag advanced lessons (difficulty 3)
        if lesson.difficulty == 3:
            db.add_tag_to_lesson(str(lesson.lesson_id), advanced_tag.tag_id)
            print(f"✓ Advanced: {lesson.title}")

        # Tag SANS-aligned lessons
        if "sans" in lesson.title.lower() or lesson_meta.order_index >= 36:
            db.add_tag_to_lesson(str(lesson.lesson_id), sans_tag.tag_id)
            print(f"✓ SANS-Aligned: {lesson.title}")

print("\n✅ Tagging complete!")
db.close()
```

Run it:
```bash
python tag_pr13_lessons.py
```

---

## Testing Checklist

### Basic Tests
```bash
# Test 1: Check tags exist
python -c "from utils.database import Database; db = Database(); tags = db.get_all_tags(); print(f'Found {len(tags)} tags:'); [print(f'  {t.icon} {t.name}') for t in tags]; db.close()"

# Test 2: Check lessons are tagged
python -c "from utils.database import Database; db = Database(); stats = db.get_tag_stats(); print('Tag usage:'); [print(f'  {k}: {v} lessons') for k,v in stats.items()]; db.close()"

# Test 3: Filter by Built-In tag
python -c "from utils.database import Database; from models.tag import TagFilter; db = Database(); tag = db.get_tag_by_name('Built-In'); filt = TagFilter(tag_ids=[tag.tag_id], match_all=False); lessons = db.get_lessons_by_tags(filt); print(f'Found {len(lessons)} Built-In lessons'); db.close()"
```

### UI Tests
1. ✅ Navigate to 🏷️ Manage Tags
2. ✅ Create a custom tag
3. ✅ View tag statistics
4. ✅ Go to 📚 My Learning → 🏷️ By Tags
5. ✅ Filter by "Built-In" (should show all lessons)
6. ✅ Verify lesson cards show colored badges

---

## Troubleshooting

### Issue: "table already exists"
**Solution**: Tables already created, safe to skip or drop first:
```bash
sqlite3 cyberlearn.db "DROP TABLE IF EXISTS lesson_tags; DROP TABLE IF EXISTS tags;"
python add_tags_system.py
```

### Issue: No tags visible in UI
**Solution**: Verify migration ran successfully:
```bash
sqlite3 cyberlearn.db "SELECT COUNT(*) FROM tags;"
# Should output: 8
```

### Issue: Import error for models.tag
**Solution**: Ensure models/tag.py exists and restart Streamlit

---

## Quick Reference

| Action | Command |
|--------|---------|
| Run migration | `python add_tags_system.py` |
| Launch app | `streamlit run app.py` |
| Check tags | `python -c "from utils.database import Database; db = Database(); print(len(db.get_all_tags())); db.close()"` |
| Tag stats | `python -c "from utils.database import Database; db = Database(); print(db.get_tag_stats()); db.close()"` |

---

## Documentation

- **Quick Start**: [QUICK_START_TAG_SYSTEM.md](QUICK_START_TAG_SYSTEM.md)
- **Full Guide**: [TAG_SYSTEM_GUIDE.md](TAG_SYSTEM_GUIDE.md)
- **Implementation**: [TAG_SYSTEM_IMPLEMENTATION_SUMMARY.md](TAG_SYSTEM_IMPLEMENTATION_SUMMARY.md)
- **UI Preview**: [TAG_SYSTEM_UI_PREVIEW.md](TAG_SYSTEM_UI_PREVIEW.md)

---

## Summary

**Step 1**: Run migration
```bash
python add_tags_system.py
```

**Step 2**: Launch app
```bash
streamlit run app.py
```

**Step 3**: Test in browser
- Login
- Click 🏷️ Manage Tags
- Create a custom tag
- Browse lessons with 🏷️ By Tags view

**Done!** Your platform now has a comprehensive tag system.
