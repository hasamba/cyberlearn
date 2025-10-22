"""
User profile and settings page
"""

import streamlit as st

from models.user import UserProfile
from utils.database import Database


def render(user: UserProfile, db: Database):
    """Render user profile page"""

    st.markdown('<h1 class="main-header">👤 Profile</h1>', unsafe_allow_html=True)

    # User info section
    st.markdown("### 📝 User Information")

    col1, col2 = st.columns(2)

    with col1:
        new_username = st.text_input("Username", value=user.username)
        new_email = st.text_input("Email", value=user.email or "")

    with col2:
        st.markdown(f"**Account Created:** {user.created_at.strftime('%Y-%m-%d')}")
        st.markdown(f"**Total XP:** {user.total_xp:,}")
        st.markdown(f"**Current Level:** {user.level} ({user.get_level_name()})")

    if st.button("💾 Update Profile"):
        user.email = new_email if new_email else None
        # Note: username change would need unique check
        db.update_user(user)
        st.success("Profile updated!")

    st.markdown("---")

    # Learning preferences
    st.markdown("### ⚙️ Learning Preferences")

    col1, col2 = st.columns(2)

    with col1:
        pace = st.selectbox(
            "Learning Pace",
            ["slow", "normal", "fast"],
            index=["slow", "normal", "fast"].index(user.learning_preferences.pace),
        )

        session_duration = st.slider(
            "Daily Session Duration (minutes)",
            15,
            60,
            user.learning_preferences.session_duration,
        )

    with col2:
        st.markdown("**Content Preferences**")

        visual_weight = st.slider(
            "Visual Learning Weight",
            0.0,
            1.0,
            user.learning_preferences.visual_weight,
            0.05,
        )

        kinesthetic_weight = st.slider(
            "Hands-on Learning Weight",
            0.0,
            1.0,
            user.learning_preferences.kinesthetic_weight,
            0.05,
        )

    if st.button("💾 Save Preferences"):
        user.learning_preferences.pace = pace
        user.learning_preferences.session_duration = session_duration
        user.learning_preferences.visual_weight = visual_weight
        user.learning_preferences.kinesthetic_weight = kinesthetic_weight

        # Normalize weights
        total = (
            visual_weight
            + kinesthetic_weight
            + user.learning_preferences.auditory_weight
        )
        if total > 0:
            user.learning_preferences.visual_weight = visual_weight / total
            user.learning_preferences.kinesthetic_weight = kinesthetic_weight / total
            user.learning_preferences.auditory_weight = (
                1.0 - visual_weight / total - kinesthetic_weight / total
            )

        db.update_user(user)
        st.success("Preferences saved!")

    st.markdown("---")

    # Statistics
    st.markdown("### 📊 Your Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Lessons Completed", user.total_lessons_completed)
        st.metric("Badges Earned", len(user.badges))

    with col2:
        hours = user.total_time_spent // 3600
        minutes = (user.total_time_spent % 3600) // 60
        st.metric("Study Time", f"{hours}h {minutes}m")
        st.metric("Current Streak", f"{user.streak_days} days")

    with col3:
        st.metric("Longest Streak", f"{user.longest_streak} days")
        avg_skill = user.skill_levels.get_overall_level()
        st.metric("Overall Skill", f"{avg_skill}/100")
