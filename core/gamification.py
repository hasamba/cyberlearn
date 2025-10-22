"""
Gamification system for CyberLearn.
Implements XP, badges, streaks, levels, and achievement tracking.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from uuid import UUID

from models.user import UserProfile
from models.progress import LessonProgress, LessonStatus


class Badge:
    """Badge definition"""

    def __init__(
        self,
        badge_id: str,
        name: str,
        description: str,
        icon: str,
        category: str,
        xp_bonus: int = 0,
    ):
        self.badge_id = badge_id
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category
        self.xp_bonus = xp_bonus


class GamificationEngine:
    """
    Manages all gamification aspects: XP, badges, streaks, levels.
    Implements Jim Kwik's 'Gamify It' principle.
    """

    def __init__(self):
        self.badges = self._initialize_badges()

    def _initialize_badges(self) -> Dict[str, Badge]:
        """Define all available badges"""
        badges = {}

        # Domain completion badges
        domains = [
            "fundamentals",
            "dfir",
            "malware",
            "active_directory",
            "pentest",
            "redteam",
            "blueteam",
        ]
        for domain in domains:
            badges[f"{domain}_complete"] = Badge(
                badge_id=f"{domain}_complete",
                name=f"{domain.replace('_', ' ').title()} Master",
                description=f"Complete all lessons in {domain}",
                icon="🎓",
                category="domain",
                xp_bonus=500,
            )

            badges[f"{domain}_mastery"] = Badge(
                badge_id=f"{domain}_mastery",
                name=f"{domain.replace('_', ' ').title()} Expert",
                description=f"Achieve 90%+ mastery in {domain}",
                icon="⭐",
                category="mastery",
                xp_bonus=1000,
            )

        # Streak badges
        streak_milestones = [7, 30, 100, 365]
        streak_names = ["Week Warrior", "Monthly Master", "Century Scholar", "Year Legend"]
        for days, name in zip(streak_milestones, streak_names):
            badges[f"streak_{days}"] = Badge(
                badge_id=f"streak_{days}",
                name=name,
                description=f"Maintain {days}-day learning streak",
                icon="🔥",
                category="streak",
                xp_bonus=days * 10,
            )

        # Performance badges
        badges["perfectionist"] = Badge(
            badge_id="perfectionist",
            name="Perfectionist",
            description="Score 100% on 10 lessons",
            icon="💯",
            category="performance",
            xp_bonus=300,
        )

        badges["speed_demon"] = Badge(
            badge_id="speed_demon",
            name="Speed Demon",
            description="Complete 10 lessons under target time",
            icon="⚡",
            category="performance",
            xp_bonus=250,
        )

        badges["persistent"] = Badge(
            badge_id="persistent",
            name="Persistent Learner",
            description="Complete 50 lessons total",
            icon="🏆",
            category="milestone",
            xp_bonus=500,
        )

        badges["dedicated"] = Badge(
            badge_id="dedicated",
            name="Dedicated Scholar",
            description="Complete 100 lessons total",
            icon="👑",
            category="milestone",
            xp_bonus=1000,
        )

        # Jim Kwik principle badges
        kwik_principles = [
            ("active_learner", "Active Learner", "Complete 20 interactive simulations"),
            ("memory_master", "Memory Master", "Use memory aids 50 times"),
            (
                "meta_thinker",
                "Meta Thinker",
                "Submit 30 reflective responses",
            ),
            ("growth_mindset", "Growth Mindset", "Overcome 5 challenging lessons"),
        ]

        for badge_id, name, desc in kwik_principles:
            badges[badge_id] = Badge(
                badge_id=badge_id,
                name=name,
                description=desc,
                icon="🧠",
                category="jim_kwik",
                xp_bonus=400,
            )

        return badges

    def calculate_xp(
        self,
        base_xp: int,
        score: int,
        time_spent: int,
        estimated_time: int,
        streak: int,
        difficulty: int,
        first_attempt: bool = False,
    ) -> Dict:
        """
        Calculate XP earned with all bonuses applied.

        Returns dict with breakdown of XP calculation.
        """

        multipliers = []
        bonus_xp = 0

        # Score multiplier
        if score >= 100:
            multipliers.append(("Perfect Score", 1.5))
        elif score >= 90:
            multipliers.append(("Excellent Score", 1.2))
        elif score >= 80:
            multipliers.append(("Good Score", 1.1))

        # Speed bonus (completed faster than estimated)
        if time_spent < estimated_time * 60:
            time_saved_pct = ((estimated_time * 60 - time_spent) / (estimated_time * 60)) * 100
            if time_saved_pct >= 25:
                multipliers.append(("Speed Bonus", 1.3))
            else:
                multipliers.append(("Speed Bonus", 1.1))

        # Streak bonus
        if streak >= 7:
            streak_mult = min(1 + (streak * 0.05), 2.0)
            multipliers.append((f"{streak}-Day Streak", streak_mult))

        # First attempt bonus
        if first_attempt and score >= 80:
            multipliers.append(("First Try Success", 1.2))

        # Difficulty multiplier
        difficulty_mult = 1 + (difficulty - 1) * 0.1
        multipliers.append((f"Difficulty {difficulty}", difficulty_mult))

        # Calculate total
        total_mult = 1.0
        for _, mult in multipliers:
            total_mult *= mult

        total_xp = int(base_xp * total_mult) + bonus_xp

        return {
            "base_xp": base_xp,
            "multipliers": multipliers,
            "total_multiplier": round(total_mult, 2),
            "bonus_xp": bonus_xp,
            "total_xp": total_xp,
        }

    def check_badge_unlocks(
        self,
        user: UserProfile,
        user_progress: List[LessonProgress],
        recent_lesson: Optional[LessonProgress] = None,
    ) -> List[Badge]:
        """
        Check for newly earned badges.

        Returns list of badges earned (not already owned).
        """

        newly_earned = []

        # Streak badges
        for days in [7, 30, 100, 365]:
            badge_id = f"streak_{days}"
            if (
                user.streak_days >= days
                and badge_id not in user.badges
            ):
                newly_earned.append(self.badges[badge_id])

        # Domain completion
        domains = [
            "fundamentals",
            "dfir",
            "malware",
            "active_directory",
            "pentest",
            "redteam",
            "blueteam",
        ]

        for domain in domains:
            domain_progress = [p for p in user_progress if self._get_lesson_domain(p) == domain]
            completed = [
                p for p in domain_progress
                if p.status in [LessonStatus.COMPLETED, LessonStatus.MASTERED]
            ]
            mastered = [p for p in domain_progress if p.status == LessonStatus.MASTERED]

            # Domain completion badge (assuming we know total lessons per domain)
            # This would need actual lesson count from database in real implementation
            badge_id = f"{domain}_complete"
            if len(completed) >= 10 and badge_id not in user.badges:  # Placeholder threshold
                newly_earned.append(self.badges[badge_id])

            # Domain mastery badge
            badge_id = f"{domain}_mastery"
            skill = getattr(user.skill_levels, domain)
            if skill >= 90 and badge_id not in user.badges:
                newly_earned.append(self.badges[badge_id])

        # Milestone badges
        if user.total_lessons_completed >= 50 and "persistent" not in user.badges:
            newly_earned.append(self.badges["persistent"])

        if user.total_lessons_completed >= 100 and "dedicated" not in user.badges:
            newly_earned.append(self.badges["dedicated"])

        # Performance badges
        perfect_scores = sum(
            1 for p in user_progress if p.best_score == 100
        )
        if perfect_scores >= 10 and "perfectionist" not in user.badges:
            newly_earned.append(self.badges["perfectionist"])

        # Jim Kwik principle badges (would need more detailed tracking)
        reflections = sum(1 for p in user_progress if p.reflection_submitted)
        if reflections >= 30 and "meta_thinker" not in user.badges:
            newly_earned.append(self.badges["meta_thinker"])

        return newly_earned

    def _get_lesson_domain(self, progress: LessonProgress) -> str:
        """Helper to get domain from lesson (would query lesson in real implementation)"""
        # Placeholder - would actually look up lesson metadata
        return "fundamentals"

    def get_user_rank(self, user_xp: int, all_users_xp: List[int]) -> Dict:
        """Calculate user's rank among all users"""

        if not all_users_xp:
            return {"rank": 1, "total_users": 1, "percentile": 100}

        all_users_xp.sort(reverse=True)
        rank = all_users_xp.index(user_xp) + 1 if user_xp in all_users_xp else len(all_users_xp)

        percentile = ((len(all_users_xp) - rank + 1) / len(all_users_xp)) * 100

        return {
            "rank": rank,
            "total_users": len(all_users_xp),
            "percentile": round(percentile, 1),
        }

    def get_next_milestone(self, user: UserProfile) -> Dict:
        """Get next achievement milestone to aim for"""

        milestones = []

        # Next level
        xp_to_next = user.get_xp_to_next_level()
        if xp_to_next > 0:
            milestones.append(
                {
                    "type": "level",
                    "description": f"Reach Level {user.level + 1}",
                    "progress": user.total_xp,
                    "target": user.total_xp + xp_to_next,
                    "percentage": 0,  # Calculate from current level base
                }
            )

        # Next streak milestone
        streak_milestones = [7, 30, 100, 365]
        next_streak = next((s for s in streak_milestones if s > user.streak_days), None)
        if next_streak:
            milestones.append(
                {
                    "type": "streak",
                    "description": f"Reach {next_streak}-day streak",
                    "progress": user.streak_days,
                    "target": next_streak,
                    "percentage": (user.streak_days / next_streak) * 100,
                }
            )

        # Next lesson milestone
        lesson_milestones = [10, 25, 50, 100, 200]
        next_lesson = next(
            (m for m in lesson_milestones if m > user.total_lessons_completed), None
        )
        if next_lesson:
            milestones.append(
                {
                    "type": "lessons",
                    "description": f"Complete {next_lesson} lessons",
                    "progress": user.total_lessons_completed,
                    "target": next_lesson,
                    "percentage": (user.total_lessons_completed / next_lesson) * 100,
                }
            )

        # Return closest milestone
        milestones.sort(key=lambda x: x["percentage"], reverse=True)
        return milestones[0] if milestones else None

    def generate_encouragement(self, context: str, user: UserProfile) -> str:
        """
        Generate motivational message based on context.
        Implements 'Reframe Limiting Beliefs' Jim Kwik principle.
        """

        messages = {
            "streak_maintained": [
                f"🔥 {user.streak_days} days strong! Your consistency is building mastery.",
                f"Amazing dedication! {user.streak_days} consecutive days of growth.",
                "Every day you show up, you're rewiring your brain for success!",
            ],
            "streak_broken": [
                "Streaks are just numbers - what matters is getting back to learning!",
                "Every expert was once a beginner who never gave up. Start again today!",
                "Progress isn't lost - your knowledge remains. Let's rebuild that momentum!",
            ],
            "perfect_score": [
                "💯 Perfect! Your hard work is clearly paying off.",
                "Exceptional work! You've mastered this concept completely.",
                "This is what focused learning looks like. Outstanding!",
            ],
            "low_score": [
                "Remember: struggle is where learning happens. Try again with confidence!",
                "Mistakes are proof you're challenging yourself. That's how growth works!",
                "Each attempt makes you stronger. You're building expertise one lesson at a time.",
            ],
            "level_up": [
                f"🎉 Level {user.level}! You're not the same learner you were when you started.",
                f"Welcome to Level {user.level}! Your growth is quantifiable and impressive.",
                "Each level represents real skills gained. You're becoming a cybersecurity professional!",
            ],
        }

        import random
        return random.choice(messages.get(context, ["Keep up the excellent work!"]))

    def get_leaderboard_position(
        self, user_id: UUID, all_users: List[UserProfile]
    ) -> Dict:
        """Get user's position on various leaderboards"""

        # Sort by XP
        xp_sorted = sorted(all_users, key=lambda u: u.total_xp, reverse=True)
        xp_rank = next(
            (i + 1 for i, u in enumerate(xp_sorted) if u.user_id == user_id), None
        )

        # Sort by streak
        streak_sorted = sorted(all_users, key=lambda u: u.streak_days, reverse=True)
        streak_rank = next(
            (i + 1 for i, u in enumerate(streak_sorted) if u.user_id == user_id), None
        )

        # Sort by lessons completed
        lessons_sorted = sorted(
            all_users, key=lambda u: u.total_lessons_completed, reverse=True
        )
        lessons_rank = next(
            (i + 1 for i, u in enumerate(lessons_sorted) if u.user_id == user_id), None
        )

        return {
            "xp_rank": xp_rank,
            "streak_rank": streak_rank,
            "lessons_rank": lessons_rank,
            "total_users": len(all_users),
        }
