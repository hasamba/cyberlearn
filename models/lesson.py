"""
Lesson and content models for CyberLearn.
Implements structured learning content with Jim Kwik principles.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum


class ContentType(str, Enum):
    """Types of content blocks in lessons"""
    EXPLANATION = "explanation"
    VIDEO = "video"
    DIAGRAM = "diagram"
    QUIZ = "quiz"
    SIMULATION = "simulation"
    REFLECTION = "reflection"
    MEMORY_AID = "memory_aid"
    REAL_WORLD = "real_world"
    CODE_EXERCISE = "code_exercise"
    MINDSET_COACH = "mindset_coach"


class JimKwikPrinciple(str, Enum):
    """Jim Kwik accelerated learning principles"""
    ACTIVE_LEARNING = "active_learning"
    MINIMUM_EFFECTIVE_DOSE = "minimum_effective_dose"
    TEACH_LIKE_IM_10 = "teach_like_im_10"
    MEMORY_HOOKS = "memory_hooks"
    META_LEARNING = "meta_learning"
    CONNECT_TO_WHAT_I_KNOW = "connect_to_what_i_know"
    REFRAME_LIMITING_BELIEFS = "reframe_limiting_beliefs"
    GAMIFY_IT = "gamify_it"
    LEARNING_SPRINT = "learning_sprint"
    MULTIPLE_MEMORY_PATHWAYS = "multiple_memory_pathways"


class QuestionType(str, Enum):
    """Assessment question types"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SCENARIO = "scenario"
    CODE_REVIEW = "code_review"
    FREE_RESPONSE = "free_response"


class Question(BaseModel):
    """Individual assessment question"""
    question_id: str  # Simple string ID like "q1", "q2", etc.
    type: QuestionType
    question: str
    options: Optional[List[str]] = None  # For multiple choice
    correct_answer: Any  # String, int index, or list for multiple correct
    explanation: str  # Why this is the correct answer
    difficulty: int = Field(ge=1, le=4)
    memory_aid: Optional[str] = None  # Reinforcement mnemonic
    points: int = Field(default=10)

    class Config:
        use_enum_values = True


class ContentBlock(BaseModel):
    """Individual content block within a lesson"""
    block_id: UUID = Field(default_factory=uuid4)
    type: ContentType
    title: Optional[str] = None
    content: Dict[str, Any]  # Flexible structure based on type

    # Jim Kwik principle integrations
    simplified_explanation: Optional[str] = None  # Teach Like I'm 10
    memory_aids: List[str] = Field(default_factory=list)  # Memory Hooks
    real_world_connection: Optional[str] = None  # Connect to What I Know
    reflection_prompt: Optional[str] = None  # Meta-Learning
    mindset_message: Optional[str] = None  # Reframe Limiting Beliefs

    # For interactive components
    is_interactive: bool = Field(default=False)
    xp_reward: int = Field(default=0)

    class Config:
        use_enum_values = True
        json_encoders = {
            UUID: lambda v: str(v)
        }


class Lesson(BaseModel):
    """Complete lesson module"""
    lesson_id: UUID = Field(default_factory=uuid4)
    domain: str  # fundamentals, dfir, malware, etc.
    title: str
    subtitle: Optional[str] = None
    difficulty: int = Field(ge=1, le=4)  # 1=Beginner, 4=Expert
    estimated_time: int = Field(ge=5, le=60)  # minutes

    # Curriculum structure
    order_index: int = Field(ge=0)  # Sequence in domain
    prerequisites: List[str] = Field(default_factory=list)  # Changed from List[UUID] to List[str] for lesson title references
    learning_objectives: List[str] = Field(min_items=1)

    # Content
    content_blocks: List[ContentBlock] = Field(min_items=1)

    # Assessment
    pre_assessment: Optional[List[Question]] = None  # Diagnostic
    post_assessment: List[Question] = Field(min_items=1)
    mastery_threshold: int = Field(default=80, ge=0, le=100)  # % to pass

    # Jim Kwik principles applied in this lesson
    jim_kwik_principles: List[JimKwikPrinciple] = Field(min_items=1)

    # Gamification
    base_xp_reward: int = Field(default=100)
    badge_unlock: Optional[str] = None  # Badge awarded on completion
    is_core_concept: bool = Field(default=False)  # Minimum Effective Dose

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: Optional[str] = None
    version: str = Field(default="1.0")

    def get_difficulty_name(self) -> str:
        """Human-readable difficulty"""
        return {1: "Beginner", 2: "Intermediate", 3: "Advanced", 4: "Expert"}.get(
            self.difficulty, "Unknown"
        )

    def calculate_xp(self, score: int, time_spent: int, streak: int = 0) -> int:
        """Calculate XP with bonuses"""
        base = self.base_xp_reward

        # Score multiplier
        if score >= 100:
            base *= 1.5  # Perfect score bonus
        elif score >= 90:
            base *= 1.2

        # Speed bonus (if under estimated time)
        if time_spent < self.estimated_time * 60:
            base *= 1.2

        # Streak bonus
        streak_multiplier = min(1 + (streak * 0.1), 2.0)
        base *= streak_multiplier

        return int(base)

    def get_interactive_blocks(self) -> List[ContentBlock]:
        """Get all interactive components"""
        return [block for block in self.content_blocks if block.is_interactive]

    def get_memory_aids(self) -> List[str]:
        """Compile all memory aids from lesson"""
        aids = []
        for block in self.content_blocks:
            aids.extend(block.memory_aids)
        return aids

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class LessonMetadata(BaseModel):
    """Lightweight lesson metadata for listing/filtering"""
    lesson_id: UUID
    domain: str
    title: str
    difficulty: int
    estimated_time: int
    order_index: int
    is_core_concept: bool
    prerequisites: List[UUID]

    class Config:
        json_encoders = {UUID: lambda v: str(v)}
