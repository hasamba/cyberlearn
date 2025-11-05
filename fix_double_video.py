#!/usr/bin/env python3
"""
Quick fix to add iframe removal code to lesson_viewer.py
This prevents double video embedding (iframe + st.video)
"""

import re
from pathlib import Path

def fix_lesson_viewer():
    """Add iframe removal code to render_video_block function"""

    file_path = Path("ui/pages/lesson_viewer.py")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if fix is already applied
    if "Remove any iframe HTML" in content:
        print("Fix already applied - iframe removal code is present")
        return

    # Find the location to insert the iframe removal code
    # Look for the pattern: text_content = text_content.replace('\\n', '\n')
    pattern = r"(text_content = text_content\.replace\('\\\\n', '\\n'\))"

    replacement = r"""\1

        # Remove any iframe HTML from text before rendering
        # This prevents double rendering (iframe in text + st.video below)
        import re
        text_content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', text_content, flags=re.DOTALL | re.IGNORECASE)"""

    new_content = re.sub(pattern, replacement, content)

    if new_content == content:
        print("ERROR: Could not find location to insert fix")
        print("Manual edit required")
        return

    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("SUCCESS: Added iframe removal code to lesson_viewer.py")
    print("Restart Streamlit to apply the fix")

if __name__ == "__main__":
    fix_lesson_viewer()
