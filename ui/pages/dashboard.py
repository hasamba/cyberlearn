"""
Dashboard page - Main user interface showing progress, recommendations, and quick stats
"""

import streamlit as st
from typing import List
import plotly.graph_objects as go
import plotly.express as px

from models.user import UserProfile
from models.progress import LessonStatus
from utils.database import Database
from core.adaptive_engine import AdaptiveEngine
from core.gamification import GamificationEngine


def render(user: UserProfile, db: Database):
    """Render main dashboard"""

    # Update streak on login
    streak_info = user.update_streak()
    db.update_user(user)

    # Header
    st.markdown('<h1 class="main-header">🏠 Dashboard</h1>', unsafe_allow_html=True)

    # Streak message
    if streak_info["streak_maintained"]:
        st.success(f"🔥 {streak_info['current_streak']} day streak maintained! Keep it up!")
    else:
        st.info("Welcome back! Start a lesson today to begin your streak.")

    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <h3>Level {user.level}</h3>
                <p>{user.get_level_name()}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <h3>{user.total_xp:,} XP</h3>
                <p>{user.get_xp_to_next_level()} to Level {user.level + 1}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <h3>{user.total_lessons_completed}</h3>
                <p>Lessons Completed</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="stat-card">
                <h3>{len(user.badges)}</h3>
                <p>Badges Earned</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Main content columns
    col_left, col_right = st.columns([2, 1])

    with col_left:
        render_recommended_lessons(user, db)
        render_skill_progress(user)

    with col_right:
        render_next_milestone(user)
        render_recent_badges(user)


def render_recommended_lessons(user: UserProfile, db: Database):
    """Show personalized lesson recommendations"""

    st.markdown("### 📚 Recommended for You")

    adaptive = AdaptiveEngine()
    user_progress = db.get_user_progress(user.user_id)
    all_lessons = db.get_all_lessons_metadata()

    # Get recommendation
    recommended_id = adaptive.get_recommended_lesson(
        user, all_lessons, user_progress
    )

    if recommended_id:
        lesson = db.get_lesson(recommended_id)

        if lesson:
            st.markdown(
                f"""
                <div class="lesson-card">
                    <h3>🎯 {lesson.title}</h3>
                    <p><strong>Domain:</strong> {lesson.domain.replace('_', ' ').title()}</p>
                    <p><strong>Difficulty:</strong> {lesson.get_difficulty_name()}</p>
                    <p><strong>Est. Time:</strong> {lesson.estimated_time} minutes</p>
                    <p><strong>XP Reward:</strong> {lesson.base_xp_reward} XP (+ bonuses)</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

            if st.button("🚀 Start Lesson", key="start_recommended", use_container_width=True):
                st.session_state.current_lesson = lesson
                st.session_state.current_page = "lesson"
                st.rerun()
        else:
            st.info("Loading lesson content...")
    else:
        # Check if diagnostic is completed
        if not user.diagnostic_completed:
            st.info("Complete the diagnostic assessment to get personalized recommendations!")
            if st.button("📊 Take Diagnostic", use_container_width=True):
                st.session_state.current_page = "diagnostic"
                st.rerun()
        else:
            # Diagnostic completed but no lessons found
            st.success("🎉 Great progress! You've completed all available lessons in your current skill range.")
            st.info("💡 **What's next?**\n- Review previous lessons to strengthen mastery\n- Check out the Learning page to explore other domains\n- Keep your streak alive by reviewing material!")

            if st.button("📚 Explore All Lessons", use_container_width=True):
                st.session_state.current_page = "learning"
                st.rerun()


def render_skill_progress(user: UserProfile):
    """Visualize skill levels across domains"""

    st.markdown("### 📊 Your Skill Levels")

    domains = [
        "Fundamentals",
        "DFIR",
        "Malware",
        "Active Directory",
        "System",
        "Linux",
        "Cloud",
        "Pentest",
        "Red Team",
        "Blue Team",
    ]

    skills = [
        user.skill_levels.fundamentals,
        user.skill_levels.dfir,
        user.skill_levels.malware,
        user.skill_levels.active_directory,
        user.skill_levels.system,
        user.skill_levels.linux,
        user.skill_levels.cloud,
        user.skill_levels.pentest,
        user.skill_levels.redteam,
        user.skill_levels.blueteam,
    ]

    # Radar chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=skills,
            theta=domains,
            fill="toself",
            name="Your Skills",
            line_color="#667eea",
            fillcolor="rgba(102, 126, 234, 0.3)",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Domain breakdown
    with st.expander("📈 Domain Details"):
        for domain, skill in zip(domains, skills):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{domain}**")
                st.progress(skill / 100)
            with col2:
                st.markdown(f"{skill}/100")


def render_next_milestone(user: UserProfile):
    """Show next achievement milestone"""

    st.markdown("### 🎯 Next Milestone")

    gamification = GamificationEngine()
    milestone = gamification.get_next_milestone(user)

    if milestone:
        st.markdown(f"**{milestone['description']}**")

        progress_pct = min(
            (milestone["progress"] / milestone["target"]) * 100, 100
        )

        st.progress(progress_pct / 100)
        st.caption(
            f"{milestone['progress']} / {milestone['target']} ({progress_pct:.0f}%)"
        )

        # Encouragement
        if progress_pct >= 75:
            st.success("Almost there! Keep pushing!")
        elif progress_pct >= 50:
            st.info("Great progress! You're halfway there!")
    else:
        st.success("🎉 All milestones achieved!")


def render_recent_badges(user: UserProfile):
    """Display recently earned badges"""

    st.markdown("### 🏆 Recent Badges")

    if user.badges:
        # Show last 3 badges
        recent = user.badges[-3:]
        for badge_id in recent:
            st.markdown(f"🏅 **{badge_id.replace('_', ' ').title()}**")

        if len(user.badges) > 3:
            st.caption(f"+ {len(user.badges) - 3} more badges")

        if st.button("View All Badges", use_container_width=True):
            st.session_state.current_page = "achievements"
            st.rerun()
    else:
        st.info("Complete lessons to earn badges!")


def render_learning_stats(user: UserProfile):
    """Show detailed learning statistics"""

    st.markdown("### 📈 Learning Statistics")

    # Time spent
    hours = user.total_time_spent // 3600
    minutes = (user.total_time_spent % 3600) // 60

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Study Time", f"{hours}h {minutes}m")
        st.metric("Lessons Completed", user.total_lessons_completed)

    with col2:
        st.metric("Current Streak", f"{user.streak_days} days")
        st.metric("Longest Streak", f"{user.longest_streak} days")
