"""
Adaptive Learning Engine for CyberLearn.
Implements intelligent lesson recommendation and difficulty adaptation.
"""

from typing import List, Dict, Optional, Tuple
from uuid import UUID
import random
from datetime import datetime

from models.user import UserProfile, SkillLevels
from models.lesson import Lesson, LessonMetadata
from models.progress import LessonProgress, LessonStatus


class AdaptiveEngine:
    """
    Core adaptive learning algorithm that personalizes content delivery
    based on user performance, preferences, and learning science principles.
    """

    def __init__(self):
        self.domain_prerequisites = {
            "fundamentals": [],
            "dfir": ["fundamentals"],
            "malware": ["fundamentals"],
            "active_directory": ["fundamentals"],
            "pentest": ["fundamentals", "active_directory"],
            "redteam": ["pentest", "malware"],
            "blueteam": ["dfir", "malware"],
        }

    def get_recommended_lesson(
        self,
        user: UserProfile,
        available_lessons: List[LessonMetadata],
        user_progress: List[LessonProgress],
        domain: Optional[str] = None,
    ) -> Optional[UUID]:
        """
        Recommend next lesson based on adaptive algorithm.

        Algorithm considers:
        1. Domain skill level -> difficulty matching
        2. Prerequisites completion
        3. Spaced repetition needs
        4. Learning preferences
        5. Minimum effective dose (core concepts first)
        """

        # Check for lessons needing review (spaced repetition)
        review_lesson = self._check_review_needed(user_progress)
        if review_lesson:
            return review_lesson

        # Filter by domain if specified, else choose optimal domain
        if not domain:
            domain = self._select_optimal_domain(user)

        # Get appropriate difficulty for user's skill level
        skill_level = getattr(user.skill_levels, domain)
        target_difficulties = self._get_target_difficulties(skill_level)

        # Filter available lessons
        candidates = self._filter_lessons(
            available_lessons, domain, target_difficulties, user_progress
        )

        if not candidates:
            return None

        # Prioritize core concepts (Minimum Effective Dose principle)
        core_lessons = [l for l in candidates if l.is_core_concept]
        if core_lessons:
            candidates = core_lessons

        # Select best lesson using multi-factor scoring
        selected = self._score_and_select_lesson(candidates, user, user_progress)

        return selected.lesson_id if selected else None

    def _check_review_needed(
        self, user_progress: List[LessonProgress]
    ) -> Optional[UUID]:
        """Check if any lessons are due for spaced repetition review"""
        for progress in user_progress:
            if progress.should_review() and progress.status != LessonStatus.MASTERED:
                return progress.lesson_id
        return None

    def _select_optimal_domain(self, user: UserProfile) -> str:
        """Select domain that needs most attention or is next logical step"""

        # If just starting, begin with fundamentals
        if not user.diagnostic_completed or user.skill_levels.fundamentals < 25:
            return "fundamentals"

        # Find weakest domain that has prerequisites met
        domains = [
            "fundamentals",
            "dfir",
            "malware",
            "active_directory",
            "pentest",
            "redteam",
            "blueteam",
        ]

        domain_scores = []
        for domain in domains:
            skill = getattr(user.skill_levels, domain)

            # Check prerequisites
            prereqs = self.domain_prerequisites.get(domain, [])
            prereqs_met = all(
                getattr(user.skill_levels, prereq) >= 30 for prereq in prereqs
            )

            if not prereqs_met:
                continue

            # Score: lower skill = higher priority
            score = 100 - skill
            domain_scores.append((domain, score))

        if not domain_scores:
            return "fundamentals"

        # Sort by score and return highest priority
        domain_scores.sort(key=lambda x: x[1], reverse=True)
        return domain_scores[0][0]

    def _get_target_difficulties(self, skill_level: int) -> List[int]:
        """Map skill level to appropriate lesson difficulties"""
        if skill_level < 25:
            return [1, 2]  # Beginner + some intermediate
        elif skill_level < 50:
            return [2, 3]  # Intermediate + some advanced
        elif skill_level < 75:
            return [3, 4]  # Advanced + expert
        else:
            return [4]  # Expert only

    def _filter_lessons(
        self,
        lessons: List[LessonMetadata],
        domain: str,
        difficulties: List[int],
        user_progress: List[LessonProgress],
    ) -> List[LessonMetadata]:
        """Filter lessons by domain, difficulty, and prerequisites"""

        completed_ids = {p.lesson_id for p in user_progress if p.status in [
            LessonStatus.COMPLETED, LessonStatus.MASTERED
        ]}

        candidates = []
        for lesson in lessons:
            # Must match domain
            if lesson.domain != domain:
                continue

            # Must match difficulty
            if lesson.difficulty not in difficulties:
                continue

            # Must not be completed (unless needs review)
            if lesson.lesson_id in completed_ids:
                continue

            # Must have prerequisites met
            if not all(prereq in completed_ids for prereq in lesson.prerequisites):
                continue

            candidates.append(lesson)

        return candidates

    def _score_and_select_lesson(
        self,
        candidates: List[LessonMetadata],
        user: UserProfile,
        user_progress: List[LessonProgress],
    ) -> Optional[LessonMetadata]:
        """Score lessons by multiple factors and select best match"""

        if not candidates:
            return None

        # Sort by order_index (curriculum sequence)
        candidates.sort(key=lambda x: x.order_index)

        # Return first in sequence (respects curriculum design)
        return candidates[0]

    def calculate_skill_update(
        self, current_skill: int, lesson_difficulty: int, score: int
    ) -> int:
        """Calculate new skill level after lesson completion"""

        # Base skill gain based on score
        if score >= 90:
            gain = 5
        elif score >= 80:
            gain = 3
        elif score >= 70:
            gain = 2
        elif score >= 60:
            gain = 1
        else:
            gain = 0  # No gain for failing scores

        # Adjust gain based on lesson difficulty
        gain *= lesson_difficulty

        # Diminishing returns at higher skill levels
        if current_skill >= 75:
            gain = int(gain * 0.5)
        elif current_skill >= 50:
            gain = int(gain * 0.75)

        new_skill = min(100, current_skill + gain)
        return new_skill

    def generate_diagnostic_assessment(
        self, num_questions: int = 20
    ) -> Dict[str, List[Dict]]:
        """
        Generate diagnostic assessment questions across all domains.
        Used for initial skill profiling.
        """

        domains = [
            "fundamentals",
            "dfir",
            "malware",
            "active_directory",
            "pentest",
            "redteam",
            "blueteam",
        ]

        # Distribute questions across domains and difficulties
        questions_per_domain = num_questions // len(domains)

        diagnostic = {}
        for domain in domains:
            domain_questions = []

            # Mix of difficulties
            difficulties = [1, 1, 2, 2, 3]  # More beginner/intermediate
            for diff in difficulties[:questions_per_domain]:
                domain_questions.append(
                    {
                        "domain": domain,
                        "difficulty": diff,
                        "question": f"[{domain.upper()}] Diagnostic question difficulty {diff}",
                        "type": "multiple_choice",
                    }
                )

            diagnostic[domain] = domain_questions

        return diagnostic

    def score_diagnostic(
        self, responses: Dict[str, List[bool]]
    ) -> SkillLevels:
        """
        Score diagnostic assessment and generate initial skill profile.

        Args:
            responses: Dict mapping domain -> list of correct/incorrect booleans

        Returns:
            SkillLevels object with initial proficiency estimates
        """

        skills = SkillLevels()

        for domain, answers in responses.items():
            if not answers:
                continue

            # Calculate percentage correct
            correct = sum(1 for a in answers if a)
            total = len(answers)
            percentage = (correct / total) * 100

            # Map to skill level (diagnostic is intentionally harder)
            # Scale up to account for diagnostic difficulty
            skill_estimate = min(100, int(percentage * 1.2))

            # Set skill level
            setattr(skills, domain, skill_estimate)

        return skills

    def should_interleave(self, user: UserProfile) -> bool:
        """Determine if learning should interleave domains (learning science)"""

        # Interleaving beneficial once past beginner stage
        avg_skill = user.skill_levels.get_overall_level()
        return avg_skill >= 30

    def calculate_learning_velocity(
        self, user_progress: List[LessonProgress]
    ) -> float:
        """
        Calculate user's learning velocity (lessons/day).
        Used for adaptive pacing recommendations.
        """

        if not user_progress:
            return 0.0

        completed = [
            p
            for p in user_progress
            if p.status in [LessonStatus.COMPLETED, LessonStatus.MASTERED]
        ]

        if not completed:
            return 0.0

        # Calculate days since first lesson
        earliest = min(p.started_at for p in completed if p.started_at)
        days = (datetime.now() - earliest).days + 1

        return len(completed) / days

    def recommend_study_schedule(
        self, user: UserProfile, velocity: float
    ) -> Dict[str, any]:
        """Generate personalized study schedule recommendation"""

        target_daily_minutes = user.learning_preferences.session_duration

        # Adaptive pacing based on velocity and skill
        if velocity < 0.5:
            # Slow pace - encourage consistency
            recommendation = {
                "sessions_per_week": 5,
                "minutes_per_session": target_daily_minutes,
                "focus": "Build momentum with daily practice",
            }
        elif velocity < 1.0:
            # Good pace - maintain
            recommendation = {
                "sessions_per_week": 6,
                "minutes_per_session": target_daily_minutes,
                "focus": "Maintain your excellent progress",
            }
        else:
            # Fast pace - suggest optimization
            recommendation = {
                "sessions_per_week": 7,
                "minutes_per_session": target_daily_minutes,
                "focus": "Challenge yourself with advanced content",
            }

        return recommendation
