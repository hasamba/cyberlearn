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
from models.tag import Tag, LessonTag, TagCreate, TagUpdate, TagFilter


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
                diagnostic_completed INTEGER DEFAULT 0,
                last_username TEXT,
                preferred_tag_filters TEXT DEFAULT '[]',
                last_active_lesson_id TEXT,
                last_active_at TEXT
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

        # Tags table (for organizing and filtering lessons)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tags (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                color TEXT NOT NULL,
                icon TEXT,
                is_system INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                user_id TEXT
            )
        """
        )

        # Lesson tags junction table (many-to-many relationship)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lesson_tags (
                lesson_id TEXT NOT NULL,
                tag_id TEXT NOT NULL,
                added_at TEXT NOT NULL,
                PRIMARY KEY (lesson_id, tag_id),
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        """
        )

        # Notes table (for user notes on lessons)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                note_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                content TEXT NOT NULL,
                images TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE
            )
        """
        )

        # Lesson notes table (enhanced notes with block-level granularity)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lesson_notes (
                note_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                content_block_index INTEGER,
                note_text TEXT,
                note_type TEXT DEFAULT 'text',
                attachments TEXT DEFAULT '[]',
                is_pinned INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE
            )
        """
        )

        # Assessment questions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS assessment_questions (
                question_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                question_text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer INTEGER NOT NULL,
                difficulty INTEGER NOT NULL,
                explanation TEXT,
                created_at TEXT NOT NULL
            )
        """
        )

        # User assessments table (stores completed assessment results)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_assessments (
                assessment_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                assessment_date TEXT NOT NULL,
                domain_scores TEXT NOT NULL,
                total_score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
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
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_lesson_tags_lesson ON lesson_tags(lesson_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_lesson_tags_tag ON lesson_tags(tag_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_notes_lesson ON notes(lesson_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_lesson_notes_user ON lesson_notes(user_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_lesson_notes_lesson ON lesson_notes(lesson_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_assessment_questions_domain ON assessment_questions(domain)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_user_assessments_user ON user_assessments(user_id)"
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

        # Check if new columns exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        has_new_columns = 'last_username' in columns and 'preferred_tag_filters' in columns
        has_last_active = 'last_active_lesson_id' in columns and 'last_active_at' in columns

        if has_new_columns and has_last_active:
            # Use new query with all fields including last_active
            cursor.execute(
                """
                UPDATE users SET
                    email = ?, last_login = ?, skill_levels = ?, total_xp = ?,
                    level = ?, streak_days = ?, longest_streak = ?, badges = ?,
                    learning_preferences = ?, total_lessons_completed = ?,
                    total_time_spent = ?, diagnostic_completed = ?,
                    last_username = ?, preferred_tag_filters = ?,
                    last_active_lesson_id = ?, last_active_at = ?
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
                    user.last_username,
                    json.dumps(user.preferred_tag_filters),
                    str(user.last_active_lesson_id) if user.last_active_lesson_id else None,
                    user.last_active_at.isoformat() if user.last_active_at else None,
                    str(user.user_id),
                ),
            )
        elif has_new_columns:
            # Use query with last_username and preferred_tag_filters but not last_active
            cursor.execute(
                """
                UPDATE users SET
                    email = ?, last_login = ?, skill_levels = ?, total_xp = ?,
                    level = ?, streak_days = ?, longest_streak = ?, badges = ?,
                    learning_preferences = ?, total_lessons_completed = ?,
                    total_time_spent = ?, diagnostic_completed = ?,
                    last_username = ?, preferred_tag_filters = ?
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
                    user.last_username,
                    json.dumps(user.preferred_tag_filters),
                    str(user.user_id),
                ),
            )
        else:
            # Use old query without new fields (backward compatible)
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
        # Handle optional fields (may not exist before migration)
        try:
            last_username = row["last_username"]
        except (IndexError, KeyError):
            last_username = None

        try:
            preferred_tag_filters = json.loads(row["preferred_tag_filters"])
        except (IndexError, KeyError):
            preferred_tag_filters = []

        try:
            last_active_lesson_id = UUID(row["last_active_lesson_id"]) if row["last_active_lesson_id"] else None
        except (IndexError, KeyError, ValueError):
            last_active_lesson_id = None

        try:
            last_active_at = datetime.fromisoformat(row["last_active_at"]) if row["last_active_at"] else None
        except (IndexError, KeyError, ValueError):
            last_active_at = None

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
            last_username=last_username,
            preferred_tag_filters=preferred_tag_filters,
            last_active_lesson_id=last_active_lesson_id,
            last_active_at=last_active_at,
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

    def get_lessons_by_domain(self, domain: str, include_hidden: bool = False) -> List[LessonMetadata]:
        """Get all lesson metadata for a domain (excludes hidden by default)"""
        cursor = self.conn.cursor()

        # Check if hidden column exists
        cursor.execute("PRAGMA table_info(lessons)")
        columns = [row[1] for row in cursor.fetchall()]
        has_hidden = 'hidden' in columns

        if has_hidden and not include_hidden:
            cursor.execute(
                """
                SELECT lesson_id, domain, title, difficulty, estimated_time,
                       order_index, is_core_concept, prerequisites
                FROM lessons WHERE domain = ? AND (hidden = 0 OR hidden IS NULL)
                ORDER BY order_index
            """,
                (domain,),
            )
        else:
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

    def get_lesson_stats_by_domain(self, user_id: Optional[UUID] = None) -> Dict[str, Dict]:
        """
        Get lesson statistics by domain.
        Returns dict with domain as key and stats as value:
        {
            'domain_name': {
                'total': int,  # Total lessons in domain
                'completed': int,  # Completed by user (if user_id provided)
                'in_progress': int,  # In progress by user (if user_id provided)
                'not_started': int  # Not started by user (if user_id provided)
            }
        }
        """
        cursor = self.conn.cursor()

        # Get total lessons per domain
        cursor.execute("""
            SELECT domain, COUNT(*) as total
            FROM lessons
            GROUP BY domain
            ORDER BY domain
        """)

        stats = {}
        for row in cursor.fetchall():
            domain = row['domain']
            stats[domain] = {
                'total': row['total'],
                'completed': 0,
                'in_progress': 0,
                'not_started': 0
            }

        # If user_id provided, get completion stats
        if user_id:
            # Completed lessons
            cursor.execute("""
                SELECT l.domain, COUNT(*) as count
                FROM lessons l
                JOIN progress p ON l.lesson_id = p.lesson_id
                WHERE p.user_id = ? AND p.status IN ('completed', 'mastered')
                GROUP BY l.domain
            """, (str(user_id),))

            for row in cursor.fetchall():
                if row['domain'] in stats:
                    stats[row['domain']]['completed'] = row['count']

            # In progress lessons
            cursor.execute("""
                SELECT l.domain, COUNT(*) as count
                FROM lessons l
                JOIN progress p ON l.lesson_id = p.lesson_id
                WHERE p.user_id = ? AND p.status = 'in_progress'
                GROUP BY l.domain
            """, (str(user_id),))

            for row in cursor.fetchall():
                if row['domain'] in stats:
                    stats[row['domain']]['in_progress'] = row['count']

            # Calculate not_started
            for domain in stats:
                stats[domain]['not_started'] = (
                    stats[domain]['total']
                    - stats[domain]['completed']
                    - stats[domain]['in_progress']
                )

        return stats

    def get_total_lesson_count(self) -> int:
        """Get total number of lessons in database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM lessons")
        return cursor.fetchone()['count']

    # TAG OPERATIONS

    def create_tag(self, tag: Tag) -> bool:
        """Create a new tag"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO tags (id, name, category, color, icon, description, created_at, is_system, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tag.tag_id,
                    tag.name,
                    tag.category,
                    tag.color,
                    tag.icon,
                    tag.description,
                    tag.created_at.isoformat(),
                    int(tag.is_system),
                    tag.user_id
                )
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """Get tag by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tags WHERE id = ?", (tag_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return Tag(
            tag_id=row['id'],
            name=row['name'],
            category=row['category'],
            color=row['color'],
            icon=row['icon'],
            description=row['description'],
            created_at=datetime.fromisoformat(row['created_at']),
            is_system=bool(row['is_system']),
            user_id=row['user_id'] if 'user_id' in row.keys() else None
        )

    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tags WHERE name = ?", (name,))
        row = cursor.fetchone()

        if not row:
            return None

        return Tag(
            tag_id=row['id'],
            name=row['name'],
            category=row['category'],
            color=row['color'],
            icon=row['icon'],
            description=row['description'],
            created_at=datetime.fromisoformat(row['created_at']),
            is_system=bool(row['is_system']),
            user_id=row['user_id'] if 'user_id' in row.keys() else None
        )

    def get_all_tags(self) -> List[Tag]:
        """Get all tags"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tags ORDER BY name")

        tags = []
        for row in cursor.fetchall():
            tags.append(Tag(
                tag_id=row['id'],
                name=row['name'],
                category=row['category'],
                color=row['color'],
                icon=row['icon'],
                description=row['description'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_system=bool(row['is_system']),
                user_id=row['user_id'] if 'user_id' in row.keys() else None
            ))

        return tags

    def get_user_tags(self, user_id: str) -> List[Tag]:
        """
        Get tags visible to user:
        - Tags created by this user (user_id = current user)
        - All system tags (is_system = 1)
        - Excludes auto-generated tags that have no user_id and aren't system
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM tags
            WHERE user_id = ? OR is_system = 1
            ORDER BY
                CASE category
                    WHEN 'Career Path' THEN 1
                    WHEN 'Course' THEN 2
                    WHEN 'Package' THEN 3
                    ELSE 4
                END,
                name
        """, (user_id,))

        tags = []
        for row in cursor.fetchall():
            tags.append(Tag(
                tag_id=row['id'],
                name=row['name'],
                category=row['category'],
                color=row['color'],
                icon=row['icon'],
                description=row['description'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_system=bool(row['is_system']),
                user_id=row['user_id'] if 'user_id' in row.keys() else None
            ))

        return tags

    def get_filterable_tags(self, user_id: str) -> List[Tag]:
        """
        Get tags for filtering lessons:
        - Career Path tags (for filtering by role)
        - Course tags (for filtering by course)
        - Package tags (for filtering by tool package)
        - User-created custom tags only
        - Excludes: System-generated Custom tags, Content category system tags
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM tags
            WHERE user_id = ?
            OR (is_system = 1 AND category IN ('Career Path', 'Course', 'Package'))
            ORDER BY
                CASE category
                    WHEN 'Career Path' THEN 1
                    WHEN 'Course' THEN 2
                    WHEN 'Package' THEN 3
                    ELSE 4
                END,
                name
        """, (user_id,))

        tags = []
        for row in cursor.fetchall():
            tags.append(Tag(
                tag_id=row['id'],
                name=row['name'],
                category=row['category'],
                color=row['color'],
                icon=row['icon'],
                description=row['description'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_system=bool(row['is_system']),
                user_id=row['user_id'] if 'user_id' in row.keys() else None
            ))

        return tags

    def update_tag(self, tag_id: str, update: TagUpdate) -> bool:
        """Update tag fields"""
        cursor = self.conn.cursor()

        # Build dynamic UPDATE query based on provided fields
        fields = []
        values = []

        if update.name is not None:
            fields.append("name = ?")
            values.append(update.name)
        if update.color is not None:
            fields.append("color = ?")
            values.append(update.color)
        if update.icon is not None:
            fields.append("icon = ?")
            values.append(update.icon)
        if update.description is not None:
            fields.append("description = ?")
            values.append(update.description)

        if not fields:
            return False

        values.append(tag_id)
        query = f"UPDATE tags SET {', '.join(fields)} WHERE tag_id = ?"

        cursor.execute(query, values)
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_tag(self, tag_id: str) -> bool:
        """
        Delete tag (only if not system tag).
        Cascade deletes lesson_tags associations.
        """
        cursor = self.conn.cursor()

        # Check if system tag
        cursor.execute("SELECT is_system FROM tags WHERE tag_id = ?", (tag_id,))
        row = cursor.fetchone()

        if not row:
            return False

        if row['is_system']:
            raise ValueError("Cannot delete system tags")

        # Delete tag (cascade handles lesson_tags)
        cursor.execute("DELETE FROM tags WHERE tag_id = ?", (tag_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_tag_to_lesson(self, lesson_id: str, tag_id: str) -> bool:
        """Add tag to lesson (many-to-many)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                VALUES (?, ?, ?)
                """,
                (lesson_id, tag_id, datetime.utcnow().isoformat())
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Already tagged
            return False

    def remove_tag_from_lesson(self, lesson_id: str, tag_id: str) -> bool:
        """Remove tag from lesson"""
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM lesson_tags WHERE lesson_id = ? AND tag_id = ?",
            (lesson_id, tag_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def get_lesson_tags(self, lesson_id: str) -> List[Tag]:
        """Get all tags for a lesson"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT t.* FROM tags t
            JOIN lesson_tags lt ON t.id = lt.tag_id
            WHERE lt.lesson_id = ?
            ORDER BY t.name
            """,
            (lesson_id,)
        )

        tags = []
        for row in cursor.fetchall():
            tags.append(Tag(
                tag_id=row['id'],
                name=row['name'],
                category=row['category'],
                color=row['color'],
                icon=row['icon'],
                description=row['description'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_system=bool(row['is_system'])
            ))

        return tags

    def get_lessons_by_tags(self, tag_filter: TagFilter) -> List[LessonMetadata]:
        """
        Get lessons filtered by tags.

        If match_all=True: lesson must have ALL specified tags
        If match_all=False: lesson must have ANY of the specified tags
        """
        if not tag_filter.tag_ids:
            return self.get_all_lessons_metadata()

        cursor = self.conn.cursor()

        if tag_filter.match_all:
            # Lesson must have ALL tags
            placeholders = ','.join(['?' for _ in tag_filter.tag_ids])
            query = f"""
                SELECT DISTINCT l.lesson_id, l.domain, l.title, l.difficulty,
                       l.estimated_time, l.order_index, l.is_core_concept, l.prerequisites
                FROM lessons l
                JOIN lesson_tags lt ON l.lesson_id = lt.lesson_id
                WHERE lt.tag_id IN ({placeholders})
                GROUP BY l.lesson_id
                HAVING COUNT(DISTINCT lt.tag_id) = ?
                ORDER BY l.domain, l.order_index
            """
            cursor.execute(query, tag_filter.tag_ids + [len(tag_filter.tag_ids)])
        else:
            # Lesson must have ANY tag
            placeholders = ','.join(['?' for _ in tag_filter.tag_ids])
            query = f"""
                SELECT DISTINCT l.lesson_id, l.domain, l.title, l.difficulty,
                       l.estimated_time, l.order_index, l.is_core_concept, l.prerequisites
                FROM lessons l
                JOIN lesson_tags lt ON l.lesson_id = lt.lesson_id
                WHERE lt.tag_id IN ({placeholders})
                ORDER BY l.domain, l.order_index
            """
            cursor.execute(query, tag_filter.tag_ids)

        lessons = []
        for row in cursor.fetchall():
            # Parse prerequisites safely
            prereqs_raw = json.loads(row["prerequisites"])
            prereqs = []
            for p in prereqs_raw:
                if p and isinstance(p, str):
                    try:
                        prereqs.append(UUID(p))
                    except (ValueError, AttributeError):
                        continue

            # Get tags for this lesson
            lesson_tags = self.get_lesson_tags(row["lesson_id"])
            tag_ids = [tag.tag_id for tag in lesson_tags]

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
                    tags=tag_ids
                )
            )

        return lessons

    def get_tag_stats(self) -> Dict[str, int]:
        """Get statistics about tag usage"""
        cursor = self.conn.cursor()

        stats = {}

        # Lesson count per tag
        cursor.execute("""
            SELECT t.name, COUNT(lt.lesson_id) as lesson_count
            FROM tags t
            LEFT JOIN lesson_tags lt ON t.id = lt.tag_id
            GROUP BY t.id, t.name
            ORDER BY lesson_count DESC
        """)

        for row in cursor.fetchall():
            stats[row['name']] = row['lesson_count']

        return stats

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
