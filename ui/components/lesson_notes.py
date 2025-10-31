"""
Lesson Notes Component

Displays and manages user notes for lessons.
Supports:
- Text notes
- Pinning notes
- Editing/deleting notes
- Note filtering
"""

import streamlit as st
import json
from datetime import datetime
from uuid import uuid4
from typing import Optional, List, Dict

def render_notes_panel(lesson_id: str, user_id: str, db, content_block_index: Optional[int] = None):
    """
    Render notes panel for a lesson or specific content block

    Args:
        lesson_id: ID of the current lesson
        user_id: ID of the current user
        db: Database instance
        content_block_index: Optional index of current content block
    """

    st.markdown("### 📝 My Notes")

    # Get existing notes
    notes = get_notes(lesson_id, user_id, db, content_block_index)

    # Add new note section
    with st.expander("➕ Add New Note", expanded=False):
        render_add_note_form(lesson_id, user_id, db, content_block_index)

    # Display existing notes
    if notes:
        st.markdown(f"**{len(notes)} note(s)**")

        # Filter options
        col_filter1, col_filter2 = st.columns(2)

        with col_filter1:
            show_pinned_only = st.checkbox("📌 Pinned only", value=False, key=f"filter_pinned_{lesson_id}")

        with col_filter2:
            if content_block_index is None:
                show_general_only = st.checkbox("📄 General notes only", value=False, key=f"filter_general_{lesson_id}")
            else:
                show_general_only = False

        # Filter notes
        filtered_notes = notes
        if show_pinned_only:
            filtered_notes = [n for n in filtered_notes if n['is_pinned']]
        if show_general_only:
            filtered_notes = [n for n in filtered_notes if n['content_block_index'] is None]

        if not filtered_notes:
            st.info("No notes match the filter criteria")
        else:
            # Display notes
            for note in filtered_notes:
                render_note_card(note, db)
    else:
        st.info("No notes yet. Add your first note above!")


def render_add_note_form(lesson_id: str, user_id: str, db, content_block_index: Optional[int] = None):
    """Render form to add a new note"""

    with st.form(f"add_note_form_{lesson_id}_{content_block_index}", clear_on_submit=True):
        note_text = st.text_area(
            "Note content",
            placeholder="Write your note here... (Markdown supported)",
            height=150,
            help="You can use Markdown formatting"
        )

        col_pin, col_submit = st.columns([1, 2])

        with col_pin:
            is_pinned = st.checkbox("📌 Pin this note", value=False)

        with col_submit:
            submitted = st.form_submit_button("💾 Save Note", use_container_width=True, type="primary")

        if submitted and note_text.strip():
            # Create note
            note_id = str(uuid4())
            now = datetime.now().isoformat()

            cursor = db.conn.cursor()
            cursor.execute("""
                INSERT INTO lesson_notes (
                    note_id, user_id, lesson_id, content_block_index,
                    note_text, note_type, is_pinned, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note_id, user_id, lesson_id, content_block_index,
                note_text, 'text', 1 if is_pinned else 0, now, now
            ))
            db.conn.commit()

            st.success("Note saved!")
            st.rerun()
        elif submitted:
            st.warning("Please enter some text for your note")


def render_note_card(note: Dict, db):
    """Render a single note card"""

    note_id = note['note_id']

    with st.container():
        # Header with pin status and actions
        col_header, col_actions = st.columns([4, 1])

        with col_header:
            pin_icon = "📌 " if note['is_pinned'] else ""
            block_info = f" (Block {note['content_block_index'] + 1})" if note['content_block_index'] is not None else " (General)"
            st.caption(f"{pin_icon}**{note['created_at'][:16]}**{block_info}")

        with col_actions:
            # Action buttons in columns
            col_edit, col_delete = st.columns(2)

            with col_edit:
                if st.button("✏️", key=f"edit_{note_id}", help="Edit note"):
                    st.session_state[f'editing_{note_id}'] = True
                    st.rerun()

            with col_delete:
                if st.button("🗑️", key=f"delete_{note_id}", help="Delete note"):
                    delete_note(note_id, db)
                    st.rerun()

        # Note content (editable or display)
        if st.session_state.get(f'editing_{note_id}', False):
            # Edit mode
            with st.form(f"edit_note_form_{note_id}"):
                edited_text = st.text_area(
                    "Edit note",
                    value=note['note_text'],
                    height=100,
                    label_visibility="collapsed"
                )

                col_pin_edit, col_save, col_cancel = st.columns(3)

                with col_pin_edit:
                    is_pinned = st.checkbox("📌 Pin", value=bool(note['is_pinned']), key=f"pin_edit_{note_id}")

                with col_save:
                    if st.form_submit_button("💾 Save", use_container_width=True):
                        update_note(note_id, edited_text, is_pinned, db)
                        st.session_state[f'editing_{note_id}'] = False
                        st.rerun()

                with col_cancel:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state[f'editing_{note_id}'] = False
                        st.rerun()
        else:
            # Display mode
            st.markdown(note['note_text'])

        st.markdown("---")


def get_notes(lesson_id: str, user_id: str, db, content_block_index: Optional[int] = None) -> List[Dict]:
    """Get all notes for a lesson or content block"""

    cursor = db.conn.cursor()

    if content_block_index is not None:
        # Get notes for specific block + general notes
        cursor.execute("""
            SELECT note_id, user_id, lesson_id, content_block_index, note_text,
                   note_type, is_pinned, created_at, updated_at
            FROM lesson_notes
            WHERE user_id = ? AND lesson_id = ?
              AND (content_block_index = ? OR content_block_index IS NULL)
            ORDER BY is_pinned DESC, created_at DESC
        """, (user_id, lesson_id, content_block_index))
    else:
        # Get all notes for lesson
        cursor.execute("""
            SELECT note_id, user_id, lesson_id, content_block_index, note_text,
                   note_type, is_pinned, created_at, updated_at
            FROM lesson_notes
            WHERE user_id = ? AND lesson_id = ?
            ORDER BY is_pinned DESC, created_at DESC
        """, (user_id, lesson_id))

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    notes = []
    for row in rows:
        note_dict = dict(zip(columns, row))
        notes.append(note_dict)

    return notes


def update_note(note_id: str, note_text: str, is_pinned: bool, db):
    """Update an existing note"""

    cursor = db.conn.cursor()
    cursor.execute("""
        UPDATE lesson_notes
        SET note_text = ?, is_pinned = ?, updated_at = ?
        WHERE note_id = ?
    """, (note_text, 1 if is_pinned else 0, datetime.now().isoformat(), note_id))
    db.conn.commit()


def delete_note(note_id: str, db):
    """Delete a note"""

    cursor = db.conn.cursor()
    cursor.execute("DELETE FROM lesson_notes WHERE note_id = ?", (note_id,))
    db.conn.commit()
