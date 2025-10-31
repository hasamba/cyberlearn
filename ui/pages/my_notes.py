"""
My Notes Page

View and manage all notes across all lessons.
Features:
- View all notes in one place
- Search notes by content
- Filter by lesson, domain, pinned status
- Export notes
- Quick navigation to lessons
"""

import streamlit as st
import json
from datetime import datetime
from typing import List, Dict, Optional

def render_my_notes_page():
    """Render the my notes management page"""

    st.title("📝 My Notes")

    db = st.session_state.db
    user = st.session_state.current_user

    # Get all notes for user
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT n.note_id, n.lesson_id, n.content_block_index, n.note_text,
               n.attachments, n.is_pinned, n.created_at, n.updated_at,
               l.title as lesson_title, l.domain
        FROM lesson_notes n
        JOIN lessons l ON n.lesson_id = l.lesson_id
        WHERE n.user_id = ?
        ORDER BY n.is_pinned DESC, n.created_at DESC
    """, (str(user.user_id),))

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    all_notes = []
    for row in rows:
        note_dict = dict(zip(columns, row))
        all_notes.append(note_dict)

    if not all_notes:
        st.info("You haven't created any notes yet! Start taking notes while learning to build your personal knowledge base.")

        if st.button("📚 Go to My Learning"):
            st.session_state.current_page = "learning"
            st.rerun()
        return

    # Statistics
    total_notes = len(all_notes)
    pinned_notes = len([n for n in all_notes if n['is_pinned']])
    lessons_with_notes = len(set(n['lesson_id'] for n in all_notes))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Total Notes", total_notes)
    with col2:
        st.metric("📌 Pinned", pinned_notes)
    with col3:
        st.metric("📚 Lessons", lessons_with_notes)

    st.markdown("---")

    # Filters and Search
    col_search, col_domain, col_pinned = st.columns([2, 1, 1])

    with col_search:
        search_query = st.text_input(
            "🔍 Search notes",
            placeholder="Search by content...",
            key="notes_search"
        )

    with col_domain:
        # Domain filter
        all_domains = sorted(set(n['domain'] for n in all_notes))
        selected_domain = st.selectbox("Domain", ["All Domains"] + all_domains)

    with col_pinned:
        # Pinned filter
        pinned_filter = st.selectbox("Status", ["All Notes", "Pinned Only", "Unpinned Only"])

    # Filter notes
    filtered_notes = all_notes

    if search_query:
        filtered_notes = [n for n in filtered_notes if search_query.lower() in n['note_text'].lower()]

    if selected_domain != "All Domains":
        filtered_notes = [n for n in filtered_notes if n['domain'] == selected_domain]

    if pinned_filter == "Pinned Only":
        filtered_notes = [n for n in filtered_notes if n['is_pinned']]
    elif pinned_filter == "Unpinned Only":
        filtered_notes = [n for n in filtered_notes if not n['is_pinned']]

    # Export button
    if filtered_notes:
        col_export, col_count = st.columns([1, 3])

        with col_export:
            if st.button("📥 Export Notes", use_container_width=True):
                export_notes(filtered_notes, user)

        with col_count:
            st.caption(f"Showing {len(filtered_notes)} of {total_notes} notes")

    st.markdown("---")

    # Display notes
    if not filtered_notes:
        st.info("No notes match your filters")
    else:
        for note in filtered_notes:
            render_note_card_full(note, db)


def render_note_card_full(note: Dict, db):
    """Render a note card with full details including lesson info"""

    with st.container():
        # Header with lesson info
        col_lesson, col_actions = st.columns([4, 1])

        with col_lesson:
            pin_icon = "📌 " if note['is_pinned'] else ""

            # Lesson title and domain
            domain_emoji = {
                "fundamentals": "🔐", "osint": "🔎", "dfir": "🔍",
                "malware": "🦠", "active_directory": "🗂️", "system": "💻",
                "linux": "🐧", "cloud": "☁️", "pentest": "🎯",
                "red_team": "🔴", "blue_team": "🛡️", "threat_hunting": "🎯",
                "ai_security": "🤖", "iot_security": "🔌", "web3_security": "🔗"
            }

            emoji = domain_emoji.get(note['domain'], "📚")
            st.markdown(f"### {pin_icon}{emoji} {note['lesson_title']}")

            # Block info and timestamp
            block_info = f"Section {note['content_block_index'] + 1}" if note['content_block_index'] is not None else "General Note"
            st.caption(f"**{block_info}** • {note['domain'].replace('_', ' ').title()} • {note['created_at'][:16]}")

        with col_actions:
            # Go to lesson button
            if st.button("➡️", key=f"goto_{note['note_id']}", help="Go to lesson"):
                # Load lesson and navigate
                lesson = db.get_lesson(note['lesson_id'])
                if lesson:
                    st.session_state.current_lesson = lesson
                    st.session_state.current_page = "lesson"

                    # Set to the right content block if specified
                    if note['content_block_index'] is not None:
                        st.session_state.current_block_index = note['content_block_index']

                    st.rerun()

        # Note content
        if note['note_text']:
            st.markdown(note['note_text'])

        # Display attachments (images)
        if note.get('attachments'):
            try:
                import json
                from pathlib import Path
                attachments = json.loads(note['attachments']) if isinstance(note['attachments'], str) else note['attachments']
                for attachment in attachments:
                    if attachment['type'] == 'image':
                        image_path = Path(attachment['path'])
                        if image_path.exists():
                            st.image(str(image_path), caption=attachment['filename'], use_container_width=True)
                        else:
                            st.warning(f"📷 Image not found: {attachment['filename']}")
            except Exception as e:
                st.error(f"Error loading attachment: {str(e)}")

        # Edit/Delete buttons
        col_edit, col_pin, col_delete = st.columns([1, 1, 1])

        with col_edit:
            if st.button("✏️ Edit", key=f"edit_full_{note['note_id']}", use_container_width=True):
                st.session_state[f"editing_full_{note['note_id']}"] = True
                st.rerun()

        with col_pin:
            pin_label = "📌 Unpin" if note['is_pinned'] else "📌 Pin"
            if st.button(pin_label, key=f"toggle_pin_{note['note_id']}", use_container_width=True):
                toggle_pin(note['note_id'], not note['is_pinned'], db)
                st.rerun()

        with col_delete:
            if st.button("🗑️ Delete", key=f"delete_full_{note['note_id']}", use_container_width=True):
                delete_note(note['note_id'], db)
                st.rerun()

        # Edit form (if in edit mode)
        if st.session_state.get(f"editing_full_{note['note_id']}", False):
            with st.form(f"edit_full_form_{note['note_id']}"):
                edited_text = st.text_area(
                    "Edit note",
                    value=note['note_text'],
                    height=150
                )

                col_save, col_cancel = st.columns(2)

                with col_save:
                    if st.form_submit_button("💾 Save", use_container_width=True):
                        update_note(note['note_id'], edited_text, db)
                        st.session_state[f"editing_full_{note['note_id']}"] = False
                        st.rerun()

                with col_cancel:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state[f"editing_full_{note['note_id']}"] = False
                        st.rerun()

        st.markdown("---")


def export_notes(notes: List[Dict], user):
    """Export notes as Markdown"""

    # Generate Markdown content
    md_content = f"# My CyberLearn Notes\n\n"
    md_content += f"**User:** {user.username}\n"
    md_content += f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md_content += f"**Total Notes:** {len(notes)}\n\n"
    md_content += "---\n\n"

    # Group notes by lesson
    notes_by_lesson = {}
    for note in notes:
        lesson_id = note['lesson_id']
        if lesson_id not in notes_by_lesson:
            notes_by_lesson[lesson_id] = {
                'title': note['lesson_title'],
                'domain': note['domain'],
                'notes': []
            }
        notes_by_lesson[lesson_id]['notes'].append(note)

    # Write notes grouped by lesson
    for lesson_id, lesson_data in notes_by_lesson.items():
        md_content += f"## {lesson_data['title']}\n"
        md_content += f"**Domain:** {lesson_data['domain'].replace('_', ' ').title()}\n\n"

        for note in lesson_data['notes']:
            pin_marker = "📌 " if note['is_pinned'] else ""
            block_info = f"Section {note['content_block_index'] + 1}" if note['content_block_index'] is not None else "General"

            md_content += f"### {pin_marker}{block_info}\n"
            md_content += f"*Created: {note['created_at'][:16]}*\n\n"
            md_content += f"{note['note_text']}\n\n"
            md_content += "---\n\n"

    # Download button
    st.download_button(
        label="📥 Download as Markdown",
        data=md_content,
        file_name=f"cyberlearn_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
        mime="text/markdown",
        use_container_width=True,
        type="primary"
    )


def update_note(note_id: str, note_text: str, db):
    """Update note text"""
    cursor = db.conn.cursor()
    cursor.execute("""
        UPDATE lesson_notes
        SET note_text = ?, updated_at = ?
        WHERE note_id = ?
    """, (note_text, datetime.now().isoformat(), note_id))
    db.conn.commit()


def toggle_pin(note_id: str, is_pinned: bool, db):
    """Toggle pin status"""
    cursor = db.conn.cursor()
    cursor.execute("""
        UPDATE lesson_notes
        SET is_pinned = ?, updated_at = ?
        WHERE note_id = ?
    """, (1 if is_pinned else 0, datetime.now().isoformat(), note_id))
    db.conn.commit()


def delete_note(note_id: str, db):
    """Delete a note"""
    cursor = db.conn.cursor()
    cursor.execute("DELETE FROM lesson_notes WHERE note_id = ?", (note_id,))
    db.conn.commit()
