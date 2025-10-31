"""
Lesson Upload Page

Allows users to upload single or multiple JSON lesson files.
Validates lessons against Pydantic model and auto-tags with "User Content".
"""

import streamlit as st
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from models.lesson import Lesson
from pydantic import ValidationError

def render_upload_lessons_page():
    """Render the lesson upload page"""

    st.title("📤 Upload Lessons")

    db = st.session_state.db
    user = st.session_state.current_user

    st.markdown("""
    Upload one or multiple lesson JSON files to add them to your lesson catalog.

    **Features:**
    - ✅ Automatic validation against lesson schema
    - 🏷️ Auto-tagged with "User Content"
    - 🔍 Duplicate detection (by lesson_id)
    - 📊 Detailed validation feedback
    """)

    st.markdown("---")

    # File uploader
    uploaded_files = st.file_uploader(
        "Select lesson JSON files",
        type=['json'],
        accept_multiple_files=True,
        help="Select one or more JSON lesson files to upload"
    )

    if uploaded_files:
        st.success(f"📁 Selected {len(uploaded_files)} file(s)")

        # Display file names
        with st.expander("Selected Files"):
            for file in uploaded_files:
                st.markdown(f"- {file.name} ({file.size / 1024:.1f} KB)")

        st.markdown("---")

        # Upload button
        if st.button("🚀 Upload and Validate", type="primary", use_container_width=True):
            upload_lessons(uploaded_files, db, user)

    else:
        st.info("👆 Select JSON lesson files to upload")

        # Usage instructions
        with st.expander("ℹ️ How to Upload Lessons"):
            st.markdown("""
            ### File Format

            Lesson files must be valid JSON matching the Lesson schema:

            ```json
            {
              "lesson_id": "uuid-here",
              "domain": "fundamentals",
              "title": "Lesson Title",
              "difficulty": 1,
              "order_index": 1,
              "estimated_time": 30,
              "prerequisites": [],
              "learning_objectives": ["objective 1", "objective 2"],
              "concepts": ["concept 1", "concept 2"],
              "content_blocks": [...],
              "post_assessment": [...],
              "jim_kwik_principles": [...],
              ...
            }
            ```

            ### Validation Rules

            - **lesson_id**: Must be a valid UUID
            - **domain**: Must be one of the 15 domains
            - **difficulty**: 1 (beginner), 2 (intermediate), or 3 (advanced)
            - **estimated_time**: Max 60 minutes
            - **content_blocks**: Must use valid ContentType values
            - **post_assessment**: Questions must have question_id and explanation

            ### What Happens on Upload

            1. Each file is validated against the Lesson schema
            2. Duplicate lesson_id check (skips if already exists)
            3. Lesson is added to database
            4. Automatically tagged with "User Content"
            5. Success/error feedback provided

            ### Tips

            - Max file size: 5MB per file
            - Use valid UUIDs for lesson_id
            - Ensure prerequisites reference existing lessons
            - Check validation errors carefully before re-uploading
            """)


def upload_lessons(uploaded_files: List[Any], db, user):
    """Process and validate uploaded lesson files"""

    st.markdown("### 🔍 Validation Results")

    results = {
        'success': [],
        'errors': [],
        'duplicates': [],
        'skipped': []
    }

    # Get "User Content" tag
    user_content_tag = db.get_tag_by_name("Package: User Content")
    if not user_content_tag:
        st.error("❌ 'Package: User Content' tag not found in database. Please run add_all_tags.py")
        return

    for file in uploaded_files:
        st.markdown(f"#### 📄 {file.name}")

        try:
            # Check file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                results['errors'].append({
                    'file': file.name,
                    'error': 'File too large (max 5MB)'
                })
                st.error(f"❌ File too large: {file.size / (1024 * 1024):.1f} MB (max 5MB)")
                continue

            # Parse JSON
            try:
                file_content = file.read().decode('utf-8')
                lesson_data = json.loads(file_content)
            except json.JSONDecodeError as e:
                results['errors'].append({
                    'file': file.name,
                    'error': f'Invalid JSON: {str(e)}'
                })
                st.error(f"❌ Invalid JSON: {str(e)}")
                continue

            # Validate against Lesson model
            try:
                lesson = Lesson(**lesson_data)
            except ValidationError as e:
                error_details = []
                for error in e.errors():
                    field = ' -> '.join(str(loc) for loc in error['loc'])
                    error_details.append(f"  - **{field}**: {error['msg']}")

                results['errors'].append({
                    'file': file.name,
                    'error': 'Validation failed',
                    'details': error_details
                })

                st.error("❌ Validation failed:")
                for detail in error_details:
                    st.markdown(detail)
                continue

            # Check for duplicate
            existing = db.get_lesson(lesson.lesson_id)
            if existing:
                results['duplicates'].append({
                    'file': file.name,
                    'lesson_id': str(lesson.lesson_id),
                    'title': lesson.title
                })
                st.warning(f"⚠️ Duplicate: Lesson already exists (ID: {lesson.lesson_id})")
                continue

            # Add to database
            success = db.create_lesson(lesson)

            if success:
                # Tag with User Content
                db.add_tag_to_lesson(str(lesson.lesson_id), user_content_tag.tag_id)

                results['success'].append({
                    'file': file.name,
                    'lesson_id': str(lesson.lesson_id),
                    'title': lesson.title,
                    'domain': lesson.domain
                })

                st.success(f"✅ Uploaded successfully")
                st.caption(f"📚 {lesson.title}")
                st.caption(f"🏷️ Domain: {lesson.domain} | Difficulty: {lesson.difficulty}")
            else:
                results['errors'].append({
                    'file': file.name,
                    'error': 'Database insert failed'
                })
                st.error("❌ Database insert failed")

        except Exception as e:
            results['errors'].append({
                'file': file.name,
                'error': f'Unexpected error: {str(e)}'
            })
            st.error(f"❌ Unexpected error: {str(e)}")

        st.markdown("---")

    # Summary
    display_upload_summary(results)


def display_upload_summary(results: Dict[str, List]):
    """Display summary of upload results"""

    st.markdown("## 📊 Upload Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("✅ Success", len(results['success']))

    with col2:
        st.metric("❌ Errors", len(results['errors']))

    with col3:
        st.metric("⚠️ Duplicates", len(results['duplicates']))

    with col4:
        total = len(results['success']) + len(results['errors']) + len(results['duplicates'])
        st.metric("📁 Total", total)

    # Success details
    if results['success']:
        with st.expander(f"✅ Successfully Uploaded ({len(results['success'])})"):
            for item in results['success']:
                st.markdown(f"- **{item['title']}** ({item['domain']})")
                st.caption(f"  File: {item['file']} | ID: {item['lesson_id']}")

    # Error details
    if results['errors']:
        with st.expander(f"❌ Errors ({len(results['errors'])})"):
            for item in results['errors']:
                st.markdown(f"- **{item['file']}**: {item['error']}")
                if 'details' in item:
                    for detail in item['details']:
                        st.markdown(detail)

    # Duplicate details
    if results['duplicates']:
        with st.expander(f"⚠️ Duplicates ({len(results['duplicates'])})"):
            for item in results['duplicates']:
                st.markdown(f"- **{item['title']}**")
                st.caption(f"  File: {item['file']} | ID: {item['lesson_id']}")

    st.markdown("---")

    # Next steps
    if results['success']:
        st.info(f"✨ {len(results['success'])} lesson(s) uploaded successfully! They are now available in your lesson catalog.")

        if st.button("📚 Go to My Learning", use_container_width=True):
            st.session_state.current_page = "learning"
            st.rerun()
