"""
Progress tracking and retention models for CyberLearn.
Implements spaced repetition and mastery tracking.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum


class LessonStatus(str, Enum):
    """Lesson completion status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"
    NEEDS_REVIEW = "needs_review"


class RetentionCheck(BaseModel):
    """Spaced repetition check result"""
    check_id: UUID = Field(default_factory=uuid4)
    checked_at: datetime = Field(default_factory=datetime.now)
    score: int = Field(ge=0, le=100)
    questions_answered: int
    time_since_completion: int  # days

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class LessonProgress(BaseModel):
    """User progress on a specific lesson"""
    progress_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    lesson_id: UUID

    # Status
    status: LessonStatus = Field(default=LessonStatus.NOT_STARTED)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Performance metrics
    attempts: int = Field(default=0, ge=0)
    quiz_scores: List[int] = Field(default_factory=list)  # Each attempt score
    best_score: int = Field(default=0, ge=0, le=100)
    time_spent: int = Field(default=0, ge=0)  # total seconds

    # Spaced repetition
    retention_checks: List[RetentionCheck] = Field(default_factory=list)
    next_review_date: Optional[datetime] = None
    mastery_level: int = Field(default=0, ge=0, le=100)

    # Engagement
    interactive_blocks_completed: List[UUID] = Field(default_factory=list)
    reflection_submitted: bool = Field(default=False)
    notes: str = Field(default="")

    def start_lesson(self):
        """Mark lesson as started"""
        if self.status == LessonStatus.NOT_STARTED:
            self.status = LessonStatus.IN_PROGRESS
            self.started_at = datetime.now()
            self.attempts += 1

    def complete_lesson(self, score: int, time_seconds: int) -> Dict:
        """Mark lesson as completed, calculate next review"""
        # Increment attempts if this is a retake (completed_at already set)
        if self.completed_at is not None:
            self.attempts += 1

        self.status = LessonStatus.COMPLETED
        self.completed_at = datetime.now()
        self.quiz_scores.append(score)
        self.best_score = max(self.best_score, score)
        self.time_spent += time_seconds

        # Determine mastery
        if score >= 90 and self.attempts == 1:
            self.status = LessonStatus.MASTERED
            self.mastery_level = 100
        elif score >= 80:
            self.mastery_level = score

        # Schedule first retention check (spaced repetition)
        self.next_review_date = self._calculate_next_review()

        return {
            "completed": True,
            "status": self.status,
            "score": score,
            "mastered": self.status == LessonStatus.MASTERED,
            "next_review": self.next_review_date
        }

    def add_retention_check(self, score: int, questions: int) -> Dict:
        """Record a retention/review attempt"""
        check = RetentionCheck(
            score=score,
            questions_answered=questions,
            time_since_completion=(datetime.now() - self.completed_at).days
            if self.completed_at
            else 0,
        )
        self.retention_checks.append(check)

        # Update mastery based on retention
        if score >= 80:
            self.mastery_level = min(100, self.mastery_level + 5)
            if self.mastery_level >= 95:
                self.status = LessonStatus.MASTERED
        else:
            self.mastery_level = max(0, self.mastery_level - 10)
            self.status = LessonStatus.NEEDS_REVIEW

        # Schedule next review
        self.next_review_date = self._calculate_next_review()

        return {
            "retention_score": score,
            "mastery_level": self.mastery_level,
            "status": self.status,
            "next_review": self.next_review_date,
        }

    def _calculate_next_review(self) -> datetime:
        """Calculate next review date using spaced repetition algorithm"""
        if not self.completed_at:
            return datetime.now()

        num_checks = len(self.retention_checks)

        # Spaced repetition intervals (days)
        intervals = [1, 3, 7, 14, 30, 60, 90]

        # Adjust based on performance
        avg_retention = (
            sum(check.score for check in self.retention_checks[-3:])
            / min(3, len(self.retention_checks))
            if self.retention_checks
            else self.best_score
        )

        # High retention = longer intervals
        if avg_retention >= 90:
            multiplier = 1.5
        elif avg_retention >= 80:
            multiplier = 1.0
        else:
            multiplier = 0.5  # More frequent review if struggling

        interval_index = min(num_checks, len(intervals) - 1)
        days = int(intervals[interval_index] * multiplier)

        return datetime.now() + timedelta(days=days)

    def should_review(self) -> bool:
        """Check if lesson is due for review"""
        if not self.next_review_date:
            return False
        return datetime.now() >= self.next_review_date

    def get_average_score(self) -> float:
        """Calculate average quiz score"""
        return sum(self.quiz_scores) / len(self.quiz_scores) if self.quiz_scores else 0

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class DomainProgress(BaseModel):
    """Aggregate progress for entire domain"""
    user_id: UUID
    domain: str
    skill_level: int = Field(default=0, ge=0, le=100)
    lessons_completed: int = Field(default=0)
    lessons_mastered: int = Field(default=0)
    total_lessons: int = Field(default=0)
    total_xp_earned: int = Field(default=0)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def completion_percentage(self) -> float:
        """Calculate % of domain completed"""
        if self.total_lessons == 0:
            return 0.0
        return (self.lessons_completed / self.total_lessons) * 100

    def mastery_percentage(self) -> float:
        """Calculate % of domain mastered"""
        if self.total_lessons == 0:
            return 0.0
        return (self.lessons_mastered / self.total_lessons) * 100

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
