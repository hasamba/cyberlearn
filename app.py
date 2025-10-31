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

            if st.button("🔍 Search Lessons", use_container_width=True):
                st.session_state.current_page = "search"
                st.rerun()

            if st.button("👤 Profile", use_container_width=True):
                st.session_state.current_page = "profile"
                st.rerun()

            if st.button("🏆 Achievements", use_container_width=True):
                st.session_state.current_page = "achievements"
                st.rerun()

            if st.button("🏷️ Manage Tags", use_container_width=True):
                st.session_state.current_page = "tags"
                st.rerun()

            if st.button("🙈 Hidden Lessons", use_container_width=True):
                st.session_state.current_page = "hidden_lessons"
                st.rerun()

            if st.button("🎯 Skill Assessment", use_container_width=True):
                st.session_state.current_page = "diagnostic"
                st.rerun()

            if st.button("📤 Upload Lessons", use_container_width=True):
                st.session_state.current_page = "upload_lessons"
                st.rerun()

            st.markdown("---")

            if st.button("🚪 Logout", use_container_width=True):
                # Save username before clearing session
                saved_username = st.session_state.get('last_username', None)
                st.session_state.current_user = None
                st.session_state.current_page = "welcome"
                # Restore username for next login
                if saved_username:
                    st.session_state.last_username = saved_username
                # Disable auto-login after logout (require manual login)
                st.session_state.disable_auto_login = True
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
            # Login/Create Account in sidebar
            st.markdown("### 🔐 Login")

            # Get last username from database (most recently logged in user)
            # Always reload to get the latest saved username
            cursor = st.session_state.db.conn.cursor()
            cursor.execute("PRAGMA table_info(users)")
            columns = [row[1] for row in cursor.fetchall()]

            if 'last_username' in columns:
                # Get most recently logged in user's username
                cursor.execute("""
                    SELECT last_username
                    FROM users
                    WHERE last_username IS NOT NULL
                    ORDER BY last_login DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                default_username = row[0] if row else ''
            else:
                # Column doesn't exist yet, use empty default
                default_username = ''

            st.session_state.last_username = default_username

            # Auto-login with last user (if available and not disabled)
            if 'disable_auto_login' not in st.session_state:
                st.session_state.disable_auto_login = False

            if default_username and not st.session_state.disable_auto_login:
                # Auto-login
                user = st.session_state.db.get_user_by_username(default_username)
                if user:
                    st.session_state.current_user = user
                    user.last_username = default_username
                    user.update_streak()
                    st.session_state.db.update_user(user)
                    st.session_state.current_page = "dashboard"
                    st.rerun()

            # Manual login option (only if auto-login tried to happen)
            if not st.session_state.disable_auto_login:
                if st.button("🔄 Different User", use_container_width=True):
                    st.session_state.disable_auto_login = True
                    st.rerun()

            if st.session_state.disable_auto_login:
                # Quick login button for last user
                if default_username:
                    if st.button(f"⚡ Quick Login as {default_username}", use_container_width=True):
                        user = st.session_state.db.get_user_by_username(default_username)
                        if user:
                            st.session_state.current_user = user
                            user.last_username = default_username
                            user.update_streak()
                            st.session_state.db.update_user(user)
                            st.session_state.current_page = "dashboard"
                            st.session_state.disable_auto_login = False
                            st.rerun()

                # Manual login form
                with st.form("login_form_sidebar"):
                    username = st.text_input("Username", value=st.session_state.get('last_username', ''), key="login_username_input")
                    submit = st.form_submit_button("Login", use_container_width=True)

                    if submit and username:
                        user = st.session_state.db.get_user_by_username(username)
                        if user:
                            st.session_state.current_user = user
                            st.session_state.last_username = username
                            # Save username to user's database record
                            user.last_username = username
                            user.update_streak()
                            st.session_state.db.update_user(user)
                            st.session_state.current_page = "dashboard"
                            st.session_state.disable_auto_login = False  # Re-enable auto-login
                            st.success(f"Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error("User not found.")

            st.markdown("---")
            st.markdown("### ✨ Create Account")

            # Register form
            with st.form("register_form_sidebar"):
                new_username = st.text_input("Username (min 3 chars)")
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
                            # Set default tag preference to Beginner
                            user.preferred_tag_filters = ["Beginner"]
                            user.last_username = new_username
                            if st.session_state.db.create_user(user):
                                user.update_streak()
                                st.session_state.db.update_user(user)
                                st.session_state.current_user = user
                                st.session_state.last_username = new_username
                                st.session_state.current_page = "diagnostic"
                                st.success(f"Welcome, {new_username}!")
                                st.rerun()
                            else:
                                st.error("Username already exists.")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

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

    st.info("👈 **Please login or create an account in the sidebar to start learning!**")

    st.markdown("---")

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
        - **Tag-Based Organization** - Filter by career paths, courses, and tools
        - **12 Learning Domains** - From fundamentals to advanced operations
        """
        )

    with col2:
        st.markdown("#### 📊 Learning Domains")
        domains = [
            "🔐 Cybersecurity Fundamentals",
            "🔎 OSINT (Open Source Intelligence)",
            "🔍 DFIR (Digital Forensics & Incident Response)",
            "🦠 Malware Analysis",
            "🗂️ Active Directory Security",
            "💻 System Internals (Windows & Linux)",
            "🐧 Linux Security & Administration",
            "☁️ Cloud Security (AWS, Azure, GCP)",
            "🎯 Penetration Testing",
            "🔴 Red Team Operations",
            "🛡️ Blue Team Defense",
            "🎯 Threat Hunting",
            "🤖 AI Security (LLM & ML Security)",
            "🔌 IoT Security (Embedded & ICS)",
            "🔗 Web3 Security (Blockchain & DeFi)",
        ]
        for domain in domains:
            st.markdown(f"- {domain}")

    st.markdown("---")

    # Career paths section
    st.markdown("#### 🎯 Career Path Tags")
    st.markdown(
        """
    Filter lessons by your target cybersecurity role:
    - 🛡️ SOC Analyst (Tier 1 & 2)
    - 🚨 Incident Responder
    - 🎯 Threat Hunter
    - 🔬 Forensic Analyst
    - 🦠 Malware Analyst
    - 🔓 Penetration Tester
    - ⚔️ Red Team Operator
    - 🔧 Security Engineer
    - ☁️ Cloud Security Specialist
    """
    )


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
            # Use new assessment page instead of old diagnostic
            from ui.pages import assessment
            assessment.render_assessment_page()
            # diagnostic.render(
            #     st.session_state.current_user, st.session_state.db
            # )
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
        elif page == "tags":
            from ui.pages import tag_management
            tag_management.render_tag_management(st.session_state.db)
        elif page == "search":
            from ui.pages import search
            search.render_search_page()
        elif page == "hidden_lessons":
            from ui.pages import hidden_lessons
            hidden_lessons.render_hidden_lessons_page()
        elif page == "upload_lessons":
            from ui.pages import upload_lessons
            upload_lessons.render_upload_lessons_page()
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
