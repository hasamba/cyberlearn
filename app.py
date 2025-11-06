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
from utils.auth_manager import AuthManager
from utils.file_session_manager import FileSessionManager
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


def inject_browser_navigation_handler():
    """Inject JavaScript to handle browser back/forward button navigation"""
    import streamlit.components.v1 as components

    components.html(
        """
        <script>
        (function() {
            // Check if handler already registered
            if (window.parent.__streamlit_navigation_handler_installed) {
                return;
            }
            window.parent.__streamlit_navigation_handler_installed = true;

            // Store the current URL to detect changes
            let currentUrl = window.parent.location.href;

            // Listen for browser back/forward navigation (popstate event)
            window.parent.addEventListener('popstate', function(event) {
                const newUrl = window.parent.location.href;

                // Only reload if URL actually changed
                if (newUrl !== currentUrl) {
                    console.log('Browser navigation detected:', currentUrl, '->', newUrl);
                    currentUrl = newUrl;

                    // Force immediate reload to sync URL with content
                    window.parent.location.reload();
                }
            }, false);

            console.log('Browser navigation handler installed for URL:', currentUrl);
        })();
        </script>
        """,
        height=0,
    )


def sync_url_to_session_state():
    """Sync URL query parameters to session state (for browser back/forward)"""
    # Get query params from URL
    params = st.query_params

    # If page is in URL, update session state
    if "page" in params:
        st.session_state.current_page = params["page"]

    # If lesson_id is in URL AND page is "lesson", load that lesson
    # This prevents lesson from loading when on other pages
    if "lesson_id" in params and params.get("page") == "lesson":
        lesson_id = params["lesson_id"]
        if st.session_state.get("db"):
            lesson = st.session_state.db.get_lesson(lesson_id)
            if lesson:
                st.session_state.current_lesson = lesson
                st.session_state.current_page = "lesson"

    # Sync content block index from URL if present
    if "block_index" in params and params.get("page") == "lesson":
        try:
            block_index = int(params["block_index"])
            st.session_state.current_block_index = block_index
        except (ValueError, TypeError):
            pass  # Invalid block_index, ignore


def sync_session_state_to_url():
    """Sync session state to URL query parameters (for shareable links)"""
    params = {}

    # Add current page to URL
    if st.session_state.get("current_page"):
        params["page"] = st.session_state.current_page

    # Add lesson ID if viewing a lesson
    if st.session_state.current_page == "lesson" and st.session_state.get("current_lesson"):
        params["lesson_id"] = str(st.session_state.current_lesson.lesson_id)

        # Add content block index if available
        if "current_block_index" in st.session_state:
            params["block_index"] = str(st.session_state.current_block_index)

    # Clear and set URL parameters (prevents old params from persisting)
    st.query_params.clear()
    st.query_params.update(params)

    # Update last known URL to prevent re-syncing on next render
    if "last_url_params" in st.session_state:
        st.session_state.last_url_params = dict(st.query_params)


def login_user(user: UserProfile):
    """
    Log in a user and create a session cookie

    Args:
        user: UserProfile object of the user to log in
    """
    # Update user's last login and streak
    user.update_streak()
    st.session_state.db.update_user(user)

    # Create session (stored in tab session state + database)
    st.session_state.session_manager.create_session(
        user.user_id,
        st.session_state.auth_manager
    )

    # Set current user in session state
    st.session_state.current_user = user

    if config.debug:
        debug_print(f"User logged in: {user.username}")


def initialize_session_state():
    """Initialize session state variables"""
    if "db" not in st.session_state:
        st.session_state.db = Database()
        if config.debug:
            debug_print("Database connection initialized")

    # Initialize auth manager
    if "auth_manager" not in st.session_state:
        st.session_state.auth_manager = AuthManager(st.session_state.db)
        if config.debug:
            debug_print("Auth manager initialized")

    # Initialize file-based session manager (persists across refreshes)
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = FileSessionManager(st.session_state.db)
        if config.debug:
            debug_print("File session manager initialized")

    # Cleanup expired sessions periodically
    st.session_state.auth_manager.cleanup_expired_sessions()

    # Check for valid session in this browser tab
    if "current_user" not in st.session_state or st.session_state.current_user is None:
        session_token = st.session_state.session_manager.get_current_session()

        if session_token:
            # Validate session token
            user_id = st.session_state.auth_manager.validate_session(session_token)

            if user_id:
                # Valid session - load user
                user = st.session_state.db.get_user(user_id)
                if user:
                    st.session_state.current_user = user
                    if config.debug:
                        debug_print(f"Session validated for user: {user.username}")
                else:
                    # User not found - invalid session
                    st.session_state.current_user = None
                    st.session_state.session_manager.clear_session(st.session_state.auth_manager)
                    if config.debug:
                        debug_print("Session validation failed: user not found")
            else:
                # Invalid or expired session
                st.session_state.current_user = None
                st.session_state.session_manager.clear_session(st.session_state.auth_manager)
                if config.debug:
                    debug_print("Session validation failed: invalid token")
        else:
            st.session_state.current_user = None
            if config.debug:
                debug_print("No active session in this tab")

    if "current_page" not in st.session_state:
        st.session_state.current_page = "welcome"

    if "current_lesson" not in st.session_state:
        st.session_state.current_lesson = None

    # Track last known URL to detect browser navigation
    if "last_url_params" not in st.session_state:
        st.session_state.last_url_params = {}

    # Get current URL params
    current_url_params = dict(st.query_params)

    # Only sync URL to session state if URL actually changed (browser back/forward)
    # This prevents overriding user button clicks
    if current_url_params != st.session_state.last_url_params:
        # URL changed - user used browser back/forward or shared link
        sync_url_to_session_state()
        st.session_state.last_url_params = current_url_params


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
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("📚 My Learning", use_container_width=True):
                st.session_state.current_page = "learning"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("🔍 Search Lessons", use_container_width=True):
                st.session_state.current_page = "search"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("👤 Profile", use_container_width=True):
                st.session_state.current_page = "profile"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("🏆 Achievements", use_container_width=True):
                st.session_state.current_page = "achievements"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("🏷️ Manage Tags", use_container_width=True):
                st.session_state.current_page = "tags"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("🙈 Hidden Lessons", use_container_width=True):
                st.session_state.current_page = "hidden_lessons"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("🎯 Skill Assessment", use_container_width=True):
                st.session_state.current_page = "diagnostic"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("📤 Upload Lessons", use_container_width=True):
                st.session_state.current_page = "upload_lessons"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("📦 Lesson Packages", use_container_width=True):
                st.session_state.current_page = "lesson_packages"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            if st.button("📝 My Notes", use_container_width=True):
                st.session_state.current_page = "my_notes"
                st.session_state.current_lesson = None
                sync_session_state_to_url()
                st.rerun()

            st.markdown("---")

            if st.button("🚪 Logout", use_container_width=True):
                # Clear session (revokes from database and clears tab state)
                st.session_state.session_manager.clear_session(st.session_state.auth_manager)

                # Clear session state
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
            # Login/Create Account in sidebar
            st.markdown("### 🔐 Login")

            # Get last username for quick login button
            cursor = st.session_state.db.conn.cursor()
            cursor.execute("""
                SELECT username
                FROM users
                WHERE last_username IS NOT NULL AND last_username != ''
                ORDER BY last_login DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            default_username = row[0] if row else ''

            # Quick login button for last user
            if default_username:
                if st.button(f"⚡ Quick Login as {default_username}", use_container_width=True):
                    user = st.session_state.db.get_user_by_username(default_username)
                    if user:
                        login_user(user)
                        st.session_state.current_page = "dashboard"
                        st.rerun()

            # Manual login form
            with st.form("login_form_sidebar"):
                username = st.text_input("Username", value=default_username, key="login_username_input")
                submit = st.form_submit_button("Login", use_container_width=True)

                if submit and username:
                    user = st.session_state.db.get_user_by_username(username)
                    if user:
                        # Save username to user's database record
                        user.last_username = username
                        login_user(user)
                        st.session_state.current_page = "dashboard"
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
                                login_user(user)
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

    # Inject browser back/forward navigation handler
    inject_browser_navigation_handler()

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
            tag_management.render_tag_management(
                st.session_state.db,
                st.session_state.current_user
            )
        elif page == "search":
            from ui.pages import search
            search.render_search_page()
        elif page == "hidden_lessons":
            from ui.pages import hidden_lessons
            hidden_lessons.render_hidden_lessons_page()
        elif page == "upload_lessons":
            from ui.pages import upload_lessons
            upload_lessons.render_upload_lessons_page()
        elif page == "lesson_packages":
            from ui.pages import lesson_packages
            lesson_packages.render_lesson_packages_page()
        elif page == "my_notes":
            from ui.pages import my_notes
            my_notes.render_my_notes_page()
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

    # Sync session state to URL after rendering (ensures URL is always current)
    sync_session_state_to_url()


if __name__ == "__main__":
    main()
