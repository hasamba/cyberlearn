"""
Lesson Browser Component with Tag Filtering
Displays lessons with colored tag badges and filter options
"""

import streamlit as st
from typing import List, Optional
from models.lesson import LessonMetadata
from models.tag import TagFilter
from models.user import UserProfile
from utils.database import Database


def render_tag_badge(tag_name: str, tag_color: str, tag_icon: Optional[str] = None) -> str:
    """Generate HTML for a colored tag badge"""
    icon = tag_icon if tag_icon else ""
    return f"""
    <span style="
        display: inline-block;
        padding: 4px 12px;
        margin: 2px 4px;
        background-color: {tag_color}20;
        border: 1px solid {tag_color};
        border-radius: 12px;
        color: {tag_color};
        font-size: 0.85em;
        font-weight: 500;
    ">
        {icon} {tag_name}
    </span>
    """


def render_lesson_card_with_tags(lesson: LessonMetadata, tags: List, db: Database, user: UserProfile):
    """Render a lesson card with colored tag badges"""

    # Get lesson tags
    lesson_tags = db.get_lesson_tags(str(lesson.lesson_id))

    # Build tag badges HTML
    tags_html = ""
    for tag in lesson_tags:
        tags_html += render_tag_badge(tag.name, tag.color, tag.icon)

    # Get progress status
    progress = db.get_lesson_progress(user.user_id, lesson.lesson_id)
    status_emoji = "🔵"  # Not started
    status_text = "Not Started"

    if progress:
        if progress.status == "completed" or progress.status == "mastered":
            status_emoji = "✅"
            status_text = "Completed"
        elif progress.status == "in_progress":
            status_emoji = "🟡"
            status_text = "In Progress"

    # Render lesson card
    st.markdown(
        f"""
        <div class="lesson-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h3>{lesson.title}</h3>
                    <p style="color: #666; margin: 5px 0;">
                        <strong>Domain:</strong> {lesson.domain.replace('_', ' ').title()} |
                        <strong>Difficulty:</strong> {"⭐" * lesson.difficulty} |
                        <strong>Time:</strong> {lesson.estimated_time} min
                    </p>
                    <div style="margin: 10px 0;">
                        {tags_html}
                    </div>
                </div>
                <div style="text-align: right; min-width: 120px;">
                    <div style="font-size: 2em;">{status_emoji}</div>
                    <div style="font-size: 0.85em; color: #666;">{status_text}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action button
    if progress and (progress.status == "completed" or progress.status == "mastered"):
        button_text = "📖 Review Lesson"
        button_key = f"review_{lesson.lesson_id}"
    elif progress and progress.status == "in_progress":
        button_text = "▶️ Continue Lesson"
        button_key = f"continue_{lesson.lesson_id}"
    else:
        button_text = "🚀 Start Lesson"
        button_key = f"start_{lesson.lesson_id}"

    if st.button(button_text, key=button_key, use_container_width=True):
        full_lesson = db.get_lesson(lesson.lesson_id)
        if full_lesson:
            st.session_state.current_lesson = full_lesson
            st.session_state.current_page = "lesson"
            st.rerun()


def render_lesson_browser(user: UserProfile, db: Database):
    """Render lesson browser with tag filtering"""

    st.markdown("### 📚 Browse Lessons")

    # Get all tags
    all_tags = db.get_all_tags()

    if not all_tags:
        st.info("No tags available. Visit the Tag Management page to create tags.")
        return

    # Tag filter UI
    st.markdown("#### Filter by Tags")

    col1, col2 = st.columns([3, 1])

    with col1:
        # Multi-select for tags
        selected_tag_names = st.multiselect(
            "Select tags to filter lessons",
            options=[tag.name for tag in all_tags],
            default=["Built-In"],  # Default to Built-In tag
            help="Select one or more tags to filter lessons. Leave empty to show all lessons."
        )

    with col2:
        # Match all vs any
        match_all = st.checkbox(
            "Match ALL tags",
            value=False,
            help="If checked, lessons must have ALL selected tags. Otherwise, lessons with ANY tag will be shown."
        )

    # Display selected tags with badges
    if selected_tag_names:
        st.markdown("**Active Filters:**")
        filter_html = ""
        for tag_name in selected_tag_names:
            tag = db.get_tag_by_name(tag_name)
            if tag:
                filter_html += render_tag_badge(tag.name, tag.color, tag.icon)
        st.markdown(filter_html, unsafe_allow_html=True)

    st.markdown("---")

    # Get filtered lessons
    if selected_tag_names:
        # Convert tag names to IDs
        selected_tag_ids = []
        for tag_name in selected_tag_names:
            tag = db.get_tag_by_name(tag_name)
            if tag:
                selected_tag_ids.append(tag.tag_id)

        tag_filter = TagFilter(tag_ids=selected_tag_ids, match_all=match_all)
        filtered_lessons = db.get_lessons_by_tags(tag_filter)
    else:
        # Show all lessons
        filtered_lessons = db.get_all_lessons_metadata()

    # Group by domain
    lessons_by_domain = {}
    for lesson in filtered_lessons:
        domain = lesson.domain
        if domain not in lessons_by_domain:
            lessons_by_domain[domain] = []
        lessons_by_domain[domain].append(lesson)

    # Display results
    if not filtered_lessons:
        st.warning("No lessons match the selected tags.")
    else:
        st.markdown(f"**Found {len(filtered_lessons)} lesson{'s' if len(filtered_lessons) != 1 else ''}**")

        # Display by domain
        for domain, lessons in sorted(lessons_by_domain.items()):
            with st.expander(f"📂 {domain.replace('_', ' ').title()} ({len(lessons)} lessons)", expanded=True):
                # Sort by order_index
                lessons_sorted = sorted(lessons, key=lambda x: x.order_index)

                for lesson in lessons_sorted:
                    render_lesson_card_with_tags(lesson, all_tags, db, user)
                    st.markdown("<br>", unsafe_allow_html=True)


def main():
    """Standalone testing"""
    st.set_page_config(page_title="Lesson Browser", layout="wide")

    db = Database()

    # Mock user for testing
    user = db.get_user_by_username("test")

    if not user:
        st.error("No test user found. Create a user first.")
    else:
        render_lesson_browser(user, db)

    db.close()


if __name__ == "__main__":
    main()
