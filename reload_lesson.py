"""
Force reload a specific lesson from JSON into database
Usage: python reload_lesson.py <lesson_file.json>
"""

import sys
import json
from pathlib import Path
from utils.database import Database
from models.lesson import Lesson

if len(sys.argv) < 2:
    print("Usage: python reload_lesson.py <lesson_file.json>")
    print("Example: python reload_lesson.py content/lesson_dfir_15_jlecmd_RICH.json")
    sys.exit(1)

lesson_file = Path(sys.argv[1])

if not lesson_file.exists():
    print(f"[ERROR] File not found: {lesson_file}")
    sys.exit(1)

# Load lesson from JSON
print(f"\n[LOADING] {lesson_file.name}")
with open(lesson_file, 'r', encoding='utf-8') as f:
    lesson_data = json.load(f)

lesson = Lesson(**lesson_data)
print(f"  Title: {lesson.title}")
print(f"  ID: {lesson.lesson_id}")

# Connect to database
db = Database()

# Check if lesson exists
existing = db.get_lesson(lesson.lesson_id)

if existing:
    print(f"\n[DELETE] Removing old version from database...")
    cursor = db.conn.cursor()
    cursor.execute('DELETE FROM lessons WHERE lesson_id = ?', (str(lesson.lesson_id),))
    db.conn.commit()
    print(f"  [OK] Deleted")

# Insert new version
print(f"\n[INSERT] Loading new version into database...")
db.create_lesson(lesson)
print(f"  [OK] Loaded")

db.close()

print(f"\n[SUCCESS] Lesson reloaded successfully!")
print(f"Restart Streamlit to see changes: streamlit run app.py")
