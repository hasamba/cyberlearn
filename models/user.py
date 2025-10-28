"""
User data models for CyberLearn adaptive learning system.
Implements learner profiles with skill tracking and preferences.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class LearningPreferences(BaseModel):
    """User's learning style preferences"""
    visual_weight: float = Field(default=0.33, ge=0.0, le=1.0)
    auditory_weight: float = Field(default=0.33, ge=0.0, le=1.0)
    kinesthetic_weight: float = Field(default=0.34, ge=0.0, le=1.0)
    pace: str = Field(default="normal", pattern="^(slow|normal|fast)$")
    session_duration: int = Field(default=30, ge=15, le=60)  # minutes

    class Config:
        frozen = False


class SkillLevels(BaseModel):
    """Skill proficiency across cybersecurity domains (0-100 scale)"""
    fundamentals: int = Field(default=0, ge=0, le=100)
    dfir: int = Field(default=0, ge=0, le=100)
    malware: int = Field(default=0, ge=0, le=100)
    active_directory: int = Field(default=0, ge=0, le=100)
    system: int = Field(default=0, ge=0, le=100)
    linux: int = Field(default=0, ge=0, le=100)
    cloud: int = Field(default=0, ge=0, le=100)
    pentest: int = Field(default=0, ge=0, le=100)
    redteam: int = Field(default=0, ge=0, le=100)
    blueteam: int = Field(default=0, ge=0, le=100)

    def get_overall_level(self) -> int:
        """Calculate overall skill level across all domains"""
        skills = [
            self.fundamentals,
            self.dfir,
            self.malware,
            self.active_directory,
            self.system,
            self.linux,
            self.cloud,
            self.pentest,
            self.redteam,
            self.blueteam
        ]
        return sum(skills) // len(skills)

    def get_weakest_domain(self) -> str:
        """Identify domain needing most attention"""
        domain_map = {
            self.fundamentals: "fundamentals",
            self.dfir: "dfir",
            self.malware: "malware",
            self.active_directory: "active_directory",
            self.system: "system",
            self.linux: "linux",
            self.cloud: "cloud",
            self.pentest: "pentest",
            self.redteam: "redteam",
            self.blueteam: "blueteam"
        }
        return domain_map[min(domain_map.keys())]


class UserProfile(BaseModel):
    """Complete user profile with progress and gamification data"""
    user_id: UUID = Field(default_factory=uuid4)
    username: str = Field(min_length=3, max_length=50)
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: datetime = Field(default_factory=datetime.now)

    # Skill tracking
    skill_levels: SkillLevels = Field(default_factory=SkillLevels)

    # Gamification
    total_xp: int = Field(default=0, ge=0)
    level: int = Field(default=1, ge=1, le=100)
    streak_days: int = Field(default=0, ge=0)
    longest_streak: int = Field(default=0, ge=0)
    badges: List[str] = Field(default_factory=list)

    # Learning preferences
    learning_preferences: LearningPreferences = Field(default_factory=LearningPreferences)

    # Statistics
    total_lessons_completed: int = Field(default=0, ge=0)
    total_time_spent: int = Field(default=0, ge=0)  # seconds
    diagnostic_completed: bool = Field(default=False)

    def calculate_level(self) -> int:
        """Calculate user level based on total XP"""
        if self.total_xp < 1000:
            return 1
        elif self.total_xp < 3000:
            return 2
        elif self.total_xp < 7000:
            return 3
        elif self.total_xp < 15000:
            return 4
        elif self.total_xp < 30000:
            return 5
        else:
            return 6

    def get_level_name(self) -> str:
        """Get human-readable level name"""
        level_names = {
            1: "Apprentice",
            2: "Practitioner",
            3: "Specialist",
            4: "Expert",
            5: "Master",
            6: "Grandmaster"
        }
        return level_names.get(self.level, "Unknown")

    def get_xp_to_next_level(self) -> int:
        """Calculate XP needed for next level"""
        thresholds = [1000, 3000, 7000, 15000, 30000, 100000]
        current_threshold_index = self.level - 1
        if current_threshold_index >= len(thresholds):
            return 0  # Max level
        return thresholds[current_threshold_index] - self.total_xp

    def add_xp(self, xp: int, multiplier: float = 1.0) -> Dict:
        """Add XP with optional multiplier, return level-up info"""
        old_level = self.level
        earned = int(xp * multiplier)
        self.total_xp += earned
        self.level = self.calculate_level()

        return {
            "xp_earned": earned,
            "total_xp": self.total_xp,
            "level_up": self.level > old_level,
            "new_level": self.level,
            "level_name": self.get_level_name()
        }

    def add_badge(self, badge_name: str) -> bool:
        """Add badge if not already owned"""
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            return True
        return False

    def update_streak(self) -> Dict:
        """Update login streak, return streak info"""
        now = datetime.now()
        days_since_last = (now - self.last_login).days

        # Initialize streak for new users
        if self.streak_days == 0:
            self.streak_days = 1
            self.longest_streak = 1

        if days_since_last == 1:
            # Consecutive day
            self.streak_days += 1
            if self.streak_days > self.longest_streak:
                self.longest_streak = self.streak_days
        elif days_since_last > 1:
            # Streak broken
            self.streak_days = 1
        # Same day login doesn't affect streak

        self.last_login = now

        return {
            "current_streak": self.streak_days,
            "longest_streak": self.longest_streak,
            "streak_maintained": days_since_last <= 1
        }

    def get_skill_difficulty_preference(self, domain: str) -> List[int]:
        """Get appropriate difficulty levels for domain"""
        skill = getattr(self.skill_levels, domain, 0)

        if skill < 25:
            return [1, 2]  # Beginner
        elif skill < 50:
            return [2, 3]  # Intermediate
        elif skill < 75:
            return [3, 4]  # Advanced
        else:
            return [4]  # Expert

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
