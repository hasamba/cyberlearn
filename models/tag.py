"""
Tag model for lesson organization and filtering.

Tags provide a many-to-many relationship allowing lessons to be categorized
into multiple groups (e.g., "Built-In" + "PWK Course" + "Advanced").
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class Tag(BaseModel):
    """
    A tag for organizing and filtering lessons.

    Lessons can have multiple tags, allowing flexible categorization:
    - System tags (built-in, advanced, certification prep)
    - Course-specific tags (PWK, SANS)
    - Tool-specific tags (Eric Zimmerman)
    - User-created tags
    """

    tag_id: str = Field(..., description="Unique identifier (UUID)")
    name: str = Field(..., min_length=1, max_length=100, description="Display name")
    color: str = Field(..., description="Hex color code (e.g., #3B82F6)")
    icon: Optional[str] = Field(None, description="Emoji icon (e.g., 🔵)")
    description: Optional[str] = Field(None, description="Tag description")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_system: bool = Field(default=False, description="System-managed tag (cannot be deleted)")

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Ensure color is a valid hex code."""
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError(f"Invalid hex color code: {v}. Must be format #RRGGBB")
        return v.upper()

    @field_validator("icon")
    @classmethod
    def validate_icon(cls, v: Optional[str]) -> Optional[str]:
        """Ensure icon is a single emoji or None."""
        if v and len(v) > 4:  # Allow up to 4 chars for multi-byte emojis
            raise ValueError(f"Icon must be a single emoji, got: {v}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "tag_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                "name": "PWK Course",
                "color": "#EF4444",
                "icon": "🔴",
                "description": "Offensive Security PWK/OSCP course aligned lessons",
                "created_at": "2025-10-29T12:00:00",
                "is_system": True
            }
        }


class LessonTag(BaseModel):
    """
    Junction model representing many-to-many relationship between lessons and tags.
    """

    lesson_id: str = Field(..., description="Lesson UUID")
    tag_id: str = Field(..., description="Tag UUID")
    added_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "lesson_id": "f1e2d3c4-b5a6-4987-8c7b-6a5b4c3d2e1f",
                "tag_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                "added_at": "2025-10-29T12:00:00"
            }
        }


class TagCreate(BaseModel):
    """Model for creating new tags."""

    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(..., description="Hex color code (e.g., #3B82F6)")
    icon: Optional[str] = Field(None, description="Emoji icon")
    description: Optional[str] = None
    is_system: bool = Field(default=False)

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Ensure color is a valid hex code."""
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError(f"Invalid hex color code: {v}")
        return v.upper()


class TagUpdate(BaseModel):
    """Model for updating existing tags."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, description="Hex color code")
    icon: Optional[str] = Field(None, description="Emoji icon")
    description: Optional[str] = None

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        """Ensure color is a valid hex code if provided."""
        if v and not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError(f"Invalid hex color code: {v}")
        return v.upper() if v else v


class TagFilter(BaseModel):
    """Model for filtering lessons by tags."""

    tag_ids: list[str] = Field(default_factory=list, description="List of tag IDs to filter by")
    match_all: bool = Field(default=False, description="If True, lesson must have ALL tags. If False, ANY tag matches")

    class Config:
        json_schema_extra = {
            "example": {
                "tag_ids": ["tag1-uuid", "tag2-uuid"],
                "match_all": False
            }
        }
