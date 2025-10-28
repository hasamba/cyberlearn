"""
Lesson viewer page - Interactive lesson delivery with all Jim Kwik principles
"""

import streamlit as st
import json
import time
from datetime import datetime
from uuid import UUID

from models.user import UserProfile
from models.lesson import Lesson, ContentType
from models.progress import LessonProgress, LessonStatus
from utils.database import Database
from core.gamification import GamificationEngine


def render(user: UserProfile, db: Database):
    """Render lesson selection/browser"""

    st.markdown('<h1 class="main-header">📚 My Learning</h1>', unsafe_allow_html=True)

    # Domain tabs
    domains = [
        ("fundamentals", "🔐 Fundamentals"),
        ("dfir", "🔍 DFIR"),
        ("malware", "🦠 Malware"),
        ("active_directory", "🗂️ Active Directory"),
        ("system", "💻 System"),
        ("linux", "🐧 Linux"),
        ("cloud", "☁️ Cloud"),
        ("pentest", "🎯 Pentest"),
        ("redteam", "🔴 Red Team"),
        ("blueteam", "🛡️ Blue Team"),
    ]

    tabs = st.tabs([name for _, name in domains])

    for idx, (domain_key, domain_name) in enumerate(domains):
        with tabs[idx]:
            render_domain_lessons(user, db, domain_key)


def render_domain_lessons(user: UserProfile, db: Database, domain: str):
    """Show lessons for specific domain"""

    lessons = db.get_lessons_by_domain(domain)
    user_progress = db.get_user_progress(user.user_id)

    progress_map = {p.lesson_id: p for p in user_progress}

    if not lessons:
        st.info(f"Lessons for {domain} are coming soon!")
        return

    skill = getattr(user.skill_levels, domain)
    st.markdown(f"**Your Skill Level:** {skill}/100")
    st.progress(skill / 100)

    st.markdown("---")

    for lesson_meta in lessons:
        lesson = db.get_lesson(lesson_meta.lesson_id)
        if not lesson:
            continue

        progress = progress_map.get(lesson_meta.lesson_id)

        # Lesson card
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                # Status indicator
                if progress:
                    if progress.status == LessonStatus.MASTERED:
                        status_emoji = "⭐"
                        status_text = "MASTERED"
                        status_color = "green"
                    elif progress.status == LessonStatus.COMPLETED:
                        status_emoji = "✅"
                        status_text = "COMPLETED"
                        status_color = "blue"
                    elif progress.status == LessonStatus.IN_PROGRESS:
                        status_emoji = "🔄"
                        status_text = "IN PROGRESS"
                        status_color = "orange"
                    else:
                        status_emoji = "📘"
                        status_text = "NOT STARTED"
                        status_color = "gray"
                else:
                    status_emoji = "📘"
                    status_text = "NOT STARTED"
                    status_color = "gray"

                st.markdown(f"### {status_emoji} {lesson.title}")
                st.markdown(f"*{lesson.subtitle}*" if lesson.subtitle else "")

                # Show status badge
                if progress and progress.status in [LessonStatus.COMPLETED, LessonStatus.MASTERED]:
                    st.markdown(f'<span style="background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">{status_emoji} {status_text}</span>', unsafe_allow_html=True)

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.caption(f"⏱️ {lesson.estimated_time} min")
                with col_b:
                    st.caption(f"🎯 {lesson.get_difficulty_name()}")
                with col_c:
                    st.caption(f"⚡ {lesson.base_xp_reward} XP")

                if lesson.is_core_concept:
                    st.caption("🔥 Core Concept (Essential)")

            with col2:
                if st.button(
                    "Start" if not progress else "Continue",
                    key=f"lesson_{lesson.lesson_id}",
                    use_container_width=True,
                ):
                    st.session_state.current_lesson = lesson
                    st.session_state.current_page = "lesson"
                    st.rerun()

        st.markdown("---")


def render_lesson(user: UserProfile, lesson: Lesson, db: Database):
    """Render interactive lesson content"""

    # Scroll to top on navigation
    if st.session_state.get("scroll_to_top", False):
        st.session_state.scroll_to_top = False
        # Use Streamlit's anchor to scroll to top
        st.markdown('<div id="top"></div>', unsafe_allow_html=True)
        st.markdown('<script>document.getElementById("top").scrollIntoView();</script>', unsafe_allow_html=True)

    # Initialize lesson state
    if "lesson_start_time" not in st.session_state:
        st.session_state.lesson_start_time = time.time()

    if "current_block_index" not in st.session_state:
        st.session_state.current_block_index = 0

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    # Header
    st.markdown(f"# {lesson.title}")
    st.markdown(f"*{lesson.subtitle}*" if lesson.subtitle else "")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📚 Domain: {lesson.domain.replace('_', ' ').title()}")
    with col2:
        st.caption(f"🎯 Difficulty: {lesson.get_difficulty_name()}")
    with col3:
        st.caption(f"⏱️ Est. Time: {lesson.estimated_time} min")

    # Progress bar for lesson
    total_blocks = len(lesson.content_blocks)
    current_idx = st.session_state.current_block_index

    # Calculate progress (clamp between 0 and 1)
    if total_blocks > 0:
        progress_value = min(current_idx / total_blocks, 1.0)
    else:
        progress_value = 0.0

    st.progress(progress_value)
    st.caption(f"Section {min(current_idx + 1, total_blocks)} of {total_blocks}")

    st.markdown("---")

    # Render current content block
    if current_idx < total_blocks:
        block = lesson.content_blocks[current_idx]
        render_content_block(block, lesson, user, db)

        # Navigation buttons
        col_prev, col_next = st.columns(2)

        with col_prev:
            if current_idx > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_block_index -= 1
                    st.session_state.scroll_to_top = True
                    st.rerun()

        with col_next:
            if current_idx < total_blocks - 1:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.current_block_index += 1
                    st.session_state.scroll_to_top = True
                    st.rerun()
            else:
                # Last block - show quiz
                if st.button("📝 Take Quiz ➡️", use_container_width=True):
                    st.session_state.current_block_index += 1
                    st.session_state.scroll_to_top = True
                    st.rerun()
    else:
        # Quiz time
        render_quiz(lesson, user, db)

    # Back button
    if st.button("🔙 Back to Lessons"):
        cleanup_lesson_state()
        st.session_state.current_page = "learning"
        st.rerun()


def render_content_block(block, lesson: Lesson, user: UserProfile, db: Database):
    """Render individual content block based on type"""

    content_type = ContentType(block.type)

    # Title
    if block.title:
        st.markdown(f"## {block.title}")

    # Main content
    if content_type == ContentType.MINDSET_COACH:
        render_mindset_block(block)

    elif content_type == ContentType.EXPLANATION:
        render_explanation_block(block)

    elif content_type == ContentType.DIAGRAM:
        render_diagram_block(block)

    elif content_type == ContentType.MEMORY_AID:
        render_memory_aid_block(block)

    elif content_type == ContentType.SIMULATION:
        render_simulation_block(block)

    elif content_type == ContentType.REFLECTION:
        render_reflection_block(block, user, lesson, db)

    elif content_type == ContentType.VIDEO:
        render_video_block(block)

    elif content_type == ContentType.CODE_EXERCISE:
        render_code_exercise_block(block)

    elif content_type == ContentType.REAL_WORLD:
        render_real_world_block(block)

    elif content_type == ContentType.QUIZ:
        # Inline quiz (different from final assessment)
        st.info("Interactive checkpoint quiz")

    # Memory aids (if present)
    if block.memory_aids:
        with st.expander("💡 Memory Aids"):
            for aid in block.memory_aids:
                st.markdown(f"- {aid}")

    # Real world connection
    if block.real_world_connection:
        with st.expander("🌍 Real-World Connection"):
            st.markdown(block.real_world_connection)

    # Reflection prompt
    if block.reflection_prompt:
        with st.expander("🤔 Reflection Prompt"):
            st.markdown(block.reflection_prompt)


def render_mindset_block(block):
    """Render mindset coaching message"""
    # Check for different possible keys in content
    text_content = block.content.get("text") or block.content.get("message", "")
    if text_content:
        st.info(text_content)
    if block.mindset_message:
        st.success(f"💪 {block.mindset_message}")


def render_explanation_block(block):
    """Render explanation content"""
    st.markdown(block.content.get("text", ""))

    if block.simplified_explanation:
        with st.expander("🎈 Simplified Explanation (ELI10)"):
            st.markdown(block.simplified_explanation)


def render_diagram_block(block):
    """Render diagram/visual"""
    st.markdown(block.content.get("description", ""))

    if "ascii_art" in block.content:
        st.code(block.content["ascii_art"], language="text")

    if "key_points" in block.content:
        st.markdown("**Key Points:**")
        for point in block.content["key_points"]:
            st.markdown(f"- {point}")


def render_memory_aid_block(block):
    """Render memory technique"""
    st.markdown("### 🧠 Memory Technique")

    # Check for text content first
    text_content = block.content.get("text", "")
    if text_content:
        st.markdown(text_content)

    if "technique" in block.content:
        st.markdown(f"**Technique:** {block.content['technique']}")

    if "visualization" in block.content:
        st.markdown(block.content["visualization"])

    if "memory_hack" in block.content:
        st.info(block.content["memory_hack"])


def render_simulation_block(block):
    """Render interactive simulation"""
    st.markdown("### 🎮 Interactive Exercise")

    scenarios = block.content.get("scenarios", [])

    for i, scenario in enumerate(scenarios):
        st.markdown(f"**Scenario {i + 1}:**")
        st.markdown(scenario["description"])

        answer_key = f"scenario_{i}"

        options = ["Confidentiality", "Integrity", "Availability"]
        user_answer = st.radio(
            "Which CIA pillar is violated?",
            options,
            key=answer_key,
            horizontal=True,
        )

        if st.button(f"Check Answer", key=f"check_{i}"):
            correct = scenario["violated_pillar"]
            if user_answer.lower() == correct:
                st.success("✅ Correct!")
                st.markdown(f"**Explanation:** {scenario['explanation']}")
            else:
                st.error("❌ Not quite. Try again!")

        st.markdown("---")


def render_reflection_block(block, user: UserProfile, lesson: Lesson, db: Database):
    """Render reflection prompt with text input"""
    st.markdown("### 💭 Reflection Time")

    st.markdown(block.content.get("prompt", ""))

    reflection_text = st.text_area(
        "Your thoughts:",
        key=f"reflection_{block.block_id}",
        height=150,
    )

    if st.button("Submit Reflection", key=f"submit_refl_{block.block_id}"):
        if reflection_text:
            # Save reflection (would update progress in real implementation)
            st.success("Reflection saved! You earned bonus XP for meta-learning.")
            # Award XP for reflection
            xp_info = user.add_xp(block.xp_reward, multiplier=1.0)
            db.update_user(user)
            st.balloons()
        else:
            st.warning("Please enter your reflection to continue.")


def render_video_block(block):
    """Render video content block"""
    st.markdown("### 🎥 Video Tutorial")

    # Check for different possible keys in content
    text_content = block.content.get("text") or block.content.get("resources") or block.content.get("description", "")

    if text_content:
        st.markdown(text_content)

    # Check for video URL
    if "url" in block.content:
        st.video(block.content["url"])
    elif "video_url" in block.content:
        st.video(block.content["video_url"])


def render_code_exercise_block(block):
    """Render code exercise block"""
    st.markdown("### 💻 Code Exercise")

    text_content = block.content.get("text", "")
    if text_content:
        st.markdown(text_content)

    # Display code examples if present
    if "code" in block.content:
        st.code(block.content["code"], language=block.content.get("language", "python"))

    if "examples" in block.content:
        for example in block.content["examples"]:
            if isinstance(example, dict):
                st.code(example.get("code", ""), language=example.get("language", "python"))
            else:
                st.code(example, language="python")


def render_real_world_block(block):
    """Render real-world application block"""
    st.markdown("### 🌍 Real-World Application")

    text_content = block.content.get("text") or block.content.get("description", "")
    if text_content:
        st.markdown(text_content)

    # Display case studies if present
    if "cases" in block.content:
        for case in block.content["cases"]:
            if isinstance(case, dict):
                st.markdown(f"**{case.get('title', 'Case Study')}**")
                st.markdown(case.get("description", ""))
            else:
                st.markdown(case)


def render_quiz(lesson: Lesson, user: UserProfile, db: Database):
    """Render final assessment quiz"""

    st.markdown("## 📝 Final Assessment")

    st.info(
        f"Answer all questions to complete the lesson. "
        f"You need {lesson.mastery_threshold}% to pass."
    )

    questions = lesson.post_assessment
    user_answers = {}

    with st.form("quiz_form"):
        for i, question in enumerate(questions):
            st.markdown(f"### Question {i + 1}")
            st.markdown(question.question)

            if question.type == "multiple_choice":
                user_answers[i] = st.radio(
                    "Select your answer:",
                    question.options,
                    key=f"q_{i}",
                )

        submit = st.form_submit_button("Submit Quiz", use_container_width=True)

        if submit:
            # Score quiz
            score = calculate_quiz_score(questions, user_answers)
            time_spent = int(time.time() - st.session_state.lesson_start_time)

            # Complete lesson
            complete_lesson(user, lesson, score, time_spent, db)

            st.rerun()


def calculate_quiz_score(questions, user_answers) -> int:
    """Calculate quiz score as percentage"""
    if not questions:
        return 100

    correct = 0
    for i, question in enumerate(questions):
        if i in user_answers:
            if question.type == "multiple_choice":
                selected = user_answers[i]
                if selected == question.options[question.correct_answer]:
                    correct += 1

    return int((correct / len(questions)) * 100)


def complete_lesson(
    user: UserProfile, lesson: Lesson, score: int, time_spent: int, db: Database
):
    """Mark lesson as completed and award XP"""

    # Get or create progress
    progress = db.get_lesson_progress(user.user_id, lesson.lesson_id)

    # Check if this is the first completion
    is_first_completion = False
    if not progress:
        progress = LessonProgress(
            user_id=user.user_id,
            lesson_id=lesson.lesson_id,
        )
        progress.start_lesson()
        is_first_completion = True
    elif progress.status == LessonStatus.NOT_STARTED or progress.status == LessonStatus.IN_PROGRESS:
        # First time completing (was in progress or not started)
        is_first_completion = True

    # Complete
    completion_info = progress.complete_lesson(score, time_spent)

    # Initialize gamification engine
    gamification = GamificationEngine()
    xp_info = None
    level_info = None
    new_badges = []

    # Only award XP and update skills on FIRST completion
    if is_first_completion:
        # Calculate XP with bonuses
        xp_info = gamification.calculate_xp(
            base_xp=lesson.base_xp_reward,
            score=score,
            time_spent=time_spent,
            estimated_time=lesson.estimated_time,
            streak=user.streak_days,
            difficulty=lesson.difficulty,
            first_attempt=(progress.attempts == 1),
        )

        # Award XP
        level_info = user.add_xp(xp_info["total_xp"])

        # Update skill level
        domain = lesson.domain
        current_skill = getattr(user.skill_levels, domain)
        adaptive = __import__("core.adaptive_engine", fromlist=["AdaptiveEngine"]).AdaptiveEngine()
        new_skill = adaptive.calculate_skill_update(current_skill, lesson.difficulty, score)
        setattr(user.skill_levels, domain, new_skill)

        # Update stats (only on first completion)
        user.total_lessons_completed += 1
        user.total_time_spent += time_spent

        # Check for badges (only on first completion)
        user_progress_list = db.get_user_progress(user.user_id)
        new_badges = gamification.check_badge_unlocks(user, user_progress_list, progress)

        for badge in new_badges:
            user.add_badge(badge.badge_id)
    else:
        # Retake - only update time spent
        user.total_time_spent += time_spent

    # Save to database
    if progress.progress_id:
        db.update_progress(progress)
    else:
        db.create_progress(progress)

    db.update_user(user)

    # Show completion message
    if is_first_completion:
        st.success(f"🎉 Lesson Completed! Score: {score}%")
        st.balloons()

        st.markdown(f"### 🏆 Rewards")
        st.markdown(f"**XP Earned:** {xp_info['total_xp']} XP")
        st.markdown(f"**Base XP:** {xp_info['base_xp']}")

        for multiplier_name, mult_value in xp_info["multipliers"]:
            st.markdown(f"- {multiplier_name}: {mult_value}x")

        if level_info["level_up"]:
            st.success(
                f"🎊 LEVEL UP! You're now Level {level_info['new_level']} - {level_info['level_name']}!"
            )

        if new_badges:
            st.markdown("### 🏅 New Badges Unlocked!")
            for badge in new_badges:
                st.markdown(f"**{badge.name}** - {badge.description}")

        # Encouragement
        encouragement = gamification.generate_encouragement(
            "perfect_score" if score == 100 else "level_up" if level_info["level_up"] else "streak_maintained",
            user,
        )
        st.info(encouragement)
    else:
        # Retake completion
        st.success(f"✅ Lesson Retake Completed! Score: {score}%")
        st.info("💡 **Note:** XP and skill level rewards are only awarded on first completion. Great job reviewing the material!")

        # Show progress improvement if score improved
        if progress.attempts > 1:
            st.markdown(f"**Attempts:** {progress.attempts}")
            st.markdown(f"**Best Score:** {progress.best_score}%")
            if score > progress.best_score:
                st.success(f"🎯 New personal best! Previous best: {progress.best_score}%")

    # Cleanup
    cleanup_lesson_state()


def cleanup_lesson_state():
    """Clean up lesson session state"""
    keys_to_remove = [
        "lesson_start_time",
        "current_block_index",
        "quiz_answers",
        "current_lesson",
    ]

    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
