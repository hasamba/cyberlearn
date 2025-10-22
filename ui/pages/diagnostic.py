"""
Diagnostic assessment page - Initial skill profiling for new users
"""

import streamlit as st

from models.user import UserProfile
from utils.database import Database
from core.adaptive_engine import AdaptiveEngine


def render(user: UserProfile, db: Database):
    """Render diagnostic assessment"""

    st.markdown('<h1 class="main-header">📊 Diagnostic Assessment</h1>', unsafe_allow_html=True)

    if user.diagnostic_completed:
        st.success("✅ You've already completed the diagnostic!")
        st.info("Your initial skill profile has been established. You can retake if needed.")

        if st.button("Retake Diagnostic"):
            user.diagnostic_completed = False
            db.update_user(user)
            st.rerun()

        if st.button("Go to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

        return

    st.markdown(
        """
        ### Welcome to Your Cybersecurity Journey!

        Before we begin, let's quickly assess your current knowledge. This helps us:

        - 📍 Identify your starting point in each domain
        - 🎯 Recommend the right lessons for your level
        - 🚀 Skip content you already know
        - 📈 Track your growth accurately

        **This assessment takes ~10 minutes and consists of 20 questions across all domains.**

        Don't worry if you don't know all the answers—that's exactly the point! Be honest so we can provide
        the best learning path for you.
    """
    )

    if st.button("🚀 Start Diagnostic", use_container_width=True):
        st.session_state.diagnostic_started = True
        st.rerun()

    if st.session_state.get("diagnostic_started"):
        render_diagnostic_quiz(user, db)


def render_diagnostic_quiz(user: UserProfile, db: Database):
    """Render diagnostic quiz"""

    st.markdown("---")
    st.markdown("## Diagnostic Quiz")

    adaptive = AdaptiveEngine()
    diagnostic_questions = adaptive.generate_diagnostic_assessment(20)

    # Flatten questions
    all_questions = []
    for domain, questions in diagnostic_questions.items():
        for q in questions:
            all_questions.append((domain, q))

    st.progress(0 if not all_questions else 1 / len(all_questions))

    # Simple implementation - collect all answers then score
    with st.form("diagnostic_form"):
        user_responses = {}

        for i, (domain, question) in enumerate(all_questions):
            st.markdown(f"### Question {i + 1}")
            st.markdown(question["question"])
            st.caption(f"Domain: {domain.replace('_', ' ').title()} | Difficulty: {question['difficulty']}")

            # Use actual answer options
            answer_idx = st.radio(
                "Select your answer:",
                range(len(question["options"])),
                format_func=lambda x: question["options"][x],
                key=f"diag_q_{i}",
            )

            if domain not in user_responses:
                user_responses[domain] = []

            # Check if answer is correct
            is_correct = (answer_idx == question["correct"])
            user_responses[domain].append(is_correct)

            st.markdown("---")

        submit = st.form_submit_button("Complete Assessment", use_container_width=True)

        if submit:
            # Score diagnostic
            skills = adaptive.score_diagnostic(user_responses)

            # Update user
            user.skill_levels = skills
            user.diagnostic_completed = True
            db.update_user(user)

            # Show results
            st.success("✅ Diagnostic Complete!")
            st.balloons()

            st.markdown("### 📊 Your Skill Profile")

            domains = [
                ("fundamentals", "🔐 Fundamentals"),
                ("dfir", "🔍 DFIR"),
                ("malware", "🦠 Malware"),
                ("active_directory", "🗂️ Active Directory"),
                ("pentest", "🎯 Pentest"),
                ("redteam", "🔴 Red Team"),
                ("blueteam", "🛡️ Blue Team"),
            ]

            for domain_key, domain_name in domains:
                skill = getattr(user.skill_levels, domain_key)
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**{domain_name}**")
                    st.progress(skill / 100)

                with col2:
                    st.markdown(f"{skill}/100")

            st.markdown("---")

            if st.button("🏠 Go to Dashboard", use_container_width=True):
                st.session_state.diagnostic_started = False
                st.session_state.current_page = "dashboard"
                st.rerun()
