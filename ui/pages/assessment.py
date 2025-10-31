"""
Enhanced User Skill Assessment Page

Comprehensive assessment covering all 15 domains:
- 93 diagnostic questions
- Multiple choice format
- Difficulty levels: beginner, intermediate, advanced
- Results visualization with radar chart
- Personalized learning path recommendations
"""

import streamlit as st
import json
from datetime import datetime
from typing import List, Dict
from uuid import uuid4

def render_assessment_page():
    """Render the skill assessment page"""

    st.title("🎯 Skill Assessment")

    db = st.session_state.db
    user = st.session_state.current_user

    # Check if assessment already in progress
    if 'assessment_in_progress' not in st.session_state:
        st.session_state.assessment_in_progress = False
        st.session_state.current_domain_index = 0
        st.session_state.domain_responses = {}

    # Get all assessment questions grouped by domain
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT domain, COUNT(*) as question_count
        FROM assessment_questions
        GROUP BY domain
        ORDER BY domain
    """)

    domains_data = cursor.fetchall()

    if not domains_data:
        st.error("No assessment questions found in database. Please run populate_assessment_questions.py")
        return

    # Domain list
    domains = [row['domain'] for row in domains_data]

    # Welcome screen
    if not st.session_state.assessment_in_progress:
        render_assessment_welcome(domains)
        return

    # Assessment in progress
    if st.session_state.current_domain_index < len(domains):
        current_domain = domains[st.session_state.current_domain_index]
        render_domain_assessment(current_domain, domains)
    else:
        # Assessment complete - show results
        render_assessment_results(domains)


def render_assessment_welcome(domains: List[str]):
    """Render welcome screen before assessment"""

    st.markdown("""
    ### Welcome to the CyberLearn Skill Assessment

    This comprehensive assessment will evaluate your knowledge across **15 cybersecurity domains**:

    """)

    # Domain list in columns
    col1, col2, col3 = st.columns(3)

    domain_emojis = {
        "fundamentals": "🔐", "osint": "🔎", "dfir": "🔍",
        "malware": "🦠", "active_directory": "🗂️", "system": "💻",
        "linux": "🐧", "cloud": "☁️", "pentest": "🎯",
        "red_team": "🔴", "blue_team": "🛡️", "threat_hunting": "🎯",
        "ai_security": "🤖", "iot_security": "🔌", "web3_security": "🔗"
    }

    for i, domain in enumerate(domains):
        col = [col1, col2, col3][i % 3]
        with col:
            emoji = domain_emojis.get(domain, "📚")
            st.markdown(f"- {emoji} {domain.replace('_', ' ').title()}")

    st.markdown("---")

    st.info("""
    **What to Expect:**
    - 📝 **93 questions** covering all domains
    - ⏱️ **15-20 minutes** to complete
    - 🎯 **Multiple choice** format
    - 📊 **Instant results** with personalized recommendations
    - 🔄 **Retake anytime** to track your progress

    **Tips:**
    - Answer honestly - this helps us recommend the right lessons
    - Take your time - accuracy is more important than speed
    - It's okay to not know everything!
    """)

    st.markdown("---")

    col_start, col_skip = st.columns(2)

    with col_start:
        if st.button("🚀 Start Assessment", use_container_width=True, type="primary"):
            st.session_state.assessment_in_progress = True
            st.session_state.current_domain_index = 0
            st.session_state.domain_responses = {}
            st.rerun()

    with col_skip:
        if st.button("⏭️ Skip for Now", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()


def render_domain_assessment(domain: str, all_domains: List[str]):
    """Render questions for a specific domain"""

    db = st.session_state.db
    user = st.session_state.current_user

    # Progress bar
    progress = st.session_state.current_domain_index / len(all_domains)
    st.progress(progress)
    st.caption(f"Domain {st.session_state.current_domain_index + 1} of {len(all_domains)}")

    domain_emojis = {
        "fundamentals": "🔐", "osint": "🔎", "dfir": "🔍",
        "malware": "🦠", "active_directory": "🗂️", "system": "💻",
        "linux": "🐧", "cloud": "☁️", "pentest": "🎯",
        "red_team": "🔴", "blue_team": "🛡️", "threat_hunting": "🎯",
        "ai_security": "🤖", "iot_security": "🔌", "web3_security": "🔗"
    }

    emoji = domain_emojis.get(domain, "📚")
    st.markdown(f"## {emoji} {domain.replace('_', ' ').title()}")

    st.markdown("---")

    # Get questions for this domain
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT question_id, question_text, options, correct_answer, difficulty, explanation
        FROM assessment_questions
        WHERE domain = ?
        ORDER BY difficulty
    """, (domain,))

    questions = cursor.fetchall()

    if not questions:
        st.warning(f"No questions found for {domain}")
        if st.button("Next Domain"):
            st.session_state.current_domain_index += 1
            st.rerun()
        return

    # Create form for all questions in this domain
    with st.form(f"domain_assessment_{domain}"):
        user_answers = {}

        for i, question in enumerate(questions):
            question_id = question['question_id']
            question_text = question['question_text']
            options = json.loads(question['options']) if isinstance(question['options'], str) else question['options']
            difficulty = question['difficulty']

            # Difficulty badge
            difficulty_names = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
            difficulty_colors = {1: "🟢", 2: "🟡", 3: "🔴"}

            st.markdown(f"### Question {i + 1} {difficulty_colors[difficulty]} {difficulty_names[difficulty]}")
            st.markdown(question_text)

            # Radio buttons for options
            selected = st.radio(
                "Select your answer:",
                options,
                key=f"q_{question_id}",
                label_visibility="collapsed"
            )

            user_answers[question_id] = {
                'selected': selected,
                'selected_index': options.index(selected),
                'correct_answer': question['correct_answer'],
                'difficulty': difficulty
            }

            st.markdown("---")

        # Submit button
        submit = st.form_submit_button("Submit Answers", use_container_width=True, type="primary")

        if submit:
            # Store responses for this domain
            st.session_state.domain_responses[domain] = user_answers

            # Move to next domain
            st.session_state.current_domain_index += 1
            st.rerun()

    # Cancel button (outside form)
    if st.button("❌ Cancel Assessment"):
        st.session_state.assessment_in_progress = False
        st.session_state.current_domain_index = 0
        st.session_state.domain_responses = {}
        st.session_state.current_page = "dashboard"
        st.rerun()


def render_assessment_results(all_domains: List[str]):
    """Render assessment results with scoring and recommendations"""

    db = st.session_state.db
    user = st.session_state.current_user

    st.markdown("# 🎉 Assessment Complete!")

    st.markdown("---")

    # Calculate scores for each domain
    domain_scores = {}
    total_questions = 0
    total_correct = 0

    for domain, responses in st.session_state.domain_responses.items():
        correct = 0
        total = len(responses)

        difficulty_correct = {1: 0, 2: 0, 3: 0}
        difficulty_total = {1: 0, 2: 0, 3: 0}

        for question_id, answer_data in responses.items():
            total_questions += 1
            difficulty = answer_data['difficulty']
            difficulty_total[difficulty] += 1

            if answer_data['selected_index'] == answer_data['correct_answer']:
                correct += 1
                total_correct += 1
                difficulty_correct[difficulty] += 1

        # Calculate skill level (0-100 scale)
        if total > 0:
            # Base score from percentage correct
            base_score = (correct / total) * 100

            # Weight by difficulty
            weighted_score = 0
            if difficulty_total[1] > 0:
                weighted_score += (difficulty_correct[1] / difficulty_total[1]) * 20  # Beginner worth 20%
            if difficulty_total[2] > 0:
                weighted_score += (difficulty_correct[2] / difficulty_total[2]) * 40  # Intermediate worth 40%
            if difficulty_total[3] > 0:
                weighted_score += (difficulty_correct[3] / difficulty_total[3]) * 40  # Advanced worth 40%

            # Average of base and weighted
            final_score = int((base_score + weighted_score) / 2)

            domain_scores[domain] = {
                'score': final_score,
                'correct': correct,
                'total': total,
                'difficulty_breakdown': {
                    'beginner': f"{difficulty_correct[1]}/{difficulty_total[1]}" if difficulty_total[1] > 0 else "N/A",
                    'intermediate': f"{difficulty_correct[2]}/{difficulty_total[2]}" if difficulty_total[2] > 0 else "N/A",
                    'advanced': f"{difficulty_correct[3]}/{difficulty_total[3]}" if difficulty_total[3] > 0 else "N/A"
                }
            }
        else:
            domain_scores[domain] = {'score': 0, 'correct': 0, 'total': 0}

    # Overall score
    overall_percentage = int((total_correct / total_questions) * 100) if total_questions > 0 else 0

    st.markdown(f"### Overall Score: {overall_percentage}%")
    st.markdown(f"**{total_correct} correct out of {total_questions} questions**")

    st.markdown("---")

    # Domain scores table
    st.markdown("### Domain Breakdown")

    for domain in all_domains:
        if domain not in domain_scores:
            continue

        score_data = domain_scores[domain]
        score = score_data['score']
        correct = score_data['correct']
        total = score_data['total']

        domain_emojis = {
            "fundamentals": "🔐", "osint": "🔎", "dfir": "🔍",
            "malware": "🦠", "active_directory": "🗂️", "system": "💻",
            "linux": "🐧", "cloud": "☁️", "pentest": "🎯",
            "red_team": "🔴", "blue_team": "🛡️", "threat_hunting": "🎯",
            "ai_security": "🤖", "iot_security": "🔌", "web3_security": "🔗"
        }

        emoji = domain_emojis.get(domain, "📚")

        with st.expander(f"{emoji} {domain.replace('_', ' ').title()} - {score}/100"):
            st.markdown(f"**Score:** {correct}/{total} correct ({score}/100)")
            st.progress(score / 100)

            # Difficulty breakdown
            breakdown = score_data.get('difficulty_breakdown', {})
            if breakdown:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"🟢 Beginner: {breakdown.get('beginner', 'N/A')}")
                with col2:
                    st.caption(f"🟡 Intermediate: {breakdown.get('intermediate', 'N/A')}")
                with col3:
                    st.caption(f"🔴 Advanced: {breakdown.get('advanced', 'N/A')}")

            # Skill level assessment
            if score >= 80:
                st.success("✨ **Advanced** - You have strong knowledge in this domain")
            elif score >= 60:
                st.info("💪 **Intermediate** - You have solid foundational knowledge")
            elif score >= 40:
                st.warning("📚 **Beginner** - Great starting point, plenty to learn!")
            else:
                st.error("🌱 **Novice** - This is a new area for you, start with fundamentals")

    st.markdown("---")

    # Save assessment to database
    st.markdown("### 💾 Save Your Results")

    if st.button("Save Assessment Results", type="primary", use_container_width=True):
        # Update user skill levels
        for domain, score_data in domain_scores.items():
            score = score_data['score']
            setattr(user.skill_levels, domain, score)

        # Save user assessment record
        cursor = db.conn.cursor()
        assessment_id = str(uuid4())

        cursor.execute("""
            INSERT INTO user_assessments (
                assessment_id, user_id, assessment_date, domain_scores, total_score, total_questions
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            str(user.user_id),
            datetime.now().isoformat(),
            json.dumps(domain_scores),
            overall_percentage,
            total_questions
        ))

        db.conn.commit()
        db.update_user(user)

        # Mark diagnostic complete
        user.diagnostic_completed = True
        db.update_user(user)

        st.success("✅ Results saved! Your skill levels have been updated.")

        # Reset assessment state
        st.session_state.assessment_in_progress = False
        st.session_state.current_domain_index = 0
        st.session_state.domain_responses = {}

        # Navigate to dashboard
        st.session_state.current_page = "dashboard"
        st.rerun()

    # Retake button
    if st.button("🔄 Retake Assessment", use_container_width=True):
        st.session_state.assessment_in_progress = False
        st.session_state.current_domain_index = 0
        st.session_state.domain_responses = {}
        st.rerun()
