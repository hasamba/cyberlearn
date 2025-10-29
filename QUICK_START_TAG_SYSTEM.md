# Quick Start: Tag System

## 1-Minute Setup

### On Your VM:

```bash
# Step 1: Run migration (creates tables + default tags)
python add_tags_system.py

# Step 2: Launch the app
streamlit run app.py
```

**Done!** Your platform now has tags.

---

## Using Tags (5 minutes)

### Create a Custom Tag

1. Login to CyberLearn
2. Click **🏷️ Manage Tags** in sidebar
3. Go to **Create Tag** tab
4. Fill in:
   - Name: "My Course"
   - Color: Pick a color
   - Icon: 🎯
   - Description: "My custom training course"
5. Click **Create Tag**

### Filter Lessons by Tags

1. Go to **📚 My Learning**
2. Toggle to **🏷️ By Tags** view
3. Select tags from dropdown (e.g., "Built-In", "Advanced")
4. Browse filtered lessons

---

## What You Get

- **8 default tags** (Built-In, Advanced, PWK Course, Eric Zimmerman Tools, SANS-Aligned, User Content, Community, Certification Prep)
- **All existing lessons** auto-tagged as "Built-In"
- **Tag management UI** for creating custom tags
- **Tag-based filtering** in lesson browser
- **Colored tag badges** on all lesson cards

---

## Next Steps

1. **Test it**: Filter lessons by "Built-In" tag
2. **Create tags**: Add tags for your courses/certifications
3. **Tag PR lessons**: When merging PR #13, tag Eric Zimmerman lessons appropriately

---

## Full Documentation

- **Complete Guide**: [TAG_SYSTEM_GUIDE.md](TAG_SYSTEM_GUIDE.md)
- **Implementation Details**: [TAG_SYSTEM_IMPLEMENTATION_SUMMARY.md](TAG_SYSTEM_IMPLEMENTATION_SUMMARY.md)

---

## Example: Tag PR #13 Lessons

After merging PR #13 (60 DFIR lessons):

```python
from utils.database import Database

db = Database()

# Get tags
ez_tag = db.get_tag_by_name("Eric Zimmerman Tools")
advanced_tag = db.get_tag_by_name("Advanced")

# Get DFIR lessons
lessons = db.get_lessons_by_domain("dfir")

for lesson_meta in lessons:
    lesson = db.get_lesson(lesson_meta.lesson_id)

    # Tag Eric Zimmerman tool lessons
    if any(tool in lesson.title.lower() for tool in
           ["amcache", "prefetch", "shimcache", "mft", "recycle bin", "registry"]):
        db.add_tag_to_lesson(str(lesson.lesson_id), ez_tag.tag_id)
        print(f"✓ Tagged: {lesson.title}")

    # Tag advanced lessons
    if lesson.difficulty == 3:
        db.add_tag_to_lesson(str(lesson.lesson_id), advanced_tag.tag_id)

print("✅ Tagging complete!")
db.close()
```

---

## That's It!

**Questions?** Check [TAG_SYSTEM_GUIDE.md](TAG_SYSTEM_GUIDE.md) for detailed documentation.
