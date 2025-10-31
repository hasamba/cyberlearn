"""
Hidden Lessons Management Page

View and manage lessons that have been hidden from the main UI
"""

import streamlit as st
import json
from datetime import datetime

def render_hidden_lessons_page():
    """Render the hidden lessons management page"""

    st.title("🙈 Hidden Lessons")

    db = st.session_state.db
    cursor = db.conn.cursor()

    # Get all hidden lessons
    cursor.execute('''
        SELECT lesson_id, title, domain, difficulty, order_index
        FROM lessons
        WHERE hidden = 1
        ORDER BY domain, order_index
    ''')

    hidden_lessons = cursor.fetchall()

    if not hidden_lessons:
        st.info("📭 No hidden lessons")
        st.markdown("""
        **What are hidden lessons?**

        Hidden lessons are removed from:
        - Domain lesson lists
        - Adaptive recommendations
        - Search results (by default)
        - Progress calculations

        You can hide lessons you want to skip or focus on specific content.
        """)
        return

    # Show count
    st.success(f"**{len(hidden_lessons)} lesson(s) hidden**")

    st.markdown("---")

    # Bulk actions
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### Hidden Lessons")

    with col2:
        if st.button("🔓 Unhide All", use_container_width=True):
            cursor.execute("UPDATE lessons SET hidden = 0")
            db.conn.commit()
            st.success("All lessons unhidden!")
            st.rerun()

    # Display hidden lessons
    for lesson_id, title, domain, difficulty, order_index in hidden_lessons:
        with st.container():
            col_info, col_action = st.columns([4, 1])

            with col_info:
                # Domain and difficulty
                domain_emoji = {
                    "fundamentals": "🔐", "osint": "🔎", "dfir": "🔍",
                    "malware": "🦠", "active_directory": "🗂️", "system": "💻",
                    "linux": "🐧", "cloud": "☁️", "pentest": "🎯",
                    "red_team": "🔴", "blue_team": "🛡️", "threat_hunting": "🎯",
                    "ai_security": "🤖", "iot_security": "🔌", "web3_security": "🔗"
                }

                difficulty_names = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
                difficulty_colors = {1: "🟢", 2: "🟡", 3: "🔴"}

                st.markdown(f"**{title}**")
                st.caption(
                    f"{domain_emoji.get(domain, '📚')} {domain.replace('_', ' ').title()} • "
                    f"{difficulty_colors[difficulty]} {difficulty_names[difficulty]} • "
                    f"Order: {order_index}"
                )

            with col_action:
                if st.button("🔓 Unhide", key=f"unhide_{lesson_id}"):
                    cursor.execute("UPDATE lessons SET hidden = 0 WHERE lesson_id = ?", (lesson_id,))
                    db.conn.commit()
                    st.success(f"Unhidden!")
                    st.rerun()

            st.markdown("---")
