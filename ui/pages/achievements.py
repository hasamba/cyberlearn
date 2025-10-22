"""
Achievements and badges page
"""

import streamlit as st

from models.user import UserProfile
from utils.database import Database
from core.gamification import GamificationEngine


def render(user: UserProfile, db: Database):
    """Render achievements page"""

    st.markdown('<h1 class="main-header">🏆 Achievements</h1>', unsafe_allow_html=True)

    gamification = GamificationEngine()

    # Summary stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total XP", f"{user.total_xp:,}")

    with col2:
        st.metric("Level", f"{user.level} - {user.get_level_name()}")

    with col3:
        st.metric("Badges Earned", len(user.badges))

    with col4:
        st.metric("Current Streak", f"{user.streak_days} days 🔥")

    st.markdown("---")

    # Badge categories
    st.markdown("## 🏅 Your Badges")

    all_badges = gamification.badges

    # Group by category
    categories = {}
    for badge_id, badge in all_badges.items():
        if badge.category not in categories:
            categories[badge.category] = []
        categories[badge.category].append((badge_id, badge))

    for category_name, badges in categories.items():
        with st.expander(f"📁 {category_name.replace('_', ' ').title()}", expanded=True):
            cols = st.columns(3)

            for i, (badge_id, badge) in enumerate(badges):
                with cols[i % 3]:
                    earned = badge_id in user.badges

                    if earned:
                        st.markdown(
                            f"""
                            <div style="border: 2px solid gold; border-radius: 10px; padding: 1rem;
                                        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
                                        text-align: center; margin-bottom: 1rem;">
                                <div style="font-size: 3rem;">{badge.icon}</div>
                                <div style="font-weight: bold; color: #000;">{badge.name}</div>
                                <div style="font-size: 0.9rem; color: #333;">{badge.description}</div>
                                <div style="margin-top: 0.5rem; color: #000;">✅ Earned</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="border: 2px dashed #ccc; border-radius: 10px; padding: 1rem;
                                        background: #f5f5f5; text-align: center; margin-bottom: 1rem;
                                        opacity: 0.6;">
                                <div style="font-size: 3rem; filter: grayscale(100%);">{badge.icon}</div>
                                <div style="font-weight: bold;">{badge.name}</div>
                                <div style="font-size: 0.9rem;">{badge.description}</div>
                                <div style="margin-top: 0.5rem;">🔒 Locked</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

    st.markdown("---")

    # Progress to next milestone
    st.markdown("## 🎯 Next Milestone")

    milestone = gamification.get_next_milestone(user)

    if milestone:
        st.markdown(f"### {milestone['description']}")

        progress_pct = min((milestone["progress"] / milestone["target"]) * 100, 100)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.progress(progress_pct / 100)

        with col2:
            st.markdown(f"**{progress_pct:.0f}%**")

        st.caption(f"{milestone['progress']} / {milestone['target']}")

        if progress_pct >= 75:
            st.success("🎉 Almost there! Keep pushing!")
        elif progress_pct >= 50:
            st.info("Great progress! You're halfway!")
    else:
        st.success("🎊 Congratulations! You've achieved all current milestones!")

    st.markdown("---")

    # Level progression
    st.markdown("## 📈 Level Progression")

    levels = [
        (1, "Apprentice", 1000),
        (2, "Practitioner", 3000),
        (3, "Specialist", 7000),
        (4, "Expert", 15000),
        (5, "Master", 30000),
        (6, "Grandmaster", 100000),
    ]

    for level, name, xp_required in levels:
        if level <= user.level:
            st.success(f"✅ Level {level}: {name} - {xp_required:,} XP")
        elif level == user.level + 1:
            xp_to_next = xp_required - user.total_xp
            st.info(
                f"⏳ Level {level}: {name} - {xp_to_next:,} XP remaining"
            )
        else:
            st.text(f"🔒 Level {level}: {name} - {xp_required:,} XP")
