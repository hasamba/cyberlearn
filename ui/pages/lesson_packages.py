"""
Lesson Package Import/Export Page

Import and export lesson packages as ZIP files:
- Export: Select multiple lessons and download as ZIP
- Import: Upload ZIP file, extract, validate, and import all lessons
- Auto-create package tag from ZIP filename
"""

import streamlit as st
import json
import zipfile
import io
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from uuid import uuid4
from models.lesson import Lesson
from pydantic import ValidationError

def render_lesson_packages_page():
    """Render the lesson package import/export page"""

    st.title("📦 Lesson Packages")

    db = st.session_state.db
    user = st.session_state.current_user

    # Tabs for Import and Export
    tab_import, tab_export = st.tabs(["📥 Import Package", "📤 Export Package"])

    with tab_import:
        render_import_tab(db, user)

    with tab_export:
        render_export_tab(db, user)


def render_import_tab(db, user):
    """Render the import package tab"""

    st.markdown("""
    ### Import Lesson Package

    Upload a ZIP file containing multiple lesson JSON files. All lessons will be:
    - ✅ Validated against the lesson schema
    - 🏷️ Tagged with the package name (from ZIP filename)
    - 📦 Tagged with "User Content"
    - 🔍 Checked for duplicates
    """)

    st.markdown("---")

    # ZIP file uploader
    uploaded_zip = st.file_uploader(
        "Select lesson package (ZIP file)",
        type=['zip'],
        help="Upload a ZIP file containing lesson JSON files"
    )

    if uploaded_zip:
        st.success(f"📁 Selected: {uploaded_zip.name} ({uploaded_zip.size / 1024:.1f} KB)")

        # Package name from filename (remove .zip extension)
        package_name = Path(uploaded_zip.name).stem

        # Display package info
        st.info(f"**Package Name:** {package_name}")

        st.markdown("---")

        # Import button
        if st.button("🚀 Import Package", type="primary", use_container_width=True):
            import_package(uploaded_zip, package_name, db, user)

    else:
        st.info("👆 Select a ZIP file to import")

        # Usage instructions
        with st.expander("ℹ️ How to Import Packages"):
            st.markdown("""
            ### Package Structure

            ZIP files should contain lesson JSON files:

            ```
            my-lesson-package.zip
            ├── lesson1.json
            ├── lesson2.json
            ├── lesson3.json
            └── ... (more lesson files)
            ```

            ### What Happens on Import

            1. ZIP file is extracted
            2. All JSON files are validated
            3. Package tag is created from ZIP filename (e.g., "Package: My Lesson Package")
            4. All lessons are imported and tagged
            5. Detailed import report provided

            ### Tips

            - Max ZIP size: 50MB
            - All JSON files must be valid lessons
            - Duplicate lesson_ids will be skipped
            - Package name is derived from ZIP filename
            """)


def render_export_tab(db, user):
    """Render the export package tab"""

    st.markdown("""
    ### Export Lesson Package

    Select multiple lessons to export as a ZIP package.
    """)

    st.markdown("---")

    # Filters in columns
    col1, col2 = st.columns(2)

    with col1:
        # Domain selector
        all_domains = [
            "fundamentals", "osint", "dfir", "malware",
            "active_directory", "system", "linux", "cloud",
            "pentest", "red_team", "blue_team", "threat_hunting",
            "ai_security", "iot_security", "web3_security"
        ]
        selected_domain = st.selectbox("Filter by Domain", ["All Domains"] + all_domains)

    with col2:
        # Tag selector
        all_tags = db.get_filterable_tags(str(user.user_id))
        tag_names = ["All Tags"] + [tag.name for tag in all_tags]
        selected_tag = st.selectbox("Filter by Tag", tag_names)

    # Get lessons based on filters
    if selected_tag != "All Tags":
        # Filter by tag
        from models.tag import TagFilter
        tag = db.get_tag_by_name(selected_tag)
        if tag:
            tag_filter = TagFilter(tag_ids=[tag.tag_id], match_all=False)
            all_lessons_metadata = db.get_lessons_by_tags(tag_filter)

            # Further filter by domain if selected
            if selected_domain != "All Domains":
                all_lessons_metadata = [l for l in all_lessons_metadata if l.domain == selected_domain]
    else:
        # No tag filter, just domain
        if selected_domain == "All Domains":
            all_lessons_metadata = db.get_all_lessons_metadata()
        else:
            all_lessons_metadata = db.get_lessons_by_domain(selected_domain)

    if not all_lessons_metadata:
        st.warning("No lessons found matching filters")
        return

    st.success(f"Found {len(all_lessons_metadata)} lessons")

    # Lesson selector (multiselect with lesson titles)
    lesson_options = {
        f"{lesson.title} ({lesson.domain})": str(lesson.lesson_id)
        for lesson in all_lessons_metadata
    }

    selected_titles = st.multiselect(
        "Select lessons to export",
        options=list(lesson_options.keys()),
        help="Select one or more lessons to include in the package"
    )

    if selected_titles:
        selected_lesson_ids = [lesson_options[title] for title in selected_titles]

        st.success(f"✅ Selected {len(selected_lesson_ids)} lesson(s)")

        # Package name input
        default_package_name = f"lesson-package-{datetime.now().strftime('%Y%m%d')}"
        package_name = st.text_input(
            "Package Name",
            value=default_package_name,
            help="Name for the ZIP file (without .zip extension)"
        )

        # Export button
        if st.button("📦 Export Package", type="primary", use_container_width=True):
            export_package(selected_lesson_ids, package_name, db)

    else:
        st.info("👆 Select lessons to export")


def import_package(uploaded_zip: Any, package_name: str, db, user):
    """Import lessons from ZIP package"""

    st.markdown("### 🔍 Import Results")

    try:
        # Check ZIP size (max 50MB)
        if uploaded_zip.size > 50 * 1024 * 1024:
            st.error(f"❌ ZIP file too large: {uploaded_zip.size / (1024 * 1024):.1f} MB (max 50MB)")
            return

        # Extract ZIP
        with zipfile.ZipFile(io.BytesIO(uploaded_zip.read())) as zip_file:
            # Get all JSON files
            json_files = [f for f in zip_file.namelist() if f.endswith('.json') and not f.startswith('__MACOSX')]

            if not json_files:
                st.error("❌ No JSON files found in ZIP package")
                return

            st.info(f"📄 Found {len(json_files)} JSON file(s) in package")

            # Create package tag
            package_tag_name = f"Package: {package_name.replace('_', ' ').replace('-', ' ').title()}"
            package_tag = db.get_tag_by_name(package_tag_name)

            if not package_tag:
                # Create new package tag
                cursor = db.conn.cursor()

                # Generate random color
                import random
                colors = ["#EF4444", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]
                color = random.choice(colors)

                cursor.execute("""
                    INSERT INTO tags (tag_id, name, color, icon, description, is_system, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    db.conn.execute("SELECT COALESCE(MAX(tag_id), 0) + 1 FROM tags").fetchone()[0],
                    package_tag_name,
                    color,
                    "📦",
                    f"Lessons from {package_name} package",
                    1,
                    datetime.now().isoformat()
                ))
                db.conn.commit()

                package_tag = db.get_tag_by_name(package_tag_name)
                st.success(f"✅ Created package tag: {package_tag_name}")

            # Get "User Content" tag
            user_content_tag = db.get_tag_by_name("Package: User Content")
            if not user_content_tag:
                st.error("❌ 'Package: User Content' tag not found")
                return

            # Process each JSON file
            results = {
                'success': [],
                'errors': [],
                'duplicates': []
            }

            for json_filename in json_files:
                st.markdown(f"#### 📄 {json_filename}")

                try:
                    # Read JSON content
                    json_content = zip_file.read(json_filename).decode('utf-8')
                    lesson_data = json.loads(json_content)

                    # Validate
                    try:
                        lesson = Lesson(**lesson_data)
                    except ValidationError as e:
                        error_details = []
                        for error in e.errors():
                            field = ' -> '.join(str(loc) for loc in error['loc'])
                            error_details.append(f"{field}: {error['msg']}")

                        results['errors'].append({
                            'file': json_filename,
                            'error': 'Validation failed',
                            'details': error_details
                        })

                        st.error(f"❌ Validation failed")
                        for detail in error_details:
                            st.caption(f"  - {detail}")
                        continue

                    # Check duplicate
                    existing = db.get_lesson(lesson.lesson_id)
                    if existing:
                        results['duplicates'].append({
                            'file': json_filename,
                            'lesson_id': str(lesson.lesson_id),
                            'title': lesson.title
                        })
                        st.warning(f"⚠️ Duplicate: {lesson.title}")
                        continue

                    # Import lesson
                    success = db.create_lesson(lesson)

                    if success:
                        # Tag with package and user content
                        db.add_tag_to_lesson(str(lesson.lesson_id), package_tag.tag_id)
                        db.add_tag_to_lesson(str(lesson.lesson_id), user_content_tag.tag_id)

                        results['success'].append({
                            'file': json_filename,
                            'lesson_id': str(lesson.lesson_id),
                            'title': lesson.title,
                            'domain': lesson.domain
                        })

                        st.success(f"✅ Imported: {lesson.title}")
                    else:
                        results['errors'].append({
                            'file': json_filename,
                            'error': 'Database insert failed'
                        })
                        st.error(f"❌ Database insert failed")

                except Exception as e:
                    results['errors'].append({
                        'file': json_filename,
                        'error': str(e)
                    })
                    st.error(f"❌ Error: {str(e)}")

            st.markdown("---")

            # Display summary
            display_import_summary(results, package_name)

    except zipfile.BadZipFile:
        st.error("❌ Invalid ZIP file")
    except Exception as e:
        st.error(f"❌ Error processing ZIP: {str(e)}")


def export_package(lesson_ids: List[str], package_name: str, db):
    """Export lessons as ZIP package"""

    try:
        # Create in-memory ZIP
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            exported_count = 0

            for lesson_id in lesson_ids:
                # Get full lesson
                lesson = db.get_lesson(lesson_id)

                if lesson:
                    # Serialize to JSON
                    lesson_json = lesson.model_dump_json(indent=2)

                    # Add to ZIP with sanitized filename
                    filename = f"lesson_{lesson.domain}_{lesson.order_index:03d}_{lesson.title[:30].replace(' ', '_')}.json"
                    zip_file.writestr(filename, lesson_json)

                    exported_count += 1

            # Create package metadata file
            metadata = {
                "package_name": package_name,
                "version": "1.0",
                "created_date": datetime.now().isoformat(),
                "lesson_count": exported_count,
                "lesson_ids": lesson_ids
            }

            zip_file.writestr("package.json", json.dumps(metadata, indent=2))

        # Prepare download
        zip_buffer.seek(0)

        st.success(f"✅ Package created with {exported_count} lesson(s)")

        # Download button
        st.download_button(
            label="📥 Download Package",
            data=zip_buffer,
            file_name=f"{package_name}.zip",
            mime="application/zip",
            use_container_width=True,
            type="primary"
        )

    except Exception as e:
        st.error(f"❌ Error creating package: {str(e)}")


def display_import_summary(results: Dict[str, List], package_name: str):
    """Display import summary"""

    st.markdown("## 📊 Import Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("✅ Success", len(results['success']))

    with col2:
        st.metric("❌ Errors", len(results['errors']))

    with col3:
        st.metric("⚠️ Duplicates", len(results['duplicates']))

    # Success details
    if results['success']:
        with st.expander(f"✅ Imported Lessons ({len(results['success'])})"):
            for item in results['success']:
                st.markdown(f"- **{item['title']}** ({item['domain']})")

    # Error details
    if results['errors']:
        with st.expander(f"❌ Errors ({len(results['errors'])})"):
            for item in results['errors']:
                st.markdown(f"- **{item['file']}**: {item['error']}")
                if 'details' in item:
                    for detail in item['details']:
                        st.caption(f"  - {detail}")

    # Duplicate details
    if results['duplicates']:
        with st.expander(f"⚠️ Duplicates ({len(results['duplicates'])})"):
            for item in results['duplicates']:
                st.markdown(f"- **{item['title']}**")

    if results['success']:
        st.success(f"🎉 Package '{package_name}' imported successfully!")

        if st.button("📚 Go to My Learning", use_container_width=True):
            st.session_state.current_page = "learning"
            st.rerun()
