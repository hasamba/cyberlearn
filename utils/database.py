"""
Database management for CyberLearn.
Handles SQLite persistence for users, lessons, and progress tracking.
"""

import sqlite3
import json
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime
from pathlib import Path

from models.user import UserProfile, SkillLevels, LearningPreferences
from models.lesson import Lesson, LessonMetadata
from models.progress import LessonProgress, DomainProgress


class Database:
    """SQLite database manager for CyberLearn"""

    def __init__(self, db_path: str = "cyberlearn.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize_database()

    def _initialize_database(self):
        """Create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access

        cursor = self.conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                created_at TEXT NOT NULL,
                last_login TEXT NOT NULL,
                skill_levels TEXT NOT NULL,
                total_xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                streak_days INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                badges TEXT DEFAULT '[]',
                learning_preferences TEXT NOT NULL,
                total_lessons_completed INTEGER DEFAULT 0,
                total_time_spent INTEGER DEFAULT 0,
                diagnostic_completed INTEGER DEFAULT 0
            )
        """
        )

        # Lessons table (metadata + content)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                title TEXT NOT NULL,
                subtitle TEXT,
                difficulty INTEGER NOT NULL,
                estimated_time INTEGER NOT NULL,
                order_index INTEGER NOT NULL,
                prerequisites TEXT DEFAULT '[]',
                learning_objectives TEXT NOT NULL,
                content_blocks TEXT NOT NULL,
                pre_assessment TEXT,
                post_assessment TEXT NOT NULL,
                mastery_threshold INTEGER DEFAULT 80,
                jim_kwik_principles TEXT NOT NULL,
                base_xp_reward INTEGER DEFAULT 100,
                badge_unlock TEXT,
                is_core_concept INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                author TEXT,
                version TEXT DEFAULT '1.0'
            )
        """
        )

        # Progress table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                progress_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                status TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                attempts INTEGER DEFAULT 0,
                quiz_scores TEXT DEFAULT '[]',
                best_score INTEGER DEFAULT 0,
                time_spent INTEGER DEFAULT 0,
                retention_checks TEXT DEFAULT '[]',
                next_review_date TEXT,
                mastery_level INTEGER DEFAULT 0,
                interactive_blocks_completed TEXT DEFAULT '[]',
                reflection_submitted INTEGER DEFAULT 0,
                notes TEXT DEFAULT '',
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id),
                UNIQUE(user_id, lesson_id)
            )
        """
        )

        # Domain progress table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS domain_progress (
                user_id TEXT NOT NULL,
                domain TEXT NOT NULL,
                skill_level INTEGER DEFAULT 0,
                lessons_completed INTEGER DEFAULT 0,
                lessons_mastered INTEGER DEFAULT 0,
                total_lessons INTEGER DEFAULT 0,
                total_xp_earned INTEGER DEFAULT 0,
                started_at TEXT,
                completed_at TEXT,
                PRIMARY KEY (user_id, domain),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )

        # Create indexes
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_progress_lesson ON progress(lesson_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_lessons_domain ON lessons(domain)"
        )

        self.conn.commit()

    # USER OPERATIONS

    def create_user(self, user: UserProfile) -> bool:
        """Create new user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (
                    user_id, username, email, created_at, last_login,
                    skill_levels, total_xp, level, streak_days, longest_streak,
                    badges, learning_preferences, total_lessons_completed,
                    total_time_spent, diagnostic_completed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    str(user.user_id),
                    user.username,
                    user.email,
                    user.created_at.isoformat(),
                    user.last_login.isoformat(),
                    user.skill_levels.json(),
                    user.total_xp,
                    user.level,
                    user.streak_days,
                    user.longest_streak,
                    json.dumps(user.badges),
                    user.learning_preferences.json(),
                    user.total_lessons_completed,
                    user.total_time_spent,
                    int(user.diagnostic_completed),
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, user_id: UUID) -> Optional[UserProfile]:
        """Retrieve user by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
        row = cursor.fetchone()

        if not row:
            return None

        return self._row_to_user(row)

    def get_user_by_username(self, username: str) -> Optional[UserProfile]:
        """Retrieve user by username"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return None

        return self._row_to_user(row)

    def update_user(self, user: UserProfile) -> bool:
        """Update existing user"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE users SET
                email = ?, last_login = ?, skill_levels = ?, total_xp = ?,
                level = ?, streak_days = ?, longest_streak = ?, badges = ?,
                learning_preferences = ?, total_lessons_completed = ?,
                total_time_spent = ?, diagnostic_completed = ?
            WHERE user_id = ?
        """,
            (
                user.email,
                user.last_login.isoformat(),
                user.skill_levels.json(),
                user.total_xp,
                user.level,
                user.streak_days,
                user.longest_streak,
                json.dumps(user.badges),
                user.learning_preferences.json(),
                user.total_lessons_completed,
                user.total_time_spent,
                int(user.diagnostic_completed),
                str(user.user_id),
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def _row_to_user(self, row: sqlite3.Row) -> UserProfile:
        """Convert DB row to UserProfile"""
        return UserProfile(
            user_id=UUID(row["user_id"]),
            username=row["username"],
            email=row["email"],
            created_at=datetime.fromisoformat(row["created_at"]),
            last_login=datetime.fromisoformat(row["last_login"]),
            skill_levels=SkillLevels.parse_raw(row["skill_levels"]),
            total_xp=row["total_xp"],
            level=row["level"],
            streak_days=row["streak_days"],
            longest_streak=row["longest_streak"],
            badges=json.loads(row["badges"]),
            learning_preferences=LearningPreferences.parse_raw(
                row["learning_preferences"]
            ),
            total_lessons_completed=row["total_lessons_completed"],
            total_time_spent=row["total_time_spent"],
            diagnostic_completed=bool(row["diagnostic_completed"]),
        )

    # LESSON OPERATIONS

    def create_lesson(self, lesson: Lesson) -> bool:
        """Store lesson in database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO lessons (
                    lesson_id, domain, title, subtitle, difficulty, estimated_time,
                    order_index, prerequisites, learning_objectives, content_blocks,
                    pre_assessment, post_assessment, mastery_threshold,
                    jim_kwik_principles, base_xp_reward, badge_unlock, is_core_concept,
                    created_at, updated_at, author, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    str(lesson.lesson_id),
                    lesson.domain,
                    lesson.title,
                    lesson.subtitle,
                    lesson.difficulty,
                    lesson.estimated_time,
                    lesson.order_index,
                    json.dumps([str(p) for p in lesson.prerequisites]),
                    json.dumps(lesson.learning_objectives),
                    json.dumps([json.loads(block.model_dump_json()) for block in lesson.content_blocks]),
                    (
                        json.dumps([json.loads(q.model_dump_json()) for q in lesson.pre_assessment])
                        if lesson.pre_assessment
                        else None
                    ),
                    json.dumps([json.loads(q.model_dump_json()) for q in lesson.post_assessment]),
                    lesson.mastery_threshold,
                    json.dumps(lesson.jim_kwik_principles),
                    lesson.base_xp_reward,
                    lesson.badge_unlock,
                    int(lesson.is_core_concept),
                    lesson.created_at.isoformat(),
                    lesson.updated_at.isoformat(),
                    lesson.author,
                    lesson.version,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_lesson(self, lesson_id: UUID) -> Optional[Lesson]:
        """Retrieve full lesson by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM lessons WHERE lesson_id = ?", (str(lesson_id),))
        row = cursor.fetchone()

        if not row:
            return None

        # Parse JSON fields from database
        row_dict = dict(row)
        row_dict['prerequisites'] = json.loads(row_dict['prerequisites'])
        row_dict['learning_objectives'] = json.loads(row_dict['learning_objectives'])
        row_dict['content_blocks'] = json.loads(row_dict['content_blocks'])
        row_dict['post_assessment'] = json.loads(row_dict['post_assessment'])
        row_dict['jim_kwik_principles'] = json.loads(row_dict['jim_kwik_principles'])
        if row_dict['pre_assessment']:
            row_dict['pre_assessment'] = json.loads(row_dict['pre_assessment'])

        return Lesson(**row_dict)

    def get_lessons_by_domain(self, domain: str) -> List[LessonMetadata]:
        """Get all lesson metadata for a domain"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT lesson_id, domain, title, difficulty, estimated_time,
                   order_index, is_core_concept, prerequisites
            FROM lessons WHERE domain = ? ORDER BY order_index
        """,
            (domain,),
        )

        lessons = []
        for row in cursor.fetchall():
            # Parse prerequisites safely, filtering out invalid UUIDs
            prereqs_raw = json.loads(row["prerequisites"])
            prereqs = []
            for p in prereqs_raw:
                if p and isinstance(p, str):
                    try:
                        prereqs.append(UUID(p))
                    except (ValueError, AttributeError):
                        # Skip invalid UUIDs
                        continue

            lessons.append(
                LessonMetadata(
                    lesson_id=UUID(row["lesson_id"]),
                    domain=row["domain"],
                    title=row["title"],
                    difficulty=row["difficulty"],
                    estimated_time=row["estimated_time"],
                    order_index=row["order_index"],
                    is_core_concept=bool(row["is_core_concept"]),
                    prerequisites=prereqs,
                )
            )

        return lessons

    def get_all_lessons_metadata(self) -> List[LessonMetadata]:
        """Get metadata for all lessons"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT lesson_id, domain, title, difficulty, estimated_time,
                   order_index, is_core_concept, prerequisites
            FROM lessons ORDER BY domain, order_index
        """
        )

        lessons = []
        for row in cursor.fetchall():
            # Parse prerequisites safely, filtering out invalid UUIDs
            prereqs_raw = json.loads(row["prerequisites"])
            prereqs = []
            for p in prereqs_raw:
                if p and isinstance(p, str):
                    try:
                        prereqs.append(UUID(p))
                    except (ValueError, AttributeError):
                        # Skip invalid UUIDs
                        continue

            lessons.append(
                LessonMetadata(
                    lesson_id=UUID(row["lesson_id"]),
                    domain=row["domain"],
                    title=row["title"],
                    difficulty=row["difficulty"],
                    estimated_time=row["estimated_time"],
                    order_index=row["order_index"],
                    is_core_concept=bool(row["is_core_concept"]),
                    prerequisites=prereqs,
                )
            )

        return lessons

    # PROGRESS OPERATIONS

    def create_progress(self, progress: LessonProgress) -> bool:
        """Create progress record"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO progress (
                    progress_id, user_id, lesson_id, status, started_at, completed_at,
                    attempts, quiz_scores, best_score, time_spent, retention_checks,
                    next_review_date, mastery_level, interactive_blocks_completed,
                    reflection_submitted, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    str(progress.progress_id),
                    str(progress.user_id),
                    str(progress.lesson_id),
                    progress.status,
                    progress.started_at.isoformat() if progress.started_at else None,
                    (
                        progress.completed_at.isoformat()
                        if progress.completed_at
                        else None
                    ),
                    progress.attempts,
                    json.dumps(progress.quiz_scores),
                    progress.best_score,
                    progress.time_spent,
                    json.dumps([c.dict() for c in progress.retention_checks]),
                    (
                        progress.next_review_date.isoformat()
                        if progress.next_review_date
                        else None
                    ),
                    progress.mastery_level,
                    json.dumps([str(b) for b in progress.interactive_blocks_completed]),
                    int(progress.reflection_submitted),
                    progress.notes,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_progress(self, progress: LessonProgress) -> bool:
        """Update progress record"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE progress SET
                status = ?, started_at = ?, completed_at = ?, attempts = ?,
                quiz_scores = ?, best_score = ?, time_spent = ?, retention_checks = ?,
                next_review_date = ?, mastery_level = ?, interactive_blocks_completed = ?,
                reflection_submitted = ?, notes = ?
            WHERE progress_id = ?
        """,
            (
                progress.status,
                progress.started_at.isoformat() if progress.started_at else None,
                progress.completed_at.isoformat() if progress.completed_at else None,
                progress.attempts,
                json.dumps(progress.quiz_scores),
                progress.best_score,
                progress.time_spent,
                json.dumps([c.dict() for c in progress.retention_checks]),
                (
                    progress.next_review_date.isoformat()
                    if progress.next_review_date
                    else None
                ),
                progress.mastery_level,
                json.dumps([str(b) for b in progress.interactive_blocks_completed]),
                int(progress.reflection_submitted),
                progress.notes,
                str(progress.progress_id),
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def get_user_progress(self, user_id: UUID) -> List[LessonProgress]:
        """Get all progress records for user"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM progress WHERE user_id = ?", (str(user_id),))

        progress_list = []
        for row in cursor.fetchall():
            progress_list.append(self._row_to_progress(row))

        return progress_list

    def get_lesson_progress(
        self, user_id: UUID, lesson_id: UUID
    ) -> Optional[LessonProgress]:
        """Get progress for specific lesson"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM progress WHERE user_id = ? AND lesson_id = ?",
            (str(user_id), str(lesson_id)),
        )
        row = cursor.fetchone()

        if not row:
            return None

        return self._row_to_progress(row)

    def _row_to_progress(self, row: sqlite3.Row) -> LessonProgress:
        """Convert DB row to LessonProgress"""
        data = dict(row)

        def parse_datetime(value):
            return datetime.fromisoformat(value) if value else None

        data["progress_id"] = UUID(data["progress_id"])
        data["user_id"] = UUID(data["user_id"])
        data["lesson_id"] = UUID(data["lesson_id"])

        data["started_at"] = parse_datetime(data.get("started_at"))
        data["completed_at"] = parse_datetime(data.get("completed_at"))
        data["next_review_date"] = parse_datetime(data.get("next_review_date"))

        quiz_scores = data.get("quiz_scores")
        data["quiz_scores"] = json.loads(quiz_scores) if quiz_scores else []

        retention_raw = data.get("retention_checks")
        data["retention_checks"] = (
            json.loads(retention_raw) if retention_raw else []
        )

        interactive_raw = data.get("interactive_blocks_completed")
        interactive_ids = json.loads(interactive_raw) if interactive_raw else []
        data["interactive_blocks_completed"] = [
            UUID(val) for val in interactive_ids if val
        ]

        data["reflection_submitted"] = bool(data.get("reflection_submitted"))

        return LessonProgress.model_validate(data)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
