"""
CyberLearn - Adaptive Cybersecurity Learning Platform
Main Streamlit application entry point

Usage:
  streamlit run app.py           # Normal mode
  streamlit run app.py -- -v     # Verbose/Debug mode
  streamlit run app.py -- --debug # Debug mode
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config, debug_print
from ui.pages import dashboard, lesson_viewer, diagnostic, profile
from utils.database import Database
from models.user import UserProfile

# Show debug info if enabled
if config.debug:
    debug_print("Application starting in DEBUG mode")
    debug_print(f"Python version: {sys.version}")
    debug_print(f"Streamlit version: {st.__version__}")
    debug_print(f"Working directory: {Path.cwd()}")

# Page configuration
st.set_page_config(
    page_title="CyberLearn - Adaptive Cyber Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .badge-icon {
        font-size: 2rem;
        margin: 0.5rem;
    }
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    .lesson-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .lesson-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    </style>
""",
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables"""
    if "db" not in st.session_state:
        st.session_state.db = Database()
        if config.debug:
            debug_print("Database connection initialized")

    if "current_user" not in st.session_state:
        st.session_state.current_user = None
        if config.debug:
            debug_print("Session state initialized (no user)")

    if "current_page" not in st.session_state:
        st.session_state.current_page = "welcome"

    if "current_lesson" not in st.session_state:
        st.session_state.current_lesson = None


def render_sidebar():
    """Render navigation sidebar"""
    with st.sidebar:
        st.markdown("# 🛡️ CyberLearn")

        if st.session_state.current_user:
            user = st.session_state.current_user

            # User info
            st.markdown(f"### Welcome, {user.username}!")
            st.markdown(f"**Level {user.level}** - {user.get_level_name()}")

            # XP Progress
            st.markdown("#### Progress to Next Level")
            xp_to_next = user.get_xp_to_next_level()
            if xp_to_next > 0:
                current_level_base = [0, 1000, 3000, 7000, 15000, 30000][
                    user.level - 1
                ]
                level_xp_range = xp_to_next + (user.total_xp - current_level_base)
                progress_pct = ((user.total_xp - current_level_base) / level_xp_range) * 100
                st.progress(progress_pct / 100)
                st.caption(f"{user.total_xp} XP / {xp_to_next + user.total_xp} XP needed")
            else:
                st.success("Max Level Achieved!")

            # Streak
            st.markdown(f"🔥 **{user.streak_days} Day Streak**")

            st.markdown("---")

            # Navigation
            st.markdown("### Navigation")

            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()

            if st.button("📚 My Learning", use_container_width=True):
                st.session_state.current_page = "learning"
                st.rerun()

            if st.button("👤 Profile", use_container_width=True):
                st.session_state.current_page = "profile"
                st.rerun()

            if st.button("🏆 Achievements", use_container_width=True):
                st.session_state.current_page = "achievements"
                st.rerun()

            st.markdown("---")

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.current_user = None
                st.session_state.current_page = "welcome"
                st.rerun()

            # Debug info section
            if config.debug:
                st.markdown("---")
                st.markdown("### 🐛 Debug Info")
                st.caption(f"User ID: {user.user_id}")
                st.caption(f"Page: {st.session_state.current_page}")
                st.caption(f"DB: {config.db_path.exists()}")
                if st.session_state.current_lesson:
                    st.caption(f"Lesson: {st.session_state.current_lesson.title}")

        else:
            st.info("Please login or create an account to start learning!")

            # Debug info for no user
            if config.debug:
                st.markdown("---")
                st.markdown("### 🐛 Debug Info")
                st.caption("No user logged in")
                st.caption(f"DB exists: {config.db_path.exists()}")


def render_welcome_page():
    """Render welcome/login page"""
    st.markdown('<h1 class="main-header">🛡️ CyberLearn</h1>', unsafe_allow_html=True)
    st.markdown(
        "### Accelerated Cybersecurity Mastery with Adaptive Learning"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🚀 Features")
        st.markdown(
            """
        - **Adaptive Learning Engine** - Content adjusts to your skill level
        - **Gamified Experience** - Earn XP, badges, and level up
        - **Jim Kwik Principles** - Accelerated learning techniques
        - **Hands-on Labs** - Interactive simulations and exercises
        - **Spaced Repetition** - Optimize retention with smart reviews
        - **7 Core Domains** - From fundamentals to advanced operations
        """
        )

    with col2:
        st.markdown("#### 📊 Learning Domains")
        domains = [
            "🔐 Cybersecurity Fundamentals",
            "🔍 DFIR (Digital Forensics & Incident Response)",
            "🦠 Malware Analysis",
            "🗂️ Active Directory Security",
            "💻 System Internals (Windows & Linux)",
            "🐧 Linux Security & Administration",
            "☁️ Cloud Security (AWS, Azure, GCP)",
            "🎯 Penetration Testing",
            "🔴 Red Team Operations",
            "🛡️ Blue Team Defense",
        ]
        for domain in domains:
            st.markdown(f"- {domain}")

    st.markdown("---")

    # Login/Register
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit and username:
                user = st.session_state.db.get_user_by_username(username)
                if user:
                    st.session_state.current_user = user
                    user.update_streak()
                    st.session_state.db.update_user(user)
                    st.session_state.current_page = "dashboard"
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("User not found. Please create an account.")

    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username (min 3 characters)")
            email = st.text_input("Email (optional)")
            submit = st.form_submit_button("Create Account", use_container_width=True)

            if submit:
                if not new_username:
                    st.error("Please enter a username.")
                elif len(new_username) < 3:
                    st.error("Username must be at least 3 characters long.")
                else:
                    try:
                        # Create new user
                        user = UserProfile(username=new_username, email=email or None)
                        if st.session_state.db.create_user(user):
                            user.update_streak()
                            st.session_state.db.update_user(user)
                            st.session_state.current_user = user
                            st.session_state.current_page = "diagnostic"
                            st.success(f"Account created! Welcome, {new_username}!")
                            st.rerun()
                        else:
                            st.error("Username already exists. Please choose another.")
                    except Exception as e:
                        st.error(f"Error creating account: {str(e)}")


def main():
    """Main application logic"""
    initialize_session_state()
    render_sidebar()

    # Route to appropriate page
    if not st.session_state.current_user:
        render_welcome_page()
    else:
        page = st.session_state.current_page

        if page == "dashboard":
            dashboard.render(
                st.session_state.current_user, st.session_state.db
            )
        elif page == "diagnostic":
            diagnostic.render(
                st.session_state.current_user, st.session_state.db
            )
        elif page == "learning":
            lesson_viewer.render(
                st.session_state.current_user, st.session_state.db
            )
        elif page == "profile":
            profile.render(
                st.session_state.current_user, st.session_state.db
            )
        elif page == "achievements":
            from ui.pages import achievements
            achievements.render(
                st.session_state.current_user, st.session_state.db
            )
        elif page == "lesson":
            if st.session_state.current_lesson:
                lesson_viewer.render_lesson(
                    st.session_state.current_user,
                    st.session_state.current_lesson,
                    st.session_state.db,
                )
        else:
            dashboard.render(
                st.session_state.current_user, st.session_state.db
            )


if __name__ == "__main__":
    main()
